"""«Erstausstattung in 60 Sekunden»: Set «Hello Little Bear» Schritt für Schritt auspacken (Wunsch der Nutzerin 25.11.2026).

Hooks (auf Englisch, Regel ab 24.11.2026):
  «everything for the first weeks, in one bag 🤍» und «newborn essentials, shipped from Switzerland, piece by piece»
  (ehrlich: «shipped from Switzerland», nicht «from Switzerland», siehe CLAUDE.md)
Ablauf: sunnozy-Tasche → jedes der 5 Teile steigt aus der Tasche, gross mit Eigenschaft (aus der Shopify-Beschreibung),
dazwischen das echte Auspack-Video → alle Teile zusammen → Baby (wach) im Set → Endfolie. Standardmusik.

    python3 tools/make_reel_hlb_auspacken.py
Ausgabe: posts/coming-soon/reels/hello-little-bear/reel_hello_little_bear_auspacken_60s_9x16.mp4
"""
import os
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_marketing4weeks as mw
from endfolie import SHOP

W, H, FPS = m.W, m.H, 30
P = m.POSTS
ORDNER = os.path.join(P, 'coming-soon', 'reels', 'hello-little-bear')
TASCHE = os.path.join(P, 'coming-soon', 'photos', 'paket-7-werbung', 'roh', 'tasche.png')
TEIL = lambda t: os.path.join(P, 'coming-soon', 'photos', 'marktplatz-galaxus-amazon', 'einzelteile', 'set_little_bear', f'set_little_bear_{t}.jpg')
AUSPACKEN = os.path.join(P, 'baby-videos', '–_Unboxing_Set_auslegen_Sto.mp4')
BABY = os.path.join(ORDNER, 'original', 'clip_bett.mp4')          # Baby wach, auf dem Rücken, im Set
PRAES = os.path.join(P, 'coming-soon', 'photos', 'hello-little-bear', 'original', 'set_praesentation.jpg')
CREME, DUNKEL, GRAU = mw.CREME, mw.DUNKEL, mw.GRAU
# Teil, Name, Eigenschaft (aus der Shopify-Beschreibung), Ausschnitt aus dem Auspack-Video (von, bis) oder None
TEILE = [('strampler', 'romper', 'teddy print · zip for easy changes', (0.3, 3.3)),
         ('body', 'bodysuit', 'striped · «funny every day» bears', None),
         ('laetzchen', 'bib', '«Hello Little Bear» embroidery', (3.5, 6.5)),
         ('muetze', 'hat', 'knot hat with little ears', (6.6, 9.6)),
         ('faeustlinge', 'mittens', 'scratch mittens for tiny hands', None)]


