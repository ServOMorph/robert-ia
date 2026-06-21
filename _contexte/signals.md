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
- PC Linux tourne sous GNOME Shell (Wayland) — stack corrigé dans contexte.md
- Fond d'écran SérénIA Tech déployé : /home/robert-ia/fond-ecran-serenia.png via gsettings
- Dock GNOME (~60px gauche) masque partiellement le fond d'écran — auto-hide non configuré
- Accès SSH root toujours actif (clé robert-ia_ed25519 fonctionne)
- Projet déployé sur PC Linux : /opt/robert-ia/app/frontend/dist/
- Écran de chargement agrandi x2 et déployé — bug /api/ready toujours non traité
- Dev Windows : `python dev.py` + `?screen=loading` pour isoler l'écran de chargement

## Dernière session (2026-06-21 — session 10)

### Décisions prises
- Dev frontend : override d'écran par ?screen=<nom> dans l'URL (dev only, via import.meta.env.DEV)
- Écran de chargement agrandi x2 (logo 80→160px, titre text-4xl→text-5xl, points 10→20px)

### Livrables produits ou modifiés
- `frontend/src/App.jsx` : ajout initialScreen() avec override URL en mode DEV
- `frontend/src/screens/Loading.css` : tailles doublées
- `frontend/dist/` : rebuild + déployé sur /opt/robert-ia/app/frontend/dist/ (PC Linux)
- `dev.py` : script racine pour lancer npm install + npm run dev depuis Windows

### Hypothèses validées / invalidées
- VALIDE : déploiement SCP sur /opt/robert-ia/app/frontend/dist/ fonctionne sans redémarrage service

### Prochaine étape exacte
Reprendre le débogage de /api/ready (P1 hérité) : /api/ps retourne true trop tôt,
premier prompt lent. Investiguer lifespan Ollama ou mock /api/ready côté backend.

### Question bloquante pour la session suivante
Aucune
