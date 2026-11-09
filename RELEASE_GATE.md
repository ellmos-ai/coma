# Release Gate: coma

> **Wo diese Datei liegt, hängt vom Zustand ab [U 2026-07-25].** Solange der Prozess läuft:
> im **Repo-Root**, aber „unsichtbar" öffentlich — getrackt und auffindbar, **nicht** in
> „Start here"-/Launchpad-Tabellen des READMEs beworben. Nach Abschluss (Gate erfüllt, Tag
> geschnitten): Statuswechsel zum **Zertifikat** — entweder gitignored oder in einen sichtbaren
> Unterordner verschieben (Empfehlung `docs/`), ab dann darf sie prominent verlinkt werden.
> Spätere Prüfungen werden als **neuer datierter Abschnitt angehängt**, nicht überschrieben —
> ein „Reviewed"-Datum ist ein Zeitzeuge, kein Verfallsdatum.
> Vollständige Regel und Begründung: `RELEASE-POLICY.md` §7, „Lebenszyklus des
> Release-Gate-Dokuments".

## Status

```
+------------------------------------------+
|                                          |
|          STATUS: UNLOCKED                |
|                                          |
+------------------------------------------+
```

> **LOCKED** = Repository must remain private.
> **UNLOCKED** = Repository may be set to public.

---

## Gating Rule

**This repository MUST NOT be changed to public visibility unless the status above reads UNLOCKED.**

The status may only be changed to UNLOCKED when:
1. All checklist items below are marked as PASS
2. The `final_gate_check.py` script exits with code 0
3. The responsible person has reviewed and signed off

---

## Checklist

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | `.gitignore` with minimum entries | :green_circle: PASS | All minimum entries present |
| 2 | `README.md` in English | :green_circle: PASS | Present and in English |
| 3 | `LICENSE` (MIT) present | :green_circle: PASS | LICENSE found |
| 4 | No `.db` files tracked | :green_circle: PASS | No `.db` files tracked |
| 5 | No `.env` files tracked | :green_circle: PASS | No `.env` files tracked |
| 6 | No secrets in tracked files | :green_circle: PASS | No secret patterns found |
| 7 | No hardcoded personal paths | :green_circle: PASS | No personal paths found |
| 8 | No PII patterns | :green_circle: PASS | No PII patterns found |
| 9 | No BACH-internal documents | :green_circle: PASS | No BACH-internal files |
| 10 | `TODO.md` with STATUS table | :green_circle: PASS | `TODO.md` with STATUS table present |

---

## Gate Check Execution

```
Date:       2026-11-09
Commit:     28a2248d39c172c3423e6a5f0b98727f38c426b2 (origin/main; earlier gate record: 274956d on 2026-09-12, .AI/_archive/checks/2026-10-03_1314/CHECKS-REG.md L896-917)
Script:     MODULES/_scripts/final_gate_check.py
Command:    PYTHONIOENCODING=utf-8 python final_gate_check.py --repo-path .
Exit Code:  0
Output:     Results: 10 PASS, 0 FAIL, 0 WARN — *** READY FOR PUBLIC RELEASE ***
```

---

## Sign-Off

| Field | Value |
|-------|-------|
| **Responsible** | Lukas Geiger (@lukisch) |
| **Review Date** | 2026-11-09 |
| **Decision** | UNLOCKED |
| **Remarks** | Public repository (`ellmos-ai/coma`). Gate record restored from fresh `final_gate_check.py` run on `origin/main` (`28a2248d39c172c3423e6a5f0b98727f38c426b2`) and historical register (`274956d`, 2026-09-12). |

---

*Template version: 1.0 | Source: MODULES/_templates/RELEASE_GATE_TEMPLATE.md*
