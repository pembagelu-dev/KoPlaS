# KoPlaS – Kolloquiumsplanung

KoPlaS unterstützt Schulen bei der Planung mündlicher Prüfungen und Kolloquien. Die Anwendung importiert Prüfungs- und Lehrkräftedaten, erstellt mit einem Solver einen Zeit- und Raumplan und ermöglicht anschließend manuelle Anpassungen in einer grafischen Oberfläche.

Die Bedienoberfläche und die Exportdokumente sind auf deutschsprachige Schulen ausgerichtet.

## Funktionen

- Import von Prüfungsdaten sowie Lehrkräfte- und Oberstufenkursdaten aus ASV-bezogenen CSV-Dateien
- Automatische Planung von Prüfungszeiten und Räumen mit CP-SAT- und MIP-Optimierung
- Konfigurierbare harte und weiche Planungsbedingungen, darunter Tages- und Wochenregeln, Abstände, Verfügbarkeiten und Prüfungsblöcke
- Manuelle Anpassung des Plans per Drag-and-drop mit laufender Konfliktprüfung
- Prüfungsblöcke mit bis zu fünf gekoppelten Prüfungen
- Bearbeitung von Räumen, Zeiten, Lehrkräften und Bedingungen; Einstellungen werden gespeichert
- Undo und Redo für Änderungen in der Slotplanung
- Berücksichtigung von Nachteilsausgleichen (NTA) bei Vorbereitungszeiten
- Export als Word-Plan für Lehrkräfte, Schüler und Reinigungspersonal
- Excel-Export mit auswählbaren Spalten
- Statistik- und Belastungsreport für Lehrkräfte

## Voraussetzungen

KoPlaS benötigt Python und folgende Pakete:

- PySide6
- pandas
- OR-Tools
- python-docx
- openpyxl

Eine virtuelle Umgebung und die Installation der Pakete lassen sich beispielsweise so einrichten:

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Anschließend die Abhängigkeiten installieren:

```bash
python -m pip install PySide6 pandas ortools python-docx openpyxl
```

## Module

| Datei | Aufgabe |
| --- | --- |
| `KoPlaS.py` | Grafische Desktop-Anwendung, Datenverwaltung, interaktive Planung und Exportsteuerung |
| `kolloPlaner.py` (0.2 Build 13) | Solver-Logik für die Zeit- und Raumplanung mit CP-SAT und MIP |
| `import_asv.py` (0.1 Build 6) | Einlesen und Umformen von ASV-CSV-Daten für den Import in den Planungsablauf |
| `export.py` (0.1 Build 14) | Erzeugung der Word-Pläne und Excel-Tabellen |
| `report.py` (0.3 Build 9) | Erstellung des Word-Statistik- und Belastungsreports |

## Hinweise

- Der Solver berücksichtigt harte Bedingungen zwingend und verwendet weiche Bedingungen zur Bewertung beziehungsweise Optimierung von Planvarianten.
- Die grafische Oberfläche unterstützt die Prüfung von Konflikten auch nach manuellen Änderungen.
- Für die Word- und Excel-Ausgaben müssen `python-docx` beziehungsweise `openpyxl` installiert sein.
- Der reguläre Planungsablauf erfolgt über die grafische Oberfläche. Die übrigen Python-Dateien stellen dafür Import-, Solver-, Export- und Reportfunktionen bereit.

## Version und Änderungshistorie

**Aktuelle Version: 1.2.10 (Build 56); Solver: 0.2 (Build 17)**

Live-Prototyp `Koplas-Test.py`: **1.2.10 (Build 53)**.

### Version 1.2.10

- Einstellungen → Zeit: Vorbereitungsdauer (1–600 Minuten) und Puffer bis zur Prüfung (0–600 Minuten) sind unabhängig einstellbar und werden mit dem Plan gespeichert. Alte Pläne behalten 30 Minuten Vorbereitung und 5 Minuten Puffer. NTA verlängert nur die Vorbereitungsdauer; Word-Vorbereitungsangaben sowie Excel-Vorbereitungs- und Absperrzeiten verwenden die neuen Werte. Prüfungszeiten und Platzierungen bleiben unverändert.
- Geprüft mit allen vier vorhandenen Plänen (772 Platzierungen): sechs Zeitkombinationen je Plan, 96 Word-/Excel-Exporte, NTA- und Absperrzeiten sowie Speichern/Laden. Die Originalpläne blieben unverändert.

