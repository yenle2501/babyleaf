// Browser-Steuerung für Ricardo: persistentes Profil, Login, Seiten auslesen.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const BASE = 'https://www.ricardo.ch';

loadDotEnv(path.join(ROOT, '.env'));

const PROFILE_DIR = process.env.RICARDO_PROFILE_DIR || path.join(ROOT, '.browser-profile');
const SCREENSHOT_DIR = path.join(ROOT, 'screenshots');

let context = null;

// Minimaler .env-Leser, damit keine Zusatzabhängigkeit nötig ist.
function loadDotEnv(file) {
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (!m || process.env[m[1]] !== undefined) continue;
    process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

function headless() {
  return String(process.env.RICARDO_HEADLESS ?? 'false').toLowerCase() === 'true';
}

export async function getContext({ forceHeaded = false } = {}) {
  if (context) return context;
  context = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless: forceHeaded ? false : headless(),
    // z.B. "chrome" = installiertes Google Chrome statt Playwright-Chromium
    channel: process.env.RICARDO_BROWSER_CHANNEL || undefined,
    locale: 'de-CH',
    timezoneId: 'Europe/Zurich',
    viewport: { width: 1280, height: 900 },
  });
  context.on('close', () => { context = null; });
  return context;
}

export async function closeBrowser() {
  if (context) await context.close().catch(() => {});
  context = null;
}

async function newPage() {
  const ctx = await getContext();
  return ctx.newPage();
}

export async function isCaptcha(page) {
  const title = await page.title().catch(() => '');
  return /Nur einen Moment|Just a moment|Captcha/i.test(title);
}

// Wartet, bis Cloudflare die Seite freigibt (im sichtbaren Browser klickt die Nutzerin das Häkchen).
async function waitPastCaptcha(page, timeoutMs) {
  const end = Date.now() + timeoutMs;
  while (Date.now() < end) {
    if (!(await isCaptcha(page))) return true;
    await page.waitForTimeout(1500);
  }
  return false;
}

function isLoginUrl(url) {
  return /login|signin|auth/i.test(new URL(url).hostname + new URL(url).pathname);
}

export async function openMyRicardo(urlPath, { timeoutMs = 45000 } = {}) {
  const page = await newPage();
  await page.goto(new URL(urlPath, BASE).toString(), { waitUntil: 'domcontentloaded' });
  if (!(await waitPastCaptcha(page, headless() ? 15000 : 120000))) {
    await page.close();
    throw new Error('Ricardo zeigt eine Captcha. Bitte einmal `npm run login` ausführen (sichtbarer Browser) und das Häkchen setzen.');
  }
  await page.waitForLoadState('networkidle', { timeout: timeoutMs }).catch(() => {});
  if (isLoginUrl(page.url())) {
    await page.close();
    throw new Error('Nicht eingeloggt. Bitte zuerst das Tool `ricardo_login` oder `npm run login` verwenden.');
  }
  return page;
}

async function fillFirst(page, selectors, value) {
  for (const sel of selectors) {
    const el = page.locator(sel).first();
    if (await el.isVisible().catch(() => false)) {
      await el.fill(value);
      return true;
    }
  }
  return false;
}

async function clickSubmit(page) {
  const btn = page.locator('button[type=submit], button:has-text("Weiter"), button:has-text("Einloggen"), button:has-text("Anmelden"), button:has-text("Login")').first();
  if (await btn.isVisible().catch(() => false)) await btn.click();
  else await page.keyboard.press('Enter');
}

export async function loginStatus() {
  const page = await newPage();
  try {
    await page.goto(`${BASE}/de/my-ricardo/selling/offers/`, { waitUntil: 'domcontentloaded' });
    await waitPastCaptcha(page, headless() ? 15000 : 60000);
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
    if (await isCaptcha(page)) return { loggedIn: false, reason: 'captcha', url: page.url() };
    return { loggedIn: !isLoginUrl(page.url()), url: page.url() };
  } finally {
    await page.close();
  }
}

