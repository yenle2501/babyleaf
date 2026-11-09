# posts – neue Struktur (09.11.2026)

Alles liegt jetzt in drei Ordnern. Gelöscht wurde nichts.

| Ordner | Was |
|---|---|
| `coming-soon/reels/` | alle Videos und Reels (mp4/mov), Musik und die Titelbilder der Reels. Die Coming-soon-Reels (Countdown, Flackern, Schleife, Weihnachts-Reveal) liegen direkt hier, alle anderen in Unterordnern nach Thema (z.B. `kampagne-weihnachtsbox/`, `pov-mama/`, `hello-little-bear/`, `videos-baby/`, `musik/`) |
| `coming-soon/photos/` | alle Produkt-, Shop-, Ads- und Marktplatzbilder, nach Thema bzw. Set (z.B. `strampler-hund-creme/`, `kampagne-weihnachtsbox/`, `marktplatz-galaxus-amazon/`, `shopify-*`, `meta-ads-*`, `paket-*`) |
| `baby-photos/` | alle Babyfotos (KI und Muster), z.B. `kampagne-weihnachtsbox/baby-pinterest-stil/`, `kampagne-weihnachtsbox/baby-in-box-kleidung/`, `baby-fotos-muster/`, `paket-17-baby-alltag/` |

Die alten Ordnernamen sind als Unterordner geblieben. READMEs liegen bei den Bildern oder Reels ihres Themas.
Jede verschobene Datei steht mit altem und neuem Pfad in `umzug_2026-11-09.json`.

**Hinweis Skripte:** Die Skripte in `tools/` verwenden noch die alten Pfade. Vor dem nächsten Neu-Erzeugen müssen die Pfade angepasst werden, Hilfe dazu: `tools/pfade.py` (`neu('kampagne-weihnachtsbox/…')` liefert den neuen Pfad).

## Wo ist was (alter Ordner → neuer Ort, Anzahl Dateien)

