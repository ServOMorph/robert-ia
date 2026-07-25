# Signals — robert-ia   (MAJ 2026-07-25)

## Actions ouvertes
- [P1] Rebasculer ou confirmer le contexte de production avant toute utilisation par le Bistrot de Nérigean
  fait quand: `ROBERT_CONTEXT` vérifié/remis sur `invariable` avant reprise Phase 5, ou décision explicite documentée de garder `moulin_du_sud`
  réf: config/robert-ia.service (ligne Environment=ROBERT_CONTEXT), backend/contexts/
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
- P2b clos : bandeau eau économisée (total cumulé, `/api/water-stats`) validé visuellement par l'utilisateur en production
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Multi-contexte : mini RAG remplacé par système multi-lieux (`backend/contexts/*.txt`, variable `ROBERT_CONTEXT`) — voir dernière session
- **PROD actuellement en `ROBERT_CONTEXT=moulin_du_sud`** (pas `invariable`/Nérigean) — choix explicite de l'utilisateur en session, à revérifier avant reprise Phase 5
- Résidu non commité hors session : `MEMORY/` (untracked) + `.claude/zones.md` (modifié, ajout alias com/memory) — non lié à ce travail, à traiter séparément

## Dernière session (2026-07-25 — session 20)

### Décisions prises
- Identité de lieu sortie du code en dur (`prompt.py`) vers des fichiers de contexte structurés (`backend/contexts/*.txt`, champs `nom`/`lieu`/`type` + connaissance)
- Sélection du contexte actif via variable d'environnement `ROBERT_CONTEXT` (défaut `invariable`), bascule = éditer le service systemd + `daemon-reload` + `restart` (~2-3 s)
- Second contexte créé : `moulin_du_sud` (Le Moulin du Sud / Symphonie Équitable, Génissac — données récupérées via web sur symphonie-equitable.fr et mairie-genissac.fr, confirmées par l'utilisateur)
- Déployé sur Linux et testé end-to-end via `/api/chat` — réponse conforme au contexte actif
- Utilisateur a choisi de laisser la prod sur `ROBERT_CONTEXT=moulin_du_sud` à l'issue du test

### Livrables produits ou modifiés
- `backend/prompt.py` : gabarit générique paramétré (nom/lieu/type), correction grammaticale ("chez" au lieu de "à" — évite la contraction incorrecte avec les articles type "Le")
- `backend/main.py` : chargement du contexte actif via `ROBERT_CONTEXT` + parsing du fichier contexte
- `backend/contexts/invariable.txt` (nouveau, remplace `backend/knowledge.txt` supprimé) : contexte L'Invariable/Nérigean migré
- `backend/contexts/moulin_du_sud.txt` (nouveau) : contexte Moulin du Sud/Génissac
- `config/robert-ia.service` : variable `Environment="ROBERT_CONTEXT=..."` ajoutée
- Déploiement Linux : fichiers backend + contexts copiés (scp), service systemd mis à jour et redémarré, `knowledge.txt` obsolète supprimé côté serveur

### Hypothèses validées / invalidées
- VALIDE : le switch de contexte fonctionne bout en bout (fichier → prompt système → réponse LLM conforme)
- VALIDE : "chez" ne se contracte jamais avec un article, contrairement à "à" (au) ou "de" (du) — corrige le bug grammatical sur les noms avec article

### Prochaine étape exacte
Vérifier/rebasculer `ROBERT_CONTEXT` avant reprise de la Phase 5 (pilote Bistrot de Nérigean) si le service doit servir L'Invariable. Sinon, poursuivre Phase 5 telle quelle.

### Question bloquante pour la session suivante
Aucune
