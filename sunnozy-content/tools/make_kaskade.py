"""Shopify-Hauptbild im Kaskaden-Look: Teile eines Sets schraeg gestaffelt, hinten oben rechts -> vorne unten links.

Vorbild: Pinterest/aboutyou-Bild der Nutzerin (4 Ripp-Bodys mit Rueschen auf hellgrauem Grund).
Quelle: freigestellte Einzelbilder (PNG mit Alpha) der echten Produktfotos aus Shopify, also keine KI-Veraenderung.
Ausgabe: 2048 x 2048 px JPG (Shopify-Empfehlung, quadratisch, Zoom-faehig), Hintergrund hellgrau wie im Vorbild.

Aufruf: python3 make_kaskade.py <teile-ordner> <ausgabe-ordner> [nur_set ...]
  <teile-ordner>/<set>/<nr>.png  (Nummern wie in SETS unten, Reihenfolge = hinten -> vorne)
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1:3]
only = set(sys.argv[3:])
os.makedirs(out, exist_ok=True)
SIZE = 2048
BG = (244, 244, 245)
FILL = 0.86  # Anteil der Bildflaeche, den das Set einnimmt (laengere Seite)

# Set -> Teile (hinten -> vorne); Eintrag 'set/nr' oder ('set/nr', drehung_grad)
SETS = {
    'growing_up_strong_kurzarm5': ['05', '04', '03', '02', '01'],
    'love_more_kurzarm5': ['03', '02', '05', '04', '01'],
    'dino_langarm3': ['03', '02', '01'],
    'flying_langarm3': ['03', '02', '01'],
    'lovely_langarm3': ['03', '02', '01'],
    'leggings5': ['05', '03', '02', '04', '01'],
    'jogginghose5': ['05', '04', '03', '02', '01'],
    'dinosaur_kurzarm5': ['04', '05', '03', '02', '01'],
    'i_love_hugs_aermellos3': [('03', -4), ('02', -11), '01'],
    'mummy_kurzarm5': ['05', '03', '04', '02', '01'],
    'mummy_langarm3': ['01', '02', '03'],
    'i_love_my_mum_kurzarm5': ['05', '04', '03', '02', '01'],
    'mumdadme_langarm5': ['04', '02', '05', '03', '01'],
}
# Kombi-Sets: zwei Kaskaden nebeneinander (Bodys links, Hosen rechts)
KOMBI = {
    'kombi_growing_up_strong': ('growing_up_strong_kurzarm5', 'jogginghose5'),
    'kombi_lovely': ('lovely_langarm3', 'leggings5'),
    'kombi_mumdadme': ('mumdadme_langarm5', 'leggings5'),
}
ROT = {}  # Feinkorrektur schiefer Quellbilder: 'set/nr' -> Grad


def load(set_, item):
    rot = 0
    if isinstance(item, tuple):
        item, rot = item
    im = Image.open(os.path.join(src, set_, item + '.png')).convert('RGBA')
    # 2 px nach innen beschneiden: entfernt hellen Saum vom Original-Hintergrund
    im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8)))
    rot = rot or ROT.get(f'{set_}/{item}', 0)
    if rot:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    return im.crop(im.getchannel('A').getbbox())


def cascade(items, h=900):
    """Teile auf gleiche Hoehe skalieren und staffeln. Liefert RGBA-Ebene inkl. weicher Schatten."""
    n = len(items)
    ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in items]
    wmax = max(i.width for i in ims)
    r = {2: 0.5, 3: 0.42, 4: 0.36, 5: 0.29}.get(n, 0.3)  # sichtbarer Anteil der hinteren Teile
    dy, dx = int(h * r), int(wmax * (0.3 if n <= 3 else 0.27))
    W = wmax + (n - 1) * dx + 200; H = h + (n - 1) * dy + 200
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i, im in enumerate(ims):  # hinten zuerst
        x = 100 + (n - 1 - i) * dx + (wmax - im.width) // 2
        y = 100 + i * dy
        a = im.getchannel('A')
        sh = Image.new('L', (W, H), 0); sh.paste(a, (x + 10, y + 18))
        sh = sh.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.20))
        shadow = Image.new('RGBA', (W, H), (60, 55, 50, 0)); shadow.putalpha(sh)
        lay = Image.alpha_composite(lay, shadow)
        lay.alpha_composite(im, (x, y))
    return lay.crop(lay.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox())


def finish(lay, name):
    s = min(SIZE * FILL / lay.width, SIZE * FILL / lay.height)
    lay = lay.resize((round(lay.width * s), round(lay.height * s)), Image.LANCZOS)
    c = Image.new('RGBA', (SIZE, SIZE), BG + (255,))
    c.alpha_composite(lay, ((SIZE - lay.width) // 2, (SIZE - lay.height) // 2))
    c = c.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.0, percent=40, threshold=2))
    c.save(os.path.join(out, name + '.jpg'), quality=93, subsampling=0)
    print(name, c.size, f'{lay.width}x{lay.height}')


for k, items in SETS.items():
    if only and k not in only:
        continue
    finish(cascade([load(k, i) for i in items]), k)

for k, (bodys, hosen) in KOMBI.items():
    if only and k not in only:
        continue
    a = cascade([load(bodys, i) for i in SETS[bodys]])
    b = cascade([load(hosen, i) for i in SETS[hosen]])
    b = b.resize((round(b.width * a.height * 0.92 / b.height), round(a.height * 0.92)), Image.LANCZOS)
    gap = int(a.width * 0.04)
    lay = Image.new('RGBA', (a.width + gap + b.width, a.height), (0, 0, 0, 0))
    lay.alpha_composite(a, (0, 0)); lay.alpha_composite(b, (a.width + gap, a.height - b.height))
    finish(lay, k)
