# Third-Party Licenses & Software Inventory

> **Repository License:** [MIT License](LICENSE) | [Attribution Notice](NOTICE)<br>
> **Audited:** 2026-09-24 (Previous Audits: 2026-09-19, 2026-09-12)<br>
> **Status:** Invariant Confirmed — Zero External Runtime Dependencies (`INV-COMA-02`)<br>
> **Architecture & Security:** 100% Local-First, Zero-Egress, Single-Writer Channel Protocol, Unprivileged User-Mode (`RunAsInvoker`)

---

## 1. Executive Summary & Zero-Copyleft Isolation Guarantee

`coma` is engineered as a provider-independent, session-decoupled agent lifecycle and process orchestration interface. To preserve maximum operational reliability across multi-agent environments (Claude Code CLI, OpenAI Codex CLI, Google Antigravity / AGY CLI, Kimi Code CLI), ensure deterministic multi-OS execution (Windows, Linux, macOS), and eliminate external supply-chain attack vectors, `coma` strictly enforces the **Zero External Runtime Dependencies** invariant (**INV-COMA-02**).

- **100% Permissive / Standard Library:** Core execution uses exclusively the Python Standard Library distributed under the Python Software Foundation License (PSFL-2.0).
- **Zero-Copyleft Isolation Guarantee:** No GPL, AGPL, or viral copyleft dependencies are incorporated into the runtime distribution.
- **Unprivileged User-Mode (`RunAsInvoker`):** `coma` executes exclusively in standard, non-elevated user space without requesting root or administrator privileges.

---

## 2. Invariant Cross-Reference Matrix (INV-COMA-01 .. INV-COMA-10)

| Invariant ID | Guarantee & Scope | Enforcing Subsystem / Module | Compliance Assurance |
|---|---|---|---|
| **INV-COMA-01** | **Single-Writer Rule** | `coma.protocol`, `coma.channels` | Exactly one writer per channel file (`IN/`, `OUT/`, `DONE/`), eliminating race conditions and lock contention. |
| **INV-COMA-02** | **Zero External Runtime Dependencies** | `pyproject.toml`, `coma/` | Zero external runtime wheels; 100% pure Python standard library (`subprocess`, `os`, `sys`, `pathlib`, `json`, `time`). |
| **INV-COMA-03** | **Session Decoupling & RC Immunity** | `coma.spawner`, `coma.session` | Subprocesses spawn in dedicated process trees outside interactive terminal sessions, bypassing remote-control permission stalls. |
| **INV-COMA-04** | **Process-Free Dry Runs** | `coma.adapters`, `coma.session` | Command builders (`build_cmd`, `build_session_plan`, `--dry-run`) construct argument vectors without launching processes or consuming tokens. |
| **INV-COMA-05** | **Deterministic Multi-Provider Fallback** | `coma.session.candidates` | Candidate chain (`ordered_candidates`, `available_candidates`) resolves CLI binaries systematically across Claude, Codex, AGY, and Kimi. |
| **INV-COMA-06** | **Fail-Closed Provider Safety** | `coma.adapters.kimi`, `coma.session` | Unverified or experimental adapters remain strictly fail-closed unless callers explicitly opt in with an established contract. |
| **INV-COMA-07** | **Bounded Probe Cleanup** | `coma.session.probe` | Reachability probes enforce strict execution timeouts and guarantee child-process termination to prevent zombie processes. |
| **INV-COMA-08** | **Idempotent Dual-Platform Starters** | `coma.starters` | Generated starter scripts (`START.bat`, `start.sh`) carry unique marker guards preventing accidental overwrites of custom wrappers. |
| **INV-COMA-09** | **Unprivileged User-Mode Execution** | `coma.spawner`, `coma.cli` | Strictly unprivileged user execution (`RunAsInvoker`); zero administrative elevation or driver hooks required. |
| **INV-COMA-10** | **48h Security & Governance SLA** | `SECURITY.md`, `ellmos-ai` | Committed 48-hour response SLA and 5-business-day vulnerability triage for all reported security hazards. |

