"""Coming-soon-Reel «Schleife» aus dem Handyvideo der Nutzerin (06.11.2026).

Rote sunnozy-Schleife vor dem Laptop mit dem Instagram-Profil, eine Hand zieht die Schleife auf und das Logo erscheint.
  0–5 s     Schleife, langsamer Zoom, oben im dunklen Bereich «Psst …» → «Wir packen gerade etwas aus.»
  5–9.3 s   Aufziehen in Zeitlupe (0.6×)
  danach    Zoom zum Logo auf dem Bildschirm, oben «sunnozy» + COMING SOON
  Schluss   Cremefarbene Karte: Logo, COMING SOON, sunnozy.ch, «Folg uns, damit Du nichts verpasst»
Warm gegradet, leichte Vignette, Musik Alex Morgan, Originalton (Schleifenrascheln) leise darunter.

    python3 tools/make_coming_soon_schleife.py
Quelle: posts/coming-soon/schleife/original/schleife.mov (iPhone, hochkant). Ausgabe: posts/reels/coming-soon/reel_sunnozy_schleife_9x16.mp4
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
QUELLE = os.path.join(m.POSTS, 'coming-soon', 'schleife', 'original', 'schleife.mov')
OUT = os.path.join(m.POSTS, 'reels', 'coming-soon')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'alex-morgan_heartwarming-story.mp3')
HELL = (253, 246, 238)

# (Quelle von, bis, Tempo, Zoom von, bis, Fokus von (x, y), bis (x, y))
SEGMENTE = [(1.0, 6.0, 1.0, 1.00, 1.10, (0.5, 0.42), (0.5, 0.42)),
            (6.0, 8.6, 0.6, 1.10, 1.14, (0.5, 0.42), (0.48, 0.41)),
            (8.6, 12.5, 1.0, 1.14, 1.38, (0.48, 0.41), (0.40, 0.38))]
T_ENDE, BLENDE_ENDE = 3.2, 0.7


def zeitplan():
    """Pro Ausgabeframe: Quellzeit, Zoom, Fokus."""
    plan = []
    for von, bis, tempo, z0, z1, f0, f1 in SEGMENTE:
        n = int(round((bis - von) / tempo * FPS))
        for i in range(n):
            e = m.ease(i / n) if tempo == 1.0 else i / n
            plan.append((von + i / n * (bis - von), z0 + (z1 - z0) * e,
                         (f0[0] + (f1[0] - f0[0]) * e, f0[1] + (f1[1] - f0[1]) * e)))
    return plan


def quelle_frames():
    """Frames der Quelle (hochkant, 1080×1920) der Reihe nach, mit Zeitstempel."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', QUELLE, '-map', '0:v:0', '-vf', f'scale={W}:{H}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    fps = 30000 / 1001; i = 0
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield i / fps, Image.frombuffer('RGB', (W, H), b)
        i += 1


def grade(im, vign):
    a = np.asarray(im).astype(np.float32)
    a = (a - 128) * 1.06 + 128 + 4                                   # etwas Kontrast
    a[..., 0] *= 1.04; a[..., 2] *= 0.94                             # wärmer
    a *= vign
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.45) / (H * 0.62)) ** 2)
    return (1 - 0.35 * np.clip(r - 0.45, 0, 1) ** 1.4)[..., None]


def text(c, zeilen, alpha, y, groesse, schrift=None, sperren=0.0, farbe=HELL):
    if alpha <= 0:
        return c
    fo = m.f(schrift or m.SERIF_I, groesse)
    ebene = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ebene)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for k, z in enumerate(zeilen):
        if sperren:
            z = (' ' * 0).join(z)
        yy = y + k * groesse * 1.15
        ds.text((W / 2, yy + 3), z, font=fo, fill=(0, 0, 0, int(170 * alpha)), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0, int(170 * alpha)))
        d.text((W / 2, yy), z, font=fo, fill=farbe + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    c.alpha_composite(ebene)
    return c


def gesperrt(c, wort, alpha, y, groesse, farbe, abstand):
    """Versalien mit grossem Buchstabenabstand (COMING SOON)."""
    if alpha <= 0:
        return c
    fo = m.f(m.SERIF, groesse)
    ebene = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ebene)
    b = [d.textlength(ch, font=fo) for ch in wort]; x = W / 2 - (sum(b) + abstand * (len(wort) - 1)) / 2
    for ch, w in zip(wort, b):
        d.text((x, y), ch, font=fo, fill=farbe + (int(255 * alpha),), anchor='lm'); x += w + abstand
    c.alpha_composite(ebene)
    return c


