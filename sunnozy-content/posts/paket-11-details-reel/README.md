# Paket 11: Reel «kleine Details»

Vorbild: Instagram-Reel «little details I never want to forget» (Bildschirmaufnahme der Nutzerin, 10 s).

## Analyse Vorbild

- **Format:** 9:16, 10 s, Handykamera, Tageslicht vom Fenster, warme Creme- und Hauttöne, leichtes Wackeln.
- **Aufbau:** 5 sehr nahe Detail-Einstellungen mit harten Schnitten, alle 1–2 s ein Schnitt:
  1. Haare werden mit weicher Babybürste gebürstet (0,5 s)
  2. Gesicht nah, Baby schaut in die Kamera (2,5 s)
  3. Beinchen und Füsse im weissen Strick-Strampler (1,5 s)
  4. Makro: Nase und Mund, Baby gähnt und lächelt (4 s)
  5. Händchen auf der Decke (1 s)
- **Text:** eine Zeile, klein, weisse Serifenschrift in Kleinbuchstaben, mittig. Kein Logo, keine Endkarte.
- **Wirkung:** Nostalgie. «Die Zeit geht so schnell vorbei», darum sind Teilen und Speichern hoch (1004 Reposts, 16 300 Mal gesendet).

## Umsetzung für sunnozy

| # | Datei | Szene | sunnozy-Produkt |
|---|---|---|---|
| 1 | `ki-fotos-9x16/1_haare_buersten.jpg` | Babybürste im Haar | Body «Little One» (Kragen) |
| 2 | `ki-fotos-9x16/2_gesicht.jpg` | Gesicht nah | Strampler «Hello World» mit Blätter-Print |
| 3 | `ki-fotos-9x16/3_fuesschen.jpg` | Füsschen | Strampler «Hello World» |
| 4 | `ki-fotos-9x16/4_gaehnen.jpg` | Makro Gähnen | Mulltuch Blau mit Tieren |
| 5 | `ki-fotos-9x16/5_haendchen.jpg` | Händchen hält Mamas Finger | Body «I Love My Mummy» |
| 6 | `ki-fotos-9x16/6_schlafen.jpg` | schläft im Tuch | Mulltuch Blau mit Tieren |

**Reel:** `reel_kleine_details_9x16.mp4`, 10,6 s, stumm. Text: «kleine Details, die ich nie vergessen will».
Generator: `tools/make_details_reel.py <ausgabe.mp4> <bild/clip> ...`. Mit `--text "..."` lässt sich der Text ändern, z.B. auf Englisch «little details I never want to forget».

**Wichtig:** Die Fotos sind KI-generiert (Canva). Die Babys sind nicht in jeder Szene dasselbe Kind, und es gibt keine echte Bewegung, nur leichtes Heranfahren und Wackeln. Beim Posten das Label «Mit KI erstellt» setzen.

## Caption

> kleine Details, die ich nie vergessen will 🤍 Die ersten Wochen gehen so schnell vorbei. Speichere dir dieses Reel für später.
> Strampler «Hello World», Mulltücher & Nuscheli, Body «I Love My Mummy», alles auf sunnozy.ch
> #sunnozy #newborn #babyschweiz #mamaschweiz #littledetails #neugeboren #babyreels

Ton: einen ruhigen Trend-Sound wählen (Piano, Lo-Fi). Den Originalton aus dem Vorbild suchst du über «Audio verwenden».

## Echte Bewegung mit Google Flow (optional)

Wie bei Paket 8: Jedes Bild in Flow als Startbild («Frames to Video») hochladen, Prompt einfügen, 8 s erzeugen und die Clips schicken. Ich schneide sie dann mit dem gleichen Skript (es nimmt auch .mp4).

| Bild | Prompt (Englisch, für Flow) |
|---|---|
| 1 | Static close-up, handheld phone feel. A mother's hand gently strokes the baby's hair with the soft white brush, two slow strokes. The baby stays calm. Soft daylight, no zoom, no text. |
| 2 | Static close-up, handheld. The newborn blinks slowly, moves the lips a little and turns the head very slightly toward the camera. Natural soft daylight, realistic, no text. |
| 3 | Static close-up of the tiny feet in the romper. The baby gently kicks and wiggles the feet twice, fabric moves naturally. Soft daylight, handheld, no text. |
| 4 | Extreme macro, handheld. The newborn finishes a big yawn, closes the mouth and makes a tiny sleepy smile. Realistic skin, soft daylight, no text. |
| 5 | Macro close-up. The baby's tiny hand squeezes the mother's finger and relaxes again, slight finger movement. Soft daylight, handheld, no text. |
| 6 | Close-up from above. The sleeping newborn breathes calmly, the little hand near the cheek twitches once. Very calm, soft daylight, no text. |
