"""KI-Hauptbild (z.B. aus Canva oder ChatGPT) auf 2048 px bringen, leicht nachschärfen und das sunnozy-Logo
oben links setzen, in Grösse, Lage und Farbe wie im Teddybär-Vorbild der Nutzerin.

Aufruf: python3 hauptbild_logo.py <eingabe> <ausgabe.jpg> [--ohne-logo]
--ohne-logo: nur vergrössern und schärfen (wenn das Logo schon im Bild ist)
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 2048


def logo(width, color=(122, 108, 104)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), color + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


if __name__ == '__main__':
    src, dst = sys.argv[1:3]
    im = Image.open(src).convert('RGB')
    if im.size != (N, N):
        im = im.resize((N, N), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    if '--ohne-logo' not in sys.argv:
        L = logo(int(N * 0.198))
        im.paste(L, (int(N * 0.035), int(N * 0.031)), L)
    im.save(dst, quality=95)
    print(dst, im.size)
