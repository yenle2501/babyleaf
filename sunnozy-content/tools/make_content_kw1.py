"""Content KW 1 Coming soon (18.–24.11.2026): Reels aus posts/baby-videos, Karussell und Stories aus posts/baby-photos.

Regeln: CLAUDE.md (Standardmusik, POV in Schreibmaschinenschrift, kein Preis, Safe Sleep: nur wache Babys ohne Plüschtier).

    python3 tools/make_content_kw1.py [reels|karussell|stories|<reel-name>]
Ausgabe: posts/content-kw1/ (Plan und Captions: posts/content-kw1/README.md)
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_reel_velours_coming_soon as vc

W, H, FPS = m.W, m.H, 30
P = m.POSTS
OUT = os.path.join(P, 'content-kw1')
VID = os.path.join(P, 'baby-videos')
FOT = os.path.join(P, 'baby-photos', 'referenzen_photos_neu')
MUSIK = os.path.join(P, 'coming-soon', 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
CREME, DUNKEL = (250, 246, 240), (60, 52, 46)

# Reels: Clips nur mit wachem Baby, ohne Plüschtier (geprüft 17.11.2026)
REELS = {
    'best_family_lachen': {'clips': [('best_family_c_bearbeitet.mp4', 1.0, 11.0)],
                           'hook': (['POV: Du hörst zum ersten', 'Mal sein Lachen'], '🥹'),
                           'ende': (['Best Family', 'coming soon'], '🤍'), 'schleier': True, 'text_y': 1500},
    'kirschen_smile': {'clips': [('strampler_kirschen_b_bearbeitet.mp4', 0.0, 10.0)],
                       'hook': (['POV: Das erste Smile', 'ist schon aufgestickt'], '🍒'),
                       'ende': (['coming soon'], '🤍')},
    'born_in_2027': {'clips': [('born_in_2027_rosa_b_bearbeitet.mp4', 0.0, 5.2), ('born_in_2027_blau_a_bearbeitet.mp4', 0.0, 5.2)],
                     'hook': (['POV: Euer Baby', 'kommt 2027'], '✨'),
                     'ende': (['rosa oder blau?', 'coming soon'], '🤍'), 'schleier': True, 'text_y': 1470},
}
BLENDE = 0.3


def clip_frames(datei, von, bis):
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                                    os.path.join(VID, datei)], capture_output=True, text=True).stdout.strip().split(','))
    sw = round(w * H / h); sw += sw % 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', os.path.join(VID, datei), '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, H), b)


def folge(clips):
    nb = int(BLENDE * FPS); puffer = []
    for k, c in enumerate(clips):
        for j, fr in enumerate(clip_frames(*c)):
            if k > 0 and j < nb and puffer:
                yield Image.blend(puffer.pop(0), fr, (j + 1) / (nb + 1))
                continue
            puffer.append(fr)
            if len(puffer) > nb:
                yield puffer.pop(0)
    yield from puffer


def mit_alpha(e, a):
    e = e.copy(); e.putalpha(e.getchannel('A').point(lambda q: int(q * a)))
    return e


def reel(name):
    r = REELS[name]
    dauer = sum(b - a for _, a, b in r['clips']) - BLENDE * (len(r['clips']) - 1)
    ty = r.get('text_y', 900)               # Text nie auf den Aufdruck des Produkts legen
    e1 = vc.text_ebene(r['hook'][0], r['hook'][1], y0=ty, groesse=56)
    e2 = vc.text_ebene(r['ende'][0], r['ende'][1], y0=ty, groesse=56)
    vig = vc.vignette()
    if r.get('schleier'):                    # heller Body unter dem Text: weicher dunkler Schleier hinter der Schrift
        sch = Image.new('L', (W, H), 0); ImageDraw.Draw(sch).ellipse((90, ty - 50, W - 90, ty + 150), fill=150)
        band = Image.new('RGBA', (W, H), (40, 30, 22, 0)); band.putalpha(sch.filter(ImageFilter.GaussianBlur(45)))
        e1 = Image.alpha_composite(band, e1); e2 = Image.alpha_composite(band, e2)
    os.makedirs(os.path.join(OUT, 'reels'), exist_ok=True)
    pfad = os.path.join(OUT, 'reels', f'reel_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = 0
    for i, fr in enumerate(folge(r['clips'])):
        t = i / FPS
        c = fr.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2)).convert('RGBA'); c.alpha_composite(vig)
        for eb, a in ((e1, 1 - m.ease((t - 2.8) / 0.4)), (e2, m.ease((t - (dauer - 2.4)) / 0.5))):
            if a > 0:
                c.alpha_composite(mit_alpha(eb, a))
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    dauer = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


# ---------- Karussell «Welches Set soll zuerst kommen?» ----------
SETS = [('born-in-2027-rosa_baby_ads.png', '«Born in 2027» Rosa'),
        ('set_bauernhof_baby_body.png', '«Bauernhof»'),
        ('set_hund_creme_baby_body_ads.png', '«I love Dogs»'),
        ('set_love_dad_mom_baby_strampler_ads.png', '«I love Dad Mom»'),
        ('set_wal_blau_baby_strampler_ads.png', '«Wal» Hellblau'),
        ('set_waldbaer_creme_baby_body.png', '«Waldbär»'),
        ('set_weltall_hellblau_baby_body.png', '«Little One» Weltall')]


def f(g):
    return ImageFont.truetype(SCHRIFT, g)


def auf_4x5(im):
    w, h = im.size
    if w / h > 0.8:
        nw = int(h * 0.8); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / 0.8); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize((1080, 1350), Image.LANCZOS)


def mitte(d, text, y, g, fill=DUNKEL):
    d.text((540, y), text, font=f(g), fill=fill, anchor='mm')


def karussell():
    o = os.path.join(OUT, 'karussell'); os.makedirs(o, exist_ok=True)
    c = Image.new('RGB', (1080, 1350), CREME); d = ImageDraw.Draw(c)
    vorschau = [auf_4x5(Image.open(os.path.join(FOT, s)).convert('RGB')).resize((300, 375), Image.LANCZOS) for s, _ in SETS[:6]]
    for k, im in enumerate(vorschau):
        c.paste(im, (60 + (k % 3) * 330, 470 + (k // 3) * 400))
    mitte(d, 'coming soon', 170, 44, (150, 130, 115))
    mitte(d, 'Welches Set soll', 270, 64)
    mitte(d, 'zuerst kommen?', 350, 64)
    mitte(d, 'Wisch durch und schreib die Nummer ✨'.replace(' ✨', ''), 1300, 34)
    c.save(os.path.join(o, '01_titel.jpg'), quality=94)
    for k, (datei, name) in enumerate(SETS, 1):
        im = auf_4x5(Image.open(os.path.join(FOT, datei)).convert('RGB')).convert('RGBA')
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.ellipse((40, 40, 150, 150), fill=(250, 246, 240, 235))
        dl.text((95, 97), str(k), font=f(64), fill=DUNKEL + (255,), anchor='mm')
        dl.rounded_rectangle((40, 1240, 40 + dl.textlength(name, font=f(36)) + 40, 1310), 30, fill=(250, 246, 240, 225))
        dl.text((60, 1275), name, font=f(36), fill=DUNKEL + (255,), anchor='lm')
        im.alpha_composite(lay); im.convert('RGB').save(os.path.join(o, f'{k + 1:02d}_{k}.jpg'), quality=94)
    c = Image.new('RGB', (1080, 1350), CREME); d = ImageDraw.Draw(c)
    for k, t in enumerate(['Schreib die Nummer', 'Deines Lieblings-Sets', 'in die Kommentare']):
        mitte(d, t, 520 + k * 85, 58)
    mitte(d, 'Eure Wünsche entscheiden mit.', 840, 34, (120, 105, 95))
    L = m.logo(300, (122, 108, 104)); c.paste(L, ((1080 - L.width) // 2, 1080), L)
    mitte(d, 'coming soon', 1230, 38, (150, 130, 115))
    c.save(os.path.join(o, f'{len(SETS) + 2:02d}_ende.jpg'), quality=94)
    print('Karussell:', sorted(os.listdir(o)))


def stories():
    o = os.path.join(OUT, 'stories'); os.makedirs(o, exist_ok=True)
    # Story 1: Umfrage rosa oder blau (Born in 2027)
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    mitte(d, 'Euer Baby kommt 2027?', 260, 60); mitte(d, 'rosa oder blau?', 345, 60)
    for k, datei in enumerate([os.path.join(FOT, 'born-in-2027-rosa_baby_ads.png'),
                               os.path.join(P, 'baby-photos', 'baby_echt_born_in_2027_blau.jpg')]):
        im = auf_4x5(Image.open(datei).convert('RGB')).resize((440, 550), Image.LANCZOS)
        c.paste(im, (80 + k * 480, 470))
    mitte(d, '(Umfrage-Sticker hier)', 1250, 30, (190, 180, 170))
    L = m.logo(220, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1700), L)
    c.save(os.path.join(o, 'story_umfrage_born_2027.jpg'), quality=93)
    # Story 2: Warteliste
    im = auf_4x5(Image.open(os.path.join(FOT, 'set_weltall_hellblau_baby_body.png')).convert('RGB'))
    c = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(c)
    c.paste(im.resize((900, 1125), Image.LANCZOS), (90, 380))
    mitte(d, 'Neue Sets kommen bald', 200, 54); mitte(d, 'Willst Du es zuerst wissen?', 275, 44, (120, 105, 95))
    mitte(d, 'Antworte mit 🤍'.replace(' 🤍', ''), 1600, 48)
    e = vc.hk.emoji('🤍', 52); c.paste(e, (540 + int(d.textlength('Antworte mit', font=f(48)) / 2) + 12, 1600 - 30), e)
    mitte(d, '(Fragen- oder Emoji-Slider-Sticker)', 1700, 28, (190, 180, 170))
    c.save(os.path.join(o, 'story_warteliste.jpg'), quality=93)
    print('Stories:', sorted(os.listdir(o)))


if __name__ == '__main__':
    teil = sys.argv[1:] or ['reels', 'karussell', 'stories']
    if 'karussell' in teil:
        karussell()
    if 'stories' in teil:
        stories()
    for name in REELS:                       # 'reels' = alle, oder einzelne Namen
        if 'reels' in teil or name in teil:
            reel(name)
