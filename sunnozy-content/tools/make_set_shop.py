"""Set-Praesentationsfotos fuer Shop/Instagram: nachschaerfen + Logo oben links (Artikelnummer nur wenn angegeben).

Aufruf: python3 make_set_shop.py <ki-roh-ordner> <ausgabeordner> [<artikelnummer>]
"""
import sys, os, glob
here = os.path.dirname(os.path.abspath(__file__))
src_dir, out = sys.argv[1:3]
art = sys.argv[3] if len(sys.argv) > 3 else ''
s = open(os.path.join(here, 'make_viral.py')).read().split('# 1) "Schick das an')[0]
g = {'__file__': os.path.join(here, 'make_viral.py')}
sys.argv = ['x', out, out, out]
exec(s.replace("B = {k: Image.open", "_B = None and {k: Image.open").replace("PK = lambda", "_PK = lambda"), g)
Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont = g['Image'], g['ImageDraw'], g['ImageFilter'], __import__('PIL.ImageEnhance').ImageEnhance, g['ImageFont']
logo = g['logo']
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
for d in ('ohne_logo', 'mit_logo'):
    os.makedirs(os.path.join(out, d), exist_ok=True)
for f in sorted(glob.glob(os.path.join(src_dir, '*.jpg'))):
    im = Image.open(f).convert('RGB')
    im = im.resize((im.width * 1080 // min(im.size), im.height * 1080 // min(im.size)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))
    name = os.path.basename(f)
    im.save(os.path.join(out, 'ohne_logo', name), quality=95)
    b = im.copy(); d = ImageDraw.Draw(b); w, h = b.size
    L = logo(int(w * 0.2), (120, 112, 115)); b.paste(L, (int(w * 0.035), int(h * 0.03)), L)
    if art:
        fnt = ImageFont.truetype(SANS, int(w * 0.03))
        tw = d.textlength(art, font=fnt); d.text((w - tw - int(w * 0.035), h - int(w * 0.03) - int(h * 0.03)), art, font=fnt, fill=(120, 112, 115))
    b.save(os.path.join(out, 'mit_logo', name), quality=95)
    print(name, im.size)
