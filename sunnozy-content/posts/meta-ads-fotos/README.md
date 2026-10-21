# Meta-Anzeigenbilder (Instagram & Facebook)

Alle Bilder für die Kampagne «Alles drin» (siehe `strategie/sunnozy-werbeplan.html`), nach Format sortiert. Es sind nur Produktbilder (Shop-Hauptbilder), keine KI-Babys. Preise und Teile stammen aus Shopify, Stand 17.10.2026.

**Update 18.10.2026:** Next-Stil, Checkliste und Geschenk sind neu aus den Shop-Hauptbildern im ChatGPT-Stil gebaut (`posts/shopify-hauptbilder-praesentation-hd/bilder/`): warmer Studio-Grund, Holzbügel, Set deutlich grösser. Im Next-Stil läuft das Bild randlos, bei Checkliste und Geschenk sitzt es als Fotokachel mit runden Ecken. Das eingebrannte Logo der Hauptbilder ist übermalt. «Alles drin» (Teile als Kacheln) bleibt unverändert, weil es aus den Einzelteilen gebaut ist.

| Ordner | Format | Wo bei Meta |
|---|---|---|
| `1x1/` | 1080 × 1080 | Feed, **Karussell** (Pflicht 1:1) |
| `4x5/` | 1080 × 1350 | Feed (grösste Fläche im Feed) |
| `9x16/` | 1080 × 1920 | Storys und Reels |

Tipp: In Meta kannst Du pro Anzeige mehrere Formate hinterlegen («Platzierungen anpassen»). Dann nimm das 4:5-Bild für den Feed und das 9:16-Bild für Storys und Reels. Dasselbe Motiv sollte in beiden Formaten laufen.

## Motive

| Motiv | Für wen | Dateien | Sets |
|---|---|---|---|
| **Next-Stil** (Preis-Etikett, Logo senkrecht) | alle | `karussell_*` (1:1, 4:5), `story_*` (9:16) | alle 6 |
| **Alles drin** (alle Teile als Kacheln) | werdende Eltern | `foto_alles_drin_*` (4:5) | alle 6 |
| **Erstausstattung? Erledigt.** (Checkliste) | werdende Eltern | `checkliste_*` (1:1, 4:5, 9:16) | Teddybär, Princess, Little and Loved, Hello World |
| **Das schönste Hallo** (Rosé) | Schenkende | `geschenk_*` (1:1, 4:5, 9:16) | Teddybär, Princess, Little and Loved, Hello World |

## So testen

1. **Kampagne «Alles drin»:** Die drei Anzeigen aus dem Werbeplan sind das Karussell (Next-Stil 1:1) und die zwei Reels.
2. **Ab Woche 2 dazu:** eine Anzeige «Checkliste» (4:5 + 9:16, Set Princess) und eine Anzeige «Geschenk» (4:5 + 9:16, Set Teddybär). Nach 7 Tagen die günstigste behalten.
3. Pro Woche höchstens 1–2 neue Anzeigen einschalten, damit Meta weiterlernen kann.

**Texte:**
- **Checkliste:** «Strampler, Body, Mützchen und mehr: Diese Erstausstattung hat alles für die ersten Wochen. Gratisversand in der Schweiz ab CHF 50.» · Überschrift: «Erstausstattung? Erledigt.»
- **Geschenk:** «Das schönste Geschenk zur Geburt: eine komplette Erstausstattung, in 2–3 Werktagen geliefert.» · Überschrift: «Das schönste Hallo»

## Bitte beachten

- **Lager:** «Hello» Rosa und «Hello Little Bear» haben nur 2 Stück. Diese Bilder erst nach dem Nachbestellen schalten.
- **Preise:** Ändert sich ein Preis, müssen die Bilder neu erzeugt werden:
  - `python3 tools/make_meta_fotos.py posts/meta-ads-fotos` (Checkliste, Geschenk)
  - `python3 tools/make_meta_ads.py posts/shopify-hauptbilder-praesentation-hd/bilder <ordner> --4x5` (Next-Stil 1:1, 4:5, 9:16; danach in `1x1/`, `4x5/`, `9x16/` verschieben)
  - `tools/make_alles_drin.py` (Alles drin)
- **Geschenkverpackung:** Die Geschenk-Anzeigen versprechen keine Geschenkverpackung. Erst erwähnen, wenn Du sie im Shop anbietest.

`uebersicht.jpg` zeigt alle Motive am Beispiel Princess und Teddybär.
