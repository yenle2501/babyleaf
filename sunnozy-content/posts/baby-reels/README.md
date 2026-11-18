# Baby-Reels (17.11.2026)

66 Einzel-Reels (Runde 1: 8, Runde 2: 16, Runde 3: 24, Runde 4: 18) und 17 Mix-Reels in `mix/` aus den neuen Grok-Clips in `../baby-videos/` (Stil «Strecken»). Skript: `tools/make_baby_reels.py`.

## Was aus der Viral-Analyse übernommen ist

Grundlage: Viral-Analyse @babyothelabel, @avalia.kids, @zayac_mehovoi (Projekt-Doc `social/viral-analyse-babyo-avalia-zayac.md`).

- **Neugeborenes streckt sich**, ein Take, Kamera fast still (zayac: 2.8 Mio. Views)
- **Hook ab dem ersten Bild**: POV / Warnung / «Schick das …», höchstens 8 Wörter
- **Klarer Empfänger** zum Teilen: Freundin, Gotti, Grosi, werdende Eltern
- **Loop**: 10 s Video, Text am Anfang (0–3.2 s) und wieder ab 8.6 s, dann 2,6 s Endfolie (gesamt 12.2 s)
- Weisse Schreibmaschinenschrift (Courier Prime) mit Emoji, oben über dem Kopf, damit Gesicht und Print frei bleiben
- Clip leicht entrauscht, wärmer, nachgeschärft. Musik: Alex Morgan (Standard-Track)
- Nur Clips ohne Plüschtier, Nuggi und lose Decke beim Baby

## Bearbeitung v2 (18.11.2026): Hook-Recherche Instagram 2026

Was 2026 bei Reels zählt (Quellen: Meta/Instagram-Hinweise zu Skip Rate, Reel-Guides von blitzcut, hoopr, unfollr, nestscale, postigniter):
- **DM-Shares** sind das wichtigste Signal → jeder Hook nennt eine Person zum Weiterschicken
- **Skip Rate in den ersten 3 s** wird gemessen, bis zu 50 % wischen weg → Bewegung ab Bild 1, Text in 0,5 s
- **Text im oberen Drittel**, 5–8 Wörter, funktioniert ohne Ton
- **7–15 s** und Loop, Wiederholungen zählen
- **Zoom-Übergänge, Schnitte im Takt, Nummern-Hooks** («1, 2, 3 oder 4?») halten die Leute und bringen Kommentare

Umgesetzt in allen Reels:
- Start bei 0,8 s: Die Grok-Clips beginnen mit dem stehenden Foto, jetzt ist ab Bild 1 Bewegung drin
- Punch-in-Zoom 112 % → 100 % in den ersten 0,5 s
- Hook tippt sich in 0,5 s ein (Schreibmaschine), am Ende steht er für den Loop wieder da
- Länge jetzt 9,2 s + Endfolie = 11,4 s
- Titelbild = Bild bei 0,6 s mit ganzem Hook (beim Hochladen als Cover wählen)

## Mix-Reels (`mix/`, `tools/make_baby_reels_mix.py`)

Mehrere Clips zusammengeschnitten, Zoom-Übergang bei jedem Schnitt, Endfolie mit 2×2-Collage der Sets.

| Reel | Hook | Inhalt | Caption |
|---|---|---|---|
| `reel_mix_welches_set_shop_9x16.mp4` | Welches Set nimmst Du? Schreib die Nummer 👇 | 4 Shop-Sets, je 2,5 s, Nummer 1–4 | Welches nimmst Du: 1, 2, 3 oder 4? Schreib die Nummer, wir schicken Dir den Link 👇 #erstausstattung #babygeschenk #neugeboren #babyschweiz #sunnozy |
| `reel_mix_gotti_such_aus_9x16.mp4` | Gotti, such Dir eins aus 🎀 | 4 Mädchen-Sets, Nummern | Markier die Gotti und lass sie wählen 🎀 #gotti #babygeschenk #babygirl #babyschweiz #sunnozy |
| `reel_mix_es_wird_ein_bub_9x16.mp4` | POV: Es wird ein Bub 💙 | Weltall, Wal, Waldbär, Bauernhof | Welches für Euren Bub? Schreib die Nummer 💙 #esisteinbub #babyboy #schwanger #babyschweiz #sunnozy |
| `reel_mix_es_wird_ein_maedchen_9x16.mp4` | POV: Es wird ein Mädchen 🎀 | Princess, Gänseblümchen, Lila Hase, Hello | Welches für Eure Kleine? Schreib die Nummer 🎀 #esisteinmaedchen #babygirl #schwanger #babyschweiz #sunnozy |
| `reel_mix_babyfieber_kompilation_9x16.mp4` | Warnung: 5× Babyfieber am Stück 🥹 | 5 Strecker, je 2 s | Wir haben gewarnt 🥹 Schick das jemandem, der auch Babyfieber hat. #babyfieber #neugeboren #babyliebe #babyschweiz #sunnozy |
| `reel_mix_haende_hoch_9x16.mp4` | Hände hoch, wer Babyfieber hat 🙌 | 5× «Hände hoch»-Pose | 🙌 Markier alle, die jetzt die Hand heben. #babyfieber #neugeboren #babyliebe #babyschweiz #sunnozy |

