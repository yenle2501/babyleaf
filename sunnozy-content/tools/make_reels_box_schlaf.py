"""Weihnachts-Geschenkboxen: ruhige POV-Reels mit schlafendem Baby (04.11.2026).

Gleiche Machart wie die Baby-Reels, die gut liefen: schlafendes Baby, langsamer Zoom, kurzer POV-Text ab Sekunde 0
(Cormorant Garamond, unteres Drittel), dann die Box mit Inhalt und Preis, Schlusskarte mit Kurzlink direkt zur Box.

    python3 tools/make_reels_box_schlaf.py              # alle Boxen, für die ein Babybild in baby/ liegt
    python3 tools/make_reels_box_schlaf.py mum_dad_me

Babybilder: KI (Canva), fiktive Babys, Safe Sleep (Rückenlage, flache Matratze, nichts im Bettchen, keine Mütze/kein Haarband).
Ausgabe: posts/kampagne-weihnachtsbox/reels-schlaf/reel_<box>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, m.FPS
BASIS = os.path.join(m.POSTS, 'kampagne-weihnachtsbox')
OUT = os.path.join(BASIS, 'reels-schlaf')
BABY = os.path.join(OUT, 'baby')
BOX = lambda k: os.path.join(BASIS, 'rote-box', 'shopify', 'geschenkbox-' + k.replace('_', '-') + '.jpg')
MUSIK = [os.path.join(m.POSTS, 'reels', 'musik', n) for n in ('alex-morgan_heartwarming-story.mp3', 'alex-morgan_no-copyright-music.mp3')]
WEINROT = (98, 22, 30)

# Preise und Inhalt wie in Shopify (Stand 04.11.2026), Kurzlink = Shopify-Weiterleitung auf die Box
BOXEN = {
    'mum_dad_me': dict(name='«Mum Dad Me»', inhalt='5 Bodys + 5 Leggings', preis='47.90', kurz='box-mum-dad-me',
        hook=['POV: Grosi hat die', 'schönste Box gefunden'], hook2=['und sie liegt schon', 'unter dem Baum']),
    'lovely_little_girl': dict(name='«Lovely Little Girl»', inhalt='3 Bodys + 5 Leggings', preis='44.90', kurz='box-lovely',
        hook=['POV: Ihr erstes Weihnachten', 'und Gotti hat vorgesorgt'], hook2=['«Lovely Little Girl»', 'fertig verpackt']),
    'growing_up_strong': dict(name='«Growing up strong»', inhalt='5 Bodys + 5 Jogginghosen', preis='47.90', kurz='box-growing-up-strong',
        hook=['POV: Götti schenkt', 'dieses Jahr Bodys'], hook2=['5 Bodys und 5 Hosen', 'in der roten Box']),
    'i_love_my_mummy': dict(name='«I love my Mummy»', inhalt='3 Bodys + 3 Halstücher', preis='34.90', kurz='box-i-love-my-mummy',
        hook=['POV: Mamas erstes', 'Weihnachten mit Baby'], hook2=['«I love my Mummy»', 'liegt schon bereit']),
    'dino': dict(name='«Dino»', inhalt='3 Bodys + 3 Mulltücher', preis='44.90', kurz='box-dino',
        hook=['POV: Opa hat den', 'kleinen Dino entdeckt'], hook2=['3 Bodys und 3 Mulltücher', 'fertig verpackt']),
    'dinosaur': dict(name='«Dinosaur»', inhalt='5 Bodys + 5 Jogginghosen', preis='47.90', kurz='box-dinosaur',
        hook=['POV: Er schläft', 'und der Baum leuchtet'], hook2=['«Dinosaur» liegt', 'schon darunter']),
    'little_one': dict(name='«Little One»', inhalt='5 Bodys + 3 Mulltücher', preis='49.90', kurz='box-little-one',
        hook=['POV: Deine Freundin', 'hat gerade geboren'], hook2=['und Du weisst sofort,', 'was Du schenkst']),
    'i_like_flying': dict(name='«I like flying»', inhalt='3 Bodys + 5 Leggings', preis='44.90', kurz='box-i-like-flying',
        hook=['POV: Tante sein', 'und das Geschenk ist da'], hook2=['«I like flying»', 'in Rosa und Pastell']),
    'little_one_jogginghosen': dict(name='«Little One»', inhalt='5 Bodys + 5 Jogginghosen', preis='47.90', kurz='box-little-one-hosen',
        hook=['POV: Grosi hat', 'schon eingepackt'], hook2=['weiche Ripp-Bodys', 'und Hosen']),
}
T_A, T_B, T_BOX, T_END = 4.6, 3.0, 2.6, 2.6


def baby_bild(k):
    for e in ('.png', '.jpg'):
        p = os.path.join(BABY, k + e)
        if os.path.exists(p):
            return Image.open(p).convert('RGB')


def zoom_bild(im, z, fx, fy):
    """9:16-Ausschnitt mit Zoom z um den Punkt (fx, fy)."""
    s = max(W / im.width, H / im.height) * z
    w, h = im.width * s, im.height * s
    x = min(max(fx * w - W / 2, 0), w - W); y = min(max(fy * h - H / 2, 0), h - H)
    return im.resize((round(w), round(h)), Image.BICUBIC).crop((round(x), round(y), round(x) + W, round(y) + H)).convert('RGBA')


def box_karte(r, t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.6)
    im = Image.open(r['box']).convert('RGB'); s = 900 / max(im.size) * (0.96 + 0.04 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 840 - im.height // 2))
    d.text((W / 2, 300), 'Weihnachts-Geschenkbox', font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    d.text((W / 2, 1380), r['name'], font=m.f(m.SERIF, 96 if len(r['name']) < 18 else 80), fill=m.WALD, anchor='mm')
    d.text((W / 2, 1470), r['inhalt'], font=m.f(m.SERIF_I, 52), fill=m.GRAU, anchor='mm')
    return c


def end_karte(r):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 600), r['name'], font=m.f(m.SERIF, 100 if len(r['name']) < 18 else 84), fill=m.WALD, anchor='mm')
    d.text((W / 2, 715), r['inhalt'], font=m.f(m.SERIF_I, 52), fill=m.GRAU, anchor='mm')
    d.text((W / 2, 850), f"CHF {r['preis']}", font=m.f(m.SERIF, 92), fill=WEINROT, anchor='mm')
    d.line((W / 2 - 70, 945, W / 2 + 70, 945), fill=(200, 192, 180), width=2)
    d.text((W / 2, 1020), 'Fertig verpackt, gratis geliefert', font=m.f(m.SERIF_I, 50), fill=m.GRAU, anchor='mm')
    d.text((W / 2, 1085), 'Grössen 0–9 Monate', font=m.f(m.SERIF_I, 50), fill=m.GRAU, anchor='mm')
    d.text((W / 2, 1200), f"sunnozy.ch/{r['kurz']}", font=m.f(m.SERIF, 56), fill=m.WALD, anchor='mm')
    L = m.logo(240, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1330), L)
    return c


def reel(key, nr):
    r = dict(BOXEN[key]); r['box'] = BOX(key)
    baby = baby_bild(key)
    teile = [dict(start=0, dauer=T_A, art='baby', z=(1.0, 1.08), f=(0.5, 0.42), text=r['hook']),
             dict(start=T_A, dauer=T_B, art='baby', z=(1.22, 1.28), f=(0.5, 0.58), text=r['hook2']),
             dict(start=T_A + T_B, dauer=T_BOX, art='box'),
             dict(start=T_A + T_B + T_BOX, dauer=T_END, art='end')]
    t_ges = sum(tl['dauer'] for tl in teile)
    end = end_karte(r)
    n = int(round(t_ges * FPS)); nb = int(m.BLENDE * FPS)

    def bild(tl, t):
        if tl['art'] == 'box':
            return box_karte(r, t)
        if tl['art'] == 'end':
            return end
        e = m.ease(t / tl['dauer']); z0, z1 = tl['z']
        return zoom_bild(baby, z0 + (z1 - z0) * e, *tl['f'])

    def roh(s):
        idx = max(i for i, tl in enumerate(teile) if tl['start'] <= s + 1e-9)
        tl = teile[idx]; t = min(s - tl['start'], tl['dauer'] - 1e-3)
        c = bild(tl, t)
        if tl['art'] == 'baby':
            alpha = 1.0 if idx == 0 else min(1, t / 0.25)
            m.text_unten(c, tl['text'], alpha)
        if idx + 1 < len(teile) and s > tl['start'] + tl['dauer'] - m.BLENDE:     # weiche Blende statt harter Schnitt (ruhig)
            a = (s - (tl['start'] + tl['dauer'] - m.BLENDE)) / m.BLENDE
            nxt = bild(teile[idx + 1], 0)
            if teile[idx + 1]['art'] == 'baby':
                nxt = m.text_unten(nxt.copy(), teile[idx + 1]['text'], 0)
            c = Image.blend(c, nxt, min(a, 1))
        return c

    erstes = roh(0)
    os.makedirs(OUT, exist_ok=True)
    datei = f'reel_{key}_9x16'
    pfad = os.path.join(OUT, datei + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        c = roh(i / FPS)
        if i >= n - nb:
            c = Image.blend(c, erstes, (i - (n - nb)) / nb)                          # Loop zurück ins erste Bild
        fr = c.convert('RGB')
        if i == int(0.6 * FPS):
            fr.save(os.path.join(OUT, datei + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    dauer = n / FPS
    musik = MUSIK[nr % 2]; ab = 6 + (nr * 13) % 60
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', musik, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.6,afade=t=out:st={dauer - 1.4:.2f}:d=1.4,volume=0.8', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s', flush=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or [k for k in BOXEN if baby_bild(k) is not None]
    for nr, k in enumerate(keys):
        reel(k, nr)
