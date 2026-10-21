"""sunnozy 9er-Feed-Raster nach Pinterest-Moodboard (Baby Clothing Brand Mood Board).

Kacheln 4:5 (1080x1350). Reihenfolge = Position im Profilraster (oben links -> unten rechts).
Aufruf: python3 make_pin_grid.py <baby-fotos> <packshots(drive2)> <drive3> <ausgabeordner>
"""
import sys, os, math
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
here = os.path.dirname(os.path.abspath(__file__))
baby_dir, pack_dir, d3, out = sys.argv[1:5]
src = open(os.path.join(here, 'make_viral.py')).read().split('# 1) "Schick das an')[0]
g = {'__file__': os.path.join(here, 'make_viral.py')}
sys.argv = ['x', baby_dir, pack_dir, out]
exec(src.replace("B = {k: Image.open", "_B = None and {k: Image.open").replace("PK = lambda", "_PK = lambda"), g)
Image, ImageDraw, ImageFont, ImageFilter, ImageOps = g['Image'], g['ImageDraw'], g['ImageFont'], g['ImageFilter'], __import__('PIL.ImageOps').ImageOps
fill, grade, logo, F, SERR, SERI, HAND, paper = g['fill'], g['grade'], g['logo'], g['F'], g['SERR'], g['SERI'], g['HAND'], g['paper']
np = g['np']
os.makedirs(out, exist_ok=True)
W, H = 1080, 1350
CREAM, PINK, PINKD, INK, SOFT, KRAFT = (246, 240, 233), (236, 205, 203), (226, 186, 184), (88, 74, 70), (150, 128, 120), (205, 182, 155)
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'


def spaced(d, cx, y, text, font, fill, track):
    w = sum(d.textlength(c, font=font) for c in text) + track * (len(text) - 1)
    x = cx - w / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + track
    return w


def sprig(d, cx, cy, s, col, width=3):
    """Feiner Zweig mit Blaettern (wie im Moodboard)."""
    pts = [(cx - 60 * s + t * 120 * s, cy + 14 * s - t * 28 * s - math.sin(t * math.pi) * 8 * s) for t in np.linspace(0, 1, 30)]
    d.line(pts, fill=col, width=width)
    for t, side in ((0.18, 1), (0.36, -1), (0.54, 1), (0.72, -1), (0.92, 0)):
        x, y = pts[int(t * 29)]
        ang = math.radians(-25 + (55 * side if side else 0))
        L, Wd = 20 * s, 7 * s
        leaf = []
        for u in np.linspace(0, math.pi, 12):
            leaf.append((math.cos(u) * L, math.sin(u) * Wd))
        for u in np.linspace(math.pi, 2 * math.pi, 12):
            leaf.append((math.cos(u) * L, math.sin(u) * Wd))
        ox, oy = x + math.cos(ang) * L * (0.9 if side else 0.6), y - math.sin(ang) * L * (0.9 if side else 0.6)
        poly = [(ox + px * math.cos(ang) + py * math.sin(ang), oy - px * math.sin(ang) + py * math.cos(ang)) for px, py in leaf]
        d.line(poly + [poly[0]], fill=col, width=max(2, width - 1))


def save(img, name):
    img.convert('RGB').save(os.path.join(out, name), quality=94)


def load(path):
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except ImportError:
        pass
    return ImageOps.exif_transpose(Image.open(path)).convert('RGB')


