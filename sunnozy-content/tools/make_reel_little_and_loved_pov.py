"""Reel Erstausstattung «Little and Loved» aus dem KI-Clip der Nutzerin (11.11.2026), Stil wie Hello Little Bear / Hello Spitze.

Clip (848×1056, 15 s, KI): Baby im rosa Gänse-Strampler des Sets, daneben das gefaltete Jäckchen mit Gänse-Stickerei.
Weil Baby und Jäckchen die ganze Breite füllen, steht der Clip in voller Breite (1080 × 1345) auf einer unscharfen,
vergrösserten Kopie desselben Bildes (wirkt randlos). Nur 0–9 s, danach wandert die Kamera vom Baby weg.
POV-Zeile in weisser Schreibmaschinenschrift am Anfang, Schluss-Text «little and loved 🤍» (Stickerei des Sets), kein Preis.

    python3 tools/make_reel_little_and_loved_pov.py [set|maedchen]
Ausgabe: posts/coming-soon/reels/little-and-loved/reel_little_and_loved_<variante>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageFilter
import make_coming_soon_reels as m
from make_reel_hello_spitze_morgen import emoji_text

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'coming-soon', 'reels', 'little-and-loved')
CLIP = os.path.join(BASIS, 'original', 'clip_bett.mp4')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
VON, BIS = 0.0, 9.0
CH = round(1056 * W / 848); CY = (H - CH) // 2
ENDE_AB = 6.4

VARIANTEN = {
    'set': (['POV: Alles passt zusammen,', 'sogar das Jäckchen ✨'], ['little and loved 🤍']),
    'maedchen': (['POV: Ihr erfahrt,', 'es wird ein Mädchen ✨'], ['little and loved 🤍']),
}


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(BIS - VON), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={W}:{CH}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * CH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        fr = Image.frombuffer('RGB', (W, CH), b)
        s = H / CH; g = fr.resize((round(W * s), H), Image.BILINEAR)
        g = g.crop(((g.width - W) // 2, 0, (g.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(28))
        g = Image.blend(g, Image.new('RGB', (W, H), (250, 247, 244)), 0.15)
        g.paste(fr, (0, CY))
        yield g


def reel(name):
    oben, unten = VARIANTEN[name]
    e1, e2 = emoji_text(oben), emoji_text(unten)
    dauer = BIS - VON
    pfad = os.path.join(BASIS, f'reel_little_and_loved_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, fr in enumerate(frames()):
        t = i / FPS; c = fr.convert('RGBA')
        for ebene, a in ((e1, 1 - m.ease((t - 2.8) / 0.4)), (e2, m.ease((t - ENDE_AB) / 0.5))):
            if a > 0:
                e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.0:.2f}:d=1.0,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
