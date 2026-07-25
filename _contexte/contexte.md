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
Phases 1–4 complètes. Phase 5 "Déploiement pilote" (Bistrot de Nérigean) à démarrer. Contexte de production confirmé sur `ROBERT_CONTEXT=moulin_du_sud` (décision explicite, pas de bascule vers `invariable`). Écran d'accueil : bandeau eau économisée refondu en badge visuel dédié avec bouton "Plus d'infos" (modale explicative), déployé sur Linux mais pas encore testé en conditions réelles sur le kiosk. Mini RAG remplacé par un système multi-contextes (`backend/contexts/*.txt` + `ROBERT_CONTEXT`). Accès SSH root désactivé : connexion via user `robert-ia` (sudo NOPASSWD).

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-22 : Claude Code prend le contrôle SSH du Linux automatiquement (instruction dans .claude/CLAUDE.md)
- 2026-06-22 : Protocole Windows→Linux — toute modification fichier applicatif faite sur Windows d'abord, puis déployée via scp (instruction dans .claude/CLAUDE.md)
- 2026-07-23 : Réseau Windows↔Linux migré du partage ICS (192.168.137.x) vers switch/Freebox (192.168.1.x) — SSH/scp utilisent le hostname mDNS `robert-ia-H81M-S2PV.local` plutôt qu'une IP en dur
- 2026-07-23 : P2b finalisé — total cumulé (jamais reset) plutôt que compteur par session : `GET /api/water-stats` compte les messages user en base, affiché sur Welcome + bandeau Chat (style aligné sur le disclaimer)
- 2026-07-23 : Fix `Cache-Control: no-cache` sur index.html — évite que Chromium reste figé sur un ancien build après déploiement (bug découvert lors du debug kiosk)
- 2026-07-25 : P3 finalisé — `PermitRootLogin no`, user `robert-ia` + sudo NOPASSWD:ALL pour préserver le contrôle SSH automatique de Claude Code (commandes CLAUDE.md mises à jour)
- 2026-07-25 : Mini RAG remplacé par système multi-contextes — `backend/contexts/<nom>.txt` (champs nom/lieu/type + connaissance), sélection via `ROBERT_CONTEXT`, gabarit de prompt générique dans `prompt.py`
- 2026-07-25 : Version app affichée dynamiquement sur l'écran d'accueil (`vite.config.js` define depuis `package.json`) — évite toute valeur codée en dur, se met à jour automatiquement à chaque bump
- 2026-07-25 : Contexte de production confirmé sur `moulin_du_sud` (pas de bascule vers `invariable` avant Phase 5)
- 2026-07-25 : Bandeau eau économisée refondu en badge dédié + bouton "Plus d'infos" ouvrant une modale explicative sur la méthode d'estimation
