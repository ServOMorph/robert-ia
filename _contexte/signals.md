# Signals — robert-ia   (MAJ 2026-07-25 — session 24)

## Actions ouvertes
- [P1] Phase 5 — Déploiement pilote au Moulin du Sud (borne mobile, suggestions déployées, prête à démarrer)
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
- Applications graphiques sur le Linux (kiosk Chromium) : lancer via le Bash tool, pas PowerShell (backticks/$() mangés) ; détecter le process avec `pgrep -f "[c]hromium.*--kiosk"` (crochets obligatoires, sinon faux positifs + pkill qui se tue lui-même) — voir .claude/memory.md
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Multi-contexte : mini RAG remplacé par système multi-lieux (`backend/contexts/*.txt`, variable `ROBERT_CONTEXT`)
- **Borne mobile** : pilote démarré au Moulin du Sud (`ROBERT_CONTEXT=moulin_du_sud`), déplacement possible vers le Bistrot de Nérigean plus tard — bascule = éditer la variable dans l'unité systemd + redémarrer (pas de script dédié à ce jour)
- Version app affichée dynamiquement sur l'écran d'accueil, lue depuis `frontend/package.json` via `define: __APP_VERSION__` dans `vite.config.js` — actuellement `1.1.0`
- Suggestions de questions cliquables sur l'écran de chat : 3 par contexte (`backend/contexts/<nom>.suggestions.txt`), disparaissent après le premier message envoyé
- Suite de tests frontend intégralement verte (20/20), backend vert sauf un échec préexistant sans rapport (`test_database.py::test_get_history_returns_ordered_messages`)
- Assets orphelins nettoyés sur le Linux (`/opt/robert-ia/app/frontend/dist/assets/` : 2 fichiers au lieu de 6)

## Dernière session (2026-07-25 — session 24)

### Décisions prises
- Ajout de suggestions de questions cliquables sur l'écran de chat (3 par contexte, disparaissent après le premier envoi)
- Confirmation : le pilote est une borne mobile, actuellement au Moulin du Sud (pas au Bistrot de Nérigean comme l'indiquait la roadmap) — corrigée
- Nettoyage des assets orphelins sur le Linux effectué (clôture de l'ancienne action P3)

### Livrables produits ou modifiés
- `backend/main.py` : `load_suggestions()` + endpoint `GET /api/suggestions`
- `backend/contexts/moulin_du_sud.suggestions.txt`, `backend/contexts/invariable.suggestions.txt` : nouveaux
- `backend/tests/test_suggestions.py` : nouveau, 4 tests
- `frontend/src/screens/Chat.jsx` : `sendMessage` scindé en `submitMessage`/`handleSubmit`/`handleSuggestion`, fetch + affichage des suggestions
- `frontend/src/screens/Chat.css` : styles `.chat-suggestions` / `.chat-suggestion`
- `frontend/src/tests/Chat.test.jsx` : 3 nouveaux tests + correction warnings `act()` préexistants
- `.claude/memory.md` : nouveau, 2 entrées (lancement app graphique via SSH, détection kiosk avec pgrep)
- Déployé sur le Linux : `main.py`, les 2 `.suggestions.txt`, frontend rebuild — vérifié en prod (`/api/suggestions` répond, kiosk relancé et stable)

### Hypothèses validées / invalidées
- VALIDE : le système multi-contextes existant supporte les suggestions sans modification — un fichier `.suggestions.txt` par contexte, absent → liste vide sans erreur
- VALIDE : borne mobile confirmée par l'utilisateur — pas de contexte dédié à créer pour l'instant
- INVALIDE : la roadmap indiquait Bistrot de Nérigean comme lieu du pilote -> corrigée vers Moulin du Sud

### Prochaine étape exacte
Installation sur le PC de l'association (Moulin du Sud) + formation animateurs.

### Question bloquante pour la session suivante
Aucune
