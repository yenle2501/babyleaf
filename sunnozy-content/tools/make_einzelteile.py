"""Einzelteile aus einem freigestellten Set-Hauptbild extrahieren -> je ein Marktplatz-Foto pro Teil.

Funktionsweise: Alpha-Kanal erodieren (trennt Teile, die sich nur leicht beruehren), Flaechen labeln,
Bruchstuecke an Nachbarn haengen, Paare (Socken, Faeustlinge) zusammenfassen, Kruemel verwerfen, jedes Teil auf reinweiss 2000x2000 setzen (via make_marktplatz-Logik).

Aufruf: python3 make_einzelteile.py <set.png> <ausgabeordner> [paar_abstand_px=40] [namen=kommagetrennt]
  namen: optional, in Lesereihenfolge (oben->unten, links->rechts); sonst teil_01, teil_02 ...
  Ausgabe: <ausgabe>/<set>_<name>.jpg + Kontaktbogen <set>_uebersicht.jpg
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from scipy import ndimage

src, out = sys.argv[1:3]
gap = int(sys.argv[3]) if len(sys.argv) > 3 else 40
names = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else None
S, FILL = 2000, 0.85
os.makedirs(out, exist_ok=True)
setname = os.path.splitext(os.path.basename(src))[0]

im = Image.open(src).convert('RGBA')
alpha = np.asarray(im.getchannel('A'))
mask = alpha > 40
total = mask.sum()
H0, W0 = mask.shape
# 1) duenne Beruehrungsstellen loesen: Maske erodieren, Flaechen labeln, Pixel dem naechsten Label zuweisen
ero = ndimage.binary_erosion(mask, iterations=max(4, round(min(H0, W0) * 0.007)))
lab, n = ndimage.label(ero)
areas = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
for i, a in enumerate(areas, 1):
    if a < total * 0.002:
        lab[lab == i] = 0
_, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
lab = np.where(mask, lab[iy, ix], 0)


def comps(lab):
    ids = [i for i in np.unique(lab) if i]
    return {i: (lab == i) for i in ids}


# 2) kleine Bruchstuecke (z.B. abgetrennter Aermel) an groesseren Nachbarn anhaengen
changed = True
while changed:
    changed = False
    cs = comps(lab); ar = {i: m.sum() for i, m in cs.items()}
    for i, m in sorted(cs.items(), key=lambda kv: ar[kv[0]]):
        if ar[i] >= total * 0.025:
            continue
        ring = ndimage.binary_dilation(m, iterations=3) & ~m
        nb = [j for j in np.unique(lab[ring]) if j and j != i and ar[j] > 4 * ar[i]]
        if nb:
            lab[m] = max(nb, key=lambda j: ar[j]); changed = True; break
# 3) Paare zusammenfassen (Socken, Faeustlinge): beide klein, aehnlich gross, nah beieinander
cs = comps(lab); ar = {i: m.sum() for i, m in cs.items()}
bb = {i: ndimage.find_objects(m.astype(int))[0] for i, m in cs.items()}


def bgap(a, b):
    ya, xa = bb[a]; yb, xb = bb[b]
    dy = max(0, max(ya.start, yb.start) - min(ya.stop, yb.stop)); dx = max(0, max(xa.start, xb.start) - min(xa.stop, xb.stop))
    return max(dy, dx)


small_ids = [i for i in cs if ar[i] < total * 0.06]
for a in small_ids:
    for b in small_ids:
        if a < b and (lab == a).any() and (lab == b).any() and 0.5 < ar[a] / ar[b] < 2 and bgap(a, b) <= gap:
            lab[lab == b] = a
parts = []
for i, m in comps(lab).items():
    if m.sum() < total * 0.004:
        continue
    ys, xs = np.nonzero(m)
    parts.append((ys.min(), xs.min(), ys.max() + 1, xs.max() + 1, m))
# Lesereihenfolge: Zeilen nach Mittelpunkt (Toleranz = 1/8 Bildhoehe), dann links->rechts
rowtol = mask.shape[0] / 8
parts.sort(key=lambda p: (round(((p[0] + p[2]) / 2) / rowtol), (p[1] + p[3]) / 2))

thumbs = []
for k, (y0, x0, y1, x1, m) in enumerate(parts):
    name = names[k] if names and k < len(names) else f'teil_{k + 1:02d}'
    a = Image.fromarray((m * alpha).astype('uint8'))
    piece = im.copy(); piece.putalpha(a); piece = piece.crop((x0, y0, x1, y1))
    sc = S * FILL / max(piece.size)
    piece = piece.resize((round(piece.width * sc), round(piece.height * sc)), Image.LANCZOS)
    rgb = piece.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2)); rgb.putalpha(piece.getchannel('A')); piece = rgb
    x, y = (S - piece.width) // 2, (S - piece.height) // 2
    bg = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    sh = Image.new('L', (S, S), 0); sh.paste(piece.getchannel('A'), (x + 4, y + 10))
    sh = sh.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.10))
    dark = Image.new('RGBA', (S, S), (90, 80, 80, 0)); dark.putalpha(sh)
    bg = Image.alpha_composite(bg, dark); bg.alpha_composite(piece, (x, y))
    arr = np.asarray(bg.convert('RGB')).copy()
    pm = np.zeros((S, S), bool); pm[y:y + piece.height, x:x + piece.width] = np.asarray(piece.getchannel('A')) > 0
    arr[(arr.min(axis=2) >= 250) & ~pm] = 255
    out_img = Image.fromarray(arr)
    fn = f'{setname}_{name}.jpg'
    out_img.save(os.path.join(out, fn), quality=95, subsampling=0)
    thumbs.append((fn, out_img.resize((300, 300))))
    print(fn)

# Kontaktbogen mit Dateinamen
cols = 4; rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 310, rows * 340), (235, 235, 235)); d = ImageDraw.Draw(sheet)
f = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 14)
for i, (fn, t) in enumerate(thumbs):
    cx, cy = (i % cols) * 310 + 5, (i // cols) * 340 + 5
    sheet.paste(t, (cx, cy)); d.text((cx, cy + 305), fn.replace(setname + '_', ''), font=f, fill=(40, 40, 40))
sheet.save(os.path.join(out, f'{setname}_uebersicht.jpg'), quality=90)
print(len(thumbs), 'Teile')
