#!/usr/bin/env python3
"""Erzeugt hardware/BatterySwitch.kicad_sch (KiCad-6-Format, von KiCad 6/7/8/9 lesbar).

Der Schaltplan ist flach (ein Blatt A3). Die Konnektivitaet laeuft ueber
Netz-Labels an kurzen Stichleitungen; Serienketten (z. B. R17A/R17B) sind
Pin-auf-Pin gesetzt. Layout-Aenderungen: Koordinaten unten anpassen und neu
ausfuehren:  python3 hardware/tools/generate_schematic.py
"""

import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "BatterySwitch.kicad_sch"

FONT = "(effects (font (size 1.27 1.27)))"
FONT_HIDE = "(effects (font (size 1.27 1.27)) hide)"


def uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Symboldefinitionen (Bibliothek "bs")
# Pins: (nummer, name, sx, sy, winkel, laenge)   -- Symbolkoordinaten, Y nach oben.
# Winkel = Richtung, in die der Pin ZUM Koerper zeigt (KiCad-Konvention).
# ---------------------------------------------------------------------------

SYMS = {
    "R": dict(
        hide_nums=True, hide_names=True,
        gfx=[("rect", -1.016, -2.54, 1.016, 2.54)],
        pins=[("1", "~", 0, 3.81, 270, 1.27), ("2", "~", 0, -3.81, 90, 1.27)],
    ),
    "RH": dict(
        hide_nums=True, hide_names=True,
        gfx=[("rect", -2.54, -1.016, 2.54, 1.016)],
        pins=[("1", "~", -3.81, 0, 0, 1.27), ("2", "~", 3.81, 0, 180, 1.27)],
    ),
    "POT": dict(
        hide_nums=True, hide_names=True,
        gfx=[("rect", -1.016, -2.54, 1.016, 2.54),
             ("line", [(-2.54, 0), (-1.016, 0)]),
             ("line", [(-1.778, 0.508), (-1.016, 0), (-1.778, -0.508)])],
        pins=[("1", "1", 0, 3.81, 270, 1.27), ("2", "wiper", -3.81, 0, 0, 1.27),
              ("3", "3", 0, -3.81, 90, 1.27)],
    ),
    "C": dict(
        hide_nums=True, hide_names=True,
        gfx=[("line", [(-1.905, 0.762), (1.905, 0.762)]),
             ("line", [(-1.905, -0.762), (1.905, -0.762)])],
        pins=[("1", "~", 0, 2.54, 270, 1.778), ("2", "~", 0, -2.54, 90, 1.778)],
    ),
    "CPOL": dict(
        hide_nums=True, hide_names=True,
        gfx=[("line", [(-1.905, 0.762), (1.905, 0.762)]),
             ("line", [(-1.905, -0.762), (1.905, -0.762)]),
             ("line", [(2.286, 1.524), (3.302, 1.524)]),
             ("line", [(2.794, 1.016), (2.794, 2.032)])],
        pins=[("1", "+", 0, 2.54, 270, 1.778), ("2", "-", 0, -2.54, 90, 1.778)],
    ),
    "D_SCHOTTKY": dict(  # Anode links, Kathode rechts
        hide_nums=True, hide_names=True,
        gfx=[("line", [(-1.27, 1.27), (-1.27, -1.27), (1.27, 0), (-1.27, 1.27)]),
             ("line", [(1.27, 1.27), (1.27, -1.27)]),
             ("line", [(1.27, 1.27), (1.905, 1.27), (1.905, 0.762)]),
             ("line", [(1.27, -1.27), (0.635, -1.27), (0.635, -0.762)])],
        pins=[("2", "A", -3.81, 0, 0, 2.54), ("1", "K", 3.81, 0, 180, 2.54)],
    ),
    "D_ZENER": dict(  # Anode unten, Kathode oben
        hide_nums=True, hide_names=True,
        gfx=[("line", [(-1.27, -1.27), (1.27, -1.27), (0, 1.27), (-1.27, -1.27)]),
             ("line", [(-1.27, 1.27), (1.27, 1.27)]),
             ("line", [(-1.27, 1.27), (-1.778, 1.778)]),
             ("line", [(1.27, 1.27), (1.778, 0.762)])],
        pins=[("1", "K", 0, 3.81, 270, 2.54), ("2", "A", 0, -3.81, 90, 2.54)],
    ),
    "LED": dict(  # Anode oben, Kathode unten
        hide_nums=True, hide_names=True,
        gfx=[("line", [(-1.27, 1.27), (1.27, 1.27), (0, -1.27), (-1.27, 1.27)]),
             ("line", [(-1.27, -1.27), (1.27, -1.27)]),
             ("line", [(1.524, 0.254), (2.286, 1.016)]),
             ("line", [(2.032, -0.254), (2.794, 0.508)])],
        pins=[("2", "A", 0, 3.81, 270, 2.54), ("1", "K", 0, -3.81, 90, 2.54)],
    ),
    "NPN": dict(
        hide_nums=True, hide_names=False,
        gfx=[("rect", -2.54, -3.81, 2.54, 3.81)],
        pins=[("1", "B", -5.08, 0, 0, 2.54), ("2", "C", 0, 6.35, 270, 2.54),
              ("3", "E", 0, -6.35, 90, 2.54)],
    ),
    "NMOS_DL": dict(  # Drain links, Source rechts, Gate unten
        hide_nums=True, hide_names=False,
        gfx=[("rect", -3.81, -2.54, 3.81, 2.54)],
        pins=[("2", "D", -6.35, 0, 0, 2.54), ("3", "S", 6.35, 0, 180, 2.54),
              ("1", "G", 0, -5.08, 90, 2.54)],
    ),
    "NMOS_DR": dict(  # Source links, Drain rechts, Gate unten
        hide_nums=True, hide_names=False,
        gfx=[("rect", -3.81, -2.54, 3.81, 2.54)],
        pins=[("3", "S", -6.35, 0, 0, 2.54), ("2", "D", 6.35, 0, 180, 2.54),
              ("1", "G", 0, -5.08, 90, 2.54)],
    ),
    "VOM1271": dict(
        hide_nums=False, hide_names=False,
        gfx=[("rect", -5.08, -5.08, 5.08, 5.08)],
        pins=[("1", "A", -7.62, 2.54, 0, 2.54), ("2", "K", -7.62, -2.54, 0, 2.54),
              ("4", "+", 7.62, 2.54, 180, 2.54), ("3", "-", 7.62, -2.54, 180, 2.54)],
    ),
    "LM393": dict(
        hide_nums=False, hide_names=False,
        gfx=[("rect", -7.62, -10.16, 7.62, 10.16)],
        pins=[("3", "IN1+", -10.16, 5.08, 0, 2.54), ("2", "IN1-", -10.16, 2.54, 0, 2.54),
              ("5", "IN2+", -10.16, -2.54, 0, 2.54), ("6", "IN2-", -10.16, -5.08, 0, 2.54),
              ("1", "OUT1", 10.16, 5.08, 180, 2.54), ("7", "OUT2", 10.16, -5.08, 180, 2.54),
              ("8", "VCC", 0, 12.7, 270, 2.54), ("4", "GND", 0, -12.7, 90, 2.54)],
    ),
    "CONN2": dict(
        hide_nums=False, hide_names=True,
        gfx=[("rect", -2.54, -5.08, 2.54, 5.08)],
        pins=[("1", "+", 5.08, 2.54, 180, 2.54), ("2", "-", 5.08, -2.54, 180, 2.54)],
    ),
    "FUSE": dict(
        hide_nums=True, hide_names=True,
        gfx=[("rect", -2.54, -0.889, 2.54, 0.889), ("line", [(-2.54, 0), (2.54, 0)])],
        pins=[("1", "~", -3.81, 0, 0, 1.27), ("2", "~", 3.81, 0, 180, 1.27)],
    ),
    "JUMPER": dict(
        hide_nums=True, hide_names=True,
        gfx=[("circle", -1.27, 0, 0.508), ("circle", 1.27, 0, 0.508),
             ("line", [(-1.27, 1.016), (1.27, 1.016)])],
        pins=[("1", "~", -3.81, 0, 0, 2.54), ("2", "~", 3.81, 0, 180, 2.54)],
    ),
}

