import sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np

src, out = sys.argv[1], sys.argv[2]

# Knock out the white logo background (keeps black letters + red Swiss cross)
a = np.asarray(Image.open(src).convert('RGB')).astype(float)
alpha = np.clip((255 - a.min(axis=2)) / 255 * 1.15, 0, 1)
alpha[alpha < 0.06] = 0
rgb = np.where(alpha[..., None] > 0, (a - 255 * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 1e-3), 0)
L = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8), 'RGBA')
L = L.crop(L.getbbox())

W, H = 2160, 3840
BG, TERRA, PEACH, PALE, INK = (252, 249, 246), (181, 72, 63), (236, 154, 138), (247, 234, 228), (40, 44, 42)
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

cx, cy = W // 2, 1500
d.ellipse([cx - 760, cy - 760, cx + 760, cy + 760], fill=PALE)
for i in range(16):
    ang = i * math.pi / 8
    r1, r2 = 820, (900 if i % 2 == 0 else 870)
    d.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)],
           fill=PEACH if i % 2 == 0 else TERRA, width=14 if i % 2 == 0 else 10)

lw = 1260
L = L.resize((lw, int(L.height * lw / L.width)), Image.LANCZOS)
img.paste(L, (cx - lw // 2, cy - L.height // 2), L)

ser = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf', 150)
sans = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 66)
sansb = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 84)
caps = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 58)


def ctext(y, t, f, fill):
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)


ctext(2560, 'Für kleine Sonnenscheine', ser, TERRA)
for dx in (-60, 0, 60):
    d.ellipse([W / 2 + dx - 13, 2797, W / 2 + dx + 13, 2823], fill=PEACH)
ctext(2900, 'Erstausstattung aus 100 % Baumwolle', sans, INK)
ctext(3040, 'sunnozy.ch', sansb, TERRA)

t, sp, bs, gap = 'VERSAND AUS DER SCHWEIZ', 14, 100, 40
tw = sum(d.textlength(c, font=caps) for c in t) + sp * (len(t) - 1)
x0, y0 = (W - (bs + gap + tw)) / 2, 3230
d.rounded_rectangle([x0, y0, x0 + bs, y0 + bs], radius=22, fill=(205, 82, 72))
c, m = x0 + bs / 2, y0 + bs / 2
d.rectangle([c - 12, m - 34, c + 12, m + 34], fill='white')
d.rectangle([c - 34, m - 12, c + 34, m + 12], fill='white')
x = x0 + bs + gap
for ch in t:
    d.text((x, y0 + 18), ch, font=caps, fill=INK)
    x += d.textlength(ch, font=caps) + sp

img.save(out + '/endfolie-logo.png')
img.resize((1080, 1920), Image.LANCZOS).save(out + '/preview.png')
