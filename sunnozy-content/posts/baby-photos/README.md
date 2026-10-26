# Baby-Fotos: Looks mit Baby

Alle Baby-Fotos liegen flach in diesem Ordner, ohne Unterordner. Alle Babys sind KI-generiert (Canva) und fiktiv. Beim Posten **«Mit KI erstellt»** einschalten.

| Look | Datei | Was das Baby trägt | Szene |
|---|---|---|---|
| 1 | `baby_<set>_1.jpg` | Strampler (bzw. Hauptteil des Sets) | zerknitterte weisse Bettdecke, von oben, Plüschtier daneben (20./21.10.2026, früher `products-photo-baby/`) |
| 2 | `baby_<set>_2.jpg` | **Body** mit Mütze und Söckchen, Fäustlingen oder Hose aus dem Set | Baby wach auf cremefarbener Strickdecke, von oben |
| 3 | `baby_<set>_3.jpg` | **Kapuzentuch nach dem Bad** im Arm der Mama; bei Sets ohne Kapuzentuch **Jäckchen** auf dem Sofa (Hello World Blatt, Hello World creme, Little and Loved) bzw. **Strampler** auf dem Schoss (Little Bear) | Handyfoto zu Hause, Tageslicht |

Looks 2 und 3 gibt es für 15 Sets (23.10.2026): bauernhof, best_family, gaensebluemchen, hase_rosa, hello_schmetterling, hello_world_blatt, hello_world_blatt_creme, lila_hase, little_and_loved_gans_rosa, little_bear, love_dad_mom, prinzessin_krone, rosa, teddy_creme, wal_blau. Übersicht: `uebersicht_looks_2_3.jpg` (Look 1: `uebersicht_handyfoto_look1.jpg`).

Format: 4:5, 2272 × 2816 px. Canva liefert höchstens 1136 × 1408; hochgerechnet mit Real-ESRGAN x4plus (seit 25./26.10.2026, vorher x4 compact), 30 % Lanczos-Original zurückgemischt, leicht nachgeschärft und feines Korn, damit die Haut nicht wächsern wirkt. Look 1 ist noch mit dem alten Verfahren hochgerechnet.

## Handyfotos pro Produkt (`baby_echt_*`)

Ein Foto pro Produkt aus dem Shop und den Coming-soon-Sets (78 Produkte), wie von einer Mama mit dem Handy aufgenommen. Übersicht: `uebersicht_echt.jpg`.

| Datei | Stil |
|---|---|
| `baby_echt_<produkt>.jpg` | **neuer Stil «echt»** (ab 25.10.2026, nach den Instagram-Beispielen der Nutzerin): echte Neugeborenen-Merkmale (geschwollene Lider, fleckige Haut, Milien), nah und nicht ganz mittig, Fensterlicht mit leicht überstrahlten Stellen, kein Studiolicht, keine glatte KI-Haut |
| ~~`baby_handy_<produkt>.jpg`~~ | erster Stil (24.10.2026), etwas glatter; am 26.10.2026 vollständig durch `baby_echt_*` ersetzt und gelöscht (in der Git-Historie noch vorhanden) |

Alle Babys sind wach, die Augen offen (bei Mützen besonders geprüft), nichts liegt auf dem Baby. Szenen im Stil «echt»: Stubenwagen mit Sherpa-Rand, an der Brust auf dem Sofa (weisses T-Shirt), auf zerknittertem Laken am Fenster, im Arm (grauer Pullover). Lätzchen, Halstücher, Sommer-Sets: 5–6 Monate altes Baby auf dem Schoss. Mulltücher: Baby liegt wach auf dem Tuch. Söckchen: Füsschen in Mamas Hand.

Bei `baby_echt_leggings_ripp_pastell.jpg` hatte die KI einen weissen, logoähnlichen Haken auf das Hosenbein gesetzt; er ist wegretuschiert. Prompts: `prompts.md`.

## Instagram-Bilder der Coming-soon-Sets

`instagram/` enthält alle Feed-, Story- und Baby-Bilder aus `posts/coming-soon/<set>/instagram/` (verschoben am 23.10.2026, flach, Dateinamen beginnen mit dem Set).

## Entstehung Looks 2 und 3

1. Referenz pro Look: die Einzelteile aus `marktplatz-galaxus-amazon/einzelteile/set_<set>/` als Collage auf Weiss.
2. Canva `generate-image` mit dieser Referenz, 4:5. Prompts: Body-Look «awake newborn on a cream knitted blanket, shot from above … wears EXACTLY the clothes from the reference», Kapuzentuch-Look «parent's arms hold an awake newborn wrapped in EXACTLY the hooded towel …, face uncovered».
3. Export über das Canva-Hilfsdesign `DAHYpiIMPVU`, Seiten 16–45 (`look_01` … `look_30`).
4. Canva-Media-IDs: `canva_ids_looks_2_3.txt`.

## Vor dem Posten prüfen

- **Schrift auf den Teilen:** Die KI schreibt Text nicht immer sauber. Beim Wal-Kapuzentuch (`baby_wal_blau_3.jpg`) ist «Just Swimming» unleserlich, beim Rosa-Kapuzentuch (`baby_rosa_3.jpg`) ist «Princess» nur angedeutet. Diese beiden lieber nicht als Produktbild verwenden, oder neu erzeugen.
- **Little and Loved, Look 3:** Das Baby trägt zur Jacke und zum T-Shirt eine cremefarbene Hose. Die Hose ist im Set enthalten, aber nicht in der Referenz; Farbe prüfen.
- Alle Babys sind wach, auf dem Rücken oder im Arm, ohne Decke über dem Körper (Safe Sleep).
