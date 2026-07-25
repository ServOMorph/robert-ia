# Signals — robert-ia   (MAJ 2026-07-25 — session 23)

## Actions ouvertes
- [P1] Phase 5 — Déploiement pilote Bistrot de Nérigean (validation kiosk faite, prête à démarrer)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
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
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Multi-contexte : mini RAG remplacé par système multi-lieux (`backend/contexts/*.txt`, variable `ROBERT_CONTEXT`)
- **PROD confirmée en `ROBERT_CONTEXT=moulin_du_sud`** — décision explicite de l'utilisateur (2026-07-25), gardée en l'état pour Phase 5
- Version app affichée dynamiquement sur l'écran d'accueil, lue depuis `frontend/package.json` via `define: __APP_VERSION__` dans `vite.config.js` — actuellement `1.1.0`
- Badge eau économisée + modale "Plus d'infos" validés visuellement par l'utilisateur sur le kiosk réel (Linux/Chromium) — Phase 5 débloquée
- Suite de tests frontend intégralement verte (17/17) : bug `App.test.jsx` corrigé (voir session 23)

## Dernière session (2026-07-25 — session 23)

### Décisions prises
- Validation visuelle du badge eau + modale "Plus d'infos" sur le kiosk réel — clôture de l'action P1 associée
- Correction du bug `App.test.jsx` traitée dans la foulée (priorisée avant Phase 5)

### Livrables produits ou modifiés
- `frontend/src/tests/App.test.jsx` : mock de `fetch` (`/api/ready`, `/api/water-stats`) + `waitFor` pour attendre la transition Loading → Welcome avant les assertions

### Hypothèses validées / invalidées
- VALIDE : le bug n'était pas dans `App.jsx` — les tests rendaient `<App/>` sans mocker `fetch` ni attendre la transition asynchrone Loading → Welcome (setTimeout 1s + fetch `/api/ready`), donc les assertions s'exécutaient pendant que l'écran Loading était encore affiché
- VALIDE : les 17 tests frontend passent (4 fichiers), aucune régression

### Prochaine étape exacte
Démarrer Phase 5 : installation sur le PC de l'association (Bistrot de Nérigean) + formation animateurs.

### Question bloquante pour la session suivante
Aucune
