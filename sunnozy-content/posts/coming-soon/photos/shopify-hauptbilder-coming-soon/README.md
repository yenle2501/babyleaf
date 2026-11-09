# Shopify-Hauptbilder für 7 neue Sets (Coming soon)

Gleicher Stil wie die Erstausstattung-Hauptbilder im Shop (`../shopify-hauptbilder-praesentation-hd/`): warmer, heller Studio-Grund, Strampler oder Body am Holzbügel mit Wandknauf, die übrigen Teile gross in Spalten, sunnozy-Logo oben links. 2048 × 2048 px.

| Datei (`bilder/`) | Shopify-Produkt (Entwurf) | Teile |
|---|---|---|
| `little-bear-rosa.jpg` | Erstausstattung-Set «Little Bear» – Rosa | 5 |
| `eisbaer-taupe.jpg` | Erstausstattung-Set «Eisbär» – Taupe | 5 |
| `waldbaer-creme.jpg` | Erstausstattung-Set «Waldbär» – Creme | 5 |
| `born-in-2027-rosa.jpg` | Erstausstattung-Set «Born in 2027» – Rosa | 6 |
| `weltall-hellblau.jpg` | Erstausstattung-Set «Little One» Weltall – Hellblau, 3-teilig | 3 |
| `gaensebluemchen-beautiful.jpg` | Erstausstattung-Set «Beautiful» Gänseblümchen | 3 |
| `blumen-musselin.jpg` | Erstausstattung-Set «Blumenwiese» Musselin | 3 |

**So entstanden:** Canva (generate-image) mit zwei Vorlagen: das Set-Bild auf Weiss (`coming-soon/<set>/marktplatz/<set>_hauptbild_weiss.jpg`) für die Teile und das Hello-Little-Bear-Hauptbild für den Stil. Export in voller Grösse (`ki-roh/`), dann `python3 tools/hauptbild_logo.py ki-roh/<set>.png bilder/<set>.jpg` (2048 px, Logo).

**Status:** In Shopify als Hauptbild übernommen am 04.11.2026 (alle 7 Produkte sind noch Entwürfe). Per `fileUpdate` an derselben Media-ID ersetzt: Position und Alt-Text bleiben gleich. Live-Bild geprüft: 2048 px, entspricht der Datei. Die bisherigen Hauptbilder liegen in `../shopify-backup-hauptbilder-coming-soon/`.

**Hinweise**
- Mit KI erstellt: Prints, Stickereien und Farben vor dem Veröffentlichen mit dem echten Set vergleichen.
- «Born in 2027»: Das Kapuzentuch hängt über dem Bügel, die anderen 5 Teile liegen daneben.
