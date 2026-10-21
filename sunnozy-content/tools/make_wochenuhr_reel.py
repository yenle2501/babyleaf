"""Reel/Pin «Wochen-Uhr» (Vorbild: Pinterest-Anzeige von Modest Roots).

Analyse Vorbild (8,7 s, Hochformat): heller grauer Papiergrund, 6 Teile im Kreis wie ein Zifferblatt, oben auf 12 Uhr
das Monogramm - 7 Positionen = 7 Wochentage. Ein feiner Stundenzeiger steht fest nach oben, ein Zeiger springt im
Uhrzeigersinn von Position zu Position; wo er hinzeigt, ersetzt der Wochentag (Serifenschrift) das Teil. Harter Schnitt
alle ~0,9 s. Nach Sonntag verschwinden die Teile (ruhiger leerer Grund), dann kurz die Wortmarke in gesperrten
Grossbuchstaben, danach beginnt die Woche neu mit Montag (ersetzt das Monogramm oben).

sunnozy-Version: 3 Sets aus T-Shirt + Hose (Sommer-Sets Krokodil und Be Brave, Hello World), echte Produktfotos;
je Set liegen T-Shirt und Hose nebeneinander auf dem Zifferblatt.
Ausgabe: Reel 9:16 (1080x1920) und Pin 2:3 (1000x1500) als mp4 + Standbild.

Aufruf: python3 make_wochenuhr_reel.py <freisteller-ordner> <ausgabe-ordner>
  Freisteller fuer diese Version: posts/paket-15-wochen-uhr/teile/
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)

src, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF = os.path.join(ROOT, 'fonts', 'cormorantR.ttf')        # Cormorant Garamond Medium
SANS = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
BG, INK = (238, 237, 235), (34, 34, 36)
FPS, TAG = 30, 0.9
TAGE = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
# Position 0 = oben (Logo), dann im Uhrzeigersinn; Winkel in Grad (0 = 12 Uhr), wie im Vorbild verteilt
WINKEL = [0, 52, 100, 150, 210, 260, 308]
TEILE = [None,                       # 0: Logo / Montag
         'krokodil_tshirt',          # 1: Sommer-Set Krokodil - T-Shirt
         'krokodil_shorts',          # 2:                       Shorts
         'be_brave_tshirt',          # 3: Sommer-Set Be Brave  - T-Shirt
         'be_brave_shorts',          # 4:                       Shorts
         'hello_world_hose',         # 5: Hello World           - Hose
         'hello_world_tshirt']       # 6:                       T-Shirt
HOSE_SKALA = 0.86                    # Hosen etwas kleiner als Shirts, wie in echt


def load_logo(width, col=(60, 58, 60)):
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


def grund(W, H):
    rng = np.random.default_rng(5)
    n = rng.normal(0, 2.2, (H, W, 1))
    a = np.clip(np.array(BG, float)[None, None, :] + n, 0, 255).astype(np.uint8)
    return Image.fromarray(a).convert('RGBA')


def setup(W, H):
    k = W / 1080
    cy = H * (0.5 if H / W > 1.7 else 0.46)
    R = 360 * k
    pos = [(W / 2 + R * math.sin(math.radians(w)) * 1.05, cy - R * math.cos(math.radians(w))) for w in WINKEL]
    return dict(k=k, c=(W / 2, cy), R=R, pos=pos, box=int(230 * k))


def bild(W, H, S, ims, tag, produkte=True, logo_oben=True, wortmarke=False):
    c = grund(W, H); d = ImageDraw.Draw(c); k = S['k']
    if wortmarke:
        f = ImageFont.truetype(SANS, int(30 * k)); t = 'SUNNOZY'
        sp = 9 * k; tw = sum(d.textlength(ch, font=f) for ch in t) + sp * (len(t) - 1); x = (W - tw) / 2
        for ch in t:
            d.text((x, H / 2), ch, font=f, fill=(110, 108, 110), anchor='lm'); x += d.textlength(ch, font=f) + sp
        return c.convert('RGB')
    if not produkte:
        return c.convert('RGB')
    for i, (px, py) in enumerate(S['pos']):
        if i == tag:
            f = ImageFont.truetype(SERIF, int(54 * k))
            d.text((px, py), TAGE[tag], font=f, fill=INK, anchor='mm'); continue
        if i == 0:
            if logo_oben:
                lg = load_logo(int(190 * k)); c.alpha_composite(lg, (int(px - lg.width / 2), int(py - lg.height / 2)))
            continue
        im = ims[i]; x, y = int(px - im.width / 2), int(py - im.height / 2)
        sh = Image.new('L', (W, H), 0); sh.paste(im.getchannel('A'), (x + 4, y + 8))
        sh = sh.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v * 0.14))
        dd = Image.new('RGBA', (W, H), (60, 55, 50, 0)); dd.putalpha(sh); c.alpha_composite(dd); c.alpha_composite(im, (x, y))
    d = ImageDraw.Draw(c); cx, cy = S['c']; w = max(2, int(3 * k))
    if tag is not None and tag != 0:          # Stundenzeiger fest auf 12, Minutenzeiger auf den Tag
        d.line([(cx, cy), (cx, cy - S['R'] * 0.5)], fill=INK, width=w)
    a = math.radians(WINKEL[tag] if tag is not None else 0)
    L = S['R'] * (0.5 if tag in (0, None) else 0.42)
    d.line([(cx, cy), (cx + L * math.sin(a), cy - L * math.cos(a))], fill=INK, width=w)
    r = 6 * k; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    return c.convert('RGB')


def render(W, H, name):
    S = setup(W, H)
    ims = [None] + [teil(t, int(S['box'] * (HOSE_SKALA if ('hose' in t or 'shorts' in t) else 1))) for t in TEILE[1:]]
    # Ablauf: Mo..So je 0,9 s, Teile weg (0,6 s), Wortmarke (0,9 s), Montag (0,9 s) -> nahtlose Schleife
    folge = [(bild(W, H, S, ims, t), TAG) for t in range(7)]
    folge += [(bild(W, H, S, ims, None, produkte=False), 0.6), (bild(W, H, S, ims, None, wortmarke=True), 0.9),
              (bild(W, H, S, ims, 0), TAG)]
    folge[1][0].save(os.path.join(out, name + '_standbild.jpg'), quality=94)
    tmp = os.path.join(out, name + '.tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    prev, n_tot = None, 0
    for im, dauer in folge:
        n = round(dauer * FPS)
        # weiches Ausblenden nur beim Wechsel zu «leer» und von der Wortmarke weg (wie im Vorbild), sonst harter Schnitt
        fade = prev is not None and (im is folge[7][0] or prev is folge[8][0])
        for j in range(n):
            if fade and j < 8:
                fr = Image.blend(prev, im, (j + 1) / 8)
                enc.stdin.write(fr.tobytes())
            else:
                enc.stdin.write(im.tobytes())
            n_tot += 1
        prev = im
    enc.stdin.close(); enc.wait()
    mp4 = os.path.join(out, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', mp4], check=True)
    os.remove(tmp)
    print(mp4, f'{n_tot / FPS:.1f} s')


render(1080, 1920, 'reel_wochen_uhr_9x16')
render(1000, 1500, 'pin_wochen_uhr_2x3')