# Referenz-Praefix -> Symbol fuer Reference-Property in der Bibliothek
LIBREF = {name: "U" for name in SYMS}


def lib_symbol(name: str, d: dict) -> str:
    pn_hide = " hide" if d["hide_names"] else ""
    num_hide = "(pin_numbers hide) " if d["hide_nums"] else ""
    s = [f'    (symbol "bs:{name}" {num_hide}(pin_names (offset 0.508){pn_hide}) (in_bom yes) (on_board yes)']
    s.append(f'      (property "Reference" "U" (id 0) (at 0 0 0) {FONT_HIDE})')
    s.append(f'      (property "Value" "{name}" (id 1) (at 0 0 0) {FONT_HIDE})')
    s.append(f'      (property "Footprint" "" (id 2) (at 0 0 0) {FONT_HIDE})')
    s.append(f'      (property "Datasheet" "" (id 3) (at 0 0 0) {FONT_HIDE})')
    s.append(f'      (symbol "{name}_0_1"')
    for g in d["gfx"]:
        if g[0] == "rect":
            _, x1, y1, x2, y2 = g
            s.append(f'        (rectangle (start {x1} {y1}) (end {x2} {y2})'
                     f' (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type none)))')
        elif g[0] == "line":
            pts = " ".join(f"(xy {p[0]} {p[1]})" for p in g[1])
            s.append(f'        (polyline (pts {pts})'
                     f' (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type none)))')
        elif g[0] == "circle":
            _, cx, cy, r = g
            s.append(f'        (circle (center {cx} {cy}) (radius {r})'
                     f' (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type none)))')
    s.append('      )')
    s.append(f'      (symbol "{name}_1_1"')
    for num, pname, px, py, ang, ln in d["pins"]:
        s.append(f'        (pin passive line (at {px} {py} {ang}) (length {ln})'
                 f' (name "{pname}" {FONT}) (number "{num}" {FONT}))')
    s.append('      )')
    s.append('    )')
    return "\n".join(s)


