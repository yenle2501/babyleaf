"""Instagram KW 45 (2.–8.11.2026): Produkt im Fokus, keine Schreibschrift, alle Reels aus vorhandenen Fotos.

    python3 tools/make_kw2.py            # alles nach posts/instagram/kw2/
    python3 tools/make_kw2.py reels      # nur Reels (auch: feed, stories)

Regeln: marke.md, Abschnitt «Instagram ab 21.10.2026». Titel Fraunces, Text Nunito Sans, Produkt füllt das Bild,
Infos nur auf der letzten Folie. Plan und Captions: posts/instagram/kw2/content-plan.md.
"""
import os, sys
from PIL import Image, ImageDraw
import make_kw1 as k

OUT = os.path.join(k.ROOT, 'posts', 'instagram', 'kw2')
P = k.POSTS
T = os.path.join(P, 'marktplatz-galaxus-amazon', 'einzelteile', 'set_teddy_creme')
TURBAN = os.path.join(P, 'coming-soon', 'turban-muetzen')
BOX_MDM = os.path.join(P, 'kampagne-weihnachtsbox', 'fotos', 'box_mum_dad_me.jpg')
BOX_MUMMY = os.path.join(P, 'kampagne-weihnachtsbox', 'fotos', 'box_i_love_my_mummy.jpg')
NAH_MDM = os.path.join(P, 'oneve-stil', 'ganz_nah_mum_dad_me.jpg')
NAH_MUMMY = os.path.join(P, 'oneve-stil', 'ganz_nah_i_love_mummy.jpg')
BAER = os.path.join(P, 'coming-soon', 'gerippt-beige-baer', 'shop', 'gerippt-beige-baer_shop_ohne_logo.jpg')
TITEL, TEXT, TEXT_B, KLEIN = 'fraunces-600.ttf', 'nunitosans-600.ttf', 'nunitosans-700.ttf', 'nunitosans-800.ttf'

# Spitaltasche, Grösse 50/56: (kurz fürs Reel, Titel, Hinweis, Bilder)
LISTE = [
    ('2–3 Bodys', '2–3 Bodys', 'Grösse 50/56, im Winter Langarm', [f'{T}/set_teddy_creme_body.jpg']),
    ('2 Strampler', '2 Strampler oder Fusshosen', 'mit Fuss bleiben die Zehen warm', [f'{T}/set_teddy_creme_strampler.jpg']),
    ('Mütze', 'Mütze und Söckchen', 'Neugeborene frieren schnell am Kopf', [f'{T}/set_teddy_creme_muetze.jpg', f'{T}/set_teddy_creme_socken.jpg']),
    ('1–2 Mulltücher', '1–2 Mulltücher', 'zum Spucken, Zudecken, Unterlegen', [os.path.join(P, 'paket-10-produkte', 'teile', 'mulltuch.png')]),
    ('Decke', 'Warme Decke', 'für die Heimfahrt im Winter', [f'{T}/set_teddy_creme_decke.jpg']),
]


def teil(p):
    if p.endswith('.png'):
        im = Image.open(p).convert('RGBA')
        return im.crop(im.getbbox())
    return k.freisteller(p)


def kopf(d, oben, titel, unter=None, W=k.FW, groesse=72):
    if oben:
        d.text((W / 2, 110), oben, font=k.f(KLEIN, 28), fill=k.SALBEI, anchor='mm')
    d.text((W / 2, 190), titel, font=k.passt(d, titel, TITEL, groesse, W - 140), fill=k.WALD, anchor='mm')
    if unter:
        d.text((W / 2, 262), unter, font=k.passt(d, unter, TEXT, 34, W - 160), fill=k.GRAU, anchor='mm')


