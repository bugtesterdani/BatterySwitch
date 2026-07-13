# Aufbau und Abgleich

## 1. Mechanischer Aufbau

- **Leistungsteil** (Q1–Q4, F1/F2, C8) mit kurzen, dicken Leiterbahnen bzw.
  10-mm²-Verdrahtung aufbauen. Bei Lochraster: Leistungsstrecke **nicht** über
  Lötaugen führen, sondern massive Drähte/Kupferschienen direkt an die
  MOSFET-Beine löten.
- Q1–Q4 auf gemeinsamen Kühlkörper montieren. **Achtung:** Die Kühlfahne des
  TO-220 ist Drain – Glimmerscheibe/Silikonpad + Isolierbuchse verwenden, sonst
  schließt der Kühlkörper BAT1, BAT2 und Last kurz.
- Steuerteil (LM393, NE555, Transistoren) kann auf normalem Lochraster sitzen;
  Verbindungen zum Leistungsteil sind nur die zwei Gate-Leitungen, die beiden
  Source-Knoten (für ZD1/ZD2) und Masse.
- **Beide Sense-Leitungen** (Messeingänge R1 und R3) separat vom Lastpfad
  **direkt an die Batteriepole** führen. Das ist beim Differenzvergleich doppelt
  wichtig: Spannungsabfälle über Sicherung und Lastkabel des gerade aktiven Akkus
  würden sonst direkt als scheinbare Spannungsdifferenz in den Vergleich eingehen.
- Beide Akku-Minuspole und der Last-Minus werden **direkt und niederohmig**
  verbunden (gemeinsame Masse).
- RV1/RV2 (Frontplatten-Potis) mit kurzen, verdrillten Leitungen anschließen –
  die Knoten sind hochohmig.

## 2. Erste Inbetriebnahme (ohne Akkus, mit Labornetzteil)

1. Nur den Steuerteil versorgen: Labornetzteil (12 V, strombegrenzt auf 100 mA)
   an BAT1+, BAT2+ (beide Sense-Eingänge zusammen) und GND.
2. **Ladungspumpe prüfen:** VCP muss ca. `2 × UVersorgung − 1,5 V` betragen
   (bei 12 V also ≈ 21 V).
3. **Inverter prüfen:** OUT und /OUT müssen immer komplementär sein
   (eine LED an, eine aus).
4. **Gates prüfen:** Beim aktiven Zweig muss das Gate auf VCP-Niveau liegen,
   beim inaktiven auf ≈ 0 V. Das Umschalten der Gates muss sichtbar verzögert
   erfolgen (Oszilloskop: erst fällt das eine Gate, einige ms später steigt das
   andere).

## 3. Nullabgleich (RV3) – einmalig

Der Nullabgleich kompensiert die Toleranzen der Teilerwiderstände, damit
„U1 = U2“ auch wirklich als gleich erkannt wird:

1. **JP1 und JP2 öffnen** (Δ-Einspeisungen getrennt → Komparator ohne Hysterese).
2. Beide Sense-Eingänge (BAT1+ und BAT2+) **zusammen** an das Labornetzteil
   (12,0 V) anschließen.
3. RV3 langsam drehen, bis die Schaltung genau am Kipppunkt steht (LEDs wechseln;
   in der Nähe des Kipppunkts kann die Anzeige wegen fehlender Hysterese flackern –
   das ist hier normal). Auf die Mitte des Flackerbereichs einstellen.
4. **JP1 und JP2 wieder schließen.**

Alternativ per Multimeter: bei gleicher Spannung an beiden Sense-Eingängen und
offenen Jumpern RV3 so einstellen, dass Knoten A und Knoten B exakt gleiche
Spannung führen (≈ 2,4 V).

## 4. Einstellen von Δ1 und Δ2 (RV1/RV2)

Zum Einstellen braucht man **zwei unabhängige Spannungen** – ideal: zweikanaliges
Labornetzteil (sonst: ein Netzteil + ein Akku).

