"""Shopify-Hauptbild der Weihnachts-Geschenkbox im Stil der übrigen Box-Hauptbilder (Box von oben, hellgrau,
Karte auf dem Inhalt, Logo oben links), aber mit der echten roten Weihnachtsbox der Nutzerin.

    python3 tools/make_shopify_geschenkbox_echt.py

Grundbild: KI (Canva) aus den Handyfotos der Nutzerin (posts/produktfotos-geschenkbox-weihnachten/quelle/).
Die Karte ist die echte Druckvorlage (karte/karte_vorne_freigestellt.png), kein KI-Text.
Ausgabe: posts/kampagne-weihnachtsbox/shopify-echt/geschenkbox-<box>.jpg (2048 × 2048)
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'posts', 'kampagne-weihnachtsbox')
OUT = os.path.join(K, 'shopify-echt')
N = 2048
def load_logo(width, col):
    """Wie in make_weihnachtsbox.py (dort nicht importierbar, weil es beim Import Argumente liest)."""
    a = np.asarray(Image.open(os.path.join(ROOT, 'logo-sunnozy.webp')).convert('RGB')).astype(float)
    al = np.clip((255 - a.min(axis=2)) / 255 * 1.2, 0, 1); al[al < 0.08] = 0
    L = Image.new('RGBA', (a.shape[1], a.shape[0]), col + (0,)); L.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    L = L.crop(L.getbbox())
    return L.resize((width, round(L.height * width / L.width)), Image.LANCZOS)


BOXEN = {  # name: (rohbild, karte-mitte x, y in Anteil, drehung)
    'growing-up-strong': ('growing_up_strong_ki.jpg', 0.735, 0.335, -8),
}


def karte(c, cx, cy, winkel, hoehe):
    k = Image.open(os.path.join(K, 'karte', 'karte_vorne_freigestellt.png')).convert('RGBA')
    k = k.resize((round(k.width * hoehe / k.height), hoehe), Image.LANCZOS)
    rgb = np.asarray(k.convert('RGB')).astype(float) * np.array([0.965, 0.95, 0.93])   # an das Studiolicht angleichen
    k = Image.merge('RGBA', (*Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).split(), k.getchannel('A')))
    k = k.rotate(winkel, Image.BICUBIC, expand=True)
    x, y = int(cx * N - k.width / 2), int(cy * N - k.height / 2)
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0))
    schatten = Image.new('RGBA', k.size, (40, 30, 25, 0)); schatten.putalpha(k.getchannel('A').point(lambda a: a * 0.32))
    sh.alpha_composite(schatten, (x + 10, y + 16))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    c.alpha_composite(k, (x, y))


def hauptbild(roh, cx, cy, w):
    c = Image.open(os.path.join(OUT, 'roh', roh)).convert('RGB').resize((N, N), Image.LANCZOS).convert('RGBA')
    karte(c, cx, cy, w, int(N * 0.30))
    L = load_logo(int(N * 0.198), (122, 108, 104)); c.alpha_composite(L, (int(N * 0.035), int(N * 0.031)))
    return c.convert('RGB')


if __name__ == '__main__':
    for name, (roh, cx, cy, w) in BOXEN.items():
        p = os.path.join(OUT, f'geschenkbox-{name}.jpg')
        hauptbild(roh, cx, cy, w).save(p, quality=95)
        print(p)