Hinweis: Die Mix-Reels «welches_set_shop» und «es_wird_ein_maedchen» zeigen Shop-Sets und Coming-soon-Sets gemischt bzw. nur Shop. Preis nie im Reel, bei Nachfrage per DM.

## Reels und Captions

| Reel | Clip | Hook | Endfolie |
|---|---|---|---|
| `reel_little_bear_freundin_9x16.mp4` | `set_little_bear_baby_strampler_1` | Schick das Deiner Freundin, die bald Mami wird 🧸 | Hello Little Bear · Erstausstattung 5 Teile · Shop |
| `reel_hello_world_erstes_outfit_9x16.mp4` | `set_hello_world_blatt_baby_body_1` | POV: Sein allererstes Outfit sagt «Hello World» ✨ | Hello World · 8 Teile · Shop |
| `reel_teddy_babyfieber_9x16.mp4` | `set_teddy_creme_baby_strampler_1` | Warnung: Babyfieber-Gefahr 🥹 | Teddybär · 8 Teile · Shop |
| `reel_dad_mom_bald_eltern_9x16.mp4` | `set_love_dad_mom_baby_body_2` | POV: In ein paar Wochen seid Ihr Mama und Papa 🤍 | I love Dad Mom · coming soon |
| `reel_weltall_astronaut_9x16.mp4` | `set_weltall_hellblau_baby_body_1` | POV: Euer kleiner Astronaut ist gelandet 🪐 | Little One · Weltall · coming soon |
| `reel_teddy_rosa_gotti_9x16.mp4` | `set_teddy_rosa_punkte_baby_strampler_1` | POV: Du wirst Gotti und das Geschenk ist klar 🎀 | Teddy Rosa · coming soon |
| `reel_prinzessin_grosi_9x16.mp4` | `set_prinzessin_krone_baby_body_1` | Schick das dem Grosi der kleinen Prinzessin 👑 | Little Princess · coming soon |
| `reel_waldbaer_winterbaby_9x16.mp4` | `set_waldbaer_creme_baby_body_1` | POV: Dein Baby kommt im Winter 🌲 | Waldbär · coming soon |

### Captions (kopierfertig)

**little_bear_freundin**
Für die Freundin, die bald Mami wird 🧸 Erstausstattung «Hello Little Bear», 5 Teile. Link in der Bio.
#erstausstattung #babygeschenk #neugeboren #babyschweiz #sunnozy

**hello_world_erstes_outfit**
Hello World ✨ Das erste Outfit für Dein Neugeborenes, 8 Teile. Link in der Bio.
#erstausstattung #hellobaby #neugeboren #babyschweiz #sunnozy

**teddy_babyfieber**
Wir haben gewarnt 🥹 Erstausstattung «Teddybär», 8 Teile. Link in der Bio.
#babyfieber #erstausstattung #neugeboren #babyschweiz #sunnozy

**dad_mom_bald_eltern**
Markier die zwei, die bald Mama und Papa werden 🤍 Bald bei uns.
#schwanger #babyliebe #erstausstattung #babyschweiz #sunnozy

**weltall_astronaut**
Kleiner Astronaut, grosse Liebe 🪐 Bald bei uns, folg uns, damit Du es nicht verpasst.
#babyboy #neugeboren #erstausstattung #babyschweiz #sunnozy

**teddy_rosa_gotti**
Gotti-Geschenk: erledigt 🎀 Schick das der Gotti, die noch sucht. Bald bei uns.
#gotti #babygeschenk #babygirl #babyschweiz #sunnozy

**prinzessin_grosi**
Für das Grosi, das schon jetzt alles verwöhnen will 👑 Bald bei uns.
#grosi #babygirl #babygeschenk #babyschweiz #sunnozy

**waldbaer_winterbaby**
Winterbabys sind die gemütlichsten 🌲 Bald bei uns.
#winterbaby #neugeboren #erstausstattung #babyschweiz #sunnozy

## Runde 2 (16 Reels)

