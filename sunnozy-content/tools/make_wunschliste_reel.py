"""Reel/Pin «Unsere Weihnachts-Wunschliste» (Vorbild: Pinterest-Anzeige «Our Wishlist» von The Sunday Collective).

Analyse Vorbild (6,4 s, Hochformat): warmer Off-White-Grund, oben «Our Wishlist:» kursiv mit roter, handgezeichneter
Unterstreichung, darunter 12 freigestellte Produkte im 3x4-Raster. Stop-Motion-Takt (0,2-0,8 s): ein roter Kritzel-
Kreis mit vier kleinen Strahlen umrahmt ein Produkt, ein roter Kritzel-Stern sitzt an einem zweiten, und der Schriftzug
«gift guide» ersetzt ein drittes Produkt - alles springt bei jedem Schritt an neue Stellen. Die Kritzeleien «kochen»
leicht (jede zweite Bildfolge minimal neu gezeichnet). Nach ~1 s eine weisse Logo-Karte (1 s), dann 1 s Raster ruhig.

sunnozy-Version: 12 echte Freisteller (Erstausstattung + Bodys/Hosen), Text Deutsch, Logo-Karte mit sunnozy.
Ausgabe: Reel 9:16 (1080x1920) und Pin 2:3 (1000x1500) als mp4 + Standbild.

Aufruf: python3 make_wunschliste_reel.py <freisteller-ordner> <ausgabe-ordner>
  <freisteller-ordner>/<set>/<nr>.png (Bodys/Hosen aus make_kaskade, Erstausstattung in eacut/)
"""
import sys, os, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF_IT = os.path.join(ROOT, 'fonts', 'cormorant.ttf')                # Cormorant Garamond Medium Italic
SLAB = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
BG, INK, ROT = (243, 241, 237), (38, 44, 62), (176, 36, 46)
FPS = 30
TITEL = 'Unsere Weihnachts-Wunschliste:'

# 12 Teile, zeilenweise (3 pro Zeile); bunt gemischt wie im Vorbild
TEILE = [
    'eacut/little_bear/03', 'cut/love_more_kurzarm5/02', 'cut/jogginghose5/01',
    'eacut/princess/07', 'cut/mummy_kurzarm5/05', 'eacut/hello_world/08',
    'eacut/little_bear/05', 'cut/flying_langarm3/01', 'eacut/princess/05',
    'eacut/little_loved/07', 'cut/growing_up_strong_kurzarm5/03', 'eacut/hello_world/04',
]
# Ablauf: (Dauer s, Kreis-Index, Stern-Index, Geschenkideen-Index) | 'LOGO' | 'RUHIG'
ABLAUF = [(0.2, 2, 7, 1), (0.8, 11, 3, 7), (1.0, 'LOGO'), (1.0, 'RUHIG'),
          (0.6, 8, 0, 4), (0.6, 10, 5, 6), (0.6, 4, 9, 11), (0.6, 6, 2, 9), (0.6, 2, 7, 1), (0.4, 11, 3, 7)]


