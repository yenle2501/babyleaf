"""Paket 7: Werbe-Formate nach Vorlagen der Nutzerin (Blossom & Pear, Belife, MKI, Dilling).

  01 weihnachten        Baby mit Weihnachtsmuetze und Kuscheltier, ohne Text (Blossom-&-Pear-Stil), 4:5
  02 shop_jetzt         Teile frei gestellt auf Leinen, untereinander, Einkaufstasche mit Logo, "JEDERZEIT / JETZT SHOPPEN", 9:16
  03 sticker_wand       Teile als Sticker mit weissem Rand und Pin an der Wand, 3x3, "JEDE FARBE / JEDER MOMENT", 9:16
  04 fotowand           9 Fotos mit Klebeband an der Wand, Mitte = Ankuendigungskarte, 9:16
  05 new_drop           9 leere Blaetter mit Bueroklammer, Handschrift "neues Set / morgen 19 Uhr", 9:16 (Teaser)
  06 angebot            Dilling-Stil: Produkt auf Salbeigruen, Serifen-Zahl, Logo senkrecht, 4:5
  07 angebot_foto       Dilling-Stil mit Lifestyle-Foto, 4:5
  08 vorteile           Dilling-Stil mit Milchglas-Karte: Titel, 5,0-Sterne, drei Vorteile, 4:5
  09 weihnachten_geschenk Geschenkbox, kleiner Text, 4:5

Angebots-Werte (Rabatt, Datum) stehen oben in ANGEBOT und muessen vor dem Posten angepasst werden.

Aufruf: python3 make_paket7.py <roh-ordner> <feed-fotos paket6> <ausgabe>
"""
import sys, os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

here = os.path.dirname(os.path.abspath(__file__))
roh, p6, out = sys.argv[1:4]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', roh, roh, roh, out]
exec(src, g)
logo, hand = g['logo'], g['g']['hand']
INK, SOFT = g['INK'], g['SOFT']
os.makedirs(out, exist_ok=True)

# ---- Angebot: VOR DEM POSTEN ANPASSEN ----
ANGEBOT = {'rabatt': '20 %', 'zeile': 'AUF ALLE SETS', 'zeitraum': 'NUR VOM 21.–23.11.', 'hinweis': 'NUR BIS MITTERNACHT'}

FONTS = os.path.join(here, '..', 'fonts')
SERIF = os.path.join(FONTS, 'cormorantR.ttf')
SERIF_I = os.path.join(FONTS, 'cormorant.ttf')
SANS = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
SANS_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
SANS_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
SANS_XB = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
F = lambda p, s: ImageFont.truetype(p, s)
BROWN = (110, 84, 66)
W45, H45, W9, H9 = 1080, 1350, 1080, 1920
random.seed(4)
R = lambda n: os.path.join(roh, n)
TEIL = lambda n: Image.open(os.path.join(roh, 'teile', n + '.png')).convert('RGBA')


def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.convert('RGB').resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def soft(im, sat=0.92):
    im = ImageEnhance.Color(im.convert('RGB')).enhance(sat)
    a = np.asarray(im).astype(np.float32); a = 10 + a * (243 / 255)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def spaced(d, xy, text, font, fill, track=0, anchor='l'):
    """Text mit Laufweite; anchor l/r/m bezogen auf x."""
    w = sum(font.getlength(c) for c in text) + track * (len(text) - 1)
    x = xy[0] - (w if anchor == 'r' else w / 2 if anchor == 'm' else 0)
    for c in text:
        d.text((x, xy[1]), c, font=font, fill=fill); x += font.getlength(c) + track
    return w


