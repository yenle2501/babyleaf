"""Content KW 3 (Mi 2.12. – Di 8.12.2026, Advent, Samichlaus am 6.12.): nur Produkte im Shop, jedes Reel mit Endfolie.

Bilder/Videos: posts/baby-photos/referenzen_photos_neu + posts/baby-videos (ohne Plüschtier/Nuggi),
Produktbilder: coming-soon/photos/shopify-hauptbilder-klar/bilder/<handle>.jpg und shopify-hauptbilder-weiss/.
Preise aus Shopify (17.11.2026), vor dem Posten prüfen.

    python3 tools/make_content_kw3.py [reels|karussell|stories|<reel-name>]
Ausgabe: posts/content-kw3/ (Plan und Captions: README.md dort)
"""
import os, sys
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_content_viral as cv
import make_reel_viral_hlb as vh
from endfolie import anhaengen, SHOP, BOX, QUELLE, SET

W, H, FPS = m.W, m.H, 30
P = m.POSTS
OUT = os.path.join(P, 'content-kw3')
FOT = os.path.join(P, 'baby-photos', 'referenzen_photos_neu')
KLAR = os.path.join(P, 'coming-soon', 'photos', 'shopify-hauptbilder-klar', 'bilder')
WEISS = os.path.join(P, 'coming-soon', 'photos', 'shopify-hauptbilder-weiss')
MUSIK = 'alex-morgan_no-copyright-music.mp3'
LAL = ((QUELLE + '/erstausstattung-set-little-and-loved.jpg', 'ohne_logo'), 'Little and Loved', 'Erstausstattung · 8 Teile')


def klar(handle):
    return cv.bild(os.path.join(KLAR, handle + '.jpg'))


# ---------- Reels ----------
def reel_advent():
    k1.OUT = OUT
    k1.REELS = {'little_and_loved_advent': {'clips': [('set_little_and_loved_gans_rosa_baby_body_2.mp4', 0.0, 10.0)],
                                            'hook': (['POV: Ihr erster', 'Advent'], '🕯️'),
                                            'ende': (['little and loved', 'jetzt im Shop'], '🤍'), 'schleier': True, 'text_y': 1560}}
    k1.reel('little_and_loved_advent')
    anhaengen(os.path.join(OUT, 'reels', 'reel_little_and_loved_advent_9x16.mp4'), *LAL)


def reel_box_lovely():
    box = cv.bild(os.path.join(BOX, 'box_lovely_little_girl.jpg'))
    szenen = [(2.2, box, None, (1.0, 1.08), (0.5, 0.5)),
              (1.7, cv.bild(os.path.join(WEISS, 'lovely_langarm3.jpg')), '1/3  3 Bodys «Lovely Little Girl»', (1.0, 1.05), (0.5, 0.5)),
              (1.7, cv.bild(os.path.join(WEISS, 'leggings5.jpg')), '2/3  5 Leggings mit Schleife', (1.0, 1.05), (0.5, 0.5)),
              (1.7, box, '3/3  Karte, fertig verpackt', (2.6, 2.6), (0.5, 0.2)),
              (2.6, cv.bild(os.path.join(WEISS, 'kombi_lovely.jpg')), None, (1.0, 1.0), (0.5, 0.5))]
    dauer = sum(s[0] for s in szenen)

    def frames():
        t0 = 0; k = 0
        for i in range(int(round(dauer * FPS))):
            t = i / FPS
            while k < len(szenen) - 1 and t >= t0 + szenen[k][0]:
                t0 += szenen[k][0]; k += 1
            d, im, label, (z0, z1), fok = szenen[k]
            c = Image.new('RGB', (W, H), cv.CREME)
            cv.karte(c, im, 960, 900 if im is box and z0 < 1.5 else 960, z0 + (z1 - z0) * m.ease((t - t0) / d), fok)
            if k == 0:
                cv.text(c, ['Was ist in der', 'Weihnachtsbox?'], 230, 62, '🎄')
            elif label:
                cv.text(c, [label], 1600, 40)
            else:
                cv.text(c, ['3 Bodys + 5 Leggings'], 230, 50)
            yield c.convert('RGBA')
    pfad = os.path.join(OUT, 'reels', 'reel_box_lovely_was_ist_drin_9x16.mp4')
    vh.schreiben(pfad, frames(), dauer, MUSIK)
    anhaengen(pfad, BOX + '/box_lovely_little_girl.jpg', 'Geschenkbox «Lovely Little Girl»', 'Preis? Schreib PREIS in die Kommentare')


