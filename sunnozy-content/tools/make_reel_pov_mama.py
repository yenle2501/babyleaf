"""POV-Reel aus drei KI-Babyclips der Nutzerin (06.11.2026).

Stil nach einem Screenshot der Nutzerin: Clip läuft ruhig durch, ein längerer POV-Satz in weisser Serifenschrift steht
die ganze Zeit mittig im Bild, darunter eine Reihe Emojis. Hier auf Deutsch (Schweizer ss, Du-Form).

    python3 tools/make_reel_pov_mama.py            # alle Text-Varianten aus TEXTE
    python3 tools/make_reel_pov_mama.py mama

Schnitt: Clip 1 (Nähe, Kamera fährt von den Söckchen zum Gesicht) → Clip 2 (Totale) → Clip 3 (näher, leicht gezoomt),
weiche Blenden, Musik Alex Morgan, am Schluss blendet das sunnozy-Logo ein.
Quellen: posts/reels/pov-mama/original/clip_<n>.mp4 (784 × 1168, KI-Video). Ausgabe: posts/reels/pov-mama/reel_pov_<name>_9x16.mp4
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import make_coming_soon_reels as m

W, H, FPS = m.W, m.H, m.FPS
BASIS = os.path.join(m.POSTS, 'reels', 'pov-mama')
CLIP = lambda n: os.path.join(BASIS, 'original', f'clip_{n}.mp4')
MUSIK = os.path.join(m.POSTS, 'reels', 'musik', 'alex-morgan_heartwarming-story.mp3')
SCHRIFT = 'fraunces-400.ttf'            # kräftige Serifenschrift wie im Instagram-Stil
EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

# (Clip, von, bis, Zoom, Fokus y 0..1)
SCHNITT = [(1, 0.4, 6.8, 1.0, 0.5), (2, 15.6, 21.2, 1.0, 0.5), (3, 18.4, 24.6, 1.22, 0.32)]
BLENDE = 0.5

TEXTE = {
    'mama': dict(zeilen=['Sie weiss es noch nicht, aber auf sie', 'warten Kaffee-Dates, Mädelsabende,',
                         'Pediküre und Shoppingtouren', 'mit Mama.'], emoji='💗🌸🎀👛💅🌷💞'),
    'gotti': dict(zeilen=['Sie weiss es noch nicht, aber ihr Gotti', 'wird sie verwöhnen: Glace-Dates,',
                          'Bastelnachmittage, Pyjama-Partys', 'und Geschenke ohne Ende.'], emoji='🎀🍦✂️🌙🎁💗'),
    # Weihnachtsbox «I like flying» (rosa Vögelchen-Body + rosa Leggings), Clip vor dem Weihnachtsbaum
    'weihnachten_mama': dict(schnitt=[('weihnachten', 0.0, 14.9, 1.0, 0.5)], y=1130, ende='i_like_flying', musik_ab=8,
        zeilen=['Sie weiss es noch nicht, aber das', 'ist ihr erstes Weihnachten mit Mama,', 'und unter dem Baum wartet schon',
                'ihre erste Geschenkbox.'], emoji='🎄🎁🎀✨💗⭐'),
    'weihnachten_gotti': dict(schnitt=[('weihnachten', 0.0, 14.9, 1.0, 0.5)], y=1130, ende='i_like_flying', musik_ab=8,
        zeilen=['Sie weiss es noch nicht, aber Gotti hat', 'ihr erstes Weihnachtsgeschenk schon', 'gefunden: rosa, weich',
                'und fertig verpackt.'], emoji='🎄🐦🎀🎁💗✨'),
}


def emoji_bild(s, hoehe):
    fo = ImageFont.truetype(EMOJI_FONT, 109)
    teile = []
    for ch in s:
        if ch in '️':
            continue
        e = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(e).text((70, 70), ch + ('️' if ch == '✂' else ''), font=fo, embedded_color=True, anchor='mm')
        e = e.crop(e.getbbox() or (0, 0, 1, 1))
        teile.append(e.resize((round(e.width * hoehe / 109), round(e.height * hoehe / 109)), Image.LANCZOS))
    gap = round(hoehe * 0.08)
    b = Image.new('RGBA', (sum(t.width for t in teile) + gap * (len(teile) - 1), max(t.height for t in teile)), (0, 0, 0, 0))
    x = 0
    for t in teile:
        b.alpha_composite(t, (x, (b.height - t.height) // 2)); x += t.width + gap
    return b


def text_ebene(t):
    """Weisse Serifenschrift mittig, dünner weicher Schatten wie im Instagram-Stil, Emojis darunter."""
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    g = 60
    while max(d.textlength(z, font=m.f(SCHRIFT, g)) for z in t['zeilen']) > 880:
        g -= 2
    fo = m.f(SCHRIFT, g); lh = g * 1.18
    y0 = t.get('y', 900) - (len(t['zeilen']) - 1) * lh / 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for k, z in enumerate(t['zeilen']):
        ds.text((W / 2 + 1, y0 + k * lh + 2), z, font=fo, fill=(30, 22, 18, 255), anchor='mm', stroke_width=6, stroke_fill=(30, 22, 18, 255))
    weich = sh.filter(ImageFilter.GaussianBlur(9))
    weich.putalpha(weich.getchannel('A').point(lambda v: min(255, int(v * 1.25))))
    c.alpha_composite(weich)
    for k, z in enumerate(t['zeilen']):
        d.text((W / 2, y0 + k * lh), z, font=fo, fill=(255, 255, 255, 255), anchor='mm')
    e = emoji_bild(t['emoji'], round(g * 0.82))
    c.alpha_composite(e, ((W - e.width) // 2, round(y0 + len(t['zeilen']) * lh - g * 0.35)))
    return c


def end_karte(key):
    """Schlusskarte für die Weihnachtsbox: Box-Hauptbild, Name, Inhalt, Preis, Kurzlink, Logo (Creme wie die Box-Reels)."""
    from make_reels_box_schlaf import BOXEN, BOX, WEINROT
    r = BOXEN[key]
    c = Image.new('RGB', (W, H), m.CREME); d = ImageDraw.Draw(c)
    im = Image.open(BOX(key)).convert('RGB'); im.thumbnail((860, 860), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 330))
    d.text((W / 2, 250), 'Weihnachts-Geschenkbox', font=m.f(m.SERIF_I, 58), fill=m.SALBEI, anchor='mm')
    d.text((W / 2, 1290), r['name'], font=m.f(m.SERIF, 96), fill=m.WALD, anchor='mm')
    d.text((W / 2, 1380), r['inhalt'], font=m.f(m.SERIF_I, 52), fill=m.GRAU, anchor='mm')
    d.text((W / 2, 1480), f"CHF {r['preis']}", font=m.f(m.SERIF, 80), fill=WEINROT, anchor='mm')
    d.text((W / 2, 1575), f"sunnozy.ch/{r['kurz']}", font=m.f(m.SERIF, 50), fill=m.WALD, anchor='mm')
    L = m.logo(200, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1640), L)
    return c


def reel(name):
    t = TEXTE[name]
    schnitt = t.get('schnitt', SCHNITT)
    os.makedirs(BASIS, exist_ok=True)
    tmp = os.path.join(BASIS, f'_text_{name}.png'); text_ebene(t).save(tmp)
    L = m.logo(230, (255, 255, 255)); lpfad = os.path.join(BASIS, '_logo.png'); L.save(lpfad)
    ein, fil = [], []
    for i, (n, von, bis, z, fy) in enumerate(schnitt):
        ein += ['-ss', str(von), '-t', str(bis - von), '-i', CLIP(n)]
        fil.append(f'[{i}:v]fps={FPS},scale=-2:{round(1920 * z / 2) * 2}:flags=lanczos,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{fy},'
                   f'unsharp=5:5:0.6,eq=saturation=1.03,setsar=1,format=yuv420p[v{i}]')
    dauern = [b - v for _, v, b, _, _ in schnitt]
    k = len(schnitt)
    letzte, off = 'v0', dauern[0]
    for i in range(1, k):
        off -= BLENDE
        fil.append(f'[{letzte}][v{i}]xfade=transition=fade:duration={BLENDE}:offset={off:.3f}[x{i}]')
        letzte = f'x{i}'; off += dauern[i]
    video = off                                                       # Länge des Videoteils
    T_ENDE = 3.4 if t.get('ende') else 0
    gesamt = video + T_ENDE - (BLENDE if T_ENDE else 0)
    fil.append(f'[{k}:v]format=rgba[txt]')
    fil.append(f'[{letzte}][txt]overlay=0:0[y1]')
    if T_ENDE:
        epfad = os.path.join(BASIS, f'_ende_{name}.png'); end_karte(t['ende']).save(epfad)
        ein += ['-loop', '1', '-t', f'{T_ENDE:.2f}', '-i', epfad]
        fil.append(f'[{k + 1}:v]fps={FPS},setsar=1,format=yuv420p[e]')
        fil.append(f'[y1]format=yuv420p[y1b]')
        fil.append(f'[y1b][e]xfade=transition=fade:duration={BLENDE}:offset={video - BLENDE:.3f},format=yuv420p[out]')
    else:
        ein += ['-loop', '1', '-t', f'{gesamt:.2f}', '-i', lpfad]
        fil.append(f'[{k + 1}:v]format=rgba,fade=t=in:st={gesamt - 2.6:.2f}:d=0.8:alpha=1[lg]')
        fil.append(f'[y1][lg]overlay=(W-w)/2:1235:enable=\'gte(t,{gesamt - 2.6:.2f})\',format=yuv420p[out]')
    fil.append(f'[{k + 2}:a]atrim=0:{gesamt:.2f},afade=t=in:d=0.5,afade=t=out:st={gesamt - 1.8:.2f}:d=1.8,volume=0.85[a]')
    pfad = os.path.join(BASIS, f'reel_pov_{name}_9x16.mp4')
    # Reihenfolge der Eingänge: Clips, Text, Schluss (Karte oder Logo), Musik
    clips = ein[:6 * k]; schluss = ein[6 * k:]          # je Clip: -ss von -t dauer -i datei
    cmd = (['ffmpeg', '-y', '-v', 'error'] + clips + ['-loop', '1', '-t', f'{gesamt:.2f}', '-i', tmp] + schluss +
           ['-ss', str(t.get('musik_ab', 30)), '-i', MUSIK, '-filter_complex', ';'.join(fil), '-map', '[out]', '-map', '[a]',
            '-t', f'{gesamt:.2f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-r', str(FPS),
            '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', pfad])
    subprocess.run(cmd, check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '1.5', '-i', pfad, '-frames:v', '1', '-q:v', '2',
                    pfad.replace('.mp4', '_titelbild.jpg')], check=True)
    for q in (tmp, lpfad, os.path.join(BASIS, f'_ende_{name}.png')):
        if os.path.exists(q):
            os.remove(q)
    print(f'{pfad}: {gesamt:.1f} s', flush=True)


if __name__ == '__main__':
    for n in sys.argv[1:] or list(TEXTE):
        reel(n)
