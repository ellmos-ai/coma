# Changelog — COMA

All notable changes to COMA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bilingual Mermaid lifecycle sequence diagram (`sequenceDiagram`) with autonumbering and strict label quoting in `README.md` and `README_de.md` per HOOK-BANNER-ASSET-01.
- Governance and Runtime Invariants section (`INV-COMA-01` to `INV-COMA-08`) documenting single-writer channels, zero network egress, headless/interactive decoupling, and bounded probe cleanup.
- Dedicated repository-level `MARKETING-LOG.txt` outlining target personas, SEO discoverability keywords, community directory submissions, and integration blueprints.
- Standard PEP 621 URLs in `pyproject.toml` (Homepage, Repository, Documentation, Issues, Changelog, Security, Marketing Log, Parent Organization, Umbrella Ecosystem).
- Extended test coverage in `tests/test_metadata.py` verifying PEP 621 URLs, sequence diagrams, invariants, and MARKETING-LOG structure (260 passed tests).

### Changed
- Synchronized Pytest status badges across English and German documentation to 260 passed unit tests.
- Enhanced quick navigation tables of contents with bilingual anchor parity.
- Updated `SECURITY.md` supported versions table to include `0.3.x`.
- Updated `llms.txt` with Last-checked date (2026-09-10), 260 verified unit tests, and session planning / starter generation context.

## [0.3.0] — 2026-09-09

### Added
- Process-free `build_session_plan()` API for interactive and headless Claude,
  Codex, AGY and fail-closed Kimi sessions.
- Provider capability records, deterministic fallback candidates and a bounded
  read-only probe with child-process cleanup.
- `coma session` CLI with dry-run support; role prompt files and user requests
  stay separate.

### Changed
- Capability help contracts reflect Claude Code 2.1.263, Codex CLI 0.153.4,
  agy 1.1.27 and Kimi 0.31.0 as observed on 2026-09-09. Kimi remains
  unverified for real prompt execution.

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
