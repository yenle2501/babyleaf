"""Produkt-Reel Erstausstattung-Set «Hello Little Bear» aus dem KI-Clip der Nutzerin (06.11.2026).

Clip (960×960, KI): Neugeborenes im Teddy-Strampler des Sets. Nur 0.5–14.5 s verwendet, ab ca. 19 s steht im Clip ein
verschwommener KI-Text. Auf 9:16 zugeschnitten, langsamer Zoom, Text oben über den Kissen, dann Schlusskarte mit dem Set.
Musik «Christmas Lullaby» (Mixkit, lizenzfrei).

    python3 tools/make_reel_hello_little_bear.py
Ausgabe: posts/reels/hello-little-bear/reel_hello_little_bear_9x16.mp4 + _titelbild.jpg
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m
from make_coming_soon_schleife import gesperrt

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'reels', 'hello-little-bear')
CLIP = os.path.join(BASIS, 'original', 'clip.mp4')
SET_BILD = os.path.join(BASIS, 'original', 'set_praesentation.jpg')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'mixkit_michael-ramir_christmas-lullaby.mp3')
VON, BIS = 0.5, 14.5
T_ENDE, BLENDE = 3.8, 0.6
WEINROT = (98, 22, 30)

TEXTE = [(0.0, 6.6, ['Die ersten Tage', 'zu Hause …']),
         (7.0, BIS - VON, ['… und überall', 'kleine Teddys.'])]


def clip_frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(BIS - VON), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale=1920:1920:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(1920 * 1920 * 3)
        if len(b) < 1920 * 1920 * 3:
            break
        yield Image.frombuffer('RGB', (1920, 1920), b)


def text_oben(c, zeilen, alpha):
    """Dunkle Cormorant (kursiv) oben über den hellen Kissen, mit weichem hellem Schein."""
    if alpha <= 0:
        return c
    fo = m.f(m.SERIF_I, 96); lh = 104
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(glow)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        y = 330 + k * lh
        dg.text((W / 2, y), z, font=fo, fill=(255, 255, 255, int(230 * alpha)), anchor='mm', stroke_width=14, stroke_fill=(255, 255, 255, int(230 * alpha)))
        dt.text((W / 2, y), z, font=fo, fill=m.WALD + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    c.alpha_composite(tx)
    return c


def end_karte(t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.8)
    im = Image.open(SET_BILD).convert('RGB'); s = 900 / im.width * (0.97 + 0.03 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 760 - im.height // 2))
    d.text((W / 2, 250), 'Erstausstattung-Set', font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    a = m.ease((t - 0.3) / 0.7)
    d.text((W / 2, 1290), '«Hello Little Bear»', font=m.f(m.SERIF, 96), fill=m.WALD + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1380), '5 Teile: Strampler, Body, Mütze,', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1440), 'Fäustlinge und Lätzchen', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    a2 = m.ease((t - 0.8) / 0.7)
    d.text((W / 2, 1545), 'CHF 28.40', font=m.f(m.SERIF, 80), fill=WEINROT + (int(255 * a2),), anchor='mm')
    d.text((W / 2, 1640), 'sunnozy.ch/hello-little-bear', font=m.f(m.SERIF, 50), fill=m.WALD + (int(255 * a2),), anchor='mm')
    L = m.logo(190, (122, 108, 104)); L.putalpha(L.getchannel('A').point(lambda v: int(v * a2)))
    c.alpha_composite(L, ((W - L.width) // 2, 1705))
    return c


def main():
    os.makedirs(BASIS, exist_ok=True)
    t_clip = BIS - VON; n_clip = int(round(t_clip * FPS)); nb = int(BLENDE * FPS); n_ende = int(T_ENDE * FPS)
    pfad = os.path.join(BASIS, 'reel_hello_little_bear_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    ende0 = end_karte(0)
    for i, fr in enumerate(clip_frames()):
        if i >= n_clip:
            break
        t = i / FPS
        z = 1.0 + 0.12 * m.ease(t / t_clip)
        bw, bh = W / z, H / z; cx, cy = 0.47 * 1920, 0.5 * 1920
        c = fr.resize((W, H), Image.BICUBIC, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')
        for a0, a1, zeilen in TEXTE:
            al = m.ease((t - a0) / 0.6) * (1 - m.ease((t - (a1 - 0.5)) / 0.5)) if a0 > 0 else (1 - m.ease((t - (a1 - 0.5)) / 0.5))
            text_oben(c, zeilen, al)
        if i >= n_clip - nb:
            c = Image.blend(c, ende0, (i - (n_clip - nb)) / nb)
        if i == int(1.0 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    for j in range(n_ende):
        enc.stdin.write(end_karte(j / FPS).convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = t_clip + T_ENDE
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.6,afade=t=out:st={dauer - 1.8:.2f}:d=1.8,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    main()
