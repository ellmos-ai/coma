# Third-Party Licenses & Software Inventory

**Project:** `coma`  
**License:** [MIT License](LICENSE)  
**Audit Date:** 2026-09-12  
**Status:** Invariant Confirmed — Zero External Runtime Dependencies (INV-COMA-02)  

---

## Runtime Architecture & Dependencies

`coma` is engineered as a provider-independent agent lifecycle and orchestration interface. To preserve maximum operational reliability across multi-agent environments (Claude, Codex, Antigravity, Kimi), ensure deterministic multi-OS execution (Windows, Linux, macOS), and eliminate external supply-chain attack vectors, `coma` enforces a strict **Zero-Runtime-Dependency** invariant (**INV-COMA-02**).

### Runtime Dependencies

| Package | Version Spec | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| *(None)* | `N/A` | `N/A` | `runtime` | 100% pure Python standard library (`subprocess`, `os`, `sys`, `pathlib`, `json`, `time`, `threading`, `shutil`, `dataclasses`, `typing`, `logging`, `stat`, `re`) |

All core subsystems—including `JobBoard`, `JobRunner`, CLI adapters (`ClaudeAdapter`, `CodexAdapter`, `AgyAdapter`, `KimiAdapter`), process spawning (`Spawner`), session planning (`build_session_plan`), reachability probing (`probe`), and starter generation (`generate_starters`)—run entirely on the Python Standard Library without third-party wheels or runtime packages.

---

## Development & Test Dependencies

The following tools and libraries are utilized exclusively during development, code style verification, packaging, and automated contract testing:

| Package / Tool | Version Spec | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [pytest](https://pytest.org/) | `>=8.0.0` | MIT | `[test]` | Automated unit, contract, regression, and metadata test execution |
| [ruff](https://github.com/astral-sh/ruff) | `>=0.5.0` | MIT OR Apache-2.0 | `[dev]` | High-performance Python linter, style enforcer, and AST validation |
| [setuptools](https://github.com/pypa/setuptools) | `>=77.0.0` | MIT | `[build-system]` | Standard PEP 517/PEP 621 build backend and packaging |
| [wheel](https://github.com/pypa/wheel) | `>=0.40.0` | MIT | `[build-system]` | Standard wheel distribution format builder |

---

## External Tools & Binaries (System Level)

| Binary / Tool | Verified Version | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [Python](https://www.python.org/) | `>=3.10` | PSF License | System Runtime | Multi-OS execution environment (`Windows`, `Linux`, `macOS`) |
| [Git](https://git-scm.com/) | `>=2.40` | GPL-2.0 | Version Control | Plan-D source-of-truth management and release tagging |
| [claude](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code) | `2.1.263` | Proprietary | Agent CLI | Anthropic Claude Code CLI adapter target |
| [codex](https://github.com/openai/codex) | `0.153.4` | Proprietary | Agent CLI | OpenAI Codex CLI adapter target |
| [agy](https://github.com/google/antigravity) | `1.1.27` | Proprietary | Agent CLI | Google Antigravity CLI adapter target |
| [kimi](https://github.com/moonshot-ai/kimi-code) | `0.31.0` | Proprietary | Agent CLI | Kimi Code CLI skeleton adapter target (fail-closed) |

---

## License Texts & Attribution

### MIT License (`coma`, `pytest`, `setuptools`, `wheel`, `ruff`)

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

### Python Software Foundation License (PSF) (`Python Standard Library`)

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
