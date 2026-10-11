# Security Policy — COMA

## Overview

COMA (`coma`) starts agent command-line tools as subprocesses and coordinates work through local files. COMA itself does not implement a network service. A launched agent CLI may contact its provider or other services; COMA does not sandbox that process or block its network access.

## Security Architecture & Principles

### 1. Local Files, Runtime Dependencies, and Data Flow

- COMA's job board, channels, status, and result handling use local filesystem paths.
- The package declares no direct external Python runtime package dependencies. This describes package dependencies, not the network behavior of child processes.
- Job prompts, instructions, process output, and results may be stored in the configured job directory and log files. Provider CLIs receive their configured arguments and inherit the launching process's environment; review workspace permissions, log contents, and environment variables accordingly.
- COMA does not provide network isolation, a firewall, or an air-gap mode.

### 2. Channel Writer Convention

- Callers assign one writer to each channel file as a protocol convention.
- Optional role checks in `Channel.append` do not provide OS-level locking or identity enforcement. They do not prevent multiple processes using the same role from writing concurrently.
- Callers are responsible for coordinating writers when concurrent access is possible. Distinct channel files alone do not prevent races.

### 3. Process Invocation and Permissions

- COMA builds explicit argument arrays and uses subprocess APIs without a shell for provider CLI invocation.
- Child processes inherit the launching process's privileges and environment. COMA does not request elevation or drop privileges, and it is not a security isolation boundary.
- Adapter profiles differ. For example, Claude's `dontAsk` profile allows Read, Edit, Write, Bash, Glob, and Grep; MCP is off by default. Its separate `read_only` preset limits tools to Read, Glob, and Grep. `bat_compat` expands permissions and can enable `bypassPermissions` and MCP. Codex defaults to `read-only`; its `write` profile uses workspace-write, and `danger-full-access` can be configured. Users remain responsible for selecting a provider profile and reviewing the provider CLI's permission and network behavior.
- Claude Code, Codex, Antigravity/AGY, and Kimi are independently developed products. Naming them as adapter targets does not imply endorsement, certification, or an official relationship.

### 4. Probe Timeouts and Cleanup

- Reachability probes use a timeout and attempt to clean up the process they start.
- Cleanup is best-effort and platform-dependent. On Windows COMA requests termination of the process tree; on Unix it kills the direct process. This does not guarantee termination of every descendant.

### 5. Test Scope

- Tests mock provider CLI execution; no test suite result is a live-provider verification.
- A probe test starts a controlled local Python process to check reachability.

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
   - Primary Security Contact: security@ellmos.ai
   - Umbrella Security: security@open-bricks.org
   - Lead Maintainer: lukas@open-bricks.org / support@lukasgeiger.com
4. Include a minimal reproduction case, details of the adapter/OS environment, and expected vs. actual behavior.

### Maintainer Response Policy

Maintainers commit to the following response targets for reports received through the channels above:

- **Initial Acknowledgment:** Within **48 hours** of receiving your report.
- **Triage & Status Assessment:** Within **5 business days** with an initial remediation assessment.
- **Coordinated Disclosure:** Security patches are validated locally and pushed via GitHub releases. We adhere to responsible, coordinated disclosure practices.
