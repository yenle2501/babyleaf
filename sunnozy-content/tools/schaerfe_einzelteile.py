"""Unscharfe Einzelteil-Bilder mit Real-ESRGAN x4 neu aufbauen.

Die Einzelteile wurden aus 1264-px-Setbildern ausgeschnitten und auf 2000x2000
hochgezogen; kleine Teile (Socken, Fäustlinge) sind dadurch 6-8x vergrössert
und weich. Das Skript schätzt pro Bild die echte Auflösung, verkleinert auf
diese, rechnet mit Real-ESRGAN x4 hoch und setzt das Teil wieder reinweiss auf
2000x2000 (gleiche Position und Grösse wie vorher).

    python3 tools/schaerfe_einzelteile.py <gewichte.pth> <bild.jpg> [...]

Gewichte: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
Braucht torch (CPU reicht), numpy, Pillow. Überschreibt die Bilder.
"""
import sys
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from PIL import Image


class RDB(nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        return self.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x


class RRDB(nn.Module):
    def __init__(self, nf, gc=32):
        super().__init__()
        self.rdb1, self.rdb2, self.rdb3 = RDB(nf, gc), RDB(nf, gc), RDB(nf, gc)

    def forward(self, x):
        return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x


class RRDBNet(nn.Module):
    def __init__(self, nf=64, nb=23):
        super().__init__()
        self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        self.body = nn.Sequential(*[RRDB(nf) for _ in range(nb)])
        self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        self.lrelu = nn.LeakyReLU(0.2, True)

    def forward(self, x):
        feat = self.conv_first(x)
        feat = feat + self.conv_body(self.body(feat))
        feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode='nearest')))
        feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode='nearest')))
        return self.conv_last(self.lrelu(self.conv_hr(feat)))


S, WEISS = 2000, 250
MIN_IN, MAX_IN = 400, 800      # Eingangsgrösse für das Netz (Kante des Teils)
ORIGINAL = 0.25                 # Anteil Originalbild, hält etwas Stoffstruktur


def lade(pfad):
    net = RRDBNet()
    sd = torch.load(pfad, map_location='cpu')
    net.load_state_dict(sd.get('params_ema', sd), strict=True)
    return net.eval()


def hochrechnen(net, img, kachel=192, rand=12):
    a = torch.from_numpy(np.asarray(img, np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = a.shape
    out = torch.zeros(1, 3, h * 4, w * 4)
    with torch.no_grad():
        for y in range(0, h, kachel):
            for x in range(0, w, kachel):
                y0, x0 = max(y - rand, 0), max(x - rand, 0)
                y1, x1 = min(y + kachel + rand, h), min(x + kachel + rand, w)
                t = net(a[:, :, y0:y1, x0:x1])
                yy, xx = (y - y0) * 4, (x - x0) * 4
                hh, ww = (min(y + kachel, h) - y) * 4, (min(x + kachel, w) - x) * 4
                out[:, :, y * 4:y * 4 + hh, x * 4:x * 4 + ww] = t[:, :, yy:yy + hh, xx:xx + ww]
    o = (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
    return Image.fromarray(o)


def echte_kante(teil):
    """Grösste Kante, auf die sich das Teil ohne sichtbaren Verlust verkleinern lässt."""
    g = np.asarray(teil.convert('L'), np.float32)
    best = max(teil.size)
    for k in (1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8):
        w, h = round(teil.width / k), round(teil.height / k)
        zur = np.asarray(teil.convert('L').resize((w, h), Image.LANCZOS)
                         .resize(teil.size, Image.LANCZOS), np.float32)
        if np.abs(zur - g).mean() < 0.35:
            best = max(w, h)
    return best


def schaerfen(net, pfad):
    im = Image.open(pfad).convert('RGB')
    a = np.asarray(im)
    maske = (a < WEISS).any(2)
    ys, xs = np.where(maske)
    m = 24
    box = (max(xs.min() - m, 0), max(ys.min() - m, 0), min(xs.max() + m + 1, S), min(ys.max() + m + 1, S))
    teil = im.crop(box)
    kante = min(max(echte_kante(teil), MIN_IN), MAX_IN)
    f = kante / max(teil.size)
    klein = teil.resize((max(round(teil.width * f), 8), max(round(teil.height * f), 8)), Image.LANCZOS)
    gross = hochrechnen(net, klein).resize(teil.size, Image.LANCZOS)
    gross = Image.blend(gross, teil, ORIGINAL)
    g = np.asarray(gross).copy()
    g[(g >= WEISS).all(2)] = 255                         # Hintergrund bleibt reinweiss
    out = Image.new('RGB', (S, S), (255, 255, 255))
    out.paste(Image.fromarray(g), box[:2])
    out.save(pfad, quality=95, subsampling=0)
    return kante, f


if __name__ == '__main__':
    torch.set_num_threads(4)
    net = lade(sys.argv[1])
    for p in sys.argv[2:]:
        kante, f = schaerfen(net, p)
        print(f'{p}: Netz-Eingang {kante}px')
