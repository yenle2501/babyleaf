"""Instagram-Karussell (4:5) «Sold Out» für das Erstausstattung-Set «Hello» in Rosa, 27.10.2026.
Idee der Nutzerin: Schleife mit langem Band und «Sold Out» in einer Serifenschrift (hier Fraunces, keine Schreibschrift).

    python3 tools/make_post_hello_ausverkauft.py

1  Sold Out: Schleife (KI, Canva) + Titel + freigestelltes Set
2  Danke: KI-Foto, Hände packen das Set in eine Geschenkbox
3  Danke-Text + echte Bewertung (MariolyG, Judge.me, wörtlich)
4  Restock in Arbeit (ohne Datum, kein Versprechen)
Ausgabe: posts/instagram/hello-ausverkauft/slide_<n>_4x5.jpg + uebersicht.jpg
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'posts', 'instagram', 'hello-ausverkauft')
BILD = os.path.join(OUT, 'bilder')
SET = os.path.join(ROOT, 'posts', 'marktplatz-galaxus-amazon', 'freigestellt', 'set_hello_schmetterling.png')
W, H = 1080, 1350
CREME, WALD, GRAU, ROSE, STERN = (251, 248, 244), (35, 48, 41), (112, 118, 114), (146, 84, 92), (214, 168, 92)
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))


def fuellen(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    t = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((t.width - w) * fx); y = int((t.height - h) * fy)
    return t.crop((x, y, x + w, y + h))


def logo(width, col):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def umbrechen(d, text, font, breite):
    zeilen, z = [], ''
    for wort in text.split():
        t = (z + ' ' + wort).strip()
        if d.textlength(t, font=font) <= breite:
            z = t
        else:
            zeilen.append(z); z = wort
    return zeilen + [z]


def absatz(d, x, y, text, font, farbe, breite, zeilenhoehe, anchor='ma'):
    for z in umbrechen(d, text, font, breite):
        d.text((x, y), z, font=font, fill=farbe, anchor=anchor); y += zeilenhoehe
    return y


def sterne(d, cx, y, r=20, abstand=52):
    for i in range(5):
        x0 = cx + (i - 2) * abstand
        pts = [(x0 + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5), y - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
        d.polygon(pts, fill=STERN)


def set_bild(breite):
    im = Image.open(SET).convert('RGBA'); im = im.crop(im.getbbox())
    return im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)


def slide1():
    c = fuellen(Image.open(os.path.join(BILD, 'schleife_ki.jpg')).convert('RGB'), W, H, 0.5, 0.0).convert('RGBA')
    d = ImageDraw.Draw(c); cx = 500
    f = F('fraunces-600.ttf', 188)
    d.text((cx, 690), 'Sold', font=f, fill=ROSE, anchor='ms'); d.text((cx, 870), 'Out', font=f, fill=ROSE, anchor='ms')
    s = set_bild(380); c.alpha_composite(s, (cx - s.width // 2 - 30, 925))
    d.text((cx - 30, 1318), 'Erstausstattung-Set «Hello» in Rosa', font=F('nunitosans-600.ttf', 30), fill=GRAU, anchor='ms')
    return c.convert('RGB')


def slide2():
    c = fuellen(Image.open(os.path.join(BILD, 'verpacken_ki.jpg')).convert('RGB'), W, H, 0.5, 0.35).convert('RGBA')
    g = np.zeros((H, 1), np.float32); g[820:, 0] = np.clip(np.arange(H - 820) / 420.0, 0, 1) ** 1.2 * 0.62
    sch = Image.new('RGBA', (W, H), (40, 28, 26, 0)); sch.putalpha(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H)))
    c = Image.alpha_composite(c, sch); d = ImageDraw.Draw(c)
    y = absatz(d, 80, 1105, 'Danke für Euer Vertrauen.', F('fraunces-600.ttf', 66), (255, 255, 255), 920, 78, 'la')
    absatz(d, 80, y + 14, 'Jede Bestellung packen wir mit ganz viel Liebe ein.', F('nunitosans-600.ttf', 34), (248, 240, 236), 920, 44, 'la')
    d.text((W - 36, 40), 'Bild mit KI erstellt', font=F('nunitosans-600.ttf', 20), fill=(255, 255, 255), anchor='ra', stroke_width=2, stroke_fill=(90, 75, 70))
    return c.convert('RGB')


def slide3():
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 290), 'Von Herzen: Danke!', font=F('fraunces-600.ttf', 74), fill=ROSE, anchor='ms')
    y = absatz(d, W / 2, 350, 'Unser Set «Hello» in Rosa ist ausverkauft. Danke für jede Bestellung, jede liebe Nachricht '
               'und Euer Vertrauen in einen kleinen Shop wie unseren. Dass Eure Kleinsten ihre ersten Tage darin erleben, '
               'bedeutet uns unglaublich viel.', F('nunitosans-400.ttf', 38), WALD, 860, 54)
    # Bewertungskarte (echt, wörtlich)
    top = y + 60; karte = (90, top, W - 90, top + 400)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((karte[0], karte[1] + 14, karte[2], karte[3] + 14), 36, fill=(0, 0, 0, 38))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(16))); d = ImageDraw.Draw(c)
    d.rounded_rectangle(karte, 36, fill=(255, 255, 255))
    sterne(d, W / 2, top + 70)
    yy = absatz(d, W / 2, top + 120, '«Super schneller Versand, alles lief sehr gut. Gerne wieder. Merci»', F('fraunces-400.ttf', 44), WALD, 760, 58)
    d.text((W / 2, yy + 24), 'MariolyG  ·  Bewertung auf sunnozy.ch', font=F('nunitosans-600.ttf', 28), fill=GRAU, anchor='ma')
    L = logo(170, (122, 108, 104)); c.alpha_composite(L, ((W - L.width) // 2, H - 130))
    return c.convert('RGB')


def slide4():
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    s = set_bild(720); c.alpha_composite(s, ((W - s.width) // 2, 110))
    y = 110 + s.height + 70
    d.text((W / 2, y + 70), 'Restock in Arbeit', font=F('fraunces-600.ttf', 84), fill=ROSE, anchor='ms')
    y = absatz(d, W / 2, y + 115, 'Wir arbeiten bereits daran, dass «Hello» in Rosa bald wieder da ist. '
               'Speichere diesen Beitrag und folge uns, dann erfährst Du es zuerst.', F('nunitosans-400.ttf', 36), WALD, 840, 50)
    L = logo(170, (122, 108, 104)); c.alpha_composite(L, ((W - L.width) // 2, H - 130))
    return c.convert('RGB')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    alle = [slide1(), slide2(), slide3(), slide4()]
    for i, im in enumerate(alle, 1):
        im.save(os.path.join(OUT, f'slide_{i}_4x5.jpg'), quality=93)
    u = Image.new('RGB', (4 * 330 + 50, 412 + 20), 'white')
    for i, im in enumerate(alle):
        u.paste(im.resize((330, 412)), (10 + i * 340, 10))
    u.save(os.path.join(OUT, 'uebersicht.jpg'), quality=88)
    print(len(alle), 'Slides')
