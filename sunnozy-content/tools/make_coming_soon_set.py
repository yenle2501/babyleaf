"""Neue Sets (Coming soon): aus echtem Lieferantenfoto Shop-Bild, Marktplatz-Bild, Instagram-Posts und Meta-Anzeigen.

Zwei Arten Quelle:
- Flatlay mit freigestelltem PNG (Canva remove-background, 2048 px): das Set kommt auf den warmen, hellen Studio-Grund
  der Shop-Hauptbilder (238, 236, 232, links oben etwas heller) mit weichem Schatten.
- Foto an der Kleiderstange (Studio, heller Grund): das Foto selbst wird verwendet, Lieferanten-Logo und Artikelnummer
  werden mit dem Grund darueber/darunter uebermalt (Kasten-Liste pro Set, Pixel im 1920er Original).
Danach je Set:
  shop/<set>_shop.jpg            2048x2048, sunnozy-Logo oben links (wie Shop-Hauptbilder)
  shop/<set>_shop_ohne_logo.jpg  ohne Logo (fuer Marktplatz-Zusatzbilder, Ads)
  instagram/<set>_feed_4x5.jpg   1080x1350 «Coming soon», Setname, Teile, «Bald auf sunnozy.ch»
  instagram/<set>_story_9x16.jpg 1080x1920, Kopf- und Fusszeile von Instagram frei
  ads/<set>_meta_1x1.jpg         Karussell-Karte im Stil der Meta-Anzeigen Erstausstattung, Etikett «Coming soon»
  ads/<set>_meta_9x16.jpg        Story/Reels-Platzierung
Look nach dem sunnozy-Designsystem: Creme, Waldgruen, Salbei, Fraunces und Nunito Sans, keine Emojis.

Mit KI=<ordner> (Canva-Export: praes_<set>.png, baby_<set>.png, markt_<set>.png) zusaetzlich:
  praesentation/<set>_praesentation.jpg (+ _ohne_logo)  Holzbuegel-Praesentation 2048 px, Logo oben links
  marktplatz/<set>_hauptbild_weiss.jpg                   nur Stangen-Sets: KI-Flatlay auf reinweiss 2000 px
  instagram/<set>_baby_4x5.jpg                           Baby im Set, ohne Text
  instagram/<set>_baby_coming_soon_4x5.jpg               dasselbe mit Etikett «Coming soon» und Setname
  ads/<set>_meta_baby_4x5.jpg                            Meta-Feed 4:5 mit Baby-Foto und Versand-Band

Aufruf: [FREI=<ordner>] [KI=<ordner>] python3 make_coming_soon_set.py <set-schluessel> <ausgabeordner>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, 'posts', 'coming-soon', 'originalFotos')
CREME, WALD, SALBEI, ROSE, GRAU = (253, 252, 250), (35, 48, 41), (122, 139, 111), (248, 234, 228), (110, 118, 113)
BG = (238, 236, 232)
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
PANEL, INK, PGRAU = (226, 221, 214), (17, 17, 17), (110, 106, 101)
N = 2048

# frei: freigestelltes PNG (Flatlay) | foto + kaesten: Stangenfoto, Kaesten (x0, y0, x1, y1) zum Uebermalen
SETS = {
    'little-bear-rosa': dict(titel='«Little Bear»', farbe='Rosa', teile=5, frei='little_bear_rosa.png',
                             liste='Strampler, Body, Mütze, Fäustlinge, Lätzchen'),
    'eisbaer-taupe': dict(titel='«Eisbär»', farbe='Taupe', teile=5, frei='eisbaer_taupe.png',
                          liste='Strampler, Body, Knotenmütze, Fäustlinge, Lätzchen'),
    'waldbaer-creme': dict(titel='«Waldbär»', farbe='Creme', teile=5, frei='waldbaer_creme.png',
                           liste='Strampler, Body, Mütze, Fäustlinge, Lätzchen'),
    'born-in-2027-rosa': dict(titel='«Born in 2027»', farbe='Rosa', teile=6, frei='born_in_2027.png',
                              liste='Kapuzentuch, Strampler, Body, Hose, Mütze, Lätzchen'),
    'weltall-hellblau': dict(titel='«Little one» Weltall', farbe='Hellblau', teile=3,
                             foto='weltall_hellblau_little_one_buegel.jpg', kaesten=[],
                             liste='Wickelbody, Fusshose, Knotenmütze'),
    'gaensebluemchen-beautiful': dict(titel='«Beautiful» Gänseblümchen', farbe='Apricot', teile=3,
                                      foto='gaensebluemchen_apricot_beautiful_buegel.jpg', kaesten=[],
                                      liste='Wickelbody, Fusshose, Mütze'),
    'blumen-musselin': dict(titel='«Blumenwiese» Musselin', farbe='Creme mit Blumen', teile=3,
                            foto='blumen_musselin_buegel.jpg', kaesten=[(35, 35, 520, 165), (1605, 1790, 1900, 1892)],
                            liste='Wickelbody, Fusshose, Haarband'),
    # Lieferantenfotos nur 580 px: Shop-Bild aus der KI-Praesentation statt aus dem Foto
    'little-princess-wickelbody': dict(titel='«Little Princess»', farbe='Rosa und Creme', teile=3, roh_ki=True,
                                       liste='Wickelbody, Fusshose, Knotenmütze'),
    'strampler-kirschen': dict(titel='Strampler 3er-Set «Kirschen»', farbe='Weinrot, Altrosa, Weiss', teile=3, roh_ki=True,
                               liste='Strampler «Smile», Strampler «You are the best», Strampler mit Kirschen'),
    'strampler-smile-gruen': dict(titel='«Smile» Salbeigrün', farbe='Salbeigrün, gerippt', teile=3, roh_ki=True,
                                  liste='Strampler «You make me happy», Kapuzentuch «Smile», Knotenmütze'),
    'strampler-hund-creme': dict(titel='«I love Dogs»', farbe='Creme und Beige', teile=8, roh_ki=True,
                                 liste='Strampler, Body, Mütze, Kapuzentuch, Lätzchen, Schmusetuch, Fäustlinge, Söckchen'),
    'i-love-you-dad': dict(titel='«I love you Dad»', farbe='Hellblau', teile=3, roh_ki=True,
                           liste='Wickelbody, Fusshose, Knotenmütze'),
}


def f(name, size):
    return ImageFont.truetype(os.path.join(ROOT, 'fonts', name), int(size))


def logo(width, color=(122, 108, 104)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), color + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def studio_grund():
    yy, xx = np.mgrid[0:N, 0:N] / N
    licht = 1.018 - 0.03 * (0.6 * xx + 0.4 * yy)
    return Image.fromarray(np.clip(np.array(BG)[None, None, :] * licht[..., None], 0, 255).astype(np.uint8), 'RGB')


def shop_aus_freisteller(png):
    cut = Image.open(png).convert('RGBA')
    cut = cut.crop(cut.getchannel('A').getbbox())
    # Platz oben fuer das Logo: Set in den Bereich unterhalb von 13 % setzen
    oben, rand = int(N * 0.13), int(N * 0.05)
    k = min((N - 2 * rand) / cut.width, (N - oben - rand) / cut.height)
    cut = cut.resize((round(cut.width * k), round(cut.height * k)), Image.LANCZOS)
    rgb = cut.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2)); rgb.putalpha(cut.getchannel('A'))
    x, y = (N - cut.width) // 2, oben + (N - oben - rand - cut.height) // 2
    c = studio_grund().convert('RGBA')
    sh = Image.new('L', (N, N), 0); sh.paste(cut.getchannel('A'), (x + 10, y + 16))
    sh = sh.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.22))
    dunkel = Image.new('RGBA', (N, N), (150, 140, 128, 0)); dunkel.putalpha(sh)
    c = Image.alpha_composite(c, dunkel); c.alpha_composite(rgb, (x, y))
    return c.convert('RGB')


def shop_aus_foto(pfad, kaesten):
    im = Image.open(pfad).convert('RGB')
    for x0, y0, x1, y1 in kaesten:                      # Logo / Artikelnummer: mit Grund daneben uebermalen
        oben = np.asarray(im.crop((x0, max(0, y0 - 14), x1, max(1, y0 - 2)))).astype(float).mean(axis=0)
        unten = np.asarray(im.crop((x0, min(im.height - 1, y1 + 2), x1, min(im.height, y1 + 14)))).astype(float).mean(axis=0) \
            if y1 + 2 < im.height else oben
        t = np.linspace(0, 1, y1 - y0)[:, None, None]
        fuell = Image.fromarray((oben[None] * (1 - t) + unten[None] * t).astype(np.uint8))
        m = Image.new('L', (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).rectangle((6, 6, x1 - x0 - 7, y1 - y0 - 7), fill=255)
        im.paste(fuell, (x0, y0), m.filter(ImageFilter.GaussianBlur(4)))
    im = im.resize((N, N), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2))


def mit_logo(im):
    im = im.copy(); L = logo(int(N * 0.198))
    im.paste(L, (int(N * 0.035), int(N * 0.031)), L)
    return im


def gesperrt(d, xy, text, font, fill, sp):
    w = sum(d.textlength(ch, font=font) for ch in text) + sp * (len(text) - 1); x = xy[0] - w / 2
    for ch in text:
        d.text((x, xy[1]), ch, font=font, fill=fill, anchor='lm'); x += d.textlength(ch, font=font) + sp


def karte(c, im, mitte, breite):
    """Foto als Karte auf Creme, feiner Schatten."""
    t = im.resize((round(breite), round(im.height * breite / im.width)), Image.LANCZOS)
    x, y = int(mitte[0] - t.width / 2), int(mitte[1] - t.height / 2)
    sh = Image.new('L', (t.width + 80, t.height + 80), 0)
    ImageDraw.Draw(sh).rectangle((40, 40, 40 + t.width, 40 + t.height), fill=55)
    c.paste(Image.new('RGB', sh.size, (205, 198, 188)), (x - 40, y - 28), sh.filter(ImageFilter.GaussianBlur(18)))
    c.paste(t, (x, y))
    return y + t.height


def stempel(d, mitte, text='COMING SOON', groesse=30, fill=WALD, schrift=CREME):
    fs = f('nunitosans-800.ttf', groesse); sp = groesse * 0.2
    tw = sum(d.textlength(ch, font=fs) for ch in text) + sp * (len(text) - 1)
    h = groesse * 2.1
    d.rectangle([mitte[0] - tw / 2 - groesse * 1.1, mitte[1] - h / 2, mitte[0] + tw / 2 + groesse * 1.1, mitte[1] + h / 2], fill=fill)
    gesperrt(d, (mitte[0], mitte[1] + 1), text, fs, schrift, sp)


def feed(st, foto, W=1080, H=1350):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    stempel(d, (W / 2, 78), groesse=24)
    d.text((W / 2, 160), st['titel'], font=f('fraunces-600.ttf', 64), fill=WALD, anchor='mm')
    d.text((W / 2, 222), f"{st['teile']} Teile  ·  {st['farbe']}", font=f('nunitosans-400.ttf', 30), fill=GRAU, anchor='mm')
    karte(c, foto, (W / 2, 290 + 820 / 2), 820)
    d = ImageDraw.Draw(c)
    d.text((W / 2, H - 112), st['liste'], font=f('nunitosans-600.ttf', 26), fill=WALD, anchor='mm')
    d.text((W / 2, H - 66), 'Bald auf sunnozy.ch  ·  Gratisversand ab CHF 50', font=f('nunitosans-400.ttf', 24), fill=GRAU, anchor='mm')
    return c


def story(st, foto, W=1080, H=1920):
    """Oben 300 px und unten 340 px bleiben frei (Instagram-Kopfzeile, Antwortfeld)."""
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    stempel(d, (W / 2, 330), groesse=30)
    d.text((W / 2, 440), st['titel'], font=f('fraunces-600.ttf', 76), fill=WALD, anchor='mm')
    d.text((W / 2, 515), f"{st['teile']} Teile  ·  {st['farbe']}", font=f('nunitosans-400.ttf', 34), fill=GRAU, anchor='mm')
    unten = karte(c, foto, (W / 2, 590 + 900 / 2), 900)
    d = ImageDraw.Draw(c)
    d.text((W / 2, unten + 62), st['liste'], font=f('nunitosans-600.ttf', 30), fill=WALD, anchor='mm')
    d.text((W / 2, unten + 112), 'Bald auf sunnozy.ch', font=f('nunitosans-400.ttf', 30), fill=GRAU, anchor='mm')
    return c


def foto_flaeche(c, im, box, luft, oben=0):
    """Wie in make_meta_ads: ganzes Foto mit Luft, Grund = Fotorand nach aussen verlaengert und weichgezeichnet."""
    x0, y0, x1, y1 = box
    s = min((x1 - x0 - 2 * luft) / im.width, (y1 - y0 - oben - 2 * luft) / im.height)
    p = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    p = p.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=2))
    px, py = (x1 - x0 - p.width) // 2, oben + (y1 - y0 - oben - p.height) // 2
    a = np.asarray(p)
    rand = np.pad(a, ((py, y1 - y0 - py - p.height), (px, x1 - x0 - px - p.width), (0, 0)), mode='edge')
    fr = max(8, round(p.width * 0.03))
    if (np.abs(a[:, :3].astype(int) - np.median(a[:, :3], axis=(0, 1))).max(axis=2) > 40).any() or \
       (np.abs(a[:, -3:].astype(int) - np.median(a[:, -3:], axis=(0, 1))).max(axis=2) > 40).any():
        # Produkt reicht bis an den Fotorand: statt Randpixel verlaengern einheitlicher Grund (Median der Ecken)
        ecken = np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3), a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)])
        rand = np.full_like(rand, np.median(ecken, axis=0).astype(np.uint8))
        fr = 2                                   # harte Kante, sonst blendet das Produkt am Rand aus
    c.paste(Image.fromarray(rand).filter(ImageFilter.GaussianBlur(25)), (x0, y0))
    m = Image.new('L', p.size, 0); ImageDraw.Draw(m).rectangle((fr, fr, p.width - fr - 1, p.height - fr - 1), fill=255)
    c.paste(p, (x0 + px, y0 + py), m.filter(ImageFilter.GaussianBlur(fr / 2)))


def badge(c, xy, text, k=1.0):
    d = ImageDraw.Draw(c); fo = ImageFont.truetype(INTER.format('SemiBold'), int(38 * k))
    w = d.textlength(text, font=fo); x, y = xy; h = 76 * k; pw = 26 * k
    d.rounded_rectangle([x, y, x + w + 2 * pw, y + h], radius=14 * k, fill=INK)
    d.text((x + pw, y + h / 2 + 2 * k), text, font=fo, fill='white', anchor='lm')


def meta_karte(foto, W=1080, H=1080):
    c = Image.new('RGB', (W, H), 'white'); split = int(W * 0.70)
    foto_flaeche(c, foto, (0, 0, split, H), 34)
    d = ImageDraw.Draw(c); d.rectangle([split, 0, W, H], fill=PANEL); pw = W - split
    lg = logo(int(H * 0.5), INK).rotate(-90, expand=True)
    if lg.width > pw * 0.62:
        s = pw * 0.62 / lg.width; lg = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS)
    ly = int(H * 0.07); c.paste(lg, (int(split + (pw - lg.width) / 2), ly), lg)
    fb = ImageFont.truetype(INTER.format('Bold'), 33); fs = ImageFont.truetype(INTER.format('Regular'), 23)
    ty = ly + lg.height + H * 0.07
    for z in ('BALD', 'IM SHOP'):
        d.text((split + pw / 2, ty), z, font=fb, fill=INK, anchor='mt'); ty += 40
    d.text((split + pw / 2, H * 0.92), 'Gratisversand ab CHF 50', font=fs, fill=PGRAU, anchor='mm')
    badge(c, (34, 30), 'COMING SOON')
    return c


def meta_story(foto, W=1080, H=1920):
    c = Image.new('RGB', (W, H), 'white'); band = 1290
    foto_flaeche(c, foto, (0, 0, W, band), 40, oben=370)
    badge(c, (40, 285), 'COMING SOON', 1.1)
    d = ImageDraw.Draw(c); d.rectangle([0, band, W, H], fill=PANEL)
    lg = logo(380, INK); c.paste(lg, ((W - lg.width) // 2, band + 40), lg)
    fb = ImageFont.truetype(INTER.format('Bold'), 40); fs = ImageFont.truetype(INTER.format('Regular'), 27)
    ty = band + 40 + lg.height + 45
    d.text((W / 2, ty), 'BALD IM SHOP', font=fb, fill=INK, anchor='mt')
    d.text((W / 2, ty + 62), 'Gratisversand ab CHF 50  ·  sunnozy.ch', font=fs, fill=PGRAU, anchor='mt')
    return c


def weiss_hauptbild(png, S=2000, fill=0.88):
    """KI-Flatlay auf (fast) weissem Grund -> reinweiss 255, Produkt auf 88 % der laengeren Seite."""
    a = np.asarray(Image.open(png).convert('RGB')).astype(float)
    mn = a.min(axis=2)
    w = np.clip((mn - 236) / (250 - 236), 0, 1)[..., None]          # 236..250 weich nach 255 ziehen
    a = a * (1 - w) + 255 * w
    im = Image.fromarray(a.astype(np.uint8))
    ys, xs = np.where(np.asarray(im.convert('L')) < 248)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    k = S * fill / max(im.size)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (S, S), (255, 255, 255)); c.paste(im, ((S - im.width) // 2, (S - im.height) // 2))
    return c.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))


def baby_coming_soon(st, baby, W=1080, H=1350):
    c = baby.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=40, threshold=2))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bw, bh = 640, 190; x0, y0 = (W - bw) / 2, H - 60 - bh
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=CREME + (238,))
    c = Image.alpha_composite(c.convert('RGBA'), lay).convert('RGB'); d = ImageDraw.Draw(c)
    stempel(d, (W / 2, y0 + 48), groesse=20)
    d.text((W / 2, y0 + 112), st['titel'], font=f('fraunces-600.ttf', 50), fill=WALD, anchor='mm')
    d.text((W / 2, y0 + 160), 'Bald auf sunnozy.ch', font=f('nunitosans-400.ttf', 24), fill=GRAU, anchor='mm')
    return c


def meta_baby(baby, W=1080, H=1350):
    c = Image.new('RGB', (W, H), 'white'); band = 1150
    b = baby.resize((W, round(baby.height * W / baby.width)), Image.LANCZOS)
    c.paste(b.crop((0, (b.height - band) // 2, W, (b.height - band) // 2 + band)), (0, 0))
    badge(c, (34, 30), 'COMING SOON')
    d = ImageDraw.Draw(c); d.rectangle([0, band, W, H], fill=PANEL)
    lg = logo(250, INK); c.paste(lg, (50, int(band + (H - band - lg.height) / 2)), lg)
    fb = ImageFont.truetype(INTER.format('Bold'), 32); fs = ImageFont.truetype(INTER.format('Regular'), 23)
    d.text((W - 50, band + 78), 'BALD IM SHOP', font=fb, fill=INK, anchor='rm')
    d.text((W - 50, band + 128), 'Gratisversand ab CHF 50', font=fs, fill=PGRAU, anchor='rm')
    return c


if __name__ == '__main__':
    key, out = sys.argv[1:3]
    frei_dir = os.environ.get('FREI', '')
    st = SETS[key]
    for sub in ('shop', 'instagram', 'ads'):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    if st.get('roh_ki'):
        roh = Image.open(os.path.join(os.environ['KI'], f'praes_{key}.png')).convert('RGB').filter(
            ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2))
    elif 'frei' in st:
        roh = shop_aus_freisteller(os.path.join(frei_dir, st['frei']))
    else:
        roh = shop_aus_foto(os.path.join(ORIG, st['foto']), st['kaesten'])
    roh.save(os.path.join(out, 'shop', f'{key}_shop_ohne_logo.jpg'), quality=95)
    mit_logo(roh).save(os.path.join(out, 'shop', f'{key}_shop.jpg'), quality=95)
    feed(st, roh).save(os.path.join(out, 'instagram', f'{key}_feed_4x5.jpg'), quality=94)
    story(st, roh).save(os.path.join(out, 'instagram', f'{key}_story_9x16.jpg'), quality=94)
    meta_karte(roh).save(os.path.join(out, 'ads', f'{key}_meta_1x1.jpg'), quality=95, subsampling=0)
    meta_story(roh).save(os.path.join(out, 'ads', f'{key}_meta_9x16.jpg'), quality=95, subsampling=0)
    ki = os.environ.get('KI', '')
    if ki:
        os.makedirs(os.path.join(out, 'praesentation'), exist_ok=True)
        pr = Image.open(os.path.join(ki, f'praes_{key}.png')).convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2))
        pr.save(os.path.join(out, 'praesentation', f'{key}_praesentation_ohne_logo.jpg'), quality=95)
        mit_logo(pr).save(os.path.join(out, 'praesentation', f'{key}_praesentation.jpg'), quality=95)
        mk = os.path.join(ki, f'markt_{key}.png')
        if os.path.exists(mk):
            os.makedirs(os.path.join(out, 'marktplatz'), exist_ok=True)
            weiss_hauptbild(mk).save(os.path.join(out, 'marktplatz', f'{key}_hauptbild_weiss.jpg'), quality=95)
        baby = Image.open(os.path.join(ki, f'baby_{key}.png')).convert('RGB')
        baby.resize((1080, 1350), Image.LANCZOS).save(os.path.join(out, 'instagram', f'{key}_baby_4x5.jpg'), quality=94)
        baby_coming_soon(st, baby).save(os.path.join(out, 'instagram', f'{key}_baby_coming_soon_4x5.jpg'), quality=94)
        b2 = os.path.join(ki, f'baby2_{key}.png')                # optional zweites Baby-Foto
        if os.path.exists(b2):
            Image.open(b2).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(
                os.path.join(out, 'instagram', f'{key}_baby_2_4x5.jpg'), quality=94)
        meta_baby(baby).save(os.path.join(out, 'ads', f'{key}_meta_baby_4x5.jpg'), quality=95, subsampling=0)
    print(key)
