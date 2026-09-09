![COMA Banner](docs/assets/banner.svg)

# COMA — Command & Communication for Autonomous Agents

**[English](README.md) | [Deutsch](README_de.md)**

[![Pytest Status](https://img.shields.io/badge/pytest-241%20passed-brightgreen.svg)](https://docs.pytest.org/)
[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](pyproject.toml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Organization: ellmos-ai](https://img.shields.io/badge/organization-ellmos--ai-blue.svg)](https://github.com/ellmos-ai)
[![Umbrella: open-bricks](https://img.shields.io/badge/umbrella-open--bricks-purple.svg)](https://github.com/open-bricks)

> [!NOTE]
> **LLM / AI Context Index:** For an AI-optimized specification and architecture overview, see [`llms.txt`](llms.txt).

> **Name Migration Notice:** The project and canonical Python package are named `COMA` / `coma`. The legacy name `COMAS`/`comas` remains available during a transition period as an import and CLI alias; new integrations must use `coma`.

> **The Agent Lifecycle Layer:** How is an autonomous AI agent spawned as a standalone process, and how do you communicate with it while it runs?

COMA is a **session-decoupled communication channel and process spawner for AI agents** (file-system based via `IN/`, `OUT/`, `DONE/`). The name stands for **Command & Communication for Agents**.

Single responsibility: COMA does not handle permissions, locks, or long-term agent memory. It works strictly with local files and standard OS processes—**no account required, no network services, no cluster dependencies**. Zero third-party dependencies, standard library only.

See [`KONZEPT.md`](KONZEPT.md) for background details and architectural decisions.

```mermaid
flowchart TD
    subgraph Client ["Orchestrator / Client Session"]
        A[JobBoard.submit] -->|Writes job prompt| B["IN/<jobid>.md"]
    end
    
    subgraph COMA ["COMA Agent Spawner"]
        B --> C{JobRunner / Spawner}
        C -->|Selects CLI Adapter| D[Claude / Codex / AGY / Kimi Adapter]
        D -->|Spawns Subprocess| E[Local Agent Process]
    end

    subgraph Agent ["Agent Execution"]
        E -->|Stream progress events| F["OUT/coma.<jobid>.from-agent.jsonl"]
        E -->|Write final output| G["OUT/<jobid>.result.md"]
    end

    subgraph Completion ["Completion Phase"]
        G --> H["OUT/coma.<jobid>.json (Status: DONE)"]
        H --> I["Move IN/<jobid>.md -> DONE/<jobid>.md"]
    end
```

| Layer | Core Question | Handled By |
|---|---|---|
| **Lifecycle & Communication** | How to spawn an agent and stream input/output? | **COMA** |
| Access Control & Locks | Who can touch which resource/repo? | `lock-master` → Roshambo |
| Memory & History | Was this attempted before, what was the outcome? | Roshambo |

Separation of verbs: COMA uses `spawn`, `send`, `poll`, `result`. A coordinator uses `claim`, `release`, `remember`, `recall`, `decide`, `status`. No overlap.

## Use Cases

1. **Decoupling from Remote Control (RC) Sessions**
   In interactive remote-control sessions, CLI permission bypass flags like `--dangerously-skip-permissions` may fail to pass through to remote clients. COMA launches the agent as an independent OS process outside the RC session, communicating cleanly via file-system channels.

2. **Session-Independent Handoffs & Relays**
   Tasks can be handed off across session boundaries between agents without blocking process threads or losing context.

3. **Background Job Execution**
   File-system based queueing (`IN/`, `OUT/`, `DONE/`) for autonomous background runners and decoupled tool executions.

## Quickstart

```python
from coma import JobBoard, JobRunner

board = JobBoard(r"C:\Users\user\_agentjobs")
board.submit("myjob", "# Instructions\nWrite result to OUT/myjob.result.md.\n")

result = JobRunner(board).run("myjob")
print(result["status"]["state"], result["result_written"])
```

Or from the command line:

```bat
coma --root C:\Users\user\_agentjobs run myjob
coma --root C:\Users\user\_agentjobs run myjob --dry-run   :: preview command without launching
coma --root C:\Users\user\_agentjobs status myjob
coma --root C:\Users\user\_agentjobs result myjob
```

## Job Protocol

```
IN/    <jobid>.md                       Job prompt (Markdown)
OUT/   <jobid>.result.md                Final agent result output
       coma.<jobid>.json               Runner status (written by runner only)
       coma.<jobid>.from-agent.jsonl   Progress stream (written by agent only)
       coma.<jobid>.to-agent.jsonl     Instruction stream (written by orchestrator only)
       coma.<jobid>.console.log        Combined stdout / stderr log
DONE/  <jobid>.md                       Completed job prompt
```

**Single writer per file:** No locking required, structural collision prevention.

## Spawner Layer

Adapters encapsulate CLI arguments for specific agent engines:

```python
from coma import ClaudeAdapter, Spawner

adapter = ClaudeAdapter(model="sonnet", permission_mode="dontAsk",
                        allowed_tools=["Read", "Write"], max_budget_usd=2.0)
print(adapter.build_cmd("Say Hello"))   # Returns argument list without running

spawner = Spawner(adapter)
result = spawner.run("Say Hello", log_file="run.log")
```

### Verified Adapters

| Adapter | Target Engine | Status |
|---|---|---|
| `claude` | Anthropic Claude Code CLI | **Verified** — Flags checked against `claude --help` 2.1.220 |
| `codex` | OpenAI Codex CLI | **Verified** — Tested against CLI 0.145.0 |
| `agy` | Google Antigravity / AGY CLI | **Verified** — Tested against agy 1.1.7 |
| `kimi` | Kimi Code CLI | **Skeleton** — help contract checked with CLI 0.31.0; no real prompt run |

### Interactive and headless sessions

`build_session_plan()` provides one process-free contract for interactive and
headless Claude, Codex, AGY and Kimi argv. A role prompt file and the user
request remain separate arguments. `ordered_candidates()` and
`available_candidates()` build a deterministic provider fallback chain, while
`build_probe_command()` and `probe()` provide a bounded read-only reachability
check with child-process cleanup. Kimi remains fail-closed unless a caller that
already owns a verified Kimi contract explicitly opts in.

```python
from coma import build_session_plan

plan = build_session_plan(
    "codex", prompt_file="AGENTS.md", request="Review the current change.",
    mode="interactive", model="gpt-6", effort="high", cwd=".",
)
print(plan.command)  # argv only; no process has started
```

### Starters from `roles[]`

`coma starters generate` reads the module's top-level `roles[]` declarations
and writes a thin `START.bat` plus executable `start.sh`. Both forward to the
unified console when it is installed and expose a visible COMA fallback when it
is not. The generator only replaces files carrying its own marker unless
`--force` is explicit.

```bat
coma starters generate --manifest ellmos-module.v2.json --output-dir starters
starters\START.bat tasksolver --provider codex --dry-run
```

## CLI Commands

| Command | Purpose |
|---|---|
| `run [jobid]` | Execute job from queue |
| `run ... --dry-run` | Build and show command string without executing |
| `cmd <prompt>` | Show command string for custom prompt |
| `session --provider … --prompt-file … --request …` | Plan or start an interactive/headless role session |
| `starters generate` · `starters run` | Generate dual-platform `roles[]` starters or use their COMA fallback |
| `submit <jobid>` | Submit job prompt into `IN/` |
| `status <jobid>` · `list` | Check status of job(s) |
| `result <jobid>` · `log <jobid>` | Read result output or console log |
| `send <jobid> <text>` · `inbox <jobid>` | Send message or read progress stream |
| `adapters` | Show adapter status & detected binaries |
| `check` · `vendor` | Verify or build vendor manifest |

## Testing

```bat
python -m pytest -q      :: 258 passed tests
```

Tests never start a provider. One bounded probe test uses the local Python
interpreter as a harmless fake CLI; all remaining subprocess calls are mocked.

## Sibling Tools & Ecosystem

COMA is part of the `ellmos-ai` orchestration architecture and the broader `open-bricks` open-source umbrella:

| Layer / Ecosystem | Repository | Purpose |
|---|---|---|
| **Agent Orchestration** | [`ellmos-ai/coma`](https://github.com/ellmos-ai/coma) | Process lifecycle spawner & session-decoupled job board |
| **Governance & Policy** | [`ellmos-ai/policy-registry`](https://github.com/ellmos-ai/policy-registry) | Central governance, role definitions & delegation rules |
| **Data Transit** | [`ellmos-ai/sqlite-transit-sync`](https://github.com/ellmos-ai/sqlite-transit-sync) | Zero-copy transaction sync & SQLite replication |
| **Fleet Inspection** | [`ellmos-ai/system-explorer`](https://github.com/ellmos-ai/system-explorer) | System introspection, MCP diagnostics & fleet monitoring |
| **Automation Flow** | [`ellmos-ai/workflowhooker`](https://github.com/ellmos-ai/workflowhooker) | Event triggers, pipeline hooks & webhook orchestration |
| **Task Delegation** | [`ellmos-ai/ellmos-delegation-authority`](https://github.com/ellmos-ai/ellmos-delegation-authority) | Autonomous task authorization & authority validation |
| **Dev Tools** | [`dev-bricks/DevCenter`](https://github.com/dev-bricks/DevCenter) | Developer workstation hub, workspace management & tools |
| **CLI Sandbox** | [`dev-bricks/CodeBox`](https://github.com/dev-bricks/CodeBox) | Sandboxed code execution & snippet validation |
| **Agent Bootstrap** | [`dev-bricks/safe-start-for-codex`](https://github.com/dev-bricks/safe-start-for-codex) | Safe startup, environment checks & preflight diagnostics |

## Security

For subprocess isolation details, single-writer protocol boundaries, and vulnerability disclosure policies, see [`SECURITY.md`](SECURITY.md).

## License

MIT License. Developed under the `ellmos-ai` / `open-bricks` ecosystem.
