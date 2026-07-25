# Signals — robert-ia   (MAJ 2026-07-25 — session 22)

## Actions ouvertes
- [P1] Tester l'écran d'accueil (nouveau bandeau eau + modale "plus d'infos") sur le kiosk
  fait quand: validation visuelle par l'utilisateur du badge eau et de la modale explicative en conditions réelles (Linux/Chromium kiosk)
  réf: frontend/src/screens/Welcome.jsx, frontend/src/screens/Welcome.css
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
- **PROD confirmée en `ROBERT_CONTEXT=moulin_du_sud`** — décision explicite de l'utilisateur (2026-07-25), gardée en l'état pour Phase 5
- Branche `v1.1` mergée (fast-forward) dans `main` et poussées toutes les deux sur le remote GitHub
- Version app affichée dynamiquement sur l'écran d'accueil, lue depuis `frontend/package.json` via `define: __APP_VERSION__` dans `vite.config.js` — actuellement `1.1.0`
- Bandeau eau économisée refondu en badge dédié (fond/bordure/couleur `--water-*`) + bouton "Plus d'infos" ouvrant une modale explicative (méthode d'estimation 0,3 L/message)
- Frontend rebuild + redéployé sur Linux (`/opt/robert-ia/app/frontend/dist/`), service `robert-ia` redémarré — scp récursif complet impossible (2 fichiers `.png` appartenant à root dans `dist/`), copie ciblée `index.html` + `assets/` utilisée en contournement

## Dernière session (2026-07-25 — session 22)

### Décisions prises
- Contexte de production confirmé sur `moulin_du_sud` (pas de bascule vers `invariable`)
- Refonte du bandeau eau économisée de l'écran d'accueil en badge visuel dédié (maquette validée avant implémentation)
- Ajout d'un bouton "Plus d'infos" sur ce badge, ouvrant une modale expliquant la méthode d'estimation de l'eau économisée
- Déploiement immédiat en production après validation

### Livrables produits ou modifiés
- `frontend/src/screens/Welcome.jsx` : badge eau (chiffre + libellé) + bouton "Plus d'infos" + modale explicative
- `frontend/src/screens/Welcome.css` : styles badge eau + overlay/modale (`water-info-*`)
- `frontend/src/styles/variables.css` : nouvelles variables `--water-bg`, `--water-border`, `--water-accent` (clair + sombre)
- Déploiement Linux : `dist/index.html` + `dist/assets/` mis à jour sur `/opt/robert-ia/app/frontend/dist/`, service redémarré

### Hypothèses validées / invalidées
- VALIDE : les 5 tests existants de `Welcome.test.jsx` passent après modification
- VALIDE : build Vite sans erreur
- EN ATTENTE : validation visuelle de l'écran d'accueil sur le kiosk réel (Linux/Chromium) — pas encore testée en conditions réelles

### Prochaine étape exacte
Tester l'écran d'accueil (badge eau + modale) sur le kiosk en conditions réelles. Puis poursuivre Phase 5 ou traiter le bug `App.test.jsx` / assets orphelins si priorisé avant.

### Question bloquante pour la session suivante
Aucune