- Einstellungen → Zeit: Änderungen erhalten Prüfungen und ihre Slot-/Raumzuordnungen; Uhrzeiten und Konfliktanzeigen werden aktualisiert. Wochenstartdaten müssen Montage sein, Woche 2 nach Woche 1 liegen und der letzte Slot vor Mitternacht enden. Während eines Solverlaufs sind Zeitänderungen gesperrt; ungültige Einstellungen werden nicht übernommen.

- Einstellungen → Zeit: Eine kleinere Slotzahl wird nur übernommen, wenn alle entfallenden Slots in beiden Wochen und allen Räumen unbelegt sind. Andernfalls nennt eine Meldung die betroffenen Termine; die Einstellungen bleiben erhalten. Zusätzliche Slots werden am Tagesende angefügt. Startzeit, Slotlänge und Pause bleiben veränderbar.

- Wordexport: Höhenreserve berücksichtigt geerbte Absatzabstände und einen kleinen definierten Abstand zum Infotext. Der Hinweis bleibt mit der letzten Tabellenzeile zusammen und wandert bei Bedarf mit ihr auf die Folgeseite.

- Wordexport: Tageshöhen werden anhand tatsächlicher Tabellenzeilen und geschätzter Umbrüche angepasst; ab 14 Datenzeilen werden Zeilen und Schriften kompakter, mindestens 8 pt. Reicht eine Seite nicht aus, setzt sich der Tag mit wiederholtem Tabellenkopf auf Folgeseiten fort. Ganze Datenzeilen bleiben zusammen.

- Wordexport: Datenzellen sind horizontal und vertikal zentriert, mit symmetrischen Innenabständen und ohne zusätzliche Absatzabstände. Die Überschrift „Raum“ passt sich der Spaltenbreite an und bleibt einzeilig; mindestens 8 pt bleiben erhalten.

- Wordexport: Ab sechs Slots passen alle drei Pläne sämtliche Tabellenspalten an die verfügbare Seitenbreite an. Zell- und Überschriftenschriften werden proportional verkleinert, mindestens auf 8 pt; Umbrüche und wachsende Zeilen sind erlaubt. Bis fünf Slots bleibt das Layout unverändert.

- Rechte Seitenleiste auf 230 Pixel verbreitert und vertikal geteilt: oben „Ablage“, unten alle Lehrkräfte mit Belastungswerten. Die schreibgeschützte Tabelle aktualisiert sich bei Datenänderungen und ist nach Kürzel oder numerischer Belastung sortierbar; das Höhenverhältnis ist verstellbar.

- Solver-Ergebnisdialog: 50 % breiter; aufgeklappter Detailtextbereich 50 % höher, auch bei erneutem Aufklappen.

- Live-Prototyp: Fensterbreite am aktuellen `LOG_WIDTH_REFERENCE` ausgerichtet; Anfangshöhe um 50 % erhöht, Protokollanteil unverändert.

- Solver-Fortschritt: Anzeige maximal paralleler Prüfungen und ungenutzte Hilfsfunktionen entfernt; „genutzte Räume“ bleibt erhalten.

- Live-Prototyp: Vor einem erneuten gültigen Solverstart wird das Protokoll geleert, sofern es Ausgaben eines früheren Solverlaufs enthält. Abgelehnte Starts erhalten das Protokoll. Gesperrte Tage bleiben im Live-Raster weiß sichtbar und können nicht belegt werden.

- Feedbacktexte nennen Engpass, entscheidende Zahlen und Handlungsmöglichkeiten kompakt; Handlungshinweise verwenden die höfliche Anrede „Sie“. Der Ergebnisdialog zeigt nur Status und Hinweisanzahl. Konkrete Meldungen stehen ausschließlich unter „Details“; im GUI-Solverlog bleiben Fortschritt und eine kurze Ergebnismeldung.

