# TODO.md — Active work

**Version:** 0.3.2
**Updated:** 2026-10-11
**Reason:** Current implementation scope, documentation accuracy, and repository hygiene
**Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Spawner & Adapters | DONE | Command construction and mocked execution are covered; prior Claude/Codex/AGY checks are historical compatibility notes, not current certification. Kimi remains unverified and fail-closed by default. |
| Multi-Channel Job Protocol | DONE | IN/OUT/DONE queues and channel files; callers assign one writer per channel. Role checks are not OS locks or identity enforcement. |
| Session Planning & Probing | DONE | Session planning constructs argv; reachability probes use a timeout and best-effort platform-dependent cleanup. Descendant termination is not guaranteed. |
| Starters Generator | DONE | Dual-platform `START.bat` and `start.sh` generation from module `roles[]` with idempotent marker guards. |
| Path Neutrality & Hygiene | DONE | Reviewed tracked files for known host-path patterns and common credential markers; this bounded check does not certify that no secrets exist. |
| AI Discoverability & Metadata | DONE | Machine-readable `llms.txt`, PEP 621 classifiers, PEP 639 license inventory, schema v2 metadata parity. |
| CI Workflows & Multi-Host Defense | DONE | Multi-OS/Python GitHub Actions with timeouts, stale triage workflow, hardened .gitignore. |
| Ecosystem Integration | DONE | Public repositories document optional integrations and specific use points; they do not imply hard dependencies. |
| Public source and package status | CURRENT | GitHub source is public; version 0.3.2 remains frozen. Install from the canonical Git repository; the PyPI name coma belongs to a different project. |

## Formalized next tasks

- [ ] **TASK-COMA-01: Kimi-Live-Verifikationsgate** (`effort=special`, `scope=kimi`, priority `normal`).
  - **Ziel:** Sobald die aktuelle `kimi-code`-Nachfolge-CLI über einen autorisierten interaktiven Promptlauf-Vertrag verfügt, Verifikationsflag in `coma/session.py` und `coma/adapters/kimi.py` von Skeleton auf Verified heben. Der frühere Check von `kimi-cli` 0.31.0 (archiviert am 2026-09-23) belegt keine Kompatibilität mit dem Nachfolger.
  - **Definition of Done:** End-to-End-Test mit der aktuellen `kimi-code`-CLI nach einem autorisierten Promptlauf-Vertrag; aktuelle Adaptergrenzen in `KONZEPT.md` dokumentieren.

- [ ] **TASK-COMA-02: Zentrale Multi-Agent-Registry** (`effort=large`, `scope=registry`, priority `normal`).
  - **Ziel:** Zentrale Schnittstelle für die Orchestrierung dynamischer Agentenflotten über COMA-Prozess-Spawner.
  - **Definition of Done:** Anbindung an `agent-ops-stack` und `system-explorer`.

- [x] **TASK-COMA-03: Provider-neutrale Session-Planung & Starters (v0.3.0)** (`effort=medium`, `scope=session`, priority `high`).
  - **Ergebnis:** `build_session_plan`, `ordered_candidates`, `probe`, `starters generate` integriert; 260 Tests grün.

- [x] **TASK-COMA-04: Release-Hygiene, Lizenzinventar & Gate-Bereitschaft (v0.3.0)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Ergebnis:** Standard-`TODO.md` mit `## STATUS`-Tabelle etabliert, `THIRD_PARTY_LICENSES.md` angelegt, `.gitignore` um Mindesteinträge gehärtet, `final_gate_check.py` auf 10/10 PASS gebracht.

- [x] **TASK-COMA-05: Pfad A Technische Hygiene, CI-Workflow & Multi-Host-Härtung (v0.3.1)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Ergebnis:** GitHub Actions Test- & Stale-Workflows mit Timeout- und Concurrency-Härtung, erweiterte Multi-Host- und Lock-Defense in `.gitignore`, PEP 621 LLM-Ready Metadaten, Pytest Runner-Flags, 270 automatisierte Vertragstests (100% grün).

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
