"""Black-Friday-Reel: 10 % auf alles (19.11.2026).

Clip: posts/baby-videos/Hands_changing_baby_bodysuits_in…_202608311248.mp4 (Hand hängt 5 Bodys über die sunnozy-Tüte).
Stil wie die Baby-Reels v2: Punch-in-Zoom am Anfang, Hook tippt sich in 0.5 s ein (Courier Prime).
Das Angebot bleibt die ganze Zeit stehen (Sale-Reel). Weil die Bodys im Clip ganz oben hängen, läuft das Video etwas
kleiner auf schwarzem Grund (Black-Friday-Look), das Angebot steht oben auf Schwarz und verdeckt nichts.
Endfolie: Standbild Tüte + Body, «Black Friday · 10 % auf alles», Link in der Bio. Musik: Alex Morgan.
Kein Rabattcode im Video, weil in Shopify noch kein Black-Friday-Rabatt angelegt ist (Stand 19.11.2026).

    python3 tools/make_reel_black_friday.py
Ausgabe: posts/baby-reels/black-friday/reel_black_friday_10_prozent_9x16.mp4 + _titelbild.jpg
"""
import os, glob, subprocess
from PIL import Image, ImageDraw, ImageFont
import make_coming_soon_reels as m
import make_baby_reels as b
from endfolie import anhaengen, SHOP

W, H, FPS = b.W, b.H, b.FPS
CLIP = glob.glob(os.path.join(b.VID, 'Hands_changing_baby_bodysuits_in*_202608311248.mp4'))[0]
OUT = os.path.join(m.POSTS, 'baby-reels', 'black-friday')
DAUER = 10.0
SCHWARZ = (24, 21, 19)
VH = 1540; VW = round(VH * 9 / 16 / 2) * 2; VY = H - VH - 40
HELL_GRADE = 'hqdn3d=1.2:1.2:3:3,eq=contrast=1.05:saturation=1.03,cas=0.3'


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-t', str(DAUER), '-i', CLIP, '-map', '0:v:0',
                          '-vf', f'fps={FPS},{HELL_GRADE},scale={VW}:{VH}:flags=lanczos',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = VW * VH * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield Image.frombuffer('RGB', (VW, VH), buf)


def punch(fr, t):
    if t >= 0.5:
        return fr
    f = 1 + 0.12 * (1 - m.ease(t / 0.5)); w, h = round(VW * f), round(VH * f)
    return fr.resize((w, h), Image.BILINEAR).crop(((w - VW) // 2, (h - VH) // 2, (w - VW) // 2 + VW, (h - VH) // 2 + VH))


def leinwand(fr):
    c = Image.new('RGB', (W, H), SCHWARZ)
    maske = Image.new('L', (VW, VH), 0); ImageDraw.Draw(maske).rounded_rectangle((0, 0, VW - 1, VH - 1), radius=28, fill=255)
    c.paste(fr, ((W - VW) // 2, VY), maske)
    return c


def ebene(k_pill=99, k_gross=99, k_klein=99, emoji=True):
    """Schwarze Pille «BLACK FRIDAY», darunter gross «10 % auf alles», klein «im ganzen Shop». k_* = sichtbare Zeichen (Schreibmaschine)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pill, gross, klein = 'BLACK FRIDAY', '10 % auf alles', 'im ganzen sunnozy-Shop'
    fp = ImageFont.truetype(b.SCHRIFT, 50); fg = ImageFont.truetype(b.SCHRIFT, 92); fk = ImageFont.truetype(b.SCHRIFT, 44)
    pw = d.textlength(pill, font=fp)
    d.rounded_rectangle((W / 2 - pw / 2 - 38, 120 - 44, W / 2 + pw / 2 + 38, 120 + 44), radius=44, fill=(255, 255, 255, 255))
    d.text((W / 2 - pw / 2, 122), pill[:k_pill], font=fp, fill=SCHWARZ + (255,), anchor='lm')
    sp = b.emoji('🤍', 64)
    gw = d.textlength(gross, font=fg) + sp.width + 18
    d.text((W / 2 - gw / 2, 232), gross[:k_gross], font=fg, fill=(255, 255, 255, 255), anchor='lm')
    kw = d.textlength(klein, font=fk)
    d.text((W / 2 - kw / 2, 318), klein[:k_klein], font=fk, fill=(235, 228, 220, 255), anchor='lm')
    if emoji:
        im.alpha_composite(sp, (int(W / 2 + gw / 2 - sp.width), int(232 - sp.height / 2 - 4)))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, 'reel_black_friday_10_prozent_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    voll = ebene()
    gesamt = len('BLACK FRIDAY') + len('10 % auf alles') + len('im ganzen sunnozy-Shop')
    tipp = {}
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', tmp], stdin=subprocess.PIPE)
    i = 0
    for i, fr in enumerate(frames()):
        t = i / FPS
        c = leinwand(punch(fr, t)).convert('RGBA')
        if t < 0.6:
            k = max(1, int(gesamt * t / 0.6) + 1)
            if k not in tipp:
                a, rest = min(k, 12), max(0, k - 12)
                g, rest2 = min(rest, 14), max(0, rest - 14)
                tipp[k] = ebene(a, g, rest2, emoji=False)
            c.alpha_composite(tipp[k])
        else:
            c.alpha_composite(voll)
        if i == int(1.0 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        if i == int(7.6 * FPS):
            # Standbild für die Endfolie: Tüte mit Body, quadratisch
            fr.crop((0, 260, VW, 260 + VW)).save('/tmp/bf_endfolie.jpg', quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = (i + 1) / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', b.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', 'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    anhaengen(pfad, '/tmp/bf_endfolie.jpg', 'Black Friday · 10 % auf alles', 'im ganzen Shop', SHOP)


if __name__ == '__main__':
    main()
