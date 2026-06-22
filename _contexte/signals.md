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
- [P2c] AVANT DÉPLOIEMENT : valider manuellement les résultats du test mini RAG
  fait quand: utilisateur confirme que les 3 réponses du test_rag.py sont conformes (culture générale / association / refus internet)
  réf: scripts/test_rag.py, log Linux : /opt/robert-ia/app/logs/test_rag_20260622_205007.txt
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)
  fait quand: `PermitRootLogin no` dans sshd_config + service redémarré + accès root vérifié refusé
  réf: contexte.md (accès SSH root actif, clé robert-ia_ed25519)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root actif (clé C:\Users\raph6\.ssh\robert-ia_ed25519, IP 192.168.137.85, user root)
- Claude Code prend le contrôle Linux automatiquement via SSH (instructions dans .claude/CLAUDE.md)
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Mini RAG déployé : knowledge.txt injecté dans system prompt — knowledge.txt à enrichir si nouvelles infos association
- test_rag.py déployé sur Linux — log test du 2026-06-22 : /opt/robert-ia/app/logs/test_rag_20260622_205007.txt

## Dernière session (2026-06-22 — session 17)

### Décisions prises
- test_rag.py : script de test automatique mini RAG créé et déployé sur Linux

### Livrables produits ou modifiés
- `scripts/test_rag.py` : créé — test 3 niveaux mini RAG via Ollama, log dans logs/

### Hypothèses validées / invalidées
- EN ATTENTE : résultats du test_rag.py à valider manuellement par l'utilisateur (session suivante)
- VALIDE (technique) : script exécuté sur Linux sans erreur, 3 réponses obtenues

### Prochaine étape exacte
Valider manuellement les 3 réponses du test_rag.py (log : /opt/robert-ia/app/logs/test_rag_20260622_205007.txt).
Si OK → P2c fermé → passer à P2b (feature eau économisée).

### Question bloquante pour la session suivante
Aucune
