"""Fast weissen Studio-Hintergrund (ca. 245-252) auf reines Weiss 255 bringen, ohne Maske.

Fuer Produktfotos, deren Grund nur leicht grau oder blaeulich ist (typisch bei KI-Bildern). Nur die Lichter werden
angehoben: Pixel unter LO bleiben unveraendert, darueber wird weich auf «Randfarbe -> 255» uebergeblendet (pro Kanal,
entfernt also auch einen leichten Farbstich des Grundes). Produktfarben und Mitteltoene bleiben gleich.

Aufruf: python3 weiss_angleichen.py <eingabe> <ausgabe>
"""
import sys
import numpy as np
from PIL import Image

src, out = sys.argv[1:3]
LO = 175

a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
b = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
bg = np.percentile(b, 60, axis=0)  # Randfarbe (robust gegen einzelne Produktpixel am Rand)
scale = 255 / np.maximum(bg - 2.5, 1)  # etwas Reserve gegen Rauschen im Grund
L = a.mean(2, keepdims=True)
t = np.clip((L - LO) / (bg.mean() - LO), 0, 1) ** 1.5
res = a * (1 - t) + np.clip(a * scale, 0, 255) * t
res = np.clip(res, 0, 255).round().astype(np.uint8)
ext = out.rsplit('.', 1)[-1].lower()
Image.fromarray(res).save(out, **({'quality': 95, 'subsampling': 0} if ext in ('jpg', 'jpeg') else {}))
c = res[[3, 3, -4, -4], [3, -4, 3, -4]]
print(out, 'Rand vorher', bg.round().astype(int).tolist(), '-> Ecken', [tuple(int(v) for v in x) for x in c])