# ---------------------------------------------------------------------------
# Schaltplan-Aufbau
# ---------------------------------------------------------------------------

body = []          # Wires, Labels, Texte, Symbole
instances = []     # symbol_instances-Eintraege

OUTDIR = {0: "L", 180: "R", 270: "U", 90: "D"}       # Pin-Winkel -> Richtung nach aussen
DIRVEC = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}   # Blattkoordinaten (Y nach unten)
LBL = {"R": (0, "left bottom"), "L": (180, "right bottom"),
       "U": (90, "left bottom"), "D": (270, "right bottom")}


def wire(x1, y1, x2, y2):
    body.append(f'  (wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f}))'
                f' (stroke (width 0) (type default) (color 0 0 0 0)) (uuid {uid()}))')


def label(net, x, y, direction):
    ang, just = LBL[direction]
    body.append(f'  (label "{net}" (at {x:.2f} {y:.2f} {ang})'
                f' (effects (font (size 1.27 1.27)) (justify {just})) (uuid {uid()}))')


def link(x1, y1, x2, y2, net=None):
    """Verbindungsleitung zwischen zwei Pin-Anschlusspunkten, optional mit Label."""
    wire(x1, y1, x2, y2)
    if net:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        label(net, mx, my, "R")


def text(s, x, y, size=2.0):
    body.append(f'  (text "{s}" (at {x:.2f} {y:.2f} 0)'
                f' (effects (font (size {size} {size}) bold) (justify left bottom)) (uuid {uid()}))')


