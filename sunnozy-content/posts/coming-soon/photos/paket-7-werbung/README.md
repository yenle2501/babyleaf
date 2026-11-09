# Paket 7: Werbe-Formate nach deinen Vorlagen

| Datei | Vorlage | Format | Inhalt |
|---|---|---|---|
| `01_weihnachten.jpg` | Blossom & Pear (Baby mit Mütze und Reh) | 4:5 | Baby mit Weihnachtsmütze und Kuscheltier, Body Teddy creme, ohne Text |
| `02_shop_jetzt.jpg` | Belife «Shop anytime / Shop now» | 9:16 | 3 Bodys freigestellt auf Leinen, Tasche mit sunnozy-Logo, «SHOPPEN JEDERZEIT / SHOPPEN JETZT» |
| `03_sticker_wand.jpg` | Belife «Every shade / Every shape» | 9:16 | 9 Teile als Sticker mit Pin, «JEDE FARBE / JEDER MOMENT» |
| `04_fotowand.jpg` | MKI «End of season sale» | 9:16 | 8 Fotos mit Klebeband, Mitte «NEUE SETS SIND DA» |
| `05_new_drop.jpg` | «New drop tomorrow at 7pm» | 9:16 | leere Blätter mit Büroklammern, Handschrift «neues Set / morgen um 19 Uhr» |
| `06_angebot.jpg` | Dilling Pullover auf Grün | 4:5 | Body auf Salbeigrün, «20 % AUF ALLE SETS», Logo senkrecht |
| `07_angebot_foto.jpg` | Dilling Kind im Grünen | 4:5 | Lifestyle-Foto, «NUR BIS MITTERNACHT 20 %» |
| `08_vorteile.jpg` | Dilling Milchglas-Karte | 4:5 | «100 % Baumwolle», 5,0 Sterne, Versand CH, gratis ab CHF 50, 14 Tage Rückgabe |
| `09_weihnachten_geschenk.jpg` | Weihnachten | 4:5 | Geschenkbox Best family, «DAS GESCHENK ZUR GEBURT» |

**Vor dem Posten anpassen:** Rabatt (20 %) und Datum (21.–23.11.) sind Platzhalter. Ändern in `tools/make_paket7.py` (oben, `ANGEBOT`) und neu laufen lassen:
`python3 tools/make_paket7.py posts/paket-7-werbung/roh posts/paket-6-soft/feed posts/paket-7-werbung`

Vorteile und 5,0 Sterne stammen aus `marke.md`. Bitte prüfen, ob das noch stimmt.
Babys, Hintergründe und Tasche sind KI-generiert (Canva); die Teile sind aus euren Produktbildern freigestellt.

## Captions
| Post | Caption |
|---|---|
| 01 | Ho ho ho 🤍 Der erste Advent mit dir. #sunnozy #erstesweihnachten #babyschweiz |
| 02 | Weich, sicher, liebevoll. Und rund um die Uhr bestellbar 🤍 Link in der Bio. #sunnozy #babyshop #schweiz |
| 03 | Jede Farbe, jeder Moment ☁️ Welcher ist dein Liebling? #sunnozy #babymode |
| 04 | Neue Sets sind da 🤍 Alle Teile im Shop. #sunnozy #neuheiten |
| 05 | Psst… morgen um 19 Uhr 🤫 Glocke aktivieren! #sunnozy #comingsoon |
| 06 | Nur dieses Wochenende: 20 % auf alle Sets 🤍 #sunnozy #babyschweiz |
| 07 | Letzte Chance: 20 % bis Mitternacht. #sunnozy |
| 08 | 100 % Baumwolle, Versand aus der Schweiz, gratis ab CHF 50 🇨🇭 #sunnozy |
| 09 | Das Geschenk zur Geburt, schön verpackt 🎁 #sunnozy #geburtsgeschenk #weihnachten |
