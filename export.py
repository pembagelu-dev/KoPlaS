Version = "0.1 (Build 11)"

"""
----------
ChangeLog
----------
Build 1.26: Schülernamen in Lehrer- und Schülerplan anhand der tatsächlichen Textbreite skaliert; lange zusammengesetzte Nachnamen werden bei Bedarf abgekürzt, NTA-Zeiten mitgemessen
Build 1.25: Sortierung im Lehrerplan an den Schülerplan angeglichen (Raumtext, frühester Slot, bisherige Gruppenreihenfolge)
Build 1.24: Unnötige Nachnamensauswertung und Excel-Zeitberechnungen entfernt; doppelte Spaltenbreitenschlüssel bereinigt
Spaltenbreiten angepasst
Pro Prüfungskommission eine Zeile je Raum
Neue Überschrift, neue Spaltenbreiten
Vorbereitung wird berechnet
NTA wird in Klammern hinzugefügt (in Arial 10)
Schulname wird in der Kopfzeile hinzugefügt (gelesen aus Oberstufenkurse Header) sowie Anlage 5
Vorbereitungsraum wurde eingepflegt
Excel-Export hinzugefügt
Kommt ein nachname mind. 4mal vor, wird der Vorname abgekürzt hinzugefügt
Absperrung bei mehr als zwei Themen-Kopplungen hinzugefügt. Raum für Aufsicht ist der Vorbereitungsraum. NTA wird berücksichtigt, falls dadurch Absperrung verkürzt werden kann.
Thema wird mit ausgegeben
Tabellenexport Spalten auswählbar
Wordexport drei Varianten (LK, SuS, Reinigungspersonal)
Tabellen alle auf Seite zentriert

----------
Bug-Fix
----------
Schulname nicht sauber rechtsbündig, jetzt mit Tabelle gelöst (OK)
Sortierung nach Räumen und dann nach Zeit
NTA Berechnung funktioniert wieder
Umlaute ausgebessert
"""

import sys
import json
from functools import lru_cache
from collections import defaultdict, OrderedDict
from typing import List, Dict, Any, Tuple, Optional

try:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment, Font, Border, Side
except ImportError:
    pass

try:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.enum.section import WD_ORIENTATION
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

except ImportError:
    print("Bitte installieren: pip install python-docx")
    sys.exit(1)

DAYS = ["Mo", "Di", "Mi", "Do", "Fr"]

# Formatvorgaben
FONT_NAME = "Arial"
FONT_SIZE_DEFAULT = 14
FONT_SIZE_HEADER_MAIN = 18
FONT_SIZE_EXAM_STUDENT = 10
ROW_HEIGHT_CM = 0.8
ROW_HEIGHT = 1.21
# Spaltenbreiten in cm
COL_W_KURS = 2.19
COL_W_PRUEFER = 1.25
COL_W_BEISITZER = 1.25
COL_W_RAUM = 1.8
COL_W_SLOT = 4.34
#Seitenränder
LEFT_MARGIN = 1.0
RIGHT_MARGIN = 1.0
TOP_MARGIN = 1.0
BOTTOM_MARGIN = 1.0

_FONT_METRICS_APP = None


@lru_cache(maxsize=8192)
def _slot_text_width_pt(text: str, size_pt: float) -> float:
    """Misst die Breite eines Arial-Fettdruck-Runs in typografischen Punkten."""
    global _FONT_METRICS_APP
    from PySide6.QtGui import QFont, QFontMetricsF, QGuiApplication

    app = QGuiApplication.instance()
    if app is None:
        _FONT_METRICS_APP = QGuiApplication([])
        app = _FONT_METRICS_APP

    font = QFont(FONT_NAME)
    font.setPointSizeF(float(size_pt))
    font.setBold(True)
    metrics = QFontMetricsF(font)
    screen = app.primaryScreen()
    dpi = screen.logicalDotsPerInchX() if screen else 96.0
    return metrics.horizontalAdvance(text) * 72.0 / dpi


def _abbreviate_surname_part(name: str) -> str:
    """Kürzt den letzten ausgeschriebenen Teil eines zusammengesetzten Nachnamens."""
    suffix = ""
    name_core = name

    # Den optionalen Initial-Bestandteil eines Namenskollisionsfalls erhalten.
    if len(name_core) >= 2 and name_core[-2].isalpha() and name_core[-1] == "." and name_core[-3:-2].isspace():
        suffix = name_core[-2:]
        name_core = name_core[:-3].rstrip()

    import re
    parts = list(re.finditer(r"[^\s-]+", name_core))
    for part in reversed(parts):
        if part.start() == 0 or len(part.group()) <= 2 or part.group().endswith("."):
            continue
        abbreviated = name_core[:part.start()] + part.group()[0] + "." + name_core[part.end():]
        return abbreviated + ((" " + suffix) if suffix else "")

    # Falls nur noch ein ungewöhnlich langer Einzelbestandteil übrig ist,
    # kürzen wir ihn moderat ab, statt die Namenszelle überlaufen zu lassen.
    if parts and len(parts[0].group()) > 13:
        part = parts[0]
        abbreviated = name_core[:part.start()] + part.group()[:11] + "." + name_core[part.end():]
        return abbreviated + ((" " + suffix) if suffix else "")
    return name


def _fit_slot_name(full_text: str, cell_width_cm: float = COL_W_SLOT) -> Tuple[str, Optional[str], int, int]:
    """Wählt eine passende Schriftgröße und kürzt bei Bedarf zusammengesetzte Namen."""
    base_text = full_text or ""
    nta_text = None
    split_idx = base_text.rfind(" (")
    if split_idx != -1 and base_text.endswith(")"):
        base_text, nta_text = base_text[:split_idx], base_text[split_idx + 1:]

    # Zellränder und eine kleine Reserve für Unterschiede zwischen Qt und Word.
    available_pt = (cell_width_cm / 2.54 * 72.0 - 12.0) * 0.98

    def fits(candidate: str, size_pt: int) -> bool:
        width = _slot_text_width_pt(candidate, size_pt)
        if nta_text:
            width += _slot_text_width_pt(" ", size_pt)
            width += _slot_text_width_pt(nta_text, min(10, size_pt))
        return width <= available_pt

    while True:
        # Lange Namen zuerst sinnvoll abkürzen, damit möglichst mindestens
        # 10 pt erhalten bleiben. Erst danach wird bis 8 pt verkleinert.
        for size_pt in range(FONT_SIZE_DEFAULT, 9, -1):
            if fits(base_text, size_pt):
                return base_text, nta_text, size_pt, min(10, size_pt)

        abbreviated = _abbreviate_surname_part(base_text)
        if abbreviated == base_text:
            # Ein nicht weiter sinnvoll kürzbarer Name bleibt vollständig;
            # 8 pt ist die Untergrenze für die Ausgabe.
            for size_pt in (9, 8):
                if fits(base_text, size_pt):
                    return base_text, nta_text, size_pt, min(10, size_pt)
            return base_text, nta_text, 8, min(10, 8)
        base_text = abbreviated


def _set_cell_no_wrap(cell) -> None:
    """Verhindert, dass Word einen bereits passend skalierten Namen umbrechen kann."""
    tc_pr = cell._tc.get_or_add_tcPr()
    if tc_pr.find(qn("w:noWrap")) is None:
        tc_pr.append(OxmlElement("w:noWrap"))

# Excel-Konstanten
XLSX_HEADER_FONT = ("Arial", 11, True)
XLSX_BODY_FONT = ("Arial", 10, False)
XLSX_THIN_BORDER = Side(style="thin", color="000000")
XLSX_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

def set_cell_text(cell, text: str, bold=False, size_pt: int = FONT_SIZE_DEFAULT, align_center=True):
    cell.text = ""
    p = cell.paragraphs[0]
    if align_center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text if text is not None else "")
    run.bold = bold
    font = run.font
    font.name = FONT_NAME
    font.size = Pt(size_pt)

def set_row_height(row, height_cm: float):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    # vorhandene trHeight entfernen
    for child in list(trPr):
        if child.tag == qn('w:trHeight'):
            trPr.remove(child)
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(int(height_cm * 567)))  # 1 cm ≈ 567 twips
    trHeight.set(qn('w:hRule'), 'exact')
    trPr.append(trHeight)

def merge_cells_horizontally(table, row_idx: int, start_col: int, end_col: int):
    if end_col <= start_col:
        return
    a = table.cell(row_idx, start_col)
    b = table.cell(row_idx, end_col)
    a.merge(b)

def add_table_borders(table):
    """
    Fügt Außenrahmen und Gitterlinien für alle Zellen hinzu.
    Robust für python-docx-Versionen, in denen tblBorders nicht existiert.
    """
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.append(tblPr)

    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is None:
        tblBorders = OxmlElement('w:tblBorders')
        tblPr.append(tblBorders)

    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tag = qn(f'w:{edge}')
        elem = tblBorders.find(tag)
        if elem is None:
            elem = OxmlElement(f'w:{edge}')
            tblBorders.append(elem)
        elem.set(qn('w:val'), 'single')
        elem.set(qn('w:sz'), '8')
        elem.set(qn('w:space'), '0')
        elem.set(qn('w:color'), '000000')

