# Shopify-Hauptbilder klarer (alle 53 aktiven Produkte)

**Status: In Shopify übernommen am 17.10.2026** (52 von 53). Per `fileUpdate` an derselben Media-ID ersetzt: Position, Alt-Text und Titel sind gleich geblieben. Danach geprüft: alle 52 READY, 2048 px, Live-Bild entspricht der Datei.

**Nicht ersetzt:** «I Like Flying» Langarm-Body 3er. Dort hattest Du das Hauptbild inzwischen selbst geändert (13_6.jpg), das bleibt so.

## Befund

- Das Theme lädt die Bilder in voller Grösse (bis 3840 px). Am Shop liegt es also nicht.
- Die Bilder selbst sind weich. Viele sind 2048 px gross, enthalten aber nur Details für etwa 800–1000 px. Sie wurden aus kleinen Lieferanten- oder KI-Bildern hochgezogen. Dazu kommen Kompressionsspuren (Farbklötzchen).

## Was gemacht wurde (`tools/hauptbild_klar.py`)

- Farbklötzchen und Farbsäume aus der JPEG-Kompression entfernt. Kanten, Schrift und Stoffstruktur bleiben unangetastet.
- Flache Flächen leicht entrauscht.
- In zwei Stufen geschärft: fein für Kanten und Schrift, grob für Mikrokontrast. Weiche Bilder bekommen mehr.
- Weisser Grund bleibt reinweiss (255). Gespeichert mit Qualität 95. Bilder unter 2048 px wurden auf 2048 px gebracht.
- Bildausschnitt, Farben und Seitenverhältnis bleiben gleich. **Nichts wird dazuerfunden.**

**KI-Upscaling getestet und verworfen:** Real-ESRGAN hat feine Muster weggeglättet, z.B. das Karo am Princess-Strampler, die Rippstruktur und die Druckknöpfe. Das hätte das Produkt verfälscht.

## Dateien

| Ordner/Datei | Inhalt |
|---|---|
| `bilder/<handle>.jpg` | 53 neue Hauptbilder, benannt nach dem Shopify-Handle |
| `check_hauptbilder_1–3.jpg` | Prüfbogen: Vorschau + Ausschnitt in 100 %, vorher/nachher |
| `produkte.json` | Produkt-ID, Media-ID, alte URL |
| `../shopify-backup-hauptbilder-vor-klar/` | alle bisherigen Hauptbilder als Backup (zum Rückgängigmachen) |

## Ehrliche Grenze

Schärfen holt heraus, was im Bild steckt, kann aber keine Details erzeugen, die die Vorlage nicht hat. Wirklich scharf werden diese Produkte nur mit besseren Fotos:
- Beim Lieferanten nach Originalfotos in voller Auflösung fragen, oder
- selbst fotografieren: Tageslicht, Handy auf Stativ, von oben, weisser Karton.

Am weichsten sind: Mulltücher 90×100 (Verpackungsfotos), Söckchen «Tier & Natur» (744 px), «Princess» Langarm-Body (922 px), Body-Sets «Little Love», «Little One» und «Sweet Friends».

## Rückgängig machen

Die bisherigen Bilder liegen in `../shopify-backup-hauptbilder-vor-klar/<handle>.jpg`. Zurück geht es genauso: hochladen und per `fileUpdate` an dieselbe Media-ID (siehe `produkte.json`).
