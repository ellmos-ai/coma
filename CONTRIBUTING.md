# Contributing to coma / Mitwirken an coma

Welcome! We welcome contributions to `coma` (Command & Communication for Autonomous Agents). To maintain deterministic session decoupling, air-gapped process isolation, single-writer filesystem safety, and compliance across multi-host environments, all contributions must adhere to the quality standards and operational invariants defined below.

---

## English

### 1. General Principles & Quality Gates
1. **Local-First & Zero-Egress (`INV-COMA-02`)**: Core library and CLI logic must operate strictly offline by default. Zero external runtime dependencies; 100% Python standard library. Never introduce telemetry, outbound sockets, or external network requests.
2. **Single-Writer Rule (`INV-COMA-01`)**: Exactly one writer per channel file (`IN/`, `OUT/`, `DONE/`), eliminating race conditions and lock contention.
3. **Session Decoupling & RC Immunity (`INV-COMA-03`)**: Subprocesses spawn in dedicated process trees outside interactive terminal sessions, bypassing remote-control permission stalls.
4. **Process-Free Dry Runs (`INV-COMA-04`)**: Command builders (`build_cmd`, `build_session_plan`, `--dry-run`) must construct argument vectors without launching processes or consuming LLM tokens.
5. **Deterministic Multi-Provider Fallback (`INV-COMA-05`)**: Candidate chain (`ordered_candidates`, `available_candidates`) resolves CLI binaries systematically across Claude Code, Codex, AGY, and Kimi.
6. **Fail-Closed Provider Safety (`INV-COMA-06`)**: Unverified or experimental adapters remain strictly fail-closed unless callers explicitly opt in with an established contract.
7. **Bounded Probe Cleanup (`INV-COMA-07`)**: Reachability probes enforce strict execution timeouts and guarantee child-process termination to prevent zombie processes.
8. **Idempotent Dual-Platform Starters (`INV-COMA-08`)**: Generated starter scripts (`START.bat`, `start.sh`) carry unique marker guards preventing accidental overwrites of custom wrappers.
9. **Unprivileged User-Mode Execution (`INV-COMA-09` / `RunAsInvoker`)**: Core process management, job board polling, and CLI execution run strictly in unprivileged user space without administrative elevation.
10. **48h Security & Governance SLA (`INV-COMA-10`)**: Maintain 48h acknowledgment and 5-business-day triage commitments for security reports.
11. **Version Freeze Discipline (`T-20260920-167562623`)**: Version 0.3.2 is strictly frozen across all manifests. Do not bump the version string. Document all advancements under `## [Unreleased]` in `CHANGELOG.md`.
12. **Clean Code & Regression Testing**: Every feature or fix must include regression tests in `tests/`. Keep test coverage at 100% pass rate.
13. **Bilingual Parity**: Maintain synchronized structural and navigational parity across `README.md` and `README_de.md` (18-point dual anchors `sec-01` through `sec-18`).

### 2. Local Development Workflow
```bash
# Install package with development dependencies
python -m pip install -e ".[test]"

# Run comprehensive test suite
python -X utf8 -m pytest -ra -v

# Run linter
python -m ruff check .

# Check bytecode compilation
python -m compileall -q .

# Check whitespace and git diff cleanliness
git diff --check
```

### 3. Submission Protocol
- Open an issue for behavioral discussions before large refactoring.
- Keep provider API keys, bearer tokens, and private credentials strictly outside the repository.
- Ensure all 10 governance invariants (`INV-COMA-01` to `INV-COMA-10`) remain VERIFIED.

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore
1. **Local-First & Zero-Egress (`INV-COMA-02`)**: Sämtliche Kernbibliotheken und CLI-Abläufe arbeiten standardmäßig zu 100% offline ohne Telemetrie, Sockets oder externe Datenübertragung. Null externe Laufzeitabhängigkeiten, 100% Python Standard-Bibliothek.
2. **Single-Writer-Regel (`INV-COMA-01`)**: Genau ein Schreiber pro Kanal-Datei (`IN/`, `OUT/`, `DONE/`), wodurch Race Conditions und Lock-Konflikte strukturell ausgeschlossen werden.
3. **Sitzungsentkopplung & RC-Immunität (`INV-COMA-03`)**: Subprozesse starten in isolierten Prozessbäumen außerhalb interaktiver Terminal-Sessions.
4. **Prozessfreie Trockenläufe (`INV-COMA-04`)**: Kommandokonstruktion (`build_cmd`, `build_session_plan`, `--dry-run`) erzeugt verifizierte argv-Vektoren ohne Prozessstart und ohne Token-Verbrauch.
5. **Deterministischer Multi-Provider-Fallback (`INV-COMA-05`)**: Systematische Adapter-Kandidatenkette über Claude Code, Codex, AGY und Kimi.
6. **Fail-Closed Provider-Sicherheit (`INV-COMA-06`)**: Unverifizierte oder experimentelle Adapter bleiben strikt fail-closed, sofern kein expliziter Opt-in vorliegt.
7. **Terminierende Sondenbereinigung (`INV-COMA-07`)**: Erreichbarkeitssonden erzwingen strikte Timeouts und garantieren die Beendigung von Kindprozessen zur Vermeidung von Zombie-Prozessen.
8. **Idempotente Plattform-Starter (`INV-COMA-08`)**: Generierte Starter-Skripte (`START.bat`, `start.sh`) besitzen eindeutige Schutzmarker gegen versehentliches Überschreiben manueller Wrapper.
9. **Unprivilegierte Benutzer-Ausführung (`INV-COMA-09` / `RunAsInvoker`)**: Sämtliche Prozess-, Job- und CLI-Aufrufe laufen strikt im unprivilegierten Standard-Benutzerkontext ohne administrative Rechte oder UAC-Elevation.
10. **48h Sicherheits- & Governance-SLA (`INV-COMA-10`)**: Einhaltung von 48h Reaktionszeit und 5 Werktagen Triage-Frist für Sicherheitsmeldungen.
11. **Strikte Versions-Freeze-Disziplin (`T-20260920-167562623`)**: Version 0.3.2 bleibt in allen Manifesten eingefroren. Keine Versionserhöhung vornehmen; alle Änderungen unter `## [Unreleased]` in `CHANGELOG.md` festhalten.
12. **Testabdeckung & Regressionstests**: Für jede Verhaltensänderung ist ein Vertragstest in `tests/` zu ergänzen. Die Testsuite muss zu 100% grün bleiben.
13. **Zweisprachige Dokumentationsparität**: `README.md` und `README_de.md` müssen strukturgleich und mit synchronen 18-Punkte-HTML-Ankern (`sec-01` bis `sec-18`) gepflegt werden.

### 2. Lokaler Entwicklungsablauf
```bash
# Entwicklungsumgebung einrichten
python -m pip install -e ".[test]"

# Vollständige Testsuite ausführen
python -X utf8 -m pytest -ra -v

# Linter-Prüfung
python -m ruff check .

# Bytecode-Kompilierung
python -m compileall -q .

# Diff- und Whitespace-Prüfung
git diff --check
```

### 3. Einreichung
- Vor größeren Eingriffen ein Issue zur Abstimmung anlegen.
- LLM-API-Schlüssel, Zugriffstoken und vertrauliche Daten niemals ins Repository committen.
- Alle 10 Invarianten (`INV-COMA-01` bis `INV-COMA-10`) müssen erfüllt bleiben.