def ueberlagerung(c, t, t_reveal, t_video):
    """Texte über dem Video, je nach Ausgabezeit t."""
    a1 = m.ease(t / 0.5) * (1 - m.ease((t - 2.3) / 0.4))
    text(c, ['Psst …'], a1, 330, 92)
    a2 = m.ease((t - 2.7) / 0.5) * (1 - m.ease((t - (t_reveal - 1.6)) / 0.5))
    text(c, ['Wir packen gerade', 'etwas aus.'], a2, 300, 84)
    a3 = m.ease((t - t_reveal) / 0.8)
    if a3 > 0:
        L = m.logo(430, HELL); L.putalpha(L.getchannel('A').point(lambda v: int(v * a3)))
        sch = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sch.alpha_composite(L, ((W - L.width) // 2, 230))
        sch2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sch2.putalpha(sch.getchannel('A').point(lambda v: int(v * 0.6)))
        c.alpha_composite(sch2.filter(ImageFilter.GaussianBlur(12)))
        c.alpha_composite(sch)
    gesperrt(c, 'COMING SOON', m.ease((t - t_reveal - 0.7) / 0.8), 440, 54, HELL, 14)
    return c


def end_karte(t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,))
    a1 = m.ease((t - 0.2) / 0.8); a2 = m.ease((t - 0.8) / 0.8); a3 = m.ease((t - 1.3) / 0.8)
    L = m.logo(560, m.WALD); L.putalpha(L.getchannel('A').point(lambda v: int(v * a1)))
    c.alpha_composite(L, ((W - L.width) // 2, 700))
    gesperrt(c, 'COMING SOON', a2, 960, 62, m.SALBEI, 16)
    d = ImageDraw.Draw(c)
    if a3 > 0:
        d.text((W / 2, 1090), 'sunnozy.ch', font=m.f(m.SERIF, 60), fill=m.WALD + (int(255 * a3),), anchor='mm')
        d.text((W / 2, 1175), 'Folg uns, damit Du nichts verpasst', font=m.f(m.SERIF_I, 50), fill=m.GRAU + (int(255 * a3),), anchor='mm')
    return c


def main():
    os.makedirs(OUT, exist_ok=True)
    plan = zeitplan(); vign = vignette()
    t_reveal = (SEGMENTE[0][1] - SEGMENTE[0][0]) + (SEGMENTE[1][1] - SEGMENTE[1][0]) / SEGMENTE[1][2] + 0.4
    t_video = len(plan) / FPS; n_ende = int(T_ENDE * FPS); nb = int(BLENDE_ENDE * FPS)
    pfad = os.path.join(OUT, 'reel_sunnozy_schleife_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    src = quelle_frames(); ts, cur = next(src); nxt = next(src, None)
    letztes = None
    for i, (s, z, (fx, fy)) in enumerate(plan):
        while nxt is not None and nxt[0] <= s:
            ts, cur = nxt; nxt = next(src, None)
        bw, bh = W / z, H / z
        cx = min(max(fx * W, bw / 2), W - bw / 2); cy = min(max(fy * H, bh / 2), H - bh / 2)
        fr = cur.resize((W, H), Image.BICUBIC, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
        c = grade(fr, vign).convert('RGBA')
        c = ueberlagerung(c, i / FPS, t_reveal, t_video)
        if i >= len(plan) - nb:                                       # weich in die Schlusskarte
            c = Image.blend(c, end_karte(0), (i - (len(plan) - nb)) / nb)
        if i == int(0.8 * FPS):
            c.convert('RGB').save(os.path.join(OUT, 'reel_sunnozy_schleife_9x16_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    for j in range(n_ende):
        enc.stdin.write(end_karte(j / FPS + BLENDE_ENDE * 0).convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = t_video + T_ENDE
    # Originalton (Rascheln) im gleichen Zeitplan: Abschnitte schneiden, Zeitlupe mit atempo
    teile = []
    for k, (von, bis, tempo, *_r) in enumerate(SEGMENTE):
        teile.append(f'[1:a]atrim={von}:{bis},asetpts=PTS-STARTPTS' + (f',atempo={tempo}' if tempo != 1 else '') + f'[o{k}]')
    fil = ';'.join(teile) + f';{"".join(f"[o{k}]" for k in range(len(SEGMENTE)))}concat=n={len(SEGMENTE)}:v=0:a=1,volume=0.35,apad[orig];' \
          f'[2:a]atrim=0:{dauer:.2f},afade=t=in:d=0.8,afade=t=out:st={dauer - 2:.2f}:d=2,volume=0.8[mus];' \
          f'[orig][mus]amix=inputs=2:duration=longest:normalize=0,atrim=0:{dauer:.2f}[a]'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', QUELLE, '-ss', '20', '-i', MUSIK, '-filter_complex', fil,
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-t', f'{dauer:.2f}', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    main()
