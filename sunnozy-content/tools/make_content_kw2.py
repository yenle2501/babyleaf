"""Content KW 2 (25.11.–1.12.2026, Black-Friday-Woche): nur Produkte, die in Shopify aktiv und an Lager sind.

Wunsch der Nutzerin: Fotos aus posts/baby-photos/referenzen_photos_neu und die passenden Grok-Videos aus posts/baby-videos.
Nicht verwendet: Bilder/Videos mit Plüschtier oder Nuggi (z.B. little_and_loved Strampler, little_bear Body, rosa Strampler,
hello_world_creme Body). Die Grok-Videos «Strecken» zeigen verschlafene Babys (Augen meist zu), der Text spricht nie vom Schlafen.

    python3 tools/make_content_kw2.py [reels|karussell|stories|<reel-name>]
Ausgabe: posts/content-kw2/ (Plan und Captions: posts/content-kw2/README.md)
"""
import os, sys
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_content_kw1 as k1

P = m.POSTS
k1.OUT = OUT = os.path.join(P, 'content-kw2')
FOT = os.path.join(P, 'baby-photos', 'referenzen_photos_neu')

k1.REELS = {
    'little_bear_haende_hoch': {'clips': [('set_little_bear_baby_strampler_1.mp4', 0.0, 10.0)],
                                'hook': (['POV: Die Hände-hoch-Pose', 'ist inklusive'], '🙌'),
                                'ende': (['Hello Little Bear', 'jetzt im Shop'], '🧸'), 'schleier': True, 'text_y': 1560},
    'hello_world_strecken': {'clips': [('set_hello_world_blatt_baby_body_1.mp4', 0.0, 10.0)],
                             'hook': (['POV: Das erste', 'grosse Strecken'], '✨'),
                             'ende': (['Hello World', 'jetzt im Shop'], '🌿'), 'schleier': True, 'text_y': 1560},
    'little_and_loved_morgen': {'clips': [('set_little_and_loved_gans_rosa_baby_body_1.mp4', 0.0, 10.0)],
                                'hook': (['POV: Jeden Morgen', 'dieses Strecken'], '🥹'),
                                'ende': (['little and loved', 'jetzt im Shop'], '🤍'), 'schleier': True, 'text_y': 1560},
    'geschenkbox_gotti': {'clips': [('weihnachtsbox_mummy_c_bearbeitet.mp4', 0.5, 12.5)],
                          'hook': (['POV: Du packst das Geschenk', 'fürs Gottikind'], '🎁'),
                          'ende': (['Geschenkbox', '«I love my Mummy»'], '🎄'), 'schleier': True, 'text_y': 1500},
}

# Karussell: Erstausstattung, die jetzt im Shop ist (Preise aus Shopify, 17.11.2026)
SETS = [('set_hello_world_creme_baby_body_ads.png', '«Hello World»', '8 Teile · CHF 29.40'),
        ('set_little_bear_baby_strampler.png', '«Hello Little Bear»', '5 Teile · CHF 28.40'),
        ('set_little_and_loved_gans_rosa_baby_body.png', '«Little and Loved»', '8 Teile · CHF 30.40'),
        ('set_rosa_baby_body.png', '«Princess»', '8 Teile · CHF 30.40'),
        ('set_hello_world_blatt_baby_strampler_ads.png', '«Hello World»', 'Strampler mit Blätter-Print')]


