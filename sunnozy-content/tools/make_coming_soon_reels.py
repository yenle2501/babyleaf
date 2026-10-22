"""Coming-soon-Reels aus KI-Babyclips (Grok): POV-Hook, Set-Auflösung, Schlusskarte. Schrift: Cormorant Garamond.

    python3 tools/make_coming_soon_reels.py              # alle Reels aus REELS
    python3 tools/make_coming_soon_reels.py blumen_a     # nur eines (Schlüssel aus REELS)

Ausgabe flach nach posts/reels/coming-soon/ (Reel 9:16 und Titelbild). Quellclips liegen in posts/coming-soon/<set>/original/.

Aufbau (nach posts/instagram/pov-hooks.md):
  0 s      Baby-Clip füllt das Bild, POV-Hook steht ab dem ersten Bild im unteren Drittel (nie über dem Gesicht)
  ~45 %    zweite Zeile löst auf (was das Set kann)
  Clipende Set-Foto auf Creme mit Name und Teilen (Produkt im Fokus)
  Schluss  Coming soon, Logo; die letzte Blende läuft zurück ins erste Bild, damit das Reel sauber loopt
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
CS = os.path.join(POSTS, 'coming-soon')
OUT = os.path.join(POSTS, 'reels', 'coming-soon')
W, H, FPS = 1080, 1920, 30
CREME, WALD, SALBEI, GRAU = (253, 252, 250), (35, 48, 41), (122, 139, 111), (110, 118, 113)
SERIF, SERIF_I = 'cormorantR.ttf', 'cormorant.ttf'   # Cormorant Garamond Medium, Regular und Italic

# clip: Quelle, von/bis (s), x: Mitte des 9:16-Ausschnitts im Clip (0..1)
REELS = {
    'little_princess': dict(
        clip=os.path.join(CS, 'little-princess', 'original', 'baby_clip_e.mp4'), von=0, bis=6, x=0.36,
        hook=['POV: Deine beste Freundin', 'bekommt ein Mädchen'], hook2=['und das Geschenk', 'ist schon da'],
        set_bild=os.path.join(POSTS, 'marktplatz-galaxus-amazon', 'hauptbild', 'set_prinzessin_krone.jpg'),
        name='«Little Princess»', teile='8 Teile, mit Kronen-Schmusetuch', datei='reel_little_princess_pov_9x16'),
    'best_family_a': dict(
        clip=os.path.join(CS, 'best-family-teddy', 'original', 'baby_clip_a.mp4'), von=0, bis=7.5, x=0.5,
        hook=['POV: Er entdeckt', 'seinen ersten Teddy'], hook2=['Die Teddy-Rassel', 'ist im Set dabei'],
        set_bild=os.path.join(POSTS, 'produktfotos-set-praesentation', 'ohne_logo', 'set_best_family_quadratisch.jpg'),
        name='«Best Family»', teile='8 Teile, mit Teddy-Rassel', datei='reel_best_family_teddy_a_9x16'),
    'best_family_b': dict(
        clip=os.path.join(CS, 'best-family-teddy', 'original', 'baby_clip_b.mp4'), von=3.5, bis=11.5, x=0.5,
        hook=['Wenn der Teddy', 'sofort der beste Freund ist'], hook2=['Body, Strampler, Mütze', 'und der Teddy dazu'],
        set_bild=os.path.join(POSTS, 'produktfotos-set-praesentation', 'ohne_logo', 'set_best_family_quadratisch.jpg'),
        name='«Best Family»', teile='8 Teile, mit Teddy-Rassel', datei='reel_best_family_teddy_b_9x16'),
    'blumen_a': dict(
        clip=os.path.join(CS, 'blumen-musselin', 'original', 'baby_clip_a.mp4'), von=0, bis=7.5, x=0.36,
        hook=['POV: Wickeln', 'um 3 Uhr nachts'], hook2=['und nichts muss', 'über den Kopf'],
        set_bild=os.path.join(CS, 'blumen-musselin', 'shop', 'blumen-musselin_shop_ohne_logo.jpg'),
        name='«Blumenwiese»', teile='Wickelbody, Fusshose, Haarband', datei='reel_blumenwiese_a_9x16'),
    'blumen_b': dict(
        clip=os.path.join(CS, 'blumen-musselin', 'original', 'baby_clip_b.mp4'), von=0, bis=7.5, x=0.36,
        hook=['Schick das der Freundin,', 'die ein Mädchen erwartet'], hook2=['Weicher Musselin,', 'Blümchen von Kopf bis Fuss'],
        set_bild=os.path.join(CS, 'blumen-musselin', 'shop', 'blumen-musselin_shop_ohne_logo.jpg'),
        name='«Blumenwiese»', teile='Wickelbody, Fusshose, Haarband', datei='reel_blumenwiese_b_9x16'),
}
T_SET, T_END, BLENDE = 2.4, 2.0, 0.35


def f(name, size):
    return ImageFont.truetype(os.path.join(ROOT, 'fonts', name), int(size))


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def logo(width, col):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def clip_frames(pfad, von, bis):
    """Alle Frames des Clips (Originalgrösse) im Bereich von..bis, auf 30 fps."""
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                    '-of', 'csv=p=0', pfad], capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', pfad, '-vf', f'fps={FPS}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    n = len(raw) // (w * h * 3)
    return [Image.frombuffer('RGB', (w, h), raw[i * w * h * 3:(i + 1) * w * h * 3]) for i in range(n)]


def fuellen(im, x, zoom):
    """Clip-Frame auf 9:16 füllen: Höhe passt, Ausschnitt um x (0..1), leichter Zoom."""
    s = H / im.height * zoom
    bw, bh = W / s, H / s
    cx = min(max(x * im.width, bw / 2), im.width - bw / 2)
    cy = im.height / 2
    return im.resize((W, H), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')


VERLAUF = None


def text_unten(c, zeilen, alpha, y=1290, groesse=92):
    """Weisse Cormorant mit weichem Schatten im unteren Drittel, über einem sanften Verlauf (keine Textbox)."""
    global VERLAUF
    if VERLAUF is None:
        g = np.zeros((H, 1), np.float32); a0 = 1050
        g[a0:, 0] = np.clip((np.arange(H - a0) / 420.0), 0, 1) ** 1.2 * 0.58
        VERLAUF = Image.fromarray((g * 255).astype(np.uint8)).resize((W, H))
    if alpha <= 0:
        return c
    dunkel = Image.new('RGBA', (W, H), (25, 18, 14, 0)); dunkel.putalpha(VERLAUF.point(lambda v: int(v * alpha)))
    c.alpha_composite(dunkel)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    while groesse > 50 and max(ds.textlength(z, font=f(SERIF, groesse)) for z in zeilen) > 800:   # rechts liegen die Instagram-Knöpfe
        groesse -= 2
    fo = f(SERIF, groesse); lh = groesse * 1.12
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        p = (W / 2, y + k * lh)
        ds.text((p[0] + 2, p[1] + 3), z, font=fo, fill=(20, 14, 10, int(200 * alpha)), anchor='mm', stroke_width=7, stroke_fill=(20, 14, 10, int(200 * alpha)))
        dt.text(p, z, font=fo, fill=(255, 255, 255, int(255 * alpha)), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    c.alpha_composite(tx)
    return c


def set_karte(r, t):
    """Produkt im Fokus: Set-Foto gross auf Creme, darunter Name und Teile."""
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    e = ease(t / 0.5)
    im = Image.open(r['set_bild']).convert('RGB'); s = 940 / max(im.size) * (0.96 + 0.04 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 860 - im.height // 2))
    d.text((W / 2, 340), 'coming soon', font=f(SERIF_I, 56), fill=SALBEI, anchor='mm')
    d.text((W / 2, 1400), r['name'], font=f(SERIF, 96), fill=WALD, anchor='mm')
    d.text((W / 2, 1490), r['teile'], font=f(SERIF_I, 50), fill=GRAU, anchor='mm')
    return c


def end_karte(r):
    c = Image.new('RGBA', (W, H), CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 760), 'Coming soon', font=f(SERIF, 120), fill=WALD, anchor='mm')
    d.text((W / 2, 880), r['name'], font=f(SERIF_I, 76), fill=SALBEI, anchor='mm')
    d.line((W / 2 - 70, 975, W / 2 + 70, 975), fill=(200, 192, 180), width=2)
    d.text((W / 2, 1050), 'Bald auf sunnozy.ch', font=f(SERIF, 52), fill=GRAU, anchor='mm')
    d.text((W / 2, 1115), 'Folge uns, damit Du es zuerst siehst', font=f(SERIF_I, 44), fill=GRAU, anchor='mm')
    L = logo(260, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1300), L)
    return c


def reel(key):
    r = REELS[key]
    frames = clip_frames(r['clip'], r['von'], r['bis'])
    n_clip = len(frames); n_set = int(T_SET * FPS); n_end = int(T_END * FPS); nb = int(BLENDE * FPS)
    n = n_clip + n_set + n_end
    end = end_karte(r)

    def clip_bild(i):
        t = i / max(n_clip - 1, 1)
        c = fuellen(frames[i], r['x'], 1.0 + 0.06 * t)
        wechsel = 0.45
        if t < wechsel:
            a = 1 - ease((t - (wechsel - 0.06)) / 0.06)
            return text_unten(c, r['hook'], a)
        return text_unten(c, r['hook2'], ease((t - wechsel) / 0.06))

    def bild(i):
        if i < n_clip:
            c = clip_bild(i)
            if i >= n_clip - nb:
                c = Image.blend(c, set_karte(r, 0), (i - (n_clip - nb)) / nb)
            return c
        i -= n_clip
        if i < n_set:
            c = set_karte(r, i / FPS)
            if i >= n_set - nb:
                c = Image.blend(c, end, (i - (n_set - nb)) / nb)
            return c
        i -= n_set
        if i >= n_end - nb:   # zurück ins erste Bild: sauberer Loop
            return Image.blend(end, clip_bild(0), (i - (n_end - nb)) / nb)
        return end

    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, r['datei'] + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        fr = bild(i).convert('RGB')
        if i == int(0.6 * FPS):
            fr.save(os.path.join(OUT, r['datei'] + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {n / FPS:.1f} s')


if __name__ == '__main__':
    for key in (sys.argv[1:] or REELS):
        reel(key)
