# Shopify-Zusatzbilder auf Reinweiss

Alle 284 Bilder der 53 Produkte wurden geprüft (Randfarbe gemessen, dann von Auge):

| Gruppe | Anzahl | Was passiert |
|---|---|---|
| schon reinweiss | 171 | nichts |
| Hauptbilder grau | 22 (+3 neu) | siehe `../shopify-hauptbilder-weiss/` |
| Studiofotos fast weiss (248–252, leicht grau/bläulich) | 41 | `tools/weiss_angleichen.py`: nur Lichter auf 255, Produktfarben unverändert |
| Studiofotos mit grauem/beigem Grund | 6 (5 verschiedene) | `tools/hintergrund_weiss.py` + Canva-Maske |
| Szenen, Babys, Holz, Decken, Nahaufnahmen | 44 | bleiben bewusst so |

Dateiname: `<shopify-handle>_bild<NN>.jpg` (NN = Position im Shop ab 00). Check-Blätter: `../shopify-check_zusatzbilder_1.jpg`, `_2.jpg`.


## In Shopify umgesetzt (15.10.2026)

- **69 Bilder ersetzt** mit `fileUpdate(originalSource)`: gleiche Medien-ID, gleiche Position, gleicher Alt-Text, nur der Bildinhalt ist jetzt weiss.
  22 Hauptbilder und 47 Zusatzbilder. Geprüft: alle READY, Ecken der ausgelieferten Bilder 253–255.
- **3 Hauptbilder neu:** Hello World und Little and Loved (neue 8-teilige Präsentation, Position 1).
  Beim Teddybär war um 14:00 UTC schon `set_teddy_creme_quadratisch.jpg` (grau) als Hauptbild hochgeladen worden;
  dieses Bild wurde auf die weisse Version umgestellt und mit Alt-Text versehen, das doppelte Bild wieder gelöscht.
- **Rückgängig machen:** Originale der 47 Zusatzbilder in `../shopify-backup-originale/` (Name = `<handle>__<position>.jpg`),
  die grauen Hauptbilder in `../shopify-hauptbilder-kaskade/` bzw. `../produktfotos-set-praesentation/mit_logo/`.
  Mit `fileUpdate(files:[{id, originalSource}])` auf die Medien-ID zurücksetzen.

