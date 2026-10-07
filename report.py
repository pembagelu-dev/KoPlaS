Version = "0.3 (Build 9)"

"""
Reportschnittstelle

----------
ChangeLog
----------
Build 9: Nicht genutzte Ausrichtungsfunktion entfernt; Quelldateiname wird bei CLI-Reports ausgegeben
Build 8: Ungenutzte Imports nsmap und WD_SECTION_START entfernt; keine Funktionsänderung
Erweiterung der LK Tabelle um S, S2, K, K2 und Belastung
Leere Seite am Ende entfernt
Zellen in Tabelle zentriert
Ausgabeinformationen etwas angepasst
Alle Lehrkräfte werden in Tabelle ausgegeben
"""

import sys
import json
import argparse
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("Fehlendes Paket: python-docx. Bitte installieren mit: pip install python-docx")
    sys.exit(1)

VALID_TAGE_ORDER = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
TAG_TO_INDEX = {t: i for i, t in enumerate(VALID_TAGE_ORDER)}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Erstellt eine Word-Statistik aus einer Kolloquiumsplan-JSON."
    )
    parser.add_argument("json_path", help="Pfad zur JSON-Datei (z. B. kolloquiumsplan.json)")
    parser.add_argument(
        "-o", "--output",
        help="Pfad zur Ausgabedatei (.docx). Standard: report_<Dateiname>.docx",
        default=None
    )
    parser.add_argument(
        "--title",
        help="Titel im Dokumentkopf",
        default="Kolloquiumsplan – Statistik"
    )
    return parser.parse_args()

def load_data(json_path: str):
    p = Path(json_path)
    if not p.exists():
        print(f"Datei nicht gefunden: {json_path}")
        sys.exit(1)
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Ungültige JSON-Datei: {e}")
        sys.exit(1)
    if not isinstance(data, list):
        print("Erwartet wird eine JSON-Liste von Objekten.")
        sys.exit(1)
    return data

def normalize_day(tag: str):
    if not isinstance(tag, str):
        return str(tag)
    tag = tag.strip()
    tag_cap = tag[:1].upper() + tag[1:].lower() if tag else tag
    mapping = {
        "Mo": "Mo", "Montag": "Mo",
        "Di": "Di", "Dienstag": "Di",
        "Mi": "Mi", "Mittwoch": "Mi",
        "Do": "Do", "Donnerstag": "Do",
        "Fr": "Fr", "Freitag": "Fr",
        "Sa": "Sa", "Samstag": "Sa",
        "So": "So", "Sonntag": "So",
    }
    return mapping.get(tag_cap, tag)

def day_sort_key(tag: str):
    t = normalize_day(tag)
    if t in TAG_TO_INDEX:
        return TAG_TO_INDEX[t]
    return len(VALID_TAGE_ORDER) + hash(t) % 1000

def add_heading(document, text, level=0):
    h = document.add_heading(level=level)
    run = h.add_run(text)
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), "Calibri")
    run.font.size = Pt(14 if level == 0 else 12)
    return h

def add_paragraph(document, text, bold=False, italic=False, align=None):
    p = document.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), "Calibri")
    run.font.size = Pt(11)
    if align:
        p.alignment = align
    return p

def add_table(document, headers, rows, style="Light List Accent 1", col_widths=None):
    table = document.add_table(rows=1, cols=len(headers))
    table.style = style
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = str(h)
    for r in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(r):
            row_cells[i].text = "" if val is None else str(val)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                try:
                    row.cells[i].width = Inches(w)
                except Exception:
                    pass
    document.add_paragraph()
    return table

def merge_first_column_same_values(table, start_row=1):
    """
    Mergt zusammenhängende identische Werte in der ersten Spalte.
    Erwartet: Tabelle ist bereits nach der ersten Spalte gruppiert/sortiert.
    """
    if len(table.rows) <= start_row:
        return
    col = 0
    current_text = table.cell(start_row, col).text
    merge_start = start_row
    for r in range(start_row + 1, len(table.rows)):
        cell = table.cell(r, col)
        if cell.text == current_text:
            # weiter gruppieren
            continue
        else:
            if r - 1 > merge_start:
                table.cell(merge_start, col).merge(table.cell(r - 1, col))
            current_text = cell.text
            merge_start = r
    # Restgruppe bis zum Ende mergen
    if len(table.rows) - 1 > merge_start:
        table.cell(merge_start, col).merge(table.cell(len(table.rows) - 1, col))

