"""Set-Video aus einem Baby-Clip (z.B. Grok-KI-Video, 848x1072, 10 s) fuer ein neues Set: Reel 9:16 und Feed 4:5.

Ablauf (ca. 14 s, stumm, Ton waehlst Du in Instagram):
1. Baby-Clip, 6 s. Ein Creme-Etikett «COMING SOON» (oder «NEU BEI SUNNOZY» mit Preis) + Setname, ab 3,2 s «Für die ersten Wochen».
   Im 9:16 faehrt der Ausschnitt langsam vom Baby zum Schmusetuch (der Clip ist breiter als 9:16).
2. Das ganze Set (Praesentationsbild) mit «Was steckt drin?».
3. Die Teile erscheinen nacheinander als Kacheln mit Namen und Zaehler.
4. Schluss: «Alles drin.», Teile-Anzahl, Preis (nur wenn angegeben), Gratisversand, Logo, sunnozy.ch.
   Ohne Preis ist das Set noch nicht im Shop: dann Stempel «COMING SOON» und «Bald auf sunnozy.ch».
Look nach dem sunnozy-Designsystem (Creme, Waldgruen, Fraunces, Nunito Sans, eckige Kacheln, keine Emojis).

Aufruf: python3 make_set_video.py <clip.mp4> <ausgabe-ohne-endung> [--set=gaensebluemchen] [--preis=30.40]
--set: Schluessel aus SETS (Standard little_princess)
--kamera=schwenk|mitte, --etikett_4x5=oben_rechts|mitte|unten: Einstellung des Sets fuer diesen Clip ueberschreiben
--preis: Set ist im Shop -> Preis statt «Coming soon»
Erzeugt <ausgabe>_9x16.mp4, <ausgabe>_4x5.mp4 und je ein _standbild.jpg.
"""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
FONT = lambda n: os.path.join(ROOT, 'fonts', n)
CREME, WALD, KACHEL, SALBEI, GRAU = (253, 252, 250), (35, 48, 41), (244, 239, 232), (122, 139, 111), (110, 118, 113)
FPS = 30

# Sets (noch nicht im Shop, darum «Coming soon», solange kein Preis angegeben ist).
# kamera 'schwenk': 9:16-Ausschnitt faehrt von links nach rechts (Baby -> Schmusetuch); 'mitte': fester Ausschnitt
# in der Mitte mit leichtem Zoom. etikett_4x5 'oben_rechts' oder 'unten' (je nachdem, wo das Gesicht nicht ist).
SETS = {
    'little_princess': dict(
        titel='«Little Princess»', ordner='set_prinzessin_krone', kamera='schwenk', etikett_4x5='oben_rechts',
        teile=[('kapuzentuch', 'Kapuzentuch'), ('strampler', 'Strampler'), ('body', 'Body'), ('muetze', 'Mütze'),
               ('schmusetuch', 'Schmusetuch'), ('laetzchen', 'Lätzchen'), ('socken', 'Söckchen'), ('faeustlinge', 'Fäustlinge')]),
    'gaensebluemchen': dict(
        titel='«Gänseblümchen»', ordner='set_gaensebluemchen', kamera='mitte', etikett_4x5='unten',
        teile=[('kapuzentuch', 'Kapuzentuch'), ('strampler', 'Strampler'), ('body', 'Body'), ('muetze', 'Mütze'),
               ('rassel', 'Rassel'), ('laetzchen', 'Lätzchen'), ('socken', 'Söckchen'), ('faeustlinge', 'Fäustlinge')]),
}
SET_BILD = lambda st: os.path.join(POSTS, 'produktfotos-set-praesentation', 'ki-roh', st['ordner'] + '_quadratisch.jpg')
ET = lambda st: os.path.join(POSTS, 'marktplatz-galaxus-amazon', 'einzelteile', st['ordner'])

T_CLIP, T_SET, T_TEIL, T_END = 6.0, 1.7, 0.45, 2.8


