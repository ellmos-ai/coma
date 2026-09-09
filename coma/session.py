"""Provider-neutrale Sitzungsplanung, Sonde und Fallback-Kette.

Die bestehenden Adapter bilden weiterhin den unbeaufsichtigten Jobpfad
``IN/OUT/DONE`` ab. Dieses Modul ergaenzt daneben den zweiten, bewusst
prozessfreien Vertrag: ein Konsument kann eine interaktive oder headless
Sitzung planen, die argv pruefen und erst danach selbst ueber den passenden
Prozesshost starten.

Die Flags wurden am 2026-09-09 gegen die lokal installierten Hilfen geprueft:
Claude Code 2.1.263, Codex CLI 0.153.4, agy 1.1.27 und Kimi 0.31.0. Kimi bleibt
fail-closed, weil nur seine Hilfe, nicht ein echter Promptlauf verifiziert ist.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

from .adapters import AdapterError

PROVIDERS: tuple[str, ...] = ("claude", "codex", "agy", "kimi")
SESSION_MODES: tuple[str, ...] = ("interactive", "headless")
PROBE_TOKEN = "COMA_SESSION_PROBE_OK"
PROBE_REQUEST = f"Reply with exactly {PROBE_TOKEN} and nothing else."
DEFAULT_PROBE_TIMEOUT = 120.0


@dataclass(frozen=True)
class ProviderCapability:
    """Belegte Eigenschaften einer CLI, ohne einen Verfuegbarkeitsclaim."""

    provider: str
    instruction_file: str
    verified: bool
    help_version: str
    supports_interactive: bool = True
    supports_headless: bool = True
    supports_effort: bool = True
    notes: tuple[str, ...] = ()


CAPABILITIES: Mapping[str, ProviderCapability] = {
    "claude": ProviderCapability(
        "claude", "CLAUDE.md", True, "Claude Code 2.1.263",
        notes=("--append-system-prompt-file, --effort und --name belegt",),
    ),
    "codex": ProviderCapability(
        "codex", "AGENTS.md", True, "Codex CLI 0.153.4",
        notes=("interaktiv ohne Subcommand; headless ueber exec",),
    ),
    "agy": ProviderCapability(
        "agy", "GEMINI.md", True, "agy 1.1.27",
        notes=("interaktiv ueber --prompt-interactive; headless ueber -p",),
    ),
    "kimi": ProviderCapability(
        "kimi", "AGENTS.md", False, "Kimi 0.31.0",
        supports_effort=False,
        notes=(
            "kein interaktiver positionaler Startprompt; Boot mit -p, danach --continue",
            "nur Hilfe geprueft; echter Promptlauf bleibt unverified",
        ),
    ),
}


@dataclass(frozen=True)
class Candidate:
    """Ein geordneter Anbieter-/Modell-/Effort-Versuch."""

    provider: str
    model: str = ""
    effort: str = ""


@dataclass(frozen=True)
class SessionPlan:
    """Vollstaendige argv einer Sitzung, ohne sie zu starten."""

    provider: str
    mode: str
    commands: tuple[tuple[str, ...], ...]
    prompt_file: Path
    cwd: Path
    executable: str
    verified: bool
    capability: ProviderCapability

    @property
    def command(self) -> list[str]:
        """Erstes Kommando fuer Ein-Schritt-Konsumenten."""
        return list(self.commands[0])


def normalize_provider(provider: str) -> str:
    normalized = str(provider).strip().lower()
    if normalized not in CAPABILITIES:
        raise AdapterError(
            f"unbekannter Provider {provider!r} — bekannt: {', '.join(PROVIDERS)}"
        )
    return normalized


def normalize_mode(mode: str) -> str:
    normalized = str(mode).strip().lower()
    if normalized not in SESSION_MODES:
        raise AdapterError(
            f"unbekannter Session-Modus {mode!r} — erlaubt: {', '.join(SESSION_MODES)}"
        )
    return normalized


def _required_text(value: str, name: str) -> str:
    text = str(value).strip()
    if not text:
        raise AdapterError(f"{name} muss ein nicht-leerer String sein")
    return text


def _resolve_executable(provider: str, explicit: str | None) -> str:
    if explicit:
        return _required_text(explicit, "executable")
    resolved = shutil.which(provider)
    if not resolved:
        raise AdapterError(f"CLI fuer Provider {provider!r} wurde nicht gefunden")
    return resolved


def build_session_plan(
    provider: str,
    *,
    prompt_file: str | os.PathLike[str],
    request: str,
    mode: str = "interactive",
    model: str = "",
    effort: str = "",
    session_name: str = "",
    cwd: str | os.PathLike[str] | None = None,
    trusted: bool = False,
    mcp_config: str | os.PathLike[str] | None = None,
    executable: str | None = None,
    allow_unverified: bool = False,
) -> SessionPlan:
    """Baut eine Sitzungs-argv fuer einen vorhandenen Rollenprompt.

    ``prompt_file`` und ``request`` bleiben getrennt: die Rollenregeln kommen
    aus der Datei, der Nutzerauftrag bleibt ein eigenes Argument. Die Funktion
    startet keinen Prozess und schreibt keine Datei.
    """
    name = normalize_provider(provider)
    actual_mode = normalize_mode(mode)
    capability = CAPABILITIES[name]
    if not capability.verified and not allow_unverified:
        raise AdapterError(
            f"Provider {name!r} ist fuer Sitzungsstarts nicht live verifiziert; "
            "allow_unverified=True ist erforderlich"
        )

    prompt_path = Path(prompt_file).expanduser().resolve()
    if not prompt_path.is_file():
        raise AdapterError(f"Prompt-Datei nicht gefunden: {prompt_path}")
    workdir = Path(cwd).expanduser().resolve() if cwd is not None else Path.cwd().resolve()
    if not workdir.is_dir():
        raise AdapterError(f"Arbeitsverzeichnis nicht gefunden: {workdir}")
    text = _required_text(request, "request")
    cli = _resolve_executable(name, executable)
    model = str(model).strip()
    effort = str(effort).strip()
    label = str(session_name).strip() or prompt_path.stem
    request_with_path = (
        f"First read the complete authorized role prompt at {prompt_path}. {text}"
    )

    if name == "claude":
        command = [cli]
        if trusted:
            command.append("--dangerously-skip-permissions")
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--effort", effort])
        command.extend(["--name", label])
        if mcp_config:
            command.extend(["--mcp-config", str(Path(mcp_config).expanduser())])
        command.extend(["--append-system-prompt-file", str(prompt_path)])
        if actual_mode == "headless":
            command.extend(["-p", request_with_path])
        else:
            command.append(request_with_path)
        commands = (tuple(command),)

    elif name == "codex":
        command = [cli]
        if actual_mode == "headless":
            command.extend(["exec", "--skip-git-repo-check"])
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend([
                "--config", f"model_reasoning_effort={json.dumps(effort)}",
            ])
        developer = (
            "Read and follow the authorized role instructions in "
            f"{prompt_path}. Read the file completely; it is the canonical "
            "source for this session."
        )
        command.extend([
            "--config", f"developer_instructions={json.dumps(developer)}",
        ])
        if trusted:
            command.extend([
                "--sandbox", "danger-full-access",
                "--ask-for-approval", "never",
            ])
        elif actual_mode == "headless":
            command.extend(["--sandbox", "read-only"])
        command.extend(["--cd", str(workdir), text])
        commands = (tuple(command),)

    elif name == "agy":
        command = [cli]
        if trusted:
            command.extend(["--dangerously-skip-permissions", "--mode", "accept-edits"])
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--effort", effort])
        command.extend(["--add-dir", str(prompt_path.parent)])
        command.extend([
            "--prompt-interactive" if actual_mode == "interactive" else "-p",
            request_with_path,
        ])
        commands = (tuple(command),)

    else:  # kimi
        base = [cli]
        if trusted and actual_mode == "interactive":
            base.append("--yolo")
        if model:
            base.extend(["--model", model])
        boot = [cli]
        if model:
            boot.extend(["--model", model])
        boot.extend(["-p", request_with_path])
        commands = (tuple(boot),)
        if actual_mode == "interactive":
            commands += (tuple(base + ["--continue"]),)

    return SessionPlan(
        provider=name,
        mode=actual_mode,
        commands=commands,
        prompt_file=prompt_path,
        cwd=workdir,
        executable=cli,
        verified=capability.verified,
        capability=capability,
    )


def ordered_candidates(
    primary: Candidate,
    *,
    provider_default: Candidate | None = None,
    fallbacks: Sequence[Candidate] = (),
) -> tuple[Candidate, ...]:
    """Deduplizierte Kette: explizite Wahl, Default, Ersatzanbieter."""
    wanted = (primary,) + ((provider_default,) if provider_default else ()) + tuple(fallbacks)
    chain: list[Candidate] = []
    seen: set[Candidate] = set()
    for item in wanted:
        candidate = Candidate(
            normalize_provider(item.provider),
            str(item.model).strip(),
            str(item.effort).strip(),
        )
        if candidate not in seen:
            seen.add(candidate)
            chain.append(candidate)
    return tuple(chain)


def available_candidates(
    candidates: Sequence[Candidate],
    *,
    which: Callable[[str], str | None] = shutil.which,
    allow_unverified: bool = False,
) -> tuple[tuple[Candidate, ...], tuple[str, ...]]:
    """Filtert eine Kette fail-closed und liefert sichtbare Skip-Gruende."""
    available: list[Candidate] = []
    skipped: list[str] = []
    unavailable: set[str] = set()
    for raw in candidates:
        candidate = Candidate(
            normalize_provider(raw.provider),
            str(raw.model).strip(),
            str(raw.effort).strip(),
        )
        name = candidate.provider
        if name in unavailable:
            continue
        capability = CAPABILITIES[name]
        if not capability.verified and not allow_unverified:
            unavailable.add(name)
            skipped.append(f"{name} — Sitzungsstart nicht live verifiziert")
            continue
        if not which(name):
            unavailable.add(name)
            skipped.append(f"{name} — CLI nicht gefunden")
            continue
        if name != "codex" and not candidate.model:
            unavailable.add(name)
            skipped.append(f"{name} — kein Modell konfiguriert")
            continue
        available.append(candidate)
    return tuple(available), tuple(skipped)


def build_probe_command(
    provider: str,
    executable: str,
    *,
    model: str = "",
    effort: str = "",
) -> list[str]:
    """Ein einmaliger, read-only Print-Aufruf fuer die Erreichbarkeitssonde."""
    name = normalize_provider(provider)
    command = [_required_text(executable, "executable")]
    if name == "claude":
        command.append("--strict-mcp-config")
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--effort", effort])
        command.extend(["-p", PROBE_REQUEST])
    elif name == "codex":
        command.extend(["exec", "--skip-git-repo-check", "--sandbox", "read-only"])
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--config", f"model_reasoning_effort={json.dumps(effort)}"])
        command.append(PROBE_REQUEST)
    elif name == "agy":
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["--effort", effort])
        command.extend(["-p", PROBE_REQUEST])
    else:
        if model:
            command.extend(["--model", model])
        command.extend(["--output-format", "text", "-p", PROBE_REQUEST])
    return command


def _terminate(proc: subprocess.Popen[object]) -> None:
    if proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            proc.kill()
    except OSError:  # pragma: no cover - taskkill fehlt
        proc.kill()


def probe(
    command: Sequence[str],
    timeout: float = DEFAULT_PROBE_TIMEOUT,
    *,
    cwd: str | os.PathLike[str] | None = None,
) -> tuple[bool, str]:
    """Erkennt den Token und beendet die eigene Sonde samt Kindprozess."""
    if timeout <= 0:
        raise AdapterError("probe timeout muss groesser als null sein")
    try:
        proc = subprocess.Popen(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            cwd=str(cwd) if cwd else None,
        )
    except OSError as exc:
        return False, f"Sonde nicht startbar: {exc}"

    timed_out = False

    def stop() -> None:
        nonlocal timed_out
        timed_out = True
        _terminate(proc)

    found = False
    timer = threading.Timer(timeout, stop)
    timer.start()
    try:
        for line in proc.stdout or ():
            if PROBE_TOKEN in line:
                found = True
                break
    finally:
        timer.cancel()
        _terminate(proc)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover
            proc.kill()
        if proc.stdout is not None:
            proc.stdout.close()

    if found:
        return True, f"{PROBE_TOKEN} erkannt"
    if timed_out:
        return False, f"kein {PROBE_TOKEN} innerhalb von {timeout:.0f}s"
    return False, f"Exit {proc.returncode} ohne {PROBE_TOKEN}"


__all__ = [
    "CAPABILITIES",
    "DEFAULT_PROBE_TIMEOUT",
    "PROBE_REQUEST",
    "PROBE_TOKEN",
    "PROVIDERS",
    "SESSION_MODES",
    "Candidate",
    "ProviderCapability",
    "SessionPlan",
    "available_candidates",
    "build_probe_command",
    "build_session_plan",
    "normalize_mode",
    "normalize_provider",
    "ordered_candidates",
    "probe",
]
