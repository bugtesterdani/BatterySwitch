# Aufbau und Abgleich

> **Sicherheit zuerst:** 72 V DC ist keine Schutzkleinspannung mehr. Nicht unter
> Spannung arbeiten, isoliertes Werkzeug, Berührungsschutz für alle blanken
> Leistungsanschlüsse. Beim Trennen unter Last entstehen DC-Lichtbögen –
> Verbindungen nur stromlos stecken/schrauben.

## 1. Mechanischer Aufbau

- **Leistungsteil** (Q1–Q4 bzw. Q1–Q8, F1/F2, C8) mit kurzen, dicken Leiterbahnen
  bzw. 10-mm²-Verdrahtung aufbauen. Bei Lochraster: Leistungsstrecke **nicht**
  über Lötaugen führen, sondern massive Drähte/Kupferschienen direkt an die
  MOSFET-Beine löten.
- MOSFETs auf gemeinsamen Kühlkörper montieren. **Achtung:** Die Kühlfahne des
  TO-247 ist Drain – Glimmerscheibe/Silikonpad + Isolierbuchse verwenden. Der
  Kühlkörper führt sonst 72 V bzw. schließt BAT1, BAT2 und Last kurz.
- **Verdrahtungsinduktivität klein halten:** kurze Wege zwischen Sicherung,
  Schalter und Last. Bei langen Batterieleitungen je Akku 220 µF/100 V direkt
  am Schalter-Eingang vorsehen (Abschalt-Spannungsspitzen!).
- Steuerteil: entweder auf Lochraster oder mit dem fertigen **Platinenlayout**
  [hardware/BatterySwitch_Steuerplatine.kicad_pcb](../hardware/BatterySwitch_Steuerplatine.kicad_pcb)
  (112×92 mm, 2 Lagen, Unterseite = GND-Zone — vor der Fertigung in KiCad
  öffnen, mit `B` die Zone füllen und den DRC laufen lassen). Anschluesse über
  Schraubklemmen: X4 = B1F/B2F/GND, X5 = Sense S1/S2, X6 = Gate/Source beider
  MOSFET-Paare, X7 = die beiden Frontplatten-Potis. Verbindungen
  zum Leistungsteil sind nur die zwei Gate/Source-Paare der VOM1271-Ausgänge
  und Masse. Die VOM1271-Ausgangsleitungen kurz halten und verdrillen.
- **Beide Sense-Abgriffe** (über F3/F4 100 mA) **direkt an der Anschlussklemme
  des jeweiligen Akku-Steckers** abnehmen, vor der Hauptsicherung F1/F2 – nicht
  irgendwo weiter hinten im Lastpfad. An die Batteriepole selbst muss (und kann)
  man bei Steckakkus nicht heran: Abfälle hinter dem Abgriff gehen nicht in die
  Messung ein, und der kleine Abfall über Akkukabel/Steckerkontakt (~0,1–0,3 V
  bei 40 A) wirkt nur wie etwas zusätzlicher Lasteinbruch. Damit der Fehler
  symmetrisch bleibt: **beide Akkuzuleitungen gleich ausführen** (Querschnitt,
  Länge, Steckertyp).
- **Gemeinsame Masse = nur im Umschalter-Kabelbaum:** Die Minus-Pins der
  beiden Akku-Stecker (X1, X2) werden im Kabelbaum direkt und niederohmig mit
  dem Fahrzeug-Minus (X3) verbunden. **An den Akkus selbst wird nichts
  geändert** – zieht man einen Akku ab und steckt ihn direkt ans Fahrzeug,
  fährt er wie gewohnt ohne Board. Die Verbindung ist nötig, weil der aktive
  Akku einen Stromrückweg braucht; für den inaktiven Akku ist sie unkritisch
  (Pluspfad beidseitig gesperrt, über Minus fließen nur ~1,3 mA Sense-Strom,
  keine Ausgleichsströme).