def build_statistics(rows, teachers_map=None):
    # Normalisieren
    dat = []
    for r in rows:
        dat.append({
            "ID": r.get("ID"),
            "Schueler": (r.get("Schueler") or "").strip(),
            "Fach": r.get("Fach"),
            "Thema": r.get("Thema"),
            "Pruefer": (r.get("Pruefer") or "").strip(),
            "Beisitzer": (r.get("Beisitzer") or "").strip(),
            "Woche": r.get("Woche"),
            "Tag": normalize_day(r.get("Tag")),
            "Uhrzeit": r.get("Uhrzeit"),
            "Raum": (r.get("Raum") or "").strip(),
        })

    # 1) Prüfungen pro Woche und Tag
    exams_per_week = Counter()
    exams_per_weekday = defaultdict(Counter)   # Woche -> Counter(Tag)
    rooms_per_week_day = defaultdict(set)      # (Woche, Tag) -> Räume

    # 2) Schülerdaten sammeln
    exams_by_student = defaultdict(list)

    # 3) Personendaten (Prüfer/Beisitzer aggregiert)
    person_exams_per_week_day = defaultdict(Counter)  # Person -> Counter((Woche, Tag))

    for e in dat:
        w = e["Woche"]
        d = e["Tag"]
        raum = e["Raum"]
        student = e["Schueler"]
        p_pruefer = e["Pruefer"]
        p_beisitzer = e["Beisitzer"]

        if isinstance(w, int):
            exams_per_week[w] += 1
        exams_per_weekday[w][d] += 1

        if raum:
            rooms_per_week_day[(w, d)].add(raum)

        if student:
            exams_by_student[student].append(e)

        if p_pruefer:
            person_exams_per_week_day[p_pruefer][(w, d)] += 1
        if p_beisitzer:
            person_exams_per_week_day[p_beisitzer][(w, d)] += 1

    # Schüler: erste/zweite Prüfung taggenauer Abstand
    def time_sort_key(e):
        # Sortiere nach Woche, Tagindex, Uhrzeit
        w = e.get("Woche")
        t = e.get("Tag")
        idx = day_sort_key(t)
        u = e.get("Uhrzeit")
        mins = 0
        if isinstance(u, str) and ":" in u:
            try:
                h, m = u.split(":")
                mins = int(h) * 60 + int(m)
            except Exception:
                mins = 0
        return (w, idx, mins)

    def day_index(tag):
        t = normalize_day(tag)
        return TAG_TO_INDEX.get(t, 0)

    student_rows = []
    for student, lst in exams_by_student.items():
        lst_sorted = sorted(lst, key=time_sort_key)
        if lst_sorted:
            w1 = lst_sorted[0].get("Woche")
            t1 = lst_sorted[0].get("Tag")
        else:
            w1 = t1 = None
        if len(lst_sorted) > 1:
            w2 = lst_sorted[1].get("Woche")
            t2 = lst_sorted[1].get("Tag")
        else:
            w2 = t2 = None

        # Abstand in Tagen, falls beide vorhanden und Wochen ints
        if isinstance(w1, int) and isinstance(w2, int) and t1 and t2:
            diff_days = 7 * (w2 - w1) + (day_index(t2) - day_index(t1))
        else:
            diff_days = None

        student_rows.append((student, w1, t1, w2, t2, diff_days))

    student_rows.sort(key=lambda x: (str(x[0]).lower()))

    # Räume pro (Woche, Tag)
    rooms_count_rows = []
    for (w, d), rooms in rooms_per_week_day.items():
        rooms_count_rows.append((w, d, len(rooms)))
    rooms_count_rows.sort(key=lambda x: (x[0], day_sort_key(x[1])))

    # Wochen/Tag-Details
    weeks_detail = {}
    for w, counter_day in exams_per_weekday.items():
        rows = [(w, d, n) for d, n in counter_day.items()]
        rows.sort(key=lambda x: (x[0], day_sort_key(x[1])))
        weeks_detail[w] = rows

    # Personentabellen: zusätzlich Anzahl unterschiedlicher Prüftage (distinct (Woche, Tag))
    person_tables = {}
    person_prueftage = {}
    for person, cnt in person_exams_per_week_day.items():
        rows = [(w, d, n) for (w, d), n in cnt.items()]
        rows.sort(key=lambda x: (x[0], day_sort_key(x[1])))
        person_tables[person] = rows
        person_prueftage[person] = len(cnt.keys())
        
    # Lehrkraftwerte aus teachers_map (optional) andocken:
    # teachers_map erwartet: dict person_code -> dict mit Keys: S, S2, K, K2, Belastung (Strings)
    teacher_stats = {}
    if isinstance(teachers_map, dict):
         # Alle Lehrkräfte aus teachers_map aufnehmen (unabhängig davon, ob sie im Plan vorkommen)
         for person, t in teachers_map.items():
             teacher_stats[person] = {
                 "S": str(t.get("S", "")) if t.get("S", "") is not None else "",
                 "S2": str(t.get("S2", "")) if t.get("S2", "") is not None else "",
                 "K": str(t.get("K", "")) if t.get("K", "") is not None else "",
                 "K2": str(t.get("K2", "")) if t.get("K2", "") is not None else "",
                 "Belastung": str(t.get("Belastung", "")) if t.get("Belastung", "") is not None else "",
             }

    stats = {
        "exams_per_week": dict(sorted(exams_per_week.items(), key=lambda x: x[0] if isinstance(x[0], int) else 999999)),
        "weeks_detail": weeks_detail,           # Woche -> [(Woche, Tag, Anzahl)]
        "rooms_per_week_day": rooms_count_rows, # [(Woche, Tag, Anzahl Räume)]
        "student_rows": student_rows,           # [(Schüler, Woche1, Tag1, Woche2, Tag2, Abstand Tage)]
        "person_tables": person_tables,         # Person -> [(Woche, Tag, Prüfungen)]
        "person_prueftage": person_prueftage,   # Person -> Anzahl distinct Prüftage
        "teacher_stats": teacher_stats,         # Person -> {"S","S2","K","K2","Belastung"} (Strings), evtl. leer
    }
    return stats

