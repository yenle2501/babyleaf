"""Zweites 9er-Raster im Pin-Stil + Einzelbilder fuer zwei Produkt-Reels.

Aufruf: python3 make_pin_grid2.py <baby-fotos> <packshots(drive2)> <drive3> <ausgabeordner>
"""
import sys, os, math
here = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:5]
src = open(os.path.join(here, 'make_pin_grid.py')).read().split('# 1) Marken-Kachel')[0]
g = {'__file__': os.path.join(here, 'make_pin_grid.py')}
sys.argv = ['x'] + args
exec(src, g)
baby_dir, pack_dir, d3, out = args
Image, ImageDraw, ImageFilter = g['Image'], g['ImageDraw'], g['ImageFilter']
fill, grade, logo, F, SERR, SERI, HAND = g['fill'], g['grade'], g['logo'], g['F'], g['SERR'], g['SERI'], g['HAND']
spaced, sprig, save, load, np = g['spaced'], g['sprig'], g['save'], g['load'], g['np']
cutout = g['g']['cutout']
W, H = 1080, 1350
CREAM, PINK, INK, SOFT = g['CREAM'], g['PINK'], g['INK'], g['SOFT']
SANS = g['SANS']
P = lambda k: os.path.join(pack_dir, k + '.jpg')
D3 = lambda k: os.path.join(d3, k + '.img')


def place(canvas, obj, cx, cy, width, rot=0):
    o = obj.resize((width, int(obj.height * width / obj.width)), Image.LANCZOS)
    if rot: o = o.rotate(rot, expand=True, resample=Image.BICUBIC)
    x, y = int(cx - o.width / 2), int(cy - o.height / 2)
    sh = Image.new('RGBA', o.size, (70, 50, 40, 0)); sh.putalpha(o.split()[3].point(lambda v: int(v * 0.22)))
    sh = sh.filter(ImageFilter.GaussianBlur(16)); canvas.paste(sh, (x + 8, y + 14), sh); canvas.paste(o, (x, y), o)


# 1) Marken-Zitat
t = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(t)
sprig(d, W / 2, 470, 1.4, SOFT)
for i, ln in enumerate(['FÜR KLEINE', 'SONNENSCHEINE.']):
    spaced(d, W / 2, 560 + i * 95, ln, F(SERR, 72), INK, 12)