# ---------------------------------------------------------------- Feed
def checkliste():
    """DM-Datei für alle, die «LISTE» kommentieren (bleibt eine Liste, wird nicht gepostet)."""
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    kopf(d, 'CHECKLISTE', 'Spitaltasche fürs Baby', 'Grösse 50/56  ·  zum Abhaken')
    y = 350
    zeilen = [(t, u) for _, t, u, _ in LISTE] + [('Babyschale fürs Auto', 'im Auto ab der ersten Fahrt Pflicht')]
    for titel, unter in zeilen:
        d.rounded_rectangle((90, y, 136, y + 46), radius=9, outline=k.WALD, width=4)
        d.text((170, y + 10), titel, font=k.f(TEXT_B, 42), fill=k.WALD, anchor='lm')
        d.text((170, y + 60), unter, font=k.passt(d, unter, 'nunitosans-400.ttf', 32, k.FW - 260), fill=k.GRAU, anchor='lm')
        y += 122
    tipp = 'Tipp: Viele Spitäler stellen Kleider für die ersten Tage. Frag bei Deinem nach.'
    d.rounded_rectangle((90, y + 10, k.FW - 90, y + 96), radius=20, fill=k.ROSE)
    d.text((k.FW / 2, y + 53), tipp, font=k.passt(d, tipp, TEXT, 28, k.FW - 240), fill=k.WALD, anchor='mm')
    k.fuss(c, d)
    c.save(os.path.join(OUT, 'checkliste_spitaltasche.jpg'), quality=94)


