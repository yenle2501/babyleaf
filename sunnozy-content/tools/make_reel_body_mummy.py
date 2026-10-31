"""Reel aus dem echten Handyvideo der Nutzerin (IMG_7459, 31.10.2026): Body-Set «I love my Mummy» Kurzarm, 5er-Pack,
dazu passend das Halstücher-Set «I love my Mummy» Beige (Video IMG_7524). Machart wie make_reels_videos_baby.py.

    python3 tools/make_reel_body_mummy.py

Das Body-Video ist ruhig (6 s, Stapel auf dem Wickeltisch): darum nur der untere Bildteil mit langsamem Zoom.
Oben stehen fremde Marken (Pflegeprodukte, Windeln): die bleiben immer ausserhalb des Ausschnitts.
Preise laut Shop (31.10.2026): Body-Set CHF 16.70 (alle Grössen 0–9 Monate), Halstücher CHF 7.99.
Ausgabe: posts/reels/im-shop/reel_body_mummy_kurzarm_9x16.mp4 + _titelbild.jpg
"""
import os
import make_coming_soon_reels as m
import make_reels_videos_baby as rv
import make_coming_soon_kombi as k
from PIL import Image, ImageDraw, ImageFilter

seg = rv.seg
rv.ZMAX = 2.0                     # Handyvideo 1080 breit: etwas mehr Zoom geht, der fremde Kram oben muss raus
REELS = {
    'body_mummy_kurzarm': dict(
        segmente=[seg('body_mummy_kurzarm', 0.0, 3.0, 1.5, 1.6, 0.48, 0.7),
                  seg('body_mummy_kurzarm', 3.0, 6.1, 1.85, 1.95, 0.4, 0.76),
                  seg('halstuecher_mummy_beige', 6.4, 9.6, 1.15, 1.22, 0.5, 0.56)],
        texte=[['Die süsseste', 'Liebeserklärung an Mama'], ['Zwei Bärchen und', '«I love my Mummy»'], ['Passend dazu:', 'das Halstuch-Set']],
        liste=(['«I love my Mummy»'], [('Body-Set Kurzarm, 5 Stück', 'CHF 16.70'), ('Halstücher, 3 Stück', 'CHF 7.99')],
               ['Grössen 0–9 Monate', 'Jetzt auf sunnozy.ch'])),
}

OBEN = {'Die süsseste', 'Zwei Bärchen und'}     # Motiv liegt unten im Bild: dort Text oben, dunkel auf dem hellen Tisch
_text_unten = m.text_unten


def text(c, zeilen, alpha, y=1290, groesse=92):
    if not zeilen or zeilen[0] not in OBEN:
        return _text_unten(c, zeilen, alpha, y, groesse)
    W = m.W; fo = m.f(m.SERIF, 88); lh = 88 * 1.12
    halo = Image.new('RGBA', c.size, (0, 0, 0, 0)); dh = ImageDraw.Draw(halo)
    tx = Image.new('RGBA', c.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    for i, z in enumerate(zeilen):
        p = (W / 2, 250 + i * lh)
        dh.text(p, z, font=fo, fill=(255, 255, 255, int(230 * alpha)), anchor='mm', stroke_width=10, stroke_fill=(255, 255, 255, int(230 * alpha)))
        dt.text(p, z, font=fo, fill=m.WALD + (int(255 * alpha),), anchor='mm')
    c.alpha_composite(halo.filter(ImageFilter.GaussianBlur(14)))
    c.alpha_composite(tx)
    return c


if __name__ == '__main__':
    m.text_unten = text
    rv.REELS = REELS
    rv.VB = os.path.join(m.POSTS, 'videos-produkt')
    m.OUT = os.path.join(m.POSTS, 'reels', 'im-shop')
    for key in REELS:
        rv.reel(key, 0)
