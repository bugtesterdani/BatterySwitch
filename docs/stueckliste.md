# Stückliste (BOM)

Bezeichner entsprechen der [Schaltungsbeschreibung](schaltung.md).
Auslegung für **58 … 72 V Systemspannung, 40 A Dauerstrom**.

## Halbleiter

| Bezeichner | Bauteil | Wert / Typ | Anmerkung |
|------------|---------|------------|-----------|
| Q1–Q4 | N-Kanal-MOSFET | **IRF100P219** (TO-247, 100 V, ≤ 2 mΩ) | Alternative: IPP023N10N5. Anforderung: UDS ≥ 100 V, RDS(on) ≤ 3 mΩ, gut leitend bei UGS = 8 V. **Empfehlung: 8 Stück** (je Zweig zwei Paare parallel, halbiert die Verluste) |
| OC1, OC2 | Photovoltaik-Gate-Treiber | **VOM1271T** (SOP-4) | liefert potentialfrei ≈ 8,4 V Gate-Spannung, integrierte Schnellentladung. Alternativen: APV1122, TLP3906 (ohne Schnellentladung → externe Entladeschaltung nötig) |
| U1 | Komparator | **LM393** (DIP-8) | beide Hälften belegt: U1a Differenzkomparator, U1b Inverter; läuft an VCC = 12 V |
| T1, T2 | NPN-Transistor | **MPSA42** (TO-92, 300 V) | schalten die Treiber-LEDs; Kollektor liegt sperrend an V+ ≈ 72 V → kein BC547! |
| T3, T4 | NPN-Transistor | **BC547B** (TO-92) | LED-Treiber Status-LEDs (nur an VCC) |
| T5 | NPN-Transistor | **MJE340** (TO-126, 300 V) | Längsregler VCC; kleiner Aufsteckkühlkörper |
| D1, D2 | Schottky-Diode | **1N5819** (1 A / 40 V) | Dioden-OR der Versorgung (sehen max. ±14 V Differenz) |
| ZD1, ZD2 | Zener-Diode | **BZX55C15** (15 V, 0,5 W) | Gate-Schutz, direkt Gate–Source-Knoten |
| ZD3 | Zener-Diode | **BZX85C13** (13 V, 1,3 W) | Referenz des VCC-Reglers |
| LED1 | LED grün, 3 mm | – | „Akku 1 aktiv“ |
| LED2 | LED gelb, 3 mm | – | „Akku 2 aktiv“ |

## Widerstände (0,25 W Metallfilm, sofern nicht anders angegeben; R1–R4 unbedingt 1 %, besser 0,1 %)

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| R1a, R1b | 27 kΩ, 1 % | Messteiler Akku 1, oben (2 in Serie wegen Spannung/Verlustleistung) |
| R2 | 2,0 kΩ, 1 % | Messteiler Akku 1, unten |
| R3a, R3b | 27 kΩ, 1 % | Messteiler Akku 2, oben |
| R4 | 1,8 kΩ, 1 % | Messteiler Akku 2, unten (fester Anteil, Rest über RV3) |
| R5, R6 | 150 kΩ | Serienwiderstände zu RV1/RV2 (begrenzen max. Δ auf ≈ 2,9 V) |
| R7, R8 | 3,3 kΩ | Pull-ups OUT und /OUT |
| R9, R10 | 47 kΩ | VCC/2-Teiler für Inverter U1b |
| R11, R12 | 27 kΩ | Basiswiderstände T1/T2 (MPSA42 braucht kräftige Basisansteuerung) |
| R13, R14 | 330 kΩ | Basiswiderstände T3/T4 (Status-LEDs) |
| R15, R16 | 2,2 kΩ | Vorwiderstände Status-LEDs |
| R17a, R17b | 3,3 kΩ, **1 W** (Metalloxid) | Vorwiderstand Treiber-LED OC1 (2 in Serie, von V+ ≈ 72 V) |
| R18a, R18b | 3,3 kΩ, **1 W** (Metalloxid) | Vorwiderstand Treiber-LED OC2 |
| R19a, R19b | 5,6 kΩ, 0,5 W | Zener-Vorwiderstand VCC-Regler (2 in Serie) |
| Rg (8×) | 10 Ω | Einzelgate-Widerstände, nur bei parallelen MOSFET-Paaren |

