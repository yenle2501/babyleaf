"""Grauen Studio-Hintergrund eines fertigen Bildes auf Reinweiss bringen, Produkt bleibt unveraendert.

Fuer Bilder ohne Freisteller (KI-Bilder, Set-Praesentationen mit Logo), damit das Hauptbild zum weissen
Hintergrund der uebrigen Shop-Fotos passt. Vorgehen:
1. Hintergrund = vom Rand aus zusammenhaengende, neutrale (unbunte) Flaeche nahe der Randhelligkeit, inkl. Schatten.
2. Lokale Hintergrundhelligkeit schaetzen (Verlauf im Studio-Licht) und durch sie teilen: Flaeche wird 255,
   weiche Schatten bleiben im gleichen Verhaeltnis erhalten, nur heller.
3. Uebergang zum Produkt 1-2 px weich, Produktpixel selbst werden nicht veraendert.

Mit Maske (empfohlen bei Creme/Weiss auf Grau): freigestelltes PNG gleicher Bildgroesse (z.B. Canva remove-background).
Dann gilt das Produkt aus der Maske als unantastbar; was ausserhalb liegt und nicht nach Hintergrund aussieht
(Logo, Wandknauf), bleibt ebenfalls original.

Aufruf: python3 hintergrund_weiss.py <eingabe> <ausgabe> [maske.png]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

src, out = sys.argv[1:3]
MASK = sys.argv[3] if len(sys.argv) > 3 else None
TOL = 45  # Schatten bis so viel dunkler als der Grund gelten als Hintergrund

im = Image.open(src).convert('RGB')
a = np.asarray(im).astype(np.float32)
H, W = a.shape[:2]
L = a.mean(2)
sat = a.max(2) - a.min(2)
Ls = ndi.uniform_filter(L, 5)

border = np.concatenate([Ls[:8].ravel(), Ls[-8:].ravel(), Ls[:, :8].ravel(), Ls[:, -8:].ravel()])
bg = float(np.median(border))

# Kandidaten: so unbunt wie der Rand (Creme/Weiss hat einen leichten Gelbstich, der Studio-Grund nicht), nicht heller
# als der Hintergrund (sonst weisses Produkt), Schatten bis bg-TOL, und keine Kante dazwischen (Produktumriss = Grenze)
warm = ndi.uniform_filter((a[..., 0] + a[..., 1]) / 2 - a[..., 2], 5)
satf = ndi.uniform_filter(sat, 5)
bw = np.concatenate([warm[:8].ravel(), warm[-8:].ravel(), warm[:, :8].ravel(), warm[:, -8:].ravel()])
bs = np.concatenate([satf[:8].ravel(), satf[-8:].ravel(), satf[:, :8].ravel(), satf[:, -8:].ravel()])
wtol = max(2.0, np.percentile(np.abs(bw - np.median(bw)), 99) + 1.0)
stol = max(3.0, np.percentile(bs, 99) + 1.5)
grad = np.hypot(ndi.sobel(Ls, 0), ndi.sobel(Ls, 1)) / 8
barrier = ndi.binary_dilation(grad > 2.2, iterations=1)
cand = (satf <= stol) & (np.abs(warm - np.median(bw)) <= wtol) & (Ls >= bg - TOL) & (Ls <= bg + 4)
if MASK:
    m = Image.open(MASK).convert('RGBA').getchannel('A').resize((W, H), Image.LANCZOS)
    prod = np.asarray(m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
    # Logo, Knauf usw.: deutlich dunkler als jeder Schatten oder kraeftig farbig (Schatten bleiben Hintergrund)
    fremd = ndi.binary_opening(((Ls < bg - TOL) | (satf > 25)) & (prod < 0.5), iterations=1)
    fremd = ndi.gaussian_filter(ndi.binary_dilation(fremd, iterations=2).astype(np.float32), 1.0)
    keep = np.maximum(prod, fremd)
    region = keep < 0.5
else:
    lab, _ = ndi.label(cand & ~barrier)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    region = np.isin(lab, edge[edge > 0])
    # Kantenpixel zwischen zwei Hintergrundflaechen (z.B. Schattenkante) wieder dazunehmen, Produkt bleibt ausgespart
    region |= cand & ndi.binary_dilation(region, iterations=2) & barrier
    region = ndi.binary_opening(region, iterations=1)
    keep = 1 - ndi.gaussian_filter(ndi.binary_dilation(region, iterations=1).astype(np.float32), 1.2)

# lokale Hintergrundhelligkeit pro Kanal (normierte Faltung nur ueber reine Hintergrundpixel)
pure = region & (np.abs(Ls - bg) <= 6)
f = 8  # verkleinert rechnen (der Verlauf ist sehr weich), dann hochskalieren
ps = pure[::f, ::f].astype(np.float32); sig = max(H, W) / 25 / f
wsum = ndi.gaussian_filter(ps, sig)
bgmap = np.stack([ndi.gaussian_filter(a[::f, ::f, c] * ps, sig) / np.maximum(wsum, 1e-3) for c in range(3)], 2)
bgmap[wsum < 1e-3] = bg
bgmap = ndi.zoom(bgmap, (H / bgmap.shape[0], W / bgmap.shape[1], 1), order=1)[:H, :W]
white = np.clip(a / np.maximum(bgmap, 1) * 255, 0, 255)

k = keep[..., None]
res = a * k + white * (1 - k)
Image.fromarray(res.round().astype(np.uint8)).save(out, quality=95, subsampling=0)
c = res[[4, 4, -5, -5], [4, -5, 4, -5]].round().astype(int)
print(out, f'bg {bg:.0f} -> Ecken', [tuple(x) for x in c], f'Hintergrund {region.mean() * 100:.0f} %')
