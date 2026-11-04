"""Fotos «Baby in der Box-Kleidung» aus den KI-Babybildern der Schlaf-Reels.

    python3 tools/make_box_baby_fotos.py

Quelle: posts/kampagne-weihnachtsbox/reels-schlaf/baby/<box>.png (1080 × 1920, KI, Safe Sleep)
Ausgabe: posts/kampagne-weihnachtsbox/baby-in-box-kleidung/<box>_9x16.jpg (Story) und <box>_4x5.jpg (Feed, 1080 × 1350), ohne Text.
"""
import os, glob
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox', 'reels-schlaf', 'baby')
OUT = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox', 'baby-in-box-kleidung')
os.makedirs(OUT, exist_ok=True)
for p in sorted(glob.glob(os.path.join(SRC, '*.png'))):
    k = os.path.splitext(os.path.basename(p))[0]
    im = Image.open(p).convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
    im.save(os.path.join(OUT, f'{k}_9x16.jpg'), quality=93)
    y = int((im.height - 1350) * 0.4)                     # Kopf und Body im Bild, etwas oberhalb der Mitte
    im.crop((0, y, 1080, y + 1350)).save(os.path.join(OUT, f'{k}_4x5.jpg'), quality=93)
    print(k)
