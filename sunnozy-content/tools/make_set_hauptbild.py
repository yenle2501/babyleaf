"""Shop-Hauptbild eines Erstausstattungs-Sets aus den scharfen Einzelteil-Bildern (2000 px, reinweiss) zusammenbauen.

Stil nach dem Vorbild der Nutzerin (Teddybär-Set): warmer, heller Studio-Grund, Decke oder Strampler an einem
Holzbügel mit Wandknauf (assets/buegel_holz.png), die übrigen Teile gross und geordnet daneben, weiche Schatten,
sunnozy-Logo oben links.
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
BG = (238, 236, 232)
BUEGEL = os.path.join(ROOT, 'assets', 'buegel_holz.png')
B_HAKEN_X, B_SPITZE_Y, B_DECKE_Y = 338, 186, 400     # Ankerpunkte im Bügel-PNG

# Pro Set: Ordner, Dateipräfix, Teil am Bügel und Kästen (x0, y0, x1, y1) in Pixeln eines 1254er-Rasters
# (Masse des Vorbilds). Jedes Teil wird in seinen Kasten eingepasst.
R = 1254
SETS = {
    'erstausstattung-set-teddybaer': ('set_teddy_creme', 'set_teddy_creme_', 'decke', {
        'decke': (25, 420, 400, 1210), 'muetze': (490, 70, 710, 360), 'socken': (755, 140, 900, 320),
        'faeustlinge': (925, 140, 1170, 320), 'beissring': (835, 330, 1010, 480), 'rassel': (1030, 335, 1180, 505),
        'strampler': (408, 400, 868, 1190), 'body': (858, 505, 1218, 958), 'laetzchen': (922, 962, 1172, 1210)}),
    'erstausstattung-set-princess': ('set_rosa', 'set_rosa_', 'decke', {
        'decke': (25, 420, 400, 1210), 'muetze': (470, 70, 700, 360), 'faeustlinge': (735, 130, 935, 320),
        'socken': (960, 120, 1080, 330), 'rassel': (1095, 110, 1225, 340),
        'strampler': (408, 400, 868, 1190), 'body': (858, 400, 1218, 900), 'laetzchen': (900, 920, 1180, 1210)}),
    'erstausstattung-set-little-and-loved': ('set_little_and_loved_gans_rosa', '', 'strampler', {
        'strampler': (25, 330, 405, 1200), 'muetze': (460, 70, 690, 330), 'faeustlinge': (725, 120, 935, 300),
        'laetzchen': (965, 60, 1215, 390), 'body': (440, 410, 820, 820), 'jaeckchen': (845, 420, 1225, 830),
        'shirt': (445, 860, 815, 1195), 'hose': (870, 850, 1200, 1225)}),
    'erstausstattung-set-hello-world': ('set_hello_world_blatt_creme', '', 'strampler', {
        'strampler': (25, 330, 405, 1200), 'muetze': (460, 70, 690, 330), 'faeustlinge': (725, 120, 935, 300),
        'laetzchen': (980, 60, 1200, 390), 'jaeckchen': (430, 420, 820, 810), 'body': (850, 410, 1220, 830),
        'shirt': (445, 860, 815, 1195), 'hose': (880, 850, 1190, 1225)}),
    'erstausstattung-set-hello-spitze': ('set_hello_schmetterling', 'set_hello_schmetterling_', 'decke', {
        'decke': (25, 420, 410, 1210), 'haeubchen': (500, 70, 720, 360), 'laetzchen': (800, 80, 1170, 420),
        'strampler': (430, 420, 850, 1200), 'body': (860, 450, 1220, 840), 'hose': (890, 850, 1200, 1220)}),
    'erstausstattung-set-hello-little-bear': ('set_little_bear', 'set_little_bear_', 'strampler', {
        'strampler': (15, 360, 660, 1235), 'muetze': (690, 110, 950, 400), 'faeustlinge': (975, 150, 1230, 380),
        'body': (680, 480, 1010, 1080), 'laetzchen': (1015, 600, 1240, 1000)}),
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
    x0, y0, x1, y1 = (v * N / R for v in box)
    w, h = x1 - x0, y1 - y0
    k = min(w / t.width, h / t.height)
    t = t.resize((round(t.width * k), round(t.height * k)), Image.LANCZOS)
    return t, (int(x0 + (w - t.width) / 2), int(y0 if oben else y0 + (h - t.height) / 2))


def schatten(c, t, pos, off=(10, 16), blur=24, staerke=0.22):
    sh = Image.new('L', (t.width + 120, t.height + 120), 0)
    sh.paste(t.split()[3], (60, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * staerke))
    dunkel = Image.new('RGB', sh.size, (150, 140, 128))
    c.paste(dunkel, (pos[0] - 60 + off[0], pos[1] - 60 + off[1]), sh)


def buegel(c, t, pos, decke):
    """Holzbügel hinter das Teil setzen. Decke: liegt über der Stange. Strampler: Bügel steckt in den Schultern."""
    B = Image.open(BUEGEL)
    k = t.width / 555 if decke else t.width * 0.78 / B.width
    B = B.resize((round(B.width * k), round(B.height * k)), Image.LANCZOS)
    x = pos[0] + t.width // 2 - round(B_HAKEN_X * k)
    y = pos[1] - round((B_DECKE_Y if decke else B_SPITZE_Y + 25) * k)
    schatten(c, B, (x, y), off=(8, 12), blur=10, staerke=0.18)
    c.alpha_composite(B, (x, y))


def hintergrund():
    yy, xx = np.mgrid[0:N, 0:N] / N
    licht = 1.018 - 0.03 * (0.6 * xx + 0.4 * yy)       # links oben etwas heller, wie im Vorbild
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
        t, pos = einpassen(t, box, oben=(name == am_buegel and name != 'decke'))
        if name == am_buegel:
            buegel(c, t, pos, decke=(name == 'decke'))
        schatten(c, t, pos)
        c.alpha_composite(t, pos)
    lg = logo(int(N * 0.205)); c.alpha_composite(lg, (int(N * 0.033), int(N * 0.028)))
    return c.convert('RGB')


if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for h in (sys.argv[2:] or SETS):
        bauen(h).save(os.path.join(out, h + '.jpg'), quality=95)
        print(h)
