# Schaltungsbeschreibung

**Systemspannung: 58 … 72 V** (Akkus mit ca. 71,x V Ladeschluss- und ca. 58 V
Entladeschlussspannung, z. B. 17s-Li-Ion oder 20s-LiFePO4).

Die Schaltung vergleicht die Spannungen **beider Akkus direkt miteinander**
(differentiell) – es gibt keine feste Umschaltspannung:

- Zustand **„Akku 1 aktiv“**: Umschalten auf Akku 2, sobald `U1 < U2 − Δ1`
- Zustand **„Akku 2 aktiv“**: Zurückschalten auf Akku 1, sobald `U2 < U1 − Δ2`

Δ1 und Δ2 werden mit **zwei getrennten Potis** eingestellt (je ca. 0,4 … 2,9 V).
Konstruktionsbedingt kommt eine **feste Zusatzhysterese** hinzu (ca. 0,1 … 0,8 V je
Richtung, siehe unten), sodass das Umschaltfenster nie kollabiert und die Schaltung
auch bei knapp eingestellten Potis nur selten schaltet.

> **Achtung – 72 V DC:** Spannungen über 60 V DC gelten nicht mehr als
> Schutzkleinspannung. Berührungsschutz vorsehen, isoliertes Werkzeug verwenden,
> niemals unter Spannung arbeiten. DC-Lichtbögen beim Trennen unter Last beachten.

Funktionsblöcke:

