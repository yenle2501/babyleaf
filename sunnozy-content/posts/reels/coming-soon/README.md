# Reels: Coming soon

Alle Reel-Videos der Coming-soon-Sets liegen hier flach in einem Ordner, ohne Unterordner, jeweils mit Titelbild. Die Baby-Clips (Quellen) liegen in `posts/coming-soon/<set>/original/`.

## POV-Reels (22.10.2026)

Erstellt aus den Grok-Videos mit `python3 tools/make_coming_soon_reels.py`. Schrift: **Cormorant Garamond** (Serif, keine Schreibschrift).

| Datei | Set | Hook (ab Sekunde 0) | Auflösung (ab ~45 %) | Dauer |
|---|---|---|---|---|
| `reel_little_princess_pov_9x16.mp4` | «Little Princess» Krone, 8 Teile | POV: Deine beste Freundin bekommt ein Mädchen | und das Geschenk ist schon da | 10,4 s |
| `reel_best_family_teddy_a_9x16.mp4` | «Best Family» Teddy, 8 Teile | POV: Er entdeckt seinen ersten Teddy | Die Teddy-Rassel ist im Set dabei | 11,9 s |
| `reel_best_family_teddy_b_9x16.mp4` | «Best Family» Teddy, 8 Teile | Wenn der Teddy sofort der beste Freund ist | Body, Strampler, Mütze und der Teddy dazu | 12,4 s |
| `reel_blumenwiese_a_9x16.mp4` | «Blumenwiese» Musselin, 3 Teile | POV: Wickeln um 3 Uhr nachts | und nichts muss über den Kopf | 11,9 s |
| `reel_blumenwiese_b_9x16.mp4` | «Blumenwiese» Musselin, 3 Teile | Schick das der Freundin, die ein Mädchen erwartet | Weicher Musselin, Blümchen von Kopf bis Fuss | 11,9 s |

### Warum so (für Reichweite)

- **Hook im ersten Bild:** Baby und Text stehen sofort da, ohne Logo-Intro. In den ersten 3 Sekunden springen die meisten ab.
- **Eine Szene, die man erleben will, oder eine, die man weiterschickt:** Freundin, Gotti, Partner. Weitergeleitet per DM ist das stärkste Signal für Leute, die uns noch nicht folgen (siehe `posts/instagram/pov-hooks.md`).
- **Zwei Texte pro Reel:** Der erste macht neugierig, der zweite löst nach etwa 3–4 s auf. Wer liest, bleibt.
- **Text im unteren Drittel:** nie über dem Gesicht, links von den Instagram-Knöpfen, über der Caption-Zone.
- **Produkt im Fokus:** Nach dem Clip kommt das ganze Set gross auf Creme, mit Name und Teilen.
- **10–12 s, sauberer Loop:** Die Schlusskarte blendet zurück ins erste Bild. Wer zweimal schaut, zählt doppelt.
- **A/B-Test:** Best Family und Blumenwiese gibt es je zweimal mit verschiedenem Hook. Mit 2–3 Tagen Abstand posten und nach 48 h Views, 3-Sekunden-Rate und Teilen vergleichen. Den Gewinner als Anzeige bewerben.

### Beim Posten

- **«Mit KI erstellt» / KI-Info einschalten:** Die Babys sind KI-generiert (Grok).
- **Sound:** Die Videos sind stumm. Einen ruhigen Trend-Sound wählen, der gerade viel genutzt wird.
- **Titelbild:** `*_titelbild.jpg` (zeigt Baby und Hook)
- **Caption:** Die erste Zeile wiederholt den Hook nicht, sondern bringt das Suchwort. Am Schluss steht eine Bitte zum Weiterleiten:
  - Little Princess: «Geburtsgeschenk fürs Mädchen: das Set «Little Princess» mit Kronen-Schmusetuch, 8 Teile, fertig aufeinander abgestimmt. Bald auf sunnozy.ch. Schick das der Freundin, die bald ein Mädchen bekommt. #geburtsgeschenk #babymädchen #erstausstattung #babyschweiz #sunnozy»
  - Best Family: «Erstausstattung mit Teddy-Rassel: das Set «Best Family», 8 Teile, Beige und Creme. Bald auf sunnozy.ch. Markier jemanden, der bald Gotti oder Götti wird. #erstausstattung #geburtsgeschenk #teddy #babyschweiz #sunnozy»
  - Blumenwiese: «Wickelbody aus Musselin: nichts über den Kopf ziehen, auch nicht um 3 Uhr nachts. Set «Blumenwiese» mit Fusshose und Haarband. Bald auf sunnozy.ch. Welche Mama braucht das? Markier sie. #wickelbody #musselin #babymädchen #babyschweiz #sunnozy»

