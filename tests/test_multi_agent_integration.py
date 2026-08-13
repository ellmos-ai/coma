# -*- coding: utf-8 -*-
"""Integration coverage for independent agents sharing one JobBoard.

These tests stay process-free: ``Popen`` is replaced with the existing fake
process fixture. The contract under test is the file protocol and the runner's
per-job isolation, not a real CLI invocation.
"""
import json
import os

from coma import ClaudeAdapter, JobRunner, from_agent, read_status
from coma.cli import main


def test_two_agents_can_start_and_finish_independently(
    board, monkeypatch, fake_popen
):
    """Two runners may use the same board without sharing status or archives."""
    board.submit("agent-a", "# Agent A\n")
    board.submit("agent-b", "# Agent B\n")

    monkeypatch.setattr(
        "coma.spawn.subprocess.Popen",
        lambda cmd, **kwargs: fake_popen(cmd, **kwargs).program(0),
    )
    runner_a = JobRunner(board, ClaudeAdapter(model="sonnet"))
    runner_b = JobRunner(board, ClaudeAdapter(model="haiku"))

    handle_a = runner_a.start("agent-a")
    handle_b = runner_b.start("agent-b")

    # Finish in the opposite order to the submission order. Each handle must
    # still finalize only its own JobPaths.
    result_b = handle_b.wait()
    result_a = handle_a.wait()

    assert result_a["job_id"] == "agent-a"
    assert result_b["job_id"] == "agent-b"
    assert result_a["status"]["state"] == "done"
    assert result_b["status"]["state"] == "done"
    assert read_status(board.paths("agent-a"))["argv"][0] == "claude"
    assert read_status(board.paths("agent-b"))["argv"][0] == "claude"
    assert board.done() == ["agent-a", "agent-b"]
    assert board.pending() == []
    assert board.paths("agent-a").to_agent_file.is_file()
    assert board.paths("agent-b").to_agent_file.is_file()
    assert board.paths("agent-a").to_agent_file != board.paths("agent-b").to_agent_file


def test_cli_dry_run_uses_oldest_job_without_mutating_the_board(
    board, monkeypatch, capsys
):
    """The CLI dry-run resolves a job but creates no runner artefacts."""
    board.submit("older", "# older\n")
    board.submit("newer", "# newer\n")
    os.utime(board.paths("older").job_file, (1_000_000, 1_000_000))

    def forbidden(*args, **kwargs):  # pragma: no cover - assertion guard
        raise AssertionError("dry-run darf keinen Prozess starten")

    monkeypatch.setattr("coma.spawn.subprocess.run", forbidden)
    monkeypatch.setattr("coma.spawn.subprocess.Popen", forbidden)

    code = main(
        ["--root", str(board.root), "--json", "run", "--dry-run"]
    )
    payload = json.loads(capsys.readouterr().out)

    assert code == 0
    assert payload["job_id"] == "older"
    assert payload["argv"][0] == "claude"
    assert board.pending() == ["older", "newer"]
    for job_id in ("older", "newer"):
        paths = board.paths(job_id)
        assert not paths.status_file.exists()
        assert not paths.console_log.exists()
        assert not paths.to_agent_file.exists()


def test_jsonl_stream_since_and_cli_inbox_keep_agent_events_separate(
    board, job, capsys
):
    """Incremental JSONL reads ignore a partial line and preserve event order."""
    stream = from_agent(job)
    stream.append({"agent": "alpha", "event": "started", "seq": 1}, role="agent")
    checkpoint = stream.count()
    stream.append({"agent": "beta", "event": "progress", "seq": 2}, role="agent")
    with stream.path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write('{"agent":"broken"\n')
    stream.append({"agent": "alpha", "event": "done", "seq": 3}, role="agent")

    delta = stream.since(checkpoint)
    assert [(row["agent"], row["event"]) for row in delta] == [
        ("beta", "progress"),
        ("alpha", "done"),
    ]

    code = main(
        [
            "--root",
            str(board.root),
            "--json",
            "inbox",
            "testjob",
            "--tail",
            "2",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert [(row["agent"], row["seq"]) for row in payload] == [
        ("beta", 2),
        ("alpha", 3),
    ]
