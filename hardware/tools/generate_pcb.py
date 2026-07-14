#!/usr/bin/env python3
"""Erzeugt hardware/BatterySwitch_Steuerplatine.kicad_pcb (KiCad-6-Format).

Steuerplatine (2 Lagen, THT + 2x SOP-4): Der 40-A-Leistungspfad bleibt
ausserhalb der Platine (Chassis-Aufbau laut docs/aufbau-und-abgleich.md).
Bottom-Lage = GND-Zone (in KiCad mit 'B' fuellen). Ein einfacher Grid-Router
verlegt die Signale; 72-V-Netze bekommen vergroesserten Abstand.
"""

import math
import uuid
from collections import deque
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "BatterySwitch_Steuerplatine.kicad_pcb"


def uid():
    return str(uuid.uuid4())


# Platinenumriss
BX1, BY1, BX2, BY2 = 20.0, 20.0, 132.0, 112.0

# Netze mit 72-V-Potential -> groesserer Abstand beim Routen
HV_NETS = {"V+", "B1F", "B2F", "S1", "S2", "N17", "N18", "N19", "A1", "A2", "K1", "K2"}

NETS = ["GND", "V+", "VCC", "OUT", "NOUT", "KA", "KB", "VM", "ZDK",
        "S1", "S2", "B1F", "B2F", "N1A", "N3A", "RVT",
        "NJ1", "NJ2", "NK1", "NK2", "N17", "N18", "N19",
        "A1", "A2", "K1", "K2", "G1", "SK1", "G2", "SK2",
        "T1B", "T2B", "T3B", "T4B", "LED1A", "LED1K", "LED2A", "LED2K"]
NETID = {n: i + 1 for i, n in enumerate(NETS)}

# ---------------------------------------------------------------------------
# Footprints: name -> dict(pads=[(nr, dx, dy, form, size, drill|None)], silk=[...], smd=False)
# form: 'c'=Kreis, 'r'=Rechteck. Alle Instanzen mit Rotation 0.
# ---------------------------------------------------------------------------

def axial(dx, first_rect=False):
    return dict(pads=[("1", 0, 0, "r" if first_rect else "c", 1.7, 0.8),
                      ("2", dx, 0, "c", 1.7, 0.8)],
                silk=[("line", 1.6, 0, dx - 1.6, 0)])

def axial_v(dy):
    return dict(pads=[("1", 0, 0, "c", 1.7, 0.8), ("2", 0, dy, "c", 1.7, 0.8)],
                silk=[("line", 0, 1.6, 0, dy - 1.6)])

def diode(dx, k_first=True):
    p1, p2 = ("1", "2") if k_first else ("2", "1")
    return dict(pads=[(p1, 0, 0, "r", 1.8, 0.9), (p2, dx, 0, "c", 1.8, 0.9)],
                silk=[("line", 1.7, 0, dx - 1.7, 0), ("line", 2.5, -1, 2.5, 1)])

def diode_v(dy):  # Pad 1 (K) oben
    return dict(pads=[("1", 0, 0, "r", 1.8, 0.9), ("2", 0, dy, "c", 1.8, 0.9)],
                silk=[("line", 0, 1.7, 0, dy - 1.7)])

def inline3(order):  # TO-92-artig, 2,54-Raster; order = Padnummern links->rechts
    return dict(pads=[(order[0], 0, 0, "c", 1.5, 0.8),
                      (order[1], 2.54, 0, "c", 1.5, 0.8),
                      (order[2], 5.08, 0, "c", 1.5, 0.8)],
                silk=[("line", -1.3, 1.6, 6.4, 1.6)])

def term(n):
    return dict(pads=[(str(i + 1), 0, i * 5.08, "r" if i == 0 else "c", 3.0, 1.3)
                      for i in range(n)],
                silk=[("line", -2.5, -2.6, -2.5, (n - 1) * 5.08 + 2.6)])

def hdr(n):
    return dict(pads=[(str(i + 1), 0, i * 2.54, "r" if i == 0 else "c", 1.7, 1.0)
                      for i in range(n)], silk=[])

