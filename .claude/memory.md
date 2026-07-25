# Mémoire projet
<!-- Fichier géré via /create_memory. Ne pas modifier manuellement sauf pour supprimer des entrées. -->

## 2026-07-25 — Lancer une app graphique via SSH
Pour lancer une application graphique sur le PC Linux (kiosk Chromium) depuis SSH, passer par le Bash tool, pas par PowerShell : PowerShell mange les backticks et `$()`, qui sont interprétés comme de l'échappement PowerShell au lieu d'être transmis à bash comme substitutions de commande.

## 2026-07-25 — Détecter le kiosk avec pgrep/pkill
Sur le PC Linux, utiliser `pgrep -f "[c]hromium.*--kiosk"` et non `pgrep -f "chromium.*--kiosk"` : sans les crochets, le motif matche le `bash -c` qui exécute la commande elle-même. Conséquences observées : faux positifs (un PID différent à chaque appel, alors que le kiosk est arrêté) et `pkill` qui tue sa propre session SSH, d'où un exit code 255.
