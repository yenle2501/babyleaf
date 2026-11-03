"""Stop-Motion-Reels der Weihnachts-Geschenkboxen nach dem Pinterest-Pin der Nutzerin (03.11.2026, «Bold gift box
packaging»): kräftige Farbflächen, eingesetzte Fläche (Quadrat, Rundbogen), die Box hüpft, die Teile springen einzeln
heraus, offene Box im Rundbogen, Schlussbild mit Preis.

    python3 tools/make_stopmotion_reels.py                # alle 9 Boxen
    python3 tools/make_stopmotion_reels.py dino dinosaur  # einzelne

Teile: Set-Fotos aus dem Shop (weisser Hintergrund, hier freigestellt), die freigestellte rote Box mit sunnozy-Band
(Vorlage der Nutzerin, Canva-Freisteller), die echte Weihnachtskarte (Druckvorlage) und die offene Box aus rote-box/komposit/.
Keine echten Handyfotos. Bewegung im Stop-Motion-Takt (8 Bilder pro Sekunde), Video 30 fps, Musik Alex Morgan (Pixabay).
Ausgabe: posts/kampagne-weihnachtsbox/rote-box/stopmotion/stopmotion_<box>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
RB = os.path.join(POSTS, 'kampagne-weihnachtsbox', 'rote-box')
SM = os.path.join(RB, 'stopmotion'); TEILE = os.path.join(SM, 'teile')
W, H, FPS, TAKT = 1080, 1920, 30, 8
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
ROT, ROSA, GRUEN, CREME, EIS, DUNKEL = (176, 24, 44), (246, 196, 205), (31, 86, 61), (248, 239, 228), (204, 232, 230), (40, 30, 30)

BOX = {  # key: (Name, Inhalt, Preis, Bodys-Datei, Unterteil-Datei)
    'mum_dad_me': ('«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90', 'bodys_mum_dad_me.jpg', 'unten_leggings.jpg'),
    'lovely_little_girl': ('«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90', 'bodys_lovely_little_girl.jpg', 'unten_leggings.jpg'),
    'growing_up_strong': ('«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90', 'bodys_growing_up_strong.jpg', 'unten_jogginghosen.jpg'),
    'i_love_my_mummy': ('«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90', 'bodys_i_love_my_mummy.jpg', 'unten_halstuecher.png'),
    'dino': ('«Dino»', '3 Bodys + 3 Mulltücher', '39.90', 'bodys_dino.jpg', 'unten_mull_blau.jpg'),
    'dinosaur': ('«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90', 'bodys_dinosaur.jpg', 'unten_jogginghosen.jpg'),
    'little_one': ('«Little One»', '5 Bodys + 3 Mulltücher', '44.90', 'bodys_little_one.jpg', 'unten_mull_gruen.jpg'),
    'i_like_flying': ('«I like flying»', '3 Bodys + 5 Leggings', '39.90', 'bodys_i_like_flying.jpg', 'unten_leggings.jpg'),
    'little_one_jogginghosen': ('«Little One»', '5 Bodys + 5 Jogginghosen', '42.90', 'bodys_little_one.jpg', 'unten_jogginghosen.jpg'),
}


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


_c = {}
def freisteller(datei):
    """Weissen Hintergrund vom Rand her entfernen (Flood-Fill), Kante weich."""
    if datei in _c:
        return _c[datei]
    p = os.path.join(TEILE, datei)
    im = Image.open(p)
    if im.mode == 'RGBA' and datei.endswith('.png') and np.asarray(im)[..., 3].min() < 250:
        out = im
    else:
        rgb = im.convert('RGB'); a = np.asarray(rgb).astype(int)
        hell = (a.min(axis=2) > 249).astype(np.uint8)
        # vom Rand aus zusammenhängendes Weiss = Hintergrund (Weiss im Kleid bleibt)
        import cv2
        ff = hell.copy(); m2 = np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8)
        for xy in [(0, 0), (ff.shape[1] - 1, 0), (0, ff.shape[0] - 1), (ff.shape[1] - 1, ff.shape[0] - 1)]:
            if ff[xy[1], xy[0]] == 1:
                cv2.floodFill(ff, m2, xy, 2)
        bg = ff == 2
        alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
        out = rgb.convert('RGBA'); out.putalpha(alpha)
    out = out.crop(out.getbbox())
    _c[datei] = out
    return out


def karte():
    if 'karte' not in _c:
        k = Image.open(os.path.join(POSTS, 'kampagne-weihnachtsbox', 'karte', 'karte_vorne_freigestellt.png')).convert('RGBA')
        _c['karte'] = k.crop(k.getbbox())
    return _c['karte']


def logo(breite, farbe=(24, 24, 24)):
    L = Image.open(os.path.join(ROOT, 'logo-sunnozy-gross.png')).convert('RGBA')
    if farbe != (24, 24, 24):
        f = Image.new('RGBA', L.size, farbe + (0,)); f.putalpha(L.getchannel('A')); L = f
    s = breite / L.width; return L.resize((breite, round(L.height * s)), Image.LANCZOS)


def setzen(c, teil, cx, cy, hoehe, winkel=0, schatten=True, skal=1.0):
    t = teil.resize((max(1, round(teil.width * hoehe * skal / teil.height)), max(1, round(hoehe * skal))), Image.BILINEAR)
    if winkel:
        t = t.rotate(winkel, Image.BICUBIC, expand=True)
    x, y = int(cx - t.width / 2), int(cy - t.height / 2)
    if schatten:
        s = Image.new('RGBA', t.size, (30, 10, 10, 0)); s.putalpha(t.getchannel('A').point(lambda v: v * 0.35))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); lay.alpha_composite(s, (max(0, x + 14), max(0, y + 22)))
        c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))
    c.paste(t, (x, y), t)


def stop(t):
    """Zeit auf den Stop-Motion-Takt runden (8 Bilder pro Sekunde)."""
    return int(t * TAKT) / TAKT


def wackel(seed, t, stark=1.0):
    r = random.Random(f'{seed}-{int(t * TAKT)}')
    return r.uniform(-6, 6) * stark, r.uniform(-6, 6) * stark, r.uniform(-2.5, 2.5) * stark


def txt(c, xy, text, groesse, farbe, font='fraunces-400.ttf', anchor='ms'):
    ImageDraw.Draw(c).text(xy, text, font=F(font, groesse), fill=farbe, anchor=anchor)


def szene_hops(t, key):
    """Rote Fläche, rosa Quadrat, die Box hüpft."""
    c = Image.new('RGBA', (W, H), ROT + (255,)); d = ImageDraw.Draw(c)
    d.rectangle((90, 420, W - 90, 420 + 900), fill=ROSA)
    ts = stop(t); hops = abs(np.sin(ts * np.pi * 1.6)) * 70
    dx, dy, dw = wackel('hops', ts, 0.6)
    setzen(c, freisteller('box_zu.png'), W / 2 + dx, 870 - hops + dy, 700, dw + np.sin(ts * 5) * 4)
    txt(c, (W / 2, 300), 'Weihnachts-Geschenkbox', 70, CREME)
    txt(c, (W / 2, 1450), BOX[key][0], 64, CREME)
    return c


def szene_teile(t, key, dauer):
    """Rosa Fläche von oben: Box oben, Teile springen nacheinander heraus."""
    c = Image.new('RGBA', (W, H), ROSA + (255,)); ts = stop(t)
    dx, dy, dw = wackel('box', ts, 0.4)
    setzen(c, freisteller('box_zu.png'), 540 + dx, 640 + dy, 540, -8 + dw)
    name, inh, preis, bodys, unten = BOX[key]
    teile = [(freisteller(bodys), 300, 1250, 540, 6), (freisteller(unten), 790, 1300, 540, -7), (karte(), 560, 1640, 280, -14)]
    takt = (dauer - 0.6) / len(teile)
    for i, (teil, x, y, h, w) in enumerate(teile):
        t0 = 0.4 + i * takt
        if ts < t0:
            continue
        k = ts - t0
        skal = 1.18 if k < 1 / TAKT else (0.94 if k < 2 / TAKT else 1.0)        # Stop-Motion-«Plopp»
        ddx, ddy, ddw = wackel(f'teil{i}', ts, 0.35)
        setzen(c, teil, x + ddx, y + ddy, h, w + ddw, skal=skal)
    zeilen = [z.strip() for z in inh.split('+')]
    n = min(len(zeilen), int((ts - 0.4) / takt) + 1) if ts >= 0.4 else 0
    for i in range(n):
        txt(c, (W / 2, 160 + i * 70), zeilen[i], 58, ROT, 'fraunces-600.ttf')
    return c


def szene_bogen(t, key):
    """Grüne Fläche, cremefarbener Rundbogen mit der offenen Box."""
    c = Image.new('RGBA', (W, H), GRUEN + (255,)); ts = stop(t)
    bx0, by0, bx1, by1 = 110, 360, W - 110, 1540
    m = Image.new('L', (W, H), 0); dm = ImageDraw.Draw(m)
    r = (bx1 - bx0) // 2
    dm.rectangle((bx0, by0 + r, bx1, by1), fill=255); dm.ellipse((bx0, by0, bx1, by0 + 2 * r), fill=255)
    bogen = Image.new('RGBA', (W, H), CREME + (255,)); c.paste(bogen, (0, 0), m)
    k = Image.open(os.path.join(RB, 'komposit', key + '.jpg')).convert('RGB')
    z = 1.0 + 0.04 * ease(ts / 2.5); bw = round((bx1 - bx0 - 60) * z); bh = round(k.height * bw / k.width)
    k = k.resize((bw, bh), Image.BILINEAR)
    px, py = (W - bw) // 2, by1 - bh - 40
    c.paste(k, (px, py), m.crop((px, py, px + bw, py + bh)))         # nur innerhalb des Rundbogens
    txt(c, (W / 2, 220), 'Alles drin.', 84, CREME)
    txt(c, (W / 2, 1660), 'Fertig verpackt mit Karte', 48, CREME, 'nunitosans-700.ttf')
    return c


def szene_ende(t, key):
    """Eisblaue Fläche, Box, Name, Preis, Logo."""
    c = Image.new('RGBA', (W, H), EIS + (255,)); d = ImageDraw.Draw(c); ts = stop(t)
    d.rectangle((90, 300, W - 90, 1180), fill=(250, 246, 240))
    dx, dy, dw = wackel('ende', ts, 0.3)
    setzen(c, freisteller('box_zu.png'), W / 2 + dx, 740 + dy, 760, -5 + dw)
    name, inh, preis = BOX[key][:3]
    txt(c, (W / 2, 1300), name, 72, DUNKEL)
    txt(c, (W / 2, 1365), inh, 40, (90, 84, 80), 'nunitosans-600.ttf')
    fo = F('nunitosans-800.ttf', 60); tx = f'CHF {preis}'; tw = d.textlength(tx, font=fo)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, 1415, W / 2 + tw / 2 + 30, 1500), 18, fill=(17, 17, 17))
    d.text((W / 2, 1478), tx, font=fo, fill=(255, 255, 255), anchor='ms')
    L = logo(380); c.alpha_composite(L, ((W - L.width) // 2, 160))
    txt(c, (W / 2, 1580), 'Jetzt auf sunnozy.ch', 44, ROT, 'fraunces-600.ttf')
    return c


SZENEN = [(2.2, 'hops'), (4.2, 'teile'), (2.6, 'bogen'), (2.8, 'ende')]


def reel(key):
    os.makedirs(SM, exist_ok=True)
    pfad = os.path.join(SM, f'stopmotion_{key}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = 0; titel = None; letzt = None; letzt_t = None
    for dauer, art in SZENEN:
        for j in range(int(dauer * FPS)):
            t = j / FPS
            if letzt is not None and stop(t) == letzt_t:      # Stop-Motion: Bild nur im Takt neu
                fr = letzt
            else:
                c = {'hops': lambda: szene_hops(t, key), 'teile': lambda: szene_teile(t, key, dauer),
                     'bogen': lambda: szene_bogen(t, key), 'ende': lambda: szene_ende(t, key)}[art]()
                fr = c.convert('RGB'); letzt, letzt_t = fr, stop(t)
            if art == 'teile' and j == int(3.6 * FPS):
                titel = fr
            enc.stdin.write(fr.tobytes()); n += 1
        letzt = None
    enc.stdin.close(); enc.wait()
    d = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '14', '-i', os.path.join(POSTS, 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3'),
                    '-t', f'{d:.2f}', '-af', f'loudnorm=I=-12:TP=-1:LRA=11,afade=t=in:d=0.2,afade=t=out:st={d - 0.7:.2f}:d=0.7,aresample=44100',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp); titel.save(pfad.replace('_9x16.mp4', '_titelbild.jpg'), quality=92)
    print(os.path.basename(pfad), f'{d:.1f} s')


if __name__ == '__main__':
    for k in (sys.argv[1:] or list(BOX)):
        reel(k)
