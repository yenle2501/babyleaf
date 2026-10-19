"""Reel/Pin «Bei 0 anfangen» (Vorbild: Instagram-Reel einer Kinderbuch-Marke, 5 s).

Analyse Vorbild: gemuetliches, warm-gedimmtes Wohnzimmerlicht. Auf dem Laptop das neue Instagram-Profil der Marke
(0 Follower), davor ein Cupcake mit goldener Zahlenkerze «0». Eine goldene Schere schneidet ein Band durch (Eroeffnung),
die Flamme flackert, wird gross und erlischt - harter Schnitt naeher ran, Rauch steigt auf. Weisse Serifenschrift,
teils kursiv, zweizeilig versetzt: «Bei 0 anfangen ist nicht schlimm» -> «Schlimm ist nur, nie anzufangen».

sunnozy-Version: KI-Szene (Handy auf Holzstaender statt Laptop, Cupcake mit «0»-Kerze, Sofa), auf dem Handy das echte
sunnozy-Profil (Besucher-Ansicht, siehe make_profil_bildschirm.py). Statt Band-Schnitt zaehlen Beitraege und Follower
von 0 auf den heutigen Stand hoch, waehrend die Kerze brennt. Dann Ausblasen, Schnitt naeher ran, Rauch, zweiter Satz,
zum Schluss tippt «Folgen» auf «Gefolgt» (+1 Follower) und das Logo erscheint.
Ausgabe: Reel 9:16 (1080x1920) und Pin 2:3 (1000x1500) als mp4 + Standbild.

Aufruf: python3 make_bei_null_reel.py <paket-ordner>
  erwartet ki-roh/szene_kerze_brennt.jpg, ki-roh/szene_kerze_aus.jpg (deckungsgleich), profil_bildschirm.png
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)

pak = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF = os.path.join(ROOT, 'fonts', 'cormorantR.ttf')
SERIF_IT = os.path.join(ROOT, 'fonts', 'cormorant.ttf')
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
FPS = 30
BEITRAEGE, FOLLOWER, GEFOLGT = 51, 88, 227          # Stand Profil-Screenshot

A = Image.open(os.path.join(pak, 'ki-roh', 'szene_kerze_brennt.jpg')).convert('RGB')
B = Image.open(os.path.join(pak, 'ki-roh', 'szene_kerze_aus.jpg')).convert('RGB')
PROFIL = Image.open(os.path.join(pak, 'profil_bildschirm.png')).convert('RGB')
SW, SH = A.size                                      # 1921 x 3414
# Bildschirm-Ecken in der Szene (vermessen: Kanten der weissen Flaeche, Geraden-Fit), TL TR BR BL
QUAD = [(578.3, 1193.3), (1031.2, 1177.0), (1033.5, 2228.2), (549.9, 2215.8)]
DOCHT = (1321.0, 1776.0)                             # Flammenfuss
FBOX = (1150, 1330, 1500, 1800)                      # Bereich fuer Flamme + Schein

# ---------- Zeitplan (s) ----------
T_ZAEHL = (0.5, 3.0)
T_FLARE, T_AUS, T_SCHNITT = 3.35, 3.75, 3.9
T_FOLGEN = 5.7
T_LOGO = 6.4
DAUER = 7.8


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def rauschen(t, seed):
    return sum(math.sin(t * f + seed * p) * w for f, p, w in ((7.1, 1.3, .5), (13.7, 2.9, .3), (23.3, 4.1, .2)))


# ---------- Handy-Bildschirm ----------
def perspektive(dst, src):
    """Koeffizienten fuer PIL PERSPECTIVE: Ausgabepunkt dst -> Eingabepunkt src."""
    M, v = [], []
    for (x, y), (u, w) in zip(dst, src):
        M.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); v.append(u)
        M.append([0, 0, 0, x, y, 1, -w * x, -w * y]); v.append(w)
    return np.linalg.solve(np.array(M, float), np.array(v, float)).tolist()


QX0, QY0 = int(min(p[0] for p in QUAD)) - 3, int(min(p[1] for p in QUAD)) - 3
QX1, QY1 = int(max(p[0] for p in QUAD)) + 4, int(max(p[1] for p in QUAD)) + 4
SC = 2                                               # Bildschirm in doppelter Zielgroesse vorbereiten (kein Flimmern)
PW, PH = int((QUAD[1][0] - QUAD[0][0]) * SC), int((QUAD[3][1] - QUAD[0][1]) * SC)
_koef = perspektive([(x - QX0, y - QY0) for x, y in QUAD], [(0, 0), (PW, 0), (PW, PH), (0, PH)])
_maske = None
_cache = {}


def bildschirm(beitr, foll, gefolgt):
    global _maske
    key = (beitr, foll, gefolgt)
    if key in _cache:
        return _cache[key]
    p = PROFIL.copy(); d = ImageDraw.Draw(p)
    fz = ImageFont.truetype(INTER.format('SemiBold'), 50)
    for x, n in ((374, beitr), (642, foll), (912, GEFOLGT)):
        d.text((x, 492), str(n), font=fz, fill=(245, 245, 245), anchor='ls')   # Ziffern 457-492 wie im Original
    if gefolgt:
        f = ImageFont.truetype(INTER.format('SemiBold'), 40)
        bw = (1170 - 98 - 22) // 2
        d.rounded_rectangle([49, 1035, 49 + bw, 1130], 24, fill=(43, 47, 53))
        d.text((49 + bw / 2, 1082), 'Gefolgt', font=f, fill='white', anchor='mm')
    p = p.resize((PW, PH), Image.LANCZOS)
    # dunkles Display im gedimmten Raum: etwas weniger hell, leichter Glanz von links oben
    a = np.asarray(p).astype(np.float32) * 0.9
    yy, xx = np.mgrid[0:PH, 0:PW]
    glanz = np.clip(1 - (xx / PW * 0.6 + yy / PH), 0, 1) ** 2 * 26
    a = np.clip(a + glanz[..., None], 0, 255).astype(np.uint8)
    p = Image.fromarray(a)
    if _maske is None:
        m = Image.new('L', (PW * 2, PH * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, PW * 2 - 1, PH * 2 - 1], int(PW * 0.13), fill=255)
        _maske = m.resize((PW, PH), Image.LANCZOS)
    size = (QX1 - QX0, QY1 - QY0)
    rgb = p.transform(size, Image.PERSPECTIVE, _koef, Image.BICUBIC)
    al = _maske.transform(size, Image.PERSPECTIVE, _koef, Image.BICUBIC)
    _cache[key] = (rgb, al)
    return _cache[key]


def mit_bildschirm(base, beitr, foll, gefolgt=False):
    rgb, al = bildschirm(beitr, foll, gefolgt)
    im = base.copy(); im.paste(rgb, (QX0, QY0), al)
    return im


# ---------- Flamme ----------
fx0, fy0, fx1, fy1 = FBOX
A_box = np.asarray(A.crop(FBOX)).astype(np.float32)
B_box = np.asarray(B.crop(FBOX)).astype(np.float32)
D_plus = Image.fromarray(np.clip(A_box - B_box, 0, 255).astype(np.uint8))
_yy, _xx = np.mgrid[0:fy1 - fy0, 0:fx1 - fx0]
_feder = np.clip(np.minimum.reduce([_xx, _yy, fx1 - fx0 - 1 - _xx, fy1 - fy0 - 1 - _yy]) / 40, 0, 1)[..., None]


def flamme(im, sy, sx, k, g):
    """Flamme (Differenz brennt-aus) um den Docht verzerren: sy Hoehe, sx Breite, k Neigung, g Helligkeit."""
    ax, ay = DOCHT[0] - fx0, DOCHT[1] - fy0
    sy, sx = max(sy, 1e-3), max(sx, 1e-3)
    co = (1 / sx, k / sx, ax - ax / sx - k * ay / sx, 0, 1 / sy, ay - ay / sy)
    w = np.asarray(D_plus.transform(D_plus.size, Image.AFFINE, co, Image.BICUBIC)).astype(np.float32)
    box = np.asarray(im.crop(FBOX)).astype(np.float32)
    basis = B_box * _feder + box * (1 - _feder)
    neu = np.clip(basis + _feder * w * g, 0, 255).astype(np.uint8)
    im = im.copy(); im.paste(Image.fromarray(neu), (fx0, fy0))
    return im


def rauch(im, t):
    """Duenne, aufsteigende Rauchfahne ab dem Docht (t = Sekunden seit dem Ausblasen)."""
    if t <= 0:
        return im
    x0, y0, x1, y1 = 1050, 700, 1600, 1790
    lay = Image.new('L', (x1 - x0, y1 - y0), 0); d = ImageDraw.Draw(lay)
    hoehe = min(1.0, t / 1.1) * 900                       # Fahne waechst nach oben
    staerke = min(1.0, t / 0.25) * max(0.0, 1 - max(0.0, t - 2.0) / 2.2)
    for s, (amp, dick, op, wl) in enumerate(((1.0, 5, 120, 95), (0.6, 3, 85, 63), (1.4, 2, 60, 131))):
        P = []
        for i in range(90):
            h = i / 89 * hoehe
            u = h / 900
            x = DOCHT[0] - x0 + (amp * (10 + 70 * u ** 1.4)) * math.sin(h / wl - t * 2.3 + s * 1.7) \
                + 25 * u * math.sin(h / 41 + t * 1.1 + s)
            P.append((x, DOCHT[1] - 34 - y0 - h))
        for i in range(len(P) - 1):
            u = i / len(P)
            d.line([P[i], P[i + 1]], fill=int(op * staerke * (1 - u) ** 1.3), width=max(1, int(dick + 10 * u)))
    lay = lay.filter(ImageFilter.GaussianBlur(4))
    weiss = Image.new('RGB', lay.size, (214, 208, 200))
    im = im.copy(); im.paste(weiss, (x0, y0), lay)
    return im


# ---------- Text ----------
def textblock(W, H, zeilen, y0, alpha, groesse):
    """zeilen: Liste aus (Teile, Versatz); Teil = (text, kursiv, skala). Weiss mit weichem Schatten, wie im Vorbild."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    y = y0
    for teile, versatz in zeilen:
        fs = [ImageFont.truetype(SERIF_IT if it else SERIF, int(groesse * sk)) for _, it, sk in teile]
        breiten = [d.textlength(t, font=f, features=['lnum']) for (t, _, _), f in zip(teile, fs)]   # lnum: grosse «0»
        x = (W - sum(breiten)) / 2 + versatz * W
        for (t, it, sk), f, b in zip(teile, fs, breiten):
            d.text((x, y), t, font=f, fill=(255, 255, 255, 255), anchor='ls', features=['lnum']); x += b
        y += groesse * 1.12
    sh = Image.new('RGBA', (W, H), (40, 28, 20, 0)); sh.putalpha(lay.getchannel('A').filter(ImageFilter.GaussianBlur(groesse * 0.12)).point(lambda v: int(v * 0.45)))
    out = Image.alpha_composite(sh, lay)
    if alpha < 1:
        out.putalpha(out.getchannel('A').point(lambda v: int(v * alpha)))
    return out


