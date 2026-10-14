"""Reel «Flatlay entsteht» (Vorbild: Boutique-Reel, Haende legen ein Set auf einer flauschigen Decke zusammen).

Analyse Vorbild: 11 s, 9:16, von oben, weisser Teddy-Plueschteppich, getrocknete Zweige am oberen Rand, Tageslicht.
Die grossen Teile liegen schon, eine Hand mit Perlenarmband legt nacheinander die kleinen Teile dazu (Schuehchen, Muetze,
Body) und zupft sie zurecht. Kein Text, keine Endkarte, nur leichtes Handkamera-Wackeln.

Umsetzung: echte Teile aus dem Lieferantenfoto (freigestellt, Prints unveraendert), KI-Hintergrund und KI-Hand.
Die Hand bringt jedes Teil von unten ins Bild, legt es ab und zieht sich zurueck. Danach Gesamtbild und Detail-Zooms.

Aufruf: python3 make_flatlay_reel.py <ordner mit set.png, rug.jpg, hand.png> <ausgabe.mp4>
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

src, out = sys.argv[1:3]
W, H, FPS = 1080, 1920, 30
S = 1.18  # Skalierung Lieferantenfoto -> Reel

setim = Image.open(os.path.join(src, 'set.png')).convert('RGBA')
rug = Image.open(os.path.join(src, 'rug.jpg')).convert('RGB').resize((W, H), Image.LANCZOS)
hand0 = Image.open(os.path.join(src, 'hand.png')).convert('RGBA')
# Aermel nach unten verlaengern (unterste Zeilen strecken), damit der Arm nie mitten im Bild endet
_ext = Image.new('RGBA', (hand0.width, hand0.height + 700), (0, 0, 0, 0)); _ext.paste(hand0, (0, 0))
_ext.paste(hand0.crop((0, hand0.height - 3, hand0.width, hand0.height)).resize((hand0.width, 700)).filter(ImageFilter.BoxBlur(6)), (0, hand0.height))
hand0 = _ext
HS = 0.7
hand0 = hand0.resize((round(hand0.width * HS), round(hand0.height * HS)), Image.LANCZOS)
PINCH = (590 * HS, 700 * HS)  # Fingerspitzen im Handbild


from scipy import ndimage
_A = np.asarray(setim.getchannel('A'))
_LAB, _ = ndimage.label(ndimage.binary_dilation(_A > 40, iterations=2))


def part(box, keep=None):
    """Teil aus dem freigestellten Set: die zusammenhaengende Flaeche in der Mitte von box (+ optionale Maske x,y -> bool)."""
    yy, xx = np.mgrid[0:_A.shape[0], 0:_A.shape[1]]
    inbox = (xx >= box[0]) & (xx < box[2]) & (yy >= box[1]) & (yy < box[3])
    lab = np.bincount(_LAB[inbox & (_A > 40)]).argmax()
    m = (_LAB == lab)
    if keep:
        m &= keep(xx, yy)
    a = np.where(m, _A, 0).astype('uint8')
    im = setim.copy(); im.putalpha(Image.fromarray(a))
    im = im.crop(im.getchannel('A').getbbox())
    return im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)


# Teile (Koordinaten im Lieferantenfoto ohne Logo/Artikelnummer, 1200x920)
MAIN = part((14, 243, 867, 882))                                             # Kapuzentuch, Body, Strampler
HAT = part((293, 85, 499, 264))
SOCKS = part((890, 200, 1049, 342))
MITT = part((1040, 347, 1187, 510), lambda x, y: (x >= 1045) & (y <= 500))  # Faeustlinge
COMF = part((836, 347, 1100, 687), lambda x, y: ~((x >= 1045) & (y <= 500)))  # Schmusetuch mit Krone
BIB = part((770, 655, 1036, 895))

MAIN_XY = (36, 600)
# (Teil, Zielposition oben links, Hand gespiegelt)
STEPS = [
    (HAT, (365, 600 - HAT.height - 34), True, -70),
    (SOCKS, (820, 400), False, 70),
    (COMF, (60, 1400), True, -25),
    (MITT, (400, 1450), False, 0),
    (BIB, (650, 1415), False, 25),
]
T_START, T_STEP, T_HOLD = 0.8, 1.2, 1.5
DETAILS = [  # Zoom-Ausschnitte (Mitte x, Mitte y, Zoom) im fertigen Flatlay
    (MAIN_XY[0] + int(330 * S), MAIN_XY[1] + int(230 * S), 1.6),   # «Make a Wish»-Body
    (MAIN_XY[0] + int(150 * S), MAIN_XY[1] + int(200 * S), 1.6),   # Krone auf dem Kapuzentuch
    (MAIN_XY[0] + int(620 * S), MAIN_XY[1] + int(560 * S), 1.7),   # Schleifen an den Fuesschen
]
T_DETAIL = 1.0


def shadow_of(im, off, blur, op):
    a = im.getchannel('A')
    pad = blur * 3
    sh = Image.new('L', (im.width + 2 * pad, im.height + 2 * pad), 0); sh.paste(a, (pad, pad))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
    lay = Image.new('RGBA', sh.size, (60, 50, 45, 0)); lay.putalpha(sh)
    return lay, (off[0] - pad, off[1] - pad)


def comp(canvas, im, x, y):
    """alpha_composite, auch wenn das Bild teilweise ausserhalb liegt."""
    x, y = int(x), int(y)
    l, t = max(0, -x), max(0, -y)
    r, b = min(im.width, canvas.width - x), min(im.height, canvas.height - y)
    if r > l and b > t:
        canvas.alpha_composite(im.crop((l, t, r, b)), (x + l, y + t))


def put(canvas, im, xy, lifted=0.0):
    """Teil mit Schatten aufs Bild setzen; lifted 0..1 = angehoben (Schatten weiter weg, weicher)."""
    off = (int(6 + 22 * lifted), int(10 + 40 * lifted))
    sh, d = shadow_of(im, off, int(12 + 16 * lifted), 0.24 - 0.08 * lifted)
    comp(canvas, sh, xy[0] + d[0], xy[1] + d[1])
    comp(canvas, im, xy[0], xy[1])


def ease_out(p): return 1 - (1 - p) ** 3
def ease_in(p): return p ** 3


def soft(im):
    im = ImageEnhance.Color(im).enhance(0.94)
    a = np.asarray(im).astype(np.float32); a = 6 + a * (247 / 255); a *= np.array([1.01, 1.0, 0.985])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


base = rug.convert('RGBA')
put(base, MAIN, MAIN_XY)
frames_static = []  # Zustand nach jedem Schritt
cur = base.copy()
for it, xy, _, _ in STEPS:
    frames_static.append(cur.copy())
    put(cur, it, xy)
final = cur

rng = np.random.default_rng(7)
grain = [Image.fromarray(rng.normal(128, 10, (H // 2, W // 2)).clip(0, 255).astype('uint8')).resize((W, H), Image.BILINEAR) for _ in range(8)]
tmp = out + '.tmp.mp4'
enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
k = 0


def emit(im, zoom=1.0, center=None):
    """Handkamera-Wackeln + optionaler Zoom, Look, Korn."""
    global k
    t = k / FPS
    cx, cy = center or (W / 2, H / 2)
    cx += 6 * math.sin(t * 1.3) + 3 * math.sin(t * 3.1 + 1)
    cy += 5 * math.sin(t * 1.1 + 2) + 3 * math.sin(t * 2.7)
    z = zoom * 1.03
    cw, ch = W / z, H / z
    cx = min(max(cx, cw / 2), W - cw / 2); cy = min(max(cy, ch / 2), H - ch / 2)
    fr = im.convert('RGB').crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BICUBIC)
    fr = soft(fr)
    fr = Image.blend(fr, Image.merge('RGB', [grain[k % 8]] * 3), 0.04)
    enc.stdin.write(fr.tobytes()); k += 1


# 1) Ausgangslage
for _ in range(int(T_START * FPS)):
    emit(base)

# 2) Hand legt die Teile nacheinander hin
n = int(T_STEP * FPS)
for (it, (tx, ty), mirror, ang), bg in zip(STEPS, frames_static):
    hand = ImageOps.mirror(hand0) if mirror else hand0
    px, py = (hand.width - PINCH[0] if mirror else PINCH[0]), PINCH[1]
    if ang:  # Hand drehen, Griffpunkt mitdrehen
        c0 = (hand.width / 2, hand.height / 2)
        hand = hand.rotate(ang, Image.BICUBIC, expand=True)
        r = math.radians(ang); ddx, ddy = px - c0[0], py - c0[1]
        px = hand.width / 2 + ddx * math.cos(r) + ddy * math.sin(r)
        py = hand.height / 2 - ddx * math.sin(r) + ddy * math.cos(r)
    r = math.radians(ang); arm = (math.sin(r), math.cos(r))  # Richtung Finger -> Arm
    pin = (tx + it.width * 0.5, ty + it.height * (0.62 if abs(ang) < 45 else 0.5))  # Griffpunkt am Teil
    start = (pin[0] + arm[0] * 1500, pin[1] + arm[1] * 1500)
    for j in range(n):
        p = j / (n - 1)
        fr = bg.copy()
        if p < 0.5:  # hereinbringen, angehoben
            q = ease_out(p / 0.5)
            hx = start[0] + (pin[0] - start[0]) * q; hy = start[1] + (pin[1] - start[1]) * q
            lift = 1.0 - 0.3 * q; rot = (1 - q) * (-8 if mirror else 8)
        elif p < 0.62:  # absetzen
            q = (p - 0.5) / 0.12
            hx, hy = pin; lift = 0.7 * (1 - q); rot = 0
        else:  # Hand zieht sich zurueck
            q = ease_in((p - 0.62) / 0.38)
            hx = pin[0] + (start[0] - pin[0]) * q; hy = pin[1] + (start[1] - pin[1]) * q
            lift = 0; rot = 0
        dx, dy = hx - pin[0], hy - pin[1]
        itm = it if not rot else it.rotate(rot, Image.BICUBIC, expand=True)
        sc = 1 + 0.05 * lift
        if p < 0.62:
            itm = itm.resize((round(itm.width * sc), round(itm.height * sc)), Image.BICUBIC)
            ix = tx + dx - (itm.width - it.width) / 2; iy = ty + dy - (itm.height - it.height) / 2
            put(fr, itm, (ix, iy), lift)
        else:
            put(fr, it, (tx, ty))
        hsh, d = shadow_of(hand, (24, 40), 26, 0.16)
        comp(fr, hsh, hx - px + d[0], hy - py + d[1])
        comp(fr, hand, hx - px, hy - py)
        emit(fr)

# 3) fertiges Flatlay, langsam heranfahren
m = int(T_HOLD * FPS)
for j in range(m):
    emit(final, 1.0 + 0.06 * j / m)

# 4) Details
for cx, cy, z in DETAILS:
    m = int(T_DETAIL * FPS)
    for j in range(m):
        emit(final, z + 0.08 * j / m, (cx, cy))

enc.stdin.close(); enc.wait()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', out], check=True)
os.remove(tmp)
final.convert('RGB').save(out.replace('.mp4', '_flatlay.jpg'), quality=93)
print(out, round(k / FPS, 1), 's')
