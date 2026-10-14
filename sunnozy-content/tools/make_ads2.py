"""Verkaufs-Anzeigen (Meta) fuer die echten sunnozy-Produkte aus dem Shop (Bodys, Kombi, Halstuecher, Mulltuecher).

Produktbilder: Fotos der Nutzerin, freigestellt in posts/paket-10-produkte/teile/.
Lifestyle: KI-Fotos in posts/paket-10-produkte/roh/. Echtes Handyfoto: posts/paket-10-produkte/original/.
Preise aus Shopify (abgefragt am 14.10.2026), vor dem Schalten pruefen.
Nutzt die Bausteine aus make_ads.py (cover, soft, place, ctext, button, pill, usp_bar, shade_bottom ...).

Aufruf: python3 make_ads2.py <ausgabe>
"""
import sys, os
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
g = {'__file__': os.path.join(here, 'make_ads.py')}
sys.argv = ['x', out]
exec(open(os.path.join(here, 'make_ads.py')).read().split('# ---------- A01')[0], g)
globals().update({k: g[k] for k in ['logo', 'cover', 'soft', 'place', 'ctext', 'button', 'pill', 'usp_bar', 'shade_bottom', 'save',
                                    'F', 'SERIF', 'SERIF_I', 'SANS', 'SANS_M', 'SANS_B', 'CREAM', 'SAND', 'INK', 'MAUVE', 'SOFT', 'P']})
PK = lambda *a: P('paket-10-produkte', *a)
WHITE = (255, 255, 255)
LILA = (232, 222, 238)

# Shopify, 14.10.2026: (Anzeigename, Inhalt, Preis, Stueckzahl fuer "pro Teil")
SHOP = {
    'kombi': ('Kombi-Set «Mum Dad Me»', '5 Bodys + 5 Leggings', '32.10', 10),
    'mumdadme': ('Body-Set «Mum Dad Me»', '5 Langarm-Bodys', '14.70', 5),
    'flying': ('Body-Set «I Like Flying»', '3 Langarm-Bodys', '12.30', 3),
    'lovely': ('Body-Set «Lovely Little Girl»', '3 Langarm-Bodys', '12.30', 3),
    'mummy': ('Body-Set «I Love My Mummy»', '3 Langarm-Bodys', '12.30', 3),
    'halstuch': ('Halstücher «I Love My Mummy»', '3 Halstücher', '7.99', 3),
    'little_one': ('Body-Set «Little One»', '5 gerippte Bodys', '14.70', 5),
    'mull': ('Mulltücher & Nuscheli', '3er-Set, Musselin', '13.40', 3),
}


def per(key):
    _, _, price, n = SHOP[key]
    return (Decimal(price) / n).quantize(Decimal('0.01'), ROUND_HALF_UP)


def teil(name, maxw, maxh, rot=0):
    im = Image.open(PK('teile', name + '.png')).convert('RGBA')
    if rot:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    im = im.crop(im.getchannel('A').getbbox())
    s = min(maxw / im.width, maxh / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def handyfoto():
    """Echtes Foto der Nutzerin: Boden mit fremder Einkaufstasche links unten durch Tischflaeche ersetzen."""
    im = Image.open(PK('original', 'mumdadme_kombi_handyfoto.jpg')).convert('RGB')
    W, H = im.size; a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    # Tischkante: Linie von (0, 960) nach (540, H); links davon = Boden
    edge_x = (yy - 960) * 540 / (H - 960)
    m = ((xx < edge_x + 18) & (yy > 940)).astype(np.float32)
    m = np.asarray(Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(10))) / 255.0
    # Tischfarbe zeilenweise rechts der Kante abgreifen
    ref = np.zeros_like(a)
    for y in range(H):
        x0 = int(min(W - 40, max(0, (y - 960) * 540 / (H - 960)) + 60))
        ref[y] = np.median(a[y, x0:x0 + 30], axis=0)
    ref = np.asarray(Image.fromarray(ref.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(25))).astype(np.float32)
    noise = np.random.default_rng(1).normal(0, 1.6, a.shape)
    a = a * (1 - m[..., None]) + (ref + noise) * m[..., None]
    return Image.fromarray(a.clip(0, 255).astype('uint8'))


