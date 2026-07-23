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

### P2b — Bandeau eau économisée [EN COURS]

Feature frontend uniquement. Le compteur se calcule côté client à partir des messages
utilisateur de la session. Aucune modification backend. Sessions anonymes : le compteur
repart de 0 à chaque nouvelle session (cohérent avec l'architecture existante).

**Décisions verrouillées (2026-07-23) :**
- Affichage : compteur dynamique, s'incrémente à chaque message envoyé
- Emplacement : bandeau `chat-header`, en alternance périodique avec le disclaimer existant
  (« Robert peut faire des erreurs… ») — le disclaimer n'est PAS supprimé
- Constante : `0,3 L par requête` (estimation prudente ; bornes documentées : Google 0,26 ml
  refroidissement direct seul / UC Riverside ~0,5 L refroidissement + production électrique)
- Label « estimation » visible dans l'UI pour honnêteté

**Étapes :**
- [ ] `frontend/src/screens/Chat.jsx` :
  - constante `WATER_LITERS_PER_REQUEST = 0.3` (commentaire : source + statut estimation)
  - compteur = (nombre de messages `role: 'user'`) × constante
  - état `bannerMode` alternant `'disclaimer'` ↔ `'water'` via `setInterval` (période ~8 s, constante nommée)
  - rendu conditionnel dans `chat-header` : disclaimer OU ligne eau
    (format `~X,X L` — 1 décimale, virgule française — + mention « estimation »)
- [ ] `frontend/src/screens/Chat.css` :
  - style de la ligne eau (icône goutte, couleur), transition douce sur l'alternance
  - vérifier que la hauteur du bandeau ne saute pas entre les deux modes
- [ ] Tests `frontend/src/tests/App.test.jsx` :
  - présence du texte eau dans le bandeau
  - incrémentation du compteur après envoi de N messages
- [ ] Build : `npm run build` dans `frontend/` → `dist/`
- [ ] Déploiement Linux (protocole Windows→Linux) :
  - `scp` du `dist/` vers `/opt/robert-ia/app/frontend/dist/`
  - `systemctl restart robert-ia` (purge cache statique) + vérification visuelle kiosk
- [ ] Validation visuelle : alternance visible, compteur correct, label « estimation » présent

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
