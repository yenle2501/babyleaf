"""Reel «Princess» (rosa Vichy-Strampler) aus den zwei Videos der Nutzerin (25.11.2026), auf Englisch.

Nur die Videos der Nutzerin, auf ihren Wunsch. Ausnahme von der Safe-Sleep-Regel (Baby schläft, Nuggi, Plüschtier und
Decke im Bett); der Text spielt nicht aufs Schlafen an. Stil wie CLAUDE.md: POV in weisser Schreibmaschinenschrift mit
Schleier, Text am Anfang und zum Loop am Ende, Standardmusik, Endfolie.

    python3 tools/make_reel_princess_gingham.py
Ausgabe: posts/coming-soon/reels/princess/reel_princess_gingham_9x16.mp4
"""
import os
import make_coming_soon_reels as m
import make_marketing4weeks as mw
from endfolie import SHOP

O = os.path.join(m.POSTS, 'coming-soon', 'reels', 'princess')
A, B = os.path.join(O, 'original', 'clip_a.mp4'), os.path.join(O, 'original', 'clip_b.mp4')
KLAR = os.path.join(m.POSTS, 'coming-soon', 'photos', 'shopify-hauptbilder-klar', 'bilder', 'erstausstattung-set-princess.jpg')

if __name__ == '__main__':
    mw.video(0, 'reel_princess_gingham', [
        ('clip', A, 0.3, 4.2),        # weit: Stubenwagen, Vichy-Strampler
        ('clip', B, 2.2, 5.0),        # näher: Herz und Rüschenkragen
        ('clip', B, 5.6, 8.2),        # Füsschen
        ('clip', A, 6.2, 9.4)],       # weit, Arme hoch
        [(0, 3.0, ['POV: her first little', 'pink outfit'], '🎀', 1420, mw.POV),
         (9.4, None, ['send this to the gotti'], '💗', 1420, mw.POV)],
        (KLAR, '«Princess»', 'newborn set · 8 pieces', SHOP), ordner=O)
