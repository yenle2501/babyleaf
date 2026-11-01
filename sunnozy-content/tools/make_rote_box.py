"""Shopify-Hauptbilder der Weihnachts-Geschenkboxen in der roten sunnozy-Box, nach der Vorlage der Nutzerin
(01.11.2026): offene Box von oben, Deckel mit «sunnozy»-Satinband oben, Blumen-Seidenpapier, Karte auf dem Inhalt.

    python3 tools/make_rote_box.py              # alle Boxen, für die ein Inhaltsbild in rote-box/inhalt/ liegt
    python3 tools/make_rote_box.py mum_dad_me   # nur eine Box

Deckel, Band, Seidenpapier und Karton kommen unverändert aus der Vorlage (`rote-box/vorlage/vorlage_offen.jpg`),
so bleibt die Bandschrift sauber. Nur der Inhalt im Karton wird ersetzt: `rote-box/inhalt/<box>.jpg`
(KI-Bild, Canva, Kleider von oben, randvoll, 4:3). Die Karte ist die echte Druckvorlage (karte/karte_vorne_freigestellt.png).
Ausgabe: `rote-box/shopify/geschenkbox-<box>.jpg` (quadratisch, 2048 px) und `rote-box/4x5/<box>.jpg` (1080 × 1350).
"""
import os, sys, glob
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox')
RB = os.path.join(K, 'rote-box')
# Vorlage, mit Real-ESRGAN 2x hochgerechnet (vorlage_offen_2x.jpg); alle Masse unten gelten für das Original 1199 × 1312
VORLAGE = os.path.join(RB, 'vorlage', 'vorlage_offen_2x.jpg')
if not os.path.exists(VORLAGE):
    VORLAGE = os.path.join(RB, 'vorlage', 'vorlage_offen.jpg')
# Innenraum des Kartons: x0, y0, x1, y1
INNEN = (213, 545, 1047, 1177)
# Umriss der Karte in der Vorlage: sie wird nach dem Einsetzen des Inhalts wieder aus der Vorlage darübergelegt
KARTE_POLY = [(600 + x / 2, 560 + y / 2) for x, y in [(196, 178), (240, 98), (418, 140), (480, 218), (320, 642), (58, 548)]]


def inhalt_einsetzen(basis, inhalt):
    W, H = basis.size; f = W / 1199
    x0, y0, x1, y1 = [round(v * f) for v in INNEN]
    bw, bh = x1 - x0, y1 - y0
    inh = inhalt.convert('RGB')
    iw, ih = inh.size
    # Inhalt so zuschneiden, dass das Seitenverhältnis passt (Mitte)
    ziel = bw / bh
    if iw / ih > ziel:
        nw = int(ih * ziel); inh = inh.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw / ziel); inh = inh.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    inh = inh.resize((bw, bh), Image.LANCZOS)
    lage = inh  # die Perspektive der Vorlage ist minimal, ein Rechteck genügt
    # Schatten unter dem Deckel und an den Kartonwänden
    a = np.asarray(lage).astype(float)
    yy = np.linspace(0, 1, bh)[:, None]; xx = np.linspace(0, 1, bw)[None, :]
    schatten = 1 - 0.16 * np.clip(1 - yy / 0.07, 0, 1) - 0.07 * np.clip(1 - xx / 0.03, 0, 1) - 0.07 * np.clip(1 - (1 - xx) / 0.03, 0, 1) \
        - 0.06 * np.clip(1 - (1 - yy) / 0.03, 0, 1)
    lage = Image.fromarray((a * schatten[..., None]).clip(0, 255).astype(np.uint8))
    m = np.full((bh, bw), 255.0)
    n = round(4 * f); m[:n, :] *= np.linspace(0, 1, n)[:, None]
    out = basis.copy(); out.paste(lage, (x0, y0), Image.fromarray(m.astype(np.uint8)))
    # Seidenpapier links/rechts und das Bandende des Deckels wieder aus der Vorlage darüberlegen
    ref = np.asarray(basis).astype(int); r, g, b = ref[..., 0], ref[..., 1], ref[..., 2]
    over = np.zeros((H, W), np.float32)
    over[:, :x0 + round(6 * f)] = 1; over[:, round(1036 * f):] = 1
    band = ((r > 175) & (r - g > 115) & (r - b > 100)).astype(np.uint8) * 255   # nur das helle Satinband, nicht der dunklere Deckelrand
    band = np.asarray(Image.fromarray(band).filter(ImageFilter.MaxFilter(2 * round(1.5 * f) + 1))) > 0
    reg = np.zeros_like(band); reg[round(538 * f):round(580 * f), round(860 * f):round(992 * f)] = True
    over[band & reg] = 1
    # Deckelunterkante verläuft schräg: links y≈543, rechts y≈568 (Original-Massstab); alles darüber ist Deckel
    xs_ = np.arange(W) / f; kante = (543 + (xs_ - 213) / (1047 - 213) * 25) * f
    over[np.arange(H)[:, None] < kante[None, :]] = 1
    om = Image.fromarray((over * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0 * f))
    out = Image.composite(basis, out, om)
    return out


