Version = "0.1 (Build 5)"

"""
Importschnittstelle Version 0.1 Build 5

----------
ChangeLog
----------
Build 5: Unbenutzte Werte entfernt, CSV-Helfer aus Zeilenschleifen gezogen und Zahlenkonvertierung gezielter abgesichert
Import der Prüfungen aus ASV
Import der Lehrkräfte der Schule (Kürzel) mit UPZ für Belastungsrechnung
Import der Oberstufenkurse mit WS, Teilnehmer in S und K sowie LF-Kürzel als Zuordnung
Fach, L-Kennzeichen und CSV-Quellzeile zur gezielten FTU-Auswahl bereitgestellt
WS bei exakt gleichen Kursbezeichnungen nur beim ersten Auftreten vergeben; Groß-/Kleinschreibung bleibt relevant
Kursnummer bei Sport (3SMW1 wurde zu 3SMW) behoben
"""

import sys
import csv
import re
from pathlib import Path
from typing import List, Dict, Optional, Any

def parse_csv(input_path: str) -> List[Dict[str, str]]:
    """
    Parse die Eingabe-CSV und gibt eine Liste von Datensätzen zurück.
    Keys je Datensatz: Schueler, Fach 1, Pruefer 1, Fach 2, Pruefer 2.

    Ignoriert nach der ersten Zeile:
      - exakte Wiederholungen der Kopfzeile: Nr.;Name, Rufname;S1;;S2;;S3;;K1;;K2;
      - Pseudo-Header-Zeilen: Name, Rufname;;--;;
    """
    results: List[Dict[str, str]] = []

    with open(input_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        rows = [[cell.strip() for cell in row] for row in reader]

    if not rows:
        return results

    header = rows[0]

    def find_index(name: str, hdr: List[str]) -> Optional[int]:
        try:
            return hdr.index(name)
        except ValueError:
            return None

    idx_name = find_index("Name, Rufname", header)
    idx_k1 = find_index("K1", header)
    idx_k2 = find_index("K2", header)

    if idx_name is None or idx_k1 is None or idx_k2 is None:
        return results
        #raise ValueError("Erforderliche Header nicht gefunden: 'Name, Rufname', 'K1', 'K2'.")

    idx_k1_next = idx_k1 + 1
    idx_k2_next = idx_k2 + 1

    max_idx = len(header) - 1
    if idx_k1_next > max_idx or idx_k2_next > max_idx:
        raise ValueError("Erwartete Spalten rechts von K1/K2 liegen außerhalb der Header-Grenzen.")

    # Normalisiere Headerzeile zur exakten Vergleichbarkeit (Trim bereits erfolgt)
    canonical_header = header[:]  # Liste der Zellen der ersten Zeile

    def is_exact_header_repeat(row: List[str]) -> bool:
        """
        Prüft, ob eine Zeile exakt die gleiche Zellenfolge wie die erste Headerzeile hat.
        Vergleicht bis zur Länge der längeren Zeile; zusätzliche leere Endzellen werden toleriert.
        """
        # Gleichheit prüfen, wobei wir trailing leere Zellen ignorieren
        def rstrip_empty(cells: List[str]) -> List[str]:
            trimmed = cells[:]
            while trimmed and trimmed[-1] == "":
                trimmed.pop()
            return trimmed

        return rstrip_empty(row) == rstrip_empty(canonical_header)

    def is_exact_pseudo_header(row: List[str]) -> bool:
        """
        Erkenne GENAU das Muster: Name, Rufname;;--;;
        Umsetzung:
          - In der Spalte 'Name, Rufname' steht 'Name, Rufname'
          - Die zwei Zellen rechts davon existieren und sind: "" und "--"
        """
        if len(row) <= idx_name:
            return False
        if row[idx_name] != "Name, Rufname":
            return False
        if len(row) <= idx_name + 2:
            return False
        return row[idx_name + 1] == "" and row[idx_name + 2] == "--"

    def safe_get(row: List[str], idx: int) -> str:
        return row[idx].strip() if idx < len(row) else ""

    def fix_smw_suffix(fach: str, pruefer: str) -> tuple[str, str]:
        fach_value = (fach or "").strip()
        pruefer_value = (pruefer or "").strip()
        # Wenn Fach wie "3SMW" (ohne Endziffer), prüfen, ob Prüfer nur aus einer einzelnen Ziffer besteht.
        if re.fullmatch(r'^[23]\s*SMW$', fach_value, flags=re.IGNORECASE) and re.fullmatch(r'^\d$', pruefer_value):
            # Ziffer an Fach anhängen und Prüfer leeren
            return f"{fach_value}{pruefer_value}", ""
        # Auch Fälle mit gemischten Spaces/Fachkern wie "3 SMW" abfangen
        if re.fullmatch(r'^[23]\s*SMW\s*$', fach_value, flags=re.IGNORECASE) and re.fullmatch(r'^\d$', pruefer_value):
            return f"{fach_value.strip()}{pruefer_value}", ""
        return fach_value, pruefer_value

    i = 1
    total_rows = len(rows)
    while i < total_rows:
        row = rows[i]

        # Leere Zeilen überspringen
        if all(c == "" for c in row):
            i += 1
            continue

        # Wiederholte Header oder Pseudo-Header ignorieren
        if is_exact_header_repeat(row) or is_exact_pseudo_header(row):
            i += 1
            continue

        # Erwartete Name-Zeile (Schueler)
        schueler = row[idx_name].strip() if idx_name < len(row) else ""
        if schueler == "":
            i += 1
            continue

        # Zwischenzeilen (leer, Header-Wiederholungen, Pseudo-Header) nach Name überspringen
        j = i + 1
        while j < total_rows:
            nxt = rows[j]
            if all(c == "" for c in nxt) or is_exact_header_repeat(nxt) or is_exact_pseudo_header(nxt):
                j += 1
                continue
            break

        if j >= total_rows:
            break

        data_row = rows[j]

        fach1 = safe_get(data_row, idx_k1)
        pruefer1 = safe_get(data_row, idx_k1_next)
        fach2 = safe_get(data_row, idx_k2)
        pruefer2 = safe_get(data_row, idx_k2_next)

        # --- Robustheitsfix für SMW/smw-Kursbezeichnungen, bei denen die Endziffer "in die nächste Spalte rutscht" ---
        # Manche ASV-Exporte haben bei Kursen wie "3SMW1" ein Spaltenversatz-Problem, sodass in K1/K2 nur "3SMW"
        # steht und die nachfolgende "1" in der Prüfer-Spalte landet. Dann hier die Ziffer zurück anfügen.
        fach1, pruefer1 = fix_smw_suffix(fach1, pruefer1)
        fach2, pruefer2 = fix_smw_suffix(fach2, pruefer2)

        results.append({
            "Schueler": schueler,
            "Fach 1": fach1,
            "Pruefer 1": pruefer1,
            "Fach 2": fach2,
            "Pruefer 2": pruefer2,
        })

        # Zum nächsten Block
        i = j + 1

    return results


def to_long_format(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Zwei Zeilen pro Schüler; Ausgabe: Schueler, Fach, Thema, Pruefer, Beisitzer.
    Thema-Vergabe:
      - Fachkern = Fach ohne führende Ziffern.
      - Pro Fachkern Nummerierung ab 1, in alphabetischer Reihenfolge der Schüler.
      - Thema = "<Fachkern>.<laufende_nummer>", wenn Fachkern nicht leer ist, sonst "--".
    """
    long_rows: List[Dict[str, str]] = []

    def fachkern(fach: str) -> str:
        fach = (fach or "").strip()
        if fach == "":
            return ""
        # führende Ziffern entfernen
        return re.sub(r'^\d+', '', fach)

    for rec in records:
        schueler = (rec.get("Schueler") or "").strip()

        # Zeile 1
        fach1 = (rec.get("Fach 1") or "").strip()
        pruefer1 = (rec.get("Pruefer 1") or "").strip()
        kern1 = fachkern(fach1)
        long_rows.append({
            "Schueler": schueler,
            "Fach": fach1,
            "Thema": kern1,   # zunächst Kern ablegen, Nummer kommt später
            "Pruefer": pruefer1,
            "Beisitzer": "",
        })

        # Zeile 2
        fach2 = (rec.get("Fach 2") or "").strip()
        pruefer2 = (rec.get("Pruefer 2") or "").strip()
        kern2 = fachkern(fach2)
        long_rows.append({
            "Schueler": schueler,
            "Fach": fach2,
            "Thema": kern2,   # zunächst Kern ablegen, Nummer kommt später
            "Pruefer": pruefer2,
            "Beisitzer": "",
        })

    # Alphabetisch nach Schüler sortieren (Nummerierungsreihenfolge)
    long_rows.sort(key=lambda r: r.get("Schueler", ""))

    # Pro Fachkern durchnummerieren und Thema final setzen
    counters: Dict[str, int] = {}
    for row in long_rows:
        kern = (row.get("Thema") or "").strip()
        if kern == "":
            # leerer Kern -> Thema "--"
            row["Thema"] = "--"
            continue
        n = counters.get(kern, 0) + 1
        counters[kern] = n
        row["Thema"] = f"{kern}.{n}"

    return long_rows

def write_output_long(long_rows: List[Dict[str, str]], output_path: str) -> None:
    """
    Schreibt Semikolon-CSV: Schueler;Fach;Thema;Pruefer;Beisitzer
    """
    fieldnames = ["Schueler", "Fach", "Thema", "Pruefer", "Beisitzer"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in long_rows:
            clean = {k: (v.strip() if isinstance(v, str) else "") for k, v in row.items()}
            if "Beisitzer" not in clean:
                clean["Beisitzer"] = ""
            writer.writerow(clean)


def main(argv: List[str]) -> int:
    """
    Aufruf: python import_asv.py <Abiturfächer Kurse.csv>
    Ausgabe: pruefungen.csv
    """
    if len(argv) < 2:
        print("Verwendung: python import_asv.py <Abiturfächer Kurse.csv>")
        return 1

    input_path = argv[1]
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Datei nicht gefunden: {input_file}")
        return 1

    try:
        records = parse_csv(str(input_file))
        long_rows = to_long_format(records)
    except Exception as e:
        print(f"Fehler: {e}")
        return 1

    output_path = "pruefungen.csv"
    try:
        write_output_long(long_rows, output_path)
    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabe: {e}")
        return 1

    print(f"Erfolgreich {len(long_rows)} Zeilen nach '{output_path}' geschrieben.")
    return 0


# --- Import: Lehrkräfte ---
def read_teachers_asv(input_path: str) -> List[Dict[str, str]]:
    """
    Liest Lehrkräfte aus einer CSV mit den Spalten:
      - Familienname
      - Kürzel
      - UPZ
    Mapping:
      Kürzel -> Lehrkraft
      UPZ -> UPZ
    'Familienname' wird ignoriert.
    Rückgabe: Liste von Dicts: {"Lehrkraft": <Kürzel>, "UPZ": <UPZ>}
    """
    rows: List[Dict[str, str]] = []
    with open(input_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader, None)
        if header is None:
            return rows

        def idx(name: str) -> Optional[int]:
            try:
                return header.index(name)
            except ValueError:
                return None

        i_kurz = idx("Kürzel")
        i_upz = idx("UPZ")
        if i_kurz is None or i_upz is None:
            return rows
            #raise ValueError("Erforderliche Header nicht gefunden: 'Name', 'UPZ', 'Kürzel'.")

        for rec in reader:
            # Leere oder zu kurze Zeilen überspringen
            if not rec or all((c or "").strip() == "" for c in rec):
                continue
            kuerzel = rec[i_kurz].strip() if i_kurz < len(rec) else ""
            upz = rec[i_upz].strip() if i_upz < len(rec) else ""
            if kuerzel == "" and upz == "":
                continue
            rows.append({"Lehrkraft": kuerzel, "UPZ": upz})
    return rows

def read_courses(input_path: str) -> List[Dict[str, Any]]:
    #Liest Oberstufenkurse aus einer CSV mit Metadaten-Headern (wiederkehrend).
    #- school_name: aus der ALLERERSTEN Zeile, direkt der Text hinter 'NNNN - ' (z. B. '0306 - Meine Schule' -> 'Meine Schule')
    #- Relevante Spalten anhand Header: 'Kurs', 'Fach', 'Std.', 'LK', 'S', 'K'; das Kennzeichen steht vor 'Std.'
    #Es können viele irrelevante/leer Spalten dazwischen liegen; wir suchen positionsunabhängig nach den Header-Strings.
    #- Zwischenheader/Seitenköpfe werden ignoriert (z. B. Zeilen, die keine Daten tragen oder wieder Headerzeilen darstellen).
    #Rückgabe pro Kurszeile inklusive Kurs/Fach/Kennzeichen und Quellzeile.
    
    results: List[Dict[str, Any]] = []
    def parse_school_name(s: str) -> str:
        # erwartet z. B. "0306 - Chiemgau-Gymnasium Traunstein;..."
        # Wir nehmen den Inhalt NACH ' - ' in der ersten Zelle
        cell0 = (s or "").split(";")[0].strip()
        # Finde ' - ' und schneide rechts davon
        if " - " in cell0:
            return cell0.split(" - ", 1)[1].strip()
        return ""

    with open(input_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        rows = [row for row in reader]

    if not rows:
        return results

    # school_name aus erster Zeile
    school_name = parse_school_name(";".join(rows[0] if rows[0] else []))

    # Wir müssen dynamisch die Datentabellen-Blöcke identifizieren.
    # Strategie:
    # - Iteriere über alle Zeilen.
    # - Wenn eine Zeile Header enthält, in der die Labels 'Std.', 'LK', 'TN', 'S', 'K' vorkommen,
    #   merken wir uns deren Spaltenindizes (positionsunabhängig).
    # - Danach folgende Zeilen bis zum nächsten Leer-/Zwischenheader als Datenzeilen lesen,
    #   solange an den relevanten Indizes plausible Werte stehen.
    hdr_idx = {
        "Std.": None, "LK": None, "S": None, "K": None, "Kurs": None,
        "Fach": None, "Kennzeichen": None,
    }

    def find_indices(header_row: List[str]) -> Dict[str, Optional[int]]:
        # Suche nach den gesuchten Überschriften (exakt oder getrimmt)
        idx_map: Dict[str, Optional[int]] = {k: None for k in hdr_idx}
        for i, cell in enumerate(header_row or []):
            name = (cell or "").strip()
            if name in idx_map:
                idx_map[name] = i
        return idx_map

    def is_header_row(row: List[str]) -> bool:
        # Ein Header ist gegeben, wenn mindestens zwei der gesuchten Labels in der Zeile vorkommen
        labels = set(k for k, v in find_indices(row).items() if v is not None)
        return len(labels.intersection({"LK", "Std.", "S", "K", "Kurs"})) >= 2

    def row_is_empty(row: List[str]) -> bool:
        return all((c or "").strip() == "" for c in (row or []))

    def safe_get(row: List[str], idx: Optional[int]) -> str:
        if idx is None:
            return ""
        return (row[idx] if idx < len(row) else "") or ""

    def to_int(value: str) -> int:
        try:
            return int(value.strip()) if value.strip() != "" else 0
        except ValueError:
            return 0

    parsing = False
    current_idx = hdr_idx.copy()
    seen_course_names = set()

    for source_row, r in enumerate(rows, start=1):
        # Zwischenheader/Seitenköpfe ignorieren:
        # - komplett leere Zeilen
        # - offensichtliche Seitenangaben wie "Seite", "Kursübersicht" als erste sinnvolle Tokens
        if row_is_empty(r):
            continue
        first_nonempty = next((c.strip() for c in r if (c or "").strip() != ""), "")
        if first_nonempty.lower().startswith("seite") or "Kursbersicht" in first_nonempty or "Kursübersicht" in first_nonempty:
            parsing = False
            current_idx = hdr_idx.copy()
            continue

        # Header-Zeile erkennen
        if is_header_row(r):
            current_idx = find_indices(r)
            std_idx = current_idx.get("Std.")
            current_idx["Kennzeichen"] = std_idx - 1 if std_idx is not None and std_idx > 0 else None
            parsing = True
            continue

        if not parsing:
            # Kein aktiver Datenblock
            continue

        # Datenzeile: robust auslesen
        lk = safe_get(r, current_idx.get("LK")).strip()
        ws_txt = safe_get(r, current_idx.get("Std.")).strip()
        s_txt = safe_get(r, current_idx.get("S")).strip()
        k_txt = safe_get(r, current_idx.get("K")).strip()
        kurs = safe_get(r, current_idx.get("Kurs")).strip()
        fach = safe_get(r, current_idx.get("Fach")).strip()
        kennzeichen = safe_get(r, current_idx.get("Kennzeichen")).strip()

        # Ggf. trivialer Filter: ohne Kürzel keine Kurszeile
        if lk == "":
            continue

        # Kursbezeichnungen gelten exakt und mit Beachtung der Groß-/Kleinschreibung.
        # Wiederholte Kennungen (auch mit abweichendem Kennzeichen) erhalten WS nur beim ersten Auftreten.
        ws = to_int(ws_txt)
        if kurs:
            if kurs in seen_course_names:
                ws = 0
            else:
                seen_course_names.add(kurs)

        rec = {
            "Lehrkraft": lk,
            "WS": ws,  # 'Std.' -> 'WS'
            "S": to_int(s_txt),
            "K": to_int(k_txt),
            "school_name": school_name,
            "Kurs": kurs,
            "Fach": fach,
            "Kennzeichen": kennzeichen,
            "source_row": source_row,
        }        
        results.append(rec)

    return results

if __name__ == "__main__":
    sys.exit(main(sys.argv))
