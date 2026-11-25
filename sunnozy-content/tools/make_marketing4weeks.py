"""30-Tage-Kampagne nach dem Marketingplan der Nutzerin (Sunnozy_30-Tage-Marketingkampagne.md, 25.11.2026) für die
Coming-soon-Produkte: Reels/TikToks, Storys und Fotos, alles auf Englisch.

Regeln (CLAUDE.md): Englisch, kein Preis bei Coming soon, Standardmusik, Endfolie an jedem Video, Safe Sleep (nur wache
Babys ohne Kuscheltier/Decke/Haarband im Bett), keine erfundenen Bewertungen oder Bestseller, keine fremden Marken.

    python3 tools/make_marketing4weeks.py                 # alles
    python3 tools/make_marketing4weeks.py bilder          # nur Fotos und Storys
    python3 tools/make_marketing4weeks.py videos          # nur Videos
    python3 tools/make_marketing4weeks.py tag05_reel_sneak_peek   # ein Video
Ausgabe: posts/marketing4weeks/woche-1 … woche-4 (Plan und Captions: posts/marketing4weeks/README.md)
"""
import os, sys, subprocess, tempfile, datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_reel_hello_little_bear_hook as hk
from endfolie import anhaengen, SHOP, CS_AUFRUF

W, H, FPS = m.W, m.H, 30
P = m.POSTS
OUT = os.path.join(P, 'marketing4weeks')
CS = os.path.join(P, 'coming-soon', 'photos')
VID = os.path.join(P, 'baby-videos')
SCHRIFT = os.path.join(m.ROOT, 'fonts', 'courierprime.ttf')
START = datetime.date(2026, 11, 26)            # Tag 1
LAUNCH_TAG = 27                                # Tag 27 = Launch
LAUNCH = START + datetime.timedelta(days=LAUNCH_TAG - 1)
LAUNCH_TXT = f'{LAUNCH.day}.{LAUNCH.month}.'

CREME, BLUSH, BEIGE, SAND = (250, 246, 240), (242, 224, 218), (236, 224, 208), (226, 210, 190)
ROSE, SALBEI, MOKKA, HIMMEL = (214, 172, 166), (176, 190, 166), (176, 142, 116), (196, 212, 224)
DUNKEL, GRAU = (62, 48, 40), (120, 105, 95)
PASTELL = [BLUSH, BEIGE, (222, 230, 214), (230, 222, 236), (220, 230, 238), SAND]

# ---------- Material ----------
FRE = lambda k: os.path.join(CS, 'marktplatz-galaxus-amazon', 'freigestellt', f'set_{k}.png')
FRE2 = lambda k: os.path.join(CS, k, 'marktplatz', f'{k}_freigestellt.png')
TEIL = lambda s, t: os.path.join(CS, 'marktplatz-galaxus-amazon', 'einzelteile', f'set_{s}', f'set_{s}_{t}.jpg')
HAUPT = lambda k: os.path.join(CS, 'produktfotos-set-praesentation', 'hauptbilder_2048', 'ohne_logo', f'set_{k}_quadratisch.jpg')
VELOURS_FOTO = os.path.join(P, 'coming-soon', 'reels', 'velours', 'original', 'produktfoto_velours.png')
VELOURS = lambda c: os.path.join(P, 'coming-soon', 'reels', 'velours', 'original', c)
R5 = lambda c: os.path.join(VID, 'runde5', 'bearbeitet', c)
ARCH = {'little_princess': os.path.join(VID, '2026-11-06_2329_baby_zuhause_cs_strampler_rosa_little_princess_94d5164c.mp4'),
        'smile_gruen': os.path.join(VID, '2026-11-06_2329_baby_zuhause_cs_strampler_smile_gruen_8129f305.mp4'),
        'weltall': os.path.join(VID, '2026-11-06_2329_baby_zuhause_cs_weltall_hellblau_effb7d61.mp4')}
BEST_FAMILY = lambda c: os.path.join(P, 'coming-soon', 'reels', 'best-family-teddy', 'original', c)
HAENDE = lambda c: os.path.join(VID, c)
SETS = {  # Coming-soon-Sets (Shopify-Entwurf), freigestellt
    'Best Family': FRE('best_family'), 'Little Princess': FRE('prinzessin_krone'), 'Bunny': FRE('hase_rosa'),
    'Whale': FRE('wal_blau'), 'Farm': FRE('bauernhof'), 'I love Dad Mom': FRE('love_dad_mom'),
    'Daisy': FRE('gaensebluemchen'), 'little and cute': FRE('lila_hase'), 'Born in 2027': FRE2('born-in-2027-rosa'),
    'Polar Bear': FRE2('eisbaer-taupe'), 'Little Bear': FRE2('little-bear-rosa'), 'Forest Bear': FRE2('waldbaer-creme'),
    'I love Dogs': os.path.join(CS, 'produktfotos-set-praesentation', 'freigestellt', 'set_hund_creme.png')}


# ---------- Bausteine ----------
def f(g):
    return ImageFont.truetype(SCHRIFT, int(g))


def zeichen(folge):
    """Emojis als Zeichengruppen: Flaggen (zwei Regionalbuchstaben) und Variantenzeichen (FE0F) bleiben zusammen."""
    out = []
    for z in folge:
        if out and (z == '\ufe0f' or z == '\u200d' or out[-1].endswith('\u200d')
                    or (0x1F1E6 <= ord(z) <= 0x1F1FF and len(out[-1]) == 1 and 0x1F1E6 <= ord(out[-1]) <= 0x1F1FF)):
            out[-1] += z
        else:
            out.append(z)
    return out


def emojis(folge, hoehe):
    teile = [hk.emoji(z, hoehe) for z in zeichen(folge)]
    im = Image.new('RGBA', (sum(t.width for t in teile) + 6 * (len(teile) - 1), hoehe), (0, 0, 0, 0)); x = 0
    for t in teile:
        im.alpha_composite(t, (x, 0)); x += t.width + 6
    return im


