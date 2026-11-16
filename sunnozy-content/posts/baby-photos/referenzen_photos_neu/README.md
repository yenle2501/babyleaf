# Baby-Fotos nach Referenzfoto (16.11.2026)

KI-Bilder: Produktfoto des Sets + ein Referenzfoto aus `SUNNO\babyphoto` hochgeladen, die KI übernimmt Kamerawinkel, Szene, Licht, Filter und Baby der Referenz und tauscht nur die Kleidung. Alle Babys sind fiktiv. Beim Posten **«Mit KI erstellt»** einschalten.

Pro Set ein Bild im **Strampler** und eins im **Body** (mit Mütze, Söckchen oder Hose aus dem Set). Strampler und Body bekommen verschiedene Referenzfotos. Sets ohne Strampler haben nur ein Bild (Body + Hose).

Prompt und Zuordnung Set → Referenz: Projekt-Doc `content/baby-referenz-prompts.md` (claude.ai-Projekt «sunnozy-medien»).

## Methode ab 16.11. nachmittags («Bearbeitung»)

Das Referenzfoto wird nur umgezogen: Gemini bekommt zuerst die Referenz, dann das Produktfoto, mit dem Auftrag «Edit image 1 … change only the baby's clothes». So bleiben Neugeborenes, Szene, Deko und Filter wie im Original. Grund: Bei der freien Generierung wurden die Babys zu alt und die Szene passte nicht mehr zur Referenz.

## Methode «Stil» (ab 16.11. abends)

Wunsch: mehr Abwechslung bei Deko, Motiv und Hintergrund (Inspiration: Pinterest «neugeborene mode»). Pinterest-Fotos werden nur als Stilvorlage genommen, nicht hochgeladen: Das Baby ist neu generiert (Neugeborenes, ca. 2 Wochen), die Szene wird im Prompt beschrieben (Bett mit Leinen, Vichy-Decke, Lammfell, Seegraskorb, Musselintuch auf dem Sofa, Gitterbett mit Wolkenlaken, Strickdecke). Kein fremdes Foto und kein echtes Kind im Ergebnis.

## Dateien

- `<produkt>_baby*.png`: Sets aus `coming-soon/photos/shopify-backup-hauptbilder-coming-soon/`
- `set_<set>_baby_strampler.png` / `_body.png`: Sets aus `coming-soon/photos/produktfotos-set-praesentation/ki-roh/`

Nicht hochgerechnet. Formate: ChatGPT 1122 × 1402, Gemini 825 × 1024 (einige 825 × 1009, unten 15 px abgeschnitten), `set_hello_world_blatt_baby_body.png` 928 × 1152.

