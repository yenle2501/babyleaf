"""Werbebilder Weihnachts-Geschenkboxen im «Katalog-Flatlay»-Stil (Vorlage der Nutzerin, 03.11.2026: Mode-Anzeige mit
Kleidung flach auf Weinrot, Preisschild oben links, rechts helle Leiste mit dem sunnozy-Logo senkrecht).

    python3 tools/make_flatlay_ads.py               # alle Boxen, für die ein Flatlay in rote-box/flatlay/roh/ liegt
    python3 tools/make_flatlay_ads.py dino          # nur eine Box

Flatlay-Fotos: KI (Canva) nach den Set-Fotos aus dem Shop und der roten sunnozy-Box, 3:4 (rote-box/flatlay/roh/<box>.jpg).
Schrift Nunito Sans + Fraunces, keine Schreibschrift, keine fremden Marken, keine Versand-Versprechen.
Ausgabe in rote-box/flatlay/: feed_<box>_1x1.jpg (Katalog-Stil), inhalt_<box>_1x1.jpg («Was ist drin?»),
zu_offen_<box>_1x1.jpg («Verpackt … und das ist drin»), story_<box>_9x16.jpg (1080 × 1920).
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


def logo(hoehe=None, breite=None, gedreht=False):
    """Echtes sunnozy-Logo (logo-sunnozy-gross.png, aus der Markendatei freigestellt)."""
    L = Image.open(os.path.join(ROOT, 'logo-sunnozy-gross.png')).convert('RGBA')
    if gedreht:
        L = L.rotate(-90, expand=True)          # liest von oben nach unten
    s = (hoehe / L.height) if hoehe else (breite / L.width)
    return L.resize((round(L.width * s), round(L.height * s)), Image.LANCZOS)


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
    s = logo(hoehe=600, gedreht=True)
    c.paste(s, (int(cx - s.width / 2), 90), s)
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
    L = logo(breite=520); c.paste(L, ((W - L.width) // 2, 1500), L)
    zentriert(d, W / 2, 1632, f'{name}  ·  {inhalt}', F('nunitosans-600.ttf', 34), GRAU)
    zentriert(d, W / 2, 1680, 'FERTIG VERPACKT MIT KARTE', F('nunitosans-800.ttf', 32), SCHWARZ)
    return c


WEINROT = (98, 22, 30)


def haekchen(d, x, y, g=26, farbe=WEINROT):
    """Gezeichnetes Häkchen im Kreis (die Schrift hat kein ✓)."""
    d.ellipse((x, y, x + g, y + g), outline=farbe, width=3)
    d.line((x + g * 0.26, y + g * 0.52, x + g * 0.44, y + g * 0.70, x + g * 0.76, y + g * 0.32), fill=farbe, width=4, joint='curve')


def inhalt(key):
    """Idee «Was ist drin?»: Flatlay links, rechts Liste mit Häkchen, Preis, Logo."""
    name, inh, preis = BOX[key]; W = H = 1080
    c = Image.new('RGB', (W, H), HELL); c.paste(foto(key, 600, 800), (0, 140))
    d = ImageDraw.Draw(c); x0 = 640
    L = logo(breite=330); c.paste(L, (x0, 150), L)
    d.text((x0, 300), 'WAS IST DRIN?', font=F('nunitosans-800.ttf', 30), fill=WEINROT, anchor='ls')
    d.text((x0, 350), name, font=F('fraunces-400.ttf', 40 if len(name) < 16 else 34), fill=SCHWARZ, anchor='ls')
    teile = [t.strip() for t in inh.split('+')] + ['Rote Geschenkbox', 'Satinband + Seidenpapier', 'Weihnachtskarte']
    y = 420
    for t in teile:
        haekchen(d, x0, y - 22); d.text((x0 + 42, y), t, font=F('nunitosans-600.ttf', 30), fill=SCHWARZ, anchor='ls'); y += 58
    preisschild(c, x0, y + 20, preis, 52)
    d.text((x0, y + 150), 'Grössen 0–9 Monate', font=F('nunitosans-600.ttf', 26), fill=GRAU, anchor='ls')
    return c


def zu_offen(key):
    """Idee «Verpackt … und das ist drin»: links die geschlossene Box, rechts das Flatlay."""
    name, inh, preis = BOX[key]; W = H = 1080
    c = Image.new('RGB', (W, H), HELL)
    zu = Image.open(os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox', 'rote-box', 'vorlage', 'vorlage_zu.jpg')).convert('RGB')
    s = max(530 / zu.width, 760 / zu.height); zu = zu.resize((round(zu.width * s), round(zu.height * s)), Image.LANCZOS)
    zu = zu.crop(((zu.width - 530) // 2, (zu.height - 760) // 2, (zu.width - 530) // 2 + 530, (zu.height - 760) // 2 + 760))
    c.paste(zu, (0, 170)); c.paste(foto(key, 530, 760), (550, 170))
    d = ImageDraw.Draw(c)
    L = logo(breite=260); c.paste(L, ((W - L.width) // 2, 50), L)
    d.text((265, 980), 'Verpackt …', font=F('fraunces-400.ttf', 44), fill=SCHWARZ, anchor='ms')
    d.text((815, 980), '… und das ist drin', font=F('fraunces-400.ttf', 44), fill=SCHWARZ, anchor='ms')
    d.text((W / 2, 1040), f'{name}  ·  {inh}', font=F('nunitosans-600.ttf', 28), fill=GRAU, anchor='ms')
    preisschild(c, 570, 192, preis, 46)
    return c


if __name__ == '__main__':
    keys = sys.argv[1:] or sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(FL, 'roh', '*.jpg')))
    for k in keys:
        feed(k).save(os.path.join(FL, f'feed_{k}_1x1.jpg'), quality=93)
        story(k).save(os.path.join(FL, f'story_{k}_9x16.jpg'), quality=93)
        inhalt(k).save(os.path.join(FL, f'inhalt_{k}_1x1.jpg'), quality=93)
        zu_offen(k).save(os.path.join(FL, f'zu_offen_{k}_1x1.jpg'), quality=93)
        print(k)
