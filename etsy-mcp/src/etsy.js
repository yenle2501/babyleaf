import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname } from "node:path";
import { API_BASE, TOKEN_URL, config, requireCredentials } from "./config.js";

export async function loadTokens() {
  try {
    return JSON.parse(await readFile(config.tokenFile, "utf8"));
  } catch {
    return null;
  }
}

export async function saveTokens(raw) {
  const tokens = {
    access_token: raw.access_token,
    refresh_token: raw.refresh_token,
    // 60 s Puffer, damit kein Token mitten im Aufruf abläuft
    expires_at: Date.now() + (raw.expires_in - 60) * 1000,
  };
  await mkdir(dirname(config.tokenFile), { recursive: true });
  await writeFile(config.tokenFile, JSON.stringify(tokens, null, 2), { mode: 0o600 });
  return tokens;
}

export async function requestToken(params) {
  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ client_id: config.keystring, ...params }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`Etsy-Token-Fehler ${res.status}: ${body.error_description ?? body.error ?? JSON.stringify(body)}`);
  }
  return saveTokens(body);
}

/** Etsy-Objekt {amount, divisor, currency_code} → 12.5 */
export function money(m) {
  return m && typeof m.amount === "number" ? m.amount / m.divisor : m;
}

// Formular-Felder: Arrays wie tags/materials/image_ids erwartet Etsy kommagetrennt
function toForm(fields) {
  const form = new URLSearchParams();
  for (const [k, v] of Object.entries(fields)) {
    if (v === undefined) continue;
    form.append(k, Array.isArray(v) ? v.join(",") : String(v));
  }
  return form;
}

export class EtsyClient {
  #tokens = null;
  #shopId = config.shopId || null;

  async accessToken() {
    if (!this.#tokens) this.#tokens = await loadTokens();
    if (!this.#tokens) {
      throw new Error("Noch nicht mit Etsy verbunden. Einmal `npm run login` im Ordner etsy-mcp ausführen.");
    }
    if (Date.now() >= this.#tokens.expires_at) {
      this.#tokens = await requestToken({ grant_type: "refresh_token", refresh_token: this.#tokens.refresh_token });
    }
    return this.#tokens.access_token;
  }

  /** Etsy-Access-Tokens beginnen mit der numerischen User-ID: "12345678.abc…" */
  async userId() {
    return (await this.accessToken()).split(".")[0];
  }

  async request(method, path, { query, form, json, multipart, auth = true } = {}) {
    requireCredentials();
    const url = new URL(API_BASE + path);
    for (const [k, v] of Object.entries(query ?? {})) {
      if (v === undefined || v === null) continue;
      url.searchParams.set(k, Array.isArray(v) ? v.join(",") : String(v));
    }
    const headers = { "x-api-key": `${config.keystring}:${config.sharedSecret}` };
    if (auth) headers.Authorization = `Bearer ${await this.accessToken()}`;
    let body;
    if (form) {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
      body = toForm(form);
    } else if (json) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(json);
    } else if (multipart) {
      body = multipart;
    }

    const res = await fetch(url, { method, headers, body });
    if (res.status === 204) return { ok: true };
    const text = await res.text();
    let data;
    try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
    if (!res.ok) {
      const msg = data.error ?? data.error_description ?? text;
      throw new Error(`Etsy ${method} ${path} → ${res.status}: ${msg}`);
    }
    return data;
  }

  async shopId() {
    if (this.#shopId) return this.#shopId;
    // getMe liefert die shop_id des eingeloggten Kontos
    const me = await this.request("GET", "/users/me");
    if (!me.shop_id) throw new Error("Das eingeloggte Etsy-Konto hat keinen Shop.");
    this.#shopId = String(me.shop_id);
    return this.#shopId;
  }
}
