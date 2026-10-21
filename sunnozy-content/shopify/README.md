# Neue Produkte aus der Katalogliste (Oktober 2026)

38 Produkte aus der Produktliste (Google Sheet), angelegt mit `tools/shopify_neue_produkte.py`.
35 sind aktiv und im Onlineshop. 3 sind Entwürfe ohne Bild, weil es bisher nur kleine Katalogfotos gibt.
Die drei Sets, die schon im Shop waren, sind nicht doppelt angelegt: Teddybär creme, Princess und Little and Loved.

## Preiskalkulation

| Posten | Betrag |
|---|---|
| Fracht | CHF 1'000 |
| Lager 77 € (Kurs 0.94) | CHF 72 |
| Ads CHF 20 pro Tag × 30 Tage | CHF 600 |
| GTIN: 90 Varianten = 9 Pakete à CHF 54 | CHF 486 |
| **Fixkosten total** | **CHF 2'158** |

- Einkaufspreis in CNY × 0.112 = EK in CHF
- Die Fixkosten werden nach Warenwert verteilt: Warenwert gesamt CHF 3'006 bei 557 Stück. Jedes Set trägt also EK × 0.72 dazu.
- Verkaufspreis = (EK + Fixkostenanteil) × 2.5 + Shopify-Gebühr (2.9 % + CHF 0.30). Gerundet auf ,90.

Manuell gesetzt (Wunsch Inhaberin): Erstausstattung 3-teilig CHF 15.90, 5-teilig CHF 20.90.

Die Kalkulation steckt in `tools/shopify_neue_produkte.py` (`preis()`). Mit anderem Faktor oder anderen Kursen dort anpassen und neu erzeugen.

## Kollektionen und Menü

| Kollektion | Handle | Regel |
|---|---|---|
| Erstausstattung für Mädchen | `erstausstattung-maedchen` | Tag `mädchen-erstausstattung` |
| Erstausstattung für Jungen | `erstausstattung-junge` | Tag `junge-erstausstattung` |
| Strampler-Sets | `strampler-sets` | Produkttyp `Strampler-Set` |
| Mützen | `accessoires-muetzen` | Tag `mütze` |
| Halstücher | `accessoires-halstuecher` | Tag `Halstücher` |
| Söckchen | `accessoires-soeckchen` | Tag `Söckchen` |
| Lätzchen-Sets | `accessoires-laetzchen` | Tag `Lätzchen` |

Unisex-Sets haben beide Tags und erscheinen deshalb in beiden Unterkategorien. Die 6 bestehenden Erstausstattungs-Sets haben die Tags ebenfalls bekommen.

Im Footer zeigt «Sortiment» auf `unser-sortiment-108` (wie `unser-sortiment-geschenkboxen`, plus Strampler-Sets).

Das neue Menü `main-menu-108` ist eine Kopie von `main-menu-geschenkboxen` mit drei Änderungen:
- Erstausstattung hat ein Untermenü: Für Mädchen, Für Jungen (ein Klick auf Erstausstattung zeigt alle)
- Neuer Tab Strampler-Sets direkt danach
- Accessoires hat ein Untermenü: Mützen, Halstücher, Söckchen, Lätzchen-Sets

Das Theme **«sunnozy FINAL 108 – Neue Produkte & Menü»** ist eine Kopie des Live-Themes. Dort zeigt der Header auf `main-menu-108`. Das Live-Theme bleibt unverändert, bis Du 108 veröffentlichst.

## Produkte