- **Δ1 (RV1) – Umschalten auf Akku 2:** Kanal B (BAT2-Sense) fest auf 12,8 V.
  Kanal A (BAT1-Sense) langsam absenken, bis auf Akku 2 umgeschaltet wird (LED2 an).
  Die Differenz `12,8 V − U(A)` am Umschaltpunkt ist Δ1. Mit RV1 auf Wunschwert
  bringen (typisch 0,8 … 1,2 V).
- **Δ2 (RV2) – Zurückschalten auf Akku 1:** Aus dem Zustand „Akku 2 aktiv“ heraus
  Kanal A wieder anheben, bis zurückgeschaltet wird (LED1 an). Die Differenz
  `U(A) − 12,8 V` am Rückschaltpunkt ist Δ2. Mit RV2 einstellen.
- **Wechselwirkung beachten:** Jedes Poti verschiebt das andere Δ um ca. 10–25 %
  (feste Zusatzhysterese, siehe [Schaltungsbeschreibung](schaltung.md)). Deshalb
  beide Messungen 1–2× im Wechsel wiederholen, bis beide Werte passen.
- Faustregel für die Wahl von Δ1: größer als der Lasteinbruch des aktiven Akkus
  bei Volllast (50-Ah-Blei bei 40 A: gut 1 V). Δ2 etwa 0,3 … 0,5 V größer als Δ1
  wählen, wenn selten zurückgeschaltet werden soll.

## 5. Test unter Last

1. Beide Akkus über die Sicherungen anschließen, zunächst **kleine Last**
   (z. B. 12-V-Lampe, wenige A).
2. Umschalten provozieren: den aktiven Akku zusätzlich belasten (Spannung sackt ab)
   und beobachten, ob sauber auf den anderen Akku gewechselt wird – und erst nach
   deutlicher Erholung (Δ2) zurück.
3. Danach schrittweise bis zur Volllast (40 A) steigern und die
   **MOSFET-Temperatur überwachen**: Nach 30 min Dauerlast sollte der Kühlkörper
   handwarm bis warm (< 60 °C) sein. Wird er heißer: Kühlkörper vergrößern oder
   zweites MOSFET-Paar parallel bestücken.
4. Spannungsabfall über dem aktiven Schalter messen: bei 40 A sollten es
   ≈ 0,14 V sein (2 × 1,7 mΩ). Deutlich mehr deutet auf schlechte
   Gate-Ansteuerung (VCP prüfen!) oder Übergangswiderstände an den Klemmen hin.

## 6. Typische Probleme

| Symptom | Ursache | Abhilfe |
|---------|---------|---------|
| Schaltet häufig hin und her | Δ1/Δ2 kleiner als Lasteinbruch; oder Sense-Leitungen am Lastpfad statt am Pol | Potis Richtung mehr Δ; Sense direkt an die Batteriepole |
| Umschaltpunkte stimmen nicht / unsymmetrisch | Nullabgleich fehlt oder verstellt | Abgleich nach Abschnitt 3 wiederholen |
| Δ ändert sich beim Drehen am anderen Poti | prinzipbedingt (feste Zusatzhysterese, 10–25 %) | wechselseitig nachjustieren |
| MOSFETs werden sofort heiß | UGS zu klein → nicht voll durchgesteuert | VCP messen (muss ≈ UBat + 9 V sein), Ladungspumpe prüfen |
| Beide LEDs glimmen / undefiniert | Störungen an den Messknoten, Masseschleife | C3/C4 bestückt? Steuerungs-Masse sternförmig anbinden |
| Last fällt beim Umschalten kurz aus | prinzipbedingt (Break-before-make) | C8 vergrößern oder empfindliche Verbraucher separat puffern |
| Beide Akkus tiefentladen | prinzipbedingt: nur Relativvergleich, kein Absolut-Schutz | externen Tiefentladeschutz hinter den Ausgang schalten |
