"""Countdown-Reels «Noch 3 Tage / 2 Tage / 1 Tag» (08.11.2026) im Flacker-Stil, je 6.8 s.

Gleicher Aufbau wie make_reel_coming_soon_flacker.py (Logo → schneller Farbwechsel → Logo mit sunnozy.ch),
nur kürzer und mit grosser Zahl. Gedacht für die 3 Tage vor dem Launch, danach folgt das Weihnachts-Reveal.

    python3 tools/make_reel_countdown.py
Ausgabe: posts/reels/coming-soon/reel_countdown_<n>_9x16.mp4 + _titelbild.jpg
"""
import os
from PIL import Image, ImageDraw
import make_reel_coming_soon_flacker as fl

FAKTOR = 0.72
fl.WECHSEL = [round(w * FAKTOR, 3) for w in fl.WECHSEL]
fl.T_LOGO2 = fl.WECHSEL[-1]
fl.T_ENDE = round(fl.T_LOGO2 + 1.5, 2)
W, H = fl.W, fl.H
ZAHL = None


def coming(f, dunkel):
    bg, fg = (f['dunkel'], f['hell']) if dunkel else (f['hell'], f['dunkel'])
    c = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(c)
    fl.gesperrt(d, 'NOCH', 640, 64, fg, 14)
    d.text((W / 2, 860), str(ZAHL), font=fl.m.f(fl.FETT, 360), fill=fg, anchor='mm')
    fl.gesperrt(d, 'TAGE' if ZAHL > 1 else 'TAG', 1090, 64, fg, 14)
    fl.gesperrt(d, 'BIS ZUM LAUNCH', 1190, 40, fg, 10)
    return c


fl.coming = coming

if __name__ == '__main__':
    for n in (3, 2, 1):
        ZAHL = n
        fl.reel('weinrot')
        alt = os.path.join(fl.OUT, 'reel_coming_soon_flackern_weinrot_9x16')
        neu = os.path.join(fl.OUT, f'reel_countdown_{n}_9x16')
        os.replace(alt + '.mp4', neu + '.mp4'); os.replace(alt + '_titelbild.jpg', neu + '_titelbild.jpg')
        print(neu + '.mp4')
