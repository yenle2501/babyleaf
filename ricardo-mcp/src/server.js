#!/usr/bin/env node
// MCP-Server für das Ricardo-Verkäuferkonto (my-ricardo → Verkaufen).
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import {
  BASE, login, loginStatus, openMyRicardo, extractArticles, pageText, screenshot, closeBrowser, getContext, isCaptcha,
} from './browser.js';

// Bereiche unter my-ricardo/selling. Falls Ricardo Pfade ändert, hilft `ricardo_page`.
const SECTIONS = {
  offers: '/de/my-ricardo/selling/offers/',
  sold: '/de/my-ricardo/selling/sold/',
  unsold: '/de/my-ricardo/selling/unsold/',
  planned: '/de/my-ricardo/selling/planned/',
};

const server = new McpServer({ name: 'ricardo', version: '0.1.0' });

const json = data => ({ content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] });
const fail = err => ({ isError: true, content: [{ type: 'text', text: String(err?.message || err) }] });

server.registerTool('ricardo_login_status', {
  description: 'Prüft, ob die gespeicherte Ricardo-Session noch eingeloggt ist.',
  inputSchema: {},
}, async () => {
  try { return json(await loginStatus()); } catch (e) { return fail(e); }
});

server.registerTool('ricardo_login', {
  description: 'Loggt sich bei Ricardo ein (E-Mail/Passwort aus .env). Öffnet einen sichtbaren Browser, '
    + 'damit Captcha oder 2-Faktor-Code von Hand erledigt werden können. Die Session wird gespeichert.',
  inputSchema: {
    interactive: z.boolean().default(true).describe('Sichtbaren Browser öffnen (für Captcha/2FA nötig)'),
  },
}, async ({ interactive }) => {
  try { return json(await login({ interactive })); } catch (e) { return fail(e); }
});

server.registerTool('ricardo_list_offers', {
  description: 'Listet Artikel aus dem Verkäuferkonto: laufende Angebote (offers), verkauft (sold), '
    + 'nicht verkauft (unsold) oder geplant (planned). Liefert ID, Titel, Preis, Link und Kartentext.',
  inputSchema: {
    section: z.enum(Object.keys(SECTIONS)).default('offers'),
    includePageText: z.boolean().default(false).describe('Zusätzlich den Seitentext zurückgeben (zur Kontrolle)'),
  },
}, async ({ section, includePageText }) => {
  let page;
  try {
    page = await openMyRicardo(SECTIONS[section]);
    const articles = await extractArticles(page);
    const result = { section, url: page.url(), count: articles.length, articles };
    if (includePageText || articles.length === 0) result.page = await pageText(page, 8000);
    return json(result);
  } catch (e) { return fail(e); } finally { await page?.close().catch(() => {}); }
});

server.registerTool('ricardo_get_article', {
  description: 'Liest einen einzelnen Ricardo-Artikel (öffentliche Artikelseite): Titel, Preis, Beschreibung, Bilder.',
  inputSchema: {
    idOrUrl: z.string().describe('Artikel-ID (z.B. 1234567890) oder komplette Ricardo-URL'),
  },
}, async ({ idOrUrl }) => {
  let page;
  try {
    const url = /^https?:/.test(idOrUrl) ? idOrUrl : `${BASE}/de/a/${idOrUrl.trim()}/`;
    if (!url.startsWith(BASE)) throw new Error('Nur ricardo.ch-Adressen sind erlaubt.');
    const ctx = await getContext();
    page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
    if (await isCaptcha(page)) throw new Error('Captcha: bitte `ricardo_login` mit sichtbarem Browser ausführen.');
    const data = await page.evaluate(() => {
      const ld = [...document.querySelectorAll('script[type="application/ld+json"]')]
        .map(s => { try { return JSON.parse(s.textContent); } catch { return null; } })
        .flat().find(x => x && (x['@type'] === 'Product' || x['@type']?.includes?.('Product')));
      return {
        title: document.querySelector('h1')?.innerText.trim() || null,
        structured: ld || null,
        images: [...document.querySelectorAll('img')].map(i => i.src).filter(s => /img\.ricardostatic|ricardo/.test(s)).slice(0, 20),
      };
    });
    const { text } = await pageText(page, 6000);
    return json({ url: page.url(), ...data, text });
  } catch (e) { return fail(e); } finally { await page?.close().catch(() => {}); }
});

server.registerTool('ricardo_page', {
  description: 'Öffnet eine beliebige Seite unter ricardo.ch/de/my-ricardo/ (z.B. Nachrichten, Bewertungen, Rechnungen) '
    + 'und gibt Text und Links zurück. Nur lesend.',
  inputSchema: {
    path: z.string().describe('Pfad, z.B. /de/my-ricardo/selling/sold/ oder /de/my-ricardo/messages/'),
  },
}, async ({ path }) => {
  let page;
  try {
    if (!path.startsWith('/de/my-ricardo/')) throw new Error('Pfad muss mit /de/my-ricardo/ beginnen.');
    page = await openMyRicardo(path);
    return json(await pageText(page));
  } catch (e) { return fail(e); } finally { await page?.close().catch(() => {}); }
});

server.registerTool('ricardo_screenshot', {
  description: 'Macht einen Screenshot einer my-ricardo-Seite und gibt den Dateipfad zurück.',
  inputSchema: {
    path: z.string().default(SECTIONS.offers),
  },
}, async ({ path }) => {
  let page;
  try {
    if (!path.startsWith('/de/my-ricardo/')) throw new Error('Pfad muss mit /de/my-ricardo/ beginnen.');
    page = await openMyRicardo(path);
    return json({ file: await screenshot(page, 'my-ricardo') });
  } catch (e) { return fail(e); } finally { await page?.close().catch(() => {}); }
});

for (const sig of ['SIGINT', 'SIGTERM']) process.on(sig, async () => { await closeBrowser(); process.exit(0); });

await server.connect(new StdioServerTransport());
