# COMA — COMmunication for Autonomous Subagents

> Konzept und Abgrenzung. Grundentscheidungen stammen vom 2026-07-26; historische
> Stände aus 2026-08 sind als damalige Beobachtungen gekennzeichnet. Dieses Dokument
> wurde am 2026-10-11 mit dem aktuellen Umfang abgeglichen. COMA 0.3.2 bleibt eingefroren.
> Aktuelle Nutzung: README.md und README_de.md; Sicherheits- und Meldewege: SECURITY.md;
> offene Arbeit: TODO.md.

## Was COMA ist

COMA ist die Lebenszyklus-Schicht für Agentenprozesse: Sie startet konfigurierte
CLI-Prozesse und stellt Datei- und Polling-Schnittstellen bereit, über die ein
aufrufendes System Aufträge und Ergebnisse austauschen kann.

| Zuständigkeit | Aufgabe | System |
|---|---|---|
| Lebenszyklus | Prozesse starten, Status und Ergebnisse bereitstellen | COMA |
| Autorisierung und Koordination | Zugriffsentscheidungen und Arbeitszuweisung | Aufrufendes System |
| Gedächtnis und Verlauf | Vorherige Versuche und Ergebnisse bewahren | Aufrufendes System |

COMA erzwingt keine Berechtigungen, verwaltet keine zentrale Agenten-Registry und
speichert kein dauerhaftes Gedächtnis. Integrationen bleiben optional; sie erzeugen
keine harte Abhängigkeit zwischen COMA und anderen Projekten.

## Prozess-, Netzwerk- und Berechtigungsgrenzen

COMA verwendet konfigurierte lokale Dateien und startet Subprozesse. Es stellt selbst
keinen Netzwerkdienst bereit. Gestartete Agenten-CLIs können ihre Anbieter oder andere
Dienste kontaktieren. Sie erben die Rechte und die Umgebung des startenden Prozesses.
COMA stellt weder eine Sandbox noch eine Netzsperre, einen Air-Gap oder eine
Berechtigungsgrenze bereit.

Die Adapter bauen CLI-Argumente. Die jeweilige Agenten-CLI bestimmt, wie sie diese
Argumente durchsetzt. In der konfigurierten Claude-Standardvariante setzt COMA
`dontAsk` mit den Werkzeugen Read, Edit, Write, Bash, Glob und Grep; das separate
`read_only`-Preset beschränkt die Werkzeugliste auf Read, Glob und Grep. MCP ist in
der Standardvariante aus. `bat_compat` verwendet `bypassPermissions` und kann
umfassendere Ausführungsmöglichkeiten einschließlich MCP zulassen. Beim Codex-Adapter
ist `read-only` der Standard; `write` wird als `workspace-write` abgebildet.
`danger-full-access` ist ausdrücklich konfigurierbar. Diese CLI-Profile ersetzen
keine Prozess- oder Netzwerksandbox.

Der Session-Probe startet die konfigurierte CLI mit Timeout und versucht die
plattformabhängige Bereinigung bestmöglich. Die Beendigung des gesamten Prozessbaums
ist nicht garantiert. Der bestehende Probe-Test startet für seine Kontrollprüfung
einen lokalen Python-Prozess und prüft den erwarteten Token-Rückgabewert; er ist kein
Live-Test eines Anbieter-CLIs.

## Datei- und Kanalprotokoll

| Datei | Protokollrolle |
|---|---|
| `IN/<jobid>.md` | Auftrag |
| `OUT/<jobid>.result.md` | Ergebnis |
| `coma.<jobid>.json` | Status; vom Runner geschrieben |
| `coma.<jobid>.from-agent.jsonl` | Fortschritt; vom Agenten geschrieben |
| `coma.<jobid>.to-agent.jsonl` | Nachrichten; vom Orchestrator geschrieben |
| `coma.<jobid>.console.log` | Laufzeit-Ausgabe |
| `DONE/<jobid>.md` | Abgeschlossener Auftrag |

Aufrufende Systeme müssen pro Kanal einen Schreiber zuordnen. Optionale Rollenprüfungen
sind weder OS-Sperren noch Identitätsprüfungen; mehrere Prozesse mit derselben Rolle
werden nicht gegenseitig ausgeschlossen. Aufrufende Systeme koordinieren konkurrierende
Schreibvorgänge selbst. JSONL ermöglicht zeilenorientierte Anhänge, garantiert aber
keine prozessübergreifende Synchronisierung für alle Dateisysteme.

## Kimi-Adapterstatus

Der Kimi-Adapter bleibt unbestätigt. Die Ausführung über Spawner und Session erfordert
ein ausdrückliches Opt-in; direkte KimiAdapter- oder Probe-Argument-Aufrufe setzen
diese Grenze nicht selbst durch. Der frühere Kompatibilitätscheck mit Version 0.31.0
bezog sich auf das inzwischen archivierte legacy kimi-cli (2026-09-23). Er belegt keine
Kompatibilität mit dem Nachfolger kimi-code. Eine aktuelle Nachfolgerprüfung bleibt
TASK-COMA-01 in TODO.md; bis dahin werden weder aktuelle Live-Unterstützung noch
Kompatibilität behauptet.

## Historischer Anlass und Entwurfsentscheidungen

Am 2026-07-26 wurde in einer Remote-Control-Arbeitssitzung beobachtet, dass ein
konkreter Agentenlauf auf eine Freigabe wartete. Ein damals gestarteter lokaler
Selbsttest und ein einzelner Auftrag liefen durch. Das ist eine historische lokale
Beobachtung, kein Nachweis für aktuelle Anbieter-Kompatibilität und keine Aussage,
dass COMA Freigaben umgeht oder Agenten unbeaufsichtigt sicher macht. Früher zitierte
Issue- und Laufzeitbeobachtungen werden hier nicht als aktuelle Anbieterzustände
ausgegeben.

Die Trennung als eigenes Modul sollte den Prozesslebenszyklus von Orchestrierung,
Rechteverwaltung und Erinnerung trennen. COMA kann von anderen Projekten optional
genutzt werden; für die konkrete Nutzerliste und ihre Integrationsstellen siehe
README.md und README_de.md.

Ein Snapshot vom 2026-08-20 bezeichnete Version 0.2.1 als erweitert, notierte damals
243 Tests sowie damalige Claude-, Codex- und AGY-Adapterchecks. Diese datierten Zahlen
und Checks sind historische Angaben, keine aktuellen Testzahlen, Zertifizierungen oder
Live-Anbieterprüfungen.

## Historische Not-Aus-Diskussion

Eine frühe Entwurfsnotiz vom 2026-07-26 schlug einen externen Workflow-Hook als
zusätzlichen Abbruchweg vor. COMA liefert WorkflowHooker nicht mit und integriert ihn
nicht. Diese historische Empfehlung ist kein Bestandteil des COMA-Protokolls und keine
Sicherheitsgarantie.

## Lizenzhinweis und aktueller Arbeitsstand

Das COMA-Projekt wird unter der MIT-Lizenz bereitgestellt. Ob gesetzliche Regeln wie
§ 521 BGB auf ein konkretes Rechtsverhältnis anwendbar sind, hängt vom Rechtsverhältnis
und dem anwendbaren Recht ab; dieses Dokument gibt keine pauschale Haftungsfreistellung.

TODO.md ist die aktuelle Aufgabenübersicht. Historische Arbeitsstände und
Implementierungsentscheidungen werden dort nicht als gegenwärtige Runtime-Garantien
fortgeschrieben.