| Medien-ID | neue Datei |
|---|---|
| `63905216823639` | mummy_langarm3.jpg |
| `63905216233815` | i_love_hugs_aermellos3.jpg |
| `63905216594263` | little_love_rosa5_KI.jpg |
| `63905216659799` | little_one5_KI.jpg |
| `63905280590167` | erstausstattung_princess_praesentation.jpg |
| `63905280622935` | erstausstattung_hello_rosa_praesentation.jpg |
| `63905280655703` | erstausstattung_hello_little_bear_praesentation.jpg |
| `63905216069975` | dinosaur_kurzarm5.jpg |
| `63905216790871` | mummy_kurzarm5.jpg |
| `63905216266583` | i_love_my_mum_kurzarm5.jpg |
| `63905216332119` | jogginghose5.jpg |
| `63905216528727` | leggings5.jpg |
| `63905216201047` | growing_up_strong_kurzarm5.jpg |
| `63905216856407` | sweet_friends_kurzarm5_KI.jpg |
| `63905215971671` | dino_langarm3.jpg |
| `63905216692567` | love_more_kurzarm5.jpg |
| `63905216168279` | flying_langarm3.jpg |
| `63905216725335` | lovely_langarm3.jpg |
| `63905216758103` | mumdadme_langarm5.jpg |
| `63905216430423` | kombi_lovely.jpg |
| `63905216463191` | kombi_mumdadme.jpg |
| `63905216397655` | kombi_growing_up_strong.jpg |
| `62417452695895` | body-set-i-love-my-mummy__02.png |
| `62417452630359` | body-set-i-love-my-mummy__03.png |
| `62417452958039` | body-set-i-love-my-mummy__04.png |
| `61769242214743` | sommer-set-krokodil__00.jpg |
| `61915268940119` | sommer-set-krokodil__01.png |
| `61902837088599` | sommer-set-be-brave__00.png |
| `62521823101271` | body-set-i-love-hugs-aermellos__02.png |
| `62521814384983` | body-set-i-love-hugs-aermellos__03.png |
| `62521814221143` | body-set-i-love-hugs-aermellos__04.png |
| `62417210409303` | erstausstattung-set-little-and-loved__06.png |
| `61920305414487` | baby-geschenkset-cute-and-hungry-4-teilig__00.png |
| `62417367433559` | erstausstattung-set-hello-world__07.png |
| `62857112813911` | body-set-i-love-my-mummy-kurzarm__02.png |
| `61861878694231` | mulltuecher-3er-set-blau-90x100-musselin__02.png |
| `61912583536983` | baby-halstuecher-3er-set-i-love-my-mummy-rosa__00.png |
| `61912583504215` | baby-halstuecher-3er-set-i-love-my-mummy-rosa__01.png |
| `63535131656535` | baby-halstuecher-3er-set-i-love-my-mummy__00.png |
| `61912548606295` | baby-halstuecher-3er-set-i-love-my-mummy__01.png |
| `62417357668695` | baby-halstuecher-3er-set-i-love-my-mummy__02.png |
| `62417357635927` | baby-halstuecher-3er-set-i-love-my-mummy__03.png |
| `62417338794327` | baby-halstuecher-3er-set-cool-like-daddy__01.png |
| `62417338892631` | baby-halstuecher-3er-set-cool-like-daddy__02.png |
| `62417338859863` | baby-halstuecher-3er-set-cool-like-daddy__03.png |
| `61912596709719` | baby-halstuecher-3er-set-baby-flowers__00.png |
| `62417336271191` | baby-halstuecher-3er-set-baby-flowers__01.png |
| `62417336205655` | baby-halstuecher-3er-set-baby-flowers__02.png |
| `62417336238423` | baby-halstuecher-3er-set-baby-flowers__03.png |
| `61920250560855` | baby-soeckchen-5er-set-spitze-bluemchen__00.png |
| `61920250495319` | baby-soeckchen-5er-set-spitze-bluemchen__01.png |
| `61920250528087` | baby-soeckchen-5er-set-spitze-bluemchen__02.png |
| `61920187547991` | baby-soeckchen-5er-set-neutral-umschlag__01.png |
| `61920238371159` | baby-soeckchen-5er-set-tier-und-natur__01.png |
| `61920353845591` | baby-geschenkset-beige-teddy-4-teilig__00.png |
| `61920353812823` | baby-geschenkset-beige-teddy-4-teilig__02.png |
| `61920283656535` | baby-geschenkset-dream-big-4-teilig__00.png |
| `61920283689303` | baby-geschenkset-dream-big-4-teilig__01.png |
| `61920345424215` | baby-geschenkset-rosa-safari-4-teilig__00.png |
| `61920345522519` | baby-geschenkset-rosa-safari-4-teilig__01.png |
| `63815292322135` | kombi-set-teddybar-latzchen-nuscheli__00.png |
| `63815292682583` | kombi-set-rosa-safari-latzchen-nuscheli__00.png |
| `63815292748119` | kombi-set-rosa-safari-latzchen-nuscheli__02.png |
| `61920215761239` | baby-soeckchen-5er-set-pastell-umschlag__00.jpg |
| `61920187515223` | baby-soeckchen-5er-set-neutral-umschlag__00.jpg |
| `61915431469399` | body-set-little-love-rosa__04.png |
| `61920238436695` | baby-soeckchen-5er-set-tier-und-natur__00.jpg |
| `61920323502423` | baby-geschenkset-grow-in-nature-4-teilig__01.jpg |
| `63815292879191` | kombi-set-grow-in-nature-latzchen-nuscheli__02.jpg |