FOOTPRINTS = {
    "AXH": axial(10.16), "AXH1W": axial(12.7), "AXV": axial_v(10.16),
    "DO41_KA": diode(10.16, True),    # Pad1=K links
    "DO41_AK": diode(10.16, False),   # Pad2=A links (K rechts)
    "DO41V": diode_v(10.16),          # K oben
    "TO92_CBE": inline3(["2", "1", "3"]),   # BC547: C B E
    "TO92_EBC": inline3(["3", "1", "2"]),   # MPSA42: E B C
    "TO126_ECB": inline3(["3", "2", "1"]),  # MJE340: E C B (Datenblatt pruefen!)
    "DIP8": dict(pads=[("1", 0, 0, "r", 1.6, 0.8), ("2", 0, 2.54, "c", 1.6, 0.8),
                       ("3", 0, 5.08, "c", 1.6, 0.8), ("4", 0, 7.62, "c", 1.6, 0.8),
                       ("5", 7.62, 7.62, "c", 1.6, 0.8), ("6", 7.62, 5.08, "c", 1.6, 0.8),
                       ("7", 7.62, 2.54, "c", 1.6, 0.8), ("8", 7.62, 0, "c", 1.6, 0.8)],
                 silk=[("line", 1.3, -1.3, 6.3, -1.3), ("line", 1.3, 8.9, 6.3, 8.9)]),
    "SOP4": dict(smd=True,
                 pads=[("1", -3.3, -1.27, "r", (2.2, 1.3), None),
                       ("2", -3.3, 1.27, "r", (2.2, 1.3), None),
                       ("3", 3.3, 1.27, "r", (2.2, 1.3), None),
                       ("4", 3.3, -1.27, "r", (2.2, 1.3), None)],
                 silk=[("line", -2.2, -2.2, 2.2, -2.2), ("line", -2.2, 2.2, 2.2, 2.2)]),
    "RAD": dict(pads=[("1", 0, 0, "r", 1.6, 0.8), ("2", 2.54, 0, "c", 1.6, 0.8)], silk=[]),
    "RADV": dict(pads=[("1", 0, 0, "r", 1.6, 0.8), ("2", 0, 2.54, "c", 1.6, 0.8)], silk=[]),
    "ELKO": dict(pads=[("1", 0, 0, "r", 1.8, 0.9), ("2", 2.54, 0, "c", 1.8, 0.9)],
                 silk=[("circle", 1.27, 0, 3.2)]),
    "ELKO_GR": dict(pads=[("1", 0, 0, "r", 2.4, 1.1), ("2", 5.08, 0, "c", 2.4, 1.1)],
                    silk=[("circle", 2.54, 0, 5.2)]),
    "TRIM": dict(pads=[("1", 0, 0, "r", 1.7, 0.9), ("2", 0, 2.54, "c", 1.7, 0.9),
                       ("3", 0, 5.08, "c", 1.7, 0.9)],
                 silk=[("line", -2.4, -2.4, 2.4, -2.4)]),
    "LED3": dict(pads=[("1", 0, 0, "r", 1.6, 0.9), ("2", 2.54, 0, "c", 1.6, 0.9)],
                 silk=[("circle", 1.27, 0, 2.4)]),
    "TERM2": term(2), "TERM3": term(3), "TERM4": term(4),
    "HDR2": hdr(2), "HDR4": hdr(4),
}

# ---------------------------------------------------------------------------
# Bestueckung: (Ref, Footprint, Wert, x, y, {Padnr: Netz})
# ---------------------------------------------------------------------------

