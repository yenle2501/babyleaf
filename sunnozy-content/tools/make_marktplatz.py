"""Marktplatz-Hauptbilder (Amazon / Galaxus) aus freigestellten PNGs.

Regeln: reinweisser Hintergrund RGB 255/255/255, kein Text/Logo, Produkt fuellt ~88 % der laengeren Seite,
quadratisch 2000x2000 px (Zoom-faehig), sRGB-JPEG. Nur ein sehr weicher Kontaktschatten; Raender bleiben reinweiss.

Aufruf: python3 make_marktplatz.py <png-ordner> <ausgabeordner> [fuellgrad=0.88] [groesse=2000]
"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1:3]
fill = float(sys.argv[3]) if len(sys.argv) > 3 else 0.88
S = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, '*.png'))):
    cut = Image.open(f).convert('RGBA')
    a = cut.getchannel('A').point(lambda v: 0 if v < 12 else v)  # Reste vom Hintergrund weg
    cut.putalpha(a)
    cut = cut.crop(a.getbbox())
    k = S * fill / max(cut.size)
    cut = cut.resize((round(cut.width * k), round(cut.height * k)), Image.LANCZOS)
    rgb = cut.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2)); rgb.putalpha(cut.getchannel('A'))
    cut = rgb
    x, y = (S - cut.width) // 2, (S - cut.height) // 2
    bg = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    sh = Image.new('L', (S, S), 0); sh.paste(cut.getchannel('A'), (x + 4, y + 10))
    sh = sh.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.10))
    dark = Image.new('RGBA', (S, S), (90, 80, 80, 0)); dark.putalpha(sh)
    bg = Image.alpha_composite(bg, dark); bg.alpha_composite(cut, (x, y))
    img = bg.convert('RGB')
    arr = np.asarray(img)
    # Sicherheit: alles, was fast weiss ist und ausserhalb des Produkts liegt, auf exakt 255
    mask = np.zeros((S, S), bool); mask[y:y + cut.height, x:x + cut.width] = np.asarray(cut.getchannel('A')) > 0
    near = (arr.min(axis=2) >= 250) & ~mask
    arr = arr.copy(); arr[near] = 255
    img = Image.fromarray(arr)
    name = os.path.splitext(os.path.basename(f))[0] + '.jpg'
    img.save(os.path.join(out, name), quality=95, subsampling=0)
    nz = (np.asarray(img).min(axis=2) < 250)
    ys, xs = np.where(nz)
    cover = max(xs.max() - xs.min(), ys.max() - ys.min()) / S
    print(name, img.size, 'Ecken:', tuple(arr[0, 0]), tuple(arr[-1, -1]), f'Fuellgrad {cover:.0%}')