| Reel | Clip | Hook | Endfolie |
|---|---|---|---|
| `reel_hello_world_werdende_mami_9x16.mp4` | `set_hello_world_blatt_baby_body_2` | Schick das der werdenden Mami in Deinem Leben ✨ | Hello World · Shop |
| `reel_teddy_grosi_erstes_mal_9x16.mp4` | `set_teddy_creme_baby_strampler_2` | POV: Das Grosi sieht ihn zum ersten Mal 🥹 | Teddybär · Shop |
| `reel_little_bear_strecken_9x16.mp4` | `set_little_bear_baby_strampler_1` (gleicher Clip wie Runde 1, Hook-Test) | Warnung: Dieses Strecken macht süchtig 🧸 | Hello Little Bear · Shop |
| `reel_dad_mom_werdender_papa_9x16.mp4` | `set_love_dad_mom_baby_body_1` | Schick das dem werdenden Papa 🤍 | coming soon |
| `reel_weltall_goetti_9x16.mp4` | `set_weltall_hellblau_baby_body_2` | POV: Du wirst Götti und suchst noch ein Geschenk 🪐 | coming soon |
| `reel_teddy_rosa_nicht_anschauen_9x16.mp4` | `set_teddy_rosa_punkte_baby_strampler_2` | Nicht anschauen, wenn Du kein Babyfieber willst 🎀 | coming soon |
| `reel_prinzessin_maedchen_9x16.mp4` | `set_prinzessin_krone_baby_body_2` | POV: Es wird ein Mädchen 👑 | coming soon |
| `reel_waldbaer_termin_winter_9x16.mp4` | `set_waldbaer_creme_baby_body_2` | Schick das Deiner Freundin mit Termin im Winter 🌲 | coming soon |
| `reel_bauernhof_morgens_9x16.mp4` | `set_bauernhof_baby_strampler_1` | POV: Morgens um 7 bei Euch zuhause ☀ | coming soon |
| `reel_bauernhof_schwester_9x16.mp4` | `set_bauernhof_baby_strampler_2` | Schick das Deiner Schwester, die bald Mami wird 🐄 | coming soon |
| `reel_wal_bub_9x16.mp4` | `set_wal_blau_baby_strampler_1` | POV: Es wird ein Bub 🐳 | coming soon |
| `reel_hase_rosa_beste_freundin_9x16.mp4` | `set_hase_rosa_baby_body_1` | POV: Deine beste Freundin schickt Dir das erste Foto 🐰 | coming soon |
| `reel_eisbaer_babyfieber_9x16.mp4` | `eisbaer-taupe_baby_v1-ohne-referenzlook_1` | Wer braucht noch einen Grund für Babyfieber? 🥹 | coming soon |
| `reel_eisbaer_januar_9x16.mp4` | `eisbaer-taupe_baby_v1-ohne-referenzlook_2` | Für das Baby, das im Januar kommt ❄ | coming soon |
| `reel_born_2027_markier_9x16.mp4` | `born-in-2027-rosa_baby_strampler_1` | Markier alle, die 2027 Mami werden 🎀 | coming soon |
| `reel_born_2027_weihnachten_9x16.mp4` | `born-in-2027-rosa_baby_strampler_3` | POV: Ihr sagt es der Familie an Weihnachten 🎄 | coming soon |

Nicht verwendet (Safe Sleep): Clips mit Plüschtier, Nuggi, Haarband, Lammfell oder Spielzeug beim Baby (u. a. `set_hello_world_creme_*`, `set_lila_hase_*`, `set_hund_creme_*`, `set_gaensebluemchen_*`, `blumen-musselin_*`, `little-bear-rosa_*`).

### Captions Runde 2 (kopierfertig)

**hello_world_werdende_mami**
Für die werdende Mami, die schon alles plant ✨ Erstausstattung «Hello World», 8 Teile. Link in der Bio.
#erstausstattung #schwanger #neugeboren #babyschweiz #sunnozy

**teddy_grosi_erstes_mal**
Der Moment, auf den das Grosi neun Monate gewartet hat 🥹 Erstausstattung «Teddybär», 8 Teile. Link in der Bio.
#grosi #erstausstattung #neugeboren #babyschweiz #sunnozy

**little_bear_strecken**
Einmal schauen reicht nicht 🧸 Erstausstattung «Hello Little Bear», 5 Teile. Link in der Bio.
#babyfieber #erstausstattung #neugeboren #babyschweiz #sunnozy

**dad_mom_werdender_papa**
Markier den Papa, der bald «I love Dad» trägt… also, sein Baby 🤍 Bald bei uns.
#werdenderpapa #schwanger #babygeschenk #babyschweiz #sunnozy

**weltall_goetti**
Götti-Geschenk gesucht? Gefunden 🪐 Bald bei uns, folg uns, damit Du es nicht verpasst.
#götti #babygeschenk #babyboy #babyschweiz #sunnozy

**teddy_rosa_nicht_anschauen**
Wir haben Dich gewarnt 🎀 Bald bei uns.
#babyfieber #babygirl #neugeboren #babyschweiz #sunnozy

**prinzessin_maedchen**
Es wird ein Mädchen 👑 Schick das der Mami, die es gerade erfahren hat. Bald bei uns.
#esisteinmaedchen #babygirl #schwanger #babyschweiz #sunnozy

**waldbaer_termin_winter**
Für alle Winterbabys und ihre Mamis 🌲 Bald bei uns.
#winterbaby #schwanger #neugeboren #babyschweiz #sunnozy

**bauernhof_morgens**
Der schönste Wecker der Welt ☀ Bald bei uns.
#babyliebe #neugeboren #erstausstattung #babyschweiz #sunnozy

