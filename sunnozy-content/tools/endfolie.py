"""Endfolie für Reels (Regel der Nutzerin ab 17.11.2026: jedes Reel hat eine Endfolie).

Hängt an ein fertiges Reel eine 2,6-s-Endfolie an, mit 0,4 s Überblendung. Danach wird die Standardmusik über die neue
Länge gelegt. Die Endfolie ist eine Creme-Fläche mit:
  - Set-Bild als Karte
  - Name in Schreibmaschinenschrift
  - Zeile darunter (z.B. «Erstausstattung · 5 Teile» oder «coming soon»)
  - Aufruf («Link in der Bio» oder «Folg uns, damit Du es nicht verpasst»)
  - sunnozy-Logo
Kein Preis: Bei Coming soon ist er verboten, bei Shop-Produkten steht er in der Caption, bei «PREIS»-Reels in der DM.

Bereits bearbeitete Reels tragen das Metadaten-Tag comment=endfolie und werden nicht doppelt bearbeitet.

    python3 tools/endfolie.py                 # alle Reels in REELS (unten), die noch keine Endfolie haben
    python3 tools/endfolie.py <reel.mp4> ...  # nur diese (müssen in REELS stehen)
In neuen Reel-Skripten: from endfolie import anhaengen; anhaengen(pfad, set_bild, name, zeile, aufruf)
"""
import os, sys, subprocess, tempfile, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, 30
P = m.POSTS
CS = os.path.join(P, 'coming-soon', 'photos')
SET = os.path.join(CS, 'produktfotos-set-praesentation', 'ohne_logo')
QUELLE = os.path.join(CS, 'meta-ads-erstausstattung', 'quelle')
BOX = os.path.join(CS, 'kampagne-weihnachtsbox', 'fotos')
MUSIK = os.path.join(P, 'coming-soon', 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
CREME, DUNKEL, GRAU = (250, 246, 240), (60, 52, 46), (120, 105, 95)
DAUER, BLENDE = 2.6, 0.4
SHOP, CS_AUFRUF = 'Link in der Bio · sunnozy.ch', 'Folg uns, damit Du es nicht verpasst'


def f(g):
    return ImageFont.truetype(SCHRIFT, g)


def ohne_shoplogo(im):
    w, h = im.size; r = int(h * 0.075)
    return im.crop((r, r, w - r, h - r))


def bild_laden(spez):
    """spez: Pfad, oder (Pfad, 'ohne_logo') für Shop-Bilder mit Logo oben links, oder (Video, Sekunde) für ein Standbild."""
    if isinstance(spez, tuple) and spez[0].endswith('.mp4'):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(spez[1]), '-i', spez[0], '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                             capture_output=True, check=True).stdout
        import io
        return Image.open(io.BytesIO(raw)).convert('RGB')
    if isinstance(spez, tuple):
        return ohne_shoplogo(Image.open(spez[0]).convert('RGB'))
    return Image.open(spez).convert('RGB')


def karte(set_bild, name, zeile, aufruf):
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    im = bild_laden(set_bild); s = min(880 / im.width, 900 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (W - im.width) // 2, 760 - im.height // 2
    sch = Image.new('L', (im.width + 80, im.height + 80), 0); ImageDraw.Draw(sch).rectangle((40, 40, im.width + 40, im.height + 40), fill=60)
    c.paste(Image.new('RGB', sch.size, (210, 200, 188)), (x - 40, y - 26), sch.filter(ImageFilter.GaussianBlur(20)))
    c.paste(im, (x, y))
    g = 64
    while d.textlength(name, font=f(g)) > 960 and g > 40:
        g -= 2
    d.text((W / 2, 1310), name, font=f(g), fill=DUNKEL, anchor='mm')
    d.text((W / 2, 1390), zeile, font=f(38), fill=GRAU, anchor='mm')
    d.text((W / 2, 1470), aufruf, font=f(34), fill=GRAU, anchor='mm')
    L = m.logo(240, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1540), L)
    return c


def hat_endfolie(pfad):
    tags = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format_tags', '-of', 'json', pfad],
                                     capture_output=True, text=True).stdout).get('format', {}).get('tags', {})
    return tags.get('comment') == 'endfolie'


def anhaengen(pfad, set_bild, name, zeile, aufruf=SHOP):
    if hat_endfolie(pfad):
        print(f'schon mit Endfolie: {os.path.basename(pfad)}'); return
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', pfad],
                             capture_output=True, text=True).stdout.strip())
    gesamt = d + DAUER - BLENDE
    with tempfile.TemporaryDirectory() as td:
        kp = os.path.join(td, 'karte.png'); karte(set_bild, name, zeile, aufruf).save(kp)
        out = os.path.join(td, 'out.mp4')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', pfad, '-loop', '1', '-framerate', str(FPS), '-t', str(DAUER), '-i', kp, '-i', MUSIK,
                        '-filter_complex',
                        f'[0:v]fps={FPS},scale={W}:{H},setsar=1,format=yuv420p[a];[1:v]fps={FPS},scale={W}:{H},setsar=1,format=yuv420p[b];'
                        f'[a][b]xfade=transition=fade:duration={BLENDE}:offset={d - BLENDE:.3f}[v];'
                        f'[2:a]atrim=0:{gesamt:.3f},afade=t=in:d=0.3,afade=t=out:st={gesamt - 1.2:.3f}:d=1.2,volume=1.4,alimiter=limit=0.89[au]',
                        '-map', '[v]', '-map', '[au]', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '160k', '-metadata', 'comment=endfolie', '-movflags', '+faststart', out], check=True)
        os.replace(out, pfad)
    print(f'{os.path.basename(pfad)}: {d:.1f} s -> {gesamt:.1f} s')


