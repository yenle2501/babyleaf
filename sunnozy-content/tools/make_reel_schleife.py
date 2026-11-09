"""Reel «Schleife» (Coming soon) fuer Instagram aufbereiten: Video der Nutzerin (Schleife wird vom Laptop geloest,
dahinter das sunnozy-Profil, Lichterkette) bleibt, die eingebrannten Serifen-Texte werden durch die Hausschrift
Sacramento ersetzt (Markenregel: alle Instagram-Posts in Sacramento), Bild leicht klarer und waermer, Ton auf
Instagram-Lautstaerke (-14 LUFS, ohne Uebersteuern), neue Schlusskarte.

Ablauf Original (16,4 s): 0-2,5 «Psst ...», 2,7-8,4 «Wir packen gerade etwas aus.», 10-12,6 Logo + COMING SOON,
ab 12,6 weisse Schlusskarte. Die Texte stehen im dunklen Wandstreifen ueber dem Laptop; der Streifen wird pro Bild
aus seinen textfreien Raendern (links/rechts) neu aufgefuellt und weich angeschlossen.

Aufruf: python3 make_reel_schleife.py <original.mp4> <ausgabe.mp4>
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1:3]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SACRAMENTO = os.path.join(ROOT, 'fonts', 'sacramento.ttf')
W, H, FPS = 1080, 1920, 30
ENDE_FILM, UEBERGANG, ENDE = 12.6, 0.5, 15.6       # Film bis 12,6 s, dann 0,5 s Ueberblendung, Schlusskarte bis 15,6 s
WEISS, TINTE, GRUND = (255, 250, 242), (52, 50, 48), (252, 250, 247)

# (von, bis, Text, y-Mitte, Groesse) - Texte im Wandstreifen, unterhalb der Instagram-Kopfzeile (> 220 px)
TEXTE = [(0.0, 2.5, 'Psst ...', 345, 120),
         (2.7, 8.4, 'Wir packen gerade\netwas aus.', 300, 96),
         (10.0, ENDE_FILM, 'coming soon', 380, 96)]


def font(g):
    return ImageFont.truetype(SACRAMENTO, g)


def logo(breite, farbe):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), farbe + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((breite, round(L.height * breite / L.width)), Image.LANCZOS)


def text_ebene(text, y, g, farbe=WEISS, schatten=(40, 25, 12)):
    """RGBA-Ebene mit Text + weichem Schatten (lesbar auf dem dunklen Streifen)."""
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    f = font(g)
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).multiline_text((W // 2, y + 4), text, font=f, fill=170, anchor='mm', align='center', spacing=int(g * 0.05))
    e.paste(schatten + (255,), (0, 0), sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(e).multiline_text((W // 2, y), text, font=f, fill=farbe + (255,), anchor='mm', align='center', spacing=int(g * 0.05))
    return e


def streifen_ende(a):
    """Unterkante des dunklen Wandstreifens: erste Zeile ab 380 px, in der die Raender deutlich dunkler werden als
    40 px darueber (schwarzer Laptoprand unter der braunen Wand)."""
    rand = np.concatenate([a[:, :120], a[:, -120:]], axis=1).mean(axis=(1, 2))
    for y in range(380, 760):
        if rand[y] < 0.6 * rand[y - 40]:
            return y
    return 470


def streifen_saeubern(a):
    """Wandstreifen ohne Text: jede Zeile aus ihrem linken/rechten Rand linear auffuellen, weich in das Original."""
    yb = streifen_ende(a)
    links = a[:yb, 30:150].astype(float).mean(axis=1)
    rechts = a[:yb, -150:-30].astype(float).mean(axis=1)
    t = np.linspace(0, 1, W)[None, :, None]
    fuell = links[:, None, :] * (1 - t) + rechts[:, None, :] * t
    fuell += np.random.default_rng(0).normal(0, 1.2, fuell.shape)        # feines Korn wie im Video
    m = np.ones((yb, 1, 1)); k = 3
    m[yb - k:] = np.linspace(1, 0, k)[:, None, None]                      # untere Kante weich ins Original
    a = a.astype(float)
    a[:yb] = fuell * m + a[:yb] * (1 - m)
    return np.clip(a, 0, 255).astype(np.uint8)


def ebene_auf(bild, ebene, alpha):
    if alpha <= 0:
        return bild
    if alpha < 1:
        ebene = ebene.copy(); ebene.putalpha(ebene.getchannel('A').point(lambda v: int(v * alpha)))
    bild.alpha_composite(ebene)
    return bild


def deckkraft(t, von, bis, ein=0.35, aus=0.35):
    if t < von or t > bis:
        return 0.0
    return min(1.0, (t - von) / ein, (bis - t) / aus)


def schlusskarte():
    c = Image.new('RGBA', (W, H), GRUND + (255,))
    lg = logo(560, TINTE); c.alpha_composite(lg, ((W - lg.width) // 2, 700))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 1020), 'coming soon', font=font(120), fill=TINTE, anchor='mm')
    d.text((W // 2, 1170), 'sunnozy.ch', font=font(84), fill=(120, 112, 104), anchor='mm')
    d.text((W // 2, 1265), 'folg uns, damit du nichts verpasst', font=font(70), fill=(120, 112, 104), anchor='mm')
    return c


ebenen = [(v, b, text_ebene(tx, y, g)) for v, b, tx, y, g in TEXTE]
logo_film = Image.new('RGBA', (W, H), (0, 0, 0, 0))
lf = logo(470, WEISS); logo_film.alpha_composite(lf, ((W - lf.width) // 2, 215))
karte = schlusskarte()

dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-t', str(ENDE_FILM + UEBERGANG),
                        '-vf', 'eq=contrast=1.06:saturation=1.08:brightness=0.01,unsharp=5:5:0.5',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
tmp = out + '.tmp.mp4'
enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', tmp],
                       stdin=subprocess.PIPE)
n, letztes = 0, None
while True:
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3:
        break
    t = n / FPS
    a = streifen_saeubern(np.frombuffer(raw, np.uint8).reshape(H, W, 3))
    bild = Image.fromarray(a).convert('RGBA')
    for v, b, e in ebenen:
        bild = ebene_auf(bild, e, deckkraft(t, v, b))
    bild = ebene_auf(bild, logo_film, deckkraft(t, 10.0, ENDE_FILM))
    if t >= ENDE_FILM:                                                   # Ueberblendung zur Schlusskarte
        bild = Image.blend(bild, karte, min(1.0, (t - ENDE_FILM) / UEBERGANG))
    enc.stdin.write(bild.convert('RGB').tobytes()); n += 1
dec.wait()
k = karte.convert('RGB').tobytes()
while n < ENDE * FPS:
    enc.stdin.write(k); n += 1
enc.stdin.close(); enc.wait()
# Ton: Original, auf Instagram-Lautstaerke, am Ende ausblenden
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', src, '-map', '0:v', '-map', '1:a', '-t', str(ENDE),
                '-af', f'loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={ENDE - 1.2}:d=1.2', '-c:v', 'copy', '-c:a', 'aac',
                '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
os.remove(tmp)
print(out, f'{n / FPS:.1f} s')
