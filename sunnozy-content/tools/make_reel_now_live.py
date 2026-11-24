"""«Jetzt online»-Reel für die Coming-soon-Sets (Wunsch der Nutzerin 24.11.2026, Vorbild: Stop-Motion-Reel «Now Live»:
freigestelltes Produkt in der Mitte, Hintergrund wechselt im Takt zwischen Weinrot, Tannengrün und Streifen).

Nur posten, wenn die gezeigten Sets in Shopify aktiv sind (Stand 24.11.2026: Teddybär und Princess aktiv, Teddybär
ausverkauft; Little Princess Krone, Hase Rosa, I love Dogs noch Entwurf).

    python3 tools/make_reel_now_live.py
Ausgabe: posts/coming-soon/reels/now-live/reel_now_live_en_9x16.mp4 (+ _titelbild.jpg), Captions im README dort.
"""
import os, sys, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_reel_hello_little_bear_hook as hk
from endfolie import anhaengen, SHOP

W, H, FPS = m.W, m.H, 30
CS = os.path.join(m.POSTS, 'coming-soon', 'photos')
OUT = os.path.join(m.POSTS, 'coming-soon', 'reels', 'now-live')
FRE = lambda k: os.path.join(CS, 'marktplatz-galaxus-amazon', 'freigestellt', f'set_{k}.png')
SET = lambda k: os.path.join(CS, k, 'marktplatz', f'{k}_freigestellt.png')
# Die fünf 8-teiligen Sets (Wunsch der Nutzerin 24.11.2026): Teddybär, Little Princess Krone, Hase Rosa, Princess, I love Dogs
BILDER = [FRE('teddy_creme'), FRE('prinzessin_krone'), FRE('hase_rosa'), FRE('rosa_A'),
          os.path.join(CS, 'produktfotos-set-praesentation', 'freigestellt', 'set_hund_creme.png')]   # mit rembg freigestellt
# Ruhigere Farben (Wunsch: andere Hintergrundfarbe als im Vorbild)
ROSE, SALBEI, MOKKA, CREME_ST = (205, 154, 150), (146, 166, 136), (168, 132, 104), (244, 236, 224)
ROT, GRUEN = ROSE, SALBEI        # Streifen: Creme, Rosa, Creme, Salbei
TAKT = 0.9                 # Sekunden pro Bild (Wunsch: langsamer als im Vorbild)
RUNDEN = 2
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'nunitosans-800.ttf')
TEXTE = {   # ab 24.11.2026 alles auf Englisch
    'en': dict(schild='now live', karte=('our newborn sets', '8 pieces each · now live', SHOP)),
}


def streifen():
    c = Image.new('RGB', (W, H), CREME_ST); d = ImageDraw.Draw(c); x = 0
    for k in range(200):
        breite, farbe = [(54, CREME_ST), (42, ROT), (54, CREME_ST), (30, GRUEN)][k % 4]
        if farbe != CREME_ST:
            d.rectangle((x, 0, x + breite - 1, H), fill=farbe)
        x += breite
        if x > W:
            break
    return c


HINTERGRUND = [Image.new('RGB', (W, H), ROSE), Image.new('RGB', (W, H), SALBEI), streifen(), Image.new('RGB', (W, H), MOKKA)]
FOLGE = [0, 1, 2, 3, 2, 0, 3, 1, 2, 0]   # Reihenfolge der Hintergründe


def produkt(pfad, breite=900, hoehe=900):
    im = Image.open(pfad).convert('RGBA'); im = im.crop(im.getbbox())
    s = min(breite / im.width, hoehe / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    schatten = Image.new('RGBA', (im.width + 120, im.height + 120), (0, 0, 0, 0))
    schatten.paste((0, 0, 0, 90), (60, 75), im.split()[3].point(lambda a: 255 if a > 20 else 0))
    return im, schatten.filter(ImageFilter.GaussianBlur(28))


def schild(text):
    fo = ImageFont.truetype(SCHRIFT, 52); em = hk.emoji('✨', 50)
    d0 = ImageDraw.Draw(Image.new('RGB', (1, 1))); tw = d0.textlength(text, font=fo)
    b, h = int(tw + em.width + 14 + 80), 96
    s = Image.new('RGBA', (b, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((0, 0, b - 1, h - 1), radius=h // 2, fill=CREME_ST + (255,))
    d.text((40, h / 2 + 2), text, font=fo, fill=MOKKA + (255,), anchor='lm')
    s.alpha_composite(em, (int(40 + tw + 14), (h - em.height) // 2))
    return s


def end_bild():
    """Alle Sets aus dem Reel: 3 oben, der Rest unten mittig."""
    c = Image.new('RGB', (1000, 700), (250, 246, 240)); n = len(BILDER); oben = (n + 1) // 2
    for k, p in enumerate(BILDER):
        reihe, pos = (0, k) if k < oben else (1, k - oben)
        anzahl = oben if reihe == 0 else n - oben
        im, _ = produkt(p, 310, 310)
        x0 = (1000 - anzahl * 330) // 2 + pos * 330
        c.paste(im, (x0 + (310 - im.width) // 2, 20 + reihe * 340 + (310 - im.height) // 2), im)
    pfad = os.path.join(tempfile.gettempdir(), 'now_live_endbild.jpg'); c.save(pfad, quality=94)
    return pfad


def reel(sprache):
    t = TEXTE[sprache]
    teile = [produkt(p) for p in BILDER]
    sch = schild(t['schild'])
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_now_live_{sprache}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    if os.path.exists(pfad):
        os.remove(pfad)
    n_bild = int(round(TAKT * FPS)); folge = [(i, (i + r * len(BILDER)) % len(FOLGE)) for r in range(RUNDEN) for i in range(len(BILDER))]
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = 0
    for k, (i, f) in enumerate(folge):
        c = HINTERGRUND[FOLGE[f]].copy().convert('RGBA')
        im, schatten = teile[i]
        x, y = (W - im.width) // 2, 1000 - im.height // 2
        c.alpha_composite(schatten, (x - 60, y - 60)); c.alpha_composite(im, (x, y))
        c.alpha_composite(sch, ((W - sch.width) // 2, 250))
        fr = c.convert('RGB')
        if k == 1:
            fr.save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        for _ in range(n_bild):
            enc.stdin.write(fr.tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    d = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', k1.MUSIK, '-t', f'{d:.2f}',
                    '-af', f'afade=t=in:d=0.2,afade=t=out:st={d - 1.0:.2f}:d=1.0,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {d:.1f} s', flush=True)
    anhaengen(pfad, end_bild(), *t['karte'])


if __name__ == '__main__':
    for s in sys.argv[1:] or list(TEXTE):
        reel(s)
