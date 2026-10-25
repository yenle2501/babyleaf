"""Instagram-Storys mit echten Kundenbewertungen (Judge.me auf sunnozy.ch, Stand 25.10.2026).

    python3 tools/make_bewertungen_storys.py

Oben das Shop-Produktbild des bewerteten Produkts (seit 25.10. statt KI-Babyfotos, Wunsch der Nutzerin), unten eine helle Karte
mit fünf Sternen, dem Bewertungstext wörtlich (auch mit kleinen Fehlern), Vorname wie bei Judge.me und Produkt.
Schrift: Fraunces für Zitat und Titel, Nunito Sans für den Rest (keine Schreibschrift).
Die Baby-Fotos sind KI-generiert: auf der Story steht klein «Produktfoto mit KI erstellt», damit niemand denkt,
das Baby gehöre zur Person, die bewertet hat.

Ausgabe: posts/instagram/bewertungen/story_<nr>_<name>_9x16.jpg + uebersicht.jpg
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = os.path.join(ROOT, 'posts', 'baby-photos')
OUT = os.path.join(ROOT, 'posts', 'instagram', 'bewertungen')
FONT = lambda n, s: ImageFont.truetype(os.path.join(ROOT, 'fonts', n), int(s))
W, H = 1080, 1920
CREME, WALD, GRAU, SALBEI, STERN = (251, 248, 244), (35, 48, 41), (112, 118, 114), (122, 140, 120), (214, 168, 92)
ANZAHL, SCHNITT = 15, '5,0'

# (Datei, Text wörtlich, Name, Produkt, KI-Foto?, Übersetzung)
STORYS = [
    ('kathrin', 'Super schnelle Abwicklung des Warenvorgangs. Sehr gute Qualität. Die Ware wurde als Geschenk weiter gereicht und ist dort sehr gut angekommen. Ich kann es nur empfehlen. Vielen Dank!',
     'Kathrin', 'Erstausstattung-Set «Teddybär»', os.path.join(OUT, 'produktbilder', 'erstausstattung_teddybaer.jpg'), False, None),
    ('anonym', "I'm simply pleasantly shocked: the quality is excellent, the delivery is fast, and the price is simply unbelievable. Thank you.",
     'Anonym', 'Erstausstattung-Set «Hello World»', os.path.join(OUT, 'produktbilder', 'erstausstattung_hello_world.jpg'), False,
     'Ich bin einfach angenehm überrascht: Die Qualität ist ausgezeichnet, die Lieferung schnell und der Preis einfach unglaublich. Danke.'),
    ('alissa', 'alles super, würde ich immer wieder kaufen',
     'Alissa', 'Erstausstattung-Set «Little and Loved»', os.path.join(OUT, 'produktbilder', 'erstausstattung_little_and_loved.jpg'), False, None),
    ('mariolyg', 'Super schneller Versand, alles lief sehr gut. Gerne wieder. Merci',
     'MariolyG', 'Erstausstattung-Set «Hello»', os.path.join(OUT, 'produktbilder', 'erstausstattung_hello_spitze.jpg'), False, None),
    ('monica', 'Super schnell Versand und sehr nette Verkäuferin mit wirklich niedlichen Produkten.',
     'Monica', 'Erstausstattung-Set «Hello Little Bear»', os.path.join(OUT, 'produktbilder', 'erstausstattung_hello_little_bear.jpg'), False, None),
    ('eff_g8mf', 'Alles tip top: schnelle Kommunikation und Versand',
     'eff_g8mf', 'Söckchen 5er-Set «Neutral Umschlag»', os.path.join(OUT, 'produktbilder', 'soeckchen_neutral_umschlag.jpg'), False, None),
    ('nalinea', 'Nur zu empfehlen. Danke',
     'Nalinea', 'Söckchen 5er-Set «Spitze & Blümchen»', os.path.join(OUT, 'produktbilder', 'soeckchen_spitze_bluemchen.jpg'), False, None),
]


def fuellen(im, w, h, fy=0.4):
    s = max(w / im.width, h / im.height)
    t = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (t.width - w) // 2; y = int((t.height - h) * fy)
    return t.crop((x, y, x + w, y + h))


def umbrechen(d, text, font, breite):
    zeilen, z = [], ''
    for wort in text.split():
        t = (z + ' ' + wort).strip()
        if d.textlength(t, font=font) <= breite:
            z = t
        else:
            zeilen.append(z); z = wort
    return zeilen + [z]


def sterne(d, cx, y, r=22, abstand=58):
    import math
    for i in range(5):
        x0 = cx + (i - 2) * abstand
        pts = [(x0 + (r if k % 2 == 0 else r * 0.45) * math.sin(k * math.pi / 5), y - (r if k % 2 == 0 else r * 0.45) * math.cos(k * math.pi / 5)) for k in range(10)]
        d.polygon(pts, fill=STERN)


def logo(width, col):
    import numpy as np
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def story(datei, text, name, produkt, bild, ki, uebers):
    c = Image.new('RGB', (W, H), CREME)
    foto_h = 1100
    im = Image.open(bild).convert('RGB')
    if ki:
        c.paste(fuellen(im, W, foto_h, 0.3), (0, 0))
    else:                                     # Produktbild freigestellt auf hellem Grund
        t = im.copy(); t.thumbnail((900, 900)); bg = Image.new('RGB', (W, foto_h), (244, 240, 235))
        bg.paste(t, ((W - t.width) // 2, (foto_h - t.height) // 2 + 30)); c.paste(bg, (0, 0))
    # Karte
    karte = Image.new('RGBA', (W - 96, 1000), (0, 0, 0, 0)); dk = ImageDraw.Draw(karte)
    dk.rounded_rectangle((0, 0, karte.width - 1, karte.height - 1), 44, fill=CREME + (255,))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((48, 1000, W - 48, 2000), 44, fill=(0, 0, 0, 60))
    c = Image.alpha_composite(c.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(18)))
    c.alpha_composite(karte, (48, 980))
    d = ImageDraw.Draw(c)
    if ki:
        d.text((W - 40, foto_h - 150), 'Produktfoto mit KI erstellt', font=FONT('nunitosans-600.ttf', 24), fill=(255, 255, 255), anchor='rs',
               stroke_width=2, stroke_fill=(80, 70, 65))
    gr = 58 if len(text) < 70 else (50 if len(text) < 130 else 44)
    f = FONT('fraunces-600.ttf', gr); fu = FONT('nunitosans-400i.ttf', 30)
    zeilen = umbrechen(d, f'«{text}»', f, W - 220)
    uz = umbrechen(d, uebers, fu, W - 240) if uebers else []
    hoehe = 70 + len(zeilen) * int(gr * 1.28) + (14 + 40 * len(uz) if uz else 0) + 30 + 50 + 40
    y = 1020 + max(0, (1560 - 1020 - hoehe) // 2)        # Block in der Karte mittig, unten frei für die Antwortleiste
    sterne(d, W / 2, y + 20); y += 70
    for z in zeilen:
        d.text((W / 2, y), z, font=f, fill=WALD, anchor='ma'); y += int(gr * 1.28)
    if uz:
        y += 14
        for z in uz:
            d.text((W / 2, y), z, font=fu, fill=GRAU, anchor='ma'); y += 40
    y += 30
    d.text((W / 2, y), name, font=FONT('nunitosans-700.ttf', 36), fill=WALD, anchor='ma'); y += 50
    d.text((W / 2, y), produkt, font=FONT('nunitosans-400.ttf', 30), fill=GRAU, anchor='ma')
    yl = max(1600, y + 70)
    L = logo(150, (122, 108, 104)); c.alpha_composite(L, ((W - L.width) // 2, yl))
    d.text((W / 2, yl + L.height + 22), 'Bewertung auf sunnozy.ch', font=FONT('nunitosans-600.ttf', 28), fill=SALBEI, anchor='ma')
    return c.convert('RGB')


def intro(fotos):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    g = 12; kw = (W - 3 * g) // 2; kh = int(kw * 1.25)
    for i, p in enumerate(fotos[:4]):
        t = Image.open(p).convert('RGB'); t.thumbnail((kw, kh)); f = Image.new('RGB', (kw, kh), (244, 240, 235))
        f.paste(t, ((kw - t.width) // 2, (kh - t.height) // 2)); c.paste(f, (g + (i % 2) * (kw + g), g + (i // 2) * (kh + g)))
    y0 = 2 * kh + 3 * g
    d.rectangle((0, y0, W, H), fill=CREME)
    sterne(d, W / 2, y0 + 110, r=30, abstand=76)
    d.text((W / 2, y0 + 190), f'{SCHNITT} von 5 Sternen', font=FONT('fraunces-600.ttf', 76), fill=WALD, anchor='ma')
    d.text((W / 2, y0 + 300), f'aus {ANZAHL} Bewertungen auf sunnozy.ch', font=FONT('nunitosans-600.ttf', 36), fill=GRAU, anchor='ma')
    d.text((W / 2, y0 + 360), 'Danke für jedes liebe Wort', font=FONT('nunitosans-400i.ttf', 34), fill=SALBEI, anchor='ma')
    L = logo(170, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, H - 120), L)
    return c


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    alle = []
    i0 = intro([s[4] for s in STORYS][:4])
    i0.save(os.path.join(OUT, 'story_00_intro_9x16.jpg'), quality=92); alle.append(i0)
    for n, s in enumerate(STORYS, 1):
        im = story(*s); im.save(os.path.join(OUT, f'story_{n:02d}_{s[0]}_9x16.jpg'), quality=92); alle.append(im)
    t = [a.resize((270, 480)) for a in alle]
    u = Image.new('RGB', (270 * 4 + 50, 480 * 2 + 30), 'white')
    for k, im in enumerate(t):
        u.paste(im, (10 + (k % 4) * 280, 10 + (k // 4) * 490))
    u.save(os.path.join(OUT, 'uebersicht.jpg'), quality=88)
    print(len(alle), 'Storys')
