#!/usr/bin/env node
// Einmaliger OAuth-Login (PKCE): öffnet Etsy im Browser und speichert die Tokens lokal.
import { createServer } from "node:http";
import { randomBytes, createHash } from "node:crypto";
import { exec } from "node:child_process";
import { AUTH_URL, SCOPES, config, requireCredentials } from "./config.js";
import { requestToken } from "./etsy.js";

requireCredentials();

const b64url = (buf) => buf.toString("base64url");
const verifier = b64url(randomBytes(32));
const challenge = b64url(createHash("sha256").update(verifier).digest());
const state = b64url(randomBytes(16));
const redirect = new URL(config.redirectUri);

const authUrl = new URL(AUTH_URL);
authUrl.search = new URLSearchParams({
  response_type: "code",
  client_id: config.keystring,
  redirect_uri: config.redirectUri,
  scope: SCOPES.join(" "),
  state,
  code_challenge: challenge,
  code_challenge_method: "S256",
}).toString();

const server = createServer(async (req, res) => {
  const url = new URL(req.url, config.redirectUri);
  if (url.pathname !== redirect.pathname) {
    res.writeHead(404).end();
    return;
  }
  const finish = (status, text) => {
    res.writeHead(status, { "Content-Type": "text/html; charset=utf-8" });
    res.end(`<p style="font-family:sans-serif">${text}</p>`);
    server.close();
  };
  if (url.searchParams.get("state") !== state) return finish(400, "Ungültiger state – bitte Login neu starten.");
  if (url.searchParams.get("error")) return finish(400, `Etsy meldet: ${url.searchParams.get("error_description") ?? url.searchParams.get("error")}`);
  try {
    await requestToken({
      grant_type: "authorization_code",
      redirect_uri: config.redirectUri,
      code: url.searchParams.get("code"),
      code_verifier: verifier,
    });
    console.log(`✓ Verbunden. Tokens gespeichert in ${config.tokenFile}`);
    finish(200, "✓ sunnozy Etsy-MCP ist verbunden. Dieses Fenster kann geschlossen werden.");
  } catch (err) {
    console.error(err.message);
    finish(500, err.message);
    process.exitCode = 1;
  }
});

server.listen(Number(redirect.port) || 80, redirect.hostname, () => {
  console.log("Im Browser bei Etsy anmelden und Zugriff erlauben:\n\n" + authUrl + "\n");
  const opener = process.platform === "darwin" ? "open" : process.platform === "win32" ? 'start ""' : "xdg-open";
  exec(`${opener} "${authUrl}"`, () => {});
});
