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

## Start

Im Projektverzeichnis die grafische Anwendung starten:

```bash
python KoPlaS.py
```

Danach können Daten über die Importfunktionen der Anwendung geladen, ein Plan erstellt und bei Bedarf manuell angepasst werden. Die Exportvarianten sind über die Exportmenüs erreichbar.

## Module

| Datei | Aufgabe |
| --- | --- |
| `KoPlaS.py` | Grafische Desktop-Anwendung, Datenverwaltung, interaktive Planung und Exportsteuerung |
| `kolloPlaner.py` | Solver-Logik für die Zeit- und Raumplanung mit CP-SAT und MIP |
| `import_asv.py` | Einlesen und Umformen von ASV-CSV-Daten; als eigenständiger Importer nutzbar |
| `export.py` | Erzeugung der Word-Pläne und Excel-Tabellen |
| `report.py` | Erstellung eines Word-Statistikreports aus einer Plan-JSON-Datei |

### ASV-Import als Kommandozeilenprogramm

Der Importer kann eine ASV-CSV-Datei einlesen und `pruefungen.csv` im aktuellen Arbeitsverzeichnis erzeugen:

```bash
python import_asv.py "Abiturfächer Kurse.csv"
```

### Statistikreport als Kommandozeilenprogramm

Aus einer Plan-JSON-Datei kann direkt ein Word-Report erstellt werden:

```bash
python report.py kolloquiumsplan.json --output statistik.docx --title "Kolloquiumsplan – Statistik"
```

## Hinweise

- Der Solver berücksichtigt harte Bedingungen zwingend und verwendet weiche Bedingungen zur Bewertung beziehungsweise Optimierung von Planvarianten.
- Die grafische Oberfläche unterstützt die Prüfung von Konflikten auch nach manuellen Änderungen.
- Für die Word- und Excel-Ausgaben müssen `python-docx` beziehungsweise `openpyxl` installiert sein.

## Versionsstand

Die Versionsangaben der Module sind in den jeweiligen Quelldateien dokumentiert. Die grafische Anwendung führt ihre Version in `KoPlaS.py`.
