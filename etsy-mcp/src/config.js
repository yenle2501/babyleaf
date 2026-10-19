import { readFileSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

// .env neben package.json laden (nur Schlüssel, die nicht schon gesetzt sind)
const envFile = join(ROOT, ".env");
if (existsSync(envFile)) {
  for (const line of readFileSync(envFile, "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (!m || line.trim().startsWith("#")) continue;
    const value = m[2].replace(/^["']|["']$/g, "");
    if (process.env[m[1]] === undefined) process.env[m[1]] = value;
  }
}

export const API_BASE = "https://openapi.etsy.com/v3/application";
export const TOKEN_URL = "https://openapi.etsy.com/v3/public/oauth/token";
export const AUTH_URL = "https://www.etsy.com/oauth/connect";

export const SCOPES = [
  "shops_r", "shops_w",
  "listings_r", "listings_w", "listings_d",
  "transactions_r", "transactions_w",
  "profile_r",
];

export const config = {
  keystring: process.env.ETSY_KEYSTRING ?? "",
  sharedSecret: process.env.ETSY_SHARED_SECRET ?? "",
  shopName: process.env.ETSY_SHOP_NAME || "sunnozyCH",
  shopId: process.env.ETSY_SHOP_ID || "",
  redirectUri: process.env.ETSY_REDIRECT_URI || "http://localhost:3003/oauth/redirect",
  tokenFile: process.env.ETSY_TOKEN_FILE || join(homedir(), ".config", "sunnozy-etsy-mcp", "tokens.json"),
  readOnly: ["1", "true", "yes"].includes((process.env.ETSY_READ_ONLY ?? "").toLowerCase()),
};

export function requireCredentials() {
  if (!config.keystring || !config.sharedSecret) {
    throw new Error(
      "ETSY_KEYSTRING und ETSY_SHARED_SECRET fehlen. Beide stehen unter https://www.etsy.com/developers/your-apps " +
      "und gehören in etsy-mcp/.env (siehe .env.example)."
    );
  }
}
