"""Meta-Anzeigen (Facebook/Instagram) fuer die Weihnachts-Geschenkboxen, im Stil der Set-Anzeigen (`make_meta_ads.py`).

Je Box: Karussell-Karte 1:1 (Foto links, rechts schmales Feld mit Logo senkrecht, «FERTIG VERPACKT», «mit
Weihnachtskarte», unten Versandversprechen), Feed 4:5 und Story 9:16 (Foto oben, Feld unten). Oben links das
schwarze Preis-Etikett. Dazu die personalisierte Box («Stell Deine Box selbst zusammen», ohne Preis-Etikett: der Preis
entsteht erst aus der Auswahl der Kundin)
und eine Uebersicht aller Boxen als Einstieg ins Karussell.
Fotos: `posts/kampagne-weihnachtsbox/fotos` (Real-ESRGAN, 2272 px), personalisierte Box: `personalisiert/`.

Aufruf: python3 make_meta_ads_geschenkbox.py <kampagnen-ordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

camp = sys.argv[1]
out = os.path.join(camp, 'meta-ads')
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
FR = lambda s: ImageFont.truetype(os.path.join(ROOT, 'fonts', 'fraunces-600.ttf'), int(s))
IN = lambda w, s: ImageFont.truetype(INTER.format(w), int(s))
PANEL, INK, GRAU, WALD = (240, 226, 224), (17, 17, 17), (110, 106, 101), (35, 48, 41)

# (Datei, Name, Inhalt, Preis)
BOXEN = [('box_mum_dad_me', 'Mum Dad Me', '5 Bodys + 5 Leggings', '42.90'),
         ('box_lovely_little_girl', 'Lovely Little Girl', '3 Bodys + 5 Leggings', '39.90'),
         ('box_growing_up_strong', 'Growing up strong', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('box_i_love_my_mummy', 'I love my Mummy', '3 Bodys + 3 Halstücher', '29.90'),
         ('box_dino', 'Dino', '3 Bodys + 3 Mulltücher', '39.90'),
         ('box_dinosaur', 'Dinosaur', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('box_little_one', 'Little One', '5 Bodys + 3 Mulltücher', '44.90'),
         ('box_i_like_flying', 'I like flying', '3 Bodys + 5 Leggings', '39.90')]


def load_logo(width, col=INK):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def flaeche(im, W, H, foto=True):
    """Foto auf W x H einpassen (ganz sichtbar), Rest mit weichem Verlauf aus den Bildecken, Kanten eingeblendet."""
    a = np.asarray(im).astype(float); k = 40
    e = [np.median(a[:k, :k].reshape(-1, 3), 0), np.median(a[:k, -k:].reshape(-1, 3), 0),
         np.median(a[-k:, :k].reshape(-1, 3), 0), np.median(a[-k:, -k:].reshape(-1, 3), 0)]
    ty, tx = np.linspace(0, 1, H)[:, None, None], np.linspace(0, 1, W)[None, :, None]
    g = (e[0] * (1 - tx) + e[1] * tx) * (1 - ty) + (e[2] * (1 - tx) + e[3] * tx) * ty
    c = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    if not foto:
        return c
    s = min(W / im.width, H / im.height); t = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    f = max(12, int(min(t.size) * 0.035))
    m = Image.new('L', t.size, 0); ImageDraw.Draw(m).rectangle([f, f, t.width - f, t.height - f], fill=255)
    c.paste(t, ((W - t.width) // 2, (H - t.height) // 2), m.filter(ImageFilter.GaussianBlur(f / 2)))
    return c


def badge(c, xy, text, k=1.0):
    if not text:
        return
    d = ImageDraw.Draw(c); f = IN('SemiBold', 44 * k)
    w = d.textlength(text, font=f); x, y = xy; h = 76 * k; pw = 26 * k
    d.rounded_rectangle([x, y, x + w + 2 * pw, y + h], radius=14 * k, fill=INK)
    d.text((x + pw, y + h / 2 + 2 * k), text, font=f, fill='white', anchor='lm')


def panel(c, x0, x1, y0, y1, zeilen=('FERTIG', 'VERPACKT'), klein='mit Weihnachtskarte'):
    d = ImageDraw.Draw(c); d.rectangle([x0, y0, x1, y1], fill=PANEL); pw = x1 - x0
    lg = load_logo(int((y1 - y0) * 0.46)).rotate(-90, expand=True)
    if lg.width > pw * 0.6:
        s = pw * 0.6 / lg.width; lg = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS)
    ly = y0 + int((y1 - y0) * 0.06); c.paste(lg, (int(x0 + (pw - lg.width) / 2), ly), lg)
    ty = ly + lg.height + (y1 - y0) * 0.06
    for z in zeilen:
        d.text((x0 + pw / 2, ty), z, font=IN('Bold', 31), fill=INK, anchor='mt'); ty += 38
    d.text((x0 + pw / 2, ty + 8), klein, font=IN('Regular', 21), fill=GRAU, anchor='mt')
    d.text((x0 + pw / 2, y1 - (y1 - y0) * 0.1), 'GRATISVERSAND', font=IN('Bold', 22), fill=INK, anchor='mm')
    d.text((x0 + pw / 2, y1 - (y1 - y0) * 0.1 + 30), 'ab CHF 50', font=IN('Regular', 21), fill=GRAU, anchor='mm')


def band(c, y0, W, H, titel, unter):
    d = ImageDraw.Draw(c); d.rectangle([0, y0, W, H], fill=PANEL)
    lg = load_logo(230); c.paste(lg, ((W - lg.width) // 2, y0 + 30), lg)
    ty = y0 + 30 + lg.height + 26
    d.text((W / 2, ty), titel, font=FR(42), fill=WALD, anchor='mt')
    d.text((W / 2, ty + 58), unter, font=IN('Regular', 26), fill=GRAU, anchor='mt')
    d.text((W / 2, H - 34), 'GRATISVERSAND AB CHF 50  ·  VERSAND IN 1–2 WERKTAGEN', font=IN('Bold', 22), fill=INK, anchor='ms')


def karte(im, preis, **kw):
    W = H = 1080; split = 760
    c = Image.new('RGB', (W, H)); c.paste(flaeche(im, split, H), (0, 0))
    panel(c, split, W, 0, H, **kw); badge(c, (30, 28), preis)
    return c


def feed(im, preis, titel, unter):
    W, H = 1080, 1350; bh = 290
    c = Image.new('RGB', (W, H)); c.paste(flaeche(im, W, H - bh), (0, 0))
    band(c, H - bh, W, H, titel, unter); badge(c, (36, 32), preis)
    return c


def story(im, preis, titel, unter):
    """9:16: oben 14 % frei (Instagram-Bedienelemente), Feld unten ab ca. 82 %."""
    W, H = 1080, 1920; top, bh = 250, 330
    c = Image.new('RGB', (W, H)); c.paste(flaeche(im, W, H - bh, foto=False), (0, 0))
    c.paste(flaeche(im, W, H - top - bh), (0, top))
    band(c, H - bh, W, H, titel, unter); badge(c, (40, top + 30), preis, 1.05)
    d = ImageDraw.Draw(c)
    d.text((W / 2, 175), 'Weihnachts-Geschenkbox', font=FR(52), fill=WALD, anchor='ms')
    return c


def uebersicht(W=1080, H=1080):
    """Einstiegskarte fuers Karussell: 2 x 2 Boxen, Titel oben."""
    c = Image.new('RGB', (W, H), (246, 241, 238)); d = ImageDraw.Draw(c)
    d.text((W / 2, 78), 'Weihnachts-Geschenkboxen', font=FR(54), fill=WALD, anchor='ms')
    d.text((W / 2, 122), 'Ganze Sets · von Hand verpackt · mit Karte', font=IN('Regular', 26), fill=GRAU, anchor='ms')
    g, oben = 14, 150; kw = (W - 3 * g) // 2; kh = (H - oben - 3 * g - 60) // 2
    for i, n in enumerate(['box_mum_dad_me', 'box_dinosaur', 'box_lovely_little_girl', 'box_little_one']):
        im = Image.open(os.path.join(camp, 'fotos', n + '.jpg')).convert('RGB')
        s = kw / im.width; im = im.resize((kw, round(im.height * s)), Image.LANCZOS)
        oy = (im.height - kh) // 2
        c.paste(im.crop((0, oy, kw, oy + kh)), (g + (i % 2) * (kw + g), oben + (i // 2) * (kh + g)))
    d.text((W / 2, H - 26), 'ab CHF 29.90  ·  GRATISVERSAND AB CHF 50', font=IN('Bold', 26), fill=INK, anchor='ms')
    return c


if __name__ == '__main__':
    for n, name, inhalt, preis in BOXEN:
        im = Image.open(os.path.join(camp, 'fotos', n + '.jpg')).convert('RGB')
        k = n[4:]
        karte(im, f'CHF {preis}').save(os.path.join(out, f'karussell_{k}_1x1.jpg'), quality=94)
        feed(im, f'CHF {preis}', f'Geschenkbox «{name}»', f'{inhalt}  ·  fertig verpackt mit Karte').save(os.path.join(out, f'feed_{k}_4x5.jpg'), quality=94)
        story(im, f'CHF {preis}', f'Geschenkbox «{name}»', f'{inhalt}  ·  mit Weihnachtskarte').save(os.path.join(out, f'story_{k}_9x16.jpg'), quality=94)
        print(k)
    pim = Image.open(os.path.join(camp, 'personalisiert', 'geschenkbox-personalisiert.jpg')).convert('RGB')
    karte(pim, None, zeilen=('DEINE', 'AUSWAHL'), klein='Name + Wunschtext').save(os.path.join(out, 'karussell_personalisiert_1x1.jpg'), quality=94)
    feed(pim, None, 'Stell Deine Box selbst zusammen', 'Sets wählen · Name & Wunschtext auf der Karte').save(os.path.join(out, 'feed_personalisiert_4x5.jpg'), quality=94)
    story(pim, None, 'Stell Deine Box selbst zusammen', 'Sets wählen · Name & Wunschtext').save(os.path.join(out, 'story_personalisiert_9x16.jpg'), quality=94)
    uebersicht().save(os.path.join(out, 'karussell_00_uebersicht_1x1.jpg'), quality=94)
    print('fertig')
