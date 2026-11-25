"""30 Reels + Feed-Posts + Storys nach der Content-Strategie der Nutzerin («Sunnozy – komplette Social-Media-Content-
Strategie», 25.11.2026). Alles auf Englisch (Regel ab 24.11.2026), nur Produkte, die in Shopify aktiv sind, Babys wach.

Stil (Teil 10 der Strategie): Creme und Zartrosa, grosse klare Hooks (fette Schrift ohne Serifen auf cremefarbenem Band,
kein Leuchten), kleines Sonnenmotiv ☀️, Standardmusik, Endfolie.
Ehrlich: «shipped from Switzerland» / «a small baby shop based in Switzerland», nicht «Swiss brand» oder «made in
Switzerland»; keine Bewertungen; keine schlafenden Babys (Reel 23 ohne «Baby schläft ein»).

    python3 tools/make_contentgpt.py                  # alles
    python3 tools/make_contentgpt.py bilder           # nur Posts und Storys
    python3 tools/make_contentgpt.py reel01 reel05    # einzelne Reels
Ausgabe: posts/contentgpt/reels/, posts/contentgpt/posts/, posts/contentgpt/storys/ (Plan + Captions: README.md)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
import make_coming_soon_reels as m
import make_marketing4weeks as mw
from endfolie import SHOP, CS_AUFRUF

W, H = m.W, m.H
P = m.POSTS
OUT = os.path.join(P, 'contentgpt')
CS = os.path.join(P, 'coming-soon', 'photos')
VID = os.path.join(P, 'baby-videos')
KLAR = lambda h: os.path.join(CS, 'shopify-hauptbilder-klar', 'bilder', h + '.jpg')
WEISS = lambda n: os.path.join(CS, 'shopify-hauptbilder-weiss', n + '.jpg')
FRE = lambda k: os.path.join(CS, 'marktplatz-galaxus-amazon', 'freigestellt', f'set_{k}.png')
def TEIL(s, t):
    lang = os.path.join(CS, 'marktplatz-galaxus-amazon', 'einzelteile', f'set_{s}', f'set_{s}_{t}.jpg')
    return lang if os.path.exists(lang) else os.path.join(CS, 'marktplatz-galaxus-amazon', 'einzelteile', f'set_{s}', f'{t}.jpg')
BOXF = lambda b: os.path.join(CS, 'kampagne-weihnachtsbox', 'fotos-echt', f'box_{b}.jpg')
R5 = lambda c: os.path.join(VID, 'runde5', 'bearbeitet', c + '.mp4')
V = lambda c: os.path.join(VID, c)
HLB_BABY = os.path.join(P, 'coming-soon', 'reels', 'hello-little-bear', 'original', 'clip_bett.mp4')
PRIN_BABY = V('princess_rosa_a_bearbeitet.mp4')
HAENDE1, HAENDE2, HAENDE3 = V('Hand_placing_baby_bodysuits_in_202608310851.mp4'), V('Hand_placing_baby_bodysuits_in_202608311030.mp4'), V('Hands_changing_baby_bodysuits_in…_202608311248.mp4')
BOX_A, BOX_B = V('weihnachtsbox_mummy_a_bearbeitet.mp4'), V('weihnachtsbox_mummy_b_bearbeitet.mp4')
UNBOX = V('–_Unboxing_Set_auslegen_Sto.mp4')
SWADDLE = V('Swaddle_blanket_product_video_20260928131531.mp4')
HLB_KLAR, HW_KLAR, LAL_KLAR, PRIN_KLAR = (KLAR('erstausstattung-set-' + h) for h in ['hello-little-bear', 'hello-world', 'little-and-loved', 'princess'])
CREME, BLUSH, BEIGE, LILA = mw.CREME, mw.BLUSH, mw.BEIGE, (232, 222, 238)
B = 'band'
TOP, LOW = 300, 1430


def reel(nr, name, szenen, texte, karte, blende=0.3):
    mw.video(0, f'reel{nr:02d}_{name}', szenen, texte, karte, blende=blende, ordner=os.path.join(OUT, 'reels'))


SHOPKARTE = lambda bild, name, zeile='newborn set': (bild, name, zeile, SHOP)
SUNNOZY = (HLB_KLAR, 'little outfits, big love', 'sunnozy.ch', SHOP)


# ---------------- Woche 1: Aufmerksamkeit & Emotionen ----------------
def reel01():
    reel(1, 'tiny_outfits', [('clip', HLB_BABY, 1.0, 3.6), ('clip', PRIN_BABY, 0.5, 3.0), ('bild', TEIL('little_bear', 'faeustlinge'), 1.8, 1.0, 1.15),
                             ('bild', TEIL('little_bear', 'strampler'), 1.8, 1.9, 2.2, 0.5, 0.8), ('clip', PRIN_BABY, 6.5, 9.3)],
         [(0, 2.4, ['nobody prepares you for', 'how fast these tiny', 'outfits get too small…'], '🥹', TOP, B),
          (2.4, 4.8, ['tiny hands.'], None, LOW, B), (4.8, 6.6, ['little feet.'], None, LOW, B), (6.6, 8.6, ['biggest love.'], None, LOW, B),
          (8.6, None, ['make every moment count'], '🤍', LOW, B)], SHOPKARTE(HLB_KLAR, '«Hello Little Bear»'))


def reel02():
    teile = ['body-set-little-love-rosa', 'baby-langarm-body-3er-set-princess-rosa-mit-herzen', 'baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen',
             'baby-langarm-body-3er-set-ripp-lovely-little-girl-lila-rosa', 'baby-kurzarm-body-5er-set-love-more-herzen-katzchen-rosa']
    reel(2, 'just_one_romper', [('produkt', KLAR(t), 1.4, [BLUSH, CREME, LILA, BEIGE, BLUSH][k]) for k, t in enumerate(teile)]
         + [('raster', [KLAR(t) for t in teile[:4]], 2.4, CREME)],
         [(0, 2.2, ['POV: you only wanted to', 'buy ONE baby romper'], '😂', TOP, B), (2.2, 3.6, ['just one outfit…'], None, LOW, B),
          (3.6, 5.0, ['okay, maybe two.'], None, LOW, B), (5.0, 6.4, ['wait… THIS ONE!'], '😍', LOW, B), (7.0, None, ['mom life.'], '☀️', LOW, B)],
         SHOPKARTE(KLAR(teile[0]), 'little favourites', 'bodysuits · leggings · newborn sets'), blende=0.15)


def reel03():
    reel(3, 'outfit_reveal', [('bild', TEIL('little_bear', 'body'), 2.0, 1.0, 1.1), ('clip', UNBOX, 0.3, 3.0),
                              ('bild', TEIL('little_bear', 'laetzchen'), 1.8, 1.4, 1.6), ('clip', HLB_BABY, 4.0, 7.0)],
         [(0, 2.2, ['wait until you see', 'this little outfit!'], '🎀', TOP, B), (2.2, 4.4, ['little outfit.'], None, LOW, B),
          (4.4, 6.4, ['big cuteness.'], None, LOW, B), (6.4, None, ['your new favourite look?'], '🤍', LOW, B)],
         SHOPKARTE(HLB_KLAR, '«Hello Little Bear»'))


def reel04():
    reel(4, 'swiss_mamas_opinion', [('produkt', FRE('rosa_A'), 2.0, BLUSH, '1  team pink'), ('produkt', FRE('little_bear'), 2.0, BEIGE, '2  team beige'),
                                    ('produkt', KLAR('baby-langarm-body-3er-set-ripp-lovely-little-girl-lila-rosa'), 2.0, LILA, '3  team lilac'),
                                    ('raster', [FRE('rosa_A'), FRE('little_bear'), KLAR('baby-langarm-body-3er-set-ripp-lovely-little-girl-lila-rosa')], 2.6, CREME)],
         [(0, 2.0, ['swiss mamas, we need', 'your opinion!'], '🇨🇭', TOP, B), (6.2, None, ['choose your favourite!', '1, 2 or 3?'], '👇', 1700, B)],
         SHOPKARTE(PRIN_KLAR, 'our favourites', 'team 1, 2 or 3?'), blende=0.15)


def reel05():
    reel(5, 'perfect_baby_gift', [('bild', BOXF('i_love_my_mummy'), 2.4, 1.0, 1.08), ('breit', BOX_A, 1.0, 5.0),
                                  ('produkt', WEISS('mummy_langarm3'), 1.8, BLUSH, '3 bodysuits'), ('produkt', KLAR('baby-halstuecher-3er-set-i-love-my-mummy'), 1.8, BEIGE, '3 bandana bibs'),
                                  ('bild', BOXF('i_love_my_mummy'), 2.4, 1.15, 1.25)],
         [(0, 2.4, ['invited to meet a new baby', 'and still need a gift?'], '🎁', TOP, B), (2.4, 6.0, ['a little gift.'], None, LOW, B),
          (6.0, 9.4, ['a lot of love.'], None, LOW, B), (9.4, None, ['made for little miracles'], '🤍', LOW, B)],
         SHOPKARTE(BOXF('i_love_my_mummy'), 'gift box «I love my Mummy»', '3 bodysuits + 3 bandana bibs'))


def reel06():
    reel(6, 'details_matter', [('bild', TEIL('little_bear', 'strampler'), 1.8, 2.2, 2.5, 0.5, 0.35), ('bild', TEIL('rosa', 'body'), 1.8, 2.0, 2.3, 0.5, 0.25),
                               ('bild', TEIL('little_and_loved_gans_rosa', 'body'), 1.8, 1.8, 2.1, 0.5, 0.45), ('bild', TEIL('hello_world_blatt', 'body'), 1.8, 1.8, 2.1, 0.5, 0.45),
                               ('produkt', FRE('little_and_loved_gans_rosa'), 2.2, CREME)],
         [(0, 2.0, ["it's all about the", 'little details'], '✨', TOP, B), (2.0, 3.8, ['soft details.'], None, LOW, B), (3.8, 5.6, ['sweet designs.'], None, LOW, B),
          (5.6, None, ['little things we love'], '🤍', LOW, B)], SHOPKARTE(LAL_KLAR, '«Little and Loved»'))


def reel07():
    reel(7, 'slow_down_mama', [('clip', HLB_BABY, 0.5, 3.5), ('clip', PRIN_BABY, 3.5, 6.3), ('clip', R5('33_box_mummy_halstuch_arm'), 2.0, 4.6), ('clip', HLB_BABY, 9.0, 12.0)],
         [(0, 2.4, ['a little reminder', 'to slow down, mama'], '🤍', TOP, B), (2.4, 5.2, ['slow mornings.'], None, LOW, B),
          (5.2, 7.8, ['tiny cuddles.'], None, LOW, B), (7.8, None, ['forever memories.'], '☀️', LOW, B)], SUNNOZY)


# ---------------- Woche 2: Produktliebe & Vertrauen ----------------
def reel08():
    reel(8, 'order_arrived', [('clip', HAENDE1, 0.0, 3.0), ('clip', UNBOX, 0.3, 4.0), ('clip', UNBOX, 5.5, 9.0), ('bild', HLB_KLAR, 2.2, 1.0, 1.06)],
         [(0, 2.4, ['POV: your sunnozy', 'order has arrived'], '📦', TOP, B), (2.4, 5.6, ['a little sunshine', 'is on its way'], '☀️', LOW, B),
          (5.6, 8.6, ['packed with love.'], None, LOW, B), (8.6, None, ['thank you for', 'choosing sunnozy'], '🤍', LOW, B)], SHOPKARTE(HLB_KLAR, '«Hello Little Bear»'))


def reel09():
    reel(9, 'something_cute_coming', [('bild', TEIL('best_family', 'body'), 1.6, 2.4, 2.8, 0.5, 0.42), ('bild', TEIL('prinzessin_krone', 'kapuzentuch'), 1.6, 2.2, 2.6, 0.5, 0.35),
                                      ('bild', TEIL('wal_blau', 'laetzchen'), 1.6, 1.2, 1.35), ('produkt', FRE('hase_rosa'), 1.8, BLUSH), ('produkt', FRE('best_family'), 1.8, BEIGE)],
         [(0, 2.0, ['something cute', 'is coming…'], '👀', TOP, B), (2.0, 4.0, ['new little favourites.'], None, LOW, B),
          (4.0, 6.2, ['new designs.'], None, LOW, B), (6.2, None, ['coming soon. stay tuned!'], '✨', LOW, B)],
         (mw.HAUPT('best_family'), 'new designs', 'coming soon', CS_AUFRUF))


def reel10():
    teile = [('erstausstattung-set-princess', BLUSH), ('erstausstattung-set-hello-little-bear', BEIGE), ('baby-langarm-body-3er-set-ripp-lovely-little-girl-lila-rosa', LILA),
             ('erstausstattung-set-little-and-loved', BLUSH), ('erstausstattung-set-hello-world', BEIGE)]
    reel(10, 'wardrobe_goals', [('produkt', KLAR(t), 1.5, bg) for t, bg in teile] + [('raster', [KLAR(t) for t, _ in teile[:4]], 2.4, CREME)],
         [(0, 2.4, ["tell me you're obsessed", 'with baby clothes', 'without telling me…'], '😍', TOP, B), (2.4, 4.4, ['tiny wardrobe.'], None, LOW, B),
          (4.4, 6.6, ['endless cuteness.'], None, LOW, B), (6.6, None, ['pink, beige or lilac?'], '👇', 1700, B)],
         SHOPKARTE(PRIN_KLAR, 'baby wardrobe goals', 'pink · beige · lilac'), blende=0.15)


def reel11():
    reel(11, 'newborn_essentials', [('produkt', KLAR('body-set-little-one-gerippt'), 2.0, CREME, 'bodysuits'),
                                    ('produkt', TEIL('little_bear', 'strampler'), 2.0, BEIGE, 'sleepsuits'),
                                    ('produkt', TEIL('little_bear', 'muetze'), 1.8, BLUSH, 'hats & mittens'),
                                    ('produkt', KLAR('baby-soeckchen-5er-set-pastell-umschlag'), 1.8, CREME, 'socks'),
                                    ('produkt', KLAR('mulltuecher-3er-set-musselin'), 2.0, BEIGE, 'muslin cloths')],
         [(0, 2.2, ['getting ready for your', 'little one? save this!'], '🤍', TOP, B), (2.2, None, ['newborn essentials'], '☀️', TOP, B)],
         SHOPKARTE(HLB_KLAR, 'newborn essentials', 'bodysuits · sleepsuits · socks'))


def reel12():
    reel(12, 'small_business_dream', [('clip', HAENDE2, 0.0, 3.5), ('clip', HAENDE3, 4.0, 7.0), ('breit', BOX_B, 1.0, 5.0), ('bild', BOXF('mum_dad_me'), 2.0, 1.0, 1.06)],
         [(0, 2.4, ['behind every small', 'business is a big dream'], '☀️', TOP, B), (2.4, 5.2, ['a small baby shop', 'based in Switzerland'], '🇨🇭', LOW, B),
          (5.2, 8.6, ['every order means', 'so much'], None, LOW, B), (8.6, None, ['thank you for', 'supporting sunnozy'], '🤍', LOW, B)], SUNNOZY)


def reel13():
    reel(13, 'cutest_gift_box', [('bild', BOXF('lovely_little_girl'), 2.2, 1.0, 1.08), ('breit', BOX_A, 5.0, 9.0),
                                 ('produkt', WEISS('lovely_langarm3'), 1.6, LILA, '3 bodysuits'), ('produkt', WEISS('leggings5'), 1.6, BLUSH, '5 leggings with bows'),
                                 ('bild', BOXF('lovely_little_girl'), 2.2, 1.12, 1.2)],
         [(0, 2.2, ['stop scrolling if you', 'love baby gifts!'], '🎀', TOP, B), (2.2, 6.0, ['a gift full of love.'], None, LOW, B),
          (6.0, 9.0, ['for the sweetest', 'little moments'], None, LOW, B), (9.0, None, ['baby gifting', 'made special'], '🤍', LOW, B)],
         SHOPKARTE(BOXF('lovely_little_girl'), 'gift box «Lovely Little Girl»', '3 bodysuits + 5 leggings'))


def reel14():
    alle = ['body-set-dinosaur-kurzarm-5er-pack', 'baby-kurzarm-body-5er-set-sommer-sweet-friends-rosa-mint', 'body-set-i-love-hugs-aermellos', 'baby-jogginghose-5er-set-ripp-pastell-mit-schleife']
    reel(14, 'expectation_reality', [('produkt', KLAR('body-set-little-one-gerippt'), 2.4, CREME, 'expectation')]
         + [('produkt', KLAR(t), 0.8, [BLUSH, BEIGE, LILA, CREME][k]) for k, t in enumerate(alle)]
         + [('raster', [KLAR(t) for t in ['body-set-little-one-gerippt'] + alle], 3.0, CREME, ['reality'])],
         [(0, 2.4, ["expectation: I won't buy", 'more baby clothes'], None, TOP, B), (2.4, 3.6, ["I don't need more."], None, TOP, B),
          (3.6, 5.0, ['just one more.'], None, TOP, B), (5.0, None, ['okay, maybe five more'], '😂', TOP, B)],
         SHOPKARTE(KLAR('body-set-little-one-gerippt'), 'bodysuit sets', '3-packs and 5-packs'), blende=0.12)


def reel15():
    reel(15, 'sunday_reset', [('clip', HAENDE3, 0.0, 3.0), ('clip', HAENDE1, 3.5, 6.5), ('clip', SWADDLE, 1.0, 4.0), ('produkt', KLAR('body-set-little-love-rosa'), 2.2, BLUSH)],
         [(0, 2.4, ["a little sunday reset for", "your baby's wardrobe"], '🤍', TOP, B), (2.4, 4.6, ['reset.'], None, LOW, B), (4.6, 7.0, ['organize.'], None, LOW, B),
          (7.0, 9.2, ['fold with love.'], None, LOW, B), (9.2, None, ['ready for a new week'], '☀️', LOW, B)], SUNNOZY)


# ---------------- Woche 3: Community, Trends & Viralität ----------------
def reel16():
    teile = ['baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen', 'baby-langarm-body-3er-set-i-like-flying-vogelchen-eis-rosa', 'baby-langarm-body-5er-set-ripp-pastell-mum-dad-me-lila-blumen', 'erstausstattung-set-princess']
    reel(16, 'just_looking', [('produkt', KLAR(t), 1.6, [BLUSH, CREME, LILA, BEIGE][k]) for k, t in enumerate(teile)] + [('raster', [KLAR(t) for t in teile], 2.4, CREME)],
         [(0, 2.2, ["me: I don't need anything.", 'also me:'], '😍', TOP, B), (2.2, 3.8, ["I'm just looking."], None, LOW, B),
          (3.8, 5.4, ['wait, this is adorable.'], None, LOW, B), (5.4, None, ['add to cart!'], '🛒', 1700, B)], SHOPKARTE(PRIN_KLAR, 'little favourites', 'leggings · bodysuits · newborn sets'), blende=0.15)


def reel17():
    reel(17, 'this_or_that', [('produkt', FRE('rosa_A'), 1.8, BLUSH, 'pink'), ('produkt', FRE('little_bear'), 1.8, BEIGE, 'beige'),
                              ('produkt', KLAR('baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen'), 1.8, LILA, 'floral'),
                              ('produkt', KLAR('body-set-little-one-gerippt'), 1.8, CREME, 'minimal')],
         [(0, 2.0, ["let's play", 'THIS or THAT!'], '🎀', TOP, B), (2.0, 3.6, ['pink or beige?'], None, TOP, B), (3.6, 5.6, ['floral or minimal?'], None, TOP, B),
          (5.6, None, ['your choice!'], '👇', TOP, B)], SHOPKARTE(PRIN_KLAR, 'this or that?', 'tell us in the comments'), blende=0.15)


def reel18():
    reel(18, 'tiny_details', [('bild', TEIL('rosa', 'body'), 2.0, 2.2, 2.5, 0.5, 0.2), ('bild', TEIL('hello_world_blatt', 'strampler'), 1.8, 2.4, 2.7, 0.5, 0.4),
                              ('bild', TEIL('little_and_loved_gans_rosa', 'body'), 1.8, 2.0, 2.3, 0.5, 0.45), ('produkt', FRE('hello_world_blatt'), 2.2, CREME)],
         [(0, 2.0, ['POV: you notice all', 'the little details'], '✨', TOP, B), (2.0, 3.8, ['the fabric.'], None, LOW, B), (3.8, 5.6, ['the details.'], None, LOW, B),
          (5.6, None, ['simply adorable.'], '🤍', LOW, B)], SHOPKARTE(HW_KLAR, '«Hello World»'))


def reel19():
    reel(19, 'waiting_mama', [('produkt', TEIL('little_bear', 'muetze'), 2.0, CREME), ('produkt', TEIL('little_bear', 'strampler'), 2.0, BEIGE),
                              ('clip', HAENDE1, 4.0, 7.0), ('bild', BOXF('i_love_my_mummy'), 2.4, 1.0, 1.08)],
         [(0, 2.4, ['to every mama waiting', 'to meet her little miracle'], '🤍', TOP, B), (2.4, 4.4, ['soon, little one.'], None, LOW, B),
          (4.4, 7.4, ['your tiny world is', 'about to change'], None, LOW, B), (7.4, None, ['the sweetest chapter', 'begins'], '☀️', LOW, B)], SUNNOZY)


def reel20():
    reel(20, 'rate_the_outfit', [('bild', PRIN_KLAR, 2.4, 1.0, 1.08), ('bild', TEIL('rosa', 'strampler'), 1.8, 1.8, 2.1, 0.5, 0.3), ('clip', PRIN_BABY, 1.0, 4.0)],
         [(0, 2.4, ['rate this baby outfit', 'from 1 to 10!'], '😍', TOP, B), (2.4, 4.2, ['cute details.'], None, LOW, B), (4.2, None, ['rate it: 1–10'], '👇', LOW, B)],
         SHOPKARTE(PRIN_KLAR, '«Princess»'))


def reel21():
    reel(21, 'pack_with_me', [('clip', HAENDE2, 0.0, 3.0), ('breit', BOX_B, 0.5, 4.5), ('breit', BOX_A, 6.0, 9.5), ('bild', BOXF('i_love_my_mummy'), 2.0, 1.0, 1.06)],
         [(0, 2.4, ['pack something special', 'with me'], '☀️', TOP, B), (2.4, 6.2, ['one little gift.'], None, LOW, B),
          (6.2, 9.4, ['packed with love.'], None, LOW, B), (9.4, None, ['ready to make', 'someone smile'], '🤍', LOW, B)],
         SHOPKARTE(BOXF('i_love_my_mummy'), 'gift box «I love my Mummy»', '3 bodysuits + 3 bandana bibs'))


def reel22():
    reel(22, 'folded_to_fabulous', [('bild', HLB_KLAR, 2.4, 1.0, 1.06), ('clip', HLB_BABY, 1.0, 4.0), ('clip', HLB_BABY, 6.0, 8.5)],
         [(0, 2.2, ['from folded', 'to fabulous!'], '✨', TOP, B), (0.6, 2.2, ['before.'], None, LOW, B), (2.4, 4.6, ['after!'], '😍', LOW, B)],
         SHOPKARTE(HLB_KLAR, '«Hello Little Bear»'))


def reel23():
    reel(23, 'only_moms_understand', [('raster', [KLAR(t) for t in ['body-set-little-love-rosa', 'body-set-dinosaur-kurzarm-5er-pack', 'baby-leggings-5er-set-ripp-pastell-mit-schleife-rosa-blumen', 'baby-kurzarm-body-5er-set-pastell-i-love-my-mum']], 3.0, CREME),
                                      ('clip', HAENDE3, 1.0, 4.0), ('clip', PRIN_BABY, 3.5, 6.5)],
         [(0, 1.8, ['only moms will understand', 'these 3 things'], '😂', TOP, B), (1.8, 3.6, ['1. buying clothes faster', 'than baby grows'], None, LOW, B),
          (3.6, 6.4, ['2. laundry every', 'single day'], None, LOW, B), (6.4, None, ['3. 100 photos of', 'one outfit'], '📸', LOW, B)], SUNNOZY)


def reel24():
    teile = ['body-set-little-one-gerippt', 'erstausstattung-set-hello-little-bear', 'baby-soeckchen-5er-set-neutral-umschlag', 'mulltuecher-3er-set-musselin']
    reel(24, 'first_wardrobe', [('produkt', KLAR(t), 1.8, [CREME, BEIGE, BLUSH, CREME][k]) for k, t in enumerate(teile)] + [('raster', [KLAR(t) for t in teile], 2.6, CREME)],
         [(0, 2.4, ['creating the cutest', 'little wardrobe for', 'your newborn'], '🤍', TOP, B), (2.4, 4.2, ['little essentials.'], None, LOW, B),
          (4.2, 6.0, ['soft colours.'], None, LOW, B), (6.0, None, ['ready for baby'], '☀️', 1700, B)], SHOPKARTE(HLB_KLAR, 'first wardrobe', 'newborn essentials'), blende=0.15)


# ---------------- Woche 4: Kaufanreize & Wiedererkennung ----------------
def reel25():
    reel(25, 'new_favourite', [('bild', LAL_KLAR, 2.2, 1.0, 1.06), ('bild', TEIL('little_and_loved_gans_rosa', 'body'), 2.0, 1.8, 2.1, 0.5, 0.45),
                               ('produkt', FRE('little_and_loved_gans_rosa'), 2.2, BLUSH, '«Little and Loved» · 8 pieces')],
         [(0, 2.2, ["your baby's next favourite", 'outfit is waiting'], '🎀', TOP, B), (2.2, 4.2, ['cute? absolutely.'], None, TOP, B),
          (4.2, None, ['100% soft cotton.'], '🤍', TOP, B)], SHOPKARTE(LAL_KLAR, '«Little and Loved»'))


def reel26():
    reel(26, 'newborn_gift', [('bild', BOXF('mum_dad_me'), 2.4, 1.0, 1.08), ('produkt', WEISS('mumdadme_langarm5'), 1.8, LILA, '5 bodysuits «Mum Dad Me»'),
                              ('produkt', WEISS('leggings5'), 1.8, BLUSH, '5 leggings with bows'), ('bild', BOXF('mum_dad_me'), 2.4, 1.15, 1.25)],
         [(0, 2.4, ['one of the sweetest gifts', 'for a newborn baby'], '🎁', TOP, B), (2.4, 5.6, ['for a little miracle.'], None, TOP, B),
          (5.6, None, ['a thoughtful little gift'], '🤍', TOP, B)], SHOPKARTE(BOXF('mum_dad_me'), 'gift box «Mum Dad Me»', '5 bodysuits + 5 leggings'))


def reel27():
    reel(27, 'piece_of_childhood', [('clip', PRIN_BABY, 0.5, 3.2), ('bild', TEIL('rosa', 'body'), 2.0, 1.4, 1.6), ('clip', HLB_BABY, 4.0, 7.0), ('clip', PRIN_BABY, 6.5, 9.3)],
         [(0, 2.4, ["it's not just baby clothes.", "it's a little piece", 'of childhood'], '🥹', TOP, B), (2.4, 4.4, ['little outfits.'], None, LOW, B),
          (4.4, 7.2, ['little memories.'], None, LOW, B), (7.2, None, ["big love. that's sunnozy"], '☀️', LOW, B)], SUNNOZY)


def reel28():
    reel(28, 'discovered_sunnozy', [('produkt', FRE('little_bear'), 1.6, BEIGE), ('produkt', FRE('rosa_A'), 1.6, BLUSH), ('clip', HAENDE1, 0.0, 3.0),
                                    ('clip', HLB_BABY, 4.0, 6.6), ('bild', BOXF('growing_up_strong'), 2.0, 1.0, 1.06)],
         [(0, 2.4, ['swiss mamas, have you', 'discovered sunnozy yet?'], '🇨🇭', TOP, B), (2.4, 4.6, ['a small baby shop', 'based in Switzerland'], None, LOW, B),
          (4.6, 7.4, ['cute baby styles.'], None, LOW, B), (7.4, None, ['gift ideas. shipped', 'from Switzerland'], '🤍', LOW, B)], SUNNOZY)


def reel29():
    reel(29, 'before_you_scroll', [('clip', PRIN_BABY, 0.5, 3.3), ('bild', TEIL('rosa', 'body'), 1.8, 2.0, 2.3, 0.5, 0.25), ('clip', PRIN_BABY, 6.5, 9.0), ('bild', PRIN_KLAR, 2.0, 1.0, 1.05)],
         [(0, 2.4, ['before you scroll…', 'look at this little cutie!'], '😍', TOP, B), (2.4, 4.6, ['too cute to scroll.'], None, LOW, B),
          (4.6, 7.2, ['little sunshine.'], '☀️', LOW, B), (7.2, None, ['find your favourite'], '🤍', LOW, B)], SHOPKARTE(PRIN_KLAR, '«Princess»'))


def reel30():
    reel(30, 'thank_you_community', [('produkt', FRE('little_and_loved_gans_rosa'), 1.6, BLUSH), ('clip', HAENDE3, 0.0, 3.0), ('breit', BOX_B, 1.0, 4.5), ('bild', HLB_KLAR, 2.0, 1.0, 1.05)],
         [(0, 2.4, ['every little order means', 'the world to us'], '🤍', TOP, B), (2.4, 4.6, ['a small shop.'], None, LOW, B),
          (4.6, 7.2, ['a big dream.'], None, LOW, B), (7.2, None, ['thank you for being', 'part of sunnozy'], '☀️', LOW, B)], SUNNOZY)


REELS = [globals()[f'reel{i:02d}'] for i in range(1, 31)]


# ---------------- Posts (4:5) und Storys (9:16) ----------------
def band(c, zeilen, y, g=58, emo=None):
    e = mw.band_ebene(zeilen, emo, y, g)
    if c.size != (W, H):
        e = e.crop((0, 0, c.width, c.height)) if c.height <= H else e
    c.alpha_composite(e.crop((0, 0) + c.size))


def speichern(c, ordner, name):
    o = os.path.join(OUT, ordner); os.makedirs(o, exist_ok=True)
    c.convert('RGB').save(os.path.join(o, name + '.jpg'), quality=93); print(name, flush=True)


def bilder():
    # Post 1: Markenbotschaft
    c = mw.leinwand('4x5', CREME); c.alpha_composite(mw.fuellen(mw.still(PRIN_BABY, 1.5), 1080, 1050, 0.5, 0.42).convert('RGBA'), (0, 0))
    mw.text(c, ['little outfits, big love'], 1135, 50, mw.DUNKEL, '☀️'); mw.logo(c, 1210, 200); speichern(c, 'posts', 'post01_little_outfits_big_love')
    # Post 2: Karussell «newborn essentials» (zum Speichern)
    folien = [('newborn essentials', 'save this for your hospital bag list', None),
              ('bodysuits', 'easy to change, soft on the skin', KLAR('body-set-little-one-gerippt')),
              ('sleepsuits', 'with feet, zip or snaps', TEIL('little_bear', 'strampler')),
              ('hats & mittens', 'for the very first days', TEIL('little_bear', 'muetze')),
              ('socks', 'tiny feet stay cosy', KLAR('baby-soeckchen-5er-set-pastell-umschlag')),
              ('muslin cloths', 'for burps, cuddles and more', KLAR('mulltuecher-3er-set-musselin'))]
    for k, (titel, unter, bild) in enumerate(folien, 1):
        c = mw.leinwand('4x5', BLUSH if k % 2 else CREME)
        if bild:
            mw.karte(c, bild, 540, 620, 820, 820); mw.text(c, [f'{k - 1}/5  {titel}'], 1130, 52, mw.DUNKEL); mw.text(c, [unter], 1210, 32, mw.GRAU)
        else:
            mw.text(c, ['newborn', 'essentials'], 520, 96, mw.DUNKEL, '☀️'); mw.text(c, [unter], 800, 36, mw.GRAU); mw.text(c, ['swipe for more'], 1150, 34, mw.GRAU)
            mw.logo(c, 1230, 200)
        speichern(c, 'posts', f'post02_essentials_{k}')
    # Post 3: Geschenk
    c = mw.leinwand('4x5', CREME); mw.karte(c, BOXF('i_love_my_mummy'), 540, 600, 900, 900)
    mw.text(c, ['a little gift. a lot of love.'], 1130, 46, mw.DUNKEL, '🎁'); mw.text(c, ['gift box «I love my Mummy» · link in bio'], 1210, 30, mw.GRAU)
    speichern(c, 'posts', 'post03_gift')
    # Post 4: This or that
    c = mw.leinwand('4x5', CREME)
    c.alpha_composite(Image.new('RGBA', (520, 900), BLUSH + (255,)), (20, 160)); c.alpha_composite(Image.new('RGBA', (520, 900), BEIGE + (255,)), (540, 160))
    mw.karte(c, FRE('rosa_A'), 280, 600, 470, 600, schatten=False); mw.karte(c, FRE('little_bear'), 800, 600, 470, 600, schatten=False)
    mw.text(c, ['pink'], 1000, 44, mw.DUNKEL, x=200); mw.text(c, ['beige'], 1000, 44, mw.DUNKEL, x=700)
    mw.text(c, ['this or that?'], 95, 56, mw.DUNKEL, '🎀'); mw.text(c, ['tell us in the comments'], 1150, 36, mw.GRAU); mw.logo(c, 1230, 180)
    speichern(c, 'posts', 'post04_this_or_that')
    # Post 5: Vorstellung
    c = mw.leinwand('4x5', BLUSH)
    for k, b in enumerate([HLB_KLAR, PRIN_KLAR, LAL_KLAR, BOXF('i_love_my_mummy')]):
        c.alpha_composite(mw.fuellen(mw.laden(b), 460, 400).convert('RGBA'), (70 + (k % 2) * 480, 110 + (k // 2) * 430))
    mw.text(c, ['hi, we are sunnozy'], 1020, 56, mw.DUNKEL, '☀️'); mw.text(c, ['a small baby shop based in Switzerland', 'newborn sets · bodysuits · gift boxes'], 1110, 30, mw.GRAU)
    mw.logo(c, 1220, 190); speichern(c, 'posts', 'post05_hi_we_are_sunnozy')
    # Post 6: Danke
    c = mw.leinwand('4x5', CREME); mw.karte(c, HLB_KLAR, 540, 520, 720, 720)
    mw.text(c, ['thank you'], 1000, 80, mw.DUNKEL, '☀️'); mw.text(c, ['for every like, share and order.', 'you are our sunshine.'], 1110, 34, mw.DUNKEL)
    mw.logo(c, 1230, 190); speichern(c, 'posts', 'post06_thank_you')
    # Storys
    c = mw.leinwand('9x16', CREME)
    c.alpha_composite(Image.new('RGBA', (W, 820), BLUSH + (255,)), (0, 180)); c.alpha_composite(Image.new('RGBA', (W, 820), BEIGE + (255,)), (0, 1000))
    mw.karte(c, FRE('rosa_A'), W / 2, 590, 700, 640, schatten=False); mw.karte(c, FRE('little_bear'), W / 2, 1410, 700, 640, schatten=False)
    mw.text(c, ['pink or beige?'], 110, 60, mw.DUNKEL, '🎀'); mw.text(c, ['(add the poll sticker here)'], 1000, 30, mw.GRAU)
    speichern(c, 'storys', 'story01_poll_pink_beige')
    c = mw.leinwand('9x16', BLUSH); mw.karte(c, PRIN_KLAR, W / 2, 900, 900, 900)
    mw.text(c, ['rate this outfit', 'from 1 to 10'], 260, 60, mw.DUNKEL, '😍'); mw.text(c, ['(add the emoji slider here)'], 1500, 30, mw.GRAU)
    mw.text(c, ['«Princess» · link in bio'], 1640, 38, mw.GRAU); speichern(c, 'storys', 'story02_rate_outfit')
    c = mw.leinwand('9x16', CREME)
    for k, b in enumerate([KLAR('body-set-little-one-gerippt'), TEIL('little_bear', 'strampler'), TEIL('little_bear', 'muetze'), KLAR('mulltuecher-3er-set-musselin')]):
        c.alpha_composite(mw.einpassen(mw.laden(b), 440, 440).convert('RGBA'), (80 + (k % 2) * 480, 560 + (k // 2) * 480))
    mw.text(c, ["what's in your", 'hospital bag?'], 250, 60, mw.DUNKEL, '🤍'); mw.text(c, ['(add the question sticker here)'], 1620, 30, mw.GRAU)
    speichern(c, 'storys', 'story03_hospital_bag')


if __name__ == '__main__':
    wahl = sys.argv[1:] or ['bilder'] + [f'reel{i:02d}' for i in range(1, 31)]
    for w in wahl:
        globals()[w]() if w != 'bilder' else bilder()
