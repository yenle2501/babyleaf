"""Paket «Baby-Alltag» im Stil von @littleandfern: Baby + Produkt, Weidenkorb, Musselin, weiches Tageslicht.

Analyse Vorbild (Raster-Screenshots): fast nur echte Szenen statt Studio - schlafende Neugeborene im Weidenkorb
(Moses-Korb) auf Musselindecken mit Wellenkante, Strick-Kuscheltier daneben, eine Erwachsenenhand im Bild; Flatlays
des ganzen Sets von oben, von einer Hand arrangiert; dazu Reels mit der Gruenderin vor der Kamera («Baby names this
week», «Look what's back in stock»). Texte: fette weisse Grossbuchstaben mit Schatten oder ein kleines, gedecktes
Etikett («SWADDLE TUTORIAL»). Farben warm-neutral, pastell.

Erzeugt aus ki-roh/ (Canva, Vorlagen = echte sunnozy-Setfotos):
  fotos/                    7 Feed-Bilder 4:5 (1080x1350)
  karussell_little_and_loved/  4 Slides 4:5: Baby, Flatlay, alle 8 Teile, Abschluss
  reel_neu_bei_sunnozy_9x16.mp4      alle Bilder, Schwenk durchs Bild, Etiketten
  reel_vom_set_zum_look_9x16.mp4     je Set: Set -> Baby traegt es (Wisch-Uebergang)

Aufruf: python3 make_baby_alltag.py <paket-ordner>
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

pak = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.dirname(os.path.abspath(pak))
KI = os.path.join(pak, 'ki-roh')
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
SERIF_IT = os.path.join(ROOT, 'fonts', 'cormorant.ttf')
CREME, TINTE, ETIKETT = (244, 239, 233), (74, 62, 56), (150, 124, 112)
FPS = 30


def lade(name):
    return Image.open(os.path.join(KI, name + '.jpg')).convert('RGB')


def load_logo(width, col=(74, 62, 56)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def gesperrt(d, xy, text, font, fill, sp, anchor_mitte=True):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1)
    x, y = xy
    if anchor_mitte:
        x -= w / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp
    return w


def etikett(im, text, cy, k=1.0):
    """Kleines gedecktes Etikett wie «SWADDLE TUTORIAL» im Vorbild."""
    W = im.width; lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(INTER.format('Regular'), int(34 * k)); sp = 3 * k
    w = sum(d.textlength(ch, font=f) for ch in text) + sp * (len(text) - 1)
    pw, ph = 30 * k, 26 * k
    d.rectangle([W / 2 - w / 2 - pw, cy - 22 * k - ph / 2, W / 2 + w / 2 + pw, cy + 22 * k + ph / 2], fill=ETIKETT + (225,))
    gesperrt(d, (W / 2, cy), text, f, (255, 255, 255, 255), sp)
    im.alpha_composite(lay)


def hook(im, zeilen, cy, groesse):
    """Fette weisse Grossbuchstaben mit weichem Schatten (wie «LOOK WHAT'S BACK IN STOCK»)."""
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(INTER.format('ExtraBold'), int(groesse))
    y = cy - (len(zeilen) - 1) * groesse * 0.55
    for z in zeilen:
        d.text((im.width / 2, y), z, font=f, fill=(255, 255, 255, 255), anchor='mm'); y += groesse * 1.1
    sh = Image.new('RGBA', im.size, (30, 20, 15, 0))
    sh.putalpha(lay.getchannel('A').filter(ImageFilter.GaussianBlur(groesse * 0.12)).point(lambda v: int(v * 0.55)))
    im.alpha_composite(sh); im.alpha_composite(lay)


def fuellen(im, W, H, fx=0.5, fy=0.5, zoom=1.0):
    """Bild formatfuellend zuschneiden; fx/fy = Lage des Ausschnitts (0 links/oben .. 1 rechts/unten)."""
    s = max(W / im.width, H / im.height) * zoom
    cw, ch = W / s, H / s
    x0 = (im.width - cw) * fx; y0 = (im.height - ch) * fy
    return im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), Image.BICUBIC)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ---------------- Feed-Fotos ----------------
