# Mémoire projet
<!-- Fichier géré via /create_memory. Ne pas modifier manuellement sauf pour supprimer des entrées. -->

## 2026-07-25 — Lancer une app graphique via SSH
Pour lancer une application graphique sur le PC Linux (kiosk Chromium) depuis SSH, passer par le Bash tool, pas par PowerShell : PowerShell mange les backticks et `$()`, qui sont interprétés comme de l'échappement PowerShell au lieu d'être transmis à bash comme substitutions de commande.

## 2026-07-25 — Détecter le kiosk avec pgrep/pkill
Sur le PC Linux, utiliser `pgrep -f "[c]hromium.*--kiosk"` et non `pgrep -f "chromium.*--kiosk"` : sans les crochets, le motif matche le `bash -c` qui exécute la commande elle-même. Conséquences observées : faux positifs (un PID différent à chaque appel, alors que le kiosk est arrêté) et `pkill` qui tue sa propre session SSH, d'où un exit code 255.

## 2026-07-25 — Relancer le kiosk sous Wayland
La session graphique du PC Linux est en Wayland : `DISPLAY=:0` ne fonctionne pas et Chromium sort immédiatement avec `Missing X server or $DISPLAY`. Commande qui fonctionne (via le Bash tool) :
`setsid env XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland /opt/robert-ia/scripts/start-kiosk.sh > /tmp/kiosk.log 2>&1 < /dev/null & disown`
`setsid` + `disown` sont nécessaires : avec un simple `nohup ... &`, le process meurt à la fermeture de la session SSH.
