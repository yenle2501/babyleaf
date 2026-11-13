"""Zwei Reels «Hello Little Bear» nach der Viral-Analyse der Nutzerin (13.11.2026, posts/content-plan/viral-analyse/).

  babyfieber  – «Warnung: Babyfieber-Gefahr 🥹»: ein Take, wachendes Neugeborenes, 9 s Loop (Regeln 2, 3, 4)
  was-ist-drin – «Was ist im Set?»: Teil für Teil, am Schluss alle 5 Teile im Raster (leer → voll),
                 «Preis? Schreib PREIS in die Kommentare» statt Preis (Regeln 4, 5)
Schrift Courier Prime (Schreibmaschine) wie die bisherigen POV-Reels. Musik lizenzfrei (siehe musik/README.md).

    python3 tools/make_reel_viral_hlb.py [babyfieber|was-ist-drin]
Ausgabe: posts/coming-soon/reels/hello-little-bear/reel_hello_little_bear_<name>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_reel_hello_little_bear_hook as hk

W, H, FPS = m.W, m.H, 30
P = os.path.join(m.POSTS, 'coming-soon')
BASIS = os.path.join(P, 'reels', 'hello-little-bear')
TEILE = os.path.join(P, 'photos', 'marktplatz-galaxus-amazon', 'einzelteile', 'set_little_bear')
MUSIK = os.path.join(P, 'reels', 'musik')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')


def emoji_ebene(zeilen, zeichen):
    alt = hk.emoji
    hk.emoji = lambda _, h: alt(zeichen, h)
    e = hk.text_ebene(zeilen)
    hk.emoji = alt
    return e


def schreiben(pfad, frames, dauer, musik, ab=0):
    tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, c in enumerate(frames):
        if i == int(0.4 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', os.path.join(MUSIK, musik), '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.2,afade=t=out:st={dauer - 1.0:.2f}:d=1.0,volume=1.5,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


# ---------- 1. Babyfieber ----------
def babyfieber():
    hk.VON, hk.BIS = 0.0, 9.0
    ebene = emoji_ebene(['Warnung:', 'Babyfieber-Gefahr ✨'], '🥹')
    dauer = 9.0

    def frames():
        for i, fr in enumerate(hk.clip_frames()):
            t = i / FPS
            a = 1 - m.ease((t - 2.4) / 0.4) if t < 7.6 else m.ease((t - 7.6) / 0.4)   # Text am Anfang und zum Loop
            c = fr.convert('RGBA')
            if a > 0:
                e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
            yield c
    schreiben(os.path.join(BASIS, 'reel_hello_little_bear_babyfieber_9x16.mp4'), frames(), dauer, 'mixkit_michael-ramir_christmas-lullaby.mp3', 4)


# ---------- 2. Was ist im Set? ----------
TEILE_LISTE = [('strampler', 'Strampler mit Reissverschluss'), ('body', 'Body «funny every day»'),
               ('muetze', 'Mütze mit Öhrchen'), ('faeustlinge', 'Fäustlinge'), ('laetzchen', 'Lätzchen «Hello Little Bear»')]
DUNKEL = (60, 52, 46)
RASTER = [(300, 680, 500), (780, 680, 500), (300, 1160, 460), (780, 1160, 460), (540, 1580, 400)]   # x, y, Grösse


def tx(d, text, y, groesse=50, fill=DUNKEL):
    fo = ImageFont.truetype(SCHRIFT, groesse)
    while d.textlength(text, font=fo) > 960 and groesse > 30:
        groesse -= 2; fo = ImageFont.truetype(SCHRIFT, groesse)
    d.text((W / 2, y), text, font=fo, fill=fill, anchor='mm')


def was_ist_drin():
    bilder = {n: Image.open(os.path.join(TEILE, f'set_little_bear_{n}.jpg')).convert('RGB') for n, _ in TEILE_LISTE}
    HOOK, PRO, RASTER_T, ENDE = 2.0, 1.35, 1.6, 2.6
    dauer = HOOK + PRO * (len(TEILE_LISTE) - 1) + RASTER_T + ENDE
    n = int(round(dauer * FPS))
    sp = hk.emoji('🧸', 46)

    def gross(name, t_lokal):
        s = 0.94 + 0.06 * m.ease(t_lokal / 0.5)
        g = round(940 * s); im = bilder[name].resize((g, g), Image.LANCZOS)
        return im, ((W - g) // 2, 470 + (940 - g) // 2)

    def frames():
        for i in range(n):
            t = i / FPS
            c = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(c)
            if t < HOOK + PRO * (len(TEILE_LISTE) - 1):
                k = 0 if t < HOOK else 1 + int((t - HOOK) // PRO)
                t0 = 0 if k == 0 else HOOK + (k - 1) * PRO
                name, label = TEILE_LISTE[k]
                im, pos = gross(name, t - t0); c.paste(im, pos)
                if k == 0:
                    tx(d, 'Was ist im Set', 250, 58)
                    tx(d, '«Hello Little Bear»?', 330, 58)
                    bx = W / 2 + d.textlength('«Hello Little Bear»?', font=ImageFont.truetype(SCHRIFT, 58)) / 2 + 12
                    c.paste(sp, (int(bx), 330 - sp.height // 2), sp)
                tx(d, f'{k + 1}/5  {label}', 1520, 44)
            else:
                # Raster füllt sich Teil für Teil (leer → voll), dann Auflösung
                tr = t - (HOOK + PRO * (len(TEILE_LISTE) - 1))
                for j, ((name, _), (x, y, g)) in enumerate(zip(TEILE_LISTE, RASTER)):
                    a = m.ease((tr - j * 0.18) / 0.3)
                    if a <= 0:
                        continue
                    gg = round(g * (0.85 + 0.15 * a)); im = bilder[name].resize((gg, gg), Image.LANCZOS)
                    if a < 1:
                        im = Image.blend(Image.new('RGB', im.size, (255, 255, 255)), im, a)
                    c.paste(im, (x - gg // 2, y - gg // 2))
                tx(d, '5 Teile · 100 % Baumwolle', 170, 52)
                if tr > RASTER_T:
                    a = m.ease((tr - RASTER_T) / 0.4)
                    f = tuple(int(255 + (v - 255) * a) for v in DUNKEL)
                    tx(d, 'Preis? Schreib PREIS', 270, 50, f)
                    tx(d, 'in die Kommentare', 335, 50, f)
            yield c.convert('RGBA')
    schreiben(os.path.join(BASIS, 'reel_hello_little_bear_was-ist-drin_9x16.mp4'), frames(), dauer, 'alex-morgan_no-copyright-music.mp3')


if __name__ == '__main__':
    wahl = sys.argv[1:] or ['babyfieber', 'was-ist-drin']
    if 'babyfieber' in wahl:
        babyfieber()
    if 'was-ist-drin' in wahl:
        was_ist_drin()
