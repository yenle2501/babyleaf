---
name: sunnozy-produktfotos
description: Produktfotos für sunnozy-Babysets erstellen, wenn die Nutzerin ein Set-Foto schickt (Handyfoto oder Lieferantenbild mit Logo/Artikelnummer) und Shop-, Instagram-, Galaxus- oder Amazon-Bilder will. Liefert pro Set eine Shop-Präsentation mit Holzbügel, ein Marktplatz-Hauptbild auf reinweiss sowie Einzelbilder jedes Teils. Auslöser z.B. "mach das gleich für dieses Set", "Produktfoto", "für Galaxus/Amazon", "weisser Hintergrund", "Einzelteile", "gleich wie beim letzten Set".
---

# sunnozy Produktfotos (Set-Workflow)

Die Nutzerin schickt ein oder mehrere Fotos von Babysets. Daraus entstehen ohne Rückfrage:

| # | Ergebnis | Ordner (unter `sunnozy-content/posts/`) |
|---|---|---|
| 1 | Shop-Präsentation: hellgrauer Studio-Hintergrund, Decke/Strampler/Jäckchen auf Holzbügel am Wandknauf, Teile luftig angeordnet. Mit und ohne sunnozy-Logo, **nie mit Artikelnummer** | `produktfotos-set-praesentation/{ki-roh,mit_logo,ohne_logo,original}/` |
| 2 | Marktplatz-Hauptbild Galaxus/Amazon: reinweiss RGB 255, 2000×2000, Produkt ≈88 % der Fläche, kein Text, kein Logo, kein Bügel, keine Deko | `marktplatz-galaxus-amazon/{freigestellt,hauptbild}/` |
| 3 | Einzelbilder pro Teil (reinweiss, 2000×2000, ≈85 %), als Zusatzbilder 2–7 oder Einzelartikel | `marktplatz-galaxus-amazon/einzelteile/<set>/` |

Dateinamen beschreibend: `set_<farbe/motiv>` (z.B. `set_teddy_creme`). Artikelnummern wie „S9329“ **nirgends** übernehmen: weder im Bild noch im Dateinamen.

## Werkzeuge

- Canva-MCP (`mcp__Canva__*`): `create-upload-url`, `generate-image`, `get-generate-image-job`, `remove-background`, `read-design`, `edit-design`, `export-design`
- Skripte in `sunnozy-content/tools/`:
  - `make_set_shop.py <roh-ordner> <ausgabe> [artikelnummer]`: Logo-/Ohne-Logo-Versionen. Keine Artikelnummer angeben.
  - `make_marktplatz.py <png-ordner> <ausgabe> [fuellgrad] [groesse]`: reinweisses Hauptbild aus freigestelltem PNG. Prüft die Ecken auf 255 und gibt den Füllgrad aus.
  - `make_einzelteile.py <set.png> <ausgabe> [paar_abstand] [namen,kommagetrennt]`: zerlegt das freigestellte Hauptbild in Einzelteile, fasst Paare wie Socken und Fäustlinge zusammen und erzeugt einen Kontaktbogen. Braucht `scipy` (`pip install scipy`).
  - `retusche_kreis.py <bild> <x> <y> <radius>`: kleine runde Stelle wegretuschieren, z.B. fremde Logos auf Bügeln.

## Ablauf

### 1. Fotos hochladen
Pro Foto `create-upload-url` aufrufen, dann `curl -X POST -H 'Content-Type: application/octet-stream' --data-binary @datei URL`. Die Antwort enthält die `mediaId`. Bilder mit sichtbarer Artikelnummer sind als Referenz in Ordnung; die Nummer darf nur nicht im Ergebnis erscheinen.

Stil-Referenz für die Bügel-Präsentation (bereits in Canva): **`MAHX8MIuH4w`**. Falls nicht mehr verfügbar, `sunnozy-content/posts/produktfotos-set-praesentation/` als Vorlage hochladen.

### 2. Bilder generieren (pro Set parallel)
**Präsentation** (`aspectRatio: SQUARE_1_1`, Referenzen `[set-foto, MAHX8MIuH4w]`):
> Premium e-commerce set presentation in exactly the style of the second reference image: light grey-white seamless studio background, soft diffused light, very soft shadows, all items smooth and wrinkle-free, spaced generously. Items exactly from the <Set-Beschreibung> in the first reference: on the left the <Decke/Strampler> folded over a plain light wooden hanger (no logo on hanger) on a small wall knob; <weitere Teile mit Position>. No text, no logos, true colours, sharp catalogue quality.

