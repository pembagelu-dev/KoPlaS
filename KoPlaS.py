Version = "1.2.8 (Build 14.49.39)"
"""
----------
ChangeLog
----------

Version 1.2.8
Summenzeile im TeachersDialog bündig ausgerichtet, Summenwerte zentriert und Lehrkraft-/UPZ-Zellen zu „Summe“ verbunden
Erfolgreiche Lehrkräfte- und Kursimporte markieren den Plan als geändert und lösen beim Beenden die Speicherabfrage aus
Report: Unbenutzte Ausrichtungsfunktion und Imports entfernt; CLI-Report gibt den Quelldateinamen aus, GUI-Report keinen Platzhalter
ASV-Import: Unbenutzte Werte entfernt, CSV-Helfer aus Zeilenschleifen gezogen und Zahlenkonvertierung gezielter abgesichert

Version 1.2.7
Drei Exportvarianten für Plan (LK, SuS, Reinigungspersonal), Auswahldialog
Fehlerbehebungen: Belastungswert im Report nur bei geplanten LK

Version 1.2.6
Änderungen an Zeit, Räume und Bedingungen führen zu Speichern bei Schließen
Suchfunktion implementiert (Strg + F bzw. Cmd + F) Schüler, Prüfer, Beisitzer, Thema

Version 1.2.5
Absperrung bei mehr als zwei Themen-Kopplungen hinzugefügt. Raum für Aufsicht ist der Vorbereitungsraum. NTA wird berücksichtigt, falls dadurch Absperrung verkürzt werden kann.
Belastungsparameter nun vom Nutzer definierbar und persistent gespeichert
Export: Auch Thema in Exceltabelle und Spalten auswählbar

Version 1.2.4
Faire Tagesverteilung der Schülerslots pro Schüler jetzt berechnet
WS und Prüfer änderbar, wird persistent gespeichert
Dialogbreiten jetzt dynamisch und OS unabhängig
Schriftgröße Block und Blockhöhe jetzt OS abhängig und angepasst (etwas größer)

Version 1.2.3
Mehr als 3er Koppel möglich (maximal 5)
Konflikte werden nach Öffnen einer Datei markiert
Prüfungen pro Tag werden gezählt und in Statusleiste ausgegeben
Raumänderung via Kontextmenü (Ändern, Löschen, Hinzufügen (rechts davon))

Version 1.2.2
Erweiterung des Reports um die Lehrerdaten zu den Prüfungen
Defaultwerte der Einstellungen angepasst
Mehr Infos im Log
Dateiname der aktuell geladenen Datei in der Statuszeile rechts
Prüfungen im Parkplatz werden dort nun ohne Slotdaten (Woche, Tag, Slot, Uhrzeit) abgelegt. Verhindert sauber falsche Berechnungen beim Drop
Summenzeile im TeachersDialog ergänzt
Speichern unter hinzugefügt

Version 1.2
PySide6 Sprachdatei Deutsch verwendet
Von Systemdialogen auf PySide6 native Dialoge umgestellt

Version 1.1
Import der Lehrkräfte mit UPZ möglich. Normalisierung der LK auf Kürzel
Import Oberstufenkurse mit WS, S, K Zahlen für Belastungsrechnung
Export des importierten Schulnamens in den Plan
Vorbereitungsraum hinzugefügt
Sortierung im Export nach Raum und Zeit (time_info erhält auch die Raumliste in exakter Reihenfolge)
Räume mit Prüfungen können nicht gelöscht werden
Teachers Dialog S2 (editierbar) und K2 (automatische Zählung aus dc.exams, leerer String, wenn nicht Beisitzer)
Prüfungsbelastung jetzt berechnet und automatisch aktualisiert
Bei Änderungen wird Speichern erfragt (Beenden, Öffnen)
kleinere Anpassungen (Fensterbreiten)
Belastungswerte sind farblich hervorgehoben
Funktion Aufsichten entfernt
Menüanpassungen (Export als Kaskade mit neuen Optionen), Sortierung in Datei anders

Version 1.0
GUI für Nutzung auch außerhalb des Terminals
Leerer Beisitzer auch per Bedingung steuerbar
Parkplatzraum für durch MIP nicht zugewiesene Prüfungen
Besseres DnD beim Parkplatz V3
Beisitzer Aktualisierung wird geprüft, Verschiebung auch in verbotenen Bereiche (dann farbiges Highlight mit stetiger Neuberechnung bei Änderungen) außer bei belegtem Slot (sonst Überlappung von Blöcken)
Konsistente Prüfung von Bedingungen bei Verschiebung und Veränderungen an Daten
Slot 2 jetzt gelb (soft speziell)
Parkplatz einspaltig (Breite wie Right Model)
Rechts Klick-Menü für Blöcke (erweitern um Prüfer als Beisitzer und Beisitzer als Prüfer sowie Beisitzer ändern)
Anpassung Exportfunktion
NTA jetzt möglich
Undo/Redo Fähigkeit für maximal 10 Schritte in der Slotplanung (nicht Bedingungen und nicht Zeit/Raumstruktur)
Parkplatz View jetzt feste Breite wie Blöcke

Version 0.1
CP-SAT Planer mit CLI Argumenten ohne GUI
Prüfungen verschiebbar
Export als Worddatei

----------
Bugfix
----------
Redaktionelle Korrekturen in ChangeLog und Bugfix-Notizen
Checkbox aktiviert soft_gap Spinbox nicht
Leere Beisitzer führen zu Parallelitätskonflikt
Ad Hoc Check bei DnD für maximale Zahl an Prüfungen pro Tag jetzt auch an Checkbox geknüpft
Tippfehler bei ignore_empty_beisitzer
Trenner zwischen Tagen (wieder) eingefügt
max_per_day wurde hart geprüft (vgl. max_dyas_per_teacher)
Beginn Slot 1 jetzt keine Verletzung mehr (auch rollenübergreifend)
Maximale Tage pro Prüfer jetzt personenspezifisch (zuvor über alle Personen gesammelt)
Highlight Violett auch im Parkplatz (OK)
Kopplungsblöcke konnten ohne Markierung rot getrennt werden (OK)
Syntax-Bugs entfernt
Statusmeldungen in Statusleiste (OK), Meldungen angepasst
Redo/Undo nicht für ExamsDialog (OK) und nicht für Parkplatz (OK)
Umlautfehler behoben, neues, einheitliches Importfenster (Öffnen des Dialogs nach Import)
LK Import überschreibt Kursimport, behoben
mehrfacher Kursimport verdoppelt die Zahlen WS, S und K, behoben
Speichern bei Beenden wird trotz Ja nicht durchgeführt
Änderung von S2 berechnet Belastung nicht neu (OK)
Tagesabstände waren in der GUI noch ohne Wochenende (im Planer bereits korrekt)
Klammer entfernt im Constraints Dialog
Kontextmenü bleibt hängen (OK)
Warnung über veraltete PySide6 Aufrufe entfernt
Header Kontextmenü für Räume öffnet nun sauber
Undo/Redo auf alle relevanten Aktionen ausgeweitet (bisher teilweise fehlerhaft)
Konsistente Fehlermeldung in der Statuszeile bei falschem Import
Versteckte ID Spalte im ExamsDialog wird jetzt auch in die Breite einbezogen
Anpassung der Dialogbreiten auf OS Spezifikationen
QDialog im DataController nicht parent sondern None
Uhrzeit nicht mehr gesetzt sondern live aus TimeSettings berechnet"
"""

"""
Aus App-Bundle ein DMG erstellen (icns Icon sowie settings.py im selben Verzeichnis \dist)
dmgbuild -s settings.py "KoPlaS" KoPlaS.dmg
"""

import sys
import os
import json
import traceback
import threading
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Set, Any
from datetime import datetime, timedelta

from PySide6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex, QSize, Signal, QObject, QMimeData, QByteArray,
    QThread, QEvent, QTimer
)
from PySide6.QtGui import (
    QKeySequence, QAction, QFont, QColor, QPainter, QStandardItemModel, QStandardItem, QGuiApplication, QCursor
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QTimeEdit, QDateEdit, QFormLayout, QCheckBox, QPlainTextEdit, QStatusBar, QMenuBar,
    QSplitter, QStyledItemDelegate, QStyleOptionViewItem, QHeaderView, QPushButton, QMenu, QTextEdit, QInputDialog
)

import re

# Import der vorhandenen Module (im selben Verzeichnis)
import kolloPlaner as K  # Solver-Logik (mit LOG_CALLBACK & VERBOSE)
import export as EXP     # Export-DOCX
import report as REP     # Statistik-Report

# -------------------------
# Hilfs-Konstanten
# -------------------------
DAYS = ["Mo", "Di", "Mi", "Do", "Fr"]
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}
WEEKS = [1, 2]

# Farben (inkl. erlaubte Ziele)
COLOR_HARD_FORBIDDEN = QColor(255, 200, 200)  # hellrot
COLOR_SOFT_WARN = QColor(255, 230, 200)       # hellorange
COLOR_ALLOWED = QColor(220, 255, 220)         # hellgrün
COLOR_NORMAL = QColor(255, 255, 255)
COLOR_SOFT_SECOND_SLOT = QColor(255, 255, 200)  # hellgelb für "Start im 2. Slot"
COLOR_HIGHLIGHT_VIOLET = QColor(230, 220, 255)  # temporäre Hervorhebung (hell-violett)
COLOR_FAIR_DISTRIBUTION = QColor(210, 235, 255)  # hellblau für späte Doppelprüfungen (faire Tagesverteilung)

# Zeitkonstanten der Solver (CP und MIP)
MAX_CP_TIME_LIMIT = 500000
MAX_MIP_TIME_LIMIT = 70000

# Betriebssystemabhängige Parameter: Schriftgröße und Prüfungsblockgröße für Blocktexte:
# - macOS: Arial 11
# - Windows: Arial 10
# - Sonst (Linux/unknown): Arial 9 (Fallback)
try:
    import platform
    _sys = (platform.system() or "").lower()
    if "darwin" in _sys or _sys == "mac" or _sys == "macos":
        FONT_DEFAULT = QFont("Arial", 14)
        FONT_BLOCK = QFont("Arial", 11)
        BLOCK_HEIGHT_MAX = 50
        BLOCK_HEIGHT_MIN = 24
        EXTRA_WIDTH_EXAMS_DIALOG = 33
        EXTRA_WIDTH_TEACHERS_DIALOG = 24
    elif "windows" in _sys:
        FONT_DEFAULT = QFont("Arial", 10)
        FONT_BLOCK = QFont("Arial", 9)
        BLOCK_HEIGHT_MAX = 65
        BLOCK_HEIGHT_MIN = 24
        EXTRA_WIDTH_EXAMS_DIALOG = 46
        EXTRA_WIDTH_TEACHERS_DIALOG = 16
    else:
        FONT_DEFAULT = QFont("Arial", 14)
        FONT_BLOCK = QFont("Arial", 9)
        BLOCK_HEIGHT_MAX = 50
        BLOCK_HEIGHT_MIN = 24
        EXTRA_WIDTH_EXAMS_DIALOG = 33
        EXTRA_WIDTH_TEACHERS_DIALOG = 24
except Exception:
    # Fallback, falls platform nicht verfügbar ist o.ä.
    FONT_DEFAULT = QFont("Arial", 10)
    FONT_BLOCK = QFont("Arial", 9)
    BLOCK_HEIGHT_MAX = 50
    BLOCK_HEIGHT_MIN = 24
    EXTRA_WIDTH_EXAMS_DIALOG = 33
    EXTRA_WIDTH_TEACHERS_DIALOG = 24

#Undo/Redo Stacklänge
MAX_UNDO = 10       #maximal 10 Einträge in der Historie

# -------------------------
# Belastungs-Kalkulation
# -------------------------
# Formel:
# Belastung = (KORREKTUR_SCHRIFTLICH_MINUTEN*S
#              + KORREKTUR_SCHRIFTLICH_MINUTEN*FAKTOR_NACHKORREKTUR*S2
#              + KOLLOQUIUM_PRUEFER_ZEIT*K
#              + KOLLOQUIUM_PRUEFER_ZEIT*FAKTOR_BEISITZER*K2
#              - UNTERRICHT_AUFWAND*WS) / UPZ

# Arbeitsordner
def ensure_work_dir():
    base = os.path.dirname(os.path.abspath(K.__file__))  # neben kolloPlaner.py
    work = os.path.join(base, "Kolloquiumsplan")
    os.makedirs(work, exist_ok=True)
    return work

WORK_DIR = ensure_work_dir()

# -------------------------
# Datenklassen
# -------------------------
@dataclass
class Exam:
    idx: int
    Schueler: str
    Fach: str
    Thema: str
    Pruefer: str
    Beisitzer: str
    NTA: Optional[int] = 0

@dataclass
class TimeSettings:
    n_slots: int = 0
    start_time: str = "12:00"
    slot_len_min: int = 30
    break_len_min: int = 30
    week1_date: Optional[str] = "2026-05-18"  # "YYYY-MM-DD"
    week2_date: Optional[str] = "2026-06-08"

@dataclass
class ConstraintsSettings:
    # Harte
    hard_student_one_per_week: bool = False
    hard_grouping_enabled: bool = False
    grouping_block_size: Optional[int] = None
    hard_unavailability: bool = False
    unavailability: Dict[str, List[str]] = field(default_factory=dict)  # "Name: ['Mo1','Di2']"
    hard_min_gap_days_same_student: Optional[int] = None
    hard_no_exam_days_enabled: bool = False
    no_exam_days: List[str] = field(default_factory=list)  # ["Mo1","Di2"]
    hard_max_days_per_teacher_enabled: bool = False
    hard_max_days_per_teacher_K: Optional[int] = None
    # Soft
    soft_desired_gap_days_same_student: Optional[int] = None
    soft_minimize_rooms_used: bool = False
    teachers_allow_5_per_day: List[str] = field(default_factory=list)
    default_max_per_day: int = 4
    soft_prefer_second_slot_start: bool = False
    weight_prefer_second_slot: int = 100  # Multiplikator wird im Solver mit SECOND_SLOT_WEIGHT kombiniert

    # Solver-Limits und Gewichte (variabel)
    cp_time_limit_sec: int = 3600
    mip_room_time_limit_sec: int = 480
    MIP_ROOM_GAP_WEIGHT: int = 2000
    GAP_WEIGHT_INNER: int = 4000
    GAP_WEIGHT_OUTER: int = 2000
    SPAN_WEIGHT: int = 200
    SECOND_SLOT_WEIGHT: int = 9000
    DAY_WEIGHT_BALANCE: int = 9000
    # Neues Verhalten: leere Beisitzer wie "" ignorieren
    ignore_empty_beisitzer: bool = True    
    # Faire Tagesverteilung: beide Prfungen eines Schlers liegen spter am Tag
    fair_day_distribution_enabled: bool = False
    fair_day_distribution_slotsum: int = 4  # Schwelle (strict >), Range 4..6 per UI

@dataclass
class AppSettings:
    rooms: List[str] = field(default_factory=lambda: [""])
    prepare_room: str = ""  # zusätzlicher Vorbereitungsraum
    time: TimeSettings = field(default_factory=TimeSettings)
    constraints: ConstraintsSettings = field(default_factory=ConstraintsSettings)
    # Neue, persistente Belastungsparameter (Defaultwerte wie zuvor als Konstanten)
    workload_korrektur_min: int = 80           # KORREKTUR_SCHRIFTLICH_MINUTEN
    workload_faktor_nachkorrektur: float = 0.5 # FAKTOR_NACHKORREKTUR
    workload_kolloq_pruefer_min: int = 90      # KOLLOQUIUM_PRUEFER_ZEIT
    workload_faktor_beisitzer: float = 0.5     # FAKTOR_BEISITZER
    workload_unterricht_aufwand_min: int = 990 # UNTERRICHT_AUFWAND
    students_note_text: str = ""


@dataclass
class ScheduleItem:
    ExamIdx: int
    Schueler: str
    Fach: str
    Thema: str
    Pruefer: str
    Beisitzer: str
    Woche: Optional[int]
    Tag: Optional[str]  # "Mo".."Fr"
    SlotIndex: Optional[int]
    Raum: Optional[str]

@dataclass
class Teacher:
    Lehrkraft: str
    UPZ: str = ""
    WS: str = ""
    S: str = ""
    S2: str = ""
    K: str = ""
    K2: str = ""
    Belastung: str = ""

# -------------------------
# Undo/Redo - Commands (minimal-differentiell)
# -------------------------
class BaseCommand:
    def apply(self, dc: "DataController"):
        raise NotImplementedError
    def revert(self, dc: "DataController"):
        raise NotImplementedError
    def label(self) -> str:
        return "Änderung"

class ChangeRoomCommand(BaseCommand):
    """
    Undo/Redo-Kommando für eine Raum-Umbenennung:
    - Ersetzt in dc.settings.rooms den alten durch den neuen Namen
    - Aktualisiert alle ScheduleItem.Raum von old_room -> new_room
    """
    def __init__(self, old_room: str, new_room: str):
        self.old_room = old_room
        self.new_room = new_room
    def _apply(self, dc: "DataController", src: str, dst: str):
        # settings.rooms ersetzen
        rooms = list(dc.settings.rooms or [])
        dc.settings.rooms = [dst if r == src else r for r in rooms]
        # schedule anpassen
        for it in dc.schedule or []:
            if (it.Raum or "").strip() == src:
                it.Raum = dst
        # Konflikte neu bewerten und UI refresh signalisieren
        try:
            dc.evaluate_conflicts()
        except Exception:
            pass
        dc.dataChanged.emit()
        dc.uiRefreshRequested.emit()
        # Dirty-Flag
        dc._dirty = True
    def apply(self, dc: "DataController"):
        self._apply(dc, self.old_room, self.new_room)
    def revert(self, dc: "DataController"):
        self._apply(dc, self.new_room, self.old_room)
    def label(self) -> str:
        return f"Raum umbenannt: {self.old_room} \u2192 {self.new_room}"

class AddRoomCommand(BaseCommand):
    """
    Fuegt einen neuen Raum an gegebener Position in settings.rooms ein.
    Vorbereitungsraum wird nicht beruehrt.
    """
    def __init__(self, room_name: str, insert_pos: int):
        self.room_name = room_name
        self.insert_pos = insert_pos
    def apply(self, dc: "DataController"):
        rooms = list(dc.settings.rooms or [])
        # Schutz: nicht doppelt einfuegen
        if self.room_name not in rooms:
            pos = max(0, min(self.insert_pos, len(rooms)))
            rooms.insert(pos, self.room_name)
            dc.settings.rooms = rooms
            dc.dataChanged.emit()
            dc.uiRefreshRequested.emit()
            dc._dirty = True
    def revert(self, dc: "DataController"):
        rooms = list(dc.settings.rooms or [])
        if self.room_name in rooms:
            rooms.remove(self.room_name)
            dc.settings.rooms = rooms
            dc.dataChanged.emit()
            dc.uiRefreshRequested.emit()
            dc._dirty = True
    def label(self) -> str:
        return f"Raum hinzugefügt: {self.room_name}"

class DeleteRoomCommand(BaseCommand):
    """
    Entfernt einen Raum aus settings.rooms.
    Da on_rightview_header_context_menu bereits sicherstellt, dass keine
    Belegungen mehr existieren, sind keine Schedule-Anpassungen ntig.
    """
    def __init__(self, room_name: str, previous_index: int):
        self.room_name = room_name
        self.previous_index = previous_index
    def apply(self, dc: "DataController"):
        rooms = list(dc.settings.rooms or [])
        if self.room_name in rooms:
            rooms.remove(self.room_name)
            dc.settings.rooms = rooms
            dc.dataChanged.emit()
            dc.uiRefreshRequested.emit()
            dc._dirty = True
    def revert(self, dc: "DataController"):
        rooms = list(dc.settings.rooms or [])
        if self.room_name not in rooms:
            pos = max(0, min(self.previous_index, len(rooms)))
            rooms.insert(pos, self.room_name)
            dc.settings.rooms = rooms
            dc.dataChanged.emit()
            dc.uiRefreshRequested.emit()
            dc._dirty = True
    def label(self) -> str:
        return f"Raum gelöscht: {self.room_name}"

class RoomsListChangeCommand(BaseCommand):
    """
    Ersetzt die komplette Raumliste (ohne Vorbereitungsraum!) als ein Undo-Schritt.
    """
    def __init__(self, before_rooms: List[str], after_rooms: List[str]):
        self.before_rooms = list(before_rooms or [])
        self.after_rooms = list(after_rooms or [])
    def _apply_list(self, dc: "DataController", rooms_new: List[str]):
        dc.settings.rooms = list(rooms_new or [])
        try:
            dc.evaluate_conflicts()
        except Exception:
            pass
        dc.dataChanged.emit()
        dc.uiRefreshRequested.emit()
        dc._dirty = True
    def apply(self, dc: "DataController"):
        self._apply_list(dc, self.after_rooms)
    def revert(self, dc: "DataController"):
        self._apply_list(dc, self.before_rooms)
    def label(self) -> str:
        return "Raumliste geändert"

class EditTeacherFieldCommand(BaseCommand):
    """
    Undo/Redo fuer TeachersDialog-Aenderungen (WS und S2).
    Identifikation per Lehrkraft-Kuerzel (Teacher.Lehrkraft).
    """
    def __init__(self, teacher_code: str, field_name: str, before_val: Any, after_val: Any):
        self.teacher_code = (teacher_code or "").strip()
        self.field_name = field_name  # "WS" | "S2"
        self.before_val = before_val
        self.after_val = after_val
    def _set_field(self, t: Teacher, val: Any):
        if self.field_name == "WS":
            t.WS = str(val) if val is not None else ""
        elif self.field_name == "S2":
            setattr(t, "S2", str(val) if val is not None else "")
    def _apply_to_dc(self, dc: "DataController", val: Any):
        t = dc.get_teacher_for(self.teacher_code)
        if not t:
            # Fallback: lineare Suche (falls Index noch nicht aufgebaut)
            for tt in getattr(dc, "teachers", []) or []:
                if (tt.Lehrkraft or "").strip() == self.teacher_code:
                    t = tt
                    break
        if t:
            self._set_field(t, val)
            # Nachfassen: Belastung neu
            try:
                dc.calculate_belastung()
            except Exception:
                pass
            dc.dataChanged.emit()
            dc._dirty = True
    def apply(self, dc: "DataController"):
        self._apply_to_dc(dc, self.after_val)
    def revert(self, dc: "DataController"):
        self._apply_to_dc(dc, self.before_val)
    def label(self) -> str:
        return f"Lehrkraft {self.teacher_code}: {self.field_name} geändert"

class MoveExamCommand(BaseCommand):
    def __init__(self, exam_idx: int, before: Dict[str, Any], after: Dict[str, Any]):
        self.exam_idx = exam_idx
        self.before = before  # keys: Woche, Tag, SlotIndex, Uhrzeit, Raum
        self.after = after
        
    def _apply_state(self, dc: "DataController", state: Dict[str, Any]):
        for it in dc.schedule:
            if it.ExamIdx == self.exam_idx:
                it.Woche = state.get("Woche")
                it.Tag = state.get("Tag")
                it.SlotIndex = state.get("SlotIndex")
                it.Raum = state.get("Raum")
                # Uhrzeit nicht blind aus state setzen, sondern konsistent neu berechnen:
                # Nur wenn der Block geplant ist (Woche/Tag/SlotIndex gesetzt) -> Uhrzeit berechnen;
                # Parkplatz -> Uhrzeit None
                dc.recompute_item_time(it)
                break
    def apply(self, dc: "DataController"):
        self._apply_state(dc, self.after)
    def revert(self, dc: "DataController"):
        self._apply_state(dc, self.before)
    def label(self) -> str:
        return "Block verschoben"

class EditExamFieldCommand(BaseCommand):
    def __init__(self, exam_idx: int, field_name: str, before_val: Any, after_val: Any):
        self.exam_idx = exam_idx
        self.field_name = field_name  # "Thema" | "Beisitzer" | "NTA"
        self.before_val = before_val
        self.after_val = after_val
    def _set_exam_field(self, ex: Exam, val: Any):
        if self.field_name == "Thema":
            ex.Thema = val
        elif self.field_name == "Pruefer":
            ex.Pruefer = val
        elif self.field_name == "Beisitzer":
            ex.Beisitzer = val
        elif self.field_name == "NTA":
            try:
                ex.NTA = int(val)
            except Exception:
                ex.NTA = 0
    def _mirror_to_schedule(self, dc: "DataController", val: Any):
        # Nur Textspiegelung für Thema/Beisitzer (NTA wird im Export genutzt, nicht im Schedule-Text)
        if self.field_name in ("Thema", "Beisitzer", "Pruefer"):
            for s in dc.schedule:
                if s.ExamIdx == self.exam_idx:
                    setattr(s, self.field_name, val)
    def apply(self, dc: "DataController"):
        ex = next((e for e in dc.exams if e.idx == self.exam_idx), None)
        if ex:
            self._set_exam_field(ex, self.after_val)
            self._mirror_to_schedule(dc, self.after_val)
    def revert(self, dc: "DataController"):
        ex = next((e for e in dc.exams if e.idx == self.exam_idx), None)
        if ex:
            self._set_exam_field(ex, self.before_val)
            self._mirror_to_schedule(dc, self.before_val)
    def label(self) -> str:
        return f"{self.field_name} geändert"

