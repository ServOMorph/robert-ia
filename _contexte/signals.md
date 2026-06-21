# Signals — robert-ia   (MAJ 2026-06-21)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
- [P2] Corriger hallucination des chiffres précis (budget 200€ → modèle invente 500€, 5000€)
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)

## Questions ouvertes
- Hallucination chiffres : accepter 18/20 ou corriger avant déploiement pilote ?

## Échéances

## Blocages

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland) — stack corrigé dans contexte.md
- Fond d'écran SérénIA Tech déployé : /home/robert-ia/fond-ecran-serenia.png via gsettings
- Dock GNOME (~60px gauche) masque partiellement le fond d'écran — auto-hide non configuré
- Accès SSH root toujours actif (clé robert-ia_ed25519 fonctionne)
- Projet déployé sur PC Linux : /opt/robert-ia/app/frontend/dist/
- Dev Windows : `python dev.py` + `?screen=loading` pour isoler l'écran de chargement
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, non corrigeable en software — gérée par formation utilisateur

## Dernière session (2026-06-21 — session 11)

### Décisions prises
- Warmup via `/api/generate` + `num_predict: 0` au lieu de `/api/chat` avec `prompt: ""` (requête malformée)
- `/api/ready` reste basé sur `/api/ps` (flag interne abandonné — latence génération incompressible sur ce CPU)
- Lenteur du premier prompt gérée par formation utilisateur, pas par optimisation logicielle

### Livrables produits ou modifiés
- `backend/main.py` : lifespan corrigé (`/api/generate`, `num_predict: 0`) — déployé sur PC Linux

### Hypothèses validées / invalidées
- INVALIDE : warmup avec premier token stream = signal "prêt" → gemma3:4b met ~5 min pour le 1er token sur i3-4130
- INVALIDE : lifespan préchargeait le modèle → requête malformée (`prompt` sur `/api/chat`), avalée silencieusement
- VALIDE : `/api/generate` + `num_predict: 0` charge le modèle en RAM rapidement, `/api/ready` retourne `true` correctement
- VALIDE : lenteur 1er prompt = prefill system prompt + génération CPU, pas un bug logiciel

### Prochaine étape exacte
Phase 4 : installation sur le PC de l'association (Bistrot de Nérigean), formation animateurs avec explication de la lenteur du premier prompt.

### Question bloquante pour la session suivante
Aucune
