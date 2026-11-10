"""Produkt-Reel Erstausstattung-Set «Teddybär» aus dem KI-Video der Nutzerin (10.11.2026).

Clip (848×1056, 15 s, KI «imagine»): Baby mit Weihnachtsmütze im Teddy-Body des Sets, umarmt einen Plüschteddy.
Der Clip steht in voller Breite auf Creme, oben ein Feld für den Text, am Schluss eine Karte mit dem Set.
Der Original-Ton wird durch Musik ersetzt: «Christmas Lullaby» (Mixkit, lizenzfrei).

    python3 tools/make_reel_teddybaer_weihnachten.py
Ausgabe: posts/coming-soon/reels/teddybaer-weihnachten/reel_teddybaer_erstes_weihnachten_9x16.mp4 + _titelbild.jpg
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
P = os.path.join(m.POSTS, 'coming-soon')
BASIS = os.path.join(P, 'reels', 'teddybaer-weihnachten')
CLIP = os.path.join(BASIS, 'original', 'clip.mp4')
SET_BILD = os.path.join(P, 'photos', 'produktfotos-set-praesentation', 'ohne_logo', 'set_teddy_creme_quadratisch.jpg')
MUSIK = os.path.join(P, 'reels', 'musik', 'mixkit_michael-ramir_christmas-lullaby.mp3')
VON, BIS = 0.2, 14.9
T_ENDE, BLENDE = 3.8, 0.6
WEINROT = (98, 22, 30)
CW = W; CH = round(1056 * W / 848)      # Clip in voller Breite: 1080 × 1345
CY = 455                                # Oberkante des Clips; darüber steht der Text

TEXTE = [(0.0, 6.4, ['Das erste', 'Weihnachten …']),
         (6.8, BIS - VON, ['… mit dem liebsten', 'Teddy im Arm.'])]


def clip_frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(BIS - VON), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={2 * CW}:{2 * CH}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = 2 * CW * 2 * CH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (2 * CW, 2 * CH), b)


def maske():
    """Weicher Übergang vom Clip in das Creme oben und unten."""
    mk = Image.new('L', (CW, CH), 255); d = ImageDraw.Draw(mk)
    for y in range(60):
        d.line([(0, y), (CW, y)], fill=int(255 * y / 60))
        d.line([(0, CH - 1 - y), (CW, CH - 1 - y)], fill=int(255 * y / 60))
    return mk


def text_oben(c, zeilen, alpha):
    if alpha <= 0:
        return
    fo = m.f(m.SERIF_I, 92); lh = 104
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        dt.text((W / 2, 225 + k * lh), z, font=fo, fill=m.WALD + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(tx)


def end_karte(t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.8)
    im = Image.open(SET_BILD).convert('RGB'); s = 900 / im.width * (0.97 + 0.03 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 760 - im.height // 2))
    d.text((W / 2, 250), 'Erstausstattung-Set', font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    a = m.ease((t - 0.3) / 0.7)
    d.text((W / 2, 1290), '«Teddybär»', font=m.f(m.SERIF, 96), fill=m.WALD + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1380), '8 Teile: Strampler, Body mit Teddy,', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    d.text((W / 2, 1440), 'Decke, Mütze, Söckchen und mehr', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a),), anchor='mm')
    a2 = m.ease((t - 0.8) / 0.7)
    d.text((W / 2, 1545), 'CHF 30.40', font=m.f(m.SERIF, 80), fill=WEINROT + (int(255 * a2),), anchor='mm')
    d.text((W / 2, 1640), 'sunnozy.ch', font=m.f(m.SERIF, 50), fill=m.WALD + (int(255 * a2),), anchor='mm')
    L = m.logo(190, (122, 108, 104)); L.putalpha(L.getchannel('A').point(lambda v: int(v * a2)))
    c.alpha_composite(L, ((W - L.width) // 2, 1705))
    return c


def main():
    t_clip = BIS - VON; n_clip = int(round(t_clip * FPS)); nb = int(BLENDE * FPS); n_ende = int(T_ENDE * FPS)
    pfad = os.path.join(BASIS, 'reel_teddybaer_erstes_weihnachten_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    ende0 = end_karte(0); mk = maske()
    for i, fr in enumerate(clip_frames()):
        if i >= n_clip:
            break
        t = i / FPS
        z = 1.0 + 0.07 * m.ease(t / t_clip)                 # langsamer Zoom auf Baby und Body
        bw, bh = 2 * CW / z, 2 * CH / z; cx = CW
        cy = min(max(1.1 * CH, bh / 2), 2 * CH - bh / 2)   # Zoom leicht unter die Mitte (Body), nie über den Rand
        bild = fr.resize((CW, CH), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
        c = Image.new('RGBA', (W, H), m.CREME + (255,))
        c.paste(bild, (0, CY), mk)
        for a0, a1, zeilen in TEXTE:
            ein = 1.0 if a0 == 0 else m.ease((t - a0) / 0.6)
            text_oben(c, zeilen, ein * (1 - m.ease((t - (a1 - 0.5)) / 0.5)))
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