def note(s, x, y):
    body.append(f'  (text "{s}" (at {x:.2f} {y:.2f} 0)'
                f' (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid()}))')


def place(ref, sym, x, y, value, nets, refpos=None, valpos=None):
    """Symbol platzieren. nets: {pinnummer: netzname | None}.
    None  -> Pin bleibt ohne Label (Pin-auf-Pin-Verbindung oder unbenutzt)."""
    d = SYMS[sym]
    su = uid()
    if refpos is None:
        refpos = (x + 2.29, y - 1.27)
    if valpos is None:
        valpos = (x + 2.29, y + 1.27)
    s = [f'  (symbol (lib_id "bs:{sym}") (at {x:.2f} {y:.2f} 0) (unit 1)',
         '    (in_bom yes) (on_board yes)',
         f'    (uuid {su})',
         f'    (property "Reference" "{ref}" (id 0) (at {refpos[0]:.2f} {refpos[1]:.2f} 0)'
         f' (effects (font (size 1.27 1.27)) (justify left)))',
         f'    (property "Value" "{value}" (id 1) (at {valpos[0]:.2f} {valpos[1]:.2f} 0)'
         f' (effects (font (size 1.27 1.27)) (justify left)))',
         f'    (property "Footprint" "" (id 2) (at {x:.2f} {y:.2f} 0) {FONT_HIDE})',
         f'    (property "Datasheet" "" (id 3) (at {x:.2f} {y:.2f} 0) {FONT_HIDE})']
    for num, _n, _px, _py, _ang, _ln in d["pins"]:
        s.append(f'    (pin "{num}" (uuid {uid()}))')
    s.append('  )')
    body.append("\n".join(s))
    instances.append(f'    (path "/{su}" (reference "{ref}") (unit 1) (value "{value}") (footprint ""))')

    for num, _name, px, py, ang, _ln in d["pins"]:
        if num not in nets or nets[num] is None:
            continue
        cx, cy = x + px, y - py               # Symbol- -> Blattkoordinaten
        dx, dy = DIRVEC[OUTDIR[ang]]
        ex, ey = cx + 2.54 * dx, cy + 2.54 * dy
        wire(cx, cy, ex, ey)
        label(nets[num], ex, ey, OUTDIR[ang])


# --------------------------- Abschnitt 1: Leistungspfad --------------------
text("Leistungspfad: Batterien, Sicherungen, MOSFET-Schalter", 20, 22)
note("F1/F2: 50 A mit >= 80 V DC-Zulassung (gPV/NH00) - KEINE Kfz-Sicherungen (32 V)!", 20, 27)

place("X1", "CONN2", 30, 40, "Super Soco Akku 1 (50Ah)", {"1": "B1P", "2": "GND"},
      refpos=(22, 33), valpos=(12, 49))
place("F1", "FUSE", 57, 37.46, "50A gPV", {"1": "B1P", "2": "B1F"}, refpos=(54, 33), valpos=(52, 43))
place("Q1", "NMOS_DL", 85, 37.46, "IRF100P219", {"2": "B1F", "3": "SK1", "1": "G1"},
      refpos=(80, 30), valpos=(76, 51))
place("Q2", "NMOS_DR", 110, 37.46, "IRF100P219", {"3": "SK1", "2": "LOAD", "1": "G1"},
      refpos=(105, 30), valpos=(101, 51))
place("ZD1", "D_ZENER", 130, 55, "15V (Gate-Schutz)", {"1": "G1", "2": "SK1"},
      refpos=(133, 53), valpos=(133, 56))

place("X2", "CONN2", 30, 75, "Super Soco Akku 2 (30Ah)", {"1": "B2P", "2": "GND"},
      refpos=(22, 68), valpos=(12, 84))
