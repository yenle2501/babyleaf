"""Werbebilder (Meta/Instagram/Pinterest) für die Weihnachts-Geschenkboxen in der roten sunnozy-Box, mit Preis.

    python3 tools/make_rote_box_ads.py

Grundlage: `rote-box/komposit/<box>.jpg` aus make_rote_box.py (Box von oben, Deckel mit sunnozy-Band, Karte).
Schrift Fraunces + Nunito Sans (keine Schreibschrift). Preise wie im Shop (BOXEN unten, Stand 01.11.2026).
Ausgabe in `rote-box/ads/`: feed_<box>_4x5.jpg (1080 × 1350), quadrat_<box>_1x1.jpg (1080 × 1080),
story_<box>_9x16.jpg (1080 × 1920, oben und unten frei für die Instagram-Bedienelemente) und uebersicht_4x5.jpg.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RB = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox', 'rote-box')
OUT = os.path.join(RB, 'ads')
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
DUNKEL, GRAU, ROT = (44, 36, 34), (112, 104, 100), (168, 24, 32)

# (Datei, Name, Inhalt, Preis)
BOXEN = [('mum_dad_me', '«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90'),
         ('lovely_little_girl', '«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90'),
         ('growing_up_strong', '«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('i_love_my_mummy', '«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90'),
         ('dino', '«Dino»', '3 Bodys + 3 Mulltücher', '39.90'),
         ('dinosaur', '«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('little_one', '«Little One»', '5 Bodys + 3 Mulltücher', '44.90'),
         ('i_like_flying', '«I like flying»', '3 Bodys + 5 Leggings', '39.90'),
         ('little_one_jogginghosen', '«Little One»', '5 Bodys + 5 Jogginghosen', '42.90')]


def hintergrund(im, W, H):
    """Hellgrauer Studiohintergrund in der Farbe der Bildränder, leicht nach unten heller."""
    a = np.asarray(im).astype(float)
    oben, unten = a[:6].reshape(-1, 3).mean(0), a[-6:].reshape(-1, 3).mean(0)
    t = np.linspace(0, 1, H)[:, None, None]
    return Image.fromarray(((1 - t) * oben + t * unten).repeat(W, 1).clip(0, 255).astype(np.uint8))


def einsetzen(c, im, breite, y):
    """Box-Foto mit weich auslaufenden Rändern einsetzen (kein sichtbarer Bildrand)."""
    h = round(im.height * breite / im.width); im = im.resize((breite, h), Image.LANCZOS)
    m = Image.new('L', (breite, h), 0); ImageDraw.Draw(m).rectangle((44, 44, breite - 44, h - 44), fill=255)
    c.paste(im, ((c.width - breite) // 2, y), m.filter(ImageFilter.GaussianBlur(30)))
    return h


def gesperrt(d, cx, y, text, font, farbe, sp):
    b = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = cx - b / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=farbe, anchor='ls'); x += d.textlength(ch, font=font) + sp


def textblock(d, cx, y, box, k=1.0):
    """Kicker, Name, Inhalt, Preis. y = Grundlinie des Kickers. Gibt die untere Kante zurück."""
    _, name, inhalt, preis = box
    gesperrt(d, cx, y, 'WEIHNACHTS-GESCHENKBOX', F('nunitosans-700.ttf', 25 * k), ROT, 5 * k)
    d.text((cx, y + 72 * k), name, font=F('fraunces-400.ttf', 62 * k), fill=DUNKEL, anchor='ms')
    d.text((cx, y + 120 * k), f'{inhalt}  ·  fertig verpackt mit Karte', font=F('nunitosans-600.ttf', 28 * k), fill=GRAU, anchor='ms')
    d.text((cx, y + 196 * k), f'CHF {preis}', font=F('fraunces-600.ttf', 64 * k), fill=ROT, anchor='ms')
    return y + 196 * k


def feed(im, box, W=1080, H=1350):
    c = hintergrund(im, W, H); einsetzen(c, im, 960, 6)
    textblock(ImageDraw.Draw(c), W / 2, 1100, box)
    return c


def quadrat(im, box, W=1080, H=1080):
    c = hintergrund(im, W, H); einsetzen(c, im, 760, 0)
    d = ImageDraw.Draw(c); _, name, inhalt, preis = box
    d.text((W / 2, 902), name, font=F('fraunces-400.ttf', 52), fill=DUNKEL, anchor='ms')
    d.text((W / 2, 948), f'{inhalt}  ·  Weihnachts-Geschenkbox', font=F('nunitosans-600.ttf', 25), fill=GRAU, anchor='ms')
    d.text((W / 2, 1022), f'CHF {preis}', font=F('fraunces-600.ttf', 56), fill=ROT, anchor='ms')
    return c


def story(im, box, W=1080, H=1920):
    c = hintergrund(im, W, H); einsetzen(c, im, 1040, 250)
    textblock(ImageDraw.Draw(c), W / 2, 1450, box)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    feeds = []
    for box in BOXEN:
        p = os.path.join(RB, 'komposit', box[0] + '.jpg')
        if not os.path.exists(p):
            print('fehlt noch:', box[0]); continue
        im = Image.open(p).convert('RGB')
        f = feed(im, box); f.save(os.path.join(OUT, f'feed_{box[0]}_4x5.jpg'), quality=93); feeds.append(f)
        quadrat(im, box).save(os.path.join(OUT, f'quadrat_{box[0]}_1x1.jpg'), quality=93)
        story(im, box).save(os.path.join(OUT, f'story_{box[0]}_9x16.jpg'), quality=93)
        print(box[0])
    if feeds:
        n = len(feeds); sp = 3 if n > 4 else n; zl = (n + sp - 1) // sp
        u = Image.new('RGB', (sp * 370 + 10, zl * 460 + 10), 'white')
        for i, f in enumerate(feeds):
            u.paste(f.resize((360, 450)), (10 + (i % sp) * 370, 10 + (i // sp) * 460))
        u.save(os.path.join(OUT, 'uebersicht_4x5.jpg'), quality=88)
