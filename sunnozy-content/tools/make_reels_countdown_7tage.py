"""Countdown-Reels «Coming soon» für 7 Tage, nach der Pinterest-Vorlage der Nutzerin (27.10.2026):
verschwommene Clips im Hintergrund, mittig «Coming soon» mit Countdown Tage : Stunden : Minuten, unten das Logo.

    python3 tools/make_reels_countdown_7tage.py        # alle 7 Tage
    python3 tools/make_reels_countdown_7tage.py 3      # nur «noch 3 Tage»

Pro Tag ein Reel (Tag 7 zuerst posten, Tag 1 am Vortag des Starts). Hintergrund: Grok-Babyclips der
Coming-soon-Sets aus posts/videos-baby, stark weichgezeichnet (nur Farben und Bewegung, keine Details).
Kein Preis, keine Schreibschrift (Nunito Sans), Musik Alex Morgan (Pixabay).
Ausgabe: posts/reels/coming-soon/countdown/reel_countdown_noch_<n>_tage_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = 1080, 1920, 30
VB = os.path.join(m.POSTS, 'videos-baby')
OUT = os.path.join(m.POSTS, 'reels', 'coming-soon', 'countdown')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'alex-morgan_heartwarming-story.mp3')
SCHNITT = 1.3                       # Sekunden pro Clip
CLIPS = {                           # nur Coming-soon-Sets, ohne schlafende Babys
    7: ['born_in_2027_blau_a', 'gaensebluemchen_d', 'eisbaer_taupe_b', 'best_family_c', 'bauernhof_b', 'little_princess_krone_f', 'born_in_2027_rosa_b'],
    6: ['hase_rosa_a', 'dino_cool_dude_a', 'gaensebluemchen_beautiful_c', 'hund_creme_a', 'love_dad_mom_a', 'lila_hase_a', 'best_family_a'],
    5: ['little_princess_krone_a', 'bauernhof_a', 'strampler_kaetzchen_tulpen_a', 'eisbaer_taupe_a', 'blumenwiese_a', 'born_in_2027_rosa_a', 'gaensebluemchen_a'],
    4: ['best_family_b', 'hase_rosa_b', 'gaensebluemchen_beautiful_a', 'strampler_blumen_hase_a', 'hund_creme_b', 'little_princess_krone_b', 'born_in_2027_blau_a'],
    3: ['gaensebluemchen_b', 'lila_hase_b', 'bauernhof_b', 'blumenwiese_b', 'little_princess_krone_c', 'eisbaer_taupe_b', 'best_family_c'],
    2: ['hase_rosa_c', 'gaensebluemchen_beautiful_b', 'born_in_2027_rosa_b', 'dino_cool_dude_a', 'gaensebluemchen_c', 'little_princess_krone_e', 'bauernhof_a'],
    1: ['born_in_2027_blau_a', 'best_family_c', 'gaensebluemchen_d', 'eisbaer_taupe_b', 'hase_rosa_a', 'little_princess_krone_f', 'born_in_2027_rosa_b'],
}
WEISS = (255, 255, 255)


def dauer(pfad):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', pfad],
                                capture_output=True, text=True).stdout.strip())


def hintergrund(fr, t):
    """9:16 füllen, langsam reinzoomen, stark weichzeichnen und leicht abdunkeln (wie die Vorlage)."""
    s = H / fr.height * (1.08 + 0.04 * t / SCHNITT)
    bw, bh = W / s, H / s
    cx, cy = fr.width / 2, fr.height / 2
    klein = fr.resize((W // 3, H // 3), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    klein = klein.filter(ImageFilter.GaussianBlur(5))
    b = klein.resize((W, H), Image.BICUBIC)
    return Image.blend(b, Image.new('RGB', (W, H), (20, 16, 14)), 0.22)


def text_ebene(n):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    def mitte(y, txt, font, sp=0):
        if sp:
            breite = sum(d.textlength(c, font=font) for c in txt) + sp * (len(txt) - 1)
            x = (W - breite) / 2
            for c in txt:
                d.text((x, y), c, font=font, fill=WEISS + (255,), anchor='ls'); x += d.textlength(c, font=font) + sp
        else:
            d.text((W / 2, y), txt, font=font, fill=WEISS + (255,), anchor='ms')
    mitte(640, 'NEUE SETS', m.f('nunitosans-800.ttf', 40), sp=6)
    f_gross = m.f('nunitosans-800.ttf', 150)
    mitte(800, 'COMING', f_gross); mitte(950, 'SOON', f_gross)
    f_zahl = m.f('nunitosans-700.ttf', 118); f_lab = m.f('nunitosans-600.ttf', 26)
    xs = [W / 2 - 300, W / 2, W / 2 + 300]
    for x, z, lab in zip(xs, [f'{n:02d}', '00', '00'], ['TAGE', 'STUNDEN', 'MINUTEN']):
        d.text((x, 1135), z, font=f_zahl, fill=WEISS + (255,), anchor='ms')
        d.text((x, 1185), lab, font=f_lab, fill=WEISS + (235,), anchor='ms')
    for x in [W / 2 - 150, W / 2 + 150]:
        d.text((x, 1125), ':', font=f_zahl, fill=WEISS + (255,), anchor='ms')
    L = m.logo(250, WEISS); lay.alpha_composite(L, ((W - L.width) // 2, 1640))
    schatten = Image.new('RGBA', (W, H), (0, 0, 0, 0)); schatten.putalpha(lay.getchannel('A').point(lambda a: a * 0.3))
    schatten = schatten.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(schatten, lay)


def reel(n):
    os.makedirs(OUT, exist_ok=True)
    clips = []
    for c in CLIPS[n]:
        p = os.path.join(VB, c + '_bearbeitet.mp4'); start = min(1.2, max(0.0, dauer(p) - SCHNITT - 0.2))
        clips.append(m.clip_frames(p, start, start + SCHNITT + 0.1))
    txt = text_ebene(n)
    n_seg = int(SCHNITT * FPS); total = n_seg * len(clips)
    pfad = os.path.join(OUT, f'reel_countdown_noch_{n}_tage_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(total):
        k, j = divmod(i, n_seg); fr = clips[k][min(j, len(clips[k]) - 1)]
        c = Image.alpha_composite(hintergrund(fr, j / FPS).convert('RGBA'), txt).convert('RGB')
        if i == int(0.4 * FPS):
            c.save(pfad.replace('_9x16.mp4', '_9x16_titelbild.jpg'), quality=92)
        enc.stdin.write(c.tobytes())
    enc.stdin.close(); enc.wait()
    d = total / FPS; ss = 8 + 6 * (7 - n)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ss), '-i', MUSIK, '-t', f'{d:.2f}',
                    '-af', f'loudnorm=I=-12:TP=-1:LRA=11,afade=t=in:d=0.3,afade=t=out:st={d - 0.6:.2f}:d=0.6,aresample=44100',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(pfad, f'{d:.1f} s')


if __name__ == '__main__':
    for n in ([int(a) for a in sys.argv[1:]] or range(7, 0, -1)):
        reel(n)
