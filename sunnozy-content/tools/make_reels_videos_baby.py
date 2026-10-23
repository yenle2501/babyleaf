"""Reels aus den KI-Babyclips in posts/videos-baby/: Hook ab Sekunde 0, Schnitte, Zoom, Set-Karte, Preis, Musik, Loop.

    python3 tools/make_reels_videos_baby.py               # alle Reels aus REELS
    python3 tools/make_reels_videos_baby.py kirschen      # nur eines

Ausgabe flach nach posts/reels/coming-soon/ (Reel 9:16 und Titelbild), Schrift Cormorant Garamond wie
make_coming_soon_reels.py. Musik: posts/reels/musik/ (Alex Morgan, Pixabay, frei nutzbar), abwechselnd pro Reel.

Segment: (clip, von, bis, tempo, zoom0, zoom1, fx, fy)
  tempo < 1 = Zeitlupe; zoom 1 = Clip füllt 9:16; fx/fy = Bildmitte (Anteil der Clipbreite/-höhe)
texte: eine Liste pro Segment (Zeilen) oder None = Text des vorherigen Segments bleibt stehen
"""
import os, sys, subprocess
from PIL import Image, ImageDraw
import make_coming_soon_reels as m
import make_coming_soon_kombi as k

P = m.POSTS
VB = os.path.join(P, 'videos-baby')
MUSIK = [os.path.join(P, 'reels', 'musik', n) for n in ('alex-morgan_heartwarming-story.mp3', 'alex-morgan_no-copyright-music.mp3')]
CS = lambda d: os.path.join(P, 'coming-soon', d, 'shop', d + '_shop_ohne_logo.jpg')
PR = lambda s: os.path.join(P, 'produktfotos-set-praesentation', 'ohne_logo', f'set_{s}_quadratisch.jpg')
W, H, FPS = m.W, m.H, m.FPS
ZMAX, ZMAX_KLEIN = 1.25, 1.6        # mehr Zoom macht die 848-px-Clips unscharf; Bauernhof-Baby ist sehr klein im Bild
KLEIN = {'bauernhof_a'}

# sanfterer Verlauf hinter dem Text als in make_coming_soon_reels (Bild bleibt hell)
import numpy as np
_g = np.zeros((H, 1), np.float32); _g[1120:, 0] = np.clip(np.arange(H - 1120) / 380.0, 0, 1) ** 1.3 * 0.42
m.VERLAUF = Image.fromarray((_g * 255).astype(np.uint8)).resize((W, H))


def ausschnitt(im, zoom, fx, fy):
    """9:16-Ausschnitt, danach immer leicht nachgeschärft."""
    from PIL import ImageFilter
    out = k.ausschnitt(im, zoom, fx, fy).convert('RGB')
    return out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2)).convert('RGBA')


def seg(clip, von, bis, z0=1.0, z1=1.06, fx=0.5, fy=0.45, tempo=1.0):
    zm = ZMAX_KLEIN if clip in KLEIN else ZMAX
    return (clip, von, bis, tempo, min(z0, zm), min(z1, zm), fx, fy)


