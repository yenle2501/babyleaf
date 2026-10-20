"""Meta-Anzeigen (Facebook/Instagram) fuer die Erstausstattungs-Sets im Stil der Next-Karussell-Anzeige.

Analyse Vorbild (Next, Karussell-Karte 1:1): links gross das Produkt am Holzbuegel auf ruhigem Grund, oben links ein
schwarzes Preis-Etikett mit abgerundeten Ecken («CHF13»), rechts ein schmales hellgraues Feld mit der Wortmarke
senkrecht (von oben nach unten lesbar, sehr gross), darunter in fetten Grossbuchstaben das Versandversprechen und
klein grau der Hinweis. Kein weiterer Text im Bild - Produktname und «Shop now» liefert Meta unter der Karte.

sunnozy-Version: die aktuellen Shop-Hauptbilder der Sets (Buegel-Praesentation auf hellem Studio-Grund, 2048 px, Logo
oben links uebermalt). Das Foto wird ganz gezeigt, mit Luft zum Rand; die Flaeche rundherum fuehrt den Studio-Grund
des Fotos weiter (weicher Uebergang), so wirkt die Karte wie ein einziges Foto. Preis aus Shopify, sunnozy-Logo
senkrecht, «GRATISVERSAND AB CHF 50» (Versandregel Schweiz in Shopify) und «Versand in 1–2 Werktagen» (wie die Leiste
im Shop). Ausgabe je Set: Karussell-Karte 1:1 (1080x1080) und Story/Reels 9:16 (1080x1920).

Aufruf: python3 make_meta_ads.py <quell-ordner> <ausgabe-ordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
PANEL, INK, GRAU = (226, 221, 214), (17, 17, 17), (110, 106, 101)   # Feld etwas dunkler als der Studio-Grund

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


def produkt(handle):
    """Shop-Hauptbild ohne Logo (Logo bei 2048 px etwa x 71-478, y 63-148, mit dem Grund darueber uebermalt)."""
    im = Image.open(os.path.join(src, handle + '.jpg')).convert('RGB')
    k = im.width / 2048
    x0, y0, x1, y1 = (round(v * k) for v in (50, 48, 500, 168))
    streifen = np.asarray(im.crop((x0, round(12 * k), x1, round(42 * k)))).astype(float).mean(axis=0)
    fuell = Image.fromarray(np.repeat(streifen[None], y1 - y0, axis=0).astype(np.uint8))
    maske = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(maske).rectangle((8, 8, x1 - x0 - 9, y1 - y0 - 9), fill=255)
    im.paste(fuell, (x0, y0), maske.filter(ImageFilter.GaussianBlur(4 * k)))
    return im


def foto_flaeche(c, im, box, luft, oben=0):
    """Flaeche box mit dem Studio-Grund des Fotos fuellen (Fotorand nach aussen verlaengert) und das ganze Foto mit
    mindestens `luft` px Abstand zum Rand mittig daraufsetzen, Kanten weich ausgeblendet. `oben`: Foto erst ab dieser
    Hoehe (Platz fuer Preis und Instagram-Kopfzeile), der Grund reicht trotzdem bis oben."""
    x0, y0, x1, y1 = box
    s = min((x1 - x0 - 2 * luft) / im.width, (y1 - y0 - oben - 2 * luft) / im.height)
    p = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    p = p.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=2))   # nach dem Verkleinern leicht nachschaerfen
    px, py = (x1 - x0 - p.width) // 2, oben + (y1 - y0 - oben - p.height) // 2
    # Grund: Fotorand nach aussen verlaengern (Randpixel sind reiner Studio-Grund), dann weichzeichnen
    rand = np.pad(np.asarray(p), ((py, y1 - y0 - py - p.height), (px, x1 - x0 - px - p.width), (0, 0)), mode='edge')
    c.paste(Image.fromarray(rand).filter(ImageFilter.GaussianBlur(25)), (x0, y0))
    f = max(8, round(p.width * 0.03))
    m = Image.new('L', p.size, 0); ImageDraw.Draw(m).rectangle((f, f, p.width - f - 1, p.height - f - 1), fill=255)
    c.paste(p, (x0 + px, y0 + py), m.filter(ImageFilter.GaussianBlur(f / 2)))



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
    d.text((x0 + pw / 2, y1 - (y1 - y0) * 0.08), 'Versand in 1–2 Werktagen', font=fs, fill=GRAU, anchor='mm')


def karte(handle, preis, W=1080, H=1080):
    c = Image.new('RGB', (W, H), 'white')
    split = int(W * 0.70)
    foto_flaeche(c, produkt(handle), (0, 0, split, H), 34)       # Foto 688 px breit, 34 px Luft links/rechts
    panel(c, split, W, 0, H)
    badge(c, (34, 30), preis)
    return c


def story(handle, preis, W=1080, H=1920):
    """9:16 fuer Stories/Reels: Set gross oben, graues Band unten mit Logo und Versandversprechen.
    Oben 14 % und unten 20 % bleiben frei von wichtigem Inhalt (Instagram-Bedienelemente)."""
    c = Image.new('RGB', (W, H), 'white')
    band = 1290
    foto_flaeche(c, produkt(handle), (0, 0, W, band), 40, oben=370)   # Foto unter dem Preis, oben bleibt Platz fuer Instagram
    badge(c, (40, 285), preis, 1.1)
    d = ImageDraw.Draw(c)
    d.rectangle([0, band, W, H], fill=PANEL)
    lg = load_logo(380); c.paste(lg, ((W - lg.width) // 2, band + 40), lg)
    fb = ImageFont.truetype(INTER.format('Bold'), 40); fs = ImageFont.truetype(INTER.format('Regular'), 27)
    ty = band + 40 + lg.height + 45
    d.text((W / 2, ty), 'GRATISVERSAND AB CHF 50', font=fb, fill=INK, anchor='mt')
    d.text((W / 2, ty + 62), 'Versand in 1–2 Werktagen', font=fs, fill=GRAU, anchor='mt')
    return c


if __name__ == '__main__':
    for handle, name, preis in SETS:
        karte(handle, preis).save(os.path.join(out, f'karussell_{name}_1x1.jpg'), quality=95, subsampling=0)
        story(handle, preis).save(os.path.join(out, f'story_{name}_9x16.jpg'), quality=95, subsampling=0)
        print(name, preis)
