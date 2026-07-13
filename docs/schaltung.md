# Schaltungsbeschreibung

Die Schaltung besteht aus fünf Funktionsblöcken:

1. [Versorgung der Steuerelektronik](#1-versorgung-der-steuerelektronik) (Dioden-OR aus beiden Akkus)
2. [Referenz und Messteiler](#2-referenz-und-messteiler) (TL431, Trimmer für die Schwelle)
3. [Komparator mit Poti-Hysterese](#3-komparator-mit-poti-hysterese) (LM393)
4. [Gate-Versorgung](#4-gate-versorgung-ladungspumpe-mit-ne555) (NE555-Ladungspumpe)
5. [Leistungsschalter und Break-before-make-Ansteuerung](#5-leistungsschalter-und-gate-ansteuerung)

Bezeichner (R1, Q1, …) sind konsistent mit der [Stückliste](stueckliste.md).

---

## 1. Versorgung der Steuerelektronik

Die Steuerung wird über zwei Schottky-Dioden aus **beiden** Akkus versorgt, damit sie
auch dann weiterläuft, wenn einer der Akkus leer ist oder abgeklemmt wird.

```
BAT1+ o────|>|──────┬─────────o  V+  (≈ UBat − 0,4 V)
           D1       │
BAT2+ o────|>|──────┤
           D2       │
                   ─┴─ C1
                   ─┬─ 100 µF/25 V  + 100 nF (C2)
                    │
GND   o─────────────┴─────────o  GND (gemeinsame Masse beider Akkus!)
```

Stromaufnahme der gesamten Steuerung: < 10 mA → 1-A-Schottky-Dioden (1N5819) genügen.

## 2. Referenz und Messteiler

Der TL431 liefert eine stabile 2,5-V-Referenz, unabhängig von der schwankenden
Batteriespannung:

```
V+ o──[R5 4,7k]──┬──────o  VREF = 2,50 V
                 │
                ┌┴┐ TL431 (Kathode oben, Referenz an Kathode,
                └┬┘        Anode an GND → feste 2,495 V)
                 │
GND o────────────┘
```

Kathodenstrom ≈ (11,4 V − 2,5 V) / 4,7 kΩ ≈ 1,9 mA (> 1 mA Mindeststrom ✓).

Die Spannung von **Batterie 1** wird über einen Teiler auf Referenzniveau
heruntergeteilt. Der Trimmer RV1 stellt die Schaltschwelle ein:

```
BAT1+ o──[R1 33k]──┬──────o  Knoten A  (zum Komparator IN+)
                   │
                  ─┴─ C3 100 nF   (filtert Störspitzen, entprellt)
                  ─┬─
                   ├──[RV1 10k Trimmer]──[R2 6,8k]──o GND
```

**Schaltschwelle** (ohne Hysterese-Anteil), mit `Rlow = RV1-Anteil + R2` (6,8 … 16,8 kΩ):

```
Uth = 2,5 V · (R1 + Rlow) / Rlow
```

| RV1-Stellung | Rlow    | Uth     |
|--------------|---------|---------|
| 0 Ω          | 6,8 kΩ  | ≈ 14,6 V |
| 5 kΩ (Mitte) | 11,8 kΩ | ≈ 9,5 V  |
| 10 kΩ        | 16,8 kΩ | ≈ 7,4 V  |

Damit ist der gesamte für 12-V-Systeme sinnvolle Bereich abgedeckt (typisch: 11,8 V
für Blei/AGM, ca. 12,0–12,4 V für LiFePO4).

## 3. Komparator mit Poti-Hysterese

Ein LM393 (Open-Collector, verträgt Versorgungs- und Eingangsspannungen bis 36 V)
vergleicht Knoten A mit der 2,5-V-Referenz. Die **Hysterese entsteht durch
Mitkopplung** vom Ausgang zurück auf den nichtinvertierenden Eingang – der
Mitkopplungswiderstand ist das Hysterese-Poti RV2:

```
                         V+
                          │
                         [R4 10k]  (Pull-up, LM393 ist Open-Collector)
                          │
Knoten A o───────┬────────┼──────────────► OUT
                 │      │\│                 │
                 └──────│+ \                │   OUT high = BAT1 aktiv
                        │    ────┬──────────┤   OUT low  = BAT2 aktiv
VREF 2,5V o─────────────│− /     │          │
                        │/       │          │
                                 │          │
                 ┌───[R3 220k]───┴─[RV2 1M Poti]
                 │                     (Hysterese)
Knoten A o───────┘
```

### Funktionsweise

- `U(A) > 2,5 V` → OUT high → Batterie 1 versorgt die Last. Die Mitkopplung hebt
  Knoten A zusätzlich an → Batterie 1 darf bis zur **unteren** Schwelle absinken.
- `U(A) < 2,5 V` → OUT low → Batterie 2 versorgt die Last. Die Mitkopplung zieht
  Knoten A herunter → Batterie 1 muss erst die **obere** Schwelle überschreiten,
  bevor zurückgeschaltet wird.

### Dimensionierung der Hysterese

Mit dem Innenwiderstand des Messteilers `Rth = R1 ∥ Rlow ≈ 7,7 kΩ` (bei 12-V-Einstellung),
dem Mitkopplungswiderstand `Rf = R3 + RV2-Anteil` (220 kΩ … 1,22 MΩ) und dem
Ausgangshub `ΔUout ≈ V+ ≈ 11,4 V` gilt am Knoten A:

```
ΔU(A) = ΔUout · Rth / (Rth + Rf)
```

Auf die Batteriespannung zurückgerechnet (Teilerverhältnis `Uth / 2,5 V ≈ 4,8` bei 12 V):

```
Hysterese  ΔUbat ≈ ΔUout · Rth / (Rth + Rf) · (Uth / 2,5 V)
```

| RV2-Stellung | Rf       | ΔU(A)   | **Hysterese ΔUbat** |
|--------------|----------|---------|----------------------|
| 0 Ω          | 220 kΩ   | 386 mV  | ≈ 1,9 V              |
| 500 kΩ       | 720 kΩ   | 121 mV  | ≈ 0,6 V              |
| 1 MΩ         | 1,22 MΩ  |  72 mV  | ≈ 0,35 V             |

**Einstellbereich der Hysterese: ca. 0,4 … 2,0 V** – kleinere Werte durch größeres R3,
größere Werte durch kleineres R3 erreichbar.

> **Praxis-Hinweis:** Die Hysterese muss größer sein als der Spannungseinbruch der
> Batterie unter Last (bei 40 A an einem 50-Ah-Bleiakku leicht 0,5–1 V), sonst pendelt
> die Schaltung. Deshalb der große Einstellbereich bis 2 V.

Die untere und obere Schwelle liegen bei:

```
Uth_low  = Uth − ΔUbat · (Anteil bei OUT high)     → Umschalten auf BAT2
Uth_high = Uth_low + ΔUbat                          → Rückschalten auf BAT1
```

Der genaue Abgleich erfolgt praktisch mit Labornetzteil, siehe
[Aufbau und Abgleich](aufbau-und-abgleich.md).

## 4. Gate-Versorgung: Ladungspumpe mit NE555

Die N-Kanal-MOSFETs schalten high-side, ihre Gates brauchen daher eine Spannung
**oberhalb** der Batteriespannung. Ein NE555 als Rechteckoszillator (~100 kHz) speist
einen Dioden-Spannungsverdoppler:

```
        V+                                     V+ o──┐
         │                                            │
   ┌─────┴─────┐        C6 100nF        D3           D4
   │  NE555    │ OUT ───┬──||──┬───|>|───┬────|>|────┬────o  VCP ≈ 2·V+ − 1,4 V
   │  astabil  │ (3)    │      │  1N4148 │   1N4148  │       (≈ 21 V)
   │ f ≈ 100kHz│        │      └─────────┘          ─┴─ C7
   └───────────┘        │      (an V+ geklemmt)     ─┬─ 10 µF/35 V
   R6=R7=4,7k, C5=1nF   │                            │
                       GND                          GND
```

- `f = 1,44 / ((R6 + 2·R7) · C5) ≈ 100 kHz`
- `VCP ≈ 2 · V+ − 2 · UF ≈ 21 V` → Gate-Source-Spannung der MOSFETs
  `UGS = VCP − UBat ≈ 9 V` — die IRLB3034 (Logic-Level) sind ab 4,5 V voll
  durchgesteuert, auch bei tiefentladenem Akku (10 V → UGS ≈ 8 V) bleibt Reserve.
- Die Ladungspumpe muss nur die Gate-Pull-ups (2× 100 kΩ ≈ 0,4 mA) treiben –
  die Schaltvorgänge sind statisch, Geschwindigkeit ist unkritisch.

## 5. Leistungsschalter und Gate-Ansteuerung

### Antiserielle MOSFET-Paare

Jeder Batteriezweig besteht aus **zwei antiseriellen N-Kanal-MOSFETs**
(Source an Source, Gates verbunden). Nur so sperrt der Schalter in **beide**
Richtungen – mit einem einzelnen MOSFET würde dessen Body-Diode die inaktive
Batterie weiter mit der Last (bzw. mit der anderen Batterie) verbinden.

```
                 Q1 (IRLB3034)      Q2 (IRLB3034)
BAT1+ o──[F1]────D─┤├─S────────S─┤├─D──────────────┬─────o LAST+
                     │►(Body)  ◄│                  │
                     └────┬─────┘                  │
                        Gate1  ◄── Ansteuerung     │
                                                   │
                 Q3 (IRLB3034)      Q4 (IRLB3034)  │
BAT2+ o──[F2]────D─┤├─S────────S─┤├─D──────────────┘
                     │►        ◄│                 ─┴─ C8 4700 µF/25 V
                     └────┬─────┘                 ─┬─  (Stützkondensator)
                        Gate2  ◄── Ansteuerung     │
                                                  GND
```

**Verlustleistung bei 40 A:** `P = I² · 2 · RDS(on) = 40² · 2 · 1,7 mΩ ≈ 5,5 W`
je aktivem Zweig (2,7 W pro TO-220-Gehäuse) → gemeinsamer Kühlkörper mit
≤ 6 K/W, oder je Zweig ein zweites Paar parallel schalten (halbiert die Verluste).

Ein 15-V-Zener (ZD1/ZD2) zwischen Gate und Source-Knoten jedes Paars schützt die
Gates vor Überspannung (UGS(max) = ±16 V beim IRLB3034; bei Verwendung anderer
Typen mit ±20 V ebenfalls sicher).

### Break-before-make-Ansteuerung

Drei Kleinsignal-NPN (BC547) erzeugen aus dem Komparatorausgang zwei
**komplementäre** Gate-Signale mit „schnell aus, langsam ein“:

```
                                    VCP (≈21 V)              VCP
                                     │                        │
              V+                   [R10 100k]              [R11 100k]
               │                     │                        │
             [R9 47k]                ├──────────o Gate1       ├──────o Gate2
               │                     │  (Q1/Q2) │             │ (Q3/Q4)
OUT o──┬─[R8 47k]─B┤ T3 (BC547)     ─┴─ C9      │            ─┴─ C10
       │           │E                ─┬─ 10nF   │            ─┬─ 10nF
       │          GND                 │        ─┴─            │
       │       Kollektor T3 = /OUT    C        ZD1 15V        C     ZD2 an
       │            │                ┤ T1      an Source-    ┤ T2   Source-
       │            └──[R12 47k]──B──┤ BC547   knoten Q1/Q2  ┤BC547 knoten Q3/Q4
       │                             │E                      │E
       └──────────────[R13 47k]──B───┼───────────────────────┘
                                    GND        (T2-Basis direkt von OUT)
```

**Logik:**

| Zustand           | OUT  | T3 | /OUT | T1  | Gate1 (BAT1) | T2  | Gate2 (BAT2) |
|-------------------|------|----|------|-----|--------------|-----|--------------|
| BAT1 über Schwelle| high | ein| low  | aus | high → **EIN** | ein | low → AUS   |
| BAT1 unter Schwelle| low | aus| high | ein | low → AUS    | aus | high → **EIN** |

**Break-before-make:** Das Ausschalten erfolgt schnell (Transistor zieht das Gate
direkt herunter), das Einschalten langsam über `R10/R11 (100 kΩ) + C9/C10 (10 nF)
+ Gate-Kapazität` → Einschaltverzögerung einige Millisekunden. Dadurch ist beim
Umschalten immer zuerst der alte Zweig vollständig aus, bevor der neue leitet —
**die beiden Akkus werden nie parallel geschaltet** (wichtig, da bei 12,8 V ↔ 11,5 V
Differenz sonst sehr hohe Ausgleichsströme fließen würden).

Während der Totzeit (wenige ms) ist die Last stromlos; der Stützkondensator C8
überbrückt das für Kleinlasten. Motoren, Lampen und die meisten 12-V-Geräte
stört die kurze Lücke nicht. Falls eine unterbrechungsfreie Versorgung zwingend
nötig ist, C8 vergrößern oder der Last einen eigenen Puffer spendieren.

### Status-LEDs

```
OUT  o──[R14 2,2k]──|>|── GND   LED1 grün  „Batterie 1 aktiv“
/OUT o──[R15 2,2k]──|>|── GND   LED2 gelb  „Batterie 2 aktiv“
```

---

## Grenzen und mögliche Erweiterungen

- **Nur Batterie 1 wird überwacht.** Ist Batterie 1 leer, läuft Batterie 2 ohne
  Tiefentladeschutz weiter. Abhilfe: zweite identische Komparatorstufe (der LM393
  enthält bereits einen zweiten, ungenutzten Komparator), die bei leerer Batterie 2
  beide Zweige abschaltet.
- **Kein Laderegler:** Die Schaltung verteilt nur die Entladung. Das Laden beider
  Akkus muss separat erfolgen (Ladegerät, Trennrelais, Ladebooster).
- **Verpolschutz:** Nicht enthalten – bei Verpolung eines Akkus leiten die
  Body-Dioden. Sicherungen F1/F2 begrenzen den Schaden; sorgfältig anschließen.
- **24-V-Betrieb:** Grundsätzlich möglich (LM393/NE555 bis 30 V+), aber Teiler,
  Zener und die MOSFET-Spannungsfestigkeit (IRLB3034: 40 V) prüfen und die
  Ladungspumpe auf einfache statt doppelte Spannung umbauen.
