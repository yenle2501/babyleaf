# Einzelteile pro Set (Galaxus / Amazon)

Jedes Teil als eigenes Produktfoto: reinweiss RGB 255, 2000×2000 px, Teil füllt ca. 85 %.
Verwendbar als Zusatzbilder 2–7 beim Set oder als Hauptbild, wenn ihr Teile einzeln verkauft.

| Set | Teile |
|---|---|
| `set_rosa` | Decke, Strampler, Body, Mütze, Fäustlinge, Socken, Rassel, Lätzchen |
| `set_hello_schmetterling` | Decke, Strampler, Body, Hose, Häubchen, Lätzchen |
| `set_teddy_creme` | Decke, Strampler, Body, Mütze, Socken, Fäustlinge, Rassel, Beissring, Lätzchen |
| `set_little_bear` | Strampler, Body, Mütze, Lätzchen, Fäustlinge |
| `set_hello_world_blatt` | Strampler, Jäckchen, Zweiteiler (Oberteil + Hose), Body, Lätzchen, Mütze, Fäustlinge |
| `set_love_dad_mom` | Kapuzentuch, Strampler, Body, Hose, Mütze, Lätzchen |
| `set_lila_hase` | Kapuzentuch, Strampler, Body, Hose, Mütze, Lätzchen |
| `set_gaensebluemchen` | Kapuzentuch, Body, Strampler, Mütze, Socken, Rassel, Fäustlinge, Lätzchen |
| `set_wal_blau` | Kapuzentuch, Body, Strampler, Mütze, Socken, Fäustlinge, Schmusetuch, Lätzchen |
| `set_bauernhof` | Kapuzentuch, Body, Strampler, Mütze, Socken, Fäustlinge, Rassel, Lätzchen |
| `set_prinzessin_krone` | Kapuzentuch, Body, Strampler, Mütze, Socken, Fäustlinge, Schmusetuch, Lätzchen |
| `set_hase_rosa` | Kapuzentuch, Body, Strampler, Mütze, Socken, Fäustlinge, Rassel, Lätzchen |
| `set_best_family` | Kapuzentuch, Body, Strampler, Mütze, Socken, Fäustlinge, Rassel, Lätzchen |

**So entstanden:**
- Frei liegende Teile (Mützen, Socken, Fäustlinge, Rasseln, Lätzchen und das ganze Hello-Set) sind **pixelgenau aus dem Hauptbild ausgeschnitten** (`tools/make_einzelteile.py`). Sie sind identisch mit dem Set-Bild.
- Teile, die sich im Hauptbild überlappen (Decken, Strampler, Bodys, Jäckchen), hat die KI einzeln neu erzeugt (Canva), mit dem Hauptbild als Vorlage.

**Die 8 neuen Sets** (Love Dad Mom bis Best family) wurden mit Abstand zwischen allen Teilen erzeugt. Deshalb sind dort **alle Teile pixelgenau aus dem Hauptbild ausgeschnitten**, auch Decken, Strampler und Bodys.
Ausnahmen: Wo sich zwei Ärmel berühren, trennt eine Schnittlinie die Teile (Gänseblümchen, Love Dad Mom).
Beim Love-Dad-Mom-Body lag der linke Ärmel unter dem Strampler; er ist vom rechten Ärmel gespiegelt ergänzt.

Pro Set gibt es einen Kontaktbogen `<set>_uebersicht.jpg`. Die ersten 5 Sets sind zusammen in `uebersicht_alle.jpg`, die 8 neuen in `uebersicht_8_neue_sets.jpg`.

Bitte vor dem Upload mit dem echten Produkt vergleichen. Bei Hello World sind die kleinen Etiketten nur angedeutet.