def karussell():
    o = os.path.join(OUT, 'karussell'); os.makedirs(o, exist_ok=True)
    c = Image.new('RGB', (1080, 1350), k1.CREME); d = ImageDraw.Draw(c)
    for k, (datei, _, _) in enumerate(SETS[:4]):
        im = k1.auf_4x5(Image.open(os.path.join(FOT, datei)).convert('RGB')).resize((392, 490), Image.LANCZOS)
        c.paste(im, (138 + (k % 2) * 412, 300 + (k // 2) * 515))
    k1.mitte(d, 'Jetzt im Shop', 120, 44, (150, 130, 115))
    k1.mitte(d, 'Erstausstattung fürs Winterbaby', 210, 50)
    c.save(os.path.join(o, '01_titel.jpg'), quality=94)
    for k, (datei, name, info) in enumerate(SETS, 2):
        im = k1.auf_4x5(Image.open(os.path.join(FOT, datei)).convert('RGB')).convert('RGBA')
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        b = max(dl.textlength(name, font=k1.f(40)), dl.textlength(info, font=k1.f(30))) + 50
        dl.rounded_rectangle((40, 1180, 40 + b, 1310), 28, fill=(250, 246, 240, 230))
        dl.text((65, 1222), name, font=k1.f(40), fill=k1.DUNKEL + (255,), anchor='lm')
        dl.text((65, 1278), info, font=k1.f(30), fill=(120, 105, 95, 255), anchor='lm')
        im.alpha_composite(lay); im.convert('RGB').save(os.path.join(o, f'{k:02d}.jpg'), quality=94)
    c = Image.new('RGB', (1080, 1350), k1.CREME); d = ImageDraw.Draw(c)
    for k, t in enumerate(['Welches ist', 'Dein Favorit?']):
        k1.mitte(d, t, 470 + k * 90, 64)
    k1.mitte(d, '100 % Baumwolle · Gratisversand ab CHF 50', 700, 32, (120, 105, 95))
    k1.mitte(d, 'Link in der Bio', 770, 32, (120, 105, 95))
    L = m.logo(300, (122, 108, 104)); c.paste(L, ((1080 - L.width) // 2, 1000), L)
    c.save(os.path.join(o, f'{len(SETS) + 2:02d}_ende.jpg'), quality=94)
    print('Karussell:', sorted(os.listdir(o)))


def stories():
    o = os.path.join(OUT, 'stories'); os.makedirs(o, exist_ok=True)
    W, H = k1.W, k1.H
    # Story 1: Umfrage Hello Little Bear oder Hello World
    c = Image.new('RGB', (W, H), k1.CREME); d = ImageDraw.Draw(c)
    k1.mitte(d, 'Welches Set würdest', 250, 56); k1.mitte(d, 'Du verschenken?', 330, 56)
    for k, (datei, name) in enumerate([('set_little_bear_baby_strampler.png', 'Hello Little Bear'), ('set_hello_world_blatt_baby_strampler_ads.png', 'Hello World')]):
        im = k1.auf_4x5(Image.open(os.path.join(FOT, datei)).convert('RGB')).resize((440, 550), Image.LANCZOS)
        c.paste(im, (80 + k * 480, 450)); k1.mitte(d, '', 0, 10)
        d.text((300 + k * 480, 1040), name, font=k1.f(34), fill=k1.DUNKEL, anchor='mm')
    k1.mitte(d, '(Umfrage-Sticker hier)', 1250, 30, (190, 180, 170))
    L = m.logo(220, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1700), L)
    c.save(os.path.join(o, 'story_umfrage_set.jpg'), quality=93)
    # Story 2: Neugeborenen-Grösse noch da (Lager am Posttag prüfen!)
    im = k1.auf_4x5(Image.open(os.path.join(FOT, 'set_little_bear_baby_strampler.png')).convert('RGB'))
    c = Image.new('RGB', (W, H), k1.CREME); d = ImageDraw.Draw(c)
    c.paste(im.resize((900, 1125), Image.LANCZOS), (90, 400))
    k1.mitte(d, 'Für Neugeborene', 200, 58); k1.mitte(d, 'Grösse 0–3 Monate ist noch da', 280, 40, (120, 105, 95))
    k1.mitte(d, 'Hello Little Bear · 5 Teile', 1610, 44)
    k1.mitte(d, '(Link-Sticker zum Produkt)', 1700, 28, (190, 180, 170))
    c.save(os.path.join(o, 'story_neugeboren.jpg'), quality=93)
    print('Stories:', sorted(os.listdir(o)))


if __name__ == '__main__':
    teil = sys.argv[1:] or ['reels', 'karussell', 'stories']
    if 'karussell' in teil:
        karussell()
    if 'stories' in teil:
        stories()
    for name in k1.REELS:
        if 'reels' in teil or name in teil:
            k1.reel(name)
