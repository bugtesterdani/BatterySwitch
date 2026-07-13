# Schaltungsbeschreibung

Die Schaltung vergleicht die Spannungen **beider Akkus direkt miteinander**
(differentiell) – es gibt keine feste Umschaltspannung:

- Zustand **„Akku 1 aktiv“**: Umschalten auf Akku 2, sobald `U1 < U2 − Δ1`
- Zustand **„Akku 2 aktiv“**: Zurückschalten auf Akku 1, sobald `U2 < U1 − Δ2`

Δ1 und Δ2 werden mit **zwei getrennten Potis** eingestellt (je ca. 0,3 … 2,3 V).
Konstruktionsbedingt kommt eine **feste Zusatzhysterese** hinzu (ca. 0,1 … 0,5 V je
Richtung, siehe unten), sodass das Umschaltfenster nie kollabiert und die Schaltung
auch bei knapp eingestellten Potis nur selten schaltet.

Funktionsblöcke:

1. [Versorgung der Steuerelektronik](#1-versorgung-der-steuerelektronik)
2. [Messteiler mit Nullabgleich](#2-messteiler-mit-nullabgleich)
3. [Differenzkomparator mit zwei Hysterese-Potis](#3-differenzkomparator-mit-zwei-hysterese-potis)
4. [Gate-Versorgung (NE555-Ladungspumpe)](#4-gate-versorgung-ladungspumpe-mit-ne555)
5. [Leistungsschalter und Gate-Ansteuerung](#5-leistungsschalter-und-gate-ansteuerung)

Bezeichner (R1, Q1, …) sind konsistent mit der [Stückliste](stueckliste.md).

---

## 1. Versorgung der Steuerelektronik

Die Steuerung wird über zwei Schottky-Dioden aus **beiden** Akkus versorgt (Dioden-OR),
damit sie weiterläuft, solange mindestens ein Akku Spannung liefert:

```
BAT1+ o────|>|──────┬─────────o  V+  (≈ max(U1, U2) − 0,4 V)
           D1       │
BAT2+ o────|>|──────┤
           D2       │
                   ─┴─ C1
                   ─┬─ 100 µF/25 V  + 100 nF (C2, je IC eines)
                    │
GND   o─────────────┴─────────o  GND (gemeinsame Masse beider Akkus!)
```

Stromaufnahme der gesamten Steuerung: < 10 mA → 1N5819 (1 A) genügt.

## 2. Messteiler mit Nullabgleich

Beide Akkuspannungen werden mit **identischen Teilern** (÷5) auf das
Eingangsspannungsniveau des Komparators gebracht. Die Messleitungen (Sense) werden
**direkt an den Batteriepolen** abgegriffen, nicht am Lastpfad:

```
BAT1+ (Sense) o──[R1 33k]──┬─────o  Knoten A  (→ Komparator IN+)
                          ─┴─ C3 100 nF
                          ─┬─
                           ├──[R2 8,2k]──o GND

BAT2+ (Sense) o──[R3 33k]──┬─────o  Knoten B  (→ Komparator IN−)
                          ─┴─ C4 100 nF
                          ─┬─
                           ├──[R4 7,5k]──[RV3 1k Trimmer]──o GND
```

- Teilerverhältnis `α = 8,2k / 41,2k ≈ 0,199` → bei 12,4 V liegen die Knoten bei ≈ 2,5 V
  (Innenwiderstand je Knoten `Rth = R1 ∥ R2 ≈ 6,6 kΩ`).
- **RV3 gleicht die Toleranzen der Teilerwiderstände ab** (Nullabgleich). Selbst mit
  1-%-Widerständen kann der Vergleichsfehler sonst ±0,2 V (auf Batterieebene) betragen –
  zu viel gegenüber Δ-Einstellungen ab 0,4 V. Abgleichprozedur siehe
  [Aufbau und Abgleich](aufbau-und-abgleich.md).
- C3/C4 filtern Störspitzen. Nicht wesentlich vergrößern (max. ≈ 470 nF), sonst wird
  die Mitkopplung des Komparators zu träge.

## 3. Differenzkomparator mit zwei Hysterese-Potis

Kern der Schaltung ist ein LM393 (Dual-Komparator, Open-Collector, bis 36 V).
**Komparator U1a** vergleicht Knoten A (Akku 1) mit Knoten B (Akku 2).
**Komparator U1b** arbeitet als Inverter und erzeugt das Gegensignal /OUT.

Die beiden Offsets Δ1 und Δ2 entstehen durch **zustandsabhängige Stromeinspeisung**
in die Messknoten: Poti RV1 speist von OUT in Knoten A, Poti RV2 speist von /OUT in
Knoten B. Es ist immer genau eine der beiden Einspeisungen aktiv (high):

```
                       V+                            V+
                        │                             │
                      [R7 4,7k]                     [R8 4,7k]
                        │                             │
 Knoten A o────┬────────┼────► OUT                    ├────► /OUT
               │      │\│      (high = Akku 1 aktiv)  │
               └──────│+ \                          │\│
                      │    ────┬────────────────────│− \
 Knoten B o───┬───────│− /     │                    │    ──────┬──► /OUT
              │       │/ U1a   │       V+ ──[R9 47k]│+ /       │
              │                │            ├───────│/ U1b     │
              │                │   [R10 47k]│ = V+/2, C11 100n │
              │                │           GND                 │
              │                │                               │
              │                └──[JP1]──[R5 150k]──[RV1 1M]──┐│
 Knoten A o───┼───────────────────────────────────────────────┘│  (Δ1)
              │                                                 │
              └──────[JP2]──[R6 150k]──[RV2 1M]─────────────────┘  (Δ2)
```

*(JP1/JP2 sind Jumper, die nur für den Nullabgleich geöffnet werden.)*

### Funktionsweise

**Zustand „Akku 1 aktiv“ (OUT high, /OUT low):**
RV1 speist Strom von OUT (≈ V+) in Knoten A → Akku 1 „wirkt“ um Δ1 höher.
Gleichzeitig zieht RV2 den Knoten B leicht Richtung /OUT (= 0 V) → kleiner fester
Zusatz. Der Komparator kippt erst, wenn

```
U1  <  U2 − Δ1        (Umschalten auf Akku 2)
```

**Zustand „Akku 2 aktiv“ (OUT low, /OUT high):**
Jetzt speist RV2 von /OUT in Knoten B → Akku 2 „wirkt“ um Δ2 höher, RV1 zieht
Knoten A leicht herunter. Zurückgeschaltet wird erst, wenn

```
U2  <  U1 − Δ2        (Zurückschalten auf Akku 1)
```

Das gesamte Umschaltfenster beträgt `Δ1 + Δ2` – nach jedem Umschalten muss sich das
Spannungsverhältnis der Akkus also um mindestens dieses Fenster ändern, bevor wieder
geschaltet wird. Zusammen mit der festen Zusatzhysterese ist das Fenster **minimal
≈ 0,65 V, typisch 1,5 … 2 V** – die Schaltung schaltet daher selten (Minuten- bis
Stundentakt beim Leerfahren), und der Stützkondensator C8 wird durch die
Umschalt-Totzeiten nicht nennenswert belastet.

### Dimensionierung

Einspeisung von OUT (High-Pegel ≈ V+ − 0,5 V ≈ 11,1 V, Knotenspannung ≈ 2,4 V) über
`Rf = R5 + RV1-Anteil` in einen Knoten mit `Rth ≈ 6,6 kΩ`:

```
Δ (eigener Anteil)  ≈ (UOUT,high − UKnoten) · Rth / (Rth + Rf) / α
Δ (fester Zusatz)   ≈  UKnoten · Rth / (Rth + Rf,anderes Poti) / α
Δ1_eff = Δ1(RV1, eigener Anteil) + Zusatz(RV2)      (Δ2 analog mit vertauschten Rollen)
```

| Poti-Stellung | Rf      | eigener Anteil | fester Zusatz fürs **andere** Δ |
|---------------|---------|----------------|----------------------------------|
| 0 Ω           | 150 kΩ  | ≈ 1,85 V       | ≈ 0,51 V                         |
| 250 kΩ        | 400 kΩ  | ≈ 0,71 V       | ≈ 0,20 V                         |
| 500 kΩ        | 650 kΩ  | ≈ 0,44 V       | ≈ 0,12 V                         |
| 1 MΩ          | 1,15 MΩ | ≈ 0,25 V       | ≈ 0,07 V                         |

**Einstellbereich je Richtung: ca. 0,3 … 2,3 V.**

Zwei bewusste Eigenschaften dieser einfachen Lösung (für den Einsatzzweck unkritisch,
da beide Potis ohnehin empirisch nachjustiert werden):

1. **Leichte gegenseitige Beeinflussung:** Jedes Poti trägt über den festen Zusatz
   ca. 10–25 % zum jeweils *anderen* Δ bei → beim Einstellen wechselseitig
   nachjustieren. Genau dieser Zusatz liefert die gewünschte feste Extra-Hysterese
   („nochmal ~0,5 V obendrauf“), damit nicht zu oft geschaltet wird.
2. **Δ skaliert schwach mit V+** (±15 % über 10,5 … 13,5 V Batteriespannung), da aus
   der Versorgung eingespeist wird.

### Inverter U1b

Der zweite LM393-Komparator vergleicht OUT mit V+/2 (R9/R10 = 47 kΩ, C11 100 nF)
und liefert /OUT mit sauberem Pegel (Pull-up R8). /OUT steuert die Einspeisung von
Δ2, die Gate-Logik von Schalter 1 und die LED „Akku 2 aktiv“.

### Verhalten beim Einschalten

Liegen beide Akkuspannungen beim Einschalten innerhalb des Fensters
(|U1 − U2| < Δ), ist der Anfangszustand nicht definiert – die Schaltung wählt
zufällig einen Akku und bleibt dort stabil. Das ist unkritisch.

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
   R19=R20=4,7k, C5=1nF │                            │
                       GND                          GND
```

- `f = 1,44 / ((R19 + 2·R20) · C5) ≈ 100 kHz`
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
Gates vor Überspannung (UGS(max) = ±16 V beim IRLB3034).

### Break-before-make-Ansteuerung

Zwei Kleinsignal-NPN schalten die Gates mit „schnell aus, langsam ein“:

```
                        VCP (≈21 V)                  VCP
                         │                            │
                       [R17 100k]                   [R18 100k]
                         │                            │
                         ├──────o Gate1 (Q1/Q2)       ├──────o Gate2 (Q3/Q4)
                        ─┴─ C9 10nF │                ─┴─ C10 10nF │
                        ─┬─        ─┴─ ZD1           ─┬─         ─┴─ ZD2
                         │C         │ an Source-      │C          │ an Source-
/OUT o───[R11 470k]──B──┤ T1        │ knoten Q1/Q2    │           │ knoten Q3/Q4
                         │E BC547                     │
                        GND              OUT o───[R12 470k]──B──┤ T2 (BC547)
                                                                 │E
                                                                GND
```

**Logik:**

| Zustand       | OUT  | /OUT | T1  | Gate1 (BAT1)   | T2  | Gate2 (BAT2)   |
|---------------|------|------|-----|----------------|-----|----------------|
| Akku 1 aktiv  | high | low  | aus | high → **EIN** | ein | low → AUS      |
| Akku 2 aktiv  | low  | high | ein | low → AUS      | aus | high → **EIN** |

**Break-before-make:** Das Ausschalten erfolgt schnell (Transistor zieht das Gate
direkt herunter), das Einschalten langsam über `R17/R18 (100 kΩ) + C9/C10 (10 nF)
+ Gate-Kapazität` → Einschaltverzögerung einige Millisekunden. Dadurch ist beim
Umschalten immer zuerst der alte Zweig vollständig aus, bevor der neue leitet —
**die beiden Akkus werden nie parallel geschaltet** (wichtig, da sie beim Umschalten
konstruktionsbedingt Δ Volt Differenz haben und sonst hohe Ausgleichsströme flössen).

Während der Totzeit (wenige ms) ist die Last stromlos; der Stützkondensator C8
überbrückt das für Kleinlasten. Motoren, Lampen und die meisten 12-V-Geräte
stört die kurze Lücke nicht. Da das Umschaltfenster Δ1 + Δ2 groß ist, tritt die
Totzeit nur selten auf und C8 altert dadurch nicht nennenswert.

### Status-LEDs

Die LEDs werden über eigene Transistoren getrieben, damit sie die Pegel von
OUT//OUT (Einspeisequellen für Δ1/Δ2!) nicht verfälschen:

```
V+ ──[R15 2,2k]──|>|──C┤ T3 (BC547)   Basis ← OUT  via R13 330k
     LED1 grün         │E             „Akku 1 aktiv“
                      GND
V+ ──[R16 2,2k]──|>|──C┤ T4 (BC547)   Basis ← /OUT via R14 330k
     LED2 gelb         │E             „Akku 2 aktiv“
                      GND
```

---

## Grenzen und mögliche Erweiterungen

- **Kein absoluter Tiefentladeschutz:** Die Schaltung vergleicht nur *relativ*.
  Beim Leerfahren wechseln sich die Akkus ab („Leapfrog“: Akku 1 bricht ein →
  Akku 2 übernimmt → Akku 2 sinkt unter Akku 1 − Δ2 → zurück usw.) und werden
  gemeinsam entladen – gewollt, um beide Kapazitäten zu nutzen. Es gibt aber
  **keine Abschaltung bei komplett leeren Akkus**. Für Blei-Akkus einen externen
  Tiefentladeschutz (Low-Voltage-Disconnect) hinter den Ausgang schalten oder
  einen zweiten LM393 als Absolut-Wächter ergänzen.
- **Kein Laderegler:** Die Schaltung verteilt nur die Entladung. Das Laden beider
  Akkus muss separat erfolgen (Ladegerät, Trennrelais, Ladebooster). Wird ein Akku
  geladen, während der andere entladen ist, schaltet die Last automatisch auf den
  geladenen Akku – das ist gewolltes Verhalten des Differenzvergleichs.
- **Verpolschutz:** Nicht enthalten – bei Verpolung eines Akkus leiten die
  Body-Dioden. Sicherungen F1/F2 begrenzen den Schaden; sorgfältig anschließen.
- **24-V-Betrieb:** Grundsätzlich möglich (LM393/NE555 bis 30 V+), aber Teiler,
  Zener und MOSFET-Spannungsfestigkeit (IRLB3034: 40 V) prüfen und die
  Ladungspumpe auf einfache statt doppelte Spannung umbauen.
