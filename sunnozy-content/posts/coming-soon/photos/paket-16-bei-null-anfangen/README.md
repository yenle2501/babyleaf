# Paket 16: «Bei 0 anfangen» (Reel + Pin)

Vorbild: Reel einer Kinderbuch-Marke («Начинать с 0 не страшно – страшно так и не начать»), 5 s.

## Analyse Vorbild

| Zeit | Bild | Text |
|---|---|---|
| 0–2,5 s | Gedimmtes, warmes Wohnzimmerlicht. Laptop mit dem neuen Instagram-Profil (0 Follower), davor ein Cupcake mit goldener Zahlenkerze «0». Eine goldene Schere schneidet ein Band durch (Eröffnung). | «Bei **0** anfangen / *ist nicht schlimm*» |
| 2,5–3,5 s | Harter Schnitt näher ran. Die Flamme lodert gross auf und erlischt. | «*Schlimm* ist nur, / nie anzufangen» |
| 3,5–5 s | Rauchfaden, ruhiges Bild | gleich |

Die Schrift ist eine weisse Serifenschrift, teils kursiv, mit einer grossen «0». Die zwei Zeilen stehen versetzt und haben einen weichen Schatten.

## sunnozy-Version

| Zeit | Inhalt |
|---|---|
| 0–3,4 s | KI-Szene: Handy auf Holzständer statt Laptop, darauf das **echte sunnozy-Profil**. Beiträge zählen von 0 auf 51, Follower von 0 auf 88, die Kerze flackert. Text 1. |
| 3,4–3,9 s | Die Flamme lodert auf, kippt (Pusten) und geht aus. Der Raum wird etwas dunkler. |
| 3,9–7,8 s | Harter Schnitt näher ran, Rauch steigt auf, Text 2. Bei 5,7 s springt «Folgen» auf «Gefolgt» (89 Follower). Ab 6,4 s erscheint das sunnozy-Logo. |

Statt des Band-Schnitts zählt der Follower-Zähler hoch. Das erzählt «bei 0 angefangen» mit Euren echten Zahlen.

| Datei | Format |
|---|---|
| `reel_bei_null_anfangen_9x16.mp4` | Instagram/TikTok Reel 1080×1920, 7,8 s, stummer Ton (Musik in der App wählen) |
| `pin_bei_null_anfangen_2x3.mp4` | Pinterest 1000×1500 |
| `*_standbild.jpg` | Titelbild |
| `profil_bildschirm.png` | Handy-Bildschirm (Besucher-Ansicht des Profils) |
| `ki-roh/` | KI-Szenen: Kerze brennt / aus (Canva, deckungsgleich) |

**Profil-Bildschirm:** Er basiert auf dem Screenshot vom 16.10.2026. Entfernt wurden das Dashboard (Aufrufe), «Profil bearbeiten» und «Personen entdecken», weil dort fremde Personen und Marken zu sehen waren. Das Raster zeigt sunnozy-Set-Fotos. Aktualisierte Zahlen kannst Du in `tools/make_bei_null_reel.py` anpassen (`BEITRAEGE, FOLLOWER, GEFOLGT`).

**KI-Hinweis:** Wohnzimmer, Handy und Cupcake sind KI-generiert. Beim Posten auf Instagram «Mit KI erstellt» (KI-Info) aktivieren.

## Bildunterschrift (Vorschlag)

> Bei 0 anfangen ist nicht schlimm. Schlimm ist nur, nie anzufangen. 🕯️
> Angefangen haben wir mit 0 Beiträgen und 0 Followern. Heute sind wir eine kleine Community von Mamis, Papis und Gottis aus der ganzen Schweiz. Danke, dass Du dabei bist! ☀️
> Neu hier? Folg uns für weiche Babysets, Geschenkideen und kleine Sonnenschein-Momente.
> 🛍️ sunnozy.ch
>
> #sunnozy #schweizerkindermode #babykleidung #kleinunternehmen #smallbusinessschweiz #babyschweiz #erstausstattung #startup #mamaschweiz #babygeschenk

Musik-Tipp: ruhiger Piano- oder Lo-Fi-Track. Ein Puste-Geräusch beim Ausgehen der Kerze (3,7 s) wirkt stark.

## Selbst filmen (Drehliste)

Falls Du lieber echtes Material willst (wirkt am authentischsten):

1. Abends, nur Stehlampe an, warmes Licht. Handy 1 auf einem Ständer mit Deinem Profil, Display-Helligkeit runter.
2. Cupcake mit Zahlenkerze «0» (gold) davor. Mit Handy 2 von leicht unten filmen, Kerze rechts im Bild.
3. **Einstellung 1** (3 s): Kerze brennt, Handy-Kamera ruhig halten.
4. **Einstellung 2** (3 s): näher ran, Kerze auspusten, Rauch filmen.
5. Optional als Eröffnung: ein Band vor dem Handy mit einer goldenen Schere durchschneiden, wie im Vorbild.
6. Texte in Instagram mit einer Serifenschrift (z.B. «Editor» oder «Classic») einfügen, zweite Zeile kursiv versetzt.

Erstellt mit `tools/make_profil_bildschirm.py` und `tools/make_bei_null_reel.py`.
