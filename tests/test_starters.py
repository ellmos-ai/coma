# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import stat
from unittest import mock

import pytest

from coma import AdapterError
from coma.cli import main
from coma.starters import GENERATED_MARKER, generate_starters, load_roles, run_starter


def _manifest(tmp_path):
    prompt = tmp_path / "prompts" / "Rolle ä.md"
    prompt.parent.mkdir()
    prompt.write_text("# Rolle", encoding="utf-8")
    manifest = tmp_path / "ellmos-module.v2.json"
    manifest.write_text(json.dumps({
        "id": "example",
        "roles": [{
            "id": "reviewer",
            "label": "REVIEWER",
            "prompt": "prompts/Rolle ä.md",
            "request": "Prüfe vollständig.",
            "providers": ["codex", "claude"],
        }],
    }, ensure_ascii=False), encoding="utf-8")
    return manifest


def test_load_roles_resolves_unicode_prompt_relative_to_manifest(tmp_path):
    role = load_roles(_manifest(tmp_path))[0]
    assert role.key == "example:reviewer"
    assert role.prompt_file.name == "Rolle ä.md"
    assert role.request == "Prüfe vollständig."


def test_generator_writes_thin_dual_platform_forwarders(tmp_path):
    manifest = _manifest(tmp_path)
    windows, posix = generate_starters(manifest, tmp_path / "bin")
    windows_text = windows.read_text(encoding="utf-8")
    posix_text = posix.read_text(encoding="utf-8")
    assert GENERATED_MARKER in windows_text
    assert "python -m unified_gui.console start" in windows_text
    assert "[FALLBACK]" in windows_text
    assert "python -m coma starters run" in windows_text
    assert GENERATED_MARKER in posix_text
    if os.name != "nt":
        assert posix.stat().st_mode & stat.S_IXUSR


def test_generator_refuses_to_overwrite_handwritten_starter(tmp_path):
    manifest = _manifest(tmp_path)
    output = tmp_path / "bin"
    output.mkdir()
    handmade = output / "START.bat"
    handmade.write_text("@echo off\necho user file\n", encoding="utf-8")
    with pytest.raises(AdapterError, match="unangetastet"):
        generate_starters(manifest, output)
    assert handmade.read_text(encoding="utf-8").endswith("user file\n")


def test_generator_is_idempotent_for_its_own_files(tmp_path):
    manifest = _manifest(tmp_path)
    first = generate_starters(manifest, tmp_path / "bin")
    before = [path.read_bytes() for path in first]
    second = generate_starters(manifest, tmp_path / "bin")
    assert [path.read_bytes() for path in second] == before


def test_generated_fallback_selects_number_and_dry_run_starts_nothing(tmp_path):
    manifest = _manifest(tmp_path)
    runner = mock.Mock()
    with mock.patch("coma.session.shutil.which", return_value="codex-test"):
        code = run_starter(
            manifest,
            role="1",
            provider="codex",
            cwd=tmp_path,
            dry_run=True,
            run=runner,
        )
    assert code == 0
    runner.assert_not_called()


def test_cli_generates_starters(tmp_path):
    manifest = _manifest(tmp_path)
    output = tmp_path / "bin"
    assert main([
        "starters", "generate", "--manifest", str(manifest),
        "--output-dir", str(output),
    ]) == 0
    assert (output / "START.bat").is_file()
    assert (output / "start.sh").is_file()