def load_logo(width, col=(255, 255, 255)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


SATZ1 = [([('Bei ', False, 1), ('0', False, 1.45), (' anfangen', False, 1)], -0.04),
         ([('ist nicht schlimm', True, 1)], 0.08)]
SATZ2 = [([('Schlimm', True, 1), (' ist nur,', False, 1)], -0.05),
         ([('nie anzufangen', False, 1)], 0.08)]


# ---------- Kamera ----------
def kamera(t, W, H):
    """Ausschnitt (cx, cy, zoom): Einstellung 1 weit, nach dem Ausblasen harter Schnitt naeher ran; leicht aus der Hand."""
    if t < T_SCHNITT:
        z = 1.0 + 0.045 * t / T_SCHNITT; cx, cy = 960, 1720
    else:
        u = (t - T_SCHNITT) / (DAUER - T_SCHNITT)
        z = 1.2 + 0.05 * u; cx, cy = 1040, 1700
    cx += 7 * rauschen(t * 0.35, 1); cy += 6 * rauschen(t * 0.3, 2)
    return cx, cy, z


def ausschnitt(im, t, W, H):
    cx, cy, z = kamera(t, W, H)
    cw = SW / z; ch = cw * H / W                     # nie breiter als die Szene (sonst schwarzer Rand im Pin)
    if ch > SH:
        ch = SH / z; cw = ch * W / H
    cx = min(max(cx, cw / 2), SW - cw / 2); cy = min(max(cy, ch / 2), SH - ch / 2)
    s = cw / W
    return im.transform((W, H), Image.AFFINE, (s, 0, cx - cw / 2, 0, s, cy - ch / 2), Image.BICUBIC)


# ---------- Bild zum Zeitpunkt t ----------
def szene(t):
    z = ease((t - T_ZAEHL[0]) / (T_ZAEHL[1] - T_ZAEHL[0]))
    beitr, foll = round(BEITRAEGE * z), round(FOLLOWER * z)
    gefolgt = t >= T_FOLGEN
    if gefolgt:
        foll = FOLLOWER + 1
    if t < T_FLARE:
        im = mit_bildschirm(A, beitr, foll)
        return flamme(im, 1 + 0.07 * rauschen(t, 1), 1 + 0.04 * rauschen(t, 2), 0.06 * rauschen(t * 0.8, 3),
                      1 + 0.08 * rauschen(t * 1.3, 4))
    if t < T_SCHNITT:
        # Flamme blaeht sich auf und kippt (Pusten), dann fallt sie zusammen; Raum wird dunkler (A -> B)
        u = (t - T_FLARE) / (T_AUS - T_FLARE)
        base = Image.blend(A, B, ease((t - T_AUS + 0.12) / 0.2))
        im = mit_bildschirm(base, beitr, foll)
        if u < 1:
            sy = 1 + 0.9 * math.sin(min(u, 1) * math.pi * 0.75); k = -0.55 * ease(u); g = 1 + 0.25 * u
        else:
            v = (t - T_AUS) / (T_SCHNITT - T_AUS); sy = 1.6 * (1 - v) ** 2; k = -0.6; g = 1.25 * (1 - v)
        im = flamme(im, sy, 1 + 0.3 * min(u, 1), k, g)
        return rauch(im, t - T_AUS - 0.05)
    return rauch(mit_bildschirm(B, BEITRAEGE, foll, gefolgt), t - T_AUS - 0.05)


def bild(t, W, H):
    im = ausschnitt(szene(t), t, W, H).convert('RGBA')
    gross = W * (0.083 if H / W > 1.7 else 0.08)
    y0 = H * (0.2 if H / W > 1.7 else 0.12)
    if t < T_AUS:
        a = ease(t / 0.35) * (1 - ease((t - T_FLARE - 0.1) / 0.3))
        if a > 0:
            im.alpha_composite(textblock(W, H, SATZ1, y0, a, gross))
    else:
        a = ease((t - T_SCHNITT - 0.1) / 0.35)
        if a > 0:
            im.alpha_composite(textblock(W, H, SATZ2, y0, a, gross))
    if t >= T_LOGO:
        lg = load_logo(int(W * 0.26)); a = ease((t - T_LOGO) / 0.5)
        lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a * 0.95)))
        im.alpha_composite(lg, ((W - lg.width) // 2, int(y0 + gross * 1.75)))
    return im.convert('RGB')


def render(W, H, name, standbild_t=2.2):
    out = pak
    bild(standbild_t, W, H).save(os.path.join(out, name + '_standbild.jpg'), quality=94)
    tmp = os.path.join(out, name + '.tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = round(DAUER * FPS)
    for i in range(n):
        enc.stdin.write(bild(i / FPS, W, H).tobytes())
    enc.stdin.close(); enc.wait()
    mp4 = os.path.join(out, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', mp4], check=True)
    os.remove(tmp)
    print(mp4, f'{n / FPS:.1f} s')


if __name__ == '__main__':
    if len(sys.argv) > 2:                  # Probebilder: make_bei_null_reel.py <ordner> probe t1 t2 ...
        for t in map(float, sys.argv[3:]):
            bild(t, 1080, 1920).save(os.path.join(sys.argv[2], f'probe_{t:.2f}.jpg'), quality=90)
    else:
        render(1080, 1920, 'reel_bei_null_anfangen_9x16')
        render(1000, 1500, 'pin_bei_null_anfangen_2x3')
