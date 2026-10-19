"""Paket 6 "soft": ruhiger Pinterest-Look (gedaempfte Farben, Leinen, Gesichter angeschnitten).

Feed (4:5, ohne Text und Logo, wie die Vorbilder), eine Story mit kleinem Instagram-Text und drei Reels (9:16):
  - reel_guten_morgen: eine lange Handkamera-Einstellung, kleiner Text in der Mitte
  - reel_monat_mit_dir: harte Schnitte zwischen Nahaufnahmen (Fuesse, Haende, Teddy), kleine Kursiv-Schrift
  - reel_lachen: Baby lacht im Bettchen, Schwenk/Schnitt aufs Kapuzentuch, ohne Text
Der Ton fehlt absichtlich: In Instagram einen ruhigen Trend-Sound waehlen.

Aufruf: python3 make_paket6.py <feed-fotos 4:5> <fotos 9:16> <ausgabe>
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)

feed_src, tall_src, out = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'fonts')
INTER = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
INTER_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
SERIF_I = os.path.join(FONTS, 'cormorant.ttf')    # Cormorant Garamond Medium Italic
SERIF_R = os.path.join(FONTS, 'cormorantR.ttf')   # Cormorant Garamond Medium
RW, RH, FPS = 1080, 1920, 30
rng = np.random.default_rng(11)


def soft(im):
    """Sanfter Pinterest-Look: leicht entsaettigt, Tiefen angehoben, minimal warm."""
    im = ImageEnhance.Color(im.convert('RGB')).enhance(0.9)
    a = np.asarray(im).astype(np.float32)
    a = 14 + a * (241 / 255)                      # Schwarz leicht angehoben, Weiss knapp unter 255
    a *= np.array([1.012, 1.0, 0.985])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def cover(im, w, h, ay=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def grain(im, amount=4.0):
    a = np.asarray(im).astype(np.float32)
    a += rng.normal(0, amount, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def heart(d, x, y, size, fill):
    """Kleines Herz wie das weisse Instagram-Emoji (Emoji-Schrift fehlt auf dem Server)."""
    t = np.linspace(0, 2 * math.pi, 80)
    hx = 16 * np.sin(t) ** 3
    hy = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    k = size / 34
    d.polygon([(x + px * k, y + py * k) for px, py in zip(hx, hy)], fill=fill)


def story_text(img, text, font, xy, anchor='la', hearts=1, shadow=True):
    """Kleiner Instagram-Text mit Herz(en), weiss mit weichem Schatten."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bb = d.textbbox(xy, text, font=font, anchor=anchor)
    hs = font.size * 0.62
    w_total = bb[2] - bb[0] + hearts * (hs * 1.25)
    dx = -w_total / 2 + (bb[2] - bb[0]) / 2 if anchor[0] == 'm' else 0
    pos = (xy[0] + dx, xy[1])
    d.text(pos, text, font=font, anchor=anchor, fill=(255, 255, 255, 255))
    bb = d.textbbox(pos, text, font=font, anchor=anchor)
    cy = (bb[1] + bb[3]) / 2
    for i in range(hearts):
        heart(d, bb[2] + hs * 0.75 + i * hs * 1.15, cy, hs, (255, 255, 255, 255))
    if shadow:
        sh = lay.split()[3].filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))
        dark = Image.new('RGBA', img.size, (40, 30, 25, 0)); dark.putalpha(sh)
        img = Image.alpha_composite(img.convert('RGBA'), dark)
    return Image.alpha_composite(img.convert('RGBA'), lay).convert('RGB')


# ---------- Feed 4:5 ----------
fd = os.path.join(out, 'feed'); os.makedirs(fd, exist_ok=True)
for f in sorted(os.listdir(feed_src)):
    if not f.endswith('.jpg'):
        continue
    img = grain(soft(cover(Image.open(os.path.join(feed_src, f)), 1080, 1350)), 3.0)
    if f.startswith('07_meilenstein'):
        # leere Holzscheibe beschriften: grosse "1", darunter MONAT (wie die Vorlage)
        d = ImageDraw.Draw(img); cx, cy = (889, 1052)
        num = Image.new('RGBA', img.size, (0, 0, 0, 0)); dn = ImageDraw.Draw(num)
        dn.text((cx, cy - 8), '1', font=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', 118), anchor='ms', fill=(255, 255, 255, 255))
        sh = num.split()[3].filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.3))
        dk = Image.new('RGBA', img.size, (90, 70, 50, 0)); dk.putalpha(sh)
        img = Image.alpha_composite(Image.alpha_composite(img.convert('RGBA'), dk), num).convert('RGB'); d = ImageDraw.Draw(img)
        f2 = ImageFont.truetype(SERIF_R, 30); txt = 'MONAT'
        sp = 6; w = sum(f2.getlength(c) for c in txt) + sp * (len(txt) - 1); x = cx - w / 2
        for c in txt:
            d.text((x, cy + 40), c, font=f2, fill=(122, 104, 88)); x += f2.getlength(c) + sp
    img.save(os.path.join(fd, f), quality=94)
    print('feed', f)

# ---------- Story ----------
sd = os.path.join(out, 'story'); os.makedirs(sd, exist_ok=True)
T = lambda n: Image.open(os.path.join(tall_src, n + '.jpg')).convert('RGB')
s = grain(soft(cover(T('s1_kaffee'), RW, RH)), 3.0)
s = story_text(s, 'Kaffee-Date.', ImageFont.truetype(INTER_M, 40), (96, 330))
s.save(os.path.join(sd, 'story_kaffee_date.jpg'), quality=94)
print('story ok')

