"""Werbebilder Weihnachts-Geschenkboxen im «Katalog-Flatlay»-Stil (Vorlage der Nutzerin, 03.11.2026: Mode-Anzeige mit
Kleidung flach auf Weinrot, Preisschild oben links, rechts helle Leiste mit Markenname senkrecht).

    python3 tools/make_flatlay_ads.py               # alle Boxen, für die ein Flatlay in rote-box/flatlay/roh/ liegt
    python3 tools/make_flatlay_ads.py dino          # nur eine Box

Flatlay-Fotos: KI (Canva) nach den Set-Fotos aus dem Shop und der roten sunnozy-Box, 3:4 (rote-box/flatlay/roh/<box>.jpg).
Schrift Nunito Sans + Fraunces, keine Schreibschrift, keine fremden Marken, keine Versand-Versprechen.
Ausgabe: rote-box/flatlay/feed_<box>_1x1.jpg (1080 × 1080, Facebook/Instagram-Feed) und story_<box>_9x16.jpg (1080 × 1920).
"""
import os, sys, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FL = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox', 'rote-box', 'flatlay')
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
HELL, SCHWARZ, GRAU = (239, 238, 236), (17, 17, 17), (110, 108, 104)
BOX = {
    'mum_dad_me': ('«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90'),
    'lovely_little_girl': ('«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90'),
    'growing_up_strong': ('«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90'),
    'i_love_my_mummy': ('«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90'),
    'dino': ('«Dino»', '3 Bodys + 3 Mulltücher', '39.90'),
    'dinosaur': ('«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90'),
    'little_one': ('«Little One»', '5 Bodys + 3 Mulltücher', '44.90'),
    'i_like_flying': ('«I like flying»', '3 Bodys + 5 Leggings', '39.90'),
    'little_one_jogginghosen': ('«Little One»', '5 Bodys + 5 Jogginghosen', '42.90'),
}


def preisschild(c, x, y, preis, gross=56):
    d = ImageDraw.Draw(c); fo = F('nunitosans-800.ttf', gross); t = f'CHF {preis}'
    w = d.textlength(t, font=fo); h = gross * 1.05
    d.rounded_rectangle((x, y, x + w + gross * 0.7, y + h + gross * 0.45), radius=gross * 0.28, fill=SCHWARZ)
    d.text((x + gross * 0.35, y + gross * 0.2), t, font=fo, fill=(255, 255, 255), anchor='la')


def senkrecht(text, groesse, farbe):
    """Text um 90° gedreht (liest von oben nach unten), freigestellt."""
    fo = F('nunitosans-800.ttf', groesse)
    probe = ImageDraw.Draw(Image.new('L', (1, 1)))
    w = int(probe.textlength(text, font=fo)) + 20; h = int(groesse * 1.25)
    lay = Image.new('L', (w, h), 0); ImageDraw.Draw(lay).text((10, h / 2), text, font=fo, fill=255, anchor='lm')
    lay = lay.crop(lay.getbbox()).rotate(-90, expand=True)
    out = Image.new('RGBA', lay.size, farbe + (0,)); out.putalpha(lay); return out


def foto(key, w, h):
    im = Image.open(glob.glob(os.path.join(FL, 'roh', key + '.*'))[0]).convert('RGB')
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))


def zentriert(d, cx, y, text, fo, farbe):
    d.text((cx, y), text, font=fo, fill=farbe, anchor='ms')


def feed(key):
    name, inhalt, preis = BOX[key]; W = H = 1080
    c = Image.new('RGB', (W, H), HELL)
    pw, ph = 750, 1000; c.paste(foto(key, pw, ph), (0, 40))
    preisschild(c, 26, 66, preis)
    cx = pw + (W - pw) / 2
    s = senkrecht('SUNNOZY', 150, SCHWARZ); s = s.resize((s.width, min(s.height, 610)), Image.LANCZOS) if s.height > 610 else s
    c.paste(s, (int(cx - s.width / 2), 80), s)
    d = ImageDraw.Draw(c); y = 80 + s.height + 90
    for z in ('FERTIG VERPACKT', 'MIT KARTE'):
        zentriert(d, cx, y, z, F('nunitosans-800.ttf', 30), SCHWARZ); y += 38
    y += 30
    zentriert(d, cx, y, 'Weihnachts-', F('nunitosans-600.ttf', 24), GRAU); y += 30
    zentriert(d, cx, y, 'Geschenkbox', F('nunitosans-600.ttf', 24), GRAU); y += 30
    zentriert(d, cx, y, 'Grössen 0–9 Monate', F('nunitosans-600.ttf', 24), GRAU)
    return c


def story(key):
    name, inhalt, preis = BOX[key]; W, H = 1080, 1920
    c = Image.new('RGB', (W, H), HELL)
    c.paste(foto(key, W, 1300), (0, 170))
    preisschild(c, 40, 210, preis, 64)
    d = ImageDraw.Draw(c)
    zentriert(d, W / 2, 1575, 'SUNNOZY', F('nunitosans-800.ttf', 120), SCHWARZ)
    zentriert(d, W / 2, 1632, f'{name}  ·  {inhalt}', F('nunitosans-600.ttf', 34), GRAU)
    zentriert(d, W / 2, 1680, 'FERTIG VERPACKT MIT KARTE', F('nunitosans-800.ttf', 32), SCHWARZ)
    return c


if __name__ == '__main__':
    keys = sys.argv[1:] or sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(FL, 'roh', '*.jpg')))
    for k in keys:
        feed(k).save(os.path.join(FL, f'feed_{k}_1x1.jpg'), quality=93)
        story(k).save(os.path.join(FL, f'story_{k}_9x16.jpg'), quality=93)
        print(k)
