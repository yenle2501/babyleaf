"""Kleine runde Stelle (z.B. fremdes Logo auf Holzbuegel) wegretuschieren: Median + Weichzeichnung in weicher Kreismaske.

Aufruf: python3 retusche_kreis.py <bild> <x> <y> <radius> [<ausgabe>]
"""
import sys
from PIL import Image, ImageDraw, ImageFilter
f, x, y, r = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
out = sys.argv[5] if len(sys.argv) > 5 else f
im = Image.open(f).convert('RGB')
box = (x - 3 * r, y - 3 * r, x + 3 * r, y + 3 * r)
patch = im.crop(box)
clean = patch.filter(ImageFilter.MedianFilter(15)).filter(ImageFilter.MedianFilter(13)).filter(ImageFilter.GaussianBlur(2))
mask = Image.new('L', patch.size, 0)
ImageDraw.Draw(mask).ellipse([2 * r, 2 * r, 4 * r, 4 * r], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(r * 0.25))
patch.paste(clean, (0, 0), mask)
im.paste(patch, box[:2])
im.save(out, quality=96)
