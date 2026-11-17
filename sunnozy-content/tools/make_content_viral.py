"""Posts nach der Viral-Analyse der Nutzerin (posts/content-plan/viral-analyse/), nur Produkte im Shop (17.11.2026).

  strecken_emoji   – Neugeborenes streckt sich, ein Take, KEIN Text, nur ein Emoji-Sticker (Format zayac, 2.8 Mio.)
  gotti_box        – «Was ist in der Gotti-Box?» Teil für Teil, Schluss «Preis? Schreib PREIS» (Format zayac «was ist drin»)
  schleifen        – «POV: Du bist besessen von Schleifen 🎀», schnelle Schnitte, Payoff: alles im Raster (Format avalia)
  gewinnspiel      – Bild für ein Weihnachts-Gewinnspiel (ENTWURF, erst nach OK der Nutzerin posten)

    python3 tools/make_content_viral.py [strecken_emoji|gotti_box|schleifen|gewinnspiel]
Ausgabe: posts/content-kw2/viral/ (Captions: README.md dort)
"""
import os, sys
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_content_kw1 as k1
import make_reel_viral_hlb as vh
import make_reel_hello_little_bear_hook as hk

W, H, FPS = m.W, m.H, 30
P = m.POSTS
OUT = os.path.join(P, 'content-kw2', 'viral')
CS = os.path.join(P, 'coming-soon', 'photos')
WEISS = os.path.join(CS, 'shopify-hauptbilder-weiss')
BOX = os.path.join(CS, 'kampagne-weihnachtsbox', 'fotos')
MUSIK = 'alex-morgan_no-copyright-music.mp3'
CREME = (250, 246, 240)


def bild(pfad):
    return Image.open(pfad).convert('RGB')


