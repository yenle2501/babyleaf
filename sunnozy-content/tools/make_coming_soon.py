"""«Coming soon» fuer neue Erstausstattungs-Sets: Teaser-Reel, Sneak-Peek-Karussell und Story-Bilder.

Idee «Es kommt Nachwuchs.»: Die neuen Sets werden nur als Ausschnitt gezeigt (ein Detail wie das Baerenmotiv),
im Reel erst unscharf, dann scharf. Kein Datum und kein Preis (stehen noch nicht fest), Ziel: Neugier, Folgen,
Kommentare. Look nach dem sunnozy-Designsystem (Creme, Waldgruen, Fraunces, Nunito Sans, keine Emojis).

Aufruf: python3 make_coming_soon.py <ausgabe-ordner>
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRAES = os.path.join(ROOT, 'posts', 'produktfotos-set-praesentation', 'ohne_logo')
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
CREME, WALD, SALBEI, GRAU, ROSE = (253, 252, 250), (35, 48, 41), (122, 139, 111), (98, 108, 102), (248, 234, 228)
FPS = 30

# Datei, Name, Hinweis, Ausschnitt-Mitte (Anteil x, y), Ausschnitt-Groesse (Anteil der Breite)
NEU = [('set_weltall_hellblau', '«Weltall»', 'Hellblau', (0.70, 0.33), 0.42),
       ('set_waldbaer_creme', '«Waldbär»', 'Creme', (0.61, 0.52), 0.40),
       ('set_teddy_rosa_punkte', '«Teddy»', 'Rosa mit Pünktchen', (0.66, 0.55), 0.40),
       ('set_hund_creme', '«Hund»', 'Creme', (0.84, 0.81), 0.36),
       ('set_smile_gruen', '«Smile»', 'Salbei', (0.80, 0.60), 0.42)]


def ausschnitt(datei, mitte, groesse):
    im = Image.open(os.path.join(PRAES, datei + '_quadratisch.jpg')).convert('RGB')
    s = int(im.width * groesse)
    cx, cy = int(im.width * mitte[0]), int(im.height * mitte[1])
    x0 = min(max(0, cx - s // 2), im.width - s); y0 = min(max(0, cy - s // 2), im.height - s)
    return im.crop((x0, y0, x0 + s, y0 + s))


def load_logo(width, col=WALD):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def gesperrt(d, xy, text, font, fill, sp):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = xy[0] - w / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def mischen(a, b, u):
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))


# ---------------- Teaser-Reel ----------------
def reel(W=1080, H=1920):
    crops = [ausschnitt(d, m, g) for d, _, _, m, g in NEU]
    T1, T2, T_SET, T_END = 1.5, 1.8, 1.15, 2.6
    t_sets = T1 + T2; t_end = t_sets + len(NEU) * T_SET; dauer = t_end + T_END
    box = 880

    def bild(t):
        c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
        if t < T1:
            u = ease(t / 0.4)
            d.text((W / 2, H * 0.44), 'Psst …', font=FONT('fraunces-600.ttf', 130), fill=mischen(CREME, WALD, u), anchor='mm')
            return c
        if t < t_sets:
            u = ease((t - T1) / 0.4)
            d.text((W / 2, H * 0.40), 'Es kommt', font=FONT('fraunces-600.ttf', 120), fill=mischen(CREME, WALD, u), anchor='mm')
            d.text((W / 2, H * 0.40 + 135), 'Nachwuchs.', font=FONT('fraunces-600.ttf', 120), fill=mischen(CREME, WALD, u), anchor='mm')
            gesperrt(d, (W / 2, H * 0.40 + 260), 'NEUE ERSTAUSSTATTUNGS-SETS', FONT('nunitosans-700.ttf', 30), mischen(CREME, SALBEI, u), 4)
            return c
        if t < t_end:
            i = int((t - t_sets) / T_SET); u = (t - t_sets - i * T_SET) / T_SET
            cr = crops[i]
            z = 1.0 + 0.06 * u
            im = cr.resize((int(box * z), int(box * z)), Image.LANCZOS)
            blur = 26 * (1 - ease(u / 0.55))
            if blur > 0.5:
                im = im.filter(ImageFilter.GaussianBlur(blur))
            im = im.crop(((im.width - box) // 2, (im.height - box) // 2, (im.width - box) // 2 + box, (im.height - box) // 2 + box))
            y0 = int(H * 0.47 - box / 2)
            c.paste(im, ((W - box) // 2, y0))
            gesperrt(d, (W / 2, y0 - 70), f'NEU  ·  {i + 1} VON {len(NEU)}', FONT('nunitosans-700.ttf', 28), SALBEI, 4)
            a = ease((u - 0.35) / 0.3)
            if a > 0:
                _, name, hinweis, _, _ = NEU[i]
                d.text((W / 2, y0 + box + 85), name, font=FONT('fraunces-600.ttf', 76), fill=mischen(CREME, WALD, a), anchor='mm')
                d.text((W / 2, y0 + box + 160), hinweis, font=FONT('nunitosans-400.ttf', 36), fill=mischen(CREME, GRAU, a), anchor='mm')
            return c
        u = ease((t - t_end) / 0.45)
        d.text((W / 2, H * 0.36), 'Bald bei sunnozy.', font=FONT('fraunces-600.ttf', 100), fill=mischen(CREME, WALD, u), anchor='mm')
        d.text((W / 2, H * 0.36 + 120), 'Folge @sunnozy.ch,', font=FONT('nunitosans-400.ttf', 40), fill=mischen(CREME, GRAU, u), anchor='mm')
        d.text((W / 2, H * 0.36 + 175), 'damit Du den Start nicht verpasst.', font=FONT('nunitosans-400.ttf', 40), fill=mischen(CREME, GRAU, u), anchor='mm')
        lg = load_logo(320); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * u)))
        c.paste(lg, ((W - lg.width) // 2, int(H * 0.36 + 270)), lg)
        return c

    pfad = os.path.join(out, 'reel_coming_soon_9x16')
    tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = round(dauer * FPS)
    for k in range(n):
        enc.stdin.write(bild(k / FPS).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad + '.mp4'], check=True)
    os.remove(tmp)
    bild(T1 + 1.2).save(pfad + '_standbild.jpg', quality=93)
    print('reel', f'{n / FPS:.1f} s')


# ---------------- Sneak-Peek-Karussell 4:5 ----------------
def karussell(W=1080, H=1350):
    d_out = os.path.join(out, 'karussell_sneak_peek'); os.makedirs(d_out, exist_ok=True)
    # 1 Titel
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    gesperrt(d, (W / 2, 330), 'SNEAK PEEK', FONT('nunitosans-700.ttf', 30), SALBEI, 6)
    d.text((W / 2, 520), 'Es kommt', font=FONT('fraunces-600.ttf', 130), fill=WALD, anchor='mm')
    d.text((W / 2, 670), 'Nachwuchs.', font=FONT('fraunces-600.ttf', 130), fill=WALD, anchor='mm')
    d.text((W / 2, 820), f'{len(NEU)} neue Erstausstattungs-Sets', font=FONT('nunitosans-400.ttf', 42), fill=GRAU, anchor='mm')
    d.text((W / 2, 880), 'Wisch für einen ersten Blick', font=FONT('nunitosans-400i.ttf', 36), fill=GRAU, anchor='mm')
    lg = load_logo(260); c.paste(lg, ((W - lg.width) // 2, H - 170), lg)
    c.save(os.path.join(d_out, '01_titel.jpg'), quality=93)
    # 2..: Ausschnitte
    for i, (datei, name, hinweis, m, g) in enumerate(NEU):
        c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
        box = 900; cr = ausschnitt(datei, m, g).resize((box, box), Image.LANCZOS)
        c.paste(cr, ((W - box) // 2, 120))
        gesperrt(d, (W / 2, 85), f'NEU  ·  {i + 1} VON {len(NEU)}', FONT('nunitosans-700.ttf', 26), SALBEI, 4)
        d.text((W / 2, 1110), name, font=FONT('fraunces-600.ttf', 80), fill=WALD, anchor='mm')
        d.text((W / 2, 1185), hinweis + '  ·  bald erhältlich', font=FONT('nunitosans-400.ttf', 36), fill=GRAU, anchor='mm')
        c.save(os.path.join(d_out, f'{i + 2:02d}_{datei.replace("set_", "")}.jpg'), quality=93)
    # letzte: Frage
    c = Image.new('RGB', (W, H), ROSE); d = ImageDraw.Draw(c)
    d.text((W / 2, 520), 'Welches wird', font=FONT('fraunces-600.ttf', 104), fill=WALD, anchor='mm')
    d.text((W / 2, 640), 'Dein Favorit?', font=FONT('fraunces-600.ttf', 104), fill=WALD, anchor='mm')
    d.text((W / 2, 790), 'Schreib es in die Kommentare.', font=FONT('nunitosans-400.ttf', 42), fill=GRAU, anchor='mm')
    d.text((W / 2, 850), 'Bald auf sunnozy.ch', font=FONT('nunitosans-700.ttf', 42), fill=WALD, anchor='mm')
    lg = load_logo(260); c.paste(lg, ((W - lg.width) // 2, H - 170), lg)
    c.save(os.path.join(d_out, f'{len(NEU) + 2:02d}_frage.jpg'), quality=93)


# ---------------- Stories 9:16 (Platz fuer Instagram-Sticker) ----------------
def stories(W=1080, H=1920):
    d_out = os.path.join(out, 'stories'); os.makedirs(d_out, exist_ok=True)
    crops = [ausschnitt(d, m, g) for d, _, _, m, g in NEU]
    # 1 Countdown
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    gesperrt(d, (W / 2, 330), 'COMING SOON', FONT('nunitosans-700.ttf', 32), SALBEI, 6)
    d.text((W / 2, 480), 'Neue Sets', font=FONT('fraunces-600.ttf', 120), fill=WALD, anchor='mm')
    d.text((W / 2, 610), 'sind unterwegs.', font=FONT('fraunces-600.ttf', 84), fill=WALD, anchor='mm')
    cr = crops[0].resize((620, 620), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    c.paste(cr, ((W - 620) // 2, 720))
    d.text((W / 2, 1420), 'Hier den Countdown-Sticker setzen', font=FONT('nunitosans-400i.ttf', 30), fill=(190, 186, 180), anchor='mm')
    c.save(os.path.join(d_out, 'story_1_countdown.jpg'), quality=93)
    # 2 Umfrage
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    d.text((W / 2, 340), 'Welches Set', font=FONT('fraunces-600.ttf', 96), fill=WALD, anchor='mm')
    d.text((W / 2, 450), 'willst Du zuerst sehen?', font=FONT('fraunces-600.ttf', 64), fill=WALD, anchor='mm')
    for k, i in enumerate((0, 2)):
        im = crops[i].resize((470, 470), Image.LANCZOS)
        x = 50 + k * 510
        c.paste(im, (x, 560))
        d.text((x + 235, 1075), NEU[i][1], font=FONT('fraunces-600.ttf', 54), fill=WALD, anchor='mm')
    d.text((W / 2, 1300), 'Hier den Umfrage-Sticker setzen', font=FONT('nunitosans-400i.ttf', 30), fill=(190, 186, 180), anchor='mm')
    c.save(os.path.join(d_out, 'story_2_umfrage.jpg'), quality=93)
    # 3 Erinnerung
    c = Image.new('RGB', (W, H), ROSE); d = ImageDraw.Draw(c)
    d.text((W / 2, 600), 'Nichts verpassen?', font=FONT('fraunces-600.ttf', 96), fill=WALD, anchor='mm')
    d.text((W / 2, 720), 'Tippe auf «Erinnern»,', font=FONT('nunitosans-400.ttf', 44), fill=GRAU, anchor='mm')
    d.text((W / 2, 780), 'dann sagen wir Dir Bescheid.', font=FONT('nunitosans-400.ttf', 44), fill=GRAU, anchor='mm')
    d.text((W / 2, 1000), 'Hier den Countdown-Sticker mit Erinnerung setzen', font=FONT('nunitosans-400i.ttf', 30), fill=(170, 150, 140), anchor='mm')
    lg = load_logo(280); c.paste(lg, ((W - lg.width) // 2, 1300), lg)
    c.save(os.path.join(d_out, 'story_3_erinnern.jpg'), quality=93)


if __name__ == '__main__':
    teil = sys.argv[2:] or ['karussell', 'stories', 'reel']
    for t in teil:
        globals()[t]()
