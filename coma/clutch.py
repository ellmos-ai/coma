"""Clutch-Anbindung fuer rollenspezifische Modellauswahl, Live-Discovery und Fallback.

E02: Clutch entscheidet Anbieter/Modell-Fallback je Rolle einzeln waehlbar,
lokal ueberstimmbar, abschaltbar. Live-CLI-Discovery (insbesondere `agy models`
sowie lokale CLI-Konfigurationen) schuetzt Starter gegen veraltete Modellnamen
und inkompatible Effort-Kombinationen.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Callable, Mapping, Sequence

from .session import Candidate, PROVIDERS

# Bekannte Gaenge auf CLI-Provider abbilden
GANG_PREFIX_MAP: tuple[tuple[str, str, Callable[[str], str]], ...] = (
    ("claude-", "claude", lambda name: "sonnet" if "sonnet" in name else ("opus" if "opus" in name else ("haiku" if "haiku" in name else name.replace("claude-", "")))),
    ("openai-", "codex", lambda name: name.replace("openai-", "")),
    ("agy-", "agy", lambda name: name.replace("agy-", "")),
    ("kimi-", "kimi", lambda name: ""),
    ("gemini-", "agy", lambda name: name),
)

_EFFORT_SUFFIXES: tuple[str, ...] = ("-xhigh", "-medium", "-thinking", "-high", "-low", "-max")
_EFFORT_FALLBACK_ORDER: tuple[str, ...] = ("high", "medium", "low", "xhigh", "max", "thinking")
_AGY_PREFERRED_ORDER: tuple[str, ...] = (
    "gemini-4-carbon",
    "gemini-4-neon",
    "gemini-4-argon",
    "gemini-4-hydrogen",
    "gemini-3.8-flash",
    "claude-opus-5-5",
    "claude-sonnet-5-5",
    "gpt-oss-120b",
)


def _strip_effort_suffix(model_id: str) -> tuple[str, str]:
    """Zerlegt 'gemini-4-carbon-high' in ('gemini-4-carbon', 'high')."""
    text = str(model_id or "").strip()
    lowered = text.lower()
    for suffix in _EFFORT_SUFFIXES:
        if lowered.endswith(suffix):
            return text[: -len(suffix)], suffix[1:]
    return text, ""


def clamp_effort(effort: str, supported: Sequence[str] | None) -> str:
    """Begrenzt Effort auf die vom Modell unterstuetzten Stufen."""
    clean = str(effort or "").strip().lower()
    allowed = tuple(str(item).strip().lower() for item in (supported or ()) if str(item).strip())
    if not allowed or not clean:
        return clean
    if clean in allowed:
        return clean
    if clean in ("xhigh", "max") and "high" in allowed:
        return "high"
    for candidate in _EFFORT_FALLBACK_ORDER:
        if candidate in allowed:
            return candidate
    return allowed[0]


def is_clutch_available(
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> bool:
    """Prueft, ob die clutch-CLI vorhanden und lauffaehig ist."""
    exe = which("clutch")
    if not exe:
        return False
    try:
        res = run([exe, "--version"], capture_output=True, text=True, timeout=5.0)
        return res.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def get_clutch_models_status(
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: float = 10.0,
) -> dict[str, dict]:
    """Liest Modell-Verfuegbarkeit und Quota-Sperren via `clutch models --status --json`."""
    exe = which("clutch")
    if not exe:
        return {}
    try:
        res = run(
            [exe, "models", "--status", "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if res.returncode != 0 or not res.stdout.strip():
            return {}
        data = json.loads(res.stdout)
        if not isinstance(data, list):
            return {}
        return {str(item.get("name")): item for item in data if isinstance(item, dict) and "name" in item}
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return {}


def discover_agy_model_efforts(
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: float = 8.0,
) -> dict[str, tuple[str, ...]]:
    """Liest die live verfuegbaren Basismodelle + Efforts aus `agy models`."""
    exe = which("agy")
    if not exe:
        return {}
    try:
        res = run(
            [exe, "models"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if res.returncode != 0 or not res.stdout.strip():
            return {}
    except (OSError, subprocess.SubprocessError):
        return {}

    raw_map: dict[str, list[str]] = {}
    for line in res.stdout.splitlines():
        stripped = line.strip()
        if not stripped or "\t" not in stripped:
            continue
        model_id = stripped.split("\t", 1)[0].strip()
        if not model_id or model_id.startswith("gemini-pro-orchestrator"):
            continue
        base, eff = _strip_effort_suffix(model_id)
        bucket = raw_map.setdefault(base, [])
        if eff and eff not in bucket:
            bucket.append(eff)

    if not raw_map:
        return {}

    ordered: dict[str, tuple[str, ...]] = {}
    for preferred in _AGY_PREFERRED_ORDER:
        if preferred in raw_map:
            ordered[preferred] = tuple(raw_map.pop(preferred))
    for remaining, efforts in raw_map.items():
        ordered[remaining] = tuple(efforts)
    return ordered


def _read_cli_default_model(provider: str) -> str:
    """Liest das aktuell konfigurierte Standardmodell aus der lokalen CLI-Config."""
    if provider == "codex":
        path = Path.home() / ".codex" / "config.toml"
        key = "model"
    elif provider == "kimi":
        path = Path.home() / ".kimi-code" / "config.toml"
        key = "default_model"
    else:
        return ""
    if not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        match = re.search(rf'^\s*{re.escape(key)}\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
        return match.group(1).strip() if match else ""
    except OSError:
        return ""


def provider_model_choices(
    provider: str,
    *,
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: float = 8.0,
) -> tuple[str, ...]:
    """Liefert aktuelle, verfuegbare Modellvorschlaege fuer einen CLI-Provider.

    Kombiniert Live-CLI-Discovery (`agy models`, lokale CLI-Configs) und
    nicht-blockierte Eintraege aus `clutch models --status --json`.
    """
    norm = str(provider or "").strip().lower()
    if norm not in PROVIDERS:
        return ()

    if norm == "agy":
        live = discover_agy_model_efforts(which=which, run=run, timeout=timeout)
        if live:
            return tuple(live.keys())

    choices: list[str] = []

    def _add(value: str) -> None:
        text = str(value or "").strip()
        if text and text not in choices:
            choices.append(text)

    if norm == "claude":
        for alias in ("opus", "sonnet", "haiku"):
            _add(alias)
    elif norm in ("codex", "kimi"):
        _add(_read_cli_default_model(norm))

    status_map = get_clutch_models_status(which=which, run=run, timeout=timeout)
    for gang_name, info in status_map.items():
        if not isinstance(info, dict):
            continue
        if info.get("availability") in ("blocked", "disabled"):
            continue
        runners = info.get("runners") or []
        if norm not in runners:
            continue
        model_id = str(info.get("model_id") or "").strip()
        if not model_id or model_id.endswith("-session"):
            continue
        if norm == "claude":
            for alias in ("opus", "sonnet", "haiku"):
                if alias in gang_name:
                    _add(alias)
                    break
            else:
                _add(model_id)
        else:
            _add(model_id)

    return tuple(choices)


def gang_to_candidate(
    gang_name: str,
    effort: str = "",
    models_status: Mapping[str, dict] | None = None,
    *,
    live_agy_efforts: Mapping[str, Sequence[str]] | None = None,
) -> tuple[Candidate | None, str | None]:
    """Mappt einen clutch-Gang auf (Candidate, skip_reason)."""
    raw_gang = str(gang_name).strip()
    if not raw_gang:
        return None, "leerer Gangname"

    status: dict = {}
    if models_status:
        status = models_status.get(raw_gang, {}) or {}
        avail = status.get("availability")
        if avail in ("blocked", "disabled"):
            reason = status.get("availability_reason") or f"Modell ist {avail}"
            return None, f"{raw_gang} — {reason}"

    provider: str | None = None
    model = ""

    # 1. Bekannte Praefixe
    for prefix, mapped_provider, model_fn in GANG_PREFIX_MAP:
        if raw_gang.startswith(prefix):
            provider = mapped_provider
            model = model_fn(raw_gang)
            if provider == "kimi" and not model:
                status_model = str(status.get("model_id") or "").strip()
                if status_model and not status_model.endswith("-session"):
                    model = status_model
            break

    # 2. Status-Lookup (Runners)
    if provider is None and models_status:
        runners = status.get("runners") or []
        for r in runners:
            if r in PROVIDERS:
                provider = r
                model = str(status.get("model_id") or "")
                break

    if provider is None:
        return None, f"{raw_gang} — kein passender CLI-Provider (Runner wird nicht unterstuetzt)"

    effective_effort = str(effort or "").strip()
    if provider == "agy" and live_agy_efforts:
        base_model, embedded_effort = _strip_effort_suffix(model)
        if base_model not in live_agy_efforts:
            return None, f"{raw_gang} — Modell {model!r} nicht in lokaler agy-CLI verfuegbar"
        supported = live_agy_efforts[base_model]
        if embedded_effort:
            effective_effort = ""
        else:
            effective_effort = clamp_effort(effective_effort, supported)
    elif status.get("efforts"):
        effective_effort = clamp_effort(effective_effort, status.get("efforts"))

    return Candidate(provider, model, effective_effort, source="clutch"), None


def resolve_clutch_candidates(
    prompt: str,
    *,
    zweck: str = "",
    effort: str = "",
    fallback: bool = True,
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: float = 10.0,
) -> tuple[tuple[Candidate, ...], tuple[str, ...]]:
    """Fragt clutch route ab und liefert gerankte, live-gefilterte Kandidaten."""
    exe = which("clutch")
    if not exe:
        return (), ("clutch CLI nicht gefunden",)

    cmd = [exe, "route", str(prompt or "TASKPLAN worker"), "--json"]
    if zweck:
        cmd.extend(["--zweck", str(zweck)])
    if effort:
        cmd.extend(["--effort", str(effort)])

    try:
        res = run(cmd, capture_output=True, text=True, timeout=timeout)
        if res.returncode != 0 or not res.stdout.strip():
            err = (res.stderr or res.stdout or f"Exit {res.returncode}").strip()
            return (), (f"clutch route fehlgeschlagen: {err}",)
        data = json.loads(res.stdout)
        if not isinstance(data, dict):
            return (), ("clutch route lieferte kein gueltiges JSON-Objekt",)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return (), (f"clutch route Aufruf fehlgeschlagen: {exc}",)

    models_status = get_clutch_models_status(which=which, run=run, timeout=timeout)

    primary_gang = data.get("gang")
    if not primary_gang:
        return (), ("clutch route enthielt keinen primaeren Gang",)

    clutch_effort = data.get("effort") or effort or ""
    gangs = [primary_gang]
    if fallback:
        alternativen = data.get("alternativen") or []
        if isinstance(alternativen, list):
            gangs.extend(alternativen)

    live_agy_efforts: dict[str, tuple[str, ...]] | None = None
    if any(str(g).startswith(("agy-", "gemini-")) for g in gangs):
        discovered = discover_agy_model_efforts(
            which=which, run=run, timeout=min(timeout, 8.0)
        )
        if discovered:
            live_agy_efforts = discovered

    candidates: list[Candidate] = []
    skipped: list[str] = []
    seen_candidates: set[tuple[str, str, str]] = set()

    for gang in gangs:
        cand, reason = gang_to_candidate(
            gang,
            clutch_effort,
            models_status,
            live_agy_efforts=live_agy_efforts,
        )
        if cand is None:
            if reason:
                skipped.append(reason)
            continue
        if cand.provider == "kimi" and not cand.model:
            local_kimi = _read_cli_default_model("kimi")
            if local_kimi:
                cand = Candidate(cand.provider, local_kimi, cand.effort, source=cand.source)
        key = (cand.provider, cand.model, cand.effort)
        if key not in seen_candidates:
            seen_candidates.add(key)
            candidates.append(cand)

    return tuple(candidates), tuple(skipped)


__all__ = [
    "GANG_PREFIX_MAP",
    "clamp_effort",
    "discover_agy_model_efforts",
    "gang_to_candidate",
    "get_clutch_models_status",
    "is_clutch_available",
    "provider_model_choices",
    "resolve_clutch_candidates",
]
