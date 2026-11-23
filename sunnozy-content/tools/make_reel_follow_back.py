"""Follow-back-Reels (Wunsch der Nutzerin 23.11.2026, Vorbild: «I only have 70 followers but if you send me this reel
I'll follow you back … let's be friends» und «Send me this reel & I'll 100% follow you back»).

Zwei Reels, eines Deutsch, eines Englisch: 5 Babyclips aneinander (Runde 5, nur wache Babys ohne Decke, Plüschtier
oder Haarband), Text unten mit Schleier, Standardmusik, Endfolie.

    python3 tools/make_reel_follow_back.py          # beide
    python3 tools/make_reel_follow_back.py de       # nur Deutsch
Ausgabe: posts/coming-soon/reels/follow-back/reel_follow_back_<sprache>_9x16.mp4 (+ _titelbild.jpg), Captions im README dort.
"""
import os, sys, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m
import make_content_kw1 as k1
vc = k1.vc
from endfolie import anhaengen, SHOP

W, H, FPS = m.W, m.H, 30
OUT = os.path.join(m.POSTS, 'coming-soon', 'reels', 'follow-back')
R5 = 'runde5/bearbeitet/'
CLIPS = [(R5 + '20_best_family_lachen.mp4', 1.0, 3.8),            # lacht
         (R5 + '33_box_mummy_halstuch_arm.mp4', 2.0, 4.2),        # Box «I love my Mummy», wach im Arm
         (R5 + '08_happy_baby.mp4', 3.0, 5.2),                    # lacht
         (R5 + '29_box_growing_up_strong_body_D.mp4', 6.5, 8.7),  # Box «Growing up strong», wach
         (R5 + '06_smile_weinrot.mp4', 6.5, 9.3)]                 # wach, schaut
TEXTE = {
    'de': dict(hook=(['Ich habe erst 116 Follower,', 'aber schick mir dieses Reel', 'und ich folge Dir zurück'], '🥹'),
               ende=(['Lass uns', 'Freundinnen sein'], '🤍'),
               karte=('Hallo, wir sind sunnozy', 'Babykleider · Geschenkboxen', SHOP)),
    'en': dict(hook=(['I only have 116 followers,', 'but send me this reel', "and I'll follow you back"], '🥹'),
               ende=(["let's be friends"], '🤍'),
               karte=("hi, we're sunnozy", 'baby clothes · gift boxes', 'link in bio · sunnozy.ch')),
}
TY = 1440            # unteres Drittel, unter den Aufdrucken
HOOK_BIS = 5.0       # Hook bleibt länger stehen, damit man ihn ganz lesen kann
SETBILD = os.path.join(m.POSTS, 'coming-soon', 'photos', 'produktfotos-set-praesentation', 'ohne_logo', 'set_{}_quadratisch.jpg')
BOXBILD = os.path.join(m.POSTS, 'coming-soon', 'photos', 'kampagne-weihnachtsbox', 'fotos', 'box_{}.jpg')
END_BILDER = [SETBILD.format('best_family'), BOXBILD.format('i_love_my_mummy'), SETBILD.format('bauernhof'), BOXBILD.format('growing_up_strong')]


def end_bild():
    """2×2-Raster der Produkte aus dem Reel, als Bild für die Endfolie."""
    c = Image.new('RGB', (1000, 1000), (250, 246, 240))
    for k, p in enumerate(END_BILDER):
        im = Image.open(p).convert('RGB'); s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width - s) // 2 + s, (im.height - s) // 2 + s)).resize((490, 490), Image.LANCZOS)
        c.paste(im, ((k % 2) * 510, (k // 2) * 510))
    pfad = os.path.join(tempfile.gettempdir(), 'follow_back_endbild.jpg'); c.save(pfad, quality=94)
    return pfad


def schleier(zeilen):
    sch = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sch).ellipse((60, TY - 60, W - 60, TY + 75 * zeilen + 70), fill=155)
    band = Image.new('RGBA', (W, H), (40, 30, 22, 0)); band.putalpha(sch.filter(ImageFilter.GaussianBlur(45)))
    return band


def reel(sprache):
    t = TEXTE[sprache]
    dauer = sum(b - a for _, a, b in CLIPS) - k1.BLENDE * (len(CLIPS) - 1)
    e1 = Image.alpha_composite(schleier(len(t['hook'][0])), vc.text_ebene(t['hook'][0], t['hook'][1], y0=TY, groesse=50))
    e2 = Image.alpha_composite(schleier(len(t['ende'][0])), vc.text_ebene(t['ende'][0], t['ende'][1], y0=TY, groesse=56))
    vig = vc.vignette()
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_follow_back_{sprache}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    if os.path.exists(pfad):
        os.remove(pfad)                       # sonst überspringt anhaengen() die Endfolie
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = 0
    for i, fr in enumerate(k1.folge(CLIPS)):
        s = i / FPS
        c = fr.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2)).convert('RGBA'); c.alpha_composite(vig)
        for eb, a in ((e1, 1 - m.ease((s - HOOK_BIS) / 0.4)), (e2, m.ease((s - (dauer - 2.6)) / 0.5))):
            if a > 0:
                c.alpha_composite(k1.mit_alpha(eb, a))
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
