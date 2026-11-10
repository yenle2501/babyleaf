"""Reels «Hello Little Bear» mit Hook-Texten, ohne Preis (10.11.2026).

Clip (848×1072, 15 s, KI): Neugeborenes wach auf weissem Laken, im Teddy-Strampler mit Reissverschluss und der Mütze
mit Bärenöhrchen aus dem Set. Langsamer Kamera-Zoom ist schon im Clip.
Zwei Varianten zum A/B-Test (Analyse: posts/coming-soon/reels/hello-little-bear/HOOKS.md):
  winter   – POV: Dein Baby kommt im Winter
  freundin – Deine Freundin bekommt bald ein Baby?

    python3 tools/make_reel_hello_little_bear_hook.py [winter|freundin]
Ausgabe: posts/coming-soon/reels/hello-little-bear/reel_hello_little_bear_<variante>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageDraw
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
P = os.path.join(m.POSTS, 'coming-soon')
BASIS = os.path.join(P, 'reels', 'hello-little-bear')
CLIP = os.path.join(BASIS, 'original', 'clip_bett.mp4')
SET_BILD = os.path.join(P, 'photos', 'hello-little-bear', 'original', 'set_praesentation.jpg')
MUSIK = os.path.join(P, 'reels', 'musik', 'mixkit_michael-ramir_christmas-lullaby.mp3')
VON, BIS = 0.0, 12.0
T_ENDE, BLENDE = 3.2, 0.5
CW = W; CH = round(1072 * W / 848)      # 1080 × 1365
CY = 440

DETAIL = ['Um 3 Uhr nachts:', 'Reissverschluss statt Knöpfe']
VARIANTEN = {
    'winter': {'texte': [(0.0, 4.0, ['POV: Dein Baby', 'kommt im Winter']),
                         (4.3, 8.0, ['… und das erste Outfit', 'liegt schon bereit.']),
                         (8.3, 12.0, DETAIL)],
               'cta': 'Link in der Bio'},
    'freundin': {'texte': [(0.0, 4.0, ['Deine Freundin bekommt', 'bald ein Baby?']),
                           (4.3, 8.0, ['Schick ihr das.', 'Mit Bärenöhrchen.']),
                           (8.3, 12.0, DETAIL)],
                 'cta': 'Schick das Deiner Freundin'},
}


def clip_frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(BIS - VON), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={CW}:{CH}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = CW * CH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (CW, CH), b)


def maske():
    mk = Image.new('L', (CW, CH), 255); d = ImageDraw.Draw(mk)
    for y in range(60):
        d.line([(0, y), (CW, y)], fill=int(255 * y / 60))
        d.line([(0, CH - 1 - y), (CW, CH - 1 - y)], fill=int(255 * y / 60))
    return mk


def text_oben(c, zeilen, alpha):
    if alpha <= 0:
        return
    g = 88
    while g > 56 and max(ImageDraw.Draw(c).textlength(z, font=m.f(m.SERIF_I, g)) for z in zeilen) > 900:
        g -= 2
    fo = m.f(m.SERIF_I, g); lh = g * 1.13
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        dt.text((W / 2, 215 + k * lh), z, font=fo, fill=m.WALD + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(tx)


def end_karte(t, cta):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.8)
    im = Image.open(SET_BILD).convert('RGB'); s = 900 / im.width * (0.97 + 0.03 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 760 - im.height // 2))
    d.text((W / 2, 250), 'Erstausstattung-Set', font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    a = m.ease((t - 0.3) / 0.7)
    d.text((W / 2, 1290), '«Hello Little Bear»', font=m.f(m.SERIF, 96), fill=m.WALD + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1380), 'Strampler, Body, Mütze mit Öhrchen,', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1440), 'Fäustlinge und Lätzchen', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    a2 = m.ease((t - 0.8) / 0.7)
    d.text((W / 2, 1560), cta, font=m.f(m.SERIF, 62), fill=m.WALD + (int(255 * a2),), anchor='mm')
    L = m.logo(190, (122, 108, 104)); L.putalpha(L.getchannel('A').point(lambda v: int(v * a2)))
    c.alpha_composite(L, ((W - L.width) // 2, 1680))
    return c


def reel(name):
    v = VARIANTEN[name]
    t_clip = BIS - VON; n_clip = int(round(t_clip * FPS)); nb = int(BLENDE * FPS); n_ende = int(T_ENDE * FPS)
    pfad = os.path.join(BASIS, f'reel_hello_little_bear_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    ende0 = end_karte(0, v['cta']); mk = maske()
    for i, fr in enumerate(clip_frames()):
        if i >= n_clip:
            break
        t = i / FPS
        c = Image.new('RGBA', (W, H), m.CREME + (255,))
        c.paste(fr, (0, CY), mk)
        for a0, a1, zeilen in v['texte']:
            ein = 1.0 if a0 == 0 else m.ease((t - a0) / 0.4)
            aus = 1.0 if a1 >= t_clip else 1 - m.ease((t - (a1 - 0.3)) / 0.3)
            text_oben(c, zeilen, ein * aus)
        if i >= n_clip - nb:
            c = Image.blend(c, ende0, (i - (n_clip - nb)) / nb)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    for j in range(n_ende):
        enc.stdin.write(end_karte(j / FPS, v['cta']).convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = t_clip + T_ENDE
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.4,afade=t=out:st={dauer - 1.5:.2f}:d=1.5,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
