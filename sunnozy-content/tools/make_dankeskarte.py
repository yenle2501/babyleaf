"""Dankeskarte fuer die Pakete (Kampagne «Wachsen mit sunnozy»), A6 hoch, druckfertig.

Format: A6 105 x 148 mm + 3 mm Beschnitt rundum = 111 x 154 mm, 300 dpi (1311 x 1819 px). Text bleibt mindestens
5 mm innerhalb des Endformats. Vorderseite: Dank + Platz fuer die Unterschrift. Rueckseite: Code fuer die naechste
Bestellung, Code zum Weitergeben, Bitte um ein Foto, Wasch-Tipp. Look nach dem sunnozy-Designsystem.

Aufruf: python3 make_dankeskarte.py <ausgabe-ordner> [CODE_WIEDER] [CODE_WEITERGEBEN]
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
CODE_WIEDER = sys.argv[2] if len(sys.argv) > 2 else 'DANKE10'
CODE_WEITER = sys.argv[3] if len(sys.argv) > 3 else 'HALLOBABY'
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
DPI = 300
MM = DPI / 25.4
W, H = round(111 * MM), round(154 * MM)
BLEED, SAFE = 3 * MM, 8 * MM                     # Text ab 3 mm Beschnitt + 5 mm Sicherheitsabstand
CREME, WALD, SALBEI, ROSE, GRAU, KACHEL = (253, 252, 250), (35, 48, 41), (122, 139, 111), (248, 234, 228), (98, 108, 102), (244, 239, 232)


def pt(p):                                       # Schriftgroesse in Punkt -> Pixel bei 300 dpi
    return p * DPI / 72


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def umbrechen(d, text, font, breite):
    zeilen, z = [], ''
    for w in text.split():
        t = (z + ' ' + w).strip()
        if d.textlength(t, font=font) <= breite:
            z = t
        else:
            zeilen.append(z); z = w
    zeilen.append(z)
    return zeilen


def absatz(d, x, y, text, font, fill, breite, zeilenabstand=1.45, mitte=False):
    for z in umbrechen(d, text, font, breite):
        d.text((x, y), z, font=font, fill=fill, anchor='mt' if mitte else 'lt')
        y += font.size * zeilenabstand
    return y


def sonne(d, cx, cy, r, col, w):
    """Kleine Sonne als Ornament (Bezug auf «kleine Sonnenscheine»)."""
    import math
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    for i in range(8):
        a = i * math.pi / 4
        d.line([(cx + math.cos(a) * r * 1.5, cy + math.sin(a) * r * 1.5), (cx + math.cos(a) * r * 2.0, cy + math.sin(a) * r * 2.0)], fill=col, width=w)


def vorderseite():
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    breite = W - 2 * SAFE - 2 * MM * 4
    lg = load_logo(int(W * 0.46)); c.paste(lg, ((W - lg.width) // 2, int(SAFE + 14 * MM)), lg)
    y = SAFE + 14 * MM + lg.height + 16 * MM
    sonne(d, W / 2, y, 2.2 * MM, SALBEI, 5); y += 12 * MM
    d.text((W / 2, y), 'Danke,', font=FONT('fraunces-600.ttf', pt(30)), fill=WALD, anchor='mt'); y += pt(30) * 1.15
    d.text((W / 2, y), 'dass Du dabei bist.', font=FONT('fraunces-600.ttf', pt(19)), fill=WALD, anchor='mt'); y += pt(19) * 2.0
    y = absatz(d, W / 2, y, 'Dein Paket haben wir mit viel Liebe in der Schweiz für Dich gepackt. Wir hoffen, Dein kleiner '
               'Sonnenschein fühlt sich darin rundum wohl.', FONT('nunitosans-400.ttf', pt(10.5)), GRAU, breite, mitte=True)
    y = H - SAFE - 30 * MM
    d.text((W / 2, y), 'Von Herzen', font=FONT('nunitosans-400i.ttf', pt(10.5)), fill=GRAU, anchor='mt')
    d.line([(W / 2 - 28 * MM, y + 17 * MM), (W / 2 + 28 * MM, y + 17 * MM)], fill=(205, 200, 192), width=3)   # Unterschrift
    return c


def code_box(d, x, y, breite, code):
    h = 13 * MM
    d.rounded_rectangle([x, y, x + breite, y + h], radius=2 * MM, outline=WALD, width=4, fill=CREME)
    fc = FONT('nunitosans-800.ttf', pt(15))
    sp = 0.9 * MM; tw = sum(d.textlength(ch, font=fc) for ch in code) + sp * (len(code) - 1); cx = x + (breite - tw) / 2
    for ch in code:
        d.text((cx, y + h / 2), ch, font=fc, fill=WALD, anchor='lm'); cx += d.textlength(ch, font=fc) + sp
    return y + h


def rueckseite():
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    x0 = SAFE + 2 * MM; breite = W - 2 * x0
    ft, fb, fs = FONT('fraunces-600.ttf', pt(13.5)), FONT('nunitosans-400.ttf', pt(9.5)), FONT('nunitosans-400.ttf', pt(8))
    y = SAFE + 4 * MM
    # 1 naechste Bestellung
    d.text((x0, y), 'Für Dein nächstes Lieblingsstück', font=ft, fill=WALD, anchor='lt'); y += pt(13.5) * 1.5
    y = absatz(d, x0, y, '10 % auf Deine nächste Bestellung auf sunnozy.ch mit dem Code:', fb, GRAU, breite)
    y = code_box(d, x0, y + 2 * MM, breite, CODE_WIEDER) + 9 * MM
    # 2 weitergeben (rosé Flaeche ueber die ganze Breite)
    box_top = y - 5 * MM
    yb = y
    d.text((x0, yb), 'Bald ein Baby im Freundeskreis?', font=ft, fill=WALD, anchor='lt'); yb += pt(13.5) * 1.5
    yb = absatz(d, x0, yb, 'Gib diesen Code weiter: 10 % auf die erste Bestellung für Deine Freundin.', fb, GRAU, breite)
    box_bottom = yb + 2 * MM + 13 * MM + 6 * MM
    rose = Image.new('RGB', (W, int(box_bottom - box_top)), ROSE)
    c.paste(rose, (0, int(box_top)))
    d = ImageDraw.Draw(c)
    yb = y
    d.text((x0, yb), 'Bald ein Baby im Freundeskreis?', font=ft, fill=WALD, anchor='lt'); yb += pt(13.5) * 1.5
    yb = absatz(d, x0, yb, 'Gib diesen Code weiter: 10 % auf die erste Bestellung für Deine Freundin.', fb, GRAU, breite)
    code_box(d, x0, yb + 2 * MM, breite, CODE_WEITER)
    y = box_bottom + 8 * MM
    # 3 Foto
    d.text((x0, y), 'Zeig uns Deinen kleinen Sonnenschein', font=ft, fill=WALD, anchor='lt'); y += pt(13.5) * 1.5
    y = absatz(d, x0, y, 'Markiere @sunnozy.ch auf Instagram oder schick uns ein Foto. Mit Deinem Einverständnis zeigen wir es '
               'in unserer Community.', fb, GRAU, breite)
    # Fuss
    fy = H - SAFE - 9 * MM
    d.line([(x0, fy - 6 * MM), (W - x0, fy - 6 * MM)], fill=(225, 219, 210), width=3)
    absatz(d, x0, fy - 3 * MM, 'Tipp: Neue Babykleidung vor dem ersten Tragen einmal waschen.', fs, GRAU, breite)
    d.text((W - x0, fy + 6 * MM), 'sunnozy.ch', font=FONT('nunitosans-700.ttf', pt(9)), fill=WALD, anchor='rm')
    return c


def schnittmarken(im):
    """Vorschau mit gestrichelter Endformat-Linie (nur zur Kontrolle, nicht drucken)."""
    v = im.copy(); d = ImageDraw.Draw(v)
    b = int(BLEED)
    for x in range(b, W - b, 24):
        d.line([(x, b), (x + 12, b)], fill=(200, 60, 60), width=2); d.line([(x, H - b), (x + 12, H - b)], fill=(200, 60, 60), width=2)
    for y in range(b, H - b, 24):
        d.line([(b, y), (b, y + 12)], fill=(200, 60, 60), width=2); d.line([(W - b, y), (W - b, y + 12)], fill=(200, 60, 60), width=2)
    return v


if __name__ == '__main__':
    v, r = vorderseite(), rueckseite()
    v.save(os.path.join(out, 'dankeskarte_A6_vorderseite.png'), dpi=(DPI, DPI))
    r.save(os.path.join(out, 'dankeskarte_A6_rueckseite.png'), dpi=(DPI, DPI))
    v.save(os.path.join(out, 'dankeskarte_A6_druck.pdf'), save_all=True, append_images=[r], resolution=DPI)
    p = Image.new('RGB', (W * 2 + 60, H), (230, 230, 230)); p.paste(schnittmarken(v), (0, 0)); p.paste(schnittmarken(r), (W + 60, 0))
    p.resize((p.width // 2, p.height // 2), Image.LANCZOS).save(os.path.join(out, 'dankeskarte_vorschau.jpg'), quality=90)
    print(W, H)
