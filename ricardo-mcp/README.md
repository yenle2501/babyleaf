# Ricardo MCP (sunnozy)

MCP-Server, mit dem Claude das Ricardo-Verkäuferkonto lesen kann
(<https://www.ricardo.ch/de/my-ricardo/selling/offers/>). Er steuert einen echten Browser
(Playwright) und speichert die Login-Session in `.browser-profile/`.

> Ricardo schützt die Seite mit einer Cloudflare-Captcha. Aus Cloud-Servern kommt man nicht durch,
> darum läuft dieser Server **lokal auf deinem Computer**. Die Captcha klickst du beim ersten Login
> einmal selbst an, danach wird die Session wiederverwendet.

## Einrichten (einmalig)

```bash
cd ricardo-mcp
npm install
npx playwright install chromium     # oder in .env: RICARDO_BROWSER_CHANNEL=chrome
cp .env.example .env                # E-Mail + Passwort eintragen
npm run login                       # Browser öffnet sich → einloggen / Captcha anklicken
```

Danach in `.env` optional `RICARDO_HEADLESS=true` setzen, damit kein Fenster mehr aufgeht.
Läuft die Session ab, einfach `npm run login` wiederholen.

## In Claude einbinden

- **Claude Code:** Im Repo-Ordner liegt `.mcp.json`, der Server `ricardo` wird automatisch angeboten.
- **Claude Desktop:** in `claude_desktop_config.json` ergänzen:

```json
{
  "mcpServers": {
    "ricardo": { "command": "node", "args": ["/PFAD/ZU/babyleaf/ricardo-mcp/src/server.js"] }
  }
}
```

## Tools

| Tool | Was es macht |
|---|---|
| `ricardo_login_status` | Prüft, ob die Session noch eingeloggt ist |
| `ricardo_login` | Login mit `.env`-Daten, sichtbarer Browser für Captcha/2FA |
| `ricardo_list_offers` | Artikel aus `offers` (laufend), `sold`, `unsold`, `planned`: ID, Titel, Preis, Link |
| `ricardo_get_article` | Einzelner Artikel per ID oder URL: Titel, Preis, Beschreibung, Bilder |
| `ricardo_page` | Beliebige Seite unter `/de/my-ricardo/` als Text + Links (z.B. Nachrichten, Bewertungen) |
| `ricardo_screenshot` | Screenshot einer my-ricardo-Seite nach `screenshots/` |

Alle Tools sind **nur lesend**. Neue Angebote einstellen oder Preise ändern ist noch nicht eingebaut.

## Sicherheit

- Zugangsdaten stehen nur in `.env` (per `.gitignore` ausgeschlossen), nie im Code.
- `.browser-profile/` enthält die Login-Cookies: nicht teilen, nicht committen.
