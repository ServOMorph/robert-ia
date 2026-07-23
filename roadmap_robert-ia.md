# Roadmap — Robert-IA
Objectif : Déployer une IA locale conversationnelle en espace associatif (air-gap, sessions anonymes, données 100 % locales)
Créée le : 2026-06-18

---

## Phase 1 — Socle projet [DONE]
- [x] Initialiser le repo GitHub public (MIT)
- [x] Mettre en place la structure de dossiers (backend, frontend, docs, context)
- [x] Appliquer le protocole vibecoding (start/close)
- [x] Configurer l'environnement de dev (Python + FastAPI + Ollama)
- [x] Polir le repo public (README, CONTRIBUTING, LICENSE, .gitignore)

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 2 — Interface et chat [DONE]
- [x] Développer l'écran d'accueil + consentement RGPD
- [x] Saisie du pseudo (session anonyme)
- [x] Interface de chat (appel Ollama via FastAPI)
- [x] Historique de session (SQLite)
- [x] Interface verrouillée (aucune config utilisateur)
- [x] Tests automatiques + documentation tests manuels

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 3 — Déploiement air-gap [DONE]
- [x] Compiler le frontend (build statique) — dist/ 149 kB JS + 8.96 kB CSS
- [x] Script de packaging complet (app + modèle Ollama + SQLite) sur disque dur — setup-airgap.sh
- [x] Écrire le protocole d'export données air-gap (récupération SQLite par disque dur) — PROTOCOLE_EXPORT_DONNEES.md
- [x] Configuration démarrage automatique (service systemd + navigateur kiosk) — start-kiosk.sh + robert-ia.service
- [x] Documentation complète (installation 7 phases + troubleshooting) — GUIDE_INSTALLATION_AIRGAP.md

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 4 — Pré-déploiement [EN COURS]

Pré-requis à lever avant l'installation au Bistrot (signals P2b, P2c, P3).

### P2c — Validation test mini RAG [FAIT]
- [x] Récupération du log `test_rag_20260622_205007.txt` via SSH (hostname mDNS)
- [x] Validation manuelle des 3 réponses (Paris / horaires L'Invariable / refus météo) — conformes 2026-07-23

### P2b — Bandeau eau économisée [PRESQUE FAIT]

**Décision finale (révisée en cours de session, 2026-07-23) :** total cumulé jamais remis à
zéro (pas un compteur par session comme prévu initialement), calculé côté backend à partir de
`robert.db`, affiché à la fois sur l'écran d'accueil et dans le bandeau du chat.

- Backend : `GET /api/water-stats` (`database.count_user_messages()` × `WATER_LITERS_PER_REQUEST`)
- Constante : `0,3 L par requête` (estimation prudente ; bornes documentées : Google 0,26 ml
  refroidissement direct seul / UC Riverside ~0,5 L refroidissement + production électrique)
- Frontend : `App.jsx` fetch le total au démarrage et l'incrémente localement à chaque message
  envoyé ; transmis en props à `Welcome.jsx` et `Chat.jsx`
- Bandeau Chat : alternance périodique avec le disclaimer existant, même style (couleur/police)
- Label « estimation » visible dans l'UI

**Étapes :**
- [x] `backend/database.py`, `backend/main.py` : `count_user_messages()`, endpoint `/api/water-stats`
- [x] `frontend/src/utils/water.js` : constante + formatage partagés
- [x] `frontend/src/App.jsx`, `Welcome.jsx`, `Chat.jsx` (+ CSS) : total fetché et affiché aux deux endroits
- [x] Tests : `backend/tests/test_water_stats.py`, `frontend/src/tests/Chat.test.jsx` — passants
- [x] Build + déploiement Linux (scp + restart backend + relance kiosk)
- [x] Fix associé : `Cache-Control: no-cache` sur `index.html` (bug de cache Chromium découvert en cours de route)
- [ ] Validation visuelle finale par l'utilisateur sur le kiosk (dernier fix de style déployé, retour en attente)

### P3 — Durcissement SSH [TODO]
- [ ] `PermitRootLogin no` dans `sshd_config` + `systemctl restart ssh`
- [ ] Vérifier que l'accès root SSH est bien refusé

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer. Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

---

## Phase 5 — Déploiement pilote [TODO]
- [ ] Installation sur le PC de l'association (Bistrot de Nérigean)
- [ ] Formation animateurs
- [ ] Visite de suivi J+15 : récupération SQLite + analyse retours
- [ ] Corrections issues du terrain
