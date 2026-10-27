"""Instagram-Karussell (4:5) «Sold Out» für das Erstausstattung-Set «Hello» in Rosa, 27.10.2026.
Zweite Version (Wunsch der Nutzerin: eleganter, Bild vom Set im Hintergrund): alle drei Bilder auf dem
KI-Foto des Sets auf cremefarbener Seide, Schrift Fraunces 400 und Nunito Sans (keine Schreibschrift).

    python3 tools/make_post_hello_ausverkauft.py

1  Sold Out: Set-Foto, Titel oben auf der leeren Seide
2  Danke: Set-Foto weichgezeichnet, helle Karte mit Danke-Text und echter Bewertung (MariolyG, wörtlich)
3  Restock in Arbeit: Ausschnitt des Sets, Text unten (ohne Datum)
Ausgabe: posts/instagram/hello-ausverkauft/slide_<n>_4x5.jpg + uebersicht.jpg
"""
import os, math, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'posts', 'instagram', 'hello-ausverkauft')
FOTO = os.path.join(OUT, 'bilder', 'set_seide_ki.jpg')
W, H = 1080, 1350
TIEF, ROSE, TAUPE, STERN = (92, 60, 62), (138, 86, 92), (124, 108, 102), (196, 158, 104)
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))


def logo(width, col):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def gesperrt(d, cx, y, text, font, farbe, sp):
    """Text mit Buchstabenabstand, mittig."""
    breite = sum(d.textlength(c, font=font) for c in text) + sp * (len(text) - 1)
    x = cx - breite / 2
    for c in text:
        d.text((x, y), c, font=font, fill=farbe, anchor='ls'); x += d.textlength(c, font=font) + sp


def umbrechen(d, text, font, breite):
    zeilen, z = [], ''
    for wort in text.split():
        t = (z + ' ' + wort).strip()
        if d.textlength(t, font=font) <= breite:
            z = t
        else:
            zeilen.append(z); z = wort
    return zeilen + [z]


def absatz(d, x, y, text, font, farbe, breite, zh):
    for z in umbrechen(d, text, font, breite):
        d.text((x, y), z, font=font, fill=farbe, anchor='ma'); y += zh
    return y


def sterne(d, cx, y, r=15, abstand=40):
    for i in range(5):
        x0 = cx + (i - 2) * abstand
        pts = [(x0 + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5), y - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
        d.polygon(pts, fill=STERN)


def linie(d, cx, y, halb, farbe):
    d.line((cx - halb, y, cx + halb, y), fill=farbe, width=2)


def basis(versatz=0):
    """Set-Foto auf 4:5; mit versatz>0 nach unten geschoben, oben mit gespiegelter, weicher Seide ergänzt."""
    im = Image.open(FOTO).convert('RGB')
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    c = Image.new('RGB', (W, H))
    c.paste(im.crop((0, 0, W, H - versatz)), (0, versatz))
    if versatz:
        oben = im.crop((0, 0, W, versatz + 60)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(6))
        maske = Image.linear_gradient('L').resize((W, versatz + 60)).point(lambda v: 255 if v < 200 else int((255 - v) * 255 / 55))
        c.paste(oben, (0, 0), maske)
    return c


def schleier(c, y0, y1, farbe=(250, 245, 240), staerke=0.75, unten=False):
    """Cremefarbener Verlauf hinter dem Text, für ruhige Lesbarkeit."""
    g = np.zeros((H, 1), np.float32)
    n = y1 - y0
    werte = np.clip(np.linspace(1, 0, n), 0, 1) ** 1.4 * staerke if not unten else np.clip(np.linspace(0, 1, n), 0, 1) ** 1.4 * staerke
    g[y0:y1, 0] = werte
    if not unten:
        g[:y0, 0] = staerke
    else:
        g[y1:, 0] = staerke
    lay = Image.new('RGBA', (W, H), farbe + (0,)); lay.putalpha(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H)))
    return Image.alpha_composite(c.convert('RGBA'), lay)


