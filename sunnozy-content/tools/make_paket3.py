"""Paket 3: Posts im Hausstil, drittes 9er-Raster, Kliniktaschen-Karussell und 3 Reels aus KI-Fotos (Canva).

Aufruf: python3 make_paket3.py <ki-foto-ordner> <ausgabeordner>
"""
import sys, os, subprocess
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
here = os.path.dirname(os.path.abspath(__file__))
gen, out = sys.argv[1:3]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x', gen, gen, gen, out]
exec(src, g)
Image, ImageDraw = g['Image'], g['ImageDraw']
fill, grade, logo, F, SERR, SERI, HAND = g['fill'], g['grade'], g['logo'], g['F'], g['SERR'], g['SERI'], g['HAND']
spaced, sprig, np = g['spaced'], g['sprig'], g['np']
hand, put_logo, heart = g['g']['hand'], g['g']['put_logo'], g['g']['heart']
CREAM, PINK, INK, SOFT, SANS = g['CREAM'], g['PINK'], g['INK'], g['SOFT'], g['SANS']
W, H = 1080, 1350
SAGE, LILA = (214, 222, 205), (226, 216, 234)
P = lambda k: Image.open(os.path.join(gen, k + '.jpg')).convert('RGB')


def save(img, sub, name):
    d = os.path.join(out, sub); os.makedirs(d, exist_ok=True)
    img.convert('RGB').save(os.path.join(d, name), quality=94)


