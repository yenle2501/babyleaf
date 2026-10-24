"""Meta-Anzeigen Weihnachts-Geschenkboxen im Handyfoto-Stil («nicht so KI»): Foto zuerst natürlich nachbearbeitet,
dann schlichte Anzeigen wie ein normaler Instagram-Post (wenig Text, keine Etiketten-Grafik).

    python3 tools/make_meta_ads_weihnachtsbox_echt.py <roh-ordner>

<roh-ordner>/<box>.jpg sind die Canva-Szenen (1136 x 1408). Ausgabe nach posts/kampagne-weihnachtsbox/:
  fotos-echt/<box>.jpg            nachbearbeitetes Foto (Shop-Zusatzbild, Posts)
  meta-ads-echt/feed_<box>_4x5.jpg, story_<box>_9x16.jpg, karussell_<box>_1x1.jpg, karussell_00_uebersicht_1x1.jpg

Nachbearbeitung gegen den KI-Look: etwas wärmer und matter (Schwarz leicht angehoben, Lichter gedämpft), Sättigung
-6 %, feines Luminanz-Korn wie bei einer Handykamera, leichte Vignette, minimal weicher (KI-Bilder sind überscharf).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox')
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
WALD, CREME = (35, 48, 41), (253, 252, 250)

# Schlüssel, Name, Inhalt kurz, Preis
BOXEN = [('mum_dad_me', '«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90'),
         ('lovely_little_girl', '«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90'),
         ('growing_up_strong', '«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('i_love_my_mummy', '«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90'),
         ('dino', '«Dino»', '3 Bodys + 3 Mulltücher', '39.90'),
         ('dinosaur', '«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90'),
         ('little_one', '«Little One»', '5 Bodys + 3 Mulltücher', '44.90'),
         ('i_like_flying', '«I like flying»', '3 Bodys + 5 Leggings', '39.90'),
         ('little_one_jogginghosen', '«Little One»', '5 Bodys + 5 Jogginghosen', '42.90')]


def natuerlich(im, seed=0):
    rng = np.random.default_rng(seed)
    im = im.convert('RGB').filter(ImageFilter.GaussianBlur(0.45))
    im = ImageEnhance.Color(im).enhance(0.94)
    a = np.asarray(im).astype(np.float32) / 255
    a = 0.035 + a * 0.93                                   # matter: Schwarz hoch, Lichter runter
    a[..., 0] *= 1.025; a[..., 2] *= 0.97                  # etwas wärmer
    h, w, _ = a.shape
    y, x = np.ogrid[:h, :w]
    r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.10 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]   # leichte Vignette
    korn = rng.normal(0, 0.018, (h, w))
    korn = np.asarray(Image.fromarray(((korn + 0.5) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255 - 0.5
    a += korn[..., None] * 0.9
    return Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8))


def logo(width, col=(255, 255, 255)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def fuellen(im, W, H):
    s = max(W / im.width, H / im.height)
    t = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (t.width - W) // 2, (t.height - H) // 2
    return t.crop((x, y, x + W, y + H))


def schatten_text(c, xy, text, font, anchor='ls', fill=(255, 255, 255)):
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((xy[0] + 2, xy[1] + 2), text, font=font, fill=(0, 0, 0, 150), anchor=anchor)
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(c).text(xy, text, font=font, fill=fill, anchor=anchor)


def unten_verlauf(c, h, staerke=0.45):
    W, H = c.size
    g = np.zeros((H, 1), np.float32); g[H - h:, 0] = np.linspace(0, 1, h) ** 1.6 * staerke
    v = Image.new('RGBA', (W, H), (20, 15, 12, 0)); v.putalpha(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H)))
    c.alpha_composite(v)


def anzeige(foto, box, W, H, unten=0, oben=0):
    """Foto randlos, unten links Name, Inhalt und Preis wie eine Bildunterschrift, Logo klein unten rechts."""
    _, name, inhalt, preis = box
    c = fuellen(foto, W, H).convert('RGBA')
    unten_verlauf(c, int(H * 0.30))
    k = W / 1080; x = int(56 * k); y = H - unten - int(70 * k)
    titel = f'Weihnachts-Geschenkbox {name}'; gr = 44 * k
    while ImageDraw.Draw(c).textlength(titel, font=FONT('fraunces-600.ttf', gr)) > W - 2 * x:
        gr -= 1
    schatten_text(c, (x, y - int(64 * k)), titel, FONT('fraunces-600.ttf', gr))
    schatten_text(c, (x, y), f'{inhalt}  ·  CHF {preis}', FONT('nunitosans-600.ttf', 32 * k))
    L = logo(int(150 * k)); c.alpha_composite(L, (x, y - int(64 * k) - int(gr) - L.height - int(22 * k)))   # Logo klein über dem Namen
    if oben:
        schatten_text(c, (W / 2, oben), 'Fertig verpackt, mit Karte', FONT('nunitosans-700.ttf', 34 * k), anchor='ms')
    return c.convert('RGB')


def uebersicht(fotos, N=1080):
    """3 x 3 echte Fotos, darunter ein schlichter Streifen."""
    c = Image.new('RGB', (N, N), CREME); g = 6; band = 150
    kw = (N - 4 * g) // 3; kh = (N - band - 4 * g) // 3
    for i, f in enumerate(fotos[:9]):
        t = fuellen(f, kw, kh); c.paste(t, (g + (i % 3) * (kw + g), g + (i // 3) * (kh + g)))
    d = ImageDraw.Draw(c)
    d.text((N / 2, N - band / 2 - 14), 'Weihnachts-Geschenkboxen', font=FONT('fraunces-600.ttf', 46), fill=WALD, anchor='mm')
    d.text((N / 2, N - band / 2 + 34), 'Ganze Sets, von Hand verpackt  ·  ab CHF 29.90', font=FONT('nunitosans-600.ttf', 28), fill=(110, 118, 113), anchor='mm')
    return c


if __name__ == '__main__':
    roh = sys.argv[1]
    for d in ('fotos-echt', 'meta-ads-echt'):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    fotos = []
    for i, box in enumerate(BOXEN):
        p = os.path.join(roh, box[0] + '.jpg')
        if not os.path.exists(p):
            print('fehlt', p); continue
        f = natuerlich(Image.open(p), seed=i)
        f.save(os.path.join(OUT, 'fotos-echt', f'box_{box[0]}.jpg'), quality=93); fotos.append(f)
        anzeige(f, box, 1080, 1350).save(os.path.join(OUT, 'meta-ads-echt', f'feed_{box[0]}_4x5.jpg'), quality=93)
        anzeige(f, box, 1080, 1080).save(os.path.join(OUT, 'meta-ads-echt', f'karussell_{box[0]}_1x1.jpg'), quality=93)
        anzeige(f, box, 1080, 1920, unten=300, oben=300).save(os.path.join(OUT, 'meta-ads-echt', f'story_{box[0]}_9x16.jpg'), quality=93)
        print(box[0])
    uebersicht(fotos).save(os.path.join(OUT, 'meta-ads-echt', 'karussell_00_uebersicht_1x1.jpg'), quality=93)