place("F2", "FUSE", 57, 72.46, "50A gPV", {"1": "B2P", "2": "B2F"}, refpos=(54, 68), valpos=(52, 78))
place("Q3", "NMOS_DL", 85, 72.46, "IRF100P219", {"2": "B2F", "3": "SK2", "1": "G2"},
      refpos=(80, 65), valpos=(76, 86))
place("Q4", "NMOS_DR", 110, 72.46, "IRF100P219", {"3": "SK2", "2": "LOAD", "1": "G2"},
      refpos=(105, 65), valpos=(101, 86))
place("ZD2", "D_ZENER", 130, 90, "15V (Gate-Schutz)", {"1": "G2", "2": "SK2"},
      refpos=(133, 88), valpos=(133, 91))

note("Antiseriell: Source an Source, sperrt in beide Richtungen.", 62, 58)
note("Empfehlung: je Zweig 2 Paare parallel, dann je Einzelgate 10R.", 62, 62)

place("C8A", "CPOL", 155, 42.54, "470u/100V", {"1": "LOAD", "2": "GND"})
place("C8B", "CPOL", 168, 42.54, "470u/100V", {"1": "LOAD", "2": "GND"})
place("X3", "CONN2", 190, 60, "Last / Controller", {"1": "LOAD", "2": "GND"},
      refpos=(183, 53), valpos=(178, 69))
note("C8: Stuetzkondensator (5-10 ms Umschalt-Totzeit)", 152, 32)

place("F3", "FUSE", 57, 95, "100mA F (Sense 1)", {"1": "B1P", "2": "S1"}, refpos=(50, 91), valpos=(45, 101))
place("F4", "FUSE", 57, 107, "100mA F (Sense 2)", {"1": "B2P", "2": "S2"}, refpos=(50, 103), valpos=(45, 113))
note("Sense-Abgriff direkt an der Akku-Steckerklemme (vor F1/F2)!", 72, 97)

# --------------------------- Abschnitt 2: 12-V-Hilfsspannung ----------------
text("12-V-Hilfsspannung (VCC) aus V+", 240, 22)

place("D1", "D_SCHOTTKY", 250, 35, "1N5819", {"2": "B1F", "1": "V+"}, refpos=(240, 31.5), valpos=(246, 31.5))
place("D2", "D_SCHOTTKY", 250, 47, "1N5819", {"2": "B2F", "1": "V+"}, refpos=(240, 43.5), valpos=(246, 43.5))
place("C12", "C", 270, 60, "100n/100V", {"1": "V+", "2": "GND"})
place("R19A", "R", 285, 35, "5k6/0.5W", {"1": "V+", "2": None})
place("R19B", "R", 285, 42.62, "5k6/0.5W", {"1": None, "2": None})
place("ZD3", "D_ZENER", 285, 60, "13V", {"1": None, "2": "GND"})
link(285, 46.43, 285, 56.19, "ZDK")
place("T5", "NPN", 310, 47, "MJE340", {"1": "ZDK", "2": "V+", "3": "VCC"},
      refpos=(314, 44), valpos=(314, 47))
place("C1", "CPOL", 330, 60, "100u/25V", {"1": "VCC", "2": "GND"})
place("C2", "C", 343, 60, "100n", {"1": "VCC", "2": "GND"})
note("T5 mit Aufsteckkuehlkoerper (ca. 0,6 W)", 300, 70)

# --------------------------- Abschnitt 3: Messteiler ------------------------
text("Messteiler mit Nullabgleich (alpha = 1/28)", 20, 125)

place("R1A", "R", 35, 133, "27k 1%", {"1": "S1", "2": None})
place("R1B", "R", 35, 140.62, "27k 1%", {"1": None, "2": None})
place("R2", "R", 35, 155, "2k0 1%", {"1": None, "2": "GND"})
link(35, 144.43, 35, 151.19, "KA")
place("C3", "C", 50, 155, "100n", {"1": "KA", "2": "GND"})