def f(name, size):
    return ImageFont.truetype(FONT(name), int(size))


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def freistellen(pfad):
    im = Image.open(pfad).convert('RGB')
    a = np.asarray(im.convert('L')); ys, xs = np.where(a < 244)
    return im.crop((max(0, xs.min() - 12), max(0, ys.min() - 12), min(im.width, xs.max() + 12), min(im.height, ys.max() + 12)))


def multiply(c, im, xy):
    x, y = xy; box = (x, y, x + im.width, y + im.height)
    c.paste(ImageChops.multiply(c.crop(box), im), box)


def gesperrt(d, xy, text, font, fill, sp):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = xy[0] - w / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def raster(n, W, top, bottom, pro=4, gap=16, rand=50):
    """Kachel-Positionen in Zeilen zu `pro`, letzte Zeile zentriert, Raster senkrecht mittig."""
    reihen = math.ceil(n / pro)
    cw = (W - 2 * rand - (pro - 1) * gap) / pro
    ch = min(cw * 1.12, (bottom - top - (reihen - 1) * gap) / reihen)
    top += ((bottom - top) - (reihen * ch + (reihen - 1) * gap)) / 2
    pos = []
    for i in range(n):
        r, kk = divmod(i, pro)
        in_reihe = min(pro, n - r * pro)
        x0 = (W - (in_reihe * cw + (in_reihe - 1) * gap)) / 2
        pos.append((x0 + kk * (cw + gap), top + r * (ch + gap), cw, ch))
    return pos


def kachel(c, im, lab, box, alpha=1.0, skala=1.0, schrift=24):
    d = ImageDraw.Draw(c)
    x, y, w, h = box; lh = schrift * 1.7
    d.rectangle([x, y, x + w, y + h], fill=KACHEL)
    s = min((w - 24) / im.width, (h - lh - 20) / im.height) * skala
    t = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    if alpha < 1:
        t = Image.blend(Image.new('RGB', t.size, (255, 255, 255)), t, alpha)
    multiply(c, t, (int(x + (w - t.width) / 2), int(y + 10 + (h - lh - 20 - t.height) / 2)))
    if alpha > 0.3:
        d.text((x + w / 2, y + h - lh / 2 - 2), lab, font=f('nunitosans-600.ttf', schrift), fill=WALD, anchor='mm')


def clip_frames(pfad):
    """Alle Frames des Clips als RGB-Arrays (auf 30 fps gebracht)."""
    p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                        '-of', 'csv=p=0', pfad], capture_output=True, text=True, check=True)
    w, h = map(int, p.stdout.strip().split(',')[:2])
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', pfad, '-t', str(T_CLIP + 0.2), '-vf', f'fps={FPS}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def etikett(c, mitte, zeile1, zeile2, u, W):
    """Creme-Etikett auf dem Video (leicht durchscheinend), blendet mit u (0..1) ein. mitte = (x, y) der Etikettmitte."""
    if u <= 0:
        return
    k = W / 1080
    bw, bh = 620 * k, 160 * k
    x0, y0 = mitte[0] - bw / 2, mitte[1] - bh / 2
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=CREME + (int(235 * u),))
    gesperrt(d, (mitte[0], y0 + 45 * k), zeile1, f('nunitosans-700.ttf', 22 * k), SALBEI + (int(255 * u),), 3 * k)
    d.text((mitte[0], y0 + 106 * k), zeile2, font=f('fraunces-600.ttf', 54 * k), fill=WALD + (int(255 * u),), anchor='mm')
    c.paste(Image.alpha_composite(c.convert('RGBA'), lay).convert('RGB'))