def text(c, zeilen, y, g=56, farbe=DUNKEL, emo=None, x=None, lh=1.25):
    """Zentrierte Zeilen (oder ab x), Emojis am Ende der letzten Zeile."""
    d = ImageDraw.Draw(c); fo = f(g)
    for k, z in enumerate(zeilen):
        em = emojis(emo, int(g * 0.9)) if emo and k == len(zeilen) - 1 else None
        b = d.textlength(z, font=fo) + (em.width + 12 if em else 0)
        x0 = (c.width - b) / 2 if x is None else x; yy = y + k * g * lh
        d.text((x0, yy), z, font=fo, fill=farbe, anchor='lm')
        if em:
            c.paste(em, (int(x0 + b - em.width), int(yy - em.height / 2 - 2)), em)


def laden(p):
    im = Image.open(p)
    return im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')


def freistellen(im):
    if im.mode == 'RGBA' and im.getbbox():
        return im.crop(im.getbbox())
    return im


def einpassen(im, b, h):
    im = freistellen(im); s = min(b / im.width, h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def fuellen(im, b, h, fx=0.5, fy=0.5, zoom=1.0):
    im = im.convert('RGB'); s = max(b / im.width, h / im.height) * zoom; cw, ch = b / s, h / s
    x0 = min(max(fx * im.width - cw / 2, 0), im.width - cw); y0 = min(max(fy * im.height - ch / 2, 0), im.height - ch)
    return im.resize((b, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def schatten_setzen(c, im, x, y, r=26, a=70):
    s = Image.new('RGBA', (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    maske = im.split()[3] if im.mode == 'RGBA' else Image.new('L', im.size, 255)
    s.paste((70, 50, 40, a), (2 * r, 2 * r + r // 2), maske)
    c.alpha_composite(s.filter(ImageFilter.GaussianBlur(r)), (x - 2 * r, y - 2 * r))
    c.alpha_composite(im.convert('RGBA'), (x, y))


def karte(c, p, mx, my, b, h, schatten=True, **kw):
    im = einpassen(laden(p), b, h) if not kw else fuellen(laden(p), b, h, **kw)
    x, y = int(mx - im.width / 2), int(my - im.height / 2)
    if schatten:
        schatten_setzen(c, im, x, y)
    else:
        c.alpha_composite(im.convert('RGBA'), (x, y))
    return im


def logo(c, y, breite=230):
    L = m.logo(breite, (122, 108, 104)); c.alpha_composite(L.convert('RGBA'), ((c.width - L.width) // 2, y))


def leinwand(fmt, farbe=CREME):
    return Image.new('RGBA', (1080, 1350) if fmt == '4x5' else (W, H), farbe + (255,))


def speichern(c, woche, name):
    o = os.path.join(OUT, f'woche-{woche}'); os.makedirs(o, exist_ok=True)
    c.convert('RGB').save(os.path.join(o, name + '.jpg'), quality=93); print(name, flush=True)


# ---------- Video-Motor ----------
def clip_cover(p, von, bis):
    yield from k1.clip_frames(p, von, bis)


def clip_breit(p, von, bis):
    """Querformat- oder breite Clips: volle Breite, oben/unten Rand verlängert."""
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p],
                                   capture_output=True, text=True).stdout.strip().split(',')[:2])
    ch = round(W * h / w); ch += ch % 2; y0 = (H - ch) // 2
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(von), '-t', str(bis - von), '-i', p, '-map', '0:v:0',
                           '-vf', f'fps={FPS},scale={W}:{ch}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * ch * 3
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        fr = Image.frombuffer('RGB', (W, ch), b)
        bg = fr.resize((W // 10, H // 10), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BICUBIC)
        bg = Image.blend(bg, Image.new('RGB', (W, H), CREME), 0.35); bg.paste(fr, (0, y0))
        yield bg


def bild_frames(p, dauer, z0=1.0, z1=1.08, fx=0.5, fy=0.5):
    im = laden(p).convert('RGB')
    for i in range(int(round(dauer * FPS))):
        yield fuellen(im, W, H, fx, fy, z0 + (z1 - z0) * m.ease(i / (dauer * FPS)))


def produkt_frames(p, dauer, bg, beschriftung=None, nummer=None):
    """Produkt mit Schatten einmal auf eine Ebene setzen, dann pro Bild nur leicht hineinzoomen (schnell)."""
    im = einpassen(laden(p), 900, 900)
    ebene = Image.new('RGBA', (W, H), (0, 0, 0, 0)); schatten_setzen(ebene, im, (W - im.width) // 2, 960 - im.height // 2, r=24, a=60)
    grund = Image.new('RGBA', (W, H), bg + (255,))
    oben = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if nummer:
        text(oben, [str(nummer)], 330, 150, DUNKEL)
    if beschriftung:
        text(oben, [beschriftung], 1560, 50, DUNKEL)
    for i in range(int(round(dauer * FPS))):
        z = 1.0 + 0.04 * m.ease(i / (dauer * FPS)); cw, ch = W / z, H / z
        c = grund.copy(); c.alpha_composite(ebene.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)))
        c.alpha_composite(oben)
        yield c.convert('RGB')


def raster_frames(pfade, dauer, bg, titel=None):
    """Sets erscheinen nacheinander im Raster 3×4 (Collection reveal)."""
    n = len(pfade); sp = 2 if n <= 4 else 3; gr = 460 if sp == 2 else 300; ab = gr + 30
    kach = [einpassen(laden(p), gr, gr) for p in pfade]
    x_rand = (W - sp * ab + 30) // 2; y_rand = 330 if sp == 3 else 420
    for i in range(int(round(dauer * FPS))):
        t = i / FPS; c = Image.new('RGBA', (W, H), bg + (255,))
        for k, im in enumerate(kach):
            a = m.ease((t - k * (dauer * 0.6 / n)) / 0.35)
            if a <= 0:
                continue
            x = x_rand + (k % sp) * ab + (gr - im.width) // 2; y = y_rand + (k // sp) * ab + (gr - im.height) // 2
            t2 = im.copy(); al = t2.split()[3].point(lambda v: int(v * a)) if t2.mode == 'RGBA' else Image.new('L', t2.size, int(255 * a))
            t2.putalpha(al); c.alpha_composite(t2.convert('RGBA'), (x, y))
        if titel and t > dauer * 0.7:
            text(c, titel, 1700, 52, DUNKEL)
        yield c.convert('RGB')


def szene_frames(s):
    art = s[0]
    if art == 'clip':
        return list(clip_cover(*s[1:4]))
    if art == 'breit':
        return list(clip_breit(*s[1:4]))
    if art == 'bild':
        return list(bild_frames(*s[1:]))
    if art == 'produkt':
        return list(produkt_frames(*s[1:]))
    if art == 'raster':
        return list(raster_frames(*s[1:]))
    if art == 'frames':                          # fertige Bilder (eigene Animationen)
        return list(s[1])
    raise ValueError(art)


def pov_ebene(zeilen, emo, y=1400, g=54, farbe=(255, 255, 255), schleier=True):
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if schleier:
        s = Image.new('L', (W, H), 0); ImageDraw.Draw(s).ellipse((50, y - 85, W - 50, y + int(len(zeilen) * g * 1.25) + 40), fill=150)
        b = Image.new('RGBA', (W, H), (40, 30, 22, 0)); b.putalpha(s.filter(ImageFilter.GaussianBlur(45))); e.alpha_composite(b)
    sl = Image.new('L', (W, H), 0); fo = f(g); ds = ImageDraw.Draw(sl); d0 = ImageDraw.Draw(e)
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    text(tx, zeilen, y, g, farbe + (255,), emo)
    if farbe == (255, 255, 255):
        for k, z in enumerate(zeilen):
            em_b = (len(zeichen(emo)) * g * 0.9 + 12) if emo and k == len(zeilen) - 1 else 0
            x0 = (W - d0.textlength(z, font=fo) - em_b) / 2
            for dx, dy in ((0, 3), (2, 3), (-2, 3)):
                ds.text((x0 + dx, y + k * g * 1.25 + dy), z, font=fo, fill=200, anchor='lm')
        sch = Image.new('RGBA', (W, H), (45, 30, 20, 0)); sch.putalpha(sl.filter(ImageFilter.GaussianBlur(8))); e.alpha_composite(sch)
    e.alpha_composite(tx)
    return e


def szene_dauer(s):
    art = s[0]
    if art in ('clip', 'breit'):
        return s[3] - s[2]
    if art == 'frames':
        return s[2]
    return s[2]


SANS = os.path.join(m.ROOT, 'fonts', 'nunitosans-800.ttf')


def band_ebene(zeilen, emo, y, g=62):
    """Grosser, gut lesbarer Text: fette Schrift ohne Serifen, dunkelbraun auf cremefarbenem Band (ohne Leuchten)."""
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(e)
    fo = ImageFont.truetype(SANS, g)
    breite = lambda k, z: d.textlength(z, font=fo) + ((len(zeichen(emo)) * g * 0.95 + 14) if emo and k == len(zeilen) - 1 else 0)
    while max(breite(k, z) for k, z in enumerate(zeilen)) > W - 160 and g > 36:
        g -= 2; fo = ImageFont.truetype(SANS, g)
    lh = int(g * 1.22); hoehe = lh * len(zeilen) + 44; bmax = max(breite(k, z) for k, z in enumerate(zeilen)) + 70
    d.rounded_rectangle(((W - bmax) / 2, y - g * 0.62 - 22, (W + bmax) / 2, y - g * 0.62 - 22 + hoehe), radius=34, fill=CREME + (238,))
    for k, z in enumerate(zeilen):
        em = emojis(emo, int(g * 0.95)) if emo and k == len(zeilen) - 1 else None
        b = breite(k, z); x0 = (W - b) / 2; yy = y + k * lh
        d.text((x0, yy), z, font=fo, fill=DUNKEL, anchor='lm')
        if em:
            e.alpha_composite(em, (int(x0 + b - em.width), int(yy - em.height / 2)))
    return e


def video(woche, name, szenen, texte, karte_end, blende=0.3, ordner=None):
    """szenen: Liste von Szenen; texte: [(von, bis, zeilen, emoji, y, stil)], bis=None: bis Ende; stil 'pov' oder 'dunkel'.
    Es liegt immer nur eine Szene im Speicher (lange Videos)."""
    nb = int(blende * FPS)
    dauer = sum(szene_dauer(s) for s in szenen) - blende * (len(szenen) - 1)
    ebenen = [(von, dauer if bis is None else bis,
               band_ebene(z, e, y) if stil == 'band' else
               pov_ebene(z, e, y, farbe=(255, 255, 255) if stil == 'pov' else DUNKEL, schleier=stil == 'pov'))
              for von, bis, z, e, y, stil in texte]
    o = ordner or os.path.join(OUT, f'woche-{woche}'); os.makedirs(o, exist_ok=True)
    pfad = os.path.join(o, name + '_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    if os.path.exists(pfad):
        os.remove(pfad)
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    n = [0]

    def schreiben(fr):
        t = n[0] / FPS; c = fr.convert('RGBA')
        for von, bis, eb in ebenen:
            a = min(m.ease((t - von) / 0.3) if von > 0 else 1, 1 - m.ease((t - bis + 0.3) / 0.3) if bis < dauer else 1)
            if a > 0:
                c.alpha_composite(k1.mit_alpha(eb, a))
        if n[0] == int(0.5 * FPS):
            c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=90)
        enc.stdin.write(c.convert('RGB').tobytes()); n[0] += 1

    rest = None
    for k, s in enumerate(szenen):
        fr = szene_frames(s); start = 0
        if rest is not None:
            for j in range(min(nb, len(rest), len(fr))):
                schreiben(Image.blend(rest[j], fr[j], (j + 1) / (nb + 1)))
            start = nb
        ende = len(fr) - (nb if k < len(szenen) - 1 else 0)
        for x in fr[start:ende]:
            schreiben(x)
        rest = fr[ende:] if k < len(szenen) - 1 else None
        del fr
    enc.stdin.close(); enc.wait()
    dauer = n[0] / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-i', k1.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=1.4,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{name}: {dauer:.1f} s', flush=True)
    anhaengen(pfad, *karte_end)


def end_collage(namen):
    c = Image.new('RGBA', (1000, 1000), CREME + (255,))
    for k, n in enumerate(namen[:4]):
        im = einpassen(laden(SETS[n]), 470, 470); im = im.convert('RGBA')
        c.alpha_composite(im, ((k % 2) * 510 + (490 - im.width) // 2, (k // 2) * 510 + (490 - im.height) // 2))
    p = os.path.join(tempfile.gettempdir(), 'm4w_' + '_'.join(x.replace(' ', '') for x in namen[:4]) + '.jpg')
    c.convert('RGB').save(p, quality=94)
    return p


CS_KARTE = lambda namen, name='coming soon to sunnozy', zeile='coming soon': (end_collage(namen), name, zeile, CS_AUFRUF)
LIVE_KARTE = lambda namen: (end_collage(namen), 'our newborn sets', 'now live', SHOP)
MAIN4 = ['Best Family', 'Little Princess', 'Bunny', 'Whale']
POV, DUN = 'pov', 'dunkel'


# ---------- Videos ----------
def tag01_reel_teaser():
    video(1, 'tag01_reel_teaser', [
        ('bild', TEIL('best_family', 'body'), 2.2, 2.4, 2.8, 0.5, 0.42),
        ('bild', TEIL('prinzessin_krone', 'kapuzentuch'), 2.2, 2.2, 2.6, 0.5, 0.35),
        ('bild', VELOURS_FOTO, 2.2, 2.6, 3.0, 0.24, 0.43),
        ('bild', TEIL('hase_rosa', 'body'), 2.2, 2.2, 2.6, 0.5, 0.45),
        ('bild', VELOURS_FOTO, 2.6, 1.6, 1.0, 0.48, 0.45)],
        [(0, 3.2, ['warning: these little', 'outfits might steal', 'your heart'], '🤍', 1380, POV), (8.0, None, ['something beautiful', 'is coming'], '🤍', 1420, POV)],
        CS_KARTE(MAIN4, 'something beautiful'))


def tag02_tiktok_getting_ready():
    video(1, 'tag02_tiktok_getting_ready', [
        ('clip', HAENDE('Hand_placing_baby_bodysuits_in_202608310851.mp4'), 0.0, 4.2),
        ('clip', HAENDE('Hands_changing_baby_bodysuits_in…_202608311248.mp4'), 4.5, 9.5)],
        [(0, 3.2, ["mama, you don't need", 'another baby outfit…', 'or do you?'], '🥹', 300, POV), (6.0, None, ['coming soon'], '✨', 330, POV)],   # Text oben: unten steht das Logo auf der Tüte
        CS_KARTE(MAIN4))


def tag03_tiktok_details():
    """Auch als Reel an Tag 13."""
    video(1, 'tag03_tiktok_details', [
        ('bild', TEIL('best_family', 'strampler'), 1.9, 1.8, 2.3, 0.5, 0.35),
        ('bild', TEIL('prinzessin_krone', 'body'), 1.9, 2.2, 2.6, 0.5, 0.45),
        ('bild', TEIL('wal_blau', 'laetzchen'), 1.9, 1.15, 1.35, 0.5, 0.5),
        ('bild', VELOURS_FOTO, 1.9, 2.6, 3.0, 0.5, 0.25),
        ('bild', TEIL('hase_rosa', 'muetze'), 1.9, 1.6, 2.0, 0.5, 0.5),
        ('bild', VELOURS_FOTO, 2.0, 2.4, 2.8, 0.2, 0.88)],
        [(0, 3.2, ['wait until you see', 'this little detail'], '👀', 1420, POV), (8.6, None, ['little details,', 'lots of love'], '🤍', 1420, POV)],
        CS_KARTE(MAIN4))


def tag04_tiktok_pink_or_beige():
    video(1, 'tag04_tiktok_pink_or_beige', [
        ('produkt', SETS['Little Princess'], 1.6, BLUSH, 'pink'), ('produkt', SETS['Best Family'], 1.6, BEIGE, 'beige'),
        ('produkt', SETS['Bunny'], 1.6, BLUSH, 'pink'), ('produkt', SETS['Forest Bear'], 1.6, BEIGE, 'beige'),
        ('produkt', SETS['Born in 2027'], 1.6, BLUSH, 'pink'), ('produkt', SETS['I love Dogs'], 1.6, BEIGE, 'beige')],
        [(0, None, ['pink or beige?'], '👇', 300, DUN)], CS_KARTE(['Little Princess', 'Best Family', 'Bunny', 'Forest Bear']), blende=0.15)


def tag05_reel_sneak_peek():
    video(1, 'tag05_reel_sneak_peek', [
        ('clip', R5('20_best_family_lachen.mp4'), 1.0, 3.4), ('clip', ARCH['little_princess'], 4.0, 6.4),
        ('clip', R5('08_happy_baby.mp4'), 3.0, 5.4), ('clip', ARCH['smile_gruen'], 5.0, 7.4),
        ('clip', VELOURS('clip_strampeln.mp4'), 4.0, 6.8)],
        [(0, 3.2, ["they'll only be", 'this little once'], '🥹', 1420, POV), (8.6, None, ['coming soon'], '🤍', 1420, POV)],
        CS_KARTE(['Best Family', 'Farm', 'Little Princess', 'Bunny']))


def tag06_tiktok_packing():
    video(1, 'tag06_tiktok_packing', [
        ('clip', HAENDE('Hand_placing_baby_bodysuits_in_202608311030.mp4'), 0.0, 4.0),
        ('breit', HAENDE('weihnachtsbox_mummy_b_bearbeitet.mp4'), 0.5, 7.0)],
        [(0, 3.2, ["POV: you're packing the", 'sweetest baby gift'], '🎀', 300, POV), (8.0, None, ['packing something special'], '🎀', 330, POV)],
        CS_KARTE(MAIN4))


def tag07_tiktok_first_smile():
    video(1, 'tag07_tiktok_first_smile', [
        ('clip', BEST_FAMILY('baby_clip_a.mp4'), 0.4, 3.0), ('clip', R5('25_happy_baby_b.mp4'), 1.0, 3.6),
        ('clip', R5('35_born_in_2027_blau.mp4'), 0.5, 3.0), ('clip', VELOURS('clip_strecken.mp4'), 5.0, 7.8)],
        [(0, 3.2, ['for all the memories', "you'll want to keep", 'forever'], '🤍', 1380, POV), (7.4, None, ['little moments.', 'big love.'], '🤍', 1420, POV)],
        CS_KARTE(['Best Family', 'Farm', 'Born in 2027', 'Little Princess']))


def tag08_tiktok_bodysuits():
    video(2, 'tag08_tiktok_bodysuits', [
        ('bild', TEIL('best_family', 'body'), 2.2, 1.0, 1.2, 0.5, 0.5), ('bild', TEIL('best_family', 'body'), 1.8, 2.3, 2.7, 0.5, 0.42),
        ('bild', TEIL('love_dad_mom', 'body'), 2.0, 1.0, 1.15, 0.5, 0.5), ('bild', TEIL('prinzessin_krone', 'body'), 2.0, 1.0, 1.15, 0.5, 0.5),
        ('bild', TEIL('wal_blau', 'body'), 2.0, 1.0, 1.15, 0.5, 0.5)],
        [(0, 3.2, ['basic? no. this is', "your baby's new", 'favourite bodysuit'], '🤍', 1460, POV), (7.4, None, ['100% cotton,', 'snap buttons'], '🤍', 1500, POV)],
        CS_KARTE(['Best Family', 'I love Dad Mom', 'Little Princess', 'Whale']))


def tag09_tiktok_which_one():
    video(2, 'tag09_tiktok_which_one', [
        ('produkt', SETS['Best Family'], 1.8, BEIGE, None, 1), ('produkt', SETS['Little Princess'], 1.8, BLUSH, None, 2),
        ('produkt', SETS['Whale'], 1.8, (220, 230, 238), None, 3), ('produkt', SETS['Bunny'], 1.8, (240, 226, 232), None, 4),
        ('raster', [SETS[n] for n in ['Best Family', 'Little Princess', 'Whale', 'Bunny']], 2.6, CREME)],
        [(0, None, ['which one would you choose?'], '👇', 1660, DUN)], CS_KARTE(MAIN4), blende=0.15)


def tag10_reel_new_outfits():
    namen = ['Best Family', 'Little Princess', 'Polar Bear', 'Bunny', 'Whale', 'I love Dogs']
    video(2, 'tag10_reel_new_outfits', [('produkt', SETS[n], 1.5, PASTELL[k % len(PASTELL)], n) for k, n in enumerate(namen)],
          [(0, 3.0, ['why are tiny clothes', 'SO cute?'], '🥹', 300, DUN), (7.0, None, ['coming soon'], '✨', 300, DUN)],
          CS_KARTE(namen))


def tag11_tiktok_gift_wrap():
    video(2, 'tag11_tiktok_gift_wrap', [('breit', HAENDE('weihnachtsbox_mummy_a_bearbeitet.mp4'), 0.5, 10.5)],
          [(0, 3.2, ['looking for a gift that', 'truly comes from', 'the heart?'], '🎀', 1460, POV), (7.6, None, ['the sweetest gift', 'for a new arrival'], '🤍', 1500, POV)],
          CS_KARTE(MAIN4))


def tag12_tiktok_unboxing():
    video(2, 'tag12_tiktok_unboxing', [('clip', HAENDE('–_Unboxing_Set_auslegen_Sto.mp4'), 0.3, 9.8)],
          [(0, 3.2, ["POV: you're pregnant", 'and discover sunnozy'], '🥹', 1500, POV), (7.0, None, ['everything in one set'], '✨', 1500, POV)],
          CS_KARTE(MAIN4))


def countdown(woche, name, zeile):
    namen = ['Best Family', 'Little Princess', 'Bunny', 'Whale', 'Polar Bear', 'I love Dogs', 'Farm', 'Born in 2027']
    video(woche, name, [('produkt', SETS[n], 0.8, PASTELL[k % len(PASTELL)]) for k, n in enumerate(namen)],
          [(0, None, zeile, '⏳', 300, DUN)], CS_KARTE(namen[:4], 'launching ' + LAUNCH_TXT), blende=0.1)


def tag14_tiktok_countdown():
    countdown(2, 'tag14_tiktok_countdown', ['2 weeks to go'])


def tag15_reel_collection():
    namen = list(SETS)[:12]
    video(3, 'tag15_reel_collection', [('produkt', SETS[n], 0.7, PASTELL[k % len(PASTELL)]) for k, n in enumerate(namen)],
          [(0, 3.0, ['the cutest baby outfits', "you'll see today"], '🤍', 300, DUN), (3.0, None, ['the new collection', f'launching {LAUNCH_TXT}'], '🤍', 300, DUN)], CS_KARTE(namen[:4], 'the new collection'), blende=0.1)


def tag16_tiktok_gift_ideas():
    video(3, 'tag16_tiktok_gift_ideas', [
        ('produkt', SETS['Little Princess'], 2.4, BLUSH, 'for a little girl'), ('produkt', SETS['Whale'], 2.4, (220, 230, 238), 'for a little boy'),
        ('produkt', SETS['Best Family'], 2.4, BEIGE, 'for every little one')],
        [(0, None, ['the perfect gift for', 'a newborn? found it'], '🎁', 280, DUN)], CS_KARTE(['Little Princess', 'Whale', 'Best Family', 'Bunny']))


def tag17_tiktok_best_family():
    video(3, 'tag17_tiktok_best_family', [
        ('clip', BEST_FAMILY('baby_clip_b.mp4'), 0.8, 3.6), ('produkt', SETS['Best Family'], 2.2, BEIGE, '«Best Family» · 8 pieces'),
        ('clip', R5('20_best_family_lachen.mp4'), 1.0, 3.8)],
        [(0, 2.5, ['when your baby already', 'has more style than you'], '🧸', 1420, POV)], CS_KARTE(['Best Family', 'Little Princess', 'Bunny', 'Whale']))


def tag18_reel_whats_inside():
    teile = [('strampler', 'romper'), ('body', 'bodysuit'), ('muetze', 'hat'), ('kapuzentuch', 'hooded towel'),
             ('laetzchen', 'bib'), ('rassel', 'rattle'), ('faeustlinge', 'mittens'), ('socken', 'socks')]
    video(3, 'tag18_reel_whats_inside', [('produkt', TEIL('best_family', t), 1.0, CREME, f'{k + 1}/8  {n}') for k, (t, n) in enumerate(teile)]
          + [('produkt', SETS['Best Family'], 2.0, BEIGE, '8 pieces, one set')],
          [(0, 2.6, ['mama, this set belongs', "in your baby's wardrobe"], '🧸', 300, DUN)], CS_KARTE(['Best Family', 'Little Princess', 'Bunny', 'Whale']), blende=0.12)


def tag19_tiktok_3_details():
    video(3, 'tag19_tiktok_3_details', [
        ('bild', TEIL('best_family', 'body'), 2.4, 2.6, 3.0, 0.5, 0.6), ('bild', TEIL('best_family', 'strampler'), 2.4, 2.6, 3.0, 0.5, 0.3),
        ('produkt', SETS['Best Family'], 2.4, BEIGE)],
        [(0, 1.2, ["3 reasons you'll love", 'this baby set'], '🤍', 1500, POV), (1.2, 2.3, ['1. 100% soft cotton'], None, 1500, POV), (2.4, 4.6, ['2. snap buttons for', 'quick changes'], None, 1500, POV),
         (4.8, None, ['3. everything', 'in one set'], '🤍', 1500, POV)], CS_KARTE(['Best Family', 'Little Princess', 'Bunny', 'Whale']))


def tag20_tiktok_velours():
    video(3, 'tag20_tiktok_velours', [
        ('bild', VELOURS_FOTO, 2.4, 1.0, 1.1, 0.48, 0.45), ('clip', VELOURS('clip_strampeln.mp4'), 4.0, 6.6),
        ('bild', VELOURS_FOTO, 1.8, 2.2, 2.4, 0.5, 0.3), ('clip', VELOURS('clip_strecken.mp4'), 5.0, 7.6)],
        [(0, 3.0, ['if love were an outfit…'], '🤍', 1500, POV), (6.6, None, ['soft velvet,', 'little ruffles'], '✨', 1500, POV)],
        (VELOURS_FOTO, 'romper «Velours»', 'coming soon', CS_AUFRUF))


def tag21_tiktok_countdown():
    countdown(3, 'tag21_tiktok_countdown', [f'{(LAUNCH - START - datetime.timedelta(days=20)).days} days to go'])


def tag22_reel_full_collection():
    namen = list(SETS)[:12]
    video(4, 'tag22_reel_full_collection', [('raster', [SETS[n] for n in namen], 6.5, CREME, ['the full collection', f'launching {LAUNCH_TXT}'])],
          [(0, 2.8, ['POV: you only wanted', 'to buy ONE outfit…'], '🙈', 160, DUN)], CS_KARTE(namen[:4], 'the full collection'))


def tag25_reel_favourite_outfits():
    video(4, 'tag25_reel_favourite_outfits', [
        ('clip', R5('25_happy_baby_b.mp4'), 1.0, 3.2), ('clip', ARCH['smile_gruen'], 5.0, 7.2), ('clip', ARCH['weltall'], 6.0, 8.2),
        ('clip', ARCH['little_princess'], 4.0, 6.2), ('clip', R5('20_best_family_lachen.mp4'), 1.0, 3.6)],
        [(0, 3.0, ['mama, please don\'t buy', 'another baby outfit…'], '🙈', 1420, POV), (8.0, None, ['tell us in the comments'], '👇', 1420, POV)],
        CS_KARTE(['Farm', 'Best Family', 'Little Princess', 'Bunny']))


def tag26_tiktok_countdown():
    countdown(4, 'tag26_tiktok_countdown', ['launching tomorrow'])


def tag30_tiktok_best_of():
    video(4, 'tag30_tiktok_best_of', [
        ('clip', R5('20_best_family_lachen.mp4'), 1.0, 3.0), ('produkt', SETS['Little Princess'], 1.2, BLUSH),
        ('clip', ARCH['smile_gruen'], 5.0, 7.0), ('produkt', SETS['Whale'], 1.2, (220, 230, 238)),
        ('bild', VELOURS_FOTO, 1.6, 1.0, 1.1, 0.48, 0.45), ('clip', R5('08_happy_baby.mp4'), 3.0, 5.0)],
        [(0, 3.0, ['they grow so fast.', 'thank you for being', 'part of these moments'], '🤍', 1380, POV)], LIVE_KARTE(MAIN4))


VIDEOS = [tag01_reel_teaser, tag02_tiktok_getting_ready, tag03_tiktok_details, tag04_tiktok_pink_or_beige, tag05_reel_sneak_peek,
          tag06_tiktok_packing, tag07_tiktok_first_smile, tag08_tiktok_bodysuits, tag09_tiktok_which_one, tag10_reel_new_outfits,
          tag11_tiktok_gift_wrap, tag12_tiktok_unboxing, tag14_tiktok_countdown, tag15_reel_collection, tag16_tiktok_gift_ideas,
          tag17_tiktok_best_family, tag18_reel_whats_inside, tag19_tiktok_3_details, tag20_tiktok_velours, tag21_tiktok_countdown,
          tag22_reel_full_collection, tag25_reel_favourite_outfits, tag26_tiktok_countdown, tag30_tiktok_best_of]


# ---------- Fotos und Storys ----------
def still(p, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', p, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                         capture_output=True, check=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert('RGB')


def story_kopf(c, zeilen, emo=None, y=330, g=60):
    text(c, zeilen, y, g, DUNKEL, emo)


def bilder():
    # Tag 2 – Story: coming soon (unscharfe Vorschau)
    c = leinwand('9x16', BLUSH); g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for k, n in enumerate(MAIN4):
        im = einpassen(laden(SETS[n]), 440, 440).convert('RGBA')
        g.alpha_composite(im, (80 + (k % 2) * 480 + (440 - im.width) // 2, 640 + (k // 2) * 480 + (440 - im.height) // 2))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    story_kopf(c, ['new little treasures', 'are coming soon'], '🤍', 330)
    text(c, ["turn on notifications so", "you don't miss the launch"], 1660, 40, GRAU); logo(c, 1760)
    speichern(c, 1, 'tag02_story_coming_soon')
    # Tag 3 – Foto: Details 2×2
    c = leinwand('4x5', CREME)
    for k, (p, fx, fy, z) in enumerate([(TEIL('best_family', 'body'), 0.5, 0.42, 2.6), (TEIL('prinzessin_krone', 'body'), 0.5, 0.45, 2.4),
                                        (VELOURS_FOTO, 0.24, 0.43, 2.8), (TEIL('hase_rosa', 'body'), 0.5, 0.45, 2.4)]):
        c.alpha_composite(fuellen(laden(p), 470, 470, fx, fy, z).convert('RGBA'), (60 + (k % 2) * 490, 150 + (k // 2) * 490))
    text(c, ['little details, lots of love'], 1190, 44, DUNKEL, '🤍'); logo(c, 1250, 190)
    speichern(c, 1, 'tag03_post_details')
    # Tag 4 – Story-Umfrage: pink or beige?
    c = leinwand('9x16', CREME)
    c.alpha_composite(Image.new('RGBA', (W, 820), BLUSH + (255,)), (0, 180)); c.alpha_composite(Image.new('RGBA', (W, 820), BEIGE + (255,)), (0, 1000))
    karte(c, SETS['Little Princess'], W / 2, 590, 700, 640, schatten=False); karte(c, SETS['Best Family'], W / 2, 1410, 700, 640, schatten=False)
    text(c, ['pink or beige?'], 110, 60, DUNKEL, '🤍')
    text(c, ['(add the poll sticker here)'], 1000, 30, GRAU)
    speichern(c, 1, 'tag04_story_pink_or_beige')
    # Tag 6 – Story: getting ready
    c = leinwand('9x16', BEIGE); karte(c, VELOURS_FOTO, W / 2, 980, 820, 900)
    story_kopf(c, ['getting everything', 'ready for you'], '🤍', 260); text(c, ['new pieces coming soon'], 1560, 42, GRAU); logo(c, 1680)
    speichern(c, 1, 'tag06_story_getting_ready')
    # Tag 7 – Foto: Markenbotschaft mit lachendem Baby (wach)
    c = leinwand('4x5', CREME)
    c.alpha_composite(fuellen(still(R5('20_best_family_lachen.mp4'), 2.0), 1080, 1040, 0.5, 0.42).convert('RGBA'), (0, 0))
    text(c, ['Little moments. Big love.'], 1140, 52, DUNKEL, '🤍'); logo(c, 1215, 200)
    speichern(c, 1, 'tag07_post_little_moments')
    # Tag 8 – Foto: Bodysuit
    c = leinwand('4x5', BEIGE); karte(c, TEIL('best_family', 'body'), 540, 600, 860, 860)
    text(c, ['the «Best Family» bodysuit'], 1110, 46, DUNKEL); text(c, ['100% cotton · snap buttons · coming soon'], 1180, 30, GRAU)
    logo(c, 1240, 180); speichern(c, 2, 'tag08_post_bodysuit')
    # Tag 9 – Story: which design?
    c = leinwand('9x16', CREME)
    for k, n in enumerate(MAIN4):
        x, y = 70 + (k % 2) * 480, 500 + (k // 2) * 560
        c.alpha_composite(Image.new('RGBA', (460, 520), PASTELL[k] + (255,)), (x, y))
        karte(c, SETS[n], x + 230, y + 250, 400, 400, schatten=False); text(c, [str(k + 1)], y + 40, 52, DUNKEL, x=x + 24)
    story_kopf(c, ['which design is', 'your favourite?'], '👇', 260); text(c, ['vote with the number in the comments'], 1660, 34, GRAU)
    speichern(c, 2, 'tag09_story_which_design')
    # Tag 11 – Story: gift
    c = leinwand('9x16', BLUSH); c.alpha_composite(fuellen(still(HAENDE('weihnachtsbox_mummy_a_bearbeitet.mp4'), 6.0), 940, 1120).convert('RGBA'), (70, 470))
    story_kopf(c, ['the sweetest gift', 'for a new arrival'], '🎀', 260); text(c, ['our gift boxes · link in bio'], 1680, 40, GRAU)   # Box «I love my Mummy» ist schon im Shop
    speichern(c, 2, 'tag11_story_gift')
    # Tag 12 – Foto: Geschenkset
    c = leinwand('4x5', CREME); karte(c, HAUPT('prinzessin_krone'), 540, 610, 900, 900)
    text(c, ['a little gift.', 'a lifetime of memories.'], 1130, 44, DUNKEL, '🎀'); text(c, ['8-piece newborn set · coming soon'], 1250, 30, GRAU)
    speichern(c, 2, 'tag12_post_gift_set')
    # Countdown-Storys
    for woche, name, gross, klein in [(2, 'tag14_story_two_weeks', '2 weeks', 'to go'),
                                      (3, 'tag21_story_countdown', f'{(LAUNCH - START - datetime.timedelta(days=20)).days} days', 'to go'),
                                      (4, 'tag26_story_tomorrow', 'tomorrow', 'is launch day')]:
        c = leinwand('9x16', BLUSH)
        for k, n in enumerate(['Best Family', 'Little Princess', 'Bunny']):
            im = einpassen(laden(SETS[n]), 300, 300).convert('RGBA'); c.alpha_composite(im, (60 + k * 330 + (300 - im.width) // 2, 1250 + (300 - im.height) // 2))
        text(c, [gross], 640, 120, DUNKEL); text(c, [klein], 790, 56, DUNKEL, '⏳' if 'to go' in klein else '🤍')
        text(c, [f'new collection · {LAUNCH_TXT}'], 950, 40, GRAU); text(c, ['add a countdown sticker'], 1700, 30, GRAU)
        speichern(c, woche, name)
    # Tag 16 / 29 – Story: gift ideas
    for woche, name, unten in [(3, 'tag16_story_gift_ideas', 'coming soon'), (4, 'tag29_story_gift_ideas', 'now live · link in bio')]:
        c = leinwand('9x16', CREME)
        for k, (n, lab, bg) in enumerate([('Little Princess', 'for a little girl', BLUSH), ('Whale', 'for a little boy', (220, 230, 238)),
                                          ('Best Family', 'for every little one', BEIGE)]):
            y = 420 + k * 430; c.alpha_composite(Image.new('RGBA', (940, 400), bg + (255,)), (70, y))
            karte(c, SETS[n], 330, y + 200, 470, 360, schatten=False); text(c, [lab], y + 200, 38, DUNKEL, x=600)
        story_kopf(c, ['gift ideas', 'for newborns'], '🎁', 210); text(c, [unten], 1760, 38, GRAU)
        speichern(c, woche, name)
    # Tag 17 – Foto: komplettes Outfit
    c = leinwand('4x5', BEIGE); karte(c, HAUPT('hase_rosa'), 540, 610, 900, 900)
    text(c, ['a complete first outfit,', 'all in one set'], 1130, 44, DUNKEL, '🤍'); text(c, ['«Bunny» · 8 pieces · coming soon'], 1250, 30, GRAU)
    speichern(c, 3, 'tag17_post_outfit')
    # Tag 19 – Story: why you'll love it (Fakten aus der Shopify-Beschreibung)
    c = leinwand('9x16', CREME); karte(c, SETS['Best Family'], W / 2, 640, 760, 600)
    story_kopf(c, ["why you'll love it"], '🤍', 200)
    for k, z in enumerate(['100% soft cotton', 'snap buttons for quick changes', '8 pieces in one set', 'washable at 30 °C']):
        text(c, ['•  ' + z], 1100 + k * 110, 44, DUNKEL, x=120)
    text(c, ['«Best Family» · coming soon'], 1640, 36, GRAU); logo(c, 1740)
    speichern(c, 3, 'tag19_story_benefits')
    # Tag 20 – Foto: Lieblingsstück Velours
    c = leinwand('4x5', CREME); c.alpha_composite(fuellen(laden(VELOURS_FOTO), 1080, 1040, 0.5, 0.45).convert('RGBA'), (0, 0))
    text(c, ['our favourite: the «Velours» romper'], 1120, 38, DUNKEL, '🤍'); text(c, ['soft velvet · puff sleeves · coming soon'], 1200, 30, GRAU)
    logo(c, 1255, 170); speichern(c, 3, 'tag20_post_favourite')
    # Tag 23 – Foto-Karussell mit Shop-Hinweis
    for k, (n, haupt, bg) in enumerate([('Best Family', 'best_family', BEIGE), ('Little Princess', 'prinzessin_krone', BLUSH), ('Whale', 'wal_blau', (220, 230, 238))]):
        c = leinwand('4x5', bg); karte(c, HAUPT(haupt), 540, 600, 880, 880)
        text(c, [f'«{n}» · 8 pieces'], 1120, 46, DUNKEL); text(c, [f'available from {LAUNCH_TXT} · link in bio'], 1200, 30, GRAU)
        speichern(c, 4, f'tag23_post_karussell_{k + 1}')
    # Tag 24 – Story: gift sets
    c = leinwand('9x16', BLUSH)
    for k, n in enumerate(['Little Princess', 'Best Family', 'Bunny', 'Whale']):
        im = einpassen(laden(SETS[n]), 440, 440).convert('RGBA'); c.alpha_composite(im, (80 + (k % 2) * 480 + (440 - im.width) // 2, 560 + (k // 2) * 480 + (440 - im.height) // 2))
    story_kopf(c, ['our newborn sets', 'make the sweetest gift'], '🎀', 260); text(c, [f'launching {LAUNCH_TXT}'], 1620, 40, GRAU); logo(c, 1720)
    speichern(c, 4, 'tag24_story_gift_sets')
    # Tag 27 – Launch: Post und Story
    c = leinwand('4x5', CREME)
    for k, n in enumerate(MAIN4):
        im = einpassen(laden(SETS[n]), 440, 400).convert('RGBA'); c.alpha_composite(im, (90 + (k % 2) * 470 + (440 - im.width) // 2, 140 + (k // 2) * 430 + (400 - im.height) // 2))
    text(c, ["IT'S HERE"], 1060, 70, DUNKEL, '🌸🤍'); text(c, ['the new collection is live · link in bio'], 1160, 30, GRAU); logo(c, 1220, 190)
    speichern(c, 4, 'tag27_post_launch')
    c = leinwand('9x16', BLUSH)
    for k, n in enumerate(MAIN4):
        im = einpassen(laden(SETS[n]), 440, 440).convert('RGBA'); c.alpha_composite(im, (80 + (k % 2) * 480 + (440 - im.width) // 2, 560 + (k // 2) * 480 + (440 - im.height) // 2))
    text(c, ["IT'S HERE"], 300, 90, DUNKEL, '🌸'); text(c, ['the new collection is live'], 420, 46, DUNKEL, '🤍')
    text(c, ['tap the link sticker to shop'], 1640, 36, GRAU); logo(c, 1740)
    speichern(c, 4, 'tag27_story_launch')
    # Tag 28 – Foto: Highlights
    c = leinwand('4x5', BEIGE)
    for k, n in enumerate(['Best Family', 'Little Princess', 'Bunny', 'I love Dogs']):
        x, y = 60 + (k % 2) * 490, 120 + (k // 2) * 470; c.alpha_composite(Image.new('RGBA', (470, 450), CREME + (255,)), (x, y))
        karte(c, SETS[n], x + 235, y + 205, 400, 360, schatten=False); text(c, [n], y + 420, 28, GRAU, x=x + 20)
    text(c, ['our 8-piece newborn sets'], 1100, 46, DUNKEL, '🤍'); text(c, ['now live · link in bio'], 1180, 32, GRAU); logo(c, 1240, 180)
    speichern(c, 4, 'tag28_post_highlights')
    # Tag 30 – Danke-Post
    c = leinwand('4x5', BLUSH); karte(c, VELOURS_FOTO, 540, 520, 700, 700)
    text(c, ['thank you'], 1000, 80, DUNKEL, '🤍'); text(c, ['for every like, share and order.', 'little moments. big love.'], 1110, 34, DUNKEL)
    logo(c, 1230, 190); speichern(c, 4, 'tag30_post_thank_you')


if __name__ == '__main__':
    wahl = sys.argv[1:] or ['bilder', 'videos']
    for w in wahl:
        if w == 'bilder':
            bilder()
        elif w == 'videos':
            for v in VIDEOS:
                v()
        elif w == 'ab':                      # python3 … ab tag05_reel_sneak_peek: ab diesem Video weiter
            pass
        else:
            globals()[w]()
