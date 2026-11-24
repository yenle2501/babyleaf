"""Coming-soon-Reel Strampler «Velours»: «POV: she is here 💓💓💖» (Wunsch der Nutzerin 24.11.2026, alles auf Englisch).

Clips: velours/original (Baby wach, auf dem Rücken, nichts im Bett) + Produktfoto der Nutzerin mit Zoom auf Rüschen
und Knöpfe. Die neu geschickten Videos (Baby schläft auf der Seite im Erwachsenenbett, Kissen, Decke, Plüschhase,
Haarband) sind wegen Safe Sleep nicht dabei.
Text: Schreibmaschinenschrift weiss mit Schleier, am Anfang und zum Loop am Ende. Standardmusik, Endfolie, kein Preis.

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
TY = 1500
# (Art, Quelle, von, bis[, Zoom-Start, Zoom-Ende, Fokus x, Fokus y])
TEILE = [('foto', FOTO, 0, 2.6, 1.0, 1.12, 0.48, 0.45),                       # ganzer Strampler, langsamer Zoom
         ('clip', os.path.join(ORIG, 'clip_strampeln.mp4'), 4.0, 6.6),          # wach, strampelt
         ('foto', FOTO, 0, 1.8, 2.2, 2.4, 0.5, 0.30),                         # Kragen und Knöpfe
         ('clip', os.path.join(ORIG, 'clip_strecken.mp4'), 5.0, 7.6),           # streckt sich, schaut
         ('foto', FOTO, 0, 1.8, 2.4, 2.6, 0.25, 0.40),                        # Rüschen am Ärmel
         ('clip', os.path.join(ORIG, 'clip_strampeln.mp4'), 9.0, 11.4)]         # wach
BLENDE = 0.3


def foto_frames(pfad, dauer, z0, z1, fx, fy):
    im = Image.open(pfad).convert('RGB')
    for i in range(int(round(dauer * FPS))):
        z = z0 + (z1 - z0) * m.ease(i / (dauer * FPS))
        s = max(W / im.width, H / im.height) * z
        cw, ch = W / s, H / s
        x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
        yield im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def alle_frames():
    teile = []
    for t in TEILE:
        if t[0] == 'foto':
            teile.append(list(foto_frames(t[1], t[3] - t[2], *t[4:])))
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
    s = Image.new('L', (W, H), 0); ImageDraw.Draw(s).ellipse((60, TY - 90, W - 60, TY + 90), fill=150)
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
