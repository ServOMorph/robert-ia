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
Phases 1–3 complètes. Phase 4 "Pré-déploiement" en cours (P2c fait, P2b en cours, P3 à faire) ; Phase 5 "Déploiement pilote" à suivre. Mini RAG déployé et validé (test 3 niveaux conforme). Réseau Windows↔Linux via switch/Freebox, SSH/scp par hostname mDNS `robert-ia-H81M-S2PV.local`. P2b (bandeau eau économisée) planifié en détail dans roadmap_robert-ia.md, implémentation reportée à la prochaine session.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-21 : Dev frontend Windows : override ?screen=<nom> en mode DEV (import.meta.env.DEV) + python dev.py
- 2026-06-21 : Dev frontend Windows : override ?screen=<nom> en mode DEV (import.meta.env.DEV) + python dev.py
- 2026-06-21 : Lifespan warmup via /api/generate + num_predict:0 (charge modèle en RAM sans génération) — /api/ready via /api/ps
- 2026-06-21 : Feature inactivité — modale après 10 min sans message, countdown 30s, retour accueil automatique
- 2026-06-21 : RustDesk autostart via rustdesk.service (enabled, multi-user.target) — daemon-reload requis après màj fichier service
- 2026-06-21 : Frontend déployé dans /opt/robert-ia/app/frontend/dist/ (pas /opt/robert-ia/frontend/dist/)
- 2026-06-22 : Claude Code prend le contrôle SSH du Linux automatiquement (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Protocole Windows→Linux — toute modification fichier applicatif faite sur Windows d'abord, puis déployée via scp (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Mini RAG — knowledge.txt injecté dans system prompt au démarrage, 3 niveaux de réponse (culture générale / association / refus météo+internet)
- 2026-07-23 : Réseau Windows↔Linux migré du partage ICS (192.168.137.x) vers switch/Freebox (192.168.1.x) — SSH/scp utilisent le hostname mDNS `robert-ia-H81M-S2PV.local` plutôt qu'une IP en dur
- 2026-07-23 : P2b (bandeau eau) — constante 0,3 L/requête (estimation prudente entre Google 0,26 ml et UC Riverside ~0,5 L), compteur dynamique en alternance avec le disclaimer, 100% frontend
