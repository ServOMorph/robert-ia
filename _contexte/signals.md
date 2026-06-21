# Signals — robert-ia   (MAJ 2026-06-21)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
- [P1] Écran de chargement : `/api/ready` retourne true trop tôt — loading screen s'efface avant que le modèle soit réellement prêt, premier prompt lent
- [P2] Corriger hallucination des chiffres précis (budget 200€ → modèle invente 500€, 5000€)
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)

## Questions ouvertes
- /api/ready retourne true via /api/ps mais premier prompt est lent — lifespan ne précharge pas réellement, ou /api/ps ment sur l'état RAM ?
- Hallucination chiffres : accepter 18/20 ou corriger avant déploiement pilote ?

## Échéances

## Blocages

## Contexte chaud
- Session 9 (2026-06-21) : PC Linux tourne sous GNOME Shell (Wayland), pas XFCE — stack à corriger
- Fond d'écran SérénIA Tech déployé : /home/robert-ia/fond-ecran-serenia.png via gsettings
- Dock GNOME (~60px gauche) masque partiellement le fond d'écran — auto-hide non configuré
- Accès SSH root toujours actif (clé robert-ia_ed25519 fonctionne)
- Écran de chargement toujours non fonctionnel (/api/ready trop rapide) — non traité cette session

## Dernière session (2026-06-21 — session 9)

### Décisions prises
- PC Linux tourne sous GNOME (pas XFCE) — stack documenté à corriger
- Fond d'écran SérénIA Tech déployé sur le PC Linux via gsettings

### Livrables produits ou modifiés
- `/home/robert-ia/fond-ecran-serenia.png` (PC Linux) : fond d'écran copié via SCP

### Hypothèses validées / invalidées
- INVALIDE : OS cible documenté comme XFCE → réalité : GNOME Shell (Wayland, gnome-shell actif)
- EN ATTENTE : dock GNOME masque ~60px gauche du fond d'écran — auto-hide non configuré

### Prochaine étape exacte
Reprendre le débogage de /api/ready (P1 hérité session 8).
Optionnel : configurer auto-hide du dock GNOME.

### Question bloquante pour la session suivante
Aucune
