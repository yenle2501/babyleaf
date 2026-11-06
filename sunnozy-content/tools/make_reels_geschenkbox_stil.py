"""Weihnachts-Geschenkboxen: Reels im Stil «Collage, schnelle Schnitte, ruhige Einstellung, Schlusskarte» (06.11.2026).

Nach dem Bildschirmvideo der Nutzerin (fremdes Reel, nur als Stil-Vorlage, nichts übernommen):
  0.0–1.8 s   Collage: Flatlay als Hintergrund, kleine Kacheln (Babyfotos, Box) darum, grosse Serifen-Versalien in der Mitte
  1.8–6.3 s   schnelle Schnitte (0.45 s): Detailausschnitte der Box, der Prints und der Babyfotos
  6.3–13.0 s  eine ruhige Einstellung, langsamer Zoom, ein Satz in Versalien blendet langsam ein
  13.0–17.5 s helle Schlusskarte (Rosé-Beige): Name der Box, Preis, Kurzlink, «Link in Bio»

    python3 tools/make_reels_geschenkbox_stil.py              # alle 9 Boxen
    python3 tools/make_reels_geschenkbox_stil.py dino mum_dad_me

Nur KI-Bilder: Babyfotos aus baby-in-box-kleidung/ (Canva, frei erfundene Babys), KI-Flatlays (rote-box/flatlay/roh/),
Box-Hauptbilder mit KI-Inhalt (rote-box/shopify/). Keine echten Fotos.
Ausgabe: posts/kampagne-weihnachtsbox/reels-stil-collage/reel_<box>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, glob, subprocess
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m
from make_reels_box_schlaf import BOXEN, MUSIK

W, H, FPS = m.W, m.H, m.FPS
BASIS = os.path.join(m.POSTS, 'kampagne-weihnachtsbox')
OUT = os.path.join(BASIS, 'reels-stil-collage')
BABYS = os.path.join(BASIS, 'baby-in-box-kleidung')
BOX = lambda k: os.path.join(BASIS, 'rote-box', 'shopify', 'geschenkbox-' + k.replace('_', '-') + '.jpg')
FLAT = lambda k: os.path.join(BASIS, 'rote-box', 'flatlay', 'roh', k + '.jpg')
ROSE = (236, 226, 221)          # helle Schlusskarte wie in der Vorlage
TAUPE = (96, 80, 76)
WEINROT = (98, 22, 30)

HOOK = ['ALLES, WAS', 'UNTER DEN', 'BAUM GEHÖRT']
RUHIG = ['FERTIG VERPACKT.', 'MIT LIEBE.']
T_COL, T_CUT, N_CUT, T_RUHIG, T_END = 1.8, 0.45, 10, 6.7, 4.5


def babyfotos(key):
    """KI-Babyfotos (9:16) der Box; 'dino_…' gehört nicht zu 'dinosaur', 'little_one_…' nicht zu 'little_one_jogginghosen'."""
    out = []
    for p in sorted(glob.glob(os.path.join(BABYS, '*_9x16.jpg'))):
        n = os.path.basename(p)[:-len('_9x16.jpg')]
        treffer = [k for k in BOXEN if n == k or n.startswith(k + '_')]
        if treffer and max(treffer, key=len) == key:
            out.append(p)
    schlaf = os.path.join(BABYS, key + '_9x16.jpg')            # schlafendes Baby ans Ende, wache Babys zuerst
    if schlaf in out:
        out.remove(schlaf); out.append(schlaf)
    return [Image.open(p).convert('RGB') for p in out]


def ausschnitt(im, z, fx, fy):
    """9:16-Ausschnitt mit Zoom z um (fx, fy), ohne das ganze Bild zu skalieren."""
    s = max(W / im.width, H / im.height) * z
    bw, bh = W / s, H / s
    cx = min(max(fx * im.width, bw / 2), im.width - bw / 2)
    cy = min(max(fy * im.height, bh / 2), im.height - bh / 2)
    return im.resize((W, H), Image.BICUBIC, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')


def versalien(c, zeilen, alpha, y, groesse, farbe=(255, 255, 255), schatten=True, sperren=0.04):
    """Zentrierte Serifen-Versalien (Cormorant), leicht gesperrt, optional mit weichem Schatten."""
    if alpha <= 0:
        return c
    tx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(tx)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    breite = lambda g: max(dt.textlength(z, font=m.f(m.SERIF, g)) + g * sperren * (len(z) - 1) for z in zeilen)
    while groesse > 30 and breite(groesse) > 860:                     # rechts liegen die Instagram-Knöpfe
        groesse -= 2
    fo = m.f(m.SERIF, groesse); lh = groesse * 1.04
    sp = groesse * sperren
    y0 = y - (len(zeilen) - 1) * lh / 2
    for k, z in enumerate(zeilen):
        breiten = [dt.textlength(ch, font=fo) for ch in z]
        x = W / 2 - (sum(breiten) + sp * (len(z) - 1)) / 2
        for ch, b in zip(z, breiten):
            p = (x, y0 + k * lh)
            if schatten:
                ds.text((p[0] + 2, p[1] + 3), ch, font=fo, fill=(20, 14, 10, int(150 * alpha)), anchor='lm')
            dt.text(p, ch, font=fo, fill=farbe + (int(255 * alpha),), anchor='lm')
            x += b + sp
    if schatten:
        c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    c.alpha_composite(tx)
    return c


def abdunkeln(c, a):
    c.alpha_composite(Image.new('RGBA', (W, H), (30, 20, 16, int(255 * a))))
    return c


def kachel(im, w, h, fx=0.5, fy=0.5, z=1.0):
    """Kleine Collage-Kachel mit runden Ecken und weichem Schatten."""
    s = max(w / im.width, h / im.height) * z
    bw, bh = w / s, h / s
    cx = min(max(fx * im.width, bw / 2), im.width - bw / 2); cy = min(max(fy * im.height, bh / 2), im.height - bh / 2)
    k = im.resize((w, h), Image.LANCZOS, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)).convert('RGBA')
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=255)
    k.putalpha(mask)
    return k


def collage(flat, babys, box):
    """Grundbild der Collage (ohne Text): Flatlay füllt das Bild, vier Kacheln am Rand wie in der Vorlage."""
    c = ausschnitt(flat, 1.0, 0.5, 0.5)
    abdunkeln(c, 0.30)
    kacheln = [
        (kachel(box, 330, 330, 0.5, 0.42, 1.25), (50, 230)),
        (kachel(babys[0], 290, 420), (720, 170)),
        (kachel(babys[1 % len(babys)], 300, 440), (60, 1230)),
        (kachel(box, 320, 320, 0.5, 0.72, 1.6), (700, 1300)),
    ]
    for k, (x, y) in kacheln:
        sch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sch).rounded_rectangle((x + 6, y + 10, x + k.width + 6, y + k.height + 10), 18, fill=(0, 0, 0, 90))
        c.alpha_composite(sch.filter(ImageFilter.GaussianBlur(12)))
        c.alpha_composite(k, (x, y))
    return c


def schnitte(flat, babys, box):
    """10 kurze Einstellungen: Details aus Box und Flatlay im Wechsel mit den Babyfotos. (Bild, Zoom von/bis, Fokus)"""
    det_box = [(1.9, 0.30, 0.42), (2.2, 0.62, 0.40), (1.9, 0.50, 0.72), (2.4, 0.84, 0.44)]
    det_flat = [(1.7, 0.35, 0.45), (1.9, 0.70, 0.40), (1.6, 0.50, 0.78)]
    folge, b = [], 0
    for i in range(N_CUT):
        if i % 3 == 1:
            z, fx, fy = det_box[(i // 3) % len(det_box)]; folge.append((box, z, z * 1.05, fx, fy))
        elif i % 3 == 2:
            folge.append((babys[b % len(babys)], 1.04, 1.10, 0.5, 0.45)); b += 1
        else:
            z, fx, fy = det_flat[(i // 3) % len(det_flat)]; folge.append((flat, z, z * 1.05, fx, fy))
    return folge


def ruhig_bild(flat, z):
    """Ruhige Einstellung: Flatlay unten, Weinrot oben als Fläche für den Satz (Ware bleibt frei)."""
    c = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    oben = flat.crop((0, 0, flat.width, 40)).resize((1, 1), Image.BOX).getpixel((0, 0))
    c.paste(oben + (255,), (0, 0, W, H))
    bw = round(W * z); bh = round(flat.height * bw / flat.width)
    f = flat.resize((bw, bh), Image.BICUBIC).convert('RGBA')
    verlauf = Image.new('L', (1, bh), 255)
    for y in range(min(220, bh)):
        verlauf.putpixel((0, y), int(255 * m.ease(y / 220)))
    f.putalpha(verlauf.resize((bw, bh)))
    c.paste(f, ((W - bw) // 2, H - bh), f)
    return c


def end_karte(r, t):
    c = Image.new('RGBA', (W, H), ROSE + (255,))
    a1 = m.ease((t - 0.3) / 1.0); a2 = m.ease((t - 1.3) / 0.8); a3 = m.ease((t - 1.9) / 0.8)
    versalien(c, ['WEIHNACHTS-', 'GESCHENKBOX'], a1, 690, 104, TAUPE, schatten=False)
    name = r['name'].upper()
    versalien(c, [name], a1, 860, 112 if len(name) < 16 else 92, TAUPE, schatten=False)
    d = ImageDraw.Draw(c)
    if a2 > 0:
        d.text((W / 2, 990), r['inhalt'], font=m.f(m.SERIF_I, 50), fill=TAUPE + (int(255 * a2),), anchor='mm')
        d.text((W / 2, 1090), f"CHF {r['preis']}", font=m.f(m.SERIF, 70), fill=WEINROT + (int(255 * a2),), anchor='mm')
    if a3 > 0:
        versalien(c, ['LINK IN BIO'], a3, 1215, 34, TAUPE, schatten=False, sperren=0.25)
        d.text((W / 2, 1275), f"sunnozy.ch/{r['kurz']}", font=m.f(m.SERIF, 40), fill=TAUPE + (int(255 * a3),), anchor='mm')
        L = m.logo(170, TAUPE); L.putalpha(L.getchannel('A').point(lambda v: int(v * a3)))
        c.alpha_composite(L, ((W - L.width) // 2, 1380))
    return c


def reel(key, nr):
    r = dict(BOXEN[key])
    babys = babyfotos(key)
    flat = Image.open(FLAT(key)).convert('RGB'); box = Image.open(BOX(key)).convert('RGB')
    grund = collage(flat, babys, box)
    folge = schnitte(flat, babys, box)
    t_cut0 = T_COL; t_ruhig0 = t_cut0 + N_CUT * T_CUT; t_end0 = t_ruhig0 + T_RUHIG; t_ges = t_end0 + T_END
    n = int(round(t_ges * FPS))

    def ruhig(t):
        c = ruhig_bild(flat, 1.0 + 0.07 * m.ease(t / T_RUHIG))
        return versalien(c, RUHIG, m.ease((t - 0.8) / 1.6), 300, 92)

    def bild(s):
        if s < t_cut0:                                                   # Collage, Text ab dem ersten Bild
            c = grund.copy()
            return versalien(c, HOOK, 1.0, H / 2 - 20, 128)
        if s < t_ruhig0:                                                 # harte, schnelle Schnitte
            i = min(int((s - t_cut0) / T_CUT), N_CUT - 1); t = (s - t_cut0 - i * T_CUT) / T_CUT
            im, z0, z1, fx, fy = folge[i]
            return ausschnitt(im, z0 + (z1 - z0) * t, fx, fy)
        if s < t_end0:
            c = ruhig(s - t_ruhig0)
            if s < t_ruhig0 + 0.3:                                       # kurze Blende aus dem letzten Schnitt
                im, z0, z1, fx, fy = folge[-1]
                c = Image.blend(ausschnitt(im, z1, fx, fy), c, (s - t_ruhig0) / 0.3)
            if s > t_end0 - 0.7:                                         # weich ins Rosé
                c = Image.blend(c, end_karte(r, 0), (s - (t_end0 - 0.7)) / 0.7)
            return c
        return end_karte(r, s - t_end0)

    os.makedirs(OUT, exist_ok=True)
    datei = f'reel_{key}_9x16'
    pfad = os.path.join(OUT, datei + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        fr = bild(i / FPS).convert('RGB')
        if i == int(0.5 * FPS):
            fr.save(os.path.join(OUT, datei + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    dauer = n / FPS
    musik = MUSIK[nr % 2]; ab = 4 + (nr * 11) % 50
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', musik, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.3,afade=t=out:st={dauer - 1.8:.2f}:d=1.8,volume=0.85', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s, {len(babys)} Babyfotos', flush=True)


if __name__ == '__main__':
    for nr, k in enumerate(sys.argv[1:] or list(BOXEN)):
        reel(k, nr)
