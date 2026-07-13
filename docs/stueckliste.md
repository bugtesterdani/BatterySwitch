# Stückliste (BOM)

Bezeichner entsprechen der [Schaltungsbeschreibung](schaltung.md).

## Halbleiter

| Bezeichner | Bauteil | Wert / Typ | Anmerkung |
|------------|---------|------------|-----------|
| Q1–Q4 | N-Kanal-MOSFET | **IRLB3034PBF** (TO-220, 40 V, 1,7 mΩ, Logic-Level) | Alternativen: IRF100P219, IRLB4132. Wichtig: RDS(on) ≤ 3 mΩ, UDS ≥ 30 V, Logic-Level (voll leitend bei UGS = 4,5 V) |
| U1 | Komparator | **LM393** (DIP-8) | Dual, Open-Collector, bis 36 V; zweite Hälfte frei für Erweiterung |
| U2 | Referenz | **TL431** (TO-92) | 2,495 V Shunt-Referenz |
| U3 | Timer | **NE555** (DIP-8) | Ladungspumpen-Oszillator |
| T1–T3 | NPN-Transistor | **BC547B** (TO-92) | beliebiger Kleinsignal-NPN (BC337, 2N3904 …) |
| D1, D2 | Schottky-Diode | **1N5819** (1 A / 40 V) | Dioden-OR der Versorgung |
| D3, D4 | Diode | **1N4148** | Ladungspumpe |
| ZD1, ZD2 | Zener-Diode | **BZX55C15** (15 V, 0,5 W) | Gate-Schutz |
| LED1 | LED grün, 3 mm | – | „Batterie 1 aktiv“ |
| LED2 | LED gelb, 3 mm | – | „Batterie 2 aktiv“ |

## Widerstände (alle 0,25 W, 1 % empfohlen für R1/R2)

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| R1 | 33 kΩ | Messteiler oben |
| R2 | 6,8 kΩ | Messteiler unten (fester Anteil) |
| R3 | 220 kΩ | Serienwiderstand zum Hysterese-Poti (begrenzt max. Hysterese auf ≈ 2 V) |
| R4 | 10 kΩ | Pull-up Komparatorausgang |
| R5 | 4,7 kΩ | Vorwiderstand TL431 |
| R6, R7 | 4,7 kΩ | NE555-Astabil |
| R8, R12, R13 | 47 kΩ | Basiswiderstände T1–T3 |
| R9 | 47 kΩ | Pull-up /OUT (Kollektor T3) |
| R10, R11 | 100 kΩ | Gate-Pull-ups nach VCP (bestimmen Einschaltverzögerung) |
| R14, R15 | 2,2 kΩ | LED-Vorwiderstände |

## Potentiometer

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| RV1 | 10 kΩ Trimmer (25 Gang empfohlen) | **Schaltschwelle** (7,4 … 14,6 V) |
| RV2 | 1 MΩ Poti, linear (Frontplatte) | **Hysterese** (0,4 … 2,0 V) |

## Kondensatoren

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| C1 | 100 µF / 25 V Elko | Versorgungspuffer Steuerung |
| C2 | 100 nF Keramik | Abblockung LM393/NE555 (je IC eines vorsehen) |
| C3 | 100 nF Keramik | Filter am Messeingang (Knoten A) |
| C5 | 1 nF Keramik | NE555-Frequenz |
| C6 | 100 nF Keramik | Pumpkondensator Ladungspumpe |
| C7 | 10 µF / 35 V Elko | VCP-Reservoir |
| C8 | 4700 µF / 25 V Low-ESR-Elko | Stützkondensator Lastausgang (überbrückt Umschalt-Totzeit) |
| C9, C10 | 10 nF Keramik | Einschaltverzögerung Gates (Break-before-make) |

## Mechanik / Leistungsteil

| Bezeichner | Bauteil | Anmerkung |
|------------|---------|-----------|
| F1, F2 | MIDI-Sicherung 50 A + Halter | direkt am Pluspol des jeweiligen Akkus |
| KK1 | Kühlkörper ≤ 6 K/W | für Q1–Q4 gemeinsam; MOSFETs elektrisch isoliert montieren (Drain = Kühlfahne!) oder isolierter Kühlkörper |
| – | Leitung 10 mm² | gesamter Lastpfad (BAT+ → Schalter → Last, sowie Masseverbund) |
| – | M8/M6-Ringkabelschuhe, Schraubklemmen ≥ 40 A | Leistungsanschlüsse |

## Hinweise zur Beschaffung

- Die vier MOSFETs sind die einzigen „kritischen“ Bauteile. Bei 40 A Dauerstrom
  lieber ein moderneres/niederohmigeres Modell wählen als sparen — jedes mΩ sind
  1,6 W Abwärme.
- Für geringere Verluste je Zweig **zwei Paare parallel** bestücken (dann 8 MOSFETs,
  Gate-Widerstände 10 Ω je Einzelgate gegen Schwingen vorsehen).
