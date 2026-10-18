# Kampagne «Weihnachts-Geschenkbox»

Für Schenkende (Gotti, Götti, Grosseltern, Freundinnen), passend zur Kampagne «Das schönste Hallo» aus dem Markenplan. In jeder Box liegt ein **ganzes Set** aus dem Shop, alle Teile sichtbar: Body-Set + Hosen-Set bzw. Body-Set + Halstücher. Box: rosa Versandkarton (Vorlage `vorlage_geschenkbox.jpg`).

Vorbild: Pinterest «Weihnachten Geschenkbox Baby»: offene Box mit Seidenpapier, Inhalt ordentlich gefaltet und gerollt, Tannenzweige, Zapfen, Kugeln, Lichterkette, Geschenkanhänger.

## Die vier Boxen

| Box | Inhalt | Shop-Produkte | Shop-Preis heute (Stand 17.10.) |
|---|---|---|---|
| «Mum Dad Me» | 5 Langarm-Bodys + 5 Leggings | Kombi-Set Mum Dad Me | CHF 32.10 |
| «Lovely Little Girl» | 3 Langarm-Bodys + 5 Leggings | Kombi-Set Lovely Little Girl | CHF 29.70 |
| «Growing up strong» | 5 Kurzarm-Bodys + 5 Jogginghosen | Kombi-Set Growing up strong | CHF 32.10 |
| «I love my Mummy» | 3 Langarm-Bodys + 3 Halstücher | Body-Set 3er + Halstücher 3er | CHF 14.30 + 7.99 |

**Preis der Box:** noch offen (Box, Seidenpapier, Karte kommen dazu). Sobald er feststeht, in `tools/make_weihnachtsbox.py` bei `PREIS` eintragen und neu erzeugen; dann steht der Preis in der Inhaltszeile.

## Dateien

| Ordner | Format | Wo |
|---|---|---|
| `4x5/` | 1080 × 1350 | Feed (Meta, Instagram), Pinterest |
| `1x1/` | 1080 × 1080 | Karussell-Anzeige (Meta) |
| `9x16/` | 1080 × 1920 | Storys, Reels |
| `ki-roh/` | 1136 × 1408 | Fotos ohne Text (auch für Posts, Shop-Produktbild) |

`alle_boxen_*` zeigt alle vier Boxen im Raster (Kollektions-Anzeige). `uebersicht.jpg` zeigt alle 4:5-Bilder.

Neu erzeugen: `python3 tools/make_weihnachtsbox.py posts/kampagne-weihnachtsbox/ki-roh posts/kampagne-weihnachtsbox`

## Anzeigentexte

**Primärtext (Varianten zum Testen):**
> Das schönste Hallo unterm Baum. Weiche Body- und Hosen-Sets aus Baumwolle, fertig verpackt in der Geschenkbox. Perfekt fürs Gottikind oder Grosskind.

> Noch kein Geschenk fürs Gottikind? Unsere Weihnachts-Geschenkbox hat alles drin: 5 Bodys und 5 Hosen, schön verpackt, in 2–3 Werktagen bei Dir.

> Geschenk gesucht, das sicher gebraucht wird? Babykleidung aus 100 % Baumwolle in der rosa Geschenkbox, bereit zum Verschenken.

**Überschrift pro Karte:** «Geschenkbox Mum Dad Me» · «Geschenkbox Lovely Little Girl» · «Geschenkbox Growing up strong» · «Geschenkbox I love my Mummy»
**Beschreibung:** Fertig verpackt · Gratisversand ab CHF 50
**Button:** «Jetzt einkaufen»
**Zielgruppe (Vorschlag):** Schweiz, 25–65, Interessen Geschenke, Weihnachten, Familie; «Freunde von Eltern mit Neugeborenen». Advantage+ darf erweitern.
**Zeitraum:** ab Anfang November bis zum letzten Bestelltermin vor Weihnachten (Termin in Text und Anzeige nennen, sobald festgelegt).

## Bitte prüfen

- **KI-Bilder:** Box und Inhalt sind mit Canva-KI erzeugt (Vorlagen: Dein Box-Foto und die Shop-Bilder der Sets). Farben, Drucke und Anzahl mit den echten Sets vergleichen. In Meta und Instagram «Mit KI erstellt» bzw. KI-Info setzen.
- **Box im Shop:** Die Boxen gibt es noch nicht als Produkt. Vor dem Schalten als Produkt (oder Bundle) anlegen, Preis festlegen, Link je Karte eintragen.
- **Lager:** Genug Sets für die Boxen bereithalten, sonst Karte pausieren.
- «I love my Mummy»: Auf dem Bild sind 3 Bodys und 3 Halstücher, wie im Shop.