# ---------- Reels ----------
rd = os.path.join(out, 'reels'); os.makedirs(rd, exist_ok=True)
GRAIN = [Image.fromarray(rng.normal(128, 10, (RH // 2, RW // 2)).clip(0, 255).astype('uint8')).resize((RW, RH)) for _ in range(6)]
S = 1.18  # Rand fuer Kamerabewegung


def prep(name):
    return soft(cover(T(name), int(RW * S), int(RH * S)))


def render(name, shots, overlay=None):
    """shots: (bild, dauer_s, (cx0,cy0,z0) -> (cx1,cy1,z1)) in Bildanteilen; harte Schnitte wie im Vorbild."""
    tmp = os.path.join(rd, name + '_tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    k = 0
    for im, dur, (a, b) in shots:
        n = int(dur * FPS)
        for i in range(n):
            u = i / max(1, n - 1); e = u * u * (3 - 2 * u)
            t = k / FPS
            cx = (a[0] + (b[0] - a[0]) * e) * im.width + 9 * math.sin(t * 1.7) + 5 * math.sin(t * 3.3 + 1)
            cy = (a[1] + (b[1] - a[1]) * e) * im.height + 7 * math.sin(t * 1.3 + 2) + 4 * math.sin(t * 2.9)
            z = a[2] + (b[2] - a[2]) * e
            cw, ch = im.width / (S * z), im.height / (S * z)
            cx = min(max(cx, cw / 2), im.width - cw / 2); cy = min(max(cy, ch / 2), im.height - ch / 2)
            rot = 0.4 * math.sin(t * 1.1)
            fr = im.rotate(rot, resample=Image.BILINEAR, center=(cx, cy)).crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((RW, RH), Image.BILINEAR)
            fr = Image.blend(fr, Image.merge('RGB', [GRAIN[k % 6]] * 3), 0.05)
            if overlay:
                fr = Image.alpha_composite(fr.convert('RGBA'), overlay).convert('RGB')
            p.stdin.write(fr.tobytes()); k += 1
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', os.path.join(rd, name + '.mp4')], check=True)
    os.remove(tmp)
    print(name, round(k / FPS, 1), 's')


def text_layer(text, font, hearts=2):
    # Text weiss auf Schwarz rendern und als Maske verwenden
    a = story_text(Image.new('RGB', (RW, RH), (0, 0, 0)), text, font, (RW // 2, int(RH * 0.44)), anchor='mm', hearts=hearts, shadow=False)
    alpha = a.convert('L')
    m = Image.new('RGBA', (RW, RH), (255, 255, 255, 0)); m.putalpha(alpha)
    sh = alpha.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))
    dark = Image.new('RGBA', (RW, RH), (40, 30, 25, 0)); dark.putalpha(sh)
    return Image.alpha_composite(dark, m)


# 1) guten morgen: eine ruhige Einstellung, langsames Reinzoomen
m1 = prep('r1_morgen')
render('reel_guten_morgen', [(m1, 8.5, ((0.5, 0.52, 1.0), (0.48, 0.55, 1.08)))],
       text_layer('guten morgen', ImageFont.truetype(INTER, 34)))

# 2) monat mit dir: kurze Schnitte zwischen Nahaufnahmen
A, B, C, D = prep('r2a_teddy'), prep('r2b_fuesse'), prep('r2c_haende'), prep('r2d_faeustchen')
render('reel_monat_mit_dir', [
    (A, 1.6, ((0.5, 0.5, 1.0), (0.5, 0.46, 1.06))),
    (B, 1.3, ((0.45, 0.4, 1.05), (0.5, 0.42, 1.12))),
    (C, 1.4, ((0.5, 0.5, 1.0), (0.52, 0.48, 1.08))),
    (B, 1.1, ((0.6, 0.35, 1.25), (0.58, 0.38, 1.3))),
    (D, 1.5, ((0.5, 0.45, 1.0), (0.48, 0.42, 1.07))),
    (C, 1.1, ((0.55, 0.55, 1.3), (0.55, 0.52, 1.36))),
    (A, 1.3, ((0.55, 0.35, 1.3), (0.53, 0.38, 1.35))),
    (D, 1.2, ((0.6, 0.55, 1.25), (0.58, 0.55, 1.3))),
    (A, 1.6, ((0.5, 0.55, 1.05), (0.5, 0.5, 1.0))),
], text_layer('2 monate mit dir', ImageFont.truetype(SERIF_I, 46), hearts=1))

# 3) lachen im bettchen: Baby -> Tuch -> Baby -> Tuch, ohne Text (wie Vorbild)
L, K = prep('r3a_lachen'), prep('r3b_bettchen')
render('reel_lachen', [
    (L, 3.0, ((0.5, 0.42, 1.04), (0.5, 0.4, 1.1))),
    (K, 2.0, ((0.45, 0.5, 1.0), (0.55, 0.52, 1.05))),
    (L, 2.6, ((0.48, 0.38, 1.1), (0.5, 0.42, 1.04))),
    (K, 1.6, ((0.55, 0.52, 1.05), (0.5, 0.5, 1.0))),
])
