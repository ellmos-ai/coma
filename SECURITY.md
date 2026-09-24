# Security Policy — COMA

## Overview

COMA (`coma`) provides a local-first, process-isolated lifecycle spawner and session-decoupled communication protocol for autonomous AI agents. Security in COMA centers around predictable process invocation, strict filesystem boundary separation, and zero external network exposure.

## Security Architecture & Principles

### 1. Local-First & Zero Network Exposure
- COMA operates strictly with standard local OS processes (`subprocess.Popen` / `subprocess.run`) and filesystem paths (`IN/`, `OUT/`, `DONE/`).
- COMA requires **zero network dependencies**, opens no listening ports, makes no background HTTP/socket requests, and has no cloud server telemetry.

### 2. Single-Writer File Protocol
- The job board protocol utilizes distinct single-writer files per channel:
  - `IN/<jobid>.md`: Written exclusively by the orchestrator / job submitter.
  - `OUT/coma.<jobid>.json`: Written exclusively by the `JobRunner`.
  - `OUT/coma.<jobid>.from-agent.jsonl`: Written exclusively by the agent process.
  - `OUT/coma.<jobid>.to-agent.jsonl`: Written exclusively by the orchestrator.
  - `OUT/<jobid>.result.md`: Written exclusively by the completing agent.
- This deterministic separation prevents race conditions and cross-agent concurrency hazards without distributed locks.

### 3. Subprocess Isolation & Non-Elevation
- COMA spawns agent CLI processes with explicit argument arrays, preventing shell-injection vulnerabilities (`shell=False`).
- COMA does not elevate privileges or execute commands as root/administrator.
- Permission modes (`--dangerously-skip-permissions`, `dontAsk`) and tool whitelists (`--allowedTools`, `--disallowedTools`) are configurable via CLI adapters (`ClaudeAdapter`, `CodexAdapter`, `AgyAdapter`, `KimiAdapter`) with safe defaults.

### 4. Deterministic Mocking in Test Suites
- Test suites run 100% locally with mocked subprocess calls to avoid accidental token consumption, unexpected execution, or remote side effects.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| 0.2.x   | :white_check_mark: |
| < 0.2.0 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability or execution hazard within COMA:

1. **Do not open a public issue.**
2. Report the vulnerability privately via GitHub Security Advisories at [https://github.com/ellmos-ai/coma/security/advisories](https://github.com/ellmos-ai/coma/security/advisories).
3. If GitHub Advisories is unavailable, contact the security team directly:
   - Primary Security Contact: `security@ellmos.ai`
   - Umbrella Security: `security@open-bricks.org`
   - Lead Maintainer: `lukas@open-bricks.org` / `support@lukasgeiger.com`
4. Include a minimal reproduction case, details of the adapter/OS environment, and expected vs. actual behavior.

### Response SLA & Disclosure Timeline

- **Initial Acknowledgment:** Within **48 hours** of receiving your report.
- **Triage & Status Assessment:** Within **5 business days** with an initial remediation assessment.
- **Coordinated Disclosure:** Security patches are validated locally and pushed via GitHub releases. We adhere to responsible, coordinated disclosure practices.