## Potentiometer / Trimmer

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| RV1 | 1 MΩ Poti, linear (Frontplatte) | **Δ1**: Umschalten auf Akku 2 bei U1 < U2 − Δ1 (≈ 0,4 … 2,9 V) |
| RV2 | 1 MΩ Poti, linear (Frontplatte) | **Δ2**: Zurückschalten auf Akku 1 bei U2 < U1 − Δ2 (≈ 0,4 … 2,9 V) |
| RV3 | 500 Ω Trimmer, 25 Gang | **Nullabgleich** der beiden Messteiler |

## Kondensatoren

| Bezeichner | Wert | Funktion |
|------------|------|----------|
| C1 | 100 µF / 25 V Elko | Puffer VCC |
| C2 | 100 nF Keramik | Abblockung LM393 (direkt am IC) |
| C3, C4 | 100 nF Keramik | Filter an den Messknoten A und B (nicht > 470 nF!) |
| C8 | 2× 470 µF / **100 V** Low-ESR-Elko | Stützkondensator Lastausgang |
| C11 | 100 nF Keramik | Stützung VCC/2-Teiler |
| C12 | 100 nF / **100 V** Keramik/Folie | Abblockung V+ |
| (optional) | 220 µF / 100 V je Akku-Eingang | bei langen Batterieleitungen gegen Abschalt-Spannungsspitzen |

## Sonstiges

| Bezeichner | Bauteil | Anmerkung |
|------------|---------|-----------|
| X1, X2 | Super-Soco-Gegenstecker (Akku-Seite), 2× | Anschluss der beiden Akkus an den Umschalter |
| X3 | Super-Soco-Batteriestecker (Fahrzeug-Seite), 1× | Ausgang des Umschalters zum Fahrzeug/Controller. **Strombelastbarkeit der Stecker für 40 A Dauer prüfen** – Kontakte ggf. verlöten statt crimpen |
| JP1, JP2 | Jumper / Stiftleiste 2-polig | trennen die Δ-Einspeisungen für den Nullabgleich |
| F1, F2 | Sicherung 50 A, **≥ 80 V DC** | z. B. gPV 14×51 mm oder NH00 mit Halter. **Kfz-Sicherungen (MIDI/MEGA/ANL) sind nur bis 32 V zugelassen – ungeeignet!** So nah wie möglich an der Anschlussklemme des jeweiligen Akku-Steckers |
| F3, F4 | Feinsicherung 100 mA flink + Halter | in den beiden Sense-Leitungen, direkt an der Anschlussklemme des Akku-Steckers |
| KK1 | Kühlkörper ≤ 6 K/W | für die MOSFETs gemeinsam; elektrisch isoliert montieren (Drain = Kühlfahne!) |
| KK2 | Aufsteckkühlkörper TO-126 | für T5 (MJE340) |
| – | Leitung 10 mm² | gesamter Lastpfad (BAT+ → Schalter → Last, sowie Masseverbund) |
| – | Leitung 0,5 mm², 2× | Sense-Leitungen von den Anschlussklemmen der Akku-Stecker (vor F1/F2) zur Steuerplatine |
| – | M8/M6-Ringkabelschuhe, Schraubklemmen ≥ 40 A | Leistungsanschlüsse |

## Hinweise zur Beschaffung

- Die MOSFETs sind die einzigen „kritischen“ Bauteile. Bei 40 A Dauerstrom
  lieber ein moderneres/niederohmigeres Modell wählen als sparen — jedes mΩ sind
  1,6 W Abwärme. 100-V-Typen unter 2,5 mΩ sind gut verfügbar (TO-220/TO-247).
- VOM1271 gibt es nur in SMD (SOP-4) – auf eine kleine Adapterplatine löten,
  wenn auf Lochraster gebaut wird.
- RV1/RV2 als lineare Potis wählen (kein log!), sonst ist die Δ-Skala stark verzerrt.
- Alle Bauteile im Pfad V+ (R17/R18/R19, C12, T1/T2-Kollektoren, T5) sehen bis zu
  72 V — Spannungsfestigkeit beim Ersatztypen-Kauf beachten.