def build_doc(stats, title, source_name=None):
    doc = Document()

    # Titel
    add_heading(doc, title, level=0)
    if source_name:
        add_paragraph(doc, f"Quelle: {Path(source_name).name}", italic=True)
    add_paragraph(doc, f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}", italic=True)
    doc.add_paragraph()

    # 1) Anzahl der Prüfungen pro Woche und Tag
    add_heading(doc, "1. Anzahl der Prüfungen pro Woche und Tag", level=1)
    add_paragraph(doc, "1.1 Gesamt pro Woche", bold=True)
    rows_week = [(w, n) for w, n in stats["exams_per_week"].items()]
    if rows_week:
        add_table(doc, ["Woche", "Prüfungen"], rows_week)
    else:
        add_paragraph(doc, "Keine Daten verfügbar.")

    add_paragraph(doc, "1.2 Aufschlüsselung pro Woche und Tag", bold=True)
    if stats["weeks_detail"]:
        combined = []
        for w in sorted(stats["weeks_detail"].keys()):
            combined.extend(stats["weeks_detail"][w])
        add_table(doc, ["Woche", "Tag", "Prüfungen"], combined)
    else:
        add_paragraph(doc, "Keine Tagesdetails verfügbar.")

    # 2) Schüler: 1./2. Prüfung mit taggenauem Abstand
    add_heading(doc, "2. Schülerübersicht: 1. und 2. Prüfung (taggenauer Abstand)", level=1)
    #add_paragraph(doc, "Abstand: 7 × (Woche2 − Woche1) + (TagIndex2 − TagIndex1), mit Mo=0 … So=6.", italic=True)
    if stats["student_rows"]:
        add_table(
            doc,
            ["Schüler", "Woche 1.", "Tag 1.", "Woche 2.", "Tag 2.", "Abstand (Tage)"],
            stats["student_rows"]
        )
    else:
        add_paragraph(doc, "Keine Schülerdaten verfügbar.")

    # 3) Anzahl genutzter Räume pro Woche und Tag
    add_heading(doc, "3. Anzahl genutzter Räume pro Woche und Tag", level=1)
    if stats["rooms_per_week_day"]:
        add_table(doc, ["Woche", "Tag", "Anzahl unterschiedlicher Räume"], stats["rooms_per_week_day"])
    else:
        add_paragraph(doc, "Keine Raumdaten verfügbar.")

    # 4) Prüfungen pro Person (Prüfer/Beisitzer aggregiert) pro Woche und Tag
    add_heading(doc, "4. Prüfungen pro Person (Prüfer/Beisitzer aggregiert) pro Woche und Tag", level=1)
    if stats["person_tables"]:
        # Kombinierte Tabelle: Person | Woche | Tag | Prüfungen | Prüftage (distinct)
        teacher_stats = stats.get("teacher_stats") or {}
        combined = []
        headers = ["Person", "Woche", "Tag", "Prüfungen", "Prüftage", "S1", "S2", "K1", "K2", "Belastung"]
        # Alle Personen: Vereinigung aus Plan-Personen und Lehrkräften
        persons_in_plan = set(stats["person_tables"].keys())
        persons_with_stats = set(teacher_stats.keys())
        all_persons = sorted(persons_in_plan | persons_with_stats, key=lambda x: x.lower())
        for person in all_persons:
            rows = stats["person_tables"].get(person, [])
            prueftage = stats["person_prueftage"].get(person, 0)
            tstats = teacher_stats.get(person, {"S": "", "S2": "", "K": "", "K2": "", "Belastung": ""})
            # Für die erste Zeile der Person S/S2/K/K2/Belastung befüllen, danach leer (wird gemergt)
            if rows:
                for i, (w, d, n) in enumerate(rows):
                    if i == 0:
                        combined.append((person, w, d, n, prueftage, tstats.get("S",""), tstats.get("S2",""), tstats.get("K",""), tstats.get("K2",""), tstats.get("Belastung","")))
                    else:
                        combined.append((person, w, d, n, "", "", "", "", "", ""))
            else:
                # Lehrkraft ohne Plan-Einträge: Dummy-Zeile mit K1/K2=0, Prüfungen=0, Prüftage=0
                combined.append((person, "", "", 0, 0, tstats.get("S",""), tstats.get("S2",""), "0", "0", tstats.get("Belastung","")))

        # Spaltenbreiten für A4 quer (ungefähr 6.75")
        col_widths = [1.10, 0.55, 0.55, 0.70, 0.85, 0.45, 0.45, 0.45, 0.45, 0.70]
        table = add_table(doc, headers, combined, col_widths=col_widths)

        # Ausrichtung: Prüftage, S1, S2, K1, K2, Belastung zentrieren (horizontal+vertikal)
        # Spaltenindizes: 4..9
        try:
            for r_idx, row in enumerate(table.rows):
                for c_idx in range(4, 10):
                    cell = row.cells[c_idx]
                    # horizontal
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    # vertikal
                    try:
                        tcPr = cell._tc.get_or_add_tcPr()
                        vjc = OxmlElement('w:vAlign')
                        vjc.set(qn('w:val'), 'center')
                        # vorhandene w:vAlign ggf. ersetzen
                        existing = tcPr.find(qn('w:vAlign'))
                        if existing is not None:
                            tcPr.remove(existing)
                        tcPr.append(vjc)
                    except Exception:
                        pass
        except Exception:
            pass

        # Merge der ersten Spalte (Person) und der Spalten Prüftage, S1, S2, K1, K2, Belastung für zusammenhängende Blöcke
        merge_first_column_same_values(table, start_row=1)
        # Hilfslogik: die gleiche Gruppierung entlang Spalten 4..9 (0-basiert) anwenden
        if len(table.rows) > 1:
            cols_to_merge = [4, 5, 6, 7, 8, 9]
            for col in cols_to_merge:
                current_text = table.cell(1, 0).text
                merge_start_row_person = 1
                for r in range(2, len(table.rows)):
                    if table.cell(r, 0).text == current_text:
                        continue
                    else:
                        if r - 1 > merge_start_row_person:
                            table.cell(merge_start_row_person, col).merge(table.cell(r - 1, col))
                        current_text = table.cell(r, 0).text
                        merge_start_row_person = r
                if len(table.rows) - 1 > merge_start_row_person:
                    table.cell(merge_start_row_person, col).merge(table.cell(len(table.rows) - 1, col))
    else:
        add_paragraph(doc, "Keine Personendaten verfügbar.")

    return doc

def main():
    args = parse_args()
    data = load_data(args.json_path)

    stats = build_statistics(data)

    src_name = Path(args.json_path).name
    if args.output:
        out_path = Path(args.output)
    else:
        stem = Path(args.json_path).stem
        out_path = Path(f"report_{stem}.docx")

    doc = build_doc(stats, args.title, src_name)
    try:
        doc.save(out_path)
    except Exception as e:
            print(f"Fehler beim Schreiben der Word-Datei: {e}")
            sys.exit(1)

    #print(f"Report erstellt: {out_path.resolve()}")

if __name__ == "__main__":
    main()
