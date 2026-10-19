"""sunnozy Trend-Content: Hook-Texte, Meme, Notizen-App, Tweet-Stil, POV-Reel-Frames.

Aufruf: python3 make_trend.py <logo.webp> <ordner mit baby-fotos> <ausgabeordner>
"""
import sys, os, math, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import instagram_schrift  # noqa: F401  Hausschrift Sacramento fuer alle Instagram-Posts (nicht Anzeigen)
import numpy as np

logo_src, photo_dir, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
W, H = 1080, 1350
SB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SER = '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
TERRA, INK, CREAM = (181, 72, 63), (25, 25, 25), (252, 249, 246)
EMOJI_RE = re.compile('([\U0001F000-\U0001FAFF☀-➿⭐❤️‍\U0001F1E6-\U0001F1FF]+)')
_emo = ImageFont.truetype(EMO, 109)


# ---------- Text mit Farb-Emojis ----------
def runs(text):
    return [(p, bool(EMOJI_RE.fullmatch(p))) for p in EMOJI_RE.split(text) if p]


def emoji_img(e, size):
    tmp = Image.new('RGBA', (len(e) * 140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), e, font=_emo, embedded_color=True)
    tmp = tmp.crop(tmp.getbbox() or (0, 0, 1, 1))
    s = size / 109 * 0.95
    return tmp.resize((max(1, int(tmp.width * s)), max(1, int(tmp.height * s))), Image.LANCZOS)


def line_width(d, text, f):
    w = 0
    for p, is_e in runs(text):
        w += emoji_img(p, f.size).width + 4 if is_e else d.textlength(p, font=f)
    return w


def draw_line(img, x, y, text, f, fill):
    d = ImageDraw.Draw(img)
    for p, is_e in runs(text):
        if is_e:
            em = emoji_img(p, f.size); img.paste(em, (int(x), int(y + f.size * 0.08)), em); x += em.width + 4
        else:
            d.text((x, y), p, font=f, fill=fill); x += d.textlength(p, font=f)


def wrap(d, text, f, maxw):
    out_, cur = [], ''
    for word in text.split(' '):
        t = (cur + ' ' + word).strip()
        if line_width(d, t, f) <= maxw: cur = t
        else: out_.append(cur); cur = word
    return out_ + [cur]


def text_block(img, text, f, fill, y, maxw, align='center', lh=1.25, x0=None, box=None, pad=22, radius=18):
    """Mehrzeiliger Text; box=(r,g,b) zeichnet TikTok-artige Hintergrundboxen pro Zeile."""
    d = ImageDraw.Draw(img)
    lines = []
    for para in text.split('\n'):
        lines += wrap(d, para, f, maxw) if para else ['']
    for ln in lines:
        w = line_width(d, ln, f)
        x = (img.width - w) / 2 if align == 'center' else x0
        if box and ln:
            d.rounded_rectangle([x - pad, y - pad * 0.55, x + w + pad, y + f.size * 1.18 + pad * 0.45], radius, fill=box)
        if ln: draw_line(img, x, y, ln, f, fill)
        y += int(f.size * lh) + (int(pad * 0.9) if box else 0)
    return y


# ---------- Bild-Helfer ----------
def knockout(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.15, 0, 1); al[al < 0.06] = 0
    rgb = np.where(al[..., None] > 0, (a - 255 * (1 - al[..., None])) / np.maximum(al[..., None], 1e-3), 0)
    L = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al * 255]).astype(np.uint8), 'RGBA')
    return L.crop(L.getbbox())


LOGO = knockout(logo_src)


def logo(width, white=False):
    L = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if white:
        a = np.asarray(L).astype(float); a[a[..., :3].max(axis=2) < 90, :3] = 255
        L = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return L


def fill(img, w, h, ay=0.5):
    s = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, int((im.height - h) * ay)
    return im.crop((x, y, x + w, y + h))


def shade(img, top=0.0, bottom=0.55):
    """Dunkler Verlauf fuer lesbaren weissen Text."""
    g = np.linspace(top, bottom, img.height)[:, None, None]
    a = np.asarray(img.convert('RGB')).astype(float) * (1 - g)
    return Image.fromarray(a.astype(np.uint8))


def handle(img, white=True, y=None):
    f = ImageFont.truetype(SB, 30)
    d = ImageDraw.Draw(img); t = '@sunnozy.ch'
    d.text(((img.width - d.textlength(t, font=f)) / 2, y or img.height - 70), t, font=f,
           fill=(255, 255, 255) if white else INK)


def save(img, name):
    img.convert('RGB').save(os.path.join(out, name), quality=93)


P = {k: Image.open(os.path.join(photo_dir, k + '.jpg')).convert('RGB') for k in ('yellow', 'pink', 'lila', 'cream')}
F = lambda p, s: ImageFont.truetype(p, s)

