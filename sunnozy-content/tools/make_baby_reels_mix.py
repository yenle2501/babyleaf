"""Mix-Reels: mehrere Grok-Babyclips zusammengeschnitten (18.11.2026).

Formate aus der Viral-Analyse:
  - «Welches nimmst Du? 1–4»: je Clip 2.5 s, grosse Nummer, Hook oben die ganze Zeit → Kommentare mit der Nummer
  - Kompilation: 4–5 Strecker hintereinander, harte Schnitte im Takt, Hook am Anfang und zum Loop am Ende
Bearbeitung v2: bei jedem Schnitt kurzer Zoom 108 % → 100 % (Zoom-Übergang), Hook tippt sich in 0.5 s ein.
Endfolie: Collage der gezeigten Sets (2×2) oder Set-Bild. Musik: Alex Morgan. Kein Preis.

    python3 tools/make_baby_reels_mix.py [name ...]
Ausgabe: posts/baby-reels/mix/reel_mix_<name>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import make_coming_soon_reels as m
import make_baby_reels as b
from endfolie import anhaengen, SET, CS, SHOP, CS_AUFRUF

W, H, FPS = b.W, b.H, b.FPS
OUT = os.path.join(m.POSTS, 'baby-reels', 'mix')

# (clip, start_s, nummer_label)
REELS = {
    'welches_set_shop': dict(
        hook=['Welches Set nimmst Du?', 'Schreib die Nummer'], emo='👇', nummern=True, seg=2.5,
        clips=[('set_little_bear_baby_strampler_1.mp4', 3.0), ('set_hello_world_blatt_baby_body_1.mp4', 3.0),
               ('set_teddy_creme_baby_strampler_1.mp4', 3.0), ('set_rosa_baby_strampler_1.mp4', 3.0)],
        ende=(['little_bear', 'hello_world_blatt', 'teddy_creme', 'rosa'], '1, 2, 3 oder 4?', 'Erstausstattungen · 5–8 Teile', SHOP)),
    'gotti_such_aus': dict(
        hook=['Gotti, such Dir eins aus'], emo='🎀', nummern=True, seg=2.5,
        clips=[('set_teddy_rosa_punkte_baby_strampler_1.mp4', 3.0), ('set_prinzessin_krone_baby_body_1.mp4', 3.0),
               ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', 3.0), ('set_hase_rosa_baby_body_1.mp4', 3.0)],
        ende=(['teddy_rosa_punkte', 'prinzessin_krone', 'little_and_loved_gans_rosa', 'hase_rosa'], 'Welche Nummer?', 'Schick das der Gotti', CS_AUFRUF)),
    'es_wird_ein_bub': dict(
        hook=['POV: Es wird ein Bub'], emo='💙', nummern=True, seg=2.5,
        clips=[('set_weltall_hellblau_baby_body_1.mp4', 3.0), ('set_wal_blau_baby_strampler_1.mp4', 3.0),
               ('set_waldbaer_creme_baby_body_1.mp4', 3.0), ('set_bauernhof_baby_strampler_2.mp4', 3.0)],
        ende=(['weltall_hellblau', 'wal_blau', 'waldbaer_creme', 'bauernhof'], 'Welches für Euren Bub?', 'coming soon', CS_AUFRUF)),
    'es_wird_ein_maedchen': dict(
        hook=['POV: Es wird ein Mädchen'], emo='🎀', nummern=True, seg=2.5,
        clips=[('set_rosa_baby_strampler_2.mp4', 3.0), ('set_gaensebluemchen_baby_strampler_1.mp4', 3.0),
               ('set_lila_hase_baby_body_2.mp4', 3.0), ('set_hello_schmetterling_baby_body_1.mp4', 3.0)],
        ende=(['rosa', 'gaensebluemchen', 'lila_hase', 'hello_schmetterling'], 'Welches für Eure Kleine?', 'Erstausstattungen und coming soon', SHOP)),
    'babyfieber_kompilation': dict(
        hook=['Warnung:', '5× Babyfieber am Stück'], emo='🥹', nummern=False, seg=2.0,
        clips=[('set_little_bear_baby_strampler_1.mp4', 3.2), ('set_love_dad_mom_baby_body_2.mp4', 3.2),
               ('set_hello_world_blatt_baby_body_2.mp4', 3.2), ('set_teddy_rosa_punkte_baby_strampler_2.mp4', 3.2),
               ('set_prinzessin_krone_baby_body_2.mp4', 3.2)],
        ende=(['little_bear', 'love_dad_mom', 'hello_world_blatt', 'teddy_rosa_punkte'], 'sunnozy Babysets', 'Erstausstattungen und coming soon', SHOP)),
    'haende_hoch': dict(
        hook=['Hände hoch,', 'wer Babyfieber hat'], emo='🙌', nummern=False, seg=2.0,
        clips=[('set_prinzessin_krone_baby_body_1.mp4', 3.6), ('set_little_bear_baby_body_1.mp4', 3.6),
               ('set_waldbaer_creme_baby_body_1.mp4', 4.0), ('set_hello_world_creme_baby_body_2.mp4', 3.6),
               ('set_love_dad_mom_baby_body_1.mp4', 3.6)],
        ende=(['prinzessin_krone', 'little_bear', 'waldbaer_creme', 'love_dad_mom'], 'sunnozy Babysets', 'Erstausstattungen und coming soon', SHOP)),
    # 18.11.2026: aus baby-videos/runde5
    'welches_lachen': dict(
        hook=['Welches Lachen', 'ist am süssesten?'], emo='🥹', nummern=True, seg=2.5,
        clips=[('runde5/07_teddy_body_ringelarm.mp4', 1.5), ('runde5/08_happy_baby.mp4', 1.5),
               ('runde5/16_best_family.mp4', 1.5), ('runde5/20_best_family_lachen.mp4', 1.5)],
        ende=(['teddy_creme', 'bauernhof', 'best_family', 'best_family'], 'Schreib die Nummer', 'Teddybär, Bauernhof, Best Family', SHOP)),
    'welche_box_fuer_wen': dict(
        hook=['Welche Weihnachtsbox', 'für welches Baby?'], emo='🎁', nummern=True, seg=2.5,
        clips=[('runde5/27_box_dinosaur_body_arm.mp4', 2.0), ('runde5/29_box_growing_up_strong_body_D.mp4', 2.0),
               ('runde5/32_box_lovely_body_arm.mp4', 2.0), ('runde5/33_box_mummy_halstuch_arm.mp4', 2.0)],
        ende=([CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-' + k + '.jpg' for k in ('dinosaur', 'growing-up-strong', 'lovely-little-girl', 'i-love-my-mummy')],
              '1, 2, 3 oder 4?', 'Weihnachtsboxen · fertig verpackt', SHOP)),
    # 18.11.2026, Kombinationen
    'box_fuer_wen': dict(
        hook=['Welche Box für wen?'], emo='🎁', nummern=False, hook_bleibt=True, seg=2.0,
        clips=[('runde5/27_box_dinosaur_body_arm.mp4', 2.0, 'fürs Grosi'), ('runde5/29_box_growing_up_strong_body_D.mp4', 2.0, 'vom Götti'),
               ('runde5/32_box_lovely_body_arm.mp4', 2.0, 'von der Gotti'), ('runde5/33_box_mummy_halstuch_arm.mp4', 2.0, 'für Mami'),
               ('runde5/40_box_dino_body.mp4', 1.5, 'vom Opa')],
        ende=([CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-' + k + '.jpg' for k in ('dinosaur', 'growing-up-strong', 'lovely-little-girl', 'i-love-my-mummy')],
              'Weihnachtsboxen', 'fertig verpackt · 5 Motive', SHOP)),
    'bub_oder_maedchen': dict(
        hook=['Bub oder Mädchen?', 'Schreib es uns'], emo='🤍', nummern=False, hook_bleibt=True, seg=2.5,
        clips=[('set_weltall_hellblau_baby_body_1.mp4', 3.0, 'Bub'), ('set_rosa_baby_strampler_1.mp4', 3.0, 'Mädchen'),
               ('set_wal_blau_baby_strampler_1.mp4', 3.0, 'Bub'), ('set_prinzessin_krone_baby_body_1.mp4', 3.0, 'Mädchen')],
        ende=(['weltall_hellblau', 'rosa', 'wal_blau', 'prinzessin_krone'], 'Bub oder Mädchen?', 'Erstausstattungen und coming soon', SHOP)),
    'erst_baden_dann_happy': dict(
        hook=['Erst baden,', 'dann happy'], emo='😄', nummern=False, seg=3.4,
        clips=[('runde5/17_kapuzentuch_happy_baby.mp4', 2.0, 'nach dem Bad'), ('runde5/08_happy_baby.mp4', 1.5, 'frisch angezogen'),
               ('runde5/25_happy_baby_b.mp4', 2.5, 'happy')],
        ende=(['bauernhof'], 'Bauernhof «Happy Baby»', 'coming soon · mit Kapuzentuch', CS_AUFRUF)),
    'best_family_tag': dict(
        hook=['Ein Morgen mit der', '«Best Family»'], emo='🧸', nummern=False, seg=3.4,
        clips=[('runde5/18_kapuzentuch_best_family.mp4', 2.0, 'nach dem Bad'), ('runde5/16_best_family.mp4', 1.5, 'Body und Mütze'),
               ('runde5/20_best_family_lachen.mp4', 2.0, 'und dieses Lachen')],
        ende=(['best_family'], '«Best Family» Teddy', 'coming soon', CS_AUFRUF)),
    'lachen_kompilation': dict(
        hook=['Schick das jemandem,', 'der heute lachen muss'], emo='😄', nummern=False, seg=2.0,
        clips=[('runde5/07_teddy_body_ringelarm.mp4', 2.0), ('runde5/08_happy_baby.mp4', 3.0), ('runde5/16_best_family.mp4', 2.0),
               ('runde5/20_best_family_lachen.mp4', 2.5), ('runde5/25_happy_baby_b.mp4', 1.5)],
        ende=(['teddy_creme', 'bauernhof', 'best_family'], 'sunnozy Babysets', 'Erstausstattungen und coming soon', SHOP)),
    'welche_farbe': dict(
        hook=['Welche Farbe', 'für Euer Baby?'], emo='🎨', nummern=False, hook_bleibt=True, seg=2.0,
        clips=[('set_rosa_baby_strampler_1.mp4', 3.0, 'Rosa'), ('set_lila_hase_baby_body_1.mp4', 3.0, 'Lila'),
               ('set_weltall_hellblau_baby_body_1.mp4', 3.0, 'Hellblau'), ('runde5/36_smile_salbeigruen.mp4', 2.0, 'Salbeigrün'),
               ('set_teddy_creme_baby_strampler_1.mp4', 3.0, 'Creme')],
        ende=(['rosa', 'lila_hase', 'weltall_hellblau', 'teddy_creme'], 'Welche Farbe?', 'Schreib sie in die Kommentare', SHOP)),
    'gotti_oder_goetti': dict(
        hook=['Gotti oder Götti:', 'wer schenkt was?'], emo='🎁', nummern=False, hook_bleibt=True, seg=2.5,
        clips=[('set_teddy_rosa_punkte_baby_strampler_1.mp4', 3.0, 'Gotti'), ('set_waldbaer_creme_baby_body_1.mp4', 3.0, 'Götti'),
               ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', 3.0, 'Gotti'), ('runde5/29_box_growing_up_strong_body_D.mp4', 2.0, 'Götti')],
        ende=(['teddy_rosa_punkte', 'waldbaer_creme', 'little_and_loved_gans_rosa', CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-growing-up-strong.jpg'],
              'Markier Gotti und Götti', 'Erstausstattungen und Weihnachtsboxen', SHOP)),
    'erstes_weihnachten': dict(
        hook=['Babys erstes Weihnachten', 'kommt näher'], emo='🎄', nummern=False, seg=2.5,
        clips=[('runde5/32_box_lovely_body_arm.mp4', 2.0), ('runde5/33_box_mummy_halstuch_arm.mp4', 2.0),
               ('runde5/40_box_dino_body.mp4', 1.5), ('runde5/27_box_dinosaur_body_arm.mp4', 2.0)],
        ende=([CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-' + k + '.jpg' for k in ('lovely-little-girl', 'i-love-my-mummy', 'dino', 'dinosaur')],
              'Weihnachtsboxen', 'fertig verpackt', SHOP)),
    'tante_markieren': dict(
        hook=['Markier die Tante,', 'die das schenken soll'], emo='🎀', nummern=True, seg=2.5,
        clips=[('set_lila_hase_baby_body_2.mp4', 3.0), ('set_hase_rosa_baby_body_1.mp4', 3.0),
               ('set_gaensebluemchen_baby_strampler_1.mp4', 3.0), ('set_hello_schmetterling_baby_body_1.mp4', 3.0)],
        ende=(['lila_hase', 'hase_rosa', 'gaensebluemchen', 'hello_schmetterling'], 'Welche Nummer?', 'Erstausstattungen und coming soon', SHOP)),
    # 18.11.2026, Nachmittag
    'body_oder_strampler_a': dict(
        hook=['Body oder Strampler:', 'was ziehst Du zuerst an?'], emo='🧸', nummern=False, hook_bleibt=True, seg=2.5,
        clips=[('set_little_bear_baby_body_1.mp4', 3.0, 'Body'), ('set_little_bear_baby_strampler_1.mp4', 3.0, 'Strampler'),
               ('set_teddy_creme_baby_body_1.mp4', 3.0, 'Body'), ('set_teddy_creme_baby_strampler_1.mp4', 3.0, 'Strampler')],
        ende=(['little_bear', 'teddy_creme'], 'Beides im Set', 'Hello Little Bear · Teddybär', SHOP)),
    'body_oder_strampler_b': dict(
        hook=['Body oder Strampler:', 'was ziehst Du zuerst an?'], emo='🎀', nummern=False, hook_bleibt=True, seg=2.5,
        clips=[('set_little_and_loved_gans_rosa_baby_body_1.mp4', 3.0, 'Body'), ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', 3.0, 'Strampler'),
               ('set_waldbaer_creme_baby_body_1.mp4', 3.0, 'Body'), ('set_waldbaer_creme_baby_strampler_1.mp4', 3.0, 'Strampler')],
        ende=(['little_and_loved_gans_rosa', 'waldbaer_creme'], 'Beides im Set', 'Little and Loved · Waldbär (coming soon)', SHOP)),
    'welches_tier': dict(
        hook=['Welches Tier', 'für Euer Baby?'], emo='🐾', nummern=False, hook_bleibt=True, seg=2.0,
        clips=[('set_hase_rosa_baby_body_1.mp4', 3.0, 'Hase'), ('set_little_bear_baby_strampler_1.mp4', 3.0, 'Bär'),
               ('set_wal_blau_baby_strampler_1.mp4', 3.0, 'Wal'), ('runde5/40_box_dino_body.mp4', 1.5, 'Dino'),
               ('set_hund_creme_baby_body_1.mp4', 3.0, 'Hund')],
        ende=(['hase_rosa', 'little_bear', 'wal_blau', 'hund_creme'], 'Welches Tier?', 'Schreib es in die Kommentare', SHOP)),
    'shop_6_in_10s': dict(
        hook=['6 Erstausstattungen', 'in 10 Sekunden'], emo='✨', nummern=False, hook_bleibt=True, seg=1.7,
        clips=[('set_little_bear_baby_strampler_1.mp4', 3.2, 'Hello Little Bear'), ('set_hello_world_blatt_baby_body_1.mp4', 3.2, 'Hello World'),
               ('set_teddy_creme_baby_strampler_1.mp4', 3.2, 'Teddybär'), ('set_rosa_baby_strampler_1.mp4', 3.2, 'Princess'),
               ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', 3.2, 'Little and Loved'), ('set_hello_schmetterling_baby_body_1.mp4', 3.2, 'Hello')],
        ende=(['little_bear', 'hello_world_blatt', 'teddy_creme', 'rosa'], 'Erstausstattungen', '5 bis 8 Teile', SHOP)),
    'coming_soon_vorschau': dict(
        hook=['Das kommt bald', 'zu sunnozy'], emo='👀', nummern=False, hook_bleibt=True, seg=2.0,
        clips=[('set_weltall_hellblau_baby_body_1.mp4', 3.0, 'Weltall'), ('set_wal_blau_baby_strampler_1.mp4', 3.0, 'Wal'),
               ('set_waldbaer_creme_baby_body_1.mp4', 3.0, 'Waldbär'), ('set_bauernhof_baby_strampler_1.mp4', 3.0, 'Bauernhof'),
               ('set_love_dad_mom_baby_body_2.mp4', 3.0, 'I love Dad Mom')],
        ende=(['weltall_hellblau', 'wal_blau', 'waldbaer_creme', 'love_dad_mom'], 'coming soon', 'Welches willst Du zuerst?', CS_AUFRUF)),
    'gotti_top3': dict(
        hook=['Unsere Top 3', 'für Gotti-Geschenke'], emo='🎀', nummern=False, hook_bleibt=True, seg=3.3,
        clips=[('set_teddy_rosa_punkte_baby_strampler_1.mp4', 3.0, 'Nr. 3'), ('set_little_and_loved_gans_rosa_baby_strampler_2.mp4', 3.0, 'Nr. 2'),
               ('runde5/32_box_lovely_body_arm.mp4', 2.0, 'Nr. 1')],
        ende=(['teddy_rosa_punkte', 'little_and_loved_gans_rosa', CS + '/kampagne-weihnachtsbox/shopify/geschenkbox-lovely-little-girl.jpg'],
              'Markier die Gotti', 'Erstausstattungen und Weihnachtsboxen', SHOP)),
    'dad_mom_alles': dict(
        hook=['Für Mama und Papa,', 'die alles teilen'], emo='🤍', nummern=False, seg=2.5,
        clips=[('set_love_dad_mom_baby_body_1.mp4', 3.0, 'Body'), ('set_love_dad_mom_baby_strampler_1.mp4', 3.0, 'Strampler'),
               ('set_love_dad_mom_baby_body_2.mp4', 3.0, 'Body'), ('set_love_dad_mom_baby_strampler_2.mp4', 3.0, 'Strampler')],
        ende=(['love_dad_mom'], 'I love Dad Mom', 'coming soon', CS_AUFRUF)),
    'schlafmuetzen': dict(
        hook=['Pssst…', '4 kleine Schlafmützen'], emo='😴', nummern=False, seg=2.5,
        clips=[('eisbaer-taupe_baby_v1-ohne-referenzlook_2.mp4', 3.0), ('set_weltall_hellblau_baby_strampler_1.mp4', 3.0),
               ('set_hund_creme_baby_body_2.mp4', 3.0), ('set_teddy_rosa_punkte_baby_body_1.mp4', 3.0)],
        ende=(['weltall_hellblau', 'hund_creme', 'teddy_rosa_punkte'], 'sunnozy', 'coming soon', CS_AUFRUF)),
}


def collage(sets, pfad):
    quelle = lambda s: s if '/' in s else f'{SET}/set_{s}_quadratisch.jpg'
    if len(sets) == 1:
        return quelle(sets[0])
    c = Image.new('RGB', (1000, 1000), (250, 246, 240))
    for k, s in enumerate(sets):
        im = Image.open(quelle(s)).convert('RGB').resize((490, 490), Image.LANCZOS)
        x = (k % 2) * 510 if not (len(sets) == 3 and k == 2) else 255
        c.paste(im, (x, 255 if len(sets) == 2 else (k // 2) * 510))
    c.save(pfad, quality=92)
    return pfad


def frames(clip, start, dauer):
    pfad = os.path.join(b.VID, clip)
    w, h = b.groesse(pfad); sw = round(w * H / h / 2) * 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dauer), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},{b.GRADE},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3; k = 0
    while k < int(round(dauer * FPS)):
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield Image.frombuffer('RGB', (W, H), buf); k += 1
    p.kill()


def label(text):
    """Kurzer Text in einer dunklen Pille unten (z. B. «fürs Grosi»)."""
    fo = ImageFont.truetype(b.SCHRIFT, 60)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=fo); y = 1560
    d.rounded_rectangle((W / 2 - tw / 2 - 40, y - 58, W / 2 + tw / 2 + 40, y + 58), radius=58, fill=(40, 30, 25, 125))
    d.text((W / 2, y + 2), text, font=fo, fill=(255, 255, 255, 255), anchor='mm')
    return im


def nummer(n):
    fo = ImageFont.truetype(b.SCHRIFT, 150)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((W / 2 - 95, 1560 - 95, W / 2 + 95, 1560 + 95), fill=(40, 30, 25, 120))   # dunkler Kreis, damit die Zahl auf hellem Stoff lesbar ist
    d.text((W / 2, 1560 + 6), str(n), font=fo, fill=(255, 255, 255, 255), anchor='mm')
    return im


def reel(name):
    r = REELS[name]
    ebene = b.text_ebene(r['hook'], r['emo'])
    seg = r['seg']; dauer = seg * len(r['clips'])
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_mix_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', tmp], stdin=subprocess.PIPE)
    i = 0
    for k, eintrag in enumerate(r['clips']):
        clip, start = eintrag[:2]
        num = label(eintrag[2]) if len(eintrag) > 2 else (nummer(k + 1) if r['nummern'] else None)
        for j, fr in enumerate(frames(clip, start, seg)):
            t = i / FPS; tj = j / FPS
            if tj < 0.25:                                                # Zoom-Übergang bei jedem Schnitt
                f = 1 + 0.08 * (1 - m.ease(tj / 0.25)); w2, h2 = round(W * f), round(H * f)
                fr = fr.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
            if r['nummern'] or r.get('hook_bleibt'):
                a = 1.0                                                  # Hook bleibt stehen, damit man mitzählt
            else:
                a = 1 - m.ease((t - 2.2) / 0.4) if t < dauer - 1.6 else m.ease((t - (dauer - 1.6)) / 0.4)
            c = fr.convert('RGBA')
            if t < b.TIPP_BIS:
                ges = sum(len(z) for z in r['hook']); kk = max(1, int(ges * t / b.TIPP_BIS) + 1)
                c.alpha_composite(b.text_ebene(b.teil(r['hook'], kk), r['emo'], mit_emoji=False, voll=r['hook']))
            elif a > 0:
                e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
            if num is not None:
                c.alpha_composite(num)
            if i == int(0.5 * FPS):
                c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
            enc.stdin.write(c.convert('RGB').tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    dauer = i / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', b.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', 'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    sets, titel, zeile, aufruf = r['ende']
    bild = collage(sets, os.path.join('/tmp', f'collage_{name}.jpg'))
    anhaengen(pfad, bild, titel, zeile, aufruf)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(REELS)):
        reel(name)