def karte(c, basis):
    """Karte aus der Vorlage (mit ihrem Schatten) wieder über den neuen Inhalt legen."""
    from PIL import ImageDraw
    f = c.width / 1199; poly = [(x * f, y * f) for x, y in KARTE_POLY]
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2 * f))
    # weicher Schatten unten rechts der Karte, wie in der Vorlage
    sh = Image.new('L', c.size, 0); ImageDraw.Draw(sh).polygon([(x + 5 * f, y + 8 * f) for x, y in poly], fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(9 * f))
    c = Image.composite(Image.new('RGB', c.size, (60, 45, 40)), c, sh)
    return Image.composite(basis, c, m)


def leinwand(im, W, H):
    """Auf W×H bringen: Hintergrund seitlich/oben/unten mit den Randfarben der Vorlage verlängern."""
    s = min(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    a = np.asarray(im)
    c = np.zeros((H, W, 3), np.uint8)
    ox, oy = (W - im.width) // 2, (H - im.height) // 2
    links = a[:, :8].mean(axis=1).astype(np.uint8); rechts = a[:, -8:].mean(axis=1).astype(np.uint8)
    c[oy:oy + im.height, :ox] = links[:, None]; c[oy:oy + im.height, ox + im.width:] = rechts[:, None]
    c[:oy] = c[oy]; c[oy + im.height:] = c[oy + im.height - 1]
    c[oy:oy + im.height, ox:ox + im.width] = a
    out = Image.fromarray(c)
    # weicher Übergang an den Nahtstellen
    bl = out.filter(ImageFilter.GaussianBlur(18)); m = np.zeros((H, W), np.uint8)
    for x in (ox, ox + im.width):
        m[:, max(0, x - 20):x + 20] = 255
    return Image.composite(bl, out, Image.fromarray(m).filter(ImageFilter.GaussianBlur(10)))


def box(name):
    basis = Image.open(VORLAGE).convert('RGB')
    inhalt = Image.open(glob.glob(os.path.join(RB, 'inhalt', name + '.*'))[0])
    bild = karte(inhalt_einsetzen(basis, inhalt), basis)
    os.makedirs(os.path.join(RB, 'shopify'), exist_ok=True); os.makedirs(os.path.join(RB, '4x5'), exist_ok=True)
    leinwand(bild, 2048, 2048).save(os.path.join(RB, 'shopify', f'geschenkbox-{name.replace("_", "-")}.jpg'), quality=95)
    leinwand(bild, 1080, 1350).save(os.path.join(RB, '4x5', f'{name}.jpg'), quality=93)
    return bild


if __name__ == '__main__':
    namen = sys.argv[1:] or sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(RB, 'inhalt', '*.jpg')))
    for n in namen:
        box(n); print(n)
