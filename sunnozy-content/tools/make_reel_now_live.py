"""«Jetzt online»-Reel für die Coming-soon-Sets (Wunsch der Nutzerin 24.11.2026, Vorbild: Stop-Motion-Reel «Now Live»:
freigestelltes Produkt in der Mitte, Hintergrund wechselt im Takt zwischen Weinrot, Tannengrün und Streifen).

Nur posten, wenn die gezeigten Sets in Shopify aktiv sind (Stand 24.11.2026: alle noch Entwurf).

    python3 tools/make_reel_now_live.py          # Deutsch und Englisch
    python3 tools/make_reel_now_live.py de
Ausgabe: posts/coming-soon/reels/now-live/reel_now_live_<sprache>_9x16.mp4 (+ _titelbild.jpg), Captions im README dort.
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
# Freigestellte Hauptbilder der Coming-soon-Sets (Shopify-Entwürfe)
BILDER = [FRE('best_family'), SET('born-in-2027-rosa'), FRE('wal_blau'), FRE('prinzessin_krone'), SET('eisbaer-taupe'),
          FRE('bauernhof'), SET('little-bear-rosa'), FRE('lila_hase'), SET('waldbaer-creme'), FRE('hase_rosa'),
          FRE('love_dad_mom'), FRE('gaensebluemchen')]
ROT, GRUEN, CREME_ST = (112, 18, 26), (26, 48, 34), (238, 228, 210)
TAKT = 0.4                 # Sekunden pro Bild, wie im Vorbild schnell im Takt
RUNDEN = 2
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'nunitosans-800.ttf')
TEXTE = {
    'de': dict(schild='jetzt online', karte=('Neue Erstausstattung', '12 Sets · jetzt online', SHOP)),
    'en': dict(schild='now live', karte=('new newborn sets', '12 sets · now live', 'link in bio · sunnozy.ch')),
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


HINTERGRUND = [Image.new('RGB', (W, H), ROT), Image.new('RGB', (W, H), GRUEN), streifen()]
FOLGE = [0, 1, 2, 2, 0, 1, 0, 2, 1, 1, 2, 0]   # Reihenfolge der Hintergründe, wie im Vorbild unregelmässig


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
    d.text((40, h / 2 + 2), text, font=fo, fill=ROT + (255,), anchor='lm')
    s.alpha_composite(em, (int(40 + tw + 14), (h - em.height) // 2))
    return s


def end_bild():
    c = Image.new('RGB', (1000, 1000), (250, 246, 240))
    for k, p in enumerate(BILDER[:4]):
        im, _ = produkt(p, 470, 470); c.paste(im, ((k % 2) * 510 + (490 - im.width) // 2, (k // 2) * 510 + (490 - im.height) // 2), im)
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
    n_bild = int(round(TAKT * FPS)); folge = [(i, (i + r * 5) % len(FOLGE)) for r in range(RUNDEN) for i in range(len(BILDER))]
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