FOTOS = ['baby_teddy_creme', 'flatlay_teddy_creme', 'baby_little_and_loved_rosa', 'flatlay_little_and_loved_rosa',
         'baby_weltall_hellblau', 'flatlay_hello_world_creme', 'baby_smile_gruen']


def fotos():
    os.makedirs(os.path.join(pak, 'fotos'), exist_ok=True)
    for i, n in enumerate(FOTOS, 1):
        fuellen(lade(n), 1080, 1350).save(os.path.join(pak, 'fotos', f'{i:02d}_{n}.jpg'), quality=93)


# ---------------- Karussell Little & Loved ----------------
TEILE_ROSA = [('strampler', 'Strampler'), ('body', 'Body'), ('shirt', 'T-Shirt'), ('jaeckchen', 'Jäckchen'),
              ('hose', 'Hose'), ('muetze', 'Mütze'), ('laetzchen', 'Lätzchen'), ('faeustlinge', 'Fäustlinge')]


def karussell():
    out = os.path.join(pak, 'karussell_little_and_loved'); os.makedirs(out, exist_ok=True)
    W, H = 1080, 1350
    # 1 Titel: Baby + Hook
    c = fuellen(lade('baby_little_and_loved_rosa'), W, H).convert('RGBA')
    hook(c, ['ALLES DRIN:', '8 TEILE'], H * 0.83, 96)
    c.convert('RGB').save(os.path.join(out, '01_titel.jpg'), quality=93)
    # 2 Flatlay
    fuellen(lade('flatlay_little_and_loved_rosa'), W, H).save(os.path.join(out, '02_flatlay.jpg'), quality=93)
    # 3 alle Teile mit Namen (Shop-Einzelbilder)
    c = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(c)
    ft = ImageFont.truetype(SERIF_IT, 64); fn = ImageFont.truetype(INTER.format('Regular'), 26)
    d.text((W / 2, 110), 'Was im Set steckt', font=ft, fill=TINTE, anchor='mm')
    src = os.path.join(POSTS, 'marktplatz-galaxus-amazon', 'einzelteile', 'set_little_and_loved_gans_rosa')
    cw, ch, top = W / 3, (H - 210) / 3, 200
    for i, (dat, name) in enumerate(TEILE_ROSA + [(None, None)]):
        cx, cy = (i % 3 + 0.5) * cw, top + (i // 3) * ch
        if name is None:
            lg = load_logo(220); c.paste(lg, (int(cx - lg.width / 2), int(cy + ch / 2 - lg.height / 2 - 10)), lg); continue
        t = Image.open(os.path.join(src, dat + '.jpg')).convert('RGB')
        t = t.crop((100, 100, t.width - 100, t.height - 100)); box = int(min(cw, ch) * 0.8)
        t.thumbnail((box, box), Image.LANCZOS)
        c.paste(t, (int(cx - t.width / 2), int(cy + 8)))
        gesperrt(d, (cx, cy + box + 26), name.upper(), fn, TINTE, 2)
    c.save(os.path.join(out, '03_alle_teile.jpg'), quality=93)
    # 4 Abschluss
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    lg = load_logo(420); c.alpha_composite(lg, ((W - lg.width) // 2, 440))
    f1 = ImageFont.truetype(SERIF_IT, 70); f2 = ImageFont.truetype(INTER.format('Regular'), 34)
    d.text((W / 2, 640), 'Das perfekte Geschenk', font=f1, fill=TINTE, anchor='mm')
    d.text((W / 2, 720), 'zur Geburt', font=f1, fill=TINTE, anchor='mm')
    gesperrt(d, (W / 2, 880), 'SUNNOZY.CH', f2, TINTE, 6)
    d.text((W / 2, 945), 'Versand in der ganzen Schweiz und EU', font=f2, fill=(120, 108, 100), anchor='mm')
    c.convert('RGB').save(os.path.join(out, '04_abschluss.jpg'), quality=93)


# ---------------- Reels ----------------
def endkarte(W, H, a=1.0):
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    lg = load_logo(int(W * 0.42)); c.alpha_composite(lg, ((W - lg.width) // 2, int(H * 0.40)))
    f = ImageFont.truetype(INTER.format('Regular'), int(W * 0.032))
    gesperrt(d, (W / 2, H * 0.40 + lg.height + W * 0.09), 'SUNNOZY.CH', f, TINTE, 6)
    d.text((W / 2, H * 0.40 + lg.height + W * 0.15), 'Versand in der ganzen Schweiz und EU', font=f, fill=(120, 108, 100), anchor='mm')
    return c


def schreiben(frames_fn, n, W, H, name):
    tmp = os.path.join(pak, name + '.tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        enc.stdin.write(frames_fn(i / FPS).convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    mp4 = os.path.join(pak, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', mp4], check=True)
    os.remove(tmp)
    print(mp4, f'{n / FPS:.1f} s')


# Reel 1: (Bild, Dauer, Etikett, Schwenk fx von->bis)
NEU = [('baby_teddy_creme', 2.2, None, (0.5, 0.5)),
       ('flatlay_teddy_creme', 1.3, 'TEDDY', (0.15, 0.85)),
       ('baby_little_and_loved_rosa', 1.3, 'LITTLE & LOVED', (0.75, 0.35)),
       ('flatlay_little_and_loved_rosa', 1.3, 'LITTLE & LOVED', (0.85, 0.15)),
       ('baby_weltall_hellblau', 1.3, 'WELTALL', (0.3, 0.7)),
       ('flatlay_hello_world_creme', 1.3, 'HELLO WORLD', (0.15, 0.85)),
       ('baby_smile_gruen', 1.3, 'SMILE', (0.6, 0.4))]


def reel_neu(W=1080, H=1920):
    ims = {n: lade(n) for n, *_ in NEU}
    starts = np.cumsum([0] + [s[1] for s in NEU]); ende = starts[-1]; dauer = ende + 1.8

    def bild(t):
        if t >= ende:
            c = endkarte(W, H)
            if t < ende + 0.25:
                prev = fuellen(ims[NEU[-1][0]], W, H, NEU[-1][3][1], 0.5, 1.06).convert('RGBA')
                c = Image.blend(prev, c, ease((t - ende) / 0.25))
            return c
        i = int(np.searchsorted(starts, t, side='right') - 1)
        n, d, lab, (a, b) = NEU[i]; u = (t - starts[i]) / d
        c = fuellen(ims[n], W, H, a + (b - a) * ease(u), 0.5, 1.0 + 0.06 * u).convert('RGBA')
        if i == 0:
            hook(c, ['NEU BEI', 'SUNNOZY'], H * 0.42, 118)
            f = ImageFont.truetype(SERIF_IT, 72); dd = ImageDraw.Draw(c)
            sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2, H * 0.42 + 190), 'für die ersten Tage', font=f, fill=(30, 20, 15, 140), anchor='mm')
            c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
            dd.text((W / 2, H * 0.42 + 190), 'für die ersten Tage', font=f, fill='white', anchor='mm')
        elif lab:
            etikett(c, lab, H * 0.62)
        return c
    schreiben(bild, round(dauer * FPS), W, H, 'reel_neu_bei_sunnozy_9x16')
    bild(0.8).convert('RGB').save(os.path.join(pak, 'reel_neu_bei_sunnozy_9x16_standbild.jpg'), quality=93)


# Reel 2: Set (Flatlay oder Studio-Praesentation) -> Baby traegt es
PAARE = [('flatlay_teddy_creme', 'baby_teddy_creme', 'TEDDY'),
         ('flatlay_little_and_loved_rosa', 'baby_little_and_loved_rosa', 'LITTLE & LOVED'),
         ('praes:set_weltall_hellblau', 'baby_weltall_hellblau', 'WELTALL'),
         ('praes:set_smile_gruen', 'baby_smile_gruen', 'SMILE')]
T_SET, T_BABY, T_WISCH = 1.1, 1.6, 0.2


def set_bild(n, W, H):
    if not n.startswith('praes:'):
        return lade(n)
    # quadratische Studio-Praesentation (ohne Logo) auf Creme, damit im Hochformat nichts abgeschnitten wird
    q = Image.open(os.path.join(POSTS, 'produktfotos-set-praesentation', 'ohne_logo', n[6:] + '_quadratisch.jpg')).convert('RGB')
    q = q.resize((W, W), Image.LANCZOS)
    c = Image.new('RGB', (W, H), CREME); c.paste(q, (0, (H - W) // 2))
    return c


def wisch(a, b, u, W):
    """Schneller Wisch nach links mit Bewegungsunschaerfe: u 0..1."""
    off = ease(u) * W
    c = Image.new('RGB', (W, a.height)); c.paste(a, (int(-off), 0)); c.paste(b, (int(W - off), 0))
    arr = np.asarray(c).astype(np.float32); s = int(60 * math.sin(math.pi * u)) + 1
    acc = np.zeros_like(arr)
    for k in range(0, s, max(1, s // 8)):
        acc += np.roll(arr, k, axis=1)
    acc /= len(range(0, s, max(1, s // 8)))
    return Image.fromarray(acc.astype(np.uint8))


def reel_look(W=1080, H=1920):
    sets = [fuellen(set_bild(s, W, H), W, H) for s, _, _ in PAARE]
    babys = [lade(b) for _, b, _ in PAARE]
    T_HOOK = 1.6
    block = T_SET + T_BABY; ende = T_HOOK + block * len(PAARE); dauer = ende + 1.8

    def bild(t):
        if t < T_HOOK:
            c = fuellen(babys[0], W, H, 0.5, 0.5, 1.12 - 0.05 * t / T_HOOK).convert('RGBA')
            hook(c, ['VOM SET', 'ZUM LIEBLINGS-', 'LOOK'], H * 0.42, 104)
            return c
        if t >= ende:
            c = endkarte(W, H)
            if t < ende + 0.25:
                c = Image.blend(fuellen(babys[-1], W, H, 0.5, 0.5, 1.08).convert('RGBA'), c, ease((t - ende) / 0.25))
            return c
        i = int((t - T_HOOK) // block); u = t - T_HOOK - i * block
        if u < T_SET - T_WISCH:
            c = fuellen(sets[i], W, H, 0.5, 0.5, 1.0 + 0.04 * u / T_SET).convert('RGBA'); etikett(c, PAARE[i][2], H * 0.62)
            return c
        if u < T_SET:
            b0 = fuellen(babys[i], W, H, 0.5, 0.5, 1.08)
            return wisch(fuellen(sets[i], W, H, 0.5, 0.5, 1.04), b0, (u - (T_SET - T_WISCH)) / T_WISCH, W).convert('RGBA')
        v = (u - T_SET) / T_BABY
        c = fuellen(babys[i], W, H, 0.5, 0.5, 1.08 - 0.06 * v).convert('RGBA'); etikett(c, PAARE[i][2], H * 0.62)
        return c
    schreiben(bild, round(dauer * FPS), W, H, 'reel_vom_set_zum_look_9x16')
    bild(0.8).convert('RGB').save(os.path.join(pak, 'reel_vom_set_zum_look_9x16_standbild.jpg'), quality=93)


if __name__ == '__main__':
    teile = sys.argv[2:] or ['fotos', 'karussell', 'reel_neu', 'reel_look']
    for t in teile:
        globals()[t]()
