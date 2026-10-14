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
