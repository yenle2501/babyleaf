"""Neue Produkte aus der Lieferantenliste (Product_catalog_with_prices_mit_Fotos.xlsx) fuer Shopify vorbereiten.

Preis: Einkauf (CNY) + anteilige Fixkosten (Fracht 1000 CHF, Lager 77 EUR, Ads 20 CHF/Tag x 30 Tage,
GTIN 54 CHF je 10 Nummern), verteilt nach Warenwert; dann x 2.5 plus Zahlungsgebuehr (2.9 % + 0.30),
aufgerundet auf .90.
Bilder: Hauptbild + Einzelteile aus dem Repo (raw.githubusercontent.com), ohne Artikelnummern im Dateinamen.

Aufruf: python3 shopify_neue_produkte.py <ausgabeordner>  -> je Produkt <handle>.json (productSet-Input)
"""
import json, math, os, sys

RAW = 'https://raw.githubusercontent.com/yenle2501/babyleaf/claude/wizardly-hawking-e7rppg/sunnozy-content/posts/'
CS = 'coming-soon/'
PF = 'produktfotos-set-praesentation/mit_logo/'
ET = 'marktplatz-galaxus-amazon/einzelteile/'
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'posts')
CNY, EUR = 0.112, 0.94
FIX = 1000 + 77 * EUR + 20 * 30 + 9 * 54          # 9 Zehnerpakete GTIN fuer 90 Varianten
WARENWERT = 3006.0                                 # Summe Bestellmenge x Einkauf, 41 Artikel
ERST = 'gid://shopify/TaxonomyCategory/bt-2'       # Geschenksets fuer Babys

G = {'03': '0-3 Monate', '36': '3-6 Monate', '69': '6-9 Monate', 'NB': 'Neugeboren (50/56)', '06': '0-6 Monate'}
SKU = {'03': '0003', '36': '0306', '69': '0609', 'NB': 'NB', '06': '0006'}


def preis(ek_cny):
    ek = ek_cny * CNY
    kosten = ek + FIX * ek / WARENWERT
    p = (kosten * 2.5 + 0.30) / (1 - 0.029)
    return f'{math.floor(p) + 0.90:.2f}'


def et(ordner, namen):
    return [ordner + n for n in namen]


def cs_et(key):
    d = os.path.join(ROOT, CS, key, 'marktplatz', 'einzelteile')
    return [f'{CS}{key}/marktplatz/einzelteile/{f}' for f in sorted(os.listdir(d))] if os.path.isdir(d) else []


def pf_et(setname):
    d = os.path.join(ROOT, ET, setname)
    return [f'{ET}{setname}/{f}' for f in sorted(os.listdir(d)) if 'uebersicht' not in f]


def weiss(key):
    return [f'{CS}{key}/marktplatz/{key}_hauptbild_weiss.jpg']