1. [Hilfsspannung VCC (12 V) aus 72 V](#1-hilfsspannung-vcc-12-v-aus-72-v)
2. [Messteiler mit Nullabgleich](#2-messteiler-mit-nullabgleich)
3. [Differenzkomparator mit zwei Hysterese-Potis](#3-differenzkomparator-mit-zwei-hysterese-potis)
4. [Gate-Ansteuerung mit Photovoltaik-Treibern](#4-gate-ansteuerung-mit-photovoltaik-treibern)
5. [Leistungsschalter](#5-leistungsschalter)

Bezeichner (R1, Q1, …) sind konsistent mit der [Stückliste](stueckliste.md).

---

## 1. Hilfsspannung VCC (12 V) aus 72 V

Der LM393 (max. 36 V) kann nicht direkt an 72 V betrieben werden. Ein einfacher
Längsregler aus Zener + Hochvolt-NPN erzeugt eine 12-V-Hilfsschiene. Versorgt wird
er über zwei Schottky-Dioden aus **beiden** Akkus (Dioden-OR), damit die Steuerung
weiterläuft, solange mindestens ein Akku Spannung liefert:

```
BAT1+ o────|>|──────┬──────────────────────┬────o  V+ (≈ max(U1,U2) − 0,4 V)
           D1       │                      │
BAT2+ o────|>|──────┤            [R19a 5,6k / 0,5 W]
           D2      ─┴─ C12               [R19b 5,6k / 0,5 W]
                   ─┬─ 100nF/100V          │
                    │                      ├──────B┤ T5 (MJE340, 300 V)
                    │                      │       │E
                    │                     ─┴─      ├────────o  VCC ≈ 12,3 V
                    │                  ZD3 ▲ 13V  ─┴─ C1 100 µF/25 V
                    │                     ─┬─     ─┬─  + C2 100 nF
GND   o─────────────┴──────────────────────┴──────┴─────────o  GND
                     (Minus beider Akku-Stecker im Kabelbaum verbunden)
```

- Zenerstrom: `(V+ − 13 V) / 11,2 kΩ ≈ 4 … 5 mA`
- T5 verheizt `(V+ − 12,3 V) · ILast ≈ 0,6 W` → TO-126 mit kleinem Aufsteckkühlkörper
- Gesamt-Eigenverbrauch der Schaltung (inkl. Messteiler, Status-LED und
  Optokoppler-LED): **ca. 25 mA aus 72 V ≈ 1,8 W** (≈ 0,6 Ah/Tag)

## 2. Messteiler mit Nullabgleich

Beide Akkuspannungen werden mit **identischen Teilern** (÷28) auf das
Eingangsspannungsniveau des Komparators gebracht. Der Sense-Abgriff (über flinke
100-mA-Sicherungen F3/F4 – eine gequetschte Sense-Leitung an 72 V ist sonst ein
Brandrisiko) erfolgt **direkt an der Anschlussklemme des Akku-Steckers im
Umschalter, vor der Hauptsicherung** – an die Batteriepole selbst kommt man bei
Steckakkus nicht heran, und das ist auch nicht nötig: Abfälle *hinter* dem
Abgriff (F1/F2, MOSFETs) gehen nicht in die Messung ein. Nur Akkukabel und
Steckerkontakt *vor* dem Abgriff wirken als kleiner Messfehler (~0,1–0,3 V bei
40 A, nur beim aktiven Akku) – gleiche Richtung wie der Lasteinbruch, also
unkritisch, solange beide Zuleitungen ähnlich ausgeführt sind:

```
BAT1+ (Sense) o──[F3]──[R1a 27k]──[R1b 27k]──┬─────o  Knoten A  (→ IN+)
                                            ─┴─ C3 100 nF
                                            ─┬─
                                             ├──[R2 2,0k]──o GND

BAT2+ (Sense) o──[F4]──[R3a 27k]──[R3b 27k]──┬─────o  Knoten B  (→ IN−)
                                            ─┴─ C4 100 nF
                                            ─┬─
                                             ├──[R4 1,8k]──[RV3 500Ω Trimmer]──o GND
```

- Teilerverhältnis `α = 2k / 56k ≈ 0,0357` → Knotenspannung ≈ 2,1 V (58 V) … 2,55 V (71,4 V);
  Innenwiderstand je Knoten `Rth = 54k ∥ 2k ≈ 1,93 kΩ`.
- Der obere Teilerwiderstand ist **aufgeteilt in 2× 27 kΩ** (Spannungs- und
  Verlustleistungsreserve; ≈ 35 V und 45 mW je Widerstand).
- **RV3 gleicht die Toleranzen der Teiler ab** (Nullabgleich). Bei ÷28-Teilung
  erzeugen schon 1-%-Widerstände bis zu ±1 V scheinbare Differenz auf
  Batterieebene – ohne Abgleich unbrauchbar. Prozedur siehe
  [Aufbau und Abgleich](aufbau-und-abgleich.md). R1–R4 als Metallfilm 1 %
  (besser 0,1 %), beide Teiler thermisch benachbart aufbauen (gleiche Drift).
- C3/C4 filtern Störspitzen. Nicht wesentlich vergrößern (max. ≈ 470 nF), sonst
  wird die Mitkopplung des Komparators zu träge.

## 3. Differenzkomparator mit zwei Hysterese-Potis

Kern der Schaltung ist ein LM393 (Dual-Komparator, Open-Collector), betrieben an
VCC = 12 V. **Komparator U1a** vergleicht Knoten A (Akku 1) mit Knoten B (Akku 2).
**Komparator U1b** arbeitet als Inverter und erzeugt das Gegensignal /OUT.

Die beiden Offsets Δ1 und Δ2 entstehen durch **zustandsabhängige Stromeinspeisung**
in die Messknoten: Poti RV1 speist von OUT in Knoten A, Poti RV2 speist von /OUT in
Knoten B. Es ist immer genau eine der beiden Einspeisungen aktiv (high):

```
                      VCC                           VCC
                        │                             │
                      [R7 3,3k]                     [R8 3,3k]
                        │                             │
 Knoten A o────┬────────┼────► OUT                    ├────► /OUT
               │      │\│      (high = Akku 1 aktiv)  │
               └──────│+ \                          │\│
                      │    ────┬────────────────────│− \
 Knoten B o───┬───────│− /     │                    │    ──────┬──► /OUT
              │       │/ U1a   │      VCC ──[R9 47k]│+ /       │
              │                │            ├───────│/ U1b     │
              │                │   [R10 47k]│ = VCC/2, C11 100n│
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
RV1 speist Strom von OUT (≈ VCC) in Knoten A → Akku 1 „wirkt“ um Δ1 höher.
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

Das gesamte Umschaltfenster beträgt `Δ1 + Δ2` — nach jedem Umschalten muss sich das
Spannungsverhältnis der Akkus um mindestens dieses Fenster ändern, bevor wieder
geschaltet wird.

> **Wichtig bei 40 A:** Ein 72-V-Akku bricht unter 40 A Last je nach
> Innenwiderstand um 1 … 3 V ein. Damit die Schaltung nach dem Umschalten nicht
> sofort zurückpendelt (der entlastete Akku erholt sich, der neue bricht ein),
> muss `Δ1 + Δ2 > 2 × Lasteinbruch` sein. Deshalb reicht der Einstellbereich
> hier bis ca. 3 V je Richtung (Fenster bis ≈ 7 V).

### Dimensionierung

Einspeisung von OUT (High-Pegel ≈ VCC − 1 V ≈ 10,7 V, Knotenspannung ≈ 2,4 V) über
`Rf = R5 + RV-Anteil` in einen Knoten mit `Rth ≈ 1,93 kΩ`:

```
Δ (eigener Anteil)  ≈ (UOUT,high − UKnoten) · Rth / (Rth + Rf) / α
Δ (fester Zusatz)   ≈  UKnoten · Rth / (Rth + Rf,anderes Poti) / α
Δ1_eff = Δ1(RV1, eigener Anteil) + Zusatz(RV2)      (Δ2 analog mit vertauschten Rollen)
```

| Poti-Stellung | Rf       | eigener Anteil | fester Zusatz fürs **andere** Δ |
|---------------|----------|----------------|----------------------------------|
| 0 Ω           | 150 kΩ   | ≈ 2,9 V        | ≈ 0,84 V                         |
| 250 kΩ        | 400 kΩ   | ≈ 1,1 V        | ≈ 0,32 V                         |
| 500 kΩ        | 650 kΩ   | ≈ 0,69 V       | ≈ 0,20 V                         |
| 1 MΩ          | 1,15 MΩ  | ≈ 0,39 V       | ≈ 0,11 V                         |

**Einstellbereich je Richtung: ca. 0,4 … 2,9 V** (plus fester Zusatz).

Zwei bewusste Eigenschaften dieser einfachen Lösung (für den Einsatzzweck
unkritisch, da beide Potis ohnehin empirisch nachjustiert werden):

1. **Leichte gegenseitige Beeinflussung:** Jedes Poti trägt über den festen Zusatz
   ca. 10–25 % zum jeweils *anderen* Δ bei → beim Einstellen wechselseitig
   nachjustieren. Genau dieser Zusatz liefert die gewünschte feste Extra-Hysterese
   („nochmal ~0,5 V obendrauf“), damit nicht zu oft geschaltet wird.
2. **Δ skaliert schwach mit VCC**, die von der Zenerdiode stabilisiert wird –
   Restabhängigkeit von der Batteriespannung < 5 %.

### Inverter U1b

Der zweite LM393-Komparator vergleicht OUT mit VCC/2 (R9/R10 = 47 kΩ, C11 100 nF)
und liefert /OUT mit sauberem Pegel (Pull-up R8). /OUT steuert die Einspeisung von
Δ2, den Gate-Treiber von Schalter 1 und die LED „Akku 2 aktiv“.

### Verhalten beim Einschalten

Liegen beide Akkuspannungen beim Einschalten innerhalb des Fensters
(|U1 − U2| < Δ), ist der Anfangszustand nicht definiert – die Schaltung wählt
einen Akku und bleibt dort stabil. Das ist unkritisch.

## 4. Gate-Ansteuerung mit Photovoltaik-Treibern

Die N-Kanal-MOSFETs schalten high-side: Ihre Gates müssen ca. 8 … 10 V **über der
72-V-Schiene** liegen (≈ 80 V gegen Masse). Statt einer Hochvolt-Ladungspumpe
kommen **Photovoltaik-MOSFET-Treiber (VOM1271)** zum Einsatz: Eine interne
LED beleuchtet einen Fotodioden-Stapel, der potentialfrei ca. 8,4 V direkt
zwischen Gate und Source liefert – egal, auf welchem Potential die Source liegt.

```
                                  ┌────────────────────┐
V+ ──[R17a 3,3k/1W]──[R17b 3,3k/1W]──|>|── LED         │ OC1 (VOM1271)
                                  │   intern           │
             MPSA42 (300 V!)  C┤──┘        + o─────────┼───o Gate1  (Q1/Q2)
/OUT? nein: OUT-Logik s.u.  B─┤ T1                     │
   OUT o──[R11 27k]───────────┤        − o─────────────┼───o Source-Knoten Q1/Q2
                              │E       (integrierte    │
                             GND        Schnellent-    │
                                        ladung)        │
                                  └────────────────────┘
   (identisch: T2 + R12 27k + R18a/b + OC2 → Gate2/Source-Knoten Q3/Q4,
    T2-Basis an /OUT)
```

- **T1 (Basis an OUT)** schaltet OC1 → Akku-1-Zweig, **T2 (Basis an /OUT)**
  schaltet OC2 → Akku-2-Zweig. Es leuchtet immer nur eine Treiber-LED.
- T1/T2 sind **MPSA42 (300 V)**: Im ausgeschalteten Zustand liegt der Kollektor
  über die LED-Vorwiderstände an V+ (72 V) – ein BC547 (45 V) würde sterben.
- LED-Strom: `(V+ − 1,3 V) / 6,6 kΩ ≈ 9 … 11 mA` über den gesamten
  Batteriespannungsbereich.

### Break-before-make – hier gratis

- **Einschalten langsam:** Der Fotodioden-Stapel liefert nur ~10 µA. Mit der
  Gate-Kapazität der MOSFETs (2× ≈ 10 nF) dauert das Aufladen bis zur
  Schwellspannung **5 … 10 ms** – die Umschaltung ist ein sanfter Soft-Start.
- **Ausschalten schnell:** Der VOM1271 enthält eine aktive
  Schnellentladeschaltung, die das Gate in **< 1 ms** entlädt.

Beim Umschalten (beide LEDs wechseln gleichzeitig) ist der alte Zweig also längst
gesperrt, bevor der neue zu leiten beginnt → **die Akkus werden nie parallel
geschaltet** (wichtig, da sie beim Umschalten konstruktionsbedingt Δ Volt
Differenz haben und sonst hohe Ausgleichsströme flössen).

Während der Totzeit (5 … 10 ms) ist die Last stromlos. Der Stützkondensator C8
überbrückt das nur für kleine Steuerlasten – ein Motorcontroller als Hauptlast
hat aber selbst genug Zwischenkreiskapazität und übersteht die Lücke problemlos.
Da das Umschaltfenster Δ1 + Δ2 groß ist, tritt die Totzeit ohnehin nur selten auf.

## 5. Leistungsschalter

### Antiserielle MOSFET-Paare

Jeder Batteriezweig besteht aus **zwei antiseriellen N-Kanal-MOSFETs**
(Source an Source, Gates verbunden). Nur so sperrt der Schalter in **beide**
Richtungen – mit einem einzelnen MOSFET würde dessen Body-Diode die inaktive
Batterie weiter mit der Last (bzw. mit der anderen Batterie) verbinden.

```
                 Q1 (IRF100P219)    Q2 (IRF100P219)
BAT1+ o──[F1]────D─┤├─S────────S─┤├─D──────────────┬─────o LAST+
                     │►(Body)  ◄│                  │
                     └────┬─────┘                  │
              Gate1 ──────┤   ZD1 15 V             │
              (von OC1)   └──▲├── Source-Knoten    │
                                                   │
                 Q3 (IRF100P219)    Q4 (IRF100P219)│
BAT2+ o──[F2]────D─┤├─S────────S─┤├─D──────────────┘
                     │►        ◄│                 ─┴─ C8  2× 470 µF/100 V
                     └────┬─────┘                 ─┬─  (Stützkondensator)
              Gate2 ──────┤   ZD2 15 V             │
              (von OC2)   └──▲├── Source-Knoten   GND
```

- **MOSFET-Anforderungen:** `UDS ≥ 100 V` (71,4 V max. + Reserve für
  Schaltspitzen), `RDS(on) ≤ 3 mΩ`, gut durchgesteuert bei UGS = 8 V
  (der VOM1271 liefert ca. 8,4 V). Referenztyp IRF100P219 (TO-247, 100 V, ≤ 2 mΩ);
  Alternative IPP023N10N5.
- **Verlustleistung bei 40 A:** `P = 40² · 2 · ≈2,2 mΩ ≈ 7 W` je aktivem Zweig
  (bei UGS 8 V etwas über Datenblattwert) → **dringend empfohlen: je Zweig zwei
  Paare parallel** (8 MOSFETs gesamt, je 10 Ω Einzelgate-Widerstand gegen
  Schwingen) → ≈ 3,5 W je Zweig, ca. 0,9 W pro Gehäuse. Kühlkörper ≤ 6 K/W.
- ZD1/ZD2 (15 V, Gate–Source) schützen die Gates vor eingekoppelten Transienten.
- **Verdrahtungsinduktivität klein halten** (kurze, dicke Leitungen): Beim
  Abschalten unter 40 A erzeugt jede µH Leitungsinduktivität Spannungsspitzen,
  die die 100-V-Reserve aufbrauchen. Bei langen Batterieleitungen je Akku einen
  Elko (220 µF/100 V) direkt an den Schalter-Eingang setzen.

### Status-LEDs

Die LEDs hängen an VCC und werden über eigene Transistoren getrieben, damit sie
die Pegel von OUT//OUT (Einspeisequellen für Δ1/Δ2!) nicht verfälschen:

```
VCC ──[R15 2,2k]──|>|──C┤ T3 (BC547)   Basis ← OUT  via R13 330k
      LED1 grün         │E             „Akku 1 aktiv“
                       GND
VCC ──[R16 2,2k]──|>|──C┤ T4 (BC547)   Basis ← /OUT via R14 330k
      LED2 gelb         │E             „Akku 2 aktiv“
                       GND
```

---

## Grenzen und mögliche Erweiterungen

- **Kein absoluter Tiefentladeschutz:** Die Schaltung vergleicht nur *relativ*.
  Beim Leerfahren wechseln sich die Akkus ab („Leapfrog“) und werden gemeinsam
  entladen – gewollt, um beide Kapazitäten zu nutzen. Die **BMS der beiden Akkus
  bleiben die letzte Instanz** gegen Tiefentladung; bei Akkus ohne BMS einen
  externen Low-Voltage-Disconnect hinter den Ausgang schalten.
- **Kein Laderegler:** Die Schaltung verteilt nur die Entladung. Das Laden beider
  Akkus muss separat erfolgen. Wird ein Akku geladen, während der andere entladen
  ist, schaltet die Last automatisch auf den geladenen Akku – gewolltes Verhalten
  des Differenzvergleichs.
- **Verpolschutz:** Nicht enthalten – bei Verpolung eines Akkus leiten die
  Body-Dioden. Sicherungen F1/F2 begrenzen den Schaden; sorgfältig anschließen.
- **Fehlerfall Messteiler:** Reißt ein unterer Teilerwiderstand (R2/R4) ab, liegt
  der volle Akku an einem LM393-Eingang (max. 36 V) – der Komparator stirbt und
  der Zustand ist undefiniert. Wer es robust mag, ergänzt je Knoten eine
  10-V-Zener nach Masse (identisch an beiden Knoten, um die Symmetrie zu wahren).
