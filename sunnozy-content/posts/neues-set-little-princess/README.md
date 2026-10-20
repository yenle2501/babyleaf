# Neues Set «Little Princess» mit Krone: Videos

Aus Deinen 3 KI-Videos (Grok, je 10 s, Baby mit Body, Söckchen und Kronen-Schmusetuch aus dem Set) sind je ein Reel 9:16 und ein Feed-Video 4:5 entstanden. Die 3 Varianten unterscheiden sich nur im Baby-Clip, so kannst Du in Meta testen, welche am besten läuft.

| Variante | Baby-Clip (`original/`) | Reel 9:16 | Feed 4:5 |
|---|---|---|---|
| A | `baby_clip_a.mp4`: reibt sich die Augen, schläft ruhig | `reel_little_princess_a_9x16.mp4` | `reel_little_princess_a_4x5.mp4` |
| B | `baby_clip_b.mp4`: streckt sich, gähnt am Schluss | `reel_little_princess_b_9x16.mp4` | `reel_little_princess_b_4x5.mp4` |
| C | `baby_clip_c.mp4`: legt die Hände auf den Bauch | `reel_little_princess_c_9x16.mp4` | `reel_little_princess_c_4x5.mp4` |

Alle Videos sind 14,8 s lang und stumm, den Sound wählst Du in Instagram. `*_standbild.jpg` sind die Titelbilder, `uebersicht.jpg` zeigt alle auf einen Blick.

## Ablauf

1. **0–6 s Baby-Clip.** Ein Etikett blendet ein: «NEU BEI SUNNOZY / Set «Little Princess»», dann «Für die ersten Wochen». Das Etikett liegt nie über dem Gesicht, im 9:16 über den Beinen, im 4:5 oben rechts. Im 9:16 fährt der Ausschnitt langsam vom Baby zum Kronen-Schmusetuch.
2. **«Was steckt drin?»** mit dem ganzen Set.
3. **Die 8 Teile** erscheinen nacheinander: Kapuzentuch, Strampler, Body, Mütze, Schmusetuch, Lätzchen, Söckchen, Fäustlinge.
4. **«Alles drin.»** mit «8 Teile, fertig aufeinander abgestimmt», «Gratisversand ab CHF 50 · sunnozy.ch» und Logo.

## Vor dem Posten prüfen

- **Preis:** Das Set ist noch nicht in Shopify, darum steht kein Preis im Video. Sobald es im Shop ist, mit Preis neu erzeugen:
  `python3 tools/make_set_video.py posts/neues-set-little-princess/original/baby_clip_a.mp4 posts/neues-set-little-princess/reel_little_princess_a --preis=30.40` (für b und c gleich)
- **Name:** Im Shop gibt es schon «Princess» (rosa, Teddy). «Little Princess» steht so auf dem Lätzchen. Wenn das neue Set im Shop anders heisst, `SET_TITEL` in `tools/make_set_video.py` anpassen.
- **KI-Video:** Das Baby ist KI-generiert. Der Body im Video hat die Schleife, aber nicht die Schrift «Make a Wish» wie der echte Body. Instagram und Facebook verlangen bei realistisch wirkenden KI-Videos die Kennzeichnung: beim Posten «KI-Info» bzw. «Mit KI erstellt» einschalten. Im Video selbst steht kein Hinweis.
- Die Holzkarte «1 Monat» stammt aus dem Clip und gehört nicht zum Set.

## Bildunterschrift (Vorschlag)

> Neu bei sunnozy: das Set «Little Princess». Kapuzentuch, Strampler, Body, Mütze, Schmusetuch mit Krone, Lätzchen, Söckchen und Fäustlinge, fertig aufeinander abgestimmt. Gratisversand in der Schweiz ab CHF 50.
> sunnozy.ch
> #sunnozy #erstausstattung #babyschweiz #geburtsgeschenk #neugeboren #babyset

Erstellt mit `tools/make_set_video.py`.
