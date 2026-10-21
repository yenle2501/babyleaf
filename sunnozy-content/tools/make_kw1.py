"""Instagram-Woche 26.10.–1.11.2026 (Content-Plan @Alex): Feed-Posts, Karussells, Reels und Stories.

    python3 tools/make_kw1.py            # alles nach posts/instagram/kw1/
    python3 tools/make_kw1.py reels      # nur die drei Reels

Quellen liegen in posts/instagram/kw1/quellen/ (Shop-Bilder von sunnozy.ch, KI-Szenen aus Canva in quellen/ki/).
Formate: Feed 1080x1350, Reels und Stories 1080x1920 (oben 250 px, unten 400 px frei fuer die Instagram-Bedienung).
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: Hausschrift Sacramento fuer alle Instagram-Texte (marke.md)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW = os.path.join(ROOT, 'posts', 'instagram', 'kw1')
Q = os.path.join(KW, 'quellen')
POSTS = os.path.join(ROOT, 'posts')
CREME, WALD, SALBEI, ROSE, GRAU, SAND = (253, 252, 250), (35, 48, 41), (122, 139, 111), (248, 234, 228), (110, 118, 113), (240, 233, 222)
FW, FH, SW, SH, FPS = 1080, 1350, 1080, 1920, 30


def f(name, size):
    return ImageFont.truetype(os.path.join(ROOT, 'fonts', name), int(size))


def passt(d, text, name, size, maxw):
    while size > 16 and d.textlength(text, font=f(name, size)) > maxw:
        size -= 1
    return f(name, size)


def umbruch(d, text, font, maxw):
    zeilen, z = [], ''
    for w in text.split():
        t = (z + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw:
            z = t
        else:
            zeilen.append(z); z = w
    return zeilen + [z]


def logo(width, color=(122, 108, 104)):
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), color + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


def karte(c, im, mitte, breite, hoehe=None):
    """Foto als Karte mit feinem Schatten; passt in breite x hoehe."""
    s = breite / im.width if hoehe is None else min(breite / im.width, hoehe / im.height)
    t = im.convert('RGB').resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = int(mitte[0] - t.width / 2), int(mitte[1] - t.height / 2)
    sh = Image.new('L', (t.width + 80, t.height + 80), 0)
    ImageDraw.Draw(sh).rectangle((40, 40, 40 + t.width, 40 + t.height), fill=55)
    c.paste(Image.new('RGB', sh.size, (205, 198, 188)), (x - 40, y - 28), sh.filter(ImageFilter.GaussianBlur(18)))
    c.paste(t, (x, y))
    return (x, y, x + t.width, y + t.height)


def freisteller(pfad):
    """Weissbild -> RGBA (Weiss transparent), zugeschnitten."""
    im = Image.open(pfad).convert('RGB'); a = np.asarray(im).astype(int)
    hell = a.min(axis=2)
    al = np.clip((255 - hell) * 6, 0, 255).astype(np.uint8)
    r = Image.fromarray(np.dstack([a.astype(np.uint8), al]), 'RGBA')
    return r.crop(r.getbbox())


def einsetzen(c, teil, box):
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / teil.width, (y1 - y0) / teil.height)
    t = teil.resize((round(teil.width * s), round(teil.height * s)), Image.LANCZOS)
    c.paste(t, (x0 + (x1 - x0 - t.width) // 2, y0 + (y1 - y0 - t.height) // 2), t)


def fuss(c, d, text='sunnozy.ch', y=None, farbe=GRAU):
    """Logo klein unten Mitte (marke.md); text bleibt fuer Aufrufer kompatibel, wird nicht gezeichnet."""
    y = FH - 64 if y is None else y
    L = logo(150, (122, 108, 104))
    c.paste(L, ((c.width - L.width) // 2, y - L.height // 2), L)


def punkte(d, n, i, y, W=FW):
    for k in range(n):
        x = W / 2 + (k - (n - 1) / 2) * 22
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=WALD if k == i else (210, 206, 198))


def stern(d, mx, my, r, fill):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        w = -np.pi / 2 + k * np.pi / 5
        pts.append((mx + rr * np.cos(w), my + rr * np.sin(w)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- Di 27.10. Karussell Winterbaby
TEDDY = os.path.join(POSTS, 'marktplatz-galaxus-amazon', 'einzelteile', 'set_teddy_creme')
DI = [
    ('Langarm-Bodys', '6–8', 'Warm an den Armen, Druckknöpfe unten – der Grundstock.', [f'{TEDDY}/set_teddy_creme_body.jpg']),
    ('Strampler oder Schlafanzug mit Fuss', '4–6', 'Für Nacht und Tag. Mit Fuss bleiben die Zehen warm.', [f'{TEDDY}/set_teddy_creme_strampler.jpg']),
    ('Hosen oder Leggings', '4–5', 'Zum Body kombiniert, schnell gewechselt.', [f'{POSTS}/coming-soon/hosen-baeren/marktplatz/einzelteile/hose_gestreift.jpg']),
    ('Mütze und Kratzhandschuhe', 'je 2–3', 'Für die ersten Spaziergänge und kleine Fingernägel.', [f'{TEDDY}/set_teddy_creme_muetze.jpg', f'{TEDDY}/set_teddy_creme_faeustlinge.jpg']),
    ('Mulltücher', '4–6', 'Spucktuch, Unterlage, Sonnenschutz im Kinderwagen.', [f'{POSTS}/paket-10-produkte/teile/mulltuch.png']),
    ('Söckchen', '5 Paar', 'Lieber eins zu viel: Söckchen verschwinden gern.', [f'{TEDDY}/set_teddy_creme_socken.jpg']),
]


def di_karussell(out):
    n = 8
    # 1 Titel
    c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
    d.text((FW / 2, 250), 'ERSTAUSSTATTUNG', font=f('nunitosans-800.ttf', 30), fill=SALBEI, anchor='mm')
    for k, z in enumerate(['Fürs Winterbaby:', 'die Liste']):
        d.text((FW / 2, 360 + k * 110), z, font=f('fraunces-600.ttf', 96), fill=WALD, anchor='mm')
    d.text((FW / 2, 600), 'Was in den Schrank gehört, wenn Dein Baby', font=f('nunitosans-400.ttf', 34), fill=GRAU, anchor='mm')
    d.text((FW / 2, 648), 'zwischen November und Februar kommt.', font=f('nunitosans-400.ttf', 34), fill=GRAU, anchor='mm')
    teile = [freisteller(p) for p in (f'{TEDDY}/set_teddy_creme_body.jpg', f'{TEDDY}/set_teddy_creme_muetze.jpg', f'{TEDDY}/set_teddy_creme_socken.jpg')]
    for t, box in zip(teile, [(110, 760, 450, 1120), (470, 790, 730, 1050), (750, 830, 970, 1050)]):
        einsetzen(c, t, box)
    d = ImageDraw.Draw(c); d.text((FW / 2, 1185), 'Speichern zum Abhaken  »', font=f('nunitosans-700.ttf', 30), fill=WALD, anchor='mm')
    punkte(d, n, 0, 1245); fuss(c, d)
    c.save(os.path.join(out, 'di_karussell_01.jpg'), quality=94)
    # 2-7 Teile
    for i, (titel, menge, txt, bilder) in enumerate(DI, start=1):
        c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
        d.text((80, 130), f'{i:02d}', font=f('fraunces-600.ttf', 40), fill=SALBEI, anchor='lm')
        fo = passt(d, titel, 'fraunces-600.ttf', 66, FW - 160)
        d.text((80, 215), titel, font=fo, fill=WALD, anchor='lm')
        d.rounded_rectangle((80, 280, 80 + d.textlength(menge, font=f('nunitosans-800.ttf', 44)) + 60, 360), radius=40, fill=ROSE)
        d.text((110, 321), menge, font=f('nunitosans-800.ttf', 44), fill=WALD, anchor='lm')
        d.text((80 + d.textlength(menge, font=f('nunitosans-800.ttf', 44)) + 90, 321), '' if 'Paar' in menge else 'Stück', font=f('nunitosans-400.ttf', 34), fill=GRAU, anchor='lm')
        flaeche = (140, 420, FW - 140, 1070)
        d.rounded_rectangle((100, 400, FW - 100, 1090), radius=36, fill=SAND)
        ts = [freisteller(p) if p.endswith('.jpg') else Image.open(p).convert('RGBA').crop(Image.open(p).convert('RGBA').getbbox()) for p in bilder]
        if len(ts) == 1:
            einsetzen(c, ts[0], flaeche)
        else:
            einsetzen(c, ts[0], (140, 440, 520, 1050)); einsetzen(c, ts[1], (560, 560, FW - 140, 940))
        d = ImageDraw.Draw(c)
        for k, z in enumerate(umbruch(d, txt, f('nunitosans-400.ttf', 34), FW - 160)):
            d.text((FW / 2, 1140 + k * 46), z, font=f('nunitosans-400.ttf', 34), fill=WALD, anchor='mm')
        punkte(d, n, i, 1245); fuss(c, d)
        c.save(os.path.join(out, f'di_karussell_{i + 1:02d}.jpg'), quality=94)
    # 8 Teddybaer
    c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
    d.text((FW / 2, 120), 'ALLES IN EINEM', font=f('nunitosans-800.ttf', 30), fill=SALBEI, anchor='mm')
    d.text((FW / 2, 200), 'Erstausstattung «Teddybär»', font=f('fraunces-600.ttf', 62), fill=WALD, anchor='mm')
    karte(c, Image.open(f'{Q}/set_teddy_creme_quadratisch.jpg'), (FW / 2, 640), 760)
    d = ImageDraw.Draw(c)
    d.text((FW / 2, 1080), '8 Teile  ·  100 % Baumwolle  ·  CHF 30.40', font=f('nunitosans-700.ttf', 36), fill=WALD, anchor='mm')
    d.text((FW / 2, 1135), 'Link in der Bio  ·  Gratisversand ab CHF 50', font=f('nunitosans-400.ttf', 30), fill=GRAU, anchor='mm')
    punkte(d, n, 7, 1245); fuss(c, d)
    c.save(os.path.join(out, 'di_karussell_08.jpg'), quality=94)


# ---------------------------------------------------------------- Mi 28.10. Bewertungsbild
def mi_bewertung(out):
    c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
    d.rounded_rectangle((70, 70, FW - 70, FH - 150), radius=48, fill=ROSE)
    d.text((FW / 2, 250), 'Das sagen unsere Kundinnen', font=f('fraunces-600.ttf', 54), fill=WALD, anchor='mm')
    d.text((FW / 2, 470), '5,0', font=f('fraunces-600.ttf', 230), fill=WALD, anchor='mm')
    for k in range(5):
        stern(d, FW / 2 + (k - 2) * 92, 640, 38, (196, 160, 92))
    d.text((FW / 2, 720), 'von 5 Sternen', font=f('nunitosans-600.ttf', 34), fill=GRAU, anchor='mm')
    d.line((FW / 2 - 60, 800, FW / 2 + 60, 800), fill=SALBEI, width=3)
    for k, z in enumerate(['«Sehr gute Qualität.', 'Ich kann es nur empfehlen.»']):
        d.text((FW / 2, 890 + k * 72), z, font=f('fraunces-400.ttf', 56), fill=WALD, anchor='mm')
    d.text((FW / 2, 1080), 'Danke für eure Bewertungen', font=f('nunitosans-600.ttf', 34), fill=SALBEI, anchor='mm')
    fuss(c, d, 'sunnozy.ch', y=FH - 75)
    c.save(os.path.join(out, 'mi_bewertung_5-0.jpg'), quality=94)


# ---------------------------------------------------------------- Fr 30.10. Karussell Gotti/Goetti
BOXEN = [
    ('I love my Mummy', '3 Bodys + 3 Halstücher', '29.90', 'sunnozy-geschenkbox-i-love-my-mummy'),
    ('Dino', '3 Bodys + 3 Mulltücher', '39.90', 'sunnozy-geschenkbox-dino'),
    ('Lovely Little Girl', '3 Bodys + 5 Leggings', '39.90', 'sunnozy-geschenkbox-lovely-little-girl'),
    ('I like flying', '3 Bodys + 5 Leggings', '39.90', 'sunnozy-geschenkbox-i-like-flying'),
    ('Mum Dad Me', '5 Bodys + 5 Leggings', '42.90', 'sunnozy-geschenkbox-mum-dad-me'),
    ('Growing up strong', '5 Bodys + 5 Jogginghosen', '42.90', 'sunnozy-geschenkbox-growing-up-strong'),
    ('Dinosaur', '5 Bodys + 5 Jogginghosen', '42.90', 'sunnozy-geschenkbox-dinosaur'),
    ('Little One', '5 Bodys + 3 Mulltücher', '44.90', 'sunnozy-geschenkbox-little-one'),
]


def ohne_shoplogo(im):
    """Shop-Bilder haben oben links das sunnozy-Logo; fuer Karten den oberen Rand abschneiden."""
    w, h = im.size; r = int(h * 0.075)
    return im.crop((r, r, w - r, h - r))


def fr_karussell(out):
    n = 10
    c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
    d.text((FW / 2, 150), 'WEIHNACHTS-GESCHENKBOXEN', font=f('nunitosans-800.ttf', 28), fill=SALBEI, anchor='mm')
    for k, z in enumerate(['Gotti- und Götti-Geschenk', 'unter 45 Franken']):
        d.text((FW / 2, 245 + k * 86), z, font=f('fraunces-600.ttf', 70), fill=WALD, anchor='mm')
    for k, (_, _, _, fn) in enumerate(BOXEN[:4]):
        im = ohne_shoplogo(Image.open(f'{Q}/{fn}.jpg'))
        karte(c, im, (320 + (k % 2) * 440, 560 + (k // 2) * 390), 350)
    d = ImageDraw.Draw(c)
    d.text((FW / 2, 1190), '8 Boxen  ·  0–3, 3–6 oder 6–9 Monate  »', font=f('nunitosans-700.ttf', 32), fill=WALD, anchor='mm')
    punkte(d, n, 0, 1245); fuss(c, d)
    c.save(os.path.join(out, 'fr_karussell_01.jpg'), quality=94)
    for i, (name, inhalt, preis, fn) in enumerate(BOXEN, start=1):
        c = Image.new('RGB', (FW, FH), CREME); d = ImageDraw.Draw(c)
        d.text((FW / 2, 110), f'Box {i} von 8', font=f('nunitosans-600.ttf', 28), fill=SALBEI, anchor='mm')
        d.text((FW / 2, 185), f'«{name}»', font=passt(d, f'«{name}»', 'fraunces-600.ttf', 72, FW - 120), fill=WALD, anchor='mm')
        karte(c, ohne_shoplogo(Image.open(f'{Q}/{fn}.jpg')), (FW / 2, 650), 800, 760)
        d = ImageDraw.Draw(c)
        d.text((FW / 2, 1100), inhalt, font=f('nunitosans-600.ttf', 38), fill=WALD, anchor='mm')
        pw = d.textlength(f'CHF {preis}', font=f('nunitosans-800.ttf', 40))
        d.rounded_rectangle((FW / 2 - pw / 2 - 34, 1140, FW / 2 + pw / 2 + 34, 1210), radius=35, fill=ROSE)
        d.text((FW / 2, 1176), f'CHF {preis}', font=f('nunitosans-800.ttf', 40), fill=WALD, anchor='mm')
        punkte(d, n, i, 1250); fuss(c, d, y=FH - 50)
        c.save(os.path.join(out, f'fr_karussell_{i + 1:02d}.jpg'), quality=94)
    c = Image.new('RGB', (FW, FH), ROSE); d = ImageDraw.Draw(c)
    for k, z in enumerate(['Markier das Gotti', 'oder den Götti,', 'die das sehen müssen']):
        d.text((FW / 2, 470 + k * 100), z, font=f('fraunces-600.ttf', 78), fill=WALD, anchor='mm')
    d.text((FW / 2, 820), 'Alle 8 Boxen auf sunnozy.ch  ·  fertig verpackt mit Karte', font=passt(d, 'Alle 8 Boxen auf sunnozy.ch  ·  fertig verpackt mit Karte', 'nunitosans-600.ttf', 34, FW - 140), fill=WALD, anchor='mm')
    d.text((FW / 2, 880), 'Lieferung in 2–3 Werktagen', font=f('nunitosans-400.ttf', 32), fill=GRAU, anchor='mm')
    punkte(d, n, 9, 1245); fuss(c, d)
    c.save(os.path.join(out, 'fr_karussell_10.jpg'), quality=94)


# ---------------------------------------------------------------- Reels
def kenburns(im, t, z0=1.0, z1=1.08, dx=0.0, dy=0.0):
    """im 1080x1920, t 0..1 -> Ausschnitt mit Zoom."""
    z = z0 + (z1 - z0) * t
    w, h = SW / z, SH / z
    cx = SW / 2 + dx * t * (SW - w) / 2; cy = SH / 2 + dy * t * (SH - h) / 2
    return im.resize((SW, SH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def textband(c, zeilen, y, groesse=64, schrift='fraunces-600.ttf', fill=(255, 255, 255), grund=None):
    """Hausstil (marke.md): weisse Schreibschrift mit weichem Schatten direkt auf dem Foto, keine Textbox."""
    fo = f(schrift, groesse); lh = groesse * 1.35
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    tx = Image.new('RGBA', c.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for k, z in enumerate(zeilen):
        pos = (SW / 2, y + lh * k + lh / 2)
        if fill[:3] == (255, 255, 255):
            ds.text((pos[0] + 2, pos[1] + 3), z, font=fo, fill=(30, 22, 18, 235), anchor='mm', stroke_width=6, stroke_fill=(30, 22, 18, 235))
        dt.text(pos, z, font=fo, fill=fill + (255,) if len(fill) == 3 else fill, anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    c.alpha_composite(tx)


def endkarte(titel, unter, bild=None, fussnote='sunnozy.ch'):
    c = Image.new('RGBA', (SW, SH), CREME + (255,)); d = ImageDraw.Draw(c)
    if bild is not None:
        karte(c, bild, (SW / 2, 900), 820, 820)
    d = ImageDraw.Draw(c)
    y0 = 330 if bild is not None else 760
    for k, z in enumerate(titel):
        d.text((SW / 2, y0 + k * 96), z, font=f('fraunces-600.ttf', 80), fill=WALD, anchor='mm')
    d.text((SW / 2, 1400 if bild is not None else y0 + len(titel) * 96 + 40), unter, font=f('nunitosans-700.ttf', 40), fill=SALBEI, anchor='mm')
    L = logo(300, (122, 108, 104)); c.paste(L, ((SW - L.width) // 2, 1480), L)
    d.text((SW / 2, 1580), fussnote, font=f('nunitosans-600.ttf', 34), fill=GRAU, anchor='mm')
    return c


def schreibe(frames_fn, n, pfad):
    tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{SW}x{SH}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    cover = None
    for i in range(n):
        fr = frames_fn(i).convert('RGB')
        if i == int(n * 0.08):
            cover = fr
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                    '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    return cover


def szenen_reel(szenen, pfad, blende=0.35):
    """szenen: Liste (dauer_s, fn(t)->RGBA). Weiche Blende zwischen den Szenen."""
    starts, t = [], 0
    for dauer, _ in szenen:
        starts.append(t); t += dauer
    n = int(t * FPS)

    def frame(i):
        s = i / FPS
        k = max(j for j, st in enumerate(starts) if st <= s)
        dauer, fn = szenen[k]
        im = fn((s - starts[k]) / dauer)
        if k + 1 < len(szenen) and s > starts[k] + dauer - blende:
            a = (s - (starts[k] + dauer - blende)) / blende
            im = Image.blend(im.convert('RGBA'), szenen[k + 1][1](0).convert('RGBA'), a)
        return im
    return schreibe(frame, n, pfad)


def mo_reel(out):
    ki = os.path.join(Q, 'ki')
    b = [Image.open(os.path.join(ki, f)).convert('RGBA') for f in ('box_1_zu.jpg', 'box_2_deckel.jpg', 'box_3_body.jpg', 'box_4_ausgelegt.jpg')]
    hook = ['POV: Das Geburtsgeschenk,', 'das wirklich gebraucht wird']

    def s1(t):
        c = kenburns(b[0], t, 1.0, 1.06); textband(c, hook, 360, 58); return c

    def s2(t):
        c = kenburns(b[1], t, 1.04, 1.0, 0, -0.3); textband(c, ['Deckel auf …'], 300, 54); return c

    def s3(t):
        c = kenburns(b[2], t, 1.0, 1.07, 0, -0.4); textband(c, ['5 Bodys …'], 300, 54); return c

    def s4(t):
        c = kenburns(b[3], t, 1.08, 1.0); textband(c, ['… 5 Leggings und die Karte'], 300, 54); return c

    end = endkarte(['8 Boxen', 'ab CHF 29.90'], 'Weihnachts-Geschenkboxen · neu', ohne_shoplogo(Image.open(f'{Q}/sunnozy-geschenkbox-mum-dad-me.jpg')))
    return szenen_reel([(2.4, s1), (2.6, s2), (2.6, s3), (2.6, s4), (2.6, lambda t: end)], os.path.join(out, 'mo_reel_geschenkboxen.mp4'))


BODYS = [
    ('Dino', 'Langarm, 3er-Set', 'sunnozy-hauptbild-dino-langarm3.jpg'),
    ('Love More', 'Kurzarm, 5er-Set', 'sunnozy-hauptbild-love-more-kurzarm5.jpg'),
    ('Little Love', 'Kurzarm, 5er-Set', 'sunnozy-hauptbild-little-love-rosa5.jpg'),
    ('Princess', 'Langarm, 3er-Set', 'princess.png'),
    ('Lovely Little Girl', 'Langarm, 3er-Set', 'sunnozy-hauptbild-lovely-langarm3.jpg'),
    ('Growing up strong', 'Kurzarm, 5er-Set', 'sunnozy-hauptbild-growing-up-strong-kurzarm5.jpg'),
]


def body_bild(name, art, datei):
    c = Image.new('RGBA', (SW, SH), CREME + (255,)); d = ImageDraw.Draw(c)
    im = Image.open(f'{Q}/{datei}').convert('RGB')
    if datei.startswith('sunnozy-hauptbild'):
        im = ohne_shoplogo(im)
    karte(c, im, (SW / 2, 960), 900, 900)
    d = ImageDraw.Draw(c)
    d.text((SW / 2, 1500), f'«{name}»', font=f('fraunces-600.ttf', 66), fill=WALD, anchor='mm')
    d.text((SW / 2, 1572), art, font=f('nunitosans-600.ttf', 36), fill=GRAU, anchor='mm')
    d.ellipse((SW - 290, 1250, SW - 90, 1450), fill=ROSE)
    d.text((SW - 190, 1350), '–20 %', font=f('nunitosans-800.ttf', 48), fill=WALD, anchor='mm')
    return c


def do_reel(out):
    bilder = [body_bild(*b) for b in BODYS]

    def hook(t):
        c = bilder[0].copy(); textband(c, ['Noch 4 Tage:', '20 % auf alle Bodys'], 270, 72, fill=WALD); return c
    szenen = [(1.8, hook)] + [(1.0, (lambda im: (lambda t: im))(im)) for im in bilder[1:]] + [(1.0, lambda t: bilder[0])]
    end = endkarte(['20 % auf alle Bodys'], 'bis 2.11. auf sunnozy.ch', None, 'Rabatt im Warenkorb')
    szenen.append((2.2, lambda t: end))
    return szenen_reel(szenen, os.path.join(out, 'do_reel_body-endspurt.mp4'), blende=0.12)


def sa_reel(out):
    ki = os.path.join(Q, 'ki')
    a = Image.open(os.path.join(ki, 'halloween_1_kuerbis.jpg')).convert('RGBA')
    b = Image.open(os.path.join(ki, 'halloween_2_bodys.jpg')).convert('RGBA')

    def s1(t):
        c = kenburns(a, t, 1.0, 1.08, 0, 0.2); textband(c, ['Unser Halloween-Kostüm', 'dieses Jahr:'], 330, 62); return c

    def s2(t):
        # kleiner Ruck wie ein Sprung: kurz hoch und zurueck
        hop = np.sin(min(t / 0.35, 1) * np.pi) * 0.035 if t < 0.35 else 0
        c = kenburns(b, t, 1.03 + hop, 1.03 + hop, 0, -hop * 8)
        if t > 0.3:
            textband(c, ['kein Kostüm nötig'], 330, 70)
        return c
    end = endkarte(['Langarm-Body', '3er-Set «Dino»'], '100 % Baumwolle · CHF 14.30', ohne_shoplogo(Image.open(f'{Q}/sunnozy-hauptbild-dino-langarm3.jpg')))
    return szenen_reel([(2.6, s1), (2.4, s2), (2.0, lambda t: end)], os.path.join(out, 'sa_reel_halloween-dino.mp4'), blende=0.15)


# ---------------------------------------------------------------- Stories
def story_grund(titel, unter=None, oben=300, farbe=CREME):
    c = Image.new('RGB', (SW, SH), farbe); d = ImageDraw.Draw(c)
    for k, z in enumerate(titel):
        d.text((SW / 2, oben + k * 92), z, font=f('fraunces-600.ttf', 76), fill=WALD, anchor='mm')
    if unter:
        d.text((SW / 2, oben + len(titel) * 92 + 10), unter, font=f('nunitosans-600.ttf', 36), fill=SALBEI, anchor='mm')
    return c


def sticker_platz(c, y, text=''):
    """Freie Flaeche fuer den Instagram-Sticker (y bis y+220); Sticker und Position stehen im README."""
    return


def stories(out):
    # Mo: 2 Boxen nebeneinander + Umfrage
    c = story_grund(['Rosa oder Dino?'], 'Welche Box würdest Du verschenken?')
    karte(c, ohne_shoplogo(Image.open(f'{Q}/sunnozy-geschenkbox-mum-dad-me.jpg')), (SW / 2 - 255, 800), 470)
    karte(c, ohne_shoplogo(Image.open(f'{Q}/sunnozy-geschenkbox-dinosaur.jpg')), (SW / 2 + 255, 800), 470)
    sticker_platz(c, 1180, 'Umfrage-Sticker: «Rosa» / «Dino»')
    c.save(os.path.join(out, 'story_mo_umfrage-rosa-dino.jpg'), quality=93)
    # Di: Frage
    c = story_grund(['Was darf in keiner', 'Erstausstattung fehlen?'], 'Wir sammeln eure Tipps', oben=520)
    sticker_platz(c, 860, 'Fragen-Sticker')
    karte(c, Image.open(f'{Q}/set_teddy_creme_quadratisch.jpg'), (SW / 2, 1230), 560)
    c.save(os.path.join(out, 'story_di_frage-erstausstattung.jpg'), quality=93)
    # Mi: Emoji-Slider
    c = story_grund(['Wie süss?'], '5,0 Sterne von euch – danke!')
    karte(c, ohne_shoplogo(Image.open(f'{Q}/sunnozy-geschenkbox-i-love-my-mummy.jpg')), (SW / 2, 860), 800)
    sticker_platz(c, 1290)
    c.save(os.path.join(out, 'story_mi_emoji-slider.jpg'), quality=93)
    # Do: Countdown
    c = story_grund(['20 % auf alle Bodys'], 'nur noch bis 2.11.', oben=300)
    for k, (_, _, fn) in enumerate([BODYS[0], BODYS[1], BODYS[5]]):
        im = Image.open(f'{Q}/{fn}').convert('RGB'); im = ohne_shoplogo(im)
        karte(c, im, (SW / 2 + (k - 1) * 345, 720), 320)
    sticker_platz(c, 1000, 'Countdown-Sticker «20 % endet» (2.11., 23:59)')
    sticker_platz(c, 1270, 'Link-Sticker sunnozy.ch')
    c.save(os.path.join(out, 'story_do_countdown.jpg'), quality=93)
    # Fr: Quiz
    c = story_grund(['Quiz:', 'Wie viele Bodys braucht', 'ein Neugeborenes?'], None, oben=380)
    sticker_platz(c, 760, 'Quiz-Sticker: 3–4 / 6–8 (richtig) / 12+')
    karte(c, ohne_shoplogo(Image.open(f'{Q}/sunnozy-hauptbild-growing-up-strong-kurzarm5.jpg')), (SW / 2, 1240), 580)
    c.save(os.path.join(out, 'story_fr_quiz-bodys.jpg'), quality=93)
    # Sa: Kuerbis + Dino
    c = Image.open(os.path.join(Q, 'ki', 'halloween_1_kuerbis.jpg')).convert('RGBA')
    textband(c, ['Verkleidet ihr', 'euer Baby?'], 300, 66)
    c = c.convert('RGB'); sticker_platz(c, 1380, 'Umfrage-Sticker: «Ja!» / «Body reicht»')
    c.save(os.path.join(out, 'story_sa_umfrage-halloween.jpg'), quality=93)
    # So: Morgen letzter Tag
    c = story_grund(['Morgen letzter Tag'], '20 % auf alle Bodys – bis 2.11., 23:59', oben=300, farbe=ROSE)
    for k, (_, _, fn) in enumerate([BODYS[4], BODYS[3], BODYS[2]]):
        im = Image.open(f'{Q}/{fn}').convert('RGB')
        if fn.startswith('sunnozy-hauptbild'):
            im = ohne_shoplogo(im)
        karte(c, im, (SW / 2 + (k - 1) * 345, 720), 320)
    sticker_platz(c, 1060, 'Link-Sticker sunnozy.ch')
    c.save(os.path.join(out, 'story_so_letzter-tag.jpg'), quality=93)


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else 'alles'
    dirs = {k: os.path.join(KW, k) for k in ('feed', 'reels', 'stories')}
    for p in dirs.values():
        os.makedirs(p, exist_ok=True)
    if was in ('alles', 'feed'):
        di_karussell(dirs['feed']); mi_bewertung(dirs['feed']); fr_karussell(dirs['feed'])
    if was in ('alles', 'stories'):
        stories(dirs['stories'])
    if was in ('alles', 'reels'):
        for name, fn in (('mo', mo_reel), ('do', do_reel), ('sa', sa_reel)):
            cover = fn(dirs['reels'])
            cover.save(os.path.join(dirs['reels'], f'{name}_reel_cover.jpg'), quality=92)
    print('fertig')
