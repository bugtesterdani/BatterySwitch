# Aufbau und Abgleich

## 1. Mechanischer Aufbau

- **Leistungsteil** (Q1–Q4, F1/F2, C8) mit kurzen, dicken Leiterbahnen bzw.
  10-mm²-Verdrahtung aufbauen. Bei Lochraster: Leistungsstrecke **nicht** über
  Lötaugen führen, sondern massive Drähte/Kupferschienen direkt an die
  MOSFET-Beine löten.
- Q1–Q4 auf gemeinsamen Kühlkörper montieren. **Achtung:** Die Kühlfahne des
  TO-220 ist Drain – Glimmerscheibe/Silikonpad + Isolierbuchse verwenden, sonst
  schließt der Kühlkörper BAT1, BAT2 und Last kurz.
- Steuerteil (LM393, TL431, NE555, Transistoren) kann auf normalem Lochraster
  sitzen; Verbindung zum Leistungsteil sind nur die zwei Gate-Leitungen, die
  beiden Source-Knoten (für ZD1/ZD2), Messleitung BAT1 und Masse.
- Die **Messleitung zu BAT1+ separat vom Lastpfad** direkt an den Batteriepol
  führen (Sense-Leitung), sonst verfälscht der Spannungsabfall über Sicherung
  und Kabel die Messung.
- Beide Akku-Minuspole und der Last-Minus werden **direkt und niederohmig**
  verbunden (gemeinsame Masse).

## 2. Erste Inbetriebnahme (ohne Akkus, mit Labornetzteil)

1. Nur den Steuerteil versorgen: Labornetzteil (12 V, strombegrenzt auf 100 mA)
   an BAT1+ und GND.
2. **VREF prüfen:** am TL431 müssen 2,49–2,50 V anliegen.
3. **Ladungspumpe prüfen:** VCP muss ca. `2 × UVersorgung − 1,5 V` betragen
   (bei 12 V also ≈ 21 V).
4. **Komparator prüfen:** Netzteilspannung langsam von 13 V auf 10 V absenken –
   LED1 muss aus- und LED2 angehen; beim Erhöhen umgekehrt, mit deutlichem
   Abstand (Hysterese) zwischen beiden Punkten.
5. **Gates prüfen:** Bei „BAT1 aktiv“ muss Gate1 auf VCP-Niveau liegen und
   Gate2 auf ≈ 0 V; nach dem Umschalten umgekehrt. Das Umschalten der Gates
   muss sichtbar verzögert erfolgen (Oszilloskop: erst fällt das eine Gate,
   einige ms später steigt das andere).

## 3. Abgleich von Schwelle und Hysterese

Der Abgleich erfolgt mit dem Labornetzteil anstelle von Batterie 1.
**Reihenfolge einhalten** – die Hysterese-Einstellung verschiebt auch die
Schaltpunkte leicht:

1. **Hysterese (RV2) zuerst grob wählen.** Faustregel: Hysterese ≥ Spannungseinbruch
   der Batterie unter Volllast. Für einen 50-Ah-Bleiakku bei 40 A sind
   1–1,5 V realistisch; bei LiFePO4 (geringerer Innenwiderstand) reichen 0,5 V.
2. **Untere Schwelle (RV1) einstellen:** Netzteil auf die gewünschte
   Umschaltspannung stellen (z. B. 11,8 V für Blei, 12,0 V für LiFePO4).
   RV1 langsam drehen, bis die Schaltung gerade auf Batterie 2 umschaltet
   (LED2 an).
3. **Obere Schwelle kontrollieren:** Netzteilspannung langsam erhöhen und den
   Rückschaltpunkt notieren (LED1 an). Die Differenz ist die eingestellte
   Hysterese. Bei Bedarf RV2 nachstellen und Schritt 2 wiederholen.
4. Beide Schaltpunkte zweimal anfahren und notieren (z. B. auf der Frontplatte).

### Empfohlene Einstellwerte

| Akkutyp (BAT1)     | Umschalten auf BAT2 bei | Rückschalten auf BAT1 bei | Hysterese |
|--------------------|-------------------------|---------------------------|-----------|
| Blei/AGM 12 V      | 11,8 V                  | 12,8 V                    | 1,0 V     |
| LiFePO4 12,8 V (4s)| 12,4 V                  | 13,1 V                    | 0,7 V     |

## 4. Test unter Last

1. Beide Akkus über die Sicherungen anschließen, zunächst **kleine Last**
   (z. B. 12-V-Lampe, wenige A).
2. Umschalten provozieren: Messleitung von BAT1 kurz über einen Vorwiderstand
   „künstlich“ absenken oder BAT1 mit einer größeren Last belasten.
3. Danach schrittweise bis zur Volllast (40 A) steigern und die
   **MOSFET-Temperatur überwachen**: Nach 30 min Dauerlast sollte der Kühlkörper
   handwarm bis warm (< 60 °C) sein. Wird er heißer: Kühlkörper vergrößern oder
   zweites MOSFET-Paar parallel bestücken.
4. Spannungsabfall über dem aktiven Schalter messen: bei 40 A sollten es
   ≈ 0,14 V sein (2 × 1,7 mΩ). Deutlich mehr deutet auf schlechte
   Gate-Ansteuerung (VCP prüfen!) oder Übergangswiderstände an den Klemmen hin.

## 5. Typische Probleme

| Symptom | Ursache | Abhilfe |
|---------|---------|---------|
| Schaltung „flattert“ beim Umschalten | Hysterese kleiner als Lasteinbruch von BAT1 | RV2 Richtung mehr Hysterese drehen; Sense-Leitung direkt am Batteriepol? |
| MOSFETs werden sofort heiß | UGS zu klein → nicht voll durchgesteuert | VCP messen (muss ≈ UBat + 9 V sein), Ladungspumpe prüfen |
| Beide LEDs glimmen / undefiniert | Masseschleife oder Störungen am Messeingang | C3 bestückt? Steuerungs-Masse sternförmig anbinden |
| Last fällt beim Umschalten kurz aus | prinzipbedingt (Break-before-make) | C8 vergrößern oder empfindliche Verbraucher separat puffern |
| Es wird nie auf BAT1 zurückgeschaltet | obere Schwelle über der Ladeschlussspannung | Hysterese verkleinern oder Schwelle (RV1) absenken |
