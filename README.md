# BatterySwitch – Automatischer 2-Akku-Umschalter (12 V, 40 A)

Automatische Umschaltung zwischen zwei 12-V-Akkus (Batterie 1: 50 Ah, Batterie 2: 30 Ah)
durch **direkten Vergleich der beiden Akkuspannungen** (differentiell, keine feste
Umschaltschwelle). Die Umschaltung erfolgt verschleißfrei über Leistungs-MOSFETs
(ausgelegt für ca. 40 A Dauerstrom). Beide Umschalt-Offsets sind **über je ein
Potentiometer getrennt einstellbar**.

## Funktionsprinzip

- Zustand **„Akku 1 aktiv“**: Auf Akku 2 wird umgeschaltet, sobald
  `U(Akku 1) < U(Akku 2) − Δ1` — Δ1 einstellbar mit Poti 1 (ca. 0,3 … 2,3 V).
- Zustand **„Akku 2 aktiv“**: Zurückgeschaltet wird, sobald
  `U(Akku 2) < U(Akku 1) − Δ2` — Δ2 einstellbar mit Poti 2 (unabhängig nachjustierbar).
- Zusätzlich wirkt eine **feste Zusatzhysterese** (ca. 0,1 … 0,5 V je Richtung,
  abhängig von den Poti-Stellungen). Das gesamte Umschaltfenster beträgt damit
  `Δ1 + Δ2` (minimal ≈ 0,65 V, typisch 1,5 … 2 V) — die Schaltung schaltet selten,
  und der Stützkondensator am Ausgang wird durch Umschalt-Totzeiten kaum belastet.
- Beim Leerfahren wechseln sich die Akkus automatisch ab und werden gemeinsam
  entladen; wird einer der Akkus geladen, übernimmt er automatisch die Last.

```
 BAT1 (50Ah) o──[Sicherung 50A]──┤ MOSFET-Schalter S1 ├──┐
      │ Sense                                             ├──o LAST +
 BAT2 (30Ah) o──[Sicherung 50A]──┤ MOSFET-Schalter S2 ├──┘
      │ Sense                                    ▲
      ▼                                          │
  Differenzkomparator (U1 ⇄ U2) ─────────────────┘
  Δ1-Poti · Δ2-Poti · Break-before-make-Gate-Ansteuerung
```

## Eckdaten

| Parameter                  | Wert                                        |
|----------------------------|---------------------------------------------|
| Systemspannung             | 12 V (Blei, AGM, LiFePO4 4s)                |
| Dauerstrom                 | 40 A (Spitze kurzzeitig höher)              |
| Schaltelemente             | 2× antiserielle N-Kanal-MOSFETs je Zweig (IRLB3034, 1,7 mΩ) |
| Verlustleistung bei 40 A   | ca. 5,5 W je aktivem Zweig → Kühlkörper nötig |
| Umschaltkriterium          | Differenz U1 − U2 (kein fester Spannungswert) |
| Δ1 (auf Akku 2 schalten)   | Poti 1, ca. 0,3 … 2,3 V                     |
| Δ2 (auf Akku 1 zurück)     | Poti 2, ca. 0,3 … 2,3 V                     |
| Zusatzhysterese (fest)     | ca. 0,1 … 0,5 V je Richtung                 |
| Eigenverbrauch Steuerung   | < 10 mA                                     |
| Umschaltung                | Break-before-make (Akkus werden nie parallel geschaltet) |

## Dokumentation

| Dokument | Inhalt |
|----------|--------|
| [docs/schaltung.md](docs/schaltung.md) | Vollständige Schaltungsbeschreibung, Schaltbilder, Dimensionierung und Formeln |
| [docs/stueckliste.md](docs/stueckliste.md) | Stückliste (BOM) mit Bauteilwerten und Alternativen |
| [docs/aufbau-und-abgleich.md](docs/aufbau-und-abgleich.md) | Aufbauhinweise, Verkabelung, Nullabgleich und Einstellen von Δ1/Δ2 |

## Sicherheitshinweise

- **Beide Akkus müssen denselben Minuspol (gemeinsame Masse) haben.** Geschaltet wird
  ausschließlich der Pluspfad (High-Side).
- Jeder Akku wird **direkt am Pluspol mit 50 A abgesichert** (MIDI-/MEGA-Sicherung).
- Leitungsquerschnitt für den Lastpfad: mindestens **10 mm²** bei 40 A. Die beiden
  Sense-Leitungen separat direkt an die Batteriepole führen.
- Während der Umschaltung ist die Last für wenige Millisekunden stromlos
  (Break-before-make). Ein Stützkondensator am Ausgang überbrückt das für
  Elektronik-Lasten; Motoren/Lampen stört die kurze Lücke nicht.
- Die Schaltung vergleicht nur **relativ** — es gibt keinen absoluten
  Tiefentladeschutz. Für empfindliche Akkus einen Low-Voltage-Disconnect hinter
  den Ausgang schalten (siehe „Grenzen“ in der Schaltungsbeschreibung).
