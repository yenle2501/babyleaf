"""Kampagne «Alles drin»: Feed-Fotos (4:5) und Reels (9:16) pro Erstausstattungs-Set, dazu ein Sammel-Reel.

Idee: Der Beweis fuer «Alles drin» sind die echten Teile. Jedes Reel fragt «Was steckt drin?», dann erscheint
Teil fuer Teil mit Namen und Zaehler, am Schluss «Alles drin.» mit Teile-Anzahl, Preis und Gratisversand.
Look nach dem sunnozy-Designsystem: Creme-Grund, Waldgruen als Schrift, Fraunces fuer Titel, Nunito Sans fuer den
Rest, Produktbilder per Multiplizieren auf dem Creme (weisse Raender verschwinden), keine Emojis.

Aufruf: python3 make_alles_drin.py <ausgabe-ordner>
"""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
ET = os.path.join(POSTS, 'marktplatz-galaxus-amazon', 'einzelteile')
FONT = lambda n: os.path.join(ROOT, 'fonts', n)
CREME, WALD, KACHEL, SALBEI, ROSE = (253, 252, 250), (35, 48, 41), (244, 239, 232), (122, 139, 111), (234, 211, 201)
GRAU = (110, 118, 113)
FPS = 30

NAMEN = {'strampler': 'Strampler', 'body': 'Body', 'shirt': 'T-Shirt', 'jaeckchen': 'Jäckchen', 'hose': 'Hose',
         'muetze': 'Mütze', 'decke': 'Decke', 'laetzchen': 'Lätzchen', 'faeustlinge': 'Fäustlinge',
         'socken': 'Söckchen', 'rassel': 'Rassel', 'beissring': 'Beissring'}

# name, Titel, Preis, Teile laut Shop, Hauptbild (Handle), Kacheln: Liste von (Dateien, Beschriftung)
def et(ordner, *teile, praefix=True):
    return [([os.path.join(ET, ordner, (ordner + '_' if praefix else '') + t + '.jpg') for t in grp.split('+')],
             ' & '.join(NAMEN[t] for t in grp.split('+'))) for grp in teile]

SETS = [
    ('teddybaer', '«Teddybär»', '30.40', 8, 'erstausstattung-set-teddybaer',
     et('set_teddy_creme', 'strampler', 'body', 'decke', 'muetze', 'laetzchen', 'faeustlinge', 'socken', 'rassel+beissring')),
    ('princess', '«Princess»', '30.40', 8, 'erstausstattung-set-princess',
     et('set_rosa', 'strampler', 'body', 'decke', 'muetze', 'laetzchen', 'faeustlinge', 'socken', 'rassel')),
    ('little_and_loved', '«Little and Loved»', '30.40', 8, 'erstausstattung-set-little-and-loved',
     et('set_little_and_loved_gans_rosa', 'strampler', 'body', 'shirt', 'jaeckchen', 'hose', 'muetze', 'laetzchen', 'faeustlinge', praefix=False)),
    ('hello_world', '«Hello World»', '29.40', 8, 'erstausstattung-set-hello-world',
     et('set_hello_world_blatt_creme', 'strampler', 'body', 'shirt', 'jaeckchen', 'hose', 'muetze', 'laetzchen', 'faeustlinge', praefix=False)),
    ('hello_rosa', '«Hello»', '30.40', 6, 'erstausstattung-set-hello-spitze', None),   # Kacheln aus dem Shopbild (siehe unten)
    ('hello_little_bear', '«Hello Little Bear»', '28.40', 5, 'erstausstattung-set-hello-little-bear',
     et('set_little_bear', 'strampler', 'body', 'muetze', 'laetzchen', 'faeustlinge')),
]
HAUPT = os.path.join(POSTS, 'shopify-hauptbilder-praesentation-hd', 'bilder')   # aktuelle Shopify-Hauptbilder (seit 18.10.2026)
HELLO_ROSA_TEILE = os.environ.get('HELLO_ROSA_TEILE', os.path.join(POSTS, 'kampagne-alles-drin', 'teile_hello_rosa'))  # aus dem Shopbild geschnitten


def f(name, size):
    return ImageFont.truetype(FONT(name), int(size))


def freistellen(pfad):
    """Produktbild auf Weiss -> zugeschnitten auf den Inhalt (bleibt RGB, wird spaeter multipliziert)."""
    im = Image.open(pfad).convert('RGB')
    a = np.asarray(im.convert('L')); ys, xs = np.where(a < 244)
    pad = 12
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad), min(im.height, ys.max() + pad)))


