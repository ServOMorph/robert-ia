# Signals — robert-ia   (MAJ 2026-06-20)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
- [P1] Écran de chargement : `/api/ready` retourne true trop tôt — loading screen s'efface avant que le modèle soit réellement prêt, premier prompt lent
- [P2] Corriger hallucination des chiffres précis (budget 200€ → modèle invente 500€, 5000€)
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)

## Questions ouvertes
- /api/ready retourne true via /api/ps mais premier prompt est lent — lifespan ne précharge pas réellement, ou /api/ps ment sur l'état RAM ?
- Hallucination chiffres : accepter 18/20 ou corriger avant déploiement pilote ?

## Échéances

## Blocages

## Contexte chaud
- Session 8 (2026-06-20) : accès SSH root temporaire depuis Windows → PC Linux (192.168.137.85)
- Firefox kiosk auto-launch validé (XFCE autostart + GDM3 auto-login)
- Chat Robert fonctionnel au reboot, mais écran de chargement non fonctionnel (/api/ready trop rapide)
- Accès root SSH accordé temporairement pour dev (à retirer avant site)

## Dernière session (2026-06-20 — session 8)

### Décisions prises
- Accès root SSH accordé temporairement sur PC Linux pour la phase dev (à retirer avant déploiement)
- Architecture split : backend (systemd) / Firefox kiosk (XFCE autostart .desktop)
- GDM3 auto-login configuré pour l'utilisateur robert-ia

### Livrables produits ou modifiés
- `scripts/start-backend.sh` : nouveau — démarre uvicorn via exec (systemd track le PID)
- `scripts/start-kiosk.sh` : modifié — Firefox only, attend /health, http://localhost:8001
- `config/robert-ia.service` : modifié — Restart=always, pas de DISPLAY/XAUTHORITY
- `config/robert-ia-kiosk.desktop` : nouveau — XFCE autostart pour Firefox
- `backend/main.py` : ajout endpoint /api/ready (check Ollama /api/ps)
- `frontend/src/screens/Loading.jsx` + `Loading.css` : nouveau — écran de chargement
- `frontend/src/App.jsx` : modifié — état initial LOADING

### Hypothèses validées / invalidées
- VALIDE : GDM3 auto-login fonctionne (plus d'écran de connexion au boot)
- VALIDE : Firefox kiosk se lance automatiquement via XFCE autostart
- VALIDE : Chat Robert fonctionnel sur PC Linux (gemma3:4b, port 8001)
- INVALIDE : /api/ready retourne true trop tôt — loading screen s'efface avant que le modèle soit en RAM

### Prochaine étape exacte
Déboguer /api/ready : identifier pourquoi l'endpoint retourne true alors que le modèle n'est pas encore
opérationnel, puis corriger pour que l'écran de chargement reste actif jusqu'au premier token possible.

### Question bloquante pour la session suivante
/api/ready retourne true via /api/ps mais le premier prompt est lent — est-ce que le lifespan
ne précharge pas réellement le modèle en RAM, ou /api/ps ment sur l'état du modèle ?
