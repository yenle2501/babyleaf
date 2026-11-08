"""Coming-soon-Reel «Flackern» (08.11.2026): Logo → COMING SOON mit immer schnellerem Farbwechsel → Logo.

Aufbau nach einem Bildschirmvideo der Nutzerin (fremdes Reel, nur Rhythmus und Aufbau übernommen):
  0–0.65 s    sunnozy-Logo auf hellem Grund
  0.65–7.5 s  COMING SOON, Hintergrund und Schrift tauschen die Farben, der Wechsel wird immer schneller (0.4 s → 0.08 s)
  7.5–9.2 s   wieder das Logo, darunter sunnozy.ch, am Ende kurze Blende in die dunkle Farbe (Loop)
Jeder Farbwechsel hat einen leisen Tick (synthetisch erzeugt), darunter läuft «Holiday 01» (Mixkit, lizenzfrei).

    python3 tools/make_reel_coming_soon_flacker.py
Ausgabe: posts/reels/coming-soon/reel_coming_soon_flackern_<farbe>_9x16.mp4 + _titelbild.jpg
"""
import os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
OUT = os.path.join(m.POSTS, 'reels', 'coming-soon')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'mixkit_lily-j_holiday-01.mp3')
FETT = 'nunitosans-800.ttf'

FARBEN = {
    'weinrot': dict(hell=(250, 228, 222), dunkel=(98, 22, 30)),       # Weinrot der Geschenkbox + Rosé
    'salbei': dict(hell=(246, 242, 234), dunkel=(96, 112, 88)),       # Salbei + Creme
}
# Wechselzeitpunkte (s): ab hier jeweils die andere Farbe, immer schneller
WECHSEL = [0.65, 1.13, 1.33, 1.53, 1.73, 1.93, 2.13, 2.33, 2.53, 2.72, 2.88, 3.05, 3.22, 3.40, 3.57, 3.73, 3.90,
           4.07, 4.22, 4.37, 4.50, 4.63, 4.77, 4.92, 5.05, 5.20, 5.33, 5.48, 5.60, 5.72, 5.83, 5.95, 6.07, 6.20,
           6.32, 6.43, 6.57, 6.65, 6.73, 6.82, 6.90, 6.98, 7.05, 7.13, 7.22, 7.30, 7.38, 7.47]
T_LOGO2, T_ENDE = 7.47, 9.2


def gesperrt(d, text, y, groesse, farbe, abstand):
    fo = m.f(FETT, groesse)
    b = [d.textlength(ch, font=fo) for ch in text]
    x = W / 2 - (sum(b) + abstand * (len(text) - 1)) / 2
    for ch, w in zip(text, b):
        d.text((x, y), ch, font=fo, fill=farbe, anchor='lm'); x += w + abstand


def logo_bild(f, mit_link):
    c = Image.new('RGB', (W, H), f['hell']); L = m.logo(620, f['dunkel'])
    c.paste(L, ((W - L.width) // 2, 860 - L.height // 2), L)
    if mit_link:
        ImageDraw.Draw(c).text((W / 2, 1060), 'sunnozy.ch', font=m.f(m.SERIF, 64), fill=f['dunkel'], anchor='mm')
    return c


def coming(f, dunkel):
    bg, fg = (f['dunkel'], f['hell']) if dunkel else (f['hell'], f['dunkel'])
    c = Image.new('RGB', (W, H), bg)
    gesperrt(ImageDraw.Draw(c), 'COMING SOON', 860, 92, fg, 6)
    return c


def ticks(dauer):
    """Leiser Tick bei jedem Farbwechsel (kurzes, gefiltertes Rauschen mit schnellem Abklingen)."""
    sr = 44100; a = np.zeros(int(dauer * sr))
    rng = np.random.default_rng(3)
    n = int(0.035 * sr); env = np.exp(-np.linspace(0, 9, n))
    klick = np.convolve(rng.standard_normal(n), np.ones(6) / 6, 'same') * env
    for i, t in enumerate(WECHSEL + [T_LOGO2]):
        s = int(t * sr); lautst = 0.18 + 0.22 * i / len(WECHSEL)
        a[s:s + n] += klick[:len(a[s:s + n])] * lautst
    return sr, (np.clip(a, -1, 1) * 32767).astype(np.int16)


def reel(name):
    f = FARBEN[name]
    os.makedirs(OUT, exist_ok=True)
    datei = os.path.join(OUT, f'reel_coming_soon_flackern_{name}_9x16')
    tmp = datei + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    bilder = {'logo': logo_bild(f, False), 'logo_link': logo_bild(f, True), 'hell': coming(f, False), 'dunkel': coming(f, True)}
    n = int(round(T_ENDE * FPS))
    for i in range(n):
        t = i / FPS
        if t < WECHSEL[0]:
            c = bilder['logo']
            if t > WECHSEL[0] - 0.12:                                   # kurze Blende ins erste Dunkel
                c = Image.blend(c, bilder['dunkel'], (t - (WECHSEL[0] - 0.12)) / 0.12)
        elif t < T_LOGO2:
            k = sum(1 for w in WECHSEL if w <= t)
            c = bilder['dunkel'] if k % 2 == 1 else bilder['hell']
        else:
            c = bilder['logo_link']
            if t > T_ENDE - 0.6:                                        # Loop: Blende ins Dunkel wie am Anfang
                c = Image.blend(c, Image.new('RGB', (W, H), f['dunkel']), (t - (T_ENDE - 0.6)) / 0.6)
        if i == int(2.0 * FPS):
            c.save(datei + '_titelbild.jpg', quality=92)
        enc.stdin.write(c.tobytes())
    enc.stdin.close(); enc.wait()
    sr, a = ticks(T_ENDE)
    wav = datei + '.ticks.wav'
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.tobytes())
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', wav, '-ss', '24', '-i', MUSIK, '-filter_complex',
                    f'[2:a]atrim=0:{T_ENDE},afade=t=in:d=0.4,afade=t=out:st={T_ENDE - 0.8}:d=0.8,volume=0.9[mu];'
                    f'[1:a]volume=1.0[ti];[mu][ti]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-t', str(T_ENDE),
                    '-movflags', '+faststart', datei + '.mp4'], check=True)
    os.remove(tmp); os.remove(wav)
    print(datei + '.mp4', flush=True)


if __name__ == '__main__':
    for k in FARBEN:
        reel(k)
