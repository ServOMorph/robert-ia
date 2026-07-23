# Signals — robert-ia   (MAJ 2026-07-23)

## Actions ouvertes
- [P1] Phase 5 — Déploiement pilote Bistrot de Nérigean (à venir, après Phase 4)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
- [P2b] PRESQUE FAIT : bandeau eau économisée — total cumulé (jamais reset) via `GET /api/water-stats`, affiché sur Welcome + bandeau Chat, style aligné sur le disclaimer
  fait quand: confirmation visuelle finale de l'utilisateur sur le kiosk (couleur/police corrigées, dernier redéploiement en attente de retour)
  réf: roadmap_robert-ia.md (Phase 4 > P2b), backend/main.py (water-stats), frontend/src/utils/water.js, App.jsx, Welcome.jsx, Chat.jsx
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)
  fait quand: `PermitRootLogin no` dans sshd_config + service redémarré + accès root vérifié refusé
  réf: contexte.md (accès SSH root actif, clé robert-ia_ed25519), roadmap_robert-ia.md (Phase 4 > P3)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root actif (clé C:\Users\raph6\.ssh\robert-ia_ed25519, hostname mDNS robert-ia-H81M-S2PV.local, user root) — réseau via switch relié à la Freebox (192.168.1.x, IP DHCP non fixe), hostname mDNS utilisé partout pour rester stable
- Claude Code prend le contrôle Linux automatiquement via SSH (instructions dans .claude/CLAUDE.md)
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Mini RAG déployé : knowledge.txt injecté dans system prompt — knowledge.txt à enrichir si nouvelles infos association
- test_rag.py : validation manuelle faite 2026-07-23, 3 réponses conformes — P2c clos
- P2b : implémenté en total cumulé (backend `/api/water-stats`), déployé sur Linux, 9,0 L déjà comptabilisés (30 messages historiques réels) — dernier fix de style (couleur/police) déployé, en attente de confirmation visuelle utilisateur
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html (avant : purge manuelle du cache nécessaire à chaque déploiement frontend)

## Dernière session (2026-07-23 — session 18, suite 2)

### Décisions prises
- P2b : portée finale = total cumulé (jamais reset), pas un compteur par session — affiché sur Welcome ET dans le bandeau Chat
- Fix Cache-Control no-cache sur index.html (bug de cache Chromium découvert en cours de session)
- Style bandeau eau aligné sur le disclaimer existant (même couleur, même police italique)

### Livrables produits ou modifiés
- `backend/database.py`, `backend/main.py` : `count_user_messages()`, endpoint `GET /api/water-stats`, header no-cache
- `frontend/src/utils/water.js` (nouveau), `App.jsx`, `Welcome.jsx`, `Chat.jsx` (+ CSS) : total cumulé fetché et affiché
- `backend/tests/test_water_stats.py`, `frontend/src/tests/Chat.test.jsx` : tests ajoutés/mis à jour
- Déployé sur Linux (scp + restart backend + kiosk relancé)

### Hypothèses validées / invalidées
- VALIDE : total cumulé fonctionnel en production (9,0 L, 30 messages historiques réels)
- VALIDE : tests backend (14/15, 1 échec préexistant confirmé sans lien) et frontend passants
- INVALIDE (auto-corrigée) : régression introduite sur Welcome.jsx (crash sans prop waterLiters) → fixée avant de conclure

### Prochaine étape exacte
Attendre confirmation visuelle de l'utilisateur sur le kiosk (style bandeau eau corrigé). Si OK → P2b clos → passer à P3 (retrait accès root SSH).

### Question bloquante pour la session suivante
Aucune