- Unlösbare Zeitpläne erhalten konkrete Befunde aus den importierten Prüfungen und aktiven Bedingungen: fehlende Raumslots, fehlende gemeinsame Prüfungstage, rollenübergreifende Personenbelastung, Tages- und Einsatztagelimits, Wochenregel, Schülerabstände und Kopplungsblöcke. Die Hinweise nennen Personen, Prüfungs-IDs, Kapazitäten und passende Einstellungen.
- Erklären die Kapazitäts- und Verfügbarkeitsprüfungen keinen einzelnen Widerspruch, untersucht der Solver nach einem nachgewiesen unlösbaren Lauf separate Varianten mit gezielten Lockerungen. Das zusätzliche Diagnosebudget beträgt insgesamt etwa 12 Sekunden einschließlich Modellaufbau, höchstens 2 Sekunden Suchzeit je Variante; ein bereits begonnener Modellaufbau kann darüber hinaus dauern. Erfolgreiche Varianten, weiterhin unlösbare Varianten und ungeklärte Zeitlimits werden getrennt ausgewiesen. Nutzerbedingungen bleiben unverändert; die Varianten bestätigen nur die Lösbarkeit des Zeitmodells, nicht die anschließende Raumvergabe.
- Der Abschlussbericht unterscheidet nachgewiesene Unlösbarkeit, fehlende Lösung innerhalb der Rechenzeit, ungültige Modelle und gültige Zeitpläne. Ein erfolgloser Lauf ersetzt den vorhandenen Plan nicht.
- Bei einem gültigen Plan nennt der Bericht konkrete Abweichungen bei gewünschten Schülerabständen, Start in Slot 2, Tageszielwerten und den optimierten Rollentauschpaaren. Die GUI ergänzt ihre Bewertung später Prüfungslagen; diese ist weiterhin kein eigenes Solverziel. Schülerabstände werden weiterhin über zwei schematische Wochen einschließlich Wochenende berechnet; Kalenderdaten sind dafür irrelevant.
- Die anschließende Raumvergabe ergänzt Hinweise zu ersatzweiser Raumzuweisung, Prüfungen im Parkplatz und Lücken im Raumplan. Die GUI ergänzt die Konflikte des tatsächlich übernommenen Plans. Modellgrenzen wie übersprungene Kopplungsblöcke und die bislang fehlende eigene Wirkung des Schalters „Min. Räume“ werden offengelegt.
- Der Ergebnisdialog zeigt Status und Hinweisanzahl; „Details“ enthält die konkreten Meldungen. Harte Regeln des CP-Zeitmodells und Wünsche werden getrennt bewertet; Optimalität der gewichteten Zielfunktion bedeutet nicht, dass jeder einzelne Wunsch erfüllt ist.
- Geprüft mit konstruierten CP-SAT-Fällen: Raumkapazität, gemeinsame Verfügbarkeit, Personen-/Einsatztagelimits, exakte Wochenregel, harter und gewünschter Schülerabstand einschließlich Wochenende, Kopplungskonflikte und übersprungene Blöcke, Rollentausch und Konflikte der Lückenregel. Zusätzlich geprüft: Zeitlimit und ungültiges Modell, Raumkonstanz-Fallback, Raumvergabe ohne gültige Lösung sowie die echte GUI-Solver-Schnittstelle, Erhalt des bisherigen Plans und der Qt-Ergebnisdialog. Die Prüfungen ersetzen keine Validierung jedes individuellen CSV-Datensatzes.

### Version 1.2.9

