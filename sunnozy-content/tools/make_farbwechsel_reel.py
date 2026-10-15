"""Reel/Pin «Farbwechsel» (Vorbild: Pinterest-Anzeige Hanna Andersson «Make outfitting easy»).

Analyse Vorbild (9 s, Hochformat): ruhiger warm-hellgrauer Grund, oben Ueberschrift in gesperrten Grossbuchstaben +
Unterzeile, in der Mitte ein 2-teiliges Set (Oberteil vorne links, Hose hinten rechts), das alle ~0,5 s per hartem
Schnitt die Farbe wechselt - Position und Groesse bleiben exakt gleich. Drei handgezeichnete Pfeile mit kurzen
Vorteilen zeigen aufs Produkt, unten das Markenlogo. Kein Ton noetig, kein Zoom, keine Uebergaenge.

sunnozy-Version: echte Freisteller der Kombi-Sets (Body + Leggings/Jogginghose in passender Farbe).
Ausgabe: Reel 9:16 (1080x1920, mp4), Pin 2:3 (1000x1500, mp4) und je ein Standbild.

Aufruf: python3 make_farbwechsel_reel.py <teile-ordner> <ausgabe-ordner>
  <teile-ordner>/<set>/<nr>.png wie bei make_kaskade.py
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
BG, INK, LOGO_COL = (243, 241, 238), (52, 50, 48), (170, 62, 58)
FPS, STEP = 30, 0.5          # 0,5 s pro Farbe wie im Vorbild
RUNDEN = 3                   # 6 Farben x 3 Runden = 9 s

# (Body, Hose) - echte Kombi-Sets aus dem Shop, Farben passend
PAARE = [
    ('lovely_langarm3/01', 'leggings5/01'),             # lila «Lovely» + Leggings lila
    ('growing_up_strong_kurzarm5/03', 'jogginghose5/01'),  # salbei + Jogginghose salbei
    ('mumdadme_langarm5/05', 'leggings5/04'),           # Bluemchen + Leggings Bluemchen
    ('growing_up_strong_kurzarm5/02', 'jogginghose5/03'),  # hellblau + Jogginghose hellblau
    ('lovely_langarm3/03', 'leggings5/05'),             # rosa Herzen + Leggings rosa
    ('mumdadme_langarm5/03', 'leggings5/03'),           # gelb «I love mummy» + Leggings gelb
]
TITEL = 'ANZIEHEN LEICHT GEMACHT'
UNTER = 'mit kuschligen Body-&-Hosen-Sets fürs Baby!'
PUNKTE = ['superweich &\ndehnbar', '100 % Baumwolle,\nsanft zur Babyhaut', 'passt immer\nzusammen']


def load_logo(width):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), LOGO_COL + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def teil(name, h):
    im = Image.open(os.path.join(src, name + '.png')).convert('RGBA')
    im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8)))
    im = im.crop(im.getchannel('A').getbbox())
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def schatten(lay, im, x, y, blur=18, op=0.18):
    sh = Image.new('L', lay.size, 0); sh.paste(im.getchannel('A'), (x + 8, y + 14))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
    d = Image.new('RGBA', lay.size, (70, 60, 50, 0)); d.putalpha(sh)
    lay.alpha_composite(d); lay.alpha_composite(im, (x, y))


def pfeil(d, pts, w, kopf):
    """Handgezeichneter Pfeil: kubische Bezierkurve mit leichtem Zittern, Spitze am Ende."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    P = []
    for i in range(61):
        t = i / 60
        x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3 * x3
        y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y3
        P.append((x + 1.2 * math.sin(i * 0.9), y + 1.2 * math.cos(i * 0.7)))
    d.line(P, fill=INK, width=w, joint='curve')
    ang = math.atan2(P[-1][1] - P[-4][1], P[-1][0] - P[-4][0])
    for s in (-1, 1):
        a = ang + math.pi + s * 0.5
        d.line([P[-1], (P[-1][0] + kopf * math.cos(a), P[-1][1] + kopf * math.sin(a))], fill=INK, width=w)


