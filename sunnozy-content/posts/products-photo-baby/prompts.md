# Baby-Fotos im Handyfoto-Stil (gewünscht 20.10.2026)

Vorbild (nur Stil, Bild NICHT verwendet): Pinterest-Pin 857724691580287486 – Neugeborenes auf zerknitterter weisser
Bettdecke, von oben mit dem Handy fotografiert, Haarband, Plüschtier daneben. Fremde Babyfotos werden aus Rechte-/
Persönlichkeitsgründen nicht verwendet; das Baby ist KI-generiert (fiktiv).

Ablauf je Set:
1. Canva generate-image, Vorlage = `produktfotos-set-praesentation/ki-roh/set_<name>_quadratisch.jpg`, Format 4:5.
2. Export 1136x1408 über Canva-Hilfsdesign DAHX-AebYko (Seiten 84-91, update_fill).
3. Real-ESRGAN x2 + 25 % Lanczos -> 2272x2816 (`tools/hochskalieren_realesrgan.py`).
4. Datei: `<set>/baby_<set>_1.jpg`.

Grundprompt: «Casual authentic smartphone snapshot taken by a parent at home, shot straight from above: a newborn baby
(fictional) ... wearing EXACTLY the <Teil> from the reference image ... rumpled white duvet, plush toy, natural soft
daylight, unstaged, candid Pinterest mom aesthetic, not a studio photo, photorealistic, crisp details, no text, no logos.»
