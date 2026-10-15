# Shopify-Zusatzbilder auf Reinweiss

Alle 284 Bilder der 53 Produkte wurden geprüft (Randfarbe gemessen, dann von Auge):

| Gruppe | Anzahl | Was passiert |
|---|---|---|
| schon reinweiss | 171 | nichts |
| Hauptbilder grau | 22 (+3 neu) | siehe `../shopify-hauptbilder-weiss/` |
| Studiofotos fast weiss (248–252, leicht grau/bläulich) | 41 | `tools/weiss_angleichen.py`: nur Lichter auf 255, Produktfarben unverändert |
| Studiofotos mit grauem/beigem Grund | 6 (5 verschiedene) | `tools/hintergrund_weiss.py` + Canva-Maske |
| Szenen, Babys, Holz, Decken, Nahaufnahmen | 44 | bleiben bewusst so |

Dateiname: `<shopify-handle>_bild<NN>.jpg` (NN = Position im Shop ab 00). Check-Blätter: `../shopify-check_zusatzbilder_1.jpg`, `_2.jpg`.
