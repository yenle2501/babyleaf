# Kampagne «Weihnachts-Geschenkbox»

Für Schenkende (Gotti, Götti, Grosseltern, Freundinnen), passend zur Kampagne «Das schönste Hallo» aus dem Markenplan. In jeder Box liegt ein **ganzes Set** aus dem Shop (Body-Set + Hosen-Set, + Halstücher oder + Mulltücher), jedes Teil gefaltet und mit Satinband gebunden, dazu die Weihnachtskarte.

Darstellung nach den Vorbildern der Nutzerin: Box von oben, randvoll und von Hand gepackt (Instagram-«Baby Box»-Stil), Karte oben in der Box. Die Fotos sind mit Canva-KI erzeugt aus: Box-Foto der Nutzerin (`vorlage_geschenkbox.jpg`), den Shop-Bildern der Sets und der Karte.

## Check: die acht Boxen

| Box | Inhalt | Preis | Gewinn* | Shopify-ID (Entwurf, in Admin unter Produkte → Typ «Geschenkbox») | Lager je Grösse |
|---|---|---|---|---|---|
| «Mum Dad Me» | 5 Langarm-Bodys + 5 Leggings | CHF 42.90 | +16.45 | ID 11293061054807 | 2 / 2 / 2 |
| «Lovely Little Girl» | 3 Langarm-Bodys + 5 Leggings | CHF 39.90 | +16.58 | ID 11293063250263 | 2 / 2 / 2 |
| «Growing up strong» | 5 Kurzarm-Bodys + 5 Jogginghosen | CHF 42.90 | +17.18 | ID 11293063348567 | 2 / 2 / 2 |
| «I love my Mummy» | 3 Langarm-Bodys + 3 Halstücher | CHF 29.90 | +13.00 | ID 11293063414103 | 2 / 2 / 1 |
| «Dino» | 3 Langarm-Bodys + 3 Mulltücher blau | CHF 39.90 | +15.53 | ID 11293063512407 | 2 / 2 / 1 |
| «Dinosaur» | 5 Kurzarm-Bodys + 5 Jogginghosen | CHF 42.90 | +17.18 | ID 11293063610711 | 2 / 2 / 2 |
| «Little One» | 5 Langarm-Bodys + 3 Mulltücher grün | CHF 44.90 | +17.35 | ID 11293063676247 | 2 / 2 / 1 |
| «I like flying» | 3 Langarm-Bodys + 5 Leggings | CHF 39.90 | +16.58 | ID 11293063741783 | 2 / 2 / 2 |

\* pro Bestellung einer Box, vor Werbung. Rechnung: `strategie/preiskalkulation-weihnachtsbox.md`.

**In Shopify angelegt (19.10.2026):** Status **Entwurf**, Typ «Geschenkbox», Hersteller sunnozy, Grössen 0–3 / 3–6 / 6–9 Monate, SKU `SNZ-XBOX-<BOX>-<GRÖSSE>`, Lager wird gezählt. Bilder: 1. Hauptbild 2048 px (Logo oben links), 2. Foto der Box. Beschreibung mit Inhalt, Verpackung, Material, Versand.

## Shopify: Tab «Geschenkboxen» und personalisierte Box (19.10.2026)

| Was | Stand |
|---|---|
| Kollektion **«Geschenkboxen»** (`/collections/geschenkboxen`) | angelegt, im Onlineshop freigegeben, enthält die 8 Boxen + die personalisierte Box (alle noch **Entwurf**, deshalb für Kundinnen noch leer) |
| Produkt **«Personalisierte Geschenkbox»** (`/products/personalisierte-geschenkbox`, ID 11293187211607) | Entwurf, CHF 15 (Box, Seidenpapier, Karte, Einpacken), Lager nicht gezählt, Vorlage `geschenkbox-personalisiert` |
| Kollektion **«Geschenkbox Auswahl»** (`geschenkbox-auswahl`) | automatisch: alle Body-Sets, Hosen-Sets, Mulltücher und Halstücher-3er-Sets; liefert die Auswahl im Konfigurator |
| Menü **«Hauptmenü mit Geschenkboxen»** (`main-menu-geschenkboxen`) | neu: Geschenkboxen + alle bisherigen Tabs. Das Live-Menü `main-menu` ist **unverändert**. |
| Theme **FINAL 107** (unveröffentlicht) | Header nutzt das neue Menü; neue Vorlage `templates/product.geschenkbox-personalisiert.json` und `snippets/bl-geschenkbox-konfigurator.liquid` (Kopie in `theme/`) |

