"""sunnozy Hausstil (Okt. 2026): Baby-Foto vollflaechig, ein Satz in Handschrift unten, Logo klein in Weiss.

Aufruf: python3 make_handschrift.py <baby-foto-ordner> <ausgabeordner>
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
photo_dir, out = sys.argv[1:3]
# Helfer (fill, grade, hand, put_logo ...) aus make_viral.py wiederverwenden, ohne dessen Posts zu erzeugen
src = open(os.path.join(here, 'make_viral.py')).read().split('# 1) "Schick das an')[0]
g = {'__file__': os.path.join(here, 'make_viral.py')}
sys.argv = ['x', photo_dir, photo_dir, out]
exec(src.replace("B = {k: Image.open", "_B = {k: Image.open").replace("PK = lambda", "_PK = lambda"), g)
Image, fill, grade, hand, put_logo = g['Image'], g['fill'], g['grade'], g['hand'], g['put_logo']
os.makedirs(out, exist_ok=True)
P = {k: Image.open(os.path.join(photo_dir, k + '.jpg')).convert('RGB') for k in ('yellow', 'pink', 'lila', 'cream')}


def post(key, text, name, ay=0.35, crop=None, size=96, y=1000, w=1080, h=1350, logo_bottom=40):
    im = P[key]
    if crop:
        W0, H0 = im.size
        im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    img = grade(fill(im, w, h, ay))
    hand(img, (w // 2, y), text, size, anchor='ma', rot=2)
    put_logo(img, 150, logo_bottom, (255, 255, 255))
    img.convert('RGB').save(os.path.join(out, name), quality=94)
    return img


posts = [
    ('lila', 'Schick das der Person,\ndie bald Mama wird.', 'mo_schick_das.jpg', 0.35, None),
    ('yellow', 'Für die Freundin, die gerade\n3 Stunden geschlafen hat.', 'di_freundin.jpg', 0.35, None),
    ('pink', 'Niemand sagt dir,\nwie klein sie wirklich sind.', 'mi_so_klein.jpg', 0.45, None),
    ('cream', 'Weich genug für die\nerste Nacht zuhause.', 'do_erste_nacht.jpg', 0.45, None),
    ('lila', 'mum. dad. me.\nAus zwei wurden drei.', 'fr_aus_zwei_wurden_drei.jpg', 0.0, (0.05, 0.0, 0.95, 0.62)),
    ('yellow', 'Markier eine Mama, die genau\ndas gerade fühlt.', 'sa_markier_eine_mama.jpg', 1.0, (0.0, 0.38, 1.0, 1.0)),
]
for k, t, n, ay, crop in posts:
    post(k, t, n, ay, crop)

# Reel-Frames (9:16) fuer So: ein Satz pro Foto
reel = [('yellow', 'Niemand hat mir gesagt …'), ('pink', '… wie weich diese ersten\nWochen sein würden.'),
        ('lila', 'mum. dad. me.'), ('cream', 'Für kleine Sonnenscheine.')]
for i, (k, t) in enumerate(reel):
    post(k, t, f'_reel_{i}.jpg', 0.35, None, size=100, y=1440, w=1080, h=1920, logo_bottom=90)
print(sorted(os.listdir(out)))