PARTS = [
    # --- Versorgung (oben) ---
    ("X4", "TERM3", "V+ Eingaenge: B1F B2F GND", 26, 30,
     {"1": "B1F", "2": "B2F", "3": "GND"}),
    ("D1", "DO41_AK", "1N5819", 38, 28, {"2": "B1F", "1": "V+"}),
    ("D2", "DO41_AK", "1N5819", 38, 33.08, {"2": "B2F", "1": "V+"}),
    ("R19A", "AXH", "5k6/0,5W", 56, 28, {"1": "V+", "2": "N19"}),
    ("R19B", "AXH", "5k6/0,5W", 70, 28, {"1": "N19", "2": "ZDK"}),
    ("ZD3", "DO41V", "13V", 84, 28, {"1": "ZDK", "2": "GND"}),
    ("T5", "TO126_ECB", "MJE340", 94, 28, {"1": "ZDK", "2": "V+", "3": "VCC"}),
    ("C12", "RAD", "100n/100V", 56, 34, {"1": "V+", "2": "GND"}),
    ("C1", "ELKO", "100u/25V", 106, 28, {"1": "VCC", "2": "GND"}),
    ("C2", "RAD", "100n", 106, 34, {"1": "VCC", "2": "GND"}),

    # --- Messteiler ---
    ("X5", "TERM2", "Sense: S1 S2", 26, 46, {"1": "S1", "2": "S2"}),
    ("R1A", "AXH", "27k 1%", 36, 44, {"1": "S1", "2": "N1A"}),
    ("R1B", "AXH", "27k 1%", 50, 44, {"1": "N1A", "2": "KA"}),
    ("R2", "AXV", "2k0 1%", 64, 44, {"1": "KA", "2": "GND"}),
    ("C3", "RADV", "100n", 69, 44, {"1": "KA", "2": "GND"}),
    ("R3A", "AXH", "27k 1%", 36, 52, {"1": "S2", "2": "N3A"}),
    ("R3B", "AXH", "27k 1%", 50, 52, {"1": "N3A", "2": "KB"}),
    ("R4", "AXH", "1k8 1%", 36, 60, {"1": "KB", "2": "RVT"}),
    ("RV3", "TRIM", "500R 25G", 52, 60, {"1": "RVT", "2": "GND", "3": "GND"}),
    ("C4", "RADV", "100n", 58, 52, {"1": "KB", "2": "GND"}),

    # --- Komparator ---
    ("U1", "DIP8", "LM393", 78, 46,
     {"1": "OUT", "2": "KB", "3": "KA", "4": "GND",
      "5": "VM", "6": "OUT", "7": "NOUT", "8": "VCC"}),
    ("R7", "AXV", "3k3", 92, 42, {"1": "VCC", "2": "OUT"}),
    ("R8", "AXV", "3k3", 96, 42, {"1": "VCC", "2": "NOUT"}),
    ("R9", "AXV", "47k", 100, 42, {"1": "VCC", "2": "VM"}),
    ("R10", "AXV", "47k", 104, 42, {"1": "VM", "2": "GND"}),
    ("C11", "RADV", "100n", 108, 44, {"1": "VM", "2": "GND"}),

    # --- Einspeisung / Poti-Anschluss ---
    ("JP1", "HDR2", "Abgleich D1", 26, 68, {"1": "KA", "2": "NJ1"}),
    ("R5", "AXH", "150k", 32, 70.54, {"1": "NJ1", "2": "NJ2"}),
    ("JP2", "HDR2", "Abgleich D2", 26, 76, {"1": "KB", "2": "NK1"}),
    ("R6", "AXH", "150k", 32, 78.54, {"1": "NK1", "2": "NK2"}),
    ("X7", "TERM4", "Potis: NJ2 OUT NK2 NOUT", 126, 44,
     {"1": "NJ2", "2": "OUT", "3": "NK2", "4": "NOUT"}),

    # --- Status-LEDs ---
    ("R13", "AXH", "330k", 60, 68, {"1": "OUT", "2": "T3B"}),
    ("T3", "TO92_CBE", "BC547B", 74, 68, {"1": "T3B", "2": "LED1K", "3": "GND"}),
    ("LED1", "LED3", "gruen", 84, 68, {"1": "LED1K", "2": "LED1A"}),
    ("R15", "AXH", "2k2", 90, 62, {"1": "VCC", "2": "LED1A"}),
    ("R14", "AXH", "330k", 60, 76, {"1": "NOUT", "2": "T4B"}),
    ("T4", "TO92_CBE", "BC547B", 74, 76, {"1": "T4B", "2": "LED2K", "3": "GND"}),
    ("LED2", "LED3", "gelb", 84, 76, {"1": "LED2K", "2": "LED2A"}),
    ("R16", "AXH", "2k2", 90, 82, {"1": "VCC", "2": "LED2A"}),

    # --- Gate-Treiber ---
    ("R11", "AXH", "27k", 26, 86, {"1": "OUT", "2": "T1B"}),
    ("T1", "TO92_EBC", "MPSA42", 40, 86, {"1": "T1B", "2": "K1", "3": "GND"}),
    ("OC1", "SOP4", "VOM1271", 56, 86, {"1": "A1", "2": "K1", "3": "SK1", "4": "G1"}),
    ("R17A", "AXH1W", "3k3/1W", 66, 80, {"1": "V+", "2": "N17"}),
    ("R17B", "AXH1W", "3k3/1W", 82, 80, {"1": "N17", "2": "A1"}),
    ("ZD1", "AXH", "15V", 66, 92, {"1": "G1", "2": "SK1"}),
    ("R12", "AXH", "27k", 26, 98, {"1": "NOUT", "2": "T2B"}),
    ("T2", "TO92_EBC", "MPSA42", 40, 98, {"1": "T2B", "2": "K2", "3": "GND"}),
    ("OC2", "SOP4", "VOM1271", 56, 98, {"1": "A2", "2": "K2", "3": "SK2", "4": "G2"}),
    ("R18A", "AXH1W", "3k3/1W", 66, 104, {"1": "V+", "2": "N18"}),
    ("R18B", "AXH1W", "3k3/1W", 82, 104, {"1": "N18", "2": "A2"}),
    ("ZD2", "AXH", "15V", 98, 92, {"1": "G2", "2": "SK2"}),
    ("X6", "TERM4", "Gates: G1 SK1 G2 SK2", 112, 86,
     {"1": "G1", "2": "SK1", "3": "G2", "4": "SK2"}),
]