**bauernhof_schwester**
Für die Schwester, die bald Mami wird 🐄 Markier sie. Bald bei uns.
#tante #babygeschenk #neugeboren #babyschweiz #sunnozy

**wal_bub**
Es wird ein Bub 🐳 Bald bei uns.
#esisteinbub #babyboy #schwanger #babyschweiz #sunnozy

**hase_rosa_beste_freundin**
Wenn Deine beste Freundin Dir das erste Foto schickt 🐰 Markier sie.
#bestefreundin #babygirl #neugeboren #babyschweiz #sunnozy

**eisbaer_babyfieber**
Babyfieber, Stufe 100 🥹 Bald bei uns.
#babyfieber #neugeboren #babyliebe #babyschweiz #sunnozy

**eisbaer_januar**
Für das Baby, das im Januar kommt ❄ Schick das der werdenden Mami. Bald bei uns.
#januarbaby #schwanger #erstausstattung #babyschweiz #sunnozy

**born_2027_markier**
Markier alle, die 2027 Mami werden 🎀 «Born in 2027» bald in Rosa und Hellblau.
#bornin2027 #schwanger #babyankündigung #babyschweiz #sunnozy

**born_2027_weihnachten**
Die schönste Weihnachtsüberraschung 🎄 «Born in 2027» bald in Rosa und Hellblau.
#bornin2027 #schwangerschaftsverkündung #weihnachten #babyschweiz #sunnozy

## Runde 3 (24 Reels, Safe Sleep hier nicht so wichtig)

Auf Wunsch der Nutzerin auch Clips mit Plüschtier, Nuggi oder Decke. **Diese nicht für Ads verwenden.**

| Reel | Clip | Hook | Endfolie |
|---|---|---|---|
| `reel_hello_world_creme_kuscheltier_9x16.mp4` | `set_hello_world_creme_baby_body_1` | POV: Das erste Kuscheltier ist schon ausgesucht 🐰 | Hello World · Creme · coming soon |
| `reel_hello_world_creme_zu_dritt_9x16.mp4` | `set_hello_world_creme_baby_body_2` | POV: Ihr seid zum ersten Mal zu dritt 🤍 | Hello World · Creme · coming soon |
| `reel_hund_hundemama_9x16.mp4` | `set_hund_creme_baby_body_1` | Schick das der Hundemama, die bald echte Mama wird 🐶 | I love Dogs · coming soon |
| `reel_hund_schlaeft_fast_9x16.mp4` | `set_hund_creme_baby_body_2` | POV: Er schläft endlich… fast 🧸 | I love Dogs · coming soon |
| `reel_lila_hase_suechtig_9x16.mp4` | `set_lila_hase_baby_body_1` | Warnung: Lila macht süchtig 💜 | Lila Hase «little and cute» · coming soon |
| `reel_lila_hase_freundin_9x16.mp4` | `set_lila_hase_baby_body_2` | Schick das Deiner Freundin, die Lila liebt 💜 | Lila Hase «little and cute» · coming soon |
| `reel_little_and_loved_erster_morgen_9x16.mp4` | `set_little_and_loved_gans_rosa_baby_body_1` | POV: Mamis Hand, Babys erster Morgen 🤍 | Little and Loved · Shop |
| `reel_little_and_loved_und_wie_9x16.mp4` | `set_little_and_loved_gans_rosa_baby_body_2` | Little and loved. Und wie 🥹 | Little and Loved · Shop |
| `reel_little_and_loved_gotti_set_9x16.mp4` | `set_little_and_loved_gans_rosa_baby_strampler_1` | POV: Die Gotti hat das Set ausgesucht 🎀 | Little and Loved · Shop |
| `reel_little_and_loved_markier_gotti_9x16.mp4` | `set_little_and_loved_gans_rosa_baby_strampler_2` | Markier die Gotti, die das schenkt 🎀 | Little and Loved · Shop |
| `reel_little_bear_guten_morgen_9x16.mp4` | `set_little_bear_baby_body_1` | POV: Sein allererstes «Guten Morgen» 🧸 | Hello Little Bear · Shop |
| `reel_little_bear_grosi_9x16.mp4` | `set_little_bear_baby_body_2` | Schick das dem Grosi, das schon fleissig strickt 🧸 | Hello Little Bear · Shop |
| `reel_prinzessin_freundin_maedchen_9x16.mp4` | `set_prinzessin_krone_baby_strampler_1` | Schick das der Freundin, die ein Mädchen erwartet 👑 | Little Princess · coming soon |
| `reel_princess_endlich_da_9x16.mp4` | `set_rosa_baby_strampler_1` | POV: Sie ist endlich da 🎀 | Princess · Shop |
| `reel_princess_gotti_gefuehle_9x16.mp4` | `set_rosa_baby_strampler_2` | Warnung: akute Gotti-Gefühle 🎀 | Princess · Shop |
| `reel_smile_erstes_laecheln_9x16.mp4` | `set_smile_gruen_baby_strampler_1` | POV: Sein erstes Lächeln 💚 | Smile · Salbeigrün · coming soon |
| `reel_teddy_body_name_9x16.mp4` | `set_teddy_creme_baby_body_1` | POV: Ihr habt den Namen schon 🧸 | Teddybär · Shop |
| `reel_teddy_rosa_fuesschen_9x16.mp4` | `set_teddy_rosa_punkte_baby_body_1` | Warnung: diese Füsschen 🥹 | Teddy Rosa · coming soon |
| `reel_wal_matrose_9x16.mp4` | `set_wal_blau_baby_body_1` | POV: Dein kleiner Matrose ist an Bord 🐳 | Wal «Sea vibes» · coming soon |
| `reel_weltall_gute_nacht_9x16.mp4` | `set_weltall_hellblau_baby_strampler_1` | Gute Nacht, kleiner Astronaut 🌙 | Little One · Weltall · coming soon |
| `reel_gaensebluemchen_sie_ist_da_9x16.mp4` | `set_gaensebluemchen_baby_strampler_1` | POV: Es ist ein Mädchen. Und sie ist da 🌼 | «It's a baby girl» · coming soon |
| `reel_hase_rosa_erster_tag_9x16.mp4` | `set_hase_rosa_baby_strampler_1` | POV: Mamis Hände, Babys erster Tag 🐰 | Hase Rosa «Little one» · coming soon |
| `reel_hello_rosa_freundin_9x16.mp4` | `set_hello_schmetterling_baby_body_1` | Schick das Deiner Freundin, die Rosa liebt 🦋 | Hello · Shop |
| `reel_waldbaer_ist_da_9x16.mp4` | `set_waldbaer_creme_baby_strampler_1` | POV: Euer kleiner Waldbär ist da 🌲 | Waldbär · coming soon |

