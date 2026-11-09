# Werbebilder im Katalog-Flatlay-Stil (03.11.2026)

Nach der Vorlage der Nutzerin (Mode-Anzeige: Kleidung flach auf Weinrot, Preisschild oben links, helle Leiste mit Marke senkrecht).
Flatlay-Fotos **mit KI erstellt** (Canva) nach den Set-Fotos aus dem Shop und der roten sunnozy-Box; Logo = echtes sunnozy-Logo.
Kein Versand-Versprechen im Bild. Neu erzeugen: `python3 tools/make_flatlay_ads.py`

| Datei | Format | Inhalt |
|---|---|---|
| `feed_<box>_1x1.jpg` | 1080 × 1080 | Katalog-Stil wie die Vorlage: Flatlay, Preisschild, Logo senkrecht, «Fertig verpackt mit Karte» |
| `inhalt_<box>_1x1.jpg` | 1080 × 1080 | «Was ist drin?»: Flatlay + Liste mit Häkchen + Preis |
| `zu_offen_<box>_1x1.jpg` | 1080 × 1080 | «Verpackt … und das ist drin»: geschlossene Box neben dem Flatlay |
| `story_<box>_9x16.jpg` | 1080 × 1920 | Story/Reel-Anzeige |
| `uebersicht_feed.jpg` | | alle 9 Feed-Bilder |
| `roh/<box>.jpg` | 1500 × 2000 | KI-Flatlay ohne Text |

Vor dem Schalten: Drucke und Farben mit der echten Ware vergleichen (KI legt die Kleider nach den Shop-Fotos aus).

# Stop-Motion-Reels (`../stopmotion/`)

Nach dem Pinterest-Pin «Bold gift box packaging»: Farbflächen, Box hüpft, Teile springen heraus, offene Box im Rundbogen, Schluss mit Preis.
9 Reels `stopmotion_<box>_9x16.mp4` (11.8 s) + Titelbild. Neu erzeugen: `python3 tools/make_stopmotion_reels.py`