# ---------------------------------------------------------------------------
# Absolute Padliste aufbauen
# ---------------------------------------------------------------------------

pads = []   # (ref, padnr, x, y, form, size, drill, netname, smd)
for ref, fp, val, x, y, nets in PARTS:
    d = FOOTPRINTS[fp]
    smd = d.get("smd", False)
    for nr, dx, dy, form, size, drill in d["pads"]:
        net = nets.get(nr)
        pads.append((ref, nr, x + dx, y + dy, form, size, drill, net, smd))

# Ueberlappungspruefung der Footprints (grob ueber Padabstaende verschiedener Refs)
def pad_r(size):
    return (max(size) if isinstance(size, tuple) else size) / 2

problems = []
for i in range(len(pads)):
    for j in range(i + 1, len(pads)):
        a, b = pads[i], pads[j]
        if a[0] == b[0]:
            continue
        d = math.hypot(a[2] - b[2], a[3] - b[3])
        if d < pad_r(a[5]) + pad_r(b[5]) + 0.5:
            problems.append((a[0], a[1], b[0], b[1], round(d, 2)))
if problems:
    print("PLATZIERUNGS-KONFLIKTE:")
    for p in problems:
        print("  ", p)
    raise SystemExit(1)
print(f"{len(PARTS)} Bauteile, {len(pads)} Pads, keine Ueberlappungen")

# ---------------------------------------------------------------------------
# Montageloecher (NPTH 3,2 mm)
# ---------------------------------------------------------------------------
MHOLES = [(25, 24), (127, 24), (25, 107), (127, 107)]

# ---------------------------------------------------------------------------
# Router: Dijkstra auf 0,635-mm-Raster, 2 Lagen (0=F.Cu, 1=B.Cu)
# ---------------------------------------------------------------------------
import heapq

G = 0.635
NX = int((BX2 - BX1) / G) + 1
NY = int((BY2 - BY1) / G) + 1

def cell(x, y):
    return (round((x - BX1) / G), round((y - BY1) / G))

def coord(c):
    return (BX1 + c[0] * G, BY1 + c[1] * G)

def clr(net):
    return 0.8 if net in HV_NETS else 0.4

TRACK_W = {"V+": 0.8, "VCC": 0.8}
def width(net):
    return TRACK_W.get(net, 0.6)

# Hindernisse: (x, y, radius, netz|None, lagen) — Radius ohne Clearance
obstacles = []
for ref, nr, x, y, form, size, drill, net, smd in pads:
    layers = (0,) if smd else (0, 1)
    obstacles.append((x, y, pad_r(size), net, layers))