def load_logo(width, col=(70, 66, 70)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def teil(name, box):
    im = Image.open(os.path.join(src, name + '.png')).convert('RGBA')
    im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8)))
    im = im.crop(im.getchannel('A').getbbox())
    s = min(box / im.width, box / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def kritzel(d, P, w):
    d.line(P, fill=ROT, width=w, joint='curve')


def kreis(d, cx, cy, rx, ry, rnd, k):
    """Handgezeichnetes Oval (gut 1 Umdrehung, Anfang/Ende ueberlappen) + vier kurze Strahlen diagonal."""
    w = max(3, int(4 * k)); P = []
    a0 = rnd.uniform(0, 6.28); n = 70
    for i in range(n + 1):
        t = a0 + i / n * 2 * math.pi * 1.12
        r = 1 + 0.035 * math.sin(3 * t + a0) + rnd.uniform(-0.012, 0.012) + 0.05 * i / n
        P.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    kritzel(d, P, w)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ox, oy = cx + sx * rx * 0.86, cy + sy * ry * 0.92   # knapp ausserhalb des Ovals, diagonal
        L = 24 * k + rnd.uniform(-3, 3) * k
        P = [(ox + sx * L * 0.7, oy + sy * L * 0.7), (ox + rnd.uniform(-2, 2) * k, oy + rnd.uniform(-2, 2) * k)]
        d.line(P, fill=ROT, width=w)
        # kleine Pfeilspitze nach innen
        ang = math.atan2(-sy, -sx)
        for s in (-1, 1):
            a = ang + math.pi + s * 0.55
            d.line([P[1], (P[1][0] + 9 * k * math.cos(a), P[1][1] + 9 * k * math.sin(a))], fill=ROT, width=w)


def stern(d, cx, cy, r, rnd, k):
    w = max(3, int(3.6 * k)); P = []
    rot = rnd.uniform(-0.25, 0.25)
    for i in range(6):
        t = -math.pi / 2 + rot + i * 4 * math.pi / 5      # Pentagramm in einem Zug (jede zweite Spitze)
        rr = r * rnd.uniform(0.93, 1.07)
        P.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    kritzel(d, P, w)


def unterstrich(d, x0, x1, y, rnd, k):
    P = [(x0 + (x1 - x0) * i / 40, y + 3 * k * math.sin(i * 0.5 + rnd.uniform(0, .4)) + i * 0.08 * k) for i in range(41)]
    kritzel(d, P, max(3, int(3.4 * k)))


def layout(W, H):
    k = W / 1080
    top = 0.15 * H if H / W > 1.7 else 0.055 * H
    cell_w, cell_h = W * 0.29, (1120 * k) / 4
    gx0 = (W - 3 * cell_w) / 2; gy0 = top + 150 * k
    return dict(k=k, top=top, cell_w=cell_w, cell_h=cell_h, gx0=gx0, gy0=gy0, box=int(min(cell_w, cell_h) * 0.78))


def zentrum(L, i):
    return L['gx0'] + (i % 3 + 0.5) * L['cell_w'], L['gy0'] + (i // 3 + 0.5) * L['cell_h']


def frame(W, H, L, ims, zustand, boil):
    k = L['k']
    if zustand == 'LOGO':
        c = Image.new('RGB', (W, H), (255, 255, 255)); lg = load_logo(int(340 * k))
        c.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2), lg); return c
    rnd = random.Random(hash((str(zustand), boil)))
    c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    ft = ImageFont.truetype(SERIF_IT, int(76 * k))
    d.text((W / 2, L['top']), TITEL, font=ft, fill=INK, anchor='mt')
    tw = d.textlength(TITEL, font=ft)
    unterstrich(d, W / 2 - tw * 0.36, W / 2 + tw * 0.36, L['top'] + 92 * k, random.Random(boil), k)
    kreis_i = stern_i = label_i = None
    if zustand != 'RUHIG':
        kreis_i, stern_i, label_i = zustand
    for i, im in enumerate(ims):
        cx, cy = zentrum(L, i)
        if i == label_i:
            a, b = 'Geschenk', 'ideen'; g = 1.0
            while True:   # Schriftzug passt ins Rasterfeld wie «gift guide» im Vorbild
                f1 = ImageFont.truetype(SLAB, int(40 * k * g)); f2 = ImageFont.truetype(SERIF_IT, int(54 * k * g))
                wa = d.textlength(a, font=f1); wb = d.textlength(b, font=f2)
                if wa + wb <= L['cell_w'] * 0.86 or g < 0.5:
                    break
                g -= 0.04
            x = cx - (wa + wb) / 2
            d.text((x, cy), a, font=f1, fill=INK, anchor='lm'); d.text((x + wa + 2 * k, cy + 2 * k), b, font=f2, fill=INK, anchor='lm')
            continue
        # leichtes Stop-Motion-Zittern der Produkte wie im Vorbild (1-2 px)
        jx, jy = rnd.uniform(-1.5, 1.5) * k, rnd.uniform(-1.5, 1.5) * k
        sh = Image.new('L', (W, H), 0); x, y = int(cx - im.width / 2 + jx), int(cy - im.height / 2 + jy)
        sh.paste(im.getchannel('A'), (x + 5, y + 9))
        sh = sh.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.16))
        dd = Image.new('RGBA', (W, H), (70, 60, 50, 0)); dd.putalpha(sh); c.alpha_composite(dd); c.alpha_composite(im, (x, y))
    d = ImageDraw.Draw(c)
    if kreis_i is not None:
        cx, cy = zentrum(L, kreis_i); kreis(d, cx, cy, L['box'] * 0.56, L['box'] * 0.5, rnd, k)
    if stern_i is not None:
        cx, cy = zentrum(L, stern_i); stern(d, cx + L['box'] * 0.36, cy - L['box'] * 0.36, 30 * k, rnd, k)
    return c.convert('RGB')


def render(W, H, name):
    L = layout(W, H)
    ims = [teil(t, L['box']) for t in TEILE]
    frame(W, H, L, ims, ABLAUF[0][1:], 0).save(os.path.join(out, name + '_standbild.jpg'), quality=94)
    tmp = os.path.join(out, name + '.tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    total = 0
    for schritt in ABLAUF:
        dauer, zustand = schritt[0], (schritt[1] if len(schritt) == 2 else schritt[1:])
        n = round(dauer * FPS); cache = {}
        for j in range(n):
            boil = j // 3                                         # Kritzel ~10x pro Sekunde neu = Stop-Motion
            if boil not in cache:
                cache[boil] = frame(W, H, L, ims, zustand, boil).tobytes()
            enc.stdin.write(cache[boil]); total += 1
    enc.stdin.close(); enc.wait()
    mp4 = os.path.join(out, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', mp4], check=True)
    os.remove(tmp)
    print(mp4, f'{total / FPS:.1f} s')


render(1080, 1920, 'reel_weihnachts_wunschliste_9x16')
render(1000, 1500, 'pin_weihnachts_wunschliste_2x3')