def kombi(pfade):
    """Mehrere Teile in einer Kachel nebeneinander (z.B. Rassel & Beissring)."""
    ims = [freistellen(p) for p in pfade]
    h = max(i.height for i in ims)
    ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    c = Image.new('RGB', (sum(i.width for i in ims) + 40 * (len(ims) - 1), h), 'white'); x = 0
    for i in ims:
        c.paste(i, (x, 0)); x += i.width + 40
    return c


def kacheln_laden(s):
    if s[0] == 'hello_rosa':
        d = HELLO_ROSA_TEILE
        return [(freistellen(os.path.join(d, 'hello_rosa_teil_04.jpg')), 'Strampler, Body & Hose'),
                (freistellen(os.path.join(d, 'hello_rosa_teil_03.jpg')), 'Decke'),
                (freistellen(os.path.join(d, 'hello_rosa_teil_01.jpg')), 'Häubchen'),
                (freistellen(os.path.join(d, 'hello_rosa_teil_02.jpg')), 'Lätzchen')]
    return [(kombi(p) if len(p) > 1 else freistellen(p[0]), lab) for p, lab in s[5]]


def hauptbild(handle):
    """Aktuelles Shop-Hauptbild ohne Logo: das Logo oben links (bei 2048 px etwa x 71-478, y 63-148) wird mit dem
    Studio-Grund direkt darueber übermalt, weiche Kante. Das Bild bleibt so gross wie im Shop (nichts abgeschnitten)."""
    im = Image.open(os.path.join(HAUPT, handle + '.jpg')).convert('RGB')
    k = im.width / 2048
    x0, y0, x1, y1 = (round(v * k) for v in (50, 48, 500, 168))
    streifen = np.asarray(im.crop((x0, round(12 * k), x1, round(42 * k)))).astype(float).mean(axis=0)
    fuell = Image.fromarray(np.repeat(streifen[None], y1 - y0, axis=0).astype(np.uint8))
    maske = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(maske).rectangle((8, 8, x1 - x0 - 9, y1 - y0 - 9), fill=255)
    im.paste(fuell, (x0, y0), maske.filter(ImageFilter.GaussianBlur(4 * k)))
    return im


def foto_karte(c, im, mitte, breite):
    """Shopfoto als Karte auf den Creme-Grund setzen (Studio-Grund des Fotos bleibt sichtbar), feiner Schatten."""
    t = im.resize((round(breite), round(im.height * breite / im.width)), Image.LANCZOS)
    x, y = int(mitte[0] - t.width / 2), int(mitte[1] - t.height / 2)
    sh = Image.new('L', (t.width + 80, t.height + 80), 0)
    ImageDraw.Draw(sh).rectangle((40, 40, 40 + t.width, 40 + t.height), fill=60)
    c.paste(Image.new('RGB', sh.size, (205, 198, 188)), (x - 40, y - 30), sh.filter(ImageFilter.GaussianBlur(18)))
    c.paste(t, (x, y))


def multiply(c, im, xy):
    """Produkt (weisser Grund) per Multiplizieren auf den Creme-Grund setzen."""
    x, y = xy; box = (x, y, x + im.width, y + im.height)
    reg = c.crop(box)
    c.paste(ImageChops.multiply(reg, im), box)


def raster(n, W, top, bottom, gap=18):
    """Kachel-Positionen: Zeilen zu 3 (bei 4 Teilen 2x2), letzte Zeile zentriert."""
    pro = 2 if n == 4 else 3
    reihen = math.ceil(n / pro)
    cw = (W - 2 * 60 - (pro - 1) * gap) / pro
    ch = min(cw * 1.08, (bottom - top - (reihen - 1) * gap) / reihen)
    top += ((bottom - top) - (reihen * ch + (reihen - 1) * gap)) / 2      # Raster senkrecht mittig
    pos = []
    for i in range(n):
        r, k = divmod(i, pro)
        in_reihe = min(pro, n - r * pro)
        x0 = (W - (in_reihe * cw + (in_reihe - 1) * gap)) / 2
        pos.append((x0 + k * (cw + gap), top + r * (ch + gap), cw, ch))
    return pos


