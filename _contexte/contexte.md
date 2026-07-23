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
Phases 1–3 complètes. Phase 4 "Pré-déploiement" en cours (P2c fait, P2b quasi-fini en attente de validation visuelle finale, P3 à faire) ; Phase 5 "Déploiement pilote" à suivre. Mini RAG déployé et validé. Réseau Windows↔Linux via switch/Freebox, SSH/scp par hostname mDNS `robert-ia-H81M-S2PV.local`. P2b (bandeau eau économisée) implémenté : total cumulé (jamais remis à zéro) calculé côté backend, affiché sur l'accueil et dans le chat.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-21 : Feature inactivité — modale après 10 min sans message, countdown 30s, retour accueil automatique
- 2026-06-21 : RustDesk autostart via rustdesk.service (enabled, multi-user.target) — daemon-reload requis après màj fichier service
- 2026-06-21 : Frontend déployé dans /opt/robert-ia/app/frontend/dist/ (pas /opt/robert-ia/frontend/dist/)
- 2026-06-22 : Claude Code prend le contrôle SSH du Linux automatiquement (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Protocole Windows→Linux — toute modification fichier applicatif faite sur Windows d'abord, puis déployée via scp (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Mini RAG — knowledge.txt injecté dans system prompt au démarrage, 3 niveaux de réponse (culture générale / association / refus météo+internet)
- 2026-07-23 : Réseau Windows↔Linux migré du partage ICS (192.168.137.x) vers switch/Freebox (192.168.1.x) — SSH/scp utilisent le hostname mDNS `robert-ia-H81M-S2PV.local` plutôt qu'une IP en dur
- 2026-07-23 : P2b finalisé — total cumulé (jamais reset) plutôt que compteur par session : `GET /api/water-stats` compte les messages user en base, affiché sur Welcome + bandeau Chat (style aligné sur le disclaimer)
- 2026-07-23 : Fix `Cache-Control: no-cache` sur index.html — évite que Chromium reste figé sur un ancien build après déploiement (bug découvert lors du debug kiosk)
