"""Instagram-Profil von sunnozy als Handy-Bildschirm fuers Reel «Bei 0 anfangen» aufbereiten.

Aus dem echten Profil-Screenshot (Dark Mode, eigene Ansicht) wird die Besucher-Ansicht:
- oben bleibt das echte Profil (Name, Bio, Link), Notiz-Blase und «+» am Profilbild weg, Profilbild neu (Logo)
- Zahlen Beitraege/Follower/Gefolgt werden ausgespart, damit das Reel sie hochzaehlen kann
- statt Dashboard, «Profil bearbeiten» und «Personen entdecken» (fremde Personen und Marken!) kommen
  die Knoepfe «Folgen»/«Nachricht», die Reiter und ein Raster aus sunnozy-Bildern
- die Navigationsleiste unten wird aus dem Screenshot uebernommen

Aufruf: python3 make_profil_bildschirm.py <screenshot.png> <ausgabe.png> <bild1.jpg> ... (9 Rasterbilder)
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

shot, out = sys.argv[1:3]
RASTER = sys.argv[3:]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1170, 2604                       # Seitenverhaeltnis des Handy-Bildschirms in der KI-Szene
BG = (12, 15, 20)
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'

s = Image.open(shot).convert('RGB')
c = Image.new('RGB', (W, H), BG)
c.paste(s.crop((0, 0, 1170, 1005)), (0, 0))
d = ImageDraw.Draw(c)
# Profilbild: Notiz-Blase und «+» entfernen, weisser Kreis mit Logo neu
d.rectangle([30, 300, 330, 625], fill=BG)
cx, cy, r = 177, 482, 129
m = Image.new('L', (r * 8, r * 8), 0); ImageDraw.Draw(m).ellipse([0, 0, r * 8 - 1, r * 8 - 1], fill=255)
m = m.resize((r * 2, r * 2), Image.LANCZOS)
c.paste((255, 255, 255), (cx - r, cy - r), m)
a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
lg = Image.new('RGBA', (a.shape[1], a.shape[0]), (20, 20, 22, 0)); lg.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
lg = lg.crop(lg.getbbox()); lg = lg.resize((206, round(lg.height * 206 / lg.width)), Image.LANCZOS)
c.paste(lg, (cx - lg.width // 2, cy - lg.height // 2), lg)
# Zahlen aussparen (Reel zeichnet sie)
d.rectangle([365, 445, 1100, 503], fill=BG)   # Ziffern 457-492, Beschriftung ab 513

# Knoepfe Besucher-Ansicht
y0, bh, gap, x0 = 1035, 95, 22, 49
bw = (W - 2 * x0 - gap) // 2
f = ImageFont.truetype(INTER.format('SemiBold'), 40)
d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 24, fill=(74, 93, 246))
d.rounded_rectangle([x0 + bw + gap, y0, x0 + 2 * bw + gap, y0 + bh], 24, fill=(43, 47, 53))
d.text((x0 + bw / 2, y0 + bh / 2), 'Folgen', font=f, fill='white', anchor='mm')
d.text((x0 + bw * 1.5 + gap, y0 + bh / 2), 'Nachricht', font=f, fill='white', anchor='mm')

# Reiter: Raster (aktiv), Reels, Markiert
ty = 1240
grau, weiss = (150, 154, 160), (245, 245, 245)
for i in range(3):
    for j in range(3):
        d.rounded_rectangle([195 - 33 + j * 24, ty - 33 + i * 24, 195 - 33 + j * 24 + 19, ty - 33 + i * 24 + 19], 4, fill=weiss)
d.rounded_rectangle([555, ty - 34, 623, ty + 34], 16, outline=grau, width=6)
d.polygon([(578, ty - 15), (578, ty + 15), (604, ty)], outline=grau, width=6)
d.rounded_rectangle([945, ty - 28, 1015, ty + 32], 10, outline=grau, width=6)
d.ellipse([965, ty - 12, 995, ty + 18], outline=grau, width=6)
d.line([(70, ty + 68), (320, ty + 68)], fill=weiss, width=5)

# Raster 3 Spalten, Kacheln 3:4 wie im aktuellen Instagram
gy, gw = 1320, (W - 8) // 3
gh = gw * 4 // 3
for k, p in enumerate(RASTER):
    im = Image.open(p).convert('RGB')
    sc = max(gw / im.width, gh / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - gw) // 2, (im.height - gh) // 2
    c.paste(im.crop((l, t, l + gw, t + gh)), ((k % 3) * (gw + 4), gy + (k // 3) * (gh + 4)))

# Navigationsleiste aus dem Screenshot (halbtransparente Pille), Hintergrund darunter weich wie im Original
px0, py0, px1, py1 = 64, 2283, 1106, 2465
ny = H - (s.height - py0)
region = c.crop((px0, ny, px1, ny + py1 - py0)).filter(ImageFilter.GaussianBlur(18))
region = Image.blend(region, Image.new('RGB', region.size, (58, 62, 65)), 0.82)
pill = s.crop((px0, py0, px1, py1))
# Icons aus dem Screenshot (hell) auf die neue Pille legen
pa = np.asarray(pill).astype(float)
icon = np.clip((pa.min(2) - 120) / 100, 0, 1)
reg = np.asarray(region).astype(float)
reg = reg * (1 - icon[..., None]) + pa * icon[..., None]
# aktiver Reiter (Profil) etwas heller hinterlegt wie im Original
pill2 = Image.fromarray(reg.astype(np.uint8))
pm = Image.new('L', ((px1 - px0) * 4, (py1 - py0) * 4), 0)
ImageDraw.Draw(pm).rounded_rectangle([0, 0, pm.width - 1, pm.height - 1], (py1 - py0) * 2, fill=255)
pm = pm.resize(pill.size, Image.LANCZOS)
c.paste(pill2, (px0, ny), pm)
# Profilbild-Knopf in der Pille: aus dem Screenshot (Kreis um das Logo)
pk = s.crop((862, 2300, 1090, 2450))
km = Image.new('L', (pk.width * 4, pk.height * 4), 0)
ImageDraw.Draw(km).rounded_rectangle([0, 0, km.width - 1, km.height - 1], pk.height * 2, fill=255)
c.paste(pk, (862, ny + 2300 - py0), km.resize(pk.size, Image.LANCZOS))
c.save(out)
print(out, c.size)