# 1) Marken-Kachel
t = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(t)
sprig(d, W / 2, 330, 1.4, SOFT)
L = logo(560, INK); t.paste(L, ((W - L.width) // 2, 430), L)
spaced(d, W / 2, 610, 'BABY ERSTAUSSTATTUNG', F(SERR, 34), SOFT, 9)
d.line([(W / 2 - 110, 690), (W / 2 + 110, 690)], fill=SOFT, width=2)
for i, ln in enumerate(['Weiche Lieblingsstücke', 'für die allerersten Momente.']):
    w = d.textlength(ln, font=F(SERR, 52)); d.text(((W - w) / 2, 740 + i * 66), ln, font=F(SERR, 52), fill=INK)
d.rectangle([W / 2 - 200, 960, W / 2 + 200, 1050], fill=PINK)
spaced(d, W / 2, 988, 'JETZT ENTDECKEN', F(SANS, 30), INK, 5)
save(t, '01_marke.jpg')

# 2) Baby-Foto (textfrei)
save(grade(fill(load(os.path.join(baby_dir, 'cream.jpg')), W, H, 0.4)), '02_baby.jpg')

# 3) Hang-Tag auf Stoff
bg = grade(fill(load(os.path.join(baby_dir, 'pink.jpg')).crop((0, 600, 924, 1152)), W, H, 0.5)).convert('RGBA')
tag = Image.new('RGBA', (430, 640), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
td.polygon([(60, 0), (370, 0), (430, 70), (430, 640), (0, 640), (0, 70)], fill=KRAFT + (255,))
td.ellipse([195, 28, 235, 68], fill=(240, 232, 222, 255))
Lt = logo(300, INK); tag.paste(Lt, ((430 - Lt.width) // 2, 230), Lt)
spaced(td, 215, 370, 'BABY CLOTHING', F(SERR, 26), (100, 84, 76), 6)
sprig(td, 215, 500, 0.8, (110, 92, 82), 2)
tag = tag.rotate(-12, expand=True, resample=Image.BICUBIC)
sh = Image.new('RGBA', tag.size, (40, 25, 20, 0)); sh.putalpha(tag.split()[3].point(lambda v: int(v * 0.3)))
sh = sh.filter(ImageFilter.GaussianBlur(16)); bg.paste(sh, (500, 560), sh); bg.paste(tag, (470, 520), tag)
d = ImageDraw.Draw(bg); d.line([(720, 0), (705, 580)], fill=(150, 120, 95), width=4)
save(bg, '03_hangtag.jpg')

# 4) Gestapelte Mulltuecher (echtes Foto)
save(grade(fill(load(os.path.join(d3, 'h8702.img')), W, H, 0.12)), '04_stapel.jpg')

# 5) Zitat-Kachel rosa
z = Image.new('RGB', (W, H), PINK); d = ImageDraw.Draw(z)
sprig(d, W / 2, 400, 1.3, INK)
for i, ln in enumerate(['DIE KLEINEN DINGE', 'SIND OFT DIE GRÖSSTEN', 'ERINNERUNGEN.']):
    spaced(d, W / 2, 520 + i * 82, ln, F(SERR, 54), INK, 8)
d.line([(W / 2 - 70, 820), (W / 2 + 70, 820)], fill=INK, width=2)
L = logo(220, INK); z.paste(L, ((W - L.width) // 2, 870), L)
save(z, '05_zitat.jpg')

# 6) Etikett-Nahaufnahme (sunnozy-Label im Strampler)
st = load(os.path.join(pack_dir, 'y022.jpg')); st = st.crop(Image.fromarray((np.asarray(st).min(axis=2) < 240).astype('uint8') * 255).getbbox()); sw, sh_ = st.size
save(grade(fill(st.crop((int(sw * .28), 0, int(sw * .72), int(sh_ * .40))), W, H, 0.3)), '06_etikett.jpg')

# 7) Set mit Schild (Geschenk-Moment)
save(grade(fill(load(os.path.join(d3, 'p7362.img')), W, H, 0.4)), '07_set.jpg')

# 8) Kleiderstange
save(grade(fill(load(os.path.join(d3, 'p7257.img')), W, H, 0.5)), '08_kleiderstange.jpg')

# 9) Werte-Kachel mit Icons + rosa Band
v = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(v)
sprig(d, W / 2, 230, 1.1, SOFT)
spaced(d, W / 2, 320, 'WEICH. SICHER. LIEBEVOLL.', F(SERR, 44), INK, 7)
d.line([(W / 2 - 90, 400), (W / 2 + 90, 400)], fill=SOFT, width=2)
icons = [('100 %\nBAUMWOLLE', 'leaf'), ('SANFT\nZUR HAUT', 'smile'), ('MIT LIEBE\nAUSGEWÄHLT', 'heart'), ('VERSAND AUS\nDER SCHWEIZ', 'cross')]
for i, (lab, kind) in enumerate(icons):
    cx, cy, r = 165 + i * 250, 600, 72
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    if kind == 'leaf':
        sprig(d, cx, cy, 0.55, INK, 3)
    elif kind == 'smile':
        d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], outline=INK, width=3); d.arc([cx - 20, cy - 12, cx + 20, cy + 20], 20, 160, fill=INK, width=3)
        d.ellipse([cx - 16, cy - 14, cx - 8, cy - 6], fill=INK); d.ellipse([cx + 8, cy - 14, cx + 16, cy - 6], fill=INK)
    elif kind == 'heart':
        g['heart'](d, cx, cy + 2, 36, INK, 3)
    else:
        d.rectangle([cx - 10, cy - 34, cx + 10, cy + 34], outline=INK, width=3); d.rectangle([cx - 34, cy - 10, cx + 34, cy + 10], outline=INK, width=3)
        d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=CREAM)
    for j, ln in enumerate(lab.split('\n')):
        spaced(d, cx, cy + r + 30 + j * 38, ln, F(SANS, 24), SOFT, 3)
d.rectangle([0, 1080, W, H], fill=PINK)
L = logo(300, INK); v.paste(L, ((W - L.width) // 2, 1080 + (270 - L.height) // 2), L)
save(v, '09_werte.jpg')

# Rastervorschau wie im Instagram-Profil
fs = sorted(f for f in os.listdir(out) if f[:2].isdigit() and f.endswith('.jpg'))
gv = Image.new('RGB', (3 * 360 + 8, 3 * 450 + 8), 'white')
for i, f in enumerate(fs):
    gv.paste(Image.open(os.path.join(out, f)).resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
gv.save(os.path.join(out, 'raster_vorschau.png'))
print(fs)