**Marktplatz** (`SQUARE_1_1`, Referenz `[set-foto]`):
> Amazon-style main product image: the complete <Set> from the reference image laid flat from directly above on a plain pure white background, no hanger, no props, no text, no logos. All items fully visible, smooth, wrinkle-free, arranged neatly and compactly to fill most of the square: <alle Teile einzeln beschreiben>. Even studio light, very soft contact shadows, true colours, sharp.

Jedes Teil konkret beschreiben, also Farbe, Print, Stickerei und Schrift. Dann übernimmt die KI die Details treuer.

### 3. Freistellen
Marktplatz-Bild → `remove-background`.

### 4. In voller Auflösung exportieren
`get-generate-image-job` liefert nur Vorschaubilder (≈200 px). Deshalb das Hilfsdesign **`DAHX6xgEj_I`** („sunnozy KI-Fotos Export“) nutzen:
1. `read-design` mit `open_transaction: true`
2. `edit-design` auf Seite 1 mit `add_page` (1264×1264 für quadratisch, 1136×1408 für 4:5)
3. `read-design` mit `page_indices` der neuen Seiten, um die Seiten-IDs zu holen
4. Pro Seite `insert_fill` mit asset_id, left 0, top 0, volle Grösse
5. `finalize: commit`
6. `export-design`: JPG quality 95 für Präsentationen, **PNG mit `transparent_background: true`** für Freisteller
7. Die Download-URLs sofort mit `curl` laden, sie laufen ab.

### 5. Nachbearbeiten
```bash
cd sunnozy-content
python3 tools/make_set_shop.py <roh> posts/produktfotos-set-praesentation          # mit_logo/ohne_logo
python3 tools/make_marktplatz.py <freigestellt> posts/marktplatz-galaxus-amazon/hauptbild
```
**Bügel prüfen:** Die KI kopiert oft das „N“-Logo der fremden Marke aus der Stil-Referenz auf den Bügel. Den Bügel heranzoomen und das Logo bei Bedarf mit `retusche_kreis.py` entfernen, dann `make_set_shop.py` erneut laufen lassen.

### 6. Einzelteile
```bash
python3 tools/make_einzelteile.py posts/marktplatz-galaxus-amazon/freigestellt/<set>.png <tmp>
```
Den Kontaktbogen `<set>_uebersicht.jpg` ansehen:
- **Frei liegende Teile** wie Mütze, Socken, Fäustlinge, Rassel oder Lätzchen werden pixelgenau getrennt. Das ist am besten, weil sie identisch zum Hauptbild sind.
- **Zusammengeklebte, überlappende Kleidungsstücke** (Decke + Strampler + Body) lassen sich nicht trennen. Diese Teile einzeln mit `generate-image` neu erzeugen, mit dem ungeschnittenen Marktplatz-Bild als Referenz:
  > E-commerce single product photo: ONLY the <Teil mit Details> from the reference image, exactly identical in colour and details, laid flat from directly above, centred, filling most of the square, plain pure white background, no other items, no props, no text, soft even light, very soft contact shadow, sharp.

  Danach wie Schritt 3 bis 5 vorgehen: `remove-background`, exportieren, dann `make_marktplatz.py <png-ordner> <ausgabe> 0.85`.
- Am Ende alles mit sprechenden Namen in `einzelteile/<set>/` ablegen (`muetze.jpg`, `socken.jpg`, `strampler.jpg` …).

### 7. Abschluss
- README in den Ordnern ergänzen: Tabelle der Sets und Teile pro Set
- `git add -A sunnozy-content && git commit && git push -u origin <branch>`
- Mit `SendUserFile` die wichtigsten Ergebnisse schicken: je Set Hauptbild, Präsentation und Einzelteil-Übersicht
- Antwort auf Deutsch (Schweizer Schreibweise: ss statt ß, Du-Form), kurz mit Tabelle

## Qualitätsregeln
- Marktplatz: Ecken = (255,255,255), Füllgrad ≥ 85 %, kein Text, nichts, was nicht im Set ist (kein Bügel, keine Deko-Hasen)
- Immer darauf hinweisen: Die Bilder sind KI-generiert. Vor dem Upload Teile-Anzahl, Prints und Farben mit dem echten Produkt abgleichen (Pflicht bei Amazon und Galaxus).
- Echte Fotos der Nutzerin unter `original/` ablegen. Keine Personen und keine fremden Marken ins Bild.
