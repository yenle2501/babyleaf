#!/usr/bin/env node
// Einmaliger Login im sichtbaren Browser: `npm run login`. Die Session bleibt im Profil gespeichert.
import { login } from './browser.js';

console.log('Browser öffnet sich. Falls eine Captcha oder ein Code kommt, bitte von Hand erledigen (max. 3 Minuten).');
const result = await login({ interactive: true });
console.log(result.loggedIn ? 'Eingeloggt. Session gespeichert.' : `Login nicht abgeschlossen: ${JSON.stringify(result)}`);
process.exit(result.loggedIn ? 0 : 1);
