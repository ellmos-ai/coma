"""COMA — COMmunication for Autonomous Subagents.

Die **Lebenszyklus-Schicht** für Agenten: Wie entsteht ein Agent als eigener
Prozess, und wie bleibt man mit ihm in Kontakt, solange er läuft?

Genau eine Verantwortung. COMA sperrt nichts, verwaltet keine Rechte und hält
kein Gedächtnis. Das Vokabular trennt sauber: COMA spricht ``spawn``, ``send``,
``poll``, ``result`` — ein Koordinator wie Roshambo spricht ``claim``,
``release``, ``remember``, ``recall``, ``decide``, ``status``.

Arbeitet mit Dateien und Prozessen: **ohne Konto, ohne Netz, ohne Cluster.**

Kurzform::

    from coma import JobBoard, JobRunner

    board = JobBoard(r"C:\\…\\_control-center\\_agentjobs")
    result = JobRunner(board).run("meinjob")
    print(result["status"]["state"], result["result_written"])

Wer nur ein Kommando braucht, ohne Jobverzeichnis::

    from coma import ClaudeAdapter, Spawner

    spawner = Spawner(ClaudeAdapter(model="sonnet"))
    print(spawner.adapter.build_cmd("Sag Hallo"))

Vollstaendige Beschreibung: ``KONZEPT.md`` und ``README.md``.
"""
from __future__ import annotations

__version__ = "0.3.2"

from .adapters import (
    ADAPTERS,
    DEFAULT_ADAPTER,
    DEFAULT_ALLOWED_TOOLS,
    KNOWN_OUTPUT_FORMATS,
    KNOWN_PERMISSION_MODES,
    MIRROR,
    NO_RESTRICTION,
    READ_ONLY_TOOLS,
    AdapterError,
    AgyAdapter,
    ClaudeAdapter,
    CliAdapter,
    CodexAdapter,
    KimiAdapter,
    SpawnSpec,
    adapter_names,
    describe_adapters,
    get_adapter,
)
from .channels import Channel, ChannelError, from_agent, to_agent
from .locks import LockBackend, LockDenied, NullLock, claimed
from .manifest import CheckReport, ManifestError, build_manifest, check_manifest, vendor
from .poll import (
    is_finished,
    is_running,
    job_view,
    overview,
    read_console_log,
    read_result,
    read_status,
    state,
    wait_for_finish,
)
from .protocol import (
    JobBoard,
    JobNotFound,
    JobPaths,
    ProtocolError,
    check_job_id,
)
from .runner import JobHandle, JobRunner
from .session import (
    CAPABILITIES,
    PROBE_SENTINEL,
    PROBE_TOKEN,
    PROVIDERS,
    Candidate,
    ProviderCapability,
    SessionPlan,
    available_candidates,
    build_probe_command,
    build_session_plan,
    ordered_candidates,
    probe,
)
from .spawn import (
    ProcessHandle,
    SpawnError,
    Spawner,
    UnverifiedAdapterError,
    wait_all,
)
from .status import (
    STATE_DONE,
    STATE_FAILED,
    STATE_RUNNING,
    StatusWriter,
)
from .starters import (
    RoleDeclaration,
    generate_starters,
    load_roles,
    run_starter,
)

__all__ = [
    "ADAPTERS",
    "CAPABILITIES",
    "DEFAULT_ADAPTER",
    "DEFAULT_ALLOWED_TOOLS",
    "KNOWN_OUTPUT_FORMATS",
    "KNOWN_PERMISSION_MODES",
    "MIRROR",
    "NO_RESTRICTION",
    "READ_ONLY_TOOLS",
    "STATE_DONE",
    "STATE_FAILED",
    "STATE_RUNNING",
    "AdapterError",
    "AgyAdapter",
    "Candidate",
    "Channel",
    "ChannelError",
    "CheckReport",
    "ClaudeAdapter",
    "CliAdapter",
    "CodexAdapter",
    "JobBoard",
    "JobHandle",
    "JobNotFound",
    "JobPaths",
    "JobRunner",
    "KimiAdapter",
    "LockBackend",
    "LockDenied",
    "ManifestError",
    "NullLock",
    "ProcessHandle",
    "PROBE_SENTINEL",
    "PROBE_TOKEN",
    "PROVIDERS",
    "ProviderCapability",
    "RoleDeclaration",
    "ProtocolError",
    "SpawnError",
    "SpawnSpec",
    "Spawner",
    "SessionPlan",
    "StatusWriter",
    "UnverifiedAdapterError",
    "__version__",
    "adapter_names",
    "available_candidates",
    "build_manifest",
    "build_probe_command",
    "build_session_plan",
    "check_job_id",
    "check_manifest",
    "claimed",
    "describe_adapters",
    "from_agent",
    "get_adapter",
    "generate_starters",
    "is_finished",
    "is_running",
    "job_view",
    "load_roles",
    "overview",
    "ordered_candidates",
    "probe",
    "read_console_log",
    "read_result",
    "read_status",
    "run_starter",
    "state",
    "to_agent",
    "vendor",
    "wait_all",
    "wait_for_finish",
]
