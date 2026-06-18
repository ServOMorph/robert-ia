# Roadmap — Robert-IA
Objectif : Déployer une IA locale conversationnelle en espace associatif (air-gap, sessions anonymes, données 100 % locales)
Créée le : 2026-06-18

---

## Phase 1 — Socle projet [EN COURS]
- [x] Initialiser le repo GitHub public (MIT)
- [ ] Mettre en place la structure de dossiers (backend, frontend, docs, context)
- [ ] Appliquer le protocole vibecoding (start/close)
- [ ] Configurer l'environnement de dev (Python + FastAPI + Ollama)
- [ ] Polir le repo public (README, CONTRIBUTING, documentation structure)

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 2 — Interface et chat [TODO]
- [ ] Développer l'écran d'accueil + consentement RGPD
- [ ] Saisie du pseudo (session anonyme)
- [ ] Interface de chat (appel Ollama via FastAPI)
- [ ] Historique de session (SQLite)
- [ ] Interface verrouillée (aucune config utilisateur)
- [ ] Tests automatiques + documentation tests manuels

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 3 — Déploiement air-gap [TODO]
- [ ] Compiler le frontend (build statique)
- [ ] Script de packaging complet (app + modèle Ollama + SQLite) sur disque dur
- [ ] Écrire le protocole d'export données air-gap (récupération SQLite par disque dur depuis la machine asso)
- [ ] Tester le déploiement complet depuis disque dur sur machine sans Internet
- [ ] Configurer démarrage automatique (service systemd + navigateur kiosk)

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 4 — Déploiement pilote [TODO]
- [ ] Installation sur le PC de l'association (Bistrot de Nérigean)
- [ ] Formation animateurs
- [ ] Visite de suivi J+15 : récupération SQLite + analyse retours
- [ ] Corrections issues du terrain
