# Set-Präsentation im Shop-Stil

Stil nach deinem Beispiel: hellgrauer Studio-Hintergrund, die Decke hängt auf einem Holzbügel an einem Wandknauf, alle Teile glatt und mit viel Abstand angeordnet.

Mit KI neu erstellt (Canva). Vorlagen waren dein Originalfoto und dein Beispielbild als Stil. Das fremde „N“-Logo auf dem Bügel ist wegretuschiert (`tools/retusche_kreis.py`).

| Ordner | Inhalt |
|---|---|
| `mit_logo/` | sunnozy-Logo oben links, **ohne** Artikelnummer (eigener Shop) |
| `ohne_logo/` | ohne Text (Instagram) |
| Formate | quadratisch (1080×1080), Hochformat (1080×1338), Querformat (1338×1080) |
| `ki-roh/` | Originaldateien aus Canva (retuschiert) |

Generator: `tools/make_set_shop.py <ordner> <ausgabe>` (Artikelnummer nur, wenn man sie als 3. Wert angibt).

Für **Galaxus und Amazon** gibt es eigene Bilder auf reinweissem Hintergrund: `posts/marktplatz-galaxus-amazon/`.

**Bitte prüfen:** Schrift „Princess“, Perlenkette, Gingham und Spitzenkragen sind sehr nah am Original. Kleine Abweichungen sind möglich, z.B. beim Etikett im Kragen.

## Alle Sets

| Set | Dateien |
|---|---|
| Rosa „Princess“ (Gingham, Perlenkette) | `set_rosa_quadratisch / _hochformat / _querformat` |
| Rosa „Hello“ Schmetterling (Ripp, Lochspitze) | `set_hello_schmetterling_quadratisch` |
| Creme Teddy (Bärengesicht, beige Streifen) | `set_teddy_creme_quadratisch` |
| Little Bear (Aquarell-Bären, „Hello Little Bear“) | `set_little_bear_quadratisch` |
| Hello World (Creme, ockerfarbene Blätter) | `set_hello_world_blatt_quadratisch` |
| Weiss „I ♥ Dad Mom“ | `set_love_dad_mom_quadratisch` |
| Lila Hase mit Blümchen | `set_lila_hase_quadratisch` |
| Rosa Gänseblümchen „It's a baby girl“ | `set_gaensebluemchen_quadratisch` |
| Hellblau Wal „Sea vibes“ | `set_wal_blau_quadratisch` |
| Bauernhof „Happy Baby“ | `set_bauernhof_quadratisch` |
| Creme/Rosa „Little Princess“ mit Krone | `set_prinzessin_krone_quadratisch` |
| Rosa Hasen „Little one“ | `set_hase_rosa_quadratisch` |
| Beige/Creme „Best family“ Teddy | `set_best_family_quadratisch` |

Jeweils in `mit_logo/` (sunnozy oben links) und `ohne_logo/`. Originalfotos liegen in `original/`.
Fremde Logos auf den Holzbügeln sind wegretuschiert.

**Korrigiert:** Bei «Gänseblümchen» und «Love Dad Mom» hatte die erste Version einen Kurzarm-Body. Laut Originalfoto ist es ein Langarm-Body; beide Präsentationen sind neu erstellt.

## In Shopify als Hauptbild gesetzt (15.10.2026)

| Bild (`mit_logo/`) | Shopify-Produkt | Status |
|---|---|---|
| `set_rosa_quadratisch.jpg` | Erstausstattung-Set «Princess» – Rosa, 8-teilig | Hauptbild ✔ |
| `set_hello_schmetterling_quadratisch.jpg` | Erstausstattung-Set «Hello» – Rosa, 6-teilig | Hauptbild ✔ |
| `set_little_bear_quadratisch.jpg` | Erstausstattung-Set «Hello Little Bear» – Creme, 5-teilig | Hauptbild ✔ |
| `set_teddy_creme_quadratisch.jpg` | Erstausstattung-Set «Teddybär» – Creme, 8-teilig | **offen:** Bild zeigt 9 Teile (Beissring und Rassel getrennt) |
| `set_hello_world_blatt_quadratisch.jpg` | Erstausstattung-Set «Hello World» – Creme, 8-teilig | **offen:** Bild zeigt 7 Teile (kein T-Shirt) |
| Bauernhof, Best family, Gänseblümchen, Hase rosa, Lila Hase, Love Dad Mom, Prinzessin Krone, Wal | nicht im Shop | – |

Alte Fotos sind nicht gelöscht, nur eine Position nach hinten gerutscht. Dateiname in Shopify: `sunnozy-set-…-praesentation.jpg`.

## Neue Sets (15.10.2026)

| Set | Teile (8) | Dateien |
|---|---|---|
| Little and Loved – Rosa mit Gänsen | Strampler, Body «little and loved», Jäckchen mit Gans, T-Shirt, Hose, Lätzchen «Mommy's little alarm duck!», Mütze, Fäustlinge | `set_little_and_loved_gans_rosa_quadratisch.jpg` |
| Hello World – Creme mit Blättern | Strampler, Body «hello world», Jäckchen «hello», T-Shirt, Hose, Lätzchen «hello I'm new here», Mütze, Fäustlinge | `set_hello_world_creme_quadratisch.jpg` (ersetzt `set_hello_world_blatt_…`, dort fehlte das T-Shirt) |

Mit KI erstellt (Vorlage: Fotos der Nutzerin in `original/`). Vor dem Upload Teile, Prints und Farben mit dem echten Produkt abgleichen.
Für den Shop gibt es die Präsentationen zusätzlich mit reinweissem Hintergrund in `../shopify-hauptbilder-weiss/`.

## Neue Sets (15.10.2026, Runde 2)

| Set | Teile | Datei (`mit_logo/`, `ohne_logo/`) |
|---|---|---|
| Hund – Creme/Beige | 8: Strampler «I ♥ DOGS», Mütze mit Öhrchen, Langarm-Body, Fäustlinge, Plüsch-Hündchen, Söckchen, Lätzchen «HUG ME!», Kapuzentuch «Home is where the Dog is» | `set_hund_creme_quadratisch.jpg` |
| Weltall – Hellblau/Weiss | 8: Strampler mit Planeten/Sonnen, Mütze, Langarm-Body mit Planet, Kapuzentuch «Little one», Fäustlinge, Sonnen-Rassel, Söckchen, Lätzchen mit Planet | `set_weltall_hellblau_quadratisch.jpg` |
| Waldbär – Creme | 5: Strampler mit Bären und Bäumen, Mütze, Ripp-Body mit Bär, Fäustlinge, Lätzchen «Little Bear» | `set_waldbaer_creme_quadratisch.jpg` |
| Teddy – Rosa mit Pünktchen | 5: Ripp-Strampler gepunktet, Mütze mit Bommel, Ripp-Body Teddy auf Wolke, Fäustlinge, Lätzchen «Little Bear» | `set_teddy_rosa_punkte_quadratisch.jpg` |
| Smile – Salbeigrün | 3: Ripp-Strampler «You make me happy», Knotenmütze, Kapuzentuch «SMILE» | `set_smile_gruen_quadratisch.jpg` |

Mit KI erstellt (Vorlage in `original/`, Artikelnummern aus den Lieferantenbildern nicht übernommen). Vor dem Upload Teile, Prints und Farben mit dem echten Produkt abgleichen.
