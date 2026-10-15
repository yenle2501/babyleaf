# Shopify-Hauptbilder auf Reinweiss

Die übrigen Shop-Fotos haben alle einen reinweissen Hintergrund (RGB 255). Die bisherigen Hauptbilder waren grau
(Kaskaden 244, KI-Bilder 242–244, Set-Präsentationen 230) und wirkten in der Galerie wie ein Fremdkörper.
Hier liegen dieselben Hauptbilder mit weissem Hintergrund. Die Produkte sind nicht verändert.

Check-Blatt: `../shopify-check_hintergrund_weiss.jpg` (links bisher, rechts neu)

| Art | Dateien | Wie entstanden |
|---|---|---|
| Kaskaden aus echten Fotos (16) | `dino_langarm3.jpg` … `mummy_langarm3.jpg`, `kombi_*.jpg`, `erstausstattung_little_and_loved.jpg` | neu gerendert mit `tools/make_kaskade.py` / `make_kaskade_set.py` (Hintergrund jetzt Weiss) |
| KI-Kaskaden (3) | `*_KI.jpg` | `tools/hintergrund_weiss.py` + Produktmaske (Canva remove-background). **Mit KI erstellt** |
| Set-Präsentationen (5) | `erstausstattung_*_praesentation.jpg` | `tools/hintergrund_weiss.py` + Maske; Logo, Bügel und Wandknauf bleiben original. **Mit KI erstellt** |

`hintergrund_weiss.py` teilt den grauen Grund durch seine eigene Helligkeit: Die Fläche wird 255, weiche Schatten
bleiben im gleichen Verhältnis erhalten. Ohne Maske funktioniert es bei farbigen Produkten. Bei Creme oder Weiss auf
Grau braucht es die Maske, sonst entstehen Flecken.

Offen (vor Upload bestätigen): Teddybär-Präsentation (zeigt 9 statt 8 Teile), Hello World (zeigt 7 statt 8 Teile),
Little and Loved (Kaskade).
