"""Alte Pfade unter posts/ in die neue Struktur (09.11.2026) übersetzen.

    from pfade import neu
    neu('kampagne-weihnachtsbox/rote-box/shopify/geschenkbox-dino.jpg')
    # -> 'coming-soon/photos/kampagne-weihnachtsbox/rote-box/shopify/geschenkbox-dino.jpg'
Pfade relativ zu posts/. Unbekannte Pfade kommen unverändert zurück.
"""
import json, os
_KARTE = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'posts', 'umzug_2026-11-09.json')))


def neu(alt):
    return _KARTE.get(alt.replace('\\', '/').lstrip('./'), alt)
