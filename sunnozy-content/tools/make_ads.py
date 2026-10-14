"""Verkaufs-Anzeigen (Meta: Instagram/Facebook) fuer sunnozy.

Preise und Teileanzahl stammen aus dem Shopify-Shop (Stand siehe SHOP unten). Vor dem Schalten pruefen.
Formate: Feed 4:5 (1080x1350), Story/Reel 9:16 (1080x1920).

Aufruf: python3 make_ads.py <ausgabe>
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', out, out, out, out]
exec(src, g)
logo = g['logo']
os.makedirs(out, exist_ok=True)
POSTS = os.path.join(here, '..', 'posts')
P = lambda *a: os.path.join(POSTS, *a)

# Shopify, abgefragt am 14.10.2026
SHOP = {
    'hello_world': ('Erstausstattung «Hello World»', 8, '20.40', 'set_hello_world_blatt'),
    'teddy': ('Erstausstattung «Teddybär»', 8, '21.40', 'set_teddy_creme'),
    'princess': ('Erstausstattung «Princess»', 8, '21.40', 'set_rosa_A'),
    'little_bear': ('Erstausstattung «Hello Little Bear»', 5, '19.40', 'set_little_bear'),
}
AB = '19.40'
USPS = ['Versand aus der Schweiz', 'Gratis ab CHF 50', '14 Tage Rückgabe']

CREAM, SAND, INK, MAUVE, SOFT = (246, 240, 232), (227, 213, 195), (74, 60, 52), (152, 120, 128), (140, 124, 112)
FONTS = os.path.join(here, '..', 'fonts')
SERIF, SERIF_I = os.path.join(FONTS, 'cormorantR.ttf'), os.path.join(FONTS, 'cormorant.ttf')
NUM = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
SANS, SANS_M, SANS_B = ('/usr/share/fonts/opentype/inter/Inter-Regular.otf', '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
                        '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf')
F = lambda p, s: ImageFont.truetype(p, s)


def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.convert('RGB').resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def soft(im):
    im = ImageEnhance.Color(im.convert('RGB')).enhance(0.93)
    a = np.asarray(im).astype(np.float32); a = 8 + a * (245 / 255)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def product(set_png, maxw, maxh):
    im = Image.open(P('marktplatz-galaxus-amazon', 'freigestellt', set_png + '.png')).convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    s = min(maxw / im.width, maxh / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def place(c, piece, xy, op=0.18):
    a = piece.getchannel('A')
    sh = Image.new('L', c.size, 0); sh.paste(a, (xy[0] + 6, xy[1] + 16))
    sh = sh.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * op))
    dark = Image.new('RGBA', c.size, (70, 55, 45, 0)); dark.putalpha(sh)
    c = Image.alpha_composite(c.convert('RGBA'), dark); c.alpha_composite(piece, xy); return c


def ctext(d, cx, y, text, font, fill, track=0):
    w = sum(font.getlength(ch) for ch in text) + track * (len(text) - 1); x = cx - w / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + track


def button(c, cx, y, text, fill=INK, fg=(255, 255, 255), size=34):
    d = ImageDraw.Draw(c); f = F(SANS_B, size)
    w = f.getlength(text) + 110; h = size + 44
    d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + h], h // 2, fill=fill)
    d.text((cx, y + h / 2), text, font=f, fill=fg, anchor='mm')
    return y + h


def pill(c, x, y, text, fill=MAUVE, fg=(255, 255, 255), size=40, anchor='l'):
    d = ImageDraw.Draw(c); f = F(SANS_B, size)
    w = f.getlength(text) + 56; h = size + 30
    x0 = x - w if anchor == 'r' else x - w / 2 if anchor == 'm' else x
    d.rounded_rectangle([x0, y, x0 + w, y + h], h // 2, fill=fill)
    d.text((x0 + w / 2, y + h / 2), text, font=f, fill=fg, anchor='mm')


def usp_bar(c, y, fg=SOFT, size=25):
    d = ImageDraw.Draw(c); W = c.width; f = F(SANS_M, size)
    txt = '   ·   '.join(USPS)
    d.text((W / 2, y), txt, font=f, fill=fg, anchor='mm')


def top_logo(c, y=56, w=230, col=INK):
    L = logo(w, col); c.alpha_composite(L, ((c.width - L.width) // 2, y)) if c.mode == 'RGBA' else c.paste(L, ((c.width - L.width) // 2, y), L)


def save(c, name):
    c.convert('RGB').save(os.path.join(out, name + '.jpg'), quality=94); print(name)


def shade_bottom(c, start=0.55, strength=150):
    W, H = c.size; a = np.zeros((H, W), 'uint8'); y0 = int(H * start)
    a[y0:] = (np.linspace(0, 1, H - y0) ** 1.3 * strength).astype('uint8')[:, None]
    ov = Image.new('RGBA', (W, H), (45, 34, 28, 0)); ov.putalpha(Image.fromarray(a))
    return Image.alpha_composite(c.convert('RGBA'), ov)


# ---------- A01 Produkt-Ad: alles fuer die ersten Wochen ----------
def ad_produkt(key, W, H, name):
    title, n, price, setp = SHOP[key]
    c = Image.new('RGBA', (W, H), CREAM + (255,)); top_logo(c)
    d = ImageDraw.Draw(c)
    hy = 170 if H < 1500 else 300
    ctext(d, W / 2, hy, 'Alles für die', F(SERIF, 78), INK)
    ctext(d, W / 2, hy + 78, 'ersten Wochen.', F(SERIF_I, 78), INK)
    box_h = 700 if H < 1500 else 900
    pr = product(setp, W - 160, box_h)
    c = place(c, pr, ((W - pr.width) // 2, hy + 200 + (box_h - pr.height) // 2))
    d = ImageDraw.Draw(c)
    yb = hy + 200 + box_h + 26
    ctext(d, W / 2, yb, f'{title} · {n} Teile'.upper(), F(SANS_M, 26), SOFT, 2)
    pill(c, W / 2, yb + 50, f'CHF {price}', size=40, anchor='m')
    if H > 1500:
        button(c, W / 2, yb + 190, 'Jetzt shoppen')
        usp_bar(c, H - 90)
    else:
        usp_bar(c, H - 52, size=23)
    save(c, name)


# ---------- A02 Preis pro Teil ----------
def ad_pro_teil(W, H, name):
    title, n, price, setp = SHOP['teddy']
    from decimal import Decimal, ROUND_HALF_UP
    per = (Decimal(price) / n).quantize(Decimal('0.01'), ROUND_HALF_UP)
    c = Image.new('RGBA', (W, H), SAND + (255,)); d = ImageDraw.Draw(c)
    pr = product(setp, 640, 900)
    c = place(c, pr, (W - pr.width - 40, (H - pr.height) // 2 + 40), 0.22)
    d = ImageDraw.Draw(c)
    x = 80
    d.text((x, 150), f'{n} Teile.', font=F(SERIF, 104), fill=INK)
    d.text((x, 265), f'CHF {price}.', font=F(SERIF, 104), fill=INK)
    d.line([(x, 420), (x + 120, 420)], fill=MAUVE, width=3)
    d.text((x, 450), 'Das sind nur', font=F(SANS, 34), fill=INK)
    d.text((x, 495), f'CHF {per} pro Teil.', font=F(SANS_B, 40), fill=INK)
    for i, t in enumerate(['100 % Baumwolle', title.replace('Erstausstattung ', 'Set ')]):
        d.text((x, 600 + i * 48), '–  ' + t, font=F(SANS, 30), fill=INK)
    button(c, x + 190, H - 270, 'Jetzt shoppen')
    L = logo(200, INK); c.alpha_composite(L, (x, H - 140))
    save(c, name)


# ---------- A03 Was ist drin? ----------
def ad_was_drin(W, H, name):
    title, n, price, setp = SHOP['princess']
    items = ['Decke', 'Strampler', 'Body', 'Mütze', 'Fäustlinge', 'Socken', 'Rassel', 'Lätzchen']
    c = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(c)
    ctext(d, W / 2, 60, 'WAS IST DRIN?', F(SANS_B, 30), MAUVE, 5)
    ctext(d, W / 2, 110, title.replace('Erstausstattung ', 'Set '), F(SERIF, 74), INK)
    pr = product(setp, 980, 760)
    c = place(c, pr, ((W - pr.width) // 2, 230 + (760 - pr.height) // 2))
    d = ImageDraw.Draw(c)
    y0 = 1020; f = F(SANS, 30)
    for i, t in enumerate(items):
        cx = 95 + (i % 4) * 250; yy = y0 + (i // 4) * 62
        d.ellipse([cx - 22, yy, cx + 22, yy + 44], fill=SAND); d.text((cx, yy + 22), str(i + 1), font=F(SANS_B, 24), fill=INK, anchor='mm')
        d.text((cx + 34, yy + 22), t, font=f, fill=INK, anchor='lm')
    pill(c, W / 2, 1170, f'{n} Teile · CHF {price}', fill=INK, size=34, anchor='m')
    usp_bar(c, H - 46, size=22)
    save(c, name)


# ---------- A04 Lifestyle + Preis (Weihnachten, Teddybaer) ----------
def ad_lifestyle(photo, W, H, name, head, sub, key=None, ay=0.4):
    c = shade_bottom(soft(cover(Image.open(photo), W, H, ay)), 0.45, 195)
    d = ImageDraw.Draw(c)
    L = logo(190, (255, 255, 255)); c.alpha_composite(L, ((W - L.width) // 2, 50))
    yb = H - (520 if H > 1500 else 420)
    for i, t in enumerate(head.split('\n')):
        ctext(d, W / 2, yb + i * 80, t, F(SERIF, 78), (255, 255, 255))
    yb += 80 * len(head.split('\n')) + 20
    if key:
        title, n, price, _ = SHOP[key]
        ctext(d, W / 2, yb, f'{title} · {n} Teile · CHF {price}'.upper(), F(SANS_M, 25), (255, 255, 255), 1)
    elif sub:
        ctext(d, W / 2, yb, sub.upper(), F(SANS_M, 25), (255, 255, 255), 2)
    button(c, W / 2, yb + 60, 'Jetzt shoppen', fill=(255, 255, 255), fg=INK)
    if H > 1500:
        usp_bar(c, H - 90, fg=(255, 255, 255))
    save(c, name)


# ---------- A09 Kollektion 2x2 ----------
def ad_kollektion(W, H, name):
    c = Image.new('RGBA', (W, H), CREAM + (255,)); top_logo(c, 50, 210)
    d = ImageDraw.Draw(c)
    ty = 150 if H < 1500 else 260
    ctext(d, W / 2, ty, 'Erstausstattungs-Sets', F(SERIF, 70), INK)
    ctext(d, W / 2, ty + 85, f'AB CHF {AB} · 100 % BAUMWOLLE', F(SANS_M, 26), SOFT, 3)
    keys = ['hello_world', 'teddy', 'princess', 'little_bear']
    cw, ch, gap = (470, 470, 20) if H > 1500 else (400, 400, 24)
    gy = ty + 150
    for i, k in enumerate(keys):
        title, n, price, setp = SHOP[k]
        x = (W - 2 * cw - gap) // 2 + (i % 2) * (cw + gap); y = gy + (i // 2) * (ch + (100 if H > 1500 else 92))
        d.rounded_rectangle([x, y, x + cw, y + ch], 24, fill=(255, 255, 255))
        pr = product(setp, cw - 50, ch - 50); c.alpha_composite(pr, (x + (cw - pr.width) // 2, y + (ch - pr.height) // 2))
        d = ImageDraw.Draw(c)
        d.text((x + 6, y + ch + 14), title.replace('Erstausstattung ', ''), font=F(SANS_M, 26), fill=INK)
        d.text((x + 6, y + ch + 50), f'{n} Teile · CHF {price}', font=F(SANS, 24), fill=SOFT)
    if H > 1500:
        button(c, W / 2, gy + 2 * (ch + 100) + 40, 'Jetzt shoppen')
        usp_bar(c, H - 90)
    save(c, name)


F45, F916 = (1080, 1350), (1080, 1920)
ad_produkt('hello_world', *F45, 'A01_alles_fuer_die_ersten_wochen_4x5')
ad_produkt('hello_world', *F916, 'A01_alles_fuer_die_ersten_wochen_9x16')
ad_pro_teil(*F45, 'A02_preis_pro_teil_4x5')
ad_was_drin(*F45, 'A03_was_ist_drin_4x5')
ad_lifestyle(P('paket-7-werbung', 'roh', 'weihnachten_baby.jpg'), *F45, 'A04_erstes_weihnachten_4x5', 'Das erste\nWeihnachten.', None, 'teddy', 0.3)
ad_lifestyle(P('paket-7-werbung', 'roh', 'weihnachten_baby.jpg'), *F916, 'A04_erstes_weihnachten_9x16', 'Das erste\nWeihnachten.', None, 'teddy', 0.3)
ad_lifestyle(P('paket-9-ads', 'roh', 'mama_arm.jpg'), *F45, 'A05_weich_auf_der_haut_4x5', 'Weich auf der Haut.\nSanft vom ersten Tag.', '100 % Baumwolle · sunnozy.ch', None, 0.3)
ad_lifestyle(P('paket-9-ads', 'roh', 'kliniktasche.jpg'), *F45, 'A06_kliniktasche_4x5', 'Kliniktasche\nschon gepackt?', f'Erstausstattungs-Sets ab CHF {AB}', None, 0.35)
ad_lifestyle(P('paket-9-ads', 'roh', 'geschenk_auspacken.jpg'), *F45, 'A07_geschenk_zur_geburt_4x5', 'Das Geschenk\nzur Geburt.', f'Sets ab CHF {AB} · Versand aus der Schweiz', None, 0.3)
ad_lifestyle(P('paket-9-ads', 'roh', 'kinderwagen.jpg'), *F45, 'A08_schweizer_shop_4x5', 'Aus der Schweiz.\nFür die Kleinsten.', 'Gratis Versand ab CHF 50', None, 0.45)
ad_kollektion(*F45, 'A09_kollektion_4x5')
ad_kollektion(*F916, 'A09_kollektion_9x16')