| Typ | Produkt | Preis CHF | Grössen | Bilder | Für | Status | Produkt-ID |
|---|---|---|---|---|---|---|---|
| Accessoires | [Baby-Knotenmützen 3er-Set «Bär» – Braun, Gestreift & Creme](https://sunnozy.ch/products/baby-knotenmuetzen-3er-set-baer) | 7.90 | 1 | 0 | Unisex | Entwurf | 11303451165015 |
| Accessoires | [Baby-Mützen 3er-Set «Schleifen» – Beere, Altrosa & Creme](https://sunnozy.ch/products/baby-muetzen-3er-set-schleifen) | 5.90 | 1 | 2 | Mädchen | aktiv | 11303451885911 |
| Accessoires | [Turban-Mützen 3er-Set mit Knotenschleife – Beere, Altrosa & Creme](https://sunnozy.ch/products/turban-muetzen-3er-set-schleife) | 7.90 | 1 | 4 | Mädchen | aktiv | 11303497105751 |
| Erstausstattungs-Set | [Erstausstattung-Set «Bauernhof» – Creme, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-bauernhof) | 30.90 | 2 | 9 | Unisex | aktiv | 11303453098327 |
| Erstausstattungs-Set | [Erstausstattung-Set «Beautiful» Gänseblümchen – Apricot, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-beautiful-gaensebluemchen) | 15.90 | 2 | 4 | Mädchen | aktiv | 11303453950295 |
| Erstausstattungs-Set | [Erstausstattung-Set «Best Family» Teddy – Beige & Creme, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-best-family-teddy) | 30.90 | 2 | 9 | Unisex | aktiv | 11303455916375 |
| Erstausstattungs-Set | [Erstausstattung-Set «Blumenwiese» Musselin – 3-teilig mit Haarband](https://sunnozy.ch/products/erstausstattung-set-blumenwiese-musselin) | 15.90 | 2 | 2 | Mädchen | aktiv | 11303456276823 |
| Erstausstattungs-Set | [Erstausstattung-Set «Born in 2027» – Hellblau, 6-teilig](https://sunnozy.ch/products/erstausstattung-set-born-in-2027-blau) | 26.90 | 2 | 0 | Junge | Entwurf | 11303456801111 |
| Erstausstattungs-Set | [Erstausstattung-Set «Born in 2027» – Rosa, 6-teilig](https://sunnozy.ch/products/erstausstattung-set-born-in-2027-rosa) | 26.90 | 2 | 4 | Mädchen | aktiv | 11303457685847 |
| Erstausstattungs-Set | [Erstausstattung-Set «Cool Dude» Dino – Creme, 6-teilig](https://sunnozy.ch/products/erstausstattung-set-dino-cool-dude) | 26.90 | 2 | 6 | Junge | aktiv | 11303458865495 |
| Erstausstattungs-Set | [Erstausstattung-Set «Dream big» Heissluftballon – Weiss & Beige, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-dream-big-heissluftballon) | 15.90 | 2 | 2 | Unisex | aktiv | 11303460077911 |
| Erstausstattungs-Set | [Erstausstattung-Set «Eisbär» – Taupe, 5-teilig](https://sunnozy.ch/products/erstausstattung-set-eisbaer-taupe) | 20.90 | 2 | 5 | Unisex | aktiv | 11303464173911 |
| Erstausstattungs-Set | [Erstausstattung-Set «Hase» – Rosa, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-hase-rosa) | 30.90 | 2 | 9 | Mädchen | aktiv | 11303469252951 |
| Erstausstattungs-Set | [Erstausstattung-Set «I love Dogs» – Creme, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-i-love-dogs) | 30.90 | 2 | 9 | Unisex | aktiv | 11303472955735 |
| Erstausstattungs-Set | [Erstausstattung-Set «I love you Dad» – Hellblau, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-i-love-you-dad) | 15.90 | 2 | 2 | Junge | aktiv | 11303474004311 |
| Erstausstattungs-Set | [Erstausstattung-Set «I ♥ Dad Mom» – Weiss, 6-teilig](https://sunnozy.ch/products/erstausstattung-set-i-love-dad-mom) | 26.90 | 2 | 7 | Unisex | aktiv | 11303470563671 |
| Erstausstattungs-Set | [Erstausstattung-Set «It's a baby girl» Gänseblümchen – Apricot, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-gaensebluemchen) | 30.90 | 2 | 9 | Mädchen | aktiv | 11303465845079 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little Bear» gerippt – Hafer, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-gerippt-beige-baer) | 15.90 | 2 | 1 | Unisex | aktiv | 11303466565975 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little Bear» – Rosa, 5-teilig](https://sunnozy.ch/products/erstausstattung-set-little-bear-rosa) | 20.90 | 2 | 5 | Mädchen | aktiv | 11303475708247 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little One» Weltall – Hellblau, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-weltall-3-teilig) | 15.90 | 2 | 4 | Junge | aktiv | 11303485178199 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little One» Weltall – Hellblau, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-weltall-little-one) | 30.90 | 2 | 1 | Junge | aktiv | 11303486062935 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little Princess» Krone – Rosa & Creme, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-little-princess-krone) | 30.90 | 2 | 9 | Mädchen | aktiv | 11303477641559 |
| Erstausstattungs-Set | [Erstausstattung-Set «Little Princess» – Rosa, 3-teilig](https://sunnozy.ch/products/erstausstattung-set-little-princess-wickelbody) | 15.90 | 2 | 2 | Mädchen | aktiv | 11303478460759 |
| Erstausstattungs-Set | [Erstausstattung-Set «Smile» – Salbeigrün, 3-teilig mit Kapuzentuch](https://sunnozy.ch/products/erstausstattung-set-smile-salbeigruen) | 15.90 | 2 | 4 | Unisex | aktiv | 11303479705943 |
| Erstausstattungs-Set | [Erstausstattung-Set «Waldbär» – Creme, 5-teilig](https://sunnozy.ch/products/erstausstattung-set-waldbaer-creme) | 20.90 | 2 | 5 | Unisex | aktiv | 11303483933015 |
| Erstausstattungs-Set | [Erstausstattung-Set «Wal» – Hellblau, 8-teilig](https://sunnozy.ch/products/erstausstattung-set-wal-blau) | 30.90 | 2 | 9 | Junge | aktiv | 11303482556759 |
| Erstausstattungs-Set | [Erstausstattung-Set «little and cute» Hase – Lila, 6-teilig](https://sunnozy.ch/products/erstausstattung-set-hase-lila) | 26.90 | 2 | 7 | Mädchen | aktiv | 11303467974999 |
| Hosen-Set | [Baby-Hosen 3er-Set «Bären» – Beige, Braun & Weiss](https://sunnozy.ch/products/baby-hosen-3er-set-baeren) | 13.90 | 3 | 4 | Unisex | aktiv | 11303449887063 |
| Hosen-Set | [Baby-Hosen 3er-Set «Herzen» – Creme, Altrosa & Rosa](https://sunnozy.ch/products/baby-hosen-3er-set-herzen) | 13.90 | 3 | 4 | Mädchen | aktiv | 11303450804567 |
| Strampler-Set | [Strampler 3er-Set «Avocado» – Grün & Weiss](https://sunnozy.ch/products/strampler-3er-set-avocado) | 25.90 | 3 | 0 | Unisex | Entwurf | 11303486816599 |
| Strampler-Set | [Strampler 3er-Set «Kirschen» – Weinrot, Altrosa & Weiss](https://sunnozy.ch/products/strampler-3er-set-kirschen) | 25.90 | 3 | 4 | Mädchen | aktiv | 11303488061783 |
| Strampler-Set | [Strampler 3er-Set «Little Princess» – Rosa & Creme](https://sunnozy.ch/products/strampler-3er-set-little-princess) | 25.90 | 3 | 4 | Mädchen | aktiv | 11303489438039 |
| Strampler-Set | [Strampler 3er-Set «Naturtöne» – Salbei, Creme & Beige](https://sunnozy.ch/products/strampler-3er-set-naturtoene) | 25.90 | 3 | 1 | Unisex | aktiv | 11303491141975 |
| Strampler-Set | [Strampler 3er-Set «Segelboote» – Creme & Blau](https://sunnozy.ch/products/strampler-3er-set-segelboote) | 25.90 | 3 | 4 | Junge | aktiv | 11303440253271 |
| Strampler-Set | [Strampler 3er-Set «Waldtiere» – Himbeer & Weiss](https://sunnozy.ch/products/strampler-3er-set-waldtiere) | 25.90 | 3 | 4 | Mädchen | aktiv | 11303492387159 |
| Strampler-Set | [Strampler-Set «Blumen & Hase» – 2 Strampler mit Haarband](https://sunnozy.ch/products/strampler-set-blumen-hase) | 19.90 | 3 | 4 | Mädchen | aktiv | 11303493730647 |
| Strampler-Set | [Strampler-Set «Kätzchen & Tulpen» – 2 Strampler mit Mütze](https://sunnozy.ch/products/strampler-set-kaetzchen-tulpen) | 19.90 | 3 | 4 | Mädchen | aktiv | 11303494811991 |
| Strampler-Set | [Strampler-Set «Sweet Home» – 2 Strampler mit Mütze](https://sunnozy.ch/products/strampler-set-sweet-home) | 19.90 | 3 | 4 | Unisex | aktiv | 11303495991639 |

## Offen

- **Entwürfe ohne Bild:** Knotenmützen «Bär», Born in 2027 Hellblau und Strampler «Avocado». Sie gehen online, sobald es Bilder gibt.
- **Einzelteile fehlen teilweise:** Bei einigen Sets gibt es nur das Hauptbild oder das Weissbild (siehe `posts/coming-soon/EINZELTEILE_OFFEN.md`).
- **KI-Bilder vor dem Verkauf mit der echten Ware vergleichen:** Anzahl Teile, Prints und Farben.
- **Weitere Verkaufskanäle:** Shop, Google & YouTube, Facebook & Instagram und Pinterest sind noch nicht aktiviert. Das geht in Shopify unter Produkte → Mehrfachauswahl → Verkaufskanäle.
