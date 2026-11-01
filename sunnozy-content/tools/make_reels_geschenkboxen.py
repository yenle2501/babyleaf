"""6 Reels (9:16, Instagram, Facebook, TikTok) und Foto-Posts für die Weihnachts-Geschenkboxen in der roten sunnozy-Box.

    python3 tools/make_reels_geschenkboxen.py            # alle Reels und Fotos
    python3 tools/make_reels_geschenkboxen.py 2 4        # nur Reel 2 und 4
    python3 tools/make_reels_geschenkboxen.py fotos      # nur die Foto-Posts

Bilder: echte Handyfotos der Nutzerin (posts/produktfotos-geschenkbox-weihnachten/quelle/, nur die ohne fremde Marken,
foto7 ohne die Tastatur rechts) und die Box-Bilder aus rote-box/komposit/ (Inhalt mit KI erstellt).
Text liegt im sicheren Bereich für TikTok und Reels: oben ab 250 px, nicht im unteren Viertel, rechts frei für die Knöpfe.
Schrift Fraunces + Nunito Sans (keine Schreibschrift). Musik: Alex Morgan (Pixabay), Lautheit normalisiert.
Ausgabe: posts/kampagne-weihnachtsbox/rote-box/reels/ und rote-box/fotos-posts/
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, 'posts')
RB = os.path.join(POSTS, 'kampagne-weihnachtsbox', 'rote-box')
Q = os.path.join(POSTS, 'produktfotos-geschenkbox-weihnachten', 'quelle')
OUT = os.path.join(RB, 'reels'); FOTOS = os.path.join(RB, 'fotos-posts')
MUSIK = {1: 'alex-morgan_heartwarming-story.mp3', 2: 'alex-morgan_no-copyright-music.mp3'}
W, H, FPS, BLENDE = 1080, 1920, 30, 0.35
DUNKEL, GRAU, ROT, WEISS = (44, 36, 34), (112, 104, 100), (168, 24, 32), (255, 255, 255)
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))

BOX = {  # key: (Name, Inhalt, Preis)
    'mum_dad_me': ('«Mum Dad Me»', '5 Bodys + 5 Leggings', '42.90'),
    'lovely_little_girl': ('«Lovely Little Girl»', '3 Bodys + 5 Leggings', '39.90'),
    'growing_up_strong': ('«Growing up strong»', '5 Bodys + 5 Jogginghosen', '42.90'),
    'i_love_my_mummy': ('«I love my Mummy»', '3 Bodys + 3 Halstücher', '29.90'),
    'dino': ('«Dino»', '3 Bodys + 3 Mulltücher', '39.90'),
    'dinosaur': ('«Dinosaur»', '5 Bodys + 5 Jogginghosen', '42.90'),
    'little_one': ('«Little One»', '5 Bodys + 3 Mulltücher', '44.90'),
    'i_like_flying': ('«I like flying»', '3 Bodys + 5 Leggings', '39.90'),
    'little_one_jogginghosen': ('«Little One»', '5 Bodys + 5 Jogginghosen', '42.90'),
}
ALLE = list(BOX)


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


def logo(width, col):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox()); return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


_cache = {}
def bild(name):
    if name not in _cache:
        if name.startswith('foto'):
            im = Image.open(os.path.join(Q, name + '.jpg')).convert('RGB')
            if name == 'foto7':                       # rechts Tastatur mit Fremdmarke: weg
                im = im.crop((0, 0, int(im.width * 0.80), im.height))
        elif name == 'zu':
            im = Image.open(os.path.join(RB, 'vorlage', 'vorlage_zu.jpg')).convert('RGB')
        else:
            im = Image.open(os.path.join(RB, 'komposit', name + '.jpg')).convert('RGB')
        _cache[name] = im
    return _cache[name]


def voll(im, t, dauer, zoom=(1.0, 1.08), fy=0.5):
    """Foto füllt 9:16, langsamer Zoom (Ken Burns)."""
    z = zoom[0] + (zoom[1] - zoom[0]) * t / max(dauer, 0.01)
    s = max(W / im.width, H / im.height) * z
    bw, bh = W / s, H / s
    cx, cy = im.width / 2, min(max(fy * im.height, bh / 2), im.height - bh / 2)
    return im.resize((W, H), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')


_bg = {}
def hintergrund(im):
    k = id(im)
    if k not in _bg:
        a = np.asarray(im.resize((60, 60))).astype(float)
        oben, unten = a[:3].reshape(-1, 3).mean(0), a[-3:].reshape(-1, 3).mean(0)
        t = np.linspace(0, 1, H)[:, None, None]
        _bg[k] = Image.fromarray(((1 - t) * oben + t * unten).repeat(W, 1).clip(0, 255).astype(np.uint8)).convert('RGBA')
    return _bg[k].copy()


def box_frame(key, t, dauer, oben=None, nummer=None, preis=True):
    """Box-Bild auf passendem Studio-Grau, Text oben (sicherer Bereich)."""
    im = bild(key); c = hintergrund(im)
    z = 1.0 + 0.045 * t / max(dauer, 0.01); b = round(1080 * z); h = round(im.height * b / im.width)
    klein = im.resize((b, h), Image.BILINEAR)
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rectangle((40, 40, b - 40, h - 40), fill=255)
    c.paste(klein, ((W - b) // 2, 560 - (h - round(im.height * 1080 / im.width)) // 2), m.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(c); name, inhalt, pr = BOX[key]
    e = ease(t / 0.4); a = int(255 * e)
    y = 300
    if nummer is not None:
        d.text((W / 2, y - 10), str(nummer), font=F('fraunces-600.ttf', 110), fill=ROT + (a,), anchor='ms'); y += 70
    elif oben:
        d.text((W / 2, y - 20), oben, font=F('nunitosans-700.ttf', 30), fill=ROT + (a,), anchor='ms'); y += 40
    d.text((W / 2, y + 62), name, font=F('fraunces-400.ttf', 80), fill=DUNKEL + (a,), anchor='ms')
    zeile = f'{inhalt}  ·  CHF {pr}' if preis else inhalt
    d.text((W / 2, y + 126), zeile, font=F('nunitosans-600.ttf', 40), fill=GRAU + (a,), anchor='ms')
    return c


def text_mitte(c, zeilen, alpha, y=1150, groesse=78, klein=None):
    """Weisse Fraunces mit weichem Schatten über einem dunklen Verlauf, im sicheren Bereich."""
    if alpha <= 0:
        return c
    g = np.zeros((H, 1), np.float32); g[800:1600, 0] = np.sin(np.linspace(0, np.pi, 800)) * 0.55
    v = Image.fromarray((g * 255 * alpha).astype(np.uint8)).resize((W, H))
    dk = Image.new('RGBA', (W, H), (25, 16, 12, 0)); dk.putalpha(v); c.alpha_composite(dk)
    fo = F('fraunces-400.ttf', groesse); lh = groesse * 1.18
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    y0 = y - (len(zeilen) - 1) * lh / 2
    for i, z in enumerate(zeilen):
        p = (W / 2, y0 + i * lh)
        ds.text((p[0] + 2, p[1] + 3), z, font=fo, fill=(15, 10, 8, int(210 * alpha)), anchor='mm', stroke_width=6, stroke_fill=(15, 10, 8, int(210 * alpha)))
        dt.text(p, z, font=fo, fill=WEISS + (int(255 * alpha),), anchor='mm')
    if klein:
        p = (W / 2, y0 + len(zeilen) * lh + 10)
        ds.text(p, klein, font=F('nunitosans-700.ttf', 36), fill=(15, 10, 8, int(200 * alpha)), anchor='mm', stroke_width=5, stroke_fill=(15, 10, 8, int(200 * alpha)))
        dt.text(p, klein, font=F('nunitosans-700.ttf', 36), fill=WEISS + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7))); c.alpha_composite(tx)
    return c


def foto_frame(name, t, dauer, zeilen, klein=None, zoom=(1.0, 1.08), fy=0.5):
    c = voll(bild(name), t, dauer, zoom, fy)
    return text_mitte(c, zeilen, ease((t - 0.15) / 0.4), klein=klein)


def endkarte(t, dauer, zeile1, zeile2, zeile3='Jetzt auf sunnozy.ch'):
    im = bild('zu'); c = hintergrund(bild('growing_up_strong'))
    s = 0.72 + 0.02 * t / dauer; b = round(im.width * s); h = round(im.height * s)
    k = im.resize((b, h), Image.BILINEAR)
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, b, h), 28, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle(((W - b) // 2 + 10, 300 + 18, (W + b) // 2 + 10, 300 + h + 18), 28, fill=(40, 30, 25, 70))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22))); c.paste(k, ((W - b) // 2, 300), m)
    d = ImageDraw.Draw(c); a = int(255 * ease(t / 0.4)); y = 300 + h + 110
    d.text((W / 2, y - 20), zeile1, font=F('fraunces-400.ttf', 74), fill=DUNKEL + (a,), anchor='ms')
    d.text((W / 2, y + 50), zeile2, font=F('nunitosans-600.ttf', 40), fill=GRAU + (a,), anchor='ms')
    d.text((W / 2, y + 125), zeile3, font=F('fraunces-600.ttf', 54), fill=ROT + (a,), anchor='ms')
    L = logo(210, (122, 108, 104)); c.alpha_composite(L, ((W - L.width) // 2, 175))
    return c


# Reels: Liste von Segmenten (Dauer, Funktion(t, dauer) -> RGBA)
def S(dauer, fn):
    return (dauer, fn)


REELS = {
    1: dict(datei='reel_1_so_kommt_sie_an', musik=1, seg=[
        S(2.4, lambda t, d: foto_frame('foto8', t, d, ['So kommt Deine', 'Geschenkbox an'], zoom=(1.0, 1.10))),
        S(2.0, lambda t, d: foto_frame('foto6', t, d, ['Blumen-Seidenpapier', 'und unser Sticker'], zoom=(1.12, 1.04), fy=0.55)),
        S(2.3, lambda t, d: foto_frame('foto9', t, d, ['Und darin:', 'ein ganzes Set'], zoom=(1.0, 1.08), fy=0.45)),
        S(2.3, lambda t, d: foto_frame('foto7', t, d, ['5 Bodys + 5 Jogginghosen'], klein='«Growing up strong» · CHF 42.90', zoom=(1.05, 1.13))),
        S(2.6, lambda t, d: endkarte(t, d, 'Fertig verpackt', '9 Boxen ab CHF 29.90, mit Karte')),
    ]),
    2: dict(datei='reel_2_welche_box', musik=2, seg=[
        S(2.0, lambda t, d: foto_frame('foto8', t, d, ['Welche Box', 'würdest Du schenken?'], zoom=(1.0, 1.06))),
        *[S(1.15, (lambda k, n: lambda t, d: box_frame(k, t, d, nummer=n))(k, i + 1)) for i, k in enumerate(ALLE)],
        S(2.6, lambda t, d: endkarte(t, d, 'Schreib Deine Zahl', 'in die Kommentare', '9 Boxen auf sunnozy.ch')),
    ]),
    3: dict(datei='reel_3_fuer_kleine_maedchen', musik=1, seg=[
        S(2.0, lambda t, d: foto_frame('foto8', t, d, ['Geschenkideen', 'für kleine Mädchen'], zoom=(1.0, 1.06))),
        *[S(2.2, (lambda k: lambda t, d: box_frame(k, t, d, oben='WEIHNACHTS-GESCHENKBOX'))(k)) for k in ['mum_dad_me', 'lovely_little_girl', 'i_like_flying']],
        S(2.5, lambda t, d: endkarte(t, d, 'Fertig verpackt mit Karte', 'Grössen 0–9 Monate')),
    ]),
    4: dict(datei='reel_4_fuer_kleine_jungs', musik=2, seg=[
        S(2.0, lambda t, d: foto_frame('foto8', t, d, ['Geschenkideen', 'für kleine Jungs'], zoom=(1.0, 1.06))),
        *[S(2.2, (lambda k: lambda t, d: box_frame(k, t, d, oben='WEIHNACHTS-GESCHENKBOX'))(k)) for k in ['dino', 'dinosaur', 'growing_up_strong']],
        S(2.5, lambda t, d: endkarte(t, d, 'Fertig verpackt mit Karte', 'Grössen 0–9 Monate')),
    ]),
    5: dict(datei='reel_5_little_one_und_mummy', musik=1, seg=[
        S(2.0, lambda t, d: foto_frame('foto9', t, d, ['Zarte Farben,', 'die zu allem passen'], zoom=(1.0, 1.06), fy=0.45)),
        *[S(2.2, (lambda k: lambda t, d: box_frame(k, t, d, oben='WEIHNACHTS-GESCHENKBOX'))(k)) for k in ['little_one', 'little_one_jogginghosen', 'i_love_my_mummy']],
        S(2.5, lambda t, d: endkarte(t, d, 'Ein Set in jeder Box', 'aus weicher Baumwolle')),
    ]),
    6: dict(datei='reel_6_pov_gotti', musik=2, seg=[
        S(2.6, lambda t, d: foto_frame('foto8', t, d, ['POV: Du bist Gotti', 'und brauchst noch', 'ein Geschenk'], zoom=(1.12, 1.0))),
        S(2.2, lambda t, d: foto_frame('foto9', t, d, ['Box auf …'], zoom=(1.0, 1.08), fy=0.45)),
        S(2.2, lambda t, d: box_frame('growing_up_strong', t, d, oben='EIN GANZES SET DRIN')),
        S(2.2, lambda t, d: foto_frame('foto7', t, d, ['Weich, praktisch,', 'sofort anziehbar'], zoom=(1.0, 1.08))),
        S(2.6, lambda t, d: endkarte(t, d, 'Nur noch schenken', 'Fertig verpackt, ab CHF 29.90')),
    ]),
}


def render(nr):
    r = REELS[nr]; os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, r['datei'] + '_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    segs = r['seg']; nb = int(BLENDE * FPS)
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    total = 0; titel = None
    for i, (dauer, fn) in enumerate(segs):
        n = int(dauer * FPS)
        for j in range(n):
            t = j / FPS; c = fn(t, dauer)
            if i + 1 < len(segs) and j >= n - nb:          # Überblendung ins nächste Segment
                a = (j - (n - nb)) / nb
                c = Image.blend(c, segs[i + 1][1](0.0, segs[i + 1][0]), ease(a))
            fr = c.convert('RGB')
            if i == 0 and j == int(0.9 * FPS):
                titel = fr
            enc.stdin.write(fr.tobytes()); total += 1
    enc.stdin.close(); enc.wait()
    d = total / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(6 + 4 * nr), '-i', os.path.join(POSTS, 'reels', 'musik', MUSIK[r['musik']]), '-t', f'{d:.2f}',
                    '-af', f'loudnorm=I=-12:TP=-1:LRA=11,afade=t=in:d=0.3,afade=t=out:st={d - 0.8:.2f}:d=0.8,aresample=44100',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    titel.save(pfad.replace('_9x16.mp4', '_titelbild.jpg'), quality=92)
    print(os.path.basename(pfad), f'{d:.1f} s')


# ---------- Foto-Posts ----------
def deckblatt(W2, H2):
    im = bild('foto8'); s = max(W2 / im.width, H2 / im.height) * 1.04
    bw, bh = W2 / s, H2 / s; cx, cy = im.width / 2, im.height / 2
    c = im.resize((W2, H2), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')
    if True:
        g = np.zeros((H2, 1), np.float32); g[int(H2 * 0.55):, 0] = np.linspace(0, 0.62, H2 - int(H2 * 0.55))
        dk = Image.new('RGBA', (W2, H2), (25, 16, 12, 0)); dk.putalpha(Image.fromarray((g * 255).astype(np.uint8)).resize((W2, H2))); c.alpha_composite(dk)
        d = ImageDraw.Draw(c); y = H2 * 0.78
        d.text((W2 / 2, y - 70), 'WEIHNACHTS-GESCHENKBOXEN', font=F('nunitosans-700.ttf', 30), fill=WEISS, anchor='ms')
        d.text((W2 / 2, y + 20), 'Fertig verpackt.', font=F('fraunces-400.ttf', 86), fill=WEISS, anchor='ms')
        d.text((W2 / 2, y + 90), '9 Boxen ab CHF 29.90 · wisch weiter ›', font=F('nunitosans-600.ttf', 34), fill=WEISS, anchor='ms')
    return c.convert('RGB')


def echt_slide(W2, H2):
    im = bild('foto9'); s = max(W2 / im.width, H2 / im.height) * 1.02
    bw, bh = W2 / s, H2 / s; cx = im.width / 2; cy = min(max(im.height * 0.47, bh / 2), im.height - bh / 2)
    c = im.resize((W2, H2), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')
    g = np.zeros((H2, 1), np.float32); g[:int(H2 * 0.3), 0] = np.linspace(0.55, 0, int(H2 * 0.3))
    dk = Image.new('RGBA', (W2, H2), (25, 16, 12, 0)); dk.putalpha(Image.fromarray((g * 255).astype(np.uint8)).resize((W2, H2))); c.alpha_composite(dk)
    d = ImageDraw.Draw(c)
    d.text((W2 / 2, H2 * 0.09), 'So kommt sie bei Dir an', font=F('fraunces-400.ttf', 64), fill=WEISS, anchor='ms')
    d.text((W2 / 2, H2 * 0.09 + 56), 'Seidenpapier, Karte, ein ganzes Set', font=F('nunitosans-600.ttf', 32), fill=WEISS, anchor='ms')
    return c.convert('RGB')


def schluss_slide(W2, H2):
    c = endkarte(1.0, 1.0, 'Welche Box gefällt Dir?', 'Grössen 0–9 Monate · mit Weihnachtskarte', 'sunnozy.ch')
    if (W2, H2) == (W, H):
        return c.convert('RGB')
    s = H2 / H; k = c.resize((round(W * s), H2), Image.LANCZOS)
    out = hintergrund(bild('growing_up_strong')).resize((W2, H2)); out.paste(k, ((W2 - k.width) // 2, 0))
    return out.convert('RGB')


def fotos():
    ig = os.path.join(FOTOS, 'karussell-4x5'); tt = os.path.join(FOTOS, 'tiktok-fotos-9x16')
    for p in (ig, tt):
        os.makedirs(p, exist_ok=True)
        for f_ in os.listdir(p):
            os.remove(os.path.join(p, f_))
    reihe = ['mum_dad_me', 'lovely_little_girl', 'i_like_flying', 'dino', 'dinosaur', 'growing_up_strong', 'little_one', 'little_one_jogginghosen', 'i_love_my_mummy']
    deckblatt(1080, 1350).save(os.path.join(ig, '01_deckblatt.jpg'), quality=93)
    deckblatt(1080, 1920).save(os.path.join(tt, '01_deckblatt.jpg'), quality=93)
    for i, k in enumerate(reihe, 2):
        Image.open(os.path.join(RB, 'ads', f'feed_{k}_4x5.jpg')).save(os.path.join(ig, f'{i:02d}_{k}.jpg'), quality=93)
        Image.open(os.path.join(RB, 'ads', f'story_{k}_9x16.jpg')).save(os.path.join(tt, f'{i:02d}_{k}.jpg'), quality=93)
    echt_slide(1080, 1350).save(os.path.join(ig, '11_so_kommt_sie_an.jpg'), quality=93)
    echt_slide(1080, 1920).save(os.path.join(tt, '11_so_kommt_sie_an.jpg'), quality=93)
    schluss_slide(1080, 1350).save(os.path.join(ig, '12_schluss.jpg'), quality=93)
    schluss_slide(1080, 1920).save(os.path.join(tt, '12_schluss.jpg'), quality=93)
    fs = sorted(os.listdir(ig)); u = Image.new('RGB', (6 * 250 + 10, 2 * 315 + 10), 'white')
    for i, f_ in enumerate(fs):
        u.paste(Image.open(os.path.join(ig, f_)).resize((240, 300)), (10 + (i % 6) * 250, 10 + (i // 6) * 315))
    u.save(os.path.join(FOTOS, 'uebersicht_karussell.jpg'), quality=88)
    print('Fotos:', len(fs), 'Slides je Format')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or 'fotos' in args:
        fotos()
    nrs = [int(a) for a in args if a.isdigit()] or ([] if args == ['fotos'] else list(REELS))
    for n in nrs:
        render(n)