def flatlay(c, box):
    """Alle Teile der Liste als lockeres Flatlay in box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    plan = [  # Anteile der box: body, strampler, mütze, socken, mulltuch, decke
        (LISTE[4][3][0], (0.00, 0.00, 0.42, 0.46)),
        (LISTE[0][3][0], (0.44, 0.00, 1.00, 0.46)),
        (LISTE[1][3][0], (0.00, 0.48, 0.46, 1.00)),
        (LISTE[2][3][0], (0.50, 0.50, 0.76, 0.74)),
        (LISTE[2][3][1], (0.78, 0.52, 1.00, 0.72)),
        (LISTE[3][3][0], (0.52, 0.76, 1.00, 1.00)),
    ]
    for p, (a, b, cc, dd) in plan:
        k.einsetzen(c, teil(p), (int(x0 + a * w), int(y0 + b * h), int(x0 + cc * w), int(y0 + dd * h)))


def karussell():
    """Do: Spitaltasche zum Speichern. Ein Teil pro Folie, gross; Infos nur auf der letzten Folie."""
    n = len(LISTE) + 2
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    kopf(d, 'ZUM SPEICHERN', 'Spitaltasche fürs Baby', 'Grösse 50/56  ·  das muss mit')
    flatlay(c, (90, 320, k.FW - 90, 1190))
    d = ImageDraw.Draw(c); k.punkte(d, n, 0, 1235); k.fuss(c, d)
    c.save(os.path.join(OUT, 'do_karussell_01.jpg'), quality=94)
    for i, (_, titel, unter, bilder) in enumerate(LISTE, start=1):
        c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
        d.text((k.FW / 2, 120), titel, font=k.passt(d, titel, TITEL, 64, k.FW - 160), fill=k.WALD, anchor='mm')
        ts = [teil(p) for p in bilder]
        if len(ts) == 1:
            k.einsetzen(c, ts[0], (110, 210, k.FW - 110, 1130))
        else:
            k.einsetzen(c, ts[0], (90, 260, 600, 1080)); k.einsetzen(c, ts[1], (620, 470, k.FW - 90, 900))
        d = ImageDraw.Draw(c)
        d.text((k.FW / 2, 1180), unter, font=k.passt(d, unter, TEXT, 34, k.FW - 160), fill=k.GRAU, anchor='mm')
        k.punkte(d, n, i, 1235); k.fuss(c, d)
        c.save(os.path.join(OUT, f'do_karussell_{i + 1:02d}.jpg'), quality=94)
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 120), 'Alles in einem Set', font=k.f(TITEL, 64), fill=k.WALD, anchor='mm')
    k.karte(c, Image.open(BAER), (k.FW / 2, 620), 800, 800)
    d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 1080), '«Little Bear» gerippt  ·  3-teilig  ·  CHF 15.90', font=k.f(TEXT_B, 36), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, 1135), 'Grösse 50/56  ·  Link in der Bio  ·  Babyschale nicht vergessen', font=k.passt(d, 'Grösse 50/56  ·  Link in der Bio  ·  Babyschale nicht vergessen', 'nunitosans-400.ttf', 30, k.FW - 160), fill=k.GRAU, anchor='mm')
    k.punkte(d, n, n - 1, 1235); k.fuss(c, d)
    c.save(os.path.join(OUT, f'do_karussell_{n:02d}.jpg'), quality=94)


# ---------------------------------------------------------------- Reels
def leinwand(foto, breite=1080, mitte_y=1010):
    """Foto auf Creme 1080x1920, volle Breite, oben und unten Platz für Text und Instagram-Bedienung."""
    c = Image.new('RGBA', (k.SW, k.SH), k.CREME + (255,))
    im = Image.open(foto).convert('RGB'); s = breite / im.width
    im = im.resize((breite, round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((k.SW - breite) // 2, int(mitte_y - im.height / 2)))
    return c


def fuellend(foto):
    """Foto füllt 1080x1920 (Mitte zugeschnitten)."""
    im = Image.open(foto).convert('RGBA'); s = max(k.SW / im.width, k.SH / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - k.SW) // 2, (im.height - k.SH) // 2
    return im.crop((x, y, x + k.SW, y + k.SH))


def zoom(c, t, z0, z1, p0, p1):
    """Ausschnitt mit Zoom z und Mittelpunkt p (Anteile 0..1), beides von t=0 nach t=1 interpoliert."""
    e = t * t * (3 - 2 * t)
    z = z0 + (z1 - z0) * e
    px, py = p0[0] + (p1[0] - p0[0]) * e, p0[1] + (p1[1] - p0[1]) * e
    w, h = k.SW / z, k.SH / z
    cx = min(max(px * k.SW, w / 2), k.SW - w / 2); cy = min(max(py * k.SH, h / 2), k.SH - h / 2)
    return c.resize((k.SW, k.SH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def text_oben(c, zeilen, farbe=k.WALD, y=300, groesse=64):
    k.textband(c, zeilen, y, groesse, TITEL, fill=farbe)
    return c


def mo_reel(out):
    """Spitaltasche 50/56: Teil für Teil gross zeigen, dann ins Raster legen. Schluss: Set und «Kommentier LISTE»."""
    ts = [teil(b[0]) for _, _, _, b in LISTE]
    namen = [kurz for kurz, _, _, _ in LISTE]
    zellen = [(90, 620, 390, 960), (390, 620, 690, 960), (690, 620, 990, 960), (240, 1010, 540, 1350), (540, 1010, 840, 1350)]
    gross = (190, 560, 890, 1290)
    start, dauer = 0.0, 1.5

    def lerp(a, b, e):
        return tuple(int(x + (y - x) * e) for x, y in zip(a, b))

    def frame(s):
        c = Image.new('RGBA', (k.SW, k.SH), k.CREME + (255,)); d = ImageDraw.Draw(c)
        d.text((k.SW / 2, 330), 'Spitaltasche fürs Baby', font=k.f(TITEL, 76), fill=k.WALD, anchor='mm')
        d.text((k.SW / 2, 420), 'Was in Grösse 50/56 mit muss', font=k.f(TEXT, 42), fill=k.SALBEI, anchor='mm')
        for i, t in enumerate(ts):
            t0 = start + i * dauer
            if s < t0:
                break
            u = s - t0
            if u < 0.95:
                d.rectangle((0, 470, k.SW, 1420), fill=k.CREME)   # Raster kurz ausblenden, das neue Teil steht allein
                box, schrift = gross, 54
                skal = 0.9 + 0.1 * min(u / 0.25, 1)
                cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                hw, hh = (box[2] - box[0]) / 2 * skal, (box[3] - box[1]) / 2 * skal
                box = (int(cx - hw), int(cy - hh), int(cx + hw), int(cy + hh))
            elif u < 1.4:
                e = (u - 0.95) / 0.45; e = e * e * (3 - 2 * e)
                box, schrift = lerp(gross, zellen[i], e), int(54 + (30 - 54) * e)
            else:
                box, schrift = zellen[i], 30
            k.einsetzen(c, t, (box[0] + 20, box[1], box[2] - 20, box[3] - 50))
            d.text(((box[0] + box[2]) / 2, box[3] - 18), namen[i], font=k.f(TEXT_B, schrift), fill=k.WALD, anchor='mm')
        return c

    ende = start + len(ts) * dauer + 1.0
    end = k.endkarte(['Alles in einem Set', 'ab CHF 15.90'], '«Little Bear» gerippt · Grösse 50/56', Image.open(BAER),
                     fussnote='Kommentier LISTE, wir schicken Dir die Checkliste')
    return k.szenen_reel([(ende, lambda t: frame(t * ende)), (3.2, lambda t: end)], os.path.join(out, 'mo_reel_spitaltasche.mp4'))


def mi_reel(out):
    """Ganz nah: Box «I love my Mummy». Start auf der Stickerei, Zoom zurück auf die ganze Box."""
    box = leinwand(BOX_MUMMY)

    def s1(t):
        return text_oben(zoom(box, t, 2.6, 2.1, (0.24, 0.30), (0.26, 0.32)), ['Ganz nah:', '«I love my Mummy»'])

    def s2(t):
        return text_oben(zoom(box, t, 2.1, 1.0, (0.26, 0.32), (0.5, 0.5)), ['3 Bodys, 3 Halstücher,', 'fertig verpackt'], groesse=56)

    end = k.endkarte(['«I love my Mummy»', 'CHF 29.90'], 'Weihnachts-Geschenkbox · neu', Image.open(BOX_MUMMY), fussnote='Link in der Bio')
    return k.szenen_reel([(2.8, s1), (3.4, s2), (3.0, lambda t: end)], os.path.join(out, 'mi_reel_i-love-my-mummy.mp4'))


def fr_reel(out):
    """Was ist in der Box «Mum Dad Me»? Box, Stickerei ganz nah, Schleife ganz nah, Box mit Karte."""
    box, nah1, nah2 = leinwand(BOX_MDM), fuellend(NAH_MDM), fuellend(NAH_MUMMY)

    def s1(t):
        return text_oben(zoom(box, t, 1.0, 1.1, (0.5, 0.5), (0.5, 0.45)), ['Was ist in der Box', '«Mum Dad Me»?'], y=200)

    def s2(t):
        return text_oben(zoom(nah1, t, 1.0, 1.12, (0.5, 0.45), (0.5, 0.4)), ['5 Bodys, gerippt'], (255, 255, 255), y=1380)

    def s3(t):
        return text_oben(zoom(nah2, t, 1.12, 1.0, (0.5, 0.55), (0.5, 0.5)), ['5 Leggings mit Schleife'], (255, 255, 255), y=1380)

    def s4(t):
        return text_oben(zoom(box, t, 1.9, 1.5, (0.62, 0.33), (0.6, 0.36)), ['Fertig verpackt, mit Karte'], y=300, groesse=58)

    end = k.endkarte(['«Mum Dad Me»', 'CHF 42.90'], 'Weihnachts-Geschenkbox · 10 Teile', Image.open(BOX_MDM), fussnote='Link in der Bio')
    return k.szenen_reel([(2.6, s1), (2.4, s2), (2.4, s3), (2.2, s4), (3.0, lambda t: end)], os.path.join(out, 'fr_reel_mum-dad-me.mp4'))


def sa_reel(out):
    """Eine Form, drei Farben: Turban-Mütze wechselt alle 0,5 s die Farbe (harte Schnitte), dann das Set."""
    farben = [('Altrosa', 'turban_altrosa.jpg'), ('Beere', 'turban_beere.jpg'), ('Creme', 'turban_creme.jpg')]
    ts = [(n, teil(os.path.join(TURBAN, 'marktplatz', 'einzelteile', p))) for n, p in farben]

    def frame(t):
        s = t * 4.5
        name, bild = ts[int(s / 0.5) % 3]
        c = Image.new('RGBA', (k.SW, k.SH), k.CREME + (255,)); d = ImageDraw.Draw(c)
        d.text((k.SW / 2, 330), 'Eine Form, drei Farben', font=k.f(TITEL, 76), fill=k.WALD, anchor='mm')
        d.text((k.SW / 2, 420), 'Turban-Mütze mit Knotenschleife', font=k.f(TEXT, 42), fill=k.SALBEI, anchor='mm')
        k.einsetzen(c, bild, (150, 540, k.SW - 150, 1300))
        d.text((k.SW / 2, 1390), name, font=k.f(TEXT_B, 48), fill=k.WALD, anchor='mm')
        return c

    end = k.endkarte(['Alle drei im Set', 'CHF 7.90'], 'Welche Farbe nimmst Du?', Image.open(os.path.join(TURBAN, 'shop', 'turban-muetzen_shop_ohne_logo.jpg')), fussnote='Link in der Bio')
    return k.szenen_reel([(4.5, frame), (3.2, lambda t: end)], os.path.join(out, 'sa_reel_turban-farben.mp4'), blende=0.15)


# ---------------------------------------------------------------- Stories
def story(titel, unter, bilder, datei):
    """Creme, Titel oben, Produktfoto(s) gross (y 480–1240), darunter bis 1500 frei für den Sticker (content-plan.md)."""
    c = k.story_grund(titel, unter, oben=300)
    if len(bilder) == 1:
        k.karte(c, bilder[0], (k.SW / 2, 860), 900, 760)
    else:
        for j, b in enumerate(bilder):
            k.karte(c, b, (k.SW / 2 + (j - 0.5) * 490, 860), 460, 700)
    c.save(os.path.join(OUT, 'stories', datei), quality=93)


def stories():
    os.makedirs(os.path.join(OUT, 'stories'), exist_ok=True)
    q = os.path.join(k.KW, 'quellen')
    bodys = [k.ohne_shoplogo(Image.open(f'{q}/{fn}').convert('RGB')) for fn in ('sunnozy-hauptbild-dino-langarm3.jpg', 'sunnozy-hauptbild-lovely-langarm3.jpg')]
    story(['Letzter Tag'], '20 % auf alle Bodys, bis heute 23:59', bodys, 'story_mo_letzter-tag.jpg')
    story(['Eure Checkliste'], 'Kommentier LISTE unter dem Reel', [Image.open(os.path.join(OUT, 'checkliste_spitaltasche.jpg'))], 'story_di_liste.jpg')
    story(['Für Mama oder', 'fürs Baby?'], None, [Image.open(BOX_MUMMY)], 'story_mi_umfrage-mummy.jpg')
    story(['Neu im Feed'], 'Spitaltasche zum Speichern', [Image.open(os.path.join(OUT, 'do_karussell_01.jpg'))], 'story_do_karussell.jpg')
    story(['Wie viele Teile', 'sind in der Box?'], None, [Image.open(BOX_MDM)], 'story_fr_quiz-box.jpg')
    story(['Welche Farbe?'], 'Altrosa, Beere oder Creme', [Image.open(os.path.join(TURBAN, 'shop', 'turban-muetzen_shop_ohne_logo.jpg'))], 'story_sa_umfrage-turban.jpg')
    story(['Unsere Woche'], 'Was willst Du nächste Woche sehen?', [Image.open(BAER), Image.open(BOX_MDM)], 'story_so_rueckblick.jpg')


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else 'alles'
    os.makedirs(os.path.join(OUT, 'reels'), exist_ok=True)
    if was in ('alles', 'feed'):
        checkliste(); karussell()
    if was in ('alles', 'stories'):
        stories()
    if was in ('alles', 'reels'):
        for name, fn in (('mo', mo_reel), ('mi', mi_reel), ('fr', fr_reel), ('sa', sa_reel)):
            fn(os.path.join(OUT, 'reels')).save(os.path.join(OUT, 'reels', f'{name}_reel_cover.jpg'), quality=92)
    print('fertig')
