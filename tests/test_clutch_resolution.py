"""Tests fuer die Clutch-Anbindung in COMA (T-20260906-737455509)."""
from __future__ import annotations

import json


from coma.clutch import (
    gang_to_candidate,
    is_clutch_available,
    resolve_clutch_candidates,
)
from coma.session import Candidate, ordered_candidates, available_candidates


class FakeCompletedProcess:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_is_clutch_available():
    # 1. Nicht im Pfad
    assert not is_clutch_available(which=lambda _: None)

    # 2. Im Pfad, aber Fehler beim Ausfuehren
    def run_fail(*args, **kwargs):
        raise OSError("Permission denied")
    assert not is_clutch_available(which=lambda _: "/bin/clutch", run=run_fail)

    # 3. Im Pfad, Exit != 0
    assert not is_clutch_available(
        which=lambda _: "/bin/clutch",
        run=lambda *args, **kwargs: FakeCompletedProcess(returncode=1),
    )

    # 4. Erfolgreich
    assert is_clutch_available(
        which=lambda _: "/bin/clutch",
        run=lambda *args, **kwargs: FakeCompletedProcess(returncode=0, stdout="clutch 0.6.3"),
    )


def test_gang_to_candidate():
    # Claude
    cand, skip = gang_to_candidate("claude-sonnet", effort="high")
    assert skip is None
    assert cand == Candidate("claude", "sonnet", "high", source="clutch")

    # Claude Opus
    cand, skip = gang_to_candidate("claude-opus", effort="xhigh")
    assert skip is None
    assert cand == Candidate("claude", "opus", "xhigh", source="clutch")

    # Codex (OpenAI)
    cand, skip = gang_to_candidate("openai-gpt-5.6-terra", effort="high")
    assert skip is None
    assert cand == Candidate("codex", "gpt-5.6-terra", "high", source="clutch")

    # AGY (Gemini / Antigravity)
    cand, skip = gang_to_candidate("agy-gemini-3.5-flash", effort="low")
    assert skip is None
    assert cand == Candidate("agy", "gemini-3.5-flash", "low", source="clutch")

    # Kimi
    cand, skip = gang_to_candidate("kimi-cli", effort="max")
    assert skip is None
    assert cand == Candidate("kimi", "", "max", source="clutch")

    # Blockiertes Modell via models_status
    status_map = {
        "claude-sonnet": {
            "name": "claude-sonnet",
            "availability": "blocked",
            "availability_reason": "Quota erreicht",
        }
    }
    cand, skip = gang_to_candidate("claude-sonnet", effort="high", models_status=status_map)
    assert cand is None
    assert "Quota erreicht" in skip

    # Unbekannter/Nicht unterstuetzter Runner
    cand, skip = gang_to_candidate("ollama-qwen3", effort="low")
    assert cand is None
    assert "nicht unterstuetzt" in skip


def test_resolve_clutch_candidates_missing_clutch():
    candidates, skipped = resolve_clutch_candidates(
        "Fix auth bug",
        which=lambda _: None,
    )
    assert candidates == ()
    assert "nicht gefunden" in skipped[0]


def test_resolve_clutch_candidates_route_failure():
    def run_mock(cmd, *args, **kwargs):
        return FakeCompletedProcess(returncode=1, stderr="Syntax error in route")

    candidates, skipped = resolve_clutch_candidates(
        "Fix auth bug",
        which=lambda _: "/bin/clutch",
        run=run_mock,
    )
    assert candidates == ()
    assert "fehlgeschlagen" in skipped[0]


def test_resolve_clutch_candidates_success():
    route_output = json.dumps({
        "gang": "claude-sonnet",
        "provider": "anthropic",
        "effort": "high",
        "alternativen": [
            "openai-gpt-5.6-terra",
            "agy-gemini-3.5-flash",
            "ollama-qwen3",
        ]
    })
    status_output = json.dumps([
        {"name": "claude-sonnet", "availability": "available", "runners": ["claude"]},
        {"name": "openai-gpt-5.6-terra", "availability": "available", "runners": ["codex"]},
        {"name": "agy-gemini-3.5-flash", "availability": "available", "runners": ["agy"]},
        {"name": "ollama-qwen3", "availability": "available", "runners": ["ollama"]},
    ])

    def run_mock(cmd, *args, **kwargs):
        if "route" in cmd:
            return FakeCompletedProcess(returncode=0, stdout=route_output)
        if "models" in cmd:
            return FakeCompletedProcess(returncode=0, stdout=status_output)
        return FakeCompletedProcess(returncode=1)

    candidates, skipped = resolve_clutch_candidates(
        "Fix auth bug",
        zweck="coding",
        effort="high",
        which=lambda _: "/bin/clutch",
        run=run_mock,
    )
    assert len(candidates) == 3
    assert candidates[0] == Candidate("claude", "sonnet", "high", source="clutch")
    assert candidates[1] == Candidate("codex", "gpt-5.6-terra", "high", source="clutch")
    assert candidates[2] == Candidate("agy", "gemini-3.5-flash", "high", source="clutch")
    assert any("ollama-qwen3" in s for s in skipped)


def test_resolve_clutch_candidates_no_fallback():
    route_output = json.dumps({
        "gang": "claude-sonnet",
        "effort": "high",
        "alternativen": ["openai-gpt-5.6-terra"],
    })

    def run_mock(cmd, *args, **kwargs):
        if "route" in cmd:
            return FakeCompletedProcess(returncode=0, stdout=route_output)
        if "models" in cmd:
            return FakeCompletedProcess(returncode=0, stdout="[]")
        return FakeCompletedProcess(returncode=1)

    candidates, skipped = resolve_clutch_candidates(
        "Fix auth bug",
        fallback=False,
        which=lambda _: "/bin/clutch",
        run=run_mock,
    )
    assert len(candidates) == 1
    assert candidates[0] == Candidate("claude", "sonnet", "high", source="clutch")


def test_ordered_and_available_candidates_preserves_source():
    c1 = Candidate("claude", "sonnet", "high", source="clutch")
    c2 = Candidate("codex", "gpt-5.6-terra", "high", source="config")

    ordered = ordered_candidates(c1, fallbacks=[c2])
    assert ordered[0].source == "clutch"
    assert ordered[1].source == "config"

    available, skipped = available_candidates(
        ordered,
        which=lambda p: f"/bin/{p}",
    )
    assert len(available) == 2
    assert available[0].source == "clutch"
    assert available[1].source == "config"
