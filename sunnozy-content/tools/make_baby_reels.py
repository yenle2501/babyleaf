"""Baby-Reels aus den Grok-Strecken-Clips vom 17.11.2026 (posts/baby-videos/set_*_1.mp4 …).

Muster aus der Viral-Analyse (babyothelabel, avalia.kids, zayac_mehovoi):
  - Neugeborenes streckt sich (zayac, 2.8 Mio. Views), ein Take, kaum Kamerabewegung
  - Text-Hook ab dem ersten Bild: POV / Warnung / Schick das …, max. ~8 Wörter
  - ein klarer Empfänger zum Teilen (Gotti, Grosi, Freundin, Partner)
  - unter 12 s, Text kommt am Ende zurück, damit der Loop sauber wirkt
Stil wie tools/make_reel_hello_little_bear_hook.py: weisse Schreibmaschinenschrift (Courier Prime) mit Emoji, Video in voller
Grösse. Text steht oben im Bild über dem Kopf des Babys, damit Gesicht und Print frei bleiben.
Bearbeitung: leicht entrauscht, etwas wärmer, nachgeschärft (wie die `_bearbeitet`-Clips). Musik: Standard-Track Alex Morgan.
Endfolie: tools/endfolie.py (Set-Bild, Name, Zeile, Aufruf, Logo). Kein Preis.

Nur Clips ohne Plüschtier, Nuggi und lose Decke beim Baby (Safe Sleep), Baby auf dem Rücken.

    python3 tools/make_baby_reels.py [name ...]
Ausgabe: posts/baby-reels/reel_<name>_9x16.mp4 + _titelbild.jpg, Captions in posts/baby-reels/README.md
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
from endfolie import anhaengen, SET, SHOP, CS_AUFRUF

W, H, FPS = m.W, m.H, 30
VID = os.path.join(m.POSTS, 'baby-videos')
OUT = os.path.join(m.POSTS, 'baby-reels')
MUSIK = os.path.join(m.POSTS, 'coming-soon', 'reels', 'musik', 'alex-morgan_no-copyright-music.mp3')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
DAUER = 10.0
TEXT_BIS, LOOP_AB = 3.2, 8.6
TEXT_Y = 250
GRADE = 'hqdn3d=1.5:1.5:4:4,eq=contrast=1.04:saturation=1.04:gamma=1.01,colorbalance=rs=0.02:bs=-0.02:rm=0.015:bm=-0.015,cas=0.35'

# name: (clip, zeilen, emoji, (set_bild, set_name, zeile, aufruf))
REELS = {
    'little_bear_freundin': ('set_little_bear_baby_strampler_1.mp4', ['Schick das Deiner Freundin,', 'die bald Mami wird'], '🧸',
                             (SET + '/set_little_bear_quadratisch.jpg', 'Hello Little Bear', 'Erstausstattung · 5 Teile', SHOP)),
    'hello_world_erstes_outfit': ('set_hello_world_blatt_baby_body_1.mp4', ['POV: Sein allererstes Outfit', 'sagt «Hello World»'], '✨',
                                  (SET + '/set_hello_world_blatt_quadratisch.jpg', 'Hello World', 'Erstausstattung · 8 Teile', SHOP)),
    'teddy_babyfieber': ('set_teddy_creme_baby_strampler_1.mp4', ['Warnung:', 'Babyfieber-Gefahr'], '🥹',
                         (SET + '/set_teddy_creme_quadratisch.jpg', 'Teddybär', 'Erstausstattung · 8 Teile', SHOP)),
    'dad_mom_bald_eltern': ('set_love_dad_mom_baby_body_2.mp4', ['POV: In ein paar Wochen', 'seid Ihr Mama und Papa'], '🤍',
                            (SET + '/set_love_dad_mom_quadratisch.jpg', 'I love Dad Mom', 'coming soon', CS_AUFRUF)),
    'weltall_astronaut': ('set_weltall_hellblau_baby_body_1.mp4', ['POV: Euer kleiner Astronaut', 'ist gelandet'], '🪐',
                          (SET + '/set_weltall_hellblau_quadratisch.jpg', 'Little One · Weltall', 'coming soon', CS_AUFRUF)),
    'teddy_rosa_gotti': ('set_teddy_rosa_punkte_baby_strampler_1.mp4', ['POV: Du wirst Gotti', 'und das Geschenk ist klar'], '🎀',
                         (SET + '/set_teddy_rosa_punkte_quadratisch.jpg', 'Teddy Rosa', 'coming soon', CS_AUFRUF)),
    'prinzessin_grosi': ('set_prinzessin_krone_baby_body_1.mp4', ['Schick das dem Grosi', 'der kleinen Prinzessin'], '👑',
                         (SET + '/set_prinzessin_krone_quadratisch.jpg', 'Little Princess', 'coming soon', CS_AUFRUF)),
    'waldbaer_winterbaby': ('set_waldbaer_creme_baby_body_1.mp4', ['POV: Dein Baby', 'kommt im Winter'], '🌲',
                            (SET + '/set_waldbaer_creme_quadratisch.jpg', 'Waldbär', 'coming soon', CS_AUFRUF)),
}


def groesse(pfad):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', pfad],
                       capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])


def clip_frames(pfad):
    w, h = groesse(pfad)
    sw = round(w * H / h / 2) * 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-t', str(DAUER), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},{GRADE},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombuffer('RGB', (W, H), b)


def emoji(zeichen, hoehe):
    fo = ImageFont.truetype(EMOJI, 109)
    im = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((70, 70), zeichen, font=fo, embedded_color=True, anchor='mm')
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * hoehe / im.height), hoehe), Image.LANCZOS)


def text_ebene(zeilen, emo):
    """Weisse Schreibmaschinenschrift mit weichem Schatten, Emoji am Ende der letzten Zeile."""
    fo = ImageFont.truetype(SCHRIFT, 52); lh = 66
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    schatten = Image.new('L', (W, H), 0); ds = ImageDraw.Draw(schatten)
    sp = emoji(emo, 46)
    for k, z in enumerate(zeilen):
        letzte = k == len(zeilen) - 1
        breite = d.textlength(z, font=fo) + (sp.width + 14 if letzte else 0)
        x0 = (W - breite) / 2; y = TEXT_Y + k * lh
        ds.text((x0 + 2, y + 3), z, font=fo, fill=210, anchor='lm')
        d.text((x0, y), z, font=fo, fill=(255, 255, 255, 255), anchor='lm')
        if letzte:
            schatten.paste(255, (int(x0 + breite - sp.width), int(y - sp.height / 2 - 4)), sp.getchannel('A').point(lambda v: v // 3))
            tx.alpha_composite(sp, (int(x0 + breite - sp.width), int(y - sp.height / 2 - 4)))
    schatten = schatten.filter(ImageFilter.GaussianBlur(7))
    schatten = schatten.point(lambda v: min(255, v))
    verlauf = Image.linear_gradient('L').resize((1, 560)).point(lambda v: int((255 - v) * 0.42)).resize((W, 560))
    schatten.paste(Image.new('L', (W, 560), 255), (0, 0), verlauf)   # weicher dunkler Verlauf oben, damit die Schrift auf Creme lesbar ist
    ebene = Image.new('RGBA', (W, H), (40, 30, 25, 0)); ebene.putalpha(schatten)
    ebene.alpha_composite(tx)
    return ebene


def reel(name):
    clip, zeilen, emo, ende = REELS[name]
    ebene = text_ebene(zeilen, emo)
    n = int(round(DAUER * FPS))
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    i = 0
    for i, fr in enumerate(clip_frames(os.path.join(VID, clip))):
        if i >= n:
            break
        t = i / FPS
        a = 1 - m.ease((t - (TEXT_BIS - 0.4)) / 0.4) if t < LOOP_AB else m.ease((t - LOOP_AB) / 0.4)
        c = fr.convert('RGBA')
        if a > 0:
            e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
            c.alpha_composite(e)
        if i == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
        enc.stdin.write(c.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    dauer = min(DAUER, (i + 1) / FPS)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    anhaengen(pfad, *ende)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(REELS)):
        reel(name)
