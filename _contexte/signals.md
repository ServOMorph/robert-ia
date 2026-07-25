# Signals — robert-ia   (MAJ 2026-07-25)

## Actions ouvertes
- [P1] Rebasculer ou confirmer le contexte de production avant toute utilisation par le Bistrot de Nérigean
  fait quand: `ROBERT_CONTEXT` vérifié/remis sur `invariable` avant reprise Phase 5, ou décision explicite documentée de garder `moulin_du_sud`
  réf: config/robert-ia.service (ligne Environment=ROBERT_CONTEXT), backend/contexts/
- [P1] Phase 5 — Déploiement pilote Bistrot de Nérigean (Phase 4 entièrement close, prête à démarrer)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
- [P2] Corriger le bug `App.test.jsx` (3 tests échouent, écran bloqué sur "Démarrage en cours") — préexistant, découvert lors de la vérification post-ajout de la version dynamique, non lié à ce changement
  fait quand: les 3 tests de `src/tests/App.test.jsx` passent
  réf: frontend/src/tests/App.test.jsx, frontend/src/App.jsx
- [P3] Nettoyer les assets orphelins sur le Linux (`assets/index-DgrLPrFD.js`, `assets/index-DlmDLWIN.css`, non référencés depuis un déploiement antérieur)
  fait quand: fichiers supprimés de /opt/robert-ia/app/frontend/dist/assets/ sur le Linux
  réf: /opt/robert-ia/app/frontend/dist/assets/ (Linux)

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root DÉSACTIVÉ (`PermitRootLogin no`) — connexion via user `robert-ia` (clé C:\Users\raph6\.ssh\robert-ia_ed25519, hostname mDNS robert-ia-H81M-S2PV.local), sudo NOPASSWD:ALL configuré (/etc/sudoers.d/robert-ia-nopasswd) pour préserver le contrôle SSH automatique
- Réseau via switch relié à la Freebox (192.168.1.x, IP DHCP non fixe), hostname mDNS utilisé partout pour rester stable
- Claude Code prend le contrôle Linux automatiquement via SSH (instructions dans .claude/CLAUDE.md, commandes mises à jour vers robert-ia@... + sudo)
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- P2b clos : bandeau eau économisée (total cumulé, `/api/water-stats`) validé visuellement par l'utilisateur en production
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Multi-contexte : mini RAG remplacé par système multi-lieux (`backend/contexts/*.txt`, variable `ROBERT_CONTEXT`)
- **PROD actuellement en `ROBERT_CONTEXT=moulin_du_sud`** (pas `invariable`/Nérigean) — choix explicite de l'utilisateur en session, à revérifier avant reprise Phase 5
- Branche `v1.1` mergée (fast-forward) dans `main` et poussées toutes les deux sur le remote GitHub
- Version app affichée dynamiquement sur l'écran d'accueil, lue depuis `frontend/package.json` via `define: __APP_VERSION__` dans `vite.config.js` — actuellement `1.1.0`
- Frontend rebuild + redéployé sur Linux (`/opt/robert-ia/app/frontend/dist/`) avec la version 1.1.0

## Dernière session (2026-07-25 — session 21)

### Décisions prises
- Merge de la branche `v1.1` dans `main` (fast-forward, aucun conflit) après commit préalable des résidus en attente (`MEMORY/`, `.claude/zones.md`) ; push des deux branches
- Affichage de la version du projet sur l'écran d'accueil, généré dynamiquement depuis `package.json` (pas de valeur codée en dur)
- Bump de version `1.0.0` → `1.1.0` suite au merge
- Build frontend + déploiement sur le Linux (index.html + assets/)

### Livrables produits ou modifiés
- `frontend/vite.config.js` : `define: { __APP_VERSION__: JSON.stringify(pkg.version) }` lu depuis `package.json`
- `frontend/src/screens/Welcome.jsx` : affichage `v{__APP_VERSION__}`
- `frontend/src/screens/Welcome.css` : classe `.welcome-version`
- `frontend/package.json` : version `1.1.0`
- Déploiement Linux : `dist/index.html` + `dist/assets/` mis à jour sur `/opt/robert-ia/app/frontend/dist/`

### Hypothèses validées / invalidées
- VALIDE : merge fast-forward sans conflit entre v1.1 et main
- VALIDE : la version s'injecte correctement dans le bundle de build (vérifiée dans le JS compilé)
- INVALIDE (hors périmètre) : les 3 échecs de `App.test.jsx` ne sont pas causés par ce changement — confirmé par test avant/après via `git stash` ; bug préexistant à traiter séparément

### Prochaine étape exacte
Poursuivre Phase 5 (pilote Bistrot de Nérigean) ou traiter le bug `App.test.jsx` / nettoyage des assets orphelins Linux si priorisé avant.

### Question bloquante pour la session suivante
Aucune
