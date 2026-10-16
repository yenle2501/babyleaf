"""Shop-Hauptbilder originalgetreu klarer machen (ohne KI, nichts wird dazuerfunden).

Warum nicht KI-Upscaling: Real-ESRGAN (x4plus und general-x4v3) wurde getestet und glaettet feine Stoffmuster weg
(Karo am Princess-Strampler, Rippstruktur der Bodys, Druckknoepfe) - das verfaelscht das Produkt.

Stattdessen, Schritt fuer Schritt:
1. Kompressionsspuren: Farbkloetzchen und Farbsaeume entstehen in den Farbkanaelen (Cb/Cr). Diese werden leicht
   geglaettet, die Helligkeit (Kanten, Schrift, Stoffstruktur) bleibt unangetastet.
2. Leichtes Entrauschen der Helligkeit nur in flachen Flaechen (Median 3x3 dort, wo kaum Struktur ist).
3. Nachschaerfen in zwei Stufen: feine Unschaerfemaske (Kanten, Schrift) + grobe mit grossem Radius (Mikrokontrast,
   «Klarheit»). Staerke richtet sich nach der gemessenen Weichheit des Bildes.
4. Weisser Grund bleibt reinweiss (255), gespeichert mit Qualitaet 95 ohne Farb-Unterabtastung.
Groesse und Bildausschnitt bleiben exakt gleich (Bilder < 2048 px werden mit Lanczos auf 2048 gebracht, vor dem
Schaerfen, damit Zoom im Shop sauber ist).

Aufruf: python3 hauptbild_klar.py <ausgabe-ordner> <bild> [<bild> ...]
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ZIEL = 2048


def weichheit(g):
    """0 = knackig .. 1 = sehr weich (Detailverlust bei halber Groesse, nur Produktflaeche)."""
    H, W = g.shape
    d = np.asarray(Image.fromarray(g.astype(np.uint8)).resize((W // 2, H // 2), Image.LANCZOS).resize((W, H), Image.LANCZOS)).astype(np.float32)
    m = g < 240
    v = np.abs(d - g)[m].mean() if m.any() else 3
    return float(np.clip((2.6 - v) / 2.2, 0, 1))


def usm(L, radius, amount, threshold=0.0):
    blur = ndi.gaussian_filter(L, radius)
    diff = L - blur
    if threshold:
        diff = np.where(np.abs(diff) < threshold, diff * (np.abs(diff) / threshold), diff)
    return L + amount * diff


def klar(im):
    if im.mode in ('RGBA', 'LA', 'P'):         # transparente PNGs: im Shop erscheint Weiss dahinter
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im)
    im = im.convert('RGB')
    lang = max(im.size)
    if lang < ZIEL:
        s = ZIEL / lang; im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    ycc = np.asarray(im.convert('YCbCr')).astype(np.float32)
    Y, Cb, Cr = ycc[..., 0], ycc[..., 1], ycc[..., 2]
    w = weichheit(Y)
    # 1 Farbkloetzchen weg
    Cb = ndi.gaussian_filter(Cb, 1.6); Cr = ndi.gaussian_filter(Cr, 1.6)
    # 2 flache Flaechen leicht entrauschen
    struktur = ndi.gaussian_filter(np.abs(ndi.laplace(ndi.gaussian_filter(Y, 0.8))), 2)
    flach = np.clip(1 - struktur / 3.0, 0, 1)
    Y = Y * (1 - 0.6 * flach) + ndi.median_filter(Y, 3) * 0.6 * flach
    # 3 schaerfen: fein + Klarheit, staerker bei weichen Bildern
    Y = usm(Y, 1.2 + 0.8 * w, 0.55 + 0.75 * w, threshold=1.5)
    Y = usm(Y, 18, 0.10 + 0.10 * w)
    ycc = np.stack([np.clip(Y, 0, 255), Cb, Cr], 2).round().astype(np.uint8)
    res = np.asarray(Image.fromarray(ycc, 'YCbCr').convert('RGB')).astype(np.float32)
    # 4 weisser Grund: was im Original fast weiss war, bleibt/ wird 255 (Schaerfe-Saeume am Rand vermeiden)
    o = np.asarray(im).astype(np.float32)
    fast_weiss = ndi.gaussian_filter((o.min(2) >= 250).astype(np.float32), 1.5)[..., None]
    res = res * (1 - fast_weiss) + 255 * fast_weiss
    return Image.fromarray(np.clip(res, 0, 255).round().astype(np.uint8)), w


if __name__ == '__main__':
    for p in sys.argv[2:]:
        r, w = klar(Image.open(p))
        name = os.path.splitext(os.path.basename(p))[0] + '.jpg'
        r.save(os.path.join(out, name), quality=95, subsampling=0)
        print(f'{name}  weich {w:.2f}  {r.size[0]}x{r.size[1]}', flush=True)
