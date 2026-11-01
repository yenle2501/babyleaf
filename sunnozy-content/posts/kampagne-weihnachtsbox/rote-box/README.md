# Weihnachts-Geschenkboxen in der roten sunnozy-Box (01.11.2026)

Nach den Vorlagen der Nutzerin (`vorlage/vorlage_offen.jpg`, `vorlage/vorlage_zu.jpg`): offene rote Weihnachtsbox von oben,
Deckel mit «sunnozy»-Satinband, Blumen-Seidenpapier, «Merry Christmas»-Karte. Deckel, Band, Papier und Karte kommen
unverändert aus der Vorlage (Schrift bleibt sauber). Nur der **Inhalt im Karton ist mit KI erstellt** (Canva, nach den
Inhalten der Boxen) und eingesetzt.

| Ordner | Was |
|---|---|
| `shopify/geschenkbox-<box>.jpg` | Hauptbilder 2048 × 2048, **in Shopify hochgeladen** (Position 1) |
| `shopify/geschenkbox-zu-mit-sunnozy-band.jpg` | geschlossene Box, bei allen 9 Boxen als Bild 2 hochgeladen |
| `ads/feed_<box>_4x5.jpg` | Anzeige Feed 1080 × 1350 mit Name, Inhalt und Preis |
| `ads/quadrat_<box>_1x1.jpg` | Anzeige 1080 × 1080 |
| `ads/story_<box>_9x16.jpg` | Story/Reel 1080 × 1920, oben und unten frei für Instagram |
| `ads/uebersicht_4x5.jpg` | alle Feed-Anzeigen auf einen Blick |
| `4x5/`, `komposit/` | Zwischenstufen (4:5 ohne Text, Grundbild für die Anzeigen) |
| `inhalt/<box>.jpg` | KI-Inhaltsbilder (4:3) |
| `vorlage/` | Vorlagen der Nutzerin, `vorlage_offen_2x.jpg` mit Real-ESRGAN scharf hochgerechnet |

## Shopify (Kollektion «Geschenkboxen», 9 Produkte)

Pro Produkt: 1. neues Hauptbild rote Box, 2. geschlossene Box, danach die bisherigen Bilder der Sets.
Entfernt wurden die alten Bilder mit der rosa Box (Hauptbild und, wo vorhanden, das Foto «in der rosa Box»).

| Box | Inhalt | Preis |
|---|---|---|
| «Mum Dad Me» | 5 Bodys + 5 Leggings | CHF 42.90 |
| «Lovely Little Girl» | 3 Bodys + 5 Leggings | CHF 39.90 |
| «Growing up strong» | 5 Bodys + 5 Jogginghosen | CHF 42.90 |
| «I love my Mummy» | 3 Bodys + 3 Halstücher | CHF 29.90 |
| «Dino» | 3 Bodys + 3 Mulltücher | CHF 39.90 |
| «Dinosaur» | 5 Bodys + 5 Jogginghosen | CHF 42.90 |
| «Little One» | 5 Bodys + 3 Mulltücher | CHF 44.90 |
| «I like flying» | 3 Bodys + 5 Leggings | CHF 39.90 |
| «Little One» Jogginghosen | 5 Bodys + 5 Jogginghosen | CHF 42.90 |

## Neu erzeugen

```bash
python3 tools/make_rote_box.py            # Hauptbilder aus inhalt/*.jpg
python3 tools/make_rote_box_ads.py        # Anzeigen (Preise in BOXEN)
```

**Vor dem Schalten der Anzeigen:** Der Inhalt ist KI-generiert. Drucke und Farben jeder Box mit der echten Ware vergleichen.
