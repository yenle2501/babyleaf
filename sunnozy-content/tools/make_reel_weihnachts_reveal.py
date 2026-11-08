"""Coming-soon-Reel «Weihnachts-Reveal» (08.11.2026), Trend: Weihnachts-Reveal mit Lichterglanz.

  0–2.8 s     warmes Lichter-Bokeh (selbst erzeugt), «Psst …» → «bald liegt etwas Kleines unter Deinem Baum»
  2.8–6 s     die rote sunnozy-Geschenkbox steigt als Bildkarte auf, langsamer Zoom, «Weihnachts-Geschenkboxen»
  6–10 s      8 schnelle Schnitte (0.5 s): Babys in den Box-Outfits (KI, Pinterest-Stil) und Box-Inhalte
  10–14 s     zurück ins Bokeh: Logo, COMING SOON, sunnozy.ch
Musik «Holiday 01» (Mixkit, lizenzfrei), der Aufbau im Stück fällt auf das Erscheinen der Box.

    python3 tools/make_reel_weihnachts_reveal.py
Ausgabe: posts/reels/coming-soon/reel_weihnachts_reveal_9x16.mp4 + _titelbild.jpg
Nur KI-Bilder bzw. Box-Hauptbilder mit KI-Inhalt (keine echten Fotos).
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'kampagne-weihnachtsbox')
OUT = os.path.join(m.POSTS, 'reels', 'coming-soon')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'mixkit_lily-j_holiday-01.mp3')
HELL = (253, 244, 232); GOLD = (232, 190, 120)
BOX = lambda k: os.path.join(BASIS, 'rote-box', 'shopify', 'geschenkbox-' + k + '.jpg')
BABY = lambda k: os.path.join(BASIS, 'baby-pinterest-stil', k + '_4x5.jpg')
SCHNITTE = [('baby', 'growing_up_strong'), ('box', 'dinosaur'), ('baby', 'mum_dad_me'), ('box', 'i-like-flying'),
            ('baby', 'dino'), ('box', 'little-one'), ('baby', 'i_love_my_mummy'), ('baby', 'lovely_little_girl')]
T1, T2, T3, T_END = 2.8, 6.0, 10.0, 14.0


def bokeh_basis():
    """Dunkler, warmer Hintergrund mit unscharfen Lichtpunkten in drei Ebenen (für leichte Bewegung)."""
    rng = np.random.default_rng(7)
    y = np.linspace(0, 1, H)[:, None]
    grund = np.zeros((H, W, 3), np.float32)
    for c, (a, b) in enumerate(zip((46, 26, 20), (16, 9, 8))):
        grund[..., c] = a * (1 - y[:, 0, None]) + b * y[:, 0, None]
    ebenen = []
    for n, r0, r1, blur, alpha in ((26, 30, 70, 18, 0.55), (40, 14, 34, 8, 0.7), (60, 4, 10, 2, 0.9)):
        L = Image.new('RGBA', (W, int(H * 1.15)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for _ in range(n):
            x, yy, r = rng.uniform(0, W), rng.uniform(0, H * 1.15), rng.uniform(r0, r1)
            farbe = tuple(int(v) for v in (np.array(GOLD) * rng.uniform(0.75, 1.1)).clip(0, 255))
            d.ellipse((x - r, yy - r, x + r, yy + r), fill=farbe + (int(255 * alpha * rng.uniform(0.4, 1)),))
        ebenen.append(L.filter(ImageFilter.GaussianBlur(blur)))
    return Image.fromarray(grund.clip(0, 255).astype(np.uint8)).convert('RGBA'), ebenen


def bokeh(basis, ebenen, t):
    c = basis.copy()
    for k, L in enumerate(ebenen):
        dy = int((t * (8 + 10 * k)) % (L.height - H))           # Lichter steigen langsam, verschieden schnell
        c.alpha_composite(L.crop((0, dy, W, dy + H)))
    return c


def text(c, zeilen, alpha, y, groesse, schrift=None):
    if alpha <= 0:
        return c
    fo = m.f(schrift or m.SERIF_I, groesse)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        yy = y + k * groesse * 1.12
        ds.text((W / 2, yy + 3), z, font=fo, fill=(0, 0, 0, int(180 * alpha)), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0, int(180 * alpha)))
        dt.text((W / 2, yy), z, font=fo, fill=HELL + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); c.alpha_composite(tx)
    return c


def gesperrt(c, wort, alpha, y, groesse, abstand):
    if alpha <= 0:
        return c
    fo = m.f(m.SERIF, groesse); e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(e)
    b = [d.textlength(ch, font=fo) for ch in wort]; x = W / 2 - (sum(b) + abstand * (len(wort) - 1)) / 2
    for ch, w in zip(wort, b):
        d.text((x, y), ch, font=fo, fill=GOLD + (int(255 * alpha),), anchor='lm'); x += w + abstand
    c.alpha_composite(e)
    return c


def karte(im, breite, radius=26):
    s = breite / im.width; k = im.resize((breite, round(im.height * s)), Image.LANCZOS).convert('RGBA')
    mk = Image.new('L', k.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, k.width - 1, k.height - 1), radius, fill=255)
    k.putalpha(mk)
    return k


def mit_schatten(c, k, x, y, alpha=1.0):
    sch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sch).rounded_rectangle((x + 10, y + 24, x + k.width + 10, y + k.height + 24), 26, fill=(0, 0, 0, int(150 * alpha)))
    c.alpha_composite(sch.filter(ImageFilter.GaussianBlur(26)))
    if alpha < 1:
        k = k.copy(); k.putalpha(k.getchannel('A').point(lambda v: int(v * alpha)))
    c.alpha_composite(k, (int(x), int(y)))
    return c


def fuell(im, z, fy=0.45):
    s = max(W / im.width, H / im.height) * z
    bw, bh = W / s, H / s; cx = im.width / 2; cy = min(max(fy * im.height, bh / 2), im.height - bh / 2)
    return im.resize((W, H), Image.BICUBIC, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')


def main():
    basis, ebenen = bokeh_basis()
    box = karte(Image.open(BOX('mum-dad-me')).convert('RGB'), 860)
    schnitte = []
    for art, k in SCHNITTE:
        schnitte.append(Image.open(BABY(k) if art == 'baby' else BOX(k)).convert('RGB'))
    L = m.logo(560, HELL)
    pfad = os.path.join(OUT, 'reel_weihnachts_reveal_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = int(T_END * FPS)
    for i in range(n):
        t = i / FPS
        if t < T2 or t >= T3:
            c = bokeh(basis, ebenen, t)
        if t < T1:
            text(c, ['Psst …'], m.ease(t / 0.5) * (1 - m.ease((t - 1.1) / 0.3)), 900, 110)
            text(c, ['bald liegt etwas Kleines', 'unter Deinem Baum'], m.ease((t - 1.3) / 0.5), 860, 84)
        elif t < T2:
            e = m.ease((t - T1) / 1.0)
            y = 1000 - box.height / 2 + (1 - e) * 500
            text(c, ['bald liegt etwas Kleines', 'unter Deinem Baum'], 1 - m.ease((t - T1) / 0.4), 860, 84)
            z = 1 + 0.05 * (t - T1) / (T2 - T1)
            bz = box.resize((round(box.width * z), round(box.height * z)), Image.BICUBIC)
            mit_schatten(c, bz, (W - bz.width) / 2, y - (bz.height - box.height) / 2, e)
            text(c, ['Weihnachts-Geschenkboxen'], m.ease((t - T1 - 0.7) / 0.6), 330, 78)
        elif t < T3:
            k = min(int((t - T2) / 0.5), len(schnitte) - 1); tt = (t - T2 - k * 0.5) / 0.5
            c = fuell(schnitte[k], 1.04 + 0.04 * tt, 0.5)
        else:
            tt = t - T3
            a = m.ease(tt / 0.8)
            Lk = L.copy(); Lk.putalpha(Lk.getchannel('A').point(lambda v: int(v * a)))
            c.alpha_composite(Lk, ((W - L.width) // 2, 760))
            gesperrt(c, 'COMING SOON', m.ease((tt - 0.6) / 0.8), 1000, 60, 16)
            text(c, ['sunnozy.ch'], m.ease((tt - 1.2) / 0.8), 1110, 58, m.SERIF)
            if t > T_END - 0.5:
                c = Image.blend(c, bokeh(basis, ebenen, t), (t - (T_END - 0.5)) / 0.5)
        fr = c.convert('RGB')
        if i == int(3.6 * FPS):
            fr.save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '25.5', '-i', MUSIK, '-t', str(T_END),
                    '-af', f'afade=t=in:d=0.6,afade=t=out:st={T_END - 1.5}:d=1.5,volume=1.15,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(pfad, flush=True)


if __name__ == '__main__':
    main()
