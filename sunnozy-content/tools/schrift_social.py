"""Hausschrift fuer alle Social-Media-Posts (nicht fuer Anzeigen): Sacramento, weiss, klein geschrieben, weicher Schatten.

Vorbild der Nutzerin (Okt. 2026): «winter is here» in duenner, verspielter Schreibschrift mittig auf einem ruhigen Foto.
Als Modul: `from schrift_social import post` oder direkt aufrufen.

Aufruf: python3 schrift_social.py <foto> <ausgabe.jpg> "<text>" [hoehe-in-prozent=50] [format=4x5|1x1|9x16]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHRIFT = os.path.join(ROOT, 'fonts', 'sacramento.ttf')
WEISS = (255, 253, 248)
FORMATE = {'4x5': (1080, 1350), '1x1': (1080, 1080), '9x16': (1080, 1920)}


def schreiben(img, text, y_anteil=0.5, groesse=None, farbe=WEISS):
    """Text mittig ins Bild, Groesse passt sich der Bildbreite an (max. 82 % Breite)."""
    W, H = img.size
    g = groesse or int(W * 0.15)
    f = ImageFont.truetype(SCHRIFT, g)
    d = ImageDraw.Draw(img)
    while d.multiline_textbbox((0, 0), text, font=f, align='center')[2] > W * 0.82 and g > 40:
        g -= 4; f = ImageFont.truetype(SCHRIFT, g)
    xy = (W // 2, int(H * y_anteil))
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).multiline_text(xy, text, font=f, fill=150, anchor='mm', align='center', spacing=int(g * 0.1))
    img.paste((55, 40, 30), (0, 0), sh.filter(ImageFilter.GaussianBlur(max(4, g // 25))))
    d.multiline_text(xy, text, font=f, fill=farbe, anchor='mm', align='center', spacing=int(g * 0.1))
    return img


def post(foto, text, y_anteil=0.5, fmt='4x5', abdunkeln=0.9):
    W, H = FORMATE[fmt]
    im = ImageOps.fit(Image.open(foto).convert('RGB'), (W, H), Image.LANCZOS)
    im = im.point(lambda v: int(v * abdunkeln))  # leicht abdunkeln, damit Weiss lesbar bleibt
    return schreiben(im, text, y_anteil)


if __name__ == '__main__':
    foto, aus, text = sys.argv[1:4]
    y = float(sys.argv[4]) / 100 if len(sys.argv) > 4 else 0.5
    fmt = sys.argv[5] if len(sys.argv) > 5 else '4x5'
    post(foto, text.replace('\\n', '\n'), y, fmt).save(aus, quality=94)