### Captions Runde 3 (kopierfertig)

**hello_world_creme_kuscheltier**
Alles bereit, fehlt nur noch das Baby 🐰 Bald bei uns.
#erstausstattung #schwanger #neugeboren #babyschweiz #sunnozy

**hello_world_creme_zu_dritt**
Zum ersten Mal zu dritt 🤍 Markier Deinen Schatz. Bald bei uns.
#elternwerden #neugeboren #babyliebe #babyschweiz #sunnozy

**hund_hundemama**
Erst Hundemama, bald Mama 🐶 Markier sie. Bald bei uns.
#hundemama #schwanger #babygeschenk #babyschweiz #sunnozy

**hund_schlaeft_fast**
Fast… 🧸 Bald bei uns.
#babyalltag #neugeboren #babyliebe #babyschweiz #sunnozy

**lila_hase_suechtig**
Lila geht immer 💜 Bald bei uns.
#babygirl #neugeboren #babyfieber #babyschweiz #sunnozy

**lila_hase_freundin**
Für die Freundin, die alles in Lila will 💜 Markier sie. Bald bei uns.
#babygirl #babygeschenk #schwanger #babyschweiz #sunnozy

**little_and_loved_erster_morgen**
Der erste Morgen zu Hause 🤍 Erstausstattung «Little and Loved», 8 Teile. Link in der Bio.
#erstausstattung #neugeboren #babygirl #babyschweiz #sunnozy

**little_and_loved_und_wie**
Little and loved. Und wie 🥹 Erstausstattung, 8 Teile. Link in der Bio.
#erstausstattung #babyfieber #babygirl #babyschweiz #sunnozy

**little_and_loved_gotti_set**
Gotti-Geschenk mit 8 Teilen 🎀 «Little and Loved». Link in der Bio.
#gotti #babygeschenk #erstausstattung #babyschweiz #sunnozy

**little_and_loved_markier_gotti**
Markier die Gotti, die das schenken soll 🎀 Link in der Bio.
#gotti #babygeschenk #babygirl #babyschweiz #sunnozy

**little_bear_guten_morgen**
Guten Morgen, kleiner Bär 🧸 Erstausstattung «Hello Little Bear», 5 Teile. Link in der Bio.
#erstausstattung #neugeboren #babyliebe #babyschweiz #sunnozy

**little_bear_grosi**
Fürs Grosi, das schon alles vorbereitet 🧸 «Hello Little Bear», 5 Teile. Link in der Bio.
#grosi #babygeschenk #erstausstattung #babyschweiz #sunnozy

**prinzessin_freundin_maedchen**
Für die Freundin, die ein Mädchen erwartet 👑 Markier sie. Bald bei uns.
#esisteinmaedchen #babygirl #schwanger #babyschweiz #sunnozy

**princess_endlich_da**
Sie ist endlich da 🎀 Erstausstattung «Princess», 8 Teile. Link in der Bio.
#babygirl #erstausstattung #neugeboren #babyschweiz #sunnozy

