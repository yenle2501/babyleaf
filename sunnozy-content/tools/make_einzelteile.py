"""Einzelteile aus einem freigestellten Set-Hauptbild extrahieren -> je ein Marktplatz-Foto pro Teil.

Funktionsweise: zusammenhaengende Flaechen labeln; verschmolzene Kleider (Aermel ueberlappen) per Kern-Trennung
(Erosion -> mehrere grosse Kerne -> Pixel dem naechsten Kern zuweisen) aufteilen; Paare (Socken, Faeustlinge: gleiche Form,
nebeneinander) zusammenfassen; Bruchstuecke (duenne Rassel-Teile) an den naechsten kleinen Nachbarn haengen; Kruemel verwerfen;
jedes Teil auf reinweiss 2000x2000 setzen (via make_marktplatz-Logik).

Aufruf: python3 make_einzelteile.py <set.png> <ausgabeordner> [paar_abstand_px=6 % der Bildbreite, '-' = Standard] [namen=kommagetrennt] [schnitt]
  schnitt: optional, Schnittlinien fuer flaechig ueberlappende Teile, Pixelkoordinaten im PNG: "x1,y1,x2,y2,...;x1,y1,..."
  namen: optional, in Lesereihenfolge (oben->unten, links->rechts); sonst teil_01, teil_02 ...; 'x' = Teil ueberspringen
  Ausgabe: <ausgabe>/<set>_<name>.jpg + Kontaktbogen <set>_uebersicht.jpg
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from scipy import ndimage

src, out = sys.argv[1:3]
gap_arg = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] not in ('', '-') else None
gap = gap_arg
names = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] not in ('', '-') else None
cuts = [list(map(int, c.split(','))) for c in sys.argv[5].split(';')] if len(sys.argv) > 5 and sys.argv[5] else []
S, FILL = 2000, 0.85
os.makedirs(out, exist_ok=True)
setname = os.path.splitext(os.path.basename(src))[0]

im = Image.open(src).convert('RGBA')
alpha = np.asarray(im.getchannel('A'))
mask = alpha > 40
full = mask.copy()
if cuts:  # Schnittlinien aus der Maske nehmen; die Linienpixel bekommen am Ende das naechste Teil
    cm = Image.new('L', im.size, 0); dc = ImageDraw.Draw(cm)
    for c in cuts:
        dc.line(list(zip(c[0::2], c[1::2])), fill=255, width=3)
    mask &= np.asarray(cm) == 0
total = mask.sum()
H0, W0 = mask.shape
if gap_arg is None:
    gap = round(min(H0, W0) * 0.06)
EROS = (max(4, round(min(H0, W0) * 0.007)), round(min(H0, W0) * 0.03), round(min(H0, W0) * 0.045))


def split(comp):
    """Verschmolzene Teile trennen: mehrere grosse Kerne nach Erosion -> naechster Kern."""
    a = comp.sum()
    for it in EROS:
        cl, cn = ndimage.label(ndimage.binary_erosion(comp, iterations=it))
        if cn < 2:
            continue
        ca = ndimage.sum(np.ones_like(cl), cl, range(1, cn + 1))
        keep = [j + 1 for j, v in enumerate(ca) if v >= max(total * 0.01, a * 0.12)]
        if len(keep) >= 2:
            cl = np.where(np.isin(cl, keep), cl, 0)
            _, (iy, ix) = ndimage.distance_transform_edt(cl == 0, return_indices=True)
            return np.where(comp, cl[iy, ix], 0)
    return comp.astype(int)


# 1) echte Flaechen, verschmolzene Kleider aufteilen
lab0, n0 = ndimage.label(mask)
lab = np.zeros(mask.shape, int); nxt = 1
for i, sl in enumerate(ndimage.find_objects(lab0), 1):
    comp = lab0[sl] == i
    if comp.sum() < total * 0.0005:
        continue
    sub = split(comp)
    view = lab[sl]
    for k in np.unique(sub):
        if k:
            view[sub == k] = nxt; nxt += 1


def comps(lab):
    ids = [i for i in np.unique(lab) if i]
    return {i: (lab == i) for i in ids}


def boxes(cs):
    return {i: ndimage.find_objects(m.astype(int))[0] for i, m in cs.items()}


if cuts:
    _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    lab = np.where(full, lab[iy, ix], 0); mask = full
# 2) Paare (Socken, Faeustlinge): klein, aehnliche Flaeche und Hoehe, nebeneinander, Abstand <= gap
cs = comps(lab); ar = {i: m.sum() for i, m in cs.items()}; bb = boxes(cs)
cand = []
small_ids = [i for i in cs if ar[i] < total * 0.06]
for x in small_ids:
    for y in small_ids:
        if x >= y:
            continue
        (ya, xa), (yb, xb) = bb[x], bb[y]
        ha, hb = ya.stop - ya.start, yb.stop - yb.start
        ov = min(ya.stop, yb.stop) - max(ya.start, yb.start)
        dx = max(0, max(xa.start, xb.start) - min(xa.stop, xb.stop))
        fa = ar[x] / (ha * (xa.stop - xa.start)); fb = ar[y] / (hb * (xb.stop - xb.start))  # Fuellgrad der Box (Form)
        if 0.6 < ar[x] / ar[y] < 1.67 and 0.75 < ha / hb < 1.33 and 0.8 < fa / fb < 1.25 and ov >= 0.6 * min(ha, hb) and dx <= gap:
            cand.append((dx, x, y))
used = set()
for dx, x, y in sorted(cand):
    if x not in used and y not in used:
        lab[lab == y] = x; used |= {x, y}
# 3) Bruchstuecke an naechsten Nachbarn (bevorzugt kleine Teile) innerhalb ~3 % Bildbreite haengen
dmax = min(H0, W0) * 0.03
changed = True
while changed:
    changed = False
    cs = comps(lab); ar = {i: m.sum() for i, m in cs.items()}
    for i, m in sorted(cs.items(), key=lambda kv: ar[kv[0]]):
        if ar[i] >= total * 0.01:
            break
        dist = ndimage.distance_transform_edt(~m)
        others = [j for j in cs if j != i]
        if not others:
            break
        dmin = dict(zip(others, ndimage.minimum(dist, lab, others)))
        near = [j for j in others if dmin[j] <= dmax]
        if not near:
            continue
        smalls = [j for j in near if ar[j] < total * 0.08]
        tgt = min(smalls or near, key=lambda j: dmin[j])
        lab[m] = tgt; changed = True; break
parts = []
for i, m in comps(lab).items():
    if m.sum() < total * 0.003:
        continue
    ys, xs = np.nonzero(m)
    parts.append((ys.min(), xs.min(), ys.max() + 1, xs.max() + 1, m))
# Lesereihenfolge: Zeilen nach Mittelpunkt (Toleranz = 1/8 Bildhoehe), dann links->rechts
rowtol = mask.shape[0] / 8
parts.sort(key=lambda p: (round(((p[0] + p[2]) / 2) / rowtol), (p[1] + p[3]) / 2))

thumbs = []
for k, (y0, x0, y1, x1, m) in enumerate(parts):
    name = names[k] if names and k < len(names) else f'teil_{k + 1:02d}'
    if name == 'x':  # Teil ueberspringen (z.B. separat rekonstruiert)
        continue
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
