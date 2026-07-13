# Stückliste (BOM)

Bezeichner entsprechen der [Schaltungsbeschreibung](schaltung.md).

## Halbleiter

| Bezeichner | Bauteil | Wert / Typ | Anmerkung |
|------------|---------|------------|-----------|
| Q1–Q4 | N-Kanal-MOSFET | **IRLB3034PBF** (TO-220, 40 V, 1,7 mΩ, Logic-Level) | Alternativen: IRF100P219, IRLB4132. Wichtig: RDS(on) ≤ 3 mΩ, UDS ≥ 30 V, Logic-Level (voll leitend bei UGS = 4,5 V) |
| U1 | Komparator | **LM393** (DIP-8) | beide Hälften belegt: U1a Differenzkomparator, U1b Inverter |
| U3 | Timer | **NE555** (DIP-8) | Ladungspumpen-Oszillator |
| T1–T4 | NPN-Transistor | **BC547B** (TO-92) | T1/T2 Gate-Ansteuerung, T3/T4 LED-Treiber; beliebiger Kleinsignal-NPN (BC337, 2N3904 …) |
| D1, D2 | Schottky-Diode | **1N5819** (1 A / 40 V) | Dioden-OR der Versorgung |
| D3, D4 | Diode | **1N4148** | Ladungspumpe |
| ZD1, ZD2 | Zener-Diode | **BZX55C15** (15 V, 0,5 W) | Gate-Schutz |
| LED1 | LED grün, 3 mm | – | „Akku 1 aktiv“ |
| LED2 | LED gelb, 3 mm | – | „Akku 2 aktiv“ |

## Widerstände (alle 0,25 W; R1–R4 unbedingt 1 % Metallfilm)

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| R1 | 33 kΩ, 1 % | Messteiler Akku 1, oben |
| R2 | 8,2 kΩ, 1 % | Messteiler Akku 1, unten |
| R3 | 33 kΩ, 1 % | Messteiler Akku 2, oben |
| R4 | 7,5 kΩ, 1 % | Messteiler Akku 2, unten (fester Anteil, Rest über RV3) |
| R5, R6 | 150 kΩ | Serienwiderstände zu RV1/RV2 (begrenzen max. Δ auf ≈ 2,3 V) |
| R7, R8 | 4,7 kΩ | Pull-ups OUT und /OUT |
| R9, R10 | 47 kΩ | V+/2-Teiler für Inverter U1b |
| R11, R12 | 470 kΩ | Basiswiderstände T1/T2 (hochohmig, um OUT//OUT nicht zu belasten) |
| R13, R14 | 330 kΩ | Basiswiderstände T3/T4 (LED-Treiber) |
| R15, R16 | 2,2 kΩ | LED-Vorwiderstände |
| R17, R18 | 100 kΩ | Gate-Pull-ups nach VCP (bestimmen Einschaltverzögerung) |
| R19, R20 | 4,7 kΩ | NE555-Astabil |

## Potentiometer / Trimmer

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| RV1 | 1 MΩ Poti, linear (Frontplatte) | **Δ1**: Umschalten auf Akku 2 bei U1 < U2 − Δ1 (≈ 0,3 … 2,3 V) |
| RV2 | 1 MΩ Poti, linear (Frontplatte) | **Δ2**: Zurückschalten auf Akku 1 bei U2 < U1 − Δ2 (≈ 0,3 … 2,3 V) |
| RV3 | 1 kΩ Trimmer, 25 Gang | **Nullabgleich** der beiden Messteiler |

## Kondensatoren

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| C1 | 100 µF / 25 V Elko | Versorgungspuffer Steuerung |
| C2 | 100 nF Keramik | Abblockung LM393/NE555 (je IC eines vorsehen) |
| C3, C4 | 100 nF Keramik | Filter an den Messknoten A und B (nicht > 470 nF!) |
| C5 | 1 nF Keramik | NE555-Frequenz |
| C6 | 100 nF Keramik | Pumpkondensator Ladungspumpe |
| C7 | 10 µF / 35 V Elko | VCP-Reservoir |
| C8 | 4700 µF / 25 V Low-ESR-Elko | Stützkondensator Lastausgang (überbrückt Umschalt-Totzeit) |
| C9, C10 | 10 nF Keramik | Einschaltverzögerung Gates (Break-before-make) |
| C11 | 100 nF Keramik | Stützung V+/2-Teiler |

## Sonstiges

| Bezeichner | Bauteil | Anmerkung |
|------------|---------|-----------|
| JP1, JP2 | Jumper / Stiftleiste 2-polig | trennen die Δ-Einspeisungen für den Nullabgleich |
| F1, F2 | MIDI-Sicherung 50 A + Halter | direkt am Pluspol des jeweiligen Akkus |
| KK1 | Kühlkörper ≤ 6 K/W | für Q1–Q4 gemeinsam; MOSFETs elektrisch isoliert montieren (Drain = Kühlfahne!) oder isolierter Kühlkörper |
| – | Leitung 10 mm² | gesamter Lastpfad (BAT+ → Schalter → Last, sowie Masseverbund) |
| – | Leitung 0,5 mm², 2× | Sense-Leitungen direkt an die Pluspole beider Akkus |
| – | M8/M6-Ringkabelschuhe, Schraubklemmen ≥ 40 A | Leistungsanschlüsse |

## Hinweise zur Beschaffung

- Die vier MOSFETs sind die einzigen „kritischen“ Bauteile. Bei 40 A Dauerstrom
  lieber ein moderneres/niederohmigeres Modell wählen als sparen — jedes mΩ sind
  1,6 W Abwärme.
- Für geringere Verluste je Zweig **zwei Paare parallel** bestücken (dann 8 MOSFETs,
  Gate-Widerstände 10 Ω je Einzelgate gegen Schwingen vorsehen).
- RV1/RV2 als lineare Potis wählen (kein log!), sonst ist die Δ-Skala stark verzerrt.
