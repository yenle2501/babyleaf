"""Reel «Outfits der Woche» im Trend-Format (Vorlage der Nutzerin, 25.10.2026): Baby von oben, pro Wochentag ein
Outfit, schnelle Schnitte (ca. 1,2 s), Wochentag gross in der Mitte, leichte Handkamera-Bewegung, Loop zurück zu Montag.

    python3 tools/make_reel_outfits_woche.py

Bilder: Baby-Fotos im echten Handy-Stil aus posts/baby-photos (Erstausstattungs-Sets, die im Shop sind).
Schrift: Cormorant Garamond kursiv wie die anderen Reels (keine Schreibschrift).
Ausgabe: posts/reels/im-shop/reel_outfits_der_woche_9x16.mp4 + _titelbild.jpg
"""
import os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = 1080, 1920, 30
BP = os.path.join(m.POSTS, 'baby-photos')
OUT = os.path.join(m.POSTS, 'reels', 'im-shop')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
TAGE = [('Montag', 'baby_echt_erstausstattung_teddybaer.jpg'),
        ('Dienstag', 'baby_echt_erstausstattung_hello_world.jpg'),
        ('Mittwoch', 'baby_echt_erstausstattung_little_and_loved.jpg'),
        ('Donnerstag', 'baby_echt_erstausstattung_princess.jpg'),
        ('Freitag', 'baby_echt_erstausstattung_hello_little_bear.jpg')]
DAUER = 1.25          # Sekunden pro Tag
ZOOM0 = 1.05          # Grundzoom, damit die Handbewegung keine Ränder zeigt


def vorbereiten(p):
    im = Image.open(p).convert('RGB')
    s = max(W / im.width, H / im.height) * ZOOM0
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def bild(im, t, seed):
    """Leichtes Wackeln wie aus der Hand + langsames Ranzoomen."""
    z = 1 + 0.035 * t / DAUER
    dx = 9 * math.sin(2 * math.pi * (0.7 * t + seed)) + 4 * math.sin(2 * math.pi * (1.9 * t + seed * 2))
    dy = 7 * math.cos(2 * math.pi * (0.5 * t + seed)) + 3 * math.sin(2 * math.pi * (2.3 * t + seed))
    w, h = W / z, H / z
    cx, cy = im.width / 2 + dx, im.height * 0.56 + dy
    cx = min(max(cx, w / 2), im.width - w / 2); cy = min(max(cy, h / 2), im.height - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return im.resize((W, H), Image.LANCZOS, box=box)


def tag_text(c, text):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = m.f(m.SERIF_I, 132)
    d.text((W / 2 + 3, H * 0.6 + 4), text, font=f, fill=(0, 0, 0, 150), anchor='mm')
    sh = lay.filter(ImageFilter.GaussianBlur(9))
    d2 = ImageDraw.Draw(sh); d2.text((W / 2, H * 0.6), text, font=f, fill=(255, 255, 255, 250), anchor='mm', stroke_width=1, stroke_fill=(255, 255, 255, 250))
    return Image.alpha_composite(c.convert('RGBA'), sh)


def titel(c, a):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = m.f(m.SERIF_I, 84)
    d.text((W / 2 + 3, 330 + 3), 'Outfits der Woche', font=f, fill=(0, 0, 0, int(140 * a)), anchor='mm')
    lay = lay.filter(ImageFilter.GaussianBlur(8)); d = ImageDraw.Draw(lay)
    d.text((W / 2, 330), 'Outfits der Woche', font=f, fill=(255, 255, 255, int(250 * a)), anchor='mm', stroke_width=1, stroke_fill=(255, 255, 255, int(250 * a)))
    return Image.alpha_composite(c, lay)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    bilder = [vorbereiten(os.path.join(BP, p)) for _, p in TAGE]
    n_tag = int(DAUER * FPS); n = n_tag * len(TAGE)
    pfad = os.path.join(OUT, 'reel_outfits_der_woche_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        k, j = divmod(i, n_tag); t = j / FPS
        c = tag_text(bild(bilder[k], t, k * 0.37), TAGE[k][0])
        if k == 0:                                   # Titel nur am Anfang, blendet aus
            c = titel(c, max(0.0, min(1.0, (DAUER - t) / 0.4)))
        fr = c.convert('RGB')
        if i == int(0.5 * FPS):
            fr.save(os.path.join(OUT, 'reel_outfits_der_woche_9x16_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    d = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '30', '-i', MUSIK, '-t', f'{d:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={d - 0.6:.2f}:d=0.6,volume=0.85', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(pfad, f'{d:.1f} s')
