# BatterySwitch – Automatischer 2-Akku-Umschalter (58–72 V, 40 A)

Automatische Umschaltung zwischen zwei Akkus (Batterie 1: 50 Ah, Batterie 2: 30 Ah)
in einem **72-V-System** (ca. 71,x V Ladeschluss, ca. 58 V Entladeschluss — z. B.
17s-Li-Ion oder 20s-LiFePO4) durch **direkten Vergleich der beiden Akkuspannungen**
(differentiell, keine feste Umschaltschwelle). Die Umschaltung erfolgt verschleißfrei
über Leistungs-MOSFETs (ausgelegt für ca. 40 A Dauerstrom). Beide Umschalt-Offsets
sind **über je ein Potentiometer getrennt einstellbar**.

## Funktionsprinzip

- Zustand **„Akku 1 aktiv“**: Auf Akku 2 wird umgeschaltet, sobald
  `U(Akku 1) < U(Akku 2) − Δ1` — Δ1 einstellbar mit Poti 1 (ca. 0,4 … 2,9 V).
- Zustand **„Akku 2 aktiv“**: Zurückgeschaltet wird, sobald
  `U(Akku 2) < U(Akku 1) − Δ2` — Δ2 einstellbar mit Poti 2 (unabhängig nachjustierbar).
- Zusätzlich wirkt eine **feste Zusatzhysterese** (ca. 0,1 … 0,8 V je Richtung,
  abhängig von den Poti-Stellungen). Das gesamte Umschaltfenster beträgt damit
  `Δ1 + Δ2` (typisch 2 … 4 V) — die Schaltung schaltet selten, und der
  Stützkondensator am Ausgang wird durch Umschalt-Totzeiten kaum belastet.
- Beim Leerfahren wechseln sich die Akkus automatisch ab und werden gemeinsam
  entladen; wird einer der Akkus geladen, übernimmt er automatisch die Last.

```
 BAT1 (50Ah, 72V) o──[Sicherung 50A/80VDC]──┤ MOSFET-Schalter S1 ├──┐
      │ Sense                                                        ├──o LAST +
 BAT2 (30Ah, 72V) o──[Sicherung 50A/80VDC]──┤ MOSFET-Schalter S2 ├──┘
      │ Sense                                          ▲
      ▼                                                │
  Differenzkomparator (U1 ⇄ U2) ───────────────────────┘
  Δ1-Poti · Δ2-Poti · Photovoltaik-Gate-Treiber · Break-before-make
```

## Eckdaten

| Parameter                  | Wert                                        |
|----------------------------|---------------------------------------------|
| Systemspannung             | 58 … 72 V DC                                |
| Dauerstrom                 | 40 A (Spitze kurzzeitig höher)              |
| Schaltelemente             | antiserielle N-Kanal-MOSFETs je Zweig (IRF100P219, 100 V, 2,4 mΩ) |
| Verlustleistung bei 40 A   | ca. 8,5 W je Zweig (1 Paar) bzw. 4,3 W (2 Paare parallel, empfohlen) → Kühlkörper |
| Gate-Ansteuerung           | Photovoltaik-Treiber VOM1271 (potentialfrei, inhärent break-before-make) |
| Umschaltkriterium          | Differenz U1 − U2 (kein fester Spannungswert) |
| Δ1 (auf Akku 2 schalten)   | Poti 1, ca. 0,4 … 2,9 V                     |
| Δ2 (auf Akku 1 zurück)     | Poti 2, ca. 0,4 … 2,9 V                     |
| Zusatzhysterese (fest)     | ca. 0,1 … 0,8 V je Richtung                 |
| Umschalt-Totzeit           | 5 … 10 ms (Akkus werden nie parallel geschaltet) |
| Eigenverbrauch Steuerung   | ca. 25 mA (≈ 1,8 W, ≈ 0,6 Ah/Tag)           |

## Dokumentation

| Dokument | Inhalt |
|----------|--------|
| [hardware/BatterySwitch.kicad_sch](hardware/BatterySwitch.kicad_sch) | **KiCad-Schaltplan** (KiCad 6/7/8/9, direkt zu öffnen) — Vorschau: [hardware/preview.svg](hardware/preview.svg) |
| [docs/schaltung.md](docs/schaltung.md) | Vollständige Schaltungsbeschreibung, Schaltbilder, Dimensionierung und Formeln |
| [docs/stueckliste.md](docs/stueckliste.md) | Stückliste (BOM) mit Bauteilwerten und Alternativen |
| [docs/aufbau-und-abgleich.md](docs/aufbau-und-abgleich.md) | Aufbauhinweise, Verkabelung, Nullabgleich und Einstellen von Δ1/Δ2 |

## Sicherheitshinweise

- **72 V DC ist keine Schutzkleinspannung.** Berührungsschutz vorsehen, nicht
  unter Spannung arbeiten, DC-Lichtbögen beim Trennen unter Last beachten.
- **Beide Akkus müssen denselben Minuspol (gemeinsame Masse) haben.** Geschaltet
  wird ausschließlich der Pluspfad (High-Side).
- Jeder Akku-Anschluss wird **direkt an der Anschlussklemme mit 50 A abgesichert** — Sicherungen mit
  **≥ 80 V DC-Zulassung** (z. B. gPV 14×51). Kfz-Sicherungen (MIDI/MEGA/ANL,
  32 V) sind ungeeignet. Die Sense-Leitungen separat mit 100 mA absichern.
- Leitungsquerschnitt für den Lastpfad: mindestens **10 mm²** bei 40 A. Die beiden
  Sense-Abgriffe direkt an den Anschlussklemmen der Akku-Stecker (vor F1/F2),
  jeweils mit 100 mA abgesichert; beide Akkuzuleitungen gleich ausführen.
- Während der Umschaltung ist die Last für 5 … 10 ms stromlos
  (Break-before-make). Motorcontroller mit eigenem Zwischenkreis stört das nicht.
- Die Schaltung vergleicht nur **relativ** — es gibt keinen absoluten
  Tiefentladeschutz. Die BMS der Akkus bleiben die letzte Schutzinstanz
  (siehe „Grenzen“ in der Schaltungsbeschreibung).
