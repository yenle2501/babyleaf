# Hook-Analyse: Reel «Hello Little Bear» auf dem Bett (10.11.2026)

Clip: `original/clip_bett.mp4` (KI, 15 s). Ein Neugeborenes liegt wach auf einem weissen Laken, im Teddy-Strampler mit Reissverschluss und der Mütze mit Bärenöhrchen. Die Kamera zoomt langsam heran. Es gibt kein Kuscheltier und keine Decke, Safe Sleep ist also in Ordnung.

Vorgabe: **kein Preis** im Reel.

## Stil (nach der Vorlage der Nutzerin, 10.11.2026)

Die Vorlage ist eine Bildschirmaufnahme eines fremden Reels. Übernommen ist nur der Stil, kein Bild, kein Text und kein Name. Erste Version mit Creme-Feld und Schlusskarte, am 10.11.2026 auf Wunsch der Nutzerin ersetzt.

- **Video in voller Grösse** (9:16), keine Ränder, keine Schlusskarte, **kein Preis**
- **Eine einzige POV-Zeile** in weisser Schreibmaschinenschrift (Courier Prime, OFL), klein, mitten im Bild, mit ✨ am Ende
- **Text nur 0–3,2 s**, dann nur das Baby. Ab 9,6 s kommt der Text zurück, damit der Loop nahtlos ins erste Bild läuft. Wer zweimal schaut, zählt doppelt.
- **11 s lang:** kurz genug, dass viele bis zum Ende schauen und das Reel noch einmal läuft

## Was die Zuschauerin anhält

Grundlage ist unsere Recherche in `posts/coming-soon/photos/instagram/pov-hooks.md` (Quellen dort).

| Regel | Umsetzung |
|---|---|
| **Hook ab dem ersten Bild**, in 2 s lesbar | Der Text steht ab Bild 1, ohne Logo-Intro, mit 6–10 Wörtern. |
| **Szene statt Beobachtung:** Wer sich erkennt, bleibt. | «POV: Dein Baby kommt im Winter ✨» betrifft alle, die im Dezember bis Februar Termin haben. Es ist jetzt November. |
| **Teilen** ist das stärkste Signal für Leute, die uns noch nicht folgen. | «POV: Du wirst bald Gotti und das Geschenk ist schon da ✨»: Das schickt man dem Gotti oder es schickt sich selbst. |
| **Ruhe statt Werbung** | Nach dem Text nur das Baby. Das Produkt wirkt durch das Bild, die Infos stehen in der Caption. |
| **Ohne Ton verständlich**, Text nie auf dem Gesicht | Der Text liegt auf dem Bauch, das Gesicht bleibt frei. |

## Varianten (A/B-Test)

| Datei | Text (0–3,2 s und ab 9,6 s) |
|---|---|
| `reel_hello_little_bear_winter_9x16.mp4` | POV: Dein Baby kommt im Winter ✨ |
| `reel_hello_little_bear_gotti_9x16.mp4` | POV: Du wirst bald Gotti und das Geschenk ist schon da ✨ |

Beide dauern 11 s, sind 1080 × 1920 und haben ein Titelbild `_titelbild.jpg` mit dem Text. Neu erzeugen: `python3 tools/make_reel_hello_little_bear_hook.py`. Musik: «Christmas Lullaby» (Mixkit, lizenzfrei). Andere Texte lassen sich in `VARIANTEN` im Skript eintragen.

**Test:** zuerst «Winter» posten, 3 Tage später «Gotti». Nach 48 h vergleichen:
- Views
- Anteil der Leute, die länger als 3 s schauen
- wie oft geteilt und gespeichert

Den Gewinner als Anzeige bewerben.

## Weitere Hooks für spätere Versionen (gleicher Clip)

- «POV: Woche 1 zu Hause und schon so wach» (genauer Moment)
- «Achte auf die Mütze 🐻» (Detail, macht neugierig und hat Inhalt)
- «Termin im Januar? Speicher Dir das.» (Speichern ist ein starkes Signal)
- Mundart fürs Gotti: «Du wirsch Gotti? Das isch s'erschte Gschänk.»

## Captions (ohne Preis)

**Winter**
> Winterbaby unterwegs? 🧸 Das Erstausstattungs-Set «Hello Little Bear» hat einen Strampler mit Reissverschluss, einen Body, eine Mütze mit Bärenöhrchen, Fäustlinge und ein Lätzchen, alles aus 100 % Baumwolle. Es gibt das Set auch in Grösse 0–3 Monate.
>
> Link in der Bio.
>
> Wann ist Dein Termin? Schreib den Monat in die Kommentare 👇
>
> #erstausstattung #winterbaby #neugeboren #babyschweiz #sunnozy

**Gotti**
> Geburtsgeschenk vom Gotti 🤍 Das Set «Hello Little Bear» hat 5 Teile aus 100 % Baumwolle, mit Reissverschluss statt Knöpfen und mit Bärenöhrchen an der Mütze.
>
> Link in der Bio.
>
> Schick das jemandem, der bald Gotti oder Götti wird.
>
> #geburtsgeschenk #erstausstattung #babygeschenk #babyschweiz #sunnozy

## Vor dem Posten

- **«Mit KI erstellt»** einschalten: Das Video ist KI.
- **Produkt markieren:** Das Set im Reel als Produkt taggen (Shopping-Tag), weil die Caption keinen klickbaren Link hat.
- **Lager prüfen:** Am 10.11. waren 5 Stück da (3 × 0–3 Monate, 2 × 3–6 Monate). Den Satz zu 0–3 Monaten nur stehen lassen, wenn diese Grösse noch da ist.
- **Print prüfen:** Teddy-Print, Reissverschluss und Mützenöhrchen mit der echten Ware vergleichen.
