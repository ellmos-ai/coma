# Contributing to coma / Mitwirken an coma

Welcome! Contributions improve COMA's local-file job protocol, subprocess lifecycle, CLI adapters, and developer documentation. The documented behavior and limits below describe the current implementation and maintainer policies.

---

## English

### 1. General Principles & Quality Gates

1. **Local COMA boundary (`INV-COMA-02`)**: COMA uses local files and subprocesses and does not implement a network service. Launched agent CLIs may contact their providers or other services; COMA does not sandbox them or block network access. Keep the direct Python runtime dependency list empty unless a change is explicitly justified.
2. **Channel writer convention (`INV-COMA-01`)**: Callers must assign one writer per channel file. Optional role checks are not OS locking or identity enforcement; callers coordinate concurrent writers.
3. **Subprocess lifecycle (`INV-COMA-03`)**: COMA starts provider CLIs as subprocesses. Child processes inherit the launcher's privileges and environment; COMA does not create a security sandbox or drop privileges.
4. **Process-free dry runs (`INV-COMA-04`)**: Command builders (`build_cmd`, `build_session_plan`, `--dry-run`) construct argument vectors without launching the provider CLI.
5. **Provider fallback (`INV-COMA-05`)**: Candidate helpers (`ordered_candidates`, `available_candidates`) resolve CLI binaries according to the configured adapter order.
6. **Adapter opt-in (`INV-COMA-06`)**: Kimi execution through the spawner/session path requires explicit opt-in; raw adapter and probe argument builders do not enforce this gate.
7. **Probe cleanup (`INV-COMA-07`)**: Reachability probes use a timeout and best-effort platform-dependent cleanup; do not describe this as guaranteed process-tree termination.
8. **Starter generation (`INV-COMA-08`)**: Generated starter scripts (`START.bat`, `start.sh`) use marker guards to avoid overwriting customized wrappers.
9. **Inherited privileges (`INV-COMA-09`)**: Child processes inherit the launching process's privileges. COMA does not request elevation or drop privileges; it is not a security isolation boundary.
10. **Maintainer response policy (`INV-COMA-10`)**: `SECURITY.md` documents the maintainers' 48-hour acknowledgment and 5-business-day triage targets.
11. **Version freeze discipline (`T-20260920-167562623`)**: Version `0.3.2` remains frozen across manifests. Do not bump it. Document changes under ## [Unreleased] in `CHANGELOG.md`.
12. **Clean code & regression testing**: Add tests for behavioral changes in `tests/`. Keep the complete suite passing.
13. **Bilingual parity**: Maintain synchronized structure and navigation across `README.md` and `README_de.md` (18-point dual anchors `sec-01` through `sec-18`).

### 2. Local Development Workflow

~~~bash
# Install package with development dependencies
python -m pip install -e ".[test]"

# Run comprehensive test suite
python -X utf8 -m pytest -ra -v

# Run linter
python -m ruff check .

# Check bytecode compilation
python -m compileall -q coma comas tests

# Check whitespace and git diff cleanliness
git diff --check
~~~

### 3. Submission Protocol

- Open an issue for behavioral discussions before large refactoring.
- Keep provider API keys, bearer tokens, and private credentials strictly outside the repository.
- Describe changes to the documented behavior or limits in the relevant public documentation.

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore

1. **Lokale COMA-Grenze (`INV-COMA-02`)**: COMA verwendet lokale Dateien und Subprozesse und stellt keinen Netzwerkdienst bereit. Gestartete Agenten-CLIs können ihre Anbieter oder andere Dienste kontaktieren; COMA isoliert sie nicht in einer Sandbox und sperrt keinen Netzzugriff. Die Liste direkter Python-Laufzeitabhängigkeiten bleibt leer, sofern eine Änderung nicht ausdrücklich begründet ist.
2. **Kanal-Schreiberkonvention (`INV-COMA-01`)**: Aufrufer müssen jedem Kanal eine schreibende Instanz zuordnen. Optionale Rollenprüfungen sind weder Betriebssystem-Sperren noch Identitätsprüfung; parallele Schreiber müssen von den Aufrufern koordiniert werden.
3. **Subprozess-Lebenszyklus (`INV-COMA-03`)**: COMA startet Anbieter-CLIs als Subprozesse. Kindprozesse erben Rechte und Umgebung des startenden Prozesses; COMA stellt keine Sicherheitssandbox bereit und gibt keine Rechte ab.
4. **Prozessfreie Trockenläufe (`INV-COMA-04`)**: Befehlsbauer (`build_cmd`, `build_session_plan`, `--dry-run`) erzeugen Argumentvektoren, ohne das Anbieter-CLI zu starten.
5. **Provider-Fallback (`INV-COMA-05`)**: Kandidatenhelfer (`ordered_candidates`, `available_candidates`) lösen CLI-Binaries entsprechend der konfigurierten Adapterreihenfolge auf.
6. **Adapter-Opt-in (`INV-COMA-06`)**: Die Kimi-Ausführung über Spawner und Sitzungsplanung erfordert ein ausdrückliches Opt-in; rohe Adapter- und Probe-Argumentgeneratoren setzen diese Sperre nicht durch.
7. **Sondenbereinigung (`INV-COMA-07`)**: Erreichbarkeitssonden verwenden ein Timeout und eine plattformabhängige Bereinigung nach bestem Bemühen; sie garantieren keine Beendigung des gesamten Prozessbaums.
8. **Starter-Erzeugung (`INV-COMA-08`)**: Generierte Starter-Skripte (`START.bat`, `start.sh`) verwenden Schutzmarker, damit angepasste Wrapper nicht versehentlich überschrieben werden.
9. **Geerbte Rechte (`INV-COMA-09`)**: Kindprozesse erben die Rechte des startenden Prozesses. COMA fordert keine Erhöhung an und gibt keine Rechte ab; es ist keine Sicherheitsgrenze.
10. **Maintainer-Antwortpolitik (`INV-COMA-10`)**: `SECURITY.md` dokumentiert die Ziele der Maintainer: Bestätigung innerhalb von 48 Stunden und Triage innerhalb von 5 Werktagen.
11. **Versions-Freeze (`T-20260920-167562623`)**: Version `0.3.2` bleibt in allen Manifesten eingefroren. Keine Versionserhöhung vornehmen. Änderungen unter ## [Unreleased] in `CHANGELOG.md` festhalten.
12. **Sauberer Code & Regressionstests**: Verhaltensänderungen durch Tests in `tests/` absichern. Die vollständige Testsuite muss grün bleiben.
13. **Zweisprachige Parität**: Struktur und Navigation in `README.md` und `README_de.md` synchron halten (18 duale Anker `sec-01` bis `sec-18`).

### 2. Lokaler Entwicklungsablauf

~~~bash
# Entwicklungsumgebung einrichten
python -m pip install -e ".[test]"

# Vollständige Testsuite ausführen
python -X utf8 -m pytest -ra -v

# Linter-Prüfung
python -m ruff check .

# Bytecode-Kompilierung
python -m compileall -q coma comas tests

# Diff- und Whitespace-Prüfung
git diff --check
~~~

### 3. Einreichung

- Vor größeren Verhaltensänderungen ein Issue zur Abstimmung anlegen.
- LLM-API-Schlüssel, Zugriffstoken und vertrauliche Daten niemals ins Repository committen.
- Änderungen an beschriebenem Verhalten oder Grenzen in der passenden öffentlichen Dokumentation erläutern.
