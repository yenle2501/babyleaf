"""Anzeigen und Shopify-Hauptbilder fuer die Kampagne «Weihnachts-Geschenkbox» (Schenkende: Gotti, Goetti, Grosseltern).

Vorbild (Pinterest-Pin der Nutzerin): offene Geschenkbox auf weissem Grund, zerknuelltes Seidenpapier, die Teile von
Hand locker hineingelegt, keine Deko. Deshalb sind die Anzeigen ruhig: Foto gross, darunter in kleiner Schrift Name,
Inhalt und Preis, kein Verlauf, kein grosser Button. Die Fotos sind mit Canva-KI aus dem Box-Foto der Nutzerin und
den Shop-Bildern der Sets erzeugt (`posts/kampagne-weihnachtsbox/fotos/`).

Je Box: 4:5 (1080x1350, Feed), 1:1 (1080x1080, Karussell), 9:16 (1080x1920, Storys) und Shopify-Hauptbild
(2048x2048, Logo oben links). Dazu eine Uebersicht aller Boxen (4:5). Preise: `strategie/preiskalkulation-weihnachtsbox.md`.

Aufruf: python3 make_weihnachtsbox.py <fotos-ordner> <ausgabe-ordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1:3]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
WALD, GRAU = (35, 48, 41), (110, 112, 106)

# (Datei, Name, Inhalt, Preis)
BOXEN = [('box_mum_dad_me', '«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90'),
         ('box_lovely_little_girl', '«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90'),
         ('box_growing_up_strong', '«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('box_i_love_my_mummy', '«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90'),
         ('box_dino', '«Dino»', '3 Bodys + 3 Mulltücher', '39.90'),
         ('box_dinosaur', '«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('box_little_one', '«Little One»', '5 Bodys + 3 Mulltücher', '44.90'),
         ('box_i_like_flying', '«I like flying»', '3 Bodys + 5 Leggings', '39.90'),
         ('box_little_one_jogginghosen', '«Little One»', '5 Bodys + 5 Jogginghosen', '42.90')]
TITEL = 'Weihnachts-Geschenkbox'


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def leinwand(im, W, H, h, y, f=60):
    """Foto auf Hoehe h skaliert bei y einsetzen. Der Grund ist ein weicher Verlauf aus den vier Bildecken (dort ist
    nur der weisse Studio-Grund), so laeuft er nahtlos bis an den Rand weiter, ohne Rosa von der Box."""
    a = np.asarray(im).astype(float); k = 40
    ecken = np.array([[np.median(a[:k, :k].reshape(-1, 3), 0), np.median(a[:k, -k:].reshape(-1, 3), 0)],
                      [np.median(a[-k:, :k].reshape(-1, 3), 0), np.median(a[-k:, -k:].reshape(-1, 3), 0)]])
    ty, tx = np.linspace(0, 1, H)[:, None, None], np.linspace(0, 1, W)[None, :, None]
    g = (ecken[0, 0] * (1 - tx) + ecken[0, 1] * tx) * (1 - ty) + (ecken[1, 0] * (1 - tx) + ecken[1, 1] * tx) * ty
    c = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    w = round(im.width * h / im.height); t = im.resize((w, h), Image.LANCZOS)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rectangle([f, f, w - f, h - f], fill=255)
    c.paste(t, ((W - w) // 2, y), m.filter(ImageFilter.GaussianBlur(f / 2)))
    return c


def zeilen(d, W, y, box, k=1.0):
    _, name, inhalt, preis = box
    d.text((W / 2, y), f'{TITEL} {name}', font=FONT('fraunces-600.ttf', 40 * k), fill=WALD, anchor='ms')
    d.text((W / 2, y + 50 * k), f'{inhalt}  ·  fertig verpackt  ·  CHF {preis}', font=FONT('nunitosans-600.ttf', 27 * k), fill=GRAU, anchor='ms')


def foto(box):
    return Image.open(os.path.join(src, box[0] + '.jpg')).convert('RGB')


def feed(box, W=1080, H=1350):
    c = leinwand(foto(box), W, H, 1215, 0); d = ImageDraw.Draw(c)
    zeilen(d, W, H - 82, box)
    return c


def quadrat(box, W=1080, H=1080):
    c = leinwand(foto(box), W, H, 960, 0); d = ImageDraw.Draw(c)
    zeilen(d, W, H - 66, box, 0.9)
    return c


def story(box, W=1080, H=1920):
    """9:16: oben 14 % und unten 20 % frei von wichtigem Inhalt (Instagram-Bedienelemente)."""
    c = leinwand(foto(box), W, H, 1300, 300); d = ImageDraw.Draw(c)
    d.text((W / 2, 250), TITEL, font=FONT('fraunces-600.ttf', 50), fill=WALD, anchor='ms')
    d.text((W / 2, 1660), box[1], font=FONT('fraunces-600.ttf', 44), fill=WALD, anchor='ms')
    d.text((W / 2, 1712), f'{box[2]}  ·  fertig verpackt  ·  CHF {box[3]}', font=FONT('nunitosans-600.ttf', 29), fill=GRAU, anchor='ms')
    return c


def shopify(box, N=2048):
    """Quadratisches Hauptbild wie die uebrigen Shop-Hauptbilder: Box mittig, Logo oben links (Position wie
    `hauptbild_logo.py`)."""
    c = leinwand(foto(box), N, N, int(N * 0.97), int(N * 0.015), f=90)
    L = load_logo(int(N * 0.198), (122, 108, 104)); c.paste(L, (int(N * 0.035), int(N * 0.031)), L)
    return c


def uebersicht(W=1080, H=1350):
    """Alle Boxen im Raster mit 2 Spalten fuer eine Kollektions-Anzeige."""
    im0 = foto(BOXEN[0])
    c = leinwand(im0, W, H, H, 0); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, H], fill=(244, 242, 239))
    d.text((W / 2, 92), TITEL + 'en', font=FONT('fraunces-600.ttf', 52), fill=WALD, anchor='ms')
    d.text((W / 2, 140), 'Ganze Sets, von Hand eingepackt  ·  ab CHF 29.90', font=FONT('nunitosans-600.ttf', 27), fill=GRAU, anchor='ms')
    g, oben = 12, 172
    reihen = (len(BOXEN) + 1) // 2
    kw = (W - 3 * g) // 2; kh = (H - oben - (reihen + 1) * g) // reihen
    f = FONT('nunitosans-700.ttf', 22)
    for i, box in enumerate(BOXEN):
        x, y = g + (i % 2) * (kw + g), oben + (i // 2) * (kh + g)
        im = foto(box); s = kw / im.width
        im = im.resize((kw, round(im.height * s)), Image.LANCZOS)
        oy = int(im.height * 0.5 - kh / 2)
        c.paste(im.crop((0, oy, kw, oy + kh)), (x, y))
        t = f'{box[1]}  CHF {box[3]}'; w = d.textlength(t, font=f) + 28
        d.rounded_rectangle([x + 10, y + kh - 44, x + 10 + w, y + kh - 10], radius=17, fill=(255, 255, 255))
        d.text((x + 24, y + kh - 27), t, font=f, fill=WALD, anchor='lm')
    return c


if __name__ == '__main__':
    for fmt in ('4x5', '1x1', '9x16', 'shopify'):
        os.makedirs(os.path.join(out, fmt), exist_ok=True)
    for box in BOXEN:
        n = box[0]
        feed(box).save(os.path.join(out, '4x5', f'{n}_4x5.jpg'), quality=94)
        quadrat(box).save(os.path.join(out, '1x1', f'{n}_1x1.jpg'), quality=94)
        story(box).save(os.path.join(out, '9x16', f'{n}_9x16.jpg'), quality=94)
        shopify(box).save(os.path.join(out, 'shopify', f'geschenkbox-{n[4:].replace("_", "-")}.jpg'), quality=95)
        print(n)
    uebersicht().save(os.path.join(out, '4x5', 'alle_boxen_4x5.jpg'), quality=94)
