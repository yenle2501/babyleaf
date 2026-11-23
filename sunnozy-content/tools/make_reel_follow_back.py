"""Follow-back-Reels (Wunsch der Nutzerin 23.11.2026, Vorbild: «I only have 70 followers but if you send me this reel
I'll follow you back … let's be friends» und «Send me this reel & I'll 100% follow you back. Let's find each other»).

Zwei Reels, eines Deutsch, eines Englisch. Clips aus den Reels, die schon im Profil sind (Hello Little Bear, Best Family,
Box «Growing up strong»), nur die mit wachem Baby. Text oben und die ganze Zeit sichtbar, fette Schrift ohne Serifen
(Nunito Sans) in Dunkelbraun, ohne Leuchten und ohne Schatten. Damit der Text keine Babygesichter verdeckt, steht der Clip in voller Breite
unten, darüber eine weich verlaufende, unscharfe Verlängerung desselben Clips. Standardmusik, Endfolie.

    python3 tools/make_reel_follow_back.py          # beide
    python3 tools/make_reel_follow_back.py de       # nur Deutsch (Instagram)
    python3 tools/make_reel_follow_back.py tiktok_de tiktok_en   # TikTok-Versionen
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
VID = m.POSTS
SERIF = os.path.join(m.ROOT, 'fonts', 'nunitosans-800.ttf')    # klare, fette Schrift ohne Serifen (Wunsch 23.11.: andere Schrift)
STRICH = 0                # keine Kontur, kein Leuchten (Wunsch der Nutzerin)
FARBE = (62, 48, 40)      # dunkelbraun auf hellem Grund, darum ohne Schatten gut lesbar
# Clips aus den Reels, die schon im Profil sind (Wunsch 23.11.), nur die mit wachem Baby
CLIPS = [('coming-soon/reels/hello-little-bear/original/clip_bett.mp4', 1.0, 3.6),          # Hello Little Bear, wach
         ('coming-soon/reels/best-family-teddy/original/baby_clip_a.mp4', 0.4, 3.0),       # Best Family, winkt, Teddy-Rassel aus dem Set
         ('baby-videos/runde5/bearbeitet/29_box_growing_up_strong_body_D.mp4', 3.5, 6.1),  # Box «Growing up strong» (Daddy's Bestie), wach
         ('coming-soon/reels/best-family-teddy/original/baby_clip_b.mp4', 0.8, 3.4),       # Best Family, winkt
         ('coming-soon/reels/hello-little-bear/original/clip_bett.mp4', 10.0, 12.8)]       # Hello Little Bear, nah, wach
BLENDE = 0.3
CH = 1344                 # Clip-Höhe nach dem Skalieren auf volle Breite (3:4-Clips ergeben 1344–1430 px)
LNUM = ['lnum']          # normale Ziffern statt Mediävalziffern («116» statt «ii6»)
TEXTE = {
    'de': dict(oben=['Ich habe erst 116 Follower,', 'aber schick mir dieses Reel', 'und ich folge Dir zurück'], oben_emoji='✨🥹',
               unten=['Lass uns Freundinnen sein'], unten_emoji='🤎🫶',
               karte=('Hallo, wir sind sunnozy', 'Babykleider · Erstausstattung', SHOP)),
    'en': dict(oben=['I only have 116 followers,', 'but send me this reel', "and I'll follow you back"], oben_emoji='✨🥹',
               unten=["let's be friends"], unten_emoji='🤎🫶',
               karte=("hi, we're sunnozy", 'baby clothes · newborn sets', 'link in bio · sunnozy.ch')),
    # TikTok (Wunsch 23.11.: dort erst 1 Follower). «Video» statt «Reel», Text etwas tiefer wegen der Reiter oben.
    'tiktok_de': dict(oben=['Ich habe erst 1 Follower,', 'aber schick mir dieses Video', 'und ich folge Dir zurück'], oben_emoji='✨🥹',
                      unten=['Lass uns Freundinnen sein'], unten_emoji='🤎🫶', datei='tiktok_follow_back_de', y0=215,
                      karte=('Hallo, wir sind sunnozy', 'Babykleider · Erstausstattung', SHOP)),
    'tiktok_en': dict(oben=['I only have 1 follower,', 'but send me this video', "and I'll follow you back"], oben_emoji='✨🥹',
                      unten=["let's be friends"], unten_emoji='🤎🫶', datei='tiktok_follow_back_en', y0=215,
                      karte=("hi, we're sunnozy", 'baby clothes · newborn sets', 'link in bio · sunnozy.ch')),
}
SETBILD = os.path.join(m.POSTS, 'coming-soon', 'photos', 'produktfotos-set-praesentation', 'ohne_logo', 'set_{}_quadratisch.jpg')
END_BILDER = [SETBILD.format('little_bear'), SETBILD.format('best_family'),
              os.path.join(m.POSTS, 'coming-soon', 'photos', 'kampagne-weihnachtsbox', 'fotos', 'box_growing_up_strong.jpg')]


# ---------- Bild: Clip in voller Breite unten, oben unscharf verlängert ----------
def clip_frames(datei, von, bis):
    pfad = os.path.join(VID, datei)
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', pfad],
                                   capture_output=True, text=True).stdout.strip().split(','))
    ch = CH                                   # alle Clips gleich hoch, sonst klappt die Überblendung nicht
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},scale={W}:-2:flags=lanczos,crop={W}:{CH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
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


VIDEO_Y = 640         # Clip beginnt hier (unten wird höchstens ein schmaler Rand abgeschnitten), darüber steht der Text


def bild(fr, mk):
    y0 = max(H - fr.height, VIDEO_Y)
    s = H / fr.height; klein = fr.resize((round(W * s / 6), round(H / 6)), Image.BILINEAR)
    bg = klein.crop(((klein.width - W // 6) // 2, 0, (klein.width - W // 6) // 2 + W // 6, H // 6)).filter(ImageFilter.GaussianBlur(5))
    bg = bg.resize((W, H), Image.BICUBIC)
    bg = Image.blend(bg, Image.new('RGB', (W, H), (250, 246, 240)), 0.45)   # heller Grund für dunkle Schrift
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
def emojis(folge, hoehe):
    """Mehrere Emojis nebeneinander (z.B. '✨🥹', '🤍🫶')."""
    teile = [hk.emoji(z, hoehe) for z in folge]
    im = Image.new('RGBA', (sum(t.width for t in teile) + 8 * (len(teile) - 1), hoehe), (0, 0, 0, 0)); x = 0
    for t in teile:
        im.alpha_composite(t, (x, 0)); x += t.width + 8
    return im


def zeile(d, sch, text, y, fo, em=None):
    breite = d.textlength(text, font=fo, features=LNUM) + (em.width + 16 if em else 0)
    x0 = (W - breite) / 2
    d.text((x0, y), text, font=fo, fill=FARBE + (255,), anchor='lm', features=LNUM, stroke_width=STRICH, stroke_fill=FARBE + (255,))
    return x0 + breite, em


def text_ebene(t):
    """Zwei Blöcke wie in der Vorlage: oben die Bitte, darunter grösser «Lass uns Freundinnen sein». Jeder Block so gross wie
    möglich (höchstens bis zur Obergrenze), Emojis am Ende der letzten Zeile."""
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    sl = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(sl)
    marken = []; y = t.get('y0', 165)

    def groesse(zeilen, emo, g):
        while max(d.textlength(z, font=ImageFont.truetype(SERIF, g), features=LNUM) + (len(emo) * g * 0.8 + 16 if k == len(zeilen) - 1 else 0)
                  for k, z in enumerate(zeilen)) > W - 90:
            g -= 2
        return g

    for zeilen, emo, gmax, abstand in ((t['oben'], t['oben_emoji'], 74, 0.5), (t['unten'], t['unten_emoji'], 84, 0)):
        g = groesse(zeilen, emo, gmax); fo = ImageFont.truetype(SERIF, g); lh = int(g * 1.2)
        y += int(g * 0.5)
        for k, z in enumerate(zeilen):
            em = emojis(emo, int(g * 0.72)) if k == len(zeilen) - 1 else None
            x, em = zeile(d, ds, z, y, fo, em)
            if em:
                marken.append((em, x - em.width, y))
            y += lh
        y += int(g * abstand)
    e = Image.new('RGBA', (W, H), (30, 20, 14, 0)); e.putalpha(sl.filter(ImageFilter.GaussianBlur(10)))
    e.alpha_composite(tx)
    for em, x, yy in marken:
        e.alpha_composite(em, (int(x), int(yy - em.height / 2 + 4)))
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
    pfad = os.path.join(OUT, t.get('datei', f'reel_follow_back_{sprache}') + '_9x16.mp4'); tmp = pfad + '.tmp.mp4'
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
