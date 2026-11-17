# sunnozy – Hinweise für Claude

Inhalte für die Babykleidungs-Marke sunnozy liegen in `sunnozy-content/`.
- Markenleitfaden: `sunnozy-content/marke.md`
- Ordnerstruktur der Posts: `sunnozy-content/posts/README.md`

## Reels

- **Musik:** Für alle Reels den Standard-Track `sunnozy-content/posts/coming-soon/reels/musik/alex-morgan_no-copyright-music.mp3` nehmen (Alex Morgan, lizenzfrei). Das wünscht die Nutzerin seit dem 17.11.2026. Einen anderen Track nur nehmen, wenn sie es ausdrücklich verlangt. Details: `musik/README.md`.
- **Text-Stil, den die Nutzerin mag:**
  - eine kurze POV-Zeile in weisser Schreibmaschinenschrift (`fonts/courierprime.ttf`) mit Emoji
  - Video in voller Grösse, Text nur am Anfang und zum Loop am Ende
  - Länge 9–12 s
  - Vorlage: `tools/make_reel_hello_little_bear_hook.py`
- **Preis:** In Coming-soon-Reels nie einen Preis zeigen.
- **Inhalt:**
  - Hook ab dem ersten Bild
  - ein klarer Empfänger zum Teilen (Gotti, Grosi, Freundin)
  - Grundlage: `posts/content-plan/viral-analyse/README.md`
- **Beim Posten:** immer «Mit KI erstellt» einschalten, höchstens 5 Hashtags.

## Allgemein

- **Sprache:** Deutsch, Schweizer Schreibweise (ss statt ß), Du-Form.
- **Nachfragen:** Nicht nachfragen, einfach machen.
- **Keine Artikelnummern.**
- **Safe Sleep:** Babys in unseren Bildern sind wach, liegen auf dem Rücken, und es liegt kein Kuscheltier, keine Decke und kein Haarband im Bett.
- **Fremde Inhalte:**
  - Keine fremden Marken.
  - Fremde Fotos nie hochladen, nur ihren Stil im Prompt beschreiben.
  - Echte Fotos der Nutzerin nicht in Reels einbauen.
- **Ehrlichkeit:**
  - Keine erfundenen Bewertungen.
  - Keine ungeprüften Werbeaussagen. Zum Beispiel: «verschickt aus der Schweiz», nicht «aus der Schweiz».
- **Shopify:** nie ins Live-Theme schreiben.
- **Git:** Committen und pushen auf den vorgegebenen Branch. Grosse Commits in Teile von etwa 300 Dateien aufteilen, sonst schlägt der Push fehl (HTTP 500).
