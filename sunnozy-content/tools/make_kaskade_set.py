"""Shopify-Hauptbild im Kaskaden-Look fuer Erstausstattungs-Sets (gleicher Stil wie make_kaskade.py).

Grosse Teile (Decke, Strampler, Body, Jaeckchen, Hose) schraeg gestaffelt links, kleine Teile (Muetze, Laetzchen,
Rassel, Socken, Faeustlinge) als zweite, kleinere Staffel rechts. Alle Teile in realistischem Groessenverhaeltnis
(ungefaehre Hoehe in cm). Quelle: freigestellte echte Shop-Fotos, Ausgabe 2048 x 2048 JPG, reinweiss (BG=r,g,b als Umgebungsvariable).

Aufruf: python3 make_kaskade_set.py <teile-ordner> <ausgabe-ordner> [nur_set ...]
"""
import sys, os
from PIL import Image, ImageFilter

src, out = sys.argv[1:3]
only = set(sys.argv[3:])
os.makedirs(out, exist_ok=True)
SIZE, FILL = 2048, 0.88
BG = tuple(int(v) for v in os.environ.get("BG", "255,255,255").split(","))
PX_CM = 16  # Pixel pro cm vor dem Einpassen

CM = {'decke': 52, 'strampler': 56, 'body': 38, 'jaeckchen': 30, 'shirt': 28, 'hose': 40,
      'muetze': 22, 'haube': 21, 'laetzchen': 29, 'rassel': 22, 'socken': 16, 'faeustlinge': 16}  # Kleinteile leicht vergroessert, damit sie im Bild lesbar sind

# Set -> (grosse Teile hinten -> vorne, kleine Teile oben -> unten); Eintrag (Datei, Art)
SETS = {
    'erstausstattung_princess': ('princess', [('03', 'decke'), ('01', 'strampler'), ('02', 'body')],
                                 [('08', 'muetze'), ('07', 'rassel'), ('05', 'socken'), ('06', 'faeustlinge'), ('04', 'laetzchen')]),
    'erstausstattung_little_and_loved': ('little_loved', [('01', 'strampler'), ('05', 'hose'), ('03', 'jaeckchen'), ('04', 'shirt'), ('02', 'body')],
                                         [('07', 'muetze'), ('08', 'faeustlinge'), ('06', 'laetzchen')]),
    'erstausstattung_hello_rosa': ('hello_rosa', [('05', 'decke'), ('01', 'strampler'), ('03', 'hose'), ('02', 'body')],
                                   [('06', 'haube'), ('04', 'laetzchen')]),
    'erstausstattung_hello_little_bear': ('little_bear', [('01', 'strampler'), ('02', 'body')],
                                          [('03', 'muetze'), ('04', 'faeustlinge'), ('05', 'laetzchen')]),
    'erstausstattung_hello_world': ('hello_world', [('01', 'strampler'), ('05', 'hose'), ('02', 'jaeckchen'), ('03', 'shirt'), ('04', 'body')],
                                    [('07', 'muetze'), ('08', 'faeustlinge'), ('06', 'laetzchen')]),
}


def load(folder, n, art):
    im = Image.open(os.path.join(src, folder, n + '.png')).convert('RGBA')
    im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7)))
    im = im.crop(im.getchannel('A').getbbox())
    h = CM[art] * PX_CM
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def shadowed(lay, im, x, y):
    W, H = lay.size
    sh = Image.new('L', (W, H), 0); sh.paste(im.getchannel('A'), (x + 10, y + 18))
    sh = sh.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.2))
    d = Image.new('RGBA', (W, H), (60, 55, 50, 0)); d.putalpha(sh)
    lay = Image.alpha_composite(lay, d); lay.alpha_composite(im, (x, y)); return lay


def cascade(items, step_y, step_x):
    """Hinten oben rechts -> vorne unten links; Mitte jedes Teils auf einer Diagonalen."""
    n = len(items)
    W = max(i.width for i in items) + (n - 1) * step_x + 300
    H = max(i.height + k * step_y for k, i in enumerate(items)) + 300
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cx0 = W - 150 - max(i.width for i in items) / 2
    for k, im in enumerate(items):
        cx = cx0 - k * step_x
        lay = shadowed(lay, im, int(cx - im.width / 2), 150 + k * step_y)
    return lay.crop(lay.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox())


def small_group(items):
    """Kleinteile: bis 3 Stueck untereinander, ab 4 Stueck in zwei Spalten (leicht versetzt)."""
    cols = 2 if len(items) >= 4 else 1
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    cw = max(i.width for i in items); pad = int(1.2 * PX_CM)
    W = cols * cw + (cols - 1) * pad + 300
    H = sum(max(i.height for i in r) for r in rows) + (len(rows) - 1) * pad + 300
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); y = 150
    for ri, r in enumerate(rows):
        rh = max(i.height for i in r)
        off = (cw // 4 if ri % 2 else 0) if cols == 2 and len(r) == 1 else 0
        for ci, im in enumerate(r):
            cx = 150 + ci * (cw + pad) + cw / 2 + (cw / 2 + pad / 2 if cols == 2 and len(r) == 1 else 0)
            lay = shadowed(lay, im, int(cx - im.width / 2), int(y + (rh - im.height) / 2))
        y += rh + pad
    return lay.crop(lay.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox())


for name, (folder, big, small) in SETS.items():
    if only and name not in only:
        continue
    B = [load(folder, n, a) for n, a in big]
    Sm = [load(folder, n, a) for n, a in small]
    nb = len(B)
    a = cascade(B, int(CM['strampler'] * PX_CM * (0.42 if nb <= 3 else 0.3)), int(CM['body'] * PX_CM * (0.32 if nb <= 3 else 0.24)))
    b = small_group(Sm)
    gap = int(4 * PX_CM)
    H = max(a.height, b.height)
    lay = Image.new('RGBA', (a.width + gap + b.width, H), (0, 0, 0, 0))
    lay.alpha_composite(a, (0, (H - a.height) // 2)); lay.alpha_composite(b, (a.width + gap, (H - b.height) // 2))
    s = min(SIZE * FILL / lay.width, SIZE * FILL / lay.height)
    lay = lay.resize((round(lay.width * s), round(lay.height * s)), Image.LANCZOS)
    c = Image.new('RGBA', (SIZE, SIZE), BG + (255,))
    c.alpha_composite(lay, ((SIZE - lay.width) // 2, (SIZE - lay.height) // 2))
    c = c.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.0, percent=40, threshold=2))
    c.save(os.path.join(out, name + '.jpg'), quality=93, subsampling=0)
    print(name, f'{lay.width}x{lay.height}')
