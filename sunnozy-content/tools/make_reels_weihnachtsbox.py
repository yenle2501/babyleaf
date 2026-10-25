"""Reels für die Weihnachts-Geschenkboxen aus Fotos (Szenen im Handyfoto-Stil + Box von oben), mit Zoom, Schnitten,
Hook ab Sekunde 0, Musik und Schlusskarte. Schrift und Text-Stil wie die Baby-Reels (Cormorant Garamond).

    python3 tools/make_reels_weihnachtsbox.py            # alle
    python3 tools/make_reels_weihnachtsbox.py gotti      # nur eines

Ausgabe: posts/kampagne-weihnachtsbox/reels/reel_<name>_9x16.mp4 + _titelbild.jpg
Szene: (bild, dauer_s, zoom0, zoom1, (fx0, fy0), (fx1, fy1), text)   text: Zeilen, None = vorheriger bleibt, {'zahl','name'}
"""
import os, sys, subprocess
from PIL import Image
import make_coming_soon_reels as m
import make_coming_soon_kombi as k
import make_reels_videos_baby as rv      # liste_karte, Musik, hellerer Textverlauf

KB = os.path.join(m.POSTS, 'kampagne-weihnachtsbox')
OUT = os.path.join(KB, 'reels')
W, H, FPS = m.W, m.H, m.FPS
E = lambda b: os.path.join(KB, 'fotos-echt', f'box_{b}.jpg')      # Szene im Handyfoto-Stil
S = lambda b: os.path.join(KB, 'fotos', f'box_{b}.jpg')           # Box von oben (Studio)
M = (0.5, 0.5)
FUSS = ['Link in der Bio', 'Versand in 2–3 Werktagen']

REELS = {
    'gotti': dict(szenen=[
        (E('lovely_little_girl'), 2.6, 1.0, 1.08, M, (0.5, 0.55), ['POV: Du bist Gotti', 'und das Geschenk ist schon da']),
        (E('dinosaur'), 2.4, 1.08, 1.0, (0.5, 0.55), M, ['Fertig verpackt,', 'mit Schleife und Karte']),
        (S('mum_dad_me'), 2.4, 1.15, 1.3, (0.5, 0.4), (0.5, 0.55), ['Ganze Sets:', 'Bodys und Hosen']),
        (E('mum_dad_me'), 2.6, 1.0, 1.06, M, (0.5, 0.45), ['Du musst nur noch', 'die Grösse wählen'])],
        liste=(['Weihnachts-', 'Geschenkboxen'], [('9 Boxen', 'ab CHF 29.90'), ('Grösse', '0–3 bis 6–9 Mt.')], ['Markier das Gotti', 'Link in der Bio'])),
    'welche_box': dict(szenen=[
        (E('mum_dad_me'), 1.4, 1.0, 1.05, M, M, ['Welche Box', 'würdest Du verschenken?']),
        (E('growing_up_strong'), 1.3, 1.0, 1.05, M, M, None),
        (E('dinosaur'), 1.3, 1.0, 1.05, M, M, None)] + [
        (E(b), 1.5, 1.0, 1.07, M, M, {'zahl': str(i + 1), 'name': n}) for i, (b, n) in enumerate([
            ('mum_dad_me', '«Mum Dad Me»'), ('lovely_little_girl', '«Lovely Little Girl»'), ('growing_up_strong', '«Growing up strong»'),
            ('i_love_my_mummy', '«I love my Mummy»'), ('dino', '«Dino»'), ('dinosaur', '«Dinosaur»'), ('little_one', '«Little One»'),
            ('i_like_flying', '«I like flying»'), ('little_one_jogginghosen', '«Little One» Hosen')])],
        liste=('Welche nimmst Du?', [('1 Mum Dad Me', 'CHF 42.90'), ('2 Lovely Little Girl', 'CHF 39.90'), ('3 Growing up strong', 'CHF 42.90'),
               ('4 I love my Mummy', 'CHF 29.90'), ('5 Dino', 'CHF 39.90'), ('6 Dinosaur', 'CHF 42.90'), ('7 Little One', 'CHF 44.90'),
               ('8 I like flying', 'CHF 39.90'), ('9 Little One Hosen', 'CHF 42.90')], ['Schreib die Zahl in die Kommentare'])),
    'was_ist_drin': dict(szenen=[
        (E('growing_up_strong'), 2.4, 1.0, 1.08, M, (0.5, 0.6), ['Was ist in der', 'Weihnachtsbox?']),
        (S('growing_up_strong'), 2.2, 1.0, 1.25, M, (0.5, 0.32), ['5 gerippte Bodys']),
        (S('growing_up_strong'), 2.2, 1.25, 1.25, (0.5, 0.32), (0.5, 0.72), ['5 Jogginghosen', 'mit Schleife']),
        (S('growing_up_strong'), 2.0, 1.25, 1.1, (0.62, 0.3), (0.6, 0.35), ['und die Karte', 'für Deinen Gruss']),
        (E('dinosaur'), 2.4, 1.0, 1.06, M, M, ['Rosa Box, Seidenpapier,', 'jedes Teil mit Band'])],
        liste=('«Growing up strong»', [('5 Bodys + 5 Hosen', 'CHF 42.90'), ('Box und Karte', 'inklusive')], FUSS)),
    'unter_30_franken': dict(szenen=[
        (E('i_love_my_mummy'), 2.6, 1.0, 1.08, M, (0.45, 0.4), ['Geschenk für die Mama', 'unter 30 Franken']),
        (S('i_love_my_mummy'), 2.2, 1.0, 1.22, M, (0.3, 0.3), ['3 Bodys', '«I love my Mummy»']),
        (S('i_love_my_mummy'), 2.2, 1.22, 1.22, (0.3, 0.75), (0.65, 0.75), ['3 Halstücher', 'mit Bärchen']),
        (E('i_love_my_mummy'), 2.4, 1.06, 1.0, (0.45, 0.45), M, ['Fertig verpackt', 'mit Karte'])],
        liste=('«I love my Mummy»', [('3 Bodys + 3 Halstücher', 'CHF 29.90'), ('Box und Karte', 'inklusive')], ['Schick das jemandem, der ein Geschenk sucht', 'Link in der Bio'])),
    'last_minute': dict(szenen=[
        (E('i_like_flying'), 2.4, 1.0, 1.07, M, M, ['Noch kein Geschenk', 'fürs Gottikind?']),
        (E('little_one'), 2.2, 1.0, 1.06, M, M, ['Wir packen es', 'für Dich ein']),
        (E('little_one_jogginghosen'), 2.2, 1.06, 1.0, M, M, ['mit Seidenpapier,', 'Band und Karte']),
        (E('growing_up_strong'), 2.4, 1.0, 1.08, M, (0.5, 0.6), ['in 2–3 Werktagen', 'bei Dir'])],
        liste=(['Weihnachts-', 'Geschenkboxen'], [('Gratisversand', 'ab CHF 50'), ('z.B. zwei Boxen', 'für zwei Gottikinder')], ['Letzter Bestelltag: ca. 18.12.', 'Link in der Bio'])),
}


