"""sunnozy virale Formate (nach Pinterest-/Trend-Recherche): Handschrift/Serif direkt im Bild, kein Textkasten.

Aufruf: python3 make_viral.py <baby-foto-ordner> <packshot-ordner> <ausgabeordner>
Schriften und Logo liegen in sunnozy-content/fonts und sunnozy-content/logo-sunnozy.webp.
"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
import numpy as np

photo_dir, pack_dir, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, 'fonts')
HAND, SERI, SERR = (os.path.join(FD, f) for f in ('sacramento.ttf', 'cormorant.ttf', 'cormorantR.ttf'))  # Handschrift fuer Social-Posts: Sacramento (Okt. 2026)
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
F = lambda p, s: ImageFont.truetype(p, s)
W, H = 1080, 1350
PAPER, INK, BROWN, OFF = (246, 240, 230), (60, 52, 48), (120, 92, 72), (255, 251, 244)
random.seed(7)


# ---------- Helfer ----------
def load_logo():
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.fromarray(np.dstack([np.zeros_like(a[..., 0]) + 30, np.zeros_like(a[..., 0]) + 30,
                                   np.zeros_like(a[..., 0]) + 30, al * 255]).astype(np.uint8), 'RGBA')
    return L.crop(L.getbbox())


LOGO = load_logo()


def logo(width, color=(40, 40, 40)):
    L = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    c = Image.new('RGBA', L.size, color + (255,)); c.putalpha(L.split()[3]); return c


def put_logo(img, width=170, bottom=45, color=(40, 40, 40)):
    L = logo(width, color); img.paste(L, ((img.width - L.width) // 2, img.height - L.height - bottom), L)


def fill(img, w, h, ay=0.5, ax=0.5):
    s = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = int((im.width - w) * ax), int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def grade(im, warm=1.0):
    a = np.asarray(im.convert('RGB')).astype(float); g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 0.9; a[..., 0] *= 1.0 + 0.02 * warm; a[..., 2] *= 1.0 - 0.015 * warm
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def paper(w=W, h=H, base=PAPER):
    """Papier-Hintergrund mit feiner Koernung."""
    n = np.random.default_rng(3).normal(0, 4, (h, w, 1))
    a = np.clip(np.array(base, float)[None, None] + n, 0, 255).astype(np.uint8)
    return Image.fromarray(a, 'RGB').filter(ImageFilter.GaussianBlur(0.6))


def cutout(path):
    """Packshot freistellen: Hintergrund von den Raendern aus per Flood-Fill entfernen."""
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(int)
    for _ in range(2):  # 1. weisser Rand, 2. evtl. hellgraues Feld
        m = Image.new('L', im.size, 0)
        work = im.copy()
        for c in [(1, 1), (im.width - 2, 1), (1, im.height - 2), (im.width - 2, im.height - 2)]:
            ImageDraw.floodfill(work, c, (255, 0, 255), thresh=22)
        bg = np.all(np.asarray(work) == (255, 0, 255), axis=2)
        box = Image.fromarray((~bg).astype(np.uint8) * 255).getbbox()
        im = im.crop(box); a = np.asarray(im).astype(int)
        if np.asarray(im)[2, 2].min() > 235: break
    work = im.copy()
    for c in [(1, 1), (im.width - 2, 1), (1, im.height - 2), (im.width - 2, im.height - 2)]:
        ImageDraw.floodfill(work, c, (255, 0, 255), thresh=26)
    bg = np.all(np.asarray(work) == (255, 0, 255), axis=2)
    alpha = Image.fromarray((~bg).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out_ = im.convert('RGBA'); out_.putalpha(alpha)
    return out_.crop(alpha.getbbox())


def place(canvas, obj, cx, cy, width, rot=0, shadow=True):
    o = obj.resize((width, int(obj.height * width / obj.width)), Image.LANCZOS)
    if rot: o = o.rotate(rot, expand=True, resample=Image.BICUBIC)
    x, y = int(cx - o.width / 2), int(cy - o.height / 2)
    if shadow:
        sh = Image.new('RGBA', o.size, (70, 50, 40, 0)); sh.putalpha(o.split()[3].point(lambda v: int(v * 0.28)))
        sh = sh.filter(ImageFilter.GaussianBlur(14)); canvas.paste(sh, (x + 10, y + 16), sh)
    canvas.paste(o, (x, y), o)


def hand(img, xy, text, size, fill=OFF, anchor='la', rot=0, shadow=True, spacing=0):
    """Handschrift direkt ins Bild, optional leicht gedreht und mit weichem Schatten."""
    f = F(HAND, size)
    tmp = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    d.multiline_text(xy, text, font=f, fill=fill + (255,), anchor=anchor, spacing=spacing or int(size * 0.15), align='center' if anchor[0] == 'm' else 'left')
    if rot: tmp = tmp.rotate(rot, center=xy, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new('RGBA', tmp.size, (0, 0, 0, 0)); sh.putalpha(tmp.split()[3].point(lambda v: int(v * 0.45)))
        sh = sh.filter(ImageFilter.GaussianBlur(6)); img.paste((30, 20, 15), (2, 3), sh)
    img.paste(tmp, (0, 0), tmp)


def serif(img, xy, text, size, fill=INK, italic=True, anchor='ma', spacing=None):
    d = ImageDraw.Draw(img)
    d.multiline_text(xy, text, font=F(SERI if italic else SERR, size), fill=fill, anchor=anchor, align='center',
                     spacing=spacing if spacing is not None else int(size * 0.12))


def heart(d, cx, cy, s, color, width=4):
    pts = [(cx + s * 16 * math.sin(t) ** 3 / 16, cy - s * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16)
           for t in np.linspace(0, 2 * math.pi, 60)]
    d.line(pts + [pts[0]], fill=color, width=width, joint='curve')


def star(d, cx, cy, r, color, width=4):
    for a in range(0, 360, 45):
        rr = r if a % 90 == 0 else r * 0.55
        d.line([cx, cy, cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))], fill=color, width=width)


def polaroid(photo, w, h, caption=None, rot=0):
    pw, ph = w + 50, h + (140 if caption else 60)
    p = Image.new('RGBA', (pw, ph), (253, 252, 249, 255)); p.paste(photo.resize((w, h)), (25, 25))
    if caption: ImageDraw.Draw(p).text((pw // 2, h + 50), caption, font=F(HAND, 54), fill=(70, 60, 55), anchor='ma')
    return p.rotate(rot, expand=True, resample=Image.BICUBIC)


def tape(canvas, cx, cy, w, h, rot, color):
    t = Image.new('RGBA', (w, h), color + (150,))
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC); canvas.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


def save(img, name):
    img.convert('RGB').save(os.path.join(out, name), quality=94)


B = {k: Image.open(os.path.join(photo_dir, k + '.jpg')).convert('RGB') for k in ('yellow', 'pink', 'lila', 'cream')}
PK = lambda k: os.path.join(pack_dir, k + '.jpg')

# 1) "Schick das an ..." – Handschrift direkt im Foto
im = grade(fill(B['lila'], W, H, 0.35))
hand(im, (W // 2, 1000), 'Schick das der Person,\ndie bald Mama wird.', 96, anchor='ma', rot=2)
put_logo(im, 150, 40, (255, 255, 255))
save(im, '01_schick_das.jpg')

# 2) "Ihr erstes Outfit nach Hause" – Flatlay auf Papier + Serif + Handnotiz
fl = paper(base=(244, 236, 228)).convert('RGBA')
place(fl, cutout(PK('a18')), 420, 800, 560, rot=-5)
place(fl, cutout(PK('a17')), 820, 560, 380, rot=8)
place(fl, cutout(PK('x16_3')), 840, 1010, 280, rot=-12)
serif(fl, (W // 2, 70), 'Ihr erstes Outfit', 92, BROWN)
serif(fl, (W // 2, 175), 'nach Hause.', 92, BROWN)
hand(fl, (560, 1150), 'Herbstbaby-Edition', 62, fill=(150, 95, 85), rot=4, shadow=False)
put_logo(fl, 140, 35)
save(fl, '02_erstes_outfit.jpg')

# 3) Scrapbook-Karussell (Cover)
sb = paper(base=(247, 242, 233)).convert('RGBA'); d = ImageDraw.Draw(sb)
p1 = polaroid(grade(fill(B['pink'], 420, 470, 0.4)), 420, 470, 'Tag 3', rot=6)
p2 = polaroid(grade(fill(B['yellow'], 400, 450, 0.3)), 400, 450, 'erster Spaziergang', rot=-5)
p3 = polaroid(grade(fill(B['cream'], 300, 300, 0.4)), 300, 300, None, rot=4)
sb.paste(p1, (40, 290), p1); sb.paste(p2, (560, 240), p2); sb.paste(p3, (600, 860), p3)
tape(sb, 260, 310, 170, 46, -20, (232, 196, 190)); tape(sb, 770, 230, 170, 46, 15, (214, 222, 205)); tape(sb, 760, 870, 140, 42, -8, (238, 222, 180))
hand(sb, (W // 2, 70), 'Woche 1 mit dir,\nin kleinen Dingen.', 84, fill=(95, 70, 60), anchor='ma', shadow=False)
heart(d, 200, 1080, 2.4, (214, 140, 130)); star(d, 420, 1150, 34, (220, 175, 110)); heart(d, 470, 990, 1.4, (214, 140, 130))
hand(sb, (110, 1180), 'mehr davon, wisch', 54, fill=(120, 95, 85), shadow=False)
d.line([(520, 1215), (565, 1215), (548, 1200)], fill=(120, 95, 85), width=4); d.line([(565, 1215), (548, 1230)], fill=(120, 95, 85), width=4)
put_logo(sb, 130, 30)
save(sb, '03_scrapbook_cover.jpg')

# 4) "Das ist dein Zeichen" – grosse Serif kursiv + Packshot
zz = paper(base=(250, 246, 240)).convert('RGBA')
serif(zz, (W // 2, 120), 'Das ist dein Zeichen,', 84, INK)
serif(zz, (W // 2, 225), 'das Geschenk nicht erst\nnach der Geburt zu kaufen.', 60, (110, 95, 88), italic=False)
place(zz, cutout(PK('a17')), W // 2, 860, 640, rot=-3)
put_logo(zz, 140, 35)
save(zz, '04_dein_zeichen.jpg')

# 5) Tiny Details – Makro, oben weich ausgeblendet, kleine Serif
mk = Image.open(PK('x14')).convert('RGB'); mw, mh = mk.size
mac = grade(fill(mk.crop((int(mw * .40), int(mh * .02), int(mw * .99), int(mh * .80))), W, H, ay=0.6)).convert('RGBA')
fade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fa = np.zeros((H, W), np.uint8); fa[:420] = np.linspace(235, 0, 420)[:, None].astype(np.uint8)
fade = Image.new('RGBA', (W, H), (250, 246, 240, 255)); fade.putalpha(Image.fromarray(fa)); mac = Image.alpha_composite(mac, fade)
serif(mac, (W // 2, 90), 'Das Detail, das man erst\nbeim dritten Hinschauen sieht.', 62, (90, 70, 66))
put_logo(mac, 120, 35)
save(mac, '05_tiny_details.jpg')

# 6) Baby in Ich-Form – kleine Handschrift
ich = grade(fill(B['yellow'], W, H, 0.45))
hand(ich, (80, 120), 'Mit 2 Wochen weiss ich:', 70, rot=-2)
hand(ich, (80, 210), 'Gerippt ist weicher.', 96, rot=-2)
put_logo(ich, 150, 40, (255, 255, 255))
save(ich, '06_mit_2_wochen.jpg')

# 7) Story-Vorlage Geburtsanzeige "mum. dad. me."
st = grade(fill(B['lila'], 1080, 1920, 0.3))
ov = Image.new('RGBA', st.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.rectangle([0, 1300, 1080, 1920], fill=(250, 246, 240, 235)); st = Image.alpha_composite(st.convert('RGBA'), ov)
serif(st, (540, 1360), 'mum. dad. me.', 110, INK)
hand(st, (540, 1510), 'seit 04:12 Uhr', 80, fill=(150, 95, 85), anchor='ma', shadow=False)
ImageDraw.Draw(st).text((540, 1660), 'NAME  ·  DATUM  ·  3.4 KG  ·  51 CM', font=F(SANS, 36), fill=(110, 95, 88), anchor='ma')
put_logo(st, 170, 70)
save(st, '07_story_geburtsanzeige.jpg')

print(sorted(os.listdir(out)))