def video(clip, W, H, preis, pfad, vorschau=None, st=SETS['little_princess']):
    SET_TITEL = st['titel']
    frames = clip_frames(clip)
    fh, fw = frames.shape[1:3]
    hoch = H / W > fh / fw                       # 9:16: Ausschnitt schmaler als der Clip -> Schwenk
    set_bild = Image.open(SET_BILD(st)).convert('RGB')
    teile = [(freistellen(os.path.join(ET(st), f"{st['ordner']}_{n}.jpg")), lab) for n, lab in st['teile']]
    n = len(teile)
    t_set = T_CLIP + 0.35; t_teile = t_set + T_SET; t_end = t_teile + n * T_TEIL + 0.3
    dauer = t_end + T_END
    k = W / 1080
    oben = 300 if hoch else 70                   # 9:16: Instagram-Kopfzeile frei lassen
    boxes = raster(n, W, oben + 210 * k, H - (640 if hoch else 230) * k, pro=3 if hoch else 4)
    # Etikett auf dem Video: nie ueber dem Babygesicht. 9:16 ueber den Beinen (unter dem Gesicht, ueber der
    # Instagram-Fusszeile), 4:5 oben rechts auf dem Bettlaken
    if hoch:
        pos_etikett = (W / 2, 1250)
    elif st['etikett_4x5'] == 'mitte':
        pos_etikett = (W / 2, H * 0.58)
    elif st['etikett_4x5'] == 'unten':
        pos_etikett = (W / 2, H - 60 * k - 80 * k)
    else:
        pos_etikett = (W - 50 * k - 310 * k, 30 * k + 80 * k)

    def clip_bild(t):
        a = frames[min(len(frames) - 1, int(t * FPS))]
        im = Image.fromarray(a)
        if hoch:
            cw = fh * W / H
            u = ease(t / T_CLIP) if t < T_CLIP else 1
            if st['kamera'] == 'schwenk':
                x = 0.02 * fw + u * (fw - cw - 0.02 * fw)      # vom Baby zum Schmusetuch
                im = im.crop((round(x), 0, round(x + cw), fh))
            else:                                             # Mitte, langsam 6 % naeher
                z = 1 + 0.06 * u; w2, h2 = cw / z, fh / z
                im = im.crop((round((fw - w2) / 2), round((fh - h2) * 0.3), round((fw + w2) / 2), round((fh - h2) * 0.3 + h2)))
        else:
            ch = fw * H / W
            y = (fh - ch) / 2
            im = im.crop((0, round(y), fw, round(y + ch)))
        im = im.resize((W, H), Image.LANCZOS)
        return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))

    def bild(t):
        if t < T_CLIP:
            c = clip_bild(t)
            u1 = ease((t - 0.3) / 0.5) * (1 - ease((t - 2.9) / 0.3))
            u2 = ease((t - 3.2) / 0.5) * (1 - ease((t - T_CLIP + 0.35) / 0.3))
            etikett(c, pos_etikett, 'NEU BEI SUNNOZY' if preis else 'COMING SOON', 'Set ' + SET_TITEL, u1, W)
            etikett(c, pos_etikett, 'ERSTAUSSTATTUNG', 'Für die ersten Wochen', u2, W)
            return c
        if t < t_set:                            # weiche Blende Video -> Creme
            u = ease((t - T_CLIP) / 0.35)
            return Image.blend(clip_bild(T_CLIP - 0.04), Image.new('RGB', (W, H), CREME), u)
        c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
        if t < t_teile:                          # ganzes Set
            u = ease((t - t_set) / 0.4)
            d.text((W / 2, oben + 70 * k), 'Was steckt drin?', font=f('fraunces-600.ttf', 84 * k), fill=WALD, anchor='mm')
            gesperrt(d, (W / 2, oben + 150 * k), 'ERSTAUSSTATTUNG ' + SET_TITEL.upper(), f('nunitosans-700.ttf', 24 * k), SALBEI, 3 * k)
            gross = (W - 80 * k) * (1 + 0.03 * (t - t_set) / T_SET)
            gross = min(gross, H - oben - 380 * k)
            im = set_bild.resize((round(gross), round(gross)), Image.LANCZOS)
            if u < 1:
                im = Image.blend(Image.new('RGB', im.size, (255, 255, 255)), im, u)
            multiply(c, im, (int((W - im.width) / 2), int(oben + 210 * k + (H - oben - 210 * k - (300 if hoch else 60) * k - im.height) / 2)))
            return c
        fertig = t >= t_end
        kk = min(n, int((t - t_teile) / T_TEIL) + 1)
        if fertig:
            d.text((W / 2, oben + 95 * k), 'Alles drin.', font=f('fraunces-600.ttf', 96 * k), fill=WALD, anchor='mm')
        else:
            gesperrt(d, (W / 2, oben + 70 * k), 'ERSTAUSSTATTUNG ' + SET_TITEL.upper(), f('nunitosans-700.ttf', 24 * k), SALBEI, 3 * k)
            d.text((W / 2, oben + 140 * k), f'{kk} von {n}  ·  {teile[kk - 1][1]}', font=f('nunitosans-700.ttf', 32 * k), fill=GRAU, anchor='mm')
        for i in range(n):
            ti = t - (t_teile + i * T_TEIL)
            if ti >= 0:
                kachel(c, teile[i][0], teile[i][1], boxes[i], alpha=ease(ti / 0.25), skala=0.86 + 0.14 * ease(ti / 0.3), schrift=22 * k)
        if fertig:
            d = ImageDraw.Draw(c)
            u = ease((t - t_end) / 0.4)
            mix = lambda col: tuple(int(CREME[j] + (col[j] - CREME[j]) * u) for j in range(3))
            y = boxes[-1][1] + boxes[-1][3] + 70 * k
            zeile = f'{n} Teile  ·  CHF {preis}' if preis else f'{n} Teile, fertig aufeinander abgestimmt'
            d.text((W / 2, y), zeile, font=f('nunitosans-700.ttf', 40 * k), fill=mix(WALD), anchor='mm')
            if not preis:                        # noch nicht im Shop: Stempel «COMING SOON»
                fs = f('nunitosans-800.ttf', 30 * k); txt = 'COMING SOON'; sp = 6 * k
                tw = sum(d.textlength(ch, font=fs) for ch in txt) + sp * (len(txt) - 1)
                bx0, by0 = W / 2 - tw / 2 - 34 * k, y + 50 * k
                d.rectangle([bx0, by0, W - bx0, by0 + 64 * k], fill=mix(WALD))
                gesperrt(d, (W / 2, by0 + 33 * k), txt, fs, mix(CREME) if u > 0.5 else mix(WALD), sp)
                y += 104 * k
            unten = 'Gratisversand ab CHF 50  ·  sunnozy.ch' if preis else 'Bald auf sunnozy.ch  ·  Gratisversand ab CHF 50'
            d.text((W / 2, y + 58 * k), unten, font=f('nunitosans-400.ttf', 28 * k), fill=mix(GRAU), anchor='mm')
            lg = load_logo(int(230 * k)); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * u)))
            c.paste(lg, (int((W - lg.width) / 2), int(y + 105 * k)), lg)
        return c

    if vorschau:                                 # nur Einzelbilder zum Pruefen
        return [bild(t) for t in vorschau]
    tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(round(dauer * FPS)):
        enc.stdin.write(bild(i / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad + '.mp4'], check=True)
    os.remove(tmp)
    bild(1.5).save(pfad + '_standbild.jpg', quality=93)
    print(os.path.basename(pfad), f'{dauer:.1f} s', flush=True)


if __name__ == '__main__':
    clip, out = sys.argv[1:3]
    preis = next((a.split('=')[1] for a in sys.argv[3:] if a.startswith('--preis=')), '')
    st = dict(SETS[next((a.split('=')[1] for a in sys.argv[3:] if a.startswith('--set=')), 'little_princess')])
    for a in sys.argv[3:]:                       # pro Clip anpassbar: --kamera=mitte, --etikett_4x5=unten
        if a.startswith('--kamera=') or a.startswith('--etikett_4x5='):
            key, val = a[2:].split('='); st[key] = val
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    video(clip, 1080, 1920, preis, out + '_9x16', st=st)
    video(clip, 1080, 1350, preis, out + '_4x5', st=st)