**So funktioniert die personalisierte Box:** Die Kundin hakt Sets an und wählt pro Set die Grösse (nur verfügbare). Danach wählt sie, ob die Weihnachtskarte beiliegt (inklusive), und gibt Name und Wunschtext ein (max. 200 Zeichen). Der Total-Preis rechnet live: gewählte Sets + CHF 15. «Box in den Warenkorb» legt alle Sets **und** die Box in den Warenkorb. Die Box trägt die Eigenschaften Inhalt, Karte, Name und Wunschtext; diese erscheinen in der Bestellung. Alle Teile einer Box haben dieselbe versteckte Nummer `_Geschenkbox`. Der Lagerbestand der Sets wird normal abgebucht.

**Live gehen (Reihenfolge):**
1. FINAL 107 in der Vorschau prüfen: Tab, Kollektion und die personalisierte Box. Dafür die Box kurz auf «Aktiv» stellen, sonst ist sie in der Vorschau nicht sichtbar.
2. FINAL 107 veröffentlichen. Erst dann gibt es den Tab und den Konfigurator; im heutigen Live-Theme FINAL 106 hätte die Box keinen Konfigurator.
3. Die 9 Geschenkbox-Produkte auf «Aktiv» stellen.

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

## Newsletter-Pop-up «Willkommensgeschenk» (Theme FINAL 107, noch nicht live)

Vorbild oykami.ch. Datei `theme/snippets/bl-newsletter-popup.liquid`, eingebunden in `layout/theme.liquid` von FINAL 107
(`{% render 'bl-newsletter-popup' %}` nach `whatsapp-bubble`, nicht im Theme-Editor). Vorschau: `theme/popup_vorschau_*.png`.

- Titel «Für Dich – ein kleines Willkommensgeschenk ♡», Felder Vorname und E-Mail, Knopf «Jetzt 10 % Gutschein abholen»,
  «Nein danke, im Moment nicht», X oben rechts, Hinweis «Abmeldung jederzeit möglich» mit Link zur Datenschutzerklärung.
- Anmeldung über das Shopify-Kundenformular: Kundin mit Marketing-Einwilligung, Tags `newsletter`, `popup-willkommen`.
- Danach zeigt das Pop-up den Code **WILLKOMMEN10** (10 % auf die erste Bestellung, einmal pro Kundin, aktiv in Shopify) mit «Kopieren».
- Erscheint nach 8 Sekunden, aber erst wenn das Cookie-Banner weg ist. Nicht im Warenkorb, Konto und Login, nicht für
  eingeloggte Abonnentinnen. «Nein danke», X oder Esc: 14 Tage Ruhe. Nach der Anmeldung nie mehr.
- Geht mit FINAL 107 live. Testen: https://sunnozy.ch/?preview_theme_id=207454601559 (neues privates Fenster).
- Tipp: In Shopify Messaging eine Willkommens-E-Mail mit dem Code für Kundinnen mit Tag `popup-willkommen` einrichten.

## Bewertungen (Judge.me) unter Preis (Theme FINAL 107, noch nicht live)

Neues Snippet `theme/snippets/bl-bewertungen-kurz.liquid`, als Block «Bewertungen kurz (unter Preis)» in der Gruppe «Header»
von `templates/product.json` (nach Preis und Versandinfo, vor Grösse und Warenkorb). Zeigt bis zu 3 Judge.me-Bewertungen
als Karten (Handy: seitlich wischen) und «Alle N Bewertungen lesen», das zum ausführlichen Bewertungs-Abschnitt unten springt.
Ohne Bewertungen erscheint nichts. Vorschau: `theme/bewertungen_vorschau_*.png`.
