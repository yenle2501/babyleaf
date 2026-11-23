"""Follow-back-Reels (Wunsch der Nutzerin 23.11.2026, Vorbild: «I only have 70 followers but if you send me this reel
I'll follow you back … let's be friends» und «Send me this reel & I'll 100% follow you back. Let's find each other»).

Zwei Reels, eines Deutsch, eines Englisch. Babyclips der Sets Teddybär, Princess und Little Princess (Krone), nur wache
Babys ohne Plüschtier, Decke oder Haarband. Text wie in der Vorlage: gross, Serifenschrift, weiss mit weichem Schatten,
oben im Bild und die ganze Zeit sichtbar. Damit der Text keine Babygesichter verdeckt, steht der Clip in voller Breite
unten, darüber eine weich verlaufende, unscharfe Verlängerung desselben Clips. Standardmusik, Endfolie.

    python3 tools/make_reel_follow_back.py          # beide
    python3 tools/make_reel_follow_back.py de       # nur Deutsch
Ausgabe: posts/coming-soon/reels/follow-back/reel_follow_back_<sprache>_9x16.mp4 (+ _titelbild.jpg), Captions im README dort.
"""
import os, sys, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_reel_hello_little_bear_hook as hk
from endfolie import anhaengen, SHOP

W, H, FPS = m.W, m.H, 30
OUT = os.path.join(m.POSTS, 'coming-soon', 'reels', 'follow-back')
VID = os.path.join(m.POSTS, 'baby-videos')
SERIF = os.path.join(m.ROOT, 'fonts', 'cormorantR.ttf')
CLIPS = [('teddy_creme_a_bearbeitet.mp4', 0.5, 3.0),             # Teddybär, lacht
         ('princess_rosa_a_bearbeitet.mp4', 0.5, 3.0),           # Princess, lacht
         ('little_princess_krone_f_bearbeitet.mp4', 0.2, 2.9),   # Little Princess, Kapuzentuch mit Krone, wach auf dem Arm
         ('teddy_creme_b_bearbeitet.mp4', 0.5, 3.0),             # Teddybär, lacht
         ('princess_rosa_a_bearbeitet.mp4', 6.5, 9.3)]           # Princess, strampelt und lacht
BLENDE = 0.3
LNUM = ['lnum']          # normale Ziffern statt Mediävalziffern («116» statt «ii6»)
TEXTE = {
    'de': dict(oben=['Ich habe erst 116 Follower,', 'aber schick mir dieses Reel', 'und ich folge Dir zurück'], oben_emoji='🥹',
               unten='Lass uns Freundinnen sein', unten_emoji='🤍',
               karte=('Hallo, wir sind sunnozy', 'Babykleider · Erstausstattung', SHOP)),
    'en': dict(oben=['I only have 116 followers,', 'but send me this reel', "and I'll follow you back"], oben_emoji='🥹',
               unten="let's be friends", unten_emoji='🤍',
               karte=("hi, we're sunnozy", 'baby clothes · newborn sets', 'link in bio · sunnozy.ch')),
}
SETBILD = os.path.join(m.POSTS, 'coming-soon', 'photos', 'produktfotos-set-praesentation', 'ohne_logo', 'set_{}_quadratisch.jpg')
END_BILDER = [SETBILD.format('teddy_creme'), SETBILD.format('rosa'), SETBILD.format('prinzessin_krone')]


# ---------- Bild: Clip in voller Breite unten, oben unscharf verlängert ----------
def clip_frames(datei, von, bis):
    pfad = os.path.join(VID, datei)
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', pfad],
                                   capture_output=True, text=True).stdout.strip().split(','))
    ch = round(W * h / w); ch += ch % 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={W}:{ch}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * ch * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, ch), b)


def maske(ch, weich=160):
    mk = Image.new('L', (W, ch), 255); d = ImageDraw.Draw(mk)
    for y in range(weich):
        d.line((0, y, W, y), fill=int(255 * y / weich))
    return mk


