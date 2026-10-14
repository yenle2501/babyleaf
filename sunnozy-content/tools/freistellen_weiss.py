"""Einzelteilbild auf Reinweiss -> transparentes PNG (fuer Sticker, Collagen).

Hintergrund = vom Bildrand aus zusammenhaengende helle Pixel (inkl. weichem Schatten). Weisse Teile bleiben erhalten,
solange ihr Rand eine Naht/Kontur hat. Kante wird leicht weichgezeichnet; Ausgabe auf das Teil zugeschnitten.

Aufruf: python3 freistellen_weiss.py <bild.jpg> <ausgabe.png> [schwelle=236]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

src, dst = sys.argv[1:3]
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 236
im = Image.open(src).convert('RGB'); a = np.asarray(im)
light = a.min(axis=2) >= thr
lab, _ = ndimage.label(light)
edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
bg = np.isin(lab, edge[edge > 0])
obj = ndimage.binary_fill_holes(~bg)
obj = ndimage.binary_opening(obj, iterations=2)
lab2, n = ndimage.label(obj)
if n > 1:  # Kruemel weg, nur grosse Flaechen behalten
    sizes = ndimage.sum(obj, lab2, range(1, n + 1))
    obj = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * 0.02])
alpha = Image.fromarray((obj * 255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
out = im.copy(); out.putalpha(alpha)
out.crop(alpha.getbbox()).save(dst)
print(dst, out.crop(alpha.getbbox()).size)