---

## 3. Level 1 Software Bill of Materials (SBOM) & SPDX Package Inventory

### Runtime Dependencies

| Package | Version Spec | SPDX Identifier | Scope | Upstream / Repository | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python Standard Library** | `>=3.10` | `Python-2.0` | `runtime` | [python/cpython](https://github.com/python/cpython) | Process management, JSON serialization, filesystem I/O, threading, and logging |
| *(External Wheels)* | `None` | `N/A` | `runtime` | `N/A` | Pure standard library invariant confirmed |

### Development, Test & Build Tooling

| Package / Tool | Version Spec | SPDX Identifier | Scope | Upstream / Repository | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[pytest](https://pytest.org/)** | `>=8.0.0` | `MIT` | `[test]` | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | Automated unit, regression, contract, and metadata test suite execution |
| **[ruff](https://github.com/astral-sh/ruff)** | `>=0.5.0` | `MIT OR Apache-2.0` | `[dev]` | [astral-sh/ruff](https://github.com/astral-sh/ruff) | High-performance Python linter, style enforcer, and AST validation |
| **[setuptools](https://github.com/pypa/setuptools)** | `>=77.0.0` | `MIT` | `[build-system]` | [pypa/setuptools](https://github.com/pypa/setuptools) | Standard PEP 517 / PEP 621 build backend and package distribution |
| **[wheel](https://github.com/pypa/wheel)** | `>=0.40.0` | `MIT` | `[build-system]` | [pypa/wheel](https://github.com/pypa/wheel) | Standard wheel binary distribution format builder |

---

## 4. External System-Level Binaries & CLI Adapter Targets

| Binary / CLI Target | Verified Version | SPDX / License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **[Python](https://www.python.org/)** | `>=3.10` | `Python-2.0` | System Runtime | Host multi-OS runtime (`Windows`, `Linux`, `macOS`) |
| **[Git](https://git-scm.com/)** | `>=2.40` | `GPL-2.0-only` | Version Control | Plan-D source-of-truth management and tag tracking |
| **[claude](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)** | `2.1.263` | `Proprietary` | Agent Engine | Anthropic Claude Code CLI adapter target (`ClaudeAdapter`) |
| **[codex](https://github.com/openai/codex)** | `0.153.4` | `Proprietary` | Agent Engine | OpenAI Codex CLI adapter target (`CodexAdapter`) |
| **[agy](https://github.com/google/antigravity)** | `1.1.27` | `Proprietary` | Agent Engine | Google Antigravity CLI adapter target (`AntigravityAdapter`) |
| **[kimi](https://github.com/moonshot-ai/kimi-code)** | `0.31.0` | `Proprietary` | Agent Engine | Kimi Code CLI skeleton adapter target (fail-closed, `KimiAdapter`) |

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

### Python Software Foundation License Version 2 (`Python Standard Library`)

```text
PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
--------------------------------------------

1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and
the Individual or Organization ("Licensee") accessing and otherwise using this
software ("Python") in source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative works,
distribute, and otherwise use Python alone or in any derivative version,
provided, however, that PSF's License Agreement and PSF's notice of copyright,
i.e., "Copyright (c) 2001-2026 Python Software Foundation; All Rights Reserved"
are retained in Python alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on or
incorporates Python or any part thereof, and wants to make the derivative work
available to others as provided herein, then Licensee hereby agrees to include in
any such work a brief summary of the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS" basis. PSF MAKES NO
REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT
LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF
MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF
PYTHON WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON FOR ANY
INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF MODIFYING,
DISTRIBUTING, OR OTHERWISE USING PYTHON, OR ANY DERIVATIVE THEREOF, EVEN IF
ADVISED OF THE POSSIBILITY THEREOF.
```

### Apache License Version 2.0 (`ruff` dual license)

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