def tasche_bild(breite):
    t = Image.open(TASCHE).convert('RGBA'); t = t.crop(t.getbbox())
    t = t.resize((breite, round(t.height * breite / t.width)), Image.LANCZOS)
    L = m.logo(int(breite * 0.5), (122, 108, 104)).convert('RGBA')
    t.alpha_composite(L, ((t.width - L.width) // 2, int(t.height * 0.55)))
    return t


TASCHE_GROSS, TASCHE_KLEIN = tasche_bild(620), tasche_bild(420)


def intro(dauer):
    """Tasche schwebt leicht, Hook steht oben (eigene Textebenen im Video)."""
    for i in range(int(round(dauer * FPS))):
        t = i / FPS; c = Image.new('RGBA', (W, H), CREME + (255,))
        dy = int(12 * m.ease(abs(((t * 0.6) % 2) - 1)))
        mw.schatten_setzen(c, TASCHE_GROSS, (W - TASCHE_GROSS.width) // 2, 760 + dy, r=30, a=55)
        yield c.convert('RGB')


def aufsteigen(teil, dauer=1.6):
    """Teil steigt aus der Tasche und wird gross."""
    im = mw.einpassen(mw.laden(TEIL(teil)), 760, 760).convert('RGBA')
    # weissen Hintergrund des Einzelbilds weich ausblenden
    px = im.load(); a = Image.new('L', im.size, 255); pa = a.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 246 and g > 246 and b > 246:
                pa[x, y] = 0
    im.putalpha(a)
    tx, ty = (W - TASCHE_KLEIN.width) // 2, 1300
    for i in range(int(round(dauer * FPS))):
        p = m.ease(i / (dauer * FPS)); c = Image.new('RGBA', (W, H), CREME + (255,))
        s = 0.25 + 0.75 * p; t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        y = int((ty + 80) * (1 - p) + (900 - t.height / 2) * p)
        c.alpha_composite(t, ((W - t.width) // 2, y))
        ta = TASCHE_KLEIN.copy(); ta.putalpha(ta.split()[3].point(lambda v: int(v * (1 - p))))
        c.alpha_composite(ta, (tx, ty + int(200 * p)))
        yield c.convert('RGB')


def zeigen(teil, nr, name, info, dauer=3.4):
    im = mw.einpassen(mw.laden(TEIL(teil)), 860, 860)
    for i in range(int(round(dauer * FPS))):
        z = 1.0 + 0.06 * m.ease(i / (dauer * FPS)); c = Image.new('RGBA', (W, H), CREME + (255,))
        t = im.resize((int(im.width * z), int(im.height * z)), Image.LANCZOS).convert('RGBA')
        c.alpha_composite(t, ((W - t.width) // 2, 900 - t.height // 2))
        mw.text(c, [f'{nr}/5  {name}'], 1430, 58, DUNKEL); mw.text(c, [info], 1520, 38, GRAU)
        yield c.convert('RGB')


def alles(dauer=4.0):
    teile = [mw.einpassen(mw.laden(TEIL(t)), 430, 430).convert('RGBA') for t, *_ in TEILE]
    pos = [(70, 330), (580, 330), (70, 800), (580, 800), (325, 1270)]
    for i in range(int(round(dauer * FPS))):
        tt = i / FPS; c = Image.new('RGBA', (W, H), CREME + (255,))
        for k, (im, (x, y)) in enumerate(zip(teile, pos)):
            a = m.ease((tt - k * 0.25) / 0.4)
            if a > 0:
                t2 = im.copy(); t2.putalpha(t2.split()[3].point(lambda v: int(v * a))); c.alpha_composite(t2, (x, y))
        yield c.convert('RGB')


def main():
    szenen = [('frames', intro(8.5), 8.5)]
    texte = [(0, 4.4, ['everything for the', 'first weeks,', 'in one bag'], '🤍', 260, mw.DUN),
             (4.4, 8.3, ['newborn essentials,', 'shipped from Switzerland,', 'piece by piece'], '✨', 260, mw.DUN)]
    t = 8.5 - 0.3
    for nr, (teil, name, info, ab) in enumerate(TEILE, 1):
        szenen.append(('frames', aufsteigen(teil), 1.6)); t += 1.6 - 0.3
        szenen.append(('frames', zeigen(teil, nr, name, info), 3.4)); t += 3.4 - 0.3
        if ab:
            szenen.append(('clip', AUSPACKEN, *ab)); t += (ab[1] - ab[0]) - 0.3
        else:
            szenen.append(('bild', TEIL(teil), 2.6, 1.6, 2.0, 0.5, 0.45)); t += 2.6 - 0.3   # Nahaufnahme
    szenen.append(('frames', alles(4.6), 4.6))
    texte.append((t + 0.4, t + 4.3, ['5 pieces, all in one bag'], '🤍', 1780, mw.DUN)); t += 4.6 - 0.3
    szenen.append(('clip', BABY, 4.0, 9.5))
    texte.append((t + 0.3, None, ['everything for the', 'first weeks'], '🧸', 1420, mw.POV))
    mw.video(0, 'reel_hello_little_bear_auspacken_60s', szenen, texte,
             (PRAES, '«Hello Little Bear»', 'newborn set · 5 pieces', SHOP), ordner=ORDNER)


if __name__ == '__main__':
    main()
