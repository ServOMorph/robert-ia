# Signals — robert-ia   (MAJ 2026-06-21)

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
_(aucune)_

## Échéances

## Blocages

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root toujours actif (clé robert-ia_ed25519 fonctionne)
- Projet déployé sur PC Linux : /opt/robert-ia/backend/data/robert.db
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Protocole récupération/analyse non encore testé end-to-end sur vrai matériel

## Dernière session (2026-06-21 — session 13)

### Décisions prises
- Protocole analyse conversations livré : script Python autonome + docs animateurs
- Test end-to-end ajouté comme prochaine étape obligatoire avant déploiement

### Livrables produits ou modifiés
- `scripts/analyse_conversations.py` : créé — export CSV + stats console, testé sur BD dev (328 msgs)
- `docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md` : créé — protocole usage Windows (animateurs)
- `docs/GUIDE_RECUPERATION_ANALYSE.md` : créé — guide complet Linux→USB→Windows avec checklist J+15

### Hypothèses validées / invalidées
- VALIDE : script Python stdlib suffit (pas de dépendance externe)
- VALIDE : export CSV UTF-8-BOM compatible Excel sans manipulation
- EN ATTENTE : test end-to-end sur vrai matériel (Linux → USB → Windows)

### Prochaine étape exacte
Tester protocole complet (arrêt Robert, copie robert.db sur USB, analyse Windows, vérification CSV dans Excel), puis implémenter feature eau économisée (P2b).

### Question bloquante pour la session suivante
Aucune
