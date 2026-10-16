# Meta-Anzeigen Erstausstattung (Facebook & Instagram, Stil Next)

## Vorbild (Next, Karussell-Anzeige)

| Element | Vorbild | sunnozy |
|---|---|---|
| Produkt | Cardigan am Holzbügel, ruhiger Grund, gross links | Set-Präsentation am Holzbügel, weisser Grund (Shop-Hauptbild, aufbereitet) |
| Preis | schwarzes Etikett oben links «CHF13» | «CHF 30.40» usw. (Preise aus Shopify) |
| Marke | Wortmarke senkrecht im hellgrauen Feld rechts | sunnozy-Logo senkrecht |
| Versprechen | «FREE DELIVERY & DUTIES PAID» | «GRATISVERSAND AB CHF 50» (Versandregel Schweiz in Shopify) |
| Kleingedrucktes | «T&Cs apply» | «Versand in 2–3 Werktagen» (Standardversand Schweiz) |
| Unter der Karte | Produktname + «Shop now» (von Meta) | Überschrift + «Jetzt einkaufen» (in Meta eintragen, siehe unten) |

## Dateien

| Set | Preis | Lager | Karussell 1:1 | Story/Reels 9:16 |
|---|---|---|---|---|
| Teddybär, Creme, 8-teilig | CHF 30.40 | 6 | `karussell_teddybaer_1x1.jpg` | `story_teddybaer_9x16.jpg` |
| Princess, Rosa, 8-teilig | CHF 30.40 | 8 | `karussell_princess_1x1.jpg` | `story_princess_9x16.jpg` |
| Little and Loved, Rosa Enten, 8-teilig | CHF 30.40 | 8 | `karussell_little_and_loved_1x1.jpg` | `story_little_and_loved_9x16.jpg` |
| Hello World, Creme, 8-teilig | CHF 29.40 | 10 | `karussell_hello_world_1x1.jpg` | `story_hello_world_9x16.jpg` |
| Hello, Rosa mit Spitze, 6-teilig | CHF 30.40 | **2** | `karussell_hello_rosa_1x1.jpg` | `story_hello_rosa_9x16.jpg` |
| Hello Little Bear, Creme, 5-teilig | CHF 28.40 | **2** | `karussell_hello_little_bear_1x1.jpg` | `story_hello_little_bear_9x16.jpg` |

«Hello» und «Hello Little Bear» haben nur noch 2 Stück. Diese Karten besser erst nach dem Nachbestellen schalten (oder an den Schluss des Karussells).

Preise ändern? In `tools/make_meta_ads.py` (`SETS`) anpassen und neu erzeugen:
`python3 tools/make_meta_ads.py posts/meta-ads-erstausstattung/quelle posts/meta-ads-erstausstattung`

## Texte für den Werbeanzeigenmanager

**Format:** Karussell, 6 Karten (1:1). Für Stories/Reels pro Karte das 9:16-Bild als Platzierungs-Variante hinterlegen.

**Primärer Text** (über der Anzeige):
> Alles für die ersten Wochen, mit einem Klick 🧸 Erstausstattungs-Sets, liebevoll aufeinander abgestimmt. Gratisversand in der ganzen Schweiz ab CHF 50.

Alternativen zum Testen:
> Das perfekte Geschenk zur Geburt 🎁 Komplette Erstausstattung ab CHF 28.40, schnell geliefert in 2–3 Werktagen.

> Baby unterwegs? 👶 Diese Sets haben alles, was ein Neugeborenes braucht, von Strampler bis Mützchen.

**Pro Karte**

| Karte | Überschrift | Beschreibung | Link |
|---|---|---|---|
| Teddybär | Erstausstattung «Teddybär» – 8-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-teddybaer |
| Princess | Erstausstattung «Princess» – 8-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-princess |
| Little and Loved | Erstausstattung «Little and Loved» – 8-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-little-and-loved |
| Hello World | Erstausstattung «Hello World» – 8-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-hello-world |
| Hello Rosa | Erstausstattung «Hello» mit Spitze – 6-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-hello-spitze |
| Hello Little Bear | Erstausstattung «Hello Little Bear» – 5-teilig | Gratisversand ab CHF 50 | https://sunnozy.ch/products/erstausstattung-set-hello-little-bear |

**Call-to-Action:** «Jetzt einkaufen»

**Zielgruppe (Vorschlag):** Schweiz, Frauen und Männer 24–42, Interessen Schwangerschaft, Babyausstattung, Babyparty, Geburt. Zusätzlich «Freunde von Eltern» für Geschenke.

**Hinweis:** Die Bilder sind die Shop-Präsentationen (teils KI-unterstützt erstellt). Meta verlangt keine KI-Kennzeichnung für normale Produktbilder; die Preise müssen aber mit dem Shop übereinstimmen. Bitte vor dem Schalten kurz prüfen.

Erstellt mit `tools/make_meta_ads.py`.
