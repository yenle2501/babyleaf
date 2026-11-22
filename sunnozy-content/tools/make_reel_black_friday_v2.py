"""Black-Friday-Reel v2 (19.11.2026, Nutzerin wollte es anders): Video in voller Grösse, Stil wie die Baby-Reels.

Zwei Varianten aus dem gleichen Clip (Hand hängt 5 Bodys über die sunnozy-Tüte):
  pov    : «POV: Black Friday bei sunnozy 🖤»
  gotti  : «Schick das der Gotti: jetzt 10 % auf alles 🎁» (Empfänger zum Teilen)
Hook oben in weisser Schreibmaschinenschrift (tippt sich in 0.5 s ein), Punch-in-Zoom, Text am Ende zum Loop zurück.
Dazu ein runder schwarzer Sticker «-10 % auf alles · 16.–30.11» rechts unten neben dem Body, poppt bei 0.6 s auf und bleibt stehen.
Kein Code (in Shopify noch kein Black-Friday-Rabatt angelegt).

    python3 tools/make_reel_black_friday_v2.py [pov|gotti]
"""
import os, sys, glob, subprocess
from PIL import Image, ImageDraw, ImageFont
import make_coming_soon_reels as m
import make_baby_reels as b
from endfolie import anhaengen, SHOP

W, H, FPS = b.W, b.H, b.FPS
CLIP = glob.glob(os.path.join(b.VID, 'Hands_changing_baby_bodysuits_in*_202608311248.mp4'))[0]
OUT = os.path.join(m.POSTS, 'baby-reels', 'black-friday')
DAUER = 10.0
TEXT_BIS, LOOP_AB = 3.0, 8.4
b.TEXT_Y = 190
VARIANTEN = {
    'pov': (['POV: Black Friday', 'bei sunnozy'], '🖤'),
    'gotti': (['Schick das der Gotti:', 'jetzt 10 % auf alles'], '🎁'),
}


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-t', str(DAUER), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},hqdn3d=1.2:1.2:3:3,eq=contrast=1.05:saturation=1.03,cas=0.3,scale={W}:{H}:flags=lanczos',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield Image.frombuffer('RGB', (W, H), buf)


def sticker():
    r = 150; im = Image.new('RGBA', (2 * r + 20, 2 * r + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 10, 10 + 2 * r, 10 + 2 * r), fill=(24, 21, 19, 245))
    d.ellipse((22, 22, 2 * r - 2, 2 * r - 2), outline=(255, 255, 255, 200), width=3)
    c = r + 10
    d.text((c, c - 66), 'BLACK FRIDAY', font=ImageFont.truetype(b.SCHRIFT, 22), fill=(255, 255, 255, 255), anchor='mm')
    d.text((c, c - 10), '-10 %', font=ImageFont.truetype(b.SCHRIFT, 62), fill=(255, 255, 255, 255), anchor='mm')
    d.text((c, c + 46), 'auf alles', font=ImageFont.truetype(b.SCHRIFT, 26), fill=(255, 255, 255, 255), anchor='mm')
    d.text((c, c + 86), '16.–30.11', font=ImageFont.truetype(b.SCHRIFT, 22), fill=(255, 255, 255, 200), anchor='mm')
    return im


def main(variante):
    zeilen, emo = VARIANTEN[variante]
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_black_friday_{variante}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    voll = b.text_ebene(zeilen, emo); st = sticker(); tipp = {}
    gesamt = sum(len(z) for z in zeilen)
    SX, SY = W - st.width - 24, 1000
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', tmp], stdin=subprocess.PIPE)
    i = 0
    for i, fr in enumerate(frames()):
        t = i / FPS
        c = b.punch(fr, t).convert('RGBA')
        if t < b.TIPP_BIS:
            k = max(1, int(gesamt * t / b.TIPP_BIS) + 1)
            if k not in tipp:
                tipp[k] = b.text_ebene(b.teil(zeilen, k), emo, mit_emoji=False, voll=zeilen)
            c.alpha_composite(tipp[k])
        else:
            a = 1 - m.ease((t - (TEXT_BIS - 0.4)) / 0.4) if t < LOOP_AB else m.ease((t - LOOP_AB) / 0.3)
            if a > 0:
                e = voll if a >= 1 else voll.copy()
                if a < 1:
                    e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
        if t >= 0.6:                                   # Sticker poppt auf (leicht überschiessend) und bleibt
            s = min(1.0, (t - 0.6) / 0.3); f = 0.6 + 0.5 * m.ease(s) - 0.1 * max(0, s - 0.6) / 0.4 * (1 if s < 1 else 0)
            f = 1.0 if s >= 1 else f
            sw = max(1, round(st.width * f))
            sx = st.resize((sw, sw), Image.LANCZOS)
            c.alpha_composite(sx, (SX + (st.width - sw) // 2, SY + (st.height - sw) // 2))
        if i == int(1.0 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        if i == int(7.6 * FPS):
            fr.crop((0, 300, W, 300 + W)).save('/tmp/bf_endfolie.jpg', quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = (i + 1) / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', b.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', 'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    anhaengen(pfad, '/tmp/bf_endfolie.jpg', 'Black Friday · 10 % auf alles', '16.–30.11 · im ganzen Shop', SHOP)


if __name__ == '__main__':
    for v in (sys.argv[1:] or list(VARIANTEN)):
        main(v)
