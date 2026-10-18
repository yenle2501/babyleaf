# Shopify-Hauptbilder Erstausstattung im Stil des ChatGPT-Vorbilds (2048 px)

Vorbild ist das Teddybär-Bild der Nutzerin aus ChatGPT: warmer, heller Studio-Grund, Decke oder Strampler an einem Holzbügel mit Wandknauf, die übrigen Teile gross und geordnet in Spalten, weiche Schatten und das sunnozy-Logo oben links.

| Datei (`bilder/`) | Shopify-Produkt | Teile | Entstehung |
|---|---|---|---|
| `erstausstattung-set-teddybaer.jpg` | «Teddybär» | 9 Bilder (Rassel und Beissring einzeln) | das ChatGPT-Bild selbst, auf 2048 px gebracht |
| `erstausstattung-set-princess.jpg` | «Princess» | 8 | Canva-KI |
| `erstausstattung-set-little-and-loved.jpg` | «Little and Loved» | 8 | Canva-KI |
| `erstausstattung-set-hello-world.jpg` | «Hello World» | 8 | Canva-KI |
| `erstausstattung-set-hello-spitze.jpg` | «Hello» Rosa | 6 | Canva-KI |
| `erstausstattung-set-hello-little-bear.jpg` | «Hello Little Bear» | 5 | Canva-KI |

**So entstanden:** In Canva (generate-image) wurden zwei Vorlagen kombiniert: das scharfe Set-Bild auf Weiss (`marktplatz-galaxus-amazon/hauptbild/`) für die Teile und das ChatGPT-Bild für den Stil. Das Ergebnis wurde in 2048 px exportiert (`ki-roh/`). Danach setzt `python3 tools/hauptbild_logo.py <ki-roh> <ausgabe>` das Logo in Grösse, Lage und Farbe wie im Vorbild.

`uebersicht.jpg` zeigt alle 6 Bilder. `check_vorher_nachher.jpg` stellt jedes Bild dem gegenüber, das jetzt im Shop ist.

**Hinweise**
- Mit KI erstellt: Prints, Stickereien und Farben bitte mit dem echten Set vergleichen.
- Teddybär: Im Bild sind 9 Teile, im Titel steht «8-teilig».

**Status:** wartet auf Freigabe. In Shopify ist noch nichts geändert.
