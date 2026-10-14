"""Reel «kleine Details» (Vorbild: Instagram-Reel «little details I never want to forget»).

Analyse Vorbild: 10 s, 9:16, Handykamera, Tageslicht, warme Creme-Toene. 5 sehr nahe Detail-Einstellungen mit harten
Schnitten (Haare buersten -> Gesicht -> Fuesschen im Strampler -> Makro Gaehnen -> Haendchen), Kamera leicht wackelnd,
langsames Heranfahren. Ein kleiner weisser Serifen-Text in Kleinbuchstaben mittig, ohne Logo und ohne Endkarte.

Eingabe: Standbilder 1080x1920 (KI-Fotos) ODER echte Clips (.mp4, z.B. aus Google Flow). Ausgabe stumm, Ton in Instagram waehlen.
Aufruf: python3 make_details_reel.py <ausgabe.mp4> <shot1> <shot2> ... [--text "..."]
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

args = sys.argv[1:]
TEXT = 'kleine Details, die ich nie vergessen will'
if '--text' in args:
    i = args.index('--text'); TEXT = args[i + 1]; del args[i:i + 2]
out, shots = args[0], args[1:]
W, H, FPS = 1080, 1920, 30
# Dauer pro Einstellung wie im Vorbild: kurzer Einstieg, laengere Gesichts-Nahaufnahmen
DUR = [0.8, 2.3, 1.6, 2.4, 1.9, 1.6, 1.6, 1.6][:len(shots)]
SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'


def soft(im):
    im = ImageEnhance.Color(im).enhance(0.92)
    a = np.asarray(im).astype(np.float32)
    a = 10 + a * (243 / 255)
    a *= np.array([1.015, 1.0, 0.98])  # minimal warm
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def text_layer():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(SERIF, 40)
    d.text((W / 2, int(H * 0.47)), TEXT, font=f, fill=(255, 255, 255, 245), anchor='mm')
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(5)).point(lambda v: int(v * 0.45))
    dark = Image.new('RGBA', (W, H), (35, 25, 20, 0)); dark.putalpha(sh)
    return Image.alpha_composite(dark, lay)


def still_frames(path, n, k0):
    src = Image.open(path).convert('RGB')
    s = max(W / src.width, H / src.height) * 1.10  # Reserve fuer Zoom und Wackeln
    src = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    for j in range(n):
        t = (k0 + j) / FPS; p = j / max(1, n - 1)
        z = 1.0 + 0.06 * p  # langsames Heranfahren
        cw, ch = W / z, H / z  # Ausschnitt in Pixeln des (um 10 % vergroesserten) Bildes
        cx = src.width / 2 + 7 * math.sin(t * 1.4) + 4 * math.sin(t * 3.3 + 1)
        cy = src.height / 2 + 6 * math.sin(t * 1.1 + 2) + 3 * math.sin(t * 2.9)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        yield src.crop(tuple(int(v) for v in box)).resize((W, H), Image.BICUBIC)


def clip_frames(path, n):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf',
                          f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
                          '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        last = Image.frombuffer('RGB', (W, H), b); yield last
    p.wait()


rng = np.random.default_rng(3)
grain = [Image.fromarray(rng.normal(128, 12, (H // 2, W // 2)).clip(0, 255).astype('uint8')).resize((W, H), Image.BILINEAR) for _ in range(8)]
txt = text_layer()
tmp = out + '.tmp.mp4'
enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
k = 0
for path, d in zip(shots, DUR):
    n = int(d * FPS)
    gen = clip_frames(path, n) if path.endswith('.mp4') else still_frames(path, n, k)
    for fr in gen:
        im = soft(fr.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2)))
        im = Image.blend(im, Image.merge('RGB', [grain[k % 8]] * 3), 0.05)
        a = min(1.0, max(0.0, (k - 4) / 10))
        l2 = txt.copy(); l2.putalpha(txt.split()[3].point(lambda v: int(v * a)))
        im = Image.alpha_composite(im.convert('RGBA'), l2).convert('RGB')
        enc.stdin.write(im.tobytes()); k += 1
enc.stdin.close(); enc.wait()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', out], check=True)
os.remove(tmp)
print(out, round(k / FPS, 1), 's')
