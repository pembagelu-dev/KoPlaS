Version = "0.2 (Build 17)"

import sys
import pandas as pd
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, replace
import time
from ortools.sat.python import cp_model

from import_asv import parse_csv, to_long_format

DAYS = ["Mo", "Di", "Mi", "Do", "Fr"]
WEEKS = [1, 2]
MIP_ROOM_SOLVER_LIMIT = 1200.0
MIP_ROOM_SOLVER_WORKER = 0
MIP_ROOM_GAP_WEIGHT = 2000
MIP_ROOM_SOFTENING = 10000

CP_WORKERS = 0

GAP_WEIGHT_INNER = 4000
GAP_WEIGHT_OUTER = 2000
SPAN_WEIGHT = 200

SECOND_SLOT_WEIGHT = 1000

DAY_WEIGHT_BALANCE = 50

# NEU: Limit weicher Permutationspaar-Terme (pro (P,B)-Gruppe nur die k nächsten Paare)
LIMIT_PERM_PAIRS = 5

@dataclass(frozen=True)
class Exam:
    idx: int
    schueler: str
    fach: str
    thema: str
    pruefer: str
    beisitzer: str

@dataclass
class ScheduleParams:
    rooms: List[str]
    slots_per_day: Dict[Tuple[int, int], int]
    timing_per_day: Dict[Tuple[int, int], Tuple[str, int, int]]

@dataclass
class ConstraintsConfig:
    hard_student_one_per_week: bool
    hard_grouping_enabled: bool
    grouping_block_size: Optional[int]
    hard_unavailability: bool
    hard_min_gap_days_same_student: Optional[int]
    hard_no_exam_days_enabled: bool
    hard_max_days_per_teacher_enabled: bool
    hard_max_days_per_teacher_K: Optional[int]

    soft_desired_gap_days_same_student: Optional[int]
    soft_minimize_rooms_used: bool

    teachers_allow_5_per_day: Set[str]
    default_max_per_day: int

    soft_prefer_second_slot_start: bool
    weight_prefer_second_slot: int
    ignore_empty_beisitzer: bool

# --- Verbose / Diagnose ---
VERBOSE = True
LOG_CALLBACK = None

def vprint(*args, **kwargs):
    if VERBOSE:
        msg = " ".join(str(a) for a in args)
        if LOG_CALLBACK:
            try:
                LOG_CALLBACK(msg)
            except Exception:
                print(msg, **kwargs)
        else:
            print(msg, **kwargs)

def status_to_str(status):
    from ortools.sat.python import cp_model
    return {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "ZULÄSSIG",
        cp_model.INFEASIBLE: "UNZULÄSSIG",
        cp_model.MODEL_INVALID: "MODELL UNGÜLTIG",
        cp_model.UNKNOWN: "UNBEKANNT",
    }.get(status, str(status))

def format_feedback(report):
    """Ein Bericht für CLI und kopierbare GUI-Dialogdetails."""
    lines = [report.get("summary", ""), f"Status: {report.get('status', 'unbekannt')}"]
    for key, title in (("findings", "Konkrete Befunde / Modellgrenzen"),
                       ("suggestions", "Nächste Schritte / geprüfte Änderungen"),
                       ("wishes", "Wünsche und Abweichungen"),
                       ("room_notes", "Raumvergabe")):
        values = report.get(key, [])
        if values:
            lines.append(title + ":")
            lines.extend("• " + value for value in values)
    if report.get("status") in ("ZULÄSSIG", "OPTIMAL") and not report.get("wishes"):
        lines.append("Keine Abweichungen bei den ausgewerteten Schülerabständen, Startwünschen und Tageszielwerten. "
                     "Dies ist keine Aussage, dass alle Raum- und Kompaktheitsziele ihr Minimum erreichen.")
    return "\n".join(lines)

def parse_day_token(token: str) -> Tuple[int, int]:
    token = token.strip()
    if len(token) < 3:
        raise ValueError(f"Ungueltiger Tag-Token: {token}")
    day = token[:2]
    week_str = token[2:]
    if day not in DAYS:
        raise ValueError(f"Ungueltiger Wochentag: {day}")
    week = int(week_str)
    if week not in WEEKS:
        raise ValueError(f"Woche muss 1 oder 2 sein: {token}")
    day_index = DAYS.index(day)
    return week, day_index

def enumerate_all_day_slots(params: ScheduleParams,
                            no_exam_days: Optional[Set[Tuple[int, int]]] = None) -> List[Tuple[int, int, int]]:
    no_exam_days = no_exam_days or set()
    res = []
    for w in WEEKS:
        for d in range(5):
            if (w, d) in no_exam_days:
                continue
            n = params.slots_per_day.get((w, d), 0)
            for s in range(n):
                res.append((w, d, s))
    return res

def pretty_time_for_slot(params: ScheduleParams, w: int, d: int, s: int) -> str:
    start_str, slot_min, break_min = params.timing_per_day[(w, d)]
    h, m = [int(x) for x in start_str.strip().split(":")]
    total_min = h * 60 + m + s * (slot_min + break_min)
    H = total_min // 60
    M = total_min % 60
    return f"{H:02d}:{M:02d}"

def read_exams_from_csv(path: str) -> List['Exam']:
    records = parse_csv(path)
    long_rows = to_long_format(records)

    exams: List[Exam] = []
    for i, row in enumerate(long_rows):
        idx = i + 1

        schueler = (row.get("Schueler") or "").strip()
        fach = (row.get("Fach") or "").strip()
        thema = (row.get("Thema") or "").strip()
        pruefer = (row.get("Pruefer") or "").strip()
        beisitzer = (row.get("Beisitzer") or "").strip()

        if pruefer and beisitzer and pruefer == beisitzer:
            raise ValueError(
                f"Pruefer und Beisitzer identisch in Zeile {idx}: {pruefer}. Dies ist nicht erlaubt."
            )

        exams.append(Exam(
            idx=idx,
            schueler=schueler,
            fach=fach,
            thema=thema,
            pruefer=pruefer,
            beisitzer=beisitzer,
        ))

    return exams

def group_exams_for_blocking(exams: List[Exam]) -> Dict[Tuple[str, str, str], List[Exam]]:
    groups = defaultdict(list)
    for e in exams:
        key = (e.thema, e.fach, e.pruefer)
        groups[key].append(e)
    return {k: v for k, v in groups.items() if len(v) >= 2}

