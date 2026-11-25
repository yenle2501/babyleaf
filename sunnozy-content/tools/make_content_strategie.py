"""Drei Video-Skripte aus der Content-Strategie der Nutzerin (25.11.2026), auf Englisch (Regel ab 24.11.2026), ohne Gesicht
der Nutzerin, nur Produkte, die in Shopify aktiv sind, Babys wach.

  video1_emotional   «nobody tells you how fast these tiny outfits get too small…» → Baby im Set → Details → Schluss
  video2_gift        «still looking for the perfect baby gift?» → Geschenkbox öffnen → Teile einzeln → Schluss
  video3_comments    «swiss mamas, we need your opinion!» → 3 Sets 1/2/3 → «which one would you choose?»

    python3 tools/make_content_strategie.py [video1_emotional|video2_gift|video3_comments]
Ausgabe: posts/content-strategie/ (Strategie, Hooks, Captions: README.md dort)
"""
import os, sys
import make_coming_soon_reels as m
import make_marketing4weeks as mw
from endfolie import SHOP

P = m.POSTS
ORDNER = os.path.join(P, 'content-strategie')
CS = os.path.join(P, 'coming-soon', 'photos')
KLAR = lambda h: os.path.join(CS, 'shopify-hauptbilder-klar', 'bilder', h + '.jpg')
FRE = lambda k: os.path.join(CS, 'marktplatz-galaxus-amazon', 'freigestellt', f'set_{k}.png')
TEIL = lambda t: os.path.join(CS, 'marktplatz-galaxus-amazon', 'einzelteile', 'set_little_bear', f'set_little_bear_{t}.jpg')
HLB_BABY = os.path.join(P, 'coming-soon', 'reels', 'hello-little-bear', 'original', 'clip_bett.mp4')
PRINCESS_BABY = os.path.join(P, 'baby-videos', 'princess_rosa_a_bearbeitet.mp4')
BOX_CLIP = os.path.join(P, 'baby-videos', 'weihnachtsbox_mummy_a_bearbeitet.mp4')
BOX_FOTO = os.path.join(CS, 'kampagne-weihnachtsbox', 'fotos', 'box_i_love_my_mummy.jpg')
WEISS = lambda n: os.path.join(CS, 'shopify-hauptbilder-weiss', n)
POV, DUN = mw.POV, mw.DUN


def end_collage(pfade):
    """Freigestellte Sets auf Creme (sonst wird der durchsichtige Grund auf der Endfolie schwarz)."""
    import tempfile
    from PIL import Image
    c = Image.new('RGBA', (1000, 1000), mw.CREME + (255,))
    for k, p in enumerate(pfade[:4]):
        im = mw.einpassen(mw.laden(p), 470, 470).convert('RGBA')
        x = (k % 2) * 510 + (490 - im.width) // 2 if not (len(pfade) == 3 and k == 2) else 255 + (490 - im.width) // 2
        c.alpha_composite(im, (x, (k // 2) * 510 + (490 - im.height) // 2))
    pfad = os.path.join(tempfile.gettempdir(), 'strategie_endbild.jpg'); c.convert('RGB').save(pfad, quality=94)
    return pfad


def video1_emotional():
    mw.video(0, 'video1_emotional', [
        ('clip', HLB_BABY, 1.0, 4.2),
        ('clip', PRINCESS_BABY, 1.0, 3.8),
        ('bild', TEIL('muetze'), 2.0, 1.6, 2.0, 0.5, 0.4),
        ('bild', TEIL('strampler'), 2.0, 2.2, 2.6, 0.5, 0.75),
        ('clip', HLB_BABY, 9.0, 11.6)],
        [(0, 2.8, ['nobody tells you how fast', 'these tiny outfits', 'get too small…'], '🥹', 1380, POV),
         (9.0, None, ['make every little', 'moment unforgettable'], '❤️', 1420, POV)],
        (KLAR('erstausstattung-set-hello-little-bear'), '«Hello Little Bear»', 'newborn set · 5 pieces', SHOP), ordner=ORDNER)


def video2_gift():
    mw.video(0, 'video2_gift', [
        ('bild', BOX_FOTO, 2.2, 1.0, 1.08, 0.5, 0.5),
        ('breit', BOX_CLIP, 1.0, 4.5),
        ('produkt', WEISS('mummy_langarm3.jpg'), 1.8, mw.BLUSH, '3 bodysuits «I love my Mummy»'),
        ('produkt', KLAR('baby-halstuecher-3er-set-i-love-my-mummy'), 1.8, mw.BEIGE, '3 bandana bibs'),
        ('bild', BOX_FOTO, 2.2, 1.6, 1.9, 0.62, 0.22)],
        [(0, 2.4, ['still looking for the', 'perfect baby gift?'], '🎁', 1420, POV),
         (8.6, None, ['discover sweet baby', 'favourites at sunnozy'], '🤍', 1420, POV)],
        (BOX_FOTO, 'gift box «I love my Mummy»', '3 bodysuits + 3 bandana bibs', SHOP), ordner=ORDNER)


def video3_comments():
    mw.video(0, 'video3_comments', [
        ('produkt', FRE('little_bear'), 2.0, mw.BEIGE, '1  «Hello Little Bear»', None),
        ('produkt', FRE('little_and_loved_gans_rosa'), 2.0, mw.BLUSH, '2  «Little and Loved»', None),
        ('produkt', FRE('hello_world_blatt'), 2.0, (222, 230, 214), '3  «Hello World»', None),
        ('raster', [FRE('little_bear'), FRE('little_and_loved_gans_rosa'), FRE('hello_world_blatt')], 2.6, mw.CREME)],
        [(0, 2.2, ['swiss mamas,', 'we need your opinion!'], '🇨🇭', 280, DUN),
         (2.2, None, ['which one would you', 'choose? 1, 2 or 3?'], '👇', 280, DUN)],
        (end_collage([FRE('little_bear'), FRE('little_and_loved_gans_rosa'), FRE('hello_world_blatt')]), 'our newborn sets', 'team 1, 2 or 3?', SHOP),
        ordner=ORDNER, blende=0.15)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['video1_emotional', 'video2_gift', 'video3_comments']:
        globals()[n]()
