# Changelog — COMA

All notable changes to COMA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] — 2026-08-16

### Added
- Dedicated security policy (`SECURITY.md`) outlining process boundaries, single-writer invariants, and vulnerability reporting.
- Automated metadata, schema, and manifest parity test suite in `tests/test_metadata.py` (5/5 passed).
- Sibling ecosystem cross-linking table in `README.md` and `README_de.md` linking `ellmos-ai` and `dev-bricks` tools.
- Badges for Version, Dependencies, and Pytest status (241 passed) in both English and German documentation.
- Standard `[tool.ruff]` and `[tool.ruff.lint]` configuration in `pyproject.toml`.

### Changed
- Updated `llms.txt` Last-checked timestamp to 2026-08-16 and test count to 241 passed Pytest unit tests.

## [0.2.0] — 2026-07-26

### Added
- Name migration from COMAS to COMA with backwards-compatibility aliases (`comas` CLI and package imports).
- Agent Spawner layer supporting `ClaudeAdapter`, `CodexAdapter`, `AntigravityAdapter`, and `KimiAdapter`.
- Session-decoupled file-based Job Board protocol (`IN/`, `OUT/`, `DONE/`).
- Vendor manifest check and check command (`coma vendor`, `coma check`).
