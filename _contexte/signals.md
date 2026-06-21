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
- Projet déployé sur PC Linux : /opt/robert-ia/app/frontend/dist/ (chemin corrigé)
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Protocole récupération/analyse non encore testé end-to-end sur vrai matériel
- rustdesk.service : enabled (multi-user.target), daemon-reload effectué — actif au prochain boot

## Dernière session (2026-06-21 — session 14)

### Décisions prises
- Feature inactivité : modale après 10 min, compte à rebours 30s, retour accueil si pas de clic
- RustDesk configuré pour démarrer automatiquement au boot (daemon-reload corrigé)

### Livrables produits ou modifiés
- `frontend/src/screens/Chat.jsx` : modifié — timer inactivité 10 min + modale countdown 30s
- `frontend/src/screens/Chat.css` : modifié — styles modale idle (overlay + modal + bouton)
- Build déployé sur PC Linux : `/opt/robert-ia/app/frontend/dist/` (anciens assets nettoyés)

### Hypothèses validées / invalidées
- VALIDE : rustdesk.service was enabled but needed daemon-reload (fichier changé sur disque)
- EN ATTENTE : test end-to-end protocole récupération sur vrai matériel

### Prochaine étape exacte
Tester protocole complet récupération/analyse (arrêt Robert, copie robert.db sur USB, analyse Windows, vérification CSV dans Excel), puis implémenter feature eau économisée (P2b).

### Question bloquante pour la session suivante
Aucune
