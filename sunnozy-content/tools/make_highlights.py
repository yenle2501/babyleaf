"""Instagram-Highlight-Cover aus den KI-Zeichnungen (ki-roh/*.png, weisser Grund).

Pro Zeichnung: Story-Format 1080x1920 (zum Hochladen als Story und dann als Highlight-Cover)
und Quadrat 1080x1080 (für «Cover bearbeiten» aus der Galerie). Grund ist Rosé #f8eae4 aus dem
sunnozy-Designsystem, die Zeichnung wird per Multiplizieren daraufgesetzt (weisser Grund verschwindet).
Dazu eine Vorschau, wie die Reihe im Profil aussieht.

Aufruf: python3 make_highlights.py <highlights-ordner>
"""
import os, sys, glob
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROSE = (248, 234, 228)
NAMEN = {'01_erstausstattung': 'Sets', '02_bodys': 'Bodys', '03_mulltuecher': 'Mulltücher', '04_accessoires': 'Accessoires',
         '05_geschenke': 'Geschenke', '06_bewertungen': 'Bewertungen', '07_versand': 'Versand', '08_ueber_uns': 'Über uns'}


def zeichnung(path):
    im = Image.open(path).convert('RGB')
    # Papiergrund der KI-Zeichnung ist nicht ganz weiss (246-254): auf 255 anheben, sonst bleibt ein heller Kasten
    im = im.point(lambda v: min(255, round(v * 255 / 244)))
    a = np.asarray(im.convert('L')); ys, xs = np.where(a < 238)
    return im.crop((xs.min() - 12, ys.min() - 12, xs.max() + 12, ys.max() + 12))


def setzen(c, t, cx, cy, groesse):
    k = groesse / max(t.size)
    t = t.resize((round(t.width * k), round(t.height * k)), Image.LANCZOS)
    x, y = int(cx - t.width / 2), int(cy - t.height / 2)
    c.paste(ImageChops.multiply(c.crop((x, y, x + t.width, y + t.height)), t), (x, y))


if __name__ == '__main__':
    base = sys.argv[1]
    out = os.path.join(base, 'cover'); os.makedirs(out, exist_ok=True)
    teile = []
    for f in sorted(glob.glob(os.path.join(base, 'ki-roh', '*.png'))):
        name = os.path.splitext(os.path.basename(f))[0]
        t = zeichnung(f); teile.append((name, t))
        story = Image.new('RGB', (1080, 1920), ROSE); setzen(story, t, 540, 960, 470)
        story.save(os.path.join(out, f'{name}_story.jpg'), quality=95)
        quad = Image.new('RGB', (1080, 1080), ROSE); setzen(quad, t, 540, 540, 470)
        quad.save(os.path.join(out, f'{name}_quadrat.jpg'), quality=95)
        print(name)
    # Vorschau wie im Profil: Kreis mit grauem Ring, Name darunter
    D, gap = 220, 70
    W = len(teile) * (D + gap) + gap
    v = Image.new('RGB', (W, D + 150), (255, 255, 255)); d = ImageDraw.Draw(v)
    f = ImageFont.truetype(os.path.join(ROOT, 'fonts', 'nunitosans-600.ttf'), 30)
    for i, (name, t) in enumerate(teile):
        x = gap + i * (D + gap); y = 30
        kreis = Image.new('RGB', (D, D), ROSE); setzen(kreis, t, D / 2, D / 2, D * 0.62)
        m = Image.new('L', (D * 4, D * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, D * 4, D * 4), fill=255)
        v.paste(kreis, (x, y), m.resize((D, D), Image.LANCZOS))
        d.ellipse((x - 12, y - 12, x + D + 12, y + D + 12), outline=(219, 222, 228), width=6)
        d.text((x + D / 2, y + D + 52), NAMEN.get(name, name), font=f, fill=(20, 20, 20), anchor='mm')
    v.save(os.path.join(base, 'vorschau_profil.jpg'), quality=92)
