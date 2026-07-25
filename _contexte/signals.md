# Signals — robert-ia   (MAJ 2026-07-25)

## Actions ouvertes
- [P1] Phase 5 — Déploiement pilote Bistrot de Nérigean (Phase 4 entièrement close, prête à démarrer)
  fait quand: installation terminée sur PC association + animateurs formés
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root DÉSACTIVÉ (`PermitRootLogin no`) — connexion via user `robert-ia` (clé C:\Users\raph6\.ssh\robert-ia_ed25519, hostname mDNS robert-ia-H81M-S2PV.local), sudo NOPASSWD:ALL configuré (/etc/sudoers.d/robert-ia-nopasswd) pour préserver le contrôle SSH automatique
- Réseau via switch relié à la Freebox (192.168.1.x, IP DHCP non fixe), hostname mDNS utilisé partout pour rester stable
- Claude Code prend le contrôle Linux automatiquement via SSH (instructions dans .claude/CLAUDE.md, commandes mises à jour vers robert-ia@... + sudo)
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Mini RAG déployé : knowledge.txt injecté dans system prompt — knowledge.txt à enrichir si nouvelles infos association
- P2b clos : bandeau eau économisée (total cumulé, `/api/water-stats`) validé visuellement par l'utilisateur en production
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Résidu non commité hors session : `MEMORY/` (untracked) — non lié à ce travail, à traiter séparément

## Dernière session (2026-07-25 — session 19)

### Décisions prises
- P2b clos : validation visuelle finale de l'utilisateur sur le kiosk confirmée
- P3 clos : accès root SSH désactivé, remplacé par user `robert-ia` + sudo NOPASSWD:ALL (nécessaire pour préserver le contrôle SSH automatique de Claude Code)

### Livrables produits ou modifiés
- Linux : `/etc/ssh/sshd_config` (`PermitRootLogin no`), `/etc/sudoers.d/robert-ia-nopasswd` (nouveau)
- `.claude/CLAUDE.md` : commandes SSH/scp mises à jour (`robert-ia@...` au lieu de `root@...`), note sudo ajoutée

### Hypothèses validées / invalidées
- VALIDE : bandeau eau économisée confirmé visuellement correct par l'utilisateur
- VALIDE : accès root SSH refusé après redémarrage du service ssh (testé)
- VALIDE : connexion `robert-ia@...` + `sudo` sans mot de passe fonctionnelle, service `robert-ia` toujours actif après le durcissement

### Prochaine étape exacte
Phase 4 entièrement close. Prochaine session : démarrer Phase 5 (déploiement pilote Bistrot de Nérigean) ou finaliser P2 (test end-to-end protocole récupération/analyse).

### Question bloquante pour la session suivante
Aucune
