"""Unboxing-Reel aus einem Querformat-Handyvideo (Geschenkbox).

Erzeugt zwei 9:16-Versionen:
  - vollbild: Video bildfuellend, Handschrift unten, Logo klein (Hausstil)
  - rahmen:   quadratischer Ausschnitt auf Creme, Handschrift oben, Logo unten
Tempo-Wechsel pro Abschnitt, langsamer Schwenk beim Reveal, Endkarte, Originalton normalisiert.

Aufruf: python3 make_unboxing.py <video.mov> <ausgabeordner>
"""
import sys, os, subprocess, math
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
src_video, out = sys.argv[1:3]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', out, out, out, out]
exec(src, g)
Image, ImageDraw = g['Image'], g['ImageDraw']
logo, F, SERR, spaced, sprig, grade = g['logo'], g['F'], g['SERR'], g['spaced'], g['sprig'], g['grade']
hand, put_logo = g['g']['hand'], g['g']['put_logo']
CREAM, INK, SOFT, SANS = g['CREAM'], g['INK'], g['SOFT'], g['SANS']
os.makedirs(out, exist_ok=True)

SW, SH, FPS = 1920, 1080, 30
RW, RH = 1080, 1920
# Abschnitte: (start, ende, tempo, schwenk-mitte-start, schwenk-mitte-ende) in Quell-Sekunden / Pixeln
SEG = [(0.0, 3.0, 1.5, 960, 960), (3.0, 8.0, 1.25, 1000, 1000), (8.0, 12.0, 1.5, 980, 980), (12.0, 19.6, 1.0, 760, 1120)]
TEXT = [(0.0, 2.0, 'Euer Paket ist da …'), (2.0, 6.0, 'mit Liebe verpackt.'), (6.0, 8.6, 'und darin …'),
        (8.6, 12.4, 'das ganze Set für\ndie ersten Tage.'), (12.4, 16.2, 'weich. sicher. liebevoll.')]
END_DUR = 2.6


def timeline():
    """Liste (quell_zeit, schwenk_mitte) fuer jedes Ausgabe-Frame."""
    tl = []
    for a, b, sp, c0, c1 in SEG:
        n = int(round((b - a) / sp * FPS))
        for i in range(n):
            u = i / max(1, n - 1)
            e = 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, (u - 0.05) / 0.7)))  # weicher Schwenk
            tl.append((a + i * sp / FPS, c0 + (c1 - c0) * e))
    return tl


def text_layers(mode):
    lays = []
    for t0, t1, txt in TEXT:
        lay = Image.new('RGBA', (RW, RH), (0, 0, 0, 0))
        if mode == 'vollbild':
            hand(lay, (RW // 2, 1470), txt, 104, fill=(255, 251, 244), anchor='ma', rot=2, shadow=True)
        else:
            hand(lay, (RW // 2, 150 if '\n' in txt else 200), txt, 96, fill=(112, 82, 66), anchor='ma', rot=2, shadow=False)
        lays.append((t0, t1, lay))
    return lays


def shade(w, h):
    a = np.zeros((h, w), 'uint8'); y0 = int(h * 0.55)
    a[y0:] = (np.linspace(0, 1, h - y0) ** 1.4 * 130).astype('uint8')[:, None]
    ov = Image.new('RGBA', (w, h), (40, 28, 22, 0)); ov.putalpha(Image.fromarray(a)); return ov


def end_card():
    c = Image.new('RGB', (RW, RH), CREAM); d = ImageDraw.Draw(c)
    sprig(d, RW / 2, 600, 1.5, SOFT)
    L = logo(560, INK); c.paste(L, ((RW - L.width) // 2, 700), L)
    spaced(d, RW / 2, 930, 'DAS GESCHENK ZUR GEBURT', F(SERR, 40), INK, 8)
    d.line([(RW / 2 - 90, 1010), (RW / 2 + 90, 1010)], fill=SOFT, width=2)
    spaced(d, RW / 2, 1060, 'SUNNOZY.CH', F(SANS, 34), SOFT, 8)
    spaced(d, RW / 2, 1120, 'GRATIS VERSAND AB CHF 50', F(SANS, 26), SOFT, 5)
    return c


def render(mode):
    tl = timeline(); lays = text_layers(mode); END = end_card()
    SHADE = shade(RW, RH) if mode == 'vollbild' else None
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src_video, '-vf', f'fps={FPS},scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    tmp = os.path.join(out, f'_{mode}.mp4')
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    fsize = SW * SH * 3; cur_idx = -1; cur = None
    last = None
    for k, (ts, cx) in enumerate(tl):
        want = int(round(ts * FPS))
        while cur_idx < want:
            buf = dec.stdout.read(fsize)
            if len(buf) < fsize: break
            cur = buf; cur_idx += 1
        im = Image.frombuffer('RGB', (SW, SH), cur)
        if mode == 'vollbild':
            cw = int(SH * RW / RH)  # 607
            x0 = int(min(SW - cw, max(0, cx - cw / 2)))
            fr = grade(im.crop((x0, 0, x0 + cw, SH)).resize((RW, RH), Image.LANCZOS)).convert('RGBA')
            fr = Image.alpha_composite(fr, SHADE)
        else:
            x0 = int(min(SW - SH, max(0, cx - SH / 2)))
            sq = grade(im.crop((x0, 0, x0 + SH, SH)).resize((RW, RW), Image.LANCZOS))
            fr = Image.new('RGBA', (RW, RH), CREAM + (255,)); fr.paste(sq, (0, 420))
        t = k / FPS
        for t0, t1, lay in lays:
            if t0 <= t < t1:
                a = min(1, (t - t0) / 0.3, (t1 - t) / 0.25)
                l2 = lay.copy(); l2.putalpha(lay.split()[3].point(lambda v, a=a: int(v * a)))
                fr = Image.alpha_composite(fr, l2)
        if mode == 'vollbild':
            put_logo(fr, 150, 60, (255, 255, 255))
        else:
            L = logo(200, INK); fr.paste(L, ((RW - L.width) // 2, 1500 + (420 - L.height) // 2 - 60), L)
        last = fr.convert('RGB'); enc.stdin.write(last.tobytes())
    dec.stdout.close(); dec.terminate()
    nf = int(0.4 * FPS)
    for i in range(int(END_DUR * FPS)):
        fr = Image.blend(last, END, min(1, (i + 1) / nf)) if i < nf else END
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    return tmp, len(tl) / FPS


def audio(video_len):
    parts, fl = [], []
    for i, (a, b, sp, *_) in enumerate(SEG):
        fl.append(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={sp}[a{i}]'); parts.append(f'[a{i}]')
    fl.append(''.join(parts) + f'concat=n={len(SEG)}:v=0:a=1,loudnorm=I=-18:TP=-2,afade=t=out:st={video_len - 0.8}:d=0.8,apad=pad_dur={END_DUR}[a]')
    dst = os.path.join(out, '_audio.m4a')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src_video, '-filter_complex', ';'.join(fl), '-map', '[a]', '-ar', '44100', '-c:a', 'aac', '-b:a', '160k', dst], check=True)
    return dst


for mode in ('vollbild', 'rahmen'):
    v, vlen = render(mode)
    a = audio(vlen)
    dst = os.path.join(out, f'reel_unboxing_geschenkbox_{mode}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', dst], check=True)
    os.remove(v); os.remove(a)
    print(dst)
