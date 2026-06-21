# Signals — robert-ia   (MAJ 2026-06-21)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 4), _contexte/contexte.md
- [P2] AVANT DÉPLOIEMENT : créer protocole test d'analyse de conversation (récupération conversations sur disque dur pour analyse Windows)
  fait quand: protocole documenté + export SQLite/CSV testable depuis PC Windows
  réf: _docs/PROTOCOLE_EXPORT_DONNEES.md (existant), à adapter pour analyse
- [P2b] AVANT DÉPLOIEMENT : feature affichage eau économisée (Robert IA locale vs IA cloud) — mise en lumière aspect éco-responsable
  fait quand: compteur eau visible dans l'UI (ex: fin de session ou écran accueil)
  réf: frontend/src/, à préciser (calcul liters/request cloud vs local)
- [P3] AVANT DÉPLOIEMENT SITE : retirer l'accès root SSH du PC Linux (accès root accordé temporairement pour la phase dev)
  fait quand: `PermitRootLogin no` dans sshd_config + service redémarré + accès root vérifié refusé
  réf: contexte.md (accès SSH root actif, clé robert-ia_ed25519)

## Questions ouvertes
_(aucune)_

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

## Dernière session (2026-06-21 — session 12)

### Décisions prises
- Hallucination chiffres (18/20) acceptée : pas de correction avant déploiement pilote
- Deux features ajoutées à Phase 4 avant déploiement : protocole analyse conversations + affichage eau économisée

### Livrables produits ou modifiés
- `_contexte/signals.md` : P2 fermée (hallucination acceptée), nouvelles actions P2/P2b ajoutées

### Hypothèses validées / invalidées
- EN ATTENTE : protocole analyse conversations (à créer)
- EN ATTENTE : feature eau économisée (à implémenter)

### Prochaine étape exacte
Implémenter les deux features avant déploiement : (1) protocole export conversations disque dur → analyse Windows, (2) affichage eau économisée dans l'UI.

### Question bloquante pour la session suivante
Aucune