def handpost(key, text, y=1060, ay=0.4, w=W, h=H, size=92, logo_bottom=40):
    img = grade(fill(P(key), w, h, ay))
    band = np.asarray(img.crop((150, y - 20, w - 150, y + 230)).convert('L')).mean()
    light = band > 165
    hand(img, (w // 2, y), text, size, fill=(112, 82, 66) if light else (255, 251, 244), anchor='ma', rot=2, shadow=not light)
    put_logo(img, 150, logo_bottom, (90, 70, 60) if light else (255, 255, 255))
    return img


# ---------- A) Hausstil Handschrift: 8 Posts ----------
HS = [
    ('schwanger', 'Noch ein paar Wochen.\nUnd schon so viel Liebe.', 990, 0.3),
    ('fuesse', 'Diese kleinen Füsse\nhaben alles verändert.', 1000, 0.5),
    ('papa', 'Schick das dem Papa,\nder jetzt alles beschützt.', 990, 0.4),
    ('gaehnen', 'Wenn die Nacht kurz war\nund der Kaffee kalt ist.', 1010, 0.4),
    ('fenster', 'Kleiner Mensch.\nGrosses Zuhause.', 1000, 0.4),
    ('pucken', 'Die erste Nacht zuhause.\nNiemand vergisst sie.', 1020, 0.4),
    ('hand', 'Halt sie fest.\nSie werden so schnell gross.', 1000, 0.4),
    ('geschenk', 'Für die Freundin,\ndie bald Mama wird.', 1000, 0.5),
]
for i, (k, t, y, ay) in enumerate(HS, 1):
    save(handpost(k, t, y, ay), 'handschrift', f'{i:02d}_{k}.jpg')

# ---------- B) Drittes 9er-Raster (Pin-Stil) ----------
R = 'raster-3'
t = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(t)
sprig(d, W / 2, 470, 1.4, SOFT)
for i, ln in enumerate(['ERSTAUSSTATTUNG.', 'MIT LIEBE GEPACKT.']):
    spaced(d, W / 2, 560 + i * 95, ln, F(SERR, 66), INK, 11)
d.line([(W / 2 - 90, 790), (W / 2 + 90, 790)], fill=SOFT, width=2)
L = logo(220, INK); t.paste(L, ((W - L.width) // 2, 840), L)
save(t, R, '01_erstausstattung.jpg')
save(grade(fill(P('flatlay'), W, H, 0.5)), R, '02_set_rosa.jpg')
save(grade(fill(P('socken'), W, H, 0.5)), R, '03_socken.jpg')
save(grade(fill(P('korb'), W, H, 0.5)), R, '04_mulltuecher.jpg')
z = Image.new('RGB', (W, H), PINK); d = ImageDraw.Draw(z)
sprig(d, W / 2, 420, 1.3, INK)
for i, ln in enumerate(['DAS SCHÖNSTE', 'AN KLEINEN DINGEN:', 'SIE BLEIBEN', 'NICHT LANGE KLEIN.']):
    spaced(d, W / 2, 520 + i * 82, ln, F(SERR, 52), INK, 8)
d.line([(W / 2 - 70, 880), (W / 2 + 70, 880)], fill=INK, width=2)
L = logo(220, INK); z.paste(L, ((W - L.width) // 2, 930), L)
save(z, R, '05_zitat.jpg')
save(grade(fill(P('stange'), W, H, 0.4)), R, '06_kleiderstange.jpg')
# Tipp-Kachel
v = Image.new('RGB', (W, H), SAGE); d = ImageDraw.Draw(v)
spaced(d, W / 2, 230, 'TIPP', F(SERR, 40), INK, 14)
d.line([(W / 2 - 60, 300), (W / 2 + 60, 300)], fill=INK, width=2)
for i, ln in enumerate(['Wasch alle Babykleider', 'vor dem ersten Tragen –', 'ohne Weichspüler.', '', 'So bleibt die Baumwolle', 'weich und sanft zur Haut.']):
    w_ = d.textlength(ln, font=F(SERR, 56)); d.text(((W - w_) / 2, 400 + i * 78), ln, font=F(SERR, 56), fill=INK)
sprig(d, W / 2, 1000, 1.0, INK)
L = logo(200, INK); v.paste(L, ((W - L.width) // 2, 1120), L)
save(v, R, '07_tipp.jpg')
save(grade(fill(P('kliniktasche'), W, H, 0.5)), R, '08_kliniktasche.jpg')
c = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(c)
heart(d, W / 2, 400, 36, SOFT, 3)
for i, ln in enumerate(['WEICH.', 'SICHER.', 'LIEBEVOLL.']):
    spaced(d, W / 2, 500 + i * 100, ln, F(SERR, 72), INK, 14)
d.rectangle([0, 1080, W, H], fill=LILA)
L = logo(300, INK); c.paste(L, ((W - L.width) // 2, 1080 + (270 - L.height) // 2), L)
save(c, R, '09_werte.jpg')
fs = sorted(f for f in os.listdir(os.path.join(out, R)) if f[:2].isdigit())
gv = Image.new('RGB', (3 * 360 + 8, 3 * 450 + 8), 'white')
for i, f in enumerate(fs):
    gv.paste(Image.open(os.path.join(out, R, f)).resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
gv.save(os.path.join(out, R, 'raster_vorschau.png'))

# ---------- C) Karussell: Kliniktasche-Checkliste ----------
K = 'karussell-kliniktasche'
save(handpost('kliniktasche', 'Kliniktasche fürs Baby.\nDie ehrliche Liste.', 990, 0.5), K, '01_cover.jpg')
SL = [
    ('FÜR DIE ERSTEN TAGE', ['4–5 Bodys (Gr. 50/56)', '2–3 Hosen oder Strampler', '1 Häubchen', '2 Paar Söckchen', 'Kratzhandschuhe'], CREAM, 'Tipp: Alles vorher waschen.'),
    ('FÜR DEN HEIMWEG', ['1 weiches Set zum Anziehen', 'Jacke oder Overall', 'eine warme Decke', 'die Babyschale fürs Auto'], PINK, 'Das erste Outfit für zuhause.'),
    ('ZUM KUSCHELN & PFLEGEN', ['3–4 Mulltücher', 'ein Spucktuch', 'ein Nuschi zum Kuscheln'], LILA, 'Windeln? Frag dein Spital –\noft sind sie schon da.'),
    ('DAS BRAUCHST DU NICHT', ['zehn Outfits', 'Schuhe', 'alles nur in Grösse 50'], SAGE, 'Babys wachsen schnell!'),
]
for i, (title, items, bg, note) in enumerate(SL, 2):
    s = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(s)
    spaced(d, W / 2, 190, f'{i - 1} / 4', F(SANS, 26), SOFT, 6)
    spaced(d, W / 2, 260, title, F(SERR, 50), INK, 8)
    d.line([(W / 2 - 80, 345), (W / 2 + 80, 345)], fill=INK, width=2)
    for j, it in enumerate(items):
        y = 440 + j * 112
        heart(d, 210, y + 30, 14, INK, 2)
        d.text((260, y), it, font=F(SERR, 54), fill=INK)
    hand(s, (W // 2, 1000), note, 66, fill=(120, 88, 74), anchor='ma', rot=2, shadow=False)
    L = logo(170, INK); s.paste(L, ((W - L.width) // 2, H - L.height - 60), L)
    save(s, K, f'{i:02d}_liste.jpg')
e = handpost('flatlay', 'Speicher dir die Liste\n& schick sie weiter.', 1000, 0.5)
save(e, K, '06_ende.jpg')

# ---------- D) Reels (9:16, 30 fps) ----------
RW, RH, FPS = 1080, 1920, 30
RD = os.path.join(out, 'reels'); os.makedirs(RD, exist_ok=True)


def end_card():
    c = Image.new('RGB', (RW, RH), CREAM); d = ImageDraw.Draw(c)
    sprig(d, RW / 2, 640, 1.5, SOFT)
    L = logo(560, INK); c.paste(L, ((RW - L.width) // 2, 740), L)
    spaced(d, RW / 2, 960, 'WEICH. SICHER. LIEBEVOLL.', F(SERR, 40), INK, 8)
    d.line([(RW / 2 - 90, 1040), (RW / 2 + 90, 1040)], fill=SOFT, width=2)
    spaced(d, RW / 2, 1090, 'SUNNOZY.CH', F(SANS, 34), SOFT, 8)
    spaced(d, RW / 2, 1150, 'GRATIS VERSAND AB CHF 50', F(SANS, 26), SOFT, 5)
    return c


def text_layer(base, text, size=104, y=1380):
    """Transparente Ebene mit Handschrift, Farbe je nach Bildhelligkeit."""
    lay = Image.new('RGBA', (RW, RH), (0, 0, 0, 0))
    if not text: return lay
    band = np.asarray(base.crop((150, y - 20, RW - 150, y + 260)).convert('L')).mean()
    light = band > 165
    hand(lay, (RW // 2, y), text, size, fill=(112, 82, 66) if light else (255, 251, 244), anchor='ma', rot=2, shadow=not light)
    return lay


def reel(name, scenes, dur=2.7, fade=0.45):
    """scenes: Liste (key|Image, text, ay). Ken Burns + Kreuzblende + eingeblendete Handschrift."""
    clips = []
    for k, txt, ay in scenes:
        im = k if isinstance(k, Image.Image) else grade(fill(P(k), int(RW * 1.1), int(RH * 1.1), ay))
        if im.size != (int(RW * 1.1), int(RH * 1.1)): im = im.resize((int(RW * 1.1), int(RH * 1.1)))
        mid = im.resize((RW, RH))
        clips.append((im, text_layer(mid, txt), isinstance(k, Image.Image)))
    n = int(dur * FPS); nf = int(fade * FPS)
    tmp = os.path.join(RD, name + '_tmp.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', tmp], stdin=subprocess.PIPE)

    def frame(ci, f):
        im, lay, static = clips[ci]
        z = 1.0 if static else 1.0 + 0.09 * f / n
        cw, ch = int(im.width / 1.1 / z * 1.0), int(im.height / 1.1 / z)
        x0 = (im.width - cw) // 2; y0 = int((im.height - ch) * (0.5 - 0.3 * (f / n - 0.5) * (ci % 2 * 2 - 1)))
        fr = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((RW, RH), Image.BILINEAR).convert('RGBA')
        a = min(1.0, max(0.0, (f - 6) / 12))
        if a > 0:
            l2 = lay.copy(); l2.putalpha(lay.split()[3].point(lambda v: int(v * a)))
            fr = Image.alpha_composite(fr, l2)
        return fr.convert('RGB')

    for ci in range(len(clips)):
        for f in range(n - nf if ci < len(clips) - 1 else n + 20):
            fr = frame(ci, f)
            if ci > 0 and f < nf:
                fr = Image.blend(frame(ci - 1, n - nf + f), fr, f / nf)
            p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    dst = os.path.join(RD, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', dst], check=True)
    os.remove(tmp)
    print(name, 'ok')


END = end_card()
END.save(os.path.join(RD, 'endkarte.jpg'), quality=92)
reel('reel_kleine_momente', [
    ('fuesse', 'Niemand sagt dir …', 0.5),
    ('hand', '… dass du sie stundenlang\nanschauen wirst.', 0.4),
    ('gaehnen', 'Jedes Gähnen.', 0.4),
    ('papa', 'Jeder Atemzug.', 0.4),
    ('fenster', 'Unser kleiner Mensch.', 0.4),
    (END, '', 0.5),
])
reel('reel_kliniktasche_pov', [
    ('schwanger', 'POV: noch 4 Wochen', 0.3),
    ('flatlay', 'alles ist gewaschen', 0.5),
    ('socken', 'die kleinsten Socken\nder Welt', 0.5),
    ('korb', 'dreimal gefaltet.\nvielleicht viermal.', 0.5),
    ('kliniktasche', 'die Tasche steht bereit.', 0.5),
    (END, '', 0.5),
])
reel('reel_geschenkidee', [
    ('geschenk', 'Suchst du ein Geschenk\nfür eine neue Mama?', 0.5),
    ('stange', 'weich.', 0.4),
    ('pucken', 'sicher.', 0.4),
    ('flatlay', 'liebevoll.', 0.5),
    (END, '', 0.5),
])