def kachel(c, d, im, lab, box, alpha=1.0, skala=1.0):
    x, y, w, h = box
    lh = 40
    d.rounded_rectangle([x, y, x + w, y + h], radius=0, fill=KACHEL)          # Kacheln eckig (Designsystem)
    s = min((w - 28) / im.width, (h - lh - 24) / im.height) * skala
    t = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    if alpha < 1:
        t = Image.blend(Image.new('RGB', t.size, (255, 255, 255)), t, alpha)
    multiply(c, t, (int(x + (w - t.width) / 2), int(y + 12 + (h - lh - 24 - t.height) / 2)))
    if alpha > 0.3:
        fl = f('nunitosans-600.ttf', 25)
        d.text((x + w / 2, y + h - lh / 2 - 4), lab, font=fl, fill=WALD, anchor='mm')


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


# ---------------- Feed-Foto 4:5 ----------------
def foto(s, teile, W=1080, H=1350):
    name, titel, preis, anzahl = s[:4]
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    gesperrt(d, (W / 2, 92), 'ERSTAUSSTATTUNG ' + titel.upper(), f('nunitosans-700.ttf', 24), SALBEI, 3)
    d.text((W / 2, 175), 'Alles drin.', font=f('fraunces-600.ttf', 96), fill=WALD, anchor='mm')
    d.text((W / 2, 252), f'{anzahl} Teile für die ersten Wochen', font=f('nunitosans-400.ttf', 32), fill=GRAU, anchor='mm')
    for (im, lab), box in zip(teile, raster(len(teile), W, 310, H - 170)):
        kachel(c, d, im, lab, box)
    d = ImageDraw.Draw(c)
    d.text((60, H - 92), f'CHF {preis}', font=f('nunitosans-700.ttf', 44), fill=WALD, anchor='lm')
    d.text((60, H - 46), 'Gratisversand ab CHF 50', font=f('nunitosans-400.ttf', 24), fill=GRAU, anchor='lm')
    lg = load_logo(230); c.paste(lg, (W - 60 - lg.width, int(H - 92 - lg.height / 2)), lg)
    return c


