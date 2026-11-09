# Shopify-Zusatzbilder für die neuen Sets (Einzelteile und Nahaufnahmen)

Gleicher Stil wie die neuen Hauptbilder (`../shopify-hauptbilder-coming-soon/`): warmer, heller Studio-Grund, grosse Teile am Holzbügel oder flach gelegt. 2048 × 2048 px, ohne Logo.

Pro Set ein Ordner mit jedem Teil einzeln (`strampler.jpg`, `body.jpg`, `muetze.jpg` …) und Nahaufnahmen von Stoff und Muster (`nah_*.jpg`).

**So entstanden:** Canva (generate-image) mit dem neuen Hauptbild des Sets als Vorlage, Export in voller Grösse, dann `python3 tools/hauptbild_logo.py <roh> <ziel> --ohne-logo` (2048 px, leicht geschärft).

## Status in Shopify (Entwürfe)

| Set | Bilder in Shopify | Stand |
|---|---|---|
| «Little Bear» Rosa | Hauptbild, Strampler, Body, Mütze, Fäustlinge, Lätzchen, Stoff, Print | übernommen 04.11.2026 |
| «Eisbär» Taupe | Hauptbild, Strampler, Body, Mütze, Fäustlinge, Lätzchen, Muster, Print | übernommen 04.11.2026 |
| «Waldbär» Creme | Hauptbild, Strampler, Body, Mütze, Fäustlinge, Lätzchen, Muster, Print | übernommen 04.11.2026 |
| «Born in 2027» Rosa | Hauptbild, Kapuzentuch, Strampler, Body, Hose, Mütze, Lätzchen, Stoff mit Ballon-Muster, Stickerei | übernommen 04.11.2026 |
| «Little One» Weltall | Hauptbild, Wickelbody, Fusshose, Knotenmütze, Weltall-Muster, Planet-Print | übernommen 04.11.2026 |
| «Beautiful» Gänseblümchen | Hauptbild, Wickelbody, Fusshose, Knotenmütze, Kragen mit Stickerei, Gänseblümchen-Muster, Weissbild (alt, behalten) | übernommen 04.11.2026 |
| «Blumenwiese» Musselin | Hauptbild, Wickelbody, Fusshose, Haarband, Musselin-Stoff, Schleife, Weissbild (alt, behalten) | übernommen 04.11.2026 |

Die bisherigen weissen Einzelteil-Bilder wurden per `fileUpdate` an derselben Media-ID ersetzt (Fäustlinge, Lätzchen, Mütze, «Strampler und Body» → Strampler, «Kapuzentuch strampler body hose» → Kapuzentuch). Die alten Dateien liegen weiterhin unter `../coming-soon/<set>/marktplatz/einzelteile/`. Body, Nahaufnahmen, Strampler und Hose (Born in 2027) sind neu dazugekommen. Reihenfolge: Hauptbild, Strampler, Body, Mütze, Fäustlinge, Lätzchen, Nahaufnahmen. Alt-Texte: «Erstausstattung-Set «…» – <Teil>».

**Mit KI erstellt:** Prints, Stickereien und Farben vor dem Veröffentlichen mit dem echten Set vergleichen.