# key, Titel, Handle, Typ, Geschlecht (m/j/u), Groessen {code: Menge}, EK CNY, Hauptbild, weitere Bilder,
# Einleitung, Teile, Farbe/Stil-Tags, Status
P = [
    # --- Accessoires
    ('muetzen-schleifen', 'Baby-Mützen 3er-Set «Schleifen» – Beere, Altrosa & Creme', 'baby-muetzen-3er-set-schleifen', 'Accessoires', 'm',
     {'06': 6}, 11, CS + 'muetzen-schleifen/shop/muetzen-schleifen_shop.jpg', weiss('muetzen-schleifen'),
     'Drei weiche Baumwollmützen mit Umschlag in zarten Rosatönen – mit verspielten Schleifen und Herzchen. Hält das Köpfchen warm und passt zu fast jedem Outfit.',
     ['1× Mütze Beere mit weissen Schleifen und Herzchen', '1× Mütze Altrosa mit grossen Schleifen', '1× Mütze Creme mit rosa Schleifen, Herzchen und Stoffschleife'],
     ['mütze', 'rosa', 'schleifen'], 'ACTIVE'),
    ('turban-muetzen', 'Turban-Mützen 3er-Set mit Knotenschleife – Beere, Altrosa & Creme', 'turban-muetzen-3er-set-schleife', 'Accessoires', 'm',
     {'06': 6}, 14, CS + 'turban-muetzen/shop/turban-muetzen_shop.jpg', cs_et('turban-muetzen'),
     'Drei süsse Turban-Mützen mit grosser Knotenschleife – der Hingucker für kleine Mädchen. Aus 100 % weicher Baumwolle, leicht dehnbar und angenehm auf der zarten Babyhaut.',
     ['1× Turban Beere mit Schleifen und Herzchen', '1× Turban Altrosa mit grossen Schleifen', '1× Turban Creme mit rosa Schleifen und Herzchen'],
     ['mütze', 'turban', 'rosa', 'schleifen'], 'ACTIVE'),
    ('muetzen-baer', 'Baby-Knotenmützen 3er-Set «Bär» – Braun, Gestreift & Creme', 'baby-knotenmuetzen-3er-set-baer', 'Accessoires', 'u',
     {'06': 6}, 14, None, [],
     'Drei kuschelige Knotenmützen in warmen Naturtönen – mit Bärchen-Etikett, feinen Streifen und Teddy-Print. Der Knoten lässt sich lösen, so wächst die Mütze ein Stück mit.',
     ['1× Knotenmütze Braun mit Bärchen-Etikett', '1× Knotenmütze Beige-weiss gestreift', '1× Knotenmütze Creme mit Teddy-Print'],
     ['mütze', 'knotenmütze', 'teddybär', 'neutral'], 'DRAFT'),
    # --- Erstausstattung 8-teilig
    ('hund-creme', 'Erstausstattung-Set «I love Dogs» – Creme, 8-teilig', 'erstausstattung-set-i-love-dogs', 'Erstausstattungs-Set', 'u',
     {'03': 10, '36': 10}, 60, PF + 'set_hund_creme_quadratisch.jpg', cs_et('strampler-hund-creme'),
     'Für kleine Hundefreunde: Dieses 8-teilige Set aus 100 % weicher Baumwolle verbindet zarte Creme- und Beigetöne mit verspielten Hündchen-Motiven. Alles, was ein Neugeborenes für den Start braucht – liebevoll in einem Set.',
     ['1× Strampler mit Fuss «I ♥ DOGS»', '1× Langarm-Body mit Hündchen-Print', '1× Mütze mit Öhrchen', '1× Kapuzentuch «Home is where the Dog is»', '1× Lätzchen «HUG ME!»', '1× Plüsch-Hündchen (Schmusetuch)', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['hund', 'creme', 'neutral'], 'ACTIVE'),
    ('hase-rosa', 'Erstausstattung-Set «Hase» – Rosa, 8-teilig', 'erstausstattung-set-hase-rosa', 'Erstausstattungs-Set', 'm',
     {'03': 5, '36': 5}, 60, PF + 'set_hase_rosa_quadratisch.jpg', pf_et('set_hase_rosa'),
     'Zuckersüss in Rosa: Dieses 8-teilige Set mit Häschen-Motiven aus 100 % Baumwolle ist ein liebevoller Begleiter für die ersten Wochen – und ein Geschenk, das Herzen höher schlagen lässt.',
     ['1× Strampler mit Fuss und Häschen-Print', '1× Langarm-Body mit Giesskannen-Motiv', '1× Knotenmütze', '1× Kapuzentuch', '1× Lätzchen', '1× Rassel Hase', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['hase', 'rosa'], 'ACTIVE'),
    ('wal-blau', 'Erstausstattung-Set «Wal» – Hellblau, 8-teilig', 'erstausstattung-set-wal-blau', 'Erstausstattungs-Set', 'j',
     {'03': 10, '36': 10}, 60, PF + 'set_wal_blau_quadratisch.jpg', pf_et('set_wal_blau'),
     'Ab ins Meer der Träume: Das 8-teilige Set in sanftem Hellblau mit süssen Walen und Segelbooten aus 100 % Baumwolle – maritim, weich und perfekt für kleine Entdecker.',
     ['1× Strampler mit Fuss und Wal-Print', '1× Langarm-Body', '1× Knotenmütze', '1× Kapuzentuch «Just swimming»', '1× Lätzchen Wal', '1× Schmusetuch Wal', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['wal', 'blau', 'maritim'], 'ACTIVE'),
    ('bauernhof', 'Erstausstattung-Set «Bauernhof» – Creme, 8-teilig', 'erstausstattung-set-bauernhof', 'Erstausstattungs-Set', 'u',
     {'03': 4, '36': 4}, 60, PF + 'set_bauernhof_quadratisch.jpg', pf_et('set_bauernhof'),
     'Willkommen auf dem Bauernhof: Kuh, Schaf und Freunde begleiten Dein Baby in diesem fröhlichen 8-teiligen Set aus 100 % Baumwolle – für Mädchen und Jungen gleichermassen schön.',
     ['1× Strampler mit Fuss und Bauernhof-Print', '1× Langarm-Body', '1× Knotenmütze', '1× Kapuzentuch', '1× Lätzchen «Hi Friends»', '1× Rassel Kuh', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['bauernhof', 'tiere', 'creme', 'neutral'], 'ACTIVE'),
    ('best-family', 'Erstausstattung-Set «Best Family» Teddy – Beige & Creme, 8-teilig', 'erstausstattung-set-best-family-teddy', 'Erstausstattungs-Set', 'u',
     {'03': 10, '36': 10}, 60, PF + 'set_best_family_quadratisch.jpg', pf_et('set_best_family'),
     'Warm, weich und voller Teddy-Liebe: Das 8-teilige Set in Beige und Creme aus 100 % Baumwolle ist zeitlos schön und passt zu jedem Baby.',
     ['1× Strampler mit Fuss und Teddy-Print', '1× Langarm-Body mit Teddy «Best family»', '1× Mütze mit Öhrchen', '1× Kapuzentuch', '1× Lätzchen', '1× Rassel Teddy', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['teddybär', 'beige', 'neutral'], 'ACTIVE'),
    ('prinzessin-krone', 'Erstausstattung-Set «Little Princess» Krone – Rosa & Creme, 8-teilig', 'erstausstattung-set-little-princess-krone', 'Erstausstattungs-Set', 'm',
     {'03': 10, '36': 10}, 60, PF + 'set_prinzessin_krone_quadratisch.jpg', pf_et('set_prinzessin_krone'),
     'Für die kleine Prinzessin: Krönchen, Schleifen und Herzchen in Rosa und Creme – das 8-teilige Set aus 100 % Baumwolle macht die ersten Tage zu etwas ganz Besonderem.',
     ['1× Strampler mit Fuss', '1× Langarm-Body «Make a Wish»', '1× Mütze', '1× Kapuzentuch mit Krone', '1× Lätzchen', '1× Schmusetuch', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['prinzessin', 'krone', 'rosa'], 'ACTIVE'),
    ('weltall-8', 'Erstausstattung-Set «Little One» Weltall – Hellblau, 8-teilig', 'erstausstattung-set-weltall-little-one', 'Erstausstattungs-Set', 'j',
     {'03': 4, '36': 4}, 60, PF + 'set_weltall_hellblau_quadratisch.jpg', [],
     'Bis zum Mond und zurück: Planeten, Sterne und Sonnen in Hellblau und Weiss – das 8-teilige Set aus 100 % Baumwolle für kleine Astronauten.',
     ['1× Strampler mit Weltall-Print', '1× Langarm-Body mit Planet', '1× Mütze', '1× Kapuzentuch «Little one»', '1× Lätzchen mit Planet', '1× Sonnen-Rassel', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['weltall', 'hellblau'], 'ACTIVE'),
    ('gaensebluemchen-8', 'Erstausstattung-Set «It\'s a baby girl» Gänseblümchen – Apricot, 8-teilig', 'erstausstattung-set-gaensebluemchen', 'Erstausstattungs-Set', 'm',
     {'03': 10, '36': 10}, 60, PF + 'set_gaensebluemchen_quadratisch.jpg', pf_et('set_gaensebluemchen'),
     'Frühlingshaft und zart: Gänseblümchen in Apricot und Creme zieren dieses 8-teilige Set aus 100 % Baumwolle – ein liebevoller Gruss zur Geburt eines Mädchens.',
     ['1× Strampler mit Fuss und Rüschen', '1× Langarm-Body «It\'s a baby girl»', '1× Mütze', '1× Kapuzentuch', '1× Lätzchen «happy»', '1× Beissring Blume', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Paar Söckchen'],
     ['gänseblümchen', 'blumen', 'apricot'], 'ACTIVE'),
    # --- Erstausstattung 5-teilig
    ('eisbaer-taupe', 'Erstausstattung-Set «Eisbär» – Taupe, 5-teilig', 'erstausstattung-set-eisbaer-taupe', 'Erstausstattungs-Set', 'u',
     {'03': 5, '36': 5}, 36, CS + 'eisbaer-taupe/shop/eisbaer-taupe_shop.jpg', cs_et('eisbaer-taupe'),
     'Ruhige Naturtöne und ein Eisbär mit Bärchen «I love you mommy»: Das 5-teilige Set aus 100 % Baumwolle ist schlicht, warm und zum Verlieben.',
     ['1× Strampler mit Fuss, Taupe mit Tannen', '1× Kurzarm-Body Creme mit Eisbär', '1× Knotenmütze mit Tannen', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Lätzchen mit Bärchen-Etikett'],
     ['eisbär', 'taupe', 'neutral'], 'ACTIVE'),
    ('waldbaer-creme', 'Erstausstattung-Set «Waldbär» – Creme, 5-teilig', 'erstausstattung-set-waldbaer-creme', 'Erstausstattungs-Set', 'u',
     {'03': 5, '36': 5}, 36, PF + 'set_waldbaer_creme_quadratisch.jpg', cs_et('waldbaer-creme'),
     'Ein Spaziergang durch den Wald: Bären, Tannen und Pilze auf Creme – das 5-teilige Set aus 100 % Baumwolle mit geripptem Body und Lätzchen «Little Bear».',
     ['1× Strampler mit Fuss und Wald-Print', '1× Kurzarm-Body gerippt mit Bär', '1× Mütze mit Wald-Print', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Lätzchen «Little Bear»'],
     ['bär', 'wald', 'creme', 'neutral'], 'ACTIVE'),
    ('little-bear-rosa', 'Erstausstattung-Set «Little Bear» – Rosa, 5-teilig', 'erstausstattung-set-little-bear-rosa', 'Erstausstattungs-Set', 'm',
     {'03': 10, '36': 10}, 36, CS + 'little-bear-rosa/shop/little-bear-rosa_shop.jpg', cs_et('little-bear-rosa'),
     'Zart gerippt mit rosa Pünktchen und einem Teddy auf der Wolke: Das 5-teilige Set aus 100 % Baumwolle ist das perfekte Geschenk für kleine Mädchen.',
     ['1× Strampler mit Fuss, gerippt mit Pünktchen', '1× Kurzarm-Body mit Teddy, Mond und Stern', '1× Mütze mit Teddys und Bommel', '1× Paar Fäustlinge (Kratzhandschuhe)', '1× Lätzchen «Little Bear»'],
     ['teddybär', 'rosa', 'gerippt'], 'ACTIVE'),
    # --- Erstausstattung 6-teilig
    ('love-dad-mom', 'Erstausstattung-Set «I ♥ Dad Mom» – Weiss, 6-teilig', 'erstausstattung-set-i-love-dad-mom', 'Erstausstattungs-Set', 'u',
     {'03': 4, '36': 4}, 52, PF + 'set_love_dad_mom_quadratisch.jpg', pf_et('set_love_dad_mom'),
     'Die schönste Liebeserklärung an Mama und Papa: Das 6-teilige Set in Weiss mit roten Herzen aus 100 % Baumwolle – frisch, fröhlich und für Mädchen wie Jungen.',
     ['1× Strampler mit Schrift-Print', '1× Body «I ♥ Dad Mom»', '1× Fusshose «Love»', '1× Knotenmütze', '1× Kapuzentuch', '1× Lätzchen'],
     ['herzen', 'weiss', 'neutral'], 'ACTIVE'),
    ('lila-hase', 'Erstausstattung-Set «little and cute» Hase – Lila, 6-teilig', 'erstausstattung-set-hase-lila', 'Erstausstattungs-Set', 'm',
     {'03': 10, '36': 10}, 52, PF + 'set_lila_hase_quadratisch.jpg', pf_et('set_lila_hase'),
     'Verspielt und zart: Häschen und Spitze in Flieder und Weiss – das 6-teilige Set aus 100 % Baumwolle für kleine Mädchen.',
     ['1× Strampler mit Spitzenkragen', '1× Body Lila mit Häschen', '1× Fusshose', '1× Knotenmütze', '1× Kapuzentuch mit Spitze', '1× Lätzchen'],
     ['hase', 'lila', 'spitze'], 'ACTIVE'),
    ('dino-cool-dude', 'Erstausstattung-Set «Cool Dude» Dino – Creme, 6-teilig', 'erstausstattung-set-dino-cool-dude', 'Erstausstattungs-Set', 'j',
     {'03': 10, '36': 10}, 52, CS + 'dino-cool-dude/shop/dino-cool-dude_shop.jpg', cs_et('dino-cool-dude'),
     'Here comes trouble! Ein freundlicher Dino, Regenbögen und Pastellzacken auf Creme – das 6-teilige Set aus 100 % Baumwolle für kleine Abenteurer.',
     ['1× Strampler mit Regenbogen-Print', '1× Langarm-Body «Cool Dude»', '1× Fusshose mit Regenbogen-Print', '1× Mütze mit Dino-Zacken', '1× Kapuzentuch «here comes TROUBLE!»', '1× Lätzchen mit Dino'],
     ['dino', 'creme'], 'ACTIVE'),
    ('born-2027-rosa', 'Erstausstattung-Set «Born in 2027» – Rosa, 6-teilig', 'erstausstattung-set-born-in-2027-rosa', 'Erstausstattungs-Set', 'm',
     {'03': 10, '36': 10}, 52, CS + 'born-in-2027-rosa/shop/born-in-2027-rosa_shop.jpg', cs_et('born-in-2027-rosa'),
     'Das Geburtsjahr zum Anziehen: Das 6-teilige Set in Rosa mit «Born in 2027» aus 100 % Baumwolle – ein Erinnerungsstück für das erste Babyfoto.',
     ['1× Strampler mit Fuss', '1× Kurzarm-Body «Born in 2027»', '1× Fusshose', '1× Knotenmütze', '1× Kapuzentuch «Born in 2027»', '1× Lätzchen «Born in 2027»'],
     ['born in 2027', 'rosa'], 'ACTIVE'),
    ('born-2027-blau', 'Erstausstattung-Set «Born in 2027» – Hellblau, 6-teilig', 'erstausstattung-set-born-in-2027-blau', 'Erstausstattungs-Set', 'j',
     {'03': 10, '36': 10}, 52, None, [],
     'Das Geburtsjahr zum Anziehen: Das 6-teilige Set in Hellblau mit «Born in 2027» aus 100 % Baumwolle – ein Erinnerungsstück für das erste Babyfoto.',
     ['1× Strampler mit Fuss', '1× Kurzarm-Body «Born in 2027»', '1× Fusshose', '1× Knotenmütze', '1× Kapuzentuch «Born in 2027»', '1× Lätzchen «Born in 2027»'],
     ['born in 2027', 'hellblau'], 'DRAFT'),
    # --- Newborn 3-teilig (Erstausstattung)
    ('smile-gruen', 'Erstausstattung-Set «Smile» – Salbeigrün, 3-teilig mit Kapuzentuch', 'erstausstattung-set-smile-salbeigruen', 'Erstausstattungs-Set', 'u',
     {'03': 5, '36': 5}, 36, PF + 'set_smile_gruen_quadratisch.jpg', cs_et('strampler-smile-gruen'),
     'Gute Laune in Salbeigrün: Ripp-Strampler «You make me happy», Knotenmütze und Kapuzentuch «SMILE» (76 × 76 cm) aus 100 % Baumwolle – modern, neutral und herrlich weich.',
     ['1× Ripp-Strampler mit Fuss «You make me happy»', '1× Knotenmütze', '1× Kapuzentuch «SMILE», 76 × 76 cm'],
     ['salbeigrün', 'gerippt', 'neutral'], 'ACTIVE'),
    ('gerippt-beige-baer', 'Erstausstattung-Set «Little Bear» gerippt – Hafer, 3-teilig', 'erstausstattung-set-gerippt-beige-baer', 'Erstausstattungs-Set', 'u',
     {'NB': 3, '03': 3}, 26, CS + 'gerippt-beige-baer/shop/gerippt-beige-baer_shop.jpg', [],
     'Schlicht und kuschelig: Wickelbody, Fusshose und Mütze mit Öhrchen in weich geripptem Hafer, jeweils mit kleinem Bärchen-Etikett. Der Wickelbody lässt sich seitlich öffnen – ideal für die ersten Wochen.',
     ['1× Wickelbody mit Bärchen-Etikett', '1× Fusshose', '1× Mütze mit Öhrchen'],
     ['gerippt', 'beige', 'neutral', 'wickelbody'], 'ACTIVE'),
    ('little-princess-wickelbody', 'Erstausstattung-Set «Little Princess» – Rosa, 3-teilig', 'erstausstattung-set-little-princess-wickelbody', 'Erstausstattungs-Set', 'm',
     {'NB': 3, '03': 3}, 26, CS + 'little-princess-wickelbody/shop/little-princess-wickelbody_shop.jpg', weiss('little-princess-wickelbody'),
     'Ein Krönchen für die Kleinste: Rosa Wickelbody mit Krone, Satinschleife und Tüll an den Schultern, dazu Fusshose und Knotenmütze mit Schleifen und Herzchen.',
     ['1× Wickelbody Rosa mit Krone «Little Princess»', '1× Fusshose Creme mit Schleifen und Herzchen', '1× Knotenmütze'],
     ['prinzessin', 'rosa', 'wickelbody'], 'ACTIVE'),
    ('i-love-you-dad', 'Erstausstattung-Set «I love you Dad» – Hellblau, 3-teilig', 'erstausstattung-set-i-love-you-dad', 'Erstausstattungs-Set', 'j',
     {'NB': 3, '03': 3}, 26, CS + 'i-love-you-dad/shop/i-love-you-dad_shop.jpg', weiss('i-love-you-dad'),
     'Für den stolzen Papa: Hellblauer Wickelbody mit Schnurrbart «I love you Dad», dazu Fusshose und Knotenmütze mit Fliegen, Hüten und Brillen.',
     ['1× Wickelbody Hellblau «I love you Dad»', '1× Fusshose mit Fliegen und Hüten', '1× Knotenmütze'],
     ['papa', 'hellblau', 'wickelbody'], 'ACTIVE'),
    ('heissluftballon-dream-big', 'Erstausstattung-Set «Dream big» Heissluftballon – Weiss & Beige, 3-teilig', 'erstausstattung-set-dream-big-heissluftballon', 'Erstausstattungs-Set', 'u',
     {'NB': 3, '03': 3}, 26, CS + 'heissluftballon-dream-big/shop/heissluftballon-dream-big_shop.jpg', weiss('heissluftballon-dream-big'),
     'Grosse Träume für kleine Abenteurer: Wickelbody mit Bären im Heissluftballon «dream BIG», dazu Fusshose und Knotenmütze mit Ballon-, Elefanten- und Löwen-Print.',
     ['1× Wickelbody Weiss mit Pünktchen «dream BIG»', '1× Fusshose Beige mit Heissluftballons', '1× Knotenmütze im gleichen Print'],
     ['heissluftballon', 'beige', 'neutral', 'wickelbody'], 'ACTIVE'),
    ('weltall-hellblau', 'Erstausstattung-Set «Little One» Weltall – Hellblau, 3-teilig', 'erstausstattung-set-weltall-3-teilig', 'Erstausstattungs-Set', 'j',
     {'NB': 3, '03': 3}, 26, CS + 'weltall-hellblau/shop/weltall-hellblau_shop.jpg', cs_et('weltall-hellblau'),
     'Ab ins All: Gerippter Wickelbody in Hellblau mit lachendem Planeten, dazu Fusshose und Knotenmütze mit Planeten und Sternen.',
     ['1× Wickelbody Hellblau gerippt mit Planet', '1× Fusshose Weiss mit Weltall-Print', '1× Knotenmütze'],
     ['weltall', 'hellblau', 'wickelbody'], 'ACTIVE'),
    ('gaensebluemchen-beautiful', 'Erstausstattung-Set «Beautiful» Gänseblümchen – Apricot, 3-teilig', 'erstausstattung-set-beautiful-gaensebluemchen', 'Erstausstattungs-Set', 'm',
     {'NB': 3, '03': 3}, 26, CS + 'gaensebluemchen-beautiful/shop/gaensebluemchen-beautiful_shop.jpg', cs_et('gaensebluemchen-beautiful') + weiss('gaensebluemchen-beautiful'),
     'Zart wie ein Frühlingsmorgen: Apricot-Wickelbody mit Rüschen, Schleifchen und Gänseblümchen «Beautiful», dazu Fusshose und Knotenmütze mit Gänseblümchen.',
     ['1× Wickelbody Apricot mit Rüschen «Beautiful»', '1× Fusshose mit Gänseblümchen', '1× Knotenmütze mit Gänseblümchen'],
     ['gänseblümchen', 'apricot', 'wickelbody'], 'ACTIVE'),
    ('blumen-musselin', 'Erstausstattung-Set «Blumenwiese» Musselin – 3-teilig mit Haarband', 'erstausstattung-set-blumenwiese-musselin', 'Erstausstattungs-Set', 'm',
     {'NB': 3, '03': 3}, 26, CS + 'blumen-musselin/shop/blumen-musselin_shop.jpg', weiss('blumen-musselin'),
     'Luftig und romantisch: Wickelbody und Fusshose aus atmungsaktivem Musselin mit Streublumen, dazu ein passendes Haarband mit Schleife.',
     ['1× Wickelbody Musselin mit Streublumen', '1× Fusshose Musselin', '1× Haarband mit Schleife'],
     ['blumen', 'musselin', 'wickelbody'], 'ACTIVE'),
    # --- Strampler-Sets
    ('strampler-blumen-hase', 'Strampler-Set «Blumen & Hase» – 2 Strampler mit Haarband', 'strampler-set-blumen-hase', 'Strampler-Set', 'm',
     {'03': 3, '36': 3, '69': 3}, 38, CS + 'strampler-blumen-hase/shop/strampler-blumen-hase_shop.jpg', cs_et('strampler-blumen-hase'),
     'Zwei Lieblingsstrampler für kleine Mädchen: einer mit Wildblumen und Spitzenkragen, einer in Rosa mit gesticktem Häschen in der Brusttasche – dazu ein passendes Haarband.',
     ['1× Strampler gerippt mit Wildblumen und Spitzenkragen', '1× Strampler Rosa mit Hase-Stickerei', '1× Haarband mit Knoten'],
     ['hase', 'blumen', 'rosa'], 'ACTIVE'),
    ('strampler-kaetzchen-tulpen', 'Strampler-Set «Kätzchen & Tulpen» – 2 Strampler mit Mütze', 'strampler-set-kaetzchen-tulpen', 'Strampler-Set', 'm',
     {'03': 3, '36': 3, '69': 3}, 38, CS + 'strampler-kaetzchen-tulpen/shop/strampler-kaetzchen-tulpen_shop.jpg', cs_et('strampler-kaetzchen-tulpen'),
     'Verspielt und zart: ein Strampler mit Kätzchen und fliederfarbenem Kragen, einer mit Tulpen und Bubikragen – dazu die passende Mütze.',
     ['1× Strampler Creme mit Kätzchen', '1× Strampler Creme mit Tulpen und Bubikragen', '1× Mütze mit Tulpen'],
     ['kätzchen', 'tulpen', 'flieder'], 'ACTIVE'),
    ('strampler-sweet-home', 'Strampler-Set «Sweet Home» – 2 Strampler mit Mütze', 'strampler-set-sweet-home', 'Strampler-Set', 'u',
     {'03': 3, '36': 3, '69': 3}, 38, CS + 'strampler-sweet-home/shop/strampler-sweet-home_shop.jpg', cs_et('strampler-sweet-home'),
     'Willkommen zu Hause: zwei Strampler in Naturtönen – einer mit Häuschen-Print, einer gestreift mit «sweet HOME» – und eine Mütze mit Bärenöhrchen.',
     ['1× Strampler Beige mit Häuschen-Print', '1× Strampler gestreift «sweet HOME»', '1× Mütze mit Öhrchen'],
     ['beige', 'neutral'], 'ACTIVE'),
    ('strampler-waldtiere', 'Strampler 3er-Set «Waldtiere» – Himbeer & Weiss', 'strampler-3er-set-waldtiere', 'Strampler-Set', 'm',
     {'03': 6, '36': 6, '69': 6}, 51, CS + 'strampler-waldtiere/shop/strampler-waldtiere_shop.jpg', cs_et('strampler-waldtiere'),
     'Drei Strampler für kleine Waldfreundinnen: Himbeer mit Füchsen und Hasen, Weiss mit Pünktchen und Eichhörnchen, Weiss mit Zweigen und Rüschen.',
     ['1× Strampler Himbeer mit Waldtieren', '1× Strampler Weiss mit Pünktchen und Eichhörnchen', '1× Strampler Weiss mit Zweigen und Rüschen'],
     ['waldtiere', 'himbeer'], 'ACTIVE'),
    ('strampler-rosa-little-princess', 'Strampler 3er-Set «Little Princess» – Rosa & Creme', 'strampler-3er-set-little-princess', 'Strampler-Set', 'm',
     {'03': 6, '36': 6, '69': 6}, 51, CS + 'strampler-rosa-little-princess/shop/strampler-rosa-little-princess_shop.jpg', cs_et('strampler-rosa-little-princess'),
     'Drei Strampler für die kleine Prinzessin: Altrosa mit Schleifen, Creme mit Tüll-Rüsche und Rosa mit Krone «Little Princess».',
     ['1× Strampler Altrosa mit Schleifen', '1× Strampler Creme mit Tüll-Rüsche', '1× Strampler Rosa «Little Princess»'],
     ['prinzessin', 'rosa', 'schleifen'], 'ACTIVE'),
    ('strampler-neutral', 'Strampler 3er-Set «Naturtöne» – Salbei, Creme & Beige', 'strampler-3er-set-naturtoene', 'Strampler-Set', 'u',
     {'03': 6, '36': 6, '69': 6}, 51, CS + 'strampler-neutral/shop/strampler-neutral_shop.jpg', [],
     'Drei schlichte Lieblingsstrampler in Naturtönen – Salbeigrün, Creme und Beige mit feinen Prints. Passen zu allem und sind perfekt für jeden Tag.',
     ['1× Strampler Salbeigrün', '1× Strampler Creme', '1× Strampler Beige'],
     ['salbeigrün', 'beige', 'neutral'], 'ACTIVE'),
    ('strampler-segelboote', 'Strampler 3er-Set «Segelboote» – Creme & Blau', 'strampler-3er-set-segelboote', 'Strampler-Set', 'j',
     {'03': 6, '36': 6, '69': 6}, 51, CS + 'strampler-segelboote/shop/strampler-segelboote_shop.jpg', cs_et('strampler-segelboote'),
     'Leinen los: Creme mit Segelbooten, Taubenblau gerippt «a Dream comes true» und Hellblau «Enjoy every single day» – drei maritime Strampler.',
     ['1× Strampler Creme mit Segelbooten', '1× Strampler Taubenblau «a Dream comes true»', '1× Strampler Hellblau «Enjoy every single day»'],
     ['segelboote', 'blau', 'maritim'], 'ACTIVE'),
    ('strampler-kirschen', 'Strampler 3er-Set «Kirschen» – Weinrot, Altrosa & Weiss', 'strampler-3er-set-kirschen', 'Strampler-Set', 'm',
     {'03': 6, '36': 6, '69': 6}, 51, CS + 'strampler-kirschen/shop/strampler-kirschen_shop.jpg', cs_et('strampler-kirschen'),
     'Süss wie Kirschen: Weinrot gerippt «Smile» (Rücken «i love my mummy»), Altrosa «You are the best» und Weiss mit Kirschen-Print.',
     ['1× Strampler Weinrot gerippt «Smile»', '1× Strampler Altrosa «You are the best»', '1× Strampler Weiss mit Kirschen'],
     ['kirschen', 'weinrot', 'rosa'], 'ACTIVE'),
    ('strampler-avocado', 'Strampler 3er-Set «Avocado» – Grün & Weiss', 'strampler-3er-set-avocado', 'Strampler-Set', 'u',
     {'03': 6, '36': 6, '69': 6}, 51, None, [],
     'Frisch und fröhlich: Weiss mit Avocado-Print, Grün mit Avocado und Weiss mit Regenbogen «LOVE» – drei Strampler für jeden Tag.',
     ['1× Strampler Weiss mit Avocados', '1× Strampler Grün mit Avocado', '1× Strampler Weiss mit Regenbogen «LOVE»'],
     ['avocado', 'grün', 'neutral'], 'DRAFT'),
    # --- Hosen-Sets
    ('hosen-herzen-rosa', 'Baby-Hosen 3er-Set «Herzen» – Creme, Altrosa & Rosa', 'baby-hosen-3er-set-herzen', 'Hosen-Set', 'm',
     {'03': 3, '36': 3, '69': 3}, 27, CS + 'hosen-herzen-rosa/shop/hosen-herzen-rosa_shop.jpg', cs_et('hosen-herzen-rosa'),
     'Drei weiche Babyhosen mit Bündchen und Schleife: Creme mit bunten Leo-Herzen, Altrosa gerippt «Love more» und Rosa mit Herzchen.',
     ['1× Hose Creme mit Leo-Herzen', '1× Hose Altrosa gerippt «Love more»', '1× Hose Rosa mit Herzchen'],
     ['hose', 'herzen', 'rosa'], 'ACTIVE'),
    ('hosen-baeren', 'Baby-Hosen 3er-Set «Bären» – Beige, Braun & Weiss', 'baby-hosen-3er-set-baeren', 'Hosen-Set', 'u',
     {'03': 3, '36': 3, '69': 3}, 27, CS + 'hosen-baeren/shop/hosen-baeren_shop.jpg', cs_et('hosen-baeren'),
     'Drei kuschelige Babyhosen mit Bündchen und Schleife: Beige gestreift, Braun mit Bärenkopf «I love hugs» und Weiss mit Bärenköpfen.',
     ['1× Hose Beige gestreift', '1× Hose Braun «I love hugs»', '1× Hose Weiss mit Bärenköpfen'],
     ['hose', 'bär', 'neutral'], 'ACTIVE'),
]

SKUKEY = lambda k: 'SNZ-' + k.upper().replace('-', '')[:14]
GESCHL = {'m': ['mädchen'], 'j': ['junge'], 'u': ['mädchen', 'junge', 'unisex']}


def beschreibung(p):
    key, titel, handle, typ, g, gr, ek, haupt, extra, intro, teile, tags, status = p
    pflege = '<li>Waschbar bei 30 °C, nicht in den Trockner</li>' if typ != 'Accessoires' else '<li>Waschbar bei 30 °C</li>'
    vorteile = ['100 % weiche, hautfreundliche Baumwolle', 'Liebevolle Details und harmonisch abgestimmte Farben',
                'Ideal als Geschenk zur Geburt oder zur Babyparty']
    if typ in ('Erstausstattungs-Set', 'Strampler-Set'):
        vorteile.insert(1, 'Druckknöpfe für schnelles An- und Ausziehen')
    return (f'<p>{intro}</p><h4>Das Set beinhaltet</h4><ul>' + ''.join(f'<li>{t}</li>' for t in teile) + '</ul>'
            '<h4>Warum Du dieses Set lieben wirst</h4><ul>' + ''.join(f'<li>{v}</li>' for v in vorteile) + '</ul>'
            '<h4>Material &amp; Pflege</h4><ul><li>100 % Baumwolle</li>' + pflege + '</ul>'
            '<p><em>Versand innert 1–2 Werktagen · Gratisversand in der Schweiz ab CHF 50.</em></p>')


UMLAUT = {'ae': 'ä', 'oe': 'ö', 'ue': 'ü'}


def bildtext(pfad):
    """Alt-Text aus dem Dateinamen: Einzelteil-Name, sonst Set-Bild."""
    if 'einzelteile' not in pfad:
        return 'Weissbild' if 'hauptbild_weiss' in pfad else 'Set aus 100 % Baumwolle'
    n = os.path.basename(pfad)[:-4]
    n = n.split('_', 2)[-1] if n.startswith('set_') else n            # set_hase_rosa_body -> body
    woerter = []
    for w in n.split('_'):
        if w not in ('segelboote', 'true'):                            # echte oe/ue, keine Umlaute
            for a, b in UMLAUT.items():
                w = w.replace(a, b)
        woerter.append(w)
    n = ' '.join(woerter)
    return n[:1].upper() + n[1:]


def produkt(p):
    key, titel, handle, typ, g, gr, ek, haupt, extra, intro, teile, tags, status = p
    pr = preis(ek)
    name = titel.split(' – ')[0]
    bilder = ([haupt] if haupt and haupt.endswith('.jpg') else []) + extra
    files = [{'originalSource': RAW + b, 'contentType': 'IMAGE', 'alt': f'{name} – {bildtext(b)}'} for b in bilder]
    alltags = sorted(set(['geschenk zur geburt', 'baumwolle'] + tags + GESCHL[g]
                         + ([f'{gg}-erstausstattung' for gg in GESCHL[g] if gg != 'unisex'] if typ == 'Erstausstattungs-Set' else [])
                         + (['erstausstattung', 'neugeborene'] if typ == 'Erstausstattungs-Set' else [])
                         + [G[c] for c in gr]))
    inp = {'title': titel, 'handle': handle, 'productType': typ, 'vendor': 'sunnozy', 'status': status,
           'descriptionHtml': beschreibung(p), 'tags': alltags,
           'seo': {'title': f'{name} | sunnozy'[:70],
                   'description': f'{titel} aus 100 % Baumwolle – {len(teile)} Teile, ideal als Geschenk zur Geburt. '
                                  'Versand innert 1–2 Werktagen, Gratisversand in der Schweiz ab CHF 50.'[:320]},
           'productOptions': [{'name': 'Grösse', 'values': [{'name': G[c]} for c in gr]}],
           'variants': [{'optionValues': [{'optionName': 'Grösse', 'name': G[c]}], 'price': pr,
                         'sku': f'{SKUKEY(key)}-{SKU[c]}', 'inventoryPolicy': 'DENY',
                         'inventoryItem': {'tracked': True},
                         'inventoryQuantities': [{'locationId': 'gid://shopify/Location/122855391575', 'name': 'available', 'quantity': m}]}
                        for c, m in gr.items()],
           'files': files}
    if typ in ('Erstausstattungs-Set', 'Strampler-Set'):
        inp['category'] = ERST
    return inp


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for p in P:
        inp = produkt(p)
        for f in inp['files']:
            pfad = os.path.join(ROOT, f['originalSource'][len(RAW):])
            assert os.path.exists(pfad), pfad
        json.dump(inp, open(os.path.join(out, inp['handle'] + '.json'), 'w'), ensure_ascii=False)
        print(f"{p[0]:32s} {inp['variants'][0]['price']:>6s}  {len(inp['files'])} Bilder  {inp['status']}")