**princess_gotti_gefuehle**
Gotti-Gefühle garantiert 🎀 «Princess», 8 Teile. Link in der Bio.
#gotti #babygirl #babygeschenk #babyschweiz #sunnozy

**smile_erstes_laecheln**
Das erste Lächeln 💚 Bald bei uns.
#neugeboren #babyliebe #babyboy #babyschweiz #sunnozy

**teddy_body_name**
Name steht, Outfit auch 🧸 Erstausstattung «Teddybär», 8 Teile. Link in der Bio.
#erstausstattung #schwanger #neugeboren #babyschweiz #sunnozy

**teddy_rosa_fuesschen**
Diese Füsschen 🥹 Bald bei uns.
#babyfieber #babygirl #neugeboren #babyschweiz #sunnozy

**wal_matrose**
Kleiner Matrose an Bord 🐳 Bald bei uns.
#babyboy #neugeboren #babygeschenk #babyschweiz #sunnozy

**weltall_gute_nacht**
Gute Nacht, kleiner Astronaut 🌙 Bald bei uns.
#babyboy #neugeboren #babyliebe #babyschweiz #sunnozy

**gaensebluemchen_sie_ist_da**
Es ist ein Mädchen 🌼 Schick das der frischgebackenen Mami. Bald bei uns.
#esisteinmaedchen #babygirl #neugeboren #babyschweiz #sunnozy

**hase_rosa_erster_tag**
Der erste Tag 🐰 Bald bei uns.
#neugeboren #babygirl #babyliebe #babyschweiz #sunnozy

**hello_rosa_freundin**
Für die Freundin, die Rosa liebt 🦋 Erstausstattung «Hello», 6 Teile. Link in der Bio.
#babygirl #erstausstattung #babygeschenk #babyschweiz #sunnozy

**waldbaer_ist_da**
Euer kleiner Waldbär ist da 🌲 Bald bei uns.
#neugeboren #babyboy #winterbaby #babyschweiz #sunnozy


## Runde 4 (18 Reels aus `baby-videos/runde5`, Stil v2)

Wache, lachende Babys und Babys im Arm. Boxen-Reels mit Endfolie zur Weihnachtsbox (Shop, ohne Preis im Video).

| Reel | Clip | Hook | Endfolie |
|---|---|---|---|
| `reel_r5_smile_mamis_stimme_9x16.mp4` | `runde5/06_smile_weinrot` | POV: Er hört Mamis Stimme zum ersten Mal 🥹 | Strampler «Smile» und «Kirschen» · coming soon |
| `reel_r5_kirschen_freundin_9x16.mp4` | `runde5/37_kirschen_weiss` | Schick das der Freundin, die Kirschen liebt 🍒 | Strampler «Kirschen» · coming soon |
| `reel_r5_teddy_lacht_an_9x16.mp4` | `runde5/07_teddy_body_ringelarm` | POV: Er lacht Dich zum ersten Mal an 🧸 | Teddybär · Shop |
| `reel_r5_happy_baby_lachen_9x16.mp4` | `runde5/08_happy_baby` | Warnung: Dieses Lachen ist ansteckend 😄 | Bauernhof «Happy Baby» · coming soon |
| `reel_r5_happy_baby_tante_9x16.mp4` | `runde5/25_happy_baby_b` | POV: Du bist Tante und er lacht Dich an 🤍 | Bauernhof «Happy Baby» · coming soon |
| `reel_r5_kapuzentuch_erstes_bad_9x16.mp4` | `runde5/17_kapuzentuch_happy_baby` | POV: Das erste Bad ist geschafft 🛁 | Bauernhof «Happy Baby» · coming soon |
| `reel_r5_best_family_seid_ihr_9x16.mp4` | `runde5/16_best_family` | POV: Ihr seid jetzt die «Best Family» 🤍 | «Best Family» Teddy · coming soon |
| `reel_r5_best_family_lachen_9x16.mp4` | `runde5/20_best_family_lachen` | Wer kann da noch schlecht drauf sein? 🥹 | «Best Family» Teddy · coming soon |
| `reel_r5_best_family_eingekuschelt_9x16.mp4` | `runde5/18_kapuzentuch_best_family` | POV: Frisch gebadet und eingekuschelt 🧸 | «Best Family» Teddy · coming soon |
| `reel_r5_baerenmuetze_papa_9x16.mp4` | `runde5/23_creme_baerenmuetze_arm` | Schick das dem Papa, der Bären liebt 🐻 | Knotenmützen «Bär» · coming soon |
| `reel_r5_born_2027_blau_9x16.mp4` | `runde5/35_born_in_2027_blau` | POV: Er kommt 2027 und hat schon sein Outfit 💙 | Born in 2027 · Hellblau · coming soon |
| `reel_r5_smile_happy_9x16.mp4` | `runde5/36_smile_salbeigruen` | Schick das der Person, die Dich happy macht 💚 | «You make me happy» · coming soon |
| `reel_r5_dad_mom_prinzessin_9x16.mp4` | `runde5/24_little_princess_dad_mom_hase` | Schick das Mama und Papa der kleinen Prinzessin 🤍 | I love Dad Mom · coming soon |
| `reel_r5_box_dinosaur_grosi_9x16.mp4` | `runde5/27_box_dinosaur_body_arm` | POV: Grosi hat ihn endlich im Arm 🦖 | Box «Dinosaur» · Shop |
| `reel_r5_box_growing_goetti_9x16.mp4` | `runde5/29_box_growing_up_strong_body_D` | POV: Götti schenkt dieses Jahr Bodys 🎁 | Box «Growing up strong» · Shop |
| `reel_r5_box_lovely_gotti_9x16.mp4` | `runde5/32_box_lovely_body_arm` | POV: Ihr erstes Weihnachten, Gotti hat vorgesorgt 🎁 | Box «Lovely Little Girl» · Shop |
| `reel_r5_box_mummy_9x16.mp4` | `runde5/33_box_mummy_halstuch_arm` | Schick das der Mami vor ihrem 1. Weihnachten 🎄 | Box «I love my Mummy» · Shop |
| `reel_r5_box_dino_opa_9x16.mp4` | `runde5/40_box_dino_body` | POV: Opa hat den kleinen Dino entdeckt 🦕 | Box «Dino» · Shop |