def parse_json_plan(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    norm = []
    for row in data:
        norm.append({
            "ID": row.get("ID"),
            "Schueler": row.get("Schueler"),
            "Fach": row.get("Fach"),
            "Thema": row.get("Thema"),
            "Pruefer": row.get("Pruefer"),
            "Beisitzer": row.get("Beisitzer"),
            "Woche": row.get("Woche"),
            "Tag": row.get("Tag"),
            "Uhrzeit": row.get("Uhrzeit"),
            "Raum": row.get("Raum"),
            "SlotIndex": row.get("SlotIndex"),  # optional
        })
    return norm

def parse_slot_times(path: str) -> Dict[str, List[str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_hhmm(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = s.strip()
    if "-" in s:
        s = s.split("-")[0].strip()
    parts = s.split(":")
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        hh = int(parts[0])
        mm = int(parts[1])
        return f"{hh:02d}:{mm:02d}"
    return s

def begin_to_idx_map(slot_labels: List[str]) -> Dict[str, int]:
    mapping = {}
    for i, lab in enumerate(slot_labels):
        b = normalize_hhmm(lab)
        if b:
            mapping[b] = i
    return mapping

def short_student_name(full: str, collision_lastnames: Optional[set] = None) -> str:
    if not full:
        return ""
    parts = [p.strip() for p in full.split(",")]
    if len(parts) == 2:
        last, first = parts[0], parts[1]
    else:
        toks = full.strip().split()
        if len(toks) >= 2:
            last, first = toks[0], toks[1]
        else:
            last, first = full.strip(), ""
    if collision_lastnames and last in collision_lastnames:
        initial = (first[0] + ".") if first else ""
        return f"{last} {initial}".strip()
    return last

def collect_lastname_collisions(rows_for_day: List[Dict[str, Any]]) -> set:
    counts = defaultdict(int)
    for r in rows_for_day:
        s = r.get("Schueler") or ""
        if "," in s:
            last = s.split(",")[0].strip()
        else:
            toks = s.strip().split()
            last = toks[0] if toks else ""
        if last:
            counts[last] += 1
    return {ln for ln, c in counts.items() if c > 1}

def collect_global_lastname_collisions(plan_rows: List[Dict[str, Any]], threshold: int = 4) -> set:
    """
    Ermittelt Nachnamen, die im gesamten Plan mindestens 'threshold' Mal vorkommen.
    Hintergrund: Jeder Schüler kommt im Plan genau zweimal vor. Damit ein Nachname
    mindestens zweimal (2 Schüler) betroffen ist, soll die Schwelle 4 sein.
    """
    counts = defaultdict(int)
    for r in plan_rows:
        s = r.get("Schueler") or ""
        if "," in s:
            last = s.split(",")[0].strip()
        else:
            toks = s.strip().split()
            last = toks[0] if toks else ""
        if last:
            counts[last] += 1
    return {ln for ln, c in counts.items() if c >= threshold}

def group_by_day(plan_rows: List[Dict[str, Any]]) -> Dict[Tuple[int, str], List[Dict[str, Any]]]:
    grouped = defaultdict(list)
    for r in plan_rows:
        w = r.get("Woche")
        t = r.get("Tag")
        if w is None or t is None:
            continue
        grouped[(int(w), str(t))].append(r)

    def room_key(val: Optional[str]) -> Tuple[int, str]:
        if val is None:
            return (10**9, "")
        s = str(val)
        num = "".join(ch for ch in s if ch.isdigit())
        return (int(num) if num else 10**6, s)

    for k in grouped:
        grouped[k].sort(key=lambda r: room_key(r.get("Raum")))
    return grouped

def enforce_landscape(section):
    section.orientation = WD_ORIENTATION.LANDSCAPE
    pw, ph = section.page_width, section.page_height
    if pw < ph:
        section.page_width, section.page_height = ph, pw

def set_column_widths(table, widths_cm: List[float]):
    """
    Erzwingt Spaltenbreiten sowohl auf Column-Objekten als auch auf jeder Zell-GridCol-Ebene.
    """
    # Column-Breiten
    for i, w_cm in enumerate(widths_cm):
        if i < len(table.columns):
            table.columns[i].width = Cm(w_cm)
    # Zellen-Breiten setzen (robuster)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths_cm):
                cell.width = Cm(widths_cm[i])

def set_header_for_section(section, school_name_text: str, variant: Optional[str] = None):
        header = section.header
        # Header leeren (Absätze und Tabellen entfernen), um Dopplungen zu vermeiden
        try:
            # Entferne alle Tabellen
            tbls = list(header._element.xpath('.//w:tbl', namespaces=header._element.nsmap))
            for t in tbls:
                header._element.remove(t)
            # Entferne alle Absätze
            pars = list(header._element.xpath('.//w:p', namespaces=header._element.nsmap))
            for p_el in pars:
                header._element.remove(p_el)
        except Exception:
            # Fallback: nur Texte leeren
            for para in header.paragraphs:
                para.text = ""
        # 1x2-Tabelle mit Gesamtbreite anlegen
        from docx.shared import Cm
        total_width = None
        try:
            # verfügbare Breite = Seitenbreite - linke/rechte Ränder
            total_width = section.page_width - section.left_margin - section.right_margin
        except Exception:
            pass
        if total_width is not None:
            tbl = header.add_table(rows=1, cols=2, width=total_width)
        else:
            # Fallback: fixe Kopfzeilenbreite ca. 24 cm
            tbl = header.add_table(rows=1, cols=2, width=Cm(24))
        # Tabellenrahmen ausblenden
        try:
            tbl_pr = tbl._tbl.tblPr
            borders = tbl_pr.tblBorders if hasattr(tbl_pr, 'tblBorders') else None
            if borders is None:
                from docx.oxml import OxmlElement
                from docx.oxml.ns import qn
                borders = OxmlElement('w:tblBorders')
                tbl_pr.append(borders)
            # Kanten auf none
            for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
                from docx.oxml import OxmlElement
                from docx.oxml.ns import qn
                elem = borders.find(qn(f'w:{edge}'))
                if elem is None:
                    elem = OxmlElement(f'w:{edge}')
                    borders.append(elem)
                elem.set(qn('w:val'), 'nil')
        except Exception:
            pass
        # Spaltenbreiten sinnvoll verteilen (z. B. 50% / 50%)
        try:
            half = total_width // 2 if total_width is not None else None
            if half is not None:
                tbl.columns[0].width = half
                tbl.columns[1].width = half
        except Exception:
            # Alternativ feste cm-Werte setzen
            try:
                tbl.columns[0].width = Cm(12)
                tbl.columns[1].width = Cm(12)
            except Exception:
                pass
                
        # Zellen formatieren und texten
        c_left = tbl.cell(0, 0)
        c_right = tbl.cell(0, 1)
        # Linke Zelle: Anlage 5 (links) nur im Standardplan; bei 'students' und 'cleaning' leer
        c_left.text = ""
        p_left = c_left.paragraphs[0]
        p_left.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if variant not in ("students", "cleaning"):
            run_l = p_left.add_run("Anlage 5")
            run_l.font.name = FONT_NAME
            run_l.font.size = Pt(11)
        # Rechte Zelle: Schulname (rechts)
        c_right.text = ""
        p_right = c_right.paragraphs[0]
        p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_r = p_right.add_run(school_name_text or "")
        run_r.font.name = FONT_NAME
        run_r.font.size = Pt(11)

        # Sicherstellen, dass vor der Tabelle kein leerer Absatz im Header steht:
        # Entferne alle führenden leeren w:p-Knoten im Header-XML (manche python-docx Versionen fügen einen ein)
        try:
            hdr_el = header._element
            # Sammle alle direkten Kindelemente
            children = list(hdr_el)
            # Entferne alle w:p am Anfang (insb. leere Absätze), solange das erste Kind ein Absatz ist
            from docx.oxml.ns import qn
            while len(children) > 0 and children[0].tag == qn('w:p'):
                hdr_el.remove(children[0])
                children = list(hdr_el)
        except Exception:
            pass

def build_document(grouped: Dict[Tuple[int, str], List[Dict[str, Any]]],
                   slot_times: Dict[str, List[str]],
                   out_path: str,
                   time_info: Optional[Dict[str, Any]] = None) -> None:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.section import WD_ORIENTATION
    from datetime import datetime, timedelta
    import re

    doc = Document()

    # Zeit-/Format-Helper früh definieren (werden in NTA-Berechnung und Header benötigt)
    import re
    def parse_begin_end(label: str):
        if not label:
            return (None, None)
        part = label.strip()
        if "-" in part:
            b, e = [x.strip() for x in part.split("-", 1)]
        else:
            b, e = part, None
        mb = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", b) if b else None
        me = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", e) if e else None
        begin = (int(mb.group(1)), int(mb.group(2))) if mb else None
        end = (int(me.group(1)), int(me.group(2))) if me else None
        return (begin, end)

    def fmt_hh_dot_mm(h: int, m: int) -> str:
        return f"{h:02d}.{m:02d}"

    def minus_35_min(hh: int, mm: int):
        t = hh * 60 + mm - 35
        if t < 0:
            t = 0
        return ((t // 60) % 24, t % 60)

    # Globaler Standard (Arial 14)
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = Pt(FONT_SIZE_DEFAULT)

    # Reihenfolge: Woche 1..n, Mo..Fr
    day_order = []
    for w in sorted({w for (w, _) in grouped.keys()}):
        for d in DAYS:
            if (w, d) in grouped:
                day_order.append((w, d))

    # Hilfsfunktionen für Datum und ausgeschriebene Tagesnamen
    day_name_map = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag"}
    def parse_date_safe(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None
    base_w1 = parse_date_safe((time_info or {}).get("week1_date"))
    base_w2 = parse_date_safe((time_info or {}).get("week2_date"))
    def date_for(w: int, tag: str) -> Optional[datetime]:
        # week1_date ist Montag der Woche 1, week2_date der Montag der Woche 2
        base = base_w1
        if w == 2 and base_w2:
            base = base_w2
        elif w > 2 and base_w1:
            # falls es mehr als 2 Wochen gäbe: relativ zu week1_date
            base = base_w1 + timedelta(days=7*(w-1))
        if not base:
            return None
        idx = DAYS.index(tag) if tag in DAYS else 0
        return base + timedelta(days=idx)

    enforce_landscape(doc.sections[0])
    # DIN A4 Querformat erzwingen und Ränder setzen
    enforce_landscape(doc.sections[0])
    # A4-Maße in cm: 29.7 x 21.0 (Querformat: Breite 29.7, Höhe 21.0)
    try:
        doc.sections[0].page_width = Cm(29.7)
        doc.sections[0].page_height = Cm(21.0)
    except Exception:
        # Fallback falls Implementation abweicht
        pass

    doc.sections[0].left_margin = Cm(LEFT_MARGIN)
    doc.sections[0].right_margin = Cm(RIGHT_MARGIN)
    doc.sections[0].top_margin = Cm(TOP_MARGIN)
    doc.sections[0].bottom_margin = Cm(BOTTOM_MARGIN)

    # Kopfzeile für erste Section
    school_name_text = (time_info or {}).get("school_name", "") if time_info else ""
    set_header_for_section(doc.sections[0], school_name_text)

    # Globale Kollisionen der Nachnamen (≥4 Vorkommen im gesamten Plan)
    # Diese Menge wird für die Kurzschreibweise (Nachname + Initial) verwendet.
    all_rows_flat = [r for rows in grouped.values() for r in rows]
    collisions_global = collect_global_lastname_collisions(all_rows_flat, threshold=4)

    for idx, (w, day_str) in enumerate(day_order):
        if idx > 0:
            section = doc.add_section()
            enforce_landscape(section)
            # A4 Querformat auch für neue Sektionen explizit setzen
            try:
                section.page_width = Cm(29.7)
                section.page_height = Cm(21.0)
            except Exception:
                pass
            section.left_margin = Cm(LEFT_MARGIN)
            section.right_margin = Cm(RIGHT_MARGIN)
            section.top_margin = Cm(TOP_MARGIN)
            section.bottom_margin = Cm(BOTTOM_MARGIN)
            # In neuen Sektionen die Kopfzeile NICHT neu erzeugen,
            # sondern mit der vorherigen verknüpfen, damit Word sie automatisch übernimmt
            try:
                section.header.is_linked_to_previous = True
            except Exception:
                # Fallback: Einige python-docx-Versionen nutzen 'link_to_previous'
                try:
                    section.header.link_to_previous = True
                except Exception:
                    pass

        rows_for_day = grouped[(w, day_str)]

        # Slot-Labels für diesen Tag
        slot_key = f"{w}-{day_str}"
        day_slot_labels = slot_times.get(slot_key, [])
        num_slots = len(day_slot_labels)

        # Überschriften:
        # Zeile 1: "K o l l o q u i u m [aktuelles Jahr]" (Arial 24, fett, zentriert)
        title1 = doc.add_paragraph()
        title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run1 = title1.add_run(f"K o l l o q u i u m {datetime.now().year}")
        run1.bold = True
        run1.font.name = FONT_NAME
        run1.font.size = Pt(24)

        # Zeile 2: "[ausgeschriebener Tag], dd.mm.yyyy" (Arial 16, fett, zentriert)
        day_full = day_name_map.get(day_str, day_str)
        dt = date_for(w, day_str)
        if dt:
            date_str = dt.strftime("%d.%m.%Y")
            subtitle_text = f"{day_full}, {date_str}"
        else:
            subtitle_text = f"{day_full}"
        title2 = doc.add_paragraph()
        title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = title2.add_run(subtitle_text)
        run2.bold = True
        run2.font.name = FONT_NAME
        run2.font.size = Pt(16)

        # Kombinationen (Raum, Prüfer, Beisitzer) in erster Auftretensreihenfolge sammeln
        combos_order = []
        seen = set()
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in seen:
                combos_order.append(key)
                seen.add(key)

        # Datencontainer pro Kombination
        # Key: (room, pruefer, beisitzer)
        group_info: Dict[Tuple[Any, str, str], Dict[str, Any]] = OrderedDict()
        for key in combos_order:
            group_info[key] = {
                "fach": None,
                "room": key[0],
                "pruefer": key[1],
                "beisitzer": key[2],
                "slots": [""] * num_slots,
            }

        # Mapping Beginn -> Slotindex
        begin_to_idx = begin_to_idx_map(day_slot_labels)

        # Fülle Prüfungen in die jeweilige Kombination
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in group_info:
                # Falls Kombination erst hier auftaucht (Sicherheit), anlegen
                group_info[key] = {
                    "fach": None,
                    "room": room,
                    "pruefer": pruefer,
                    "beisitzer": beisitzer,
                    "slots": [""] * num_slots,
                }

            info = group_info[key]
            if info["fach"] is None:
                info["fach"] = r.get("Fach") or ""

            # Slotwahl
            slot_index = None
            if r.get("SlotIndex") is not None:
                try:
                    si = int(r.get("SlotIndex"))
                    if 0 <= si < num_slots:
                        slot_index = si
                except Exception:
                    pass

            if slot_index is None:
                start_norm = normalize_hhmm(r.get("Uhrzeit"))
                if start_norm in begin_to_idx:
                    slot_index = begin_to_idx[start_norm]
                elif r.get("Uhrzeit") in day_slot_labels:
                    slot_index = day_slot_labels.index(r.get("Uhrzeit"))

            # Schülername eintragen
            if slot_index is not None and 0 <= slot_index < num_slots:
                # Globale Kollisionen verwenden (nicht mehr tagesbezogen)
                name = short_student_name(r.get("Schueler") or "", collision_lastnames=collisions_global)
                # Individuelle Vorbereitungszeit anzeigen, wenn NTA > 0.
                # Modell:
                # - Vorbereitung dauert 30 Minuten
                # - Vorbereitung endet 5 Minuten vor Prüfungsbeginn
                # - Bei NTA x% verlängert sich die Dauer auf 30*(1+x/100)
                # - individueller Start = Slot-Beginn - (5 + Dauer)
                nta_val = 0
                try:
                    nta_val = int(r.get("NTA") or 0)
                except Exception:
                    nta_val = 0

                if nta_val > 0:
                    # Slot-Beginn für diesen Schüler ermitteln
                    label = day_slot_labels[slot_index] if slot_index < len(day_slot_labels) else None
                    b_tuple, _e = parse_begin_end(label) if label else (None, None)
                    if b_tuple:
                        b_h, b_m = b_tuple
                        dur_min = int(round(30 * (1 + (nta_val / 100.0))))
                        total_before = 5 + dur_min
                        start_min = (b_h * 60 + b_m) - total_before
                        if start_min < 0:
                            start_min = start_min % (24 * 60)
                        st_h, st_m = (start_min // 60) % 24, start_min % 60
                        name = f"{name} ({fmt_hh_dot_mm(st_h, st_m)})"
                info["slots"][slot_index] = name

        # Sortierung wie im Schülerplan: Raumtext, frühester belegter Slot, Erstauftreten
        def min_slot_index(slots_list):
            try:
                return min(i for i, v in enumerate(slots_list) if (v or "").strip() != "")
            except ValueError:
                return 10**6  # kein belegter Slot

        # Stabilitätsanker: Erstauftretensindex merken
        combo_with_keys = []
        for idx_combo, (key, info) in enumerate(group_info.items()):
            room_alpha = str(info.get("room")) if info.get("room") is not None else ""
            earliest = min_slot_index(info.get("slots", []))
            combo_with_keys.append((room_alpha, earliest, idx_combo, key))

        combo_with_keys.sort(key=lambda x: (x[0], x[1], x[2]))
        # group_info in der sortierten Reihenfolge neu aufbauen
        group_info = OrderedDict((key, group_info[key]) for (_, _, _, key) in combo_with_keys)

        # Tabelle: 1 Headerzeile + eine Zeile pro Kombination
        header_rows = 1
        total_rows = header_rows + len(group_info)
        total_cols = 4 + max(0, num_slots)

        table = doc.add_table(rows=total_rows, cols=total_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        add_table_borders(table)

        # Spaltenbreiten gemäß Vorgabe:
        widths = [COL_W_KURS, COL_W_PRUEFER, COL_W_BEISITZER, COL_W_RAUM] + [COL_W_SLOT] * num_slots
        set_column_widths(table, widths)

        # Header-Zeile: Höhe erhöhen, damit 2 Zeilen (Zeit + Vorbereitung) sicher sichtbar sind
        h1 = table.rows[0]
        try:
            set_row_height(h1, ROW_HEIGHT)  # 1.21 cm: robust für 2 Zeilen in Arial 14/12
        except Exception:
            # Fallback: alte Höhe verwenden, falls API abweicht
            set_row_height(h1, ROW_HEIGHT_CM)

        # Spalte 1: Kurs
        set_cell_text(h1.cells[0], "Kurs", bold=True)

        # Spalten 2+3: Lehrer (zusammengeführt)
        set_cell_text(h1.cells[1], "Lehrer", bold=True)
        merge_cells_horizontally(table, 0, 1, 2)

        # Spalte 4: Raum
        set_cell_text(h1.cells[3], "Raum", bold=True)

        # Slotspalten: Zeitlabels (mit Punkt-Format) + Vorbereitung (35 Min vorher)            
        for si in range(num_slots):
            col = 4 + si
            label = day_slot_labels[si] if si < len(day_slot_labels) else ""
            # Slot-Label in Punkt-Format wandeln (hh.mm - hh.mm)
            b, e = parse_begin_end(label)
            if b and e:
                label_dot = f"{fmt_hh_dot_mm(b[0], b[1])} - {fmt_hh_dot_mm(e[0], e[1])}"
            elif b:
                label_dot = fmt_hh_dot_mm(b[0], b[1])
            else:
                label_dot = label
            # Zeile 1: Slot-Label fett
            set_cell_text(h1.cells[col], label_dot, bold=True)
            # Zeile 2: Vorbereitung (35 Min vor Beginn), Arial 12 normal, zentriert
            # Kein neuer Absatz – stattdessen Zeilenumbruch im selben Absatz
            cell = h1.cells[col]
            p = cell.paragraphs[0]  # vorhandenen Absatz (vom Slot-Label) weiterverwenden
            br = p.add_run()
            br.add_break(WD_BREAK.LINE)  # Zeilenumbruch innerhalb desselben Absatzes
            if b:
                vh, vm = minus_35_min(b[0], b[1])
                prep_txt = f"Vorbereitung: {fmt_hh_dot_mm(vh, vm)}"
            else:
                prep_txt = "Vorbereitung:"
            run_prep = p.add_run(prep_txt)
            run_prep.bold = False
            run_prep.font.name = FONT_NAME
            run_prep.font.size = Pt(12)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Datenzeilen befüllen (eine Zeile pro Kombination)
        row_ptr = 1
        for (room, pruefer, beisitzer), info in group_info.items():
            row = table.rows[row_ptr]
            set_row_height(row, ROW_HEIGHT_CM)

            # Kurs
            set_cell_text(row.cells[0], info["fach"] or "", bold=False)

            # Lehrer-Spalten: Prüfer + Beisitzer
            set_cell_text(row.cells[1], pruefer or "", bold=False)
            set_cell_text(row.cells[2], beisitzer or "", bold=False)

            # Raum
            set_cell_text(row.cells[3], str(room) if room is not None else "", bold=False)

            # Slots: Schülernamen
            for si in range(num_slots):
                cell = row.cells[4 + si]
                full = info["slots"][si] or ""
                # Breitenbasierte Schriftgröße; lange zusammengesetzte Namen
                # werden bei Bedarf gekürzt. Die NTA-Zeit wird mitgemessen.
                base_text, nta_text, size_name, size_nta = _fit_slot_name(full)

                # Zelle leeren und manuell formatierte Runs schreiben
                cell.text = ""
                _set_cell_no_wrap(cell)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # Run 1: Name (fett, dynamische Größe)
                run_name = p.add_run(base_text)
                run_name.bold = True
                run_name.font.name = FONT_NAME
                run_name.font.size = Pt(size_name)

                # Run 2: NTA-Zeit in Klammern als eigener Run in Arial 10 fett
                if nta_text:
                    # optionales Leerzeichen vor der Klammer
                    run_space = p.add_run(" ")
                    run_space.font.name = FONT_NAME
                    run_space.font.size = Pt(size_name)

                    run_nta = p.add_run(nta_text)  # z. B. "(14.19)"
                    run_nta.bold = True
                    run_nta.font.name = FONT_NAME
                    run_nta.font.size = Pt(size_nta)

            # Zentrierung sicherstellen
            for c in range(total_cols):
                for p in row.cells[c].paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            row_ptr += 1

        # Abstand nach Tabelle
        doc.add_paragraph()

        # Vorbereitung: Raum <prepare_room> unter die Tabelle setzen (zentriert, Arial 16, fett)
        try:
            prepare_room_text = (time_info or {}).get("prepare_room", "")
        except Exception:
            prepare_room_text = ""
        if prepare_room_text:
            prep_para = doc.add_paragraph()
            prep_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            prep_run = prep_para.add_run(f"Vorbereitung: Raum {prepare_room_text}")
            prep_run.bold = True
            prep_run.font.name = FONT_NAME
            prep_run.font.size = Pt(16)

    doc.save(out_path)

def build_document_students(grouped: Dict[Tuple[int, str], List[Dict[str, Any]]],
                            slot_times: Dict[str, List[str]],
                            out_path: str,
                            time_info: Optional[Dict[str, Any]] = None,
                            students_note_text: str = "") -> None:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.enum.section import WD_ORIENTATION
    from datetime import datetime, timedelta
    import re

    doc = Document()

    # Hilfsfunktionen aus build_document (identisch übernommen)
    def parse_begin_end(label: str):
        if not label:
            return (None, None)
        part = label.strip()
        if "-" in part:
            b, e = [x.strip() for x in part.split("-", 1)]
        else:
            b, e = part, None
        mb = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", b) if b else None
        me = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", e) if e else None
        begin = (int(mb.group(1)), int(mb.group(2))) if mb else None
        end = (int(me.group(1)), int(me.group(2))) if me else None
        return (begin, end)

    def fmt_hh_dot_mm(h: int, m: int) -> str:
        return f"{h:02d}.{m:02d}"

    def minus_35_min(hh: int, mm: int):
        t = hh * 60 + mm - 35
        if t < 0:
            t = 0
        return ((t // 60) % 24, t % 60)

    def normalize_hhmm(s: Optional[str]) -> Optional[str]:
        if not s:
            return None
        s = s.strip()
        if "-" in s:
            s = s.split("-")[0].strip()
        parts = s.split(":")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            hh = int(parts[0])
            mm = int(parts[1])
            return f"{hh:02d}:{mm:02d}"
        return s

    def begin_to_idx_map(slot_labels: List[str]) -> Dict[str, int]:
        mapping = {}
        for i, lab in enumerate(slot_labels):
            b = normalize_hhmm(lab)
            if b:
                mapping[b] = i
        return mapping

    def enforce_landscape(section):
        section.orientation = WD_ORIENTATION.LANDSCAPE
        pw, ph = section.page_width, section.page_height
        if pw < ph:
            section.page_width, section.page_height = ph, pw

    def set_column_widths(table, widths_cm: List[float]):
        for i, w_cm in enumerate(widths_cm):
            if i < len(table.columns):
                table.columns[i].width = Cm(w_cm)
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                if i < len(widths_cm):
                    cell.width = Cm(widths_cm[i])

    def set_cell_text(cell, text: str, bold=False, size_pt: int = FONT_SIZE_DEFAULT, align_center=True):
        cell.text = ""
        p = cell.paragraphs[0]
        if align_center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text if text is not None else "")
        run.bold = bold
        font = run.font
        font.name = FONT_NAME
        font.size = Pt(size_pt)

    def set_row_height(row, height_cm: float):
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        for child in list(trPr):
            if child.tag == qn('w:trHeight'):
                trPr.remove(child)
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), str(int(height_cm * 567)))
        trHeight.set(qn('w:hRule'), 'exact')
        trPr.append(trHeight)

    def merge_cells_horizontally(table, row_idx: int, start_col: int, end_col: int):
        if end_col <= start_col:
            return
        a = table.cell(row_idx, start_col)
        b = table.cell(row_idx, end_col)
        a.merge(b)

    def add_table_borders(table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.append(tblPr)
        tblBorders = tblPr.find(qn('w:tblBorders'))
        if tblBorders is None:
            tblBorders = OxmlElement('w:tblBorders')
            tblPr.append(tblBorders)
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            tag = qn(f'w:{edge}')
            elem = tblBorders.find(tag)
            if elem is None:
                elem = OxmlElement(f'w:{edge}')
                tblBorders.append(elem)
            elem.set(qn('w:val'), 'single')
            elem.set(qn('w:sz'), '8')
            elem.set(qn('w:space'), '0')
            elem.set(qn('w:color'), '000000')

    # Globaler Stil
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = Pt(FONT_SIZE_DEFAULT)

    # Tage in Ausgabe-Reihenfolge
    day_order = []
    for w in sorted({w for (w, _) in grouped.keys()}):
        for d in DAYS:
            if (w, d) in grouped:
                day_order.append((w, d))

    day_name_map = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag"}
    def parse_date_safe(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None
    base_w1 = parse_date_safe((time_info or {}).get("week1_date"))
    base_w2 = parse_date_safe((time_info or {}).get("week2_date"))
    def date_for(w: int, tag: str) -> Optional[datetime]:
        base = base_w1
        if w == 2 and base_w2:
            base = base_w2
        elif w > 2 and base_w1:
            base = base_w1 + timedelta(days=7*(w-1))
        if not base:
            return None
        idx = DAYS.index(tag) if tag in DAYS else 0
        return base + timedelta(days=idx)

    # Querformat + Seitenränder (wie build_document)
    enforce_landscape(doc.sections[0])
    try:
        doc.sections[0].page_width = Cm(29.7)
        doc.sections[0].page_height = Cm(21.0)
    except Exception:
        pass
    doc.sections[0].left_margin = Cm(LEFT_MARGIN)
    doc.sections[0].right_margin = Cm(RIGHT_MARGIN)
    doc.sections[0].top_margin = Cm(TOP_MARGIN)
    doc.sections[0].bottom_margin = Cm(BOTTOM_MARGIN)

    # Kopfzeile für erste Section (wie build_document; nutzt set_header_for_section aus dem Modul)
    school_name_text = (time_info or {}).get("school_name", "") if time_info else ""
    set_header_for_section(doc.sections[0], school_name_text, variant="students")

    # Globale Nachnamenskollisionen (wie build_document)
    all_rows_flat = [r for rows in grouped.values() for r in rows]
    collisions_global = collect_global_lastname_collisions(all_rows_flat, threshold=4)

    for idx, (w, day_str) in enumerate(day_order):
        if idx > 0:
            section = doc.add_section()
            enforce_landscape(section)
            try:
                section.page_width = Cm(29.7)
                section.page_height = Cm(21.0)
            except Exception:
                pass
            section.left_margin = Cm(LEFT_MARGIN)
            section.right_margin = Cm(RIGHT_MARGIN)
            section.top_margin = Cm(TOP_MARGIN)
            section.bottom_margin = Cm(BOTTOM_MARGIN)
            try:
                section.header.is_linked_to_previous = True
            except Exception:
                try:
                    section.header.link_to_previous = True
                except Exception:
                    pass

        rows_for_day = grouped[(w, day_str)]
        slot_key = f"{w}-{day_str}"
        day_slot_labels = slot_times.get(slot_key, [])
        num_slots = len(day_slot_labels)

        # Titelzeilen (wie build_document)
        title1 = doc.add_paragraph()
        title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run1 = title1.add_run(f"K o l l o q u i u m {datetime.now().year}")
        run1.bold = True
        run1.font.name = FONT_NAME
        run1.font.size = Pt(24)

        day_full = day_name_map.get(day_str, day_str)
        dt = date_for(w, day_str)
        if dt:
            date_str = dt.strftime("%d.%m.%Y")
            subtitle_text = f"{day_full}, {date_str}"
        else:
            subtitle_text = f"{day_full}"
        title2 = doc.add_paragraph()
        title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = title2.add_run(subtitle_text)
        run2.bold = True
        run2.font.name = FONT_NAME
        run2.font.size = Pt(16)

        # Kombinationen (wie build_document), aber wir sortieren gleich wie dort
        combos_order = []
        seen = set()
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in seen:
                combos_order.append(key)
                seen.add(key)

        group_info: Dict[Tuple[Any, str, str], Dict[str, Any]] = OrderedDict()
        for key in combos_order:
            group_info[key] = {
                "fach": None,
                "room": key[0],
                "pruefer": key[1],
                "beisitzer": key[2],
                "slots": [""] * num_slots,
            }

        begin_to_idx = begin_to_idx_map(day_slot_labels)
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in group_info:
                group_info[key] = {
                    "fach": None,
                    "room": room,
                    "pruefer": pruefer,
                    "beisitzer": beisitzer,
                    "slots": [""] * num_slots,
                }
            info = group_info[key]
            if info["fach"] is None:
                info["fach"] = r.get("Fach") or ""

            slot_index = None
            if r.get("SlotIndex") is not None:
                try:
                    si = int(r.get("SlotIndex"))
                    if 0 <= si < num_slots:
                        slot_index = si
                except Exception:
                    pass
            if slot_index is None:
                start_norm = normalize_hhmm(r.get("Uhrzeit"))
                if start_norm in begin_to_idx:
                    slot_index = begin_to_idx[start_norm]
                elif r.get("Uhrzeit") in day_slot_labels:
                    slot_index = day_slot_labels.index(r.get("Uhrzeit"))

            if slot_index is not None and 0 <= slot_index < num_slots:
                name = short_student_name(r.get("Schueler") or "", collision_lastnames=collisions_global)
                nta_val = 0
                try:
                    nta_val = int(r.get("NTA") or 0)
                except Exception:
                    nta_val = 0
                if nta_val > 0:
                    label = day_slot_labels[slot_index] if slot_index < len(day_slot_labels) else None
                    b_tuple, _e = parse_begin_end(label) if label else (None, None)
                    if b_tuple:
                        b_h, b_m = b_tuple
                        dur_min = int(round(30 * (1 + (nta_val / 100.0))))
                        total_before = 5 + dur_min
                        start_min = (b_h * 60 + b_m) - total_before
                        if start_min < 0:
                            start_min = start_min % (24 * 60)
                        st_h, st_m = (start_min // 60) % 24, start_min % 60
                        name = f"{name} ({fmt_hh_dot_mm(st_h, st_m)})"
                info["slots"][slot_index] = name

        def min_slot_index(slots_list):
            try:
                return min(i for i, v in enumerate(slots_list) if (v or "").strip() != "")
            except ValueError:
                return 10**6

        # Sortierreihenfolge wie build_document
        combo_with_keys = []
        for idx_combo, (key, info) in enumerate(group_info.items()):
            room_alpha = str(info.get("room")) if info.get("room") is not None else ""
            earliest = min_slot_index(info.get("slots", []))
            combo_with_keys.append((room_alpha, earliest, idx_combo, key))
        combo_with_keys.sort(key=lambda x: (x[0], x[1], x[2]))
        group_info = OrderedDict((key, group_info[key]) for (_, _, _, key) in combo_with_keys)

        # Tabelle: 1 Headerzeile + eine Zeile pro Kombination; Spalten: Kurs | Lehrer(2) | Slots...
        # Variante "Schüler": KEINE Raum-Spalte
        header_rows = 1
        total_rows = header_rows + len(group_info)
        total_cols = 3 + max(0, num_slots)  # Kurs(1) + Lehrer zusammengeführt(2) + Slots

        table = doc.add_table(rows=total_rows, cols=total_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        add_table_borders(table)

        # Spaltenbreiten: Kurs, Prüfer, Beisitzer, Slots...
        widths = [COL_W_KURS, COL_W_PRUEFER, COL_W_BEISITZER] + [COL_W_SLOT] * num_slots
        set_column_widths(table, widths)

        # Header-Zeile höher (wie build_document)
        h1 = table.rows[0]
        try:
            set_row_height(h1, ROW_HEIGHT)
        except Exception:
            set_row_height(h1, ROW_HEIGHT_CM)

        # Kurs
        set_cell_text(h1.cells[0], "Kurs", bold=True)
        # Lehrer (Prüfer+Beisitzer zusammenführen)
        set_cell_text(h1.cells[1], "Lehrer", bold=True)
        merge_cells_horizontally(table, 0, 1, 2)

        # Slotspalten: Kopf-Inhalt getauscht: Vorbereitung fett zuerst, danach Prüfung normal
        for si in range(num_slots):
            col = 3 + si
            label = day_slot_labels[si] if si < len(day_slot_labels) else ""
            b, e = parse_begin_end(label)
            if b and e:
                label_dot = f"{fmt_hh_dot_mm(b[0], b[1])} - {fmt_hh_dot_mm(e[0], e[1])}"
            elif b:
                label_dot = fmt_hh_dot_mm(b[0], b[1])
            else:
                label_dot = label
            cell = h1.cells[col]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Vorbereitung zuerst (fett)
            if b:
                vh, vm = minus_35_min(b[0], b[1])
                prep_txt = f"Vorbereitung: {fmt_hh_dot_mm(vh, vm)}"
            else:
                prep_txt = "Vorbereitung:"
            run_prep = p.add_run(prep_txt)
            run_prep.bold = True
            run_prep.font.name = FONT_NAME
            run_prep.font.size = Pt(12)
            # Zeilenumbruch
            br = p.add_run()
            br.add_break(WD_BREAK.LINE)
            # Prüfung normal, mit Präfix "Prüfung:" und Schriftgröße 10
            run_exam = p.add_run(f"Prüfung: {label_dot}")
            run_exam.bold = False
            run_exam.font.name = FONT_NAME
            run_exam.font.size = Pt(FONT_SIZE_EXAM_STUDENT)

        # Datenzeilen
        row_ptr = 1
        for (_room, pruefer, beisitzer), info in group_info.items():
            row = table.rows[row_ptr]
            set_row_height(row, ROW_HEIGHT_CM)
            # Kurs
            set_cell_text(row.cells[0], info["fach"] or "", bold=False)
            # Lehrer
            set_cell_text(row.cells[1], pruefer or "", bold=False)
            set_cell_text(row.cells[2], beisitzer or "", bold=False)
            # Slots
            for si in range(num_slots):
                cell = row.cells[3 + si]
                full = info["slots"][si] or ""
                base_text, nta_text, size_name, size_nta = _fit_slot_name(full)
                cell.text = ""
                _set_cell_no_wrap(cell)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_name = p.add_run(base_text)
                run_name.bold = True
                run_name.font.name = FONT_NAME
                run_name.font.size = Pt(size_name)
                if nta_text:
                    run_space = p.add_run(" ")
                    run_space.font.name = FONT_NAME
                    run_space.font.size = Pt(size_name)
                    run_nta = p.add_run(nta_text)
                    run_nta.bold = True
                    run_nta.font.name = FONT_NAME
                    run_nta.font.size = Pt(size_nta)
            # Zentrieren
            for c in range(total_cols):
                for p in row.cells[c].paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_ptr += 1

        # Abstand nach Tabelle
        doc.add_paragraph()

        # Schüler-Variante: Hinweistext aus Eingabe statt „Vorbereitung: Raum …“
        note = (students_note_text or "").strip()
        if note:
            prep_para = doc.add_paragraph()
            prep_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            prep_run = prep_para.add_run(note)
            prep_run.bold = True
            prep_run.font.name = FONT_NAME
            prep_run.font.size = Pt(16)

    doc.save(out_path)
    
def build_document_cleaning(grouped: Dict[Tuple[int, str], List[Dict[str, Any]]],
                            slot_times: Dict[str, List[str]],
                            out_path: str,
                            time_info: Optional[Dict[str, Any]] = None) -> None:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.enum.section import WD_ORIENTATION
    from datetime import datetime, timedelta
    import re

    doc = Document()

    # Hilfsfunktionen aus build_document (identisch übernommen)
    def parse_begin_end(label: str):
        if not label:
            return (None, None)
        part = label.strip()
        if "-" in part:
            b, e = [x.strip() for x in part.split("-", 1)]
        else:
            b, e = part, None
        mb = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", b) if b else None
        me = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", e) if e else None
        begin = (int(mb.group(1)), int(mb.group(2))) if mb else None
        end = (int(me.group(1)), int(me.group(2))) if me else None
        return (begin, end)

    def fmt_hh_dot_mm(h: int, m: int) -> str:
        return f"{h:02d}.{m:02d}"

    def normalize_hhmm(s: Optional[str]) -> Optional[str]:
        if not s:
            return None
        s = s.strip()
        if "-" in s:
            s = s.split("-")[0].strip()
        parts = s.split(":")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            hh = int(parts[0])
            mm = int(parts[1])
            return f"{hh:02d}:{mm:02d}"
        return s

    def begin_to_idx_map(slot_labels: List[str]) -> Dict[str, int]:
        mapping = {}
        for i, lab in enumerate(slot_labels):
            b = normalize_hhmm(lab)
            if b:
                mapping[b] = i
        return mapping

    def enforce_landscape(section):
        section.orientation = WD_ORIENTATION.LANDSCAPE
        pw, ph = section.page_width, section.page_height
        if pw < ph:
            section.page_width, section.page_height = ph, pw

    def set_column_widths(table, widths_cm: List[float]):
        for i, w_cm in enumerate(widths_cm):
            if i < len(table.columns):
                table.columns[i].width = Cm(w_cm)
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                if i < len(widths_cm):
                    cell.width = Cm(widths_cm[i])

    def set_cell_text(cell, text: str, bold=False, size_pt: int = FONT_SIZE_DEFAULT, align_center=True):
        cell.text = ""
        p = cell.paragraphs[0]
        if align_center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text if text is not None else "")
        run.bold = bold
        font = run.font
        font.name = FONT_NAME
        font.size = Pt(size_pt)

    def set_row_height(row, height_cm: float):
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        for child in list(trPr):
            if child.tag == qn('w:trHeight'):
                trPr.remove(child)
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), str(int(height_cm * 567)))
        trHeight.set(qn('w:hRule'), 'exact')
        trPr.append(trHeight)

    def merge_cells_horizontally(table, row_idx: int, start_col: int, end_col: int):
        if end_col <= start_col:
            return
        a = table.cell(row_idx, start_col)
        b = table.cell(row_idx, end_col)
        a.merge(b)

    def add_table_borders(table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            tbl.append(tblPr)
        tblBorders = tblPr.find(qn('w:tblBorders'))
        if tblBorders is None:
            tblBorders = OxmlElement('w:tblBorders')
            tblPr.append(tblBorders)
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            tag = qn(f'w:{edge}')
            elem = tblBorders.find(tag)
            if elem is None:
                elem = OxmlElement(f'w:{edge}')
                tblBorders.append(elem)
            elem.set(qn('w:val'), 'single')
            elem.set(qn('w:sz'), '8')
            elem.set(qn('w:space'), '0')
            elem.set(qn('w:color'), '000000')

    # Globaler Stil
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = Pt(FONT_SIZE_DEFAULT)

    # Tage in Ausgabe-Reihenfolge
    day_order = []
    for w in sorted({w for (w, _) in grouped.keys()}):
        for d in DAYS:
            if (w, d) in grouped:
                day_order.append((w, d))

    day_name_map = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag"}
    def parse_date_safe(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None
    base_w1 = parse_date_safe((time_info or {}).get("week1_date"))
    base_w2 = parse_date_safe((time_info or {}).get("week2_date"))
    def date_for(w: int, tag: str) -> Optional[datetime]:
        base = base_w1
        if w == 2 and base_w2:
            base = base_w2
        elif w > 2 and base_w1:
            base = base_w1 + timedelta(days=7*(w-1))
        if not base:
            return None
        idx = DAYS.index(tag) if tag in DAYS else 0
        return base + timedelta(days=idx)

    # Querformat + Seitenränder (wie build_document)
    enforce_landscape(doc.sections[0])
    try:
        doc.sections[0].page_width = Cm(29.7)
        doc.sections[0].page_height = Cm(21.0)
    except Exception:
        pass
    doc.sections[0].left_margin = Cm(LEFT_MARGIN)
    doc.sections[0].right_margin = Cm(RIGHT_MARGIN)
    doc.sections[0].top_margin = Cm(TOP_MARGIN)
    doc.sections[0].bottom_margin = Cm(BOTTOM_MARGIN)

    # Kopfzeile für erste Section (wie build_document)
    school_name_text = (time_info or {}).get("school_name", "") if time_info else ""
    set_header_for_section(doc.sections[0], school_name_text, variant="cleaning")

    for idx, (w, day_str) in enumerate(day_order):
        if idx > 0:
            section = doc.add_section()
            enforce_landscape(section)
            try:
                section.page_width = Cm(29.7)
                section.page_height = Cm(21.0)
            except Exception:
                pass
            section.left_margin = Cm(LEFT_MARGIN)
            section.right_margin = Cm(RIGHT_MARGIN)
            section.top_margin = Cm(TOP_MARGIN)
            section.bottom_margin = Cm(BOTTOM_MARGIN)
            try:
                section.header.is_linked_to_previous = True
            except Exception:
                try:
                    section.header.link_to_previous = True
                except Exception:
                    pass

        rows_for_day = grouped[(w, day_str)]
        slot_key = f"{w}-{day_str}"
        day_slot_labels = slot_times.get(slot_key, [])
        num_slots = len(day_slot_labels)

        # Titelzeilen (wie build_document)
        title1 = doc.add_paragraph()
        title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run1 = title1.add_run(f"K o l l o q u i u m {datetime.now().year}")
        run1.bold = True
        run1.font.name = FONT_NAME
        run1.font.size = Pt(24)

        day_full = day_name_map.get(day_str, day_str)
        dt = date_for(w, day_str)
        if dt:
            date_str = dt.strftime("%d.%m.%Y")
            subtitle_text = f"{day_full}, {date_str}"
        else:
            subtitle_text = f"{day_full}"
        title2 = doc.add_paragraph()
        title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = title2.add_run(subtitle_text)
        run2.bold = True
        run2.font.name = FONT_NAME
        run2.font.size = Pt(16)

        # Kombinationen (Raum, Prüfer, Beisitzer) wie build_document
        combos_order = []
        seen = set()
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in seen:
                combos_order.append(key)
                seen.add(key)

        group_info: Dict[Tuple[Any, str, str], Dict[str, Any]] = OrderedDict()
        for key in combos_order:
            group_info[key] = {
                "fach": None,
                "room": key[0],
                "pruefer": key[1],
                "beisitzer": key[2],
                "slots": [""] * num_slots,
            }

        begin_to_idx = begin_to_idx_map(day_slot_labels)
        for r in rows_for_day:
            room = r.get("Raum")
            pruefer = r.get("Pruefer") or ""
            beisitzer = r.get("Beisitzer") or ""
            key = (room, pruefer, beisitzer)
            if key not in group_info:
                group_info[key] = {
                    "fach": None,
                    "room": room,
                    "pruefer": pruefer,
                    "beisitzer": beisitzer,
                    "slots": [""] * num_slots,
                }
            info = group_info[key]
            if info["fach"] is None:
                info["fach"] = r.get("Fach") or ""

            slot_index = None
            if r.get("SlotIndex") is not None:
                try:
                    si = int(r.get("SlotIndex"))
                    if 0 <= si < num_slots:
                        slot_index = si
                except Exception:
                    pass
            if slot_index is None:
                start_norm = normalize_hhmm(r.get("Uhrzeit"))
                if start_norm in begin_to_idx:
                    slot_index = begin_to_idx[start_norm]
                elif r.get("Uhrzeit") in day_slot_labels:
                    slot_index = day_slot_labels.index(r.get("Uhrzeit"))

            if slot_index is not None and 0 <= slot_index < num_slots:
                # Reinigung: Schülernamen anonymisieren -> "Prüfung" (nur Kennzeichnung)
                name = "Prüfung" if (r.get("Schueler") or "").strip() else ""
                info["slots"][slot_index] = name

        # Sortierung (stabil wie Erstauftreten; Raumname sekundär)
        def min_slot_index(slots_list):
            try:
                return min(i for i, v in enumerate(slots_list) if (v or "").strip() != "")
            except ValueError:
                return 10**6
        combo_with_keys = []
        for idx_combo, (key, info) in enumerate(group_info.items()):
            room_alpha = str(info.get("room")) if info.get("room") is not None else ""
            earliest = min_slot_index(info.get("slots", []))
            combo_with_keys.append((room_alpha, earliest, idx_combo, key))
        combo_with_keys.sort(key=lambda x: (x[0], x[1], x[2]))
        group_info = OrderedDict((key, group_info[key]) for (_, _, _, key) in combo_with_keys)

        # Tabelle: 1 Headerzeile + eine Zeile pro Kombination
        # Variante "Reinigung": KEINE Kurs- und Lehrer-Spalten; dafür Raum bleibt bestehen
        header_rows = 1
        total_rows = header_rows + len(group_info)
        total_cols = 1 + max(0, num_slots)  # Raum + Slots

        table = doc.add_table(rows=total_rows, cols=total_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        add_table_borders(table)

        # Spaltenbreiten: Raum, Slots...
        widths = [COL_W_RAUM] + [COL_W_SLOT] * num_slots
        set_column_widths(table, widths)

        # Header-Zeile
        h1 = table.rows[0]
        try:
            set_row_height(h1, ROW_HEIGHT)
        except Exception:
            set_row_height(h1, ROW_HEIGHT_CM)

        # Raum
        set_cell_text(h1.cells[0], "Raum", bold=True)

        # Slotspalten: Zeitlabels normal (wie build_document), Vorbereitung wird nicht extra in Kopf fett markiert
        for si in range(num_slots):
            col = 1 + si
            label = day_slot_labels[si] if si < len(day_slot_labels) else ""
            b, e = parse_begin_end(label)
            if b and e:
                label_dot = f"{fmt_hh_dot_mm(b[0], b[1])} - {fmt_hh_dot_mm(e[0], e[1])}"
            elif b:
                label_dot = fmt_hh_dot_mm(b[0], b[1])
            else:
                label_dot = label
            set_cell_text(h1.cells[col], label_dot, bold=True)

        # Datenzeilen
        row_ptr = 1
        for (room, _pruefer, _beisitzer), info in group_info.items():
            row = table.rows[row_ptr]
            set_row_height(row, ROW_HEIGHT_CM)
            # Raum
            set_cell_text(row.cells[0], str(room) if room is not None else "", bold=False)
            # Slots
            for si in range(num_slots):
                cell = row.cells[1 + si]
                val = (info["slots"][si] or "").strip()
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.bold = True if val else False
                run.font.name = FONT_NAME
                run.font.size = Pt(FONT_SIZE_DEFAULT)
                # Belegte Slots dunkelgrau hinterlegen
                if val:
                    tcPr = cell._tc.get_or_add_tcPr()
                    # w:shd-Element suchen oder anlegen
                    shd = tcPr.find(qn('w:shd'))
                    if shd is None:
                        shd = OxmlElement('w:shd')
                        tcPr.append(shd)
                    # Schattierungsattribute setzen
                    shd.set(qn('w:val'), 'clear')
                    shd.set(qn('w:color'), 'auto')
                    shd.set(qn('w:fill'), '666666')  # dunkelgrau
            # Zentrierung
            for c in range(total_cols):
                for p in row.cells[c].paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_ptr += 1

        # Abstand nach Tabelle
        doc.add_paragraph()

        # Vorbereitungsraum weiterhin textlich unterhalb der Tabelle
        try:
            prepare_room_text = (time_info or {}).get("prepare_room", "")
        except Exception:
            prepare_room_text = ""
        if prepare_room_text:
            prep_para = doc.add_paragraph()
            prep_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            prep_run = prep_para.add_run(f"Vorbereitung: Raum {prepare_room_text}")
            prep_run.bold = True
            prep_run.font.name = FONT_NAME
            prep_run.font.size = Pt(16)

    doc.save(out_path)

def build_xlsx(grouped: Dict[Tuple[int, str], List[Dict[str, Any]]],
               slot_times: Dict[str, List[str]],
               out_path: str,
               time_info: Optional[Dict[str, Any]] = None) -> None:
    """
    Erzeugt eine Excel-Tabelle mit folgender Struktur:
    A ID | B Schüler | C Kurs | D Thema | E Prüfer | F Beisitzer | G Tag | H-J Vorbereitung | K-M Prüfung | N-P Absperrung
    - H = Vorbereitungsraum (aus time_info['prepare_room'])
    - I = Beginn Vorbereitung = Prüfungsbeginn - (30*(1+NTA/100)) - 5 Min
    - J = Ende Vorbereitung = 5 Min vor Prüfungsbeginn
    - K = Prüfungsraum
    - L = Prüfungsbeginn
    - M = Prüfungsende = Prüfungsbeginn + slot_len_min
    Datum (G): "Mo. dd.mm.yyyy"
    Kopfzeilen: AutoFilter, H-J gemergt "Vorbereitung", K-M gemergt "Prüfung", N-P gemergt "Absperrung"
    """
    # Schutz: openpyxl vorhanden?
    try:
        Workbook  # noqa
    except Exception:
        raise RuntimeError("openpyxl ist nicht installiert. Bitte 'pip install openpyxl' ausführen.")

    from datetime import datetime, timedelta
    import re

    # Hilfsfunktionen (analog zum DOCX-Export)
    def parse_begin_end(label: str):
        if not label:
            return (None, None)
        part = label.strip()
        if "-" in part:
            b, e = [x.strip() for x in part.split("-", 1)]
        else:
            b, e = part, None
        mb = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", b) if b else None
        me = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", e) if e else None
        begin = (int(mb.group(1)), int(mb.group(2))) if mb else None
        end = (int(me.group(1)), int(me.group(2))) if me else None
        return (begin, end)

    def norm_hhmm(s: Optional[str]) -> Optional[str]:
        if not s:
            return None
        s = s.strip()
        if "-" in s:
            s = s.split("-")[0].strip()
        return s

    def begin_to_idx_map(slot_labels: List[str]) -> Dict[str, int]:
        mapping = {}
        for i, lab in enumerate(slot_labels):
            b = norm_hhmm(lab)
            if b:
                mapping[b] = i
        return mapping

    DAYS = ["Mo", "Di", "Mi", "Do", "Fr"]
    day_name_map = {"Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag", "Fr": "Freitag"}

    def parse_date_safe(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None

    base_w1 = parse_date_safe((time_info or {}).get("week1_date"))
    base_w2 = parse_date_safe((time_info or {}).get("week2_date"))
    slot_len_min = int((time_info or {}).get("slot_len_min", 30))
    prepare_room = (time_info or {}).get("prepare_room", "")

    def date_for(w: int, tag: str) -> Optional[datetime]:
        base = base_w1
        if w == 2 and base_w2:
            base = base_w2
        elif w > 2 and base_w1:
            base = base_w1 + timedelta(days=7 * (w - 1))
        if not base:
            return None
        idx = DAYS.index(tag) if tag in DAYS else 0
        return base + timedelta(days=idx)

    # Flatten grouped -> Listenzeilen
    rows_out: List[Dict[str, Any]] = []
    # Reihenfolge: Woche, Tag (Mo..Fr), dann innerhalb Tages nach SlotIndex/Start
    for w in sorted({w for (w, _) in grouped.keys()}):
        for d in DAYS:
            key = (w, d)
            if key not in grouped:
                continue
            day_rows = list(grouped[key])
            # Sortierung innerhalb Tages: nach SlotIndex, dann Raum, dann ID
            slot_labels = slot_times.get(f"{w}-{d}", [])
            b2i = begin_to_idx_map(slot_labels)
            def slot_key(r):
                # SlotIndex bevorzugt, sonst über Uhrzeit
                si = r.get("SlotIndex")
                if si is None:
                    b = norm_hhmm(r.get("Uhrzeit"))
                    si = b2i.get(b, 10**6)
                room = r.get("Raum") or ""
                rid = int("".join(ch for ch in str(room) if ch.isdigit()) or "0")
                return (si, rid, r.get("ID") or 0)
            day_rows.sort(key=slot_key)
            # in rows_out eintragen
            for r in day_rows:
                rows_out.append(dict(r))

    # Excel erstellen
    wb = Workbook()
    ws = wb.active
    ws.title = "Kolloquiumsplan"

    # Nutzer-Optionen aus time_info lesen (Default: alle True)
    options = {}
    if time_info and isinstance(time_info.get("options"), dict):
        options = dict(time_info["options"])
    else:
        options = {
            "ID": True, "Schüler": True, "Kurs": True, "Thema": True,
            "Prüfer": True, "Beisitzer": True, "Tag": True,
            "Vorbereitung": True, "Prüfung": True, "Absperrung": True
        }

    prepare_room = (time_info or {}).get("prepare_room") or ""

    # Spaltenbreiten nach Bezeichnung (fix)
    WIDTHS_BY_NAME = {
        "ID": 6,
        "Schüler": 24,
        "Kurs": 10,
        "Thema": 10,
        "Prüfer": 10,
        "Beisitzer": 10,
        "Tag": 16,
        "Vorbereitung_Raum": 12, "Vorbereitung_Beginn": 9, "Vorbereitung_Ende": 9,
        "Prüfung_Raum": 10, "Prüfung_Beginn": 9, "Prüfung_Ende": 9,
        "Absperrung_Raum": 12, "Absperrung_Beginn": 9, "Absperrung_Ende": 9,
    }

    # Dynamische Spalten-Definitionen
    cols = []  # (group, top_label, bottom_label, write_fn, width_name)

    if options.get("ID", True):
        cols.append((None, "ID", "ID", lambda r, wsi: r.get("ID"), "ID"))
    if options.get("Schüler", True):
        cols.append((None, "Schüler", "Schüler", lambda r, wsi: r.get("Schueler") or "", "Schüler"))
    if options.get("Kurs", True):
        cols.append((None, "Kurs", "Kurs", lambda r, wsi: r.get("Fach") or "", "Kurs"))
    if options.get("Thema", True):
        cols.append((None, "Thema", "Thema", lambda r, wsi: r.get("Thema") or "", "Thema"))
    if options.get("Prüfer", True):
        cols.append((None, "Prüfer", "Prüfer", lambda r, wsi: r.get("Pruefer") or "", "Prüfer"))
    if options.get("Beisitzer", True):
        cols.append((None, "Beisitzer", "Beisitzer", lambda r, wsi: r.get("Beisitzer") or "", "Beisitzer"))
    if options.get("Tag", True):
        cols.append((None, "Tag", "Tag", lambda r, wsi: format_day_with_date(int(r.get("Woche")), str(r.get("Tag"))), "Tag"))

    if options.get("Vorbereitung", True):
        cols.extend([
            ("Vorbereitung", "Vorbereitung", "Raum",   lambda r, wsi: prepare_room or "", "Vorbereitung_Raum"),
            ("Vorbereitung", None,           "Beginn", lambda r, wsi: (wsi[0] - timedelta(minutes=5 + int(round(30 * (1 + (int(r.get('NTA') or 0) / 100.0)))))).strftime("%H:%M") if wsi[0] else "", "Vorbereitung_Beginn"),
            ("Vorbereitung", None,           "Ende",   lambda r, wsi: (wsi[0] - timedelta(minutes=5)).strftime("%H:%M") if wsi[0] else "", "Vorbereitung_Ende"),
        ])
    if options.get("Prüfung", True):
        cols.extend([
            ("Prüfung", "Prüfung", "Raum",   lambda r, wsi: r.get("Raum") or "", "Prüfung_Raum"),
            ("Prüfung", None,     "Beginn", lambda r, wsi: wsi[0].strftime("%H:%M") if wsi[0] else "", "Prüfung_Beginn"),
            ("Prüfung", None,     "Ende",   lambda r, wsi: wsi[1].strftime("%H:%M") if wsi[1] else "", "Prüfung_Ende"),
        ])
    if options.get("Absperrung", True):
        cols.extend([
            ("Absperrung", "Absperrung", "Raum",   lambda r, wsi: (cluster_info_by_exam.get(r.get("ID")) or {}).get("abs_room") or "", "Absperrung_Raum"),
            ("Absperrung", None,         "Beginn", lambda r, wsi: ((cluster_info_by_exam.get(r.get("ID")) or {}).get("abs_begin") or None).strftime("%H:%M") if (cluster_info_by_exam.get(r.get("ID")) or {}).get("abs_begin") else "", "Absperrung_Beginn"),
            ("Absperrung", None,         "Ende",   lambda r, wsi: ((cluster_info_by_exam.get(r.get("ID")) or {}).get("abs_end") or None).strftime("%H:%M") if (cluster_info_by_exam.get(r.get("ID")) or {}).get("abs_end") else "", "Absperrung_Ende"),
        ])

    # Kopfzeilen (2 Zeilen) + Merges dynamisch
    headers_top = []
    headers_bottom = []
    merge_instructions = []

    i = 0
    col_index = 1
    while i < len(cols):
        grp, top, bot, _fn, _w = cols[i]
        if grp is None:
            headers_top.append(top)
            headers_bottom.append(bot)
            merge_instructions.append((1, col_index, 2, col_index))
            col_index += 1
            i += 1
        else:
            g = cols[i:i+3]
            headers_top.extend([g[0][1], None, None])
            headers_bottom.extend([g[0][2], g[1][2], g[2][2]])
            merge_instructions.append((1, col_index, 1, col_index+2))
            col_index += 3
            i += 3

    ws.append(headers_top)
    ws.append(headers_bottom)
    for (r1, c1, r2, c2) in merge_instructions:
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)

    # Format Kopfzeilen
    def apply_header_style(cells):
        for cell in cells:
            cell.alignment = XLSX_CENTER
            name, size, bold = XLSX_HEADER_FONT
            cell.font = Font(name=name, size=size, bold=bold)
            # Rahmen dünn
            cell.border = Border(left=XLSX_THIN_BORDER, right=XLSX_THIN_BORDER, top=XLSX_THIN_BORDER, bottom=XLSX_THIN_BORDER)

    apply_header_style(ws[1])
    apply_header_style(ws[2])

    # Hilf: Format Datumstext "Mo. dd.mm.yyyy"
    def format_day_with_date(w: int, tag: str) -> str:
        dt = date_for(w, tag)
        day_abbr = f"{tag}."
        if dt:
            return f"{day_abbr} {dt.strftime('%d.%m.%Y')}"
        return day_abbr

    # Slot-Beginn/Ende aus SlotIndex oder Uhrzeit berechnen
    def slot_start_end_for(r: Dict[str, Any]) -> Tuple[Optional[datetime], Optional[datetime]]:
        tag = str(r.get("Tag"))
        w = int(r.get("Woche"))
        labels = slot_times.get(f"{w}-{tag}", [])
        si = r.get("SlotIndex")
        if si is not None and 0 <= int(si) < len(labels):
            lab = labels[int(si)]
        else:
            # Versuche Uhrzeit-String als Label zu finden
            u = r.get("Uhrzeit")
            lab = None
            if u in labels:
                lab = u
            else:
                # match by begin time
                u_beg = norm_hhmm(u)
                for lab2 in labels:
                    b, _e = parse_begin_end(lab2)
                    if b and u_beg == f"{b[0]:02d}:{b[1]:02d}":
                        lab = lab2
                        break
        if not lab:
            return (None, None)
        b, e = parse_begin_end(lab)
        if not b:
            return (None, None)
        # Datumsteil für den Tag
        dt_day = date_for(w, tag) or datetime.now()
        start_dt = dt_day.replace(hour=b[0], minute=b[1], second=0, microsecond=0)
        end_dt = start_dt + timedelta(minutes=slot_len_min)
        return (start_dt, end_dt)

    # Themencluster-Ermittlung pro Tag: map (Woche, Tag) -> Liste von Reihen (sortiert nach Start)
    # Wir bilden Cluster pro (Thema, Fach, Pruefer) mit zeitlicher Reihung am selben Tag.
    from collections import defaultdict
    by_day = defaultdict(list)
    for r in rows_out:
        by_day[(int(r.get("Woche")), str(r.get("Tag")))].append(r)
    # Hilfsfunktion: gruppiere nach (Thema, Fach, Pruefer) und sortiere nach Start_dt
    def clusters_for_day(day_rows):
        groups = defaultdict(list)
        for rr in day_rows:
            key = ((rr.get("Thema") or "").strip(),
                   (rr.get("Fach") or "").strip(),
                   (rr.get("Pruefer") or "").strip())
            groups[key].append(rr)
        clusters = []
        for key, items in groups.items():
            # nur wenn Thema gesetzt
            if key[0] == "":
                continue
            # Startzeiten berechnen
            decorated = []
            for it in items:
                s_dt, _e_dt = slot_start_end_for(it)
                decorated.append((s_dt, it))
            decorated.sort(key=lambda x: (x[0] or 0))
            # gesamte Sequenz als eine zeitliche Reihe betrachten
            seq = [it for (_s, it) in decorated if _s is not None]
            if 3 <= len(seq) <= 5:
                clusters.append(seq)
        return clusters
 
    # Precompute: pro (Woche, Tag) die Cluster und die Vorbereitungs-Startzeit des letzten
    cluster_info_by_exam = {}
    for (w_d, day_rows) in by_day.items():
        clist = clusters_for_day(day_rows)
        for cl in clist:
            # letzter Schueler des Clusters
            last = cl[-1]
            last_start_dt, _last_end_dt = slot_start_end_for(last)
            # Vorbereitung des letzten: Ende = 5 Min vor Pruefungsbeginn; Beginn = Ende - (30*(1+NTA/100))
            last_nta = 0
            try:
                last_nta = int(last.get("NTA") or 0)
            except Exception:
                last_nta = 0
            last_prep_end = (last_start_dt - timedelta(minutes=5)) if last_start_dt else None
            last_prep_begin = (last_prep_end - timedelta(minutes=int(round(30*(1+(last_nta/100.0)))))) if last_prep_end else None
            # fuer die ersten k Schueler laut Staffelung Absperrung eintragen
            k = 1 if len(cl) == 3 else (2 if len(cl) == 4 else 3)  # 3->1, 4->2, 5->3
            for idx_in_seq, exam_row in enumerate(cl):
                if idx_in_seq < k:
                    # Beginn = Ende seiner Pruefung; Ende = last_prep_begin
                    _s_dt, e_dt = slot_start_end_for(exam_row)
                    cluster_info_by_exam[exam_row.get("ID")] = {
                        "abs_room": prepare_room or "",
                        "abs_begin": e_dt,
                        "abs_end": last_prep_begin
                    }
                else:
                    # kein Eintrag fuer spaetere im Cluster
                    cluster_info_by_exam.setdefault(exam_row.get("ID"), None)
 
    # Datenzeilen
    row_idx = 3
    for r in rows_out:
        start_dt, end_dt = slot_start_end_for(r)
 
        # Werte dynamisch je Spalte schreiben
        col_no = 1
        for (_grp, _top, _bot, writer, _wname) in cols:
            ws.cell(row=row_idx, column=col_no, value=writer(r, (start_dt, end_dt)))
            col_no += 1

        # Stil dynamisch je vorhandener Spalte
        for col in range(1, len(cols) + 1):
            c = ws.cell(row=row_idx, column=col)
            bot_label = headers_bottom[col - 1]
            is_time_like = bot_label in ("Tag", "Beginn", "Ende")
            c.alignment = XLSX_CENTER if is_time_like else Alignment(vertical="center", wrap_text=True)
            c.border = Border(left=XLSX_THIN_BORDER, right=XLSX_THIN_BORDER, top=XLSX_THIN_BORDER, bottom=XLSX_THIN_BORDER)
            name, size, bold = XLSX_BODY_FONT
            c.font = Font(name=name, size=size, bold=bold)
        row_idx += 1

    # Spaltenbreiten nach Bezeichnung
    for idx, (_grp, _top, _bot, _fn, wname) in enumerate(cols, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = WIDTHS_BY_NAME.get(wname, 10)

    # AutoFilter dynamisch
    last_col = get_column_letter(len(cols))
    ws.auto_filter.ref = f"A2:{last_col}{max(2, row_idx - 1)}"

    # Höhe Kopfzeilen
    ws.row_dimensions[1].height = 20
    ws.row_dimensions[2].height = 20

    wb.save(out_path)

def main():
    if len(sys.argv) < 4:
        print("Aufruf: python export.py <kolloquiumsplan.json> <slot_times.json> <output.docx>")
        sys.exit(1)
    plan_json = sys.argv[1]
    slot_json = sys.argv[2]
    out_docx = sys.argv[3]

    plan_rows = parse_json_plan(plan_json)
    slot_times = parse_slot_times(slot_json)

    grouped = group_by_day(plan_rows)
    if not grouped:
        print("Keine geplanten Tage gefunden.")
        sys.exit(2)
        
    build_document(grouped, slot_times, out_docx)
    #print(f"Word-Datei erstellt: {out_docx}")

if __name__ == "__main__":
    main()