def lifestyle(photo, W, H, name, head, sub, ay=0.4, tag=None):
    c = shade_bottom(soft(cover(photo if isinstance(photo, Image.Image) else Image.open(photo), W, H, ay)), 0.45, 200)
    d = ImageDraw.Draw(c)
    L = logo(190, WHITE); c.alpha_composite(L, ((W - L.width) // 2, 50))
    if tag:
        pill(c, W / 2, 140, tag, fill=(255, 255, 255), fg=INK, size=26, anchor='m')
    lines = head.split('\n')
    yb = H - (560 if H > 1500 else 400) - 80 * (len(lines) - 1)
    d = ImageDraw.Draw(c)
    for i, t in enumerate(lines):
        ctext(d, W / 2, yb + i * 80, t, F(SERIF, 78), WHITE)
    yb += 80 * len(lines) + 18
    for i, s in enumerate(sub if isinstance(sub, list) else [sub]):
        ctext(d, W / 2, yb + i * 40, s.upper(), F(SANS_M, 25), WHITE, 1.5)
    yb += 40 * len(sub if isinstance(sub, list) else [sub]) + 16
    button(c, W / 2, yb, 'Jetzt shoppen', fill=WHITE, fg=INK)
    if H > 1500:
        usp_bar(c, H - 90, fg=WHITE)
    save(c, name)


def price_block(c, x, y, key, align='l', big=96):
    title, inhalt, price, n = SHOP[key]
    d = ImageDraw.Draw(c)
    anc = {'l': 'la', 'm': 'ma'}[align]
    d.text((x, y), f'CHF {price}', font=F(SANS_B, big), fill=INK, anchor=anc)
    d.text((x, y + big + 16), f'nur CHF {per(key)} pro {"Teil" if key == "kombi" else "Stück" if key in ("mull", "halstuch") else "Body"}',
           font=F(SANS_M, 32), fill=MAUVE, anchor=anc)


# ---------- B01 Echtes Foto: so kommt das Kombi-Set an ----------
def ad_echt(W, H, name):
    c = shade_bottom(cover(handyfoto(), W, H, 0.35), 0.5, 215)
    pill(c, 50, 50, 'ECHTES FOTO · UNSER PRODUKT', fill=WHITE, fg=INK, size=24)
    d = ImageDraw.Draw(c)
    title, inhalt, price, _ = SHOP['kombi']
    yb = H - (560 if H > 1500 else 430)
    ctext(d, W / 2, yb, 'So kommt es bei dir an.', F(SERIF, 74), WHITE)
    ctext(d, W / 2, yb + 96, f'{title} · {inhalt}'.upper(), F(SANS_M, 25), WHITE, 1.5)
    ctext(d, W / 2, yb + 140, f'CHF {price} · NUR CHF {per("kombi")} PRO TEIL', F(SANS_B, 30), WHITE, 1.5)
    button(c, W / 2, yb + 200, 'Jetzt shoppen', fill=WHITE, fg=INK)
    if H > 1500:
        usp_bar(c, H - 90, fg=WHITE)
    L = logo(170, WHITE); c.alpha_composite(L, (W - L.width - 50, 62))
    save(c, name)


# ---------- Foto oben, Creme-Feld unten (Text verdeckt das Produkt nicht) ----------
def panel(photo, W, H, PH, name, head, sub, ay=0.4, tag=None):
    c = Image.new('RGBA', (W, H), CREAM + (255,))
    ph = photo if isinstance(photo, Image.Image) else Image.open(photo)
    c.paste(soft(cover(ph, W, PH, ay)).convert('RGBA'), (0, 0))
    L = logo(180, WHITE); sh = L.getchannel('A').filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.35))
    dark = Image.new('RGBA', L.size, (40, 30, 25, 0)); dark.putalpha(sh)
    lx = (W - L.width) // 2
    c.alpha_composite(dark, (lx, 46)); c.alpha_composite(L, (lx, 44))
    if tag:
        pill(c, 40, PH - 80, tag, fill=WHITE, fg=INK, size=24)
    d = ImageDraw.Draw(c)
    lines = head.split('\n'); y = PH + 34
    for i, t in enumerate(lines):
        ctext(d, W / 2, y + i * 70, t, F(SERIF, 66), INK)
    y += 70 * len(lines) + 14
    for i, t in enumerate(sub):
        ctext(d, W / 2, y + i * 38, t.upper(), F(SANS_M if i == 0 else SANS_B, 24 if i == 0 else 28), INK if i else SOFT, 1.5)
    y += 38 * len(sub) + 18
    button(c, W / 2, y, 'Jetzt shoppen', size=30)
    if H - (y + 74) > 90:
        usp_bar(c, H - 60, size=23)
    save(c, name)