def reel_samichlaus():
    fotos = ['set_hello_world_creme_baby_body_ads.png', 'set_little_bear_baby_strampler.png',
             'set_little_and_loved_gans_rosa_baby_body.png', 'set_rosa_baby_body.png', 'set_hello_world_blatt_baby_strampler_ads.png']
    bilder = [k1.auf_4x5(cv.bild(os.path.join(FOT, f))) for f in fotos]
    PRO, dauer = 1.9, 1.9 * len(fotos)

    def frames():
        for i in range(int(round(dauer * FPS))):
            t = i / FPS; k = min(int(t // PRO), len(bilder) - 1); tl = t - k * PRO
            z = 1.0 + 0.08 * m.ease(tl / PRO)
            im = bilder[k]; w, h = im.size; cw, ch = w / z, h / z
            fr = im.resize((W, round(W * ch / cw)), Image.LANCZOS, box=((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2))
            c = Image.new('RGB', (W, H), cv.CREME); c.paste(fr, (0, (H - fr.height) // 2))
            if k > 0 and tl < 0.3:                       # weicher Übergang
                c = Image.blend(c, prev, 1 - tl / 0.3)
            if tl > PRO - 0.05:
                prev = c.copy()
            c = c.convert('RGBA')
            if t < 3.0:
                a = 1 - m.ease((t - 2.6) / 0.4)
                c.alpha_composite(k1.mit_alpha(e1, a))
            yield c
    prev = None
    e1 = k1.vc.text_ebene(['POV: Der Samichlaus bringt', 'dieses Jahr Babykleider'], '🎅', y0=1560, groesse=52)
    pfad = os.path.join(OUT, 'reels', 'reel_samichlaus_9x16.mp4')
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    vh.schreiben(pfad, frames(), dauer, MUSIK)
    anhaengen(pfad, os.path.join(P, 'content-kw2', 'karussell', '01_titel.jpg'), 'Erstausstattung', '4 Sets jetzt im Shop')


def reel_bodys():
    handles = ['body-set-i-love-my-mummy', 'baby-langarm-body-3er-set-princess-rosa-mit-herzen',
               'baby-langarm-body-3er-set-ripp-lovely-little-girl-lila-rosa', 'baby-langarm-body-3er-set-i-like-flying-vogelchen-eis-rosa',
               'baby-langarm-body-5er-set-ripp-pastell-mum-dad-me-lila-blumen', 'baby-langarm-body-3er-set-dino-daddy-mommy-love-me-blau']
    bilder = [klar(h) for h in handles]
    HOOK, SCHNITT, RASTER = 2.4, 0.9, 3.4
    dauer = HOOK + SCHNITT * (len(bilder) - 1) + RASTER
    kacheln = [b.resize((470, 470), Image.LANCZOS) for b in bilder]

    def frames():
        for i in range(int(round(dauer * FPS))):
            t = i / FPS; c = Image.new('RGB', (W, H), cv.CREME)
            if t < HOOK:
                cv.karte(c, bilder[0], 960, 1000, 1.0 + 0.05 * m.ease(t / HOOK))
                cv.text(c, ['POV: Du kannst Dich', 'nicht entscheiden'], 260, 56, '🙈')
            elif t < HOOK + SCHNITT * (len(bilder) - 1):
                k = 1 + int((t - HOOK) // SCHNITT)
                cv.karte(c, bilder[k], 960, 1000, 1.0 + 0.05 * ((t - HOOK) % SCHNITT) / SCHNITT)
            else:
                tr = t - (HOOK + SCHNITT * (len(bilder) - 1))
                for j, kach in enumerate(kacheln):
                    a = m.ease((tr - j * 0.15) / 0.3)
                    if a > 0:
                        c.paste(Image.blend(Image.new('RGB', kach.size, cv.CREME), kach, a), (60 + (j % 2) * 490, 260 + (j // 2) * 500))
                if tr > 1.3:
                    cv.text(c, ['Also nimm einfach alle'], 150, 50, '✨')
            yield c.convert('RGBA')
    pfad = os.path.join(OUT, 'reels', 'reel_bodys_entscheiden_9x16.mp4')
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    vh.schreiben(pfad, frames(), dauer, MUSIK)
    anhaengen(pfad, os.path.join(KLAR, 'baby-langarm-body-5er-set-ripp-pastell-mum-dad-me-lila-blumen.jpg'), 'Body-Sets', '3er- und 5er-Packs')


REELS = {'little_and_loved_advent': reel_advent, 'box_lovely': reel_box_lovely, 'samichlaus': reel_samichlaus, 'bodys': reel_bodys}


# ---------- Karussell: Geschenkideen nach Budget ----------
BUDGET = [('unter CHF 10', [('baby-halstuecher-3er-set-baby-flowers', 'Halstücher 3er', 'CHF 7.99'),
                            ('baby-soeckchen-5er-set-spitze-bluemchen', 'Söckchen 5er', 'CHF 4.40'),
                            ('baby-geschenkset-beige-teddy-4-teilig', 'Lätzchen + Söckchen', 'CHF 7.99')]),
          ('unter CHF 20', [('body-set-i-love-my-mummy', 'Body-Set 3er', 'CHF 14.30'),
                            ('baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen', 'Leggings 5er', 'CHF 17.40'),
                            ('mulltuecher-3er-set-rosa', 'Mulltücher 3er', 'CHF 14.40')]),
          ('unter CHF 35', [('erstausstattung-set-hello-little-bear', 'Erstausstattung', 'ab CHF 28.40'),
                            ('erstausstattung-set-hello-world', 'Hello World', 'CHF 29.40'),
                            ('weihnachts-geschenkbox-i-love-my-mummy-3-bodys-3-halstucher', 'Box «I love my Mummy»', 'CHF 34.90')]),
          ('Geschenkboxen', [('weihnachts-geschenkbox-lovely-little-girl-3-bodys-5-leggings', '«Lovely Little Girl»', 'CHF 44.90'),
                             ('weihnachts-geschenkbox-mum-dad-me-5-bodys-5-leggings', '«Mum Dad Me»', 'CHF 47.90'),
                             ('weihnachts-geschenkbox-dinosaur-5-bodys-5-jogginghosen', '«Dinosaur»', 'CHF 47.90')])]


def produktbild(handle):
    p = os.path.join(KLAR, handle + '.jpg')
    if not os.path.exists(p):
        alt = {'baby-halstuecher-3er-set-baby-flowers': os.path.join(P, 'coming-soon', 'photos', 'shopify-zusatzbilder-weiss', 'baby-halstuecher-3er-set-baby-flowers_bild00.jpg'),
               'body-set-i-love-my-mummy': os.path.join(WEISS, 'mummy_langarm3.jpg'),
               'baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen': os.path.join(WEISS, 'leggings5.jpg'),
               'erstausstattung-set-hello-little-bear': os.path.join(WEISS, 'erstausstattung_hello_little_bear_praesentation.jpg'),
               'erstausstattung-set-hello-world': os.path.join(WEISS, 'erstausstattung_hello_world_praesentation.jpg')}
        p = alt.get(handle) or os.path.join(BOX, 'box_' + handle.split('geschenkbox-')[-1].split('-3-')[0].split('-5-')[0].replace('-', '_') + '.jpg')
    return cv.bild(p)


def karussell():
    o = os.path.join(OUT, 'karussell'); os.makedirs(o, exist_ok=True)
    c = Image.new('RGB', (1080, 1350), k1.CREME); d = ImageDraw.Draw(c)
    k1.mitte(d, 'Advent bei sunnozy', 330, 40, (150, 130, 115))
    for z, t in enumerate(['Geschenkideen', 'nach Budget']):
        k1.mitte(d, t, 470 + z * 95, 76)
    for z, (stufe, _) in enumerate(BUDGET):
        k1.mitte(d, stufe, 740 + z * 70, 40, k1.DUNKEL)
    k1.mitte(d, 'Wisch durch und speicher es Dir', 1130, 32, (120, 105, 95))
    L = m.logo(220, (122, 108, 104)); c.paste(L, ((1080 - L.width) // 2, 1210), L)
    c.save(os.path.join(o, '01_titel.jpg'), quality=94)
    for s, (stufe, produkte) in enumerate(BUDGET, 2):
        c = Image.new('RGB', (1080, 1350), k1.CREME); d = ImageDraw.Draw(c)
        k1.mitte(d, stufe, 110, 66)
        for j, (handle, name, preis) in enumerate(produkte):
            y = 220 + j * 370
            im2 = produktbild(handle); im2.thumbnail((320, 320), Image.LANCZOS)
            c.paste(im2, (80 + (320 - im2.width) // 2, y + (320 - im2.height) // 2))
            d.text((450, y + 130), name, font=k1.f(40), fill=k1.DUNKEL, anchor='lm')
            d.text((450, y + 190), preis, font=k1.f(38), fill=(150, 90, 70), anchor='lm')
        c.save(os.path.join(o, f'{s:02d}_{stufe.replace(" ", "_").lower()}.jpg'), quality=94)
    c = Image.new('RGB', (1080, 1350), k1.CREME); d = ImageDraw.Draw(c)
    for z, t in enumerate(['Fertig verpackt,', 'gratis geliefert']):
        k1.mitte(d, t, 480 + z * 90, 60)
    k1.mitte(d, 'bei allen Geschenkboxen', 680, 36, (120, 105, 95))
    k1.mitte(d, 'Gratisversand ab CHF 50 · Link in der Bio', 760, 30, (120, 105, 95))
    L = m.logo(280, (122, 108, 104)); c.paste(L, ((1080 - L.width) // 2, 1000), L)
    c.save(os.path.join(o, f'{len(BUDGET) + 2:02d}_ende.jpg'), quality=94)
    print('Karussell:', sorted(os.listdir(o)))


def stories():
    o = os.path.join(OUT, 'stories'); os.makedirs(o, exist_ok=True)
    c = Image.new('RGB', (W, H), k1.CREME); d = ImageDraw.Draw(c)
    k1.mitte(d, 'Was bringt der Samichlaus?', 260, 54)
    for j, (bildp, name) in enumerate([(os.path.join(WEISS, 'mummy_langarm3.jpg'), 'Body-Set'), (os.path.join(BOX, 'box_i_love_my_mummy.jpg'), 'Geschenkbox')]):
        im = cv.bild(bildp); im = k1.auf_4x5(im).resize((440, 550), Image.LANCZOS) if im.width != im.height else im.resize((440, 440), Image.LANCZOS)
        c.paste(im, (80 + j * 480, 420)); d.text((300 + j * 480, 1020), name, font=k1.f(38), fill=k1.DUNKEL, anchor='mm')
    k1.mitte(d, '(Umfrage-Sticker hier)', 1250, 30, (190, 180, 170))
    L = m.logo(220, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1700), L)
    c.save(os.path.join(o, 'story_samichlaus_umfrage.jpg'), quality=93)
    c = Image.new('RGB', (W, H), k1.CREME); d = ImageDraw.Draw(c)
    im = k1.auf_4x5(cv.bild(os.path.join(BOX, 'box_mum_dad_me.jpg'))).resize((860, 1075), Image.LANCZOS); c.paste(im, (110, 420))
    k1.mitte(d, 'Weihnachtsgeschenk', 200, 58); k1.mitte(d, 'noch nicht bestellt?', 280, 46, (120, 105, 95))
    k1.mitte(d, 'Versand aus der Schweiz in 1–2 Werktagen', 1580, 32, k1.DUNKEL)
    k1.mitte(d, '(Link-Sticker zu den Geschenkboxen)', 1660, 28, (190, 180, 170))
    c.save(os.path.join(o, 'story_rechtzeitig.jpg'), quality=93)
    print('Stories:', sorted(os.listdir(o)))


if __name__ == '__main__':
    teil = sys.argv[1:] or ['karussell', 'stories', 'reels']
    if 'karussell' in teil:
        karussell()
    if 'stories' in teil:
        stories()
    for name, fn in REELS.items():
        if 'reels' in teil or name in teil:
            fn()