| Alter Ordner | Neuer Ort |
|---|---|
| baby-fotos-muster | baby-photos/baby-fotos-muster (4) |
| coming-soon | coming-soon/photos (8) |
| coming-soon/best-family-teddy | coming-soon/reels (2) |
| coming-soon/blumen-musselin | coming-soon/photos (9), coming-soon/reels (2) |
| coming-soon/born-in-2027-blau | coming-soon/photos (12) |
| coming-soon/born-in-2027-rosa | coming-soon/photos (13) |
| coming-soon/dino-cool-dude | coming-soon/photos (15) |
| coming-soon/eisbaer-taupe | coming-soon/photos (14) |
| coming-soon/gaensebluemchen | coming-soon/reels (3), coming-soon/photos (2) |
| coming-soon/gaensebluemchen-beautiful | coming-soon/photos (11) |
| coming-soon/gerippt-beige-baer | coming-soon/photos (9) |
| coming-soon/heissluftballon-dream-big | coming-soon/photos (10) |
| coming-soon/hosen-baeren | coming-soon/photos (13) |
| coming-soon/hosen-herzen-rosa | coming-soon/photos (13) |
| coming-soon/i-love-you-dad | coming-soon/photos (9) |
| coming-soon/knotenmuetzen-baer | coming-soon/photos (9) |
| coming-soon/little-bear-rosa | coming-soon/photos (14) |
| coming-soon/little-princess | coming-soon/reels (5), coming-soon/photos (2) |
| coming-soon/little-princess-wickelbody | coming-soon/photos (9) |
| coming-soon/muetzen-schleifen | coming-soon/photos (8) |
| coming-soon/originalFotos | coming-soon/photos (43) |
| coming-soon/schleife | coming-soon/reels (1) |
| coming-soon/strampler-avocado | coming-soon/photos (9) |
| coming-soon/strampler-blumen-hase | coming-soon/photos (13) |
| coming-soon/strampler-hund-creme | coming-soon/photos (17) |
| coming-soon/strampler-kaetzchen-tulpen | coming-soon/photos (13) |
| coming-soon/strampler-kirschen | coming-soon/photos (13) |
| coming-soon/strampler-neutral | coming-soon/photos (3) |
| coming-soon/strampler-rosa-little-princess | coming-soon/photos (13) |
| coming-soon/strampler-segelboote | coming-soon/photos (13) |
| coming-soon/strampler-smile-gruen | coming-soon/photos (12) |
| coming-soon/strampler-sweet-home | coming-soon/photos (13) |
| coming-soon/strampler-waldtiere | coming-soon/photos (13) |
| coming-soon/turban-muetzen | coming-soon/photos (9) |
| coming-soon/waldbaer-creme | coming-soon/photos (14) |
| coming-soon/weltall-hellblau | coming-soon/photos (14) |
| instagram | coming-soon/photos (101), coming-soon/reels (7) |
| kampagne-alles-drin | coming-soon/photos (19), coming-soon/reels (14) |
| kampagne-coming-soon-sets | coming-soon/photos (1) |
| kampagne-weihnachtsbox | coming-soon/photos (308), baby-photos/kampagne-weihnachtsbox (162), coming-soon/reels (84) |
| marktplatz-galaxus-amazon | coming-soon/photos (163) |
| meta-ads-erstausstattung | coming-soon/photos (36) |
| meta-ads-fotos | coming-soon/photos (50) |
| oneve-stil | coming-soon/photos (9) |
| paket-10-produkte | coming-soon/photos (48) |
| paket-11-details-reel | coming-soon/photos (6), coming-soon/reels (2) |
| paket-13-farbwechsel-reel | coming-soon/reels (4), coming-soon/photos (1) |
| paket-14-weihnachts-wunschliste | coming-soon/reels (4), coming-soon/photos (1) |
| paket-15-wochen-uhr | coming-soon/photos (7), coming-soon/reels (4) |
| paket-16-bei-null-anfangen | coming-soon/photos (4), coming-soon/reels (4) |
| paket-17-baby-alltag | baby-photos/paket-17-baby-alltag (20), coming-soon/reels (4) |
| paket-18-baby-alltag-2 | baby-photos/paket-18-baby-alltag-2 (18), coming-soon/reels (4) |
| paket-3 | coming-soon/photos (39), coming-soon/reels (3) |
| paket-4 | coming-soon/photos (17), coming-soon/reels (1) |
| paket-5 | coming-soon/photos (25) |
| paket-6-soft | coming-soon/photos (26), coming-soon/reels (3) |
| paket-7-werbung | coming-soon/photos (25) |
| paket-8-video-flow | coming-soon/photos (5), coming-soon/reels (5) |
| paket-9-ads | coming-soon/photos (17) |
| posts_preview.png | coming-soon/photos (1) |
| product-photos-present | coming-soon/photos (34) |
| produktfotos-geschenkbox-weihnachten | coming-soon/photos (16) |
| produktfotos-outfit | coming-soon/photos (12) |
| produktfotos-pro | coming-soon/photos (17) |
| produktfotos-set-praesentation | coming-soon/photos (88) |
| reels-neu | coming-soon/reels (4) |
| reels/coming-soon | coming-soon/reels (171), coming-soon/photos (2) |
| reels/hello-little-bear | coming-soon/reels (3), coming-soon/photos (2) |
| reels/im-shop | coming-soon/reels (12), coming-soon/photos (1) |
| reels/musik | coming-soon/reels (6) |
| reels/pov-mama | coming-soon/reels (12), coming-soon/photos (1) |
| reels/runde5 | coming-soon/reels (23), coming-soon/photos (1) |
| schrift-sacramento | coming-soon/photos (2) |
| sets-flatlay | coming-soon/photos (4) |
| shopify-backup-hauptbilder-coming-soon | coming-soon/photos (7) |
| shopify-backup-hauptbilder-vor-chatgpt-stil | coming-soon/photos (6) |
| shopify-backup-hauptbilder-vor-klar | coming-soon/photos (53) |
| shopify-backup-originale | coming-soon/photos (48) |
| shopify-backup-preise | coming-soon/photos (1) |
| shopify-check_erstausstattung.jpg | coming-soon/photos (1) |
| shopify-check_hintergrund_weiss.jpg | coming-soon/photos (1) |
| shopify-check_seite1.jpg | coming-soon/photos (1) |
| shopify-check_seite2.jpg | coming-soon/photos (1) |
| shopify-check_seite3.jpg | coming-soon/photos (1) |
| shopify-check_teddy_helloworld.jpg | coming-soon/photos (1) |
| shopify-check_zusatzbilder_1.jpg | coming-soon/photos (1) |
| shopify-check_zusatzbilder_2.jpg | coming-soon/photos (1) |
| shopify-hauptbilder-coming-soon | coming-soon/photos (16) |
| shopify-hauptbilder-kaskade | coming-soon/photos (26) |
| shopify-hauptbilder-klar | coming-soon/photos (58) |
| shopify-hauptbilder-praesentation-hd | coming-soon/photos (15) |
| shopify-hauptbilder-weiss | coming-soon/photos (29) |
| shopify-zusatzbilder-coming-soon | coming-soon/photos (46) |
| shopify-zusatzbilder-weiss | coming-soon/photos (48) |
| studio-fotos | coming-soon/photos (44) |
| unboxing | coming-soon/reels (3) |
| videos-baby | coming-soon/reels (163), coming-soon/photos (5) |
| videos-produkt | coming-soon/reels (6) |
| viral-muster | coming-soon/photos (7) |
| woche-handschrift | coming-soon/photos (7), coming-soon/reels (1) |