def layout(W, H):
    """Alle Positionen relativ zur Bildgroesse; Produktbereich wie im Vorbild leicht links der Mitte."""
    k = W / 1080
    top = 0.19 * H if H / W > 1.7 else 0.075 * H        # Reel: Platz fuer Instagram-Kopfzeile und -Bildunterschrift
    return dict(k=k, titel_y=top, unter_y=top + 62 * k, body_h=int(560 * k), hose_h=int(520 * k),
                body_xy=(int(150 * k), int(top + 230 * k)), hose_xy=(int(560 * k), int(top + 520 * k)),
                logo_y=int(top + 1170 * k))


def standbild(W, H, body, hose, L):
    c = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(c); k = L['k']
    ft = ImageFont.truetype(INTER.format('Medium'), int(46 * k)); fu = ImageFont.truetype(INTER.format('Regular'), int(30 * k))
    fp = ImageFont.truetype(INTER.format('Regular'), int(25 * k))
    # Ueberschrift gesperrt (Buchstabenabstand von Hand)
    sp = 6 * k; tw = sum(d.textlength(ch, font=ft) for ch in TITEL) + sp * (len(TITEL) - 1); x = (W - tw) / 2
    for ch in TITEL:
        d.text((x, L['titel_y']), ch, font=ft, fill=INK); x += d.textlength(ch, font=ft) + sp
    d.text((W / 2, L['unter_y']), UNTER, font=fu, fill=INK, anchor='mt')
    # Hose hinten rechts, Body vorne links (wie im Vorbild)
    bx, by = L['body_xy']; hx, hy = L['hose_xy']
    hx += int((360 * k - hose.width) / 2); bx += int((520 * k - body.width) / 2)
    schatten(c, hose, hx, hy); schatten(c, body, bx, by)
    d = ImageDraw.Draw(c); w = max(3, int(3.2 * k)); kopf = 16 * k
    t = L['titel_y']
    # 1) oben rechts -> Schulter Body
    d.multiline_text((W - 60 * k, t + 205 * k), PUNKTE[0], font=fp, fill=INK, anchor='ra', align='right', spacing=4)
    pfeil(d, [(W - 230 * k, t + 200 * k), (W - 300 * k, t + 160 * k), (W - 400 * k, t + 180 * k), (W - 430 * k, t + 260 * k)], w, kopf)
    # 2) links Mitte -> Body unten
    d.multiline_text((40 * k, t + 830 * k), PUNKTE[1], font=fp, fill=INK, spacing=4)
    pfeil(d, [(70 * k, t + 912 * k), (100 * k, t + 985 * k), (270 * k, t + 975 * k), (300 * k, t + 805 * k)], w, kopf)
    # 3) unten rechts -> Hose
    d.multiline_text((W - 60 * k, t + 1060 * k), PUNKTE[2], font=fp, fill=INK, anchor='ra', align='right', spacing=4)
    pfeil(d, [(W - 260 * k, t + 1075 * k), (W - 330 * k, t + 1080 * k), (W - 360 * k, t + 1040 * k), (W - 350 * k, t + 990 * k)], w, kopf)
    lg = load_logo(int(250 * k)); c.alpha_composite(lg, ((W - lg.width) // 2, L['logo_y']))
    return c.convert('RGB')


def render(W, H, name):
    L = layout(W, H)
    frames = [standbild(W, H, teil(b, L['body_h']), teil(h, L['hose_h']), L) for b, h in PAARE]
    frames[0].save(os.path.join(out, name + '_standbild.jpg'), quality=94)
    n = int(STEP * FPS); tmp = os.path.join(out, name + '.tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    raw = [f.tobytes() for f in frames]
    for _ in range(RUNDEN):
        for r in raw:
            for _ in range(n):
                enc.stdin.write(r)
    enc.stdin.close(); enc.wait()
    mp4 = os.path.join(out, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', mp4], check=True)
    os.remove(tmp)
    print(mp4, f'{len(PAARE) * RUNDEN * STEP:.1f} s')


render(1080, 1920, 'reel_anziehen_leicht_gemacht_9x16')
render(1000, 1500, 'pin_anziehen_leicht_gemacht_2x3')
