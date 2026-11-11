"""Reel Erstausstattung «Hello» Rosa mit Spitze: «Aufwachen» aus drei KI-Clips der Nutzerin (11.11.2026).

Stil wie die Hello-Little-Bear-Reels (Vorlage der Nutzerin): volles Video, POV-Zeile in weisser Schreibmaschinenschrift
mit Emoji, kein Preis, keine Schlusskarte. Drei Clips zusammengeschnitten:
  1. clip_strecken  0.0–5.0 s  Baby streckt sich und gähnt         -> Hook (POV) 0–3.2 s
  2. clip_details  10.6–14.6 s Kamera fährt zu Spitzenkragen und Häubchen (Produkt)
  3. clip_aufwachen 1.6–6.0 s  Baby wird wach und öffnet die Augen  -> Schluss-Text, läuft in den Loop
Zwei Varianten zum Testen (Texte in VARIANTEN).

    python3 tools/make_reel_hello_spitze_morgen.py [morgen|grosi]
Ausgabe: posts/coming-soon/reels/hello-spitze/reel_hello_spitze_<variante>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageFilter
import make_coming_soon_reels as m
import make_reel_hello_little_bear_hook as hk

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'coming-soon', 'reels', 'hello-spitze')
O = os.path.join(BASIS, 'original')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'alex-morgan_heartwarming-story.mp3')
SZENEN = [('clip_strecken.mp4', 0.0, 5.0), ('clip_details.mp4', 10.6, 14.6), ('clip_aufwachen.mp4', 1.6, 6.0)]
BLENDE = 0.3

VARIANTEN = {
    'morgen': (['POV: Ihr erster Morgen', 'zu Hause ✨'], ['guten Morgen,', 'kleine Prinzessin 🤍']),
    'grosi': (['POV: Du bist Grosi und sie', 'trägt Dein Geschenk ✨'], ['guten Morgen,', 'Schätzli 🤍']),
}


def frames(datei, von, bis):
    """Quadratischer Clip auf volle Höhe, mittig auf 9:16 zugeschnitten; 544er-Clip leicht nachgeschärft."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', os.path.join(O, datei), '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={H}:{H}:flags=lanczos,crop={W}:{H}:{(H - W) // 2}:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = W * H * 3; scharf = 'aufwachen' in datei
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        im = Image.frombuffer('RGB', (W, H), b)
        yield im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2)) if scharf else im


def emoji_text(zeilen):
    """hk.text_ebene kann nur ✨; hier ✨ und 🤍 am Zeilenende."""
    alt = hk.emoji
    def emoji(_, h):
        return alt(zeichen[0], h)
    zeichen = ['✨']
    for z in zeilen:
        if '🤍' in z:
            zeichen[0] = '🤍'
    hk.emoji = emoji
    ebene = hk.text_ebene([z.replace('🤍', '✨') for z in zeilen])
    hk.emoji = alt
    return ebene


def reel(name):
    oben, unten = VARIANTEN[name]
    e1, e2 = emoji_text(oben), emoji_text(unten)
    nb = int(BLENDE * FPS)
    laengen = [int((b - a) * FPS) for _, a, b in SZENEN]
    dauer = (sum(laengen) - nb * (len(SZENEN) - 1)) / FPS
    start3 = (laengen[0] + laengen[1] - 2 * nb) / FPS

    def folge_gen():                          # Clips nacheinander, weiche Überblendung, ohne alles im Speicher
        puffer = []
        for k, s in enumerate(SZENEN):
            for j, fr in enumerate(frames(*s)):
                if k > 0 and j < nb and puffer:
                    yield Image.blend(puffer.pop(0), fr, (j + 1) / (nb + 1))
                    continue
                puffer.append(fr)
                if len(puffer) > nb:
                    yield puffer.pop(0)
        yield from puffer
    folge = folge_gen()
    pfad = os.path.join(BASIS, f'reel_hello_spitze_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, fr in enumerate(folge):
        t = i / FPS; c = fr.convert('RGBA')
        for ebene, a in ((e1, 1 - m.ease((t - 2.8) / 0.4)),
                         (e2, m.ease((t - (start3 + 1.8)) / 0.5))):    # Schluss-Text, wenn die Augen aufgehen
            if a > 0:
                e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
