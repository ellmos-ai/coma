# TODO.md — Active work

**Version:** 0.3.0  
**Updated:** 2026-09-12  
**Reason:** Standardization, path neutrality, gate readiness, and AI discoverability  
**Purpose:** Track only work that remains open.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Core Spawner & Adapters | DONE | Process-free command generation, mocked runner execution, Claude/Codex/AGY verified, Kimi fail-closed; verified by 260 automated tests (100% green). |
| Multi-Channel Job Protocol | DONE | IN/OUT/DONE queues, single-writer channels (`coma.<jobid>.json`, `to-agent.jsonl`, `from-agent.jsonl`, `result.md`, `console.log`), atomic moves. |
| Session Planning & Probing | DONE | Process-free `build_session_plan`, deterministic `ordered_candidates`, bounded reachability `probe` with child-process cleanup. |
| Starters Generator | DONE | Dual-platform `START.bat` and `start.sh` generation from module `roles[]` with idempotent marker guards. |
| Path Neutrality & Hygiene | DONE | Neutral environments, standard `.gitignore` patterns, zero personal paths, zero secrets. |
| AI Discoverability & Metadata | DONE | Machine-readable `llms.txt`, PEP 621 classifiers, PEP 639 license inventory, schema v2 metadata parity. |
| Ecosystem Integration | DONE | Registered in `.MODULES/.ORCHESTRATION/coma`, Plan-D pointer configured, shared under `ellmos-ai` and `open-bricks`. |
| Public Release Gate | USER | MIT License selected; explicit public visibility approval pending from user. |

## Formalized next tasks

- [ ] **TASK-COMA-01: Kimi-Live-Verifikationsgate** (`effort=special`, `scope=kimi`, priority `normal`).
  - **Ziel:** Sobald Kimi Code CLI über einen autorisierten interaktiven Promptlauf-Vertrag verfügt, Verifikationsflag in `coma/session.py` und `coma/adapters/kimi.py` von Skeleton auf Verified heben.
  - **Definition of Done:** End-to-End Test mit Kimi-CLI-Prozess in isolierter Sandbox; Dokumentation in `BEFUNDE.md` und `KONZEPT.md`.

- [ ] **TASK-COMA-02: Zentrale Multi-Agent-Registry** (`effort=large`, `scope=registry`, priority `normal`).
  - **Ziel:** Zentrale Schnittstelle für die Orchestrierung dynamischer Agentenflotten über COMA-Prozess-Spawner.
  - **Definition of Done:** Anbindung an `agent-ops-stack` und `system-explorer`.

- [x] **TASK-COMA-03: Provider-neutrale Session-Planung & Starters (v0.3.0)** (`effort=medium`, `scope=session`, priority `high`).
  - **Ergebnis:** `build_session_plan`, `ordered_candidates`, `probe`, `starters generate` integriert; 260 Tests grün.

- [x] **TASK-COMA-04: Release-Hygiene, Lizenzinventar & Gate-Bereitschaft (v0.3.0)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Ergebnis:** Standard-`TODO.md` mit `## STATUS`-Tabelle etabliert, `THIRD_PARTY_LICENSES.md` angelegt, `.gitignore` um Mindesteinträge gehärtet, `final_gate_check.py` auf 10/10 PASS gebracht.

---
<!-- REMEMBER: ENDUSERTEXTE BEKOMMEN ECHTE UMLAUTE Ü Ö Ä ß -->
