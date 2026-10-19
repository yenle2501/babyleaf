"""Erzeugt die neuen Posts und Stories fuer den Wochenplan KW 43 (sunnozy-Stil, 4:5 bzw. 9:16).

Aufruf: python3 make_week.py <logo.webp> <ordner mit baby-fotos> <ordner mit packshots> <ausgabeordner>
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
import numpy as np

logo_src, photo_dir, pack_dir, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)

W, H = 1080, 1350
BG, CREAM, PALE = (252, 249, 246), (246, 240, 232), (247, 234, 228)
TERRA, PEACH, INK, MAUVE = (181, 72, 63), (236, 154, 138), (40, 44, 42), (122, 90, 95)
SER = '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
SANSB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
font = lambda p, s: ImageFont.truetype(p, s)


# ---------- Bausteine ----------
def knockout(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.15, 0, 1)
    al[al < 0.06] = 0
    rgb = np.where(al[..., None] > 0, (a - 255 * (1 - al[..., None])) / np.maximum(al[..., None], 1e-3), 0)
    L = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8), 'RGBA')
    return L.crop(L.getbbox())


LOGO = knockout(logo_src)


def logo(width, white=False):
    L = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if white:
        a = np.asarray(L).astype(float)
        a[a[..., :3].max(axis=2) < 90, :3] = 255
        L = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return L


def paste_logo(img, width=210, bottom=50, white=False):
    L = logo(width, white)
    img.paste(L, ((img.width - L.width) // 2, img.height - L.height - bottom), L)


def fill(img, w, h, ay=0.5):
    s = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def fit(img, w, h):
    s = min(w / img.width, h / img.height)
    return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)


def grade(im):
    a = np.asarray(im.convert('RGB')).astype(float)
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 0.88
    a[..., 0] *= 1.02; a[..., 2] *= 0.985
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def rounded(img, r):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width, img.height], r, fill=255)
    return m


def card(canvas, im, box, r=28, pad=30):
    """Karte mit Packshot; Kartenfarbe = Hintergrundfarbe des Packshots (weiss oder hellgrau)."""
    x0, y0, x1, y1 = box
    a0 = np.asarray(im)
    nz = np.argwhere(a0.min(axis=2) < 246)  # weissen Rand abschneiden
    if len(nz):
        (ty, tx), (by, bx) = nz.min(0), nz.max(0); im = im.crop((tx, ty, bx + 1, by + 1))
    a = np.asarray(im)
    color = tuple(int(v) for v in np.median(np.concatenate([a[:10, :10].reshape(-1, 3), a[:10, -10:].reshape(-1, 3)]), axis=0))
    if min(color) < 200:  # Packshot ohne hellen Rand: bildfuellend
        ph = fill(im, x1 - x0, y1 - y0); canvas.paste(ph, (x0, y0), rounded(ph, r)); return
    ImageDraw.Draw(canvas).rounded_rectangle(box, r, fill=color)
    p = fit(im, x1 - x0 - 2 * pad, y1 - y0 - 2 * pad)
    canvas.paste(p, (x0 + (x1 - x0 - p.width) // 2, y0 + (y1 - y0 - p.height) // 2))


def ctext(d, y, s, f, col, w=W):
    d.text(((w - d.textlength(s, font=f)) / 2, y), s, font=f, fill=col)


def wrap(d, s, f, maxw):
    lines, cur = [], ''
    for word in s.split():
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = word
    return lines + [cur]


def ctext_wrap(d, y, s, f, col, maxw=860, lh=1.35, w=W):
    for line in wrap(d, s, f, maxw):
        ctext(d, y, line, f, col, w); y += int(f.size * lh)
    return y


def dots(d, y, w=W):
    for dx in (-30, 0, 30): d.ellipse([w / 2 + dx - 7, y - 7, w / 2 + dx + 7, y + 7], fill=PEACH)


def ch_badge(d, x0, y0, bs):
    d.rounded_rectangle([x0, y0, x0 + bs, y0 + bs], radius=bs * 0.22, fill=(205, 82, 72))
    c, m, a, b = x0 + bs / 2, y0 + bs / 2, bs * 0.12, bs * 0.34
    d.rectangle([c - a, m - b, c + a, m + b], fill='white'); d.rectangle([c - b, m - a, c + b, m + a], fill='white')


def endslide(w=W, h=H):
    e = Image.new('RGB', (w, h), BG); d = ImageDraw.Draw(e)
    k = w / 1080
    cx, cy, R = w // 2, int(h * 0.385), int(330 * k)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=PALE)
    for i in range(16):
        ang = i * math.pi / 8; r1, r2 = R + 30 * k, R + (70 if i % 2 == 0 else 55) * k
        d.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)],
               fill=PEACH if i % 2 == 0 else TERRA, width=int((8 if i % 2 == 0 else 6) * k))
    L = logo(int(540 * k)); e.paste(L, (cx - L.width // 2, cy - L.height // 2), L)
    y = cy + R + int(110 * k)
    ctext(d, y, 'Für kleine Sonnenscheine', font(SER, int(74 * k)), TERRA, w)
    dots(d, y + int(120 * k), w)
    ctext(d, y + int(150 * k), 'Erstausstattung aus 100 % Baumwolle', font(SANS, int(34 * k)), INK, w)
    ctext(d, y + int(210 * k), 'sunnozy.ch', font(SANSB, int(42 * k)), TERRA, w)
    f4 = font(SANS, int(29 * k)); s, sp, bs, gp = 'VERSAND AUS DER SCHWEIZ', 7 * k, 50 * k, 20 * k
    tw = sum(d.textlength(c, font=f4) for c in s) + sp * (len(s) - 1)
    x0, y0 = (w - (bs + gp + tw)) / 2, y + int(285 * k)
    ch_badge(d, x0, y0, bs); x = x0 + bs + gp
    for c in s: d.text((x, y0 + 9 * k), c, font=f4, fill=INK); x += d.textlength(c, font=f4) + sp
    return e


def info_slide(title, body, kicker=None, image=None):
    """Info-Folie: Serif-Titel in Mauve, max. ~15 Woerter Text, optional Bild-Karte."""
    s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
    y = 110
    if kicker:
        ctext(d, y, kicker.upper(), font(SANS, 30), TERRA); y += 70
    y = ctext_wrap(d, y, title, font(SER, 84), MAUVE, maxw=900, lh=1.1) + 20
    dots(d, y + 10); y += 50
    y = ctext_wrap(d, y, body, font(SANS, 40), INK, maxw=820)
    if image is not None:
        top = y + 50; bottom = H - 150
        card(s, image, (140, top, W - 140, bottom))
    paste_logo(s, 180, 45)
    return s


def save(img, name):
    img.convert('RGB').save(os.path.join(out, name), quality=93)


B = {k: Image.open(os.path.join(photo_dir, k + '.jpg')).convert('RGB') for k in ('yellow', 'pink', 'lila', 'cream')}
PK = {k: Image.open(os.path.join(pack_dir, f)).convert('RGB') for k, f in
      [('bodyset', '01.img'), ('herz', '04.img'), ('teddy', '13.img'), ('handschuhe', '163.img'),
       ('kapuze', '055.img'), ('mulltuch', 'root1.img'), ('body_weiss', 'root2.img'), ('hose', 'root3.img')]}

# ---------- DI: Karussell "Wie fällt es aus?" ----------
s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
ph = grade(fill(B['yellow'], 860, 820, 0.35)); s.paste(ph, (110, 110), rounded(ph, 34))
ctext(d, 975, 'Wie fällt es aus?', font(SER, 96), MAUVE)
dots(d, 1110)
ctext(d, 1140, 'Unser kleiner Grössen-Guide · zum Speichern', font(SANS, 36), INK)
paste_logo(s, 170, 40)
save(s, 'di_groesse_01_cover.jpg')

s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
ctext(d, 110, 'GRÖSSENTABELLE', font(SANS, 30), TERRA)
ctext(d, 165, 'Welche Grösse passt?', font(SER, 84), MAUVE)
d.rounded_rectangle([110, 310, W - 110, 1130], 34, fill=(255, 255, 255))
rows = [('Grösse', 'Körperlänge', 'Alter'), ('50', 'bis 50 cm', 'Neugeboren'), ('56', '51–56 cm', '0–2 Monate'),
        ('62', '57–62 cm', '2–4 Monate'), ('68', '63–68 cm', '4–6 Monate'), ('74', '69–74 cm', '6–9 Monate'),
        ('80', '75–80 cm', '9–12 Monate')]
xs = (180, 420, 690); y = 360
for i, r in enumerate(rows):
    f = font(SANSB if i == 0 else SANS, 42 if i else 36)
    col = TERRA if i == 0 else INK
    for x, t in zip(xs, r): d.text((x, y), t, font=f, fill=col)
    y += 108
    if i < len(rows) - 1: d.line([170, y - 30, W - 170, y - 30], fill=(236, 226, 218), width=2)
ctext(d, 1175, 'Richtwerte – jedes Baby wächst anders.', font(SANS, 34), MAUVE)
paste_logo(s, 170, 40)
save(s, 'di_groesse_02_tabelle.jpg')

pk = B['pink']; tex = grade(fill(pk.crop((int(pk.width * .08), int(pk.height * .45), int(pk.width * .62), int(pk.height * .72))), 820, 470))
s = info_slide('Ripp wächst mit', 'Der Rippstoff dehnt sich sanft. So passt das Set länger, ohne zu drücken.', 'Tipp 1', None)
s.paste(tex, (130, 640), rounded(tex, 30)); save(s, 'di_groesse_03_ripp.jpg')

s = info_slide('Im Zweifel grösser', 'Zwischen zwei Grössen? Nimm die grössere – Babys wachsen schneller, als man denkt.', 'Tipp 2', PK['bodyset'])
save(s, 'di_groesse_04_tipp.jpg')
save(endslide(), 'di_groesse_05_endfolie.jpg')

# ---------- FR: Karussell "Geschenk zur Geburt" ----------
s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
ctext(d, 95, 'GESCHENK ZUR GEBURT', font(SANS, 30), TERRA)
ctext(d, 145, 'Kleine Geschenke,', font(SER, 80), MAUVE)
ctext(d, 235, 'grosse Freude', font(SER, 80), MAUVE)
card(s, PK['herz'], (70, 380, W - 70, 860))
card(s, PK['teddy'], (70, 885, 530, 1220), pad=22)
card(s, PK['kapuze'], (550, 885, W - 70, 1220), pad=22)
paste_logo(s, 160, 38)
save(s, 'fr_geschenk_01_cover.jpg')

for n, (k, name) in enumerate([('herz', 'Herz-Bodys'), ('teddy', 'Teddy-Bodys'), ('kapuze', 'Kapuzentuch Princess'),
                                ('mulltuch', 'Mulltuch Teddy')], start=2):
    s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
    card(s, PK[k], (70, 70, W - 70, 1150))
    ctext(d, 1185, name, font(SER, 54), MAUVE)  # kleine Bildunterschrift wie bei oneve
    paste_logo(s, 140, 30)
    save(s, f'fr_geschenk_0{n}_{k}.jpg')

s = info_slide('Schön verpackt verschenken', 'Gratis Versand ab CHF 50 · 14 Tage Rückgabe · Versand aus der Schweiz', 'Gut zu wissen', PK['handschuhe'])
save(s, 'fr_geschenk_06_service.jpg')
save(endslide(), 'fr_geschenk_07_endfolie.jpg')

# ---------- SO: Mitmach-Post "Welche Farbe?" ----------
s = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(s)
ctext(d, 95, 'SONNTAGSFRAGE', font(SANS, 30), TERRA)
ctext(d, 145, 'Welche Farbe für', font(SER, 84), MAUVE)
ctext(d, 240, 'dein Baby?', font(SER, 84), MAUVE)
R = 170
for i, (k, lab, ay) in enumerate([('lila', 'Lila', .35), ('pink', 'Rosa', .5), ('yellow', 'Gelb', .35), ('cream', 'Creme', .45)]):
    cx = 300 + (i % 2) * 480; cy = 530 + (i // 2) * 420
    ph = grade(fill(B[k], 2 * R, 2 * R, ay))
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    d.ellipse([cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8], fill=(255, 255, 255))
    s.paste(ph, (cx - R, cy - R), m)
    f = font(SANSB, 38); t = f'{i + 1}  {lab}'
    d.text((cx - d.textlength(t, font=f) / 2, cy + R + 22), t, font=f, fill=INK)
ctext(d, 1215, 'Schreib deine Zahl in die Kommentare', font(SANS, 36), MAUVE)
paste_logo(s, 150, 35)
save(s, 'so_sonntagsfrage.jpg')

# ---------- Stories 9:16 ----------
SW, SH = 1080, 1920
st = Image.new('RGB', (SW, SH), CREAM); d = ImageDraw.Draw(st)
ctext(d, 170, 'NEU IM FEED', font(SANS, 36), TERRA, SW)
ctext(d, 230, 'Wie fällt es aus?', font(SER, 100), MAUVE, SW)
pv = Image.open(os.path.join(out, 'di_groesse_01_cover.jpg')); pv = pv.resize((760, 950))
st.paste(pv, ((SW - 760) // 2, 420), rounded(pv, 30))
ctext(d, 1420, 'Tippe auf den Post ↓', font(SANS, 40), INK, SW)
paste_logo(st, 230, 120)
st.save(os.path.join(out, 'story_neu_im_feed.jpg'), quality=93)

st = Image.new('RGB', (SW, SH), CREAM); d = ImageDraw.Draw(st)
ctext(d, 160, 'Lila oder Gelb?', font(SER, 110), MAUVE, SW)
for i, (k, ay) in enumerate([('lila', .35), ('yellow', .35)]):
    ph = grade(fill(B[k], 470, 900, ay)); st.paste(ph, (60 + i * 490, 360), rounded(ph, 30))
ctext(d, 1330, '(Platz für den Umfrage-Sticker)', font(SANS, 30), (170, 150, 150), SW)
paste_logo(st, 230, 120)
st.save(os.path.join(out, 'story_umfrage.jpg'), quality=93)

files = sorted(f for f in os.listdir(out) if f.endswith('.jpg'))
print(len(files), files)
