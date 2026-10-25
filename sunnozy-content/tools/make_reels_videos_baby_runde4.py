"""Runde 4 (25.10.2026): Reels aus 14 neuen Grok-Clips, gleiche Machart wie make_reels_videos_baby.py.

    python3 tools/make_reels_videos_baby_runde4.py              # alle
    python3 tools/make_reels_videos_baby_runde4.py born_2027_blau

Coming-soon-Sets: nur «Coming soon», kein Preis -> posts/reels/coming-soon/
Sets im Shop (Princess, Teddybär, Little and Loved): Schlusskarte mit Preis -> posts/reels/im-shop/
Nicht verwendet: little_and_loved_b (schlafendes Baby mit Haarband und Plüschhase daneben, Safe Sleep).
"""
import os, sys
import make_coming_soon_reels as m
import make_reels_videos_baby as rv

seg, CS, PR = rv.seg, rv.CS, rv.PR

REELS = {
    # Coming soon
    'born_2027_blau': dict(name='«Born in 2027»', teile='6 Teile in Hellblau', bild=CS('born-in-2027-blau'),
        segmente=[seg('born_in_2027_blau_a', 0, 4, fy=0.35), seg('born_in_2027_blau_a', 5, 7.5, 1.22, 1.25, 0.5, 0.36), seg('born_in_2027_blau_a', 9, 13, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['POV: Er kommt 2027', 'und hat schon sein Outfit'], ['«Born in 2027»', 'in Hellblau'], ['Body, Hose, Mütze', 'und mehr, 6 Teile']]),
    'born_2027_junge_maedchen': dict(
        segmente=[seg('born_in_2027_rosa_b', 0, 3, fy=0.4), seg('born_in_2027_rosa_b', 5, 7.5, 1.2, 1.25, 0.5, 0.36), seg('born_in_2027_blau_a', 0.5, 3.5, fy=0.35),
                  seg('born_in_2027_blau_a', 6, 8.5, 1.2, 1.25, 0.5, 0.36), seg('born_in_2027_rosa_b', 10, 13, 1.0, 1.05, fy=0.4, tempo=0.85)],
        texte=[['2027 wird', 'Euer Jahr?'], {'zahl': '1', 'name': 'Rosa'}, {'zahl': '2', 'name': 'Hellblau'}, ['«Born in 2027»', 'Body, Hose, Mütze'], ['Rosa oder Hellblau?', 'Schreib es in die Kommentare']],
        liste=(['«Born in 2027»', 'Rosa oder Hellblau?'], [('1 Rosa', '6 Teile'), ('2 Hellblau', '6 Teile')], ['Markier jemanden, der 2027 Mama wird', 'Coming soon auf sunnozy.ch'])),
    'bauernhof_happy_baby': dict(name='«Bauernhof»', teile='8 Teile mit Tieren', bild=PR('bauernhof'),
        segmente=[seg('bauernhof_b', 0, 4, fy=0.4), seg('bauernhof_b', 5, 7.5, 1.22, 1.25, 0.5, 0.42), seg('bauernhof_b', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Dieses Lachen', 'am Morgen'], ['Body «Happy Baby»', 'mit Bauernhof-Tieren'], ['8 Teile für', 'die ersten Wochen']]),
    'gaensebluemchen_baby_girl': dict(name='«It\'s a baby girl»', teile='8 Teile mit Gänseblümchen', bild=PR('gaensebluemchen'),
        segmente=[seg('gaensebluemchen_d', 0, 4, fy=0.4), seg('gaensebluemchen_d', 5, 7.5, 1.22, 1.25, 0.5, 0.42), seg('gaensebluemchen_d', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['POV: Ihr verratet es', 'endlich allen'], ['«It\'s a baby girl»', 'mit Gänseblümchen'], ['8 Teile für', 'die ersten Wochen']]),
    'wickelbody_schlaf': dict(name='«Little Princess»', teile='Wickelbody, Hose, Mütze', bild=CS('little-princess-wickelbody'),
        segmente=[seg('little_princess_wickelbody_b', 0, 4.5, 1.0, 1.06, 0.55, 0.4, tempo=0.85), seg('little_princess_wickelbody_b', 6, 9, 1.2, 1.25, 0.5, 0.4), seg('little_princess_wickelbody_b', 10, 14, 1.05, 1.0, 0.55, 0.42, tempo=0.85)],
        texte=[['Der Moment,', 'wenn sie endlich schläft'], ['Wickelbody', '«Little Princess»'], ['Wickelbody, Hose', 'und Mütze']]),
    'eisbaer_hand': dict(name='«Eisbär»', teile='Strampler, Body, Mütze, Fäustlinge, Lätzchen', bild=CS('eisbaer-taupe'),
        segmente=[seg('eisbaer_taupe_b', 0, 4, fy=0.38), seg('eisbaer_taupe_b', 5, 7.5, 1.2, 1.25, 0.55, 0.4), seg('eisbaer_taupe_b', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Nur eine Hand', 'auf dem Bauch'], ['Strampler mit', 'kleinen Tannen'], ['Für Dein', 'Winterbaby']]),
    'beautiful_sofa': dict(name='«Beautiful»', teile='Wickelbody, Hose, Mütze', bild=CS('gaensebluemchen-beautiful'),
        segmente=[seg('gaensebluemchen_beautiful_c', 0, 4, fy=0.4), seg('gaensebluemchen_beautiful_c', 5, 7.5, 1.2, 1.25, 0.45, 0.45), seg('gaensebluemchen_beautiful_c', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Sonntag auf dem Sofa', 'mit ihr'], ['Apricot', 'mit Gänseblümchen'], ['«Beautiful»,', '3 Teile']]),
    'best_family_lachen': dict(name='«Best Family» Teddy', teile='8 Teile mit Teddy-Rassel', bild=PR('best_family'),
        segmente=[seg('best_family_c', 0, 4, fy=0.38), seg('best_family_c', 5, 7.5, 1.2, 1.25, 0.5, 0.42), seg('best_family_c', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Wenn Papa', 'Grimassen schneidet'], ['Teddy-Body', '«Best Family»'], ['Mütze mit', 'Bärenohren']]),
    'krone_nach_dem_bad': dict(name='«Little Princess» Krone', teile='8 Teile mit Kapuzentuch', bild=PR('prinzessin_krone'),
        segmente=[seg('little_princess_krone_f', 0, 4, fy=0.4), seg('little_princess_krone_f', 6, 8.5, 1.1, 1.18, 0.55, 0.35), seg('little_princess_krone_f', 10, 14, 1.0, 1.05, fy=0.4, tempo=0.85)],
        texte=[['Nach dem', 'ersten Bad'], ['Kapuzentuch', 'mit Krone'], ['Warm eingepackt,', 'kleine Prinzessin']]),
    # im Shop
    'princess_lachen': dict(shop=True,
        segmente=[seg('princess_rosa_a', 0, 4, fy=0.38), seg('princess_rosa_a', 5, 7.5, 1.2, 1.25, 0.5, 0.42), seg('princess_rosa_a', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Sie lacht,', 'Du schmilzt'], ['Body mit Teddy,', 'Mütze mit Öhrchen'], ['Erstausstattung', '«Princess»']],
        liste=(['Erstausstattung', '«Princess»'], [('8 Teile in Rosa', 'CHF 30.40')], ['Jetzt auf sunnozy.ch', 'Link in der Bio'])),
    'teddybaer_lachen': dict(shop=True,
        segmente=[seg('teddy_creme_a', 0, 4, fy=0.38), seg('teddy_creme_b', 2, 5, 1.0, 1.06, fy=0.4), seg('teddy_creme_a', 6, 8.5, 1.2, 1.25, 0.5, 0.42), seg('teddy_creme_b', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Wenn Du sein', 'Lieblingslied singst'], None, ['Body mit Bärchen,', 'gestreifte Mütze'], ['Erstausstattung', '«Teddybär»']],
        liste=(['Erstausstattung', '«Teddybär»'], [('8 Teile in Creme', 'CHF 30.40')], ['Jetzt auf sunnozy.ch', 'Link in der Bio'])),
    'little_and_loved_sofa': dict(shop=True,
        segmente=[seg('little_and_loved_a', 0, 4, fy=0.38), seg('little_and_loved_a', 5, 7.5, 1.2, 1.25, 0.45, 0.48), seg('little_and_loved_a', 9.5, 13.5, 1.05, 1.0, fy=0.4, tempo=0.85)],
        texte=[['Erstes Jäckchen,', 'erstes Lächeln'], ['Jacke mit', 'gestickter Ente'], ['Erstausstattung', '«Little and Loved»']],
        liste=(['Erstausstattung', '«Little and Loved»'], [('8 Teile, rosa Enten', 'CHF 30.40')], ['Jetzt auf sunnozy.ch', 'Link in der Bio'])),
    'lachen_sammlung': dict(
        segmente=[seg('princess_rosa_a', 0, 2.2, fy=0.4), seg('princess_rosa_a', 2.5, 4.7, fy=0.4), seg('best_family_c', 0.5, 2.7, fy=0.4),
                  seg('teddy_creme_a', 0, 2.2, fy=0.4), seg('bauernhof_b', 0.5, 2.7, fy=0.4), seg('gaensebluemchen_d', 0, 2.2, fy=0.4),
                  seg('born_in_2027_blau_a', 6, 8.2, fy=0.35)],
        texte=[['Welches Lachen', 'gewinnt?'], {'zahl': '1', 'name': '«Princess»'}, {'zahl': '2', 'name': '«Best Family»'}, {'zahl': '3', 'name': '«Teddybär»'},
               {'zahl': '4', 'name': '«Bauernhof»'}, {'zahl': '5', 'name': '«It\'s a baby girl»'}, {'zahl': '6', 'name': '«Born in 2027»'}],
        liste=('Welches Lachen gewinnt?', [('1 Princess', 'im Shop'), ('2 Best Family', 'coming soon'), ('3 Teddybär', 'im Shop'),
               ('4 Bauernhof', 'coming soon'), ('5 It\'s a baby girl', 'coming soon'), ('6 Born in 2027', 'coming soon')],
               ['Schreib die Zahl in die Kommentare', 'sunnozy.ch'])),
}

if __name__ == '__main__':
    rv.REELS = REELS
    for key in (sys.argv[1:] or REELS):
        m.OUT = os.path.join(m.POSTS, 'reels', 'im-shop' if REELS[key].get('shop') else 'coming-soon')
        rv.reel(key, list(REELS).index(key) + 7)