- **Betrieb mit nur einem Akku am Board** funktioniert ebenfalls: Der leere
  Steckplatz liest über den Messteiler 0 V, die Schaltung bleibt dauerhaft
  auf dem vorhandenen Akku.
- RV1/RV2 (Frontplatten-Potis) mit kurzen, verdrillten Leitungen anschließen –
  die Knoten sind hochohmig. Beide Messteiler (R1–R4) thermisch benachbart
  platzieren, damit Temperaturdrift gleichsinnig wirkt.

## 2. Erste Inbetriebnahme (Steuerteil, ohne Leistungspfad)

Für die ersten Tests genügt **ein** Akku oder ein Netzteil mit 58 … 72 V
(zur Not zwei 30-V-Labornetzteile in Serie). Strombegrenzung auf 100 mA.
Leistungs-MOSFETs noch nicht mit der Last verbinden.

1. Versorgung an BAT1+, beide Sense-Eingänge zunächst **zusammen** an dieselbe
   Quelle, GND anschließen.
2. **VCC prüfen:** ≈ 12 … 12,5 V. T5 darf nur mäßig warm werden.
3. **Inverter prüfen:** OUT und /OUT müssen komplementär sein
   (eine Status-LED an, eine aus).
4. **Gate-Treiber prüfen:** Am aktiven Zweig ≈ 8 V zwischen Gate und
   Source-Knoten, am inaktiven ≈ 0 V. Beim Umschalten muss das neue Gate
   sichtbar langsam kommen (einige ms, mit Oszi gut zu sehen), das alte
   schnell fallen.

## 3. Nullabgleich (RV3) – einmalig

Der Nullabgleich kompensiert die Toleranzen der Teilerwiderstände, damit
„U1 = U2“ auch wirklich als gleich erkannt wird. Bei der ÷28-Teilung erzeugen
schon 1-%-Widerstände bis ±1 V Scheindifferenz – dieser Schritt ist Pflicht.

**Variante A – mit Multimeter (empfohlen, keine 72-V-Quelle mit Feinregelung nötig):**

1. **JP1 und JP2 öffnen** (Δ-Einspeisungen getrennt).
2. Beide Sense-Eingänge zusammen an einen Akku (oder die Testquelle) klemmen.
3. Mit dem Multimeter Knoten A und Knoten B messen (≈ 2,1 … 2,6 V) und RV3 so
   einstellen, dass **beide Knoten auf < 1 mV gleich** sind (1 mV am Knoten
   ≈ 30 mV auf Batterieebene).
4. **JP1 und JP2 wieder schließen.**

**Variante B – über den Kipppunkt:** Wie A, aber mit fein einstellbarer Quelle:
RV3 auf die Mitte des Bereichs stellen, in dem die LEDs wechseln/flackern
(ohne Hysterese ist Flackern am Kipppunkt normal).

## 4. Einstellen von Δ1 und Δ2 (RV1/RV2)

Volle Präzision braucht zwei unabhängige 58…72-V-Quellen – die hat kaum jemand.
Praktikabel sind zwei Wege:

**Variante A – rechnerisch über die Knotenspannung (Multimeter genügt):**

1. Beide Sense-Eingänge zusammen an eine Quelle/einen Akku, Zustand
   „Akku 1 aktiv“ (LED1 an; ggf. durch kurzes Öffnen von JP2 erzwingen).
2. Knoten A messen, dann **JP1 öffnen** und erneut messen. Die Differenz ΔU(A),
   geteilt durch α = 0,0357, ist das aktuell eingestellte Δ1:
   `Δ1 ≈ ΔU(A) / 0,0357` (z. B. 36 mV Differenz ≙ 1,0 V). RV1 entsprechend
   einstellen, JP1 schließen. Für Δ2 analog mit JP2/Knoten B im Zustand
   „Akku 2 aktiv“.
3. Als Startwert taugt auch die Tabelle in der
   [Schaltungsbeschreibung](schaltung.md) (Poti-Stellung → Δ).

