# Third-Party Licenses & Software Inventory

> **Repository License:** [MIT License](LICENSE) | [Attribution Notice](NOTICE)<br>
> **Inventory snapshot:** 2026-10-04 (previous snapshots: 2026-10-01, 2026-09-28, 2026-09-24, 2026-09-19, 2026-09-12)<br>
> **Scope:** COMA project and listed Python packages for runtime metadata, testing, and build.<br>
> **Process boundary:** Launched provider CLIs inherit caller privileges and environment and may access networks.

---

## 1. Project Scope and License Inventory

The COMA project is provided under the MIT license. pyproject.toml declares no direct external Python runtime package dependencies (INV-COMA-02). This package metadata does not cover the Python runtime, build tools, separately installed agent CLIs, or provider services.

- COMA uses configured local filesystem paths and starts provider CLIs as subprocesses. Launched CLIs inherit the launching process's privileges and environment and may contact providers or other services.
- COMA does not provide a network sandbox, an air-gap guarantee, privilege dropping, or a security isolation boundary.
- One writer per channel is a protocol requirement for callers. Optional role checks are not OS locking or identity enforcement; callers coordinate concurrent writes.

---

## 2. Invariant Cross-Reference Matrix (INV-COMA-01 .. INV-COMA-10)

| Invariant ID | Behavior and Caller Scope | Subsystem / Metadata | Description and Limits |
|---|---|---|---|
| **INV-COMA-01** | **Channel writer convention** | coma.channels | One writer per channel is a caller protocol requirement; role checks do not enforce OS locking or identity. |
| **INV-COMA-02** | **Direct runtime packages** | pyproject.toml | No direct external Python runtime package dependencies are declared; this does not describe provider CLIs or services. |
| **INV-COMA-03** | **Subprocess lifecycle** | coma.spawn, coma.session | Provider CLIs run as subprocesses and inherit caller privileges and environment; COMA does not sandbox them. |
| **INV-COMA-04** | **Process-Free Dry Runs** | `coma.adapters`, `coma.session` | Command builders (`build_cmd`, `build_session_plan`, `--dry-run`) construct argument vectors without launching processes or consuming tokens. |
| **INV-COMA-05** | **Deterministic Multi-Provider Fallback** | `coma.session` | Candidate chain (`ordered_candidates`, `available_candidates`) resolves CLI binaries systematically across Claude, Codex, AGY, and Kimi. |
| **INV-COMA-06** | **Kimi execution opt-in** | `coma.spawn`, `coma.session` | Spawner/session execution of the unverified Kimi adapter requires explicit opt-in; raw adapter or probe argument construction does not enforce that gate. |
| **INV-COMA-07** | **Probe cleanup** | coma.session | A timeout and best-effort platform-dependent cleanup are used; descendant termination is not guaranteed. |
| **INV-COMA-08** | **Idempotent Dual-Platform Starters** | `coma.starters` | Generated starter scripts (`START.bat`, `start.sh`) carry unique marker guards preventing accidental overwrites of custom wrappers. |
| **INV-COMA-09** | **Inherited privileges** | coma.spawn | Child processes inherit the launching process privileges; COMA does not request elevation or drop privileges. |
| **INV-COMA-10** | **Maintainer response policy** | SECURITY.md | Maintainers publish acknowledgment and triage response targets. |

---

## 3. Level 1 Software Bill of Materials (SBOM) & SPDX Package Inventory

### Runtime Dependencies

| Package | Version Spec | SPDX Identifier | Scope | Upstream / Repository | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python Standard Library** | `>=3.10` | `Python-2.0` | `runtime` | [python/cpython](https://github.com/python/cpython) | Process management, JSON serialization, filesystem I/O, threading, and logging |
| *(External Wheels)* | None | N/A | runtime | N/A | No direct external Python runtime packages are declared in project metadata |

### Development, Test & Build Tooling

| Package / Tool | Version Spec | SPDX Identifier | Scope | Upstream / Repository | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[pytest](https://pytest.org/)** | `>=8.0.0` | `MIT` | `[test]` | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | Automated unit, regression, contract, and metadata test suite execution |
| **[ruff](https://github.com/astral-sh/ruff)** | not pinned | `MIT` | maintainer/CI tooling | [astral-sh/ruff](https://github.com/astral-sh/ruff) | Python linter used by maintainers and CI |
| **[setuptools](https://github.com/pypa/setuptools)** | `>=77.0.0` | `MIT` | `[build-system]` | [pypa/setuptools](https://github.com/pypa/setuptools) | Standard PEP 517 / PEP 621 build backend and package distribution |
| **[wheel](https://github.com/pypa/wheel)** | not pinned | `MIT` | `[build-system]` | [pypa/wheel](https://github.com/pypa/wheel) | Standard wheel binary distribution format builder |

---

## 4. External System-Level Binaries & CLI Adapter Targets

| Binary / CLI Target | Prior checked version | Terms assessed here | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **[Python](https://www.python.org/)** | `>=3.10` | `Python-2.0` | System Runtime | Host multi-OS runtime (`Windows`, `Linux`, `macOS`) |
| **[Git](https://git-scm.com/)** | `>=2.40` | `GPL-2.0-only` | Version Control | Plan-D source-of-truth management and tag tracking |
| **[claude](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)** | 2.1.263 (prior check) | Not assessed | External CLI | Anthropic Claude Code CLI adapter target (ClaudeAdapter) |
| **[codex](https://github.com/openai/codex)** | 0.153.4 (prior check) | Not assessed | External CLI | OpenAI Codex CLI adapter target (CodexAdapter) |
| **[agy](https://antigravity.google/docs/cli/overview/)** | 1.1.27 (prior check) | Not assessed | External CLI | Google Antigravity CLI adapter target (AgyAdapter) |
| **[kimi](https://github.com/MoonshotAI/kimi-code)** | legacy kimi-cli 0.31.0 (prior check; archived 2026-09-23) | Not assessed | External CLI | KimiAdapter targets the kimi-code successor; current compatibility is unverified |

The recorded Kimi CLI check covered legacy kimi-cli 0.31.0, archived on 2026-09-23. That check does not establish compatibility with its kimi-code successor. See the [kimi-code repository](https://github.com/MoonshotAI/kimi-code) and the [successor getting-started guide](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/guides/getting-started.md).

---

## 5. License Texts & Attribution

### MIT License (`coma`, `pytest`, `ruff`, `setuptools`, `wheel`)

```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Python Software Foundation License Version 2 (Python Standard Library)

The Python Standard Library is licensed under the PSF License Version 2. See the [complete upstream license text](https://docs.python.org/3/license.html).
