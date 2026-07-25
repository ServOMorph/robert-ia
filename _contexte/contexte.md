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
Phases 1–4 complètes. Phase 5 "Déploiement pilote" — borne mobile : le PC Linux lui-même est déplacé de lieu en lieu (aucune installation sur un PC tiers), actuellement en démo au Moulin du Sud (`ROBERT_CONTEXT=moulin_du_sud`). Reste : formation animateurs + visite de suivi J+15. Badge eau, modale "Plus d'infos" et suggestions de questions cliquables (3 par contexte, sur une ligne) validés/déployés en prod, kiosk vérifié stable. Suite de tests frontend intégralement verte (20/20). Environnement de dev Windows fonctionnel (`backend/venv`, `run.py`). Accès SSH root désactivé : connexion via user `robert-ia` (sudo NOPASSWD).

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-07-25 : P3 finalisé — `PermitRootLogin no`, user `robert-ia` + sudo NOPASSWD:ALL pour préserver le contrôle SSH automatique de Claude Code (commandes CLAUDE.md mises à jour)
- 2026-07-25 : Mini RAG remplacé par système multi-contextes — `backend/contexts/<nom>.txt` (champs nom/lieu/type + connaissance), sélection via `ROBERT_CONTEXT`, gabarit de prompt générique dans `prompt.py`
- 2026-07-25 : Version app affichée dynamiquement sur l'écran d'accueil (`vite.config.js` define depuis `package.json`) — évite toute valeur codée en dur, se met à jour automatiquement à chaque bump
- 2026-07-25 : Contexte de production confirmé sur `moulin_du_sud` (pas de bascule vers `invariable` avant Phase 5)
- 2026-07-25 : Bandeau eau économisée refondu en badge dédié + bouton "Plus d'infos" ouvrant une modale explicative sur la méthode d'estimation
- 2026-07-25 : Badge eau + modale validés visuellement sur le kiosk réel — Phase 5 débloquée ; bug `App.test.jsx` corrigé (tests rendaient `<App/>` sans mocker le fetch de `/api/ready`)
- 2026-07-25 : Suggestions de questions cliquables ajoutées à l'écran de chat (`GET /api/suggestions`, 3 par contexte, disparaissent après le premier message) ; pilote confirmé comme borne mobile démarrant au Moulin du Sud (roadmap corrigée, elle indiquait Bistrot de Nérigean)
- 2026-07-25 : Correction — la borne mobile Phase 5 est le PC Linux lui-même déplacé de lieu en lieu, pas une installation sur un PC tiers au Moulin du Sud (roadmap/README/signals corrigés)
- 2026-07-25 : `docs/PHASE3_SUMMARY.md` archivé (`docs/archive/`, bandeau d'avertissement) plutôt que réécrit — contenu obsolète (port 8000, Firefox, gemma3:1b) mais historique préservé