# ---------- B03 Produkt-Trio mit Preis (I Like Flying) ----------
def ad_trio(W, H, name, key, teile, bg, head):
    title, inhalt, price, _ = SHOP[key]
    c = Image.new('RGBA', (W, H), bg + (255,)); d = ImageDraw.Draw(c)
    L = logo(210, INK); c.alpha_composite(L, ((W - L.width) // 2, 50))
    ty = 150 if H < 1500 else 270
    ctext(d, W / 2, ty, head, F(SERIF_I, 76), INK)
    ctext(d, W / 2, ty + 100, f'{title} · {inhalt}'.upper(), F(SANS_M, 25), SOFT, 2)
    box_y, box_h = ty + 160, (640 if H < 1500 else 860)
    tops = []
    n = len(teile); bw = (W - 80) / n * 1.2
    for i, (t, rot) in enumerate(teile):
        pr = teil(t, bw, box_h, rot)
        cx = 40 + (W - 80) / n * (i + 0.5)
        dy = 30 if i % 2 else 0
        tops.append(int(box_y + (box_h - pr.height) / 2 + dy) + pr.height)
        c = place(c, pr, (int(cx - pr.width / 2), int(box_y + (box_h - pr.height) / 2 + dy)), 0.2)
    yb = max(tops) + (50 if H < 1500 else 90)
    price_block(c, W / 2, yb, key, 'm', 84)
    if H > 1500:
        button(c, W / 2, yb + 210, 'Jetzt shoppen')
        usp_bar(c, H - 90)
    else:
        usp_bar(c, H - 50, size=23)
    save(c, name)


# ---------- B07 Duo: Body-Set + Halstuecher ----------
def ad_duo(W, H, name):
    c = Image.new('RGBA', (W, H), SAND + (255,)); d = ImageDraw.Draw(c)
    L = logo(210, INK); c.alpha_composite(L, ((W - L.width) // 2, 50))
    ctext(d, W / 2, 150, 'I love my Mummy', F(SERIF_I, 80), INK)
    ctext(d, W / 2, 252, 'DAS PASST ZUSAMMEN', F(SANS_M, 26), SOFT, 4)
    for i, (k, t, mw, mh) in enumerate([('mummy', 'mummy_3er', 560, 520), ('halstuch', 'halstuecher_mummy', 420, 420)]):
        x0 = 40 + i * 540; cw = 500
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([x0, 330, x0 + cw, 880], 28, fill=CREAM)
        pr = teil(t, cw - 50, 470)
        c = place(c, pr, (x0 + (cw - pr.width) // 2, 330 + (550 - pr.height) // 2), 0.15)
        d = ImageDraw.Draw(c)
        title, inhalt, price, _ = SHOP[k]
        d.text((x0 + cw / 2, 915), inhalt, font=F(SANS_M, 32), fill=INK, anchor='ma')
        d.text((x0 + cw / 2, 965), f'CHF {price}', font=F(SANS_B, 52), fill=INK, anchor='ma')
    d.text((W / 2, 1075), 'Bodys & Halstücher passend zueinander', font=F(SANS, 30), fill=INK, anchor='ma')
    button(c, W / 2, 1140, 'Jetzt shoppen')
    usp_bar(c, H - 46, size=22)
    save(c, name)


# ---------- B09 Preis pro Body (Little One) ----------
def ad_pro_body(W, H, name, key, t):
    title, inhalt, price, n = SHOP[key]
    c = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(c)
    pr = teil(t, 560, 760)
    c = place(c, pr, (W - pr.width - 60, (H - pr.height) // 2 + 30), 0.2)
    d = ImageDraw.Draw(c); x = 80
    d.text((x, 160), f'{n} Bodys.', font=F(SERIF, 104), fill=INK)
    d.text((x, 275), f'CHF {price}.', font=F(SERIF, 104), fill=INK)
    d.line([(x, 430), (x + 120, 430)], fill=MAUVE, width=3)
    d.text((x, 460), 'Das sind nur', font=F(SANS, 34), fill=INK)
    d.text((x, 505), f'CHF {per(key)} pro Body.', font=F(SANS_B, 40), fill=INK)
    for i, s in enumerate([title.replace('Body-Set ', 'Set '), 'gerippt, weich', 'Druckknöpfe im Schritt']):
        d.text((x, 610 + i * 48), '–  ' + s, font=F(SANS, 30), fill=INK)
    button(c, x + 190, H - 270, 'Jetzt shoppen')
    L = logo(200, INK); c.alpha_composite(L, (x, H - 140))
    save(c, name)


# ---------- B10 Kollektion Langarm-Bodys ----------
def ad_bodys(W, H, name):
    items = [('flying_vogel', 'I Like Flying', 'flying'), ('lovely_lila', 'Lovely Little Girl', 'lovely'),
             ('mumdadme_body', 'Mum Dad Me', 'mumdadme'), ('flying_eis_rosa', 'I Like Flying', 'flying'),
             ('lovely_herzen', 'Lovely Little Girl', 'lovely'), ('little_one', 'Little One', 'little_one')]
    c = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(c)
    L = logo(200, INK); c.alpha_composite(L, ((W - L.width) // 2, 46))
    ty = 140 if H < 1500 else 250
    ctext(d, W / 2, ty, 'Langarm-Bodys', F(SERIF, 72), INK)
    ctext(d, W / 2, ty + 90, 'SETS AB CHF 12.30 · VERSAND AUS DER SCHWEIZ', F(SANS_M, 24), SOFT, 2)
    cw, gap = 310, 22
    ch = 300 if H < 1500 else 380
    lab = 82
    gy = ty + 150
    for i, (t, lbl, k) in enumerate(items):
        x = (W - 3 * cw - 2 * gap) // 2 + (i % 3) * (cw + gap); y = gy + (i // 3) * (ch + lab + 14)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([x, y, x + cw, y + ch], 22, fill=WHITE)
        pr = teil(t, cw - 40, ch - 36); c.alpha_composite(pr, (x + (cw - pr.width) // 2, y + (ch - pr.height) // 2))
        d = ImageDraw.Draw(c)
        _, inhalt, price, _ = SHOP[k]
        d.text((x + 6, y + ch + 12), lbl, font=F(SANS_M, 25), fill=INK)
        d.text((x + 6, y + ch + 46), f'{inhalt.split()[0]}er-Set · CHF {price}', font=F(SANS, 23), fill=SOFT)
    yb = gy + 2 * (ch + lab + 14) + 10
    if H > 1500:
        button(c, W / 2, yb + 40, 'Jetzt shoppen')
        usp_bar(c, H - 90)
    else:
        usp_bar(c, H - 46, size=22)
    save(c, name)


F45, F916 = (1080, 1350), (1080, 1920)
R = lambda n: PK('roh', n)
ad_echt(*F45, 'B01_echtes_foto_kombi_4x5')
panel(handyfoto(), *F916, 1440, 'B01_echtes_foto_kombi_9x16', 'So kommt es bei dir an.',
      [f'{SHOP["kombi"][0]} · {SHOP["kombi"][1]}', f'CHF {SHOP["kombi"][2]} · nur CHF {per("kombi")} pro Teil'], 0.5, 'ECHTES FOTO · UNSER PRODUKT')
lifestyle(R('mumdadme_bett.jpg'), *F45, 'B02_mum_dad_me_4x5', 'Mum. Dad. Me.',
          [f'{SHOP["kombi"][0]} · {SHOP["kombi"][1]}', f'CHF {SHOP["kombi"][2]}'], 0.25)
lifestyle(R('mumdadme_bett.jpg'), *F916, 'B02_mum_dad_me_9x16', 'Mum. Dad. Me.',
          [f'{SHOP["kombi"][0]} · {SHOP["kombi"][1]}', f'CHF {SHOP["kombi"][2]}'], 0.25)
ad_trio(*F45, 'B03_i_like_flying_4x5', 'flying', [('flying_eis_creme', 6), ('flying_vogel', 0), ('flying_eis_rosa', -6)], LILA, 'Kleine Vögelchen.')
ad_trio(*F916, 'B03_i_like_flying_9x16', 'flying', [('flying_eis_creme', 6), ('flying_vogel', 0), ('flying_eis_rosa', -6)], LILA, 'Kleine Vögelchen.')
lifestyle(R('flying_spielmatte.jpg'), *F45, 'B04_spielmatte_flying_4x5', 'Bunt, weich\nund gut gelaunt.',
          [f'{SHOP["flying"][0]} · {SHOP["flying"][1]}', f'CHF {SHOP["flying"][2]}'], 0.3)
lifestyle(R('lovely_korb.jpg'), *F45, 'B05_lovely_little_girl_4x5', 'Lovely Little Girl.',
          [f'{SHOP["lovely"][0].replace("Body-Set ", "Body-Set ")} · {SHOP["lovely"][1]}', f'CHF {SHOP["lovely"][2]}'], 0.3)
panel(R('mummy_mama_arm.jpg'), *F45, 1000, 'B06_i_love_my_mummy_4x5', 'Für die liebste Mama.',
      ['Body-Set «I Love My Mummy» · Halstücher 3er', f'Bodys 3er CHF {SHOP["mummy"][2]} · Halstücher CHF {SHOP["halstuch"][2]}'], 0.55)
ad_duo(*F45, 'B07_mummy_body_halstuch_4x5')
lifestyle(R('mulltuch_newborn.jpg'), *F45, 'B08_mulltuch_4x5', 'Ein Tuch\nfür alles.',
          ['Mulltücher & Nuscheli · 3er-Set · Musselin', f'CHF {SHOP["mull"][2]}'], 0.3)
ad_pro_body(*F45, 'B09_little_one_pro_body_4x5', 'little_one', 'little_one')
ad_bodys(*F45, 'B10_langarm_bodys_4x5')
ad_bodys(*F916, 'B10_langarm_bodys_9x16')
