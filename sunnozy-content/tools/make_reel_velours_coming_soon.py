"""Coming-soon-Reel Strampler «Velours» Creme mit Puffärmeln und Rüschen (13.11.2026, zweite Fassung).

Die erste Fassung (zwei Clips mit verschiedenen Kamerawinkeln zusammengeschnitten) gefiel der Nutzerin nicht.
Neu: je Reel **eine durchgehende Einstellung**, ohne Schnitt:
  - Zeitlupe (0,6×, Zwischenbilder berechnet) genau im süssesten Moment
  - langsamer Zoom auf das Baby
  - warme, leicht kontrastreichere Farben, sanfte Vignette, nachgeschärft
  - Text in Schreibmaschinenschrift, grösser und mit stärkerem Schatten, damit er auf Creme lesbar bleibt
  - Schluss «coming soon 🤍», kein Preis

  strampeln: clip_strampeln 4.0–11.4 s, Zeitlupe 8.0–10.6 s (Beinchen mit Rüschen strampeln, «O»-Mund)
  strecken:  clip_strecken  0.0–8.0 s,  Zeitlupe 0.8–3.2 s (grosses Strecken, Puffärmel)

    python3 tools/make_reel_velours_coming_soon.py [strampeln|strecken|weihnachten]
Ausgabe: posts/coming-soon/reels/velours/reel_velours_<variante>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import make_coming_soon_reels as m
import make_reel_hello_little_bear_hook as hk

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'coming-soon', 'reels', 'velours')
O = os.path.join(BASIS, 'original')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'mixkit_lily-j_holiday-01.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
TEMPO = 0.6

VARIANTEN = {
    'strampeln': {'clip': 'clip_strampeln.mp4', 'teile': [(4.0, 8.0, 1), (8.0, 10.6, TEMPO), (10.6, 11.4, 1)],
                  'hook': ['POV: Puffärmel, Rüschen', 'und Babyfieber'], 'emoji': '🎀', 'zoom': (1.0, 1.12), 'mitte': 0.45},
    'strecken': {'clip': 'clip_strecken.mp4', 'teile': [(0.0, 0.8, 1), (0.8, 3.2, TEMPO), (3.2, 8.0, 1)],
                 'hook': ['POV: Ihr erster Winter,', 'ganz in Velours'], 'emoji': '✨', 'zoom': (1.0, 1.10), 'mitte': 0.42},
    # Weihnachtsmodus (Wunsch der Nutzerin): gleicher Clip wie «strecken», goldwarme Farben, weinroter Rand,
    # Lichter-Bokeh an den Rändern und leise fallende Funken, Weihnachts-Hook
    'weihnachten': {'clip': 'clip_strecken.mp4', 'teile': [(0.0, 0.8, 1), (0.8, 3.2, TEMPO), (3.2, 8.0, 1)],
                    'hook': ['POV: Ihr erstes Weihnachten,', 'ganz in Velours'], 'emoji': '🎄', 'zoom': (1.0, 1.10), 'mitte': 0.42,
                    'look': 'weihnacht', 'ende': '🎄', 'musik': 'mixkit_michael-ramir_christmas-lullaby.mp3'},
}


def warm_weihnacht(im):
    a = np.asarray(im).astype(np.float32)
    a[..., 0] = a[..., 0] * 1.08 + 6; a[..., 1] = a[..., 1] * 0.99; a[..., 2] = a[..., 2] * 0.82   # goldwarm
    a = (a - 128) * 1.08 + 128                                                                     # mehr Tiefe
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return ImageEnhance.Color(im).enhance(1.06)


def rand_rot():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W * 0.6)) ** 2 + ((y - H / 2) / (H * 0.6)) ** 2)
    a = np.clip((r - 0.5) / 0.65, 0, 1) ** 1.5 * 130
    v = Image.new('RGBA', (W, H), (98, 22, 30, 0)); v.putalpha(Image.fromarray(a.astype(np.uint8)))
    return v


class Lichter:
    """Unscharfe Lichterkette (Bokeh) nur am Rand, damit Gesicht und Strampler frei bleiben, dazu fallende Funken."""
    def __init__(self, seed=7):
        rng = np.random.default_rng(seed); self.orbs = []
        while len(self.orbs) < 34:
            x, y = rng.uniform(0, W), rng.uniform(0, H)
            if 190 < x < 890 and 230 < y < 1680:
                continue
            farbe = [(255, 214, 140), (255, 190, 110), (255, 236, 190), (235, 110, 90)][rng.choice(4, p=[.4, .3, .2, .1])]
            self.orbs.append((x, y, rng.uniform(34, 105), farbe, rng.uniform(.55, .9), rng.uniform(0, 6.3), rng.uniform(.6, 1.6)))
        self.funken = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.5, 6), rng.uniform(25, 60), rng.uniform(0, 6.3)) for _ in range(80)]
        self.schein = self.lichtschein()
        self.kreis = {}

    def orb(self, r, farbe):
        k = (int(r), farbe)
        if k not in self.kreis:
            g = int(r * 2.6); im = Image.new('RGBA', (g, g), farbe + (0,))
            mk = Image.new('L', (g, g), 0); ImageDraw.Draw(mk).ellipse((g / 2 - r, g / 2 - r, g / 2 + r, g / 2 + r), fill=255)
            im.putalpha(mk.filter(ImageFilter.GaussianBlur(r * 0.35))); self.kreis[k] = im
        return self.kreis[k]

    @staticmethod
    def lichtschein():
        """Warmer Schein oben links und rechts, wie von einer Lichterkette ausserhalb des Bildes."""
        y, x = np.mgrid[0:H, 0:W]
        a = np.zeros((H, W), np.float32)
        for cx, cy, r in ((0, 0, 620), (W, 120, 560), (W, H, 520)):
            a += np.clip(1 - np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r, 0, 1) ** 1.8
        e = Image.new('RGBA', (W, H), (255, 196, 110, 0)); e.putalpha(Image.fromarray((np.clip(a, 0, 1) * 120).astype(np.uint8)))
        return e

    def ebene(self, t):
        e = self.schein.copy()
        for x, y, r, farbe, alpha, ph, sp in self.orbs:
            a = alpha * (0.75 + 0.25 * np.sin(ph + t * sp))
            o = self.orb(r, farbe); o2 = o.copy(); o2.putalpha(o.getchannel('A').point(lambda q: int(q * a)))
            e.alpha_composite(o2, (int(x - o.width / 2 + 8 * np.sin(ph + t * 0.3)), int(y - o.height / 2)))
        d = ImageDraw.Draw(e)
        for x, y, r, v, ph in self.funken:
            yy = (y + v * t) % H; xx = x + 12 * np.sin(ph + t * 0.8)
            if 220 < xx < 860 and 300 < yy < 1600:
                a = 90                                  # über dem Baby nur ganz zart
            else:
                a = 200
            d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(255, 248, 230, min(255, int(a * 1.2 * (0.6 + 0.4 * np.sin(ph + t * 3))))))
        return e


def zeitachse(clip, teile, ziel):
    """Teile normal oder in Zeitlupe (Bewegungs-Interpolation) zu einem 30-fps-Clip zusammensetzen."""
    fc, labels = [], []
    for k, (a, b, v) in enumerate(teile):
        if v == 1:
            fc.append(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS}[t{k}]')
        else:
            fc.append(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,minterpolate=fps={round(FPS / v)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,'
                      f'setpts=PTS/{v},fps={FPS}[t{k}]')
        labels.append(f'[t{k}]')
    fc.append(''.join(labels) + f'concat=n={len(teile)}:v=1:a=0[v]')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(O, clip), '-filter_complex', ';'.join(fc), '-map', '[v]',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', ziel], check=True)


def frames(pfad):
    w, h = 768, 1168
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', pfad, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        yield Image.frombuffer('RGB', (w, h), b)


def vignette():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((r - 0.55) / 0.6, 0, 1) ** 1.6 * 70
    v = Image.new('RGBA', (W, H), (60, 40, 25, 0)); v.putalpha(Image.fromarray(a.astype(np.uint8)))
    return v


def warm(im):
    a = np.asarray(im).astype(np.float32)
    a[..., 0] *= 1.03; a[..., 2] *= 0.95                    # leicht wärmer
    a = (a - 128) * 1.05 + 128 + 2                          # etwas mehr Kontrast
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return ImageEnhance.Color(im).enhance(0.95)


def text_ebene(zeilen, zeichen, y0=900, groesse=58):
    fo = ImageFont.truetype(SCHRIFT, groesse); lh = int(groesse * 1.22)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    sch = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(sch)
    em = hk.emoji(zeichen, int(groesse * 0.9)) if zeichen else None
    for k, z in enumerate(zeilen):
        letzte = k == len(zeilen) - 1 and em is not None
        breite = d.textlength(z, font=fo) + (em.width + 14 if letzte else 0)
        x0 = (W - breite) / 2; y = y0 + k * lh
        for dx, dy in ((0, 3), (2, 3), (-2, 3), (0, 0)):
            ds.text((x0 + dx, y + dy), z, font=fo, fill=200, anchor='lm')
        d.text((x0, y), z, font=fo, fill=(255, 255, 255, 255), anchor='lm')
        if letzte:
            tx.alpha_composite(em, (int(x0 + breite - em.width), int(y - em.height / 2 - 4)))
    sch = sch.filter(ImageFilter.GaussianBlur(9))
    e = Image.new('RGBA', (W, H), (45, 30, 20, 0)); e.putalpha(sch)
    e.alpha_composite(tx)
    return e


def reel(name):
    v = VARIANTEN[name]
    dauer = sum((b - a) / s for a, b, s in v['teile'])
    with tempfile.TemporaryDirectory() as td:
        zw = os.path.join(td, 'zeit.mp4'); zeitachse(v['clip'], v['teile'], zw)
        e1, e2 = text_ebene(v['hook'], v['emoji']), text_ebene(['coming soon'], v.get('ende', '🤍'), y0=930, groesse=64)
        xmas = v.get('look') == 'weihnacht'
        vig = rand_rot() if xmas else vignette(); lichter = Lichter() if xmas else None
        pfad = os.path.join(BASIS, f'reel_velours_{name}_9x16.mp4'); tmp = os.path.join(td, 'v.mp4')
        enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
        sw = round(768 * H / 1168); n = 0
        for i, fr in enumerate(frames(zw)):
            t = i / FPS
            z = v['zoom'][0] + (v['zoom'][1] - v['zoom'][0]) * m.ease(t / dauer)
            gross = fr.resize((round(sw * z), round(H * z)), Image.LANCZOS)
            x0 = (gross.width - W) // 2; y0 = int((gross.height - H) * v['mitte'])
            c = gross.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
            c = (warm_weihnacht(c) if xmas else warm(c)).convert('RGBA'); c.alpha_composite(vig)
            if lichter:
                c.alpha_composite(lichter.ebene(t))
            for eb, a in ((e1, 1 - m.ease((t - 2.6) / 0.4)), (e2, m.ease((t - (dauer - 2.0)) / 0.5))):
                if a > 0:
                    e = eb.copy(); e.putalpha(e.getchannel('A').point(lambda q: int(q * a)))
                    c.alpha_composite(e)
            if i == int(0.5 * FPS):
                c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
            enc.stdin.write(c.convert('RGB').tobytes()); n += 1
        enc.stdin.close(); enc.wait()
        dauer = n / FPS
        musik = os.path.join(os.path.dirname(MUSIK), v['musik']) if 'musik' in v else MUSIK
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4' if 'musik' in v else '0', '-i', musik, '-t', f'{dauer:.2f}',
                        '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.0:.2f}:d=1.0,volume=1.4,alimiter=limit=0.89',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
