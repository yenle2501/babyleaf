# Kampagne «Weihnachts-Geschenkbox»

Für Schenkende (Gotti, Götti, Grosseltern, Freundinnen), passend zur Kampagne «Das schönste Hallo» aus dem Markenplan. In jeder Box liegt ein **ganzes Set** aus dem Shop (Body-Set + Hosen-Set, + Halstücher oder + Mulltücher), jedes Teil gefaltet und mit Satinband gebunden, dazu die Weihnachtskarte.

Darstellung nach den Vorbildern der Nutzerin: Box von oben, randvoll und von Hand gepackt (Instagram-«Baby Box»-Stil), Karte oben in der Box. Die Fotos sind mit Canva-KI erzeugt aus: Box-Foto der Nutzerin (`vorlage_geschenkbox.jpg`), den Shop-Bildern der Sets und der Karte.

## Check: die acht Boxen

| Box | Inhalt | Preis | Gewinn* | Shopify (Entwurf) | Lager je Grösse |
|---|---|---|---|---|---|
| «Mum Dad Me» | 5 Langarm-Bodys + 5 Leggings | CHF 42.90 | +16.45 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293061054807) | 2 / 2 / 2 |
| «Lovely Little Girl» | 3 Langarm-Bodys + 5 Leggings | CHF 39.90 | +16.58 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063250263) | 2 / 2 / 2 |
| «Growing up strong» | 5 Kurzarm-Bodys + 5 Jogginghosen | CHF 42.90 | +17.18 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063348567) | 2 / 2 / 2 |
| «I love my Mummy» | 3 Langarm-Bodys + 3 Halstücher | CHF 29.90 | +13.00 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063414103) | 2 / 2 / 1 |
| «Dino» | 3 Langarm-Bodys + 3 Mulltücher blau | CHF 39.90 | +15.53 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063512407) | 2 / 2 / 1 |
| «Dinosaur» | 5 Kurzarm-Bodys + 5 Jogginghosen | CHF 42.90 | +17.18 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063610711) | 2 / 2 / 2 |
| «Little One» | 5 Langarm-Bodys + 3 Mulltücher grün | CHF 44.90 | +17.35 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063676247) | 2 / 2 / 1 |
| «I like flying» | 3 Langarm-Bodys + 5 Leggings | CHF 39.90 | +16.58 | [Produkt](https://admin.shopify.com/store/sunnozy/products/11293063741783) | 2 / 2 / 2 |

\* pro Bestellung einer Box, vor Werbung. Rechnung: `strategie/preiskalkulation-weihnachtsbox.md`.

**In Shopify angelegt (19.10.2026):** Status **Entwurf**, Typ «Geschenkbox», Hersteller sunnozy, Grössen 0–3 / 3–6 / 6–9 Monate, SKU `SNZ-XBOX-<BOX>-<GRÖSSE>`, Lager wird gezählt. Bilder: 1. Hauptbild 2048 px (Logo oben links), 2. Foto der Box. Beschreibung mit Inhalt, Verpackung, Material, Versand.

## Dateien

| Ordner | Was | Wo |
|---|---|---|
| `fotos/` | Box-Fotos ohne Text, 1136 × 1408 | Posts, Shop-Zusatzbild |
| `shopify/` | Hauptbilder 2048 × 2048 | Shopify (bereits hochgeladen) |
| `4x5/` | Anzeigen 1080 × 1350 + `alle_boxen_4x5.jpg` | Meta-Feed, Pinterest |
| `1x1/` | Anzeigen 1080 × 1080 | Meta-Karussell |
| `9x16/` | Anzeigen 1080 × 1920 | Storys, Reels |
| `karte/` | Weihnachtskarte (Anhänger 60 × 100 mm): `karte_druck.pdf` (2 Seiten, 3 mm Beschnitt), PNGs, `karte_vorschau.jpg` | Druckerei, in jede Box |

Neu erzeugen:
- Anzeigen und Hauptbilder: `python3 tools/make_weihnachtsbox.py posts/kampagne-weihnachtsbox/fotos posts/kampagne-weihnachtsbox` (Preise in `BOXEN`)
- Karte: `python3 tools/make_weihnachtskarte.py posts/kampagne-weihnachtsbox/karte` (zweites Argument ändert den Gruss, z.B. `"Frohe\nWeihnachten"`)

## Meta-Anzeigen

**Kampagne:** «Das schönste Hallo – Weihnachten», Ziel Umsatz, ab Anfang November bis zum letzten Bestelltermin, CHF 5–10/Tag zusätzlich zu «Alles drin». Advantage+-Zielgruppe, Schweiz, Vorschlag 25–65.
**Anzeige A:** Karussell mit den 8 Boxen (`1x1/`), Link je Karte auf das Produkt.
**Anzeige B:** Einzelbild «Mum Dad Me» oder «Dino» (`4x5/` + `9x16/`).
**Anzeige C:** Übersicht `4x5/alle_boxen_4x5.jpg`, Link auf eine Kollektion «Weihnachts-Geschenkboxen».

**Primärtext (Varianten):**
> Das schönste Hallo unterm Baum. Ganze Sets aus weicher Baumwolle, von Hand verpackt, mit Weihnachtskarte. Fürs Gottikind, Grosskind und alle Kleinen.

> Noch kein Geschenk fürs Gottikind? Unsere Weihnachts-Geschenkboxen sind fertig verpackt und in 2–3 Werktagen bei Dir. Ab CHF 29.90.

> Zwei Gottikinder? Mit zwei Boxen ist der Versand gratis.

**Überschrift:** «Weihnachts-Geschenkbox «Name»» · **Beschreibung:** «Fertig verpackt, mit Karte» · **Button:** «Jetzt einkaufen»

## Vor dem Freischalten prüfen

- [ ] Produkte in Shopify ansehen und auf **Aktiv** stellen; Kollektion «Weihnachts-Geschenkboxen» anlegen (ich kann das übernehmen).
- [ ] **Lager ist nicht verknüpft:** Wird eine Box verkauft, sinkt der Bestand der Einzel-Sets nicht automatisch. Bestand bewusst klein gehalten (2 pro Grösse). Nach jedem Box-Verkauf die Sets von Hand abbuchen, oder die kostenlose App **Shopify Bundles** nutzen, die das automatisch macht.
- [ ] KI-Bilder: Prints und Farben mit den echten Sets vergleichen. Bei Meta und Instagram «Mit KI erstellt» setzen.
- [ ] Box-Material (Karton, Seidenpapier, Satinband, Karte) einkaufen; Kosten in der Preiskalkulation nachtragen (Annahme CHF 1.50).
- [ ] Karte drucken lassen (`karte/karte_druck.pdf`, Anhängerform mit Loch stanzen lassen).
- [ ] Letzten Bestelltermin für Weihnachten festlegen und in Shop und Anzeigen nennen.
