"""Mix-Reels: mehrere Grok-Babyclips zusammengeschnitten (18.11.2026).

Formate aus der Viral-Analyse:
  - «Welches nimmst Du? 1–4»: je Clip 2.5 s, grosse Nummer, Hook oben die ganze Zeit → Kommentare mit der Nummer
  - Kompilation: 4–5 Strecker hintereinander, harte Schnitte im Takt, Hook am Anfang und zum Loop am Ende
Bearbeitung v2: bei jedem Schnitt kurzer Zoom 108 % → 100 % (Zoom-Übergang), Hook tippt sich in 0.5 s ein.
Endfolie: Collage der gezeigten Sets (2×2) oder Set-Bild. Musik: Alex Morgan. Kein Preis.

    python3 tools/make_baby_reels_mix.py [name ...]
Ausgabe: posts/baby-reels/mix/reel_mix_<name>_9x16.mp4 + _titelbild.jpg
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import make_coming_soon_reels as m
import make_baby_reels as b
from endfolie import anhaengen, SET, SHOP, CS_AUFRUF

W, H, FPS = b.W, b.H, b.FPS
OUT = os.path.join(m.POSTS, 'baby-reels', 'mix')

# (clip, start_s, nummer_label)
REELS = {
    'welches_set_shop': dict(
        hook=['Welches Set nimmst Du?', 'Schreib die Nummer'], emo='👇', nummern=True, seg=2.5,
        clips=[('set_little_bear_baby_strampler_1.mp4', 3.0), ('set_hello_world_blatt_baby_body_1.mp4', 3.0),
               ('set_teddy_creme_baby_strampler_1.mp4', 3.0), ('set_rosa_baby_strampler_1.mp4', 3.0)],
        ende=(['little_bear', 'hello_world_blatt', 'teddy_creme', 'rosa'], '1, 2, 3 oder 4?', 'Erstausstattungen · 5–8 Teile', SHOP)),
    'gotti_such_aus': dict(
        hook=['Gotti, such Dir eins aus'], emo='🎀', nummern=True, seg=2.5,
        clips=[('set_teddy_rosa_punkte_baby_strampler_1.mp4', 3.0), ('set_prinzessin_krone_baby_body_1.mp4', 3.0),
               ('set_little_and_loved_gans_rosa_baby_strampler_1.mp4', 3.0), ('set_hase_rosa_baby_body_1.mp4', 3.0)],
        ende=(['teddy_rosa_punkte', 'prinzessin_krone', 'little_and_loved_gans_rosa', 'hase_rosa'], 'Welche Nummer?', 'Schick das der Gotti', CS_AUFRUF)),
    'es_wird_ein_bub': dict(
        hook=['POV: Es wird ein Bub'], emo='💙', nummern=True, seg=2.5,
        clips=[('set_weltall_hellblau_baby_body_1.mp4', 3.0), ('set_wal_blau_baby_strampler_1.mp4', 3.0),
               ('set_waldbaer_creme_baby_body_1.mp4', 3.0), ('set_bauernhof_baby_strampler_2.mp4', 3.0)],
        ende=(['weltall_hellblau', 'wal_blau', 'waldbaer_creme', 'bauernhof'], 'Welches für Euren Bub?', 'coming soon', CS_AUFRUF)),
    'es_wird_ein_maedchen': dict(
        hook=['POV: Es wird ein Mädchen'], emo='🎀', nummern=True, seg=2.5,
        clips=[('set_rosa_baby_strampler_2.mp4', 3.0), ('set_gaensebluemchen_baby_strampler_1.mp4', 3.0),
               ('set_lila_hase_baby_body_2.mp4', 3.0), ('set_hello_schmetterling_baby_body_1.mp4', 3.0)],
        ende=(['rosa', 'gaensebluemchen', 'lila_hase', 'hello_schmetterling'], 'Welches für Eure Kleine?', 'Erstausstattungen und coming soon', SHOP)),
    'babyfieber_kompilation': dict(
        hook=['Warnung:', '5× Babyfieber am Stück'], emo='🥹', nummern=False, seg=2.0,
        clips=[('set_little_bear_baby_strampler_1.mp4', 3.2), ('set_love_dad_mom_baby_body_2.mp4', 3.2),
               ('set_hello_world_blatt_baby_body_2.mp4', 3.2), ('set_teddy_rosa_punkte_baby_strampler_2.mp4', 3.2),
               ('set_prinzessin_krone_baby_body_2.mp4', 3.2)],
        ende=(['little_bear', 'love_dad_mom', 'hello_world_blatt', 'teddy_rosa_punkte'], 'sunnozy Babysets', 'Erstausstattungen und coming soon', SHOP)),
    'haende_hoch': dict(
        hook=['Hände hoch,', 'wer Babyfieber hat'], emo='🙌', nummern=False, seg=2.0,
        clips=[('set_prinzessin_krone_baby_body_1.mp4', 3.6), ('set_little_bear_baby_body_1.mp4', 3.6),
               ('set_waldbaer_creme_baby_body_1.mp4', 4.0), ('set_hello_world_creme_baby_body_2.mp4', 3.6),
               ('set_love_dad_mom_baby_body_1.mp4', 3.6)],
        ende=(['prinzessin_krone', 'little_bear', 'waldbaer_creme', 'love_dad_mom'], 'sunnozy Babysets', 'Erstausstattungen und coming soon', SHOP)),
}


def collage(sets, pfad):
    c = Image.new('RGB', (1000, 1000), (250, 246, 240))
    for k, s in enumerate(sets):
        im = Image.open(f'{SET}/set_{s}_quadratisch.jpg').convert('RGB').resize((490, 490), Image.LANCZOS)
        c.paste(im, ((k % 2) * 510, (k // 2) * 510))
    c.save(pfad, quality=92)
    return pfad


def frames(clip, start, dauer):
    pfad = os.path.join(b.VID, clip)
    w, h = b.groesse(pfad); sw = round(w * H / h / 2) * 2
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dauer), '-i', pfad, '-map', '0:v:0',
                          '-vf', f'fps={FPS},{b.GRADE},scale={sw}:{H}:flags=lanczos,crop={W}:{H}:{(sw - W) // 2}:0',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = W * H * 3; k = 0
    while k < int(round(dauer * FPS)):
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield Image.frombuffer('RGB', (W, H), buf); k += 1
    p.kill()


def nummer(n):
    fo = ImageFont.truetype(b.SCHRIFT, 150)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((W / 2 + 3, 1560 + 4), str(n), font=fo, fill=(40, 30, 25, 140), anchor='mm')
    d.text((W / 2, 1560), str(n), font=fo, fill=(255, 255, 255, 255), anchor='mm')
    return im


def reel(name):
    r = REELS[name]
    ebene = b.text_ebene(r['hook'], r['emo'])
    seg = r['seg']; dauer = seg * len(r['clips'])
    os.makedirs(OUT, exist_ok=True)
    pfad = os.path.join(OUT, f'reel_mix_{name}_9x16.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'veryfast', tmp], stdin=subprocess.PIPE)
    i = 0
    for k, (clip, start) in enumerate(r['clips']):
        num = nummer(k + 1) if r['nummern'] else None
        for j, fr in enumerate(frames(clip, start, seg)):
            t = i / FPS; tj = j / FPS
            if tj < 0.25:                                                # Zoom-Übergang bei jedem Schnitt
                f = 1 + 0.08 * (1 - m.ease(tj / 0.25)); w2, h2 = round(W * f), round(H * f)
                fr = fr.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
            if r['nummern']:
                a = 1.0                                                  # Hook bleibt stehen, damit man mitzählt
            else:
                a = 1 - m.ease((t - 2.2) / 0.4) if t < dauer - 1.6 else m.ease((t - (dauer - 1.6)) / 0.4)
            c = fr.convert('RGBA')
            if t < b.TIPP_BIS:
                ges = sum(len(z) for z in r['hook']); kk = max(1, int(ges * t / b.TIPP_BIS) + 1)
                c.alpha_composite(b.text_ebene(b.teil(r['hook'], kk), r['emo'], mit_emoji=False, voll=r['hook']))
            elif a > 0:
                e = ebene.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * a)))
                c.alpha_composite(e)
            if num is not None:
                c.alpha_composite(num)
            if i == int(0.5 * FPS):
                c.convert('RGB').save(pfad.replace('.mp4', '_titelbild.jpg'), quality=92)
            enc.stdin.write(c.convert('RGB').tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    dauer = i / FPS
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', '4', '-i', b.MUSIK, '-t', f'{dauer:.2f}',
                    '-af', 'afade=t=in:d=0.3,volume=1.6,alimiter=limit=0.89',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    sets, titel, zeile, aufruf = r['ende']
    bild = collage(sets, os.path.join('/tmp', f'collage_{name}.jpg'))
    anhaengen(pfad, bild, titel, zeile, aufruf)


if __name__ == '__main__':
    for name in (sys.argv[1:] or list(REELS)):
        reel(name)
