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
| `KoPlaS.py` (1.2.10 Build 64) | Grafische Desktop-Anwendung, Datenverwaltung, interaktive Planung und Exportsteuerung |
| `kolloPlaner.py` (0.2 Build 17) | Solver-Logik für die Zeit- und Raumplanung mit CP-SAT und MIP |
| `import_asv.py` (0.1 Build 6) | Einlesen und Umformen von ASV-CSV-Daten für den Import in den Planungsablauf |
| `export.py` (0.1 Build 14) | Erzeugung der Word-Pläne und Excel-Tabellen |
| `report.py` (0.3 Build 9) | Erstellung des Word-Statistik- und Belastungsreports |

## Hinweise

- Der Solver berücksichtigt harte Bedingungen zwingend und verwendet weiche Bedingungen zur Bewertung beziehungsweise Optimierung von Planvarianten.
- Die grafische Oberfläche unterstützt die Prüfung von Konflikten auch nach manuellen Änderungen.
- Für die Word- und Excel-Ausgaben müssen `python-docx` beziehungsweise `openpyxl` installiert sein.
- Der reguläre Planungsablauf erfolgt über die grafische Oberfläche. Die übrigen Python-Dateien stellen dafür Import-, Solver-, Export- und Reportfunktionen bereit.

## Version und Änderungshistorie

**Aktuelle Version: 1.2.10 (Build 64); Solver: 0.2 (Build 17)**

### Version 1.2.10

- „Min. Räume“ minimiert die täglich genutzte Raumzahl
- Beisitzeränderungen an einzelnen Prüfungen verwenden denselben Dialog und Undo-Schritt wie Sammeländerungen.
- Abweichende Höchstzahl an Prüfungstagen für ausgewählte Prüfer festlegen
- Ausnahmezahl der Prüfungen pro Tag für ausgewählte Prüfer einstellbar
- Prüfungen desselben Raum-Tagesblocks per Umschalt markieren und gemeinsam ändern/verschieben.

### Version 1.2.9

- Tageslimits zählen Prüfer- und Beisitzereinsätze gemeinsam; Import- und Startprüfungen wurden erweitert.
- Schülernamen passen sich im Plan und Parkplatz an die verfügbare Zellgröße an.
- Themenkopplungen werden in Solver und manueller Konfliktprüfung einheitlich bewertet.

### Version 1.2.8

- Import, Bearbeitung und Speicherung von Prüfungs-, Lehrkräfte- und Kursdaten verbessert.
- Word-Export, Lehrkräfteübersicht und Kursauswertung überarbeitet.
- Tab-Navigation und Undo/Redo im Ausschüsse- und Planungsdialog verbessert.

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
