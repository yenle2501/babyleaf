"""Hausstil "Handschrift" fuer beliebige Bilder: Liste (datei, text, ay, y-position) -> 4:5 Posts.

Textfarbe automatisch: weiss mit Schatten auf dunkleren Bildern, warmes Braun auf sehr hellen Flaechen.
Aufruf: python3 make_handschrift_bilder.py <bildordner> <ausgabeordner>
"""
import sys, os
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
img_dir, out = sys.argv[1:3]
src = open(os.path.join(here, 'make_viral.py')).read().split('# 1) "Schick das an')[0]
g = {'__file__': os.path.join(here, 'make_viral.py')}
sys.argv = ['x', img_dir, img_dir, out]
exec(src.replace("B = {k: Image.open", "_B = None and {k: Image.open").replace("PK = lambda", "_PK = lambda"), g)
Image, fill, grade, hand, put_logo = g['Image'], g['fill'], g['grade'], g['hand'], g['put_logo']
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except ImportError:
    pass
os.makedirs(out, exist_ok=True)
W, H = 1080, 1350

POSTS = [
    ('p7254.img', 'Das Lächeln, für das sich\njede Nacht lohnt.', 0.3, 1060, 'mama_laecheln.jpg'),
    ('p_life.img', 'Für die kleine Person,\ndie alles verändert hat.', 0.25, 1080, 'kleine_person.jpg'),
    ('p7257.img', 'Kleiner Schrank,\ngrosse Liebe.', 0.5, 1070, 'kleiner_schrank.jpg'),
    ('p7362.img', 'Schick das dem Papa, der noch\nnicht weiss, was ihn erwartet.', 0.4, 1080, 'schick_dem_papa.jpg'),
    ('p7365.img', 'Für den kleinen Jungen,\nder bald kommt.', 0.4, 1060, 'kleiner_junge.jpg'),
    ('p7046.img', 'Markier die Mama, die immer\nein Lätzchen dabei hat.', 0.5, 1080, 'laetzchen_mama.jpg'),
    ('h8702.img', 'Mulltücher.\nMan hat nie genug.', 0.35, 1080, 'mulltuecher.jpg'),
    ('h8292.img', 'Willkommen,\nkleiner Mensch.', 0.5, 1050, 'willkommen.jpg'),
]

for f, text, ay, y, name in POSTS:
    from PIL import ImageOps
    im = ImageOps.exif_transpose(Image.open(os.path.join(img_dir, f))).convert('RGB')
    if name == 'willkommen.jpg' and im.width > im.height: im = im.rotate(90, expand=True)
    img = grade(fill(im, W, H, ay))
    band = np.asarray(img.crop((150, y - 20, W - 150, y + 230)).convert('L')).mean()
    light = band > 185
    col = (112, 82, 66) if light else (255, 251, 244)
    hand(img, (W // 2, y), text, 92, fill=col, anchor='ma', rot=2, shadow=not light)
    put_logo(img, 150, 40, (90, 70, 60) if light else (255, 255, 255))
    img.convert('RGB').save(os.path.join(out, name), quality=94)
    print(name, 'hell' if light else 'dunkel', int(band))
