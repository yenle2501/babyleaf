"""Reel «Outfits der Woche» im Trend-Format (Vorlage der Nutzerin, 25.10.2026): Baby von oben, pro Wochentag ein
Outfit, schnelle Schnitte (ca. 1,2 s), Wochentag gross in der Mitte, leichte Handkamera-Bewegung, Loop zurück zu Montag.

    python3 tools/make_reel_outfits_woche.py

Clips: die Grok-Babyvideos der Nutzerin aus posts/videos-baby (*_bearbeitet.mp4), je 1,1 s pro Tag.
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
VB = os.path.join(m.POSTS, 'videos-baby')
# (Tag, Clip, Start in s, Bildmitte x)
TAGE = [('Montag', 'teddy_creme_a', 2.0, 0.5),
        ('Dienstag', 'princess_rosa_a', 1.0, 0.5),
        ('Mittwoch', 'gaensebluemchen_d', 2.5, 0.5),
        ('Donnerstag', 'best_family_c', 1.0, 0.5),
        ('Freitag', 'bauernhof_b', 0.5, 0.5),
        ('Samstag', 'born_in_2027_rosa_b', 1.0, 0.55),
        ('Sonntag', 'eisbaer_taupe_b', 1.5, 0.52)]
DAUER = 1.1           # Sekunden pro Tag


def bild(frames, i, fx, t):
    """9:16-Ausschnitt aus dem Clip-Frame, langsam leicht reinzoomen, nachgeschärft."""
    import make_reels_videos_baby as rv
    fr = frames[min(i, len(frames) - 1)]
    return rv.ausschnitt(fr, 1.0 + 0.05 * t / DAUER, fx, 0.45).convert('RGB')


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
    clips = [m.clip_frames(os.path.join(VB, c + '_bearbeitet.mp4'), v, v + DAUER + 0.2) for _, c, v, _ in TAGE]
    n_tag = int(DAUER * FPS); n = n_tag * len(TAGE)
    pfad = os.path.join(OUT, 'reel_outfits_der_woche_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        k, j = divmod(i, n_tag); t = j / FPS
        c = tag_text(bild(clips[k], j, TAGE[k][3], t), TAGE[k][0])
        if k == 0:                                   # Titel nur am Anfang, blendet aus
            c = titel(c, max(0.0, min(1.0, (DAUER - t) / 0.4)))
        fr = c.convert('RGB')
        if i == int(0.5 * FPS):
            fr.save(os.path.join(OUT, 'reel_outfits_der_woche_9x16_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    d = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '18', '-i', MUSIK, '-t', f'{d:.2f}',
                    '-af', f'loudnorm=I=-12:TP=-1:LRA=11,afade=t=in:d=0.15,afade=t=out:st={d - 0.4:.2f}:d=0.4,aresample=44100', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(pfad, f'{d:.1f} s')
