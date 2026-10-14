"""Paket 5: realistische KI-Babyfotos (Pinterest-Motive) mit den sunnozy-Sets -> Instagram-Karussells.

Folie 1: Foto mit Handschrift + Logo (Hausstil wie Paket 4).
Folie 2: "Im Bild"-Folie mit der Set-Praesentation auf Creme, Teileanzahl und Shop-Hinweis.

Aufruf: python3 make_paket5.py <foto-ordner> <praesentation-ordner (ohne_logo)> <ausgabeordner>
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
gen, praes, out = sys.argv[1:4]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', gen, gen, gen, out]
exec(src, g)
Image, ImageDraw = g['Image'], g['ImageDraw']
fill, grade, logo, F, SERR, np = g['fill'], g['grade'], g['logo'], g['F'], g['SERR'], g['np']
spaced, sprig = g['spaced'], g['sprig']
hand, put_logo = g['g']['hand'], g['g']['put_logo']
CREAM, INK, SOFT, SANS = g['CREAM'], g['INK'], g['SOFT'], g['SANS']
W, H = 1080, 1350

# (datei, set, set-name auf Folie 2, teile, text, text-position, ausschnitt-anker y)
POSTS = [
    ('01_fenster_lila', 'set_lila_hase', 'Lila Hase', 6, 'Guten Morgen,\nkleiner Sonnenschein.', 'unten', 0.4),
    ('02_papa_brust', 'set_best_family', 'Best family', 8, 'Der schönste Platz\nder Welt: bei Papa.', 'unten', 0.4),
    ('03_fuesschen_wal', 'set_wal_blau', 'Wal blau', 8, 'Zehn kleine Zehen.\nUnd mein ganzes Herz.', 'oben', 0.5),
    ('04_kuh_rassel', 'set_bauernhof', 'Bauernhof', 8, 'Hallo, kleine Kuh.\nWir werden Freunde.', 'unten', 0.4),
    ('05_meilenstein', 'set_gaensebluemchen', 'Gänseblümchen', 8, 'Ein Monat Liebe.\nUnd jeden Tag mehr.', 'unten', 0.4),
    ('06_nach_dem_baden', 'set_hase_rosa', 'Hase rosa', 8, 'Frisch gebadet.\nBereit zum Kuscheln.', 'unten', 0.3),
    ('07_mama_kuss', 'set_prinzessin_krone', 'Prinzessin', 8, 'Mein grösster Wunsch\nliegt hier.', 'unten', 0.3),
    ('08_draussen', 'set_love_dad_mom', 'I love Dad & Mom', 6, 'Handy weg.\nWir sind hier.', 'unten', 0.4),
]
# Handschrift auf der leeren Holzscheibe im Meilenstein-Foto (Mitte x, y in 1080x1350)
SCHEIBE = {'05_meilenstein': ((881, 850), '1 Monat')}


def shade(img, wo):
    """Sanfter dunkler Verlauf unten (oder oben), damit die weisse Handschrift lesbar ist."""
    w, h = img.size
    a = np.zeros((h, w), 'uint8')
    if wo == 'unten':
        y0 = int(h * 0.58)
        a[y0:] = (np.linspace(0, 1, h - y0) ** 1.4 * 120).astype('uint8')[:, None]
    else:
        y1 = int(h * 0.38)
        a[:y1] = (np.linspace(1, 0, y1) ** 1.4 * 120).astype('uint8')[:, None]
        y0 = int(h * 0.85)  # Logo unten trotzdem lesbar
        a[y0:] = (np.linspace(0, 1, h - y0) ** 1.4 * 80).astype('uint8')[:, None]
    ov = Image.new('RGBA', (w, h), (40, 28, 22, 0)); ov.putalpha(Image.fromarray(a))
    return Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')


def slide1(k, text, wo, ay):
    img = shade(grade(fill(Image.open(os.path.join(gen, k + '.jpg')).convert('RGB'), W, H, ay)), wo)
    if k in SCHEIBE:
        (cx, cy), t = SCHEIBE[k]
        hand(img, (cx, cy - 40), t, 70, fill=(112, 82, 66), anchor='ma', rot=-4, shadow=False)
    y = 1010 if wo == 'unten' else 90
    hand(img, (W // 2, y), text, 90, fill=(255, 251, 244), anchor='ma', rot=2, shadow=True)
    put_logo(img, 150, 40, (255, 255, 255))
    return img.convert('RGB')


def slide2(setname, label, teile):
    c = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(c)
    spaced(d, W / 2, 70, 'IM BILD', F(SANS, 26), SOFT, 8)
    hand(c, (W // 2, 105), 'Set ' + label, 92, fill=(112, 82, 66), anchor='ma', rot=1, shadow=False)
    p = Image.open(os.path.join(praes, setname + '_quadratisch.jpg')).convert('RGB').resize((900, 900), Image.LANCZOS)
    c.paste(p, ((W - 900) // 2, 250))
    d = ImageDraw.Draw(c)
    spaced(d, W / 2, 1185, f'{teile}-TEILIGES SET', F(SERR, 30), INK, 5)
    spaced(d, W / 2, 1240, 'SUNNOZY.CH  ·  LINK IN DER BIO', F(SANS, 24), SOFT, 6)
    return c


for d in ('folie1', 'folie2'):
    os.makedirs(os.path.join(out, d), exist_ok=True)
for k, setname, label, teile, text, wo, ay in POSTS:
    slide1(k, text, wo, ay).save(os.path.join(out, 'folie1', k + '.jpg'), quality=94)
    slide2(setname, label, teile).save(os.path.join(out, 'folie2', k + '_set.jpg'), quality=94)
    print(k, 'ok')
