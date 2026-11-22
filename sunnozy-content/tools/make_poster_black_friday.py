"""Black-Friday-Poster (22.11.2026): statisches Feed-Bild (4:5) zum Reel, gleicher Clip/Sticker/Zeitraum.

Frame aus dem gleichen Clip wie das Reel (Hand hängt 5 Bodys über die sunnozy-Tüte), oben Headline
«Black Friday bei sunnozy 🖤», runder schwarzer Sticker «-10 % auf alles 16.–30.11» wie im Reel,
unten «Link in der Bio · sunnozy.ch» und Logo. Kein Code (in Shopify noch kein Black-Friday-Rabatt).

    python3 tools/make_poster_black_friday.py
"""
import os
import make_coming_soon_reels as m
import make_baby_reels as b
from make_reel_black_friday_v2 import CLIP, OUT, sticker
from PIL import Image, ImageDraw, ImageFont
import subprocess

PW, PH = 1080, 1350  # 4:5 Feed-Format


def frame(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', CLIP, '-frames:v', '1',
                          '-vf', f'hqdn3d=1.2:1.2:3:3,eq=contrast=1.05:saturation=1.03,cas=0.3,scale={b.W}:{b.H}:flags=lanczos',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert('RGB')


def main():
    fr = frame(1.3)                                   # Hand schon da, Body hängt schön sichtbar
    crop = fr.crop((0, 380, b.W, 380 + PH))            # 1080x1350, Headline-Freiraum oben, Tüte unten sichtbar
    c = crop.convert('RGBA')
    d = ImageDraw.Draw(c)
    f = lambda g: ImageFont.truetype(b.SCHRIFT, g)
    d.text((PW / 2, 110), 'Black Friday', font=f(76), fill=(255, 255, 255, 255), anchor='mm')
    zeile2 = 'bei sunnozy'
    w2 = d.textlength(zeile2 + ' ', font=f(50))
    herz = b.emoji('🖤', 44)
    d.text((PW / 2 - (w2 + herz.width) / 2, 190), zeile2, font=f(50), fill=(255, 255, 255, 255), anchor='lm')
    c.alpha_composite(herz, (round(PW / 2 - (w2 + herz.width) / 2 + w2), 190 - herz.height // 2))
    st = sticker()
    SX, SY = PW - st.width - 24, PH - st.height - 160
    c.alpha_composite(st, (SX, SY))
    d.text((PW / 2, PH - 86), 'Link in der Bio · sunnozy.ch', font=f(30), fill=(255, 255, 255, 255), anchor='mm')
    L = m.logo(110, (255, 255, 255)); c.alpha_composite(L, ((PW - L.width) // 2, PH - 50))
    out = os.path.join(OUT, 'poster_black_friday_4x5.jpg')
    c.convert('RGB').save(out, quality=94)
    print(out)


if __name__ == '__main__':
    main()
