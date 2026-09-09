# -*- coding: utf-8 -*-
"""Vertraege fuer interaktive/headless Sitzungen ohne echten Modellstart."""
from __future__ import annotations

import sys

import pytest

from coma import (
    CAPABILITIES,
    PROBE_TOKEN,
    AdapterError,
    Candidate,
    available_candidates,
    build_probe_command,
    build_session_plan,
    ordered_candidates,
    probe,
)
from coma.cli import main


@pytest.fixture
def prompt_file(tmp_path):
    path = tmp_path / "Rolle mit Umlaut ä.md"
    path.write_text("# Rolle\n", encoding="utf-8")
    return path


def test_capabilities_record_verified_help_contracts():
    assert set(CAPABILITIES) == {"claude", "codex", "agy", "kimi"}
    assert CAPABILITIES["claude"].help_version == "Claude Code 2.1.263"
    assert CAPABILITIES["kimi"].verified is False
    assert CAPABILITIES["kimi"].supports_effort is False


def test_claude_interactive_and_headless_contract(prompt_file, tmp_path):
    common = dict(
        prompt_file=prompt_file,
        request="Prüfe vollständig.",
        model="sonnet",
        effort="high",
        session_name="review",
        cwd=tmp_path,
        executable="claude-test",
    )
    interactive = build_session_plan("claude", **common)
    headless = build_session_plan("claude", mode="headless", **common)
    assert interactive.command[:7] == [
        "claude-test", "--model", "sonnet", "--effort", "high", "--name", "review",
    ]
    assert interactive.command[interactive.command.index("--append-system-prompt-file") + 1] == str(prompt_file)
    assert "-p" not in interactive.command
    assert headless.command[-2] == "-p"
    assert "Prüfe vollständig." in headless.command[-1]


def test_codex_contract_uses_interactive_root_or_exec(prompt_file, tmp_path):
    interactive = build_session_plan(
        "codex", prompt_file=prompt_file, request="Arbeite.", model="gpt-6",
        effort="xhigh", cwd=tmp_path, executable="codex-test",
    )
    headless = build_session_plan(
        "codex", prompt_file=prompt_file, request="Arbeite.", mode="headless",
        cwd=tmp_path, executable="codex-test",
    )
    assert interactive.command[0] == "codex-test"
    assert "exec" not in interactive.command
    assert interactive.command[-3:] == ["--cd", str(tmp_path), "Arbeite."]
    assert headless.command[1:3] == ["exec", "--skip-git-repo-check"]
    assert headless.command[headless.command.index("--sandbox") + 1] == "read-only"


def test_agy_modes_and_unicode_path_are_single_arguments(prompt_file, tmp_path):
    interactive = build_session_plan(
        "agy", prompt_file=prompt_file, request="Los.", model="Gemini Test",
        effort="high", cwd=tmp_path, executable="agy-test",
    )
    headless = build_session_plan(
        "agy", prompt_file=prompt_file, request="Los.", mode="headless",
        model="Gemini Test", cwd=tmp_path, executable="agy-test",
    )
    assert interactive.command[-2] == "--prompt-interactive"
    assert str(prompt_file) in interactive.command[-1]
    assert headless.command[-2] == "-p"


def test_kimi_is_fail_closed_and_two_phase_when_explicit(prompt_file, tmp_path):
    with pytest.raises(AdapterError, match="nicht live verifiziert"):
        build_session_plan(
            "kimi", prompt_file=prompt_file, request="Los.", cwd=tmp_path,
            executable="kimi-test",
        )
    plan = build_session_plan(
        "kimi", prompt_file=prompt_file, request="Los.", cwd=tmp_path,
        executable="kimi-test", allow_unverified=True,
    )
    assert len(plan.commands) == 2
    assert plan.commands[0][-2] == "-p"
    assert plan.commands[1][-1] == "--continue"


def test_ordered_and_available_fallback_chain_is_deduplicated():
    chain = ordered_candidates(
        Candidate("claude", "opus", "high"),
        provider_default=Candidate("claude", "opus", "high"),
        fallbacks=(Candidate("kimi", "k2", ""), Candidate("codex")),
    )
    available, skipped = available_candidates(
        chain, which=lambda name: f"/fake/{name}"
    )
    assert available == (Candidate("claude", "opus", "high"), Candidate("codex"))
    assert skipped == ("kimi — Sitzungsstart nicht live verifiziert",)


def test_probe_command_contracts_do_not_invent_effort_for_kimi():
    command = build_probe_command("kimi", "kimi-test", model="k2", effort="max")
    assert command == [
        "kimi-test", "--model", "k2", "--output-format", "text", "-p",
        "Reply with exactly COMA_SESSION_PROBE_OK and nothing else.",
    ]


def test_probe_accepts_token_from_bounded_fake_process(tmp_path):
    command = [sys.executable, "-c", f"print({PROBE_TOKEN!r})"]
    assert probe(command, 5, cwd=tmp_path) == (True, f"{PROBE_TOKEN} erkannt")


def test_cli_session_dry_run_never_starts_provider(prompt_file, tmp_path, capsys):
    code = main([
        "session", "--provider", "codex", "--prompt-file", str(prompt_file),
        "--request", "Nur planen.", "--cwd", str(tmp_path), "--dry-run",
    ])
    assert code == 0
    assert "Nur planen." in capsys.readouterr().out