for mx, my in MHOLES:
    obstacles.append((mx, my, 3.1, None, (0, 1)))

routed_tracks = []   # (x1, y1, x2, y2, layer, net, width)
routed_vias = []     # (x, y, net)

def blocked_map(net):
    """Belegt-Raster fuer das Routen von `net` (True = gesperrt)."""
    w2 = width(net) / 2
    blk = [[[False] * NY for _ in range(NX)], [[False] * NY for _ in range(NX)]]
    margin = 1.0
    mcells = int(margin / G) + 1
    for L in (0, 1):
        for i in range(NX):
            for j in range(NY):
                if i < mcells or j < mcells or i >= NX - mcells or j >= NY - mcells:
                    blk[L][i][j] = True
    def mark(cx, cy, r, layers):
        ic, jc = cell(cx, cy)
        rc = int(r / G) + 1
        for i in range(max(0, ic - rc), min(NX, ic + rc + 1)):
            for j in range(max(0, jc - rc), min(NY, jc + rc + 1)):
                x, y = coord((i, j))
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    for L in layers:
                        blk[L][i][j] = True
    for ox, oy, orad, onet, layers in obstacles:
        if onet == net:
            continue
        mark(ox, oy, orad + max(clr(onet) if onet else 0.4, clr(net)) + w2, layers)
    for x1, y1, x2, y2, L, tnet, tw in routed_tracks:
        if tnet == net:
            continue
        r = tw / 2 + max(clr(tnet), clr(net)) + w2
        steps = max(1, int(math.hypot(x2 - x1, y2 - y1) / (G / 2)))
        for s in range(steps + 1):
            mark(x1 + (x2 - x1) * s / steps, y1 + (y2 - y1) * s / steps, r, (L,))
    for vx, vy, vnet in routed_vias:
        if vnet == net:
            continue
        mark(vx, vy, 0.4 + max(clr(vnet), clr(net)) + w2, (0, 1))
    return blk

def route_net(net):
    plist = [(x, y) for ref, nr, x, y, f, s, d, n, smd in pads if n == net]
    if len(plist) < 2:
        return True
    blk = blocked_map(net)
    w = width(net)
    # eigene Padzellen freigeben + exakte Stichleitung Pad -> Rasterzelle
    own_cells = set()
    pad_layers = {}
    for (x, y), th in [((x, y), lay) for ref, nr, x, y, f, sz, dr, n, lay_smd in pads
                       if n == net for lay in [not lay_smd]]:
        c = cell(x, y)
        own_cells.add(c)
        cx, cy = coord(c)
        if abs(cx - x) > 1e-6 or abs(cy - y) > 1e-6:
            routed_tracks.append((x, y, cx, cy, 0, net, w))
        pad_layers[c] = (0, 1) if th else (0,)
    targets = {(cell(*plist[0]), L) for L in pad_layers[cell(*plist[0])]}
    for px, py in plist[1:]:
        start = cell(px, py)
        dist = {}
        prev = {}
        pq = [(0, start, 0)]
        dist[(start, 0)] = 0
        goal = None
        while pq:
            d, c, L = heapq.heappop(pq)
            if dist.get((c, L), 1e18) < d:
                continue
            if (c, L) in targets:
                goal = (c, L)
                break
            i, j = c
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < NX and 0 <= nj < NY:
                    nc = (ni, nj)
                    if blk[L][ni][nj] and nc not in own_cells and (nc, L) not in targets:
                        continue
                    nd = d + 1
                    if nd < dist.get((nc, L), 1e18):
                        dist[(nc, L)] = nd
                        prev[(nc, L)] = (c, L)
                        heapq.heappush(pq, (nd, nc, L))
            # Via
            oL = 1 - L
            if not blk[oL][i][j] or c in own_cells or (c, oL) in targets:
                nd = d + 14
                if nd < dist.get((c, oL), 1e18):
                    dist[(c, oL)] = nd
                    prev[(c, oL)] = (c, L)
                    heapq.heappush(pq, (nd, c, oL))
        if goal is None:
            print(f"  !! Netz {net}: keine Route zu Pad bei {px},{py}")
            return False
        # Pfad rueckverfolgen, in Segmente/Vias umsetzen
        path = [goal]
        while path[-1] in prev:
            path.append(prev[path[-1]])
        path.reverse()
        seg_start = path[0]
        for k in range(1, len(path)):
            (c0, L0), (c1, L1) = path[k - 1], path[k]
            if L0 != L1:  # Via
                x, y = coord(c0)
                if seg_start[0] != c0:
                    flush_seg(seg_start, (c0, L0), net, w)
                routed_vias.append((x, y, net))
                seg_start = (c1, L1)
            else:
                # Richtungswechsel? -> Segment abschliessen
                if k >= 2 and path[k - 2][1] == L0:
                    pi, pj = path[k - 2][0]
                    ci, cj = c0
                    ni, nj = c1
                    if (ci - pi, cj - pj) != (ni - ci, nj - cj):
                        flush_seg(seg_start, (c0, L0), net, w)
                        seg_start = (c0, L0)
        if seg_start[0] != path[-1][0]:
            flush_seg(seg_start, path[-1], net, w)
        for c, L in path:
            targets.add((c, L))
        # Zielpad: beide Lagen falls THT
        for L in pad_layers[cell(px, py)]:
            targets.add((cell(px, py), L))
    return True