| Datei | Tool | Referenz |
|---|---|---|
| eisbaer-taupe_baby | ChatGPT | Download (18) |
| eisbaer-taupe_baby_v1-ohne-referenzlook | ChatGPT | Download (17), nur Stimmung |
| eisbaer-taupe_baby_body | Gemini, Stil | Taupe Leinendecke auf Bett, Strick-Eisbär |
| blumen-musselin_baby | ChatGPT | Soft, natural, and cozy… |
| born-in-2027-rosa_baby | Gemini | Baby Beanie, Jumper & Booties |
| born-in-2027-rosa_baby_strampler | Gemini, Stil | Rosa Grobstrickdecke auf weissem Bett, Trockenblumen |
| gaensebluemchen-beautiful_baby | Gemini | Download (13) |
| little-bear-rosa_baby | Gemini | Download (19) |
| little-bear-rosa_baby_body | Gemini, Stil | Weisse Teddyfleece-Decke, rosa Strickherz |
| set_waldbaer_creme_baby_strampler | Gemini | Download (12) |
| set_waldbaer_creme_baby_body | Gemini, Stil | Moosgrünes Musselintuch auf Holzboden, Tannzapfen, Holzbaum |
| weltall-hellblau_baby_body | Gemini | Milo Tan Gingham… |
| set_bauernhof | Strampler Gemini / Body Gemini, Stil | Strampler Soft… / Body: hellblaue Vichy-Decke, Holzschaf |
| set_best_family | Strampler Gemini / Body Gemini, Stil | Strampler D19 / Body: Teddy-Teppich am Fenster, Strickteddy, Weidenkorb |
| set_gaensebluemchen | Gemini | Strampler D17, Body Soft… |
| set_hase_rosa | Gemini | Strampler Milo, Body D18 |
| set_hello_schmetterling | Gemini | Strampler D12, Body D13 |
| set_hello_world_blatt | Gemini | Strampler D13, Body Baby Beanie |
| set_hello_world_creme | Gemini | Strampler Baby Beanie, Body D11 |
| set_hund_creme | Gemini | Strampler D18, Body D4 |
| set_lila_hase | Gemini, Bearbeitung | Strampler Soft…, Body D19 |
| set_little_and_loved_gans_rosa | Gemini, Bearbeitung | Strampler D12, Body Milo |
| set_little_bear | Gemini, Bearbeitung | Strampler D17, Body D12 |
| set_love_dad_mom | Gemini, Bearbeitung | Strampler D11, Body D17 |
| set_prinzessin_krone | Gemini, Bearbeitung | Strampler D12, Body Soft… |
| set_rosa | Strampler ChatGPT, Body Gemini, Bearbeitung | Strampler D13, Body D18 |
| set_smile_gruen | ChatGPT, Bearbeitung | Baby Beanie (nur Strampler) |
| set_teddy_creme | Strampler Gemini, Bearbeitung / Body ChatGPT, Stil | Strampler D18 / Body: Bett mit Leinen, Strickhase |
| set_teddy_rosa_punkte | Strampler Gemini, Stil / Body ChatGPT, Stil | Vichy-Decke mit Leinenkissen / Lammfell, Holzrassel |
| set_wal_blau | Gemini, Stil | Seegraskorb mit Waffeldecke / Musselintuch auf Sofa, Strickwal |
| set_weltall_hellblau | Gemini, Stil | blaue Strickdecke, Holzmond / Gitterbett mit Wolkenlaken |

Strampler und Body haben jetzt bei allen Sets eine eigene Szene. Die 6 Bilder mit doppelter Referenz (eisbaer-taupe Body, little-bear-rosa Body, set_waldbaer_creme Body, born-in-2027-rosa Strampler, set_bauernhof Body, set_best_family Body) wurden im Stil neu gemacht; alte Versionen in der Git-History.

## Vor dem Posten prüfen

- **Sicherer Schlaf:** Die KI übernimmt Requisiten aus der Referenz. Schlafendes Baby mit Plüschtier, Nuggi oder Decke: `set_hund_creme_baby_body` (Teddy am Gesicht, Decke über den Beinen), `set_hello_world_blatt_baby_strampler` (Nuggi, Plüschtier), `set_hello_world_creme_baby_body` (Plüschhase), `set_best_family_baby_strampler` (Plüschlöwe, Nuggi). Nicht für Ads verwenden.
- `born-in-2027-rosa_baby`: kleine Krönchen auf den Füsschen sind erfunden, gibt es im Set nicht.
- `weltall-hellblau_baby_body`: Hand der Mutter im Bild (aus der Referenz).
- `set_love_dad_mom_baby_strampler`: Baby liegt auf dem Bauch (aus Referenz D11), Schrift im Print teils gespiegelt.
- Bei der Bearbeitung bleiben Plüschtiere und Nuggi der Referenz drin (D12, D17, D19). Für Ads Referenzen ohne Plüschtier wählen.
- `set_teddy_rosa_punkte_baby_strampler` und `set_wal_blau_baby_strampler`: Baby schläft (ohne Decke oder Plüschtier am Gesicht).
- `set_waldbaer_creme_baby_body` (Stil): Bär-Motiv auf dem Body kleiner als im Original. `set_best_family_baby_body`: Mütze gestrickt statt Jersey.
- Prints und Schriften mit dem echten Set vergleichen.