_cache = {}


def bild(p):
    if p not in _cache:
        _cache[p] = Image.open(p).convert('RGB')
    return _cache[p]


def frame(sz, t):
    p, dauer, z0, z1, f0, f1, _ = sz
    e = m.ease(t / dauer)
    im = bild(p)
    return rv.ausschnitt(im, z0 + (z1 - z0) * e, f0[0] + (f1[0] - f0[0]) * e, f0[1] + (f1[1] - f0[1]) * e)


def reel(key, nr):
    r = REELS[key]
    teile, t0 = [], 0.0
    for sz in r['szenen']:
        teile.append(dict(start=t0, dauer=sz[1], sz=sz, text=sz[6], karte=False)); t0 += sz[1]
    end = rv.liste_karte(*r['liste'])
    teile.append(dict(start=t0, dauer=3.4, karte=True)); t0 += 3.4
    n = int(round(t0 * FPS)); nb = int(m.BLENDE * FPS)

    def text_von(i):
        while i >= 0 and teile[i].get('text') is None:
            i -= 1
        return teile[i]['text'] if i >= 0 else None

    def roh(s):
        i = max(j for j, tl in enumerate(teile) if tl['start'] <= s + 1e-9)
        tl = teile[i]; t = min(s - tl['start'], tl['dauer'] - 1e-3)
        if tl['karte']:
            return end.copy()
        c = frame(tl['sz'], t)
        z = text_von(i); a = min(1, t / 0.12) if (tl['text'] is not None and i > 0) else 1.0
        if isinstance(z, dict):
            k.zahl(c, z['zahl'], z['name'], a)
        elif z:
            m.text_unten(c, z, a)
        if i + 1 < len(teile) and teile[i + 1]['karte'] and s > tl['start'] + tl['dauer'] - m.BLENDE:
            c = Image.blend(c, end, min(1, (s - (tl['start'] + tl['dauer'] - m.BLENDE)) / m.BLENDE))
        return c

    erstes = roh(0)
    os.makedirs(OUT, exist_ok=True)
    datei = f'reel_{key}_9x16'; pfad = os.path.join(OUT, datei + '.mp4'); tmp = pfad + '.tmp.mp4'
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
    dauer = n / FPS; musik = rv.MUSIK[nr % 2]; ab = 15 + nr * 17
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', musik, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.4,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=0.85', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for key in (sys.argv[1:] or REELS):
        reel(key, list(REELS).index(key))