# ===== 1) Meme: Erwartung vs. Realitaet =====
m = Image.new('RGB', (W, H), 'white')
top = fill(P['cream'], W, H // 2, 0.4); bot = fill(P['pink'], W, H // 2, 0.25)
m.paste(top, (0, 0)); m.paste(bot, (0, H // 2))
ImageDraw.Draw(m).rectangle([0, H // 2 - 3, W, H // 2 + 3], fill='white')
text_block(m, 'Erwartung:', F(SB, 50), INK, 40, 900, box=(255, 255, 255))
text_block(m, 'Ich ziehe ihr EIN süsses Outfit an ✨', F(SB, 44), INK, 470, 900, box=(255, 255, 255))
text_block(m, 'Realität:', F(SB, 50), INK, H // 2 + 40, 900, box=(255, 255, 255))
text_block(m, 'Outfit Nr. 4 und es ist 9:30 Uhr 😅', F(SB, 44), INK, H - 150, 900, box=(255, 255, 255))
save(m, 'meme_erwartung_realitaet.jpg')

# ===== 2) Notizen-App-Karussell =====
NOTE_BG, NOTE_Y = (255, 253, 247), (224, 161, 0)


def note_page(title=None, items=(), footer=None, photo=None):
    s = Image.new('RGB', (W, H), NOTE_BG); d = ImageDraw.Draw(s)
    d.text((60, 60), '‹ Notizen', font=F(SR, 40), fill=NOTE_Y)
    d.text((W - 200, 60), 'Fertig', font=F(SB, 40), fill=NOTE_Y)
    y = 200
    if title:
        y = text_block(s, title, F(SB, 64), INK, y, 960, align='left', x0=60, lh=1.18) + 30
    if photo is not None:
        ph = fill(photo, 560, 560, 0.35).rotate(-3, expand=True, fillcolor=NOTE_BG)
        pol = Image.new('RGB', (620, 700), 'white'); pol.paste(fill(photo, 560, 560, 0.35), (30, 30))
        ImageDraw.Draw(pol).text((40, 615), 'die ersten Wochen 🤍'.replace(' 🤍', ''), font=F(SER, 44), fill=(90, 90, 90))
        pol = pol.rotate(-3, expand=True, fillcolor=NOTE_BG)
        sh = Image.new('RGBA', pol.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 60), (0, 0, pol.width, pol.height))
        s.paste(pol, ((W - pol.width) // 2, y + 10))
    for it in items:
        y = text_block(s, it, F(SR, 58), INK, y, 940, align='left', x0=70, lh=1.3) + 60
    if footer:
        text_block(s, footer, F(SB, 40), TERRA, H - 150, 960)
    d.text((60, H - 60), '@sunnozy.ch', font=F(SR, 26), fill=(160, 160, 160))
    return s


save(note_page('Dinge, die mir niemand über die ersten Wochen gesagt hat 🫶', photo=P['yellow']), 'notizen_01_cover.jpg')
save(note_page(items=['1. Du ziehst dein Baby 3x am Tag um. Body, Body, Body 🙃',
                      '2. Wickelbodys > alles, was über den Kopf muss',
                      '3. Mulltücher sind immer genau da, wo du sie NICHT brauchst']), 'notizen_02.jpg')
save(note_page(items=['4. Du machst Hunderte Fotos von schlafenden Füsschen 📸',
                      '5. Kalter Kaffee wird dein Lieblingsgetränk ☕',
                      '6. Grösse 50 passt oft nur 2–3 Wochen. Wirklich.']), 'notizen_03.jpg')
save(note_page(items=['7. Du wirst weinen. Vor Glück, vor Müdigkeit, wegen einer Werbung 🥹',
                      '8. Hilfe annehmen ist kein Versagen 🤍'],
               footer='Schick das einer werdenden Mama 📌'), 'notizen_04.jpg')

# ===== 3) Hook-Karussell: Tipps mit grossen Texten auf Vollbild =====
def hook_slide(photo, ay, big, small=None, kicker=None, bottom=True):
    s = shade(fill(photo, W, H, ay), 0.05 if bottom else 0.5, 0.62 if bottom else 0.1)
    y = 700 if bottom else 140
    if kicker: y = text_block(s, kicker, F(SB, 36), (255, 220, 200), y, 900) + 10
    y = text_block(s, big, F(SB, 82), (255, 255, 255), y, 940, lh=1.12) + 20
    if small: text_block(s, small, F(SR, 40), (255, 255, 255), y, 900)
    handle(s)
    return s


save(hook_slide(P['lila'], 0.4, 'Stopp ✋ Bevor du die Erstausstattung kaufst …', 'Diese 5 Dinge brauchst du wirklich 👉'), 'tipps_01_hook.jpg')
save(hook_slide(P['yellow'], 0.4, '1. Wickelbodys statt Überkopf', 'Neugeborene mögen nichts über dem Gesicht. Druckknöpfe = weniger Tränen 🥹', '5–7 STÜCK'), 'tipps_02.jpg')
save(hook_slide(P['pink'], 0.4, '2. Hosen mit weichem Bund', 'Nichts, was am Bäuchlein drückt. Ripp dehnt sich mit ☁️', '4–5 STÜCK'), 'tipps_03.jpg')
save(hook_slide(P['cream'], 0.4, '3. Mützchen, Söckchen, Handschuhe', 'Kleine Füsse kühlen schnell aus. Und die Fingernägel sind scharf 😅', 'JE 2'), 'tipps_04.jpg')
s = hook_slide(P['lila'], 0.75, '4. Mulltücher. Viele. 5. Eine Grösse grösser.', 'Grösse 50 ist schneller vorbei, als du denkst.', '3–6 STÜCK')
save(s, 'tipps_05.jpg')
e = Image.new('RGB', (W, H), CREAM)
L = logo(620); e.paste(L, ((W - L.width) // 2, 380), L)
text_block(e, 'Speichern 📌 und an eine werdende Mama schicken', F(SB, 58), INK, 720, 900, lh=1.2)
text_block(e, 'Alles davon gibt es bei sunnozy.ch 🇨🇭', F(SR, 40), TERRA, 1000, 900)
save(e, 'tipps_06_cta.jpg')

# ===== 4) Mama-Moment: grosses Zitat auf Vollbild =====
q = shade(fill(P['yellow'], W, H, 0.6), 0.55, 0.05)
text_block(q, 'Niemand hat mir gesagt, wie sehr ich diese kleinen Füsse lieben werde. 🥹', F(SB, 76), (255, 255, 255), 150, 920, lh=1.18)
handle(q)
save(q, 'mama_moment_fuesse.jpg')

# ===== 5) Tweet-Stil =====
bg = fill(P['lila'], W, H, 0.4).filter(ImageFilter.GaussianBlur(28))
bg = Image.blend(bg, Image.new('RGB', (W, H), (255, 255, 255)), 0.25)
d = ImageDraw.Draw(bg)
cx0, cy0, cx1 = 70, 330, W - 70
card = Image.new('RGB', (cx1 - cx0, 640), 'white'); cd = ImageDraw.Draw(card)
av = Image.new('RGB', (110, 110), (247, 234, 228)); al = logo(96); av.paste(al, (7, (110 - al.height) // 2), al)
mk = Image.new('L', (110, 110), 0); ImageDraw.Draw(mk).ellipse([0, 0, 110, 110], fill=255)
card.paste(av, (40, 40), mk)
cd.text((170, 48), 'sunnozy', font=F(SB, 40), fill=INK)
draw_line(card, 170 + cd.textlength('sunnozy ', font=F(SB, 40)), 48, '🇨🇭', F(SB, 40), INK)
cd.text((170, 100), '@sunnozy.ch', font=F(SR, 32), fill=(110, 118, 125))
y = text_block(card, 'Babys: wachsen 3 cm in 2 Wochen\nIch: hab Grösse 56 noch nicht mal gewaschen 🙃',
               F(SR, 50), INK, 200, card.width - 90, align='left', x0=45, lh=1.3)
draw_line(card, 45, 560, '🤍 2.408     🔁 312     💬 186', F(SR, 34), (110, 118, 125))
mk2 = Image.new('L', card.size, 0); ImageDraw.Draw(mk2).rounded_rectangle([0, 0, *card.size], 36, fill=255)
bg.paste(card, (cx0, cy0), mk2)
text_block(bg, 'Kennst du das? 👇', F(SB, 54), INK, 1060, 900, box=(255, 255, 255))
save(bg, 'tweet_groesse_56.jpg')

# ===== 6) Story "Rate das Outfit" =====
st = fill(P['lila'], 1080, 1920, 0.4)
text_block(st, 'Rate das Outfit 1–10 🎀', F(SB, 76), INK, 180, 960, box=(255, 255, 255))
text_block(st, '(Platz für den Slider-Sticker)', F(SR, 30), (255, 255, 255), 1600, 900)
save(st, 'story_rate_das_outfit.jpg')

# ===== 7) POV-Reel: Einzelbilder (werden in ffmpeg animiert) =====
reel = [('yellow', 0.35, 'POV: Du ziehst deinem Baby zum ersten Mal sein Lieblings-Set an 🥹', 'top'),
        ('pink', 0.45, 'so weich ☁️', 'bottom'),
        ('lila', 0.35, 'mum · dad · me 🤍', 'bottom'),
        ('cream', 0.4, 'und plötzlich ist alles perfekt ✨', 'bottom')]
for i, (k, ay, txt, pos) in enumerate(reel):
    fr = fill(P[k], 1080, 1920, ay)
    y = 260 if pos == 'top' else 1450
    text_block(fr, txt, F(SB, 68 if pos == 'top' else 64), INK, y, 900, box=(255, 255, 255), lh=1.15)
    fr.convert('RGB').save(os.path.join(out, f'_reel_{i}.png'))

print(sorted(os.listdir(out)))
