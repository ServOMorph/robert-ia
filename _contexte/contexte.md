# Contexte — robert-ia

## Objectif (immuable sauf décision explicite)
Déployer une IA locale conversationnelle dans des espaces associatifs (air-gap, sessions anonymes, données 100 % locales). Modèle économique : revenus sur services (déploiement, maintenance, ateliers), code MIT open source.

## Stack / contraintes techniques (stable, rarement modifié)
- OS cible : Ubuntu 24.04.1 LTS (XFCE), machine air-gap (i3-4130, 4 Go RAM, 120 Go)
- IA : Ollama, modèle gemma3:1b
- Backend : Python + FastAPI
- Base de données : SQLite
- Frontend : React + Vite (build statique)
- Affichage : navigateur kiosk (mono-onglet)
- Déploiement : disque dur (pas de réseau sur site)
- Backup code : GitHub public MIT

## État actuel (réécrit intégralement à chaque /close)
Phase 1 (socle) en cours. Repo GitHub robert-ia créé (MIT). Cadrage complet réalisé : stack décidée, roadmap 4 phases créée. Prochaine étape : structure de dossiers + protocole vibecoding + environnement de dev.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-06-18 : Stack Python+FastAPI / SQLite / React+Vite / Ollama gemma3:1b / kiosk browser
- 2026-06-18 : Licence MIT
- 2026-06-18 : v1 sessions anonymes (pseudo, pas de mot de passe) — comptes complets reportés v2
- 2026-06-18 : _contexte/ public dans le repo GitHub
- 2026-06-18 : Backup code = GitHub uniquement (pas de ZIP Drive)
- 2026-06-18 : Protocole d'export données air-gap (SQLite par disque dur) à développer en Phase 3
