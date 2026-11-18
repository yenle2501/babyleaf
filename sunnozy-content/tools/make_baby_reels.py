"""Baby-Reels aus den Grok-Strecken-Clips vom 17.11.2026 (posts/baby-videos/set_*_1.mp4 …).

Muster aus der Viral-Analyse (babyothelabel, avalia.kids, zayac_mehovoi):
  - Neugeborenes streckt sich (zayac, 2.8 Mio. Views), ein Take, kaum Kamerabewegung
  - Text-Hook ab dem ersten Bild: POV / Warnung / Schick das …, max. ~8 Wörter
  - ein klarer Empfänger zum Teilen (Gotti, Grosi, Freundin, Partner)
  - unter 12 s, Text kommt am Ende zurück, damit der Loop sauber wirkt
Stil wie tools/make_reel_hello_little_bear_hook.py: weisse Schreibmaschinenschrift (Courier Prime) mit Emoji, Video in voller
Grösse. Text steht oben im Bild über dem Kopf des Babys, damit Gesicht und Print frei bleiben.
Bearbeitung: leicht entrauscht, etwas wärmer, nachgeschärft (wie die `_bearbeitet`-Clips). Musik: Standard-Track Alex Morgan.
Endfolie: tools/endfolie.py (Set-Bild, Name, Zeile, Aufruf, Logo). Kein Preis.

Bearbeitung v2 (18.11.2026, nach Hook-Recherche Instagram 2026): Skip-Rate in den ersten 1–3 s entscheidet, DM-Shares sind
das wichtigste Signal, erstes Bild braucht sichtbare Bewegung, Text in 0.5 s da, oberes Drittel, Loop.
  - Start erst bei 0.8 s: Grok-Clips beginnen mit dem stehenden Foto, so ist ab Bild 1 Bewegung drin
  - Punch-in-Zoom 112 % → 100 % in den ersten 0.5 s
  - Hook tippt sich in 0.5 s ein (Schreibmaschine), am Loop-Ende steht er sofort ganz da

Runde 1+2 nur Clips ohne Plüschtier, Nuggi und lose Decke (Safe Sleep). Runde 3 auch solche Clips, auf Wunsch der Nutzerin.

    python3 tools/make_baby_reels.py [name ...]
Ausgabe: posts/baby-reels/reel_<name>_9x16.mp4 + _titelbild.jpg, Captions in posts/baby-reels/README.md
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
from endfolie import anhaengen, SET, CS, SHOP, CS_AUFRUF

W, H, FPS = m.W, m.H, 30
VID = os.path.join(m.POSTS, 'baby-videos')
OUT = os.path.join(m.POSTS, 'baby-reels')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
VON, DAUER = 0.8, 9.2
ZOOM_BIS, TIPP_BIS = 0.5, 0.5
TEXT_BIS, LOOP_AB = 3.0, 8.0
TEXT_Y = 250
GRADE = 'hqdn3d=1.5:1.5:4:4,eq=contrast=1.04:saturation=1.04:gamma=1.01,colorbalance=rs=0.02:bs=-0.02:rm=0.015:bm=-0.015,cas=0.35'

# name: (clip, zeilen, emoji, (set_bild, set_name, zeile, aufruf))
REELS = {
    'little_bear_freundin': ('set_little_bear_baby_strampler_1.mp4', ['Schick das Deiner Freundin,', 'die bald Mami wird'], '🧸',
                             (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile', SHOP)),
    'hello_world_erstes_outfit': ('set_hello_world_blatt_baby_body_1.mp4', ['POV: Sein allererstes Outfit', 'sagt «Hello World»'], '✨',
                                  (SET + '/set_hello_world_blatt_quadratisch.jpg', 'Hello World', 'Erstausstattung · 8 Teile', SHOP)),
    'teddy_babyfieber': ('set_teddy_creme_baby_strampler_1.mp4', ['Warnung:', 'Babyfieber-Gefahr'], '🥹',
                         (SET + '/set_teddy_creme_quadratisch.jpg', 'Teddybär', 'Erstausstattung · 8 Teile', SHOP)),
    'dad_mom_bald_eltern': ('set_love_dad_mom_baby_body_2.mp4', ['POV: In ein paar Wochen', 'seid Ihr Mama und Papa'], '🤍',
                            (SET + '/set_love_dad_mom_quadratisch.jpg', 'I love Dad Mom', 'coming soon', CS_AUFRUF)),
    'weltall_astronaut': ('set_weltall_hellblau_baby_body_1.mp4', ['POV: Euer kleiner Astronaut', 'ist gelandet'], '🪐',
                          (SET + '/set_weltall_hellblau_quadratisch.jpg', 'Little One · Weltall', 'coming soon', CS_AUFRUF)),
    'teddy_rosa_gotti': ('set_teddy_rosa_punkte_baby_strampler_1.mp4', ['POV: Du wirst Gotti', 'und das Geschenk ist klar'], '🎀',
                         (SET + '/set_teddy_rosa_punkte_quadratisch.jpg', 'Teddy Rosa', 'coming soon', CS_AUFRUF)),
    'prinzessin_grosi': ('set_prinzessin_krone_baby_body_1.mp4', ['Schick das dem Grosi', 'der kleinen Prinzessin'], '👑',
                         (SET + '/set_prinzessin_krone_quadratisch.jpg', 'Little Princess', 'coming soon', CS_AUFRUF)),
    'waldbaer_winterbaby': ('set_waldbaer_creme_baby_body_1.mp4', ['POV: Dein Baby', 'kommt im Winter'], '🌲',
                            (SET + '/set_waldbaer_creme_quadratisch.jpg', 'Waldbär', 'coming soon', CS_AUFRUF)),
    # Runde 2 (17.11.2026, abends)
    'hello_world_werdende_mami': ('set_hello_world_blatt_baby_body_2.mp4', ['Schick das der werdenden', 'Mami in Deinem Leben'], '✨',
                                  (SET + '/set_hello_world_blatt_quadratisch.jpg', 'Hello World', 'Erstausstattung · 8 Teile', SHOP)),
    'teddy_grosi_erstes_mal': ('set_teddy_creme_baby_strampler_2.mp4', ['POV: Das Grosi sieht ihn', 'zum ersten Mal'], '🥹',
                               (SET + '/set_teddy_creme_quadratisch.jpg', 'Teddybär', 'Erstausstattung · 8 Teile', SHOP)),
    'little_bear_strecken': ('set_little_bear_baby_strampler_1.mp4', ['Warnung: Dieses Strecken', 'macht süchtig'], '🧸',
                             (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile', SHOP)),
    'dad_mom_werdender_papa': ('set_love_dad_mom_baby_body_1.mp4', ['Schick das dem', 'werdenden Papa'], '🤍',
                               (SET + '/set_love_dad_mom_quadratisch.jpg', 'I love Dad Mom', 'coming soon', CS_AUFRUF)),
    'weltall_goetti': ('set_weltall_hellblau_baby_body_2.mp4', ['POV: Du wirst Götti', 'und suchst noch ein Geschenk'], '🪐',
                       (SET + '/set_weltall_hellblau_quadratisch.jpg', 'Little One · Weltall', 'coming soon', CS_AUFRUF)),
    'teddy_rosa_nicht_anschauen': ('set_teddy_rosa_punkte_baby_strampler_2.mp4', ['Nicht anschauen, wenn Du', 'kein Babyfieber willst'], '🎀',
                                   (SET + '/set_teddy_rosa_punkte_quadratisch.jpg', 'Teddy Rosa', 'coming soon', CS_AUFRUF)),
    'prinzessin_maedchen': ('set_prinzessin_krone_baby_body_2.mp4', ['POV: Es wird', 'ein Mädchen'], '👑',
                            (SET + '/set_prinzessin_krone_quadratisch.jpg', 'Little Princess', 'coming soon', CS_AUFRUF)),
    'waldbaer_termin_winter': ('set_waldbaer_creme_baby_body_2.mp4', ['Schick das Deiner Freundin', 'mit Termin im Winter'], '🌲',
                               (SET + '/set_waldbaer_creme_quadratisch.jpg', 'Waldbär', 'coming soon', CS_AUFRUF)),
    'bauernhof_morgens': ('set_bauernhof_baby_strampler_1.mp4', ['POV: Morgens um 7', 'bei Euch zuhause'], '☀',
                          (SET + '/set_bauernhof_quadratisch.jpg', 'Bauernhof «Happy Baby»', 'coming soon', CS_AUFRUF)),
    'bauernhof_schwester': ('set_bauernhof_baby_strampler_2.mp4', ['Schick das Deiner Schwester,', 'die bald Mami wird'], '🐄',
                            (SET + '/set_bauernhof_quadratisch.jpg', 'Bauernhof «Happy Baby»', 'coming soon', CS_AUFRUF)),
    'wal_bub': ('set_wal_blau_baby_strampler_1.mp4', ['POV: Es wird', 'ein Bub'], '🐳',
                (SET + '/set_wal_blau_quadratisch.jpg', 'Wal «Sea vibes»', 'coming soon', CS_AUFRUF)),
    'hase_rosa_beste_freundin': ('set_hase_rosa_baby_body_1.mp4', ['POV: Deine beste Freundin', 'schickt Dir das erste Foto'], '🐰',
                                 (SET + '/set_hase_rosa_quadratisch.jpg', 'Hase Rosa «Little one»', 'coming soon', CS_AUFRUF)),
    'eisbaer_babyfieber': ('eisbaer-taupe_baby_v1-ohne-referenzlook_1.mp4', ['Wer braucht noch einen', 'Grund für Babyfieber?'], '🥹',
                           ((CS + '/eisbaer-taupe/shop/eisbaer-taupe_shop_ohne_logo.jpg'), 'Eisbär Taupe', 'coming soon', CS_AUFRUF)),
    'eisbaer_januar': ('eisbaer-taupe_baby_v1-ohne-referenzlook_2.mp4', ['Für das Baby,', 'das im Januar kommt'], '❄',
                       ((CS + '/eisbaer-taupe/shop/eisbaer-taupe_shop_ohne_logo.jpg'), 'Eisbär Taupe', 'coming soon', CS_AUFRUF)),
    'born_2027_markier': ('born-in-2027-rosa_baby_strampler_1.mp4', ['Markier alle,', 'die 2027 Mami werden'], '🎀',
                          ((CS + '/born-in-2027-rosa/shop/born-in-2027-rosa_shop_ohne_logo.jpg'), 'Born in 2027', 'coming soon · Rosa und Hellblau', CS_AUFRUF)),
    'born_2027_weihnachten': ('born-in-2027-rosa_baby_strampler_3.mp4', ['POV: Ihr sagt es der Familie', 'an Weihnachten'], '🎄',
                              ((CS + '/born-in-2027-rosa/shop/born-in-2027-rosa_shop_ohne_logo.jpg'), 'Born in 2027', 'coming soon · Rosa und Hellblau', CS_AUFRUF)),
    # Runde 3 (17.11.2026, spät): Safe Sleep laut Nutzerin hier nicht so wichtig, auch Clips mit Plüschtier/Nuggi/Decke
    'hello_world_creme_kuscheltier': ('set_hello_world_creme_baby_body_1.mp4', ['POV: Das erste Kuscheltier', 'ist schon ausgesucht'], '🐰',
        (SET + '/set_hello_world_creme_quadratisch.jpg', 'Hello World · Creme', 'coming soon', CS_AUFRUF)),
    'hello_world_creme_zu_dritt': ('set_hello_world_creme_baby_body_2.mp4', ['POV: Ihr seid', 'zum ersten Mal zu dritt'], '🤍',
        (SET + '/set_hello_world_creme_quadratisch.jpg', 'Hello World · Creme', 'coming soon', CS_AUFRUF)),
    'hund_hundemama': ('set_hund_creme_baby_body_1.mp4', ['Schick das der Hundemama,', 'die bald echte Mama wird'], '🐶',
        (SET + '/set_hund_creme_quadratisch.jpg', 'I love Dogs', 'coming soon', CS_AUFRUF)),
    'hund_schlaeft_fast': ('set_hund_creme_baby_body_2.mp4', ['POV: Er schläft endlich…', 'fast'], '🧸',
        (SET + '/set_hund_creme_quadratisch.jpg', 'I love Dogs', 'coming soon', CS_AUFRUF)),
    'lila_hase_suechtig': ('set_lila_hase_baby_body_1.mp4', ['Warnung:', 'Lila macht süchtig'], '💜',
        (SET + '/set_lila_hase_quadratisch.jpg', 'Lila Hase «little and cute»', 'coming soon', CS_AUFRUF)),
    'lila_hase_freundin': ('set_lila_hase_baby_body_2.mp4', ['Schick das Deiner Freundin,', 'die Lila liebt'], '💜',
        (SET + '/set_lila_hase_quadratisch.jpg', 'Lila Hase «little and cute»', 'coming soon', CS_AUFRUF)),
    'little_and_loved_erster_morgen': ('set_little_and_loved_gans_rosa_baby_body_1.mp4', ['POV: Mamis Hand,', 'Babys erster Morgen'], '🤍',
        (SET + '/set_little_and_loved_gans_rosa_quadratisch.jpg', 'Little and Loved', 'Erstausstattung · 8 Teile', SHOP)),
    'little_and_loved_und_wie': ('set_little_and_loved_gans_rosa_baby_body_2.mp4', ['Little and loved.', 'Und wie'], '🥹',
        (SET + '/set_little_and_loved_gans_rosa_quadratisch.jpg', 'Little and Loved', 'Erstausstattung · 8 Teile', SHOP)),
    'little_and_loved_gotti_set': ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', ['POV: Die Gotti hat', 'das Set ausgesucht'], '🎀',
        (SET + '/set_little_and_loved_gans_rosa_quadratisch.jpg', 'Little and Loved', 'Erstausstattung · 8 Teile', SHOP)),
    'little_and_loved_markier_gotti': ('set_little_and_loved_gans_rosa_baby_strampler_2.mp4', ['Markier die Gotti,', 'die das schenkt'], '🎀',
        (SET + '/set_little_and_loved_gans_rosa_quadratisch.jpg', 'Little and Loved', 'Erstausstattung · 8 Teile', SHOP)),
    'little_bear_guten_morgen': ('set_little_bear_baby_body_1.mp4', ['POV: Sein allererstes', '«Guten Morgen»'], '🧸',
        (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile', SHOP)),
    'little_bear_grosi': ('set_little_bear_baby_body_2.mp4', ['Schick das dem Grosi,', 'das schon fleissig strickt'], '🧸',
        (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile', SHOP)),
    'prinzessin_freundin_maedchen': ('set_prinzessin_krone_baby_strampler_1.mp4', ['Schick das der Freundin,', 'die ein Mädchen erwartet'], '👑',
        (SET + '/set_prinzessin_krone_quadratisch.jpg', 'Little Princess', 'coming soon', CS_AUFRUF)),
    'princess_endlich_da': ('set_rosa_baby_strampler_1.mp4', ['POV: Sie ist', 'endlich da'], '🎀',
        (SET + '/set_rosa_quadratisch.jpg', 'Princess', 'Erstausstattung · 8 Teile', SHOP)),
    'princess_gotti_gefuehle': ('set_rosa_baby_strampler_2.mp4', ['Warnung:', 'akute Gotti-Gefühle'], '🎀',
        (SET + '/set_rosa_quadratisch.jpg', 'Princess', 'Erstausstattung · 8 Teile', SHOP)),
    'smile_erstes_laecheln': ('set_smile_gruen_baby_strampler_1.mp4', ['POV: Sein erstes', 'Lächeln'], '💚',
        (SET + '/set_smile_gruen_quadratisch.jpg', 'Smile · Salbeigrün', 'coming soon', CS_AUFRUF)),
    'teddy_body_name': ('set_teddy_creme_baby_body_1.mp4', ['POV: Ihr habt', 'den Namen schon'], '🧸',
        (SET + '/set_teddy_creme_quadratisch.jpg', 'Teddybär', 'Erstausstattung · 8 Teile', SHOP)),
    'teddy_rosa_fuesschen': ('set_teddy_rosa_punkte_baby_body_1.mp4', ['Warnung:', 'diese Füsschen'], '🥹',
        (SET + '/set_teddy_rosa_punkte_quadratisch.jpg', 'Teddy Rosa', 'coming soon', CS_AUFRUF)),
    'wal_matrose': ('set_wal_blau_baby_body_1.mp4', ['POV: Dein kleiner Matrose', 'ist an Bord'], '🐳',
        (SET + '/set_wal_blau_quadratisch.jpg', 'Wal «Sea vibes»', 'coming soon', CS_AUFRUF)),
    'weltall_gute_nacht': ('set_weltall_hellblau_baby_strampler_1.mp4', ['Gute Nacht,', 'kleiner Astronaut'], '🌙',
        (SET + '/set_weltall_hellblau_quadratisch.jpg', 'Little One · Weltall', 'coming soon', CS_AUFRUF)),
    'gaensebluemchen_sie_ist_da': ('set_gaensebluemchen_baby_strampler_1.mp4', ['POV: Es ist ein Mädchen.', 'Und sie ist da'], '🌼',
        (SET + '/set_gaensebluemchen_quadratisch.jpg', "«It's a baby girl»", 'coming soon', CS_AUFRUF)),
    'hase_rosa_erster_tag': ('set_hase_rosa_baby_strampler_1.mp4', ['POV: Mamis Hände,', 'Babys erster Tag'], '🐰',
        (SET + '/set_hase_rosa_quadratisch.jpg', 'Hase Rosa «Little one»', 'coming soon', CS_AUFRUF)),
    'hello_rosa_freundin': ('set_hello_schmetterling_baby_body_1.mp4', ['Schick das Deiner Freundin,', 'die Rosa liebt'], '🦋',
        (SET + '/set_hello_schmetterling_quadratisch.jpg', 'Hello', 'Erstausstattung · 6 Teile', SHOP)),
    'waldbaer_ist_da': ('set_waldbaer_creme_baby_strampler_1.mp4', ['POV: Euer kleiner Waldbär', 'ist da'], '🌲',
        (SET + '/set_waldbaer_creme_quadratisch.jpg', 'Waldbär', 'coming soon', CS_AUFRUF)),
    # Runde 4 (18.11.2026): Clips aus baby-videos/runde5 (wach, lachend, im Arm), Stil v2
    'r5_smile_mamis_stimme': ('runde5/06_smile_weinrot.mp4', ['POV: Er hört Mamis', 'Stimme zum ersten Mal'], '🥹',
        (CS + '/strampler-kirschen/shop/strampler-kirschen_shop_ohne_logo.jpg', 'Strampler «Smile» und «Kirschen»', 'coming soon', CS_AUFRUF)),
    'r5_kirschen_freundin': ('runde5/37_kirschen_weiss.mp4', ['Schick das der Freundin,', 'die Kirschen liebt'], '🍒',
        (CS + '/strampler-kirschen/shop/strampler-kirschen_shop_ohne_logo.jpg', 'Strampler «Kirschen»', 'coming soon', CS_AUFRUF)),
    'r5_teddy_lacht_an': ('runde5/07_teddy_body_ringelarm.mp4', ['POV: Er lacht Dich', 'zum ersten Mal an'], '🧸',
        (SET + '/set_teddy_creme_quadratisch.jpg', 'Teddybär', 'Erstausstattung · 8 Teile', SHOP)),
    'r5_happy_baby_lachen': ('runde5/08_happy_baby.mp4', ['Warnung: Dieses Lachen', 'ist ansteckend'], '😄',
        (SET + '/set_bauernhof_quadratisch.jpg', 'Bauernhof «Happy Baby»', 'coming soon', CS_AUFRUF)),
    'r5_happy_baby_tante': ('runde5/25_happy_baby_b.mp4', ['POV: Du bist Tante', 'und er lacht Dich an'], '🤍',
        (SET + '/set_bauernhof_quadratisch.jpg', 'Bauernhof «Happy Baby»', 'coming soon', CS_AUFRUF)),
    'r5_kapuzentuch_erstes_bad': ('runde5/17_kapuzentuch_happy_baby.mp4', ['POV: Das erste Bad', 'ist geschafft'], '🛁',
        (SET + '/set_bauernhof_quadratisch.jpg', 'Bauernhof «Happy Baby»', 'coming soon · mit Kapuzentuch', CS_AUFRUF)),
    'r5_best_family_seid_ihr': ('runde5/16_best_family.mp4', ['POV: Ihr seid jetzt', 'die «Best Family»'], '🤍',
        (SET + '/set_best_family_quadratisch.jpg', '«Best Family» Teddy', 'coming soon', CS_AUFRUF)),
    'r5_best_family_lachen': ('runde5/20_best_family_lachen.mp4', ['Wer kann da noch', 'schlecht drauf sein?'], '🥹',
        (SET + '/set_best_family_quadratisch.jpg', '«Best Family» Teddy', 'coming soon', CS_AUFRUF)),
    'r5_best_family_eingekuschelt': ('runde5/18_kapuzentuch_best_family.mp4', ['POV: Frisch gebadet', 'und eingekuschelt'], '🧸',
        (SET + '/set_best_family_quadratisch.jpg', '«Best Family» Teddy', 'coming soon · mit Kapuzentuch', CS_AUFRUF)),
    'r5_baerenmuetze_papa': ('runde5/23_creme_baerenmuetze_arm.mp4', ['Schick das dem Papa,', 'der Bären liebt'], '🐻',
        (CS + '/knotenmuetzen-baer/shop/knotenmuetzen-baer_shop_ohne_logo.jpg', 'Knotenmützen «Bär»', 'coming soon', CS_AUFRUF)),
    'r5_born_2027_blau': ('runde5/35_born_in_2027_blau.mp4', ['POV: Er kommt 2027', 'und hat schon sein Outfit'], '💙',
        (CS + '/born-in-2027-blau/shop/born-in-2027-blau_shop_ohne_logo.jpg', 'Born in 2027 · Hellblau', 'coming soon', CS_AUFRUF)),
    'r5_smile_happy': ('runde5/36_smile_salbeigruen.mp4', ['Schick das der Person,', 'die Dich happy macht'], '💚',
        (CS + '/strampler-smile-gruen/shop/strampler-smile-gruen_shop_ohne_logo.jpg', '«You make me happy»', 'coming soon', CS_AUFRUF)),
    'r5_dad_mom_prinzessin': ('runde5/24_little_princess_dad_mom_hase.mp4', ['Schick das Mama und Papa', 'der kleinen Prinzessin'], '🤍',
        (SET + '/set_love_dad_mom_quadratisch.jpg', 'I love Dad Mom', 'coming soon', CS_AUFRUF)),
    'r5_box_dinosaur_grosi': ('runde5/27_box_dinosaur_body_arm.mp4', ['POV: Grosi hat ihn', 'endlich im Arm'], '🦖',
        (CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-dinosaur.jpg', 'Box «Dinosaur»', 'Weihnachtsbox · 5 Bodys + 5 Hosen', SHOP)),
    'r5_box_growing_goetti': ('runde5/29_box_growing_up_strong_body_D.mp4', ['POV: Götti schenkt', 'dieses Jahr Bodys'], '🎁',
        (CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-growing-up-strong.jpg', 'Box «Growing up strong»', 'Weihnachtsbox · 5 Bodys + 5 Hosen', SHOP)),
    'r5_box_lovely_gotti': ('runde5/32_box_lovely_body_arm.mp4', ['POV: Ihr erstes Weihnachten,', 'Gotti hat vorgesorgt'], '🎁',
        (CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-lovely-little-girl.jpg', 'Box «Lovely Little Girl»', 'Weihnachtsbox · 3 Bodys + 5 Leggings', SHOP)),
    'r5_box_mummy': ('runde5/33_box_mummy_halstuch_arm.mp4', ['Schick das der Mami', 'vor ihrem 1. Weihnachten'], '🎄',
        (CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-i-love-my-mummy.jpg', 'Box «I love my Mummy»', 'Weihnachtsbox · 3 Bodys + 3 Halstücher', SHOP)),
    'r5_box_dino_opa': ('runde5/40_box_dino_body.mp4', ['POV: Opa hat den', 'kleinen Dino entdeckt'], '🦕',
        (CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-dino.jpg', 'Box «Dino»', 'Weihnachtsbox · 3 Bodys + 3 Mulltücher', SHOP)),
}


def groesse(pfad):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', pfad],
                       capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])


def clip_frames(pfad):
    w, h = groesse(pfad)
    sw = round(w * H / h / 2) * 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(DAUER), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},{GRADE},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, H), b)


def emoji(zeichen, hoehe):
    fo = ImageFont.truetype(EMOJI, 109)
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((70, 70), zeichen, font=fo, embedded_color=True, anchor='mm')
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * hoehe / im.height), hoehe), Image.LANCZOS)


def teil(zeilen, k):
    aus = []
    for z in zeilen:
        aus.append(z[:k]); k -= len(z)
        if k <= 0:
            break
    return [a for a in aus if a]


def punch(fr, t):
    if t >= ZOOM_BIS:
        return fr
    f = 1 + 0.12 * (1 - m.ease(t / ZOOM_BIS))
    w, h = round(W * f), round(H * f)
    return fr.resize((w, h), Image.BILINEAR).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))


def text_ebene(zeilen, emo, mit_emoji=True, voll=None):
    """Weisse Schreibmaschinenschrift mit weichem Schatten, Emoji am Ende der letzten Zeile."""
    g = 52
    while max(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(z, font=ImageFont.truetype(SCHRIFT, g)) for z in (voll or zeilen)) > 930:
        g -= 2
    fo = ImageFont.truetype(SCHRIFT, g); lh = round(g * 1.27)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    schatten = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(schatten)
    sp = emoji(emo, 46)
    for k, z in enumerate(zeilen):
        letzte = k == len(zeilen) - 1
        ref = (voll or zeilen)[k]                     # Position immer von der ganzen Zeile, damit beim Tippen nichts springt
        breite = d.textlength(ref, font=fo) + (sp.width + 14 if (voll is None and letzte) or (voll and k == len(voll) - 1) else 0)
        x0 = (W - breite) / 2; y = TEXT_Y + k * lh
        ds.text((x0 + 2, y + 3), z, font=fo, fill=210, anchor='lm')
        d.text((x0, y), z, font=fo, fill=(255, 255, 255, 255), anchor='lm')
        if letzte and mit_emoji:
            schatten.paste(255, (int(x0 + breite - sp.width), int(y - sp.height / 2 - 4)), sp.getchannel('A').point(lambda v: v // 3))
            tx.alpha_composite(sp, (int(x0 + breite - sp.width), int(y - sp.height / 2 - 4)))
    schatten = schatten.filter(ImageFilter.GaussianBlur(7))
    schatten = schatten.point(lambda v: min(255, v))
    verlauf = Image.linear_gradient('L').resize((1, 560)).point(lambda v: int((255 - v) * 0.42)).resize((W, 560))
    schatten.paste(Image.new('L', (W, 560), 255), (0, 0), verlauf)   # weicher dunkler Verlauf oben, damit die Schrift auf Creme lesbar ist
    ebene = Image.new('RGBA', (W, H), (40, 30, 25, 0)); ebene.putalpha(schatten)
    ebene.alpha_composite(tx)
    return ebene


def reel(name):
    clip, zeilen, emo, ende = REELS[name]
    ebene = text_ebene(zeilen, emo)
    n = int(round(DAUER * FPS))
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', tmp], stdin=subprocess.PIPE)
    i = 0
    tipp = {}                                     # Schreibmaschine: Ebene je Anzahl sichtbarer Zeichen
    gesamt = sum(len(z) for z in zeilen)
    for i, fr in enumerate(clip_frames(os.path.join(VID, clip))):
        if i >= n:
            break
        t = i / FPS
        c = punch(fr, t).convert('RGBA')
        if t < TIPP_BIS:
            k = max(1, int(gesamt * t / TIPP_BIS) + 1)
            if k not in tipp:
                tipp[k] = text_ebene(teil(zeilen, k), emo, mit_emoji=False, voll=zeilen)
            c.alpha_composite(tipp[k])
        else:
            a = 1 - m.ease((t - (TEXT_BIS - 0.4)) / 0.4) if t < LOOP_AB else 1.0
            if a > 0:
                e = ebene if a >= 1 else ebene.copy()
                if a < 1:
                    e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
        if i == int(0.6 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = min(DAUER, (i + 1) / FPS)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    anhaengen(pfad, *ende)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(REELS)):
        reel(name)
