# Signals — robert-ia   (MAJ 2026-07-25 — session 25)

## Actions ouvertes
- [P1] Phase 5 — Formation animateurs + visite de suivi J+15 (borne en démo au Moulin du Sud)
  fait quand: animateurs formés + visite J+15 effectuée (récupération SQLite + analyse retours)
  réf: roadmap_robert-ia.md (Phase 5), _contexte/contexte.md
- [P2] TESTER protocole récupération + analyse conversations (end-to-end)
  fait quand: test réalisé sur PC Windows avec un vrai robert.db exporté depuis Linux via USB — CSV généré et lisible dans Excel
  réf: scripts/analyse_conversations.py, docs/GUIDE_RECUPERATION_ANALYSE.md, docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md
- [P3] Corriger `/api/health` dans docs/GUIDE_RECUPERATION_ANALYSE.md:66 — cette route n'existe pas côté backend (tombe sur le catch-all frontend), le bon endpoint est `/health`
  fait quand: doc corrigée
  réf: docs/GUIDE_RECUPERATION_ANALYSE.md, backend/main.py

## Contexte chaud
- PC Linux tourne sous GNOME Shell (Wayland)
- Accès SSH root DÉSACTIVÉ (`PermitRootLogin no`) — connexion via user `robert-ia` (clé C:\Users\raph6\.ssh\robert-ia_ed25519, hostname mDNS robert-ia-H81M-S2PV.local), sudo NOPASSWD:ALL configuré (/etc/sudoers.d/robert-ia-nopasswd) pour préserver le contrôle SSH automatique
- Réseau via switch relié à la Freebox (192.168.1.x, IP DHCP non fixe), hostname mDNS utilisé partout pour rester stable
- Claude Code prend le contrôle Linux automatiquement via SSH (instructions dans .claude/CLAUDE.md, commandes mises à jour vers robert-ia@... + sudo)
- Applications graphiques sur le Linux (kiosk Chromium) : lancer via le Bash tool, pas PowerShell (backticks/$() mangés) ; détecter le process avec `pgrep -f "[c]hromium.*--kiosk"` (crochets obligatoires) ; relance nécessite `XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0` (session Wayland, `DISPLAY=:0` ne fonctionne pas) + `setsid`/`disown` pour survivre à la fermeture SSH — voir .claude/memory.md
- Optimisations RAM appliquées : OLLAMA_NO_MMAP=false + KEEP_ALIVE=5m + Chromium + RustDesk désactivé ; modèle gemma3:4b chargé en RAM (2,9 Go, keep_alive Forever, 100% CPU, pas de GPU)
- Protocole récupération : robert.db récupéré via SSH + CSV généré — test USB + vérification Excel restants
- Lenteur 1er prompt (~5 min sur i3-4130) = contrainte matérielle, gérée par formation
- Cache Chromium : ne survit plus aux redéploiements grâce au header `Cache-Control: no-cache` sur index.html
- Multi-contexte : mini RAG remplacé par système multi-lieux (`backend/contexts/*.txt`, variable `ROBERT_CONTEXT`)
- **Borne mobile** : c'est le PC Linux lui-même qui est déplacé de lieu en lieu — aucune installation sur un PC tiers. Actuellement en démo au Moulin du Sud (`ROBERT_CONTEXT=moulin_du_sud`), déplacement possible vers le Bistrot de Nérigean plus tard — bascule = éditer la variable dans l'unité systemd + redémarrer (pas de script dédié à ce jour)
- Version app affichée dynamiquement sur l'écran d'accueil, lue depuis `frontend/package.json` via `define: __APP_VERSION__` dans `vite.config.js` — actuellement `1.1.0`
- Suggestions de questions cliquables sur l'écran de chat : 3 par contexte (`backend/contexts/<nom>.suggestions.txt`), affichées sur une seule ligne, disparaissent après le premier message envoyé
- Suite de tests frontend intégralement verte (20/20), backend vert sauf un échec préexistant sans rapport (`test_database.py::test_get_history_returns_ordered_messages`)
- Port backend : dev = 8000 (`python -m uvicorn main:app --reload` via `run.py`), prod = 8001 (`scripts/start-backend.sh`) — doc désormais cohérente sur ce point
- `backend/venv/` créé sur Windows (absent jusqu'ici, uvicorn manquant) — `run.py` détecte et utilise automatiquement ce venv s'il existe
- `docs/PHASE3_SUMMARY.md` déplacé vers `docs/archive/` (bandeau d'avertissement, contenu obsolète : port 8000, Firefox, gemma3:1b)

## Dernière session (2026-07-25 — session 25)

### Décisions prises
- Correction : la borne mobile Phase 5 est le PC Linux déplacé physiquement, pas une installation sur un PC tiers au Moulin du Sud
- PHASE3_SUMMARY.md archivé (bandeau d'avertissement) plutôt que réécrit — évite de falsifier l'historique

### Livrables produits ou modifiés
- `roadmap_robert-ia.md`, `_contexte/contexte.md`, `README.md` : correction borne mobile
- `frontend/src/screens/Chat.css` : suggestions cliquables en ligne (row), police réduite — buildé et déployé sur Linux
- `.claude/memory.md` : entrée relance kiosk sous Wayland
- `run.py` : relais de sortie backend/frontend via threads (fix blocage `readline`), arrêt propre des deux process, détection auto du venv backend
- `backend/venv/` : créé, dépendances installées
- `README.md`, `docs/PROTOCOLE_EXPORT_DONNEES.md`, `docs/GUIDE_INSTALLATION_AIRGAP.md`, `scripts/setup-airgap.sh` : corrections port 8000→8001 en production
- `docs/PHASE3_SUMMARY.md` → `docs/archive/PHASE3_SUMMARY.md`
- Linux : assets orphelins supprimés, kiosk relancé et vérifié stable

### Hypothèses validées / invalidées
- VALIDE : modèle LLM identique Windows/Linux/prod = `gemma3:4b`
- INVALIDE : le pilote nécessitait une installation sur le PC de l'association -> pivot : c'est le PC Linux qui se déplace

### Prochaine étape exacte
Formation animateurs au Moulin du Sud, puis visite de suivi J+15 (récupération SQLite + analyse).

### Question bloquante pour la session suivante
Aucune