**Variante B – im Betrieb mit beiden Akkus:** Beide Akkus mit unterschiedlichem
Ladezustand anschließen, Last zuschalten und die Umschaltpunkte über die
Akkuspannungen (BMS-App/Voltmeter) beobachten; Potis nachführen.

**Wahl der Werte:**

- Δ1 **größer als der Lasteinbruch** des Akkus bei Volllast wählen. Bei 40 A an
  einem 72-V-Paket sind je nach Innenwiderstand 1 … 3 V Einbruch realistisch –
  im Zweifel Δ1 ≈ 1,5 … 2 V als Start.
- Δ2 etwa 0,3 … 0,5 V größer als Δ1, wenn selten zurückgeschaltet werden soll.
- **Wechselwirkung beachten:** Jedes Poti verschiebt das andere Δ um ca. 10–25 %
  (feste Zusatzhysterese). Beide Einstellungen 1–2× im Wechsel wiederholen.
- Pendelt die Schaltung unter Volllast (schnelles Hin- und Herschalten): beide
  Δ vergrößern, bis `Δ1 + Δ2 > 2 × Lasteinbruch`.

## 5. Test unter Last

1. Beide Akkus über die Sicherungen anschließen, zunächst **kleine Last**
   (z. B. Lampe/Widerstand, wenige A).
2. Umschalten provozieren: den aktiven Akku zusätzlich belasten (Spannung sackt
   ab) und beobachten, ob sauber auf den anderen Akku gewechselt wird – und erst
   nach deutlicher Erholung (Δ2) zurück.
3. Danach schrittweise bis zur Volllast (40 A) steigern und die
   **MOSFET-Temperatur überwachen**: Nach 30 min Dauerlast sollte der Kühlkörper
   handwarm bis warm (< 60 °C) sein. Wird er heißer: Kühlkörper vergrößern oder
   (falls noch nicht geschehen) zweites MOSFET-Paar je Zweig parallel bestücken.
4. Spannungsabfall über dem aktiven Schalter messen: bei 40 A und einem Paar
   ≈ 0,2 V, bei zwei parallelen Paaren ≈ 0,1 V. Deutlich mehr deutet auf
   schlechte Gate-Ansteuerung (VOM1271-LED-Strom prüfen: ~10 mA) oder
   Übergangswiderstände an den Klemmen hin.

## 6. Typische Probleme

| Symptom | Ursache | Abhilfe |
|---------|---------|---------|
| Schaltet häufig hin und her | Δ1+Δ2 kleiner als 2× Lasteinbruch (inkl. Kabel/Stecker-Abfall); oder Sense-Abgriff hinter F1/F2 statt an der Steckerklemme | Potis Richtung mehr Δ; Sense-Abgriff direkt an die Anschlussklemme legen |
| Umschaltpunkte stimmen nicht / unsymmetrisch | Nullabgleich fehlt oder verstellt | Abschnitt 3 wiederholen |
| Δ ändert sich beim Drehen am anderen Poti | prinzipbedingt (feste Zusatzhysterese, 10–25 %) | wechselseitig nachjustieren |
| MOSFETs werden sofort heiß | UGS zu klein → nicht voll durchgesteuert | Gate-Source ≈ 8 V? VOM1271-LED-Strom ≈ 10 mA? T1/T2 schalten durch? |
| Keine Funktion, VCC = 0 | Zener/Regler-Pfad | ZD3-Spannung (13 V) und R19a/b prüfen |
| Beide LEDs glimmen / undefiniert | Störungen an den Messknoten, Masseschleife | C3/C4 bestückt? Steuerungs-Masse sternförmig anbinden |
| Last fällt beim Umschalten 5–10 ms aus | prinzipbedingt (Break-before-make) | unkritisch für Motorcontroller (eigene Zwischenkreis-Elkos); sonst C8 vergrößern |
| Beide Akkus tiefentladen | prinzipbedingt: nur Relativvergleich | BMS der Akkus ist letzte Instanz; ggf. externen Low-Voltage-Disconnect ergänzen |
