"""Reels aus den Grok-Clips «Weihnachts-Geschenkbox I love my Mummy» (Auspacken), gleiche Machart wie
make_reels_videos_baby.py: Hook ab Sekunde 0, Schnitte, Zoom, Text in Cormorant, Musik, Loop, Schlusskarte.
Die Box ist im Shop, deshalb steht der Preis auf der Schlusskarte.

    python3 tools/make_reels_weihnachtsbox_video.py            # alle
    python3 tools/make_reels_weihnachtsbox_video.py auspacken  # nur eines

Clips: posts/videos-baby/weihnachtsbox_mummy_{a,b,c}_bearbeitet.mp4 (unten 200 px mit eingebranntem Text
weggeschnitten, nachbearbeitet). Ausgabe: posts/kampagne-weihnachtsbox/reels/reel_mummy_<name>_9x16.mp4 + _titelbild.jpg
"""
import os, sys
import make_coming_soon_reels as m
import make_reels_videos_baby as rv

seg = rv.seg
A, B, C = 'weihnachtsbox_mummy_a', 'weihnachtsbox_mummy_b', 'weihnachtsbox_mummy_c'
PREIS = [('3 Bodys + 3 Halstücher', 'CHF 29.90'), ('Box, Seidenpapier, Karte', 'inklusive')]

REELS = {
    'mummy_auspacken': dict(
        segmente=[seg(A, 0, 2.6, 1.0, 1.08, 0.42, 0.45), seg(A, 1.2, 3.4, 1.2, 1.25, 0.4, 0.42, tempo=0.8), seg(B, 2.6, 5.6, 1.1, 1.18, 0.62, 0.38),
                  seg(A, 6.0, 8.4, 1.0, 1.06, 0.45, 0.45), seg(A, 10.2, 12.8, 1.05, 1.12, 0.52, 0.5)],
        texte=[['POV: Du packst', 'Mamas Geschenk aus'], ['«I love my Mummy»', 'mit Bärchen-Stickerei'], ['Die Karte für', 'Deinen Gruss ist dabei'],
               ['Halstücher', 'mit Bärchen'], ['und gestreift,', 'für jeden Tag']],
        liste=(['Weihnachts-Geschenkbox', '«I love my Mummy»'], PREIS, ['Markier jemanden, der das braucht', 'Link in der Bio'])),
    'mummy_was_ist_drin': dict(
        segmente=[seg(C, 0, 2.4, 1.0, 1.06, 0.45, 0.45), seg(A, 1.0, 3.6, 1.15, 1.22, 0.4, 0.42), seg(C, 4.0, 6.6, 1.0, 1.08, 0.5, 0.4),
                  seg(B, 3.0, 5.6, 1.15, 1.2, 0.64, 0.36), seg(C, 11.0, 14.0, 1.0, 1.06, 0.55, 0.45, tempo=0.85)],
        texte=[['Was ist in der Box', 'für CHF 29.90?'], {'zahl': '3', 'name': 'Bodys'}, {'zahl': '3', 'name': 'Halstücher'},
               {'zahl': '+', 'name': 'Karte zum Beschriften'}, ['alles fertig verpackt', 'in der rosa Box']],
        liste=('«I love my Mummy»', PREIS, ['Versand in 2–3 Werktagen', 'Link in der Bio'])),
    'mummy_erstes_weihnachten': dict(
        segmente=[seg(C, 10.0, 12.6, 1.0, 1.08, 0.48, 0.4, tempo=0.85), seg(B, 10.4, 12.8, 1.0, 1.06, 0.48, 0.45), seg(B, 6.4, 9.2, 1.05, 1.12, 0.42, 0.45),
                  seg(C, 12.4, 14.9, 1.08, 1.0, 0.6, 0.38, tempo=0.85)],
        texte=[['Ihr erstes Weihnachten', 'mit Baby'], ['Schenk ihr etwas,', 'das sie jeden Tag braucht'], ['Bodys und Halstücher', 'mit «I love my Mummy»'],
               ['Mit Karte für', 'Deine Worte']],
        liste=(['Geschenk für', 'die frischgebackene Mama'], PREIS, ['Schick das dem Papa', 'Link in der Bio'])),
    'mummy_unter_30': dict(
        segmente=[seg(A, 0, 2.2, 1.0, 1.06, 0.45, 0.45), seg(C, 1.2, 3.6, 1.05, 1.12, 0.42, 0.42), seg(C, 4.2, 7.0, 1.0, 1.06, 0.5, 0.42),
                  seg(B, 0.6, 3.0, 1.0, 1.06, 0.5, 0.45), seg(A, 12.6, 14.9, 1.0, 1.05, 0.55, 0.45, tempo=0.85)],
        texte=[['Babyparty am Wochenende', 'und noch kein Geschenk?'], ['Das hier kostet', 'unter 30 Franken'], ['3 Bodys, 3 Halstücher', 'in Creme und Braun'],
               ['Box auf, Karte rein,', 'fertig'], ['Gratisversand', 'ab CHF 50']],
        liste=(['Weihnachts-Geschenkbox', '«I love my Mummy»'], PREIS, ['Speicher Dir das für später', 'Link in der Bio'])),
}

if __name__ == '__main__':
    m.OUT = os.path.join(m.POSTS, 'kampagne-weihnachtsbox', 'reels')
    rv.REELS = REELS
    for key in (sys.argv[1:] or REELS):
        rv.reel(key, list(REELS).index(key) + 3)
