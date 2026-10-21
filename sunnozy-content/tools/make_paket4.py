"""Paket 4: realistische KI-Fotos mit echten sunnozy-Outfits (Canva, Referenzbild) ->
Handschrift-Posts + Reel "Ein Tag mit dir" mit Handkamera-Bewegung und Filmkorn.

Aufruf: python3 make_paket4.py <foto-ordner> <ausgabeordner>
"""
import sys, os, math, subprocess
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
here = os.path.dirname(os.path.abspath(__file__))
gen, out = sys.argv[1:3]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', gen, gen, gen, out]
exec(src, g)
Image, ImageDraw = g['Image'], g['ImageDraw']
fill, grade, logo, F, SERR, np = g['fill'], g['grade'], g['logo'], g['F'], g['SERR'], g['np']
spaced, sprig = g['spaced'], g['sprig']
hand, put_logo = g['g']['hand'], g['g']['put_logo']
CREAM, INK, SOFT, SANS = g['CREAM'], g['INK'], g['SOFT'], g['SANS']
W, H = 1080, 1350
P = lambda k: Image.open(os.path.join(gen, k + '.jpg')).convert('RGB')


def colour(img, y, x0=150):
    return False  # immer weisse Schrift; Lesbarkeit kommt vom Verlauf


def shade(img):
    """Sanfter dunkler Verlauf im unteren Drittel, damit die weisse Handschrift immer lesbar ist."""
    w, h = img.size
    a = np.zeros((h, w), 'uint8'); y0 = int(h * 0.58)
    a[y0:] = (np.linspace(0, 1, h - y0) ** 1.4 * 120).astype('uint8')[:, None]
    ov = Image.new('RGBA', (w, h), (40, 28, 22, 0)); ov.putalpha(Image.fromarray(a))
    return Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')


