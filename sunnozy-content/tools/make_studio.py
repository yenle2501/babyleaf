"""Handyfotos -> Studio-Produktfotos.

Eingabe: freigestellte PNGs (Canva "Hintergrund entfernen", gleiche Bildgroesse wie das Original).
Schritte: Weissabgleich + Belichtung auf den Kleidern, sanfte Schaerfe, Studio-Hintergrund
(Hohlkehle mit Lichtverlauf + feines Korn), Kontakt- und Umgebungsschatten.
Ausgabe: studio/ (4:5, warmweiss), shop/ (4:5 hochaufgeloest, reinweiss), farbig/ (Pastell-Hintergruende).

Aufruf: python3 make_studio.py <cutout-ordner> <ausgabeordner>
"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

src, out = sys.argv[1:3]
BG = {'warmweiss': (247, 243, 238), 'reinweiss': (255, 255, 255), 'rosa': (242, 224, 222), 'lila': (232, 226, 240), 'salbei': (226, 232, 220)}


def correct(rgba):
    """Weissabgleich auf hellen, ungesaettigten Stoffpixeln + Belichtung."""
    a = np.asarray(rgba).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    m = al > 200
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    lum0 = rgb.mean(axis=2)
    thr = np.percentile(lum0[m], 90) if m.any() else 255
    neutral = m & (lum0 >= thr) & ((mx - mn) < 45)  # hellste Stoffstellen = weisse Teile
    if neutral.sum() > 500:
        ref = rgb[neutral].mean(axis=0)
        gain = np.clip(ref.mean() / ref, 0.93, 1.08) * np.array([1.01, 1.0, 0.985])  # Farbstich entfernen, leicht warm
    else:
        gain = np.array([1.01, 1.0, 0.985])
    rgb = rgb * gain
    # Belichtung: 98. Perzentil der Helligkeit auf ~246, vorsichtig
    lum = rgb[m].mean(axis=1)
    p = np.percentile(lum, 98) if lum.size else 246
    rgb = rgb * min(1.08, max(1.0, 246 / max(p, 1)))
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    im = Image.fromarray(rgb)
    im = ImageEnhance.Color(im).enhance(1.0)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    # Kante minimal weicher, damit kein harter Saum entsteht
    alpha = Image.fromarray(al.astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    im.putalpha(alpha)
    return im


def backdrop(w, h, col, seamless=True):
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(-1, 1, w)[None, :]
    light = 1.0 + 0.035 * (1 - y) - 0.05 * (x ** 2) * 0.6  # oben heller, Raender leicht dunkler
    if seamless:
        light = light - 0.025 * np.clip((y - 0.62) / 0.38, 0, 1) ** 2  # Hohlkehle unten
    base = np.array(col, np.float32)[None, None, :] * light[..., None]
    rng = np.random.default_rng(3)
    base += rng.normal(0, 1.2, (h, w, 1))
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def shadow(alpha, w, h, op_contact=0.22, op_amb=0.10):
    a = alpha.point(lambda v: v)
    contact = Image.new('L', (w, h), 0); contact.paste(a, (6, 12))
    contact = contact.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * op_contact))
    amb = Image.new('L', (w, h), 0); amb.paste(a, (0, 30))
    amb = amb.filter(ImageFilter.GaussianBlur(45)).point(lambda v: int(v * op_amb))
    return Image.fromarray(np.maximum(np.asarray(contact), np.asarray(amb)))


def compose(cut, col, size, fit):
    """fit: 'same' = Originalausschnitt behalten (Kleider laufen aus dem Bild), sonst zentriert mit Rand."""
    W, H = size
    if fit == 'same':
        s = max(W / cut.width, H / cut.height)
        c = cut.resize((int(cut.width * s), int(cut.height * s)), Image.LANCZOS)
        bb = c.getchannel('A').getbbox()
        cx = (bb[0] + bb[2]) / 2
        x0 = int(min(max(0, cx - W / 2), c.width - W)); y0 = int((c.height - H) / 2)
        c = c.crop((x0, y0, x0 + W, y0 + H))
    else:
        bb = cut.getchannel('A').getbbox(); c0 = cut.crop(bb)
        s = min(W * 0.84 / c0.width, H * 0.84 / c0.height)
        c0 = c0.resize((int(c0.width * s), int(c0.height * s)), Image.LANCZOS)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); c.paste(c0, ((W - c0.width) // 2, (H - c0.height) // 2))
    bg = backdrop(W, H, col, seamless=col != BG['reinweiss']).convert('RGBA')
    sh = shadow(c.getchannel('A'), W, H, *( (0.14, 0.06) if col == BG['reinweiss'] else (0.22, 0.10) ))
    dark = Image.new('RGBA', (W, H), (60, 45, 38, 0)); dark.putalpha(sh)
    bg = Image.alpha_composite(bg, dark)
    return Image.alpha_composite(bg, c).convert('RGB')


for d in ('studio', 'shop', 'farbig', 'freigestellt'):
    os.makedirs(os.path.join(out, d), exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, '*.png'))):
    name = os.path.splitext(os.path.basename(f))[0]
    cut = correct(Image.open(f).convert('RGBA'))
    a = np.asarray(cut.getchannel('A'))
    touches = (a[:, :4].max() > 50) or (a[:, -4:].max() > 50) or (a[-4:, :].max() > 50) or (a[:4, :].max() > 50)
    fit = 'same' if touches else 'center'
    cut.save(os.path.join(out, 'freigestellt', name + '.png'))
    compose(cut, BG['warmweiss'], (1080, 1350), fit).save(os.path.join(out, 'studio', name + '.jpg'), quality=95)
    compose(cut, BG['reinweiss'], (1600, 2000), fit).save(os.path.join(out, 'shop', name + '.jpg'), quality=95)
    for k in ('rosa', 'lila', 'salbei'):
        compose(cut, BG[k], (1080, 1350), fit).save(os.path.join(out, 'farbig', f'{name}_{k}.jpg'), quality=95)
    print(name, fit)
