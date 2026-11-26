"""Meme-Reel «you loved it?!» für kleine Shops (Vorbild der Nutzerin 26.11.2026, Bildschirmaufnahme), auf Englisch.

Aufbau wie im Vorbild: 1) Hände packen eine Bestellung, «the only question in my mind after a customer receives their
order» → 2) Reaktion «did you love it??» / gross «YOU LOVED IT?!» → 3) Danke-Folie. Das Kind aus dem Vorbild ist fremdes
Material und wird nicht verwendet; stattdessen lachendes Baby im Set «Princess» (wach). Standardmusik, Endfolie.

    python3 tools/make_reel_you_loved_it.py
Ausgabe: posts/contentgpt/reels/reel31_you_loved_it_9x16.mp4
"""
import os
import make_coming_soon_reels as m
import make_marketing4weeks as mw

P = m.POSTS
V = lambda c: os.path.join(P, 'baby-videos', c)
KLAR = os.path.join(P, 'coming-soon', 'photos', 'shopify-hauptbilder-klar', 'bilder', 'erstausstattung-set-princess.jpg')

if __name__ == '__main__':
    mw.video(0, 'reel31_you_loved_it', [
        ('breit', V('weihnachtsbox_mummy_b_bearbeitet.mp4'), 0.5, 4.3),     # Hände packen die Box
        ('clip', V('princess_rosa_a_bearbeitet.mp4'), 0.6, 3.0),            # Baby lacht
        ('clip', V('princess_rosa_a_bearbeitet.mp4'), 6.6, 9.4)],
        [(0, 3.9, ['the only question in my', 'mind after a customer', 'receives their order'], None, 300, 'band'),
         (3.9, 4.9, ['did you love it??'], None, 1380, 'band'),
         (4.9, None, ['YOU', 'LOVED', 'IT?!'], None, 1200, 'band_gross')],
        (KLAR, 'thanks for watching', 'and a big thank you if you', 'like · comment · share · follow'),
        ordner=os.path.join(P, 'contentgpt', 'reels'), blende=0.2)
