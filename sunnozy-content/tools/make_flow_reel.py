"""KI-Videoclips (Google Flow / Veo) zu einem sunnozy-Reel schneiden.

Schritte: Ausschnitte waehlen (harte Schnitte wie im Pinterest-Vorbild), Format zuschneiden (9:16 Reel + 4:5 Feed),
einheitlicher Soft-Look (leicht entsaettigt, Tiefen angehoben, minimal warm), feines Filmkorn gegen den "zu glatten"
KI-Look, leichte Handkamera-Bewegung, kleiner Story-Text mit Herz, Endkarte mit Logo. Ton: stumm (Trend-Sound in Instagram).

Aufruf: python3 make_flow_reel.py <ausgabeordner> <clip1.mp4> <clip2.mp4> <clip3.mp4>
  clip1 = Zoom auf schlafendes Baby (Gesicht verdeckt), clip2 = Zoom bis Gesicht, clip3 = weit, Baby wacht auf und laechelt
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

out, c1, c2, c3 = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', out, out, out, out]
exec(src, g)
logo, spaced, sprig, F, SERR, CREAM, INK, SOFT, SANS = g['logo'], g['spaced'], g['sprig'], g['F'], g['SERR'], g['CREAM'], g['INK'], g['SOFT'], g['SANS']
os.makedirs(out, exist_ok=True)
FPS = 30
INTER_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
SW, SH = 816, 1104  # Flow-Ausgabe

# (clip, start_s, ende_s, x-mitte des Motivs 0..1) – Schlafen -> Gesicht -> Aufwachen & Laecheln
SHOTS = [(c1, 1.0, 5.2, 0.52), (c2, 3.0, 6.0, 0.50), (c3, 2.6, 11.0, 0.56)]
TEXT = 'sonntagmorgen'
END_DUR = 2.4


def frames(path, t0, t1):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(t0), '-to', str(t1), '-i', path, '-vf', f'fps={FPS},scale={SW}:{SH}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = SW * SH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (SW, SH), b)
    p.wait()


def soft(im):
    im = ImageEnhance.Color(im).enhance(0.9)
    a = np.asarray(im).astype(np.float32)
    a = 12 + a * (242 / 255)
    a *= np.array([1.012, 1.0, 0.985])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def heart(d, x, y, size, fill):
    t = np.linspace(0, 2 * math.pi, 80)
    hx = 16 * np.sin(t) ** 3; hy = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    k = size / 34
    d.polygon([(x + a * k, y + b * k) for a, b in zip(hx, hy)], fill=fill)


def text_layer(W, H, y):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(INTER_M, 34)
    w = f.getlength(TEXT); hs = 22
    x0 = (W - w - hs * 2.4) / 2
    d.text((x0, y), TEXT, font=f, fill=(255, 255, 255, 255), anchor='lm')
    heart(d, x0 + w + hs * 0.9, y, hs, (255, 255, 255, 255)); heart(d, x0 + w + hs * 2.0, y, hs, (255, 255, 255, 255))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))
    dark = Image.new('RGBA', (W, H), (40, 30, 25, 0)); dark.putalpha(sh)
    return Image.alpha_composite(dark, lay)


def end_card(W, H):
    c = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(c)
    cy = H // 2
    sprig(d, W / 2, cy - 230, 1.4, SOFT)
    L = logo(520, INK); c.paste(L, ((W - L.width) // 2, cy - 140), L)
    spaced(d, W / 2, cy + 80, 'WEICH. SICHER. LIEBEVOLL.', F(SERR, 38), INK, 7)
    d.line([(W / 2 - 90, cy + 150), (W / 2 + 90, cy + 150)], fill=SOFT, width=2)
    spaced(d, W / 2, cy + 195, 'SUNNOZY.CH', F(SANS, 32), SOFT, 8)
    return c


def render(name, W, H, text_y):
    rng = np.random.default_rng(5)
    grain = [Image.fromarray(rng.normal(128, 11, (H // 2, W // 2)).clip(0, 255).astype('uint8')).resize((W, H), Image.BILINEAR) for _ in range(8)]
    txt = text_layer(W, H, text_y)
    tmp = os.path.join(out, name + '_tmp.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    k = 0; last = None
    ar = W / H
    for path, t0, t1, cx in SHOTS:
        for fr in frames(path, t0, t1):
            # Ausschnitt im Zielformat, 4 % Rand fuer die Handkamera-Bewegung
            ch = SH * 0.96 if SW / SH > ar else SW / ar * 0.96
            cw = ch * ar
            t = k / FPS
            x = cx * SW + 5 * math.sin(t * 1.3) + 3 * math.sin(t * 2.7 + 1) - cw / 2
            y = SH / 2 + 4 * math.sin(t * 1.1 + 2) + 2 * math.sin(t * 3.1) - ch / 2
            x = min(max(x, 0), SW - cw); y = min(max(y, 0), SH - ch)
            im = fr.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.LANCZOS)
            im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
            im = soft(im)
            im = Image.blend(im, Image.merge('RGB', [grain[k % 8]] * 3), 0.045)
            a = min(1.0, max(0.0, (k - 8) / 12))  # Text sanft einblenden
            if a > 0:
                l2 = txt.copy(); l2.putalpha(txt.split()[3].point(lambda v: int(v * a)))
                im = Image.alpha_composite(im.convert('RGBA'), l2).convert('RGB')
            enc.stdin.write(im.tobytes()); k += 1; last = im
    END = end_card(W, H); nf = int(0.5 * FPS)
    for i in range(int(END_DUR * FPS)):
        enc.stdin.write((Image.blend(last, END, (i + 1) / nf) if i < nf else END).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', os.path.join(out, name + '.mp4')], check=True)
    os.remove(tmp)
    print(name, round(k / FPS + END_DUR, 1), 's')


render('reel_sonntagmorgen_9x16', 1080, 1920, int(1920 * 0.44))
render('feed_sonntagmorgen_4x5', 1080, 1350, int(1350 * 0.12))
