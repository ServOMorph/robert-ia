# Signals — robert-ia   (MAJ 2026-07-23)

## Actions ouvertes
- [P1] Phase 5 — Déploiement pilote Bistrot de Nérigean (à venir, après Phase 4)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
- [P2b] EN COURS : feature bandeau eau économisée — compteur dynamique, alternance avec le disclaimer, 0,3 L/requête (estimation)
  fait quand: Chat.jsx/Chat.css implémentés + tests passants + build + déployé sur Linux (scp + restart) + validation visuelle kiosk
  réf: roadmap_robert-ia.md (Phase 4 > P2b, plan détaillé), frontend/src/screens/Chat.jsx, Chat.css
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
- P2b : constante 0,3 L/requête choisie (borne prudente ; bornes documentées Google 0,26 ml / UC Riverside ~0,5 L) — implémentation reportée session suivante

## Dernière session (2026-07-23 — session 18, suite)

### Décisions prises
- P2c validé : les 3 réponses du test mini RAG sont conformes
- Roadmap restructurée : Phase 4 = "Pré-déploiement" (P2b/P2c/P3), ancien "Déploiement pilote" devient Phase 5
- P2b verrouillé : compteur dynamique (nb messages × 0,3 L), alternance périodique avec le disclaimer existant, label "estimation" dans l'UI

### Livrables produits ou modifiés
- `roadmap_robert-ia.md` : Phase 4 restructurée, P2c marqué [FAIT], plan détaillé P2b (Chat.jsx, Chat.css, tests, build, déploiement)

### Hypothèses validées / invalidées
- VALIDE : test mini RAG conforme (Paris / horaires L'Invariable / refus météo)
- VALIDE : implémentation P2b 100% frontend, aucune modification backend nécessaire

### Prochaine étape exacte
Implémenter P2b : Chat.jsx (constante + logique compteur + alternance bannière), Chat.css (style), tests, build frontend, déploiement scp + restart sur Linux, validation visuelle kiosk.

### Question bloquante pour la session suivante
Aucune
