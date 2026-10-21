"""Meta-Anzeigen (Facebook/Instagram) fuer die Erstausstattungs-Sets im Stil der Next-Karussell-Anzeige.

Analyse Vorbild (Next, Karussell-Karte 1:1): links gross das Produkt am Holzbuegel auf ruhigem Grund, oben links ein
schwarzes Preis-Etikett mit abgerundeten Ecken («CHF13»), rechts ein schmales hellgraues Feld mit der Wortmarke
senkrecht (von oben nach unten lesbar, sehr gross), darunter in fetten Grossbuchstaben das Versandversprechen und
klein grau der Hinweis. Kein weiterer Text im Bild - Produktname und «Shop now» liefert Meta unter der Karte.

sunnozy-Version (Update 18.10.2026): die neuen Shop-Hauptbilder im ChatGPT-Stil (warmer Studio-Grund, Holzbuegel,
2048 px, `posts/shopify-hauptbilder-praesentation-hd/bilder`). Das eingebrannte Logo oben links wird mit dem
Studio-Grund uebermalt, dort sitzt jetzt das Preis-Etikett. Das Bild laeuft randlos, die Leinwand bekommt die Farbe
des Studio-Grunds, die Kanten werden weich eingeblendet. Preis aus Shopify, sunnozy-Logo, «GRATISVERSAND AB CHF 50»
(Versandregel Schweiz in Shopify) und «Versand in 2–3 Werktagen».
Ausgabe je Set: Karussell-Karte 1:1 (1080x1080) und 4:5 (1080x1350), Story/Reels 9:16 (1080x1920).

Aufruf: python3 make_meta_ads.py <quell-ordner> <ausgabe-ordner> [--4x5]
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
PANEL, INK, GRAU = (226, 222, 216), (17, 17, 17), (110, 106, 101)

# (Bild = Shopify-Handle, Dateiname, Preis aus Shopify)
SETS = [('erstausstattung-set-teddybaer', 'teddybaer', '30.40'),
        ('erstausstattung-set-princess', 'princess', '30.40'),
        ('erstausstattung-set-little-and-loved', 'little_and_loved', '30.40'),
        ('erstausstattung-set-hello-world', 'hello_world', '29.40'),
        ('erstausstattung-set-hello-spitze', 'hello_rosa', '30.40'),
        ('erstausstattung-set-hello-little-bear', 'hello_little_bear', '28.40')]


def load_logo(height_or_width, col=INK):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((height_or_width, round(L.height * height_or_width / L.width)), Image.LANCZOS)


def hauptbild(handle):
    """Shop-Hauptbild ohne Logo. Das Logo liegt bei allen sechs Bildern bei x 72-478, y 63-148 (von 2048 px,
    `hauptbild_logo.py`); die Flaeche wird zwischen dem Grund darueber und darunter verlaufend aufgefuellt."""
    im = Image.open(os.path.join(src, handle + '.jpg')).convert('RGB')
    a = np.asarray(im).astype(float); s = im.width / 2048
    x0, x1, y0, y1 = int(56 * s), int(496 * s), int(50 * s), int(164 * s)
    k = np.ones(41) / 41
    glatt = lambda z: np.stack([np.convolve(np.pad(z[:, c], 20, mode='edge'), k, 'valid') for c in range(3)], 1)
    oben, unten = glatt(a[y0 - 10:y0, x0:x1].mean(0)), glatt(a[y1:y1 + 10, x0:x1].mean(0))
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = oben[None] * (1 - t) + unten[None] * t
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def grund(im):
    """Farbe des Studio-Grunds (Median des Bildrands)."""
    a = np.asarray(im)
    rand = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(rand, axis=0))


def einblenden(c, im, xy, size, f=48):
    """Bild quadratisch einsetzen, Kanten weich in die Leinwand (gleiche Grundfarbe) auslaufen lassen."""
    t = im.resize((size, size), Image.LANCZOS)
    m = Image.new('L', (size, size), 0)
    ImageDraw.Draw(m).rectangle([f, f, size - f, size - f], fill=255)
    c.paste(t, xy, m.filter(ImageFilter.GaussianBlur(f / 2)))


def badge(c, xy, preis, k=1.0):
    d = ImageDraw.Draw(c); f = ImageFont.truetype(INTER.format('SemiBold'), int(44 * k))
    t = f'CHF {preis}'; w = d.textlength(t, font=f)
    x, y = xy; h = 76 * k; pw = 26 * k
    d.rounded_rectangle([x, y, x + w + 2 * pw, y + h], radius=14 * k, fill=INK)
    d.text((x + pw, y + h / 2 + 2 * k), t, font=f, fill='white', anchor='lm')


def panel(c, x0, x1, y0, y1, k=1.0):
    """Rechtes Feld: Logo senkrecht, Versandversprechen, Hinweis."""
    d = ImageDraw.Draw(c); d.rectangle([x0, y0, x1, y1], fill=PANEL)
    pw = x1 - x0
    lg = load_logo(int((y1 - y0) * 0.5)).rotate(-90, expand=True)     # von oben nach unten lesbar
    if lg.width > pw * 0.62:
        s = pw * 0.62 / lg.width; lg = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS)
    ly = y0 + int((y1 - y0) * 0.07)
    c.paste(lg, (int(x0 + (pw - lg.width) / 2), ly), lg)
    fb = ImageFont.truetype(INTER.format('Bold'), int(33 * k)); fs = ImageFont.truetype(INTER.format('Regular'), int(23 * k))
    ty = ly + lg.height + (y1 - y0) * 0.07
    for z in ('GRATISVERSAND', 'AB CHF 50'):
        d.text((x0 + pw / 2, ty), z, font=fb, fill=INK, anchor='mt'); ty += 40 * k
    d.text((x0 + pw / 2, y1 - (y1 - y0) * 0.08), 'Versand in 2–3 Werktagen', font=fs, fill=GRAU, anchor='mm')


def band(c, y0, W, H, logo_w=380):
    """Feld unten (4:5, 9:16): Logo, Versandversprechen, Hinweis, zentriert."""
    d = ImageDraw.Draw(c); d.rectangle([0, y0, W, H], fill=PANEL)
    lg = load_logo(logo_w); c.paste(lg, ((W - lg.width) // 2, y0 + 44), lg)
    ty = y0 + 44 + lg.height + 36
    d.text((W / 2, ty), 'GRATISVERSAND AB CHF 50', font=ImageFont.truetype(INTER.format('Bold'), 40), fill=INK, anchor='mt')
    d.text((W / 2, ty + 58), 'Versand in 2–3 Werktagen', font=ImageFont.truetype(INTER.format('Regular'), 27), fill=GRAU, anchor='mt')


def karte(handle, preis, W=1080, H=1080):
    im = hauptbild(handle)
    c = Image.new('RGB', (W, H), grund(im))
    split = int(W * 0.70)
    einblenden(c, im, (0, (H - split) // 2), split)
    panel(c, split, W, 0, H)
    badge(c, (34, 30), preis)
    return c


def karte_4x5(handle, preis, W=1080, H=1350):
    """4:5 fuer den Feed: Set randlos quadratisch oben, Preis auf dem frei gewordenen Logo-Platz, Feld unten."""
    im = hauptbild(handle)
    c = Image.new('RGB', (W, H), grund(im))
    einblenden(c, im, (0, 0), W, f=30)
    band(c, W, W, H, 300)
    badge(c, (40, 34), preis)
    return c


def story(handle, preis, W=1080, H=1920):
    """9:16 fuer Stories/Reels: Set randlos in voller Breite, Preis-Etikett oben links im Bild, Feld unten mit Logo
    und Versandversprechen. Oben 14 % bleiben frei (Instagram-Bedienelemente); das Feld beginnt bei 71 %."""
    im = hauptbild(handle)
    c = Image.new('RGB', (W, H), grund(im))
    top = 285
    einblenden(c, im, (0, top), W, f=40)
    band(c, top + W, W, H)
    badge(c, (40, top + 40), preis, 1.1)
    return c


if __name__ == '__main__':
    for handle, name, preis in SETS:
        karte(handle, preis).save(os.path.join(out, f'karussell_{name}_1x1.jpg'), quality=95, subsampling=0)
        story(handle, preis).save(os.path.join(out, f'story_{name}_9x16.jpg'), quality=95, subsampling=0)
        if '--4x5' in sys.argv:
            karte_4x5(handle, preis).save(os.path.join(out, f'karussell_{name}_4x5.jpg'), quality=95, subsampling=0)
        print(name, preis)
