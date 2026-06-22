# Signals — robert-ia   (MAJ 2026-06-22)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 4), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
- [P2b] AVANT DÉPLOIEMENT : feature affichage eau économisée (Robert IA locale vs IA cloud) — mise en lumière aspect éco-responsable
  fait quand: compteur eau visible dans l'UI (ex: fin de session ou écran accueil)
  réf: frontend/src/, à préciser (calcul liters/request cloud vs local)
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)
  fait quand: `PermitRootLogin no` dans sshd_config + service redémarré + accès root vérifié refusé
  réf: contexte.md (accès SSH root actif, clé robert-ia_ed25519)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root actif (clé C:\Users\raph6\.ssh\robert-ia_ed25519, IP 192.168.137.85, user root)
- Claude Code prend le contrôle Linux automatiquement via SSH (instrutions dans .claude/CLAUDE.md)
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération/analyse non encore testé end-to-end sur vrai matériel
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation

## Dernière session (2026-06-22 — session 15)

### Décisions prises
- CLAUDE.md : section SSH ajoutée — Claude prend le contrôle du Linux automatiquement sans demander de copier-coller

### Livrables produits ou modifiés
- `.claude/CLAUDE.md` : modifié — section "Contrôle SSH du PC Linux" avec commande, règles, référence doc

### Hypothèses validées / invalidées
- VALIDE : l'info SSH survivait au /close via contexte.md et CONTROLE_SSH_CLAUDE.md — lacune = absence d'instruction automatique dans CLAUDE.md

### Prochaine étape exacte
Tester protocole complet récupération/analyse (arrêt Robert, copie robert.db sur USB, analyse Windows, vérification CSV dans Excel), puis feature eau économisée (P2b).

### Question bloquante pour la session suivante
Aucune
