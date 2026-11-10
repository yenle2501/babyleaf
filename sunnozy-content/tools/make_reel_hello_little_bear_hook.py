"""Reels «Hello Little Bear» im Stil der Vorlage der Nutzerin (10.11.2026): POV-Text in Schreibmaschinenschrift.

Vorlage (Bildschirmaufnahme, fremdes Reel, nur der Stil ist übernommen): Video in voller Grösse, eine kurze POV-Zeile
in weisser Schreibmaschinenschrift mit ✨ mitten im Bild. Der Text steht nur am Anfang und kommt zum Loop am Ende zurück,
dazwischen läuft nur das Video. Es gibt keine Schlusskarte und keinen Preis.

Clip (848×1072, 15 s, KI): Neugeborenes wach auf weissem Laken, im Teddy-Strampler mit Reissverschluss und der Mütze
mit Bärenöhrchen aus dem Set. Die Kamera zoomt langsam heran.
Schrift: Courier Prime (OFL, fonts/courierprime.ttf). Musik: «Christmas Lullaby» (Mixkit, lizenzfrei).

    python3 tools/make_reel_hello_little_bear_hook.py [winter|gotti]
Ausgabe: posts/coming-soon/reels/hello-little-bear/reel_hello_little_bear_<variante>_9x16.mp4 + _titelbild.jpg
Analyse und Captions: posts/coming-soon/reels/hello-little-bear/HOOKS.md
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
P = os.path.join(m.POSTS, 'coming-soon')
BASIS = os.path.join(P, 'reels', 'hello-little-bear')
CLIP = os.path.join(BASIS, 'original', 'clip_bett.mp4')
MUSIK = os.path.join(P, 'reels', 'musik', 'mixkit_michael-ramir_christmas-lullaby.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
VON, BIS = 0.0, 11.0
TEXT_BIS, LOOP_AB = 3.2, 9.6            # Text sichtbar 0–3.2 s und wieder ab 9.6 s (Loop)
TEXT_Y = 930

VARIANTEN = {
    'winter': ['POV: Dein Baby kommt', 'im Winter ✨'],
    'gotti': ['POV: Du wirst bald Gotti', 'und das Geschenk ist schon da ✨'],
}


def clip_frames():
    sw = round(848 * H / 1072)           # auf volle Höhe skalieren, mittig auf 1080 Breite zuschneiden
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(VON), '-t', str(BIS - VON), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, H), b)


def emoji(zeichen, hoehe):
    fo = ImageFont.truetype(EMOJI, 109)
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((70, 70), zeichen, font=fo, embedded_color=True, anchor='mm')
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * hoehe / im.height), hoehe), Image.LANCZOS)


def text_ebene(zeilen):
    """Weisse Schreibmaschinenschrift mit weichem Schatten (lesbar auf hellem Stoff), ✨ als Farb-Emoji."""
    fo = ImageFont.truetype(SCHRIFT, 50); lh = 60
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    schatten = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(schatten)
    sp = emoji('✨', 44)
    for k, z in enumerate(zeilen):
        rein = z.replace(' ✨', '')
        breite = d.textlength(rein, font=fo) + (sp.width + 14 if '✨' in z else 0)
        x0 = (W - breite) / 2; y = TEXT_Y + k * lh
        ds.text((x0 + 2, y + 3), rein, font=fo, fill=150, anchor='lm')
        d.text((x0, y), rein, font=fo, fill=(255, 255, 255, 255), anchor='lm')
        if '✨' in z:
            tx.alpha_composite(sp, (int(x0 + breite - sp.width), int(y - sp.height / 2 - 4)))
    schatten = schatten.filter(ImageFilter.GaussianBlur(6))
    ebene = Image.new('RGBA', (W, H), (40, 30, 25, 0)); ebene.putalpha(schatten)
    ebene.alpha_composite(tx)
    return ebene


def reel(name):
    ebene = text_ebene(VARIANTEN[name])
    dauer = BIS - VON; n = int(round(dauer * FPS))
    pfad = os.path.join(BASIS, f'reel_hello_little_bear_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, fr in enumerate(clip_frames()):
        if i >= n:
            break
        t = i / FPS
        a = 1 - m.ease((t - (TEXT_BIS - 0.4)) / 0.4) if t < LOOP_AB else m.ease((t - LOOP_AB) / 0.4)
        c = fr.convert('RGBA')
        if a > 0:
            e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
            c.alpha_composite(e)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