REELS = {
    'eisbaer_taupe': dict(name='«Eisbär»', teile='Strampler, Body, Mütze, Fäustlinge, Lätzchen', preis='20.90', bild=CS('eisbaer-taupe'),
        segmente=[seg('eisbaer_taupe_a', 0, 4), seg('eisbaer_taupe_a', 5, 7.5, 1.35, 1.45, 0.45, 0.5), seg('eisbaer_taupe_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['POV: Dein Winterbaby', 'kommt im Dezember'], ['Strampler mit Eisbären,', 'Mütze mit Öhrchen'], ['5 Teile für', 'die ersten Wochen']]),
    'dino_cool_dude': dict(name='«Cool Dude»', teile='6 Teile mit Dino', preis='26.90', bild=CS('dino-cool-dude'),
        segmente=[seg('dino_cool_dude_a', 0, 4), seg('dino_cool_dude_a', 4.5, 7, 1.4, 1.5, 0.5, 0.45), seg('dino_cool_dude_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['Wenn er jetzt schon', 'cooler ist als Papa'], ['«Cool Dude»', 'mit Dino'], ['6 Teile,', 'alles passt zusammen']]),
    'born_in_2027_rosa': dict(name='«Born in 2027»', teile='6 Teile in Rosa', preis='26.90', bild=CS('born-in-2027-rosa'),
        segmente=[seg('born_in_2027_rosa_a', 0, 4, fx=0.55), seg('born_in_2027_rosa_a', 5, 7.5, 1.4, 1.5, 0.6, 0.42), seg('born_in_2027_rosa_a', 9, 13, 1.05, 1.0, fx=0.55, tempo=0.85)],
        texte=[['Born in 2027?', 'Dann ist das ihr Set'], ['Body, Hose, Mütze', 'in Rosa'], ['Schick das der Freundin,', 'die 2027 Mama wird']]),
    'segelboote': dict(name='Strampler «Segelboote»', teile='3 Strampler in Creme und Blau', preis='25.90', bild=CS('strampler-segelboote'),
        segmente=[seg('strampler_segelboote_a', 0, 4), seg('strampler_segelboote_a', 5, 7.5, 1.4, 1.5, 0.48, 0.5), seg('strampler_segelboote_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['POV: Sein erster', 'Mittagsschlaf zu Hause'], ['Strampler mit', 'kleinen Segelbooten'], ['3 Strampler', 'im Set']]),
    'rosa_little_princess': dict(name='Strampler «Little Princess»', teile='3 Strampler in Rosa und Creme', preis='25.90', bild=CS('strampler-rosa-little-princess'),
        segmente=[seg('strampler_rosa_little_princess_a', 0, 4), seg('strampler_rosa_little_princess_a', 5, 7.5, 1.4, 1.5, 0.48, 0.45), seg('strampler_rosa_little_princess_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['POV: Sie ist', 'endlich da'], ['Strampler', '«Little Princess»'], ['3 Strampler', 'im Set']]),
    'kirschen': dict(name='Strampler «Kirschen»', teile='3 Strampler: Weinrot, Altrosa, Weiss', preis='25.90', bild=CS('strampler-kirschen'),
        segmente=[seg('strampler_kirschen_a', 0, 4), seg('strampler_kirschen_a', 6, 8, 1.35, 1.45, 0.48, 0.5), seg('strampler_kirschen_b', 0, 3.5, fx=0.45), seg('strampler_kirschen_b', 9, 12, 1.0, 1.08, 0.5, 0.45)],
        texte=[['Welcher ist', 'Dein Favorit?'], ['1: Weiss mit Kirschen'], ['2: Weinrot mit «Smile»'], ['3: Altrosa', 'Schreib 1, 2 oder 3']]),
    'kaetzchen_tulpen': dict(name='«Kätzchen & Tulpen»', teile='2 Strampler mit Mütze', preis='19.90', bild=CS('strampler-kaetzchen-tulpen'),
        segmente=[seg('strampler_kaetzchen_tulpen_a', 0, 4), seg('strampler_kaetzchen_tulpen_a', 5, 7.5, 1.4, 1.5, 0.48, 0.45), seg('strampler_kaetzchen_tulpen_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['POV: Sie schläft', 'endlich'], ['Kätzchen-Strampler', 'mit lila Kragen'], ['2 Strampler', 'und eine Mütze']]),
    'blumen_hase': dict(name='«Blumen & Hase»', teile='2 Strampler mit Haarband', preis='19.90', bild=CS('strampler-blumen-hase'),
        segmente=[seg('strampler_blumen_hase_a', 0, 4, fx=0.42), seg('strampler_blumen_hase_a', 4, 6, 1.4, 1.5, 0.45, 0.5), seg('strampler_blumen_hase_a', 6, 8.5, 1.05, 1.0, fx=0.42, tempo=0.85)],
        texte=[['Blümchen', 'von Kopf bis Fuss'], ['mit passendem', 'Haarband'], ['2 Strampler', 'im Set']]),
    'weltall': dict(name='«Little One» Weltall', teile='Body, Hose, Mütze', preis='15.90', bild=CS('weltall-hellblau'),
        segmente=[seg('weltall_hellblau_a', 0, 4), seg('weltall_hellblau_a', 5, 7.5, 1.4, 1.5, 0.48, 0.42), seg('weltall_hellblau_a', 9, 13, 1.05, 1.0, tempo=0.85)],
        texte=[['POV: Euer kleiner', 'Astronaut'], ['Body mit Planet,', 'Hose mit Weltall'], ['3 Teile', 'mit Mütze']]),
    'little_princess_wickelbody': dict(name='«Little Princess»', teile='Wickelbody, Hose, Mütze', preis='15.90', bild=CS('little-princess-wickelbody'),
        segmente=[seg('little_princess_wickelbody_a', 0, 4, fx=0.55), seg('little_princess_wickelbody_a', 5, 7.5, 1.35, 1.45, 0.58, 0.42), seg('little_princess_wickelbody_a', 9, 13, 1.05, 1.0, fx=0.6, tempo=0.85)],
        texte=[['Kleine Prinzessin,', 'grosser Blick'], ['Wickelbody mit Krone,', 'nichts über den Kopf'], ['3 Teile', 'mit Mütze']]),
    'hase_rosa': dict(name='«Hase» Rosa', teile='8 Teile mit Hasen-Rassel', preis='30.90', bild=PR('hase_rosa'),
        segmente=[seg('hase_rosa_a', 0, 3.5, fx=0.42), seg('hase_rosa_b', 0, 3), seg('hase_rosa_a', 9, 13, 1.0, 1.1, 0.5, 0.5, tempo=0.85), seg('hase_rosa_c', 1, 4)],
        texte=[['Wenn die Rassel', 'spannender ist als alles'], ['Strampler', 'mit Hasen'], ['Die Hasen-Rassel', 'ist im Set dabei'], None]),
    'love_dad_mom': dict(name='«I love Dad Mom»', teile='6 Teile in Weiss', preis='26.90', bild=PR('love_dad_mom'),
        segmente=[seg('love_dad_mom_a', 0, 4, fx=0.55), seg('love_dad_mom_a', 6, 8.5, 1.3, 1.4, 0.55, 0.45), seg('love_dad_mom_a', 10, 14, 1.05, 1.0, fx=0.55, tempo=0.85)],
        texte=[['Schick das', 'Mama und Papa'], ['Body', '«I love Dad Mom»'], ['6 Teile', 'für die Kleinsten']]),
    'lila_hase': dict(name='«little and cute» Hase', teile='6 Teile in Lila', preis='26.90', bild=PR('lila_hase'),
        segmente=[seg('lila_hase_a', 0, 4, fx=0.55), seg('lila_hase_b', 1, 4.5, fx=0.55), seg('lila_hase_a', 9, 13, 1.0, 1.06, 0.55, 0.45, tempo=0.85)],
        texte=[['POV: Sie hat', 'ihren Hasen gefunden'], ['Body in Lila', '«little and cute»'], ['6 Teile', 'mit Mütze und Hose']]),
    'wal_blau': dict(name='«Wal» Hellblau', teile='8 Teile', preis='30.90', bild=PR('wal_blau'),
        segmente=[seg('wal_blau_a', 0, 4, fx=0.55), seg('wal_blau_b', 1, 4.5, fx=0.55), seg('wal_blau_a', 7, 10, 1.25, 1.35, 0.55, 0.5, tempo=0.85)],
        texte=[['Ganz nah:', '«Wal» in Hellblau'], ['Strampler', 'mit kleinen Walen'], ['8 Teile,', 'alles drin']]),
    'gaensebluemchen_beautiful': dict(name='«Beautiful» Gänseblümchen', teile='Body, Hose, Mütze in Apricot', preis='15.90', bild=CS('gaensebluemchen-beautiful'),
        segmente=[seg('gaensebluemchen_beautiful_a', 0, 4), seg('gaensebluemchen_beautiful_b', 2, 5.5), seg('gaensebluemchen_beautiful_a', 9, 13, 1.0, 1.08, 0.55, 0.42, tempo=0.85)],
        texte=[['Der grosse', 'Strecker'], ['Body «Beautiful»', 'mit Gänseblümchen'], ['3 Teile', 'in Apricot']]),
    'hund_creme': dict(name='«I love Dogs»', teile='8 Teile in Creme', preis='30.90', bild=CS('strampler-hund-creme'),
        segmente=[seg('hund_creme_a', 0, 4, fx=0.45), seg('hund_creme_b', 0, 3.5, fx=0.45), seg('hund_creme_a', 9, 13, 1.0, 1.06, 0.5, 0.45, tempo=0.85)],
        texte=[['POV: Sein erster', 'bester Freund'], ['Strampler', '«I love Dogs»'], ['8 Teile', 'in Creme']]),
    'gaensebluemchen': dict(name='«It\'s a baby girl»', teile='8 Teile mit Gänseblümchen', preis='30.90', bild=PR('gaensebluemchen'),
        segmente=[seg('gaensebluemchen_a', 0, 3.5, fx=0.42), seg('gaensebluemchen_c', 4, 7.5, fx=0.45), seg('gaensebluemchen_c', 10, 13.5, 1.0, 1.06, 0.5, 0.4, tempo=0.85)],
        texte=[['Gänseblümchen', 'für Dein Mädchen'], ['Strampler', 'mit Rüschen'], ['8 Teile,', 'fertig abgestimmt']]),
    'bauernhof': dict(name='«Bauernhof»', teile='8 Teile mit Tieren', preis='30.90', bild=PR('bauernhof'),
        segmente=[seg('bauernhof_a', 0, 4, 1.7, 1.8, 0.5, 0.5), seg('bauernhof_a', 5, 8, 2.1, 2.2, 0.48, 0.5), seg('bauernhof_a', 10, 13.5, 1.8, 1.7, 0.5, 0.5)],
        texte=[['Kleiner', 'Bauernhof-Fan'], ['Strampler mit', 'Kühen und Schafen'], ['8 Teile', 'in Creme']]),
    # ---- Sammel-Reels (mehrere Sets) ----
    'welches_set_jungs': dict(
        segmente=[seg('dino_cool_dude_a', 0, 1.2), seg('weltall_hellblau_a', 0, 1.2), seg('strampler_segelboote_a', 0, 1.2),
                  seg('dino_cool_dude_a', 9, 11.4), seg('weltall_hellblau_a', 5, 7.4, 1.05, 1.12), seg('strampler_segelboote_a', 5, 7.4, 1.05, 1.12),
                  seg('wal_blau_b', 1, 3.4, fx=0.55), seg('eisbaer_taupe_a', 5, 7.4, 1.05, 1.12)],
        texte=[['Welches Set', 'für einen Jungen?'], None, None, {'zahl': '1', 'name': '«Cool Dude»'}, {'zahl': '2', 'name': '«Little One» Weltall'},
               {'zahl': '3', 'name': '«Segelboote»'}, {'zahl': '4', 'name': '«Wal»'}, {'zahl': '5', 'name': '«Eisbär»'}],
        liste=('Welches nimmst Du?', [('1  «Cool Dude»', 'CHF 26.90'), ('2  «Little One» Weltall', 'CHF 15.90'), ('3  «Segelboote»', 'CHF 25.90'),
               ('4  «Wal»', 'CHF 30.90'), ('5  «Eisbär»', 'CHF 20.90')], ['Schreib die Zahl in die Kommentare', 'Link in der Bio'])),
    'welches_set_maedchen': dict(
        segmente=[seg('strampler_kirschen_b', 0, 1.2, fx=0.45), seg('hase_rosa_a', 0, 1.2, fx=0.42), seg('lila_hase_a', 0, 1.2, fx=0.55),
                  seg('strampler_kirschen_a', 0, 2.4), seg('hase_rosa_c', 1, 3.4), seg('lila_hase_b', 1, 3.4, fx=0.55),
                  seg('little_princess_wickelbody_a', 0, 2.4, fx=0.55), seg('strampler_blumen_hase_a', 0, 2.4, fx=0.42)],
        texte=[['Welches Set', 'für ein Mädchen?'], None, None, {'zahl': '1', 'name': '«Kirschen»'}, {'zahl': '2', 'name': '«Hase» Rosa'},
               {'zahl': '3', 'name': '«little and cute»'}, {'zahl': '4', 'name': '«Little Princess»'}, {'zahl': '5', 'name': '«Blumen & Hase»'}],
        liste=('Welches nimmst Du?', [('1  «Kirschen»', 'CHF 25.90'), ('2  «Hase» Rosa', 'CHF 30.90'), ('3  «little and cute»', 'CHF 26.90'),
               ('4  «Little Princess»', 'CHF 15.90'), ('5  «Blumen & Hase»', 'CHF 19.90')], ['Schreib die Zahl in die Kommentare', 'Link in der Bio'])),
    'unter_20_franken': dict(
        segmente=[seg('weltall_hellblau_a', 0, 2.6), seg('gaensebluemchen_beautiful_b', 2, 4.4), seg('little_princess_wickelbody_a', 5, 7.4, 1.05, 1.12, 0.58, 0.45),
                  seg('strampler_kaetzchen_tulpen_a', 0, 2.4), seg('strampler_blumen_hase_a', 3, 5.4, fx=0.42)],
        texte=[['Erstausstattung', 'unter 20 Franken'], ['«Little One» Weltall', 'CHF 15.90'], ['«Little Princess»', 'CHF 15.90'],
               ['«Kätzchen & Tulpen»', 'CHF 19.90'], ['«Blumen & Hase»', 'CHF 19.90']],
        liste=(['Alle unter', 'CHF 20'], [('«Little One» Weltall', 'CHF 15.90'), ('«Beautiful»', 'CHF 15.90'), ('«Little Princess»', 'CHF 15.90'),
               ('«Kätzchen & Tulpen»', 'CHF 19.90'), ('«Blumen & Hase»', 'CHF 19.90')], ['Speicher Dir das für später', 'Link in der Bio'])),
    'acht_teile_geschenk': dict(
        segmente=[seg('hase_rosa_c', 0, 2.6), seg('hund_creme_a', 0, 2.4, fx=0.45), seg('wal_blau_a', 0, 2.4, fx=0.55),
                  seg('gaensebluemchen_c', 4, 6.4, fx=0.45), seg('bauernhof_a', 0, 2.6, 1.5, 1.6, 0.5, 0.5)],
        texte=[['Geschenk zur Geburt?', '8 Teile, ein Set'], ['«I love Dogs»'], ['«Wal» Hellblau'], ['«It\'s a baby girl»'], ['«Bauernhof»']],
        liste=(['8 Teile,', 'je CHF 30.90'], [('«Hase» Rosa', 'mit Rassel'), ('«I love Dogs»', 'Creme'), ('«Wal»', 'Hellblau'),
               ('«It\'s a baby girl»', 'Apricot'), ('«Bauernhof»', 'Creme')], ['Markier das Gotti oder den Götti', 'Link in der Bio'])),
    'team_junge_oder_maedchen': dict(
        segmente=[seg('dino_cool_dude_a', 0, 2.2), seg('strampler_kirschen_b', 0, 2.2, fx=0.45), seg('weltall_hellblau_a', 5, 7.2),
                  seg('hase_rosa_c', 1, 3.2), seg('wal_blau_a', 0, 2.2, fx=0.55), seg('lila_hase_a', 0, 2.2, fx=0.55)],
        texte=[['Team Junge', 'oder Team Mädchen?'], ['Team Mädchen'], ['Team Junge'], ['Team Mädchen'], ['Team Junge'], ['Team Mädchen']],
        liste=(['Team Junge', 'oder Team Mädchen?'], [('Junge', '«Cool Dude», «Weltall», «Wal»'), ('Mädchen', '«Kirschen», «Hase», «Lila»')],
               ['Schreib es in die Kommentare', 'Link in der Bio'])),
    'suesseste_momente': dict(
        segmente=[seg('gaensebluemchen_c', 10, 12.6, 1.0, 1.08, 0.5, 0.4), seg('strampler_kirschen_b', 10, 12.6, 1.0, 1.06, 0.5, 0.42),
                  seg('hase_rosa_c', 0, 2.6), seg('lila_hase_a', 8, 10.6, 1.0, 1.08, 0.55, 0.42), seg('love_dad_mom_a', 9, 11.6, 1.0, 1.06, 0.55, 0.45)],
        texte=[['Die süssesten', '10 Sekunden heute'], None, ['Schick das jemandem,', 'der das heute braucht'], None, None],
        liste=(['Neu bei sunnozy'], [], ['Babykleider aus der Schweiz', 'Link in der Bio'])),
}


def set_karte(r, t):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    e = m.ease(t / 0.5)
    im = Image.open(r['bild']).convert('RGB'); s = 940 / max(im.size) * (0.96 + 0.04 * e)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c.paste(im, ((W - im.width) // 2, 860 - im.height // 2))
    d.text((W / 2, 340), 'neu bei sunnozy', font=m.f(m.SERIF_I, 56), fill=m.SALBEI, anchor='mm')
    d.text((W / 2, 1400), r['name'], font=m.f(m.SERIF, 92 if len(r['name']) < 20 else 76), fill=m.WALD, anchor='mm')
    d.text((W / 2, 1490), r['teile'], font=m.f(m.SERIF_I, 50), fill=m.GRAU, anchor='mm')
    return c


def end_karte(r):
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    d.text((W / 2, 740), r['name'], font=m.f(m.SERIF, 104 if len(r['name']) < 20 else 84), fill=m.WALD, anchor='mm')
    d.text((W / 2, 870), f'CHF {r["preis"]}', font=m.f(m.SERIF_I, 80), fill=m.SALBEI, anchor='mm')
    d.line((W / 2 - 70, 965, W / 2 + 70, 965), fill=(200, 192, 180), width=2)
    d.text((W / 2, 1040), 'Link in der Bio', font=m.f(m.SERIF, 52), fill=m.GRAU, anchor='mm')
    d.text((W / 2, 1105), 'Gratisversand ab CHF 50', font=m.f(m.SERIF_I, 44), fill=m.GRAU, anchor='mm')
    L = m.logo(260, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, 1290), L)
    return c


def liste_karte(titel, zeilen, fuss):
    """Schlusskarte für Sammel-Reels: Titel, Liste Name + Preis, Aufforderung, Logo."""
    c = Image.new('RGBA', (W, H), m.CREME + (255,)); d = ImageDraw.Draw(c)
    y = 640 - len(zeilen) * 38
    for z in (titel if isinstance(titel, list) else [titel]):
        d.text((W / 2, y), z, font=m.f(m.SERIF, 92), fill=m.WALD, anchor='mm'); y += 100
    y += 30
    for links, rechts in zeilen:
        d.text((120, y), links, font=m.f(m.SERIF, 62), fill=m.WALD, anchor='lm')
        d.text((W - 120, y), rechts, font=m.f(m.SERIF_I, 56), fill=m.SALBEI, anchor='rm'); y += 88
    y += 40
    d.line((W / 2 - 70, y, W / 2 + 70, y), fill=(200, 192, 180), width=2); y += 70
    for z in (fuss if isinstance(fuss, list) else [fuss]):
        d.text((W / 2, y), z, font=m.f(m.SERIF_I, 50), fill=m.GRAU, anchor='mm'); y += 64
    L = m.logo(240, (122, 108, 104)); c.paste(L, ((W - L.width) // 2, max(y + 60, 1330)), L)
    return c


def reel(key, nr):
    r = REELS[key]
    teile, t0 = [], 0.0
    for sg, tx in zip(r['segmente'], r['texte']):
        clip, von, bis, tempo, z0, z1, fx, fy = sg
        fr = m.clip_frames(os.path.join(VB, clip + '_bearbeitet.mp4'), von, bis + 0.2)
        dauer = (bis - von) / tempo
        teile.append(dict(start=t0, dauer=dauer, frames=fr, tempo=tempo, z=(z0, z1), f=(fx, fy), text=tx, karte=False)); t0 += dauer
    if 'liste' in r:
        end = liste_karte(*r['liste'])
        teile.append(dict(start=t0, dauer=3.4, fn=lambda t: end, karte=True)); t0 += 3.4
    else:
        teile.append(dict(start=t0, dauer=2.4, fn=lambda t: set_karte(r, t), karte=True)); t0 += 2.4
        end = end_karte(r)
        teile.append(dict(start=t0, dauer=2.2, fn=lambda t: end, karte=True)); t0 += 2.2
    n = int(round(t0 * FPS)); nb = int(m.BLENDE * FPS)

    def bild(tl, t):
        if tl['karte']:
            return tl['fn'](t)
        fr = tl['frames']; p = t * tl['tempo'] * FPS
        i = min(int(p), len(fr) - 1); j = min(i + 1, len(fr) - 1); a = p - int(p)
        im = fr[i] if a < 0.05 or i == j else Image.blend(fr[i], fr[j], a)
        e = m.ease(t / tl['dauer']); z0, z1 = tl['z']
        return ausschnitt(im, z0 + (z1 - z0) * e, *tl['f'])

    def text_von(idx):
        while idx >= 0 and teile[idx].get('text') is None:
            idx -= 1
        return teile[idx]['text'] if idx >= 0 else None

    def roh(s):
        idx = max(i for i, tl in enumerate(teile) if tl['start'] <= s + 1e-9)
        tl = teile[idx]; t = min(s - tl['start'], tl['dauer'] - 1e-3)
        c = bild(tl, t)
        if not tl['karte']:
            zeilen = text_von(idx)
            neu = tl['text'] is not None and idx > 0
            alpha = min(1, t / 0.12) if neu else 1.0
            if isinstance(zeilen, dict):          # grosse Zahl + Name (Vergleich zum Kommentieren)
                k.zahl(c, zeilen['zahl'], zeilen['name'], alpha)
            elif zeilen:
                m.text_unten(c, zeilen, alpha)
        if idx + 1 < len(teile) and teile[idx + 1]['karte'] and s > tl['start'] + tl['dauer'] - m.BLENDE:
            a = (s - (tl['start'] + tl['dauer'] - m.BLENDE)) / m.BLENDE
            c = Image.blend(c, bild(teile[idx + 1], 0), min(a, 1))
        return c

    erstes = roh(0)
    os.makedirs(m.OUT, exist_ok=True)
    datei = f'reel_{key}_9x16'
    pfad = os.path.join(m.OUT, datei + '.mp4'); tmp = pfad + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        c = roh(i / FPS)
        if i >= n - nb:
            c = Image.blend(c, erstes, (i - (n - nb)) / nb)
        fr = c.convert('RGB')
        if i == int(0.6 * FPS):
            fr.save(os.path.join(m.OUT, datei + '_titelbild.jpg'), quality=92)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    dauer = n / FPS
    musik = MUSIK[nr % 2]; ab = 8 + (nr * 11) % 60          # pro Reel anderer Ausschnitt
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-ss', str(ab), '-i', musik, '-t', f'{dauer:.2f}',
                    '-af', f'afade=t=in:d=0.4,afade=t=out:st={dauer - 1.2:.2f}:d=1.2,volume=0.85', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', pfad], check=True)
    os.remove(tmp)
    print(f'{pfad}: {dauer:.1f} s, Musik {os.path.basename(musik)} ab {ab} s', flush=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(REELS)
    for key in keys:
        reel(key, list(REELS).index(key))