### Vor dem Posten prüfen

- **Coming soon oder schon im Shop?** In `shopify/README.md` sind alle drei Sets als **aktiv** eingetragen (Best Family CHF 30.90, Blumenwiese CHF 15.90, Little Princess Krone CHF 30.90). Wenn sie schon kaufbar sind, «Coming soon» durch «Neu» und den Preis ersetzen (`set_karte` und `end_karte` im Skript).
- **Safe Sleep:** In den schlafenden Clips liegen ein Plüschhase und ein Tuch neben dem Baby (Little Princess), und das Baby liegt auf einer Strickdecke (Blumenwiese). Beide Babys tragen im Schlaf ein Haarband. Die Babys liegen auf dem Rücken. `marke.md` sagt aber: keine losen Decken oder Tücher im Bett zeigen. Wenn Dir das zu heikel ist, nur die Best-Family-Reels (Baby wach) posten.
- **KI-Abweichungen:**
  - Little Princess: Im Clip trägt das Baby ein rosa Haarband, das im Set nicht drin ist (das Set hat eine Mütze).
  - Best Family: Das Baby trägt Body und Fusshose. Das Set hat einen Strampler, keine Hose.

## Zusammengeschnittene Reels (22.10.2026)

Erstellt mit `python3 tools/make_coming_soon_kombi.py`. Mehrere Clips pro Reel, harte Schnitte im Takt von 1,2–2,6 s, Zoom auf Details, Zeitlupe bei den schönsten Momenten, weiche Blende nur in die Set-Karte und am Schluss zurück ins erste Bild (Loop).

| Datei | Inhalt | Texte | Dauer |
|---|---|---|---|
| `reel_best_family_teddy_kombi_9x16.mp4` | Lächeln, Stickerei ganz nah, Teddy-Rassel, Umarmung in Zeitlupe, Set | POV: Er entdeckt seinen ersten Teddy → Die Teddy-Rassel ist im Set dabei → und er lässt ihn nicht mehr los | 13,9 s |
| `reel_blumenwiese_kombi_9x16.mp4` | Ganz nah: Wickelverschluss, Haarband, Fusshose, Baby in Zeitlupe, Set | Ganz nah: «Blumenwiese» → Wickelbody, nichts über den Kopf → Haarband im gleichen Muster → Fusshose aus weichem Musselin → Blümchen von Kopf bis Fuss | 14,5 s |
| `reel_little_princess_looks_9x16.mp4` | Strampler-Look, Body-Look, Kronen-Schmusetuch, Söckchen, Set | Ein Set, zwei Looks → Look 1: Strampler → Look 2: Body mit Söckchen → Dazu das Kronen-Schmusetuch → 8 Teile | 14,7 s |
| `reel_coming_soon_1-2-3_9x16.mp4` | Alle drei Sets, je mit grosser Zahl | Welches Set würdest Du verschenken? → 1 «Blumenwiese», 2 «Best Family», 3 «Little Princess» → Schreib 1, 2 oder 3 in die Kommentare | 15,0 s |
| `reel_coming_soon_details_9x16.mp4` | Schnelle Detail-Montage aller drei Sets | Die kleinen Details machen den Unterschied → 3 neue Sets, bald bei sunnozy → Speicher Dir das für später → Welches gefällt Dir? | 12,6 s |

**Für Reichweite:** Das 1-2-3-Reel holt Kommentare, die einfach zu schreiben sind, nämlich eine Zahl. Das Detail-Reel wird gespeichert. Die Kombi-Reels sind die stärkere Version der Einzel-Reels: Mit mehr Schnitten bleiben die Leute länger dran.

**Posting-Reihenfolge (Vorschlag):** zuerst das 1-2-3-Reel (Kommentare sammeln), 2 Tage später das Kombi-Reel des Sets mit den meisten Stimmen, danach das Detail-Reel.

**Nicht verwendet (Safe Sleep):** `little-princess/original/baby_clip_d.mp4` (Bauchlage) und die Gänseblümchen-Clips (Decke über dem Baby).

## Ältere Reels (vom 19./20.10.2026)

Erstellt mit `tools/make_set_video.py`: `reel_little_princess_{a,b,c,kombi}_{9x16,4x5}.mp4` und `reel_gaensebluemchen_{a,b,c}_{9x16,4x5}.mp4`, mit `*_standbild.jpg`. Beschreibung und Befehle stehen in `posts/coming-soon/little-princess/README.md` und `posts/coming-soon/gaensebluemchen/README.md`.
