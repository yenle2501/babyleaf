"""Shopify-Bilder für die Weihnachts-Geschenkbox «Growing up strong» aus den echten Handyfotos der Nutzerin (31.10.2026).

    python3 tools/make_geschenkbox_weihnachten_fotos.py

Echte Box (Teddy-Weihnachtsdruck, rotes sunnozy-Satinband, Karte «Merry Christmas», Seidenpapier mit Blumen,
Sticker «Frohe Weihnachten»), Inhalt 5 gerippte Bodys + 5 Ripp-Hosen. Der unruhige Schreibtisch-Hintergrund wurde in
Canva entfernt (Freisteller in posts/.../geschenkbox-weihnachten/freigestellt/), die Box selbst ist unverändert.
Nur Bild 5 (Weihnachtszimmer) hat einen KI-Hintergrund, die Box darauf ist das echte Foto.

Ausgabe (2000 × 2000, JPG): posts/produktfotos-geschenkbox-weihnachten/growing-up-strong/
  01_hauptbild.jpg            Box zu, von oben, heller Hintergrund, mit Logo (02_hauptbild_ohne_logo.jpg ohne)
  03_box_offen.jpg            Deckel ab, Seidenpapier offen, alle 10 Teile sichtbar
  04_box_schraeg.jpg          Box zu, schräg
  05_unterm_baum.jpg          Box zu, schräg, im Weihnachtszimmer (Hintergrund KI)
  06_inhalt.jpg               Blick in die Box: 5 Bodys, 5 Hosen
  07_seidenpapier.jpg         Seidenpapier mit Sticker «Frohe Weihnachten»
  08_das_ist_drin.jpg         Übersicht mit Text: was in der Box ist
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = os.path.join(ROOT, 'posts', 'produktfotos-geschenkbox-weihnachten', 'quelle')
OUT = os.path.join(ROOT, 'posts', 'produktfotos-geschenkbox-weihnachten', 'growing-up-strong')
S = 2000
HG = (246, 242, 237)
WALD, GRAU, ROT = (35, 48, 41), (112, 118, 114), (150, 32, 36)
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))


def auffrischen(im):
    """Handyfoto bei Kunstlicht: etwas heller, klarer, minimal wärmer."""
    rgb = im.convert('RGB')
    rgb = ImageEnhance.Brightness(rgb).enhance(1.07)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    rgb = ImageEnhance.Color(rgb).enhance(1.05)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    if im.mode == 'RGBA':
        rgb.putalpha(im.getchannel('A'))
    return rgb


def freisteller(name):
    im = Image.open(os.path.join(QUELLE, 'freigestellt', name)).convert('RGBA')
    return auffrischen(im.crop(im.getchannel('A').getbbox()))


def hintergrund():
    """Heller, warmer Studiohintergrund mit leichtem Verlauf."""
    y = np.linspace(0, 1, S)[:, None]
    oben, unten = np.array([250, 247, 243]), np.array(HG) - 6
    a = (oben * (1 - y) + unten * y)[:, None, :].repeat(S, axis=1)
    return Image.fromarray(a.astype(np.uint8)).convert('RGBA')


def platzieren(c, obj, hoehe_max, breite_max, cy=0.52, schatten=0.35):
    s = min(hoehe_max / obj.height, breite_max / obj.width)
    o = obj.resize((round(obj.width * s), round(obj.height * s)), Image.LANCZOS)
    x = (S - o.width) // 2; y = int(S * cy - o.height / 2)
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0))
    maske = o.getchannel('A').point(lambda v: int(v * schatten))
    schw = Image.new('RGBA', o.size, (40, 28, 22, 255)); schw.putalpha(maske)
    sh.alpha_composite(schw, (x + 18, y + 34))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(28)))
    c.alpha_composite(o, (x, y))
    return c


def logo(width, col):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def auf_quadrat(im, rand=0.05):
    """Foto ohne Freistellen auf ein Quadrat mit Rand in Hintergrundfarbe."""
    c = hintergrund(); m = int(S * rand)
    s = min((S - 2 * m) / im.width, (S - 2 * m) / im.height)
    t = auffrischen(im).resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(t, ((S - t.width) // 2, (S - t.height) // 2))
    return c


def speichern(c, name):
    c.convert('RGB').save(os.path.join(OUT, name), quality=93)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    oben, offen, schraeg = freisteller('box_zu_oben.png'), freisteller('box_offen.png'), freisteller('box_zu_schraeg.png')

    c = platzieren(hintergrund(), oben, 1780, 1500, cy=0.51)
    speichern(c, '02_hauptbild_ohne_logo.jpg')
    L = logo(300, (122, 108, 104)); c.alpha_composite(L, (70, 60)); speichern(c, '01_hauptbild.jpg')

    speichern(platzieren(hintergrund(), offen, 1550, 1860, cy=0.5, schatten=0.25), '03_box_offen.jpg')
    speichern(platzieren(hintergrund(), schraeg, 1500, 1800, cy=0.52), '04_box_schraeg.jpg')

    raum = Image.open(os.path.join(QUELLE, 'hintergrund_weihnachtszimmer_ki.jpg')).convert('RGBA').resize((S, S), Image.LANCZOS)
    warm = schraeg.copy(); r, g, b, a = warm.split()
    warm = Image.merge('RGBA', (r.point(lambda v: min(255, int(v * 1.03))), g.point(lambda v: int(v * 0.97)), b.point(lambda v: int(v * 0.86)), a))
    warm = ImageEnhance.Brightness(warm).enhance(0.9)          # an das warme Kerzenlicht angleichen
    c = platzieren(raum, warm, 1050, 1300, cy=0.68, schatten=0.55)
    ImageDraw.Draw(c).text((S - 40, S - 40), 'Hintergrund mit KI erstellt', font=F('nunitosans-600.ttf', 30),
                           fill=(255, 255, 255, 200), anchor='rs', stroke_width=2, stroke_fill=(60, 40, 30, 160))
    speichern(c, '05_unterm_baum.jpg')

    inhalt = Image.open(os.path.join(QUELLE, 'foto7.jpg')).crop((0, 180, 1300, 1990))
    inhalt = ImageEnhance.Brightness(inhalt).enhance(1.08)
    speichern(auf_quadrat(inhalt, 0.04), '06_inhalt.jpg')
    papier = Image.open(os.path.join(QUELLE, 'foto6.jpg')).crop((140, 700, 1390, 1950))
    speichern(auffrischen(papier).resize((S, S), Image.LANCZOS).convert('RGBA'), '07_seidenpapier.jpg')

    # Übersicht «Das ist drin»
    c = hintergrund(); d = ImageDraw.Draw(c)
    d.text((S / 2, 170), 'Das ist drin', font=F('fraunces-600.ttf', 110), fill=WALD, anchor='ms')
    d.text((S / 2, 245), 'Weihnachts-Geschenkbox «Growing up strong»', font=F('nunitosans-600.ttf', 44), fill=GRAU, anchor='ms')
    c = platzieren(c, offen, 860, 1300, cy=0.415, schatten=0.22); d = ImageDraw.Draw(c)
    punkte = ['5 gerippte Kurzarm-Bodys', '5 passende Ripp-Hosen mit Bindeband', 'Seidenpapier mit sunnozy-Sticker',
              'Rotes sunnozy-Satinband und Karte «Merry Christmas»']
    fp = F('nunitosans-600.ttf', 46)
    x0 = (S - max(d.textlength(p, font=fp) for p in punkte) - 60) / 2
    y = 1330
    for p in punkte:
        d.ellipse((x0, y - 26, x0 + 20, y - 6), fill=ROT)
        d.text((x0 + 50, y), p, font=fp, fill=WALD, anchor='ls'); y += 84
    d.text((S / 2, y + 60), '100 % Baumwolle  ·  0–3, 3–6 oder 6–9 Monate', font=F('nunitosans-400.ttf', 42), fill=GRAU, anchor='ms')
    L = logo(240, (122, 108, 104)); c.alpha_composite(L, ((S - L.width) // 2, S - 150))
    speichern(c, '08_das_ist_drin.jpg')

    bilder = sorted(f for f in os.listdir(OUT) if f.endswith('.jpg') and f[0].isdigit())
    u = Image.new('RGB', (4 * 410 + 10, 2 * 410 + 10), 'white')
    for i, f in enumerate(bilder[:8]):
        u.paste(Image.open(os.path.join(OUT, f)).resize((400, 400)), (10 + (i % 4) * 410, 10 + (i // 4) * 410))
    u.save(os.path.join(OUT, 'uebersicht.jpg'), quality=88)
    print(len(bilder), 'Bilder')
