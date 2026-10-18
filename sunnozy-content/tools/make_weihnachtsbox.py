"""Meta-/Pinterest-Anzeigen fuer die Kampagne «Weihnachts-Geschenkbox» (Schenkende: Gotti, Goetti, Grosseltern).

Vorbild: Pinterest-Pins «Weihnachten Geschenkbox Baby»: offene Geschenkbox mit Seidenpapier, Inhalt ordentlich
gefaltet und gerollt, Tannenzweige, Zapfen, Kugeln, Lichterkette, Geschenkanhaenger; oben eine kurze Headline,
unten Name und Inhalt der Box. Die Fotos sind mit Canva-KI aus dem Box-Foto der Nutzerin und den Shop-Bildern der
Kombi-Sets erzeugt (`posts/kampagne-weihnachtsbox/ki-roh/`).

Je Box: 4:5 (1080x1350, Feed), 1:1 (1080x1080, Karussell), 9:16 (1080x1920, Storys/Reels) und eine Uebersicht
aller Boxen (4:5 und 1:1). Preise erst eintragen, wenn sie feststehen (`PREIS`), sonst erscheint nur der Inhalt.

Aufruf: python3 make_weihnachtsbox.py <ki-roh-ordner> <ausgabe-ordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1:3]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
CREME, WALD, SALBEI, ROSE = (253, 250, 246), (35, 48, 41), (122, 139, 111), (184, 120, 128)

# (Datei, Name, Inhalt)
BOXEN = [('box_mum_dad_me', '«Mum Dad Me»', '5 Bodys + 5 Leggings'),
         ('box_lovely_little_girl', '«Lovely Little Girl»', '3 Bodys + 5 Leggings'),
         ('box_growing_up_strong', '«Growing up strong»', '5 Bodys + 5 Jogginghosen'),
         ('box_i_love_my_mummy', '«I love my Mummy»', '3 Bodys + 3 Halstücher')]
PREIS = {}          # z.B. {'box_mum_dad_me': '34.90'}, sobald die Boxpreise feststehen
LABEL, HEADLINE, ZEILE = 'WEIHNACHTS-GESCHENKBOX', 'Das schönste Hallo unterm Baum', 'Fürs Gottikind, Grosskind und alle Kleinen'


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def verlauf(c, y0, y1, oben=True, stark=238):
    """Creme-Verlauf ueber das Foto legen (oben: deckend -> transparent, unten umgekehrt)."""
    h = y1 - y0
    a = np.linspace(stark, 0, h) if oben else np.linspace(0, stark, h)
    a = np.clip(a * 1.15, 0, stark) if not oben else a
    m = Image.fromarray(np.repeat(a[:, None], c.width, 1).astype(np.uint8))
    c.paste(Image.new('RGB', (c.width, h), CREME), (0, y0), m)


def gesperrt(d, xy, text, font, fill, sp):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = xy[0] - w / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp


def knopf(d, mitte, y, text, k=1.0):
    f = FONT('nunitosans-800.ttf', 30 * k); w = d.textlength(text, font=f) + 70 * k; h = 66 * k
    d.rounded_rectangle([mitte - w / 2, y, mitte + w / 2, y + h], radius=h / 2, fill=WALD)
    d.text((mitte, y + h / 2 + 1), text, font=f, fill=CREME, anchor='mm')


def foto(name, W, H, oben=0):
    """Foto deckend auf W x H bringen (mittig), oben ab Zeile `oben` (in Originalpixeln) beginnen."""
    im = Image.open(os.path.join(src, name + '.jpg')).convert('RGB')
    s = max(W / im.width, H / (im.height - oben))
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = min(int(oben * s), im.height - H)
    return im.crop((x, y, x + W, y + H))


def kopf(c, d, W, y, gross=60):
    gesperrt(d, (W / 2, y), LABEL, FONT('nunitosans-800.ttf', 24), ROSE, 6)
    d.text((W / 2, y + 82), HEADLINE, font=FONT('fraunces-600.ttf', gross), fill=WALD, anchor='ms')
    d.text((W / 2, y + 128), ZEILE, font=FONT('nunitosans-600.ttf', 28), fill=SALBEI, anchor='ms')


def fuss(c, d, W, y, box, knopf_y=None):
    name, titel, inhalt = box
    d.text((W / 2, y), 'Geschenkbox ' + titel, font=FONT('fraunces-600.ttf', 46), fill=WALD, anchor='ms')
    zeile = inhalt + '  ·  fertig verpackt' + (f'  ·  CHF {PREIS[name]}' if name in PREIS else '')
    d.text((W / 2, y + 46), zeile, font=FONT('nunitosans-700.ttf', 28), fill=WALD, anchor='ms')
    if knopf_y:
        knopf(d, W / 2, knopf_y, 'Jetzt verschenken')


def feed(box, W=1080, H=1350):
    c = foto(box[0], W, H, oben=20); d = ImageDraw.Draw(c)
    verlauf(c, 0, 330); verlauf(c, H - 330, H, oben=False)
    d = ImageDraw.Draw(c)
    kopf(c, d, W, 62)
    fuss(c, d, W, H - 160, box, knopf_y=H - 96)
    return c


def quadrat(box, W=1080, H=1080):
    c = foto(box[0], W, H, oben=150); d = ImageDraw.Draw(c)
    verlauf(c, 0, 250, stark=232); verlauf(c, H - 220, H, oben=False)
    d = ImageDraw.Draw(c)
    gesperrt(d, (W / 2, 50), LABEL, FONT('nunitosans-800.ttf', 22), ROSE, 6)
    d.text((W / 2, 122), HEADLINE, font=FONT('fraunces-600.ttf', 54), fill=WALD, anchor='ms')
    fuss(c, d, W, H - 80, box)
    return c


def story(box, W=1080, H=1920):
    """9:16: oben 14 % und unten 20 % frei von wichtigem Inhalt (Instagram-Bedienelemente)."""
    c = Image.new('RGB', (W, H), CREME)
    f = foto(box[0], W, 1339)
    top = 330
    c.paste(f, (0, top))
    verlauf(c, top, top + 120, stark=255)
    verlauf(c, top + 1339 - 160, top + 1339, oben=False, stark=255)
    d = ImageDraw.Draw(c)
    d.rectangle([0, top + 1339, W, H], fill=CREME)
    kopf(c, d, W, 220, gross=62)
    fuss(c, d, W, 1640, box, knopf_y=1712)
    return c


def uebersicht(W, H):
    """Alle Boxen im Raster, Headline oben, Logo unten."""
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    oben = 170 if H > W else 140
    gesperrt(d, (W / 2, 58), LABEL + 'EN', FONT('nunitosans-800.ttf', 24), ROSE, 6)
    d.text((W / 2, 132 if H > W else 122), HEADLINE, font=FONT('fraunces-600.ttf', 58 if H > W else 52), fill=WALD, anchor='ms')
    unten = 150 if H > W else 70
    g = 16; kw = (W - 3 * g) // 2; kh = (H - oben - unten - g) // 2
    f = FONT('nunitosans-800.ttf', 24)
    for i, box in enumerate(BOXEN):
        x, y = g + (i % 2) * (kw + g), oben + (i // 2) * (kh + g)
        im = Image.open(os.path.join(src, box[0] + '.jpg')).convert('RGB')
        s = max(kw / im.width, kh / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        ox = (im.width - kw) // 2; oy = int((im.height - kh) * 0.45)
        c.paste(im.crop((ox, oy, ox + kw, oy + kh)), (x, y))
        t = box[1]; w = d.textlength(t, font=f) + 36
        d.rounded_rectangle([x + 14, y + kh - 58, x + 14 + w, y + kh - 14], radius=22, fill=CREME)
        d.text((x + 32, y + kh - 36), t, font=f, fill=WALD, anchor='lm')
    if H > W:
        knopf(d, W / 2, H - 120, 'Jetzt verschenken')
    else:
        lg = load_logo(150); c.paste(lg, ((W - lg.width) // 2, H - 52), lg)
    return c


if __name__ == '__main__':
    for fmt in ('4x5', '1x1', '9x16'):
        os.makedirs(os.path.join(out, fmt), exist_ok=True)
    for box in BOXEN:
        n = box[0]
        feed(box).save(os.path.join(out, '4x5', f'{n}_4x5.jpg'), quality=94)
        quadrat(box).save(os.path.join(out, '1x1', f'{n}_1x1.jpg'), quality=94)
        story(box).save(os.path.join(out, '9x16', f'{n}_9x16.jpg'), quality=94)
        print(n)
    uebersicht(1080, 1350).save(os.path.join(out, '4x5', 'alle_boxen_4x5.jpg'), quality=94)
    uebersicht(1080, 1080).save(os.path.join(out, '1x1', 'alle_boxen_1x1.jpg'), quality=94)
