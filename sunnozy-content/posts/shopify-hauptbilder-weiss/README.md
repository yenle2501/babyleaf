# Shopify-Hauptbilder auf Reinweiss

Die übrigen Shop-Fotos haben alle einen reinweissen Hintergrund (RGB 255). Die bisherigen Hauptbilder waren grau
(Kaskaden 244, KI-Bilder 242–244, Set-Präsentationen 230) und wirkten in der Galerie wie ein Fremdkörper.
Hier liegen dieselben Hauptbilder mit weissem Hintergrund. Die Produkte sind nicht verändert.

Check-Blatt: `../shopify-check_hintergrund_weiss.jpg` (links bisher, rechts neu)

| Art | Dateien | Wie entstanden |
|---|---|---|
| Kaskaden aus echten Fotos (16) | `dino_langarm3.jpg` … `mummy_langarm3.jpg`, `kombi_*.jpg` | neu gerendert mit `tools/make_kaskade.py` / `make_kaskade_set.py` (Hintergrund jetzt Weiss) |
| KI-Kaskaden (3) | `*_KI.jpg` | `tools/hintergrund_weiss.py` + Produktmaske (Canva remove-background). **Mit KI erstellt** |
| Set-Präsentationen (6) | `erstausstattung_*_praesentation.jpg` | `tools/hintergrund_weiss.py` + Maske; Logo, Bügel und Wandknauf bleiben original. **Mit KI erstellt** |

`hintergrund_weiss.py` teilt den grauen Grund durch seine eigene Helligkeit: Die Fläche wird 255, weiche Schatten
bleiben im gleichen Verhältnis erhalten. Ohne Maske funktioniert es bei farbigen Produkten. Bei Creme oder Weiss auf
Grau braucht es die Maske, sonst entstehen Flecken.

Neu als Hauptbild (bisher kein Präsentationsbild im Shop): Teddybär (Bild zeigt 9 Teile, Beissring und Rassel getrennt,
Shop sagt 8-teilig), Hello World und Little and Loved (beide neu erstellt am 15.10., je 8 Teile wie im Shop).

Zusatzbilder: siehe `../shopify-zusatzbilder-weiss/`.

## Theme-Fix: Hauptbild ganz sichtbar (15.10.2026)

Auf der Produktseite (Desktop) wurde das quadratische Hauptbild links/rechts angeschnitten, weil
`snippets/bl-head-polish.liquid` (Fix 1) die Galerie-Bilder mit `object-fit: cover` füllt.
Im neuen Theme **«sunnozy FINAL 106 – Hauptbild ganz sichtbar»** (Kopie von FINAL 104) steht dort `contain`
plus weisser Hintergrund. Mobil war schon `contain`, Zoom-Ansicht und Kollektionskarten sind unverändert.
Vorher/Nachher-Screenshots und die geänderte Datei in `theme-fix/`. Veröffentlichen im Shopify-Admin.
