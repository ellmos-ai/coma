"""Clutch-Anbindung fuer rollenspezifische Modellauswahl und Fallback.

E02: Clutch entscheidet Anbieter/Modell-Fallback je Rolle einzeln waehlbar,
lokal ueberstimmbar, abschaltbar.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from typing import Callable, Mapping

from .session import Candidate, PROVIDERS

# Bekannte Gaenge auf CLI-Provider abbilden
GANG_PREFIX_MAP: tuple[tuple[str, str, Callable[[str], str]], ...] = (
    ("claude-", "claude", lambda name: "sonnet" if "sonnet" in name else ("opus" if "opus" in name else ("haiku" if "haiku" in name else name.replace("claude-", "")))),
    ("openai-", "codex", lambda name: name.replace("openai-", "")),
    ("agy-", "agy", lambda name: name.replace("agy-", "")),
    ("kimi-", "kimi", lambda name: ""),
    ("gemini-", "agy", lambda name: name),
)


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


def gang_to_candidate(
    gang_name: str,
    effort: str = "",
    models_status: Mapping[str, dict] | None = None,
) -> tuple[Candidate | None, str | None]:
    """Mappt einen clutch-Gang auf (Candidate, skip_reason)."""
    raw_gang = str(gang_name).strip()
    if not raw_gang:
        return None, "leerer Gangname"

    if models_status:
        status = models_status.get(raw_gang, {})
        avail = status.get("availability")
        if avail in ("blocked", "disabled"):
            reason = status.get("availability_reason") or f"Modell ist {avail}"
            return None, f"{raw_gang} — {reason}"

    # 1. Bekannte Praefixe
    for prefix, provider, model_fn in GANG_PREFIX_MAP:
        if raw_gang.startswith(prefix):
            model = model_fn(raw_gang)
            return Candidate(provider, model, effort, source="clutch"), None

    # 2. Status-Lookup (Runners)
    if models_status:
        status = models_status.get(raw_gang, {})
        runners = status.get("runners") or []
        for r in runners:
            if r in PROVIDERS:
                model_id = str(status.get("model_id") or "")
                return Candidate(r, model_id, effort, source="clutch"), None

    return None, f"{raw_gang} — kein passender CLI-Provider (Runner wird nicht unterstuetzt)"


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
    """Fragt clutch route ab und liefert gerankte Kandidaten."""
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

    candidates: list[Candidate] = []
    skipped: list[str] = []
    seen_candidates: set[tuple[str, str, str]] = set()

    for gang in gangs:
        cand, reason = gang_to_candidate(gang, clutch_effort, models_status)
        if cand is None:
            if reason:
                skipped.append(reason)
            continue
        key = (cand.provider, cand.model, cand.effort)
        if key not in seen_candidates:
            seen_candidates.add(key)
            candidates.append(cand)

    return tuple(candidates), tuple(skipped)


__all__ = [
    "GANG_PREFIX_MAP",
    "gang_to_candidate",
    "get_clutch_models_status",
    "is_clutch_available",
    "resolve_clutch_candidates",
]