place("R3A", "R", 75, 133, "27k 1%", {"1": "S2", "2": None})
place("R3B", "R", 75, 140.62, "27k 1%", {"1": None, "2": None})
place("R4", "R", 75, 155, "1k8 1%", {"1": None, "2": None})
link(75, 144.43, 75, 151.19, "KB")
link(75, 158.81, 75, 166.19)
place("RV3", "POT", 75, 170, "500R Trimmer", {"1": None, "2": "GND", "3": "GND"},
      refpos=(78, 168), valpos=(78, 171))
place("C4", "C", 90, 155, "100n", {"1": "KB", "2": "GND"})
note("RV3: Nullabgleich (JP1/JP2 offen, U(KA)=U(KB))", 20, 182)

# --------------------------- Abschnitt 4: Komparator ------------------------
text("Differenzkomparator + Inverter (LM393)", 125, 125)

place("U1", "LM393", 150, 150, "LM393", {"3": "KA", "2": "KB", "1": "OUT",
                                          "5": "VM", "6": "OUT", "7": "NOUT",
                                          "8": "VCC", "4": "GND"},
      refpos=(144, 133), valpos=(139, 171))
place("R7", "R", 180, 133, "3k3", {"1": "VCC", "2": "OUT"})
place("R8", "R", 192, 133, "3k3", {"1": "VCC", "2": "NOUT"})
place("R9", "R", 206, 133, "47k", {"1": "VCC", "2": None})
place("R10", "R", 206, 150, "47k", {"1": None, "2": "GND"})
link(206, 136.81, 206, 146.19, "VM")
place("C11", "C", 220, 150, "100n", {"1": "VM", "2": "GND"})
note("OUT high = Akku 1 aktiv, NOUT = invertiert (U1b)", 125, 172)

# --------------------------- Abschnitt 5: Hysterese-Potis -------------------
text("Einstellbare Umschalt-Offsets (Mitkopplung)", 250, 125)

place("JP1", "JUMPER", 260, 133, "Abgleich D1", {"1": "KA", "2": "NJ1"}, refpos=(256, 128), valpos=(252, 139))
place("R5", "RH", 280, 133, "150k", {"1": "NJ1", "2": "NJ2"}, refpos=(277, 128), valpos=(277, 139))
place("RV1", "POT", 300, 140, "1M lin (Delta1)", {"1": "NJ2", "2": "OUT", "3": "OUT"},
      refpos=(303, 138), valpos=(303, 141))

place("JP2", "JUMPER", 260, 160, "Abgleich D2", {"1": "KB", "2": "NK1"}, refpos=(256, 155), valpos=(252, 166))
place("R6", "RH", 280, 160, "150k", {"1": "NK1", "2": "NK2"}, refpos=(277, 155), valpos=(277, 166))
place("RV2", "POT", 300, 167, "1M lin (Delta2)", {"1": "NK2", "2": "NOUT", "3": "NOUT"},
      refpos=(303, 165), valpos=(303, 168))
note("Delta1: U1 < U2 - D1 -> Akku 2 | Delta2: U2 < U1 - D2 -> Akku 1", 250, 180)
note("Je Richtung ca. 0,4-2,9 V + fester Zusatz 0,1-0,8 V", 250, 184)

# --------------------------- Abschnitt 6: Status-LEDs -----------------------
text("Status-LEDs", 345, 125)

place("R15", "R", 355, 133, "2k2", {"1": "VCC", "2": None})
place("LED1", "LED", 355, 148, "gruen (Akku 1)", {"2": None, "1": None},
      refpos=(358, 146), valpos=(358, 149))
place("T3", "NPN", 355, 168, "BC547B", {"1": None, "2": None, "3": "GND"},
      refpos=(359, 166), valpos=(359, 169))
place("R13", "RH", 337, 168, "330k", {"1": "OUT", "2": None}, refpos=(334, 163), valpos=(334, 174))
link(355, 136.81, 355, 144.19)
link(355, 151.81, 355, 161.65)
link(340.81, 168, 349.92, 168)

