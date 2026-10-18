"""Shop-Hauptbild eines Erstausstattungs-Sets aus den scharfen Einzelteil-Bildern (2000 px, reinweiss) zusammenbauen.

Stil wie die KI-Präsentationen: hellgrauer Studio-Hintergrund, Decke oder Strampler auf einem Holzbügel
am Wandknauf, die übrigen Teile luftig daneben, weiche Schatten, sunnozy-Logo oben links.
Jedes Teil wird verkleinert statt vergrössert, deshalb bleiben Print, Rippen und Spitze scharf.

Aufruf: python3 make_set_hauptbild.py <ausgabeordner> [set ...]
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEILE = os.path.join(ROOT, 'posts', 'marktplatz-galaxus-amazon', 'einzelteile')
N = 2048
BG = (231, 231, 230)

# Pro Set: Ordner, Dateipräfix, Teil am Bügel und Kästen (x, y, b, h) in Anteilen der Bildbreite.
# Das Teil wird in seinen Kasten eingepasst; 'oben' richtet es oben statt mittig aus.
SETS = {
    'erstausstattung-set-teddybaer': ('set_teddy_creme', 'set_teddy_creme_', 'decke', {
        'decke': (0.04, 0.215, 0.30, 0.56), 'strampler': (0.33, 0.28, 0.31, 0.67),
        'muetze': (0.36, 0.06, 0.15, 0.17), 'socken': (0.535, 0.075, 0.11, 0.15), 'faeustlinge': (0.665, 0.085, 0.13, 0.13),
        'beissring': (0.65, 0.255, 0.14, 0.09), 'rassel': (0.81, 0.215, 0.15, 0.14),
        'body': (0.65, 0.39, 0.31, 0.31), 'laetzchen': (0.69, 0.72, 0.24, 0.22)}),
    'erstausstattung-set-princess': ('set_rosa', 'set_rosa_', 'decke', {
        'decke': (0.04, 0.215, 0.30, 0.52), 'strampler': (0.34, 0.30, 0.29, 0.60),
        'muetze': (0.37, 0.06, 0.15, 0.17), 'faeustlinge': (0.545, 0.085, 0.13, 0.13), 'socken': (0.70, 0.07, 0.11, 0.16),
        'rassel': (0.84, 0.06, 0.12, 0.18), 'body': (0.65, 0.29, 0.31, 0.33), 'laetzchen': (0.69, 0.67, 0.23, 0.23)}),
    'erstausstattung-set-little-and-loved': ('set_little_and_loved_gans_rosa', '', 'strampler', {
        'strampler': (0.03, 0.215, 0.26, 0.70), 'muetze': (0.31, 0.06, 0.18, 0.17), 'faeustlinge': (0.52, 0.08, 0.15, 0.13),
        'laetzchen': (0.72, 0.05, 0.22, 0.22), 'body': (0.32, 0.29, 0.28, 0.30), 'jaeckchen': (0.63, 0.31, 0.32, 0.29),
        'shirt': (0.32, 0.63, 0.28, 0.25), 'hose': (0.66, 0.62, 0.25, 0.34)}),
    'erstausstattung-set-hello-world': ('set_hello_world_blatt_creme', '', 'strampler', {
        'strampler': (0.03, 0.215, 0.26, 0.70), 'muetze': (0.31, 0.06, 0.18, 0.17), 'faeustlinge': (0.52, 0.08, 0.15, 0.13),
        'laetzchen': (0.74, 0.05, 0.19, 0.22), 'jaeckchen': (0.32, 0.30, 0.30, 0.28), 'body': (0.65, 0.29, 0.28, 0.31),
        'shirt': (0.32, 0.63, 0.28, 0.25), 'hose': (0.67, 0.62, 0.24, 0.34)}),
    'erstausstattung-set-hello-spitze': ('set_hello_schmetterling', 'set_hello_schmetterling_', 'decke', {
        'decke': (0.03, 0.22, 0.38, 0.70), 'haeubchen': (0.47, 0.07, 0.20, 0.24), 'laetzchen': (0.72, 0.08, 0.26, 0.25),
        'strampler': (0.42, 0.37, 0.20, 0.59), 'body': (0.62, 0.38, 0.20, 0.34), 'hose': (0.81, 0.38, 0.17, 0.58)}),
    'erstausstattung-set-hello-little-bear': ('set_little_bear', 'set_little_bear_', 'strampler', {
        'strampler': (0.03, 0.215, 0.40, 0.75), 'muetze': (0.53, 0.06, 0.24, 0.24), 'body': (0.44, 0.34, 0.30, 0.38),
        'laetzchen': (0.76, 0.36, 0.21, 0.30), 'faeustlinge': (0.58, 0.76, 0.24, 0.18)}),
}


def freistellen(path):
    """Teil vom reinweissen Grund lösen: Hintergrund = fast weisse Fläche, die mit dem Bildrand verbunden ist.
    Weisse Stellen im Teil (weisser Body, Kragen) bleiben, reinweisse Löcher (Halsloch am Lätzchen,
    Ring der Rassel) werden durchsichtig."""
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    mn = a.min(axis=2)
    lab, _ = ndimage.label(mn >= 250)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    obj = ndimage.binary_fill_holes(~np.isin(lab, list(rand)))
    lab2, n2 = ndimage.label((mn >= 250) & obj)
    if n2:
        mittel = ndimage.mean(mn, lab2, range(1, n2 + 1))
        groesse = ndimage.sum(np.ones_like(lab2), lab2, range(1, n2 + 1))
        obj &= ~np.isin(lab2, [i + 1 for i in range(n2) if mittel[i] >= 253.5 and groesse[i] > 1500])
    obj = ndimage.binary_opening(obj, iterations=2)
    obj = ndimage.binary_erosion(obj, iterations=3)          # heller Saum der Originalkante weg
    alpha = Image.fromarray((obj * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    # verbleibende helle Randpixel an den Grund angleichen (multiplizieren statt überdecken)
    rand_band = obj & ~ndimage.binary_erosion(obj, iterations=4)
    b = a.astype(np.float32)
    b[rand_band] = b[rand_band] * np.array(BG, np.float32) / 255 * 1.03
    im = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
    rgba = im.copy(); rgba.putalpha(alpha)
    return rgba.crop(alpha.getbbox())


def einpassen(t, box, oben=False):
    x, y, w, h = (v * N for v in box)
    s = min(w / t.width, h / t.height)
    t = t.resize((round(t.width * s), round(t.height * s)), Image.LANCZOS)
    return t, (int(x + (w - t.width) / 2), int(y if oben else y + (h - t.height) / 2))


def schatten(c, t, pos, off=(0, 14), blur=22, staerke=0.20):
    sh = Image.new('L', (t.width + 120, t.height + 120), 0)
    sh.paste(t.split()[3], (60, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * staerke))
    dunkel = Image.new('RGB', sh.size, (120, 120, 118))
    c.paste(dunkel, (pos[0] - 60 + off[0], pos[1] - 60 + off[1]), sh)


def buegel(c, cx, y, breite):
    """Holzbügel mit Messinghaken an einem Wandknauf, 4-fach überabgetastet für saubere Kanten."""
    k = 4; W = int(breite * 1.3); H = int(N * 0.20)
    L = Image.new('RGBA', (W * k, H * k), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    mx = W * k // 2
    knopf_y, bar_y = int(H * 0.12) * k, int(H * 0.80) * k
    r = int(N * 0.013) * k
    # Haken
    d.line([(mx, knopf_y + r), (mx, bar_y - int(H * 0.22) * k)], fill=(150, 130, 95, 255), width=int(N * 0.004) * k)
    d.arc([mx - int(N * 0.018) * k, knopf_y - r // 2, mx + int(N * 0.018) * k, knopf_y + int(N * 0.03) * k],
          200, 340, fill=(150, 130, 95, 255), width=int(N * 0.004) * k)
    # Bügel: zwei Arme, leicht gebogen
    dicke = int(N * 0.012) * k; halb = int(breite / 2) * k
    top = bar_y - int(H * 0.22) * k
    for sgn in (-1, 1):
        pts = []
        for i in range(41):
            u = i / 40
            pts.append((mx + sgn * u * halb, top + (bar_y - top) * (1 - (1 - u) ** 1.8)))
        for j in range(dicke):
            sh = j / dicke
            col = (int(196 + 30 * (1 - sh)), int(158 + 26 * (1 - sh)), int(110 + 22 * (1 - sh)), 255)
            d.line([(px, py + j) for px, py in pts], fill=col, width=2)
    d.ellipse([mx - dicke * 0.9, top - dicke * 0.2, mx + dicke * 0.9, top + dicke * 1.4], fill=(205, 168, 118, 255))
    # Wandknauf
    d.ellipse([mx - r, knopf_y - r, mx + r, knopf_y + r], fill=(176, 140, 98, 255))
    d.ellipse([mx - r * 0.55, knopf_y - r * 0.7, mx + r * 0.25, knopf_y - r * 0.05], fill=(214, 184, 140, 255))
    L = L.resize((W, H), Image.LANCZOS)
    pos = (int(cx - W / 2), int(y - H * 0.80))
    schatten(c, L, pos, off=(6, 10), blur=10, staerke=0.25)
    c.alpha_composite(L, pos)
    return pos[1] + int(H * 0.80) - int(H * 0.22)   # Oberkante des Bügels


def hintergrund():
    yy, xx = np.mgrid[0:N, 0:N] / N
    licht = 1 + 0.025 * (1 - ((xx - 0.45) ** 2 + (yy - 0.35) ** 2) * 2)
    a = np.clip(np.array(BG)[None, None, :] * licht[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(a, 'RGB').convert('RGBA')


def logo(width, color=(120, 112, 115)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), color + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def bauen(handle):
    ordner, prefix, am_buegel, kaesten = SETS[handle]
    c = hintergrund()
    for name, box in kaesten.items():
        t = freistellen(os.path.join(TEILE, ordner, prefix + name + '.jpg'))
        t, pos = einpassen(t, box, oben=(name == am_buegel))
        schatten(c, t, pos)
        c.alpha_composite(t, pos)
        if name == am_buegel:
            strampler = name == 'strampler'
            buegel(c, pos[0] + t.width // 2, pos[1] + t.height * (0.075 if strampler else 0.012),
                   t.width * (0.56 if strampler else 0.86))
    lg = logo(int(N * 0.2)); c.alpha_composite(lg, (int(N * 0.035), int(N * 0.03)))
    return c.convert('RGB')


if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for h in (sys.argv[2:] or SETS):
        bauen(h).save(os.path.join(out, h + '.jpg'), quality=95)
        print(h)
