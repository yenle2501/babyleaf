# sunnozy Etsy-MCP

Ein eigener MCP-Server für den Etsy-Shop **sunnozyCH**. Damit kann Claude den Shop direkt
lesen und bearbeiten: Artikel, Preise und Lager, Bilder, Übersetzungen, Bestellungen und Bewertungen.
Er läuft lokal auf deinem Computer und nutzt die offizielle Etsy Open API v3.

## Tools

| Lesen | Schreiben |
|---|---|
| `etsy_shop_info`: Shop-Übersicht | `etsy_update_listing`: Titel, Beschreibung, Tags, Status |
| `etsy_list_listings`: Artikel mit Aufrufen und Favoriten | `etsy_set_price_quantity`: Preis und Lager (auch pro SKU) |
| `etsy_get_listing`: ein Artikel komplett, mit Varianten | `etsy_create_draft_listing`: neuer Artikel als Entwurf |
| `etsy_list_orders` / `etsy_get_order`: Bestellungen | `etsy_upload_image`: Bild aus Datei oder URL |
| `etsy_list_reviews`: Bewertungen | `etsy_set_translation`: Texte in DE, EN, FR … |
| `etsy_shop_setup`: Sections, Versand, Rückgabe | `etsy_mark_shipped`: versendet melden, mit Sendungsnummer |
| `etsy_find_category`: taxonomy_id suchen | `etsy_update_shop`: Ankündigung, Käufer-Nachricht |

Mit `ETSY_READ_ONLY=1` werden nur die Lese-Tools angeboten.

## Einrichtung (einmalig, ca. 10 Minuten)

**1. Etsy-App anlegen.** Auf <https://www.etsy.com/developers/register> mit dem sunnozyCH-Konto anmelden:
- Name: `sunnozy-mcp`
- «Who will be the users of this application?» → *Just myself or colleagues*
- «Is your application commercial?» → *No*

Etsy prüft neue Apps manchmal ein paar Tage. Danach stehen unter
<https://www.etsy.com/developers/your-apps> der **Keystring** und das **Shared Secret**.
Bei der App unter *Callback URLs* folgende Adresse eintragen: `http://localhost:3003/oauth/redirect`

**2. Installieren** (Node.js 18 oder neuer):

```bash
cd etsy-mcp
npm install
cp .env.example .env   # Keystring und Shared Secret eintragen
```

**3. Mit Etsy verbinden:**

```bash
npm run login
```

Der Browser öffnet die Etsy-Freigabe. Nach dem Klick auf «Zugriff erlauben» speichert der Login die Tokens in
`~/.config/sunnozy-etsy-mcp/tokens.json`. Der Server erneuert sie danach selbst
(der Refresh-Token gilt 90 Tage. Wird der Server länger nicht genutzt, einfach `npm run login` wiederholen).

Dein Etsy-Passwort braucht und speichert der Server nicht.

**4. In Claude einbinden.**

- *Claude Code*: Die Datei `.mcp.json` im Repo-Hauptordner registriert den Server schon. Claude Code im Repo starten und den Server freigeben.
- *Claude Desktop*: In `claude_desktop_config.json` ergänzen (Pfad anpassen):

```json
{
  "mcpServers": {
    "sunnozy-etsy": {
      "command": "node",
      "args": ["/PFAD/ZU/babyleaf/etsy-mcp/src/index.js"]
    }
  }
}
```

## Beispiele

- «Welche Etsy-Artikel haben die meisten Aufrufe, aber keine Verkäufe?»
- «Zeig mir alle offenen Etsy-Bestellungen.»
- «Setz bei Artikel 1234567890 die Menge der SKU SET-56 auf 0.»
- «Schreib die Tags aller aktiven Artikel auf Englisch neu, maximal 13 pro Artikel.»
- «Lade sunnozy-content/…/hauptbild.jpg als Hauptbild zu Artikel 1234567890 hoch.»

## Hinweise

- Schreibende Tools ändern den echten Shop. Claude fragt vor jedem Aufruf um Erlaubnis, solange du sie nicht dauerhaft freigibst.
- Tags: höchstens 13, je 20 Zeichen, nur Buchstaben, Zahlen, Leerzeichen, `-` und `'`.
- Ein Entwurf wird erst mit Bild und `state=active` öffentlich (Etsy verrechnet dann die Einstellgebühr).
- Tests: `npm test`
