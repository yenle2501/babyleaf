"""Meta-Anzeigenbilder in 1:1, 4:5 und 9:16 fuer zwei Test-Motive (Werbeplan, Kampagne «Alles drin»).

Motiv «Checkliste» (werdende Eltern): «Erstausstattung? Erledigt.» - das Set als Bild, darunter jedes Teil mit Haken.
Motiv «Geschenk» (Schenkende): «Das schönste Hallo» auf Rosé, Set, Teile, Preis, Lieferzeit.
Nur echte Produktbilder (Shop-Hauptbilder), Preise und Teile aus Shopify, Look nach dem sunnozy-Designsystem.
Update 18.10.2026: Grundlage sind die neuen Hauptbilder im ChatGPT-Stil (warmer Studio-Grund, Holzbuegel). Sie sitzen
als Fotokachel mit runden Ecken und weichem Schatten auf Creme bzw. Rosé, deutlich groesser als vorher; das
eingebrannte Logo wird mit dem Studio-Grund uebermalt.
In Storys bleiben oben 14 % und unten 20 % frei von wichtigem Inhalt (Instagram-Bedienelemente).

Aufruf: python3 make_meta_fotos.py <ausgabe-ordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILDER = os.path.join(ROOT, 'posts', 'shopify-hauptbilder-praesentation-hd', 'bilder')
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
CREME, WALD, SALBEI, GRAU, ROSE = (253, 252, 250), (35, 48, 41), (122, 139, 111), (98, 108, 102), (248, 234, 228)

# Sets mit genug Lager (Stand 17.10.2026); «Hello» und «Hello Little Bear» erst nach dem Nachbestellen
SETS = [('teddybaer', '«Teddybär»', '30.40', 'erstausstattung-set-teddybaer',
         ['Strampler', 'Body', 'Decke', 'Mütze', 'Lätzchen', 'Fäustlinge', 'Söckchen', 'Rassel & Beissring']),
        ('princess', '«Princess»', '30.40', 'erstausstattung-set-princess',
         ['Strampler', 'Body', 'Decke', 'Mütze', 'Lätzchen', 'Fäustlinge', 'Söckchen', 'Rassel']),
        ('little_and_loved', '«Little and Loved»', '30.40', 'erstausstattung-set-little-and-loved',
         ['Strampler', 'Body', 'T-Shirt', 'Jäckchen', 'Hose', 'Mütze', 'Lätzchen', 'Fäustlinge']),
        ('hello_world', '«Hello World»', '29.40', 'erstausstattung-set-hello-world',
         ['Strampler', 'Body', 'T-Shirt', 'Jäckchen', 'Hose', 'Mütze', 'Lätzchen', 'Fäustlinge'])]

FORMATE = {'1x1': (1080, 1080), '4x5': (1080, 1350), '9x16': (1080, 1920)}


def produkt(handle):
    """Shop-Hauptbild ohne Logo. Das Logo liegt bei allen Bildern bei x 72-478, y 63-148 (von 2048 px,
    `hauptbild_logo.py`); die Flaeche wird zwischen dem Grund darueber und darunter verlaufend aufgefuellt."""
    im = Image.open(os.path.join(BILDER, handle + '.jpg')).convert('RGB')
    a = np.asarray(im).astype(float); s = im.width / 2048
    x0, x1, y0, y1 = int(56 * s), int(496 * s), int(50 * s), int(164 * s)
    k = np.ones(41) / 41
    glatt = lambda z: np.stack([np.convolve(np.pad(z[:, c], 20, mode='edge'), k, 'valid') for c in range(3)], 1)
    oben, unten = glatt(a[y0 - 10:y0, x0:x1].mean(0)), glatt(a[y1:y1 + 10, x0:x1].mean(0))
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = oben[None] * (1 - t) + unten[None] * t
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def setzen(c, im, box, r=26):
    """Hauptbild als quadratische Fotokachel mit runden Ecken und weichem Schatten mittig in die Box setzen."""
    x, y, w, h = box
    n = int(min(w, h))
    t = im.resize((n, n), Image.LANCZOS)
    px, py = int(x + (w - n) / 2), int(y + (h - n) / 2)
    sh = Image.new('L', c.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([px, py + 10, px + n, py + n + 10], radius=r, fill=60)
    c.paste(Image.new('RGB', c.size, WALD), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    m = Image.new('L', (n, n), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, n - 1, n - 1], radius=r, fill=255)
    c.paste(t, (px, py), m)


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def gesperrt(d, xy, text, font, fill, sp):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = xy[0] - w / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp


def haken(d, x, y, r, col):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    w = max(3, int(r / 4))
    d.line([(x - r * 0.45, y + r * 0.02), (x - r * 0.1, y + r * 0.38), (x + r * 0.5, y - r * 0.35)], fill=CREME, width=w, joint='curve')


def checkliste(d, teile, x0, y0, spalten, breite, zeile, gross):
    f = FONT('nunitosans-600.ttf', gross)
    pro = (len(teile) + spalten - 1) // spalten
    for i, t in enumerate(teile):
        sp, r = divmod(i, pro)
        x = x0 + sp * breite; y = y0 + r * zeile
        haken(d, x + gross * 0.45, y, gross * 0.45, SALBEI)
        d.text((x + gross * 1.25, y), t, font=f, fill=WALD, anchor='lm')


def motiv_checkliste(s, fmt):
    name, titel, preis, handle, teile = s
    W, H = FORMATE[fmt]
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    im = produkt(handle)
    ft = FONT('fraunces-600.ttf', 88)
    if fmt == '1x1':
        d.text((60, 120), 'Erstausstattung?', font=ft, fill=WALD, anchor='ls')
        d.text((60, 215), 'Erledigt.', font=ft, fill=SALBEI, anchor='ls')
        setzen(c, im, (50, 252, 600, 612))
        d = ImageDraw.Draw(c)
        checkliste(d, teile, 680, 330, 1, 0, 70, 34)
        y = 945
    elif fmt == '4x5':
        d.text((W / 2, 150), 'Erstausstattung?', font=ft, fill=WALD, anchor='ms')
        d.text((W / 2, 250), 'Erledigt.', font=ft, fill=SALBEI, anchor='ms')
        setzen(c, im, (0, 290, W, 670))
        d = ImageDraw.Draw(c)
        checkliste(d, teile, 150, 1012, 2, 430, 54, 32)
        y = 1250
    else:
        d.text((W / 2, 400), 'Erstausstattung?', font=FONT('fraunces-600.ttf', 96), fill=WALD, anchor='ms')
        d.text((W / 2, 510), 'Erledigt.', font=FONT('fraunces-600.ttf', 96), fill=SALBEI, anchor='ms')
        setzen(c, im, (0, 560, W, 740))
        d = ImageDraw.Draw(c)
        checkliste(d, teile, 150, 1356, 2, 430, 52, 31)
        y = 1580
    zeile = f'{len(teile)} Teile  ·  CHF {preis}  ·  Gratisversand ab CHF 50'
    if fmt == '1x1':          # links buendig, rechts sitzt das Logo
        d.text((60, y), 'ERSTAUSSTATTUNG ' + titel.upper(), font=FONT('nunitosans-700.ttf', 24), fill=SALBEI, anchor='lm')
        d.text((60, y + 52), zeile, font=FONT('nunitosans-700.ttf', 30), fill=WALD, anchor='lm')
    else:
        gesperrt(d, (W / 2, y), 'ERSTAUSSTATTUNG ' + titel.upper(), FONT('nunitosans-700.ttf', 24), SALBEI, 3)
        d.text((W / 2, y + 52), zeile, font=FONT('nunitosans-700.ttf', 30), fill=WALD, anchor='mm')
    if fmt == '1x1':
        lg = load_logo(190); c.paste(lg, (W - 60 - lg.width, int(y - 10 - lg.height / 2)), lg)
    return c


def motiv_geschenk(s, fmt):
    name, titel, preis, handle, teile = s
    W, H = FORMATE[fmt]
    c = Image.new('RGB', (W, H), ROSE); d = ImageDraw.Draw(c)
    im = produkt(handle)
    oben = {'1x1': 70, '4x5': 110, '9x16': 300}[fmt]
    gesperrt(d, (W / 2, oben), 'GESCHENK ZUR GEBURT', FONT('nunitosans-700.ttf', 26), SALBEI, 5)
    gr = 92 if fmt != '1x1' else 84
    d.text((W / 2, oben + 110), 'Das schönste Hallo', font=FONT('fraunces-600.ttf', gr), fill=WALD, anchor='ms')
    bild_h = {'1x1': 640, '4x5': 760, '9x16': 860}[fmt]
    setzen(c, im, (70, oben + 150, W - 140, bild_h))
    d = ImageDraw.Draw(c)
    y = oben + 150 + bild_h + 45
    d.text((W / 2, y), 'Erstausstattung ' + titel, font=FONT('fraunces-600.ttf', 48), fill=WALD, anchor='mm')
    d.text((W / 2, y + 62), f'{len(teile)} Teile  ·  CHF {preis}  ·  in 2–3 Werktagen bei Dir', font=FONT('nunitosans-600.ttf', 30), fill=GRAU, anchor='mm')
    if fmt != '1x1':
        lg = load_logo(230); c.paste(lg, ((W - lg.width) // 2, int(y + 115)), lg)
    return c


if __name__ == '__main__':
    for fmt in FORMATE:
        os.makedirs(os.path.join(out, fmt), exist_ok=True)
    for s in SETS:
        for fmt in FORMATE:
            motiv_checkliste(s, fmt).save(os.path.join(out, fmt, f'checkliste_{s[0]}_{fmt}.jpg'), quality=94)
            motiv_geschenk(s, fmt).save(os.path.join(out, fmt, f'geschenk_{s[0]}_{fmt}.jpg'), quality=94)
        print(s[0])
