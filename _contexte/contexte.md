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
Phases 1–3 complètes. Phase 4 en cours. Démarrage automatique validé : GDM3 auto-login + Chromium kiosk + backend systemd. Feature inactivité déployée. Optimisations RAM appliquées. Mini RAG déployé : knowledge.txt (infos L'Invariable) injecté dans system prompt — 3 niveaux de réponse (culture générale / association / pas d'internet). Protocole Windows→Linux établi. Avant déploiement Bistrot : test mini RAG (P2c), feature eau économisée (P2b), retrait accès root SSH (P3).

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-20 : GDM3 auto-login robert-ia + accès root SSH temporaire Windows→Linux (192.168.137.85) pour dev
- 2026-06-21 : OS réel = GNOME Shell / Wayland (Ubuntu 24.04 par défaut, pas XFCE) — fond d'écran via gsettings
- 2026-06-21 : Dev frontend Windows : override ?screen=<nom> en mode DEV (import.meta.env.DEV) + python dev.py
- 2026-06-21 : Lifespan warmup via /api/generate + num_predict:0 (charge modèle en RAM sans génération) — /api/ready via /api/ps
- 2026-06-21 : Feature inactivité — modale après 10 min sans message, countdown 30s, retour accueil automatique
- 2026-06-21 : RustDesk autostart via rustdesk.service (enabled, multi-user.target) — daemon-reload requis après màj fichier service
- 2026-06-21 : Frontend déployé dans /opt/robert-ia/app/frontend/dist/ (pas /opt/robert-ia/frontend/dist/)
- 2026-06-22 : Claude Code prend le contrôle SSH du Linux automatiquement (instruction dans .claude/CLAUDE.md) — clé robert-ia_ed25519, IP 192.168.137.85, user root
- 2026-06-22 : Protocole Windows→Linux — toute modification fichier applicatif faite sur Windows d'abord, puis déployée via scp (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Mini RAG — knowledge.txt injecté dans system prompt au démarrage, 3 niveaux de réponse (culture générale / association / refus météo+internet)
