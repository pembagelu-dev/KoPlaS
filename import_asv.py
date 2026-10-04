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
Doppelter Import S und K LF Sport behoben
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
    #- Relevante Spalten anhand Header: 'Std.', 'LK', 'S', 'K', 'Kurs' (Groß/Kleinschreibung und Punkt wie im Beispiel)
    #Es können viele irrelevante/leer Spalten dazwischen liegen; wir suchen positionsunabhängig nach den Header-Strings.
    #- Zwischenheader/Seitenköpfe werden ignoriert (z. B. Zeilen, die keine Daten tragen oder wieder Headerzeilen darstellen).
    #Rückgabe pro Kurszeile: Dict mit Keys:
    #{"Lehrkraft": <LK>, "S": <int>, "K": <int>, "WS": <int>, "school_name": <str>}
    
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
    hdr_idx = {"Std.": None, "LK": None, "S": None, "K": None, "Kurs": None}  # wir benötigen LK, Std.(->WS), S, K, Kurs

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

    for r in rows:
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

        # Ggf. trivialer Filter: ohne Kürzel keine Kurszeile
        if lk == "":
            continue

        rec = {
            "Lehrkraft": lk,
            "WS": to_int(ws_txt),  # 'Std.' -> 'WS'
            "S": to_int(s_txt),
            "K": to_int(k_txt),
            "school_name": school_name,
            "Kurs": kurs,
        }        
        results.append(rec)

    # --- Konsolidierung von SMW/smw-Kurs-Paaren pro Lehrkraft ---
    #
    # Regeln:
    # - Paare sind identisch bis auf Groß-/Kleinschreibung der Zeichenfolge "SMW"/"smw" im Kurs (z. B. "3SMW1" vs "3smw1").
    # - Pro Lehrkraft maximal ein SMW- und ein smw-Eintrag für dasselbe Paar.
    # - Konsolidierung: WS = Summe(WS beider Zeilen), S/K stammen ausschließlich aus der SMW-Zeile.
    # - Nur anwenden für echte SMW/smw-Paare; ansonsten Datensätze unverändert übernehmen.
    #
    # Vorgehen:
    # - Schlüssel je Datensatz zur Paarbildung: (Lehrkraft, normalisierte Kurskennung), wobei
    #   normalisierte Kurskennung = Kurs mit ersetztem "smw"/"SMW" zu einem einheitlichen Token, z. B. "__SMW__".
    # - Pro Schlüssel sammeln wir "upper" (enthält 'SMW' in Großbuchstaben) und "lower" (enthält 'smw' in Kleinbuchstaben).
    # - Wenn upper und lower vorhanden -> zusammenführen gemäß Regeln.
    # - Wenn nur upper oder nur lower vorhanden -> nur übernehmen, aber:
    #     - Wenn nur lower existiert, S/K aus der lower-Zeile übernehmen (da keine SMW-Zeile existiert).
    #
    from collections import defaultdict
    import re

    def _has_smw(s: str) -> bool:
        # robuste, case-insensitive Erkennung von SMW/smw
        return bool(re.search(r'smw', (s or ''), flags=re.IGNORECASE))

    def _normalize_smw_token_with_num(kurs_value: str) -> tuple[str, str]:
        """
        Liefert einen Normalisierungs-Schlüssel inkl. extrahierter Endziffer.
        key: Lehrkraft-übergreifend identisch für gleiche Kurs-Variante (SMW/smw vereinheitlicht)
        num: extrahierte Abschlussziffer (falls vorhanden), sonst ''.
        Beispiele:
          "3SMW1" -> ("3__SMW__1", "1")
          "3smw1" -> ("3__SMW__1", "1")
          "3SMW"  -> ("3__SMW__", "")
        """
        s = (kurs_value or "").strip()
        # SMW/smw vereinheitlichen
        base = re.sub(r'smw', '__SMW__', s, flags=re.IGNORECASE)
        # Endziffer extrahieren
        m = re.search(r'(\d)$', base)
        num = m.group(1) if m else ''
        return base, num

    def _ends_with_digit(s: str) -> bool:
        return bool(re.search(r'\d$', (s or '').strip()))

    def _ensure_digit_suffix(course: str, fallback_digit: str) -> str:
        
        #Stellt sicher, dass der Kursstring mit einer Ziffer endet.
        #Falls nicht und fallback_digit gesetzt ist, wird diese angehängt.
        
        c = (course or '').strip()
        if _ends_with_digit(c) or not fallback_digit:
            return c
        return f"{c}{fallback_digit}"

    def _pick_course(upper_course: str, lower_course: str, fallback_digit: str) -> str:
        # Wählt die robusteste Kursbezeichnung und stellt sicher, dass die Endziffer vorhanden ist.
        u = (upper_course or '').strip()
        l = (lower_course or '').strip()
        if not u and not l:
            return _ensure_digit_suffix('', fallback_digit)
        if not u:
            return _ensure_digit_suffix(l, fallback_digit)
        if not l:
            return _ensure_digit_suffix(u, fallback_digit)
        # identisch bis auf Case
        if u.lower() == l.lower():
            return _ensure_digit_suffix(u, fallback_digit)
        # Bevorzuge Variante, die mit Ziffer endet
        eu, el = _ends_with_digit(u), _ends_with_digit(l)
        if eu and not el:
            return u
        if el and not eu:
            return l
        # sonst längere Variante
        chosen = u if len(u) >= len(l) else l
        return _ensure_digit_suffix(chosen, fallback_digit)

    buckets: Dict[tuple, Dict[str, Optional[Dict[str, Any]]]] = defaultdict(lambda: {"upper": None, "lower": None})
    others: List[Dict[str, Any]] = []

    # Zuerst in SMW/smw-Buckets und "others" einsortieren
    for rec in results:
        # trims für Robustheit
        rec["Kurs"] = (rec.get("Kurs") or "").strip()
        kurs_val = rec["Kurs"]
        lk_val = (rec.get("Lehrkraft") or "").strip()
        if _has_smw(kurs_val):
            norm, _ = _normalize_smw_token_with_num(kurs_val)
            key = (lk_val, norm)
            # nach Groß-/Kleinschreibung vorsortieren (für S/K-Quelle bleibt 'upper' maßgeblich)
            if re.search(r'SMW', kurs_val):
                buckets[key]["upper"] = rec
            elif re.search(r'smw', kurs_val):
                buckets[key]["lower"] = rec
            else:
                # gemischte Schreibweise: als 'upper' behandeln
                buckets[key]["upper"] = rec
        else:
            # Nicht betroffen von SMW/smw-Regeln -> direkt übernehmen
            others.append(rec)

    consolidated: List[Dict[str, Any]] = []

    # Konsolidierung der SMW/smw-Paare
    for (lk_val, norm_kurs), pair in buckets.items():
        upper = pair.get("upper")
        lower = pair.get("lower")
        # Die erwartete Endziffer aus dem normalisierten Schlüssel ableiten (falls vorhanden)
        _ , digit_fallback = _normalize_smw_token_with_num(norm_kurs)
        if upper and lower:
            # Zusammenführen nach Regeln
            merged = {
                "Lehrkraft": lk_val,
                "WS": int(upper.get("WS", 0)) + int(lower.get("WS", 0)),
                "S": int(upper.get("S", 0)),  # ausschließlich aus SMW (upper)
                "K": int(upper.get("K", 0)),  # ausschließlich aus SMW (upper)
                "school_name": upper.get("school_name", "") or lower.get("school_name", ""),
                # Kurs-Bezeichnung robust wählen und Endziffer sicherstellen
                "Kurs": _pick_course(upper.get("Kurs", ""), lower.get("Kurs", ""), digit_fallback),
            }
            consolidated.append(merged)
        elif upper and not lower:
            # Nur SMW vorhanden -> unverändert übernehmen
            upper["Kurs"] = _ensure_digit_suffix((upper.get("Kurs") or '').strip(),
                                                 _normalize_smw_token_with_num(upper.get("Kurs") or '')[1])
            consolidated.append(upper)
        elif lower and not upper:
            # Nur smw vorhanden -> übernehmen, S/K aus dieser Zeile (keine SMW-Zeile vorhanden)
            lower["Kurs"] = _ensure_digit_suffix((lower.get("Kurs") or '').strip(),
                                                 _normalize_smw_token_with_num(lower.get("Kurs") or '')[1])
            consolidated.append(lower)
        # Falls weder upper noch lower (sollte nicht vorkommen), nichts tun
    # Andere Kurse anhängen
    consolidated.extend(others)

    return consolidated

if __name__ == "__main__":
    sys.exit(main(sys.argv))
