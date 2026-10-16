# Kampagne «Alles drin»

Teil des Markenplans (`strategie/sunnozy-markenplan.html`). Idee: Die echten Teile sind der Beweis für «Alles drin». Jedes Reel fragt «Was steckt drin?», dann erscheint Teil für Teil mit Namen. Am Schluss steht «Alles drin.» mit Teile-Anzahl, Preis und Gratisversand. Der Look folgt dem sunnozy-Designsystem: Creme, Waldgrün, Fraunces und Nunito Sans, keine Emojis.

## Dateien

| Set | Preis | Feed-Foto 4:5 | Reel 9:16 |
|---|---|---|---|
| Teddybär | CHF 30.40 | `foto_alles_drin_teddybaer_4x5.jpg` | `reel_alles_drin_teddybaer_9x16.mp4` (9,3 s) |
| Princess | CHF 30.40 | `foto_alles_drin_princess_4x5.jpg` | `reel_alles_drin_princess_9x16.mp4` (9,3 s) |
| Little and Loved | CHF 30.40 | `foto_alles_drin_little_and_loved_4x5.jpg` | `reel_alles_drin_little_and_loved_9x16.mp4` (9,3 s) |
| Hello World | CHF 29.40 | `foto_alles_drin_hello_world_4x5.jpg` | `reel_alles_drin_hello_world_9x16.mp4` (9,3 s) |
| Hello Rosa | CHF 30.40 | `foto_alles_drin_hello_rosa_4x5.jpg` | `reel_alles_drin_hello_rosa_9x16.mp4` (6,9 s) |
| Hello Little Bear | CHF 28.40 | `foto_alles_drin_hello_little_bear_4x5.jpg` | `reel_alles_drin_hello_little_bear_9x16.mp4` (7,5 s) |
| Alle 6 Sets | ab CHF 28.40 | | `reel_alles_drin_6_sets_9x16.mp4` (11,7 s): «Baby unterwegs?» → 6 Sets → «Alles drin.» |

`*_standbild.jpg` sind die Titelbilder der Reels. Die Reels sind stumm, den Sound wählst Du in Instagram oder Meta.

**Dankeskarte** (`dankeskarte/`): A6 hoch, 105 × 148 mm + 3 mm Beschnitt, 300 dpi. `dankeskarte_A6_druck.pdf` hat 2 Seiten (Vorder- und Rückseite) und kann direkt in die Druckerei. Die rote Linie in `dankeskarte_vorschau.jpg` zeigt das Endformat und wird nicht gedruckt.

**Mail-Texte:** `strategie/mail-ablauf.md`

## Vor dem Einsatz prüfen

- **Codes anlegen:** Die Codes **DANKE10** (10 % auf die nächste Bestellung) und **HALLOBABY** (10 % auf die erste Bestellung, zum Weitergeben) sind auf Karte und in den Mails, existieren in Shopify aber noch nicht. Andere Namen? Dann neu erzeugen: `python3 tools/make_dankeskarte.py posts/kampagne-alles-drin/dankeskarte CODE1 CODE2`.
- **Teddybär:** Im Shop steht «8-teilig», die Einzelbilder zeigen 9 Teile. Rassel und Beissring sind deshalb als ein Teil zusammengefasst. Bitte prüfen, wie Du sie zählst.
- **Hello Rosa:** Strampler, Body und Hose überlappen sich im Shopbild. Sie erscheinen deshalb als eine Kachel, zusammen sind es die 6 Teile laut Shop.
- **Bilder:** Die Einzelbilder stammen aus den Marktplatz-Bildern, teils KI-unterstützt. Prints und Farben mit dem echten Set vergleichen.

## Bildunterschrift (Vorschlag)

> Alles drin für die ersten Wochen. Strampler, Body, Mützchen und mehr, fertig aufeinander abgestimmt. Ab CHF 28.40, in 2–3 Werktagen bei Dir, Gratisversand in der Schweiz ab CHF 50.
> sunnozy.ch
> #sunnozy #erstausstattung #babyschweiz #geburtsgeschenk #neugeboren #babyset

Erstellt mit `tools/make_alles_drin.py` und `tools/make_dankeskarte.py`.