def flush_seg(a, b, net, w):
    (ca, La), (cb, Lb) = a, b
    x1, y1 = coord(ca)
    x2, y2 = coord(cb)
    routed_tracks.append((x1, y1, x2, y2, La, net, w))

# Netz-Reihenfolge: HV zuerst, dann nach Ausdehnung
def net_extent(net):
    ps = [(x, y) for ref, nr, x, y, f, s, d, n, smd in pads if n == net]
    if len(ps) < 2:
        return 0
    xs = [p[0] for p in ps]; ys = [p[1] for p in ps]
    return (max(xs) - min(xs)) + (max(ys) - min(ys))

order = [n for n in NETS if n != "GND" and net_extent(n) > 0]
order.sort(key=lambda n: (n not in HV_NETS, net_extent(n)))

fails = []
for n in order:
    print(f"route {n} ...")
    if not route_net(n):
        fails.append(n)
print(f"Routing fertig: {len(routed_tracks)} Segmente, {len(routed_vias)} Vias, "
      f"Fehlschlaege: {fails if fails else 'keine'}")

# ---------------------------------------------------------------------------
# .kicad_pcb schreiben (KiCad-6-Format)
# ---------------------------------------------------------------------------

def f2(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")

out = []
out.append('(kicad_pcb (version 20211014) (generator pcbnew)')
out.append('  (general (thickness 1.6))')
out.append('  (paper "A4")')
out.append('  (title_block (title "BatterySwitch Steuerplatine") (date "2026-07-14") (rev "1")'
           ' (comment 1 "58-72V/40A Akku-Umschalter - Steuerteil; Leistungsteil extern"))')
out.append('''  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (44 "Edge.Cuts" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )''')
out.append('  (setup (pad_to_mask_clearance 0.05) (grid_origin 20 20))')
out.append('  (net 0 "")')
for n in NETS:
    out.append(f'  (net {NETID[n]} "{n}")')

FONT = '(effects (font (size 1 1) (thickness 0.15)))'

for ref, fp, val, X, Y, nets in PARTS:
    d = FOOTPRINTS[fp]
    smd = d.get("smd", False)
    out.append(f'  (footprint "bs:{fp}" (layer "F.Cu") (tstamp {uid()}) (at {f2(X)} {f2(Y)})')
    out.append(f'    (attr {"smd" if smd else "through_hole"})')
    out.append(f'    (fp_text reference "{ref}" (at 2.5 -2.5) (layer "F.SilkS") {FONT} (tstamp {uid()}))')
    out.append(f'    (fp_text value "{val}" (at 2.5 3.6) (layer "F.Fab") {FONT} (tstamp {uid()}))')
    for g in d["silk"]:
        if g[0] == "line":
            _, x1, y1, x2, y2 = g
            out.append(f'    (fp_line (start {f2(x1)} {f2(y1)}) (end {f2(x2)} {f2(y2)})'
                       f' (layer "F.SilkS") (width 0.12) (tstamp {uid()}))')
        elif g[0] == "circle":
            _, cx, cy, dia = g
            out.append(f'    (fp_circle (center {f2(cx)} {f2(cy)}) (end {f2(cx + dia / 2)} {f2(cy)})'
                       f' (layer "F.SilkS") (width 0.12) (fill none) (tstamp {uid()}))')
    for nr, dx, dy, form, size, drill in d["pads"]:
        net = nets.get(nr)
        netstr = f' (net {NETID[net]} "{net}")' if net else ''
        if smd:
            sx, sy = size
            out.append(f'    (pad "{nr}" smd rect (at {f2(dx)} {f2(dy)}) (size {f2(sx)} {f2(sy)})'
                       f' (layers "F.Cu" "F.Paste" "F.Mask"){netstr} (tstamp {uid()}))')
        else:
            shape = "circle" if form == "c" else "rect"
            out.append(f'    (pad "{nr}" thru_hole {shape} (at {f2(dx)} {f2(dy)})'
                       f' (size {f2(size)} {f2(size)}) (drill {f2(drill)})'
                       f' (layers *.Cu *.Mask){netstr} (tstamp {uid()}))')
    out.append('  )')

# Montageloecher als eigene Footprints (NPTH)
for k, (mx, my) in enumerate(MHOLES, 1):
    out.append(f'  (footprint "bs:MH32" (layer "F.Cu") (tstamp {uid()}) (at {f2(mx)} {f2(my)})')
    out.append('    (attr through_hole exclude_from_pos_files exclude_from_bom)')
    out.append(f'    (fp_text reference "H{k}" (at 0 -4) (layer "F.SilkS") {FONT} (tstamp {uid()}))')
    out.append(f'    (fp_text value "M3" (at 0 4) (layer "F.Fab") {FONT} (tstamp {uid()}))')
    out.append(f'    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2)'
               f' (layers *.Cu *.Mask) (tstamp {uid()}))')
    out.append('  )')

# Umriss
out.append(f'  (gr_rect (start {f2(BX1)} {f2(BY1)}) (end {f2(BX2)} {f2(BY2)})'
           f' (layer "Edge.Cuts") (width 0.15) (tstamp {uid()}))')
out.append(f'  (gr_text "BatterySwitch Steuerplatine 58-72V" (at 76 23 0) (layer "F.SilkS")'
           f' (effects (font (size 1.5 1.5) (thickness 0.25))) (tstamp {uid()}))')
out.append(f'  (gr_text "GND-Zone auf B.Cu - in KiCad mit B fuellen" (at 76 109.5 0) (layer "Cmts.User")'
           f' {FONT} (tstamp {uid()}))')

# Leiterbahnen + Vias
LNAME = {0: "F.Cu", 1: "B.Cu"}
for x1, y1, x2, y2, L, net, w in routed_tracks:
    out.append(f'  (segment (start {f2(x1)} {f2(y1)}) (end {f2(x2)} {f2(y2)}) (width {f2(w)})'
               f' (layer "{LNAME[L]}") (net {NETID[net]}) (tstamp {uid()}))')
for vx, vy, net in routed_vias:
    out.append(f'  (via (at {f2(vx)} {f2(vy)}) (size 0.8) (drill 0.4)'
               f' (layers "F.Cu" "B.Cu") (net {NETID[net]}) (tstamp {uid()}))')

# GND-Zone auf der Unterseite
out.append(f'''  (zone (net {NETID["GND"]}) (net_name "GND") (layer "B.Cu") (tstamp {uid()}) (hatch edge 0.5)
    (connect_pads (clearance 0.5))
    (min_thickness 0.25)
    (fill yes (thermal_gap 0.5) (thermal_bridge_width 0.6))
    (polygon (pts (xy {f2(BX1)} {f2(BY1)}) (xy {f2(BX2)} {f2(BY1)}) (xy {f2(BX2)} {f2(BY2)}) (xy {f2(BX1)} {f2(BY2)})))
  )''')

out.append(')')
OUT.write_text("\n".join(out), encoding="utf-8")
print(f"geschrieben: {OUT} ({OUT.stat().st_size} Bytes)")
