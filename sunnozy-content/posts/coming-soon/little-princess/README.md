# Neues Set «Little Princess» mit Krone: Videos

**Die Videos und Titelbilder liegen seit 22.10.2026 in `posts/reels/coming-soon/`** (alle Reels flach in einem Ordner). Hier bleiben `original/` mit den Baby-Clips und dieses README.

Aus Deinen KI-Videos (Grok, je 10 s, Baby mit Body, Söckchen und Kronen-Schmusetuch aus dem Set) sind je ein Reel 9:16 und ein Feed-Video 4:5 entstanden. Die Varianten unterscheiden sich nur im Baby-Clip, so kannst Du in Meta testen, welche am besten läuft.

| Variante | Baby-Clip (`original/`) | Reel 9:16 | Feed 4:5 |
|---|---|---|---|
| A | `baby_clip_a.mp4`: reibt sich die Augen, schläft ruhig | `reel_little_princess_a_9x16.mp4` | `reel_little_princess_a_4x5.mp4` |
| B | `baby_clip_b.mp4`: streckt sich, gähnt am Schluss | `reel_little_princess_b_9x16.mp4` | `reel_little_princess_b_4x5.mp4` |
| C | `baby_clip_c.mp4`: legt die Hände auf den Bauch | `reel_little_princess_c_9x16.mp4` | `reel_little_princess_c_4x5.mp4` |
| Kombi | `baby_clip_d.mp4` (3–8 s, Bauchlage im Strampler) + Überblendung + `baby_clip_c.mp4` (0,5–6 s, Body und Kronen-Schmusetuch) | `reel_little_princess_kombi_9x16.mp4` | `reel_little_princess_kombi_4x5.mp4` |

A–C sind 14,8 s lang, das Kombi-Video 18,8 s. Alle sind stumm, den Sound wählst Du in Instagram. `*_standbild.jpg` sind die Titelbilder, `uebersicht.jpg` zeigt alle auf einen Blick.

## Ablauf

1. **0–6 s Baby-Clip.** Ein Etikett blendet ein: «COMING SOON / Set «Little Princess»», dann «Für die ersten Wochen». Das Etikett liegt nie über dem Gesicht, im 9:16 über den Beinen, im 4:5 oben rechts. Im 9:16 fährt der Ausschnitt bei A–C langsam vom Baby zum Kronen-Schmusetuch, im Kombi-Video zoomt er im ersten Clip langsam näher und schwenkt im zweiten. Im Kombi-Video steht «Coming soon» auf dem ersten Clip (im 4:5 auf der Körpermitte, weil oben der Kopf ist) und «Für die ersten Wochen» auf dem zweiten.
2. **«Was steckt drin?»** mit dem ganzen Set.
3. **Die 8 Teile** erscheinen nacheinander: Kapuzentuch, Strampler, Body, Mütze, Schmusetuch, Lätzchen, Söckchen, Fäustlinge.
4. **«Alles drin.»** mit «8 Teile, fertig aufeinander abgestimmt», Stempel «COMING SOON», «Bald auf sunnozy.ch · Gratisversand ab CHF 50» und Logo.

## Vor dem Posten prüfen

- **Coming soon:** Das Set ist noch nicht in Shopify, darum steht «Coming soon» statt eines Preises im Video. Sobald es im Shop ist, mit Preis neu erzeugen (dann steht «Neu bei sunnozy» und der Preis statt «Coming soon»):
  `python3 tools/make_set_video.py posts/coming-soon/little-princess/original/baby_clip_a.mp4 posts/reels/coming-soon/reel_little_princess_a --set=little_princess --preis=30.40` (für b und c gleich). Kombi-Video:
  `python3 tools/make_set_video.py "posts/coming-soon/little-princess/original/baby_clip_d.mp4:3:5:mitte:mitte,posts/coming-soon/little-princess/original/baby_clip_c.mp4:0.5:5.5:schwenk:oben_rechts" posts/reels/coming-soon/reel_little_princess_kombi --set=little_princess --preis=30.40`
- **Name:** Im Shop gibt es schon «Princess» (rosa, Teddy). «Little Princess» steht so auf dem Lätzchen. Wenn das neue Set im Shop anders heisst, `titel` in `SETS` in `tools/make_set_video.py` anpassen.
- **KI-Video:** Das Baby ist KI-generiert. Der Body im Video hat die Schleife, aber nicht die Schrift «Make a Wish» wie der echte Body. Instagram und Facebook verlangen bei realistisch wirkenden KI-Videos die Kennzeichnung: beim Posten «KI-Info» bzw. «Mit KI erstellt» einschalten. Im Video selbst steht kein Hinweis.
- Die Holzkarte «1 Monat» stammt aus dem Clip und gehört nicht zum Set.

## Bildunterschrift (Vorschlag)

> Coming soon: das Set «Little Princess». Kapuzentuch, Strampler, Body, Mütze, Schmusetuch mit Krone, Lätzchen, Söckchen und Fäustlinge, fertig aufeinander abgestimmt. Bald auf sunnozy.ch, Gratisversand in der Schweiz ab CHF 50.
> sunnozy.ch
> #sunnozy #erstausstattung #babyschweiz #geburtsgeschenk #neugeboren #babyset

Erstellt mit `tools/make_set_video.py`.
