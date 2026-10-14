"""Verdeckten Teil eines symmetrischen Kleidungsstuecks (z.B. Body-Aermel unter dem Strampler) durch Spiegeln ergaenzen.

Nimmt aus dem freigestellten Set-PNG die Flaeche innerhalb eines Polygons (nur dieses Teil), bestimmt die Symmetrieachse
aus dem untersten Fuenftel (Schritt/Beine) und fuellt fehlende Pixel auf der gewaehlten Seite mit dem gespiegelten Bild.
Ergebnis: PNG mit nur diesem Teil -> danach make_einzelteile.py <png> <ausgabe> - <name>

Aufruf: python3 spiegel_ergaenzen.py <set.png> <ausgabe.png> "<x1,y1,x2,y2,...>" [links|rechts]
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

src, dst, poly = sys.argv[1], sys.argv[2], list(map(int, sys.argv[3].split(',')))
side = sys.argv[4] if len(sys.argv) > 4 else 'links'
a = np.asarray(Image.open(src).convert('RGBA')).copy()
H, W = a.shape[:2]
reg = Image.new('L', (W, H), 0); ImageDraw.Draw(reg).polygon(list(zip(poly[0::2], poly[1::2])), fill=255)
a[np.asarray(reg) == 0] = 0
al = a[..., 3] > 40
ys, xs = np.nonzero(al)
y0 = ys.min() + int((ys.max() - ys.min()) * 0.8)
rows = [np.nonzero(al[y])[0] for y in range(y0, ys.max() - 5)]
cx = np.mean([(r.min() + r.max()) / 2 for r in rows if len(r)])
xx = np.arange(W)
fl = a[:, np.clip(np.round(2 * cx - xx).astype(int), 0, W - 1)]
half = xx[None, :] < cx if side == 'links' else xx[None, :] > cx
fill = (a[..., 3] < 128) & (fl[..., 3] > 0) & half
a[fill] = fl[fill]
Image.fromarray(a).save(dst)
print('Achse x =', round(cx, 1), '| ergaenzte Pixel:', int(fill.sum()))