R = os.path.join(P, 'coming-soon', 'reels')
K1, K2 = os.path.join(P, 'content-kw1', 'reels'), os.path.join(P, 'content-kw2', 'reels')
V = os.path.join(P, 'content-kw2', 'viral')
HLB = (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile')
HW = ((QUELLE + '/erstausstattung-set-hello-world.jpg', 'ohne_logo'), 'Hello World', 'Erstausstattung · 8 Teile')
LAL = ((QUELLE + '/erstausstattung-set-little-and-loved.jpg', 'ohne_logo'), 'Little and Loved', 'Erstausstattung · 8 Teile')
VELOURS = ((os.path.join(R, 'velours', 'original', 'clip_strecken.mp4'), 4.0), 'Strampler «Velours»', 'coming soon', CS_AUFRUF)

REELS = {   # Datei: (Bild, Name, Zeile[, Aufruf])
    f'{K1}/reel_best_family_lachen_9x16.mp4': (SET + '/set_best_family_quadratisch.jpg', 'Best Family', 'coming soon', CS_AUFRUF),
    f'{K1}/reel_kirschen_smile_9x16.mp4': ((CS + '/strampler-kirschen/shop/strampler-kirschen_shop_ohne_logo.jpg'), 'Strampler «Kirschen»', 'coming soon', CS_AUFRUF),
    f'{K1}/reel_born_in_2027_9x16.mp4': ((CS + '/born-in-2027-rosa/shop/born-in-2027-rosa_shop_ohne_logo.jpg'), 'Born in 2027', 'coming soon · Rosa und Hellblau', CS_AUFRUF),
    f'{K2}/reel_little_bear_haende_hoch_9x16.mp4': HLB,
    f'{K2}/reel_hello_world_strecken_9x16.mp4': HW,
    f'{K2}/reel_little_and_loved_morgen_9x16.mp4': LAL,
    f'{K2}/reel_geschenkbox_gotti_9x16.mp4': (BOX + '/box_i_love_my_mummy.jpg', 'Geschenkbox «I love my Mummy»', '3 Bodys + 3 Halstücher, fertig verpackt'),
    f'{V}/reel_strecken_emoji_9x16.mp4': HW,
    f'{V}/reel_gotti_box_was_ist_drin_9x16.mp4': (BOX + '/box_mum_dad_me.jpg', 'Geschenkbox «Mum Dad Me»', 'Preis? Schreib PREIS in die Kommentare', 'Link in der Bio · sunnozy.ch'),
    f'{V}/reel_schleifen_9x16.mp4': (os.path.join(CS, 'shopify-hauptbilder-weiss', 'kombi_lovely.jpg'), 'Alles mit Schleife', 'Leggings · Jogginghosen · Geschenkboxen'),
    f'{R}/hello-little-bear/reel_hello_little_bear_winter_9x16.mp4': HLB,
    f'{R}/hello-little-bear/reel_hello_little_bear_gotti_9x16.mp4': HLB,
    f'{R}/hello-little-bear/reel_hello_little_bear_babyfieber_9x16.mp4': HLB,
    f'{R}/hello-little-bear/reel_hello_little_bear_was-ist-drin_9x16.mp4': HLB[:2] + ('Preis? Schreib PREIS in die Kommentare',),
    f'{R}/hello-spitze/reel_hello_spitze_morgen_9x16.mp4': ((QUELLE + '/erstausstattung-set-hello-spitze.jpg', 'ohne_logo'), 'Hello mit Spitze', 'Erstausstattung · 6 Teile'),
    f'{R}/hello-spitze/reel_hello_spitze_grosi_9x16.mp4': ((QUELLE + '/erstausstattung-set-hello-spitze.jpg', 'ohne_logo'), 'Hello mit Spitze', 'Erstausstattung · 6 Teile'),
    f'{R}/little-and-loved/reel_little_and_loved_set_9x16.mp4': LAL,
    f'{R}/little-and-loved/reel_little_and_loved_maedchen_9x16.mp4': LAL,
    f'{R}/velours/reel_velours_strampeln_9x16.mp4': VELOURS,
    f'{R}/velours/reel_velours_strecken_9x16.mp4': VELOURS,
    f'{R}/velours/reel_velours_sunnozy_coming_soon_9x16.mp4': VELOURS,
}


if __name__ == '__main__':
    ziele = [os.path.abspath(a) for a in sys.argv[1:]] or list(REELS)
    for z in ziele:
        anhaengen(z, *REELS[z])