place("R16", "R", 390, 133, "2k2", {"1": "VCC", "2": None})
place("LED2", "LED", 390, 148, "gelb (Akku 2)", {"2": None, "1": None},
      refpos=(393, 146), valpos=(393, 149))
place("T4", "NPN", 390, 168, "BC547B", {"1": None, "2": None, "3": "GND"},
      refpos=(394, 166), valpos=(394, 169))
place("R14", "RH", 372, 168, "330k", {"1": "NOUT", "2": None}, refpos=(369, 163), valpos=(369, 174))
link(390, 136.81, 390, 144.19)
link(390, 151.81, 390, 161.65)
link(375.81, 168, 384.92, 168)

# --------------------------- Abschnitt 7: Gate-Treiber ----------------------
text("Gate-Treiber: Photovoltaik-Koppler VOM1271 (potentialfrei, break-before-make)", 20, 205)

place("R17A", "R", 35, 212, "3k3/1W", {"1": "V+", "2": None})
place("R17B", "R", 35, 219.62, "3k3/1W", {"1": None, "2": "A1"})
place("OC1", "VOM1271", 70, 232, "VOM1271", {"1": "A1", "2": "K1", "4": "G1", "3": "SK1"},
      refpos=(64, 222), valpos=(64, 242))
place("T1", "NPN", 40, 245, "MPSA42 (300V!)", {"1": None, "2": "K1", "3": "GND"},
      refpos=(44, 243), valpos=(44, 246))
place("R11", "RH", 22, 245, "27k", {"1": "OUT", "2": None}, refpos=(19, 240), valpos=(19, 251))
link(25.81, 245, 34.92, 245)
note("OUT high -> T1 ein -> OC1 -> Akku-1-Zweig EIN", 20, 262)

place("R18A", "R", 130, 212, "3k3/1W", {"1": "V+", "2": None})
place("R18B", "R", 130, 219.62, "3k3/1W", {"1": None, "2": "A2"})
place("OC2", "VOM1271", 165, 232, "VOM1271", {"1": "A2", "2": "K2", "4": "G2", "3": "SK2"},
      refpos=(159, 222), valpos=(159, 242))
place("T2", "NPN", 135, 245, "MPSA42 (300V!)", {"1": None, "2": "K2", "3": "GND"},
      refpos=(139, 243), valpos=(139, 246))
place("R12", "RH", 117, 245, "27k", {"1": "NOUT", "2": None}, refpos=(114, 240), valpos=(114, 251))
link(120.81, 245, 129.92, 245)
note("NOUT high -> T2 ein -> OC2 -> Akku-2-Zweig EIN", 115, 262)

note("Einschalten langsam (uA-Fotostrom, 5-10 ms), Ausschalten schnell (<1 ms,", 210, 232)
note("integrierte Entladung) -> Akkus werden nie parallel geschaltet.", 210, 236)
note("Gate/Source-Leitungen (G1/SK1, G2/SK2) kurz und verdrillt fuehren.", 210, 242)

# --------------------------- Datei zusammensetzen ---------------------------

libsyms = "\n".join(lib_symbol(n, d) for n, d in SYMS.items())

doc = f'''(kicad_sch (version 20211123) (generator eeschema)

  (uuid {uid()})

  (paper "A3")

  (title_block
    (title "BatterySwitch - Automatischer 2-Akku-Umschalter")
    (date "2026-07-13")
    (rev "1")
    (comment 1 "58-72 V, 40 A Dauerstrom, Differenzvergleich mit 2 Hysterese-Potis")
    (comment 2 "Details: docs/schaltung.md")
  )

  (lib_symbols
{libsyms}
  )

{chr(10).join(body)}

  (sheet_instances
    (path "/" (page "1"))
  )

  (symbol_instances
{chr(10).join(instances)}
  )
)
'''

OUT.write_text(doc, encoding="utf-8")
print(f"geschrieben: {OUT} ({len(doc)} Bytes)")
