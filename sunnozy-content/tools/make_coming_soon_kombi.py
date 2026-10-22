"""Zusammengeschnittene Coming-soon-Reels: mehrere KI-Babyclips, harte Schnitte, Zoom auf Details, Zeitlupe, Loop.

    python3 tools/make_coming_soon_kombi.py               # alle Reels aus REELS
    python3 tools/make_coming_soon_kombi.py vergleich     # nur eines

Ausgabe flach nach posts/reels/coming-soon/ (wie make_coming_soon_reels.py, gleiche Schrift Cormorant Garamond).
Nicht verwendet (Safe Sleep): little-princess baby_clip_d (Bauchlage), gaensebluemchen (Decke über dem Baby).

Segment: (clip, von, bis, tempo, (zoom0, zoom1), (fx0, fy0), (fx1, fy1))
  tempo < 1 = Zeitlupe; zoom 1 = Clip füllt 9:16; f = Bildpunkt in der Mitte (Anteil 0..1 der Clipbreite/-höhe)
  ('set', set) = Set-Karte, ('ende', set) = Schlusskarte, je mit Dauer als drittem Wert
Texte: (von_s, bis_s, zeilen) auf der Gesamtzeit; ('zahl', von, bis, '1', 'Name') für den Vergleich
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

CS, W, H, FPS = m.CS, m.W, m.H, m.FPS
CLIPS = {
    'bf_a': os.path.join(CS, 'best-family-teddy', 'original', 'baby_clip_a.mp4'),
    'bf_b': os.path.join(CS, 'best-family-teddy', 'original', 'baby_clip_b.mp4'),
    'bl_a': os.path.join(CS, 'blumen-musselin', 'original', 'baby_clip_a.mp4'),
    'bl_b': os.path.join(CS, 'blumen-musselin', 'original', 'baby_clip_b.mp4'),
    'lp_c': os.path.join(CS, 'little-princess', 'original', 'baby_clip_c.mp4'),
    'lp_e': os.path.join(CS, 'little-princess', 'original', 'baby_clip_e.mp4'),
}
SETS = {k: m.REELS[v] for k, v in (('bf', 'best_family_a'), ('bl', 'blumen_a'), ('lp', 'little_princess'))}
MITTE = (0.5, 0.5)
KOMMENTAR = 'Schreib 1, 2 oder 3 in die Kommentare'

REELS = {
    # Ein Baby, ein Teddy: Lächeln, Zoom auf die Stickerei, Umarmung in Zeitlupe, Set
    'best_family_kombi': dict(datei='reel_best_family_teddy_kombi_9x16', set='bf', segmente=[
        ('bf_a', 0.0, 2.2, 1.0, (1.0, 1.05), (0.5, 0.42), (0.5, 0.42)),
        ('bf_b', 0.5, 1.9, 1.0, (1.55, 1.7), (0.42, 0.44), (0.42, 0.46)),     # Stickerei (hier nicht verdeckt)
        ('bf_a', 5.0, 6.4, 1.0, (1.45, 1.55), (0.78, 0.55), (0.72, 0.52)),    # Teddy-Rassel
        ('bf_b', 4.0, 6.2, 0.7, (1.05, 1.2), (0.5, 0.42), (0.5, 0.38)),       # Umarmung, Zeitlupe
        ('bf_b', 0.6, 2.4, 1.0, (1.1, 1.0), (0.5, 0.4), MITTE),
        ('set', 'bf', 2.2), ('ende', 'bf', 1.8)],
        texte=[(0.0, 3.6, ['POV: Er entdeckt', 'seinen ersten Teddy']), (3.6, 5.0, ['Die Teddy-Rassel', 'ist im Set dabei']),
               (5.0, 10.2, ['und er lässt ihn', 'nicht mehr los'])]),
    # Ganz nah: Wickelbody, Blümchen, Haarband, Füsse
    'blumenwiese_kombi': dict(datei='reel_blumenwiese_kombi_9x16', set='bl', segmente=[
        ('bl_a', 0.0, 2.0, 1.0, (1.0, 1.06), (0.38, 0.5), (0.38, 0.48)),
        ('bl_a', 2.0, 3.6, 1.0, (1.6, 1.75), (0.56, 0.48), (0.58, 0.5)),     # Wickelverschluss
        ('bl_b', 2.0, 3.6, 1.0, (1.55, 1.7), (0.24, 0.16), (0.24, 0.18)),    # Haarband
        ('bl_a', 9.0, 10.6, 1.0, (1.5, 1.6), (0.8, 0.82), (0.82, 0.86)),     # Füsse
        ('bl_b', 6.0, 9.0, 0.8, (1.08, 1.0), (0.4, 0.45), (0.38, 0.5)),
        ('set', 'bl', 2.2), ('ende', 'bl', 1.8)],
        texte=[(0.0, 2.0, ['Ganz nah:', '«Blumenwiese»']), (2.0, 3.6, ['Wickelbody,', 'nichts über den Kopf']),
               (3.6, 5.2, ['Haarband', 'im gleichen Muster']), (5.2, 6.8, ['Fusshose', 'aus weichem Musselin']),
               (6.8, 10.5, ['Blümchen', 'von Kopf bis Fuss'])]),
    # Little Princess: Strampler-Look, Body-Look, Krone ganz nah
    'little_princess_kombi_pov': dict(datei='reel_little_princess_looks_9x16', set='lp', segmente=[
        ('lp_e', 0.0, 2.6, 1.0, (1.0, 1.06), (0.36, 0.45), (0.38, 0.42)),
        ('lp_e', 3.0, 4.4, 1.0, (1.5, 1.65), (0.42, 0.95), (0.42, 0.97)),    # Schleifen an den Füsschen
        ('lp_c', 1.0, 3.8, 0.8, (1.0, 1.08), (0.42, 0.45), (0.4, 0.42)),
        ('lp_c', 5.0, 6.6, 1.0, (1.55, 1.7), (0.64, 0.38), (0.64, 0.34)),    # Kronen-Schmusetuch
        ('lp_c', 7.0, 8.6, 1.0, (1.4, 1.5), (0.3, 0.86), (0.3, 0.88)),       # Söckchen
        ('set', 'lp', 2.2), ('ende', 'lp', 1.8)],
        texte=[(0.0, 2.6, ['Ein Set,', 'zwei Looks']), (2.6, 4.0, ['Look 1: Strampler', 'mit Schleifchen']),
               (4.0, 7.5, ['Look 2:', 'Body mit Söckchen']), (7.5, 9.1, ['Dazu das', 'Kronen-Schmusetuch']),
               (9.1, 10.8, ['8 Teile,', 'alles aufeinander abgestimmt'])]),
    # Vergleich zum Kommentieren: 1, 2 oder 3?
    'vergleich': dict(datei='reel_coming_soon_1-2-3_9x16', set=None, segmente=[
        ('bl_a', 0.0, 1.6, 1.0, (1.0, 1.04), (0.38, 0.5), (0.38, 0.5)),
        ('bf_a', 0.2, 1.8, 1.0, (1.0, 1.04), (0.5, 0.42), (0.5, 0.42)),
        ('lp_e', 0.0, 1.6, 1.0, (1.0, 1.04), (0.36, 0.45), (0.36, 0.45)),
        ('bl_b', 1.0, 3.6, 1.0, (1.0, 1.08), (0.4, 0.45), (0.4, 0.45)),
        ('bf_b', 4.0, 6.6, 1.0, (1.05, 1.15), (0.5, 0.42), (0.5, 0.4)),
        ('lp_c', 1.0, 3.6, 1.0, (1.0, 1.08), (0.42, 0.45), (0.42, 0.42)),
        ('ende', KOMMENTAR, 2.4)],
        texte=[(0.0, 4.8, ['Welches Set', 'würdest Du verschenken?']),
               ('zahl', 4.8, 7.4, '1', '«Blumenwiese»'), ('zahl', 7.4, 10.0, '2', '«Best Family»'),
               ('zahl', 10.0, 12.6, '3', '«Little Princess»')]),
    # Schnelle Detail-Montage aller drei Sets
    'details': dict(datei='reel_coming_soon_details_9x16', set=None, segmente=[
        ('bf_b', 0.5, 1.7, 1.0, (1.6, 1.75), (0.42, 0.44), (0.42, 0.46)),
        ('bl_a', 2.0, 3.2, 1.0, (1.6, 1.75), (0.56, 0.48), (0.58, 0.5)),
        ('lp_c', 5.0, 6.2, 1.0, (1.55, 1.7), (0.64, 0.38), (0.64, 0.34)),
        ('lp_e', 3.0, 4.2, 1.0, (1.5, 1.65), (0.42, 0.95), (0.42, 0.97)),
        ('bl_b', 2.0, 3.2, 1.0, (1.55, 1.7), (0.24, 0.16), (0.24, 0.18)),
        ('bf_a', 5.0, 6.2, 1.0, (1.45, 1.55), (0.78, 0.55), (0.72, 0.52)),
        ('bf_b', 4.0, 6.4, 0.75, (1.0, 1.08), (0.5, 0.42), (0.5, 0.4)),
        ('ende', 'Bald auf sunnozy.ch', 2.2)],
        texte=[(0.0, 2.4, ['Die kleinen Details', 'machen den Unterschied']), (2.4, 4.8, ['3 neue Sets,', 'bald bei sunnozy']),
               (4.8, 7.2, ['Speicher Dir das', 'für später']), (7.2, 10.5, ['Welches gefällt Dir?'])]),
}

_cache = {}


def frames(key):
    if key not in _cache:
        _cache[key] = m.clip_frames(CLIPS[key], 0, 15.1)
    return _cache[key]


def ausschnitt(im, zoom, fx, fy):
    s = H / im.height * zoom
    bw, bh = W / s, H / s
    cx = min(max(fx * im.width, bw / 2), im.width - bw / 2)
    cy = min(max(fy * im.height, bh / 2), im.height - bh / 2)
    out = im.resize((W, H), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    if zoom > 1.25:
        out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    return out.convert('RGBA')


def clip_bild(seg, t):
    """seg-Frame zur Zeit t (s, ab Segmentstart). Zeitlupe mischt Nachbarframes."""
    key, von, bis, tempo, (z0, z1), (fx0, fy0), (fx1, fy1) = seg
    fr = frames(key)
    p = (von + t * tempo) * FPS
    i = min(int(p), len(fr) - 1); j = min(i + 1, len(fr) - 1); a = p - int(p)
    im = fr[i] if a < 0.05 or i == j else Image.blend(fr[i], fr[j], a)
    dauer = (bis - von) / tempo
    e = m.ease(t / dauer)
    return ausschnitt(im, z0 + (z1 - z0) * e, fx0 + (fx1 - fx0) * e, fy0 + (fy1 - fy0) * e)


def ende_alle(zeile):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 720), 'Coming soon', font=m.f(m.SERIF, 120), fill=m.WALD, anchor='mm')
    for k, n in enumerate(['«Blumenwiese»', '«Best Family»', '«Little Princess»']):
        d.text((W / 2, 850 + k * 70), n, font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    d.line((W / 2 - 70, 1090, W / 2 + 70, 1090), fill=(200, 192, 180), width=2)
    d.text((W / 2, 1160), zeile, font=m.f(m.SERIF, 50), fill=m.GRAU, anchor='mm')
    L = m.logo(260, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1320), L)
    return c


def zahl(c, nummer, name, alpha):
    """Grosse Zahl und Setname im unteren Drittel (Kommentar-Vergleich)."""
    m.text_unten(c, [name], alpha, y=1400, groesse=80)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 3, 1230 + 4), nummer, font=m.f(m.SERIF, 230), fill=(20, 14, 10, int(190 * alpha)), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(c).text((W / 2, 1230), nummer, font=m.f(m.SERIF, 230), fill=(255, 255, 255, int(255 * alpha)), anchor='mm')
    return c


def reel(key):
    r = REELS[key]
    # Zeitachse: (start, dauer, render(t))
    teile, t0 = [], 0.0
    for seg in r['segmente']:
        if seg[0] == 'set':
            dauer = seg[2]; fn = (lambda st: lambda t: m.set_karte(st, t))(SETS[seg[1]]); karte = True
        elif seg[0] == 'ende':
            dauer = seg[2]; bild = m.end_karte(SETS[seg[1]]) if seg[1] in SETS else ende_alle(seg[1]); fn = (lambda b: lambda t: b)(bild); karte = True
        else:
            dauer = (seg[2] - seg[1]) / seg[3]; fn = (lambda s: lambda t: clip_bild(s, t))(seg); karte = False
        teile.append((t0, dauer, fn, karte)); t0 += dauer
    n = int(round(t0 * FPS)); nb = int(m.BLENDE * FPS)

    def roh(s):
        k = max(i for i, (st, _, _, _) in enumerate(teile) if st <= s + 1e-9)
        st, dauer, fn, karte = teile[k]
        c = fn(min(s - st, dauer - 1e-3))
        if not karte:
            for tx in r['texte']:
                if tx[0] == 'zahl':
                    _, a, b, nr, name = tx
                    if a <= s < b:
                        zahl(c, nr, name, min(1, (s - a) / 0.12))
                elif tx[0] <= s < tx[1]:
                    m.text_unten(c, tx[2], 1.0 if tx[0] == 0 else min(1, (s - tx[0]) / 0.12))
        # weiche Blende nur in Karten hinein; zwischen Clips harte Schnitte
        if k + 1 < len(teile) and teile[k + 1][3] and s > st + dauer - m.BLENDE:
            a = (s - (st + dauer - m.BLENDE)) / m.BLENDE
            c = Image.blend(c, teile[k + 1][2](0), min(a, 1))
        return c

    erstes = roh(0)
    os.makedirs(m.OUT, exist_ok=True)
    pfad = os.path.join(m.OUT, r['datei'] + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        c = roh(i / FPS)
        if i >= n - nb:   # Loop zurück ins erste Bild
            c = Image.blend(c, erstes, (i - (n - nb)) / nb)
        fr = c.convert('RGB')
        if i == int(0.6 * FPS):
            fr.save(os.path.join(m.OUT, r['datei'] + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {n / FPS:.1f} s')


if __name__ == '__main__':
    for key in (sys.argv[1:] or REELS):
        reel(key)
