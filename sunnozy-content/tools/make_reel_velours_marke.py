"""Coming-soon-Reel mit Marken-Vorstellung: Velours-Strampler (Clip «Strecken») + «sunnozy = Babykleidung» (13.11.2026).

Wunsch der Nutzerin: Video für Coming soon, dazu schreiben, was sunnozy ist (Babykleidung), besser gemacht.
Gleicher Clip und Look wie reel_velours_strecken (Zeitlupe beim Strecken, langsamer Zoom, warme Farben), ohne Weihnachtseffekte.
Neu: Text oben im Bild auf einem sanften dunklen Verlauf (statt weiss auf dem cremefarbenen Strampler), drei Teile:
  0–3 s    Hook        «POV: Ihr erster Winter, ganz in Velours ✨»
  3.3–6.3  Marke       sunnozy-Logo + «Babykleidung, verschickt aus der Schweiz 🇨🇭»
  6.6–Ende Teaser      Logo bleibt + «Neue Kollektion · coming soon 🤍»
Kein Preis. Musik «Holiday 01» (Mixkit, lizenzfrei).

    python3 tools/make_reel_velours_marke.py
Ausgabe: posts/coming-soon/reels/velours/reel_velours_sunnozy_coming_soon_9x16.mp4 + _titelbild.jpg
"""
import os, subprocess, tempfile
import numpy as np
from PIL import Image, ImageFilter
import make_coming_soon_reels as m
import make_reel_velours_coming_soon as vc

W, H, FPS = m.W, m.H, 30
TEILE = vc.VARIANTEN['strecken']['teile']
ZOOM, MITTE = (1.0, 1.10), 0.42
TEXTE = [(0.0, 3.0, ['POV: Ihr erster Winter,', 'ganz in Velours'], '✨', 200),
         (3.3, 6.3, ['Babykleidung,', 'verschickt aus der Schweiz'], '🇨🇭', 250),
         (6.6, 99, ['Neue Kollektion', 'coming soon'], '🤍', 250)]
LOGO_AB = 3.3


def verlauf():
    """Sanfter warmer Verlauf oben, damit weisser Text lesbar ist."""
    a = np.clip(1 - np.arange(H) / 640, 0, 1) ** 1.5 * 150
    v = Image.new('RGBA', (W, H), (40, 28, 20, 0)); v.putalpha(Image.fromarray(np.tile(a[:, None], (1, W)).astype(np.uint8)))
    return v


def logo_ebene():
    L = m.logo(400, (255, 255, 255))
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sch = Image.new('RGBA', L.size, (40, 28, 20, 0)); sch.putalpha(L.getchannel('A').point(lambda q: int(q * 0.6)))
    x, y = (W - L.width) // 2, 120 - L.height // 2
    e.alpha_composite(sch.filter(ImageFilter.GaussianBlur(8)), (x + 2, y + 4))
    e.alpha_composite(L, (x, y))
    return e


def mit_alpha(ebene, a):
    e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda q: int(q * a)))
    return e


def main():
    dauer = sum((b - a) / s for a, b, s in TEILE)
    pfad = os.path.join(vc.BASIS, 'reel_velours_sunnozy_coming_soon_9x16.mp4')
    with tempfile.TemporaryDirectory() as td:
        zw = os.path.join(td, 'zeit.mp4'); vc.zeitachse('clip_strecken.mp4', TEILE, zw)
        ebenen = [(a0, a1, vc.text_ebene(z, em, y0=y, groesse=54)) for a0, a1, z, em, y in TEXTE]
        vig, verl, logo = vc.vignette(), verlauf(), logo_ebene()
        tmp = os.path.join(td, 'v.mp4')
        enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
        sw = round(768 * H / 1168); n = 0
        for i, fr in enumerate(vc.frames(zw)):
            t = i / FPS
            z = ZOOM[0] + (ZOOM[1] - ZOOM[0]) * m.ease(t / dauer)
            gross = fr.resize((round(sw * z), round(H * z)), Image.LANCZOS)
            x0 = (gross.width - W) // 2; y0 = int((gross.height - H) * MITTE)
            c = gross.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
            c = vc.warm(c).convert('RGBA'); c.alpha_composite(vig); c.alpha_composite(verl)
            for a0, a1, eb in ebenen:
                ein = 1.0 if a0 == 0 else m.ease((t - a0) / 0.35)
                aus = 1 - m.ease((t - (a1 - 0.3)) / 0.3)
                if ein * aus > 0:
                    c.alpha_composite(mit_alpha(eb, ein * aus))
            if t >= LOGO_AB:
                c.alpha_composite(mit_alpha(logo, m.ease((t - LOGO_AB) / 0.4)))
            if i == int(0.5 * FPS):
                c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
            enc.stdin.write(c.convert('RGB').tobytes()); n += 1
        enc.stdin.close(); enc.wait()
        dauer = n / FPS
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', vc.MUSIK, '-t', f'{dauer:.2f}',
                        '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.0:.2f}:d=1.0,volume=1.4,alimiter=limit=0.89',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    main()