# ---------- Handschrift-Posts ----------
POSTS = [
    ('decke_lila', 'Hallo Welt.\nIch bin neu hier.', 1010, 0.3),
    ('teddy_lacht', 'Dieses Lachen\nam Morgen.', 1030, 0.3),
    ('papa_gelb', 'I love mummy.\nUnd Papa ein bisschen auch.', 1010, 0.3),
    ('kapuzentuch', 'Frisch gebadet.\nDer schönste Duft der Welt.', 1020, 0.3),
    ('kuss_rosa', 'Tausend Küsse.\nUnd es reicht nie.', 1010, 0.3),
    ('bett_rosa', 'Endlich schläft sie.\nUnd ich schau ihr zu.', 1010, 0.4),
    ('bauchlage_gelb', 'Kleine Muskeln,\ngrosse Fortschritte.', 1020, 0.4),
    ('mama_lila', 'Du und ich.\nFür immer.', 1030, 0.3),
]
pd = os.path.join(out, 'handschrift'); os.makedirs(pd, exist_ok=True)
for i, (k, t, y, ay) in enumerate(POSTS, 1):
    img = shade(grade(fill(P(k), W, H, ay)))
    light = colour(img, y)
    hand(img, (W // 2, y), t, 90, fill=(112, 82, 66) if light else (255, 251, 244), anchor='ma', rot=2, shadow=not light)
    put_logo(img, 150, 40, (90, 70, 60) if light else (255, 255, 255))
    img.convert('RGB').save(os.path.join(pd, f'{i:02d}_{k}.jpg'), quality=94)

# ---------- Reel "Ein Tag mit dir" ----------
RW, RH, FPS = 1080, 1920, 30
rd = os.path.join(out, 'reels'); os.makedirs(rd, exist_ok=True)
rng = np.random.default_rng(7)
GRAIN = [Image.fromarray(rng.normal(128, 9, (RH // 2, RW // 2)).clip(0, 255).astype('uint8')).resize((RW, RH)) for _ in range(6)]


def end_card():
    c = Image.new('RGB', (RW, RH), CREAM); d = ImageDraw.Draw(c)
    sprig(d, RW / 2, 640, 1.5, SOFT)
    L = logo(560, INK); c.paste(L, ((RW - L.width) // 2, 740), L)
    spaced(d, RW / 2, 960, 'WEICH. SICHER. LIEBEVOLL.', F(SERR, 40), INK, 8)
    d.line([(RW / 2 - 90, 1040), (RW / 2 + 90, 1040)], fill=SOFT, width=2)
    spaced(d, RW / 2, 1090, 'SUNNOZY.CH', F(SANS, 34), SOFT, 8)
    spaced(d, RW / 2, 1150, 'GRATIS VERSAND AB CHF 50', F(SANS, 26), SOFT, 5)
    return c


def reel(name, scenes, dur=2.4, fade=0.35, ty=1440):
    S = 1.14  # Rand fuer Kamerabewegung
    clips = []
    for k, txt, ay in scenes:
        static = isinstance(k, Image.Image)
        im = k.resize((int(RW * S), int(RH * S))) if static else shade(grade(fill(P(k), int(RW * S), int(RH * S), ay)))
        lay = Image.new('RGBA', (RW, RH), (0, 0, 0, 0))
        if txt:
            light = colour(im.resize((RW, RH)), ty)
            hand(lay, (RW // 2, ty), txt, 100, fill=(112, 82, 66) if light else (255, 251, 244), anchor='ma', rot=2, shadow=not light)
        clips.append((im, lay, static))
    n, nf = int(dur * FPS), int(fade * FPS)
    tmp = os.path.join(rd, name + '_tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', tmp], stdin=subprocess.PIPE)

    def frame(ci, f):
        im, lay, static = clips[ci]
        t = (ci * n + f) / FPS
        if static:
            fr = im.resize((RW, RH)).convert('RGBA')
        else:
            # Handkamera: langsames Reinzoomen + weiches Schwanken + minimale Drehung
            z = 1.0 + 0.06 * f / n
            cw, ch = RW * S / (S * z) * 1.0, RH * S / (S * z)
            cx = im.width / 2 + 14 * math.sin(t * 1.3) + 6 * math.sin(t * 3.1)
            cy = im.height / 2 + 10 * math.sin(t * 1.7 + 1) + 4 * math.sin(t * 2.9)
            rot = 0.35 * math.sin(t * 1.1)
            box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
            fr = im.rotate(rot, resample=Image.BILINEAR, center=(cx, cy)).crop(tuple(int(v) for v in box)).resize((RW, RH), Image.BILINEAR)
            fr = Image.blend(fr, Image.merge('RGB', [GRAIN[f % 6]] * 3), 0.06).convert('RGBA')
        a = min(1.0, max(0.0, (f - 5) / 10))
        if a > 0:
            l2 = lay.copy(); l2.putalpha(lay.split()[3].point(lambda v: int(v * a)))
            fr = Image.alpha_composite(fr, l2)
        return fr.convert('RGB')

    for ci in range(len(clips)):
        for f in range(n - nf if ci < len(clips) - 1 else n + 24):
            fr = frame(ci, f)
            if ci > 0 and f < nf:
                fr = Image.blend(frame(ci - 1, n - nf + f), fr, f / nf)
            p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', os.path.join(rd, name + '.mp4')], check=True)
    os.remove(tmp)
    print(name, 'ok')


END = end_card()
reel('reel_ein_tag_mit_dir', [
    ('decke_lila', '6:00 – Hallo Welt', 0.3),
    ('teddy_lacht', '7:30 – das erste Lachen', 0.3),
    ('bauchlage_gelb', '10:00 – Bauchlage-Training', 0.4),
    ('kapuzentuch', '17:00 – Badezeit', 0.3),
    ('papa_gelb', '18:30 – Papa-Zeit', 0.3),
    ('kuss_rosa', '19:30 – tausend Küsse', 0.3),
    ('bett_rosa', '20:00 – endlich schläft sie', 0.4),
    (END, '', 0.5),
])
