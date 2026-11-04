"""Reels aus den Baby-Videos Runde 5 (posts/videos-baby/runde5, Grok, 04.11.2026) zum Vorplanen.

    python3 tools/make_reels_runde5.py            # alle
    python3 tools/make_reels_runde5.py box_dino   # eines

Machart wie die Baby-Reels: Clip füllt das Bild, Text ab Sekunde 0 (Cormorant, unteres Drittel), zweite Zeile
löst auf, dann Produktkarte, Schlusskarte, Loop ins erste Bild, ruhige Musik.
- Box-Reels: Schlusskarte mit Preis und Kurzlink direkt zur Box (wie tools/make_reels_box_schlaf.py).
- Set-Reels: Schlusskarte ohne Preis («auf sunnozy.ch»), damit sie auch nach dem Shop-Start passen.
Nicht verwendet (Safe Sleep): 02, 03, 09, 10 (Haarband/Decke beim schlafenden Baby), 05, 12, 13, 15, 31 (Plüschtier daneben).
Ausgabe: posts/reels/runde5/reel_<key>_9x16.mp4 + _titelbild.jpg; bearbeitete Clips: runde5/bearbeitet/<clip>.mp4
"""
import os, sys, subprocess
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_reels_box_schlaf as bx

W, H, FPS = m.W, m.H, m.FPS
P = m.POSTS
SRC = os.path.join(P, 'videos-baby', 'runde5')
BEA = os.path.join(SRC, 'bearbeitet')
OUT = os.path.join(P, 'reels', 'runde5')
CS = lambda d: os.path.join(P, 'coming-soon', d, 'shop', d + '_shop_ohne_logo.jpg')
PR = lambda s: os.path.join(P, 'produktfotos-set-praesentation', 'ohne_logo', f'set_{s}_quadratisch.jpg')
FILTER = 'hqdn3d=1.2:1.2:5:5,eq=contrast=1.04:saturation=1.04:brightness=0.01,colorbalance=rm=0.02:bm=-0.02,cas=0.45'


def seg(clip, von, bis, z0=1.0, z1=1.06, fx=0.5, fy=0.45, tempo=1.0):
    return dict(clip=clip, von=von, bis=bis, z=(z0, z1), f=(fx, fy), tempo=tempo)


BOX = lambda k, **kw: dict(art='box', box=k, **kw)
SET = lambda name, teile, bild, **kw: dict(art='set', name=name, teile=teile, bild=bild, **kw)