class ColloquiumScheduler:
    def __init__(self,
                 exams: List[Exam],
                 params: ScheduleParams,
                 config: ConstraintsConfig,
                 unavailability: Dict[str, Set[Tuple[int, int]]],
                 no_exam_days: Set[Tuple[int, int]]):
        self.exams = exams
        self.params = params
        self.config = config
        # Separater Bericht; solve() und extract_schedule() behalten ihre API.
        self.feedback = {"status": None, "summary": "", "findings": [],
                         "suggestions": [], "wishes": [], "room_notes": []}
        # Die GUI zeigt den vollständigen Bericht im Ergebnisdialog.
        self.log_detailed_feedback = True
        self._diagnostic_allow_gaps = False
        self.unavailability = unavailability
        self.no_exam_days = no_exam_days

        self.all_slots = enumerate_all_day_slots(params, no_exam_days=self.no_exam_days)

        self.day_to_gslots: Dict[Tuple[int, int], List[int]] = defaultdict(list)
        for gslot, (w, d, s) in enumerate(self.all_slots):
            self.day_to_gslots[(w, d)].append(gslot)

        self.model = cp_model.CpModel()
        self.x = {}
        for e in self.exams:
            for gslot in range(len(self.all_slots)):
                self.x[(e.idx, gslot)] = self.model.NewBoolVar(f"x_e{e.idx}_g{gslot}")

        self.soft_terms = []
        self.teacher_day_used: Dict[Tuple[str, int, int], cp_model.IntVar] = {}

        # NEU: Caches für (Prüfer->Exams) und slotweise Summen/Bools je Tag, Wiederverwendung hart/weich
        self._exams_by_teacher: Dict[str, List[Exam]] = defaultdict(list)
        for e in self.exams:
            # Ursprünglich nur Prüfer:
            self._exams_by_teacher[e.pruefer].append(e)
            # ERWEITERUNG: rollenübergreifend auch Beisitzer zuordnen (sofern nicht ignoriert/leer)
            try:
                if (not getattr(self.config, "ignore_empty_beisitzer", False)) or (e.beisitzer and e.beisitzer.strip() != ""):
                    # Prüfe, dass Prüfer und Beisitzer nicht identisch sind (wird bereits beim Einlesen validiert)
                    # und füge Beisitzer zur Aggregation hinzu, damit Tageslimits (Regel 7) rollenübergreifend greifen.
                    self._exams_by_teacher[e.beisitzer].append(e)
            except Exception:
                # Fallback: falls config nicht gesetzt ist, verhalte dich konservativ und füge Beisitzer hinzu, wenn nicht leer
                if e.beisitzer and e.beisitzer.strip() != "":
                    self._exams_by_teacher[e.beisitzer].append(e)

        # pro (Lehrer, (w,d)) -> Dict mit:
        #   "b": List[BoolVar] belegter Slots (lokale Slot-Indexierung innerhalb Tages)
        #   "sum_slot": List[LinExpr] Summe x[(e, gslot)] über Exams des Lehrers im globalen Slot
        self._teacher_day_struct: Dict[Tuple[str, int, int], Dict[str, List]] = {}

        vprint("[Init] Prüfungen:", len(self.exams),
               "| Slots gesamt:", len(self.all_slots),
               "| Erlaubte Tage:", len({(w, d) for (w, d, _) in self.all_slots}))
        if self.no_exam_days:
            vprint("[Init] Tage ohne Prüfung:", ", ".join(f"{DAYS[d]}{w}" for (w, d) in sorted(self.no_exam_days)))
        try:
            if getattr(self.config, "ignore_empty_beisitzer", False):
                vprint("[Init] Hinweis: Leere Beisitzer werden ignoriert")
        except Exception:
            pass

    def _build_teacher_day_struct(self):
        # Einmalige Konstruktion b- und Summen-Vektoren pro (Prüfer, Tag) für Wiederverwendung
        for teacher, exs in self._exams_by_teacher.items():
            for (w, d), day_slots in self.day_to_gslots.items():
                nslots = len(day_slots)
                if nslots == 0:
                    continue
                b = [self.model.NewBoolVar(f"b_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                sum_slot = []
                for s_local, gslot in enumerate(day_slots):
                    slot_sum = sum(self.x[(e.idx, gslot)] for e in exs)
                    # Kopplung b[s] == (slot_sum >= 1)
                    # Da slot_sum Bool-Summe ist, können wir b == slot_sum setzen, wenn max 1.
                    # Hier erlauben wir ">=1" via <=/>=:
                    self.model.Add(b[s_local] >= slot_sum)
                    self.model.Add(b[s_local] <= slot_sum)
                    sum_slot.append(slot_sum)
                self._teacher_day_struct[(teacher, w, d)] = {"b": b, "sum_slot": sum_slot}

    def add_basic_constraints(self):
        vprint("[Constraints] Grundregeln werden vorbereitet ")
        num_slots = len(self.all_slots)
        # Jede Prüfung genau einmal
        for e in self.exams:
            self.model.Add(sum(self.x[(e.idx, g)] for g in range(num_slots)) == 1)

        # Ressourcen-Konflikte
        students = defaultdict(list)
        pruefer = defaultdict(list)
        beisitzer = defaultdict(list)
        for e in self.exams:
            students[e.schueler].append(e)
            pruefer[e.pruefer].append(e)
            if not self.config.ignore_empty_beisitzer or (e.beisitzer and e.beisitzer.strip() != ""):
                beisitzer[e.beisitzer].append(e)

        vprint("[Constraints] Erkannte Konfliktgruppen:",
               f"Schüler: {sum(1 for v in students.values() if len(v) > 1)},",
               f"Prüfer: {sum(1 for v in pruefer.values() if len(v) > 1)},",
               f"Beisitzer: {sum(1 for v in beisitzer.values() if len(v) > 1)}")

        for group in [students, pruefer, beisitzer]:
            for _, exs in group.items():
                if len(exs) <= 1:
                    continue
                for g in range(num_slots):
                    self.model.Add(sum(self.x[(e.idx, g)] for e in exs) <= 1)

        # Rollenübergreifender Konflikt
        role_union = defaultdict(list)
        for e in self.exams:
            role_union[e.pruefer].append(e)
            if not self.config.ignore_empty_beisitzer or (e.beisitzer and e.beisitzer.strip() != ""):
                role_union[e.beisitzer].append(e)

        vprint("[Constraints] Personen mit mehreren Rollen am selben Tag (potenziell kritisch):",
               sum(1 for v in role_union.values() if len(v) > 1))
        for _, exs in role_union.items():
            if len(exs) <= 1:
                continue
            for g in range(num_slots):
                self.model.Add(sum(self.x[(e.idx, g)] for e in exs) <= 1)

        # Permutationsschutz (P,B) vs. (B,P) (nur bei realen Beisitzern)
        pair_map: Dict[Tuple[str, str], List[Exam]] = defaultdict(list)
        for e in self.exams:
            if not self.config.ignore_empty_beisitzer or (e.beisitzer and e.beisitzer.strip() != ""):
                pair_map[(e.pruefer, e.beisitzer)].append(e)

        seen = set()
        perm_pairs = 0
        perm_pairs_list: List[Tuple[str, str]] = []  # NEU: konkrete (P,B)-Paare für Ausgabe
        for (P, B), exs_pb in pair_map.items():
            if (B, P) in pair_map:
                key = tuple(sorted([P, B]))
                if key in seen:
                    continue
                seen.add(key)
                perm_pairs += 1
                # NEU: konkretes Paar hinzufügen (kanonische Reihenfolge P<B für stabile Ausgabe)
                p1, p2 = sorted([P, B])
                perm_pairs_list.append((p1, p2))
                exs_bp = pair_map[(B, P)]
                for g in range(num_slots):
                    self.model.Add(
                        sum(self.x[(e.idx, g)] for e in exs_pb) +
                        sum(self.x[(e.idx, g)] for e in exs_bp)
                        <= 1
                    )
        # NEU: detaillierte Ausgabe der erkannten Paare (sofern vorhanden)
        if perm_pairs > 0:
            try:
                # Duplikate entfernen und sortieren
                uniq = sorted(set(perm_pairs_list))
                formatted = ", ".join([f"({p},{b})" for (p, b) in uniq])
                vprint(f"[Constraints] Paare mit wechselseitigen Rollen (besonders zu beachten): {perm_pairs} -> {formatted}")
            except Exception:
                vprint(f"[Constraints] Paare mit wechselseitigen Rollen (besonders zu beachten): {perm_pairs}")
        
        #Kapazitätsgrenze je globalem Slot: nicht mehr Prüfungen parallel als Räume vorhanden
        R = len(self.params.rooms) if getattr(self.params, "rooms", None) else 0
        if R > 0:
            for gslot in range(len(self.all_slots)):
                self.model.Add(sum(self.x[(e.idx, gslot)] for e in self.exams) <= R)
        else:
            vprint("Nicht genügend Räume definiert. Kapazitätsgrenze pro Slot kann nicht gesetzt werden.")
        
        vprint("[Constraints] Grundregeln sind gesetzt.")

    def add_hard_constraints(self):
        vprint("[Constraints] Harte Regeln werden angewendet ")
        vprint("[Constraints] Einstellungen:",
               f"pro Schüler/Woche genau 1: {self.config.hard_student_one_per_week},",
               f"Kopplung: {self.config.hard_grouping_enabled} (Größe={self.config.grouping_block_size}),",
               f"Abwesenheiten: {self.config.hard_unavailability},",
               f"Abstand Schüler (Tage): {self.config.hard_min_gap_days_same_student},",
               f"Tage ohne Prüfungen: {self.config.hard_no_exam_days_enabled},",
               f"Max. Tage/Lehrer: {self.config.hard_max_days_per_teacher_enabled} (K={self.config.hard_max_days_per_teacher_K}),",
               f"Max/Tag je Prüfer: {self.config.default_max_per_day} (5er-Ausnahmen: {len(self.config.teachers_allow_5_per_day)})")

        # 1) Schüler pro Woche genau eine Prüfung (hart & exakt, unverändert)
        if self.config.hard_student_one_per_week:
            by_student = defaultdict(list)
            for e in self.exams:
                by_student[e.schueler].append(e)
            for _, exs in by_student.items():
                for w in WEEKS:
                    vars_week = []
                    for e in exs:
                        for gslot, (ww, _, _) in enumerate(self.all_slots):
                            if ww == w:
                                vars_week.append(self.x[(e.idx, gslot)])
                    if vars_week:
                        self.model.Add(sum(vars_week) == 1)

        # 2) Kopplung (2/3) aufeinanderfolgend im selben Tag (unverändert)
        if self.config.hard_grouping_enabled and self.config.grouping_block_size in (2, 3, 4, 5):
            block_size = self.config.grouping_block_size
            groups = group_exams_for_blocking(self.exams)
            for _, exs in groups.items():
                exs_sorted = sorted(exs, key=lambda e: e.schueler)
                for i in range(0, len(exs_sorted), block_size):
                    chunk = exs_sorted[i:i+block_size]
                    if len(chunk) <= 1:
                        continue
                    zvars = []
                    zinfo = []
                    for (w, d), day_slots in self.day_to_gslots.items():
                        nslots = len(day_slots)
                        if nslots >= len(chunk):
                            for s0 in range(nslots - len(chunk) + 1):
                                z = self.model.NewBoolVar(f"z_grp_w{w}d{d}_s{s0}_i{i}")
                                zvars.append(z)
                                zinfo.append((z, (w, d), s0, day_slots))
                    if not zvars:
                        continue
                    else:
                        self.model.Add(sum(zvars) == 1)
                        for z, (w, d), s0, day_slots in zinfo:
                            for j, e in enumerate(chunk):
                                gslot = day_slots[s0 + j]
                                self.model.Add(self.x[(e.idx, gslot)] == 1).OnlyEnforceIf(z)
                                for g2 in range(len(self.all_slots)):
                                    if g2 != gslot:
                                        self.model.Add(self.x[(e.idx, g2)] == 0).OnlyEnforceIf(z)

        # 3) Abwesenheiten Prüfer/Beisitzer (hart)
        if self.config.hard_unavailability:
            for e in self.exams:
                unavailable_days = set()
                if e.pruefer in self.unavailability:
                    unavailable_days |= self.unavailability[e.pruefer]
                if e.beisitzer in self.unavailability:
                    unavailable_days |= self.unavailability[e.beisitzer]
                if unavailable_days:
                    for gslot, (w, d, _) in enumerate(self.all_slots):
                        if (w, d) in unavailable_days:
                            self.model.Add(self.x[(e.idx, gslot)] == 0)

        # 4) Minimaler Abstand a Tage für gleichen Schüler (hart)
        if self.config.hard_min_gap_days_same_student is not None:
            a = self.config.hard_min_gap_days_same_student
            by_student = defaultdict(list)
            for e in self.exams:
                by_student[e.schueler].append(e)

            day_ordinal = {}
            ordinal = 0
            for w in WEEKS:
                for d in range(7):
                    day_ordinal[(w, d)] = ordinal
                    ordinal += 1
            slot_day_ord = [day_ordinal[(w, d)] for (w, d, _) in self.all_slots]
            max_day_ord = ordinal - 1

            for _, exs in by_student.items():
                if len(exs) <= 1:
                    continue
                for i in range(len(exs)):
                    for j in range(i + 1, len(exs)):
                        e1, e2 = exs[i], exs[j]
                        d1 = self.model.NewIntVar(0, max_day_ord, f"d1_e{e1.idx}_{e2.idx}")
                        d2 = self.model.NewIntVar(0, max_day_ord, f"d2_e{e1.idx}_{e2.idx}")
                        self.model.Add(d1 == sum(slot_day_ord[g] * self.x[(e1.idx, g)] for g in range(len(self.all_slots))))
                        self.model.Add(d2 == sum(slot_day_ord[g] * self.x[(e2.idx, g)] for g in range(len(self.all_slots))))
                        diff_lower = -max_day_ord
                        diff_upper =  max_day_ord
                        diff = self.model.NewIntVar(diff_lower, diff_upper, f"df_e{e1.idx}_{e2.idx}")
                        self.model.Add(diff == d1 - d2)
                        absdiff = self.model.NewIntVar(0, max_day_ord, f"ad_e{e1.idx}_{e2.idx}")
                        self.model.AddAbsEquality(absdiff, diff)
                        self.model.Add(absdiff >= a)

        # 5) Tage ohne Prüfungen (hart)
        if self.config.hard_no_exam_days_enabled and self.no_exam_days:
            forbidden_pairs = set(self.no_exam_days)
            if forbidden_pairs:
                for gslot, (ww, dd, _) in enumerate(self.all_slots):
                    if (ww, dd) in forbidden_pairs:
                        for e in self.exams:
                            self.model.Add(self.x[(e.idx, gslot)] == 0)

        # 6) Maximal K Tage pro Person (rollenübergreifend)
        if self.config.hard_max_days_per_teacher_enabled and self.config.hard_max_days_per_teacher_K is not None:
            Kmax = self.config.hard_max_days_per_teacher_K
            exams_by_person = defaultdict(list)
            for e in self.exams:
                # Wie in KoPlaS.evaluate_conflicts: Personen werden rollenübergreifend
                # gezählt, leere Beisitzer sind aber keine eigene Person.
                if e.pruefer:
                    exams_by_person[e.pruefer].append(e)
                beisitzer = (e.beisitzer or "").strip()
                if beisitzer:
                    exams_by_person[beisitzer].append(e)

            for person, exs in exams_by_person.items():
                day_used_vars = []
                for (w, d), day_slots in self.day_to_gslots.items():
                    used = self.model.NewBoolVar(f"tday_{person}_w{w}d{d}")
                    occupied = []
                    for e in exs:
                        for gslot in day_slots:
                            occupied.append(self.x[(e.idx, gslot)])
                    # Exakte Äquivalenz: used ist 1 genau dann, wenn mindestens
                    # eine Prüfung dieser Person an diesem Tag liegt. Nur die
                    # Richtung x <= used ließ den Solver used immer auf 0 setzen.
                    self.model.AddMaxEquality(used, occupied)
                    day_used_vars.append(used)
                self.model.Add(sum(day_used_vars) <= Kmax)

        # 7) Max. Prüfungen pro Prüfer/Tag (hart)
        exams_by_teacher = self._exams_by_teacher  # bereits vorbereitet
        # HINWEIS: self._exams_by_teacher wurde in __init__ rollenübergreifend befüllt
        # (Prüfer + Beisitzer, sofern Beisitzer nicht ignoriert/leer). Dadurch zählt diese Regel
        # Einsätze in beiden Rollen in die Tagesobergrenze mit ein.
        for teacher, exs in exams_by_teacher.items():
            max_per_day = 5 if teacher in self.config.teachers_allow_5_per_day else self.config.default_max_per_day
            for (w, d), day_slots in self.day_to_gslots.items():
                self.model.Add(sum(self.x[(e.idx, g)] for e in exs for g in day_slots) <= max_per_day)

        # NEU: Einmal b/sum_slot vorbereiten (für harte Lücken & weiche Kompaktheit)
        self._build_teacher_day_struct()

        # 8) Keine Lücken pro Prüfer/Tag (hart) – effizient via gemeinsamen b-Vektoren
        for teacher, _ in exams_by_teacher.items():
            if self._diagnostic_allow_gaps:
                continue
            for (w, d), day_slots in self.day_to_gslots.items():
                key = (teacher, w, d)
                if key not in self._teacher_day_struct:
                    continue
                b = self._teacher_day_struct[key]["b"]
                nslots = len(b)
                if nslots == 0:
                    continue

                # Prefix/Suffix nur einmal bilden (hart)
                prefix = [self.model.NewIntVar(0, nslots, f"pref_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                suffix = [self.model.NewIntVar(0, nslots, f"suff_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                self.model.Add(prefix[0] == b[0])
                for s in range(1, nslots):
                    self.model.Add(prefix[s] == prefix[s-1] + b[s])
                self.model.Add(suffix[nslots-1] == b[nslots-1])
                for s in range(nslots-2, -1, -1):
                    self.model.Add(suffix[s] == suffix[s+1] + b[s])
                for s in range(nslots):
                    left_pos = self.model.NewBoolVar(f"leftpos_{teacher}_w{w}d{d}_s{s}")
                    right_pos = self.model.NewBoolVar(f"rightpos_{teacher}_w{w}d{d}_s{s}")
                    self.model.Add(prefix[s] >= 1).OnlyEnforceIf(left_pos)
                    self.model.Add(prefix[s] <= 0).OnlyEnforceIf(left_pos.Not())
                    self.model.Add(suffix[s] >= 1).OnlyEnforceIf(right_pos)
                    self.model.Add(suffix[s] <= 0).OnlyEnforceIf(right_pos.Not())
                    both = self.model.NewBoolVar(f"both_{teacher}_w{w}d{d}_s{s}")
                    self.model.AddBoolAnd([left_pos, right_pos]).OnlyEnforceIf(both)
                    self.model.AddBoolOr([left_pos.Not(), right_pos.Not()]).OnlyEnforceIf(both.Not())
                    # Harte Lückenvermeidung
                    self.model.Add(b[s] == 1).OnlyEnforceIf(both)

        vprint("[Constraints] Harte Regeln sind gesetzt.")

    def add_soft_constraints(self):
        vprint("[Constraints] Weiche Ziele werden berücksichtigt ")
        before_terms = len(self.soft_terms)

        # 1) Gewünschter Abstand d Tage (weich)
        if self.config.soft_desired_gap_days_same_student is not None:
            d_desired = self.config.soft_desired_gap_days_same_student
            day_ordinal = {}
            ordinal = 0
            for w in WEEKS:
                for d in range(7):
                    day_ordinal[(w, d)] = ordinal
                    ordinal += 1
            slot_day_ord = [day_ordinal[(w, d)] for (w, d, _) in self.all_slots]
            max_day_ord = ordinal - 1

            by_student = defaultdict(list)
            for e in self.exams:
                by_student[e.schueler].append(e)

            for _, exs in by_student.items():
                if len(exs) <= 1:
                    continue
                # Optional: Paare begrenzen ist hier nicht sinnvoll – belassen alle Paare
                for i in range(len(exs)):
                    for j in range(i + 1, len(exs)):
                        e1, e2 = exs[i], exs[j]
                        d1 = self.model.NewIntVar(0, max_day_ord, f"sd1_e{e1.idx}_{e2.idx}")
                        d2 = self.model.NewIntVar(0, max_day_ord, f"sd2_e{e1.idx}_{e2.idx}")
                        self.model.Add(d1 == sum(slot_day_ord[g] * self.x[(e1.idx, g)] for g in range(len(self.all_slots))))
                        self.model.Add(d2 == sum(slot_day_ord[g] * self.x[(e2.idx, g)] for g in range(len(self.all_slots))))
                        diff = self.model.NewIntVar(-max_day_ord, max_day_ord, f"sdiff_e{e1.idx}_{e2.idx}")
                        self.model.Add(diff == d1 - d2)
                        absdiff = self.model.NewIntVar(0, max_day_ord, f"sabs_e{e1.idx}_{e2.idx}")
                        self.model.AddAbsEquality(absdiff, diff)
                        under = self.model.NewIntVar(0, max(0, d_desired), f"sunder_e{e1.idx}_{e2.idx}")
                        over = self.model.NewIntVar(0, max_day_ord, f"sover_e{e1.idx}_{e2.idx}")
                        self.model.Add(absdiff - d_desired == over - under)
                        self.soft_terms.append(under)

        # 2) Startpräferenz Tagesblöcke (weich) – reuse b-Vektoren
        if self.config.soft_prefer_second_slot_start:
            base_weight = max(1, int(self.config.weight_prefer_second_slot))
            late_bias_weight = max(0, base_weight // 4)

            for teacher, _ in self._exams_by_teacher.items():
                for (w, d), _day_slots in self.day_to_gslots.items():
                    key = (teacher, w, d)
                    if key not in self._teacher_day_struct:
                        continue
                    b = self._teacher_day_struct[key]["b"]
                    nslots = len(b)
                    if nslots == 0:
                        continue

                    start_bools = []
                    for s in range(nslots):
                        sb = self.model.NewBoolVar(f"start_{teacher}_w{w}d{d}_s{s}")
                        if s == 0:
                            self.model.Add(sb == b[0])
                        else:
                            # sb == b[s] & not b[s-1]
                            self.model.Add(sb <= b[s])
                            self.model.Add(sb <= 1 - b[s-1])
                            self.model.Add(sb >= b[s] - b[s-1])
                        start_bools.append(sb)

                    for s in range(nslots):
                        dist = abs(s - 1)
                        if dist > 0:
                            term = self.model.NewIntVar(0, base_weight * dist, f"pref_term_{teacher}_w{w}d{d}_s{s}")
                            self.model.Add(term == base_weight * dist).OnlyEnforceIf(start_bools[s])
                            self.model.Add(term == 0).OnlyEnforceIf(start_bools[s].Not())
                            self.soft_terms.append(term)

                        if late_bias_weight > 0 and s > 0:
                            bias_term = self.model.NewIntVar(0, late_bias_weight * s, f"early_bias_{teacher}_w{w}d{d}_s{s}")
                            self.model.Add(bias_term == late_bias_weight * s).OnlyEnforceIf(start_bools[s])
                            self.model.Add(bias_term == 0).OnlyEnforceIf(start_bools[s].Not())
                            self.soft_terms.append(bias_term)

        # 3) Weich: Permutationspaare dichter zusammen – PAARZAHL LIMITIEREN
        w_perm_adjacent = 3
        pair_map: Dict[Tuple[str, str], List[Exam]] = defaultdict(list)
        for e in self.exams:
            pair_map[(e.pruefer, e.beisitzer)].append(e)
        num_slots_all = len(self.all_slots)
        for (P, B), exs_pb in pair_map.items():
            if (B, P) not in pair_map:
                continue
            exs_bp = pair_map[(B, P)]
            # Heuristik: sortiere nach ExamIdx, nur die k nächsten Paare bestrafen
            exs_pb_sorted = sorted(exs_pb, key=lambda ee: ee.idx)
            exs_bp_sorted = sorted(exs_bp, key=lambda ee: ee.idx)
            pairs = []
            # Greedy Match (gleichen Rang)
            for i in range(min(len(exs_pb_sorted), len(exs_bp_sorted))):
                pairs.append((exs_pb_sorted[i], exs_bp_sorted[i]))
                if len(pairs) >= LIMIT_PERM_PAIRS:
                    break
            # Fallback: wenn ungleich lang, ergänze mit restlichen nächsten
            i_bp = 0
            while len(pairs) < LIMIT_PERM_PAIRS and i_bp < len(exs_bp_sorted):
                for e1 in exs_pb_sorted:
                    pairs.append((e1, exs_bp_sorted[i_bp]))
                    if len(pairs) >= LIMIT_PERM_PAIRS:
                        break
                i_bp += 1

            for (e1, e2) in pairs:
                if not hasattr(self, "_permutation_pairs"):
                    self._permutation_pairs = []
                if (e1, e2) not in self._permutation_pairs and (e2, e1) not in self._permutation_pairs:
                    self._permutation_pairs.append((e1, e2))
                t1 = self.model.NewIntVar(0, num_slots_all - 1, f"perm_t1_e{e1.idx}_e{e2.idx}")
                t2 = self.model.NewIntVar(0, num_slots_all - 1, f"perm_t2_e{e1.idx}_e{e2.idx}")
                self.model.Add(t1 == sum(g * self.x[(e1.idx, g)] for g in range(num_slots_all)))
                self.model.Add(t2 == sum(g * self.x[(e2.idx, g)] for g in range(num_slots_all)))
                diff = self.model.NewIntVar(-num_slots_all, num_slots_all, f"perm_diff_e{e1.idx}_e{e2.idx}")
                self.model.Add(diff == t2 - t1)
                ad = self.model.NewIntVar(0, num_slots_all, f"perm_abs_e{e1.idx}_e{e2.idx}")
                self.model.AddAbsEquality(ad, diff)
                slack = self.model.NewIntVar(0, num_slots_all, f"perm_slack_e{e1.idx}_e{e2.idx}")
                self.model.Add(slack >= ad - 1)
                self.model.Add(slack >= 0)
                for _ in range(w_perm_adjacent):
                    self.soft_terms.append(slack)

        # 4) Weiche Kompaktheit pro Prüfer/Tag – reuse b-Vektoren
        gap_weight_inner   = GAP_WEIGHT_INNER
        gap_weight_outer   = GAP_WEIGHT_OUTER
        span_weight        = SPAN_WEIGHT

        for teacher, _ in self._exams_by_teacher.items():
            for (w, d), _day_slots in self.day_to_gslots.items():
                key = (teacher, w, d)
                if key not in self._teacher_day_struct:
                    continue
                b = self._teacher_day_struct[key]["b"]
                nslots = len(b)
                if nslots == 0:
                    continue

                prefix = [self.model.NewIntVar(0, nslots, f"soft_pref_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                suffix = [self.model.NewIntVar(0, nslots, f"soft_suff_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                self.model.Add(prefix[0] == b[0])
                for s in range(1, nslots):
                    self.model.Add(prefix[s] == prefix[s-1] + b[s])
                self.model.Add(suffix[nslots-1] == b[nslots-1])
                for s in range(nslots-2, -1, -1):
                    self.model.Add(suffix[s] == suffix[s+1] + b[s])

                left_pos  = [self.model.NewBoolVar(f"soft_left_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                right_pos = [self.model.NewBoolVar(f"soft_right_{teacher}_w{w}d{d}_s{s}") for s in range(nslots)]
                for s in range(nslots):
                    self.model.Add(prefix[s] >= 1).OnlyEnforceIf(left_pos[s])
                    self.model.Add(prefix[s] <= 0).OnlyEnforceIf(left_pos[s].Not())
                    self.model.Add(suffix[s] >= 1).OnlyEnforceIf(right_pos[s])
                    self.model.Add(suffix[s] <= 0).OnlyEnforceIf(right_pos[s].Not())

                # Wenn harte Lücken aktiv (wie oben), reduzieren wir die weiche Doppelstrafe:
                # Hier lassen wir Outer-Strafen bestehen (für Ränder), Inner-Strafen werden geringer gewichtet.
                inner_weight = gap_weight_inner // 2  # Halbierung, um Doppelzählung zu entschärfen

                for s in range(nslots):
                    both = self.model.NewBoolVar(f"soft_both_{teacher}_w{w}d{d}_s{s}")
                    self.model.AddBoolAnd([left_pos[s], right_pos[s]]).OnlyEnforceIf(both)
                    self.model.AddBoolOr([left_pos[s].Not(), right_pos[s].Not()]).OnlyEnforceIf(both.Not())

                    gap_inner = self.model.NewBoolVar(f"soft_gap_inner_{teacher}_w{w}d{d}_s{s}")
                    self.model.Add(gap_inner <= both)
                    self.model.Add(gap_inner <= 1 - b[s])

                    if inner_weight > 0:
                        term = self.model.NewIntVar(0, inner_weight, f"soft_gi_term_{teacher}_w{w}d{d}_s{s}")
                        self.model.Add(term == inner_weight).OnlyEnforceIf(gap_inner)
                        self.model.Add(term == 0).OnlyEnforceIf(gap_inner.Not())
                        self.soft_terms.append(term)

                for s in range(nslots):
                    outside = self.model.NewBoolVar(f"soft_outside_{teacher}_w{w}d{d}_s{s}")
                    both_lr = self.model.NewBoolVar(f"soft_bothlr_{teacher}_w{w}d{d}_s{s}")
                    self.model.AddBoolAnd([left_pos[s], right_pos[s]]).OnlyEnforceIf(both_lr)
                    self.model.AddBoolOr([left_pos[s].Not(), right_pos[s].Not()]).OnlyEnforceIf(both_lr.Not())
                    self.model.Add(outside <= 1 - both_lr)
                    self.model.Add(1 - outside <= both_lr)

                    outer_free = self.model.NewBoolVar(f"soft_outer_free_{teacher}_w{w}d{d}_s{s}")
                    self.model.Add(outer_free <= outside)
                    self.model.Add(outer_free <= 1 - b[s])

                    if gap_weight_outer > 0:
                        term2 = self.model.NewIntVar(0, gap_weight_outer, f"soft_go_term_{teacher}_w{w}d{d}_s{s}")
                        self.model.Add(term2 == gap_weight_outer).OnlyEnforceIf(outer_free)
                        self.model.Add(term2 == 0).OnlyEnforceIf(outer_free.Not())
                        self.soft_terms.append(term2)

                count = self.model.NewIntVar(0, nslots, f"soft_count_{teacher}_w{w}d{d}")
                self.model.Add(count == sum(b))

                if span_weight > 0 and nslots >= 2:
                    sum_left  = self.model.NewIntVar(0, nslots, f"soft_sumleft_{teacher}_w{w}d{d}")
                    sum_right = self.model.NewIntVar(0, nslots, f"soft_sumright_{teacher}_w{w}d{d}")
                    self.model.Add(sum_left  == sum(left_pos))
                    self.model.Add(sum_right == sum(right_pos))

                    span_proxy = self.model.NewIntVar(0, 2*nslots, f"soft_span_{teacher}_w{w}d{d}")
                    self.model.Add(span_proxy >= sum_left + sum_right - 2*count)
                    self.model.Add(span_proxy <= sum_left + sum_right)
                    for _ in range(span_weight):
                        self.soft_terms.append(span_proxy)

        # 5) Gleichmäßigere Verteilung über erlaubte Tage (weich)
        allowed_days = [(w, d) for w in WEEKS for d in range(5) if (w, d) not in self.no_exam_days]
        if allowed_days:
            total_exams = len(self.exams)
            num_days = len(allowed_days)
            base_target = total_exams // num_days
            remainder = total_exams - base_target * num_days

            self._day_targets = {}
            self._day_count_vars = {}
            for i, (w, d) in enumerate(allowed_days):
                target = base_target + (1 if i < remainder else 0)
                self._day_targets[(w, d)] = target

            for (w, d) in allowed_days:
                slots = self.day_to_gslots[(w, d)]
                cnt = self.model.NewIntVar(0, len(self.exams), f"day_count_w{w}d{d}")
                self.model.Add(cnt == sum(self.x[(e.idx, g)] for e in self.exams for g in slots))
                self._day_count_vars[(w, d)] = cnt

            weight_balance = DAY_WEIGHT_BALANCE
            for i, (w, d) in enumerate(allowed_days):
                target = base_target + (1 if i < remainder else 0)
                sp = self.model.NewIntVar(0, len(self.exams), f"dpos_w{w}d{d}")
                sn = self.model.NewIntVar(0, len(self.exams), f"dneg_w{w}d{d}")
                self.model.Add(self._day_count_vars[(w, d)] - target == sp - sn)
                if weight_balance > 0:
                    for _ in range(weight_balance):
                        self.soft_terms.append(sp)
                        self.soft_terms.append(sn)

        added_terms = len(self.soft_terms) - before_terms
        vprint(f"[Constraints] Weiche Ziele ergänzt (+{added_terms}).")

    def _available_days(self, exam):
        """Tatsächliche Tagesdomäne einer Prüfung, nach Sperren und Abwesenheiten."""
        days = {day for day, slots in self.day_to_gslots.items() if slots}
        if self.config.hard_unavailability:
            days -= self.unavailability.get(exam.pruefer, set())
            days -= self.unavailability.get(exam.beisitzer, set())
        return days

    def _infeasibility_findings(self):
        """Nur notwendige Bedingungen melden; keine Regel ohne Beleg beschuldigen."""
        findings = []
        def tag(day):
            return f"{DAYS[day[1]]}{day[0]}"
        capacity = len(self.all_slots) * len(self.params.rooms)
        if len(self.exams) > capacity:
            findings.append(f"Raumkapazität: {len(self.exams)} Prüfungen, aber nur {capacity} "
                            "Plätze. Ergänzen Sie Räume oder Slots oder geben Sie weitere Prüfungstage frei "
                            "(Einstellungen → Räume/Zeit/Bedingungen).")
        domains = {e.idx: self._available_days(e) for e in self.exams}
        students = defaultdict(list)
        for e in self.exams:
            students[e.schueler].append(e)
            if not domains[e.idx]:
                findings.append(f"Prüfung #{e.idx}: {e.schueler}, {e.fach}, Prüfer {e.pruefer}, "
                                f"Beisitzer {e.beisitzer or 'leer'}: kein gemeinsamer Prüfungstag. "
                                "Prüfen Sie Abwesenheiten und Tagessperren (Einstellungen → Bedingungen) "
                                "sowie die Slotzahl (Einstellungen → Zeit).")
            if e.pruefer and e.pruefer == e.beisitzer:
                findings.append(f"Prüfung #{e.idx} ({e.schueler}, {e.fach}): {e.pruefer} ist zugleich "
                                "Prüfer und Beisitzer. Weisen Sie unterschiedliche Lehrkräfte zu.")
        for person, exams in self._exams_by_teacher.items():
            days = set().union(*(domains[e.idx] for e in exams))
            limit = 5 if person in self.config.teachers_allow_5_per_day else self.config.default_max_per_day
            capacities = sorted((min(limit, len(self.day_to_gslots[day])) for day in days), reverse=True)
            max_days = len(days)
            if self.config.hard_max_days_per_teacher_enabled and self.config.hard_max_days_per_teacher_K is not None:
                max_days = min(max_days, max(0, self.config.hard_max_days_per_teacher_K))
                capacities = capacities[:max(0, self.config.hard_max_days_per_teacher_K)]
            possible = sum(capacities)
            if len(exams) > possible:
                p = sum(e.pruefer == person for e in exams)
                b = sum(e.beisitzer == person for e in exams)
                cause = f"maximal {limit} Prüfungen pro Tag an {max_days} möglichen Einsatztagen"
                if possible < limit * max_days:
                    cause += "; begrenzt durch die verfügbaren Slots"
                findings.append(f"Lehrkraft {person or '(leeres Kürzel)'}: {len(exams)} Einsätze "
                                f"({p} als Prüfer, {b} als Beisitzer). Mit den aktuellen Einstellungen "
                                f"sind höchstens {possible} möglich ({cause}). "
                                "Prüfen Sie Tageslimit, Einsatztage und Abwesenheiten (Einstellungen → Bedingungen) "
                                "oder ändern Sie die Ausschussbesetzung. Zusätzliche Räume helfen hier nicht.")
            # Kapazität innerhalb einer eingeschränkten Tagesmenge: andere Einsätze
            # derselben Person können nicht auf zusätzliche Tage ausweichen.
            for restricted in {frozenset(domains[e.idx]) for e in exams}:
                if not restricted or restricted == days:
                    continue
                forced = [e for e in exams if domains[e.idx] <= restricted]
                available = sum(min(limit, len(self.day_to_gslots[d])) for d in restricted)
                if len(forced) > available:
                    findings.append(f"Lehrkraft {person}: {len(forced)} Einsätze müssen auf "
                                    f"{', '.join(map(tag, sorted(restricted)))} liegen, dort sind nur "
                                    f"{available} möglich. Erhöhen Sie das Tageslimit oder ermöglichen Sie "
                                    "weitere gemeinsame Prüfungstage (Einstellungen → Bedingungen).")
        for student, exams in students.items():
            weeks = {w for w, _ in set().union(*(domains[e.idx] for e in exams))}
            # Entspricht der exakten Wochenregel des Modells: je Woche mit Slots = 1.
            model_weeks = {w for w, _, _ in self.all_slots}
            if self.config.hard_student_one_per_week:
                if len(exams) != len(model_weeks):
                    findings.append(f"Schüler {student}: {len(exams)} Prüfungen, aber die Regel "
                                    f"„Genau eine Prüfung pro Woche“ verlangt {len(model_weeks)}. "
                                    "Prüfen Sie die Prüfungsdaten oder deaktivieren Sie diese Regel unter Bedingungen.")
                missing = model_weeks - weeks
                if missing:
                    findings.append(f"Schüler {student}: keine Prüfung kann in Woche "
                                    f"{', '.join(map(str, sorted(missing)))} stattfinden, obwohl dort genau "
                                    "eine verlangt wird. Prüfen Sie Abwesenheiten, Tagessperren oder die Wochenregel.")
            gap = self.config.hard_min_gap_days_same_student
            if gap is not None and len(exams) > 1:
                for i, first in enumerate(exams):
                    for second in exams[i + 1:]:
                        distances = [abs((w1 - w2) * 7 + d1 - d2)
                                     for w1, d1 in domains[first.idx] for w2, d2 in domains[second.idx]
                                     if not self.config.hard_student_one_per_week or w1 != w2]
                        if distances and max(distances) < gap:
                            findings.append(f"Schüler {student}, Prüfungen #{first.idx}/#{second.idx}: "
                                            f"höchstens {max(distances)} Tage Abstand möglich, gefordert {gap}. "
                                            "Verringern Sie den Mindestabstand oder ermöglichen Sie weitere "
                                            "Prüfungstage (Einstellungen → Bedingungen).")
        if self.config.hard_grouping_enabled and self.config.grouping_block_size in (2, 3, 4, 5):
            size = self.config.grouping_block_size
            for (topic, subject, teacher), exams in group_exams_for_blocking(self.exams).items():
                exams = sorted(exams, key=lambda e: e.schueler)
                for start in range(0, len(exams), size):
                    chunk = exams[start:start + size]
                    if len(chunk) < 2:
                        continue
                    # Ohne langen Tag überspringt das bestehende Modell den Block.
                    if not any(len(slots) >= len(chunk) for slots in self.day_to_gslots.values()):
                        continue
                    common = set.intersection(*(domains[e.idx] for e in chunk))
                    common = {d for d in common if len(self.day_to_gslots[d]) >= len(chunk)}
                    if not common:
                        findings.append(f"Kopplungsblock {subject}, Thema „{topic}“, Prüfer {teacher}, "
                                        f"kein gemeinsamer Tag mit {len(chunk)} aufeinanderfolgenden Slots. "
                                        "Prüfen Sie Abwesenheiten, Slotzahl oder Kopplung.")
        return findings

    def _probe_changes(self):
        """Bis zu 12 s Suchzeit plus Modellaufbau; Einstellungen und Hauptmodell bleiben erhalten.

        FEASIBLE ist ein Nachweis für das geänderte Zeitmodell, UNKNOWN keine Aussage.
        Raumkonstanz wird erst bei der anschließenden Raumvergabe geprüft.
        """
        variants = []
        c = self.config
        if c.hard_max_days_per_teacher_enabled and c.hard_max_days_per_teacher_K is not None:
            variants.append((f"Maximale Einsatztage von {c.hard_max_days_per_teacher_K} auf "
                             f"{c.hard_max_days_per_teacher_K + 1} erhöhen",
                             replace(c, hard_max_days_per_teacher_K=c.hard_max_days_per_teacher_K + 1), self.no_exam_days, False))
        if c.hard_min_gap_days_same_student is not None and c.hard_min_gap_days_same_student > 0:
            variants.append((f"Harten Schülerabstand von {c.hard_min_gap_days_same_student} auf "
                             f"{c.hard_min_gap_days_same_student - 1} Tage verringern",
                             replace(c, hard_min_gap_days_same_student=c.hard_min_gap_days_same_student - 1), self.no_exam_days, False))
        if c.hard_grouping_enabled:
            variants.append(("Harte Kopplung deaktivieren", replace(c, hard_grouping_enabled=False), self.no_exam_days, False))
        if c.hard_student_one_per_week:
            variants.append(("Regel „Genau eine Prüfung pro Woche“ deaktivieren", replace(c, hard_student_one_per_week=False), self.no_exam_days, False))
        variants.append((f"Standard-Tageslimit von {c.default_max_per_day} auf {c.default_max_per_day + 1} erhöhen",
                         replace(c, default_max_per_day=c.default_max_per_day + 1), self.no_exam_days, False))
        for day in sorted(self.no_exam_days):
            variants.append((f"Prüfungstag {DAYS[day[1]]}{day[0]} freigeben", c, self.no_exam_days - {day}, False))
        if c.hard_unavailability and self.unavailability:
            variants.append(("Abwesenheiten vollständig deaktivieren (nur Diagnose)", replace(c, hard_unavailability=False), self.no_exam_days, False))
        # Vorrangig erkennen, ob die nicht einstellbare Lückenregel beteiligt ist.
        variants.insert(0, ("Lücken zwischen Personeneinsätzen erlauben (nur Diagnose, derzeit kein GUI-Schalter)", c, self.no_exam_days, True))
        variants = [(*variant, self.params) for variant in variants]
        extra_room = "Zusätzlicher Diagnoseraum"
        while extra_room in self.params.rooms:
            extra_room += "_"
        variants.insert(2, ("Einen zusätzlichen Raum bereitstellen", c, self.no_exam_days, False,
                            replace(self.params, rooms=list(self.params.rooms) + [extra_room])))
        variants.insert(3, ("Einen zusätzlichen Slot je vorhandenem Prüfungstag bereitstellen", c,
                            self.no_exam_days, False,
                            replace(self.params, slots_per_day={day: slots + 1 if slots > 0 else 0
                                                               for day, slots in self.params.slots_per_day.items()})))
        results = []
        deadline = time.monotonic() + 12
        for label, config, blocked, allow_gaps, params in variants:
            if time.monotonic() >= deadline:
                break
            vprint(f"Diagnoseversuch (separate Kopie): {label}")
            trial = ColloquiumScheduler(self.exams, params, config, self.unavailability, blocked)
            trial._diagnostic_allow_gaps = allow_gaps
            trial.add_basic_constraints()
            trial.add_hard_constraints()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            probe = cp_model.CpSolver()
            probe.parameters.max_time_in_seconds = min(2.0, remaining)
            probe.parameters.num_search_workers = 1
            result = probe.Solve(trial.model)
            if result in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                results.append(f"Erfolgreich geprüft: {label}. Ein Zeitplan ist damit möglich.")
            elif result == cp_model.INFEASIBLE:
                results.append(f"Nicht ausreichend: {label} löst den Konflikt allein nicht.")
            else:
                results.append(f"Ungeklärt: {label}; im Diagnosezeitbudget keine Entscheidung.")
        if len(results) < len(variants):
            results.append("Weitere Varianten wurden wegen des Diagnosezeitbudgets nicht untersucht.")
        return results

    def _solution_wishes(self, solver):
        """Konkrete Abweichungen von messbaren Wünschen, aus der gültigen Lösung."""
        assigned = {e.idx: next(self.all_slots[g] for g in range(len(self.all_slots))
                               if solver.BooleanValue(self.x[(e.idx, g)])) for e in self.exams}
        wishes = []
        desired = self.config.soft_desired_gap_days_same_student
        if desired is not None:
            students = defaultdict(list)
            for e in self.exams:
                students[e.schueler].append(e)
            for student, exams in students.items():
                for i, first in enumerate(exams):
                    for second in exams[i + 1:]:
                        w1, d1, _ = assigned[first.idx]
                        w2, d2, _ = assigned[second.idx]
                        gap = abs((w1 - w2) * 7 + d1 - d2)
                        if gap < desired:
                            wishes.append(f"Schülerabstand {student}, {first.fach}/{second.fach}: "
                                          f"{gap} statt gewünschter {desired} Tage.")
        if self.config.soft_prefer_second_slot_start:
            for person, exams in self._exams_by_teacher.items():
                starts = {}
                for e in exams:
                    w, d, slot = assigned[e.idx]
                    starts[(w, d)] = min(starts.get((w, d), slot), slot)
                for (w, d), slot in sorted(starts.items()):
                    if slot != 1:
                        wishes.append(f"Startwunsch: {person or '(leeres Kürzel)'}, {DAYS[d]}{w}: "
                                      f"Beginn in Slot {slot + 1} statt Slot 2.")
        if DAY_WEIGHT_BALANCE > 0:
            for day, target in getattr(self, "_day_targets", {}).items():
                actual = sum(assigned[e.idx][:2] == day for e in self.exams)
                if actual != target:
                    wishes.append(f"Tagesverteilung: {DAYS[day[1]]}{day[0]}: {actual} Prüfungen "
                                  f"statt Zielwert {target}.")
        # Nur tatsächlich in add_soft_constraints() optimierte Permutationspaare
        # auswerten, statt alle beliebigen Rollentauschkombinationen zu behaupten.
        for first, second in getattr(self, "_permutation_pairs", []):
            pos1 = self.all_slots.index(assigned[first.idx])
            pos2 = self.all_slots.index(assigned[second.idx])
            distance = abs(pos1 - pos2)
            if distance > 1:
                wishes.append(f"Nähe bei Rollentausch {first.pruefer}/{first.beisitzer}: "
                              f"Prüfungen #{first.idx}/#{second.idx} haben {distance} Zeitplätze Abstand "
                              "statt direkt benachbarter Zeitplätze.")
        return wishes

    def solve(self, time_limit_sec: Optional[int] = 60):
        vprint("Solver gestartet")
        if self.soft_terms:
            self.model.Minimize(sum(self.soft_terms))

        solver = cp_model.CpSolver()
        if time_limit_sec:
            solver.parameters.max_time_in_seconds = float(time_limit_sec)
        solver.parameters.num_search_workers = CP_WORKERS
        solver.parameters.linearization_level = 1  # Tipp: 2 testen für evtl. bessere Pruning
        solver.parameters.cp_model_presolve = True
        solver.parameters.cp_model_probing_level = 1  # aktiviert Probing

        # Live-Status
        import time
        class FriendlyProgress(cp_model.CpSolverSolutionCallback):
            def __init__(self, outer: "ColloquiumScheduler"):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.outer = outer
                import time
                self.start = time.time()
                self.last_report = self.start
                self.best_obj = None
                self.solution_count = 0
                self.min_report_interval = 20.0
                self.min_improvement = 1000
                self.last_logged_obj = None
                self.last_logged_time = self.start

            def OnSolutionCallback(self):
                import time
                self.solution_count += 1
                now = time.time()
                elapsed = now - self.start

                curr_obj = None
                try:
                    curr_obj = int(self.ObjectiveValue()) if self.ObjectiveValue() is not None else None
                except Exception:
                    curr_obj = None

                allow_time = (now - self.last_logged_time) >= self.min_report_interval
                allow_improve = False
                if curr_obj is not None:
                    if self.last_logged_obj is None or (self.last_logged_obj - curr_obj) >= self.min_improvement:
                        allow_improve = True

                if VERBOSE and (allow_time or allow_improve):
                    days_used, days_total, day_dev, gap_issues, start_issues, rooms_used = self._compute_live_indicators()
                    # Initialisiere den Basis-Objektivwert einmalig (erster gültiger curr_obj)
                    if getattr(self, "base_obj", None) is None and curr_obj is not None:
                        self.base_obj = curr_obj
 
                    # Qualität berechnen
                    if curr_obj is not None and getattr(self, "base_obj", None) is not None:
                        base_obj = self.base_obj
                        if base_obj <= 0:
                            # Sonderfall: absolute Differenz verwenden
                            qual_str = f"{abs(base_obj - curr_obj):.1f}"
                        else:
                            qual_pct = (base_obj - curr_obj) / base_obj * 100.0
                            # Negative Prozentwerte vermeiden (falls curr_obj schlechter als base_obj ist)
                            qual_pct = max(0.0, qual_pct)
                            qual_str = f"{qual_pct:.1f}%"
                    else:
                       qual_str = "n/a"
                    day_dev_str = "" if day_dev is None else str(int(day_dev))
                    vprint(
                        f"Laufzeit {elapsed:.0f}s | {self.solution_count} Lösungen | Qualität {qual_str} | "
                        f"Tage: {days_used}/{days_total} belegt | "
                        f"Tagesverteilung: Abw. {day_dev_str} | Abstand(Std): {gap_issues} | "
                        f"Startwunsch: {start_issues} | genutzte Räume: {rooms_used}"
                    )
                    self.last_logged_time = now
                    if curr_obj is not None:
                        self.last_logged_obj = curr_obj

            def _compute_live_indicators(self):
                days_used = 0
                days_total = 0
                day_dev = None
                if hasattr(self.outer, "_day_count_vars") and self.outer._day_count_vars:
                    days_total = len(self.outer._day_count_vars)
                    counts = {}
                    for (w, d), var in self.outer._day_count_vars.items():
                        counts[(w, d)] = self.Value(var)
                    days_used = sum(1 for c in counts.values() if c > 0)
                    if hasattr(self.outer, "_day_targets") and self.outer._day_targets:
                        day_dev = sum(abs(counts[(w, d)] - self.outer._day_targets.get((w, d), 0))
                                      for (w, d) in counts.keys())

                gap_issues = 0
                if self.outer.config.soft_desired_gap_days_same_student is not None:
                    desired = self.outer.config.soft_desired_gap_days_same_student
                    ord_map = {}
                    for w in WEEKS:
                        for d in range(5):
                            ord_map[(w, d)] = (w - 1) * 7 + d
                    e_to_day = {}
                    for e in self.outer.exams:
                        gs = None
                        for gslot, (w, d, s) in enumerate(self.outer.all_slots):
                            if self.Value(self.outer.x[(e.idx, gslot)]):
                                gs = (w, d)
                                break
                        e_to_day[e.idx] = gs
                    by_student = defaultdict(list)
                    for e in self.outer.exams:
                        by_student[e.schueler].append(e)
                    for _, exs in by_student.items():
                        if len(exs) <= 1:
                            continue
                        ords = []
                        for e in exs:
                            wd = e_to_day.get(e.idx)
                            if wd is not None:
                                ords.append(ord_map[wd])
                        ords.sort()
                        for i in range(len(ords)-1):
                            if abs(ords[i+1] - ords[i]) < desired:
                                gap_issues += 1
                                break

                start_issues = 0
                if self.outer.config.soft_prefer_second_slot_start:
                    exams_by_teacher = defaultdict(list)
                    for e in self.outer.exams:
                        exams_by_teacher[e.pruefer].append(e)
                    for teacher, exs in exams_by_teacher.items():
                        for (w, d), day_slots in self.outer.day_to_gslots.items():
                            b = []
                            for gslot in day_slots:
                                active = sum(self.Value(self.outer.x[(e.idx, gslot)]) for e in exs)
                                b.append(1 if active >= 1 else 0)
                            if any(b):
                                try:
                                    start_pos = b.index(1)
                                    if start_pos != 1:
                                        start_issues += 1
                                except ValueError:
                                    pass

                rooms_used = 0
                try:
                    all_rooms = set(self.outer.params.rooms) if getattr(self.outer.params, "rooms", None) else set()
                    R = len(all_rooms)
                    max_parallel = 0
                    for gslot_idx, (w, d, s) in enumerate(self.outer.all_slots):
                        par = sum(self.Value(self.outer.x[(e.idx, gslot_idx)]) for e in self.outer.exams)
                        if par > max_parallel:
                            max_parallel = par
                    rooms_used = min(R, max_parallel) if R > 0 else 0
                except Exception:
                    rooms_used = 0

                return days_used, days_total, day_dev, gap_issues, start_issues, rooms_used

        cb = FriendlyProgress(self)

        solver.parameters.log_search_progress = False
        solver.parameters.log_to_stdout = False

        status = solver.Solve(self.model, cb)

        report = self.feedback
        report.update(status=status_to_str(status), findings=[], suggestions=[], wishes=[], room_notes=[])
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            report["summary"] = ("Gültiger Zeitplan gefunden; alle im Zeitmodell erzwungenen harten Regeln eingehalten. "
                                 + ("Gewichtete Ziele optimal für dieses Modell." if status == cp_model.OPTIMAL
                                    else "Die bestmögliche Qualität ist noch nicht nachgewiesen."))
            report["wishes"] = self._solution_wishes(solver)
            if self.config.hard_grouping_enabled and self.config.grouping_block_size in (2, 3, 4, 5):
                size = self.config.grouping_block_size
                for key, exams in group_exams_for_blocking(self.exams).items():
                    exams = sorted(exams, key=lambda e: e.schueler)
                    for start in range(0, len(exams), size):
                        chunk = exams[start:start + size]
                        if len(chunk) > 1 and not any(len(slots) >= len(chunk) for slots in self.day_to_gslots.values()):
                            report["findings"].append(f"Kopplung nicht erzwungen: Thema „{key[0]}“, Fach {key[1]}, "
                                                      f"Prüfer {key[2]}: kein Tag hat {len(chunk)} Slots. "
                                                      "Prüfen Sie Slotzahl oder Blockgröße.")
            if self.config.soft_minimize_rooms_used:
                report["wishes"].append("Wunsch „Min. Räume“: Der Schalter hat derzeit keine eigene Wirkung im Solver.")
        elif status == cp_model.INFEASIBLE:
            report["summary"] = "Mit den aktuellen Daten und harten Regeln ist kein Zeitplan möglich (nachgewiesen)."
            report["findings"] = self._infeasibility_findings()
            if not report["findings"]:
                report["findings"].append("Keine einzelne Engstelle erkannt; Regelkombinationen wurden geprüft. "
                                          "Personeneinsätze müssen pro Tag lückenlos liegen.")
                vprint(report["findings"][0])
                report["suggestions"] = self._probe_changes()
                report["suggestions"].insert(0, "Nur das Zeitmodell wurde geprüft; Einstellungen bleiben unverändert. "
                                            "Raumvergabe und Wünsche sind noch nicht geprüft.")
            else:
                report["suggestions"].append("Beheben Sie zuerst die genannten Engstellen. "
                                             "Weitere Konflikte können bestehen bleiben.")
        elif status == cp_model.MODEL_INVALID:
            report["summary"] = "Das Solvermodell ist ungültig; dies ist kein Nachweis unlösbarer Prüfungsdaten."
            report["findings"].append(self.model.Validate() or solver.ResponseStats())
        else:
            report["summary"] = "Innerhalb der Rechenzeit wurde kein Plan gefunden; Unlösbarkeit ist nicht nachgewiesen."
            report["suggestions"].append("Erhöhen Sie die CP-Rechenzeit (Einstellungen → Bedingungen).")
        vprint(format_feedback(report) if self.log_detailed_feedback else report["summary"])
        return solver, status

    def assign_rooms_for_day_mip(self,
                                 day_exams: List[Tuple[Exam, int]],
                                 w: int,
                                 d: int,
                                 rooms_cost_weight: int = 1) -> Dict[int, Optional[str]]:
        # --- Diagnose: Eingang ---
        vprint(f"[MIP] Start Raumvergabe für {DAYS[d]} (Woche {w}) | Prüfungen an Tag: {len(day_exams)} | Räume: {len(self.params.rooms)}")
        # Zeige parallele Prüfungen pro Slot
        _par_by_slot = defaultdict(int)
        for _e, s_local in day_exams:
            _par_by_slot[s_local] += 1

        rooms = self.params.rooms
        R = len(rooms)

        # Clusterbildung: Prüfer-Konstanz, Permutation, Kopplung, Rollenübergreifend
        parent = {}
        def find(a):
            parent.setdefault(a, a)
            if parent[a] != a:
                parent[a] = find(parent[a])
            return parent[a]
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        exams_by_teacher = defaultdict(list)
        for e, s_local in day_exams:
            exams_by_teacher[e.pruefer].append((e, s_local))
        for p, lst in exams_by_teacher.items():
            base = lst[0][0].idx
            for (e, _) in lst[1:]:
                union(base, e.idx)

        pair_present = defaultdict(set)
        for e, _ in day_exams:
            pair_present[frozenset({e.pruefer, e.beisitzer})].add((e.pruefer, e.beisitzer))
        for pbset, ordered in pair_present.items():
            if len(ordered) >= 2 and any((b, a) in ordered for (a, b) in ordered):
                p1, p2 = list(pbset)
                left = exams_by_teacher.get(p1, [])
                right = exams_by_teacher.get(p2, [])
                if left and right:
                    base = left[0][0].idx
                    for (e, _) in left[1:]:
                        union(base, e.idx)
                    for (e, _) in right:
                        union(base, e.idx)

        by_key = defaultdict(list)
        for e, s_local in day_exams:
            by_key[(e.thema, e.fach, e.pruefer)].append((e, s_local))
        for lst in by_key.values():
            lst.sort(key=lambda t: t[1])
            base = lst[0][0].idx
            for (e, _) in lst[1:]:
                union(base, e.idx)

        #Rollenübergreifende Clusterbildung: (A,B) und (B,C) werden wegen B zu einme Cluster
        #person_exams = defaultdict(list)
        #for e, s_local in day_exams:
        #    person_exams[e.pruefer].append((e, s_local))
        #    if not self.config.ignore_empty_beisitzer or (e.beisitzer and e.beisitzer.strip() != ""):
        #        person_exams[e.beisitzer].append((e, s_local))

        #for person, plist in person_exams.items():
        #    if len(plist) <= 1:
        #        continue
        #    base = plist[0][0].idx
        #    for (e, _) in plist[1:]:
        #        union(base, e.idx)

        cluster_members = defaultdict(list)
        for e, _ in day_exams:
            cluster_members[find(e.idx)].append(e.idx)
        clusters = list(cluster_members.values())
        K = len(clusters)

        local_slots = sorted(set(s for (_, s) in day_exams))

        exam_to_cluster = {}
        for cid, members in enumerate(clusters):
            for eidx in members:
                exam_to_cluster[eidx] = cid
        slot_clusters: Dict[int, Set[int]] = defaultdict(set)
        for (e, s_local) in day_exams:
            slot_clusters[s_local].add(exam_to_cluster[e.idx])

        # --- Diagnose: Cluster-Überblick ---
        try:
            vprint(f"[MIP] Cluster gesamt: {K} | Slots an Tag: {len(local_slots)}")
            # Sortierte Slot-Liste für reproduzierbare Ausgabe
            _sorted_slots = sorted(local_slots)
            for s in _sorted_slots:
                c_cnt = len(slot_clusters[s])
                par_cnt = _par_by_slot.get(s, 0)
                vprint(f"[MIP]  Slot {s:02d}: parallel Prüfungen={par_cnt}, aktive Cluster={c_cnt}")
        except Exception:
            pass

        # Bisherige 'impossible'-Heuristik: Cluster-Anzahl pro Slot > R
        impossible = any(len(slot_clusters[s]) > R for s in local_slots)
        if impossible:
            # --- Diagnose: genaue Slots mit Überlast ausgeben
            try:
                over_slots = []
                for s in sorted(local_slots):
                    c_cnt = len(slot_clusters[s])
                    if c_cnt > R:
                        over_slots.append((s, c_cnt, _par_by_slot.get(s, 0)))
                if over_slots:
                    msg = "; ".join([f"s={s} (Cluster={c_cnt} > Räume={R}, Prüfungen={par})" for (s, c_cnt, par) in over_slots])
                    vprint(f"[MIP][Warn] Cluster-basierte Kapazität übersteigt Räume: {msg}")
                    vprint("[MIP][Hinweis] Prüfen Sie die Raumkonstanz der Ausschüsse und Themenblöcke.")
            except Exception:
                pass

        model = cp_model.CpModel()
        a = [[model.NewBoolVar(f"a_c{c}_r{r}") for r in range(R)] for c in range(K)]
        z = {}
        for s in local_slots:
            for r in range(R):
                for c in range(K):
                    if c in slot_clusters[s]:
                        z[(s, r, c)] = model.NewBoolVar(f"z_s{s}_r{r}_c{c}")

        # Jeder Cluster genau ein Raum (tageweit)
        for c in range(K):
            model.Add(sum(a[c][r] for r in range(R)) == 1)

        # z nur erlaubt, wenn a[c,r] = 1
        for s in local_slots:
            for r in range(R):
                for c in slot_clusters[s]:
                    model.Add(z[(s, r, c)] <= a[c][r])

        # Jeder aktive Cluster im Slot s genau einem Raum
        for s in local_slots:
            model.Add(sum(z[(s, r, c)] for r in range(R) for c in slot_clusters[s]) == len(slot_clusters[s]))

        # Slot-Raum-Kapazität
        for s in local_slots:
            for r in range(R):
                model.Add(sum(z[(s, r, c)] for c in slot_clusters[s]) <= 1)

        room_soft_terms = []

        # NEU: tageweite Raumnutzungsindikatoren y[r] für Reihenfolgepräferenz
        y = [model.NewBoolVar(f"y_r{r}") for r in range(R)]
        for r in range(R):
            for c in range(K):
                model.Add(a[c][r] <= y[r])
            sum_a_r = model.NewIntVar(0, K, f"sum_a_r{r}")
            model.Add(sum_a_r == sum(a[c][r] for c in range(K)))
            model.Add(y[r] <= sum_a_r)

        # Lücken je Raum minimieren
        for r in range(R):
            nslots = len(local_slots)
            if nslots == 0:
                continue

            b_r = []
            for idx_s, s in enumerate(local_slots):
                br = model.NewBoolVar(f"room_used_r{r}_s{idx_s}")
                model.Add(br >= sum(z[(s, r, c)] for c in slot_clusters[s]))
                b_r.append(br)

            prefix = [model.NewIntVar(0, nslots, f"r{r}_pref_{i}") for i in range(nslots)]
            suffix = [model.NewIntVar(0, nslots, f"r{r}_suff_{i}") for i in range(nslots)]
            model.Add(prefix[0] == b_r[0])
            for i in range(1, nslots):
                model.Add(prefix[i] == prefix[i-1] + b_r[i])
            model.Add(suffix[nslots-1] == b_r[nslots-1])
            for i in range(nslots-2, -1, -1):
                model.Add(suffix[i] == suffix[i+1] + b_r[i])

            for i in range(nslots):
                left_pos  = model.NewBoolVar(f"r{r}_left_{i}")
                right_pos = model.NewBoolVar(f"r{r}_right_{i}")
                model.Add(prefix[i] >= 1).OnlyEnforceIf(left_pos)
                model.Add(prefix[i] <= 0).OnlyEnforceIf(left_pos.Not())
                model.Add(suffix[i] >= 1).OnlyEnforceIf(right_pos)
                model.Add(suffix[i] <= 0).OnlyEnforceIf(right_pos.Not())
                both = model.NewBoolVar(f"r{r}_both_{i}")
                model.AddBoolAnd([left_pos, right_pos]).OnlyEnforceIf(both)
                model.AddBoolOr([left_pos.Not(), right_pos.Not()]).OnlyEnforceIf(both.Not())
                gap_i = model.NewBoolVar(f"r{r}_gap_{i}")
                model.Add(gap_i <= both)
                model.Add(gap_i <= 1 - b_r[i])
                room_soft_terms.append(gap_i)

        # Ziel: Reihenfolgepräferenz + Lücken
        # Entfernt: Präferenz 'vorderste Räume zuerst'
        gap_weight = 1
        tiny = 1
        a_order_term = sum((r + 1) * a[c][r] for c in range(K) for r in range(R))
        # Neue Zielfunktion ohne room_order_term
        model.Minimize(gap_weight * sum(room_soft_terms) + tiny * a_order_term)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = MIP_ROOM_SOLVER_LIMIT
        solver.parameters.num_search_workers = MIP_ROOM_SOLVER_WORKER
        solver.parameters.log_search_progress = False
        solver.parameters.log_to_stdout = False

        # NEU: Heuristische Startlösung (AddHint) in Raumreihenfolge
        # Weisen wir Cluster sequentiell Räume über Slots zu (greedy), dann setzen wir a und z als Hint.
        #hints_a = []
        #hints_z = []
        #cluster_fixed_room: Dict[int, Optional[int]] = {}
        #for s in local_slots:
        #    used_rooms = set()
        #    c_order = sorted(slot_clusters[s])
        #    for c in c_order:
        #        r_choice = cluster_fixed_room.get(c, None)
        #        if r_choice is not None and r_choice < R and r_choice not in used_rooms:
        #            used_rooms.add(r_choice)
        #            continue
        #        chosen = None
        #        for r in range(R):
        #            if r not in used_rooms:
        #                chosen = r
        #                break
        #        if chosen is not None:
        #            used_rooms.add(chosen)
        #            cluster_fixed_room[c] = chosen
        #        else:
        #            cluster_fixed_room.setdefault(c, None)
        # Setze Hints:
        #for c in range(K):
        #    r_idx = cluster_fixed_room.get(c, None)
        #    for r in range(R):
        #        hints_a.append((a[c][r], 1 if (r_idx is not None and r == r_idx) else 0))
        #for s in local_slots:
        #    for r in range(R):
        #        for c in slot_clusters[s]:
        #            val = 1 if (cluster_fixed_room.get(c, None) == r) else 0
        #            hints_z.append((z[(s, r, c)], val))
        #for var, val in hints_a + hints_z:
        #    model.AddHint(var, val)
        
        status = solver.Solve(model)
        if status == cp_model.INFEASIBLE or impossible:
            vprint(f"Raumvergabe für {DAYS[d]} (Woche {w}): Anforderungen zu hoch – es wird eine einfache Zuweisung versucht.")
            # Zusatzdiagnose: maximal gleichzeitige Cluster vs. Räume
            try:
                peak_clusters = max((len(slot_clusters[s]) for s in local_slots), default=0)
                peak_parallel = max((_par_by_slot.get(s, 0) for s in local_slots), default=0)
                vprint(f"[MIP][Diag] Peak: aktive Cluster={peak_clusters}, parallele Prüfungen={peak_parallel}, Räume={R}")
            except Exception:
                pass
        elif status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            vprint(f"Raumvergabe für {DAYS[d]} (Woche {w}): Räume wurden passend verteilt.")
            if status == cp_model.FEASIBLE:
                self.feedback["room_notes"].append(f"{DAYS[d]}{w}: gültige Raumzuweisung gefunden; "
                                                    "beste Raumqualität innerhalb der Rechenzeit nicht nachgewiesen.")

        assign: Dict[int, Optional[str]] = {}
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) and not impossible:
            for c in range(K):
                room_name = None
                for r in range(R):
                    if solver.BooleanValue(a[c][r]):
                        room_name = self.params.rooms[r]
                        break
                if room_name is None:
                    room_name = self.params.rooms[c % R] if R > 0 else None
                assign[c] = room_name

        elif status == cp_model.INFEASIBLE or impossible:
            self.feedback["room_notes"].append(
                f"{DAYS[d]}{w}: Raumkonstanz der Ausschuss-/Themencluster nicht erfüllbar; "
                "ersatzweise einfache Raumzuweisung. Prüfen Sie Räume oder Ausschussbesetzung.")
            cluster_fixed_room = {}
            for s in local_slots:
                used_rooms = set()
                c_order = sorted(slot_clusters[s])
                for c in c_order:
                    r_choice = cluster_fixed_room.get(c, None)
                    if r_choice is not None and r_choice < R and r_choice not in used_rooms:
                        used_rooms.add(r_choice)
                        continue
                    chosen = None
                    for r in range(R):
                        if r not in used_rooms:
                            chosen = r
                            break
                    if chosen is not None:
                        used_rooms.add(chosen)
                        cluster_fixed_room[c] = chosen
                    else:
                        cluster_fixed_room.setdefault(c, None)
            for c in range(K):
                r_idx = cluster_fixed_room.get(c, None)
                assign[c] = self.params.rooms[r_idx] if r_idx is not None and r_idx < R else None
        else:
            self.feedback["room_notes"].append(
                f"{DAYS[d]}{w}: Raumvergabe mit Status {status_to_str(status)}, keine gültige Raumlösung. "
                + ("Erhöhen Sie die Raum-Rechenzeit; Unlösbarkeit ist nicht nachgewiesen."
                   if status == cp_model.UNKNOWN else "Prüfen Sie das Raummodell: " + model.Validate()))
            for c in range(K):
                # UNKNOWN/MODEL_INVALID haben keine auswertbaren Variablenwerte.
                assign[c] = None

        exam_to_room: Dict[int, Optional[str]] = {}
        for (e, _) in day_exams:
            cid = None
            for cc, members in enumerate(clusters):
                if e.idx in members:
                    cid = cc
                    break
            exam_to_room[e.idx] = assign.get(cid, None)

        used_by_slot_room: Dict[Tuple[int, str], int] = {}
        for (e, s_local) in day_exams:
            room = exam_to_room.get(e.idx)
            if room is None:
                continue
            key = (s_local, room)
            if key in used_by_slot_room:
                exam_to_room[e.idx] = None
            else:
                used_by_slot_room[key] = e.idx
        return exam_to_room

    def extract_schedule(self, solver: cp_model.CpSolver) -> List[Dict]:
        e_to_gslot = {}
        for e in self.exams:
            gs_found = None
            for gslot, (w, d, s) in enumerate(self.all_slots):
                if solver.BooleanValue(self.x[(e.idx, gslot)]):
                    gs_found = gslot
                    break
            e_to_gslot[e.idx] = gs_found

        per_day: Dict[Tuple[int, int], List[Tuple[Exam, int]]] = defaultdict(list)
        for e in self.exams:
            gslot = e_to_gslot[e.idx]
            if gslot is None:
                continue
            w, d, s = self.all_slots[gslot]
            per_day[(w, d)].append((e, s))

        e_to_room = {}
        for (w, d), lst in per_day.items():
            if not lst:
                continue
            day_mapping = self.assign_rooms_for_day_mip(lst, w, d)
            e_to_room.update(day_mapping)

        schedule = []
        for e in self.exams:
            gslot = e_to_gslot[e.idx]
            if gslot is None:
                schedule.append({
                    "ExamIdx": e.idx, "Schueler": e.schueler, "Fach": e.fach, "Thema": e.thema,
                    "Pruefer": e.pruefer, "Beisitzer": e.beisitzer, "Woche": None, "Tag": None,
                    "SlotIndex": None, "Uhrzeit": None, "Raum": None
                })
            else:
                w, d, s = self.all_slots[gslot]
                schedule.append({
                    "ExamIdx": e.idx, "Schueler": e.schueler, "Fach": e.fach, "Thema": e.thema,
                    "Pruefer": e.pruefer, "Beisitzer": e.beisitzer, "Woche": w, "Tag": DAYS[d],
                    "SlotIndex": s, "Uhrzeit": pretty_time_for_slot(self.params, w, d, s),
                    "Raum": e_to_room.get(e.idx)
                })
        parked = [row for row in schedule if not row.get("Raum")]
        if parked:
            self.feedback["room_notes"].append(
                f"{len(parked)} Prüfungen ohne Raum, im Parkplatz: "
                + "; ".join(f"#{row['ExamIdx']} {row['Schueler']} ({row['Fach']})" for row in parked)
                + ". Prüfen Sie die Raumzuweisung.")
        # Tatsächlich erzielte Raumlücken nennen, nicht pauschal Kompaktheit behaupten.
        room_slots = defaultdict(list)
        for row in schedule:
            if row.get("Raum"):
                room_slots[(row["Woche"], row["Tag"], row["Raum"])].append(row["SlotIndex"])
        for (week, day, room), slots in sorted(room_slots.items()):
            gaps = max(slots) - min(slots) + 1 - len(set(slots))
            if gaps:
                self.feedback["room_notes"].append(f"Raum {room}, {day}{week}: {gaps} unbelegte Slots "
                                                   "zwischen Prüfungen.")
        if self.log_detailed_feedback and self.feedback["room_notes"]:
            vprint(format_feedback(self.feedback))
        return schedule

def prompt_yes_no(msg: str) -> bool:
    while True:
        s = input(msg + " (j/n): ").strip().lower()
        if s in ("j", "ja", "y", "yes"):
            return True
        if s in ("n", "nein", "no"):
            return False
        print("Bitte 'j' oder 'n' eingeben.")

def prompt_int(msg: str, min_v: Optional[int] = None, max_v: Optional[int] = None) -> int:
    while True:
        try:
            v = int(input(msg + ": ").strip())
            if min_v is not None and v < min_v:
                print(f"Bitte Zahl >= {min_v}")
                continue
            if max_v is not None and v > max_v:
                print(f"Bitte Zahl <= {max_v}")
                continue
            return v
        except Exception:
            print("Bitte eine Ganzzahl eingeben.")

def prompt_list(msg: str) -> List[str]:
    s = input(msg + " (durch Komma getrennt, leer für keine): ").strip()
    if not s:
        return []
    return [t.strip() for t in s.split(",") if t.strip()]

def collect_schedule_params() -> ScheduleParams:
    rooms = prompt_list("Raumnummern eingeben")
    if not rooms:
        print("Hinweis: Keine Räume angegeben, es wird ein Standardraum 'R1' verwendet.")
        rooms = ["R1"]

    print("Einheitliche Tagesstruktur (gilt für alle Tage):")
    n_slots = prompt_int("Anzahl Zeitslots pro Tag", min_v=0, max_v=50)
    start_time = input("Startzeit (z.B. 08:00): ").strip() or "08:00"
    slot_len = prompt_int("Slotlänge in Minuten", min_v=1, max_v=600)
    break_len = prompt_int("Pausenlänge in Minuten", min_v=0, max_v=600)

    slots_per_day = {}
    timing_per_day = {}
    for w in WEEKS:
        for d_idx in range(5):
            slots_per_day[(w, d_idx)] = n_slots
            timing_per_day[(w, d_idx)] = (start_time, slot_len, break_len)
    return ScheduleParams(rooms=rooms, slots_per_day=slots_per_day, timing_per_day=timing_per_day)

def collect_constraints() -> Tuple[ConstraintsConfig, Dict[str, Set[Tuple[int, int]]], Set[Tuple[int, int]]]:
    hard_student_one_per_week = prompt_yes_no("Harte Bedingung: Pro Schüler pro Woche genau eine Prüfung aktivieren?")
    hard_grouping_enabled = prompt_yes_no("Harte Bedingung: Kopplung gleicher (Thema, Fach, Prüfer) aktivieren?")
    grouping_block_size = None
    if hard_grouping_enabled:
        grouping_block_size = prompt_int("Blockgröße N (2-5)", min_v=2, max_v=5)

    hard_unavailability = prompt_yes_no("Harte Bedingung: Abwesenheitstage für Prüfer/Beisitzer beachten?")
    unavailability = defaultdict(set)
    if hard_unavailability:
        print("Abwesenheitstage pro Person (Format: Name: Mo1, Di2, ...). Leerzeile beendet.")
        while True:
            line = input("Eintrag (oder leer): ").strip()
            if not line:
                break
            if ":" not in line:
                print("Format: Name: Mo1, Di2, ...")
                continue
            name, tokens = line.split(":", 1)
            name = name.strip()
            days_tokens = [t.strip() for t in tokens.split(",") if t.strip()]
            for t in days_tokens:
                w, d = parse_day_token(t)
                unavailability[name].add((w, d))

    hard_min_gap_days_same_student = None
    if prompt_yes_no("Harte Bedingung: Minimaler Abstand a (Tage) für Prüfungen desselben Schülers?"):
        hard_min_gap_days_same_student = prompt_int("a (in Tagen)", min_v=0, max_v=10)

    hard_no_exam_days_enabled = prompt_yes_no("Harte Bedingung: Bestimmte Tage komplett ohne Prüfungen?")
    no_exam_days = set()
    if hard_no_exam_days_enabled:
        day_tokens = prompt_list("Tage (z.B. Mo1, Di2)")
        for t in day_tokens:
            w, d = parse_day_token(t)
            no_exam_days.add((w, d))
        if no_exam_days:
            human = ", ".join(f"{DAYS[d]}{w}" for (w, d) in sorted(no_exam_days))
            print(f"AUSGESCHLOSSENE TAGE: {human}")

    hard_max_days_per_teacher_enabled = prompt_yes_no("Harte Bedingung: Maximal K Tage pro Prüfer?")
    hard_max_days_per_teacher_K = None
    if hard_max_days_per_teacher_enabled:
        hard_max_days_per_teacher_K = prompt_int("K (max Tage pro Prüfer)", min_v=1, max_v=10)

    soft_desired_gap_days_same_student = None
    if prompt_yes_no("Weiche Bedingung: Gewünschter Abstand d (Tage) für Prüfungen desselben Schülers?"):
        soft_desired_gap_days_same_student = prompt_int("d (in Tagen)", min_v=0, max_v=10)

    soft_minimize_rooms_used = prompt_yes_no("Weiche Bedingung: Minimale Zahl an genutzten Räumen?")

    allow5 = set(prompt_list("Prüfer, die bis zu 5 Prüfungen am Tag machen (durch Komma getrennt, leer für keine)"))
    default_max_per_day = 4
    try:
        default_max_per_day = prompt_int("Max. Prüfungen/Tag für alle übrigen Prüfer (Standard 4):", min_v=1, max_v=10)
    except Exception:
        default_max_per_day = 4

    soft_prefer_second_slot_start = prompt_yes_no("Weiche Bedingung: Prüfer-Tagesblöcke sollen idealerweise im 2. Slot beginnen?")
    weight_prefer_second_slot = 5
    if soft_prefer_second_slot_start:
        try:
            weight_prefer_second_slot = prompt_int("Gewicht für 'Start im 2. Slot' (z.B. 1..100):", min_v=1, max_v=100)*SECOND_SLOT_WEIGHT
        except Exception:
            weight_prefer_second_slot = 5

    try:
        ignore_empty_beisitzer = prompt_yes_no("Leere Beisitzer (\"\") ignorieren (empfohlen)?")
    except Exception:
        ignore_empty_beisitzer = True

    cfg = ConstraintsConfig(
        hard_student_one_per_week=hard_student_one_per_week,
        hard_grouping_enabled=hard_grouping_enabled,
        grouping_block_size=grouping_block_size,
        hard_unavailability=hard_unavailability,
        hard_min_gap_days_same_student=hard_min_gap_days_same_student,
        hard_no_exam_days_enabled=hard_no_exam_days_enabled,
        hard_max_days_per_teacher_enabled=hard_max_days_per_teacher_enabled,
        hard_max_days_per_teacher_K=hard_max_days_per_teacher_K,
        soft_desired_gap_days_same_student=soft_desired_gap_days_same_student,
        soft_minimize_rooms_used=soft_minimize_rooms_used,
        teachers_allow_5_per_day=allow5,
        default_max_per_day=default_max_per_day,
        soft_prefer_second_slot_start=soft_prefer_second_slot_start,
        weight_prefer_second_slot=weight_prefer_second_slot,
        ignore_empty_beisitzer=ignore_empty_beisitzer,
    )
    return cfg, unavailability, no_exam_days

def main():
    print("CSP-Solver: Slots (hart) + Tages-Raumoptimierung (hart kapazitätsbegrenzt, ohne Doppelbelegung) + Permutationsschutz + Block-/Limitregeln")
    if len(sys.argv) < 2:
        print("Aufruf: python kolloquium_solver.py <pruefungen.csv>")
        print("CSV-Header: Schueler;Fach;Thema;Pruefer;Beisitzer")
        sys.exit(1)

    csv_path = sys.argv[1]
    exams = read_exams_from_csv(csv_path)
    print(f"{len(exams)} Prüfungen geladen.")

    params = collect_schedule_params()
    cfg, unavailability, no_exam_days = collect_constraints()

    scheduler = ColloquiumScheduler(exams, params, cfg, unavailability, no_exam_days)
    scheduler.add_basic_constraints()
    scheduler.add_hard_constraints()
    scheduler.add_soft_constraints()

    time_limit = prompt_int("Zeitlimit für Slot-Solver in Sekunden", min_v=1, max_v=7200)
    solver, status = scheduler.solve(time_limit_sec=time_limit)

    status_de_map = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "ZULÄSSIG",
        cp_model.INFEASIBLE: "UNZULÄSSIG",
        cp_model.MODEL_INVALID: "MODELL UNGÜLTIG",
        cp_model.UNKNOWN: "UNBEKANNT",
    }
    print(f"Lösungsstatus (Slots): {status_de_map.get(status, str(status))}")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = scheduler.extract_schedule(solver)
        out_df = pd.DataFrame(schedule)
        out_file = "kolloquiumsplan.csv"

        tag_cat = pd.CategoricalDtype(categories=DAYS, ordered=True)
        if "Tag" in out_df.columns:
            out_df["Tag"] = out_df["Tag"].astype(tag_cat)

        def time_to_minutes(t):
            if pd.isna(t) or t is None or t == "":
                return None
            try:
                h, m = str(t).split(":")
                return int(h) * 60 + int(m)
            except Exception:
                return None
        out_df["UhrzeitMin"] = out_df["Uhrzeit"].apply(time_to_minutes)

        out_df.sort_values(
            by=["Woche", "Tag", "Raum", "UhrzeitMin"],
            inplace=True,
            na_position="last"
        )
        out_df.drop(columns=["UhrzeitMin"], inplace=True)

        out_df.to_csv(out_file, index=False, sep=";")
        print(f"Plan exportiert nach: {out_file}")
        print("\nGeplanter Kolloquiumsplan (Ausschnitt):")
        print(out_df.head(40).to_string(index=False))

        # -- BEGIN EXPORT SNIPPET (JSON-Übergabe an export.py) --
        export_columns = ["ID", "Schueler", "Fach", "Thema", "Pruefer", "Beisitzer", "Woche", "Tag", "Uhrzeit", "Raum"]

        col_map = {
            "ExamIdx": "ID",
            "Schueler": "Schueler",
            "Fach": "Fach",
            "Thema": "Thema",
            "Pruefer": "Pruefer",
            "Beisitzer": "Beisitzer",
            "Woche": "Woche",
            "Tag": "Tag",
            "Uhrzeit": "Uhrzeit",
            "Raum": "Raum",
        }

        export_df = out_df.rename(columns=col_map)
        export_df = export_df[[c for c in export_columns if c in export_df.columns]].copy()
        export_df.to_json("kolloquiumsplan.json", orient="records", force_ascii=False)

        import json
        slot_times = {}

        for w in WEEKS:
            for d_idx, tagstr in enumerate(DAYS):
                n_slots = params.slots_per_day.get((w, d_idx), 0)
                if n_slots <= 0:
                    continue
                start_str, slot_min, break_min = params.timing_per_day[(w, d_idx)]
                try:
                    hh, mm = [int(x) for x in start_str.strip().split(":")]
                except Exception:
                    hh, mm = 8, 0
                base_min = hh * 60 + mm
                labels = []
                for s in range(n_slots):
                    begin_min = base_min + s * (slot_min + break_min)
                    end_min = begin_min + slot_min
                    begin_str = f"{begin_min // 60:02d}:{begin_min % 60:02d}"
                    end_str = f"{end_min // 60:02d}:{end_min % 60:02d}"
                    labels.append(f"{begin_str} - {end_str}")
                slot_times[f"{w}-{tagstr}"] = labels

        with open("slot_times.json", "w", encoding="utf-8") as f:
            json.dump(slot_times, f, ensure_ascii=False, indent=2)

        print("JSON für export.py geschrieben: kolloquiumsplan.json, slot_times.json")

        try:
            import subprocess
            subprocess.run([sys.executable, "export.py", "kolloquiumsplan.json", "slot_times.json", "kolloquiumsplan.docx"], check=True)
            print("Kolloquiumsplan als Word erstellt: kolloquiumsplan.docx")
        except Exception as e:
            print(f"Hinweis: export.py konnte nicht automatisch gestartet werden: {e}")
        try:
            import subprocess
            subprocess.run([sys.executable, "report.py", "kolloquiumsplan.json"], check=True)
            print("Report zum Plan erstellt: kolloquiumsplan_report.docx")
        except Exception as e:
            print(f"Hinweis: report.py konnte nicht automatisch gestartet werden: {e}")
        # -- END EXPORT SNIPPET --
    else:
        print("Kein gültiger Zeitplan. Prüfen Sie die genannten Engstellen und Bedingungen.")

if __name__ == "__main__":
    main()