def slide1():
    c = schleier(basis(170), 330, 560, staerke=0.55); d = ImageDraw.Draw(c)
    gesperrt(d, W / 2, 128, 'ERSTAUSSTATTUNG «HELLO»  ·  ROSA', F('nunitosans-600.ttf', 23), TAUPE, 5)
    d.text((W / 2, 300), 'Sold Out', font=F('fraunces-400.ttf', 158), fill=TIEF, anchor='ms')
    linie(d, W / 2, 352, 46, ROSE)
    d.text((W / 2, 412), 'Danke für Euer Vertrauen', font=F('fraunces-400.ttf', 40), fill=ROSE, anchor='ms')
    return c.convert('RGB')


def slide2():
    b = basis(0).filter(ImageFilter.GaussianBlur(16))
    c = Image.blend(b, Image.new('RGB', (W, H), (250, 245, 240)), 0.35).convert('RGBA')
    karte = (110, 170, W - 110, H - 170)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((karte[0], karte[1] + 16, karte[2], karte[3] + 16), fill=(60, 40, 40, 40))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(22)))
    k = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(k).rectangle(karte, fill=(252, 249, 246, 238))
    c = Image.alpha_composite(c, k); d = ImageDraw.Draw(c)
    d.rectangle((karte[0] + 18, karte[1] + 18, karte[2] - 18, karte[3] - 18), outline=(214, 190, 186), width=1)
    cx = W / 2
    gesperrt(d, cx, 300, 'VON HERZEN', F('nunitosans-600.ttf', 22), TAUPE, 6)
    d.text((cx, 395), 'Danke.', font=F('fraunces-400.ttf', 96), fill=TIEF, anchor='ms')
    linie(d, cx, 440, 40, ROSE)
    y = absatz(d, cx, 482, 'Unser Set «Hello» in Rosa ist ausverkauft. Danke für jede Bestellung, jede liebe Nachricht '
               'und Euer Vertrauen in einen kleinen Shop wie unseren.', F('nunitosans-400.ttf', 33), (78, 70, 68), 700, 48)
    sterne(d, cx, y + 70)
    y = absatz(d, cx, y + 112, '«Super schneller Versand, alles lief sehr gut. Gerne wieder. Merci»', F('fraunces-400.ttf', 38), TIEF, 690, 52)
    d.text((cx, y + 18), 'MariolyG, Bewertung auf sunnozy.ch', font=F('nunitosans-600.ttf', 24), fill=TAUPE, anchor='ma')
    L = logo(150, (150, 128, 122)); c.alpha_composite(L, (int(cx - L.width / 2), karte[3] - 110))
    return c.convert('RGB')


def slide3():
    im = Image.open(FOTO).convert('RGB')
    # Ausschnitt: Body mit Spitzenkragen und Häubchen
    x0, y0 = int(im.width * 0.40), int(im.height * 0.20); bw = int(im.width * 0.58); bh = int(bw * H / W)
    c = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + bw, y0 + bh))
    c = schleier(c, 760, 1030, staerke=0.88, unten=True); d = ImageDraw.Draw(c)
    gesperrt(d, W / 2, 1080, 'BALD WIEDER DA', F('nunitosans-600.ttf', 22), TAUPE, 6)
    d.text((W / 2, 1160), 'Restock in Arbeit', font=F('fraunces-400.ttf', 76), fill=TIEF, anchor='ms')
    absatz(d, W / 2, 1192, 'Speichere diesen Beitrag und folge uns, dann erfährst Du es zuerst.', F('nunitosans-400.ttf', 28), (78, 70, 68), 960, 40)
    L = logo(120, (150, 128, 122)); c.alpha_composite(L, (int(W / 2 - L.width / 2), 1268))
    return c.convert('RGB')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for alt in glob.glob(os.path.join(OUT, 'slide_*_4x5.jpg')):
        os.remove(alt)
    alle = [slide1(), slide2(), slide3()]
    for i, im in enumerate(alle, 1):
        im.save(os.path.join(OUT, f'slide_{i}_4x5.jpg'), quality=93)
    u = Image.new('RGB', (len(alle) * 340 + 10, 432), 'white')
    for i, im in enumerate(alle):
        u.paste(im.resize((330, 412)), (10 + i * 340, 10))
    u.save(os.path.join(OUT, 'uebersicht.jpg'), quality=88)
    print(len(alle), 'Slides')
