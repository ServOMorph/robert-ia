# Contexte — robert-ia

## Objectif (immuable sauf décision explicite)
Déployer une IA locale conversationnelle dans des espaces associatifs (air-gap, sessions anonymes, données 100 % locales). Modèle économique : revenus sur services (déploiement, maintenance, ateliers), code MIT open source.

## Stack / contraintes techniques (stable, rarement modifié)
- OS cible : Ubuntu 24.04.1 LTS (GNOME Shell / Wayland), machine air-gap (i3-4130, 4 Go RAM, 120 Go)
- IA : Ollama, modèle gemma3:4b (remplace 1b jugé non viable — sous réserve RAM 4 Go)
- Backend : Python + FastAPI
- Base de données : SQLite
- Frontend : React + Vite (build statique)
- Affichage : navigateur kiosk (mono-onglet)
- Déploiement : disque dur (pas de réseau sur site)
- Backup code : GitHub public MIT

## État actuel (réécrit intégralement à chaque /close)
Phases 1–3 complètes. Phase 4 en cours. Démarrage automatique validé : GDM3 auto-login + Firefox kiosk + backend systemd. Protocole récupération/analyse conversations livré (`scripts/analyse_conversations.py` + docs) — non encore testé end-to-end sur vrai matériel. Avant déploiement Bistrot : test protocole récupération (P2), feature eau économisée (P2b), retrait accès root SSH (P3).

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-18 : Ollama keep_alive -1 + préchargement lifespan — modèle en RAM dès le démarrage du serveur
- 2026-06-19 : Mémoire conversationnelle intra-session — /api/chat, fenêtre 8 messages, num_ctx 2048
- 2026-06-19 : gemma3:1b non viable (mémoire contextuelle insuffisante) → pivot gemma3:4b (RAM à valider)
- 2026-06-20 : Architecture mémoire — tête épinglée K=4 + fenêtre glissante 16 + system prompt enrichi → 18/20
- 2026-06-20 : FastAPI sert le frontend statique (StaticFiles) — file:// abandonné, tout sur port 8001
- 2026-06-20 : Architecture split backend (systemd) / Firefox kiosk (GNOME autostart) — Wayland incompatible avec DISPLAY depuis service système
- 2026-06-20 : GDM3 auto-login robert-ia + accès root SSH temporaire Windows→Linux (192.168.137.85) pour dev
- 2026-06-21 : OS réel = GNOME Shell / Wayland (Ubuntu 24.04 par défaut, pas XFCE) — fond d'écran via gsettings
- 2026-06-21 : Dev frontend Windows : override ?screen=<nom> en mode DEV (import.meta.env.DEV) + python dev.py
- 2026-06-21 : Lifespan warmup via /api/generate + num_predict:0 (charge modèle en RAM sans génération) — /api/ready via /api/ps
