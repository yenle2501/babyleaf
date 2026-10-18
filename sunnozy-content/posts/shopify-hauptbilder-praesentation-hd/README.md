# Shopify-Hauptbilder Erstausstattung: neu aus den Einzelteilen gebaut (2048 px)

Die neuen Hauptbilder folgen dem Vorbild der Nutzerin (Teddybär-Set aus ChatGPT): warmer, heller Studio-Grund, Decke oder Strampler an einem Holzbügel mit Wandknauf, die übrigen Teile gross und geordnet daneben, weiche Schatten und das sunnozy-Logo oben links. Der Holzbügel ist aus diesem Vorbild freigestellt (`assets/buegel_holz.png`).

**Darum sind sie scharf:** Die alte Präsentation war ein einziges KI-Bild mit 1264 px, darin hatte jedes Teil nur rund 300 px. Jetzt wird jedes Teil einzeln aus seinem 2000-px-Bild (`marktplatz-galaxus-amazon/einzelteile/`) freigestellt und für das Gesamtbild **verkleinert** statt vergrössert. So bleiben Karomuster, Rippen, Spitze und Schrift scharf. Das Endformat ist 2048 × 2048 px, wie von Shopify empfohlen.

Erstellt mit: `python3 tools/make_set_hauptbild.py <ausgabe> [handle ...]`. Die Anordnung pro Set steht oben im Skript.

| Datei (`bilder/`) | Shopify-Produkt | Teile |
|---|---|---|
| `erstausstattung-set-teddybaer.jpg` | Erstausstattung-Set «Teddybär» | 9 Bilder: Decke, Strampler, Body, Mütze, Söckchen, Fäustlinge, Rassel, Beissring, Lätzchen |
| `erstausstattung-set-princess.jpg` | Erstausstattung-Set «Princess» | 8: Decke, Strampler, Body, Mütze, Fäustlinge, Söckchen, Rassel, Lätzchen |
| `erstausstattung-set-little-and-loved.jpg` | Erstausstattung-Set «Little and Loved» | 8: Strampler, Body, Jäckchen, T-Shirt, Hose, Mütze, Fäustlinge, Lätzchen |
| `erstausstattung-set-hello-world.jpg` | Erstausstattung-Set «Hello World» | 8: Strampler, Body, Jäckchen, T-Shirt, Hose, Mütze, Fäustlinge, Lätzchen |
| `erstausstattung-set-hello-spitze.jpg` | Erstausstattung-Set «Hello» Rosa | 6: Decke, Strampler, Body, Hose, Häubchen, Lätzchen |
| `erstausstattung-set-hello-little-bear.jpg` | Erstausstattung-Set «Hello Little Bear» | 5: Strampler, Body, Mütze, Fäustlinge, Lätzchen |

`check_vorher_nachher.jpg` zeigt pro Set das Bild, das jetzt im Shop ist, das neue Bild und je einen Detailausschnitt.

**Hinweise**
- Mit KI erstellt: Die Einzelteil-Bilder stammen aus den KI-Marktplatzbildern. Prints und Farben bitte mit dem echten Set vergleichen.
- Teddybär: Rassel und Beissring sind zwei Bilder, im Titel steht «8-teilig».

**Status:** wartet auf Freigabe. In Shopify ist noch nichts geändert.