def karte(c, im, mitte_y, breite, zoom=1.0, fokus=(0.5, 0.5)):
    """Bild zentriert einsetzen; zoom > 1 schneidet um den Fokuspunkt heraus (Ken Burns)."""
    zoom = max(zoom, 1.0); w, h = im.size; cw, ch = w / zoom, h / zoom
    x0 = min(max(fokus[0] * w - cw / 2, 0), w - cw); y0 = min(max(fokus[1] * h - ch / 2, 0), h - ch)
    t = im.resize((breite, round(breite * ch / cw)), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    c.paste(t, ((W - t.width) // 2, int(mitte_y - t.height / 2)))


def text(c, zeilen, y, g=54, emoji=None):
    d = ImageDraw.Draw(c); fo = k1.f(g)
    for k, z in enumerate(zeilen):
        d.text((W / 2, y + k * g * 1.25), z, font=fo, fill=k1.DUNKEL, anchor='mm')
    if emoji:
        e = hk.emoji(emoji, int(g * 0.95)); z = zeilen[-1]
        x = W / 2 + d.textlength(z, font=fo) / 2 + 10; yy = y + (len(zeilen) - 1) * g * 1.25
        c.paste(e, (int(x), int(yy - e.height / 2)), e)


# ---------- 1. Strecken, nur Emoji ----------
def strecken_emoji():
    sticker = hk.emoji('🥹', 150)

    def frames():
        for fr in k1.clip_frames('set_hello_world_blatt_baby_body_2.mp4', 0.0, 10.0):
            c = fr.convert('RGBA'); c.alpha_composite(sticker, (W - sticker.width - 110, 330))
            yield c
    vh.schreiben(os.path.join(OUT, 'reel_strecken_emoji_9x16.mp4'), frames(), 10.0, MUSIK)


# ---------- 2. Was ist in der Gotti-Box? ----------
def gotti_box():
    box = bild(os.path.join(BOX, 'box_mum_dad_me.jpg'))
    szenen = [  # (Dauer, Bild, Zeilen-Label, Emoji, zoom, fokus)
        (2.2, box, None, None, (1.0, 1.08), (0.5, 0.5)),
        (1.7, bild(os.path.join(WEISS, 'mumdadme_langarm5.jpg')), '1/3  5 Bodys «Mum Dad Me»', None, (1.0, 1.05), (0.5, 0.5)),
        (1.7, bild(os.path.join(WEISS, 'leggings5.jpg')), '2/3  5 Leggings mit Schleife', None, (1.0, 1.05), (0.5, 0.5)),
        (1.7, box, '3/3  Karte, fertig verpackt', None, (2.6, 2.6), (0.62, 0.2)),
        (3.4, bild(os.path.join(WEISS, 'kombi_mumdadme.jpg')), None, None, (1.0, 1.0), (0.5, 0.5)),
    ]
    dauer = sum(s[0] for s in szenen)

    def frames():
        n = int(round(dauer * FPS)); t0 = 0; k = 0
        for i in range(n):
            t = i / FPS
            while k < len(szenen) - 1 and t >= t0 + szenen[k][0]:
                t0 += szenen[k][0]; k += 1
            d, im, label, _, (z0, z1), fok = szenen[k]
            z = z0 + (z1 - z0) * m.ease((t - t0) / d)
            c = Image.new('RGB', (W, H), CREME)
            karte(c, im, 960, 960 if im is not box or z > 1.5 else 900, z, fok)
            if k == 0:
                text(c, ['Was ist in der', 'Gotti-Box?'], 230, 62, '🎁')
            elif label:
                text(c, [label], 1600, 40)
            if k == len(szenen) - 1:
                text(c, ['5 Bodys + 5 Leggings'], 230, 50)
                if t - t0 > 1.0:
                    text(c, ['Preis? Schreib PREIS', 'in die Kommentare'], 1580, 46)
            yield c.convert('RGBA')
    vh.schreiben(os.path.join(OUT, 'reel_gotti_box_was_ist_drin_9x16.mp4'), frames(), dauer, MUSIK)


# ---------- 3. Besessen von Schleifen ----------
def schleifen():
    bilder = [(bild(os.path.join(WEISS, 'leggings5.jpg')), (3.0, (0.36, 0.67))),     # Start: ganz nah auf eine Schleife
              (bild(os.path.join(WEISS, 'jogginghose5.jpg')), (1.6, (0.5, 0.35))),
              (bild(os.path.join(BOX, 'box_lovely_little_girl.jpg')), (1.4, (0.5, 0.75))),
              (bild(os.path.join(WEISS, 'kombi_lovely.jpg')), (1.0, (0.5, 0.5))),
              (bild(os.path.join(BOX, 'box_mum_dad_me.jpg')), (1.4, (0.5, 0.75))),
              (bild(os.path.join(WEISS, 'leggings5.jpg')), (1.0, (0.5, 0.5)))]
    HOOK, SCHNITT, RASTER = 2.6, 0.85, 4.0
    dauer = HOOK + SCHNITT * (len(bilder) - 1) + RASTER
    kacheln = [b.resize((470, 470 if b.width == b.height else 583), Image.LANCZOS) for b, _ in bilder]

    def frames():
        for i in range(int(round(dauer * FPS))):
            t = i / FPS; c = Image.new('RGB', (W, H), CREME)
            if t < HOOK:
                im, (z, fok) = bilder[0]
                karte(c, im, 960, 1000, z - (z - 1.4) * m.ease(t / HOOK), fok)
                text(c, ['POV: Du bist besessen', 'von Schleifen'], 260, 56, '🎀')
            elif t < HOOK + SCHNITT * (len(bilder) - 1):
                k = 1 + int((t - HOOK) // SCHNITT); im, (z, fok) = bilder[k]
                tl = (t - HOOK) - (k - 1) * SCHNITT
                karte(c, im, 960, 1000, z * (1 - 0.06 * tl / SCHNITT), fok)
            else:
                tr = t - (HOOK + SCHNITT * (len(bilder) - 1))
                for j, kach in enumerate(kacheln):
                    a = m.ease((tr - j * 0.15) / 0.3)
                    if a <= 0:
                        continue
                    x = 60 + (j % 2) * 490; y = 260 + (j // 2) * 500
                    k2 = kach.crop((0, 0, 470, 470))
                    c.paste(Image.blend(Image.new('RGB', k2.size, CREME), k2, a), (x, y))
                if tr > 1.4:
                    text(c, ['Alles mit Schleife'], 150, 52, '🎀')
                    text(c, ['Link in der Bio'], 1790, 40)
            yield c.convert('RGBA')
    vh.schreiben(os.path.join(OUT, 'reel_schleifen_9x16.mp4'), frames(), dauer, MUSIK)


# ---------- 4. Gewinnspiel (Entwurf) ----------
def gewinnspiel():
    c = Image.new('RGB', (1080, 1350), CREME)
    im = bild(os.path.join(BOX, 'box_i_love_my_mummy.jpg'))
    im = k1.auf_4x5(im).resize((860, 1075), Image.LANCZOS); c.paste(im, (110, 250))
    d = ImageDraw.Draw(c)
    d.text((540, 95), 'GEWINNSPIEL', font=k1.f(70), fill=k1.DUNKEL, anchor='mm')
    d.text((540, 175), 'Gewinne die Geschenkbox «I love my Mummy»', font=k1.f(34), fill=(120, 105, 95), anchor='mm')
    c.save(os.path.join(OUT, 'gewinnspiel_entwurf_4x5.jpg'), quality=94)
    print('Gewinnspiel-Bild gespeichert')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    wahl = sys.argv[1:] or ['gewinnspiel', 'strecken_emoji', 'gotti_box', 'schleifen']
    for w in wahl:
        globals()[w]()
