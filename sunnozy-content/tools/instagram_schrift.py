"""Hausschrift fuer ALLE Instagram-Posts (Feed, Karussell, Storys, Reels): Sacramento. Nicht fuer Anzeigen.

Wunsch der Nutzerin (19.10.2026): Schrift wie im Beispiel «winter is here» (duenne, verspielte Schreibschrift).
Einbinden: als erste Zeile nach den Imports eines Instagram-Generators `import instagram_schrift  # noqa`.
Danach laedt jedes `ImageFont.truetype(...)` in diesem Skript Sacramento statt der dort genannten Schrift. Die Groesse
wird um 25 % erhoeht, weil Sacramento bei gleicher Punktgroesse kleiner laeuft. Das Logo (Bild) bleibt unveraendert.
Anzeigen-Generatoren (make_ads*, make_meta_ads*, make_paket7, make_paket9, make_weihnachtsbox) binden das NICHT ein.
Abschalten fuer ein einzelnes Skript: Umgebungsvariable SUNNOZY_SCHRIFT_AUS=1.
"""
import os, re
from PIL import ImageFont, ImageDraw

SACRAMENTO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'sacramento.ttf')
FAKTOR = 1.25


def form(text):
    """Schreibschrift in Grossbuchstaben ist kaum lesbar: GROSS geschriebene Texte werden klein geschrieben
    (wie im Vorbild «winter is here»), gesperrte Buchstaben («S N E A K   P E E K») werden zusammengezogen."""
    if not isinstance(text, str) or not text.strip():
        return text
    zeilen = []
    for z in text.split('\n'):
        if re.fullmatch(r'\s*(\S ){2,}\S\s*', z) or re.fullmatch(r'\s*(\S ){2,}\S(\s{2,}(\S ){1,}\S)+\s*', z):
            z = '  '.join(w.replace(' ', '') for w in re.split(r'\s{2,}', z.strip()))
        buchstaben = [c for c in z if c.isalpha()]
        if len(buchstaben) > 1 and all(c.isupper() for c in buchstaben):
            z = re.sub(r'\bchf\b', 'CHF', z.lower())  # Waehrung bleibt gross
        zeilen.append(z)
    return '\n'.join(zeilen)


if not os.environ.get('SUNNOZY_SCHRIFT_AUS') and not getattr(ImageFont, '_sunnozy_sacramento', False):
    _original = ImageFont.truetype

    def _truetype(font=None, size=10, *args, **kwargs):
        return _original(SACRAMENTO, max(1, int(round(size * FAKTOR))), *args, **kwargs)

    ImageFont.truetype = _truetype
    ImageFont._sunnozy_sacramento = True

    # Text vor dem Zeichnen und Messen gleich umformen, damit Breiten und Positionen stimmen
    for _name in ('text', 'multiline_text', 'textlength', 'textbbox', 'multiline_textbbox'):
        _alt = getattr(ImageDraw.ImageDraw, _name, None)
        if _alt is None:
            continue

        def _neu(self, xy_oder_text, *args, _alt=_alt, _name=_name, **kwargs):
            if _name == 'textlength':
                return _alt(self, form(xy_oder_text), *args, **kwargs)
            if args:
                args = (form(args[0]),) + args[1:]
            elif 'text' in kwargs:
                kwargs['text'] = form(kwargs['text'])
            return _alt(self, xy_oder_text, *args, **kwargs)

        setattr(ImageDraw.ImageDraw, _name, _neu)
