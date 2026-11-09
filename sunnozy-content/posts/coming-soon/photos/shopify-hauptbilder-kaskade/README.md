# Shopify-Hauptbilder im Kaskaden-Look

Vorlage: Pinterest-Bild der Nutzerin (Ripp-Bodys schräg gestaffelt auf hellgrauem Grund).
Format: **2048 × 2048 px**, JPG. Das ist die Shopify-Empfehlung: quadratisch, Zoom funktioniert. Hintergrund hellgrau (#F4F4F5).

## So entstanden

- **16 Bilder aus echten Shop-Fotos** (`<set>.jpg`): Die Einzelbilder jedes Sets aus Shopify wurden freigestellt (lokal oder mit Canva) und mit `tools/make_kaskade.py` gestaffelt, hinten oben rechts und vorne unten links. Prints, Farben und Teile-Anzahl entsprechen exakt den Shop-Fotos.
- **3 KI-Bilder** (`<set>_KI.jpg`): Für «Little Love», «Little One» und «Sweet Friends» gibt es im Shop keine Einzelbilder. Diese Bilder hat Canva aus dem Gruppenfoto im gleichen Stil erzeugt. **Prints vor dem Hochladen mit dem echten Produkt vergleichen.**

| Datei | Shopify-Produkt | Teile |
|---|---|---|
| `dino_langarm3.jpg` | Langarm-Body 3er «Daddy Mommy love me» Dino | 3 |
| `dinosaur_kurzarm5.jpg` | Body-Set «Dinosaur» Kurzarm 5er | 5 |
| `flying_langarm3.jpg` | Langarm-Body 3er «I Like Flying» | 3 |
| `growing_up_strong_kurzarm5.jpg` | Kurzarm-Body 5er «Growing up strong» | 5 |
| `i_love_hugs_aermellos3.jpg` | Body-Set «I Love Hugs» ärmellos 3er | 3 |
| `i_love_my_mum_kurzarm5.jpg` | «I love my Mum» Kurzarm-Body 5er | 5 |
| `jogginghose5.jpg` | Baby Jogginghose 5er-Set | 5 |
| `kombi_growing_up_strong.jpg` | Kombi-Set «Growing up strong», 5 Bodys + 5 Hosen | 10 |
| `kombi_lovely.jpg` | Kombi-Set «Lovely Little Girl», 3 Bodys + 5 Leggings | 8 |
| `kombi_mumdadme.jpg` | Kombi-Set «Mum Dad Me», 5 Bodys + 5 Leggings | 10 |
| `leggings5.jpg` | Baby Leggings 5er-Set | 5 |
| `love_more_kurzarm5.jpg` | Kurzarm-Body 5er «Love More» | 5 |
| `lovely_langarm3.jpg` | Langarm-Body 3er «Lovely Little Girl» | 3 |
| `mumdadme_langarm5.jpg` | «Mum Dad Me» Langarm-Body 5er | 5 |
| `mummy_kurzarm5.jpg` | Body-Set «I Love My Mummy» Kurzarm 5er | 5 |
| `mummy_langarm3.jpg` | Body-Set «I Love My Mummy» Langarm 3er | 3 |
| `little_love_rosa5_KI.jpg` | Body-Set «Little Love» Rosa 5er (KI) | 5 |
| `little_one5_KI.jpg` | Body-Set «Little One» 5er (KI) | 5 |
| `sweet_friends_kurzarm5_KI.jpg` | Kurzarm-Body 5er «Sweet Friends» (KI) | 5 |

Nicht gemacht: «Princess» Langarm 3er, weil das Set ausverkauft ist (Lager 0).

Neu erzeugen: Einzelteile als `<teile>/<set>/<nr>.png` ablegen, dann `python3 tools/make_kaskade.py <teile> posts/shopify-hauptbilder-kaskade`. Die Reihenfolge der Teile steht in `SETS` im Skript.

## In Shopify übernommen (15.10.2026)

Alle 19 Bilder sind als **erstes Bild (Hauptbild)** in den Produkten gesetzt: Upload über Staged Upload, dann `productUpdate` und `productReorderMedia`. Danach geprüft: Bei allen 19 Produkten ist das neue Bild das Hauptbild, Status READY, 2048 × 2048 px.
- Es wurde **nichts gelöscht**. Die bisherigen Fotos sind eine Position nach hinten gerutscht (jedes Produkt hat jetzt 1 Bild mehr).
- Dateiname in Shopify: `sunnozy-hauptbild-<set>.jpg`, Alt-Text: «<Produkt> – alle Teile im Überblick».
- **Rückgängig machen:** in Shopify beim Produkt das Bild `sunnozy-hauptbild-…` löschen oder nach hinten ziehen. Dann ist das alte Hauptbild wieder vorne.
- Vorher-/Nachher-Übersicht: `../shopify-check_seite1–3.jpg`
