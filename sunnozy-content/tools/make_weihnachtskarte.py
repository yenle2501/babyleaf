"""Weihnachts-Anhaenger / Dankeskarte fuer die Geschenkboxen, druckfertig.

Vorbild (Bild der Nutzerin): weisser Geschenkanhaenger mit abgeschraegten Ecken und Loch, rot-weiss gestreifte
Aquarell-Schleife, darunter «Merry Christmas» in feiner Schreibschrift. Die Schleife ist mit Canva-KI erzeugt
(`posts/kampagne-weihnachtsbox/karte/schleife.png`), die Schrift ist Great Vibes (Google Fonts, OFL).

Format: 60 x 100 mm + 3 mm Beschnitt = 66 x 106 mm, 300 dpi. Vorderseite: Schleife, Gruss, Logo. Rueckseite: «Für»,
«Von», Dank und sunnozy.ch. Die Stanzform (abgeschraegte Ecken, Loch 5 mm) liegt als Vorschau bei; die Druckerei
schneidet bzw. stanzt danach. Ausserdem ein freigestellter Anhaenger als PNG (fuer Fotos und Anzeigen).

Aufruf: python3 make_weihnachtskarte.py <karten-ordner> [Gruss]
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
GRUSS = sys.argv[2] if len(sys.argv) > 2 else 'Merry\nChristmas'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
DPI = 300
MM = DPI / 25.4
W, H = round(66 * MM), round(106 * MM)
B = 3 * MM                                       # Beschnitt
TINTE, WALD, GRAU, PAPIER = (28, 28, 30), (35, 48, 41), (110, 112, 106), (255, 255, 255)


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def form(w, h, x0=0, y0=0):
    """Anhaengerform: oben abgeschraegte Ecken (12 mm), Loch 5 mm mittig 9 mm unter der Oberkante."""
    s = 12 * MM
    return [(x0 + s, y0), (x0 + w - s, y0), (x0 + w, y0 + s), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0 + s)]


def vorne():
    c = Image.new('RGB', (W, H), PAPIER)
    sl = Image.open(os.path.join(out, 'schleife.png')).convert('RGB')
    a = np.asarray(sl).astype(float); m = (255 - a.min(axis=2)) > 12; ys, xs = np.where(m)
    sl = sl.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    a = np.asarray(sl).astype(float); a = np.clip(a * 255 / np.percentile(a, 97, axis=(0, 1)), 0, 255)
    sl = Image.fromarray(a.astype(np.uint8))                # Papiergrund der Schleife auf Reinweiss
    bw = int(40 * MM); sl = sl.resize((bw, round(sl.height * bw / sl.width)), Image.LANCZOS)
    x, y = (W - bw) // 2, int(B + 17 * MM)
    reg = c.crop((x, y, x + sl.width, y + sl.height))
    c.paste(Image.fromarray(np.minimum(np.asarray(reg), np.asarray(sl))), (x, y))
    d = ImageDraw.Draw(c)
    f = FONT('greatvibes.ttf', 11.5 * MM)
    ty = y + sl.height + 3 * MM
    for z in GRUSS.split('\n'):
        d.text((W / 2, ty), z, font=f, fill=TINTE, anchor='mt'); ty += 10 * MM
    lg = load_logo(int(18 * MM), (122, 108, 104)); c.paste(lg, ((W - lg.width) // 2, int(H - B - 7 * MM)), lg)
    return c


def hinten():
    c = Image.new('RGB', (W, H), PAPIER); d = ImageDraw.Draw(c)
    fs, fl = FONT('greatvibes.ttf', 9 * MM), FONT('nunitosans-600.ttf', 2.5 * MM)
    x0, x1 = B + 8 * MM, W - B - 8 * MM
    for i, t in enumerate(('Für', 'Von')):
        y = B + 30 * MM + i * 16 * MM
        d.text((x0, y), t, font=fs, fill=TINTE, anchor='ls')
        d.line([(x0 + 13 * MM, y), (x1, y)], fill=(200, 196, 190), width=3)
    y = B + 70 * MM
    for z in ('Von Hand für Dich eingepackt.', 'Danke, dass Du mit sunnozy schenkst.'):
        d.text((W / 2, y), z, font=fl, fill=GRAU, anchor='ms'); y += 4.6 * MM
    d.text((W / 2, H - B - 8 * MM), 'sunnozy.ch', font=FONT('nunitosans-700.ttf', 3.2 * MM), fill=WALD, anchor='ms')
    return c


def ausgeschnitten(seite):
    """Endformat mit Stanzform als RGBA (ohne Beschnitt), fuer Fotos, Anzeigen und Vorschau."""
    e = seite.crop((int(B), int(B), int(W - B), int(H - B)))
    m = Image.new('L', e.size, 0); dm = ImageDraw.Draw(m)
    dm.polygon(form(e.width, e.height), fill=255)
    r, cy = 2.5 * MM, 9 * MM
    dm.ellipse([e.width / 2 - r, cy - r, e.width / 2 + r, cy + r], fill=0)
    e = e.convert('RGBA'); e.putalpha(m)
    return e


if __name__ == '__main__':
    v, h = vorne(), hinten()
    v.save(os.path.join(out, 'karte_vorne_druck.png'), dpi=(DPI, DPI))
    h.save(os.path.join(out, 'karte_hinten_druck.png'), dpi=(DPI, DPI))
    v.save(os.path.join(out, 'karte_druck.pdf'), resolution=DPI, save_all=True, append_images=[h])
    av, ah = ausgeschnitten(v), ausgeschnitten(h)
    av.save(os.path.join(out, 'karte_vorne_freigestellt.png'))
    vs = Image.new('RGB', (av.width * 2 + 120, av.height + 80), (236, 232, 226))
    for i, e in enumerate((av, ah)):
        sh = Image.new('RGBA', e.size, (0, 0, 0, 0)); sh.putalpha(e.getchannel('A').point(lambda p: p * 0.18))
        vs.paste((90, 80, 70), (40 + i * (e.width + 40) + 8, 48), sh)
        vs.paste(e, (40 + i * (e.width + 40), 40), e)
    vs.save(os.path.join(out, 'karte_vorschau.jpg'), quality=92)
    print('ok', v.size)
