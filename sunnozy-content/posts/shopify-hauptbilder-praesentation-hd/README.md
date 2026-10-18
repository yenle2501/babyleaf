# Shopify-Hauptbilder Erstausstattung: Präsentation in 2048 px

Die neuen Hauptbilder zeigen die Set-Präsentation mit hellgrauem Studio-Hintergrund, Holzbügel und sunnozy-Logo (`produktfotos-set-praesentation/mit_logo`). Sie sollen die Bilder auf reinweissem Hintergrund ersetzen, die heute im Shop sind.

**Qualität:** Die Bilder sind neu ab den KI-Rohdateien (1264 px) gerechnet, auf 2048 × 2048 px. Das ist die Grösse, die Shopify empfiehlt. Die bisherigen `mit_logo`-Dateien hatten nur 1080 px.

Getestet wurde auch ein KI-Hochrechner (Real-ESRGAN). Er glättet aber das Karomuster (Princess), die Lochspitze und die Rippen. Darum ist er nicht verwendet.

Erstellt mit: `python3 tools/make_set_shop.py <ki-roh> <ausgabe> --groesse=2048`

| Datei (`bilder/`) | Shopify-Produkt | Quelle |
|---|---|---|
| `erstausstattung-set-teddybaer.jpg` | Erstausstattung-Set «Teddybär» | `set_teddy_creme_quadratisch` |
| `erstausstattung-set-princess.jpg` | Erstausstattung-Set «Princess» | `set_rosa_quadratisch` |
| `erstausstattung-set-little-and-loved.jpg` | Erstausstattung-Set «Little and Loved» | `set_little_and_loved_gans_rosa_quadratisch` |
| `erstausstattung-set-hello-world.jpg` | Erstausstattung-Set «Hello World» | `set_hello_world_creme_quadratisch` |
| `erstausstattung-set-hello-spitze.jpg` | Erstausstattung-Set «Hello» Rosa | `set_hello_schmetterling_quadratisch` |
| `erstausstattung-set-hello-little-bear.jpg` | Erstausstattung-Set «Hello Little Bear» | `set_little_bear_quadratisch` |

`check_vorher_nachher.jpg` zeigt pro Set: das Bild, das jetzt im Shop ist, das neue Bild und einen Detailausschnitt alt (1080 px) gegen neu (2048 px).

**Status:** wartet auf Freigabe. In Shopify ist noch nichts geändert.
