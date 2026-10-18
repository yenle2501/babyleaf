"""Instagram-Storys für die 8 Highlights (1080x1920), passend zu den Highlight-Covern.

Inhalte nur aus echten Quellen: Shop-Bilder, Judge.me-Bewertungen (Shopify), Texte von
sunnozy.ch (Über uns, FAQ, Rücksendung). Look nach dem sunnozy-Designsystem: Creme, Waldgrün,
Rosé, Fraunces + Nunito Sans, keine Emojis. Oben 14 % und unten 20 % bleiben frei für die
Instagram-Bedienelemente.

Aufruf: python3 make_highlight_storys.py <instagram/highlights>
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
F = lambda n, s: ImageFont.truetype(P('fonts', n), int(s))
CREME, WALD, SALBEI, ROSE, GRAU = (253, 252, 250), (35, 48, 41), (122, 139, 111), (248, 234, 228), (98, 108, 102)
W, H = 1080, 1920
TOP, BOTTOM = 290, 1530          # Inhalt zwischen diesen Linien (IG-Safe-Zone)
SET = lambda h: P('posts', 'shopify-hauptbilder-praesentation-hd', 'bilder', f'erstausstattung-set-{h}.jpg')
SHOP = lambda h: P('posts', 'shopify-hauptbilder-klar', 'bilder', f'{h}.jpg')


def icon(name, d):
    im = Image.open(P('instagram', 'highlights', 'ki-roh', name + '.png')).convert('RGB')
    im = im.point(lambda v: min(255, round(v * 255 / 244)))
    a = np.asarray(im.convert('L')); ys, xs = np.where(a < 238)
    im = im.crop((xs.min() - 12, ys.min() - 12, xs.max() + 12, ys.max() + 12))
    k = d * 0.62 / max(im.size); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c = Image.new('RGB', (d, d), ROSE); x, y = (d - im.width) // 2, (d - im.height) // 2
    c.paste(ImageChops.multiply(c.crop((x, y, x + im.width, y + im.height)), im), (x, y))
    m = Image.new('L', (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, d * 4, d * 4), fill=255)
    return c, m.resize((d, d), Image.LANCZOS)


def umbruch(d, text, font, breite):
    zeilen = []
    for absatz in text.split('\n'):
        z = ''
        for w in absatz.split(' '):
            t = (z + ' ' + w).strip()
            if d.textlength(t, font=font) <= breite: z = t
            else: zeilen.append(z); z = w
        zeilen.append(z)
    return zeilen


def text(d, xy, s, font, fill, breite, zab=1.25, anchor='la'):
    x, y = xy
    for z in umbruch(d, s, font, breite):
        d.text((x, y), z, font=font, fill=fill, anchor=anchor); y += font.size * zab
    return y


def gesperrt(d, cx, y, s, font, fill, sp=4):
    w = sum(d.textlength(ch, font=font) for ch in s) + sp * (len(s) - 1); x = cx - w / 2
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp


def sterne(d, cx, y, n=5, r=22, fill=WALD):
    for i in range(n):
        x0 = cx + (i - (n - 1) / 2) * r * 2.4
        pts = []
        for k in range(10):
            a = -np.pi / 2 + k * np.pi / 5; rr = r if k % 2 == 0 else r * 0.45
            pts.append((x0 + rr * np.cos(a), y + rr * np.sin(a)))
        d.polygon(pts, fill=fill)


def bildkarte(c, path, box, rand=26, grund=(255, 255, 255)):
    x, y, w, h = box
    im = Image.open(path).convert('RGB')
    k = min((w - 2 * rand) / im.width, (h - 2 * rand) / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    karte = Image.new('RGB', (w, h), grund)
    karte.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=255)
    sh = Image.new('L', (w + 60, h + 60), 0); ImageDraw.Draw(sh).rounded_rectangle((30, 40, w + 30, h + 40), 34, fill=40)
    from PIL import ImageFilter
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    c.paste(Image.new('RGB', sh.size, (200, 190, 180)), (x - 30, y - 30), sh)
    c.paste(karte, (x, y), m)


def zentrieren(c):
    """Inhalt zwischen TOP und Fusszeile senkrecht mittig setzen."""
    oben, unten = TOP - 40, BOTTOM - 80
    feld = c.crop((0, oben, W, unten))
    a = np.asarray(feld.convert('L')).astype(int)
    zeilen = np.where((np.abs(a - 252) > 6).any(axis=1))[0]
    if not len(zeilen): return c
    y0, y1 = zeilen.min(), zeilen.max()
    inhalt = feld.crop((0, y0, W, y1 + 1))
    neu = Image.new('RGB', feld.size, CREME)
    neu.paste(inhalt, (0, (feld.height - inhalt.height) // 2))
    c.paste(neu, (0, oben))
    return c


def fuss(d, ki=False):
    d.text((W / 2, BOTTOM - 20), 'sunnozy.ch', font=F('nunitosans-700.ttf', 30), fill=SALBEI, anchor='ms')


def kopf(c, d, ic, eyebrow, y=TOP + 10, gross=150):
    ci, m = icon(ic, gross); c.paste(ci, ((W - gross) // 2, y), m)
    gesperrt(d, W / 2, y + gross + 34, eyebrow.upper(), F('nunitosans-700.ttf', 24), SALBEI, 5)
    return y + gross + 90


def story_intro(ic, eyebrow, titel, sub):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    ci, m = icon(ic, 420); c.paste(ci, ((W - 420) // 2, 470), m)
    gesperrt(d, W / 2, 960, eyebrow.upper(), F('nunitosans-700.ttf', 26), SALBEI, 6)
    y = text(d, (W / 2, 1060), titel, F('fraunces-600.ttf', 76), WALD, 900, 1.15, 'ma')
    text(d, (W / 2, y + 30), sub, F('nunitosans-400.ttf', 38), GRAU, 860, 1.4, 'ma')
    c = zentrieren(c); d = ImageDraw.Draw(c); fuss(d); return c


def story_produkt(ic, eyebrow, titel, bild, zeile, ki=True):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    y = kopf(c, d, ic, eyebrow)
    y = text(d, (W / 2, y), titel, F('fraunces-600.ttf', 62), WALD, 920, 1.15, 'ma')
    unten = BOTTOM - 190
    bildkarte(c, bild, (90, int(y + 30), 900, int(unten - y - 40)))
    d = ImageDraw.Draw(c)
    text(d, (W / 2, unten + 22), zeile, F('nunitosans-600.ttf', 32), WALD, 900, 1.35, 'ma')
    c = zentrieren(c); d = ImageDraw.Draw(c); fuss(d, ki); return c


def story_liste(ic, eyebrow, titel, punkte, schluss=''):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    y = kopf(c, d, ic, eyebrow, y=TOP + 40, gross=170)
    y = text(d, (W / 2, y + 10), titel, F('fraunces-600.ttf', 74), WALD, 900, 1.15, 'ma') + 60
    fk, ft = F('nunitosans-700.ttf', 44), F('nunitosans-400.ttf', 38)
    for kopfz, txt in punkte:
        d.ellipse((100, y + 12, 126, y + 38), fill=SALBEI)
        d.text((156, y), kopfz, font=fk, fill=WALD)
        y = text(d, (156, y + 62), txt, ft, GRAU, 830, 1.35) + 44
    if schluss:
        text(d, (W / 2, y + 20), schluss, F('nunitosans-600.ttf', 34), SALBEI, 880, 1.35, 'ma')
    c = zentrieren(c); d = ImageDraw.Draw(c); fuss(d); return c


def story_zitat(zitat, name, produkt, bild, uebersetzung='', verifiziert=False):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    ci, m = icon('06_bewertungen', 130); c.paste(ci, ((W - 130) // 2, TOP + 10), m)
    sterne(d, W / 2, TOP + 200)
    fz = F('fraunces-600.ttf', 56 if len(zitat) < 90 else 48)
    y = text(d, (W / 2, TOP + 260), '«' + zitat + '»', fz, WALD, 900, 1.22, 'ma')
    if uebersetzung:
        y = text(d, (W / 2, y + 14), 'Übersetzt: «' + uebersetzung + '»', F('nunitosans-400i.ttf', 30), GRAU, 880, 1.35, 'ma')
    who = name + (' · verifizierter Kauf' if verifiziert else '')
    d.text((W / 2, y + 40), who, font=F('nunitosans-700.ttf', 32), fill=SALBEI, anchor='ma')
    d.text((W / 2, y + 88), produkt, font=F('nunitosans-400.ttf', 28), fill=GRAU, anchor='ma')
    oben = y + 150; unten = BOTTOM - 70
    if bild and unten - oben > 300:
        bildkarte(c, bild, (240, int(oben), 600, int(min(600, unten - oben))))
    c = zentrieren(c); d = ImageDraw.Draw(c)
    d.text((W / 2, BOTTOM - 20), 'Bewertung auf sunnozy.ch', font=F('nunitosans-700.ttf', 28), fill=SALBEI, anchor='ms')
    return c


def inhalte():
    S = {}
    S['01_erstausstattung'] = [
        story_intro('01_erstausstattung', 'Erstausstattung', 'Alles drin für die ersten Wochen.',
                    'Komplette Sets aus 100 % Baumwolle, fertig aufeinander abgestimmt.'),
        story_produkt('01_erstausstattung', 'Set «Teddybär»', 'Creme mit Bärchen', SET('teddybaer'), 'Decke, Strampler, Body, Mütze, Söckchen, Fäustlinge, Rassel und Lätzchen'),
        story_produkt('01_erstausstattung', 'Set «Princess»', 'Rosa mit Karo und Spitze', SET('princess'), '8 Teile · 0–3 und 3–6 Monate'),
        story_produkt('01_erstausstattung', 'Set «Little and Loved»', 'Rosa mit Gänsen', SET('little-and-loved'), '8 Teile · 0–3 und 3–6 Monate'),
        story_produkt('01_erstausstattung', 'Set «Hello World»', 'Creme mit Blättern', SET('hello-world'), '8 Teile · 0–3 und 3–6 Monate'),
        story_produkt('01_erstausstattung', 'Set «Hello»', 'Zartrosa, gerippt, mit Spitze', SET('hello-spitze'), '6 Teile · 0–3 und 3–6 Monate'),
        story_produkt('01_erstausstattung', 'Set «Hello Little Bear»', 'Creme mit Bärchen-Print', SET('hello-little-bear'), '5 Teile · 0–3 und 3–6 Monate'),
    ]
    S['02_bodys'] = [
        story_intro('02_bodys', 'Bodys', 'Die Alltagshelden im Babyschrank.',
                    'Im 3er- oder 5er-Pack, langarm, kurzarm und ärmellos.'),
        story_produkt('02_bodys', 'Kurzarm, 5er-Pack', '«Little One» gerippt', SHOP('body-set-little-one-gerippt'), '100 % Baumwolle · bei 30 °C waschbar'),
        story_produkt('02_bodys', 'Kurzarm, 5er-Pack', '«Love More» Herzen und Kätzchen', SHOP('baby-kurzarm-body-5er-set-love-more-herzen-katzchen-rosa'), 'Immer genug zum Wechseln'),
        story_produkt('02_bodys', 'Langarm, 3er-Pack', '«Princess» mit Herzen', SHOP('baby-langarm-body-3er-set-princess-rosa-mit-herzen'), 'Für kühlere Tage'),
        story_liste('02_bodys', 'Gut zu wissen', 'Welche Grösse?', [
            ('Nach Alter', 'Unsere Grössen gehen nach Monaten: 0–3, 3–6 und 6–9 Monate.'),
            ('Im Zweifel grösser', 'Babys wachsen schnell. Lieber eine Grösse grösser wählen.'),
            ('Pflege', 'Schonwaschgang bei 30 °C und an der Luft trocknen.')], 'Alle Grössen im Grössenberater auf sunnozy.ch'),
    ]
    S['03_mulltuecher'] = [
        story_intro('03_mulltuecher', 'Mulltücher', 'Ein Tuch, viele Aufgaben.',
                    'Weicher Baumwoll-Musselin im 3er-Set, mit jeder Wäsche weicher.'),
        story_liste('03_mulltuecher', 'Musselin im Alltag', 'Wofür Du sie brauchst', [
            ('Spucktuch', 'Über der Schulter, beim Stillen oder Schöppeln.'),
            ('Leichte Decke', 'Für warme Tage und den Mittagsschlaf.'),
            ('Unterwegs', 'Als Sonnenschutz am Kinderwagen oder Wickelunterlage.'),
            ('Nuscheli', 'Zum Kuscheln und Einschlafen.')]),
        story_produkt('03_mulltuecher', '112 × 112 cm', '3er-Set «Teddybär»', SHOP('mulltuecher-3er-set-teddybaer'), 'Auch in Neutral, Rosa und Blau'),
        story_produkt('03_mulltuecher', '90 × 100 cm', '3er-Set Rosa', SHOP('mulltuecher-3er-set-90x100'), 'Auch in Blau und Grün/Natur'),
    ]
    S['04_accessoires'] = [
        story_intro('04_accessoires', 'Accessoires', 'Kleine Begleiter für jeden Tag.',
                    'Söckchen, Halstücher und Lätzchen aus 100 % Baumwolle.'),
        story_produkt('04_accessoires', 'Söckchen, 5er-Set', '«Spitze und Blümchen»', SHOP('baby-soeckchen-5er-set-spitze-bluemchen'), 'Warm für die kleinsten Füsse'),
        story_produkt('04_accessoires', 'Halstücher, 3er-Set', '«I Love My Mummy»', SHOP('baby-halstuecher-3er-set-i-love-my-mummy-rosa'), 'Saugstark beim Zahnen und Sabbern'),
        story_produkt('04_accessoires', 'Lätzchen und Söckchen', 'Geschenkset «Beige Teddy»', SHOP('baby-geschenkset-beige-teddy-4-teilig'), '4-teilig · ein schönes Mitbringsel'),
    ]
    S['05_geschenke'] = [
        story_intro('05_geschenke', 'Geschenke zur Geburt', 'Das schönste Hallo.',
                    'Komplette Sets, fertig kombiniert und schön zum Auspacken.'),
        story_liste('05_geschenke', 'So kommt Dein Geschenk an', 'Hübsch verpackt, ohne Plastik', [
            ('Seidenpapier und Papierschnur', 'Jedes Paket wird von Hand gepackt.'),
            ('Im Karton', 'Die ganze Verpackung darf ins Altpapier.'),
            ('Schnell da', 'Verpackt innert 1–2 Werktagen, Zustellung meist 2–3 Werktage.')]),
        story_produkt('05_geschenke', 'Tipp', 'Creme passt immer, auch wenn es noch eine Überraschung ist', SET('teddybaer'), 'Erstausstattung-Set «Teddybär»'),
        story_zitat('Die Ware wurde als Geschenk weiter gereicht und ist dort sehr gut angekommen. Ich kann es nur empfehlen.',
                    'Kathrin', 'Erstausstattung-Set «Teddybär»', SET('teddybaer')),
    ]
    S['06_bewertungen'] = [
        story_intro('06_bewertungen', 'Bewertungen', '5,0 von 5 Sternen',
                    'Aus 13 Bewertungen auf sunnozy.ch. Danke für jedes liebe Wort.'),
        story_zitat('Super schnelle Abwicklung des Warenvorgangs. Sehr gute Qualität. Die Ware wurde als Geschenk weiter gereicht und ist dort sehr gut angekommen.',
                    'Kathrin', 'Erstausstattung-Set «Teddybär»', SET('teddybaer')),
        story_zitat("I'm simply pleasantly shocked: the quality is excellent, the delivery is fast.",
                    'Anonym', 'Erstausstattung-Set «Hello World»', SET('hello-world'),
                    uebersetzung='Ich bin einfach angenehm überrascht: Die Qualität ist ausgezeichnet, die Lieferung schnell.', verifiziert=True),
        story_zitat('Super Qualität, sieht genau wie aus dem Bild. Schnelle Versand.', 'Andrea', 'Erstausstattung-Set «Teddybär»', SET('teddybaer')),
        story_zitat('Super schneller Versand, alles lief sehr gut. Gerne wieder. Merci', 'MariolyG', 'Erstausstattung-Set «Hello»', SET('hello-spitze')),
        story_zitat('Super schnell Versand und sehr nette Verkäuferin mit wirklich niedlichen Produkten.', 'Monica', 'Erstausstattung-Set «Hello Little Bear»', SET('hello-little-bear')),
        story_zitat('Alles tip top: schnelle Kommunikation und Versand', 'eff_g8mf', 'Söckchen 5er-Set «Neutral Umschlag»', SHOP('baby-soeckchen-5er-set-neutral-umschlag')),
    ]
    S['07_versand'] = [
        story_intro('07_versand', 'Versand', 'Von Baden direkt zu Dir.',
                    'Wir packen jede Bestellung persönlich und schicken sie mit der Schweizerischen Post.'),
        story_liste('07_versand', 'Versand in der Schweiz', 'Kosten und Lieferzeit', [
            ('CHF 5.90 pro Bestellung', 'Ab CHF 50 liefern wir gratis.'),
            ('Verpackt innert 1–2 Werktagen', 'Danach dauert die Zustellung meist 2–3 Werktage.'),
            ('Versandbestätigung', 'Sobald Dein Paket unterwegs ist, bekommst Du eine E-Mail.')]),
        story_liste('07_versand', 'Rückgabe', '14 Tage Rückgabe', [
            ('Ungetragen zurück', 'In der Originalverpackung, innerhalb von 14 Tagen nach Erhalt.'),
            ('Einfach per E-Mail', 'Schreib an info@sunnozy.ch mit Deiner Bestellnummer.'),
            ('Geld zurück', 'Nach Erhalt und Prüfung erstatten wir den Betrag innert weniger Tage.')]),
        story_liste('07_versand', 'Bezahlen', 'Sicher bezahlen', [
            ('TWINT und Karte', 'Dazu Klarna und Shop Pay.'),
            ('SSL-verschlüsselt', 'Alle Zahlungen laufen über Shopify.')]),
    ]
    S['08_ueber_uns'] = [
        story_intro('08_ueber_uns', 'Über uns', 'Für die ersten grossen Momente.',
                    'Weiche Babykleidung, in der alles zusammenpasst.'),
        story_liste('08_ueber_uns', 'Woran wir glauben', 'Weniger, aber richtig', [
            ('Komplette Sets', 'Statt hundert Einzelteile, vom ersten Body bis zur Kuscheldecke.'),
            ('Hautfreundlich', '100 % Baumwolle, sanft zur zartesten Haut.'),
            ('Ehrlich', 'Faire Preise, 14 Tage Rückgabe und Versand aus der Schweiz.')]),
        story_intro('08_ueber_uns', 'Wer dahinter steht', 'Persönlich aus Baden.',
                    'Jede Bestellung wird von uns persönlich zusammengestellt, verpackt und verschickt. Schreib uns, wir freuen uns.'),
    ]
    return S


if __name__ == '__main__':
    base = sys.argv[1]
    for name, storys in inhalte().items():
        o = os.path.join(base, 'storys', name); os.makedirs(o, exist_ok=True)
        for i, s in enumerate(storys, 1):
            s.save(os.path.join(o, f'story_{i:02d}.jpg'), quality=93)
        print(name, len(storys))
