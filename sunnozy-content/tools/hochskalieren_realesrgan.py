"""KI-Hochskalierung (Real-ESRGAN) fuer zu kleine KI-Fotos, kachelweise auf CPU.

Die Canva-KI-Fotos der Geschenkboxen sind nur ca. 1136 px breit und wirkten im Shop (2048 px) unscharf.
Bewaehrt: Modell RealESRGAN_x2 (Hugging Face ai-forever/Real-ESRGAN), danach 25 % Original (Lanczos) zurueckmischen,
damit die Stoffstruktur natuerlich bleibt. Abhaengigkeiten: torch (CPU), torchvision, spandrel, pillow.

Aufruf: python hochskalieren_realesrgan.py <ein.jpg> <aus.jpg> <modell.pth> [zielbreite]
"""
import sys, time, torch, numpy as np
from PIL import Image
from spandrel import ModelLoader
torch.set_num_threads(max(1, torch.get_num_threads()))
m = ModelLoader().load_from_file(sys.argv[3] if len(sys.argv) > 3 else 'modelle/RealESRGAN_x4plus.pth').eval()
s = m.scale
im = Image.open(sys.argv[1]).convert('RGB'); a = np.asarray(im).astype(np.float32) / 255
H, W, _ = a.shape; T, P = 256, 16
out = np.zeros((H * s, W * s, 3), np.float32); t = time.time()
with torch.no_grad():
    for y in range(0, H, T):
        for x in range(0, W, T):
            y0, x0, y1, x1 = max(0, y - P), max(0, x - P), min(H, y + T + P), min(W, x + T + P)
            r = m(torch.from_numpy(a[y0:y1, x0:x1]).permute(2, 0, 1)[None])[0].permute(1, 2, 0).clamp(0, 1).numpy()
            yy, xx = (y - y0) * s, (x - x0) * s
            h, w = min(T, H - y) * s, min(T, W - x) * s
            out[y * s:y * s + h, x * s:x * s + w] = r[yy:yy + h, xx:xx + w]
res = Image.fromarray((out * 255).round().astype(np.uint8))
if len(sys.argv) > 4: res = res.resize((int(sys.argv[4]), round(res.height * int(sys.argv[4]) / res.width)), Image.LANCZOS)
res.save(sys.argv[2], quality=95); print(res.size, round(time.time() - t), 's', 'scale', s)