# ---------------- Reel 9:16 ----------------
def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def reel(s, teile, W=1080, H=1920):
    name, titel, preis, anzahl, handle = s[:5]
    haupt = hauptbild(handle)
    T_HOOK, T_TEIL, T_END = 1.6, 0.6, 2.6
    n = len(teile); t_grid = T_HOOK; t_end = T_HOOK + n * T_TEIL + 0.3
    dauer = t_end + T_END
    boxes = raster(n, W, 470, 1470)
    fz = f('nunitosans-700.ttf', 30)

    def bild(t):
        c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
        if t < T_HOOK:
            # Hook: ganzes Set, langsam rein, Frage
            z = 1.0 + 0.06 * t / T_HOOK
            foto_karte(c, haupt, (W / 2, H * 0.62), W * 0.84 * z)
            d.text((W / 2, H * 0.27), 'Was steckt drin?', font=f('fraunces-600.ttf', 92), fill=WALD, anchor='mm')
            gesperrt(d, (W / 2, H * 0.27 + 95), 'ERSTAUSSTATTUNG ' + titel.upper(), f('nunitosans-700.ttf', 26), SALBEI, 3)
            return c
        # Teile erscheinen nacheinander
        k = min(n, int((t - t_grid) / T_TEIL) + 1)
        fertig = t >= t_end
        if fertig:
            d.text((W / 2, 330), 'Alles drin.', font=f('fraunces-600.ttf', 104), fill=WALD, anchor='mm')
        else:
            gesperrt(d, (W / 2, 300), 'ERSTAUSSTATTUNG ' + titel.upper(), f('nunitosans-700.ttf', 26), SALBEI, 3)
            # bei «Hello» sind Teile gruppiert (ueberlappen im Shopbild), dort nur der Name, sonst «3 von 8 · Decke»
            zeile = teile[k - 1][1] if name == 'hello_rosa' else f'{k} von {anzahl}  ·  {teile[k - 1][1]}'
            d.text((W / 2, 380), zeile, font=fz, fill=GRAU, anchor='mm')
        for i in range(n):
            ti = t - (t_grid + i * T_TEIL)
            if ti < 0:
                continue
            a = ease(ti / 0.25); sk = 0.86 + 0.14 * ease(ti / 0.3)
            kachel(c, d, teile[i][0], teile[i][1], boxes[i], alpha=a, skala=sk)
            d = ImageDraw.Draw(c)
        if fertig:
            u = ease((t - t_end) / 0.4)
            col = tuple(int(CREME[j] + (WALD[j] - CREME[j]) * u) for j in range(3))
            d.text((W / 2, 1545), f'{anzahl} Teile  ·  CHF {preis}', font=f('nunitosans-700.ttf', 46), fill=col, anchor='mm')
            col2 = tuple(int(CREME[j] + (GRAU[j] - CREME[j]) * u) for j in range(3))
            d.text((W / 2, 1605), 'Gratisversand ab CHF 50  ·  sunnozy.ch', font=f('nunitosans-400.ttf', 30), fill=col2, anchor='mm')
            lg = load_logo(250)
            lg.putalpha(lg.getchannel('A').point(lambda v: int(v * u)))
            c.paste(lg, ((W - lg.width) // 2, 175 - lg.height // 2), lg)
        return c
    schreiben(bild, dauer, W, H, os.path.join(out, f'reel_alles_drin_{name}_9x16'))


def schreiben(bild, dauer, W, H, pfad):
    tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = round(dauer * FPS)
    for i in range(n):
        enc.stdin.write(bild(i / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad + '.mp4'], check=True)
    os.remove(tmp)
    bild(dauer - 0.5).save(pfad + '_standbild.jpg', quality=93)
    print(os.path.basename(pfad), f'{n / FPS:.1f} s', flush=True)


# ---------------- Sammel-Reel: alle 6 Sets ----------------
def sammel_reel(W=1080, H=1920):
    sets = [(s, hauptbild(s[4])) for s in SETS]
    T_HOOK, T_SET, T_END = 1.8, 1.25, 2.4
    dauer = T_HOOK + len(sets) * T_SET + T_END

    def bild(t):
        c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
        if t < T_HOOK:
            d.text((W / 2, H * 0.40), 'Baby unterwegs?', font=f('fraunces-600.ttf', 96), fill=WALD, anchor='mm')
            d.text((W / 2, H * 0.40 + 110), 'Diese Sets haben alles', font=f('nunitosans-400.ttf', 42), fill=GRAU, anchor='mm')
            d.text((W / 2, H * 0.40 + 165), 'für die ersten Wochen.', font=f('nunitosans-400.ttf', 42), fill=GRAU, anchor='mm')
            return c
        if t >= T_HOOK + len(sets) * T_SET:
            d.text((W / 2, H * 0.36), 'Alles drin.', font=f('fraunces-600.ttf', 110), fill=WALD, anchor='mm')
            d.text((W / 2, H * 0.36 + 110), '6 Erstausstattungs-Sets ab CHF 28.40', font=f('nunitosans-600.ttf', 40), fill=WALD, anchor='mm')
            d.text((W / 2, H * 0.36 + 168), 'Gratisversand ab CHF 50  ·  Versand in 1–2 Werktagen', font=f('nunitosans-400.ttf', 32), fill=GRAU, anchor='mm')
            lg = load_logo(330); c.paste(lg, ((W - lg.width) // 2, int(H * 0.36 + 260)), lg)
            return c
        i = int((t - T_HOOK) / T_SET); u = (t - T_HOOK - i * T_SET) / T_SET
        s, im = sets[i]
        z = 1.0 + 0.05 * u
        foto_karte(c, im, (W / 2, H * 0.6), W * 0.86 * z)
        gesperrt(d, (W / 2, H * 0.22), 'ERSTAUSSTATTUNG ' + s[1].upper(), f('nunitosans-700.ttf', 28), SALBEI, 3)
        d.text((W / 2, H * 0.22 + 80), f'{s[3]} Teile  ·  CHF {s[2]}', font=f('fraunces-600.ttf', 64), fill=WALD, anchor='mm')
        return c
    schreiben(bild, dauer, W, H, os.path.join(out, 'reel_alles_drin_6_sets_9x16'))


if __name__ == '__main__':
    teil = sys.argv[2:] or ['fotos', 'reels', 'sammel']
    for s in SETS:
        teile = kacheln_laden(s)
        if 'fotos' in teil:
            foto(s, teile).save(os.path.join(out, f'foto_alles_drin_{s[0]}_4x5.jpg'), quality=94)
        if 'reels' in teil:
            reel(s, teile)
    if 'sammel' in teil:
        sammel_reel()