### Captions Runde 4 (kopierfertig)

**r5_smile_mamis_stimme**
Dieser Blick, wenn er Mamis Stimme hört 🥹 Bald bei uns.
#neugeboren #babyliebe #mamasein #babyschweiz #sunnozy

**r5_kirschen_freundin**
Für die Freundin, die Kirschen liebt 🍒 Markier sie. Bald bei uns.
#babygirl #babygeschenk #neugeboren #babyschweiz #sunnozy

**r5_teddy_lacht_an**
Das erste Lachen 🧸 Erstausstattung «Teddybär», 8 Teile. Link in der Bio.
#erstausstattung #babylachen #neugeboren #babyschweiz #sunnozy

**r5_happy_baby_lachen**
Versuch, nicht mitzulachen 😄 Bald bei uns.
#babylachen #happybaby #babyliebe #babyschweiz #sunnozy

**r5_happy_baby_tante**
Tante sein ist das Beste 🤍 Schick das Deiner Schwester. Bald bei uns.
#tante #babyliebe #babygeschenk #babyschweiz #sunnozy

**r5_kapuzentuch_erstes_bad**
Erstes Bad geschafft 🛁 Kapuzentuch im gleichen Muster. Bald bei uns.
#erstesbad #neugeboren #babypflege #babyschweiz #sunnozy

**r5_best_family_seid_ihr**
Jetzt seid Ihr die Best Family 🤍 Markier Deinen Schatz. Bald bei uns.
#bestfamily #elternwerden #babyliebe #babyschweiz #sunnozy

**r5_best_family_lachen**
Gute Laune garantiert 🥹 Bald bei uns.
#babylachen #neugeboren #babyliebe #babyschweiz #sunnozy

**r5_best_family_eingekuschelt**
Frisch gebadet und eingekuschelt 🧸 Bald bei uns.
#neugeboren #kuschelzeit #babypflege #babyschweiz #sunnozy

**r5_baerenmuetze_papa**
Für den Papa, der Bären liebt 🐻 Markier ihn. Bald bei uns.
#papawerden #babymuetze #neugeboren #babyschweiz #sunnozy

**r5_born_2027_blau**
Er kommt 2027 💙 «Born in 2027» bald in Hellblau und Rosa.
#bornin2027 #babyboy #schwanger #babyschweiz #sunnozy

**r5_smile_happy**
Schick das der Person, die Dich happy macht 💚 Bald bei uns.
#youmakemehappy #babyliebe #neugeboren #babyschweiz #sunnozy

**r5_dad_mom_prinzessin**
Für Mama und Papa der kleinen Prinzessin 🤍 Bald bei uns.
#elternwerden #babygirl #babygeschenk #babyschweiz #sunnozy

**r5_box_dinosaur_grosi**
Grosi-Moment 🦖 Weihnachtsbox «Dinosaur»: 5 Bodys + 5 Hosen, fertig verpackt. Link in der Bio.
#weihnachtsgeschenk #grosi #babygeschenk #babyschweiz #sunnozy

**r5_box_growing_goetti**
Götti-Geschenk erledigt 🎁 Box «Growing up strong»: 5 Bodys + 5 Hosen. Link in der Bio.
#götti #weihnachtsgeschenk #babygeschenk #babyschweiz #sunnozy

**r5_box_lovely_gotti**
Ihr erstes Weihnachten 🎁 Box «Lovely Little Girl»: 3 Bodys + 5 Leggings. Link in der Bio.
#gotti #weihnachtsgeschenk #babygirl #babyschweiz #sunnozy

**r5_box_mummy**
Für Mamis erstes Weihnachten mit Baby 🎄 Box «I love my Mummy»: 3 Bodys + 3 Halstücher. Link in der Bio.
#erstesweihnachten #mamasein #babygeschenk #babyschweiz #sunnozy

