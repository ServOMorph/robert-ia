# Contexte — robert-ia

## Objectif (immuable sauf décision explicite)
Déployer une IA locale conversationnelle dans des espaces associatifs (air-gap, sessions anonymes, données 100 % locales). Modèle économique : revenus sur services (déploiement, maintenance, ateliers), code MIT open source.

## Stack / contraintes techniques (stable, rarement modifié)
- OS cible : Ubuntu 24.04.1 LTS (XFCE), machine air-gap (i3-4130, 4 Go RAM, 120 Go)
- IA : Ollama, modèle gemma3:4b (remplace 1b jugé non viable — sous réserve RAM 4 Go)
- Backend : Python + FastAPI
- Base de données : SQLite
- Frontend : React + Vite (build statique)
- Affichage : navigateur kiosk (mono-onglet)
- Déploiement : disque dur (pas de réseau sur site)
- Backup code : GitHub public MIT

## État actuel (réécrit intégralement à chaque /close)
Phases 1–3 complètes. Mémoire conversationnelle intra-session implémentée (session 5) : /api/chat Ollama, fenêtre glissante 8 messages, num_ctx 2048. Modèle changé gemma3:1b → gemma3:4b (1b score 4/20 aux tests mémoire — non viable). RAM 4 Go à valider. 12 tests pytest (dont 3 nouveaux get_history + 4 chat réécrits). Phase 4 déploiement pilote Bistrot de Nérigean en attente validation RAM gemma3:4b.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-18 : Stack Python+FastAPI / SQLite / React+Vite / Ollama gemma3:1b / kiosk browser
- 2026-06-18 : Licence MIT
- 2026-06-18 : v1 sessions anonymes (pseudo, pas de mot de passe) — comptes complets reportés v2
- 2026-06-18 : _contexte/ public dans le repo GitHub
- 2026-06-18 : Backup code = GitHub uniquement (pas de ZIP Drive)
- 2026-06-18 : Protocole d'export données air-gap (SQLite par disque dur) à développer en Phase 3
- 2026-06-18 : Fonts Google exclues de l'UI (air-gap) — fallback système uniquement
- 2026-06-18 : Navigation par machine d'état React (pas de router) — interface verrouillée par design
- 2026-06-18 : Ollama keep_alive -1 + préchargement lifespan — modèle en RAM dès le démarrage du serveur
- 2026-06-19 : Mémoire conversationnelle intra-session — /api/chat, fenêtre 8 messages, num_ctx 2048
- 2026-06-19 : gemma3:1b non viable (mémoire contextuelle insuffisante) → pivot gemma3:4b (RAM à valider)