class SearchDialog(QDialog):
    """
    Einfache UND-Suche über fünf Felder (case-insensitive Contains):
    Schüler, Prüfer, Beisitzer, Thema, Fach.
    OK ist nur aktiv, wenn mindestens ein Feld befüllt ist.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Suchen")
        self.setModal(True)
        layout = QVBoxLayout(self)
        # Eingabefelder
        self.le_schueler = QLineEdit(self); self.le_schueler.setPlaceholderText("Schüler")
        self.le_pruefer = QLineEdit(self); self.le_pruefer.setPlaceholderText("Prüfer")
        self.le_beisitzer = QLineEdit(self); self.le_beisitzer.setPlaceholderText("Beisitzer")
        self.le_thema = QLineEdit(self); self.le_thema.setPlaceholderText("Thema")
        layout.addWidget(QLabel("Mindestens ein Feld ausfüllen (UND-Suche über alle befüllten Felder):"))
        layout.addWidget(self.le_schueler)
        layout.addWidget(self.le_pruefer)
        layout.addWidget(self.le_beisitzer)
        layout.addWidget(self.le_thema)
        # Buttons
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("OK", self); self.btn_ok.setEnabled(False)
        self.btn_cancel = QPushButton("Abbrechen", self)
        btns.addStretch(1); btns.addWidget(self.btn_ok); btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        # Logik: OK nur aktiv, wenn mind. eines nicht leer
        for le in (self.le_schueler, self.le_pruefer, self.le_beisitzer, self.le_thema):
            le.textChanged.connect(self._update_ok_enabled)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.resize(360, self.sizeHint().height())

    def _update_ok_enabled(self):
        fields = [self.le_schueler.text(), self.le_pruefer.text(), self.le_beisitzer.text(),
                  self.le_thema.text()]
        self.btn_ok.setEnabled(any((s or "").strip() for s in fields))

    def criteria(self):
        # Liefert ein Dict nur mit befüllten, getrimmten, lower()-Felder
        def norm(s): return (s or "").strip()
        crit = {}
        if norm(self.le_schueler.text()): crit["schueler"] = norm(self.le_schueler.text())
        if norm(self.le_pruefer.text()): crit["pruefer"] = norm(self.le_pruefer.text())
        if norm(self.le_beisitzer.text()): crit["beisitzer"] = norm(self.le_beisitzer.text())
        if norm(self.le_thema.text()): crit["thema"] = norm(self.le_thema.text())
        return crit

def exam_matches_criteria_caseins_contains(ex, criteria: dict) -> bool:
    """
    UND-Suche: Alle befüllten Kriterien müssen als Teilstring (case-insensitive) passen.
    Keine Normalisierung, direkte Contains-Suche auf den jeweiligen Strings.
    Keys: schueler, pruefer, beisitzer, thema, fach
    """
    if not criteria:
        return False
    def contains(field_val, needle):
        return needle.lower() in (field_val or "").lower()
    for key, val in criteria.items():
        if key == "schueler" and not contains(ex.Schueler, val): return False
        if key == "pruefer" and not contains(ex.Pruefer, val): return False
        if key == "beisitzer" and not contains((ex.Beisitzer or ""), val): return False
        if key == "thema" and not contains(ex.Thema, val): return False
    return True

# -------------------------
# Daten-Controller
# -------------------------
class DataController(QObject):
    
    dataChanged = Signal()
    logMessage = Signal(str)
    statusMessage = Signal(str)
    actionStateChanged = Signal()  # neu: signalisiert Änderungen am Undo/Redo-Status
    uiRefreshRequested = Signal()  # neu: fordert UI-Refresh (Buttons/Views) an, z. B. nach Parking-Drops

    def __init__(self):
        super().__init__()
        self.exams: List[Exam] = []
        self.settings = AppSettings()
        # Default für neuen planspezifischen Schülerhinweis und Abwärtskompatibilität
        if not hasattr(self.settings, "students_note_text"):
            self.settings.students_note_text = ""
        self.schedule: List[ScheduleItem] = []
        self.teachers: List[Teacher] = []
        # schneller Index nach Kürzel (Lehrkraft) -> Teacher
        self.teacher_by_code: Dict[str, Teacher] = {}
        # Metadaten
        self.school_name: Optional[str] = None
        self.last_open_path: Optional[str] = None
        self.last_csv_dir: Optional[str] = None
        self.error_log: List[str] = []
        # Änderungs-Tracking: wurde seit dem letzten Laden/Speichern etwas geändert?
        self._dirty: bool = False
        # Log-Drosselung (ohne QTimer)
        self._last_log_emit_ts = 0.0
        self._log_lock = threading.Lock()
        # Permanente Konfliktkarte: ExamIdx -> ("hard"|"soft"|None, [messages])
        self.conflict_map: Dict[int, Tuple[Optional[str], List[str]]] = {}
        # Temporre Karte fr faire Tagesverteilung: ExamIdx -> True, wenn Blau-Markierung gelten soll
        self.fair_day_map: Dict[int, bool] = {}
        # Undo/Redo-Stapel (max 10 Schritte)
        self.undo_stack: List[BaseCommand] = []
        self.redo_stack: List[BaseCommand] = []
        self.max_undo: int = MAX_UNDO        
        # Temporärer Highlight-Zustand (nur Anzeige, wird bei Drop zurückgesetzt)
        # highlight_mode in {"pruefer","beisitzer","schueler","fach"} oder None
        self.highlight_mode: Optional[str] = None
        # highlight_value: z. B. "Müller", "Schmidt", "Meier" oder bei "Fach" der extrahierte Buchstabenteil in lower-case
        self.highlight_value: Optional[str] = None

    # Klasse.DataController: Hilfsmethode zum Markieren von Änderungen an Einstellungen
    def mark_dirty_and_emit(self):
        self._dirty = True
        try:
            self.dataChanged.emit()
        except Exception:
            pass
        try:
            self.uiRefreshRequested.emit()
        except Exception:
            pass
 
    def recompute_item_time(self, it: "ScheduleItem"):
        """
        Setzt it.Uhrzeit anhand der aktuellen TimeSettings neu,
        wenn Woche/Tag/SlotIndex gesetzt sind; sonst None.
        """
        try:
            if it is None:
                return
            if it.Woche is None or it.Tag is None or it.SlotIndex is None:
                it.Uhrzeit = None
                return
            t = self.settings.time
            hh, mm = 8, 0
            try:
                hh, mm = [int(x) for x in (t.start_time or "08:00").split(":")]
            except Exception:
                pass
            begin_min = hh * 60 + mm + int(it.SlotIndex) * (int(t.slot_len_min) + int(t.break_len_min))
            it.Uhrzeit = f"{begin_min//60:02d}:{begin_min%60:02d}"
        except Exception:
            # Fallback: nicht crashen, Uhrzeit lieber None lassen
            try:
                it.Uhrzeit = None
            except Exception:
                pass

    def clear_highlight(self):
        self.highlight_mode, self.highlight_value = None, None
    
    def count_beisitzer(self):
        """
        Zählt für jede Lehrkraft (identifiziert über Teacher.Lehrkraft) die Anzahl
        der Beisitzertätigkeiten über alle dc.exams und schreibt das Ergebnis
        in das Feld K2 der jeweiligen Teacher-Einträge.
        - Zählbasis: ausschließlich dc.exams (Quelle der Wahrheit)
        - Vergleich: ex.Beisitzer (getrimmt) == Teacher.Lehrkraft (getrimmt)
        - Leere Beisitzer werden ignoriert
        """
        # Map von Code -> Zähler
        counts: Dict[str, int] = {}
        # Vorab alle Codes erfassen (trimmen)
        for t in getattr(self, "teachers", []) or []:
            code = (t.Lehrkraft or "").strip()
            if code:
                counts[code] = 0
        # Zählen über alle Exams
        for ex in self.exams or []:
            be = (ex.Beisitzer or "").strip()
            if be == "":
                continue
            # Nur zählen, wenn Beisitzer exakt einem bekannten Code entspricht
            if be in counts:
                counts[be] += 1
        # In Teacher.K2 zurückschreiben (als String, wie bei K/WS/S)
        for t in getattr(self, "teachers", []) or []:
            code = (t.Lehrkraft or "").strip()
            if code and code in counts:
                # Wenn Zähler > 0, Zahl schreiben, sonst leerer String
                t.K2 = str(counts[code]) if counts[code] > 0 else ""
            else:
                # Kein gültiger Code in counts -> leer lassen
                t.K2 = ""
        # Änderungen signalisieren
        self.dataChanged.emit()

    def calculate_belastung(self):
        """
        Berechnet die Belastung je Lehrkraft anhand der Konstanten und schreibt
        das Ergebnis als String (mit 2 Nachkommastellen) in Teacher.Belastung.
        Interne Konvertierung:
        - UPZ kommt als '12.0' -> es wird die Ganzzahl vor dem Punkt verwendet (12).
        - WS, S, S2, K, K2 kommen als Strings natürlicher Zahlen -> int-Parsing; leere Strings -> 0.
        Negative Ergebnisse sind erlaubt (keine Kappung).
        """
        def to_int_safe(val: Optional[str]) -> int:
            try:
                s = str(val).strip()
                if s == "":
                    return 0
                return int(s)
            except Exception:
                return 0
        def parse_upz_int(upz_str: Optional[str]) -> int:
            try:
                s = str(upz_str).strip()
                if s == "":
                    return 0
                # Nur den Teil vor dem Punkt nehmen
                if "." in s:
                    s = s.split(".", 1)[0]
                return int(s)
            except Exception:
                return 0

        for t in getattr(self, "teachers", []) or []:
            upz_i = parse_upz_int(t.UPZ)*60
            ws_i  = to_int_safe(t.WS)
            s_i   = to_int_safe(t.S)
            s2_i  = to_int_safe(getattr(t, "S2", ""))
            k_i   = to_int_safe(t.K)
            k2_i  = to_int_safe(getattr(t, "K2", ""))
            # Division durch 0 vermeiden: falls UPZ == 0, Ergebnis als 0.00 definieren
            if upz_i == 0:
                belastung_val = 0.0
            else:
                numerator = (
                    self.settings.workload_korrektur_min * s_i
                    + self.settings.workload_korrektur_min * self.settings.workload_faktor_nachkorrektur * s2_i
                    + self.settings.workload_kolloq_pruefer_min * k_i
                    + self.settings.workload_kolloq_pruefer_min * self.settings.workload_faktor_beisitzer * k2_i
                    - self.settings.workload_unterricht_aufwand_min * ws_i
                )
                belastung_val = float(numerator) / float(upz_i)
            # Als String mit 2 Nachkommastellen speichern
            try:
                t.Belastung = f"{belastung_val:.2f}"
            except Exception:
                t.Belastung = "0.00"
        # Änderungen signalisieren
        self.dataChanged.emit()

    def _rebuild_teacher_index(self):
        """
        Baut den Kürzel-Index aus self.teachers neu auf.
        Annahme: Lehrkraft-Feld enthält eindeutiges 2-Zeichen-Kürzel.
        """
        self.teacher_by_code = {}
        for t in self.teachers or []:
            code = (t.Lehrkraft or "").strip()
            if code:
                self.teacher_by_code[code] = t

    def get_teacher_for(self, name_or_code: Optional[str]) -> Optional["Teacher"]:
        """
        Liefert den Teacher-Datensatz, wenn der angegebene String exakt
        einem Lehrkräfte-Kürzel entspricht. Sonst None.
        """
        if not name_or_code:
            return None
        key = name_or_code.strip()
        return self.teacher_by_code.get(key)

    def log(self, msg: str):
        """
        Thread-sicheres, leichtes Throttling für Log-Meldungen.
        - Signals (logMessage) sind thread-safe (queued).
        - Vermeidet QTimer.singleShot aus Nicht-GUI-Threads.
        """
        import time
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        now = time.time()
        with self._log_lock:
            if (now - self._last_log_emit_ts) >= 0.000000001:
                try:
                    self.logMessage.emit(line)
                except Exception:
                    try:
                        print(line)
                    except Exception:
                        pass
                self._last_log_emit_ts = now
            else:
                pass

    def status(self, msg: str):
        self.statusMessage.emit(msg)

    # -------------------------
    # Undo/Redo API
    # -------------------------
    def push_command(self, cmd: BaseCommand):
        # Neue Aktion pushen, Redo leeren
        self.redo_stack.clear()
        # Kappe bei max_undo
        if len(self.undo_stack) >= self.max_undo:
            self.undo_stack.pop(0)
        self.undo_stack.append(cmd)
        self.actionStateChanged.emit()  # UI kann Undo/Redo-Actions aktualisieren
        # jede Benutzeraktion über Undo/Redo-Commands markiert den Plan als geändert
        self._dirty = True
    actionStateChanged = Signal()  # neu: signalisiert Änderungen am Undo/Redo-Status


    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def undo(self) -> Optional[str]:
        if not self.undo_stack:
            return None
        cmd = self.undo_stack.pop()
        cmd.revert(self)
        self.redo_stack.append(cmd)
        self.actionStateChanged.emit()  # neu
        return f"Rückgängig: {cmd.label()}"

    def redo(self) -> Optional[str]:
        if not self.redo_stack:
            return None
        cmd = self.redo_stack.pop()
        cmd.apply(self)
        self.undo_stack.append(cmd)
        self.actionStateChanged.emit()  # neu
        return f"Wiederholen: {cmd.label()}"

    # CSV Import
    def import_csv(self, path: str):
        try:
            exams = K.read_exams_from_csv(path)
            self.exams = [Exam(
                idx=e.idx, Schueler=e.schueler, Fach=e.fach,
                Thema=e.thema, Pruefer=e.pruefer, Beisitzer=e.beisitzer
            ) for e in exams]
            self.dataChanged.emit()
            self.status(f"{len(self.exams)} Prüfungen importiert")
            self._dirty = True
        except Exception as e:
            self.report_error("CSV-Import fehlgeschlagen", e)

    # Speichern / Öffnen (.kolloPlan)
    def to_dict(self) -> Dict[str, Any]:
        exams_list = [asdict(x) for x in self.exams]
        settings_obj = asdict(self.settings)
        sched_list = [asdict(x) for x in self.schedule]
        # "Uhrzeit" existiert im ScheduleItem nicht mehr – falls Altobjekte asdict enthalten, defensiv entfernen
        for r in sched_list:
            if "Uhrzeit" in r:
                r.pop("Uhrzeit", None)
        teachers_list = [asdict(t) for t in self.teachers]
        return {
            "version": 1,
            "exams": exams_list,
            "settings": settings_obj,
            "schedule": sched_list,
            "teachers": teachers_list,
            "school_name": self.school_name or "",
        }

    def from_dict(self, obj: Dict[str, Any]):
        # Robust gegen alte Pläne ohne NTA
        ex_list = []
        for x in obj.get("exams", []):
            if "NTA" not in x:
                x["NTA"] = 0
            ex_list.append(Exam(**x))
        self.exams = ex_list
        s = obj.get("settings", {})
        t = s.get("time", {})
        c = s.get("constraints", {})
        # prepare_room robust: ggf. leerer Default
        prepare_room_val = s.get("prepare_room", "")
        try:
            ts = TimeSettings(**t)
        except Exception:
            ts = TimeSettings()
        try:
            cs = ConstraintsSettings(**c)
        except Exception:
            cs = ConstraintsSettings()
        self.settings = AppSettings(rooms=s.get("rooms", [""]), prepare_room=prepare_room_val, time=ts, constraints=cs, students_note_text=s.get("students_note_text", ""))
        
        # Minimaler Fix: neu eingeführtes Feld sicher aus den Settings übernehmen
        try:
            settings_src = obj.get("settings", {}) or {}
            val = settings_src.get("students_note_text", None)
            if val is None:
                # optionaler Fallback für sehr alte Dateien (falls es je top-level war)
                val = obj.get("students_note_text", None)
            if val is not None:
                self.settings.students_note_text = val or ""
        except Exception:
            pass
        

        # "Uhrzeit" beim Laden ignorieren (Zeiten werden live aus SlotIndex bestimmt)
        sched_in = obj.get("schedule", [])
        cleaned_sched = []
        for x in sched_in:
            if isinstance(x, dict) and "Uhrzeit" in x:
                x = dict(x)  # kopieren, um Original nicht zu verändern
                x.pop("Uhrzeit", None)
            cleaned_sched.append(ScheduleItem(**x))
        self.schedule = cleaned_sched
        # Teachers (optional in älteren Dateien)
        self.teachers = []
        for x in obj.get("teachers", []):
            try:
                # Abwärtkompatibel: fehlende S2/K2 auf "" setzen
                if "S2" not in x:
                    x["S2"] = ""
                if "K2" not in x:
                    x["K2"] = ""
                self.teachers.append(Teacher(**x))
            except Exception:
                # robust gegen Altformat
                lf = x.get("Lehrkraft", "") if isinstance(x, dict) else ""
                upz = x.get("UPZ", "") if isinstance(x, dict) else ""
                ws = x.get("WS", "") if isinstance(x, dict) else ""
                s1 = x.get("S", "") if isinstance(x, dict) else ""
                s2 = x.get("S2", "") if isinstance(x, dict) else ""
                k1 = x.get("K", "") if isinstance(x, dict) else ""
                k2 = x.get("K2", "") if isinstance(x, dict) else ""
                bel = x.get("Belastung", "") if isinstance(x, dict) else ""
                self.teachers.append(Teacher(
                    Lehrkraft=lf,
                    UPZ=upz,
                    WS=ws,
                    S=s1,
                    S2=s2,
                    K=k1,
                    K2=k2,
                    Belastung=bel
                ))
        # Index der Lehrkräfte aktualisieren
        self._rebuild_teacher_index()

        # Schule (optional in älteren Dateien)
        self.school_name = obj.get("school_name") or None
        self.dataChanged.emit()

    def save_file(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        self.status(f"Gespeichert: {os.path.basename(path)}")
        self.last_open_path = path
        self._dirty = False

    def open_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        self.from_dict(obj)
        self.status(f"Geöffnet: {os.path.basename(path)}")
        self.last_open_path = path
        self._dirty = False
        #Nach dem Öffnen werden Konflikte evaluiert und markiert
        self.evaluate_conflicts()
        self.dataChanged.emit()

    # Export/Report API
    def build_slot_times(self) -> Dict[str, List[str]]:
        slot_times = {}
        t = self.settings.time
        try:
            hh, mm = [int(x) for x in t.start_time.strip().split(":")]
        except Exception:
            hh, mm = 8, 0
        base_min = hh * 60 + mm
        for w in WEEKS:
            for d_idx, tag in enumerate(DAYS):
                labels = []
                for s in range(t.n_slots):
                    begin_min = base_min + s * (t.slot_len_min + t.break_len_min)
                    end_min = begin_min + t.slot_len_min
                    begin_str = f"{begin_min // 60:02d}:{begin_min % 60:02d}"
                    end_str = f"{end_min // 60:02d}:{end_min % 60:02d}"
                    labels.append(f"{begin_str} - {end_str}")
                slot_times[f"{w}-{tag}"] = labels
        return slot_times

    def schedule_as_plan_list(self) -> List[Dict[str, Any]]:
        plan = []
        # Uhrzeit wird dynamisch aus SlotIndex + aktuellen TimeSettings berechnet
        slot_times = self.build_slot_times()
        for s in self.schedule:
            # Standard: keine Uhrzeit, falls unvollständig
            uhr = None
            try:
                if s.Woche is not None and s.Tag is not None and s.SlotIndex is not None:
                    key = f"{int(s.Woche)}-{str(s.Tag)}"
                    times = slot_times.get(key, [])
                    if 0 <= int(s.SlotIndex) < len(times):
                        # Liefert "HH:MM - HH:MM"
                        uhr = times[int(s.SlotIndex)]
            except Exception:
                uhr = None
            plan.append({
                "ID": s.ExamIdx,
                "Schueler": s.Schueler,
                "Fach": s.Fach,
                "Thema": s.Thema,
                "Pruefer": s.Pruefer,
                "Beisitzer": s.Beisitzer,
                "Woche": s.Woche,
                "Tag": s.Tag,
                "Uhrzeit": uhr,
                "Raum": s.Raum,
            })
        return plan

    def export_docx(self, out_docx: str):
        # Nur vollständig geplante Einträge exportieren (kein Parkplatz/keine Nones)
        all_rows = self.schedule_as_plan_list()
        plan_rows = [
            r for r in all_rows
            if r.get("Woche") is not None and r.get("Tag") is not None and r.get("Uhrzeit") is not None and (r.get("Raum") or "") != ""
        ]
        exam_map = {e.idx: e for e in self.exams}
        grouped: Dict[Tuple[int, str], List[Dict[str, Any]]] = {}
        for r in plan_rows:
            w = r.get("Woche")
            t = r.get("Tag")
            if w is None or t is None:
                continue
            # NTA aus Exam holen (robust default 0)
            nta = 0
            try:
                ex = exam_map.get(r.get("ID"))
                if ex and getattr(ex, "NTA", None) is not None:
                    nta = int(ex.NTA)
            except Exception:
                nta = 0
            grouped.setdefault((int(w), str(t)), []).append({
                "ID": r.get("ID"), "Schueler": r.get("Schueler"), "Fach": r.get("Fach"),
                "Thema": r.get("Thema"), "Pruefer": r.get("Pruefer"), "Beisitzer": r.get("Beisitzer"),
                "Woche": r.get("Woche"), "Tag": r.get("Tag"), "Uhrzeit": r.get("Uhrzeit"),
                "Raum": r.get("Raum"), "SlotIndex": None, "NTA": nta
            })
        slot_times = self.build_slot_times()
        # Zeit-Infos für Datum pro Tag übergeben
        t = self.settings.time
        time_info = {
            "n_slots": t.n_slots,
            "start_time": t.start_time,
            "slot_len_min": t.slot_len_min,
            "break_len_min": t.break_len_min,
            "week1_date": t.week1_date,
            "week2_date": t.week2_date,
            "school_name": self.school_name or "",
            "prepare_room": self.settings.prepare_room or "",
            "rooms": list(self.settings.rooms or []),
        }
        EXP.build_document(grouped, slot_times, out_docx, time_info=time_info)
        self.status(f"Export erstellt: {os.path.basename(out_docx)}")

    def export_docx_students(self, out_docx: str, students_note_text: str = ""):
        all_rows = self.schedule_as_plan_list()
        plan_rows = [
            r for r in all_rows
            if r.get("Woche") is not None and r.get("Tag") is not None and r.get("Uhrzeit") is not None and (r.get("Raum") or "") != ""
        ]
        exam_map = {e.idx: e for e in self.exams}
        grouped = {}
        for r in plan_rows:
            w = r.get("Woche")
            t = r.get("Tag")
            if w is None or t is None:
                continue
            nta = 0
            try:
                ex = exam_map.get(r.get("ID"))
                if ex and getattr(ex, "NTA", None) is not None:
                    nta = int(ex.NTA)
            except Exception:
                nta = 0
            grouped.setdefault((int(w), str(t)), []).append({**r, "NTA": nta})
        slot_times = self.build_slot_times()
        t = self.settings.time
        time_info = {
            "slot_len_min": t.slot_len_min,
            "week1_date": t.week1_date,
            "week2_date": t.week2_date,
            "prepare_room": self.settings.prepare_room or "",
            "rooms": list(self.settings.rooms or []),
        }
        EXP.build_document_students(grouped, slot_times, out_docx, time_info=time_info, students_note_text=students_note_text)
        self.status(f"Export erstellt: {os.path.basename(out_docx)}")

    def export_docx_cleaning(self, out_docx: str):
        all_rows = self.schedule_as_plan_list()
        plan_rows = [
            r for r in all_rows
            if r.get("Woche") is not None and r.get("Tag") is not None and r.get("Uhrzeit") is not None and (r.get("Raum") or "") != ""
        ]
        exam_map = {e.idx: e for e in self.exams}
        grouped = {}
        for r in plan_rows:
            w = r.get("Woche")
            t = r.get("Tag")
            if w is None or t is None:
                continue
            nta = 0
            try:
                ex = exam_map.get(r.get("ID"))
                if ex and getattr(ex, "NTA", None) is not None:
                    nta = int(ex.NTA)
            except Exception:
                nta = 0
            grouped.setdefault((int(w), str(t)), []).append({**r, "NTA": nta})
        slot_times = self.build_slot_times()
        t = self.settings.time
        time_info = {
            "slot_len_min": t.slot_len_min,
            "week1_date": t.week1_date,
            "week2_date": t.week2_date,
            "prepare_room": self.settings.prepare_room or "",
            "rooms": list(self.settings.rooms or []),
        }
        EXP.build_document_cleaning(grouped, slot_times, out_docx, time_info=time_info)
        self.status(f"Export erstellt: {os.path.basename(out_docx)}")

    def export_xlsx(self, out_xlsx: str):
        # Nur vollständig geplante Einträge exportieren (kein Parkplatz/keine Nones)
        all_rows = self.schedule_as_plan_list()
        plan_rows = [
            r for r in all_rows
            if r.get("Woche") is not None and r.get("Tag") is not None and r.get("Uhrzeit") is not None and (r.get("Raum") or "") != ""
        ]
        # NTA beilegen aus Exams
        exam_map = {e.idx: e for e in self.exams}
        grouped: Dict[Tuple[int, str], List[Dict[str, Any]]] = {}
        for r in plan_rows:
            w = int(r.get("Woche")); t = str(r.get("Tag"))
            ex = exam_map.get(r.get("ID"))
            nta = 0
            try:
                if ex and getattr(ex, "NTA", None) is not None:
                    nta = int(ex.NTA)
            except Exception:
                nta = 0
            grouped.setdefault((w, t), []).append({
                **r,
                "NTA": nta,
            })
        slot_times = self.build_slot_times()
        t = self.settings.time
        time_info = {
            "slot_len_min": t.slot_len_min,
            "week1_date": t.week1_date,
            "week2_date": t.week2_date,
            "prepare_room": self.settings.prepare_room or "",
        }
 
        # Spaltenauswahl-Dialog vor dem Speichern anzeigen
        class ColumnSelectionDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Spaltenauswahl")
                lay = QVBoxLayout(self)
                lay.addWidget(QLabel("Bitte wählen Sie die zu exportierenden Spalten:"))
                self._checks = []
                labels = ["ID", "Schüler", "Kurs", "Thema", "Prüfer", "Beisitzer", "Tag", "Vorbereitung", "Prüfung", "Absperrung"]
                for txt in labels:
                    cb = QCheckBox(txt, self)
                    cb.setChecked(True)
                    lay.addWidget(cb)
                    self._checks.append(cb)
                btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
                btns.accepted.connect(self.accept)
                btns.rejected.connect(self.reject)
                lay.addWidget(btns)

            def options(self):
                return {cb.text(): cb.isChecked() for cb in self._checks}

        try:
            from PySide6.QtWidgets import QWidget
            parent = self if isinstance(self, QWidget) else None
        except Exception:
            parent = None
        dlg = ColumnSelectionDialog(parent)
        if dlg.exec() != QDialog.Accepted:
            return
        opts = dlg.options()

        # Optionen in time_info mitgeben, ohne die Signatur von build_xlsx zu ändern
        time_info = dict(time_info or {})
        time_info["options"] = opts

        EXP.build_xlsx(grouped, slot_times, out_xlsx, time_info=time_info)
        self.status(f"Excel-Export erstellt: {os.path.basename(out_xlsx)}")
 
    def report_docx(self, out_docx: str, title: str = "Kolloquiumsplan – Statistik"):
        # Nur vollständig geplante Einträge in die Statistik geben
        all_rows = self.schedule_as_plan_list()
        plan_rows = [
            r for r in all_rows
            if r.get("Woche") is not None and r.get("Tag") is not None and r.get("Uhrzeit") is not None and (r.get("Raum") or "") != ""
        ]
        # Lehrkraftdaten müssen vorhanden sein
        if not getattr(self, "teachers", None):
            self.status("Lehrkraftdaten fehlen: Bitte Lehrkräfte importieren/setzen, bevor der Report erstellt wird.")
            return
        # Mapping Person (Kürzel) -> Werte für S, S2, K, K2, Belastung
        teachers_map = {}
        try:
            for t in (self.teachers or []):
                code = (t.Lehrkraft or "").strip()
                if code == "":
                    continue
                teachers_map[code] = {
                    "S": (t.S or "").strip(),
                    "S2": (getattr(t, "S2", "") or "").strip(),
                    "K": (t.K or "").strip(),
                    "K2": (getattr(t, "K2", "") or "").strip(),
                    "Belastung": (t.Belastung or "").strip(),
                }
        except Exception:
            teachers_map = {}

        stats = REP.build_statistics(plan_rows, teachers_map=teachers_map)
        doc = REP.build_doc(stats, title)
        doc.save(out_docx)
        self.status(f"Report erstellt: {os.path.basename(out_docx)}")

    # Solver – Hintergrundlauf (threaded)
    def run_solver_background(self):
        def log_cb(msg: str):
            self.log(msg)  # Signal zur GUI

        # Exams
        k_exams: List[K.Exam] = []
        for x in self.exams:
            k_exams.append(K.Exam(
                idx=x.idx, schueler=x.Schueler, fach=x.Fach,
                thema=x.Thema, pruefer=x.Pruefer, beisitzer=x.Beisitzer
            ))

        rooms = self.settings.rooms or [""]
        t = self.settings.time
        slots_per_day = {(w, d): t.n_slots for w in WEEKS for d in range(5)}
        timing_per_day = {(w, d): (t.start_time, t.slot_len_min, t.break_len_min) for w in WEEKS for d in range(5)}
        params = K.ScheduleParams(rooms=rooms, slots_per_day=slots_per_day, timing_per_day=timing_per_day)

        c = self.settings.constraints
        una = {}
        for name, tokens in (c.unavailability or {}).items():
            sset = set()
            for tok in tokens:
                w, d = self._parse_day_token(tok)
                sset.add((w, d))
            una[name] = sset
        no_exam_days = set()
        for tok in c.no_exam_days or []:
            w, d = self._parse_day_token(tok)
            no_exam_days.add((w, d))

        cfg = K.ConstraintsConfig(
            hard_student_one_per_week=c.hard_student_one_per_week,
            hard_grouping_enabled=c.hard_grouping_enabled,
            grouping_block_size=c.grouping_block_size,
            hard_unavailability=c.hard_unavailability,
            hard_min_gap_days_same_student=c.hard_min_gap_days_same_student,
            hard_no_exam_days_enabled=c.hard_no_exam_days_enabled,
            hard_max_days_per_teacher_enabled=c.hard_max_days_per_teacher_enabled,
            hard_max_days_per_teacher_K=c.hard_max_days_per_teacher_K,
            soft_desired_gap_days_same_student=c.soft_desired_gap_days_same_student,
            soft_minimize_rooms_used=c.soft_minimize_rooms_used,
            teachers_allow_5_per_day=set(c.teachers_allow_5_per_day or []),
            default_max_per_day=c.default_max_per_day,
            soft_prefer_second_slot_start=c.soft_prefer_second_slot_start,
            weight_prefer_second_slot=c.weight_prefer_second_slot * c.SECOND_SLOT_WEIGHT,
            ignore_empty_beisitzer=bool(getattr(c, "ignore_empty_beisitzer", True)),
        )

        self._apply_solver_weights(c)

        old_verbose = getattr(K, "VERBOSE", True)
        old_cb = getattr(K, "LOG_CALLBACK", None)
        K.VERBOSE = True
        K.LOG_CALLBACK = log_cb
        try:
            scheduler = K.ColloquiumScheduler(k_exams, params, cfg, una, no_exam_days)
            scheduler.add_basic_constraints()
            scheduler.add_hard_constraints()
            scheduler.add_soft_constraints()
            solver, status = scheduler.solve(time_limit_sec=int(c.cp_time_limit_sec))
            schedule_rows = scheduler.extract_schedule(solver) if status in (K.cp_model.OPTIMAL, K.cp_model.FEASIBLE) else []
        finally:
            K.LOG_CALLBACK = old_cb
            K.VERBOSE = old_verbose

        return schedule_rows, status

    def _apply_solver_weights(self, c: ConstraintsSettings):
        try:
            K.MIP_ROOM_SOLVER_LIMIT = float(max(1, int(c.mip_room_time_limit_sec)))
        except Exception:
            pass
        try:
            K.MIP_ROOM_GAP_WEIGHT = int(c.MIP_ROOM_GAP_WEIGHT)
            K.GAP_WEIGHT_INNER = int(c.GAP_WEIGHT_INNER)
            K.GAP_WEIGHT_OUTER = int(c.GAP_WEIGHT_OUTER)
            K.SPAN_WEIGHT = int(c.SPAN_WEIGHT)
            K.SECOND_SLOT_WEIGHT = int(c.SECOND_SLOT_WEIGHT)
            K.DAY_WEIGHT_BALANCE = int(c.DAY_WEIGHT_BALANCE)
        except Exception:
            pass

    def _parse_day_token(self, token: str) -> Tuple[int, int]:
        token = token.strip()
        day = token[:2]
        week = int(token[2:])
        if day not in DAYS:
            raise ValueError(f"Ungültiger Tag: {token}")
        return week, DAYS.index(day)

    def report_error(self, title: str, e: Exception):
        msg = f"{title}: {e}\n{traceback.format_exc()}"
        self.error_log.append(msg)
        self.log(msg)

    # -------------------------
    # Konfliktbewertung global (permanent)
    # -------------------------
    def evaluate_conflicts(self):
        """
        Berechnet für alle geplanten ScheduleItems (mit Woche/Tag/Slot und Raum != "")
        harte und weiche Konflikte gemäß aktivierter Constraints.
        Parkplatz-Items (Raum == "" oder ohne Woche/Tag/Slot) werden ignoriert.
        Ergebnis in self.conflict_map.
        """
        cmap: Dict[int, Tuple[Optional[str], List[str]]] = {}
        # Index auf schnelle Suche
        exam_by_idx: Dict[int, Exam] = {e.idx: e for e in self.exams}
        # Nur geplante Items berücksichtigen
        planned = [it for it in self.schedule if (it.Raum is not None and it.Raum != "" and it.Woche is not None and it.Tag is not None and it.SlotIndex is not None)]
        c = self.settings.constraints
        # Hilfsstrukturen
        # Map (w,d,s) -> Liste ExamIdx im Slot (über Räume hinweg, zur Ressourcenkollision)
        slot_map: Dict[Tuple[int,int,int], List[int]] = {}
        for it in planned:
            w = int(it.Woche); d = DAY_INDEX.get(it.Tag, None); s = int(it.SlotIndex)
            if d is None:
                continue
            slot_map.setdefault((w,d,s), []).append(it.ExamIdx)

        ignore_empty_beis = bool(getattr(c, "ignore_empty_beisitzer", True))
        teachers_allow_5 = set(c.teachers_allow_5_per_day or [])
        default_max_per_day = c.default_max_per_day

        # Funktion zum Markieren
        def mark(idx: int, level: str, msg: str):
            cur = cmap.get(idx, (None, []))
            cur_level, msgs = cur
            # Priorität: hard > soft > None
            if cur_level is None or (cur_level == "soft" and level == "hard"):
                cur_level = level
            msgs = msgs + [msg]
            cmap[idx] = (cur_level, msgs)

        # Hilfskarten:
        # - Tage pro Person (rollenübergreifend) für harte K-Regel
        days_by_person: Dict[str, Set[Tuple[int,int]]] = {}
        for it in planned:
            w = int(it.Woche); d = DAY_INDEX.get(it.Tag, None)
            if d is None:
                continue
            ex = exam_by_idx.get(it.ExamIdx)
            if not ex:
                continue
            day_key = (w, d)
            # Prüfer
            if ex.Pruefer:
                days_by_person.setdefault(ex.Pruefer, set()).add(day_key)
            # Beisitzer (rollenübergreifend zählen)
            be = ex.Beisitzer or ""
            if be:
                days_by_person.setdefault(be, set()).add(day_key)

        # Harter Check: max Tage pro Person (rollenübergreifend)
        if c.hard_max_days_per_teacher_enabled and c.hard_max_days_per_teacher_K is not None:
            K_days = int(c.hard_max_days_per_teacher_K)
            for person, day_set in days_by_person.items():
                if len(day_set) > K_days:
                    # Markiere alle Items an Tagen, die zur Überschreitung beitragen
                    for it in planned:
                        ex = exam_by_idx.get(it.ExamIdx)
                        if not ex:
                            continue
                        if (ex.Pruefer == person or (ex.Beisitzer or "") == person):
                            mark(it.ExamIdx, "hard", f"Max Tage pro Person überschritten (K={K_days})")

        # Prüfen pro geplantes Item (weitere Regeln)
        for it in planned:
            ex = exam_by_idx.get(it.ExamIdx)
            if not ex:
                continue
            w = int(it.Woche); d = DAY_INDEX.get(it.Tag, None); s = int(it.SlotIndex)
            if d is None:
                continue
                
            # Harte Regeln
            # 1) No-Exam-Days
            if c.hard_no_exam_days_enabled:
                tok = f"{DAYS[d]}{w}"
                if tok in (c.no_exam_days or []):
                    mark(it.ExamIdx, "hard", f"Tag gesperrt ({tok})")

            # 2) Unavailability
            if c.hard_unavailability:
                una = c.unavailability or {}
                tok = f"{DAYS[d]}{w}"
                if ex.Pruefer in una and tok in una.get(ex.Pruefer, []):
                    mark(it.ExamIdx, "hard", f"Prüfer abwesend ({tok})")
                be = ex.Beisitzer or ""
                if be and be in una and tok in una.get(be, []):
                    mark(it.ExamIdx, "hard", f"Beisitzer abwesend ({tok})")

            # 3) Ressourcenkollisionen im selben Slot
            peers = [pid for pid in slot_map.get((w,d,s), []) if pid != it.ExamIdx]
            for pid in peers:
                other = exam_by_idx.get(pid)
                if not other:
                    continue
                if other.Schueler == ex.Schueler:
                    mark(it.ExamIdx, "hard", "Schülerkonflikt im gleichen Slot")
                if other.Pruefer == ex.Pruefer:
                    mark(it.ExamIdx, "hard", "Prüferkonflikt im gleichen Slot")
                # Beisitzer-Kollision; leere ggf. ignorieren
                ex_b = ex.Beisitzer or ""
                ot_b = other.Beisitzer or ""
                if not ignore_empty_beis or (ex_b != "" and ot_b != ""):
                    if ex_b == ot_b:
                        mark(it.ExamIdx, "hard", "Beisitzerkonflikt im gleichen Slot")
                # Rollenübergreifend
                if not ignore_empty_beis:
                    if other.Pruefer == ex_b or ot_b == ex.Pruefer:
                        mark(it.ExamIdx, "hard", "Rollenübergreifender Konflikt im gleichen Slot")
                else:
                    if (ex_b != "" and other.Pruefer == ex_b) or (ot_b != "" and ot_b == ex.Pruefer):
                        mark(it.ExamIdx, "hard", "Rollenübergreifender Konflikt im gleichen Slot")

            # 4) Max/Tag pro Prüfer (SOFT): tagesspezifische, rollen-spezifische Warnung
            same_day_count = 0
            for jt in planned:
                if jt.Woche == w and jt.Tag == DAYS[d]:
                    o = exam_by_idx.get(jt.ExamIdx)
                    if o and o.Pruefer == ex.Pruefer:
                        same_day_count += 1
            max_per = 5 if ex.Pruefer in teachers_allow_5 else default_max_per_day
            if same_day_count > max_per:
                mark(it.ExamIdx, "soft", f"Max/Tag Prüfer überschritten (>{max_per})")

            # 5) Pro Schüler/Woche genau 1
            if c.hard_student_one_per_week:
                same_week = 0
                for jt in planned:
                    if jt.ExamIdx == it.ExamIdx:
                        continue
                    o = exam_by_idx.get(jt.ExamIdx)
                    if o and o.Schueler == ex.Schueler and jt.Woche == w:
                        same_week += 1
                if same_week >= 1:
                    mark(it.ExamIdx, "hard", f"Schüler bereits eine Prüfung in Woche {w}")

            # 6) Mindestabstand gleiche/r Schüler/in (hart)
            if c.hard_min_gap_days_same_student is not None:
                req = int(c.hard_min_gap_days_same_student)
                # 7 Tage pro Woche (inkl. Wochenende), exklusive Zählweise wie im CP-Snippet
                ord_it = (w - 1) * 7 + d
                for jt in planned:
                    if jt.ExamIdx == it.ExamIdx:
                        continue
                    o = exam_by_idx.get(jt.ExamIdx)
                    if (
                        o
                        and o.Schueler == ex.Schueler
                        and jt.Woche is not None
                        and jt.Tag is not None
                    ):
                        od = (int(jt.Woche) - 1) * 7 + DAY_INDEX.get(jt.Tag, 0)
                        # Konsistent zu: abs(d1 - d2) >= req
                        if abs(ord_it - od) < req:
                            mark(it.ExamIdx, "hard", "Mindestabstand Schüler verletzt")
                            break

            # Weiche Regeln
            # 1) Start im 2. Slot (weich)
            if c.soft_prefer_second_slot_start:
                # Sammle alle Slot-Indizes dieses Prüfers an diesem Tag
                # Rollenübergreifend pro Person (Prüfer und Beisitzer), leere Beisitzer optional ignorieren
                persons: List[str] = []
                if ex.Pruefer:
                    persons.append(ex.Pruefer)
                be_txt = (ex.Beisitzer or "").strip()
                if not (getattr(c, "ignore_empty_beisitzer", True) and be_txt == "") and be_txt != "":
                    persons.append(be_txt)
                # Für jede betroffene Person prüfen, ob deren erste Prüfung an diesem Tag in Slot 0 oder 1 liegt
                for person in persons:
                    p_slots: List[int] = []
                    for jt in planned:
                        o = exam_by_idx.get(jt.ExamIdx)
                        if not o:
                            continue
                        if jt.Woche == w and jt.Tag == DAYS[d] and jt.SlotIndex is not None:
                            # Person beteiligt als Prüfer oder Beisitzer (rollenübergreifend)
                            o_be = (o.Beisitzer or "").strip()
                            if o.Pruefer == person or (o_be == person and not (getattr(c, "ignore_empty_beisitzer", True) and o_be == "")):
                                p_slots.append(int(jt.SlotIndex))
                    if p_slots:
                        earliest = min(p_slots)
                        # Keine Verletzung, wenn früheste Beteiligung Slot 0 oder 1 ist
                        if earliest not in (0, 1):
                            mark(it.ExamIdx, "soft", "Start nicht im 2. Slot")
                            # Einmalige Markierung genügt; weitere Personen müssen nicht geprüft werden
                            break
            
            # 2) gewünschter Abstand gleiche/r Schüler/in (weich)
            if c.soft_desired_gap_days_same_student is not None:
                desired = int(c.soft_desired_gap_days_same_student)
                # 7 Tage pro Woche (inkl. Wochenende), exklusive Zählweise
                ord_it = (w - 1) * 7 + d
                for jt in planned:
                    if jt.ExamIdx == it.ExamIdx:
                        continue
                    o = exam_by_idx.get(jt.ExamIdx)
                    if (
                        o
                        and o.Schueler == ex.Schueler
                        and jt.Woche is not None
                        and jt.Tag is not None
                    ):
                        od = (int(jt.Woche) - 1) * 7 + DAY_INDEX.get(jt.Tag, 0)
                        if abs(ord_it - od) < desired:
                            mark(it.ExamIdx, "soft", "geringer Schülerabstand")
                            break

        self.conflict_map = cmap
        # kein automatisches dataChanged hier; der Aufrufer triggert Refresh

        # --- Zusätzliche harte Prüfung: Kopplungsblöcke (Gruppierung) ---
        # Wenn aktiv, markiere alle Items eines (Thema,Fach,Pruefer)-Clusters hart,
        # die nicht gemeinsam im gleichen (Woche, Tag)-Paar liegen UND nicht als konsekutive Slots im selben Raum liegen.
        c = self.settings.constraints
        if getattr(c, "hard_grouping_enabled", False):
            # Cluster bilden: key = (Thema, Fach, Prüfer)
            clusters: Dict[Tuple[str, str, str], List[ScheduleItem]] = {}
            # Nur geplante Items (Raum != "" und Woche/Tag/Slot gesetzt) betrachten
            planned_items = [
                it for it in self.schedule
                if (it.Raum is not None and it.Raum != "" and it.Woche is not None and it.Tag is not None and it.SlotIndex is not None)
            ]
            # Mapping idx -> Exam zur Attributabfrage
            exam_by_idx: Dict[int, Exam] = {e.idx: e for e in self.exams}
            for it in planned_items:
                ex = exam_by_idx.get(it.ExamIdx)
                if not ex:
                    continue
                # Nur vollständige Schlüssel zulassen
                thema = (ex.Thema or "").strip()
                fach = (ex.Fach or "").strip()
                pruefer = (ex.Pruefer or "").strip()
                if thema == "" or fach == "" or pruefer == "":
                    continue
                key = (thema, fach, pruefer)
                clusters.setdefault(key, []).append(it)

            # Für jedes Cluster prüfen, ob alle Items am selben (Woche, Tag) liegen
            for key, items in clusters.items():
                if len(items) <= 1:
                    continue  # kein Kopplungsbedarf
                day_pairs: Set[Tuple[int, str]] = set()
                for it in items:
                    try:
                        day_pairs.add((int(it.Woche), str(it.Tag)))
                    except Exception:
                        pass
                if len(day_pairs) > 1:
                    # Verletzung: markiere alle Items des Clusters hart
                    for it in items:
                        def mark_local(idx: int, level: str, msg: str):
                            cur = cmap.get(idx, (None, []))
                            cur_level, msgs = cur
                            if cur_level is None or (cur_level == "soft" and level == "hard"):
                                cur_level = level
                            msgs = msgs + [msg]
                            cmap[idx] = (cur_level, msgs)
                        mark_local(it.ExamIdx, "hard", "Kopplungsblock verletzt (Gruppierung)")
                    continue  # weitere Adjazenzprüfung entfällt, da bereits Tages-Trennung
                # Zusätzliche harte Bedingung: konsektutive Slots im selben Raum (pausenlos, raumgebunden)
                # Gruppiere Items (am gemeinsamen Tag) nach Raum und sammle Slots
                try:
                    # Tag/Woche sind identisch, daher nimm das (Woche,Tag)-Paar aus einem Item
                    w, d = next(iter(day_pairs))
                    room_slots: Dict[str, List[int]] = {}
                    for it in items:
                        if int(it.Woche) == int(w) and str(it.Tag) == str(d):
                            if it.Raum and it.SlotIndex is not None:
                                room_slots.setdefault(str(it.Raum), []).append(int(it.SlotIndex))
                    total = sum(len(v) for v in room_slots.values())
                    if total >= 2:
                        non_empty_rooms = [r for r, lst in room_slots.items() if len(lst) > 0]
                        if len(non_empty_rooms) != 1:
                            # Slots über mehrere Räume verteilt -> Verletzung
                            for it in items:
                                def mark_local(idx: int, level: str, msg: str):
                                    cur = cmap.get(idx, (None, []))
                                    cur_level, msgs = cur
                                    if cur_level is None or (cur_level == "soft" and level == "hard"):
                                        cur_level = level
                                    msgs = msgs + [msg]
                                    cmap[idx] = (cur_level, msgs)
                                mark_local(it.ExamIdx, "hard", "Kopplungsblock verletzt (nicht konsekutive Slots im selben Raum)")
                        else:
                            room = non_empty_rooms[0]
                            seq = sorted(set(room_slots.get(room, [])))
                            # Lückenlose Sequenz prüfen: keine Pausen/gaps und alle Elemente im selben Raum
                            if len(seq) < total or any(seq[i] + 1 != seq[i+1] for i in range(len(seq)-1)):
                                for it in items:
                                    def mark_local(idx: int, level: str, msg: str):
                                        cur = cmap.get(idx, (None, []))
                                        cur_level, msgs = cur
                                        if cur_level is None or (cur_level == "soft" and level == "hard"):
                                            cur_level = level
                                        msgs = msgs + [msg]
                                        cmap[idx] = (cur_level, msgs)
                                    mark_local(it.ExamIdx, "hard", "Kopplungsblock verletzt (nicht konsekutive Slots im selben Raum)")
                except Exception:
                    # Bei Inkonsistenzen (fehlende Daten) hier keine zusätzliche Markierung
                    pass

    def evaluate_fair_day_distribution(self):
        """
        Ermittelt fr alle geplanten Prfungen (mit Raum != "" und validem SlotIndex),
        ob fr deren Schler beide Prfungen spte Slots ergeben, sodass die Summe der
        beiden Slotindizes strikt grer ist als der per Constraint gesetzte Schwellenwert.
        Ergebnis in self.fair_day_map (ExamIdx -> True). Parkplatzprfungen werden ignoriert.
        Falls Feature deaktiviert: Karte geleert.
        """
        try:
            c = self.settings.constraints
            if not getattr(c, "fair_day_distribution_enabled", False):
                self.fair_day_map = {}
                return
            threshold = int(getattr(c, "fair_day_distribution_slotsum", 4))
        except Exception:
            self.fair_day_map = {}
            return

        # Nur voll geplante Items (kein Parkplatz)
        planned = [
            it for it in (self.schedule or [])
            if (it.Raum or "") != "" and it.Woche is not None and it.Tag is not None and it.SlotIndex is not None
        ]
        # Schueler -> Liste[(ExamIdx, SlotIndex)]
        by_student: Dict[str, List[Tuple[int, int]]] = {}
        for it in planned:
            try:
                by_student.setdefault(it.Schueler or "", []).append((int(it.ExamIdx), int(it.SlotIndex)))
            except Exception:
                continue
        mark: Dict[int, bool] = {}
        for sch, lst in by_student.items():
            if len(lst) != 2:
                continue  # Anforderungen: genau zwei Prfungen
            try:
                ssum = lst[0][1] + lst[1][1]
            except Exception:
                continue
            if ssum > threshold:  # strikt grer
                for ex_idx, _s in lst:
                    mark[ex_idx] = True
        self.fair_day_map = mark

# -------------------------
# Tabelle/Modelle für Hauptansicht
# -------------------------
def compute_day_dates(ts: TimeSettings) -> Dict[Tuple[int, int], str]:
    res = {}
    fmt = "%Y-%m-%d"
    for w in WEEKS:
        base = ts.week1_date if w == 1 else ts.week2_date
        if base:
            try:
                dt = datetime.strptime(base, fmt)
            except Exception:
                dt = None
        else:
            dt = None
        for d in range(5):
            label = DAYS[d]
            if dt:
                day_dt = dt + timedelta(days=d)
                label = f"{DAYS[d]}. {day_dt.strftime('%d.%m.%y')}"
            res[(w, d)] = label
    return res

class LeftModel(QAbstractTableModel):
    def __init__(self, dc: DataController):
        super().__init__()
        self.dc = dc
        self.day_dates = compute_day_dates(self.dc.settings.time)
        self.dc.dataChanged.connect(self._recalc)
        self._recalc()

    def _recalc(self):
        self.beginResetModel()
        self.day_dates = compute_day_dates(self.dc.settings.time)
        t = self.dc.settings.time
        self.rows = []
        for w in WEEKS:
            for d in range(5):
                for s in range(t.n_slots):
                    self.rows.append((w, d, s))
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ["Tag", "Zeit"][section]
        return None

    def data(self, index, role):
        if not index.isValid():
            return None
        w, d, s = self.rows[index.row()]
        t = self.dc.settings.time

        if role == Qt.DisplayRole:
            if index.column() == 0:
                if s == 0:
                    return self.day_dates.get((w, d), DAYS[d])
                return ""
            if index.column() == 1:
                try:
                    hh, mm = [int(x) for x in t.start_time.split(":")]
                except Exception:
                    hh, mm = 8, 0
                begin_min = hh*60 + mm + s*(t.slot_len_min + t.break_len_min)
                return f"{begin_min//60:02d}:{begin_min%60:02d}"
        return None

class RightModel(QAbstractTableModel):
    dropped = Signal(int, int, int, str)  # (row, col, exam_idx, reason)
    current_drag_exam_idx: Optional[int] = None  # für Hover-Färbung
    PARKING_ROOM_NAME = "Kein Raum zugewiesen"
    # Subindex der im Parkplatz angeklickten Kachel fr den aktuellen Drag
    current_drag_from_subindex: Optional[int] = None


    def __init__(self, dc: DataController):
        super().__init__()
        self.dc = dc
        self.dc.dataChanged.connect(self._recalc)
        self._recalc()

    def _recalc(self):
        self.beginResetModel()
        t = self.dc.settings.time
        self.rows = []
        for w in WEEKS:
            for d in range(5):
                for s in range(t.n_slots):
                    self.rows.append((w, d, s))
        
        # Basis-Räume aus Settings
        self.rooms = list(self.dc.settings.rooms or [""])

        # cell_map: fr echte Rume 1:1 Belegung        
        self.cell_map: Dict[Tuple[int,int,int,str], Any] = {}
        for w, d, s in self.rows:
            for r in self.rooms:
                self.cell_map[(w,d,s,r)] = None
        
        for it in self.dc.schedule:
            if it.Woche is None or it.Tag is None or it.SlotIndex is None:
                continue
            w = int(it.Woche); d = DAY_INDEX.get(str(it.Tag), None); s = int(it.SlotIndex)
            if d is None:
                continue
            room = it.Raum if (it.Raum is not None and it.Raum != "") else ""
            if room == "":
                # Im separaten Parkplatz-View dargestellt; hier nicht anzeigen
                continue
            key = (w, d, s, room)
            if key in self.cell_map:
                self.cell_map[key] = it.ExamIdx
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return max(1, len(self.rooms))

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.rooms[section] if 0 <= section < len(self.rooms) else ""
        return None

    def flags(self, index: QModelIndex):
        fl = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDropEnabled
        w, d, s = self.rows[index.row()]
        room = self.rooms[index.column()]
        val = self.cell_map.get((w, d, s, room))
        # Drag erlaubt, wenn in echtem Raum belegt
        if val is not None:
            fl |= Qt.ItemIsDragEnabled
        return fl

    def mimeTypes(self):
        return ["application/x-kollo-exam"]

    def mimeData(self, indexes):
        md = QMimeData()
        for idx in indexes:
            if not idx.isValid():
                continue
            w, d, s = self.rows[idx.row()]
            room = self.rooms[idx.column()]
            cell = self.cell_map.get((w, d, s, room))
            if cell is not None:
                payload = {"ExamIdx": cell, "from": (w, d, s, room)}
                md.setData("application/x-kollo-exam", QByteArray(json.dumps(payload).encode("utf-8")))
                RightModel.current_drag_exam_idx = cell
                break
        return md

    def supportedDropActions(self):
        return Qt.MoveAction

    def canDropMimeData(self, data, action, row, col, parent):
        return data.hasFormat("application/x-kollo-exam")

    def dropMimeData(self, data, action, row, col, parent):
        if not data.hasFormat("application/x-kollo-exam"):
            return False
        try:
            payload = json.loads(bytes(data.data("application/x-kollo-exam")).decode("utf-8"))
            ex_idx = payload["ExamIdx"]

            # Fallback: wenn row/col -1 sind, parent benutzen
            if row < 0 or col < 0:
                if parent and parent.isValid():
                    row = parent.row()
                    col = parent.column()
                else:
                    return False

            # Schutz: Indexgrenzen
            if not (0 <= row < len(self.rows)) or not (0 <= col < len(self.rooms)):
                return False

            to_w, to_d, to_s = self.rows[row]
            to_room = self.rooms[col]

            # Änderung: Drop wird immer akzeptiert. Prüfung erfolgt nach dem Setzen für die Färbung/Status.
            ok, hard_reason, soft_reasons = self._check_move(ex_idx, to_w, to_d, to_s, to_room)
            # Blockiere nur, wenn Zielslot im Raum belegt ist (einzige Blockade)
            if not ok and hard_reason and "Ziel-Slot ist bereits belegt" in hard_reason:
                self.dropped.emit(row, col, ex_idx, f"Nicht möglich: {hard_reason}")
                return False

            # Update Schedule (immer setzen, selbst bei harten/soften Regelverstößen)
            did = False
            for it in self.dc.schedule:
                if it.ExamIdx == ex_idx:
                    it.Woche = to_w
                    it.Tag = DAYS[to_d]
                    it.SlotIndex = to_s
                    # Uhrzeit stets aus TimeSettings neu berechnen
                    self.dc.recompute_item_time(it)
                    it.Raum = to_room
                    did = True
                    break

            self._recalc()
            self.layoutChanged.emit()
            # Nach Setzen: globale Konflikte berechnen und Views aktualisieren
            self.dc.evaluate_conflicts()
            # Faire Tagesverteilung neu bewerten
            try:
                self.dc.evaluate_fair_day_distribution()
            except Exception:
                pass
            self.dc.dataChanged.emit()

            # Undo/Redo: Move als Command erfassen (auch wenn Herkunft PARKING war)
            try:
                # Helper: Zustand eines Items im aktuellen Plan
                def find_item_state(dc: DataController, exam_idx: int) -> Dict[str, Any]:
                    for it in dc.schedule:
                        if it.ExamIdx == exam_idx:
                            return {
                                "Woche": it.Woche, "Tag": it.Tag, "SlotIndex": it.SlotIndex,
                                "Uhrzeit": it.Uhrzeit, "Raum": it.Raum
                            }
                    # Nicht gefunden -> Parkplatz-Zustand
                    return {"Woche": None, "Tag": None, "SlotIndex": None, "Uhrzeit": None, "Raum": ""}

                # AFTER-State nach der Platzierung
                after_state = find_item_state(self.dc, ex_idx)

                # BEFORE-State aus Payload herleiten
                before_state = None
                origin = payload.get("from")
                if isinstance(origin, (list, tuple)) and len(origin) == 4:
                    bw, bd, bs, broom = origin
                    # Uhrzeit vorher anhand Settings ermitteln (nur für Konsistenz, kann None bleiben)
                    before_state = {"Woche": bw, "Tag": DAYS[bd], "SlotIndex": bs, "Uhrzeit": None, "Raum": broom}
                else:
                    # Herkunft: PARKING oder unbekannt -> Parkplatz-Zustand
                    before_state = {"Woche": None, "Tag": None, "SlotIndex": None, "Uhrzeit": None, "Raum": ""}
                self.dc.push_command(MoveExamCommand(ex_idx, before_state, after_state))
            except Exception:
                pass

            if did:
                # Statusmeldung auf Basis der Prüfergebnisse
                if not ok and hard_reason:
                    self.dropped.emit(row, col, ex_idx, f"Plaziert (harte Regel verletzt: {hard_reason})")
                elif soft_reasons:
                    self.dropped.emit(row, col, ex_idx, "Plaziert (Hinweis: " + "; ".join(soft_reasons) + ")")
                else:
                    self.dropped.emit(row, col, ex_idx, "Plaziert")
                return True
            else:
                self.dropped.emit(row, col, ex_idx, "Keine Änderung vorgenommen")
                return False
        except Exception as e:
            self.dropped.emit(row if row >= 0 else 0, col if col >= 0 else 0, -1, f"Fehler beim Verschieben: {e}")
            return False
        finally:
            RightModel.current_drag_exam_idx = None
            RightModel.current_drag_from_subindex = None

    def data(self, index, role):
        if not index.isValid():
            return None
        w, d, s = self.rows[index.row()]
        room = self.rooms[index.column()]
        cell = self.cell_map.get((w, d, s, room))

        if role == Qt.BackgroundRole:
            # Permanente Konfliktfrbung: falls Item geplant ist
            if room is not None and room != "" and cell is not None:
                # Temporre violette Hervorhebung hat Vorrang vor Konflikt-/Hoverfarben
                if self._is_highlighted(cell):
                    return COLOR_HIGHLIGHT_VIOLET
                state = self.dc.conflict_map.get(cell)
                if state:
                    level, msgs = state
                    if level == "hard":
                        return COLOR_HARD_FORBIDDEN
                    if level == "soft":
                        # Sonderfall: Start-im-2.-Slot als hellgelb hervorheben
                        if any("Start nicht im 2. Slot" in m for m in msgs or []):
                            return COLOR_SOFT_SECOND_SLOT
                    return COLOR_SOFT_WARN
                # Keine Konfliktfarbe aktiv: ggf. faire Tagesverteilung einfärben
                try:
                    if getattr(self.dc, "fair_day_map", None) and self.dc.fair_day_map.get(cell, False):
                        return COLOR_FAIR_DISTRIBUTION
                except Exception:
                    pass

            drag_idx = RightModel.current_drag_exam_idx
            if drag_idx is not None:
                # Temporäre violette Hervorhebung hat Vorrang (auch im Hover)
                if cell is not None and self._is_highlighted(cell):
                    return COLOR_HIGHLIGHT_VIOLET

                ok, hard_reason, soft_reasons = self._check_move(drag_idx, w, d, s, room)
                if not ok and hard_reason:
                    return COLOR_HARD_FORBIDDEN
                elif soft_reasons:
                    # Hover-Farbgebung: gelb bei Start-im-2.-Slot, sonst orange
                    if any("Start nicht im 2. Slot" in m for m in soft_reasons):
                        return COLOR_SOFT_SECOND_SLOT
                    return COLOR_SOFT_WARN
                else:
                  return COLOR_ALLOWED
            return COLOR_NORMAL

        if role == Qt.DisplayRole:
            ex_idx = cell
            if ex_idx is None:
                return ""
            ex = self._exam_by_idx(ex_idx)
            if not ex:
                return ""
            line1 = ex.Schueler or ""
            line2 = f"{ex.Pruefer or ''} | {ex.Beisitzer or ''}"
            line3 = ex.Thema or ""
            return f"{line1}\n{line2}\n{line3}"
                        
        if role == Qt.FontRole:
            return FONT_BLOCK

        return None

    def _is_highlighted(self, exam_idx: int) -> bool:
        #Prüft, ob der gegebene Exam-Block gem aktuellem Highlight-Modus gehighlighted werden soll.
        mode = getattr(self.dc, "highlight_mode", None)
        value = getattr(self.dc, "highlight_value", None)
        if not mode or value is None:
            return False
        ex = self._exam_by_idx(exam_idx)
        if not ex:
            return False
        if mode == "pruefer":
            return (ex.Pruefer or "") == value
        if mode == "beisitzer":
            return (ex.Beisitzer or "") == value
        if mode == "schueler":
            return (ex.Schueler or "") == value
        if mode == "fach":
            # extrahiere Buchstabenteil des Fachs und vergleiche lower-case
            # Annahme: Format Zahl+Buchstaben+Zahl, z. B. "3geo2"
            f = (ex.Fach or "")
            m = re.match(r"^\d*([A-Za-z]+)\d*$", f)
            core = m.group(1).lower() if m else re.sub(r"\d+", "", f).lower()
            return core == value
        if mode == "search":
            # UND-Suche über mehrere Felder (case-insensitive Contains, keine Normalisierung beim Fach)
            try:
                return exam_matches_criteria_caseins_contains(ex, value if isinstance(value, dict) else {})
            except Exception:
                return False
        return False

    def _exam_by_idx(self, idx: int) -> Optional[Exam]:
        for ex in self.dc.exams:
            if ex.idx == idx:
                return ex
        return None

    def _check_move(self, exam_idx: int, to_w: int, to_d: int, to_s: int, to_room: str) -> Tuple[bool, Optional[str], List[str]]:
        ex = self._exam_by_idx(exam_idx)
        if ex is None:
            return False, "Unbekannte Prüfung", []
        c = self.dc.settings.constraints
        ignore_empty_beisitzer = bool(getattr(c, "ignore_empty_beisitzer", True))


        # Ziel-Slot bereits belegt? (einzige Drop-Blockade)
        if self.cell_map.get((to_w, to_d, to_s, to_room)) is not None:
            occupied_idx = self.cell_map.get((to_w, to_d, to_s, to_room))
            if occupied_idx != exam_idx:
                return False, "Ziel-Slot ist bereits belegt", []

        # No Exam Days (hart)
        if c.hard_no_exam_days_enabled:
            tok = f"{DAYS[to_d]}{to_w}"
            if tok in (c.no_exam_days or []):
                return False, f"Tag {tok} ist gesperrt", []

        # Unavailability (hart): Prüfer/Beisitzer
        if c.hard_unavailability:
            una = c.unavailability or {}
            if ex.Pruefer in una and f"{DAYS[to_d]}{to_w}" in una[ex.Pruefer]:
                return False, f"Prüfer abwesend ({DAYS[to_d]}{to_w})", []
            if ex.Beisitzer in una and f"{DAYS[to_d]}{to_w}" in una.get(ex.Beisitzer, []):
                return False, f"Beisitzer abwesend ({DAYS[to_d]}{to_w})", []

        # Ressourcen-Konflikte (hart)
        for it in self.dc.schedule:
            if it.Woche == to_w and it.Tag == DAYS[to_d] and it.SlotIndex == to_s and it.ExamIdx != exam_idx:
                other = self._exam_by_idx(it.ExamIdx)
                if other:
                    if other.Schueler == ex.Schueler:
                        return False, "Schülerkonflikt im gleichen Slot", []
                    if other.Pruefer == ex.Pruefer:
                        return False, "Prüferkonflikt im gleichen Slot", []
                    # Beisitzer-Konflikte: leere Beisitzer optional ignorieren
                    ex_b = ex.Beisitzer if ex.Beisitzer is not None else ""
                    ot_b = other.Beisitzer if other.Beisitzer is not None else ""
                    if not ignore_empty_beisitzer or (ex_b != "" and ot_b != ""):
                        if ot_b == ex_b:
                            return False, "Beisitzerkonflikt im gleichen Slot", []
                    # Rollenübergreifend: nur nicht-leere Beisitzer vergleichen, falls Flag aktiv
                    if not ignore_empty_beisitzer:
                        if other.Pruefer == ex_b or ot_b == ex.Pruefer:
                            return False, "Rollenbergreifender Konflikt im gleichen Slot", []
                    else:
                        if (ex_b != "" and other.Pruefer == ex_b) or (ot_b != "" and ot_b == ex.Pruefer):
                            return False, "Rollenbergreifender Konflikt im gleichen Slot", []

        # Soft: Max/Tag pro Prüfer (tagesspezifisch)
        soft_msgs: List[str] = []
        same_day_count = 0
        for it in self.dc.schedule:
            if it.Woche == to_w and it.Tag == DAYS[to_d]:
                other = self._exam_by_idx(it.ExamIdx)
                if other and other.Pruefer == ex.Pruefer:
                    same_day_count += 1
        max_per_day = 5 if ex.Pruefer in (c.teachers_allow_5_per_day or []) else c.default_max_per_day
        if same_day_count > max_per_day:
            soft_msgs.append(f"maximale Prüfungen pro Tag für Prüfer überschritten (>{max_per_day})")

        # Pro Schüler/Woche genau 1 (hart), falls aktiviert
        if c.hard_student_one_per_week:
            same_week_count = 0
            for it in self.dc.schedule:
                if it.ExamIdx == exam_idx:
                    continue
                other = self._exam_by_idx(it.ExamIdx)
                if other and other.Schueler == ex.Schueler and it.Woche is not None:
                    if int(it.Woche) == int(to_w):
                        same_week_count += 1
            if same_week_count >= 1:
                return False, f"Schüler hat bereits eine Prüfung in Woche {to_w}", []

        # Mindestabstand gleiche/r Schüler/in (hart)
        if c.hard_min_gap_days_same_student is not None:
            req = int(c.hard_min_gap_days_same_student)
            # 7 Tage pro Woche (inkl. Wochenende), exklusive Zählweise wie im CP-Snippet:
            # Abstand = Anzahl Kalendertage zwischen den Prüfungstagen
            ord_to = (to_w - 1) * 7 + to_d
            for it in self.dc.schedule:
                if it.ExamIdx == exam_idx:
                    continue
                other = self._exam_by_idx(it.ExamIdx)
                if (
                    other
                    and other.Schueler == ex.Schueler
                    and it.Woche is not None
                    and it.Tag is not None
                ):
                    od = (int(it.Woche) - 1) * 7 + DAY_INDEX.get(it.Tag, 0)
                    # Konsistent zu: abs(d1 - d2) >= a
                    if abs(ord_to - od) < req:
                        return False, "Mindestabstand Schüler verletzt", []

        # Harte Regel: Kopplungsblöcke (Gruppierung gleicher (Thema, Fach, Prüfer)) müssen am selben (Woche, Tag) liegen
        if getattr(c, "hard_grouping_enabled", False):
            thema = (ex.Thema or "").strip()
            fach = (ex.Fach or "").strip()
            pruefer = (ex.Pruefer or "").strip()
            if thema != "" and fach != "" and pruefer != "":
                # Sammle geplante Items im Cluster und prüfe (Woche, Tag)
                cluster_day_pairs: Set[Tuple[int, str]] = set()
                # Für die Adjazenzprüfung zusätzlich: (Raum, SlotIndex) am Ziel-Tag/Woche
                same_day_room_slots: Dict[str, List[int]] = {}
                target_pair = (to_w, DAYS[to_d])
                for it in self.dc.schedule:
                    o = self._exam_by_idx(it.ExamIdx)
                    if not o:
                        continue
                    if (o.Thema or "").strip() == thema and (o.Fach or "").strip() == fach and (o.Pruefer or "").strip() == pruefer:
                        if it.ExamIdx == exam_idx:
                            # der verschobene Block zählt mit dem Ziel-Tag
                            cluster_day_pairs.add(target_pair)
                            # Für die Adjazenz-/Raumprüfung berücksichtigen wir den Ziel-Slot/-Raum
                            if to_w is not None and to_d is not None and to_s is not None and to_room:
                                key_w, key_d = to_w, DAYS[to_d]
                                if key_w == target_pair[0] and key_d == target_pair[1]:
                                    same_day_room_slots.setdefault(to_room, []).append(int(to_s))
                        else:
                            if it.Woche is not None and it.Tag is not None:
                                cluster_day_pairs.add((int(it.Woche), str(it.Tag)))
                            # Sammle Slots pro Raum nur für den Ziel-(Woche,Tag)
                            try:
                                if it.Woche is not None and it.Tag is not None and int(it.Woche) == target_pair[0] and str(it.Tag) == target_pair[1]:
                                    if it.Raum and it.SlotIndex is not None:
                                        same_day_room_slots.setdefault(str(it.Raum), []).append(int(it.SlotIndex))
                            except Exception:
                                pass
                # Wenn mehr als ein (Woche, Tag)-Paar vorkommt, wäre die Kopplung verletzt
                if len(cluster_day_pairs) > 1:
                    return False, "Kopplungsblock verletzt (Gruppierung)", []
                # Zusätzliche harte Bedingung: konsektutive Slots im selben Raum (pausenlos, raumgebunden)
                # Gilt nur, wenn mindestens zwei Items am selben (Woche,Tag) existieren
                total_same_day = sum(len(v) for v in same_day_room_slots.values())
                if total_same_day >= 2:
                    # Es darf genau EIN Raum den gesamten Block enthalten; in diesem Raum müssen die Slots eine lückenlose Sequenz bilden
                    # Falls die Slots auf mehrere Räume verteilt sind, Verletzung
                    non_empty_rooms = [r for r, lst in same_day_room_slots.items() if len(lst) > 0]
                    if len(non_empty_rooms) != 1:
                        return False, "Kopplungsblock verletzt (Gruppierung)", []
                    room = non_empty_rooms[0]
                    seq = sorted(set(same_day_room_slots.get(room, [])))
                    # Lückenlose Sequenz prüfen
                    if len(seq) < total_same_day or any(seq[i] + 1 != seq[i+1] for i in range(len(seq)-1)):
                        return False, "Kopplungsblock verletzt (Gruppierung)", []

        # Harte K-Regel: max Tage pro Person (rollenübergreifend, alle Wochen)
        if c.hard_max_days_per_teacher_enabled and c.hard_max_days_per_teacher_K is not None:
            K_days = int(c.hard_max_days_per_teacher_K)
            # Prüfe K nur für die am aktuell verschobenen Block beteiligten Personen (rollenübergreifend)
            involved_persons: List[str] = []
            if ex.Pruefer:
                involved_persons.append(ex.Pruefer.strip())
            be_txt = (ex.Beisitzer or "").strip()
            if not (ignore_empty_beisitzer and be_txt == "") and be_txt != "":
                involved_persons.append(be_txt)

            # Simuliere den Plan nach dem Move: exam_idx auf (to_w,to_d) verlegen
            # und zähle Tage pro Person NUR für involved_persons
            days_by_person: Dict[str, Set[Tuple[int,int]]] = {p: set() for p in involved_persons}

            def add_day_if_involved(person: Optional[str], w: Optional[int], d_name: Optional[str]):
                if not person:
                    return
                person = person.strip()
                if person == "":
                    return
                if person not in days_by_person:
                    return
                if w is None or d_name is None:
                    return
                d_idx = DAY_INDEX.get(d_name, None)
                if d_idx is None:
                    return
                days_by_person[person].add((int(w), int(d_idx)))

            for it in self.dc.schedule:
                exo = self._exam_by_idx(it.ExamIdx)
                if not exo:
                    continue
                if it.ExamIdx == exam_idx:
                    # simulierter Tag für den verschobenen Block
                    add_day_if_involved(exo.Pruefer, to_w, DAYS[to_d])
                    be_sim = (exo.Beisitzer or "").strip()
                    if not (ignore_empty_beisitzer and be_sim == ""):
                        add_day_if_involved(be_sim, to_w, DAYS[to_d])
                else:
                    if it.Woche is None or it.Tag is None:
                        continue
                    add_day_if_involved(exo.Pruefer, it.Woche, it.Tag)
                    be_o = (exo.Beisitzer or "").strip()
                    if not (ignore_empty_beisitzer and be_o == ""):
                        add_day_if_involved(be_o, it.Woche, it.Tag)

            # prüfen: nur für die beteiligten Personen
            for person, dset in days_by_person.items():
                if len(dset) > K_days:
                    return False, f"maximale Tage pro Prüfer/Beisitzer überschritten (K={K_days})", []

        # Soft-Hinweise
        soft = list(soft_msgs)
        
        # Start im 2. Slot (weich)
        if c.soft_prefer_second_slot_start:
            # Sammle alle Slot-Indizes dieses Prüfers an diesem Tag (ohne den verschobenen selbst)
            # Rollenübergreifend pro Person (Prüfer und Beisitzer), leere Beisitzer optional ignorieren
            persons: List[str] = []
            if ex.Pruefer:
                persons.append(ex.Pruefer)
            be_txt = (ex.Beisitzer or "").strip()
            if not (getattr(c, "ignore_empty_beisitzer", True) and be_txt == "") and be_txt != "":
                persons.append(be_txt)

            def earliest_for_person(person: str) -> Optional[int]:
                # Ermittele den frühesten Slot-Index (inkl. des Ziel-Moves) für die Person an diesem Tag
                slots_for_p: List[int] = []
                for it in self.dc.schedule:
                    other = self._exam_by_idx(it.ExamIdx)
                    if not other or it.Woche is None or it.Tag is None or it.SlotIndex is None:
                        continue
                    if int(it.Woche) == to_w and it.Tag == DAYS[to_d]:
                        o_be = (other.Beisitzer or "").strip()
                        involved = (other.Pruefer == person) or (o_be == person and not (getattr(c, "ignore_empty_beisitzer", True) and o_be == ""))
                        if involved:
                            # Wenn es der gerade verschobene Block ist, ersetze den Slot mit to_s
                            if it.ExamIdx == exam_idx:
                                slots_for_p.append(int(to_s))
                            else:
                                slots_for_p.append(int(it.SlotIndex))
                # Falls der verschobene Block noch nicht im Tages-Set war (z. B. aus Parkplatz), hinzufügen
                if ex.Pruefer == person or ((ex.Beisitzer or "").strip() == person and not (getattr(c, "ignore_empty_beisitzer", True) and (ex.Beisitzer or "").strip() == "")):
                    slots_for_p.append(int(to_s))
                return min(slots_for_p) if slots_for_p else None

            # Wenn für irgendeine beteiligte Person der früheste Slot nicht 0 oder 1 ist, Soft-Hinweis hinzufügen
            for person in persons:
                earliest = earliest_for_person(person)
                if earliest is not None and earliest not in (0, 1):
                    soft.append("Start nicht im 2. Slot")
                    break

        # gewünschter Abstand gleiche/r Schüler/in (weich)
        if c.soft_desired_gap_days_same_student is not None:
            desired = int(c.soft_desired_gap_days_same_student)
            # 7 Tage pro Woche (inkl. Wochenende), exklusive Zählweise
            ord_to = (to_w - 1) * 7 + to_d
            for it in self.dc.schedule:
                if it.ExamIdx == exam_idx:
                    continue
                other = self._exam_by_idx(it.ExamIdx)
                if other and other.Schueler == ex.Schueler and it.Woche is not None and it.Tag is not None:
                    od = (int(it.Woche) - 1) * 7 + DAY_INDEX.get(it.Tag, 0)
                    if abs(ord_to - od) < desired:
                        soft.append("geringer Schülerabstand")
                        break

        return True, None, soft

# -------------------------
# Delegates
# -------------------------
class LeftDelegate(QStyledItemDelegate):
    def __init__(self, dc: DataController, parent=None):
        super().__init__(parent)
        self.dc = dc
        self.font = FONT_DEFAULT

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.font = self.font
        painter.fillRect(opt.rect, QColor(250, 250, 250) if index.column() == 0 else QColor(255, 255, 255))
        painter.setFont(self.font)
        painter.setPen(Qt.black)
        text = index.data(Qt.DisplayRole) or ""
        painter.drawText(opt.rect.adjusted(6, 0, -6, 0), Qt.AlignVCenter | (Qt.AlignHCenter if index.column() == 0 else Qt.AlignLeft), text)
        model: LeftModel = index.model()
        if model and hasattr(model, "rows") and 0 <= index.row() < len(model.rows):
            w, d, s = model.rows[index.row()]
            if s == self.dc.settings.time.n_slots - 1:
                y = opt.rect.bottom()
                painter.setPen(QColor(0, 0, 0))
                painter.drawLine(opt.rect.left(), y, opt.rect.right(), y)
        painter.restore()

class RightDelegate(QStyledItemDelegate):
    def __init__(self, dc: DataController, parent=None):
        super().__init__(parent)
        self.dc = dc
        self.font = FONT_BLOCK

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        bg = index.data(Qt.BackgroundRole)
        if isinstance(bg, QColor):
            painter.fillRect(opt.rect, bg)
            if bg == COLOR_ALLOWED:
                pen = painter.pen()
                pen.setColor(QColor(80, 160, 80))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawRect(opt.rect.adjusted(1, 1, -1, -1))
        else:
            painter.fillRect(opt.rect, COLOR_NORMAL)

        painter.setFont(self.font)
        painter.setPen(Qt.black)
        model: RightModel = index.model()
        if not hasattr(model, "rows") or not hasattr(model, "rooms") or not index.isValid():
            painter.restore()
            return
        w, d, s = model.rows[index.row()]
        room = model.rooms[index.column()]

        # Raum-Zellen zeichnen
        text = index.data(Qt.DisplayRole) or ""
        inner = opt.rect.adjusted(8, 6, -8, -6)
        flags = Qt.AlignHCenter | Qt.AlignVCenter | Qt.TextWordWrap
        painter.drawText(inner, flags, text)

        # Abschlusslinie nach letztem Slot eines Tages
        try:
            if s == self.dc.settings.time.n_slots - 1:
                y = opt.rect.bottom()
                pen = painter.pen()
                pen.setColor(QColor(0, 0, 0))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(opt.rect.left(), y, opt.rect.right(), y)
        except Exception:
            pass
        painter.restore()

#-------------------------
# Parkplatz-Model und -Delegate (eigene View)
# -------------------------
class ParkingModel(QAbstractTableModel):
    """
    Globale, durchgängige Parkplatz-Ansicht:
    - 1 Spalte, beliebig viele Zeilen
    - Zeigt alle ScheduleItems mit Raum == "" (leer) als Kacheln
    - Drag erlaubt (herausziehen), Drop erlaubt (zurück parken), aber kein Re-Sortieren erzwungen
    - Drop in Parkplatz: keine Prüfungen (immer okay)
    """
    dropped = Signal(str)  # status message

    COLS = 1

    def __init__(self, dc: DataController):
        super().__init__()
        self.dc = dc
        self.dc.dataChanged.connect(self._recalc)
        self.items: List[int] = []  # Liste ExamIdx im Parkplatz
        self._recalc()

    def _recalc(self):
        self.beginResetModel()
        self.items = [it.ExamIdx for it in self.dc.schedule if (it.Raum is None or it.Raum == "")]
        # Anzahl Zeilen: deckt alle Items ab
        self._rows = (len(self.items) + self.COLS - 1) // self.COLS if self.items else 0
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return self._rows

    def columnCount(self, parent=QModelIndex()):
        return self.COLS

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ""  # Einspaltig, kein Header-Text notwendig
        return None

    def index_to_item(self, row: int, col: int) -> Optional[int]:
        idx = row * self.COLS + col
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None

    def flags(self, index: QModelIndex):
        fl = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDropEnabled
        ex_idx = self.index_to_item(index.row(), index.column())
        if ex_idx is not None:
            fl |= Qt.ItemIsDragEnabled
        return fl

    def mimeTypes(self):
        return ["application/x-kollo-exam"]

    def mimeData(self, indexes):
        md = QMimeData()
        # Eine Kachel ziehen
        for idx in indexes:
            if not idx.isValid():
                continue
            ex_idx = self.index_to_item(idx.row(), idx.column())
            if ex_idx is None:
                continue
            # Herkunft "PARKING" kennzeichnen
            payload = {"ExamIdx": ex_idx, "from": ("PARKING",)}
            md.setData("application/x-kollo-exam", QByteArray(json.dumps(payload).encode("utf-8")))
            RightModel.current_drag_exam_idx = ex_idx
            break
        return md

    def supportedDropActions(self):
        return Qt.MoveAction

    def canDropMimeData(self, data, action, row, col, parent):
        return data.hasFormat("application/x-kollo-exam")

    def dropMimeData(self, data, action, row, col, parent):
        if not data.hasFormat("application/x-kollo-exam"):
            return False
        try:
            payload = json.loads(bytes(data.data("application/x-kollo-exam")).decode("utf-8"))
            ex_idx = payload.get("ExamIdx")
            if ex_idx is None:
                return False
            # Drop in Parkplatz ist immer erlaubt. Wir setzen Raum = "".
            did = False
            # Undo: BEFORE-State aus aktuellem Plan ermitteln
            def find_item_state(dc: DataController, exam_idx: int) -> Dict[str, Any]:
                for it in dc.schedule:
                    if it.ExamIdx == exam_idx:
                        return {
                            "Woche": it.Woche, "Tag": it.Tag, "SlotIndex": it.SlotIndex,
                            "Uhrzeit": it.Uhrzeit, "Raum": it.Raum
                        }
                return {"Woche": None, "Tag": None, "SlotIndex": None, "Uhrzeit": None, "Raum": ""}
            before_state = find_item_state(self.dc, ex_idx)
            
            for it in self.dc.schedule:
                if it.ExamIdx == ex_idx:
                    # Punkt 3: Im Parkplatz darf kein Slot/Tag/Woche/Uhrzeit belegt bleiben
                    it.Raum = ""
                    it.Woche = None
                    it.Tag = None
                    it.SlotIndex = None
                    # Uhrzeit konsistent auf None setzen
                    self.dc.recompute_item_time(it)  # setzt auf None bei fehlenden Indizes
                    did = True
                    break
            if did:
                # AFTER-State: Parkplatz-Zustand
                after_state = {"Woche": None, "Tag": None, "SlotIndex": None, "Uhrzeit": None, "Raum": ""}
                # Zuerst globale Konflikte neu bewerten, dann Modelle/View aktualisieren
                self.dc.evaluate_conflicts()
                try:
                    self.dc.evaluate_fair_day_distribution()
                except Exception:
                    pass
                self._recalc()
                self.layoutChanged.emit()
                self.dc.dataChanged.emit()
                # Undo/Redo: MoveCommand pushen
                try:
                    self.dc.push_command(MoveExamCommand(ex_idx, before_state, after_state))
                    self.dc.uiRefreshRequested.emit()  # neu: UI soll Actions/Views sofort aktualisieren
                except Exception:
                    pass
                self.dropped.emit("In Parkplatz verschoben")
                return True
            return False
        except Exception as e:
            self.dropped.emit(f"Fehler beim Parken: {e}")
            return False
        finally:
            RightModel.current_drag_exam_idx = None

    def data(self, index, role):
        if not index.isValid():
            return None
        ex_idx = self.index_to_item(index.row(), index.column())
        if ex_idx is None:
            return None
            
        if role == Qt.BackgroundRole:
            # Temporäre violette Hervorhebung hat Vorrang
            if self._is_highlighted(ex_idx):
                return COLOR_HIGHLIGHT_VIOLET
            return COLOR_NORMAL
            
        if role == Qt.DisplayRole:
            ex = None
            for e in self.dc.exams:
                if e.idx == ex_idx:
                    ex = e
                    break
            if not ex:
                return ""
            line1 = ex.Schueler or ""
            line2 = f"{ex.Pruefer or ''} | {ex.Beisitzer or ''}"
            line3 = ex.Thema or ""
            return f"{line1}\n{line2}\n{line3}"
        if role == Qt.FontRole:
            return FONT_BLOCK
        return None

    def _is_highlighted(self, exam_idx: int) -> bool:
        mode = getattr(self.dc, "highlight_mode", None)
        value = getattr(self.dc, "highlight_value", None)
        if not mode or value is None:
            return False
        # Exam-Daten ermitteln
        ex = next((e for e in self.dc.exams if e.idx == exam_idx), None)
        if not ex:
            return False
        if mode == "pruefer":
            return (ex.Pruefer or "") == value
        if mode == "beisitzer":
            return (ex.Beisitzer or "") == value
        if mode == "schueler":
            return (ex.Schueler or "") == value
        if mode == "fach":
            f = (ex.Fach or "")
            m = re.match(r"^\d*([A-Za-z]+)\d*$", f)
            core = m.group(1).lower() if m else re.sub(r"\d+", "", f).lower()
            return core == value
        return False
        
class ParkingDelegate(QStyledItemDelegate):
    def __init__(self, dc: DataController, parent=None):
        super().__init__(parent)
        self.dc = dc
        self.font = FONT_BLOCK

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        # Hintergrund aus Model übernehmen (inkl. Highlight-Farbe)
        bg = index.data(Qt.BackgroundRole)
        if isinstance(bg, QColor):
            painter.fillRect(opt.rect, bg)
            # Optionaler grüner Rahmen wie im RightDelegate bei "erlaubt"
            if bg == COLOR_ALLOWED:
                pen = painter.pen()
                pen.setColor(QColor(80, 160, 80))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawRect(opt.rect.adjusted(1, 1, -1, -1))
        else:
            painter.fillRect(opt.rect, COLOR_NORMAL)

        # Kachelrahmen
        pen = painter.pen()
        pen.setColor(QColor(120, 120, 120))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(opt.rect.adjusted(1, 1, -1, -1))

        # Text
        painter.setFont(self.font)
        painter.setPen(Qt.black)
        text = index.data(Qt.DisplayRole) or ""
        inner = opt.rect.adjusted(8, 6, -8, -6)
        flags = Qt.AlignHCenter | Qt.AlignVCenter | Qt.TextWordWrap
        painter.drawText(inner, flags, text)

        # Keine Tagesabschlusslinie im Parkplatz
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        # gleiche Höhe wie in der rechten Tabelle, damit 3 Zeilen sauber passen
        return QSize(option.rect.width(), BLOCK_HEIGHT_MAX)
            
# -------------------------
# Solver-Worker für Thread
# -------------------------
class SolverWorker(QObject):
    finished = Signal(object, object)  # (schedule_rows, status)
    error = Signal(str)

    def __init__(self, dc: DataController):
        super().__init__()
        self.dc = dc

    def run(self):
        try:
            schedule_rows, status = self.dc.run_solver_background()
            self.finished.emit(schedule_rows, status)
        except Exception as e:
            self.error.emit(f"{e}\n{traceback.format_exc()}")

class ExportPlanOptionsDialog(QDialog):
        def __init__(self, parent=None, settings=None):
            super().__init__(parent)
            self.setWindowTitle("Export-Optionen")
            lay = QVBoxLayout(self)
            self.cb_teacher = QCheckBox("Plan für Lehrer", self)
            self.cb_teacher.setChecked(True)
            self.cb_students = QCheckBox("Plan für Schüler", self)
            self.cb_cleaning = QCheckBox("Plan für Reinigungspersonal", self)
            lay.addWidget(self.cb_teacher)
            lay.addWidget(self.cb_students)
            self.edit_students_note = QLineEdit(self)
            self.edit_students_note.setPlaceholderText("Text unter der Tagestabelle (ersetzt 'Vorbereitungsraum: <Raum>')")
            # Vorbelegen aus den planspezifischen Settings (falls vorhanden)
            try:
                if settings is not None and getattr(settings, "students_note_text", None):
                    self.edit_students_note.setText(settings.students_note_text or "")
            except Exception:
                pass
            lay.addWidget(self.edit_students_note)
            lay.addWidget(self.cb_cleaning)
            btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
            btn_box.accepted.connect(self.accept)
            btn_box.rejected.connect(self.reject)
            lay.addWidget(btn_box)

        def teacherChecked(self) -> bool:
            return self.cb_teacher.isChecked()

        def studentsChecked(self) -> bool:
            return self.cb_students.isChecked()

        def cleaningChecked(self) -> bool:
            return self.cb_cleaning.isChecked()

        def studentsNoteText(self) -> str:
            return (self.edit_students_note.text() or "").strip()

# -------------------------
# Hauptfenster
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KoPlaS - Kolloquium-Planungs-System")
        self.resize(QGuiApplication.primaryScreen().availableGeometry().size())
        self.showMaximized()

        self.dc = DataController()
        self.dc.logMessage.connect(self.on_log)
        self.dc.statusMessage.connect(self.on_status)

        # Neu: Undo/Redo-Action-State und UI-Refresh zentral aktualisieren
        self.dc.actionStateChanged.connect(self._update_undo_redo_actions)
        self.dc.uiRefreshRequested.connect(self._update_undo_redo_actions)
        # auf einen UI-Refresh nach Parking-Drops zusätzlich mit sanftem Refresh reagieren
        self.dc.uiRefreshRequested.connect(lambda: (self.rightView.viewport().update(), self.parkingView.viewport().update()))
        # Live-Update der Lehrkräftebelastung im geöffneten Dialog nach Settings-Änderung
        self.dc.dataChanged.connect(self._maybe_refresh_teachers_dialog)

        # Menü/Status
        self._build_menu()
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.status_label = QLabel("Bereit")
        # Linkes Status-Label als normales Widget, damit showMessage weiterhin sichtbar bleibt
        self.statusBar().addWidget(self.status_label)
        # Optional: kleinere Mindestbreite fr das linke Label
        self.status_label.setMinimumWidth(120)
        # Rechter Bereich: Zuerst Zählungs-Label, dann Dateiname (beide rechtsbndig)
        self.count_label = QLabel("")
        self.count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.statusBar().addPermanentWidget(self.count_label)
        self.file_label = QLabel("")
        self.file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.statusBar().addPermanentWidget(self.file_label)
        
        # Initial: Undo/Redo-Actions dem aktuellen Stack-Zustand anpassen
        # (falls bereits Kommandos geladen wurden)
        self._update_undo_redo_actions()
        
        # Initial: Dateiname-Label entsprechend dem aktuellen Zustand
        self._update_file_label()
        # Initial: Zählung setzen
        self._update_day_counts_label()
        
        # Optional: Placebo-Startmeldung
        #self.statusBar().showMessage("Bereit", 2000)
        
        # Hauptbereich
        central = QWidget()
        lay = QHBoxLayout(central)
        splitter = QSplitter(Qt.Horizontal)
        self.splitter = splitter

        self.leftView = QTableView()
        # Linke Tabelle: Zeilenhöhe fix wie rechts (z. B. 45 px)
        lvh = self.leftView.verticalHeader()
        lvh.setVisible(False)
        lvh.setDefaultSectionSize(BLOCK_HEIGHT_MAX)
        lvh.setMinimumSectionSize(BLOCK_HEIGHT_MIN)
        self.leftView.setModel(LeftModel(self.dc))
        self.leftView.setItemDelegate(LeftDelegate(self.dc, self.leftView))
        self.leftView.verticalHeader().setVisible(False)
        self.leftView.horizontalHeader().setStretchLastSection(True)
        self.leftView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.leftView.setEditTriggers(QTableView.NoEditTriggers)
        self.leftView.setSelectionMode(QTableView.NoSelection)
        self.leftView.setFixedWidth(260)
        self.leftView.setFont(FONT_DEFAULT)

        self.rightView = QTableView()
        rm = RightModel(self.dc)
        self.rightView.setModel(rm)
        self.rightView.setItemDelegate(RightDelegate(self.dc, self.rightView))
        
        hh = self.rightView.horizontalHeader()
        # Wichtig: Fixed, damit setColumnWidth greift
        hh.setSectionResizeMode(QHeaderView.Fixed)
        # Horizontales Scrollen ermglichen (fr Parkplatz mit >3 Kacheln)
        self.rightView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.rightView.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        # Header-Kontextmenü aktivieren
        try:
            hh = self.rightView.horizontalHeader()
            hh.setContextMenuPolicy(Qt.CustomContextMenu)
            hh.customContextMenuRequested.connect(self.on_rightview_header_context_menu)
        except Exception:
            pass

        # Jetzt Spaltenbreite setzen (z. B. halb so breit wie vorher)
        for i in range(max(1, len(rm.rooms))):
            # normale Rume: 150px, Parkplatz breiter fr 3 parallele Kacheln
            room_name = rm.rooms[i]
            if room_name == RightModel.PARKING_ROOM_NAME:
                self.rightView.setColumnWidth(i, 520)  # ca. 3 Kacheln + Abstnde
            else:
                self.rightView.setColumnWidth(i, 150)

        vh = self.rightView.verticalHeader()
        vh.setVisible(False)  # kann bleiben
        # setDefaultSectionSize greift sicher – wähle eine feste Pixelhöhe
        vh.setDefaultSectionSize(BLOCK_HEIGHT_MAX)  # Beispielwert ~ 3 Textzeilen; passe bei Bedarf an (z. B. 84 oder 96)
        vh.setMinimumSectionSize(BLOCK_HEIGHT_MIN)  # sinnvolle Untergrenze

        self.rightView.verticalHeader().setVisible(False)
        # DnD Einstellungen
        self.rightView.setSelectionBehavior(QTableView.SelectItems)
        self.rightView.setSelectionMode(QTableView.SingleSelection)
        self.rightView.setDragDropMode(QTableView.DragDrop)
        self.rightView.setDragEnabled(True)
        self.rightView.setAcceptDrops(True)
        self.rightView.setDropIndicatorShown(True)
        self.rightView.setDefaultDropAction(Qt.MoveAction)
        self.rightView.setFont(FONT_DEFAULT)
        self.rightView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Kontextmenü: Rechtsklick am Mauszeiger
        self.rightView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.rightView.customContextMenuRequested.connect(self.on_rightview_context_menu)


        # Synchrones vertikales Scrollen
        self.leftView.verticalScrollBar().valueChanged.connect(self.rightView.verticalScrollBar().setValue)
        self.rightView.verticalScrollBar().valueChanged.connect(self.leftView.verticalScrollBar().setValue)

        # Neue Parkplatz-View rechts vom Plan
        self.parkingView = QTableView()
        self.parkingModel = ParkingModel(self.dc)
        self.parkingView.setModel(self.parkingModel)
        self.parkingView.setItemDelegate(ParkingDelegate(self.dc, self.parkingView))
        # Fixe Breite VOR dem Hinzufügen zum Splitter setzen
        self.parkingView.setFixedWidth(160)
        self.parkingView.setMinimumWidth(160)
        self.parkingView.setMaximumWidth(160)
        self.parkingView.setSelectionBehavior(QTableView.SelectItems)
        self.parkingView.setSelectionMode(QTableView.SingleSelection)
        self.parkingView.setDragEnabled(True)
        self.parkingView.setAcceptDrops(True)
        self.parkingView.setDropIndicatorShown(True)
        self.parkingView.setDefaultDropAction(Qt.MoveAction)
        self.parkingView.verticalHeader().setVisible(False)
        # gleiche Zeilenhöhe wie der Plan, damit 3 Zeilen lesbar sind
        self.parkingView.verticalHeader().setDefaultSectionSize(BLOCK_HEIGHT_MAX)
        self.parkingView.verticalHeader().setMinimumSectionSize(BLOCK_HEIGHT_MIN)
        
        self.parkingView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.parkingView.setFont(FONT_DEFAULT)
        self.parkingView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Kontextmen fr Parkplatz
        self.parkingView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.parkingView.customContextMenuRequested.connect(self.on_parking_context_menu)

        # Einspaltig: eine Spalte breit genug für Blocktext
        for i in range(1):
            self.parkingView.setColumnWidth(i, 160)
        # Fixe Breite für die gesamte Parkplatz-View (nicht veränderbar)
        self.parkingView.setMinimumWidth(160)
        self.parkingView.setMaximumWidth(160)
        self.parkingView.setFixedWidth(160)
        # Optional: horizontales Scrollen deaktivieren (eine Spalte, feste Breite)
        self.parkingView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Optional: vertikales Scrollen nur bei Bedarf
        self.parkingView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        splitter.addWidget(self.leftView)
        splitter.addWidget(self.rightView)
        splitter.addWidget(self.parkingView)
        # Splitter-Stretch: linke und mittlere Ansicht dehnbar, Parkplatz fest
        splitter.setStretchFactor(0, 0)  # left fixed width (von setFixedWidth auf leftView nicht gesetzt, aber meist klein)
        splitter.setStretchFactor(1, 1)  # right (Plan) dehnbar
        splitter.setStretchFactor(2, 0)  # parkingView nicht dehnbar
        lay.addWidget(splitter)
        self.setCentralWidget(central)

        # Nach Aufbau: Layout erzwingen und Splitter-Geometrie setzen,
        # damit rechts keine grauen Flächen verbleiben
        self._init_splitter_sizes()

        # Signale
        rm.dropped.connect(self.on_drop_result)
        # Optional: Parkplatz-Meldungen nicht in die Statusleiste, um Drop-Meldungen nicht zu verdrängen
        # self.parkingModel.dropped.connect(lambda msg: self.statusBar().showMessage(msg, 3000))
        self.parkingModel.dropped.connect(lambda msg: None)
        self.dc.dataChanged.connect(self.refresh_views)
        # Nach jeder Datenänderung Zählung aktualisieren
        self.dc.dataChanged.connect(self._update_day_counts_label)

        # Log-Fenster
        self.logWin = LogWindow(self, self.dc)

        # Drag-Hover-Repaint drosseln (~30 FPS)
        self.rightView.viewport().setAttribute(Qt.WA_Hover, True)
        self._repaint_scheduled = False
        self.rightView.viewport().installEventFilter(self)
        self.examsDialog: Optional[ExamsDialog] = None

    def _init_splitter_sizes(self):
        """
        Setzt initiale Splittergrößen so, dass die parkingView exakt 160 px erhält
        und kein grauer Bereich entsteht. Danach ein force-Layout.
        """
        try:
            # Aktuelle Gesamtbreite des Splitters
            total_w = self.splitter.width() if self.splitter.width() > 0 else self.width()
            # Breite links (fix: 260), rechts (Plan) = Rest - 160
            left_w = 260
            park_w = 160
            plan_w = max(200, total_w - left_w - park_w)  # mindestens 200 px
            self.splitter.setSizes([left_w, plan_w, park_w])
            # Layout aktualisieren
            self.splitter.updateGeometry()
            self.splitter.repaint()
        except Exception:
            pass

    def eventFilter(self, obj, event):
        if obj is self.rightView.viewport():
            if event.type() in (QEvent.MouseMove, QEvent.HoverMove, QEvent.DragMove):
                if not self._repaint_scheduled:
                    self._repaint_scheduled = True
                    def do_update():
                        self._repaint_scheduled = False
                        self.rightView.viewport().update()
                    QTimer.singleShot(33, do_update)  # ~30fps
        return super().eventFilter(obj, event)

    def _build_menu(self):
        menubar = self.menuBar() or QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("Datei")
        act_open = QAction("Öffnen", self); act_open.triggered.connect(self.on_open)
        act_open.setShortcut(QKeySequence.StandardKey.Open)  # Ctrl+O
        # Klassisches Speichern: Ctrl+S -> direkt in last_open_path (falls vorhanden), sonst Save As
        act_save = QAction("Speichern", self); act_save.triggered.connect(self.on_save)
        act_save.setShortcut(QKeySequence.StandardKey.Save)  # Ctrl+S
        # Neu: "Speichern unter..."
        act_save_as = QAction("Speichern unter...", self); act_save_as.triggered.connect(self.on_save_as)
        # Ctrl+Shift+S als verbreiteter Shortcut fr "Speichern unter"
        act_save_as.setShortcut(QKeySequence("Ctrl+Shift+S"))
        file_menu.addActions([act_open, act_save, act_save_as])
        # Untermenü Export
        export_menu = file_menu.addMenu("Export")
        act_export_plan = QAction("Plan", self); act_export_plan.triggered.connect(self.on_export_plan)
        act_export_stats = QAction("Statistik", self); act_export_stats.triggered.connect(self.on_export_stats)
        act_export_table = QAction("Tabelle", self); act_export_table.triggered.connect(self.on_export_table)
        export_menu.addAction(act_export_plan)
        export_menu.addAction(act_export_stats)
        export_menu.addAction(act_export_table)
        act_quit = QAction("Beenden", self); act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

        # Bearbeiten-Menü: Undo/Redo
        edit_menu = menubar.addMenu("Bearbeiten")
        self.act_undo = QAction("Rückgängig", self)
        self.act_redo = QAction("Wiederholen", self)
        self.act_undo.setShortcut(QKeySequence.StandardKey.Undo)   # Ctrl+Z
        self.act_redo.setShortcut(QKeySequence.StandardKey.Redo)   # Ctrl+Y
        self.act_undo.triggered.connect(self.on_undo)
        self.act_redo.triggered.connect(self.on_redo)
        edit_menu.addAction(self.act_undo)
        edit_menu.addAction(self.act_redo)
        
        # Suchen
        self.act_search = QAction("Suchen", self)
        self.act_search.setShortcut(QKeySequence.StandardKey.Find)  # Ctrl+F / Cmd+F
        self.act_search.triggered.connect(self.on_search)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_search)
        
        self._update_undo_redo_actions()

        settings_menu = menubar.addMenu("Einstellungen")
        # Untermenü: Ausschüsse
        committees_menu = settings_menu.addMenu("Ausschüsse")
        act_import_exams = QAction("Prüfungen importieren", self); act_import_exams.triggered.connect(self.on_import)
        act_assign_committees = QAction("Ausschüsse besetzen", self); act_assign_committees.triggered.connect(self.on_committees)
        committees_menu.addAction(act_import_exams)
        committees_menu.addAction(act_assign_committees)
        # Untermenü: Lehrkräfte
        teachers_menu = settings_menu.addMenu("Lehrkräfte")
        act_teachers_import = QAction("Lehrkräfte importieren", self); act_teachers_import.triggered.connect(self.on_teachers_import)
        act_courses_import = QAction("Oberstufenkurse importieren", self); act_courses_import.triggered.connect(self.on_courses_import)
        act_teachers_load = QAction("Lehrkräftebelastung", self); act_teachers_load.triggered.connect(self.on_teachers)
        act_workload_params = QAction("Belastungsparameter", self); act_workload_params.triggered.connect(self.on_workload_params)

        teachers_menu.addAction(act_teachers_import)
        teachers_menu.addAction(act_courses_import)
        teachers_menu.addAction(act_teachers_load)
        teachers_menu.addAction(act_workload_params)

        # übrige Einstellungen
        act_rooms = QAction("Räume", self); act_rooms.triggered.connect(self.on_rooms)
        act_time = QAction("Zeit", self); act_time.triggered.connect(self.on_time)
        act_constraints = QAction("Bedingungen", self); act_constraints.triggered.connect(self.on_constraints)
        settings_menu.addActions([act_rooms, act_time, act_constraints])
        
        assign_menu = menubar.addMenu("Zuteilung")
        act_assign = QAction("Zuteilung starten", self); act_assign.triggered.connect(self.on_assign)
        act_errors = QAction("Logbuch", self); act_errors.triggered.connect(self.on_errors)
        assign_menu.addAction(act_assign)
        assign_menu.addAction(act_errors)

        help_menu = menubar.addMenu("Hilfe")
        act_info = QAction("Info", self); act_info.triggered.connect(self.menu_info)
        act_feedback = QAction("Feedback senden", self); act_feedback.triggered.connect(self.menu_send_feedback)
        help_menu.addAction(act_info)
        help_menu.addAction(act_feedback)

    # Menü-Handler
    def on_open(self):
        # Qt-eigenen (nicht-nativen) Dialog erzwingen, damit Qt-Übersetzungen greifen
        dlg = QFileDialog(self, "Öffnen", WORK_DIR)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["KolloPlan (*.kolloPlan)", "Alle Dateien (*)"])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # WICHTIG: Qt-Dialog statt macOS-Dialog
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
    
        # Warnen bei ungespeicherten Änderungen vor dem Laden einer neuen Datei
        if getattr(self.dc, "_dirty", False):
            ans = QMessageBox.question(
                self,
                "Ungespeicherte Änderungen",
                "Es liegen ungespeicherte Änderungen vor. Möchten Sie vor dem Öffnen speichern?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )
            if ans == QMessageBox.Cancel:
                return
            if ans == QMessageBox.Yes:
                self.on_save()
        try:
            self.dc.open_file(fn)
            self.refresh_views()
            # Dateiname nach erfolgreichem Laden aktualisieren
            self._update_file_label()
        except Exception as e:
            self.dc.report_error("Öffnen fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))
            
    def on_save(self):
        #Klassisches Speichern:
        #- Wenn ein Pfad vorhanden ist (self.dc.last_open_path), ohne Dialog dorthin speichern.
        #- Andernfalls Save-As-Dialog anzeigen.
        #Nach erfolgreichem Speichern wird der Dateiname rechts in der Statusleiste aktualisiert.
        target_path = getattr(self.dc, "last_open_path", None)
        if target_path and str(target_path).strip() != "":
            try:
                self.dc.save_file(target_path)
                self._update_file_label()
            except Exception as e:
                self.dc.report_error("Speichern fehlgeschlagen", e)
                QMessageBox.critical(self, "Fehler", str(e))
            return

        # Save As
        # vorhandener Pfad/Dateiname, falls bereits geffnet, sonst WORK_DIR/plan.kolloPlan
        suggested = getattr(self.dc, "last_open_path", None)
        start_path = suggested if (suggested and str(suggested).strip() != "") else os.path.join(WORK_DIR, "plan.kolloPlan")
        dlg = QFileDialog(self, "Speichern", start_path)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["KolloPlan (*.kolloPlan)"])
        dlg.setDefaultSuffix("kolloPlan")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, False)

        if not dlg.exec():
            return

        fn = dlg.selectedFiles()[0]

        try:
            self.dc.save_file(fn)
            self._update_file_label()
        except Exception as e:
            self.dc.report_error("Speichern fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))

    def on_save_as(self):
        """
        Speichern unter:
        - Öffnet immer einen Dateidialog mit dem aktuell geffneten Pfad/Dateinamen als Vorschlag (falls vorhanden),
          sonst WORK_DIR/plan.kolloPlan.
        - Nach erfolgreichem Speichern wird last_open_path auf den neuen Pfad gesetzt,
          das Statusleisten-Label aktualisiert und zukünftiges 'Speichern' schreibt ohne Dialog in diese Datei.
        - Ungespeicherte Änderungen werden direkt in die neue Datei geschrieben; die alte Datei bleibt unverändert.
        """
        # Vorschlag: vorhandener Pfad/Dateiname (falls vorhanden), sonst WORK_DIR/plan.kolloPlan
        suggested = getattr(self.dc, "last_open_path", None)
        start_path = suggested if (suggested and str(suggested).strip() != "") else os.path.join(WORK_DIR, "plan.kolloPlan")
        dlg = QFileDialog(self, "Speichern unter", start_path)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["KolloPlan (*.kolloPlan)"])
        dlg.setDefaultSuffix("kolloPlan")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, False)

        if not dlg.exec():
            return

        fn = dlg.selectedFiles()[0]
        try:
            # Speichern in die neue Datei (setzt in save_file bereits last_open_path und _dirty = False)
            self.dc.save_file(fn)
            # Datei-Pfad-Anzeige aktualisieren
            self._update_file_label()
        except Exception as e:
            self.dc.report_error("Speichern unter fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))
      
    def on_import(self):
        # Qt-eigenen (nicht-nativen) Dialog erzwingen
        start_dir = self.dc.last_csv_dir or ""
        dlg = QFileDialog(self, "Prüfungen-CSV wählen", start_dir)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["CSV (*.csv)", "Alle Dateien (*)"])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # Qt-Dialog statt nativer macOS-Dialog
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
    
        try:
            self.dc.import_csv(fn)
            self.dc.last_csv_dir = os.path.dirname(fn)
            self.refresh_views()
            # Nach Import automatisch den Exams-Dialog zur Prüfung/Weiterbearbeitung öffnen
            self.on_committees()
        except Exception as e:
            self.dc.report_error("CSV-Import fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))
        
    def on_export_plan(self):
        if not self.dc.schedule:
            QMessageBox.information(self, "Hinweis", "Kein Plan vorhanden. Bitte lösen oder laden.")
            return
        dlg_opts = ExportPlanOptionsDialog(self, settings=self.dc.settings)
        if dlg_opts.exec() != QDialog.Accepted:
            return
        sel_teacher = dlg_opts.teacherChecked()
        sel_students = dlg_opts.studentsChecked()
        sel_cleaning = dlg_opts.cleaningChecked()
        students_note_text = dlg_opts.studentsNoteText()
        # Planspezifisch und persistent im Settings-Objekt ablegen
        try:
            # defensiv: Attribut bei älteren Dateien ggf. noch nicht vorhanden
            if not hasattr(self.dc.settings, "students_note_text"):
                setattr(self.dc.settings, "students_note_text", "")
            self.dc.settings.students_note_text = students_note_text
            # Änderung sicher als „dirty“ markieren und Views/Signals aktualisieren
            self.dc.mark_dirty_and_emit()
            # optional: Statusmeldung, kein erzwungenes Autosave
            self.status("Hinweistext für Schüler im Plan gespeichert.")
        except Exception:
            pass

        if not (sel_teacher or sel_students or sel_cleaning):
            return

        from datetime import datetime
        year = datetime.now().year

        # Option 1: Lehrer
        if sel_teacher:
            start_path = os.path.join(WORK_DIR, f"Kolloquiumsplan_{year}_LK.docx")
            dlg = QFileDialog(self, "Export Plan (Lehrer) DOCX", start_path)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setNameFilters(["Word (*.docx)"])
            dlg.setDefaultSuffix("docx")
            dlg.setOption(QFileDialog.DontUseNativeDialog, True)
            dlg.setOption(QFileDialog.DontConfirmOverwrite, False)

            if dlg.exec():
                fn = dlg.selectedFiles()[0]
                try:
                    self.dc.export_docx(fn)
                except Exception as e:
                    self.dc.report_error("Export Plan (Lehrer) fehlgeschlagen", e)
                    QMessageBox.critical(self, "Fehler", str(e))

        # Option 2: Schüler
        if sel_students:
            start_path = os.path.join(WORK_DIR, f"Kolloquiumsplan_{year}_SuS.docx")
            dlg = QFileDialog(self, "Export Plan (Schüler) DOCX", start_path)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setNameFilters(["Word (*.docx)"])
            dlg.setDefaultSuffix("docx")
            dlg.setOption(QFileDialog.DontUseNativeDialog, True)
            dlg.setOption(QFileDialog.DontConfirmOverwrite, False)

            if dlg.exec():
                fn = dlg.selectedFiles()[0]
                try:
                    self.dc.export_docx_students(fn, students_note_text=students_note_text)
                except Exception as e:
                    self.dc.report_error("Export Plan (Schüler) fehlgeschlagen", e)
                    QMessageBox.critical(self, "Fehler", str(e))

        # Option 3: Reinigung
        if sel_cleaning:
            start_path = os.path.join(WORK_DIR, f"Kolloquiumsplan_{year}_Reinigung.docx")
            dlg = QFileDialog(self, "Export Plan (Reinigungspersonal) DOCX", start_path)
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            dlg.setFileMode(QFileDialog.AnyFile)
            dlg.setNameFilters(["Word (*.docx)"])
            dlg.setDefaultSuffix("docx")
            dlg.setOption(QFileDialog.DontUseNativeDialog, True)
            dlg.setOption(QFileDialog.DontConfirmOverwrite, False)

            if dlg.exec():
                fn = dlg.selectedFiles()[0]
                try:
                    self.dc.export_docx_cleaning(fn)
                except Exception as e:
                    self.dc.report_error("Export Plan (Reinigungspersonal) fehlgeschlagen", e)
                    QMessageBox.critical(self, "Fehler", str(e))
   
    def on_export_stats(self):
        if not self.dc.schedule:
            QMessageBox.information(self, "Hinweis", "Kein Plan vorhanden. Bitte lösen oder laden.")
            return
    
        start_path = os.path.join(WORK_DIR, "kolloquiumsplan_report.docx")
        dlg = QFileDialog(self, "Export Statistik (DOCX)", start_path)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Word (*.docx)"])
        dlg.setDefaultSuffix("docx")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, False)
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
        try:
            self.dc.report_docx(fn, "Kolloquiumsplan  Statistik")
        except Exception as e:
            self.dc.report_error("Export Statistik fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))
    
    def on_export_table(self):
        if not self.dc.schedule:
            QMessageBox.information(self, "Hinweis", "Kein Plan vorhanden. Bitte lösen oder laden.")
            return
    
        start_path = os.path.join(WORK_DIR, "kolloquiumsplan.xlsx")
        dlg = QFileDialog(self, "Export Tabelle (XLSX)", start_path)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Excel (*.xlsx)"])
        dlg.setDefaultSuffix("xlsx")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, False)
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
        try:
            self.dc.export_xlsx(fn)
        except Exception as e:
            self.dc.report_error("Export Tabelle fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))
            
    def on_teachers(self):
        if not self.dc.teachers:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst Lehrkräfte oder Oberstufenkurse importieren oder die korrekte Importdatei wählen.")
            return
        dlg = TeachersDialog(self, self.dc)
        dlg.exec()

    def on_teachers_import(self):
        # Qt-eigenen (nicht-nativen) Dialog erzwingen
        start_dir = self.dc.last_csv_dir or ""
        dlg = QFileDialog(self, "Lehrkräfte-CSV wählen", start_dir)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["CSV (*.csv)", "Alle Dateien (*)"])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
    
        try:
            from import_asv import read_teachers_asv
            rows = read_teachers_asv(fn)
            # Zusammenführen statt Ersetzen:
            by_code: Dict[str, Teacher] = {}
            for t in getattr(self.dc, "teachers", []):
                code = (t.Lehrkraft or "").strip()
                if code:
                    by_code[code] = t
    
            for r in rows or []:
                code = (r.get("Lehrkraft") or "").strip()
                upz_csv = (r.get("UPZ") or "").strip()
                if not code:
                    continue
                if code in by_code:
                    if upz_csv != "":
                        by_code[code].UPZ = upz_csv
                else:
                    by_code[code] = Teacher(Lehrkraft=code, UPZ=upz_csv, WS="", S="", K="", Belastung="")
    
            self.dc.teachers = list(by_code.values())
            self.dc._rebuild_teacher_index()
            self.dc.last_csv_dir = os.path.dirname(fn)
            self.dc.status(f"{len(rows or [])} Lehrkräfte importiert/aktualisiert")
    
            try:
                self.dc.count_beisitzer()
            except Exception:
                pass
            try:
                self.dc.calculate_belastung()
            except Exception:
                pass
            # Importierte Lehrkräftedaten sind Bestandteil des Plans und müssen gespeichert werden.
            self.dc._dirty = True
            self.dc.dataChanged.emit()
            self.on_teachers()
        except Exception as e:
            self.dc.report_error("Lehrkräfte-Import fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))

    def on_courses_import(self):
        # Qt-eigenen (nicht-nativen) Dialog erzwingen
        start_dir = self.dc.last_csv_dir or ""
        dlg = QFileDialog(self, "Oberstufenkurse-CSV wählen", start_dir)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["CSV (*.csv)", "Alle Dateien (*)"])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
    
        if not dlg.exec():
            return
    
        fn = dlg.selectedFiles()[0]
    
        try:
            from import_asv import read_courses
            course_rows = read_courses(fn)  # Keys: Lehrkraft, WS, S, K, school_name

            # Konsistentes Verhalten wie bei on_teachers_import/on_import:
            # Wenn keine verwertbaren Kursdaten geliefert wurden, Statuswarnung und Abbruch,
            # ohne Logbucheintrag und ohne Dialogöffnung.
            if not course_rows:
                self.dc.status(f"{len(course_rows or [])} Kurse importiert")
                self.on_teachers()
                return
 
            by_code: Dict[str, Teacher] = {}
            for t in getattr(self.dc, "teachers", []):
                code = (t.Lehrkraft or "").strip()
                if code:
                    by_code[code] = t
    
            # innerhalb EINES Imports aggregieren, nicht über mehrere Imports hinweg
            current: Dict[str, Dict[str, int]] = {}
            for r in course_rows or []:
                code = (r.get("Lehrkraft") or "").strip()
                if not code:
                    continue
                def to_int_safe(v) -> int:
                    try:
                        s = str(v).strip()
                        return int(s) if s != "" else 0
                    except Exception:
                        return 0
                ws_val = to_int_safe(r.get("WS", 0))
                s_val  = to_int_safe(r.get("S", 0))
                k_val  = to_int_safe(r.get("K", 0))
                prev = current.get(code, {"WS": 0, "S": 0, "K": 0})
                prev["WS"] += ws_val
                prev["S"]  += s_val
                prev["K"]  += k_val
                current[code] = prev
    
            for code, sums in current.items():
                t = by_code.get(code)
                if not t:
                    by_code[code] = Teacher(
                        Lehrkraft=code,
                        UPZ="",
                        WS=str(sums["WS"]),
                        S=str(sums["S"]),
                        K=str(sums["K"]),
                        Belastung=""
                    )
                else:
                    t.WS = str(sums["WS"])
                    t.S  = str(sums["S"])
                    t.K  = str(sums["K"])
    
            self.dc.teachers = list(by_code.values())
            self.dc._rebuild_teacher_index()
            self.dc.last_csv_dir = os.path.dirname(fn)
    
            try:
                sn = next((r.get("school_name") for r in (course_rows or []) if (r.get("school_name") or "").strip() != ""), "")
                if sn:
                    self.dc.school_name = sn
            except Exception:
                pass
    
            try:
                self.dc.count_beisitzer()
            except Exception:
                pass
            try:
                self.dc.calculate_belastung()
            except Exception:
                pass
    
            self.dc.status(f"{len(course_rows or [])} Kurse importiert")
            # Importierte Kurs- und Lehrkräftedaten sind Bestandteil des Plans.
            self.dc._dirty = True
            self.dc.dataChanged.emit()
            self.on_teachers()
        except Exception as e:
            self.dc.report_error("Kurs-Import fehlgeschlagen", e)
            QMessageBox.critical(self, "Fehler", str(e))

    def on_committees(self):
        if not self.dc.exams:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst Prüfungen importieren oder die korrekte Importdatei wählen.")
            return
        dlg = ExamsDialog(self, self.dc)
        dlg.exec()
        # Nach Rückkehr aus dem Dialog Konflikte neu bewerten und Views refreshen
        self.dc.evaluate_conflicts()
        self.refresh_views()

    def on_rooms(self):
        dlg = RoomsDialog(self, self.dc.settings.rooms)
        # bestehenden Vorbereitungsraum in Dialog übernehmen
        try:
            dlg.set_prepare_room(getattr(self.dc.settings, "prepare_room", "") or "")
        except Exception:
            pass
        if dlg.exec() == QDialog.Accepted:
            old_rooms = list(self.dc.settings.rooms or [])
            new_rooms = dlg.get_rooms() or [""]
            prepare_room_new = dlg.get_prepare_room() or ""
            prepare_room_old = getattr(self.dc.settings, "prepare_room", "") or ""

            # Räume, die entfernt würden (ausgenommen leerer Platzhalter)
            removed = [r for r in old_rooms if r and r not in new_rooms]

            # Prüfen, ob entfernte Räume in der aktuellen Planung belegt sind
            conflicts = []
            if removed:
                for it in self.dc.schedule or []:
                    room = (it.Raum or "").strip()
                    if room in removed:
                        conflicts.append(room)
                # eindeutige Konflikträume
                conflicts = sorted(set(conflicts))

            if conflicts:
                # Warnung und Änderung NICHT übernehmen
                QMessageBox.warning(
                    self,
                    "Räume können nicht gelöscht werden",
                    "Die folgenden Räume sind aktuell in der Planung belegt und können nicht gelöscht werden:\n\n"
                    + "\n".join(conflicts)
                    + "\n\nBitte verschieben Sie die betroffenen Prüfungen oder parken Sie sie, bevor Sie die Räume entfernen."
                )
                return

            # Wenn keine Konflikte: Änderungen bernehmen
            # Vorbereitungsraum NICHT undo-fähig -> direkt setzen
            self.dc.settings.prepare_room = prepare_room_new
            # Raumliste als ein Undo-Schritt setzen
            if new_rooms != old_rooms:
                cmd = RoomsListChangeCommand(old_rooms, new_rooms)
                cmd.apply(self.dc)
                self.dc.push_command(cmd)
            else:
                # dennoch View refreshen, falls nur prepare_room geändert wurde
                self.dc.dataChanged.emit()
            self.refresh_views()
            # Dirty-Flag setzen, falls sich prepare_room tatsächlich geändert hat
            if (prepare_room_new or "") != (prepare_room_old or ""):
                self.dc.mark_dirty_and_emit()
            
    def on_time(self):
        dlg = TimeDialog(self, self.dc.settings.time)
        if dlg.exec() == QDialog.Accepted:
            old_time = self.dc.settings.time
            new_time = dlg.apply()
            self.dc.settings.time = new_time
            self.dc.dataChanged.emit()
            self.refresh_views()
            # Dirty-Flag nur setzen, wenn sich etwas geändert hat
            try:
                changed = False
                # Versuche feldweisen Vergleich gängiger Attribute
                for attr in ("n_slots", "start_time", "slot_len_min", "break_len_min", "week1_date", "week2_date"):
                    if getattr(old_time, attr, None) != getattr(new_time, attr, None):
                        changed = True
                        break
                # Fallback: falls verfügbar, dict- oder repr-Vergleich
                if not changed:
                    if getattr(old_time, "__dict__", None) is not None and getattr(new_time, "__dict__", None) is not None:
                        changed = old_time.__dict__ != new_time.__dict__
                    else:
                        changed = repr(old_time) != repr(new_time)
                if changed:
                    self.dc.mark_dirty_and_emit()
            except Exception:
                # Bei Vergleichsproblem: sicherheitshalber als geändert markieren
                self.dc.mark_dirty_and_emit()

    def on_constraints(self):
        dlg = ConstraintsDialog(self, self.dc.settings.constraints)
        if dlg.exec() == QDialog.Accepted:
            old_c = self.dc.settings.constraints
            new_c = dlg.apply()
            self.dc.settings.constraints = new_c
            # Nach dem Übernehmen der Constraints: Konflikte neu bewerten und Anzeige aktualisieren
            self.dc.evaluate_conflicts()
            # Faire Tagesverteilung neu bewerten
            try:
                self.dc.evaluate_fair_day_distribution()
            except Exception:
                pass
            self.dc.dataChanged.emit()
            self.refresh_views()
            # Dirty-Flag nur setzen, wenn sich etwas geändert hat
            try:
                changed = False
                if getattr(old_c, "__dict__", None) is not None and getattr(new_c, "__dict__", None) is not None:
                    changed = old_c.__dict__ != new_c.__dict__
                else:
                    changed = repr(old_c) != repr(new_c)
                if changed:
                    self.dc.mark_dirty_and_emit()
            except Exception:
                self.dc.mark_dirty_and_emit()

    def on_assign(self):
        if not self.dc.exams:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst Prüfungen importieren.")
            return
        self.logWin.show()
        self.dc.status("Solver gestartet...")

        # Thread + Worker starten
        self.thread = QThread(self)
        self.worker = SolverWorker(self.dc)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_solver_finished)
        self.worker.error.connect(self._on_solver_error)
        # Thread beenden/aufräumen
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_solver_finished(self, schedule_rows, status):
        # Plan in GUI bernehmen
        # Wichtig: Items ohne zugewiesenen Raum (leer/None) sind "geparkt" und
        # erhalten Woche/Tag/SlotIndex/Uhrzeit = None sowie Raum = "".
        self.dc.schedule = []
        for r in schedule_rows:
            raum_in = r.get("Raum")
            is_parking = (raum_in is None) or (str(raum_in).strip() == "")
            if is_parking:
                woche = None
                tag = None
                slot = None
                raum_out = ""
            else:
                woche = r.get("Woche")
                tag = r.get("Tag")
                slot = r.get("SlotIndex")
                raum_out = raum_in
            self.dc.schedule.append(ScheduleItem(
                ExamIdx=r.get("ExamIdx"),
                Schueler=r.get("Schueler"),
                Fach=r.get("Fach"),
                Thema=r.get("Thema"),
                Pruefer=r.get("Pruefer"),
                Beisitzer=r.get("Beisitzer"),
                Woche=woche,
                Tag=tag,
                SlotIndex=slot,
                Raum=raum_out
            ))
        # Nach Solverlauf Konflikte berechnen
        self.dc.evaluate_conflicts()
        # Faire Tagesverteilung neu bewerten
        self.dc.evaluate_fair_day_distribution()
        self.dc.dataChanged.emit()
        self.dc.status("Zuteilung abgeschlossen.")
        self.refresh_views()
        # Nach Solverlauf gilt der neue Plan als geändert
        self.dc._dirty = True
        # Zählung nach Solverlauf aktualisieren
        self._update_day_counts_label()

    def _apply_after_undo_redo(self, msg: Optional[str]):
        # Nach Undo/Redo: Konflikte neu, Views aktualisieren, Status zeigen
        self.dc.clear_highlight()
        self.dc.evaluate_conflicts()
        self.dc.evaluate_fair_day_distribution()
        # Sicherstellen, dass alle geplanten Items eine konsistente Uhrzeit haben
        try:
            for it in getattr(self.dc, "schedule", []) or []:
                self.dc.recompute_item_time(it)
        except Exception:
            pass
        self.dc.dataChanged.emit()
        self.refresh_views()
        if msg:
            self.statusBar().showMessage(msg, 4000)
        self._update_undo_redo_actions()
        # Undo/Redo bedeutet geänderte Daten (bis zum nächsten Speichern)
        self.dc._dirty = True
        # Zählung aktualisieren
        self._update_day_counts_label()

    def on_undo(self):
        msg = self.dc.undo()
        self._apply_after_undo_redo(msg)

    def on_redo(self):
        msg = self.dc.redo()
        self._apply_after_undo_redo(msg)

    def on_search(self):
        dlg = SearchDialog(self)
        if dlg.exec() == QDialog.Accepted:
            crit = dlg.criteria()
            if not crit:
                return
            # Highlight-Modus "search" aktivieren, Wert ist das Kriterien-Dict
            self.dc.highlight_mode = "search"
            self.dc.highlight_value = crit
            # Views aktualisieren
            self.refresh_views()
            self.statusBar().showMessage("Suchhervorhebung aktiv", 6000)

    def _update_undo_redo_actions(self):
        can_u = self.dc.can_undo()
        can_r = self.dc.can_redo()
        if hasattr(self, "act_undo"):
            self.act_undo.setEnabled(can_u)
        if hasattr(self, "act_redo"):
            self.act_redo.setEnabled(can_r)

    def _on_solver_error(self, msg: str):
        self.dc.report_error("Solver-Fehler", Exception(msg))
        QMessageBox.critical(self, "Fehler", msg)

    def on_errors(self):
        self.logWin.show()

    def menu_send_feedback(self):
        try:
            from PySide6.QtGui import QDesktopServices
            from PySide6.QtCore import QUrl
            QDesktopServices.openUrl(QUrl("mailto:guenther.klauser@chgts.de"))
        except Exception:
            QMessageBox.critical(self, "Fehler", "Konnte das E-Mail-Programm nicht öffnen.")

    # Menü-Handler – Einstellungen -> Lehrkräfte -> Belastungsparameter
    def on_workload_params(self):
        try:
            dlg = WorkloadDialog(self, self.dc)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Dialog konnte nicht erstellt werden:\n{e}")
            return
        if dlg.exec():
            # Werte wurden bereits im Dialog in dc.settings geschrieben.
            # Belastung neu berechnen und UI aktualisieren
            try:
                self.dc.calculate_belastung()
            except Exception:
                pass
            # Falls TeachersDialog offen ist: soft refresh
            self._maybe_refresh_teachers_dialog()
            # Dirty-Flag setzen analog anderer Settings-Dialoge
            self.dc._dirty = True

    # Hilfsfunktion – falls TeachersDialog offen, neu laden/auffrischen
    def _maybe_refresh_teachers_dialog(self):
        try:
            # Durch Kinder gehen und TeachersDialog finden
            for w in self.findChildren(QWidget):
                if isinstance(w, TeachersDialog):
                    # einfache Aktualisierung: dc.calculate_belastung schon erfolgt,
                    # wir stoßen ein Daten-Refresh im Dialog an
                    if hasattr(w, "_load_teachers"):
                        w._load_teachers()
                    break
        except Exception:
            pass
     
    def menu_info(self):
        try:
            dlg = QDialog(self)
            dlg.setWindowTitle("Info")
            dlg.resize(370, 360)
            layout = QVBoxLayout(dlg)

            title = QLabel("KoPlaS – Kolloquium-Planungs-System")
            title.setWordWrap(True)
            title.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout.addWidget(title)

            txt = QTextEdit()
            txt.setReadOnly(True)
            txt.setPlainText(
                "KoPlaS\n\n"
                "Version: " + Version + "\n"
                "Software zur Planung der Kolloquiumsprüfungen in der PuLSt des bayerischen Gymnasiums.\n"
                "Funktionen: Datenimport aus ASV, Solver-basierte Zeitzuteilung mit Raumoptimierung (CP-SAT und MIP Solver - verwendetes Paktet: ortools), manuelle Anpassungen mit Livevorschau und Prüfen der Rahmenbedingungen, Export als Wordplan, Statistik und Belastungsanalyse.\n\n"
                 "Python-Quellcode ist beim Verfasser erhältlich.\n\n"
                "Entwickelt für schulische Einsatzszenarien. Lizensiert unter CC BY-NC 3.0 DE\n\n"
                "Kontakt/Feedback: guenther.klauser@chgts.de\n"
            )
            layout.addWidget(txt)

            btn = QPushButton("Schließen")
            btn.clicked.connect(dlg.accept)
            layout.addWidget(btn)

            dlg.exec()
        except Exception:
            QMessageBox.critical(self, "Fehler", "Info-Fenster konnte nicht geöffnet werden.")

    def on_drop_result(self, row: int, col: int, exam_idx: int, msg: str):
        self.statusBar().showMessage(msg, 5000)
        # Nach einem erfolgreichen Move: temporre Hervorhebung deaktivieren
        self.dc.clear_highlight()
        self.dc.evaluate_conflicts()
        self.dc.evaluate_fair_day_distribution()
        self.dc.dataChanged.emit()
        self._update_undo_redo_actions()
        # Zählung aktualisieren
        self._update_day_counts_label()

    # Dateiname wird hier bewusst nicht aktualisiert (kein Dateiwechsel/-speichern)
    # -------------------------
    # Helfer: Dateiname in Statusleiste aktualisieren
    # -------------------------
    def _update_file_label(self):
        #Setzt das rechte, permanente Status-Label auf den Basename der aktuell geffneten Datei.
        #Wenn kein Pfad vorhanden ist, bleibt das Label leer.
        try:
            path = getattr(self.dc, "last_open_path", None)
            if path and str(path).strip() != "":
                name = os.path.basename(str(path))
                self.file_label.setText(name)
            else:
                self.file_label.setText("")
        except Exception:
            try:
                self.file_label.setText("")
            except Exception:
                pass

    def _update_day_counts_label(self):
        """
        Baut den Text 'Woche 1: a|b|c|d|e - Woche 2: f|g|h|i|j' anhand der
        vollständig geplanten Prüfungen (Woche, Tag, SlotIndex, Uhrzeit gesetzt und Raum != "").
        Zeigt den Text links vom Dateinamen, getrennt durch ' | ' (vom Dateinamen).
        """
        try:
            # Zähler initialisieren
            w1 = [0, 0, 0, 0, 0]  # Mo..Fr
            w2 = [0, 0, 0, 0, 0]
            for it in getattr(self.dc, "schedule", []) or []:
                if (
                    it.Woche is not None and
                    it.Tag is not None and
                    it.SlotIndex is not None and
                    (it.Raum or "") != ""
                ):
                    try:
                        d_idx = DAY_INDEX.get(str(it.Tag), None)
                        if d_idx is None:
                            continue
                        if int(it.Woche) == 1:
                            w1[d_idx] += 1
                        elif int(it.Woche) == 2:
                            w2[d_idx] += 1
                    except Exception:
                        continue
            txt = f"Woche 1: {w1[0]}|{w1[1]}|{w1[2]}|{w1[3]}|{w1[4]} - Woche 2: {w2[0]}|{w2[1]}|{w2[2]}|{w2[3]}|{w2[4]}"
            # Der Trenner zum Dateinamen wird im Layout durch die Reihenfolge der Permanent-Widgets erreicht.
            # Hier nur den Zähltext selbst setzen.
            self.count_label.setText(txt)
        except Exception:
            # Fallback: leeren Text setzen
            try:
                self.count_label.setText("")
            except Exception:
                pass

    def on_log(self, msg: str):
        # Optional: Log nicht in die Statusleiste schreiben, um User-Feedback (Drop) nicht zu überdecken
        # self.statusBar().showMessage(msg, 1500)
        # Oder: nur im LogWindow anzeigen (bereits der Fall), hier nichts tun:
        pass

    def on_status(self, msg: str):
        self.status_label.setText(msg)

    def refresh_views(self):
        self.leftView.setModel(LeftModel(self.dc))
        rm = RightModel(self.dc)
        rm.dropped.connect(self.on_drop_result)
        self.rightView.setModel(rm)
        self.rightView.setItemDelegate(RightDelegate(self.dc, self.rightView))
        self.rightView.verticalHeader().setVisible(False)
        self.rightView.verticalHeader().setDefaultSectionSize(BLOCK_HEIGHT_MAX)
        self.rightView.verticalHeader().setMinimumSectionSize(BLOCK_HEIGHT_MIN)
        self.rightView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.rightView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.rightView.setHorizontalScrollMode(QTableView.ScrollPerPixel)
        
        hh = self.rightView.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Fixed)
        for i in range(max(1, len(rm.rooms))):
            room_name = rm.rooms[i]
            self.rightView.setColumnWidth(i, 150)
        # Header-Kontextmenü auch nach Model-Wechsel erneut sicherstellen
        try:
            hh.setContextMenuPolicy(Qt.CustomContextMenu)
            hh.customContextMenuRequested.connect(self.on_rightview_header_context_menu)
        except Exception:
            pass

        # Parkplatz-View aktualisieren
        self.parkingModel = ParkingModel(self.dc)
        self.parkingModel.dropped.connect(lambda msg: self.statusBar().showMessage(msg, 3000))
        self.parkingView.setModel(self.parkingModel)
        self.parkingView.setItemDelegate(ParkingDelegate(self.dc, self.parkingView))
        self.parkingView.verticalHeader().setVisible(False)
        self.parkingView.verticalHeader().setDefaultSectionSize(BLOCK_HEIGHT_MAX)
        self.parkingView.verticalHeader().setMinimumSectionSize(BLOCK_HEIGHT_MIN)
        self.parkingView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        for i in range(1):
            self.parkingView.setColumnWidth(i, 160)
        self._update_undo_redo_actions()
        # Nach Refresh auch faire Tagesverteilung neu bewerten (falls UI-nderungen vorher)
        try:
            self.dc.evaluate_fair_day_distribution()
        except Exception:
            pass
        # Nach Refresh sicherstellen, dass das Dateiname-Label dem aktuellen Pfad entspricht
        self._update_file_label()
        # Zählung aktualisieren
        self._update_day_counts_label()

    def on_rightview_context_menu(self, pos):
        index = self.rightView.indexAt(pos)
        if not index.isValid():
            return
        rm: RightModel = self.rightView.model()
        if not hasattr(rm, "rows") or not hasattr(rm, "rooms"):
            return
        w, d, s = rm.rows[index.row()]
        room = rm.rooms[index.column()]
        cell = rm.cell_map.get((w, d, s, room))
        if cell is None:
            return
        ex = None
        for e in self.dc.exams:
            if e.idx == cell:
                ex = e
                break
        if not ex:
            return
        menu = QMenu(self)
        act_pruefer = QAction("Gleicher Prüfer", self)
        act_pruefer_as_beis = QAction("Gleicher Prüfer als Beisitzer", self)
        act_beis = QAction("Gleicher Beisitzer", self)
        act_beis_as_pruefer = QAction("Gleicher Beisitzer als Prüfer", self)
        act_schueler = QAction("Gleicher Schüler", self)
        act_fach = QAction("Gleiches Fach", self)
        act_edit_beis = QAction("Beisitzer ändern", self)

        # Reihenfolge: Prüfer, Prüfer als Beisitzer, Beisitzer, Beisitzer als Prüfer, Schler, Fach
        menu.addAction(act_pruefer)
        menu.addAction(act_pruefer_as_beis)
        menu.addAction(act_beis)
        menu.addAction(act_beis_as_pruefer)
        menu.addAction(act_schueler)
        menu.addAction(act_fach)
        menu.addSeparator(); menu.addAction(act_edit_beis)

        chosen = menu.exec(self.rightView.viewport().mapToGlobal(pos))
        if not chosen:
            return
        if chosen == act_pruefer and ex.Pruefer:
            self.dc.highlight_mode = "pruefer"
            self.dc.highlight_value = ex.Pruefer
        elif chosen == act_pruefer_as_beis and ex.Pruefer:
            # Alle Blöcke highlighten, wo Beisitzer == aktueller Prüfer
            self.dc.highlight_mode = "beisitzer"
            self.dc.highlight_value = ex.Pruefer
        elif chosen == act_beis and (ex.Beisitzer or "").strip() != "":
            self.dc.highlight_mode = "beisitzer"
            self.dc.highlight_value = (ex.Beisitzer or "").strip()
        elif chosen == act_beis_as_pruefer and (ex.Beisitzer or "").strip() != "":
            # Alle Blöcke highlighten, wo Prüfer == aktueller Beisitzer
            self.dc.highlight_mode = "pruefer"
            self.dc.highlight_value = (ex.Beisitzer or "").strip()
        elif chosen == act_schueler and ex.Schueler:
            self.dc.highlight_mode = "schueler"
            self.dc.highlight_value = ex.Schueler
        elif chosen == act_fach and ex.Fach:
            m = re.match(r"^\d*([A-Za-z]+)\d*$", ex.Fach)
            core = m.group(1).lower() if m else re.sub(r"\d+", "", ex.Fach).lower()
            if core:
                self.dc.highlight_mode = "fach"
                self.dc.highlight_value = core
            else:
                return
        elif chosen == act_edit_beis:
            # Exams-Dialog öffnen (falls nicht offen) und auf die Zeile mit ex.idx fokussieren
            try:
                if self.examsDialog is None:
                    self.examsDialog = ExamsDialog(self, self.dc)
                    # Beim Schließen Referenz zurücksetzen
                    def on_closed():
                        self.examsDialog = None
                    self.examsDialog.finished.connect(on_closed)
                    self.examsDialog.show()
                else:
                    # bereits offen -> in den Vordergrund bringen
                    self.examsDialog.raise_()
                    self.examsDialog.activateWindow()
                # Fokus auf die Zeile
                if hasattr(self.examsDialog, "focus_exam_row"):
                    self.examsDialog.focus_exam_row(ex.idx)
            except Exception:
                pass        
        else:
            return
        # Refresh beider Views
        self.dc.dataChanged.emit()
        self.rightView.viewport().update()
        self.parkingView.viewport().update()

    def on_rightview_header_context_menu(self, pos):
        """
        Kontextmenü auf dem Spaltenkopf der rechten Tabelle (Räume).
        Erlaubt: Raum umbenennen (nur in neuen, nicht existierenden Namen),
        nicht identisch mit prepare_room.
        """
        try:
            # Reentrancy-/Mehrfach-Open-Schutz
            if getattr(self, "_header_menu_open", False):
                return
                
            header = self.rightView.horizontalHeader()
            
            # Sicherstellen, dass nur Custom-ContextMenu genutzt wird
            try:
                if header.contextMenuPolicy() != Qt.CustomContextMenu:
                    header.setContextMenuPolicy(Qt.CustomContextMenu)
            except Exception:
                pass

            logical = header.logicalIndexAt(pos)
            rm: RightModel = self.rightView.model()
            if not hasattr(rm, "rooms") or logical < 0 or logical >= len(rm.rooms):
                return
            old_room = (rm.rooms[logical] or "").strip()
            if old_room == "":
                # leere Platzhalterspalte nicht umbenennen
                return
            menu = QMenu(self)
            act_change = QAction("Raum \u00e4ndern", self)
            act_delete = QAction("Raum l\u00f6schen", self)
            act_add = QAction("Raum hinzuf\u00fcgen", self)
            menu.addAction(act_change)
            menu.addAction(act_delete)
            menu.addAction(act_add)
            # Globalposition zuverlässig vom Header-Viewport ableiten:
            hv = header.viewport() if hasattr(header, "viewport") else header
            # Falls pos nicht vom Header stammt (abhängig vom Signal), vorsichtig mappen:
            if hv is not None and hv.rect().contains(pos):
                global_pos = hv.mapToGlobal(pos)
            else:
                # Fallback: aktuelle Cursorposition verwenden
                global_pos = QCursor.pos()

            # Hilfsfunktionen für Aktionen (synchron nach exec aufrufen)
            def do_room_input():
                new_room, ok = QInputDialog.getText(self, "Raum\u00e4nderung", "Neuer Raumname:", QLineEdit.Normal, old_room)
                if not ok:
                    return
                new_room = (new_room or "").strip()
                if new_room == "" or new_room == old_room:
                    return
                # Geltungsprüfungen:
                # 1) Neuer Raum darf nicht bereits in settings.rooms existieren
                if any((r or "").strip() == new_room for r in (self.dc.settings.rooms or [])):
                    QMessageBox.warning(self, "Ung\u00fcltiger Raum", "Der angegebene Raum existiert bereits in der Raumliste.")
                    return
                # 2) Neuer Raum darf nicht dem Vorbereitungsraum entsprechen
                if (self.dc.settings.prepare_room or "").strip() == new_room:
                    QMessageBox.warning(self, "Ung\u00fcltiger Raum", "Der angegebene Raum stimmt mit dem Vorbereitungsraum \u00fcberein.")
                    return
                # Undo/Redo: als ein Schritt erfassen
                cmd = ChangeRoomCommand(old_room, new_room)
                cmd.apply(self.dc)
                self.dc.push_command(cmd)
                # UI aktualisieren (Modell neu aufbauen, Spaltenbreiten setzen)
                self.refresh_views()
                self.statusBar().showMessage(f"Raum '{old_room}' umbenannt in '{new_room}'.", 4000)
                        
            def do_room_delete():
                # Schutz: Vorbereitungsraum darf nicht gel\u00f6scht werden
                if (self.dc.settings.prepare_room or "").strip() == old_room:
                    QMessageBox.warning(self, "R\u00e4ume", "Der Vorbereitungsraum kann nicht gel\u00f6scht werden.")
                    return
                # Pr\u00fcfen, ob der Raum belegt ist (analog zu on_rooms)
                conflicts = []
                for it in (self.dc.schedule or []):
                    room = (it.Raum or "").strip()
                    if room == old_room:
                        conflicts.append(room)
                if conflicts:
                    QMessageBox.warning(
                        self,
                        "R\u00e4ume k\u00f6nnen nicht gel\u00f6scht werden",
                        "Der ausgew\u00e4hlte Raum ist aktuell in der Planung belegt und kann nicht gel\u00f6scht werden.\n\n"
                        "Bitte verschieben Sie die betroffenen Pr\u00fcfungen oder parken Sie sie, bevor Sie den Raum entfernen."
                    )
                    return
                # Undo/Redo: DeleteRoomCommand mit Merken der alten Position
                rooms = list(self.dc.settings.rooms or [])
                try:
                    prev_idx = next(i for i, r in enumerate(rooms) if (r or "").strip() == old_room)
                except StopIteration:
                    prev_idx = -1
                if prev_idx < 0:
                    return
                cmd = DeleteRoomCommand(old_room, prev_idx)
                cmd.apply(self.dc)
                self.dc.push_command(cmd)
                self.refresh_views()
                self.statusBar().showMessage(f"Raum '{old_room}' gel\u00f6scht.", 4000)

            def do_room_add():
                # Neuen Raum erfragen
                new_room, ok = QInputDialog.getText(self, "Raum hinzuf\u00fcgen", "Neuer Raumname:", QLineEdit.Normal, "")
                if not ok:
                    return
                new_room = (new_room or "").strip()
                if new_room == "":
                    return
                # Validierung: nicht identisch mit vorhandenem Raum oder Vorbereitungsraum
                if any((r or "").strip() == new_room for r in (self.dc.settings.rooms or [])):
                    QMessageBox.warning(self, "Ung\u00fcltiger Raum", "Der angegebene Raum existiert bereits in der Raumliste.")
                    return
                if (self.dc.settings.prepare_room or "").strip() == new_room:
                    QMessageBox.warning(self, "Ung\u00fcltiger Raum", "Der angegebene Raum stimmt mit dem Vorbereitungsraum \u00fcberein.")
                    return
                # Einfügen direkt rechts neben dem angeklickten Raum
                rooms = list(self.dc.settings.rooms or [])
                try:
                    base_idx = next(i for i, r in enumerate(rooms) if (r or "").strip() == old_room)
                except StopIteration:
                    base_idx = len(rooms) - 1
                insert_pos = max(0, base_idx + 1)
                # Undo/Redo: AddRoomCommand
                cmd = AddRoomCommand(new_room, insert_pos)
                cmd.apply(self.dc)
                self.dc.push_command(cmd)
                self.refresh_views()
                self.statusBar().showMessage(f"Raum '{new_room}' hinzugef\u00fcgt.", 4000)
            
            # Modal/synchron wie im anderen Kontextmenü
            self._header_menu_open = True
            chosen = menu.exec(global_pos)
            if not chosen:
                return
            if chosen == act_change:
                do_room_input()
            elif chosen == act_delete:
                do_room_delete()
            elif chosen == act_add:
                do_room_add()
            # Nach Abarbeitung kurze Pufferzeit, um Release-/weitere Context-Events zu „schlucken“
            QTimer.singleShot(0, lambda: setattr(self, "_header_menu_open", False))
        except Exception as e:
            try:
                QMessageBox.critical(self, "Fehler", f"Raum\u00e4nderung fehlgeschlagen:\n{e}")
            except Exception:
                pass
        finally:
            # Fallback, falls oben vorzeitig returned wurde
            if getattr(self, "_header_menu_open", False):
                QTimer.singleShot(0, lambda: setattr(self, "_header_menu_open", False))

    # Klasse: MainWindow, Methode: on_parking_context_menu
    def on_parking_context_menu(self, pos):
        index = self.parkingView.indexAt(pos)
        if not index.isValid():
            return
        pm: ParkingModel = self.parkingView.model()
        ex_idx = pm.index_to_item(index.row(), index.column())
        if ex_idx is None:
            return
        ex = None
        for e in self.dc.exams:
            if e.idx == ex_idx:
                ex = e
                break
        if not ex:
            return
        menu = QMenu(self)
        act_pruefer = QAction("Gleicher Prüfer", self)
        act_pruefer_as_beis = QAction("Gleicher Prüfer als Beisitzer", self)
        act_beis = QAction("Gleicher Beisitzer", self)
        act_beis_as_pruefer = QAction("Gleicher Beisitzer als Prüfer", self)
        act_schueler = QAction("Gleicher Schüler", self)
        act_fach = QAction("Gleiches Fach", self)
        act_edit_beis = QAction("Beisitzer ändern", self)

        # Reihenfolge: Prüfer, Prüfer als Beisitzer, Beisitzer, Beisitzer als Prüfer, Schler, Fach
        menu.addAction(act_pruefer)
        menu.addAction(act_pruefer_as_beis)
        menu.addAction(act_beis)
        menu.addAction(act_beis_as_pruefer)
        menu.addAction(act_schueler)
        menu.addAction(act_fach)
        menu.addSeparator(); menu.addAction(act_edit_beis)


        chosen = menu.exec(self.parkingView.viewport().mapToGlobal(pos))
        if not chosen:
            return
        if chosen == act_pruefer and ex.Pruefer:
            self.dc.highlight_mode = "pruefer"
            self.dc.highlight_value = ex.Pruefer
        elif chosen == act_pruefer_as_beis and ex.Pruefer:
            # Alle Blöcke highlighten, wo Beisitzer == aktueller Prüfer
            self.dc.highlight_mode = "beisitzer"
            self.dc.highlight_value = ex.Pruefer
        elif chosen == act_beis and (ex.Beisitzer or "").strip() != "":
            self.dc.highlight_mode = "beisitzer"
            self.dc.highlight_value = (ex.Beisitzer or "").strip()
        elif chosen == act_beis_as_pruefer and (ex.Beisitzer or "").strip() != "":
            # Alle Blöcke highlighten, wo Prüfer == aktueller Beisitzer
            self.dc.highlight_mode = "pruefer"
            self.dc.highlight_value = (ex.Beisitzer or "").strip()
        elif chosen == act_schueler and ex.Schueler:
            self.dc.highlight_mode = "schueler"
            self.dc.highlight_value = ex.Schueler
        elif chosen == act_fach and ex.Fach:
            m = re.match(r"^\d*([A-Za-z]+)\d*$", ex.Fach)
            core = m.group(1).lower() if m else re.sub(r"\d+", "", ex.Fach).lower()
            if core:
                self.dc.highlight_mode = "fach"
                self.dc.highlight_value = core
            else:
                return
        elif chosen == act_edit_beis:
            # Exams-Dialog öffnen (falls nicht offen) und auf die Zeile mit ex.idx fokussieren
            try:
                if self.examsDialog is None:
                    self.examsDialog = ExamsDialog(self, self.dc)
                    # Beim Schließen Referenz zurücksetzen
                    def on_closed():
                        self.examsDialog = None
                    self.examsDialog.finished.connect(on_closed)
                    self.examsDialog.show()
                else:
                    self.examsDialog.raise_()
                    self.examsDialog.activateWindow()
                if hasattr(self.examsDialog, "focus_exam_row"):
                    self.examsDialog.focus_exam_row(ex.idx)
            except Exception:
                pass        
        else:
            return
        # Refresh beider Views
        self.dc.dataChanged.emit()

    def closeEvent(self, event):
        """
        Beim Beenden prüfen, ob ungespeicherte Änderungen vorliegen.
        Zeige ggf. Speichern-Dialog an. Schließe NUR, wenn
        - keine Änderungen vorliegen, oder
        - der Nutzer Nein gewählt hat, oder
        - das Speichern erfolgreich war.
        """
        # Standard: nicht schließen, bis Logik entscheidet
        event.ignore()
        try:
            # Wenn nichts geändert: direkt schließen
            if not getattr(self.dc, "_dirty", False):
                event.accept()
                return

            ans = QMessageBox.question(
                self,
                "Ungespeicherte Änderungen",
                "Es liegen ungespeicherte Änderungen vor. Möchten Sie vor dem Beenden speichern?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )
            if ans == QMessageBox.Cancel:
                # Schließen abbrechen
                return
            if ans == QMessageBox.No:
                # Ohne Speichern schließen
                event.accept()
                return

            # ans == QMessageBox.Yes: Speichern
            target_path = getattr(self.dc, "last_open_path", None)
            if not target_path or str(target_path).strip() == "":
                # Save-As Dialog (Qt-eigen, nicht-nativ, damit deutsch übersetzt)
                start_path = os.path.join(WORK_DIR, "plan.kolloPlan")
                dlg = QFileDialog(self, "Speichern", start_path)
                dlg.setAcceptMode(QFileDialog.AcceptSave)
                dlg.setFileMode(QFileDialog.AnyFile)
                dlg.setNameFilters(["KolloPlan (*.kolloPlan)"])
                dlg.setDefaultSuffix("kolloPlan")
                dlg.setOption(QFileDialog.DontUseNativeDialog, True)
                dlg.setOption(QFileDialog.DontConfirmOverwrite, False)
            
                if not dlg.exec():
                    # Nutzer hat abgebrochen -> Schließen abbrechen
                    return
            
                target_path = dlg.selectedFiles()[0]
            
            try:
                self.dc.save_file(target_path)
                # Nach erfolgreichem Speichern beim Beenden Dateiname-Label aktualisieren
                self._update_file_label()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Speichern fehlgeschlagen:\n{e}")
                # Schließen abbrechen
                return
            
            # Erfolgreich gespeichert -> schließen
            event.accept()
        except Exception:
            # Fallback: bei unerwarteten Fehlern lieber schließen
            event.accept()

# -------------------------
# Dialoge
# -------------------------

#Aktuell ist ImportCSVDialog() ungenutzt, stammt noch aus der Terminalversion mit CLI-Aufruf. Eventuell für Vorschau und Separatoränderungen in Zukunft nutzbar

class ImportCSVDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Prüfungen (CSV)")
        layout = QVBoxLayout(self)
        self.pathEdit = QLineEdit(self)
        btn_browse = QPushButton("Datei auswählen...")
        btn_browse.clicked.connect(self.browse)
        top = QHBoxLayout()
        top.addWidget(self.pathEdit)
        top.addWidget(btn_browse)
        layout.addLayout(top)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

    def browse(self):
        fn, _ = QFileDialog.getOpenFileName(self, "CSV wählen", "", "CSV (*.csv);;Alle Dateien (*)")
        if fn:
            self.pathEdit.setText(fn)

    def path(self) -> str:
        return self.pathEdit.text().strip()

class RoomsDialog(QDialog):
    def __init__(self, parent, rooms: List[str]):
        super().__init__(parent)
        self.setWindowTitle("Räume")
        self.edit = QLineEdit(", ".join(rooms))
        # Neue Eingabe für Vorbereitungsraum
        self.edit_prepare = QLineEdit()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Räume (durch Komma getrennt)"))
        layout.addWidget(self.edit)
        layout.addWidget(QLabel("Vorbereitungsraum"))
        layout.addWidget(self.edit_prepare)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

    def set_prepare_room(self, prepare_room: str):
        try:
            self.edit_prepare.setText(prepare_room or "")
        except Exception:
            self.edit_prepare.setText("")

    def get_rooms(self) -> List[str]:
        txt = self.edit.text().strip()
        if not txt:
            return []
        return [t.strip() for t in txt.split(",") if t.strip()]

    def get_prepare_room(self) -> str:
        return self.edit_prepare.text().strip()

class TimeDialog(QDialog):
    def __init__(self, parent, t: TimeSettings):
        super().__init__(parent)
        self.setWindowTitle("Zeitstruktur")
        self.t = t
        form = QFormLayout()
        self.spin_slots = QSpinBox()
        self.spin_slots.setRange(0, 50)
        self.spin_slots.setValue(t.n_slots)

        self.time_start = QTimeEdit()
        hh, mm = 8, 0
        try:
            hh, mm = [int(x) for x in t.start_time.split(":")]
        except Exception:
            pass
        self.time_start.setDisplayFormat("HH:mm")
        self.time_start.setTime(self.time_start.time().fromString(f"{hh:02d}:{mm:02d}", "HH:mm"))

        self.spin_slotlen = QSpinBox(); self.spin_slotlen.setRange(1, 600); self.spin_slotlen.setValue(t.slot_len_min)
        self.spin_break = QSpinBox(); self.spin_break.setRange(0, 600); self.spin_break.setValue(t.break_len_min)

        self.date_w1 = QDateEdit(); self.date_w1.setCalendarPopup(True)
        self.date_w2 = QDateEdit(); self.date_w2.setCalendarPopup(True)
        if t.week1_date:
            y, m, d = [int(x) for x in t.week1_date.split("-")]
            self.date_w1.setDate(self.date_w1.date().fromString(f"{y:04d}-{m:02d}-{d:02d}", "yyyy-MM-dd"))
        if t.week2_date:
            y, m, d = [int(x) for x in t.week2_date.split("-")]
            self.date_w2.setDate(self.date_w2.date().fromString(f"{y:04d}-{m:02d}-{d:02d}", "yyyy-MM-dd"))

        form.addRow("Anzahl Slots/Tag", self.spin_slots)
        form.addRow("Startzeit", self.time_start)
        form.addRow("Slotlänge (Min)", self.spin_slotlen)
        form.addRow("Pausenlänge (Min)", self.spin_break)
        form.addRow("Startdatum Woche 1 (Mo)", self.date_w1)
        form.addRow("Startdatum Woche 2 (Mo)", self.date_w2)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

    def apply(self) -> TimeSettings:
        t = TimeSettings()
        t.n_slots = int(self.spin_slots.value())
        t.start_time = self.time_start.time().toString("HH:mm")
        t.slot_len_min = int(self.spin_slotlen.value())
        t.break_len_min = int(self.spin_break.value())
        if self.date_w1.date().isValid():
            t.week1_date = self.date_w1.date().toString("yyyy-MM-dd")
        if self.date_w2.date().isValid():
            t.week2_date = self.date_w2.date().toString("yyyy-MM-dd")
        return t

class ConstraintsDialog(QDialog):
    # Unverändert – Ihr bestehender, funktionierender Dialog
    def __init__(self, parent, c: ConstraintsSettings):
        super().__init__(parent)
        self.setWindowTitle("Bedingungen")
        self.c = c
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Harte
        self.cb_s1w = QCheckBox(); self.cb_s1w.setChecked(c.hard_student_one_per_week)
        self.cb_group = QCheckBox(); self.cb_group.setChecked(c.hard_grouping_enabled)
        self.spin_group = QSpinBox(); self.spin_group.setRange(2, 5); self.spin_group.setValue(c.grouping_block_size or 2); self.spin_group.setEnabled(self.cb_group.isChecked())
        self.cb_unav = QCheckBox(); self.cb_unav.setChecked(c.hard_unavailability)
        self.edit_unav = QPlainTextEdit(); self.edit_unav.setPlaceholderText("Format:\nName: Mo1, Di2\nName2: Mi1\n..."); self.edit_unav.setEnabled(self.cb_unav.isChecked())
        if c.unavailability:
            txt = []
            for k, lst in c.unavailability.items():
                txt.append(f"{k}: {', '.join(lst)}")
            self.edit_unav.setPlainText("\n".join(txt))
        self.cb_min_gap = QCheckBox(); self.cb_min_gap.setChecked(c.hard_min_gap_days_same_student is not None)
        self.spin_min_gap = QSpinBox(); self.spin_min_gap.setRange(0, 10); self.spin_min_gap.setEnabled(self.cb_min_gap.isChecked())
        if c.hard_min_gap_days_same_student is not None:
            self.spin_min_gap.setValue(c.hard_min_gap_days_same_student)
        self.cb_no_exam = QCheckBox(); self.cb_no_exam.setChecked(c.hard_no_exam_days_enabled)
        self.edit_no_exam = QLineEdit(", ".join(c.no_exam_days or [])); self.edit_no_exam.setEnabled(self.cb_no_exam.isChecked())
        self.cb_max_days = QCheckBox(); self.cb_max_days.setChecked(c.hard_max_days_per_teacher_enabled)
        self.spin_max_days = QSpinBox(); self.spin_max_days.setRange(1, 10); self.spin_max_days.setEnabled(self.cb_max_days.isChecked())
        if c.hard_max_days_per_teacher_K is not None:
            self.spin_max_days.setValue(c.hard_max_days_per_teacher_K or 2)

        # Soft
        self.cb_soft_gap = QCheckBox(); self.cb_soft_gap.setChecked(c.soft_desired_gap_days_same_student is not None)
        self.spin_soft_gap = QSpinBox(); self.spin_soft_gap.setRange(0, 10); self.spin_soft_gap.setEnabled(self.cb_soft_gap.isChecked())
        if c.soft_desired_gap_days_same_student is not None:
            self.spin_soft_gap.setValue(c.soft_desired_gap_days_same_student)
        self.cb_min_rooms = QCheckBox(); self.cb_min_rooms.setChecked(c.soft_minimize_rooms_used)
        self.edit_allow5 = QLineEdit(", ".join(c.teachers_allow_5_per_day or []))
        self.spin_max_per_day = QSpinBox(); self.spin_max_per_day.setRange(1, 10); self.spin_max_per_day.setValue(c.default_max_per_day)
        self.cb_pref_second = QCheckBox(); self.cb_pref_second.setChecked(c.soft_prefer_second_slot_start)
        self.spin_pref_weight = QSpinBox(); self.spin_pref_weight.setRange(1, 100); self.spin_pref_weight.setValue(c.weight_prefer_second_slot); self.spin_pref_weight.setEnabled(self.cb_pref_second.isChecked())
        self.cb_ignore_empty_beisitzer = QCheckBox(); self.cb_ignore_empty_beisitzer.setChecked(getattr(c, "ignore_empty_beisitzer", True))
        # Neue Option: faire Tagesverteilung
        self.cb_fair = QCheckBox(); self.cb_fair.setChecked(getattr(c, "fair_day_distribution_enabled", False))
        self.spin_fair = QSpinBox(); self.spin_fair.setRange(4, 6); self.spin_fair.setValue(getattr(c, "fair_day_distribution_slotsum", 4)); self.spin_fair.setEnabled(self.cb_fair.isChecked())

        # Limits/Gewichte
        self.spin_cp_time = QSpinBox(); self.spin_cp_time.setRange(1, MAX_CP_TIME_LIMIT); self.spin_cp_time.setValue(c.cp_time_limit_sec)
        self.spin_mip_time = QSpinBox(); self.spin_mip_time.setRange(1, MAX_MIP_TIME_LIMIT); self.spin_mip_time.setValue(c.mip_room_time_limit_sec)
        self.spin_mip_gap_w = QSpinBox(); self.spin_mip_gap_w.setRange(0, 100000); self.spin_mip_gap_w.setValue(c.MIP_ROOM_GAP_WEIGHT)
        self.spin_gi = QSpinBox(); self.spin_gi.setRange(0, 100000); self.spin_gi.setValue(c.GAP_WEIGHT_INNER)
        self.spin_go = QSpinBox(); self.spin_go.setRange(0, 100000); self.spin_go.setValue(c.GAP_WEIGHT_OUTER)
        self.spin_span = QSpinBox(); self.spin_span.setRange(0, 100000); self.spin_span.setValue(c.SPAN_WEIGHT)
        self.spin_second = QSpinBox(); self.spin_second.setRange(0, 100000); self.spin_second.setValue(c.SECOND_SLOT_WEIGHT)
        self.spin_balance = QSpinBox(); self.spin_balance.setRange(0, 100000); self.spin_balance.setValue(c.DAY_WEIGHT_BALANCE)

        self.cb_group.toggled.connect(self.spin_group.setEnabled)
        self.cb_unav.toggled.connect(self.edit_unav.setEnabled)
        self.cb_min_gap.toggled.connect(self.spin_min_gap.setEnabled)
        self.cb_no_exam.toggled.connect(lambda on: self.edit_no_exam.setEnabled(on))
        self.cb_max_days.toggled.connect(self.spin_max_days.setEnabled)
        self.cb_pref_second.toggled.connect(self.spin_pref_weight.setEnabled)
        self.cb_soft_gap.toggled.connect(self.spin_soft_gap.setEnabled)
        self.cb_fair.toggled.connect(self.spin_fair.setEnabled)

        form.addRow("Genau eine Prüfung pro Woche (hart)", self.cb_s1w)
        hl = QHBoxLayout(); hl.addWidget(self.cb_group); hl.addWidget(QLabel("Blockgröße:")); hl.addWidget(self.spin_group)
        form.addRow("Kopplungen (hart)", hl)
        form.addRow("Abwesenheiten beachten (hart)", self.cb_unav)
        form.addRow("Abwesenheiten (Name: Mo1, Di2 ...)", self.edit_unav)
        hl2 = QHBoxLayout(); hl2.addWidget(self.cb_min_gap); hl2.addWidget(QLabel("Abstand (Tage):")); hl2.addWidget(self.spin_min_gap)
        form.addRow("Min. Abstand gleicher Schüler (hart)", hl2)
        form.addRow("Tage ohne Prüfungen (hart)", self.cb_no_exam)
        form.addRow("Liste Tage (z.B. Mo1, Di2)", self.edit_no_exam)
        hl3 = QHBoxLayout(); hl3.addWidget(self.cb_max_days); hl3.addWidget(QLabel("Max. Prüfungstage/Person:")); hl3.addWidget(self.spin_max_days)
        form.addRow("Max. Tage pro Prüfer (hart)", hl3)
        form.addRow(QLabel("—"))
        hl4 = QHBoxLayout(); hl4.addWidget(self.cb_soft_gap); hl4.addWidget(QLabel("gewünschter Abstand in Tagen:")); hl4.addWidget(self.spin_soft_gap)
        form.addRow("Abstand gleicher Schüler (weich)", hl4)
        form.addRow("Min. Räume (weich)", self.cb_min_rooms)
        form.addRow("Prüfer mit 5 Prüfungen/Tag (kommagetrennt)", self.edit_allow5)
        form.addRow("Prüfungen/Tag für übrige Prüfer", self.spin_max_per_day)
        hl5 = QHBoxLayout(); hl5.addWidget(self.cb_pref_second); hl5.addWidget(QLabel("Gewicht:")); hl5.addWidget(self.spin_pref_weight)
        form.addRow("Start im 2. Slot (weich)", hl5)
        form.addRow(QLabel("—"))
        form.addRow(QLabel(""))
        form.addRow("Leere Beisitzer ignorieren", self.cb_ignore_empty_beisitzer)
        hl_fair = QHBoxLayout(); hl_fair.addWidget(self.cb_fair); hl_fair.addWidget(QLabel("Slotsumme:")); hl_fair.addWidget(self.spin_fair)
        form.addRow("faire Tagesverteilung", hl_fair)
        form.addRow("Zeitlimit Zuteilung (s)", self.spin_cp_time)
        form.addRow("Zeitlimit Raumoptimierung (s)", self.spin_mip_time)
        form.addRow("Strafe für Lücken", self.spin_mip_gap_w)
        form.addRow("Strafe Kompaktheit", self.spin_gi)
        form.addRow("Strafe Rand", self.spin_go)
        form.addRow("Strafe Spannweite", self.spin_span)
        form.addRow("Strafe 2. Slot", self.spin_second)
        form.addRow("Strafe gleichmäßige Tagesverteilung", self.spin_balance)

        layout.addLayout(form)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)
        # Nach dem Schließen dieses Dialogs könnte der Splitter neu layouten
        # -> initiale Größen erneut setzen, um graue Bereiche zu vermeiden
        QTimer.singleShot(0, getattr(self.parent(), "_init_splitter_sizes", lambda: None))

    def apply(self) -> ConstraintsSettings:
        c = ConstraintsSettings()
        c.hard_student_one_per_week = self.cb_s1w.isChecked()
        c.hard_grouping_enabled = self.cb_group.isChecked()
        c.grouping_block_size = int(self.spin_group.value()) if c.hard_grouping_enabled else None
        c.hard_unavailability = self.cb_unav.isChecked()
        if c.hard_unavailability:
            unav = {}
            for line in self.edit_unav.toPlainText().splitlines():
                line = line.strip()
                if not line or ":" not in line:
                    continue
                name, tokens = line.split(":", 1)
                tok_list = [t.strip() for t in tokens.split(",") if t.strip()]
                unav[name.strip()] = tok_list
            c.unavailability = unav
        c.hard_min_gap_days_same_student = int(self.spin_min_gap.value()) if self.cb_min_gap.isChecked() else None
        c.hard_no_exam_days_enabled = self.cb_no_exam.isChecked()
        c.no_exam_days = [t.strip() for t in self.edit_no_exam.text().split(",") if t.strip()] if c.hard_no_exam_days_enabled else []
        c.hard_max_days_per_teacher_enabled = self.cb_max_days.isChecked()
        c.hard_max_days_per_teacher_K = int(self.spin_max_days.value()) if c.hard_max_days_per_teacher_enabled else None

        c.soft_desired_gap_days_same_student = int(self.spin_soft_gap.value()) if self.cb_soft_gap.isChecked() else None
        c.soft_minimize_rooms_used = self.cb_min_rooms.isChecked()
        c.teachers_allow_5_per_day = [t.strip() for t in self.edit_allow5.text().split(",") if t.strip()]
        c.default_max_per_day = int(self.spin_max_per_day.value())
        c.soft_prefer_second_slot_start = self.cb_pref_second.isChecked()
        c.weight_prefer_second_slot = int(self.spin_pref_weight.value())

        c.cp_time_limit_sec = int(self.spin_cp_time.value())
        c.mip_room_time_limit_sec = int(self.spin_mip_time.value())
        c.MIP_ROOM_GAP_WEIGHT = int(self.spin_mip_gap_w.value())
        c.GAP_WEIGHT_INNER = int(self.spin_gi.value())
        c.GAP_WEIGHT_OUTER = int(self.spin_go.value())
        c.SPAN_WEIGHT = int(self.spin_span.value())
        c.SECOND_SLOT_WEIGHT = int(self.spin_second.value())
        c.DAY_WEIGHT_BALANCE = int(self.spin_balance.value())
        c.ignore_empty_beisitzer = bool(self.cb_ignore_empty_beisitzer.isChecked())
        c.fair_day_distribution_enabled = bool(self.cb_fair.isChecked())
        c.fair_day_distribution_slotsum = int(self.spin_fair.value())

        return c

class ExamsDialog(QDialog):
    """
    Ausschüsse – editierbar: Thema (Spalte 3), Beisitzer (Spalte 5)
    Versteckte ID-Spalte (Spalte 0) für stabile Synchronisation unabhängig von Sortierung.
    """
    def __init__(self, parent, dc: DataController):
        super().__init__(parent)
        self.setWindowTitle("Ausschüsse – Prüfungen")
        self.dc = dc
        layout = QVBoxLayout(self)
        self.table = QTableView()
        self.model = QStandardItemModel(0, 7)
        self.model.setHorizontalHeaderLabels(["ID", "Schüler", "NTA (%)", "Fach", "Thema", "Prüfer", "Beisitzer"])
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSortingEnabled(True)
        # ID-Spalte verstecken
        self.table.setColumnHidden(0, True)
        self.load()
        self._in_programmatic_change = False
        # Puffer für "vorher"-Werte (row, col) -> str/int für Undo
        self._edit_before_cache: Dict[Tuple[int, int], Any] = {}
        # Vor der Änderung alten Wert puffern (Start der User-Interaktion)
        self.table.pressed.connect(self._capture_before_value)
        self.table.clicked.connect(self._capture_before_value)
        # Live-Validierung bei Änderungen (nur Spalten 5 Beisitzer)
        self.model.itemChanged.connect(self.on_item_changed)

        layout.addWidget(self.table)
        # Dynamische Anfangsgroesse nur beim Öffnen: Breite aus Spaltenbreiten ableiten,
        # gedeckelt auf 90% der Bildschirmbreite; keine Live-Nachführung.
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        def _computed_table_width(tv: QTableView) -> int:
            hh = tv.horizontalHeader()
            vh = tv.verticalHeader()
            total = 0
            # Summe sichtbarer Spaltenbreiten
            if tv.model() is not None:
                for c in range(tv.model().columnCount()):
                    if not tv.isColumnHidden(c):
                        total += tv.columnWidth(c)
                # WICHTIG: Versteckte ID-Spalte (Index 0) explizit mit einrechnen,
                # da columnWidth(0) bei versteckter Spalte nicht zählt.
                if tv.isColumnHidden(0):
                    total += hh.sectionSize(0)
            # vertikaler Header, Rahmen, evtl. Scrollbar und kleines Polster
            if vh.isVisible():
                total += vh.width()
            total += tv.frameWidth() * 2
            if tv.verticalScrollBar().isVisible():
                total += tv.verticalScrollBar().width()
            total += EXTRA_WIDTH_EXAMS_DIALOG
            return total
        screen = QGuiApplication.primaryScreen()
        screen_w = screen.availableGeometry().width() if screen else 1280
        screen_h = screen.availableGeometry().height() if screen else 800
        table_w = _computed_table_width(self.table)
        # Layout-Margins (links/rechts) des Dialog-Layouts addieren
        try:
            lm = layout.contentsMargins()
            layout_lr = lm.left() + lm.right()
        except Exception:
            layout_lr = 0
        # Mindestbreite am Inhalt inkl. Layout-Margins orientieren, aber auf 90% der Bildschirmbreite deckeln
        min_w = min(max(480, table_w + layout_lr), int(screen_w * 0.9))
        self.setMinimumWidth(min_w)
        # Höhe: sinnvolle Mindesthöhe beibehalten, Zielhöhe deckeln
        self.setMinimumHeight(450)
        target_h = min(770, int(screen_h * 0.9))
        self.resize(self.minimumWidth(), target_h)

        box = QDialogButtonBox(QDialogButtonBox.Close)
        layout.addWidget(box)
        box.rejected.connect(self.reject); box.accepted.connect(self.accept)

        #box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        #box.accepted.connect(self.on_ok)
        #box.rejected.connect(self.reject)
        #layout.addWidget(box)

    def focus_exam_row(self, exam_idx: int):
        """
        Fokussiert (scrollt zu) die Zeile mit der gegebenen Exam-ID und selektiert sie.
        Funktioniert unabhängig von aktueller Sortierung, da ID in Spalte 0 steht.
        """
        try:
            # Durchsuche alle Zeilen nach passender ID (Spalte 0 ist versteckt, aber vorhanden)
            match_row = -1
            for r in range(self.model.rowCount()):
                item_id = self.model.item(r, 0)
                if not item_id:
                    continue
                try:
                    if int(item_id.text()) == int(exam_idx):
                        match_row = r
                        break
                except Exception:
                    continue
            if match_row >= 0:
                # Selektiere eine sichtbare Spalte (z. B. Thema, Spalte 4)
                idx = self.model.index(match_row, 4)
                self.table.scrollTo(idx)
                self.table.setCurrentIndex(idx)
                self.table.selectRow(match_row)
        except Exception:
            pass

    def load(self):
        self.model.setRowCount(0)
        for ex in self.dc.exams:
            nta_val = 0 if getattr(ex, "NTA", None) is None else int(ex.NTA)
            row = [
                QStandardItem(str(ex.idx)),           # 0 ID (hidden)
                QStandardItem(ex.Schueler),           # 1 Schueler
                QStandardItem(str(nta_val)),          # 2 NTA (%)
                QStandardItem(ex.Fach),               # 3 Fach
                QStandardItem(ex.Thema),              # 4 Thema (editierbar)
                QStandardItem(ex.Pruefer),            # 5 Pruefer (editierbar)
                QStandardItem(ex.Beisitzer),          # 6 Beisitzer (editierbar)
            ]
            # Editierbarkeit
            row[2].setEditable(True)   # NTA
            row[4].setEditable(True)   # Thema
            row[5].setEditable(True)   # Prfer
            row[6].setEditable(True)   # Beisitzer
            # andere: fix
            row[1].setEditable(False); row[3].setEditable(False)
            self.model.appendRow(row)
        # Nach dem Laden initiale Konfliktfarben anwenden
        self.apply_row_colors()

    def _capture_before_value(self, index: QModelIndex):
        try:
            if not index.isValid():
                return
            r, c = index.row(), index.column()
            # Nur editierbare Spalten:
            if c not in (2, 4, 5, 6):
                return
            it = self.model.item(r, c)
            val = it.text() if it else ""
            # Für NTA als int vormerken
            if c == 2:
                try:
                    val = int(val) if str(val).strip() != "" else 0
                except Exception:
                    val = 0
            self._edit_before_cache[(r, c)] = val
        except Exception:
            pass

    def on_ok(self):
        # Änderungen anhand ID zurückschreiben
        updates = {}
        for r in range(self.model.rowCount()):
            try:
                exam_idx = int(self.model.item(r, 0).text())
            except Exception:
                continue
            # Neue Spaltenindizes: 2=NTA, 4=Thema, 6=Beisitzer 5=Pruefer
            tema_item = self.model.item(r, 4)
            pruef_item = self.model.item(r, 5)
            beis_item = self.model.item(r, 6)
            nta_item = self.model.item(r, 2)
            thema = tema_item.text() if tema_item else ""
            pruefer = pruef_item.text() if pruef_item else ""
            beisitzer = beis_item.text() if beis_item else ""
            try:
                nta = int(nta_item.text()) if nta_item and nta_item.text().strip() != "" else 0
            except Exception:
                nta = 0
            nta = max(0, min(200, nta))
            updates[exam_idx] = (thema, pruefer, beisitzer, nta)

        exam_by_id = {ex.idx: ex for ex in self.dc.exams}
        for eid, (thema, pruefer, beisitzer, nta) in updates.items():
            if eid in exam_by_id:
                exam_by_id[eid].Thema = thema
                exam_by_id[eid].Pruefer = pruefer
                exam_by_id[eid].Beisitzer = beisitzer
                exam_by_id[eid].NTA = nta

        # bestehende schedule spiegeln (Text-Anpassungen, nicht NTA)
        for s in self.dc.schedule:
            if s.ExamIdx in exam_by_id:
                s.Thema = exam_by_id[s.ExamIdx].Thema
                s.Pruefer = exam_by_id[s.ExamIdx].Pruefer
                s.Beisitzer = exam_by_id[s.ExamIdx].Beisitzer

        # Nach Speicherung globale Konfliktbewertung und Refresh
        self.dc.evaluate_conflicts()
        self.dc.dataChanged.emit()
        # Daten sind geändert
        self.dc._dirty = True
        self.accept()

    def on_item_changed(self, item: QStandardItem):
        # Nur Beisitzer-Spalte (5) und Thema (3) relevant; Beisitzer löst Validierung aus
        col = item.column()
        row = item.row()
        if col not in (2, 4, 5, 6):
            return
        # ID holen
        try:
            exam_idx = int(self.model.item(row, 0).text())
        except Exception:
            return
        # Änderungen in dc.exams spiegeln (live)
        if getattr(self, "_in_programmatic_change", False):
            return        
        for ex in self.dc.exams:
            if ex.idx == exam_idx:
                if col == 4:
                    ex.Thema = item.text()
                elif col == 5:
                    ex.Pruefer = item.text()
                elif col == 6:
                    ex.Beisitzer = item.text()
                elif col == 2:
                    try:
                        val = int(item.text()) if item.text().strip() != "" else 0
                    except Exception:
                        val = 0
                    val = max(0, min(200, val))
                    ex.NTA = val
                    if item.text() != str(val):
                        item.setText(str(val))
                break
        
        # Undo/Redo: Edit als Command erfassen (mit vor-Änderungswert aus Cache)
        try:
            field = None
            if col == 4:
                field = "Thema"
                after_val = item.text()
            elif col == 5:
                field = "Pruefer"
                after_val = item.text()
            elif col == 6:
                field = "Beisitzer"
                after_val = item.text()
            elif col == 2:
                field = "NTA"
                try:
                    after_val = int(item.text()) if item.text().strip() != "" else 0
                except Exception:
                    after_val = 0
            if field is not None:
                before_val = self._edit_before_cache.get((row, col), "" if field != "NTA" else 0)
                # Command pushen
                self.dc.push_command(EditExamFieldCommand(exam_idx, field, before_val, after_val))
                # Nach Push: lokalen Cache fr diese Zelle lschen (optional)
                self._edit_before_cache.pop((row, col), None)
        except Exception:
            pass

        # schedule-Spiegel (Text) aktualisieren
        for s in self.dc.schedule:
            if s.ExamIdx == exam_idx:
                if col == 4:
                    s.Thema = item.text()
                elif col == 5:
                    s.Pruefer = item.text()
                elif col == 6:
                    s.Beisitzer = item.text()
        # Live-Konfliktbewertung (Beisitzer leer -> keine Prüfung/keine Färbung extra)
        self.dc.evaluate_conflicts()
        # Faire Tagesverteilung neu bewerten
        try:
            self.dc.evaluate_fair_day_distribution()
        except Exception:
            pass
        # K2 (Beisitzer-Zählung) aktualisieren, wenn der Beisitzer geändert wurde
        try:
            if col == 6:
                self.dc.count_beisitzer()
                # Nach K2-Update auch Belastung neu berechnen
                self.dc.calculate_belastung()
        except Exception:
            pass
        # Tabellenfärbung im Dialog und im Plan aktualisieren
        self.apply_row_colors()
        self.dc.dataChanged.emit()
        # Daten sind geändert
        self.dc._dirty = True
        # Undo/Redo Buttons-Status aktualisieren
        wnd = self.parent() if isinstance(self.parent(), QMainWindow) else None
        try:
            # Finde MainWindow, um Aktionen zu aktualisieren
            mw = self.parent()
            while mw and not isinstance(mw, QMainWindow):
                mw = mw.parent()
            if mw and hasattr(mw, "_update_undo_redo_actions"):
                mw._update_undo_redo_actions()
        except Exception:
            pass

    def apply_row_colors(self):
        """
        Färbt Beisitzer-Felder (Spalte 5) je nach Konfliktstatus:
        - leer: Standard
        - hard: rot, soft: orange, sonst hellgrün
        """
        for r in range(self.model.rowCount()):
            try:
                exam_idx = int(self.model.item(r, 0).text())
            except Exception:
                continue
            be_item = self.model.item(r, 6)
            if not be_item:
                continue
            be_txt = be_item.text().strip() if be_item.text() else ""
            if be_txt == "":
                # leere Beisitzer ignorieren
                be_item.setBackground(QColor(255, 255, 255))
                continue
            state = self.dc.conflict_map.get(exam_idx)
            if not state or state[0] is None:
                be_item.setBackground(COLOR_ALLOWED)  # konfliktfrei -> grün
            else:
                level, _msgs = state
                if level == "hard":
                    be_item.setBackground(COLOR_HARD_FORBIDDEN)
                elif level == "soft":
                    be_item.setBackground(COLOR_SOFT_WARN)
                else:
                    be_item.setBackground(QColor(255, 255, 255))

class TeachersDialog(QDialog):
    def __init__(self, parent, dc: DataController):
        super().__init__(parent)
        self.setWindowTitle("Lehrkräfte")
        layout = QVBoxLayout(self)
        self.table = QTableView()
        self.dc = dc
        self.model = QStandardItemModel(0, 8)
        self.model.setHorizontalHeaderLabels(["Lehrkraft", "UPZ", "WS", "S", "S2", "K", "K2", "Belastung"])
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSortingEnabled(True)

        # Bei Settings-Änderungen (inkl. Workload) Tabelle aktualisieren
        try:
            self.dc.dataChanged.connect(lambda: self._load_teachers())
        except Exception:
            pass

        # Vor dem Laden K2 anhand der aktuellen Exams zählen/aktualisieren
        try:
            self.dc.count_beisitzer()
        except Exception:
            pass

        # Danach Belastung berechnen (nutzt u. a. K2)
        try:
            self.dc.calculate_belastung()
        except Exception:
            pass
        self._load_teachers()

        # Nur S2 und WS editierbar -> Item-Changed-Handler
        self.model.itemChanged.connect(self._on_item_changed)
        # Wir erstellen eine kleine, einzeilige Nicht-Editable QTableView, die nur die Summen anzeigt.
        self.summary_view = QTableView()
        self.summary_model = QStandardItemModel(1, 8)
        # Dieselben Header-Labels verwenden (Header verstecken später)
        self.summary_model.setHorizontalHeaderLabels(["Lehrkraft", "UPZ", "WS", "S", "S2", "K", "K2", "Belastung"])
        self.summary_view.setModel(self.summary_model)
        # Darstellung: keine Kopfzeile zeigen, keine Auswahl
        self.summary_view.horizontalHeader().setVisible(False)
        self.summary_view.verticalHeader().setVisible(False)
        self.summary_view.setFixedHeight( self.table.verticalHeader().defaultSectionSize() + 6 )  # etwas Padding
        self.summary_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.summary_view.setSelectionMode(QTableView.NoSelection)
        self.summary_view.setEditTriggers(QTableView.NoEditTriggers)
        # Visuelle Formatierung: fette Schrift, leichter Hintergrund
        self._apply_summary_style()
        
        # Layout: Tabelle oben, Summenzeile darunter
        layout.addWidget(self.table)
        layout.addWidget(self.summary_view)
        box = QDialogButtonBox(QDialogButtonBox.Close)
        layout.addWidget(box)
        box.rejected.connect(self.reject); box.accepted.connect(self.accept)
        # Dynamische Anfangsgroesse nur beim Öffnen: Breite aus Spaltenbreiten ermitteln
        # (Tabelle und Summenzeile), gedeckelt auf 90% der Bildschirmbreite.
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        def _computed_table_width(tv: QTableView) -> int:
            vh = tv.verticalHeader()
            total = 0
            if tv.model() is not None:
                for c in range(tv.model().columnCount()):
                    if not tv.isColumnHidden(c):
                        total += tv.columnWidth(c)
            if vh.isVisible():
                total += vh.width()
            total += tv.frameWidth() * 2
            if tv.verticalScrollBar().isVisible():
                total += tv.verticalScrollBar().width()
            total += EXTRA_WIDTH_TEACHERS_DIALOG
            return total
        screen = QGuiApplication.primaryScreen()
        screen_w = screen.availableGeometry().width() if screen else 1280
        screen_h = screen.availableGeometry().height() if screen else 800
        table_w = _computed_table_width(self.table)
        summary_w = _computed_table_width(self.summary_view)
        # Layout-Margins (links/rechts) des Dialog-Layouts addieren
        try:
            lm = layout.contentsMargins()
            layout_lr = lm.left() + lm.right()
        except Exception:
            layout_lr = 0
        # Breite der ButtonBox mit einrechnen (kann breiter als die Tabellen sein)
        try:
            buttons_w = box.sizeHint().width()
        except Exception:
            buttons_w = 0
        needed_w = max(table_w, summary_w, buttons_w)
        # Mindestbreite inkl. Layout-Margins berechnen und auf 90% der Bildschirmbreite deckeln
        min_w = min(max(405, needed_w + layout_lr), int(screen_w * 0.9))
        self.setMinimumWidth(min_w)
        self.setMinimumHeight(420)
        target_h = min(620, int(screen_h * 0.9))
        self.resize(self.minimumWidth(), target_h)
        
        # Initiale Summenberechnung und Anbindung an DataController-Änderungen
        self._update_summaries()
        self.dc.dataChanged.connect(self._update_summaries)

    def _load_teachers(self):
        self.model.setRowCount(0)
        for t in getattr(self.dc, "teachers", []):
            # Spalten: Lehrkraft, UPZ, WS, S, S2, K, K2, Belastung
            it_lehr = QStandardItem(t.Lehrkraft or ""); it_lehr.setEditable(False)
            it_upz  = QStandardItem(t.UPZ or ""); it_upz.setEditable(False)
            it_ws   = QStandardItem(t.WS or ""); it_ws.setEditable(True)
            it_s    = QStandardItem(t.S or ""); it_s.setEditable(False)
            it_s2   = QStandardItem(getattr(t, "S2", "") or ""); it_s2.setEditable(True)
            it_k    = QStandardItem(t.K or ""); it_k.setEditable(False)
            it_k2   = QStandardItem(getattr(t, "K2", "") or ""); it_k2.setEditable(False)
            it_bel  = QStandardItem(t.Belastung or ""); it_bel.setEditable(False)
            # Alignment setzen: Mitte horizontal, zentriert vertikal
            center = Qt.AlignCenter
            for it in (it_upz, it_ws, it_s, it_s2, it_k, it_k2, it_bel):
                it.setTextAlignment(center)
            # Optional: Lehrkraft links lassen (Standard) oder ebenfalls zentrieren
            #it_lehr.setTextAlignment(center)
            
            # Belastung farblich hervorheben:
            # - rot bei positiv (> 0)
            # - grün bei negativ (< 0)
            # - keine Färbung bei exakt 0 oder nicht parsebarem Wert
            try:
                bel_val = float((t.Belastung or "0").replace(",", "."))
                if bel_val > 0:
                    it_bel.setBackground(QColor(255, 200, 200))  # hellrot
                elif bel_val < 0:
                    it_bel.setBackground(QColor(220, 255, 220))  # hellgrün
                else:
                    # genau 0 -> Standardhintergrund (keine Färbung)
                    pass
            except Exception:
                # nicht parsebar -> keine Färbung
                pass
            self.model.appendRow([it_lehr, it_upz, it_ws, it_s, it_s2, it_k, it_k2, it_bel])
        # Nach dem (Neu-)Laden ebenfalls die Summenzeile aktualisieren
        self._update_summaries()

    def _on_item_changed(self, item: QStandardItem):
        # Nur S2 und WS sind editierbar/persistiert
        col = item.column()
        if col not in (2, 4):
            return
        try:
            row = item.row()
            # Lehrkraft als Schlüssel in Spalte 0
            key_item = self.model.item(row, 0)
            code = (key_item.text() if key_item else "").strip()
            if not code:
                return
            # Spaltenbehandlung
            if col == 4:
                # neuen S2-Wert (frei, als String)
                before_val = None
                # Vorher-Wert aus dc holen
                try:
                    t_now = next((tt for tt in getattr(self.dc, "teachers", []) if (tt.Lehrkraft or "").strip() == code), None)
                    before_val = getattr(t_now, "S2", "") if t_now else ""
                except Exception:
                    before_val = ""
                new_s2 = item.text()
                # In dc.teachers schreiben
                for t in getattr(self.dc, "teachers", []):
                    if (t.Lehrkraft or "").strip() == code:
                        t.S2 = new_s2
                        break
                # Undo/Redo-Command pushen
                try:
                    cmd = EditTeacherFieldCommand(code, "S2", before_val, new_s2)
                    self.dc.push_command(cmd)
                except Exception:
                    pass
            elif col == 2:
                # WS numerisch validieren: leer -> "", sonst nichtnegativer Integer
                txt = item.text().strip() if item.text() is not None else ""
                if txt == "":
                    new_ws = ""
                else:
                    try:
                        v = int(txt)
                        if v < 0:
                            v = 0
                        new_ws = str(v)
                    except Exception:
                        # Ungültige Eingabe zurück auf vorherigen validen Zustand: ""
                        new_ws = ""
                # Falls Anzeige korrigiert werden muss, direkt im Item setzen
                if item.text() != new_ws:
                    item.setText(new_ws)
                # Persistenz in dc.teachers
                before_val = None
                try:
                    t_now = next((tt for tt in getattr(self.dc, "teachers", []) if (tt.Lehrkraft or "").strip() == code), None)
                    before_val = (t_now.WS if t_now and t_now.WS is not None else "")
                except Exception:
                    before_val = ""
                for t in getattr(self.dc, "teachers", []):
                    if (t.Lehrkraft or "").strip() == code:
                        t.WS = new_ws  # als String speichern (Belastung parst später Integer)
                        break
                # Undo/Redo-Command pushen
                try:
                    cmd = EditTeacherFieldCommand(code, "WS", before_val, new_ws)
                    self.dc.push_command(cmd)
                except Exception:
                    pass
            # Nach Änderung von S2 oder WS: Belastung neu berechnen
            try:
                self.dc.calculate_belastung()
            except Exception:
                pass
            # Änderung signalisieren und Zeile im Dialog aktualisieren (Belastungswert + Farbe)
            self.dc.dataChanged.emit()
            try:
                # Aktualisierte Teacher-Daten holen
                t_now = next((tt for tt in getattr(self.dc, "teachers", []) if (tt.Lehrkraft or "").strip() == code), None)
                if t_now:
                    # Spalte 7 = Belastung im Dialogmodell
                    bel_item = self.model.item(row, 7)
                    if bel_item:
                        bel_item.setText(t_now.Belastung or "")
                        # Farbe entsprechend dem neuen Wert setzen
                        try:
                            bel_val = float((t_now.Belastung or "0").replace(",", "."))
                            # Reset zunächst
                            bel_item.setBackground(QColor(255, 255, 255))
                            if bel_val > 0:
                                bel_item.setBackground(QColor(255, 200, 200))  # hellrot
                            elif bel_val < 0:
                                bel_item.setBackground(QColor(220, 255, 220))  # hellgrün
                        except Exception:
                            # bei Parsefehler keine Färbung
                            bel_item.setBackground(QColor(255, 255, 255))
            except Exception:
                pass
            # Optional: ganze Zeile neu zeichnen
            try:
                self.table.viewport().update()
            except Exception:
                pass
            # Markiere Daten als geändert
            self.dc._dirty = True
        except Exception:
            pass
        finally:
            # Nach jeder Item-Änderung S, S2, K, K2 Summen aktualisieren
            try:
                self._update_summaries()
            except Exception:
                pass

    def _apply_summary_style(self):
        #Formatierung der Summenzeile: fette Schrift, leichter Hintergrund.
        try:
            # Leeren Zeilenkopf anzeigen und dessen Breite an die Haupttabelle angleichen.
            # So beginnen die Summenspalten an derselben horizontalen Position.
            main_v_header = self.table.verticalHeader()
            summary_v_header = self.summary_view.verticalHeader()
            self.summary_model.setVerticalHeaderLabels([""])
            summary_v_header.setVisible(not main_v_header.isHidden())
            summary_v_header.setFixedWidth(main_v_header.width())
            main_v_header.geometriesChanged.connect(
                lambda: summary_v_header.setFixedWidth(main_v_header.width())
            )

            # Schrift wie Standard, aber fett
            bold_font = QFont(self.table.font())
            bold_font.setBold(True)
            for c in range(self.summary_model.columnCount()):
                it = self.summary_model.item(0, c)
                if it is None:
                    it = QStandardItem("")
                    self.summary_model.setItem(0, c, it)
                it.setEditable(False)
                it.setFont(bold_font)
                it.setTextAlignment(Qt.AlignCenter)
                # Leichter grauer Hintergrund, nur dezent
                it.setBackground(QColor(255, 255, 255))
            self.summary_model.item(0, 0).setText("Summe")
            self.summary_view.setSpan(0, 0, 1, 2)
            # Spaltenbreiten synchronisieren mit der Haupttabelle
            try:
                for c in range(self.model.columnCount()):
                    w = self.table.columnWidth(c) if c < self.table.model().columnCount() else 80
                    self.summary_view.setColumnWidth(c, w)
            except Exception:
                pass
            # Entferne Rahmen und Setze Fixed Height
            self.summary_view.setFrameStyle(1)
            self.summary_view.setShowGrid(False)
        except Exception:
            pass

    def _compute_sums(self):
        #Berechnet Summen der Spalten S(3), S2(4), K(5), K2(6) über self.dc.teachers.
        #Liefert Dictionary mit ints oder 0.
        sums = {"WS": 0, "S": 0, "S2": 0, "K": 0, "K2": 0}
        try:
            for t in getattr(self.dc, "teachers", []) or []:
                def to_int_safe(v):
                    try:
                        s = str(v).strip()
                        return int(s) if s != "" else 0
                    except Exception:
                        return 0
                sums["WS"] += to_int_safe(t.WS)
                sums["S"]  += to_int_safe(t.S)
                sums["S2"] += to_int_safe(getattr(t, "S2", ""))
                sums["K"] += to_int_safe(t.K)
                sums["K2"] += to_int_safe(getattr(t, "K2", ""))
        except Exception:
            pass
        return sums

    def _update_summaries(self):
        #Aktualisiert die Summenzeile (S, S2, K, K2). Wird bei dc.dataChanged und nach Item-Änderungen aufgerufen.
        try:
            sums = self._compute_sums()
            # Flle die Summary-Modellelemente:
            # Wir zeigen in den relevanten Spalten die Summen; andere Spalten leer oder passend beschriftet
            labels = ["Summe", "", str(sums.get("WS", 0)), str(sums.get("S", 0)), str(sums.get("S2", 0)), str(sums.get("K", 0)), str(sums.get("K2", 0)), ""]
            for c, txt in enumerate(labels):
                it = self.summary_model.item(0, c)
                if it is None:
                    it = QStandardItem(txt)
                    self.summary_model.setItem(0, c, it)
                else:
                    it.setText(txt)
                # Setze Font/Bg erneut (falls Model neu erstellt wurde)
                f = it.font() or QFont(self.table.font())
                f.setBold(True)
                it.setFont(f)
                it.setBackground(QColor(255, 255, 255))
            # Synchronisiere Spaltenbreiten
            try:
                for c in range(min(self.model.columnCount(), self.summary_model.columnCount())):
                    w = self.table.columnWidth(c)
                    self.summary_view.setColumnWidth(c, w)
            except Exception:
                pass
            # Force repaint
            self.summary_view.viewport().update()
        except Exception:
            pass

# Dialog zur Eingabe der Belastungsparameter
class WorkloadDialog(QDialog):
    def __init__(self, parent, dc: DataController):
        super().__init__(parent)
        self.dc = dc
        self.setWindowTitle("Belastungsparameter")

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Eingabeelemente gemäß Spezifikation
        # Schriftliche Korrektur (Minuten): 0–600
        self.spin_korr = QSpinBox()
        self.spin_korr.setRange(0, 600)
        self.spin_korr.setValue(int(getattr(self.dc.settings, "workload_korrektur_min", 80)))

        # Faktor Zweitkorrektur: 0.0–1.0 in 0.1
        self.dspin_nach = QDoubleSpinBox()
        self.dspin_nach.setRange(0.0, 1.0)
        self.dspin_nach.setSingleStep(0.1)
        self.dspin_nach.setDecimals(1)
        self.dspin_nach.setValue(float(getattr(self.dc.settings, "workload_faktor_nachkorrektur", 0.5)))

        # Kolloquium Prüfer (Minuten): 0–600
        self.spin_koll = QSpinBox()
        self.spin_koll.setRange(0, 600)
        self.spin_koll.setValue(int(getattr(self.dc.settings, "workload_kolloq_pruefer_min", 90)))

        # Faktor Beisitzer: 0.0–1.0 in 0.1
        self.dspin_beis = QDoubleSpinBox()
        self.dspin_beis.setRange(0.0, 1.0)
        self.dspin_beis.setSingleStep(0.1)
        self.dspin_beis.setDecimals(1)
        self.dspin_beis.setValue(float(getattr(self.dc.settings, "workload_faktor_beisitzer", 0.5)))

        # Unterrichtsaufwand (Minuten): 0–600 (gem. Spezifikation)
        self.spin_unter = QSpinBox()
        self.spin_unter.setRange(0, 600)
        self.spin_unter.setValue(int(getattr(self.dc.settings, "workload_unterricht_aufwand_min", 990)))

        # Beschriftungen exakt wie vorgegeben
        form.addRow("Schriftliche Korrektur (Minuten):", self.spin_korr)
        form.addRow("Faktor Zweitkorrektur:", self.dspin_nach)
        form.addRow("Kolloquium Prüfer (Minuten):", self.spin_koll)
        form.addRow("Faktor Beisitzer:", self.dspin_beis)
        form.addRow("Unterrichsaufwand (Minuten):", self.spin_unter)

        layout.addLayout(form)

        # Buttons analog TimeDialog
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(btns)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def accept(self):
        try:
            s = self.dc.settings
            s.workload_korrektur_min = int(self.spin_korr.value())
            s.workload_faktor_nachkorrektur = float(self.dspin_nach.value())
            s.workload_kolloq_pruefer_min = int(self.spin_koll.value())
            s.workload_faktor_beisitzer = float(self.dspin_beis.value())
            s.workload_unterricht_aufwand_min = int(self.spin_unter.value())
            # Änderungen markieren, Persistenz greift über bestehende Save/Load-Logik
            self.dc._dirty = True
        except Exception:
            pass
        super().accept()

class LogWindow(QDialog):
    def __init__(self, parent, dc: DataController):
        super().__init__(parent)
        self.setWindowTitle("Logbuch")
        # Mindestgröße, damit es nicht kleiner gezogen werden kann
        self.setMinimumSize(700, 450)
        self.resize(900, 600)        
        self.dc = dc
        layout = QVBoxLayout(self)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        box = QDialogButtonBox(QDialogButtonBox.Close)
        layout.addWidget(box)
        box.rejected.connect(self.reject); box.accepted.connect(self.accept)
        self.dc.logMessage.connect(self.append)

    def append(self, msg: str):
        self.text.appendPlainText(msg)

# -------------------------
# main
# -------------------------
def main():
    
    app = QApplication(sys.argv)
    
    #Übersetzungen installieren (vor dem Erzeugen von Widgets!)
    from PySide6.QtCore import QTranslator, QLibraryInfo
    import os, glob

    translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    #print("Qt TranslationsPath:", translations_path)

    tr_qt = QTranslator()
    ok_qt = tr_qt.load("qt_de", translations_path)
    if ok_qt:
        app.installTranslator(tr_qt)

    tr_base = QTranslator()
    ok_base = tr_base.load("qtbase_de", translations_path)
    if ok_base:
        app.installTranslator(tr_base)
    
    app.setFont(FONT_DEFAULT)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