- Harte Begrenzung der maximalen Einsatztage zählt Lehrkräfte über Prüfer- und Beisitzerrolle hinweg. Der Solver erkennt belegte Personentage jetzt exakt; leere Beisitzer werden nicht als gemeinsame Person gezählt.
- In Plan und Parkplatz wird die Schrift des Schülernamens anhand der verfügbaren Zellbreite und -höhe angepasst. Der vollständige Name bleibt bis zu zwei Schriftgrößenstufen erhalten; erst wenn er weiterhin nicht passt, wird die kollisionsbewusste Export-Kurzform verwendet. Thema, Prüfer und Beisitzer bleiben unverändert; Prüfungsblock und Drag-and-drop-Zelle bleiben einteilig.
- Lehrkräfteimport unterstützt sowohl die bisherige CSV mit UPZ als auch die mehrseitige ASV-Lehrerliste mit Metadaten und wiederholten Tabellenköpfen. Für die Anwendung werden daraus die Kürzel übernommen.
- UPZ geht nicht mehr in die Belastungsberechnung ein und wird im Lehrkräfte-Dialog nicht mehr angezeigt. Das Feld bleibt intern lesbar, damit ältere gespeicherte Pläne abwärtskompatibel bleiben.
- „Zuteilung starten“ prüft vor dem Hintergrundlauf, ob Prüfungen, mindestens ein benannter Raum, mindestens ein Slot und ein nicht gesperrter Planungstag vorhanden sind. Fehlende Voraussetzungen werden mit einem Hinweis angezeigt, statt einen leeren bzw. unzulässigen Solverlauf zu starten.
- Die Live-Konfliktprüfung und die Prüfung manueller Verschiebungen verwenden für Themenkopplungen dieselbe nach Schüler sortierte Blockbildung und Blockgröße wie der Solver. Mehrere gekoppelte Teilblöcke werden einzeln bewertet, statt fälschlich als ein gemeinsamer Gesamtblock.
- Geprüft: Solverfälle für rollenübergreifende Tagesgrenzen, leere Beisitzer und deaktivierte Tagesgrenze; GUI-Solver-Schnittstelle und Live-Konfliktanzeige; CP-SAT-Fall mit zwei gültigen 2er-Kopplungsblöcken an unterschiedlichen Tagen; gültige und ungültige Blocklagen in der Live-Prüfung und manuellen Verschiebeprüfung; Qt-Messung und Zeichnung der Prüfungsblöcke; Zellinhalt und Drag-and-drop-Payload; Syntax und Modulimporte; ASV-Prüfungsimport beider Lehrkräfte-CSV-Formate; Belastungsberechnung unabhängig von UPZ; Tabellen- und Summenspalten des Lehrkräfte-Dialogs; Solver-Vorprüfung für fehlende Prüfungen/Räume/Slots und vollständig gesperrte Tage; echter Minimal-Solverlauf mit einem Raum und Slot.

### Version 1.2.8

- Im Ausschüsse-Dialog bestätigt Tab die Eingabe und springt zur Bearbeitung derselben Spalte in die nächste Zeile.
- Word-Exporte passen Schülernamen samt NTA-Zeit an die feste Slotbreite an; lange zusammengesetzte Nachnamen werden bei Bedarf abgekürzt.
- Fehler beim Parken von Prüfungsblöcken behoben: Der Undo-Zustand greift sicher auf die optional dynamisch berechnete Uhrzeit zu.
- Prüfungs-, Lehrkräfte- und Kursimporte ersetzen jeweils ihre eigene Datenquelle. Die Lehrkräfteliste wird aus den getrennten Quellen und den Prüfungsbeteiligten neu aufgebaut; K2 und Belastung werden aktualisiert. Ein Import funktioniert weiterhin einzeln, und der Solver benötigt nur Prüfungsdaten.
- Bei einer bestehenden Planung fragt jeder CSV-Import vor dem Übernehmen nach. Bei Zustimmung werden Plan, ID-bezogene Markierungen und Undo/Redo-Historie gelöscht; bei Abbruch oder ungültigen CSV-Daten bleibt der bisherige Stand erhalten. Planungs- und Solver-Einstellungen bleiben bestehen.
- Importe sind während eines laufenden Solverdurchlaufs gesperrt; parallele Solverläufe werden verhindert.
- Quelldaten werden in gespeicherten Plänen mitgeführt. Veraltete Lehrkraftkürzel in Bedingungen bleiben erhalten und werden nach einem Import in der Statusmeldung angezeigt.
- Belastungseinstellungen bleiben beim Speichern und erneuten Öffnen eines Plans erhalten.
- Summenzeile im Lehrkräfte-Dialog bündig ausgerichtet, Werte zentriert und Lehrkraft-/UPZ-Zellen zur Beschriftung „Summe“ verbunden.
- Erfolgreiche Lehrkräfte- und Kursimporte werden als Planänderung erkannt und führen beim Beenden zur Speicherabfrage.
- Beim Kursimport können die FTU-Kurse unter den L-Sportkursen ausgewählt werden; nur diese liefern S-/K-Werte. Wochenstunden werden je exakt geschriebener Kursbezeichnung nur einmal angerechnet; Groß-/Kleinschreibung bleibt relevant.
- Summen in S/S2 und K/K2 werden durch Division mit 3 bzw. 2 gegen die Zahl eindeutiger Schüler geprüft; Abweichungen werden rot, passende Werte grün markiert. Die Markierung bleibt nach Aktualisierungen erhalten.
- Report-Modul (0.3 Build 9): ungenutzte Ausrichtungsfunktion und Imports entfernt; der CLI-Report nennt die Quelldatei, der GUI-Report keinen Platzhalter.
- ASV-Importmodul (0.1 Build 5): ungenutzte Werte entfernt, CSV-Helfer aus Zeilenschleifen verschoben und Zahlenkonvertierung gezielter abgesichert.

