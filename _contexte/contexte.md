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
Phases 1–3 complètes. Mémoire conversationnelle intra-session optimisée (session 6) : tête épinglée HEAD_K=4 + fenêtre glissante 16 messages, num_ctx 4096, system prompt enrichi (règles mémoire + honnêteté). Score test mémoire : 18/20 (vs 8/20 en session 5). 2 échecs résiduels sur chiffres précis (budget 200€ — hallucination modèle). Test automatique disponible : `python backend/test_manuels/run_test_memoire.py`. Backend actif sur port 8001 (port 8000 en état fantôme Windows). Phase 4 déploiement pilote Bistrot de Nérigean conditionnée à : (1) décision sur les 2 échecs restants, (2) validation RAM gemma3:4b sur i3-4130 4 Go.

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
- 2026-06-20 : Architecture mémoire — tête épinglée K=4 + fenêtre glissante 16 + system prompt enrichi → 18/20