def bild(fr, mk):
    y0 = H - fr.height
    s = H / fr.height; klein = fr.resize((round(W * s / 6), round(H / 6)), Image.BILINEAR)
    bg = klein.crop(((klein.width - W // 6) // 2, 0, (klein.width - W // 6) // 2 + W // 6, H // 6)).filter(ImageFilter.GaussianBlur(5))
    bg = bg.resize((W, H), Image.BICUBIC)
    bg = Image.blend(bg, Image.new('RGB', (W, H), (60, 48, 40)), 0.18)
    bg.paste(fr, (0, y0), mk)
    return bg


def folge():
    teile = [list(clip_frames(*c)) for c in CLIPS]
    nb = int(BLENDE * FPS)
    for k, t in enumerate(teile):
        start = nb if k > 0 else 0
        ende = len(t) - (nb if k < len(teile) - 1 else 0)
        for i in range(start, ende):
            yield t[i]
        if k < len(teile) - 1:
            for j in range(nb):
                yield Image.blend(t[ende + j], teile[k + 1][j], (j + 1) / (nb + 1))


# ---------- Text wie in der Vorlage ----------
def zeile(d, sch, text, y, fo, em=None):
    breite = d.textlength(text, font=fo, features=LNUM) + (em.width + 16 if em else 0)
    x0 = (W - breite) / 2
    for dx, dy in ((0, 4), (3, 4), (-3, 4), (0, 0)):
        sch.text((x0 + dx, y + dy), text, font=fo, fill=210, anchor='lm', features=LNUM)
    d.text((x0, y), text, font=fo, fill=(255, 255, 255, 255), anchor='lm', features=LNUM)
    return x0 + breite, em


def text_ebene(t):
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    sl = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(sl)
    g = 104
    while max(d.textlength(z, font=ImageFont.truetype(SERIF, g), features=LNUM) + (g * 0.9 if k == len(t['oben']) - 1 else 0)
              for k, z in enumerate(t['oben'])) > W - 70:
        g -= 2
    fo = ImageFont.truetype(SERIF, g); lh = int(g * 1.06); y = 205
    emojis = []
    for k, z in enumerate(t['oben']):
        em = hk.emoji(t['oben_emoji'], int(g * 0.8)) if k == len(t['oben']) - 1 else None
        x, em = zeile(d, ds, z, y, fo, em)
        if em:
            emojis.append((em, x - em.width, y))
        y += lh
    fo2 = ImageFont.truetype(SERIF, int(g * 0.95)); y += int(g * 0.55)
    em = hk.emoji(t['unten_emoji'], int(g * 0.72))
    x, _ = zeile(d, ds, t['unten'], y, fo2, em); emojis.append((em, x - em.width, y))
    e = Image.new('RGBA', (W, H), (30, 20, 14, 0)); e.putalpha(sl.filter(ImageFilter.GaussianBlur(12)))
    e.alpha_composite(tx)
    for em, x, yy in emojis:
        e.alpha_composite(em, (int(x), int(yy - em.height / 2 - 2)))
    return e


def end_bild():
    """Die drei Sets aus dem Reel: zwei oben, eines unten in der Mitte."""
    c = Image.new('RGB', (1000, 1000), (250, 246, 240))
    for k, p in enumerate(END_BILDER):
        im = Image.open(p).convert('RGB'); s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width - s) // 2 + s, (im.height - s) // 2 + s)).resize((490, 490), Image.LANCZOS)
        c.paste(im, ((k % 2) * 510 if k < 2 else 255, (k // 2) * 510))
    pfad = os.path.join(tempfile.gettempdir(), 'follow_back_endbild.jpg'); c.save(pfad, quality=94)
    return pfad


def reel(sprache):
    t = TEXTE[sprache]
    ebene = text_ebene(t)
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_follow_back_{sprache}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    if os.path.exists(pfad):
        os.remove(pfad)                       # sonst überspringt anhaengen() die Endfolie
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    mk = None; n = 0
    for i, fr in enumerate(folge()):
        mk = mk or maske(fr.height)
        c = bild(fr.filter(ImageFilter.UnsharpMask(radius=2, percent=45, threshold=2)), mk).convert('RGBA')
        c.alpha_composite(ebene)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    d = n / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', k1.MUSIK, '-t', f'{d:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={d - 1.2:.2f}:d=1.2,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {d:.1f} s', flush=True)
    anhaengen(pfad, end_bild(), *t['karte'])


if __name__ == '__main__':
    for s in sys.argv[1:] or list(TEXTE):
        reel(s)
