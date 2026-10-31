"""Reel aus den echten Handyvideos der Nutzerin (31.10.2026): Halstücher 3er-Sets «I love my Mummy» Beige,
«Cool like Daddy» und «Baby Flowers». Gleiche Machart wie make_reels_videos_baby.py (Schnitte, Zoom, Text, Musik, Loop).

    python3 tools/make_reel_halstuecher.py

Clips: posts/videos-produkt/halstuecher_*_bearbeitet.mp4 (iPhone-Videos hochkant, leicht aufgehellt, ohne Ton).
Alle drei Sets sind im Shop (CHF 7.99, je 3 Halstücher, 100 % Baumwolle laut Produkttitel, Stand 31.10.2026).
Ausgabe: posts/reels/im-shop/reel_halstuecher_3er_sets_9x16.mp4 + _titelbild.jpg
"""
import os
import make_coming_soon_reels as m
import make_reels_videos_baby as rv
import make_coming_soon_kombi as k
from PIL import Image, ImageDraw, ImageFilter

seg = rv.seg
REELS = {
    'halstuecher_3er_sets': dict(
        segmente=[seg('halstuecher_alle_drei', 2.5, 13.8, 1.2, 1.24, 0.5, 0.57, tempo=2.4),
                  seg('halstuecher_mummy_beige', 6.4, 9.9, 1.15, 1.22, 0.5, 0.56),
                  seg('halstuecher_cool_like_daddy', 5.6, 9.1, 1.15, 1.22, 0.5, 0.56),
                  seg('halstuecher_baby_flowers', 6.0, 9.0, 1.15, 1.22, 0.5, 0.56)],
        texte=[['Welches Halstuch-Set', 'ist Dein Favorit?'], {'zahl': '1', 'name': '«I love my Mummy»'},
               {'zahl': '2', 'name': '«Cool like Daddy»'}, {'zahl': '3', 'name': '«Baby Flowers»'}],
        liste=(['Halstücher', 'im 3er-Set'], [('1  I love my Mummy', 'CHF 7.99'), ('2  Cool like Daddy', 'CHF 7.99'), ('3  Baby Flowers', 'CHF 7.99')],
               ['100 % Baumwolle, 3 Stück pro Set', 'Schreib Deine Zahl in die Kommentare', 'Jetzt auf sunnozy.ch'])),
}

def zahl(c, nummer, name, alpha):
    """Wie k.zahl, aber die Zahl in Fraunces: in Cormorant sieht die «1» wie ein «I» aus."""
    W, H = m.W, m.H
    f = m.f('fraunces-600.ttf', 210)
    m.text_unten(c, [name], alpha, y=1400, groesse=80)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 3, 1235 + 4), nummer, font=f, fill=(20, 14, 10, int(190 * alpha)), anchor='mm')
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(c).text((W / 2, 1235), nummer, font=f, fill=(255, 255, 255, int(255 * alpha)), anchor='mm')
    return c


if __name__ == '__main__':
    k.zahl = zahl
    rv.REELS = REELS
    rv.VB = os.path.join(m.POSTS, 'videos-produkt')
    m.OUT = os.path.join(m.POSTS, 'reels', 'im-shop')
    for key in REELS:
        rv.reel(key, 1)
