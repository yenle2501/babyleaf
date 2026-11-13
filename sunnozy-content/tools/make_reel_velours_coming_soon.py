"""Coming-soon-Reel Strampler «Velours» Creme mit Puffärmeln und Rüschen, aus drei Grok-Clips der Nutzerin (13.11.2026).

Stil wie die POV-Reels (Schreibmaschinenschrift, volles Video, kein Preis), nach der Viral-Analyse:
Hook ab Bild 1, Neugeborenes mit kleiner Bewegung (Strecken, Strampeln), ~10 s Loop, Schluss «coming soon 🤍».
  1. clip_strecken  0.0–5.0 s  Hand zum Mund, dann Ärmchen weit auf
  2. clip_strampeln 5.0–10.5 s Ärmchen hoch, Beinchen mit Rüschen strampeln, Hände zurück zum Mund (passt zum Loop)
(clip_ruhig ist nicht verwendet: wenig Bewegung.)

    python3 tools/make_reel_velours_coming_soon.py [rueschen|winter]
Ausgabe: posts/coming-soon/reels/velours/reel_velours_<variante>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image
import make_coming_soon_reels as m
import make_reel_hello_little_bear_hook as hk

W, H, FPS = m.W, m.H, 30
BASIS = os.path.join(m.POSTS, 'coming-soon', 'reels', 'velours')
O = os.path.join(BASIS, 'original')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'mixkit_lily-j_holiday-01.mp3')
SZENEN = [('clip_strecken.mp4', 0.0, 5.0), ('clip_strampeln.mp4', 5.0, 10.5)]
BLENDE = 0.3
ENDE_AB = 7.9

VARIANTEN = {
    'rueschen': (['POV: Puffärmel, Rüschen', 'und Babyfieber'], '🎀'),
    'winter': (['POV: Ihr erster Winter,', 'ganz in Velours'], '✨'),
}


def ebene(zeilen, zeichen):
    alt = hk.emoji
    hk.emoji = lambda _, h: alt(zeichen, h)
    zeilen = zeilen[:-1] + [zeilen[-1] + ' ✨']
    e = hk.text_ebene(zeilen)
    hk.emoji = alt
    return e


def frames(datei, von, bis):
    sw = round(768 * H / 1168)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', os.path.join(O, datei), '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, H), b)


def folge():
    nb = int(BLENDE * FPS); puffer = []
    for k, s in enumerate(SZENEN):
        for j, fr in enumerate(frames(*s)):
            if k > 0 and j < nb and puffer:
                yield Image.blend(puffer.pop(0), fr, (j + 1) / (nb + 1))
                continue
            puffer.append(fr)
            if len(puffer) > nb:
                yield puffer.pop(0)
    yield from puffer


def reel(name):
    zeilen, zeichen = VARIANTEN[name]
    e1, e2 = ebene(zeilen, zeichen), ebene(['coming soon'], '🤍')
    dauer = sum(b - a for _, a, b in SZENEN) - BLENDE * (len(SZENEN) - 1)
    pfad = os.path.join(BASIS, f'reel_velours_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i, fr in enumerate(folge()):
        t = i / FPS; c = fr.convert('RGBA')
        for eb, a in ((e1, 1 - m.ease((t - 2.8) / 0.4)), (e2, m.ease((t - ENDE_AB) / 0.5))):
            if a > 0:
                e = eb.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.0:.2f}:d=1.0,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(VARIANTEN)):
        reel(name)
