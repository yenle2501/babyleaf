"""Instagram KW 45 (2.–8.11.2026): Spitaltasche-Checkliste (DM-Datei) und Karussell vom Donnerstag.

    python3 tools/make_kw2.py

Reels werden diese Woche echt gefilmt (siehe posts/instagram/kw2/content-plan.md), hier entstehen nur die Grafiken.
"""
import os
from PIL import Image, ImageDraw
import make_kw1 as k

OUT = os.path.join(k.ROOT, 'posts', 'instagram', 'kw2')
T = k.TEDDY
LISTE = [
    ('2–3 Bodys', 'Grösse 50/56, im Winter Langarm', [f'{T}/set_teddy_creme_body.jpg']),
    ('2 Strampler oder Fusshosen', 'mit Fuss bleiben die Zehen warm', [f'{T}/set_teddy_creme_strampler.jpg']),
    ('Mütze, Söckchen, Kratzhandschuhe', 'je 1–2, Neugeborene frieren schnell am Kopf', [f'{T}/set_teddy_creme_muetze.jpg', f'{T}/set_teddy_creme_socken.jpg']),
    ('1–2 Mulltücher', 'zum Spucken, Zudecken, Unterlegen', [os.path.join(k.POSTS, 'paket-10-produkte', 'teile', 'mulltuch.png')]),
    ('Warmes Outfit und Decke', 'für die Heimfahrt im Winter', [f'{T}/set_teddy_creme_decke.jpg']),
    ('Babyschale fürs Auto', 'im Auto ab der ersten Fahrt Pflicht', []),
]


def teil(p):
    if p.endswith('.png'):
        im = Image.open(p).convert('RGBA')
        return im.crop(im.getbbox())
    return k.freisteller(p)


def checkliste():
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 110), 'CHECKLISTE', font=k.f('nunitosans-800.ttf', 30), fill=k.SALBEI, anchor='mm')
    d.text((k.FW / 2, 190), 'Spitaltasche fürs Baby', font=k.f('fraunces-600.ttf', 72), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, 255), 'Grösse 50/56  ·  zum Abhaken', font=k.f('nunitosans-400.ttf', 32), fill=k.GRAU, anchor='mm')
    y = 340
    for titel, unter, _ in LISTE:
        d.rounded_rectangle((90, y, 140, y + 50), radius=10, outline=k.WALD, width=4)
        d.text((175, y + 10), titel, font=k.f('nunitosans-700.ttf', 40), fill=k.WALD, anchor='lm')
        d.text((175, y + 56), unter, font=k.f('nunitosans-400.ttf', 30), fill=k.GRAU, anchor='lm')
        y += 128
    d.rounded_rectangle((90, y + 10, k.FW - 90, y + 120), radius=24, fill=k.ROSE)
    d.text((k.FW / 2, y + 45), 'Tipp: Viele Spitäler stellen Kleider für die ersten Tage.', font=k.passt(d, 'Tipp: Viele Spitäler stellen Kleider für die ersten Tage.', 'nunitosans-600.ttf', 30, k.FW - 240), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, y + 88), 'Frag bei Deinem nach.', font=k.f('nunitosans-600.ttf', 30), fill=k.WALD, anchor='mm')
    k.fuss(c, d, 'Neugeborenen-Sets auf sunnozy.ch')
    c.save(os.path.join(OUT, 'checkliste_spitaltasche.jpg'), quality=94)


def karussell():
    n = len(LISTE) + 2
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 260), 'ZUM SPEICHERN', font=k.f('nunitosans-800.ttf', 30), fill=k.SALBEI, anchor='mm')
    for i, z in enumerate(['Spitaltasche', 'fürs Baby:', 'die Checkliste']):
        d.text((k.FW / 2, 370 + i * 100), z, font=k.f('fraunces-600.ttf', 92), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, 700), 'Was in Grösse 50/56 wirklich mit muss', font=k.f('nunitosans-400.ttf', 36), fill=k.GRAU, anchor='mm')
    for t, box in zip([teil(LISTE[0][2][0]), teil(LISTE[2][2][0]), teil(LISTE[2][2][1])], [(130, 780, 470, 1130), (490, 820, 750, 1080), (770, 860, 970, 1080)]):
        k.einsetzen(c, t, box)
    d = ImageDraw.Draw(c); d.text((k.FW / 2, 1185), 'Wischen  »', font=k.f('nunitosans-700.ttf', 30), fill=k.WALD, anchor='mm')
    k.punkte(d, n, 0, 1245); k.fuss(c, d)
    c.save(os.path.join(OUT, 'do_karussell_01.jpg'), quality=94)
    for i, (titel, unter, bilder) in enumerate(LISTE, start=1):
        c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
        d.text((80, 130), f'{i:02d}', font=k.f('fraunces-600.ttf', 40), fill=k.SALBEI, anchor='lm')
        d.text((80, 215), titel, font=k.passt(d, titel, 'fraunces-600.ttf', 66, k.FW - 160), fill=k.WALD, anchor='lm')
        d.rounded_rectangle((100, 300, k.FW - 100, 1060), radius=36, fill=k.SAND)
        ts = [teil(p) for p in bilder]
        if len(ts) == 1:
            k.einsetzen(c, ts[0], (150, 340, k.FW - 150, 1020))
        elif len(ts) == 2:
            k.einsetzen(c, ts[0], (150, 360, 560, 1000)); k.einsetzen(c, ts[1], (590, 480, k.FW - 150, 900))
        else:
            d.text((k.FW / 2, 640), 'Die Heimfahrt', font=k.f('fraunces-600.ttf', 64), fill=k.WALD, anchor='mm')
            d.text((k.FW / 2, 730), 'nicht vergessen.', font=k.f('fraunces-600.ttf', 64), fill=k.WALD, anchor='mm')
            d.text((k.FW / 2, 830), 'Schon vor der Geburt einbauen und üben.', font=k.f('nunitosans-400.ttf', 34), fill=k.GRAU, anchor='mm')
        d = ImageDraw.Draw(c)
        d.text((k.FW / 2, 1120), unter, font=k.passt(d, unter, 'nunitosans-400.ttf', 36, k.FW - 160), fill=k.WALD, anchor='mm')
        k.punkte(d, n, i, 1245); k.fuss(c, d)
        c.save(os.path.join(OUT, f'do_karussell_{i + 1:02d}.jpg'), quality=94)
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 120), 'ALLES IN EINEM', font=k.f('nunitosans-800.ttf', 30), fill=k.SALBEI, anchor='mm')
    d.text((k.FW / 2, 200), 'Neugeborenen-Sets', font=k.f('fraunces-600.ttf', 66), fill=k.WALD, anchor='mm')
    k.karte(c, Image.open(os.path.join(k.POSTS, 'coming-soon', 'gerippt-beige-baer', 'shop', 'gerippt-beige-baer_shop.jpg')), (k.FW / 2, 650), 740)
    d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 1080), '3-teilig  ·  Grösse 50/56  ·  ab CHF 15.90', font=k.f('nunitosans-700.ttf', 36), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, 1135), 'Link in der Bio  ·  Gratisversand ab CHF 50', font=k.f('nunitosans-400.ttf', 30), fill=k.GRAU, anchor='mm')
    k.punkte(d, n, n - 1, 1245); k.fuss(c, d)
    c.save(os.path.join(OUT, f'do_karussell_{n:02d}.jpg'), quality=94)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    checkliste(); karussell()
    print('fertig')