**r5_box_dino_opa**
Opa hat den kleinen Dino entdeckt 🦕 Box «Dino»: 3 Bodys + 3 Mulltücher. Link in der Bio.
#opa #weihnachtsgeschenk #babygeschenk #babyschweiz #sunnozy

### Mix-Reels neu (18.11.2026)

| Reel | Hook | Caption |
|---|---|---|
| `mix/reel_mix_welches_lachen_9x16.mp4` | Welches Lachen ist am süssesten? 🥹 (1–4) | Schreib die Nummer 🥹 Schick das jemandem, der heute ein Lachen braucht. #babylachen #neugeboren #babyliebe #babyschweiz #sunnozy |
| `mix/reel_mix_welche_box_fuer_wen_9x16.mp4` | Welche Weihnachtsbox für welches Baby? 🎁 (1–4) | 1, 2, 3 oder 4? Schreib die Nummer, wir schicken Dir den Link 🎁 #weihnachtsgeschenk #babygeschenk #gotti #babyschweiz #sunnozy |

Nummern in den Mix-Reels jetzt auf dunklem Kreis (besser lesbar).

### Kombi-Reels (18.11.2026, Mittag)

Clips aus verschiedenen Videos kombiniert, mit Label je Clip (dunkle Pille unten) statt Nummer. Labels nennen die Person oder Farbe → Kommentare und Markieren.

| Reel | Hook | Aufbau | Caption |
|---|---|---|---|
| `mix/reel_mix_box_fuer_wen_9x16.mp4` | Welche Box für wen? 🎁 | 5 Boxen: fürs Grosi, vom Götti, von der Gotti, für Mami, vom Opa | Wer schenkt bei Euch welche Box? 🎁 Markier sie. Link in der Bio. #weihnachtsgeschenk #babygeschenk #gotti #babyschweiz #sunnozy |
| `mix/reel_mix_bub_oder_maedchen_9x16.mp4` | Bub oder Mädchen? Schreib es uns 🤍 | Bub / Mädchen im Wechsel | Bub oder Mädchen? Schreib es in die Kommentare 🤍 #schwanger #genderreveal #babyboy #babygirl #sunnozy |
| `mix/reel_mix_erst_baden_dann_happy_9x16.mp4` | Erst baden, dann happy 😄 | Bauernhof: Kapuzentuch → Body → Lachen | Erst baden, dann happy 😄 Bauernhof-Set mit Kapuzentuch, bald bei uns. #erstesbad #happybaby #neugeboren #babyschweiz #sunnozy |
| `mix/reel_mix_best_family_tag_9x16.mp4` | Ein Morgen mit der «Best Family» 🧸 | Kapuzentuch → Body und Mütze → Lachen | Ein Morgen mit der Best Family 🧸 Bald bei uns. #bestfamily #babyliebe #neugeboren #babyschweiz #sunnozy |
| `mix/reel_mix_lachen_kompilation_9x16.mp4` | Schick das jemandem, der heute lachen muss 😄 | 5× Babylachen | Schick das jemandem, der heute ein Lachen braucht 😄 #babylachen #gutelaune #neugeboren #babyschweiz #sunnozy |
| `mix/reel_mix_welche_farbe_9x16.mp4` | Welche Farbe für Euer Baby? 🎨 | Rosa, Lila, Hellblau, Salbeigrün, Creme | Welche Farbe nimmst Du? Schreib sie in die Kommentare 🎨 #erstausstattung #babymode #neugeboren #babyschweiz #sunnozy |
| `mix/reel_mix_gotti_oder_goetti_9x16.mp4` | Gotti oder Götti: wer schenkt was? 🎁 | Gotti / Götti im Wechsel | Markier Gotti und Götti 🎁 #gotti #götti #babygeschenk #babyschweiz #sunnozy |
| `mix/reel_mix_erstes_weihnachten_9x16.mp4` | Babys erstes Weihnachten kommt näher 🎄 | 4 Weihnachtsbox-Babys | Das erste Weihnachten mit Baby 🎄 Weihnachtsboxen fertig verpackt. Link in der Bio. #erstesweihnachten #weihnachtsgeschenk #babygeschenk #babyschweiz #sunnozy |
| `mix/reel_mix_tante_markieren_9x16.mp4` | Markier die Tante, die das schenken soll 🎀 | 4 Mädchen-Sets, Nummern 1–4 | Markier die Tante und schreib die Nummer 🎀 #tante #babygeschenk #babygirl #babyschweiz #sunnozy |

## Vor dem Posten

- «Mit KI erstellt» einschalten
- Prints im Video mit dem echten Set vergleichen
- Eigenen Kommentar anpinnen (z. B. «Nach dem Video will das ganze Team ein Baby 🥹») und in der ersten Stunde alle Kommentare beantworten
- Coming-soon-Reels: kein Preis, auch nicht in der Caption