// Login mit E-Mail/Passwort aus der Umgebung. Bei Captcha oder 2FA bleibt der Browser
// sichtbar offen, bis die Nutzerin den Schritt selbst erledigt hat.
export async function login({ interactive = true, timeoutMs = 180000 } = {}) {
  const email = process.env.RICARDO_EMAIL;
  const password = process.env.RICARDO_PASSWORD;
  if (interactive) await closeBrowser();
  const ctx = await getContext({ forceHeaded: interactive });
  const page = await ctx.newPage();
  try {
    await page.goto(`${BASE}/de/my-ricardo/selling/offers/`, { waitUntil: 'domcontentloaded' });
    await waitPastCaptcha(page, interactive ? timeoutMs : 15000);
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});

    if (!isLoginUrl(page.url())) {
      const loginLink = page.locator('a:has-text("Einloggen"), button:has-text("Einloggen"), a:has-text("Anmelden")').first();
      if (await loginLink.isVisible().catch(() => false)) {
        await loginLink.click();
        await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
      }
    }

    if (isLoginUrl(page.url()) && email && password) {
      const emailSel = ['input[type=email]', 'input[name=email]', 'input[name=username]', 'input[autocomplete=username]', '#email'];
      const pwSel = ['input[type=password]', 'input[name=password]', '#password'];
      if (await fillFirst(page, emailSel, email)) {
        // Manche Logins zeigen das Passwortfeld erst nach "Weiter".
        if (!(await page.locator(pwSel[0]).first().isVisible().catch(() => false))) {
          await clickSubmit(page);
          await page.locator(pwSel[0]).first().waitFor({ state: 'visible', timeout: 15000 }).catch(() => {});
        }
        if (await fillFirst(page, pwSel, password)) await clickSubmit(page);
      }
    }

    // Auf Rückkehr zu my-ricardo warten (deckt auch manuelle Captcha/2FA-Schritte ab).
    const end = Date.now() + (interactive ? timeoutMs : 30000);
    while (Date.now() < end) {
      const url = page.url();
      if (url.startsWith(BASE) && !isLoginUrl(url) && !(await isCaptcha(page))) {
        return { loggedIn: true, url };
      }
      await page.waitForTimeout(1500);
    }
    const shot = await screenshot(page, 'login-fehlgeschlagen');
    return { loggedIn: false, url: page.url(), screenshot: shot };
  } finally {
    await page.close().catch(() => {});
    // Nach interaktivem Login wieder im konfigurierten Modus starten.
    if (interactive) await closeBrowser();
  }
}

export async function screenshot(page, name) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  const file = path.join(SCREENSHOT_DIR, `${name}-${Date.now()}.png`);
  await page.screenshot({ path: file, fullPage: true }).catch(() => {});
  return file;
}

// Sichtbaren Text und Links einer Seite liefern (Fallback, falls sich das Layout ändert).
export async function pageText(page, maxChars = 20000) {
  const text = await page.evaluate(() => document.body?.innerText || '');
  const links = await page.evaluate(() =>
    [...document.querySelectorAll('a[href]')].map(a => ({ text: a.innerText.trim().slice(0, 120), href: a.href }))
      .filter(l => l.text)
  );
  return { url: page.url(), title: await page.title(), text: text.slice(0, maxChars), links: links.slice(0, 300) };
}

// Artikel aus einer Liste herauslesen: Ricardo-Artikel-URLs enden auf -<ID>/.
export async function extractArticles(page) {
  // Lazy-Loading: einmal durchscrollen.
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 800) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 150));
    }
  });
  return page.evaluate(() => {
    const out = new Map();
    for (const a of document.querySelectorAll('a[href*="/a/"]')) {
      const m = a.href.match(/\/a\/[^/?#]*?-?(\d{6,})\/?/);
      if (!m) continue;
      const id = m[1];
      // Die nächste "Karte" um den Link herum enthält Titel, Preis, Gebote usw.
      let card = a;
      for (let i = 0; i < 6 && card.parentElement; i++) {
        card = card.parentElement;
        if (card.innerText && card.innerText.split('\n').length >= 3) break;
      }
      const lines = (card.innerText || a.innerText || '').split('\n').map(s => s.trim()).filter(Boolean);
      const prev = out.get(id);
      if (prev && prev.details.length >= lines.length) continue;
      const price = lines.find(l => /CHF|Fr\.|\d+[.,]\d{2}/.test(l)) || null;
      out.set(id, {
        id,
        url: a.href.split('?')[0],
        title: (a.innerText.trim() || lines[0] || '').slice(0, 200),
        price,
        details: lines.slice(0, 15),
        image: card.querySelector('img')?.src || null,
      });
    }
    return [...out.values()];
  });
}
