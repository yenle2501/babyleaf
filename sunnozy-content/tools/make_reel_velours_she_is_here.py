"""Coming-soon-Reel Strampler «Velours»: «POV: she is here 💓💓💖» (Wunsch der Nutzerin 24.11.2026, alles auf Englisch).

Nur die zwei Videos, die die Nutzerin am 24.11. geschickt hat (`velours/original/clip_bett_a.mp4`, `clip_bett_b.mp4`),
auf ausdrücklichen Wunsch der Nutzerin. Ausnahme von der Safe-Sleep-Regel: Das Baby schläft auf der Seite im
Erwachsenenbett mit Kissen, Decke, Plüschhase und Haarband.
Die Clips (800×1136) stehen in voller Breite, damit Kopf und Füsse ganz im Bild sind, oben und unten eine unscharfe
Verlängerung. Text: Schreibmaschinenschrift weiss mit Schleier, am Anfang und zum Loop am Ende. Standardmusik, Endfolie.

    python3 tools/make_reel_velours_she_is_here.py
Ausgabe: posts/coming-soon/reels/velours/reel_velours_she_is_here_9x16.mp4
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_reel_hello_little_bear_hook as hk
import make_reel_velours_coming_soon as vc
from endfolie import anhaengen, CS_AUFRUF

W, H, FPS = m.W, m.H, 30
V = os.path.join(m.POSTS, 'coming-soon', 'reels', 'velours')
ORIG = os.path.join(V, 'original')
FOTO = os.path.join(ORIG, 'produktfoto_velours.png')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
TEXT, EMOJI = ['POV: she is here'], '💓💓💖'
TY = 420                 # über den Kissen, nicht auf dem Baby
TEILE = [('bett', os.path.join(ORIG, 'clip_bett_a.mp4'), 0.3, 5.8),
         ('bett', os.path.join(ORIG, 'clip_bett_b.mp4'), 1.0, 6.8)]
BLENDE = 0.3


def foto_frames(pfad, dauer, z0, z1, fx, fy):
    im = Image.open(pfad).convert('RGB')
    for i in range(int(round(dauer * FPS))):
        z = z0 + (z1 - z0) * m.ease(i / (dauer * FPS))
        s = max(W / im.width, H / im.height) * z
        cw, ch = W / s, H / s
        x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
        yield im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def bett_frames(pfad, von, bis):
    """Clip in voller Breite, mittig, oben und unten unscharf verlängert."""
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', pfad],
                                   capture_output=True, text=True).stdout.strip().split(','))
    ch = round(W * h / w); ch += ch % 2; y0 = (H - ch) // 2
    mk = Image.new('L', (W, ch), 255); d = ImageDraw.Draw(mk)
    for y in range(90):
        a = int(255 * y / 90); d.line((0, y, W, y), fill=a); d.line((0, ch - 1 - y, W, ch - 1 - y), fill=a)
    for fr in _roh(pfad, von, bis, ch):
        bg = Image.new('RGB', (W, H))
        oben = fr.crop((0, 0, W, 50)).resize((W // 8, (y0 + 90) // 8)).filter(ImageFilter.GaussianBlur(3)).resize((W, y0 + 90), Image.BICUBIC)
        unten = fr.crop((0, ch - 50, W, ch)).resize((W // 8, (H - y0 - ch + 90) // 8)).filter(ImageFilter.GaussianBlur(3)).resize((W, H - y0 - ch + 90), Image.BICUBIC)
        bg.paste(oben, (0, 0)); bg.paste(unten, (0, y0 + ch - 90))       # Rand verlängert: oben Wand, unten Leintuch
        bg.paste(fr, (0, y0), mk)
        yield bg


def _roh(pfad, von, bis, ch):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={W}:{ch}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * ch * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, ch), b)


def alle_frames():
    teile = []
    for t in TEILE:
        if t[0] == 'foto':
            teile.append(list(foto_frames(t[1], t[3] - t[2], *t[4:])))
        elif t[0] == 'bett':
            teile.append(list(bett_frames(t[1], t[2], t[3])))
        else:
            teile.append(list(k1.clip_frames(t[1], t[2], t[3])))
    nb = int(BLENDE * FPS)
    for k, t in enumerate(teile):
        start = nb if k > 0 else 0; ende = len(t) - (nb if k < len(teile) - 1 else 0)
        for i in range(start, ende):
            yield t[i]
        if k < len(teile) - 1:
            for j in range(nb):
                yield Image.blend(t[ende + j], teile[k + 1][j], (j + 1) / (nb + 1))


def text_ebene():
    fo = ImageFont.truetype(SCHRIFT, 60)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    sl = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(sl)
    teile = [hk.emoji(z, 54) for z in EMOJI]; ew = sum(e.width for e in teile) + 6 * (len(teile) - 1)
    z = TEXT[0]; breite = d.textlength(z, font=fo) + 16 + ew; x0 = (W - breite) / 2
    for dx, dy in ((0, 3), (2, 3), (-2, 3), (0, 0)):
        ds.text((x0 + dx, TY + dy), z, font=fo, fill=200, anchor='lm')
    d.text((x0, TY), z, font=fo, fill=(255, 255, 255, 255), anchor='lm')
    x = x0 + d.textlength(z, font=fo) + 16
    for e in teile:
        tx.alpha_composite(e, (int(x), int(TY - e.height / 2 - 4))); x += e.width + 6
    # Schleier hinter dem Text (heller Strampler)
    s = Image.new('L', (W, H), 0); ImageDraw.Draw(s).ellipse((60, TY - 90, W - 60, TY + 90), fill=150)   # Schleier hinter dem Text
    e = Image.new('RGBA', (W, H), (40, 30, 22, 0)); e.putalpha(s.filter(ImageFilter.GaussianBlur(45)))
    sch = Image.new('RGBA', (W, H), (45, 30, 20, 0)); sch.putalpha(sl.filter(ImageFilter.GaussianBlur(9)))
    e.alpha_composite(sch); e.alpha_composite(tx)
    return e


def main():
    ebene = text_ebene(); vig = vc.vignette()
    pfad = os.path.join(V, 'reel_velours_she_is_here_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    if os.path.exists(pfad):
        os.remove(pfad)
    frames = list(alle_frames()); n = len(frames); dauer = n / FPS
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, fr in enumerate(frames):
        t = i / FPS
        c = vc.warm(fr).filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=2)).convert('RGBA'); c.alpha_composite(vig)
        a = max(1 - m.ease((t - 2.8) / 0.4), m.ease((t - (dauer - 2.4)) / 0.5))   # Anfang und Loop am Ende
        if a > 0:
            c.alpha_composite(k1.mit_alpha(ebene, a))
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', k1.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)
    anhaengen(pfad, FOTO, 'romper «Velours»', 'coming soon', CS_AUFRUF)


if __name__ == '__main__':
    main()
