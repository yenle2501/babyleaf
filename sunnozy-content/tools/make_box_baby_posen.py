"""Babyfotos in der Box-Kleidung, wach, verschiedene Posen, Body und Hose Ton in Ton (05.11.2026).

    python3 tools/make_box_baby_posen.py <png-ordner>

Quelle: KI-Bilder (Canva, fiktive Babys) 1080 × 1920, Dateiname <box>_<farbe>_<pose>.png.
Referenz pro Bild: vorlagen-shopify/<name>.jpg (Body links, Hose rechts, aus den Shopify-Einzelbildern).
Ausgabe: posts/kampagne-weihnachtsbox/baby-in-box-kleidung/<name>_9x16.jpg und _4x5.jpg (1080 × 1350),
dazu uebersicht_<box>.jpg pro Box.
"""
import os, sys, glob
from PIL import Image, ImageFilter, ImageDraw
import make_coming_soon_reels as m

OUT = os.path.join(m.POSTS, 'kampagne-weihnachtsbox', 'baby-in-box-kleidung')
VORLAGEN = os.path.join(OUT, 'vorlagen-shopify')        # Body + Hose aus den Shopify-Einzelbildern, Referenz für die KI
BOXEN = ['mum_dad_me', 'lovely_little_girl', 'growing_up_strong', 'dinosaur', 'i_like_flying', 'little_one_jogginghosen',
         'dino', 'i_love_my_mummy', 'little_one', 'body']   # body = einzelne Body-Sets (nicht Box)


def anzeige(t):
    for a, b in (('bluemchen', 'blümchen'), ('fuesse', 'füsse'), ('gruen', 'grün'), ('glace', 'glacé')):
        t = t.replace(a, b)
    return t.replace('_', ' ')


def box_von(name):
    return next(b for b in BOXEN if name.startswith(b + '_'))


def main(src):
    gruppen = {}
    for p in sorted(glob.glob(os.path.join(src, '*.png'))):
        k = os.path.splitext(os.path.basename(p))[0]
        im = Image.open(p).convert('RGB')
        if im.size != (1080, 1920):
            im = im.resize((1080, 1920), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
        im.save(os.path.join(OUT, f'{k}_9x16.jpg'), quality=93)
        y = int((im.height - 1350) * 0.4)
        im.crop((0, y, 1080, y + 1350)).save(os.path.join(OUT, f'{k}_4x5.jpg'), quality=93)
        gruppen.setdefault(box_von(k), []).append((k, im))
        print(k)
    for box, bilder in gruppen.items():
        tw, th, rh = 300, 533, 169                         # unter jedem Foto die Shopify-Vorlage (Body + Hose)
        c = Image.new('RGB', (tw * len(bilder), th + 46 + rh), m.CREME); d = ImageDraw.Draw(c)
        for i, (k, im) in enumerate(bilder):
            c.paste(im.resize((tw, th), Image.LANCZOS), (i * tw, 0))
            d.text((i * tw + tw / 2, th + 23), anzeige(k[len(box) + 1:]), font=m.f(m.SERIF_I, 26), fill=m.GRAU, anchor='mm')
            v = os.path.join(VORLAGEN, k + '.jpg')
            if os.path.exists(v):
                c.paste(Image.open(v).convert('RGB').resize((tw, rh), Image.LANCZOS), (i * tw, th + 46))
        c.save(os.path.join(OUT, f'uebersicht_{box}.jpg'), quality=90)
        print('uebersicht', box)


if __name__ == '__main__':
    main(sys.argv[1])