### Version 1.2.7

- Drei Word-Exportvarianten für Lehrkräfte, Schüler und Reinigungspersonal mit Auswahldialog
- Belastungswerte im Report werden nur für eingeplante Lehrkräfte berücksichtigt

### Version 1.2.6

- Suchfunktion für Schüler, Prüfer, Beisitzer und Themen
- Änderungen an Zeiten, Räumen und Bedingungen werden beim Schließen gespeichert

### Version 1.2.5

- Erweiterte Absperrungs- und Vorbereitungsplanung mit NTA-Berücksichtigung
- Belastungsparameter können angepasst und gespeichert werden
- Excel-Export enthält Themen; die auszugebenden Spalten sind auswählbar

### Version 1.2.4

- Fairere Verteilung der Prüfungsslots pro Schüler
- Lehrkräfte- und Kursdaten können angepasst und gespeichert werden
- Dialoggrößen und Blockdarstellung wurden für unterschiedliche Betriebssysteme angepasst

### Version 1.2.3

- Prüfungskopplungen mit bis zu fünf Prüfungen
- Konfliktmarkierungen beim Öffnen einer Datei und Prüfungszahlen pro Tag
- Räume können über ein Kontextmenü geändert, ergänzt und entfernt werden

### Version 1.2.2

- Statistikreport um Lehrkräftedaten erweitert
- Dateistatus und Protokollmeldungen verbessert
- Speichern unter sowie eine Summenzeile im Lehrkräfte-Dialog ergänzt
- Prüfungen im Parkplatz werden ohne ungültige Slotdaten geführt

### Version 1.2

- Deutsche PySide6-Übersetzungen und native Dialoge

### Version 1.1

- Import von Lehrkräften mit UPZ sowie Oberstufenkursen mit WS-, S- und K-Daten
- Schulname und Vorbereitungsraum in den Plan übernommen
- Prüfungsbelastung und Raum-/Zeitsortierung ergänzt
- Speichern bei Änderungen sowie weitere Einstellungen für Lehrkräfte ergänzt

### Version 1.0

- Grafische Oberfläche mit manueller Prüfungsverschiebung
- Parkplatz für nicht zugewiesene Prüfungen
- Prüfung von Bedingungen bei manuellen Änderungen sowie Undo und Redo für die Slotplanung
- Word-Export

### Version 0.1

- Erste CP-SAT-Planung mit verschiebbaren Prüfungen und Word-Export

### Laufende Fehlerbehebungen

- Importprüfungen und Fehlermeldungen vereinheitlicht; Probleme mit doppelten Kursimporten und überschriebenen Daten behoben
- Konflikt- und Bedingungsprüfung bei Drag-and-drop sowie Änderungen an Prüfungen konsolidiert
- Berechnung von Tagesabständen, Prüferlimits und Belastungswerten korrigiert
- Speichern, Undo/Redo, Statusmeldungen und Kontextmenüs weiter stabilisiert
