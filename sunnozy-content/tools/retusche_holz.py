"""Fremdes Logo/Stempel auf einem Holzbuegel wegretuschieren, ohne die Buegelkante zu verwischen.

Nur Holzpixel (R-B > 30) im Kreis werden durch die geglaettete Holzfarbe der Umgebung ersetzt, plus feines Korn.
Besser als retusche_kreis.py, wenn das Logo nah an der Buegelkante sitzt.

Aufruf: python3 retusche_holz.py <bild> <x> <y> <radius> [<ausgabe>]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, x, y, r = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
out = sys.argv[5] if len(sys.argv) > 5 else src
a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = a.shape
yy, xx = np.mgrid[:H, :W]
d = np.hypot(xx - x, yy - y)
wood = ndimage.binary_erosion((a[..., 0] - a[..., 2]) > 30, iterations=2)
m = wood.astype(np.float32)
sm = np.stack([ndimage.gaussian_filter(a[..., c] * m, 9) for c in range(3)], -1) / np.maximum(ndimage.gaussian_filter(m, 9), 1e-3)[..., None]
sm += np.random.default_rng(1).normal(0, 1.6, (H, W, 1))
w = np.clip((r - d) / (r * 0.3), 0, 1) * ndimage.gaussian_filter(m, 1.2)
a = a * (1 - w[..., None]) + sm * w[..., None]
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(out, quality=96)