d.line([(W / 2 - 90, 790), (W / 2 + 90, 790)], fill=SOFT, width=2)
L = logo(220, INK); t.paste(L, ((W - L.width) // 2, 840), L)
save(t, '01_sonnenscheine.jpg')

# 2) Mama + Baby
save(grade(fill(load(D3('p7254')), W, H, 0.3)), '02_mama_baby.jpg')

# 3) Haeubchen freigestellt auf Creme, kleine Bildunterschrift (oneve-Stil)
c = Image.new('RGBA', (W, H), CREAM + (255,)); place(c, cutout(P('x14')), W / 2, 600, 760, rot=-6)
d = ImageDraw.Draw(c); spaced(d, W / 2, 1150, 'HÄUBCHEN MIT SPITZE', F(SERR, 34), SOFT, 7)
save(c, '03_haeubchen.jpg')

# 4) Lachendes Baby
save(grade(fill(load(D3('p_life')), W, H, 0.25)), '04_baby_lacht.jpg')

# 5) Rosa Kachel: Teddy-Kollektion mit freigestelltem Body
z = Image.new('RGBA', (W, H), PINK + (255,)); d = ImageDraw.Draw(z)
spaced(d, W / 2, 150, 'NEU', F(SERR, 40), INK, 14)
spaced(d, W / 2, 215, 'TEDDY-KOLLEKTION', F(SERR, 64), INK, 10)
place(z, cutout(P('a17')), W / 2, 760, 680, rot=-4)
L = logo(170, INK); z.paste(L, ((W - L.width) // 2, H - L.height - 60), L)
save(z, '05_teddy_neu.jpg')

# 6) Laetzchen
save(grade(fill(load(D3('p7046')), W, H, 0.5)), '06_laetzchen.jpg')

# 7) Hand auf blauem Body
save(grade(fill(load(D3('p7365')), W, H, 0.4)), '07_hand_body.jpg')

# 8) Creme: Bodys-Mehrfachpack freigestellt
c = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(c)
spaced(d, W / 2, 150, 'EINE FORM.', F(SERR, 60), INK, 10)
spaced(d, W / 2, 230, 'VIELE LIEBLINGE.', F(SERR, 60), INK, 10)
place(c, cutout(P('z07')), W / 2, 760, 900)
save(c, '08_viele_lieblinge.jpg')

# 9) Service-Kachel mit Icons
v = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(v)
sprig(d, W / 2, 230, 1.1, SOFT)
spaced(d, W / 2, 320, 'SCHÖN VERPACKT. SCHNELL BEI DIR.', F(SERR, 40), INK, 5)
d.line([(W / 2 - 90, 400), (W / 2 + 90, 400)], fill=SOFT, width=2)
items = [('GESCHENK-\nVERPACKUNG', 'gift'), ('GRATIS VERSAND\nAB CHF 50', 'truck'), ('14 TAGE\nRÜCKGABE', 'back')]
for i, (lab, kind) in enumerate(items):
    cx, cy, r = 230 + i * 310, 610, 80
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    if kind == 'gift':
        d.rectangle([cx - 34, cy - 10, cx + 34, cy + 34], outline=INK, width=3); d.rectangle([cx - 40, cy - 24, cx + 40, cy - 10], outline=INK, width=3)
        d.line([(cx, cy - 24), (cx, cy + 34)], fill=INK, width=3); d.arc([cx - 26, cy - 44, cx, cy - 22], 180, 360, fill=INK, width=3); d.arc([cx, cy - 44, cx + 26, cy - 22], 180, 360, fill=INK, width=3)
    elif kind == 'truck':
        d.rectangle([cx - 46, cy - 24, cx + 10, cy + 18], outline=INK, width=3); d.polygon([(cx + 10, cy - 10), (cx + 34, cy - 10), (cx + 46, cy + 4), (cx + 46, cy + 18), (cx + 10, cy + 18)], outline=INK)
        for wx in (cx - 28, cx + 28): d.ellipse([wx - 10, cy + 12, wx + 10, cy + 32], outline=INK, width=3, fill=CREAM)
    else:
        d.arc([cx - 38, cy - 38, cx + 38, cy + 38], 40, 330, fill=INK, width=3); d.polygon([(cx + 36, cy - 30), (cx + 44, cy - 6), (cx + 20, cy - 10)], fill=INK)
    for j, ln in enumerate(lab.split('\n')):
        spaced(d, cx, cy + r + 30 + j * 38, ln, F(SANS, 24), SOFT, 3)
d.rectangle([0, 1080, W, H], fill=PINK)
L = logo(300, INK); v.paste(L, ((W - L.width) // 2, 1080 + (270 - L.height) // 2), L)
save(v, '09_service.jpg')

fs = sorted(f for f in os.listdir(out) if f[:2].isdigit() and f.endswith('.jpg'))
gv = Image.new('RGB', (3 * 360 + 8, 3 * 450 + 8), 'white')
for i, f in enumerate(fs):
    gv.paste(Image.open(os.path.join(out, f)).resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
gv.save(os.path.join(out, 'raster_vorschau.png'))

# ---------- Reel-Frames (9:16) ----------
rf = os.path.join(out, '_reel'); os.makedirs(rf, exist_ok=True)
RW, RH = 1080, 1920
# Reel A: "Was fuer die Kliniktasche" – Teile erscheinen nacheinander (Stop-Motion)
items = [('a18', 'Strampler', 300, 610, 330, -4), ('a17', 'Body', 790, 600, 340, 5), ('x14', 'Häubchen', 300, 1070, 320, -6),
         ('x16_3', 'Kratzhandschuhe', 790, 1060, 280, 4), ('y03', 'Hose', 300, 1500, 270, -4), ('root1', 'Mulltuch', 790, 1490, 360, 3)]
cuts = {}
for k, *_ in items:
    pth = P(k) if os.path.exists(P(k)) else os.path.join(pack_dir.replace('drive2', 'drive'), k + '.img')
    cuts[k] = cutout(pth)
base = Image.new('RGBA', (RW, RH), (244, 238, 230, 255)); d = ImageDraw.Draw(base)
hd = F(HAND, 92)
d.text((RW // 2, 150), 'Kliniktasche fürs Baby', font=hd, fill=(110, 82, 70), anchor='ma')
d.text((RW // 2, 260), 'das brauchst du wirklich', font=F(HAND, 66), fill=(160, 120, 105), anchor='ma')
base.convert('RGB').save(os.path.join(rf, 'a_00.jpg'), quality=92)
for i, (k, lab, cx, cy, w, rot) in enumerate(items, start=1):
    place(base, cuts[k], cx, cy, w, rot)
    d = ImageDraw.Draw(base)
    ly = cy + int(cuts[k].height * w / cuts[k].width / 2) + 6
    d.text((cx, min(ly, RH - 120)), f'{i}. {lab}', font=F(HAND, 58), fill=(120, 88, 74), anchor='ma')
    base.convert('RGB').save(os.path.join(rf, f'a_{i:02d}.jpg'), quality=92)
fin = base.copy(); d = ImageDraw.Draw(fin)
L = logo(260, INK); fin.paste(L, ((RW - L.width) // 2, RH - L.height - 40), L)
fin.convert('RGB').save(os.path.join(rf, 'a_99.jpg'), quality=92)

# Reel B: "Die kleinen Details" – Makro-Ausschnitte mit Serif-Untertitel
det = [(P('x14'), (0.42, 0.05, 0.99, 0.75), 'SPITZE AM HÄUBCHEN'), (P('y022'), (0.28, 0.0, 0.72, 0.38), 'UNSER ETIKETT'),
       (P('a17'), (0.25, 0.15, 0.80, 0.60), 'GESTICKTER TEDDY'), (P('y022'), (0.55, 0.30, 0.95, 0.60), 'EIN KLEINES HERZ'),
       (P('d13'), (0.30, 0.30, 0.75, 0.70), 'FUNNY EVERY DAY')]
for i, (pth, box, cap) in enumerate(det):
    im = load(pth); im = im.crop(Image.fromarray((np.asarray(im).min(axis=2) < 240).astype('uint8') * 255).getbbox())
    w0, h0 = im.size
    fr = grade(fill(im.crop((int(box[0] * w0), int(box[1] * h0), int(box[2] * w0), int(box[3] * h0))), RW, RH))
    ov = Image.new('RGBA', (RW, RH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rectangle([0, RH - 330, RW, RH], fill=(246, 240, 233, 235))
    fr = Image.alpha_composite(fr.convert('RGBA'), ov); d = ImageDraw.Draw(fr)
    spaced(d, RW / 2, RH - 260, cap, F(SERR, 52), INK, 9)
    L = logo(170, INK); fr.paste(L, ((RW - L.width) // 2, RH - L.height - 60), L)
    fr.convert('RGB').save(os.path.join(rf, f'b_{i:02d}.jpg'), quality=92)
t = Image.new('RGB', (RW, RH), CREAM); d = ImageDraw.Draw(t)
for i, ln in enumerate(['DIE KLEINEN', 'DETAILS.']):
    spaced(d, RW / 2, 700 + i * 100, ln, F(SERR, 80), INK, 12)
sprig(d, RW / 2, 620, 1.3, SOFT)
t.save(os.path.join(rf, 'b_hook.jpg'), quality=92)
print(fs)
