"""Content-Plan KW 46 (10.–16.11.2026): Karussell-Folien und Story-Umfrage aus vorhandenen Bildern.

    python3 tools/make_content_plan_kw1.py      # schreibt nach posts/content-plan/kw1/

Plan und Captions: posts/content-plan/kw1/README.md. Nur vorhandene Fotos, nichts neu generiert.
Design wie KW 45 (make_kw1/make_kw2): Titel Fraunces, Text Nunito Sans, Creme-Grund, Infos nur auf der letzten Folie.
"""
import os, shutil
from PIL import Image, ImageDraw
import make_kw1 as k

P = k.POSTS
OUT = os.path.join(P, 'content-plan', 'kw1')
PROD = os.path.join(P, 'instagram', 'produkte')
SETS = os.path.join(P, 'coming-soon', 'photos', 'meta-ads-erstausstattung', 'quelle')
BABY = os.path.join(P, 'baby-photos')
CS = os.path.join(P, 'coming-soon', 'photos')


def auf_4x5(pfad):
    im = Image.open(pfad).convert('RGB'); w, h = im.size
    if w / h > 0.8:
        nw = int(h * 0.8); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / 0.8); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize((k.FW, k.FH), Image.LANCZOS)


def endfolie(name, zeile, set_bild, fussnote='Link in der Bio · sunnozy.ch'):
    """Letzte Folie: Set komplett, Name, Inhalt und Preis, Logo."""
    c = Image.new('RGB', (k.FW, k.FH), k.CREME); d = ImageDraw.Draw(c)
    d.text((k.FW / 2, 110), name, font=k.f('fraunces-600.ttf', 68), fill=k.WALD, anchor='mm')
    d.text((k.FW / 2, 185), zeile, font=k.f('nunitosans-700.ttf', 34), fill=k.SALBEI, anchor='mm')
    k.karte(c, k.ohne_shoplogo(Image.open(set_bild).convert('RGB')), (k.FW / 2, 700), 820, 820)
    L = k.logo(240); c.paste(L, ((k.FW - L.width) // 2, 1180), L)
    d.text((k.FW / 2, 1275), fussnote, font=k.f('nunitosans-600.ttf', 30), fill=k.GRAU, anchor='mm')
    return c


def karussell(prefix, folien, end):
    for i, quelle in enumerate(folien, 1):
        ziel = os.path.join(OUT, f'{prefix}_{i}.jpg')
        if isinstance(quelle, str) and quelle.endswith('_4x5'):
            auf_4x5(quelle[:-4]).save(ziel, quality=94)
        else:
            shutil.copy(quelle, ziel)
    end.save(os.path.join(OUT, f'{prefix}_{len(folien) + 1}.jpg'), quality=94)


def story_umfrage():
    c = k.story_grund(['Was soll als', 'Nächstes kommen?'], 'Stimm ab, Du entscheidest mit', oben=260)
    d = ImageDraw.Draw(c)
    for j, (name, pfad) in enumerate([('Segelboote', 'strampler-segelboote'), ('Kirschen', 'strampler-kirschen')]):
        x = k.SW / 2 + (j - 0.5) * 500
        im = Image.open(os.path.join(CS, pfad, 'shop', f'{pfad}_shop_ohne_logo.jpg')).convert('RGB')
        box = k.karte(c, im, (x, 860), 460, 620)
        d.text((x, box[3] + 60), name, font=k.f('fraunces-600.ttf', 48), fill=k.WALD, anchor='mm')
    # y 1350–1600 bleibt frei für den Umfrage-Sticker
    L = k.logo(200); c.paste(L, ((k.SW - L.width) // 2, 1720), L)
    c.save(os.path.join(OUT, 'di_story_umfrage.jpg'), quality=93)


def main():
    os.makedirs(OUT, exist_ok=True)
    lal = os.path.join(PROD, 'little-and-loved')
    karussell('mo_karussell_little_and_loved',
              [f'{lal}/{n}.jpg' for n in ('1_baby', '2_kragen', '3_aermel', '4_fuss', '5_flatlay')],
              endfolie('Little and Loved', '8 Teile · 100 % Baumwolle · CHF 30.40', f'{SETS}/erstausstattung-set-little-and-loved.jpg'))
    hw = os.path.join(PROD, 'hello-world')
    karussell('do_karussell_hello_world',
              [f'{hw}/1_baby.jpg', f'{hw}/2_kragen.jpg', f'{BABY}/baby_echt_erstausstattung_hello_world.jpg_4x5'],
              endfolie('Hello World', '8 Teile · 100 % Baumwolle · CHF 29.40', f'{SETS}/erstausstattung-set-hello-world.jpg'))
    pr = os.path.join(PROD, 'princess')
    karussell('sa_karussell_princess',
              [f'{pr}/1_baby.jpg', f'{BABY}/baby_echt_erstausstattung_princess.jpg_4x5'],
              endfolie('Princess', '8 Teile · 100 % Baumwolle · CHF 30.40', f'{SETS}/erstausstattung-set-princess.jpg'))
    story_umfrage()
    print('fertig:', sorted(os.listdir(OUT)))


if __name__ == '__main__':
    main()
