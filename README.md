# BatterySwitch – Automatischer 2-Akku-Umschalter (12 V, 40 A)

Automatische Umschaltung zwischen zwei 12-V-Akkus (Batterie 1: 50 Ah, Batterie 2: 30 Ah)
anhand der Batteriespannung. Die Umschaltung erfolgt verschleißfrei über
Leistungs-MOSFETs (ausgelegt für ca. 40 A Dauerstrom), die **Hysterese ist über ein
Potentiometer einstellbar** (ca. 0,4 V … 2 V).

## Funktionsprinzip

- Batterie 1 (50 Ah) ist die **Primärbatterie** und versorgt die Last, solange ihre
  Spannung über der eingestellten Schwelle liegt.
- Sinkt die Spannung von Batterie 1 unter die untere Schwelle, schaltet die Schaltung
  auf Batterie 2 (30 Ah, Reserve) um.
- Erholt sich Batterie 1 (z. B. durch Ladung) über die obere Schwelle
  (untere Schwelle + Hysterese), wird auf Batterie 1 zurückgeschaltet.
- Die Hysterese verhindert ein Hin- und Herschalten („Flattern“), wenn die
  Batteriespannung unter Last einbricht und sich im Leerlauf wieder erholt.
  Sie wird mit einem Poti stufenlos eingestellt.

```
 BAT1 (50Ah) o──[Sicherung 50A]──┤ MOSFET-Schalter S1 ├──┐
                                                          ├──o LAST +
 BAT2 (30Ah) o──[Sicherung 50A]──┤ MOSFET-Schalter S2 ├──┘
                                                 ▲
                 ┌───────────────────────────────┘
 U(BAT1) ──►  Komparator mit einstellbarer Hysterese (Poti)
              + Break-before-make-Gate-Ansteuerung
```

## Eckdaten

| Parameter                  | Wert                                        |
|----------------------------|---------------------------------------------|
| Systemspannung             | 12 V (Blei, AGM, LiFePO4 4s)                |
| Dauerstrom                 | 40 A (Spitze kurzzeitig höher)              |
| Schaltelemente             | 2× antiserielle N-Kanal-MOSFETs je Zweig (IRLB3034, 1,7 mΩ) |
| Verlustleistung bei 40 A   | ca. 5,5 W je aktivem Zweig → Kühlkörper nötig |
| Schaltschwelle             | einstellbar ca. 7,4 … 14,6 V (Trimmer)      |
| Hysterese                  | einstellbar ca. 0,4 … 2,0 V (Poti)          |
| Eigenverbrauch Steuerung   | < 10 mA                                     |
| Umschaltung                | Break-before-make (Akkus werden nie parallel geschaltet) |

## Dokumentation

| Dokument | Inhalt |
|----------|--------|
| [docs/schaltung.md](docs/schaltung.md) | Vollständige Schaltungsbeschreibung, Schaltbilder, Dimensionierung und Formeln |
| [docs/stueckliste.md](docs/stueckliste.md) | Stückliste (BOM) mit Bauteilwerten und Alternativen |
| [docs/aufbau-und-abgleich.md](docs/aufbau-und-abgleich.md) | Aufbauhinweise, Verkabelung, Inbetriebnahme und Abgleich von Schwelle & Hysterese |

## Sicherheitshinweise

- **Beide Akkus müssen denselben Minuspol (gemeinsame Masse) haben.** Geschaltet wird
  ausschließlich der Pluspfad (High-Side).
- Jeder Akku wird **direkt am Pluspol mit 50 A abgesichert** (MIDI-/MEGA-Sicherung).
- Leitungsquerschnitt für den Lastpfad: mindestens **10 mm²** bei 40 A.
- Während der Umschaltung ist die Last für wenige Millisekunden stromlos
  (Break-before-make). Ein Stützkondensator am Ausgang überbrückt das für
  Elektronik-Lasten; Motoren/Lampen stört die kurze Lücke nicht.
- Die Schaltung überwacht nur Batterie 1. Batterie 2 wird als Reserve ohne eigene
  Tiefentladeüberwachung betrieben – siehe „Grenzen“ in der Schaltungsbeschreibung.
