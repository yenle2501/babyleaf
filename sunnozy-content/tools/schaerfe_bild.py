"""Ganze Shop-/Präsentations-/Marktplatzbilder mit Real-ESRGAN x4 aus ihrer echten Auflösung neu aufbauen (09.11.2026).

Viele Coming-soon-Hauptbilder sind 2048 px gross, enthalten aber nur die Details eines ~1000-px-Bildes (KI-Bild
hochgezogen). Das Skript schätzt die echte Auflösung, verkleinert darauf, rechnet mit Real-ESRGAN x4 hoch, bringt das
Bild auf die alte Grösse zurück und mischt 20 % Original darunter (natürliche Stoffstruktur). Reinweisse Flächen
bleiben reinweiss (Marktplatz).

    python3 tools/schaerfe_bild.py <RealESRGAN_x4plus.pth> <bild.jpg> [...]      # überschreibt die Bilder
"""
import sys
import numpy as np
import torch
from PIL import Image
from schaerfe_einzelteile import lade, hochrechnen

MAX_IN, MIN_IN, ORIGINAL = 1000, 500, 0.2


def echte_kante(im):
    g = np.asarray(im.convert('L'), np.float32)
    best = max(im.size)
    for k in (1.25, 1.5, 2, 2.5, 3, 4):
        w, h = round(im.width / k), round(im.height / k)
        zur = np.asarray(im.convert('L').resize((w, h), Image.LANCZOS).resize(im.size, Image.LANCZOS), np.float32)
        if np.abs(zur - g).mean() < 0.6:
            best = max(w, h)
    return best


def schaerfen(net, pfad):
    im = Image.open(pfad).convert('RGB')
    kante = min(max(echte_kante(im), MIN_IN), MAX_IN)
    f = kante / max(im.size)
    klein = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    gross = Image.blend(hochrechnen(net, klein).resize(im.size, Image.LANCZOS), im, ORIGINAL)
    a = np.asarray(gross).copy(); o = np.asarray(im)
    a[(o >= 254).all(2)] = 255                           # reinweisse Flächen bleiben reinweiss
    Image.fromarray(a).save(pfad, quality=95, subsampling=0)
    return kante


if __name__ == '__main__':
    torch.set_num_threads(int(__import__('os').environ.get('THREADS', 4)))
    net = lade(sys.argv[1])
    for p in sys.argv[2:]:
        print(f'{p}: Netz-Eingang {schaerfen(net, p)}px', flush=True)