def fit(im, maxw, maxh):
    s = min(maxw / im.width, maxh / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def drop_shadow(base, piece, xy, blur=14, off=(6, 14), op=0.28, rot=0):
    a = piece.getchannel('A')
    sh = Image.new('L', base.size, 0); sh.paste(a, (xy[0] + off[0], xy[1] + off[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
    dark = Image.new('RGBA', base.size, (60, 45, 35, 0)); dark.putalpha(sh)
    base = Image.alpha_composite(base.convert('RGBA'), dark)
    base.alpha_composite(piece, xy)
    return base


def save(img, name):
    img.convert('RGB').save(os.path.join(out, name + '.jpg'), quality=94); print(name)


# ---------- 01 Weihnachten (ohne Text, wie Blossom & Pear) ----------
save(soft(cover(Image.open(R('weihnachten_baby.jpg')), W45, H45), 0.97), '01_weihnachten')

# ---------- 02 Shop jetzt (Belife-Stil) ----------
c = cover(Image.open(R('leinen.jpg')), W9, H9).convert('RGBA')
items = ['set_hello_schmetterling_body', 'set_lila_hase_body', 'set_best_family_body']
y = 120
for i, n in enumerate(items):
    p = fit(TEIL(n), 330, 330)
    c = drop_shadow(c, p, (110 + (i % 2) * 40, y)); y += p.height + 24
bag = Image.open(R('tasche.png')).convert('RGBA'); bag = bag.crop(bag.getchannel('A').getbbox()); bag = fit(bag, 430, 520)
L = logo(170, INK); bx, by = 80, H9 - bag.height - 170
bag.alpha_composite(L, ((bag.width - L.width) // 2 - 20, int(bag.height * 0.55)))
c = drop_shadow(c, bag, (bx, by), blur=22, off=(-30, 18), op=0.35)
d = ImageDraw.Draw(c)
Lt = logo(300, BROWN); c.alpha_composite(Lt, (W9 - Lt.width - 90, 150))
spaced(d, (W9 - 90, 760), 'SHOPPEN', F(SANS_M, 50), BROWN, 2, 'r')
spaced(d, (W9 - 90, 815), 'JEDERZEIT', F(SANS_XB, 92), BROWN, 0, 'r')
spaced(d, (W9 - 90, 1000), 'SHOPPEN', F(SANS_M, 50), BROWN, 2, 'r')
spaced(d, (W9 - 90, 1055), 'JETZT', F(SANS_XB, 150), BROWN, 0, 'r')
spaced(d, (W9 - 90, H9 - 200), 'SUNNOZY.CH', F(SANS_B, 52), BROWN, 1, 'r')
save(c, '02_shop_jetzt')

# ---------- 03 Sticker-Wand (Belife-Stil) ----------
c = cover(Image.open(R('wand.jpg')), W9, H9).convert('RGBA')


def sticker(im, w, h):
    im = fit(im, w, h)
    pad = 16
    a = im.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    big = Image.new('L', (im.width + 2 * pad, im.height + 2 * pad), 0); big.paste(a, (pad, pad))
    big = big.filter(ImageFilter.MaxFilter(2 * pad + 1)).filter(ImageFilter.GaussianBlur(1.5))
    s = Image.new('RGBA', big.size, (255, 255, 255, 0)); s.putalpha(big)
    s.alpha_composite(im, (pad, pad))
    return s


def pin(base, x, y):
    d = ImageDraw.Draw(base)
    d.ellipse([x - 15 + 4, y - 15 + 6, x + 15 + 4, y + 15 + 6], fill=(0, 0, 0, 40))
    d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=(235, 235, 238, 220), outline=(190, 190, 195, 255), width=2)
    d.ellipse([x - 6, y - 9, x + 3, y - 2], fill=(255, 255, 255, 255))


grid = ['set_hello_schmetterling_body', 'set_best_family_muetze', 'set_lila_hase_body',
        'set_best_family_rassel', 'set_prinzessin_krone_strampler', 'set_wal_blau_socken',
        'set_best_family_body', 'set_gaensebluemchen_laetzchen', 'set_hello_schmetterling_hose']
cw, ch = 300, 330
for i, n in enumerate(grid):
    s = sticker(TEIL(n), cw - 40, ch - 40).rotate(random.uniform(-3, 3), resample=Image.BICUBIC, expand=True)
    cx = 210 + (i % 3) * 330; cy = 540 + (i // 3) * 400
    x, y = cx - s.width // 2, cy - s.height // 2
    c = drop_shadow(c, s, (x, y), blur=10, off=(5, 10), op=0.22)
    pin(c, cx, y + 26)
d = ImageDraw.Draw(c)
spaced(d, (300, 300), 'JEDE FARBE', F(SANS_M, 34), (95, 85, 78), 3, 'm')
spaced(d, (780, 300), 'JEDER MOMENT', F(SANS_M, 34), (95, 85, 78), 3, 'm')
L = logo(260, (95, 85, 78)); c.alpha_composite(L, ((W9 - L.width) // 2, H9 - 250))
save(c, '03_sticker_wand')

# ---------- 04 Fotowand mit Klebeband (MKI-Stil) ----------
wall = cover(Image.open(R('wand.jpg')), W9, H9)
wall = ImageEnhance.Brightness(wall).enhance(0.62); wall = ImageEnhance.Color(wall).enhance(0.6)
c = wall.convert('RGBA')
fotos = sorted(f for f in os.listdir(p6) if f.endswith('.jpg'))
pics = [os.path.join(p6, f) for f in fotos]
pw, ph, gap = 270, 340, 26
x0 = (W9 - 3 * pw - 2 * gap) // 2; y0 = (H9 - 3 * ph - 2 * gap) // 2 + 30
k = 0
for i in range(9):
    x = x0 + (i % 3) * (pw + gap) + random.randint(-4, 4); y = y0 + (i // 3) * (ph + gap) + random.randint(-4, 4)
    card = Image.new('RGBA', (pw, ph), (250, 249, 246, 255))
    if i == 4:
        dc = ImageDraw.Draw(card)
        for j, t in enumerate(['NEUE SETS', 'SIND DA']):
            spaced(dc, (pw // 2, 110 + j * 52), t, F(SANS_XB, 40), (30, 28, 26), 0, 'm')
        spaced(dc, (pw // 2, 250), 'SUNNOZY.CH', F(SANS_B, 16), (60, 55, 50), 2, 'm')
    else:
        im = cover(Image.open(pics[k % len(pics)]), pw - 16, ph - 16, 0.4); k += 1
        card.paste(im, (8, 8))
    card = card.rotate(random.uniform(-1.2, 1.2), resample=Image.BICUBIC, expand=True)
    c = drop_shadow(c, card, (x, y), blur=8, off=(3, 6), op=0.35)
    tape = Image.new('RGBA', (110, 34), (236, 234, 226, 200)); tape = tape.rotate(random.uniform(-4, 4), expand=True)
    c.alpha_composite(tape, (x + pw // 2 - 55, y - 16))
save(c, '04_fotowand')

# ---------- 05 New Drop Teaser (Handschrift auf Blaettern) ----------
c = Image.new('RGBA', (W9, H9), (226, 228, 226, 255))
grad = np.linspace(1.04, 0.92, H9)[:, None, None] * np.ones((1, W9, 1))
c = Image.fromarray(np.clip(np.asarray(c.convert('RGB')).astype(np.float32) * grad, 0, 255).astype(np.uint8)).convert('RGBA')
pw, ph, gap = 290, 400, 30
x0 = (W9 - 3 * pw - 2 * gap) // 2; y0 = (H9 - 3 * ph - 2 * gap) // 2
for i in range(9):
    x = x0 + (i % 3) * (pw + gap) + random.randint(-6, 6); y = y0 + (i // 3) * (ph + gap) + random.randint(-6, 6)
    sheet = Image.new('RGBA', (pw, ph), (242, 243, 242, 255))
    ImageDraw.Draw(sheet).line([(0, ph - 3), (pw, ph - 3)], fill=(205, 206, 205, 255), width=3)
    sheet = sheet.rotate(random.uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True)
    c = drop_shadow(c, sheet, (x, y), blur=7, off=(2, 6), op=0.3)
    d = ImageDraw.Draw(c); cx = x + random.randint(50, pw - 70); a = math.radians(random.uniform(-35, 35))
    pts = [(0, 0), (0, 70), (14, 82), (28, 70), (28, 10), (18, 2), (8, 10), (8, 60)]
    pts = [(cx + px * math.cos(a) - py * math.sin(a), y - 22 + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
    d.line(pts, fill=(160, 162, 166, 255), width=4, joint='curve')
c = c.convert('RGB')
hand(c, (W9 // 2, 820), 'neues Set', 110, fill=(25, 25, 25), anchor='ma', rot=-1, shadow=False)
hand(c, (W9 // 2, 960), 'morgen um 19 Uhr', 96, fill=(25, 25, 25), anchor='ma', rot=1, shadow=False)
save(c, '05_new_drop')


# ---------- 06–08 Dilling-Stil ----------
def vertical_logo(c, x, y, h, col=(255, 255, 255)):
    L = logo(h, col).rotate(-90, expand=True); c.alpha_composite(L, (x - L.width // 2, y - L.height // 2))


def offer(c, x, y, small_top=None):
    d = ImageDraw.Draw(c)
    if small_top:
        spaced(d, (x, y - 200), small_top, F(SANS_M, 32), (255, 255, 255), 1)
    d.text((x - 6, y), ANGEBOT['rabatt'], font=F('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', 170), fill=(255, 255, 255), anchor='ls')
    spaced(d, (x, y + 30), ANGEBOT['zeile'], F(SERIF, 70), (255, 255, 255), 3)
    spaced(d, (x, y + 140), 'FÜR BABYS · SUNNOZY.CH', F(SANS_M, 30), (255, 255, 255), 2)


src6 = Image.open(R('body_salbei.jpg')).convert('RGB')
sage = tuple(int(v) for v in np.asarray(src6)[:40, :40].reshape(-1, 3).mean(0))
c = Image.new('RGBA', (W45, H45), sage + (255,))
b6 = fit(src6, 760, 940)
fm = Image.new('L', b6.size, 0); ImageDraw.Draw(fm).rectangle([30, 30, b6.width - 30, b6.height - 30], fill=255)
c.paste(b6, ((W45 - b6.width) // 2 - 60, 40), fm.filter(ImageFilter.GaussianBlur(25)))
vertical_logo(c, W45 - 120, 520, 330)
offer(c, 110, 1110, ANGEBOT['zeitraum'])
save(c, '06_angebot')

c = soft(cover(Image.open(os.path.join(p6, '02_hand_in_hand.jpg')), W45, H45, 0.3)).convert('RGBA')
sh = Image.new('L', (W45, H45), 0); ImageDraw.Draw(sh).rectangle([0, 520, W45, H45], fill=110)
dark = Image.new('RGBA', (W45, H45), (40, 30, 26, 0)); dark.putalpha(sh.filter(ImageFilter.GaussianBlur(160)))
c = Image.alpha_composite(c, dark)
vertical_logo(c, W45 - 110, 560, 330)
offer(c, 110, 1060, ANGEBOT['hinweis'])
save(c, '07_angebot_foto')

c = soft(cover(Image.open(os.path.join(p6, '05_stubenwagen.jpg')), W45, H45, 0.4)).convert('RGBA')
box = (300, 760, 1000, 1170)
blur = c.crop(box).filter(ImageFilter.GaussianBlur(18))
glass = Image.new('RGBA', blur.size, (90, 80, 76, 95))
blur = Image.alpha_composite(blur.convert('RGBA'), glass)
m = Image.new('L', blur.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, blur.width - 1, blur.height - 1], 22, fill=255)
c.paste(blur, box[:2], m)
d = ImageDraw.Draw(c); x = box[0] + 44
d.text((x, box[1] + 40), '100 % Baumwolle', font=F(SERIF, 54), fill=(255, 255, 255))
d.text((x, box[1] + 100), 'für die ersten Wochen', font=F(SERIF, 54), fill=(255, 255, 255))
d.text((x, box[1] + 190), '5,0', font=F(SANS, 26), fill=(255, 255, 255))
for j in range(5):
    cx, cy, r = x + 70 + j * 32, box[1] + 204, 13
    pts = [(cx + (r if k % 2 == 0 else r * 0.45) * math.sin(math.pi * k / 5), cy - (r if k % 2 == 0 else r * 0.45) * math.cos(math.pi * k / 5)) for k in range(10)]
    d.polygon(pts, fill=(255, 255, 255))
d.text((x + 240, box[1] + 192), 'Kundenbewertungen', font=F(SANS, 24), fill=(255, 255, 255))
for j, t in enumerate(['Versand aus der Schweiz', 'Gratis ab CHF 50', '14 Tage Rückgabe']):
    yy = box[1] + 268 + j * 44
    d.ellipse([x + 4, yy + 12, x + 12, yy + 20], fill=(220, 220, 220)); d.text((x + 30, yy), t, font=F(SANS, 28), fill=(255, 255, 255))
save(c, '08_vorteile')

# ---------- 09 Geschenk ----------
c = soft(cover(Image.open(R('geschenkbox.jpg')), W45, H45), 0.97).convert('RGBA')
d = ImageDraw.Draw(c)
spaced(d, (W45 // 2, 70), 'DAS GESCHENK ZUR GEBURT', F(SANS_M, 30), (255, 255, 255), 5, 'm')
L = logo(190, (255, 255, 255)); c.alpha_composite(L, ((W45 - L.width) // 2, H45 - 120))
save(c, '09_weihnachten_geschenk')
