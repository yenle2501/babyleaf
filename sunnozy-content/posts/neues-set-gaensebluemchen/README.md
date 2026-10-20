# Neues Set «Gänseblümchen»: Videos (Coming soon)

Aus Deinen 3 KI-Videos (Grok, je 10 s, schlafendes Baby im Nestchen mit Strampler und Kapuzentuch aus dem Set) sind je ein Reel 9:16 und ein Feed-Video 4:5 entstanden. Aufbau und Look sind gleich wie bei «Little Princess» (`../neues-set-little-princess/`).

| Variante | Baby-Clip (`original/`) | Reel 9:16 | Feed 4:5 |
|---|---|---|---|
| A | `baby_clip_a.mp4` | `reel_gaensebluemchen_a_9x16.mp4` | `reel_gaensebluemchen_a_4x5.mp4` |
| B | `baby_clip_b.mp4` | `reel_gaensebluemchen_b_9x16.mp4` | `reel_gaensebluemchen_b_4x5.mp4` |
| C | `baby_clip_c.mp4` | `reel_gaensebluemchen_c_9x16.mp4` | `reel_gaensebluemchen_c_4x5.mp4` |

Die 3 Clips unterscheiden sich nur wenig (kleine Hand- und Mundbewegungen, bei C gähnt das Baby). Alle Videos sind 14,8 s lang und stumm. `*_standbild.jpg` sind die Titelbilder, `uebersicht.jpg` zeigt alle auf einen Blick.

## Ablauf

1. **0–6 s Baby-Clip** mit Etikett «COMING SOON / Set «Gänseblümchen»», dann «Für die ersten Wochen». Das Etikett liegt unten auf der Decke, nie über dem Gesicht. Im 9:16 zoomt das Bild langsam etwas näher.
2. **«Was steckt drin?»** mit dem ganzen Set.
3. **Die 8 Teile** nacheinander: Kapuzentuch, Strampler, Body, Mütze, Rassel, Lätzchen, Söckchen, Fäustlinge.
4. **«Alles drin.»** mit «8 Teile, fertig aufeinander abgestimmt», Stempel «COMING SOON», «Bald auf sunnozy.ch · Gratisversand ab CHF 50» und Logo.

## Vor dem Posten prüfen

- **Coming soon:** Das Set ist noch nicht in Shopify (geprüft am 20.10.2026). Sobald es im Shop ist, mit Preis neu erzeugen:
  `python3 tools/make_set_video.py posts/neues-set-gaensebluemchen/original/baby_clip_a.mp4 posts/neues-set-gaensebluemchen/reel_gaensebluemchen_a --set=gaensebluemchen --preis=30.40` (für b und c gleich)
- **Name:** «Gänseblümchen» ist der Arbeitsname. Auf dem Body steht «It's a baby girl». Wenn das Set im Shop anders heisst, `titel` in `SETS` in `tools/make_set_video.py` anpassen.
- **KI-Video:** Das Baby ist KI-generiert. Beim Posten auf Instagram und Facebook «KI-Info» bzw. «Mit KI erstellt» einschalten. Im Clip trägt das Baby den Strampler mit Gänseblümchen und liegt unter dem Kapuzentuch, das passt zum Set.

## Bildunterschrift (Vorschlag)

> Coming soon: das Set «Gänseblümchen». Kapuzentuch, Strampler, Body «It's a baby girl», Mütze, Rassel, Lätzchen, Söckchen und Fäustlinge, fertig aufeinander abgestimmt. Bald auf sunnozy.ch, Gratisversand in der Schweiz ab CHF 50.
> sunnozy.ch
> #sunnozy #erstausstattung #babyschweiz #geburtsgeschenk #neugeboren #babyset

Erstellt mit `tools/make_set_video.py --set=gaensebluemchen`.