REELS = {
    # ---- Weihnachts-Geschenkboxen ----
    'box_dino': BOX('dino', segmente=[seg('40_box_dino_body', 0, 4.5), seg('40_box_dino_body', 6, 9, 1.18, 1.24, 0.5, 0.55), seg('40_box_dino_body', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['Wenn der Body', 'schon alles sagt'], ['«Daddy Mommy', 'love me»'], ['Box «Dino»,', 'fertig verpackt']]),
    'box_dinosaur': BOX('dinosaur', segmente=[seg('27_box_dinosaur_body_arm', 0, 4.5), seg('27_box_dinosaur_body_arm', 6, 9, 1.18, 1.24, 0.5, 0.55), seg('27_box_dinosaur_body_arm', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Grosi hat ihn', 'endlich im Arm'], ['und das Geschenk', 'trägt er schon'], ['Box «Dinosaur»', '5 Bodys + 5 Hosen']]),
    'box_growing_up_strong': BOX('growing_up_strong', segmente=[seg('29_box_growing_up_strong_body_D', 0, 4.5), seg('29_box_growing_up_strong_body_D', 6, 9, 1.18, 1.24, 0.5, 0.55), seg('29_box_growing_up_strong_body_D', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Götti schenkt', 'dieses Jahr Bodys'], ['weiche Ripp-Bodys', 'mit Hosen'], ['«Growing up strong»,', 'fertig verpackt']]),
    'box_lovely': BOX('lovely_little_girl', segmente=[seg('32_box_lovely_body_arm', 0, 4.5), seg('32_box_lovely_body_arm', 6, 9, 1.18, 1.24, 0.5, 0.55), seg('32_box_lovely_body_arm', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Ihr erstes Weihnachten', 'und Gotti hat vorgesorgt'], ['«Lovely»', 'in Lila und Rosa'], ['3 Bodys + 5 Leggings', 'in der roten Box']]),
    'box_mummy': BOX('i_love_my_mummy', segmente=[seg('33_box_mummy_halstuch_arm', 0, 4.5), seg('33_box_mummy_halstuch_arm', 6, 9, 1.18, 1.24, 0.5, 0.55), seg('33_box_mummy_halstuch_arm', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Mamas erstes', 'Weihnachten mit Baby'], ['Halstuch', '«I love my Mummy»'], ['3 Bodys + 3 Halstücher', 'fertig verpackt']]),
    # ---- Sets ----
    'weltall': SET('«Little One» Weltall', 'Wickelbody, Fusshose, Mütze', CS('weltall-hellblau'),
        segmente=[seg('01_weltall_hellblau', 0, 4.5), seg('01_weltall_hellblau', 6, 9, 1.2, 1.25, 0.5, 0.5), seg('01_weltall_hellblau', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Euer kleiner', 'Astronaut schläft'], ['Planeten und Sterne', 'von Kopf bis Fuss'], ['3 Teile', 'mit Mütze']]),
    'kirschen_smile': SET('Strampler «Kirschen»', '3 Strampler: Weinrot, Altrosa, Weiss', CS('strampler-kirschen'),
        segmente=[seg('06_smile_weinrot', 0, 4.5), seg('06_smile_weinrot', 6, 9, 1.15, 1.22, 0.5, 0.5), seg('37_kirschen_weiss', 1, 5, 1.0, 1.06, tempo=0.85)],
        texte=[['Weinrot', 'oder Kirschen?'], ['«Smile»', 'in Weinrot'], ['oder Weiss', 'mit Kirschen']]),
    'best_family': SET('«Best Family» Teddy', '8 Teile mit Teddy-Rassel', PR('best_family'),
        segmente=[seg('16_best_family', 0, 4), seg('20_best_family_lachen', 2, 5, 1.1, 1.16, 0.5, 0.45), seg('18_kapuzentuch_best_family', 2, 6, 1.0, 1.06, tempo=0.85)],
        texte=[['Dieses Lachen', 'am Morgen'], ['Mütze', 'mit Bärenohren'], ['und nach dem Bad', 'ins Kapuzentuch']]),
    'bauernhof': SET('«Bauernhof»', '8 Teile mit Tieren', PR('bauernhof'),
        segmente=[seg('08_happy_baby', 0, 4), seg('25_happy_baby_b', 3, 6, 1.12, 1.18, 0.5, 0.48), seg('17_kapuzentuch_happy_baby', 2, 6, 1.0, 1.06, tempo=0.85)],
        texte=[['Happy Baby', 'am Sonntag'], ['Body mit', 'Bauernhof-Tieren'], ['Kapuzentuch', 'im gleichen Muster']]),
    'born_2027_blau': SET('«Born in 2027»', '6 Teile in Hellblau', CS('born-in-2027-blau'),
        segmente=[seg('35_born_in_2027_blau', 0, 4.5), seg('35_born_in_2027_blau', 6, 9, 1.15, 1.2, 0.5, 0.5), seg('35_born_in_2027_blau', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['POV: Er kommt 2027', 'und hat schon sein Outfit'], ['«Born in 2027»', 'in Hellblau'], ['Body, Hose, Mütze', 'und mehr']]),
    'smile_salbeigruen': SET('«Smile» Salbeigrün', 'Strampler, Mütze, Kapuzentuch', CS('strampler-smile-gruen').replace('_ohne_logo', '') if not os.path.exists(CS('strampler-smile-gruen')) else CS('strampler-smile-gruen'),
        segmente=[seg('36_smile_salbeigruen', 0, 4.5), seg('36_smile_salbeigruen', 6, 9, 1.15, 1.22, 0.5, 0.5), seg('36_smile_salbeigruen', 10.5, 14, 1.0, 1.06, tempo=0.85)],
        texte=[['Du machst mich', 'jeden Tag glücklich'], ['«You make me happy»', 'in Salbeigrün'], ['Ripp-Strampler', 'mit Knotenmütze']]),
}


def bearbeiten(clip):
    os.makedirs(BEA, exist_ok=True)
    ziel = os.path.join(BEA, clip + '.mp4')
    if not os.path.exists(ziel):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(SRC, clip + '.mp4'), '-vf', FILTER, '-an',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', ziel], check=True)
    return ziel


def ausschnitt(im, z, fx, fy):
    s = max(W / im.width, H / im.height) * z
    w, h = im.width * s, im.height * s
    x = min(max(fx * w - W / 2, 0), w - W); y = min(max(fy * h - H / 2, 0), h - H)
    return im.resize((round(w), round(h)), Image.BICUBIC).crop((round(x), round(y), round(x) + W, round(y) + H)).convert('RGBA')


def set_karte(r, t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.5)
    im = Image.open(r['bild']).convert('RGB'); s = 940 / max(im.size) * (0.96 + 0.04 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 860 - im.height // 2))
    d.text((W / 2, 1400), r['name'], font=m.f(m.SERIF, 92 if len(r['name']) < 20 else 76), fill=m.WALD, anchor='mm')
    d.text((W / 2, 1490), r['teile'], font=m.f(m.SERIF_I, 50), fill=m.GRAU, anchor='mm')
    return c


def set_end(r):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 760), r['name'], font=m.f(m.SERIF, 100 if len(r['name']) < 20 else 82), fill=m.WALD, anchor='mm')
    d.text((W / 2, 870), r['teile'], font=m.f(m.SERIF_I, 52), fill=m.GRAU, anchor='mm')
    d.line((W / 2 - 70, 965, W / 2 + 70, 965), fill=(200, 192, 180), width=2)
    d.text((W / 2, 1050), 'auf sunnozy.ch', font=m.f(m.SERIF, 56), fill=m.WALD, anchor='mm')
    L = m.logo(250, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1250), L)
    return c


def reel(key, nr):
    r = dict(REELS[key])
    if r['art'] == 'box':
        r.update(bx.BOXEN[r['box']]); r['box'] = bx.BOX(r['box'])
        karte, end = (lambda t: bx.box_karte(r, t)), bx.end_karte(r)
    else:
        karte, end = (lambda t: set_karte(r, t)), set_end(r)
    teile, t0 = [], 0.0
    for sg, tx in zip(r['segmente'], r['texte']):
        fr = m.clip_frames(bearbeiten(sg['clip']), sg['von'], sg['bis'] + 0.2)
        dauer = (sg['bis'] - sg['von']) / sg['tempo']
        teile.append(dict(sg, start=t0, dauer=dauer, frames=fr, text=tx, karte=False)); t0 += dauer
    teile.append(dict(start=t0, dauer=2.6, fn=karte, karte=True)); t0 += 2.6
    teile.append(dict(start=t0, dauer=2.6, fn=lambda t: end, karte=True)); t0 += 2.6
    n = int(round(t0 * FPS)); nb = int(m.BLENDE * FPS)

    def bild(tl, t):
        if tl['karte']:
            return tl['fn'](t)
        fr = tl['frames']; p = t * tl['tempo'] * FPS
        i = min(int(p), len(fr) - 1); j = min(i + 1, len(fr) - 1); a = p - int(p)
        im = fr[i] if a < 0.05 or i == j else Image.blend(fr[i], fr[j], a)
        e = m.ease(t / tl['dauer']); z0, z1 = tl['z']
        return ausschnitt(im, z0 + (z1 - z0) * e, *tl['f'])

    def roh(s):
        idx = max(i for i, tl in enumerate(teile) if tl['start'] <= s + 1e-9)
        tl = teile[idx]; t = min(s - tl['start'], tl['dauer'] - 1e-3)
        c = bild(tl, t)
        if not tl['karte'] and tl['text']:
            m.text_unten(c, tl['text'], 1.0 if idx == 0 else min(1, t / 0.2))
        if idx + 1 < len(teile) and s > tl['start'] + tl['dauer'] - m.BLENDE:
            a = (s - (tl['start'] + tl['dauer'] - m.BLENDE)) / m.BLENDE
            c = Image.blend(c, bild(teile[idx + 1], 0), min(a, 1))
        return c

    erstes = roh(0)
    os.makedirs(OUT, exist_ok=True)
    datei = f'reel_{key}_9x16'
    pfad = os.path.join(OUT, datei + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        c = roh(i / FPS)
        if i >= n - nb:
            c = Image.blend(c, erstes, (i - (n - nb)) / nb)
        fr = c.convert('RGB')
        if i == int(0.6 * FPS):
            fr.save(os.path.join(OUT, datei + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    dauer = n / FPS
    musik = bx.MUSIK[nr % 2]; ab = 10 + (nr * 17) % 60
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', musik, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.5,afade=t=out:st={dauer - 1.3:.2f}:d=1.3,volume=0.8', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(REELS)
    for nr, k in enumerate(keys):
        reel(k, nr)
