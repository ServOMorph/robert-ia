## v1.6 — 2026-06-22

### Ajouté
- `scripts/test_rag.py` : script de test automatique mini RAG — 3 niveaux (culture générale / association / refus internet), log dans logs/

## v1.5 — 2026-06-22

### Ajouté
- `backend/knowledge.txt` : base de connaissance L'Invariable (adresse, horaires, concept) — injectée dans le system prompt au démarrage
- `config/ollama.service` : fichier de service Ollama ajouté côté Windows (synchronisation)

### Modifié
- `backend/prompt.py` : system prompt refondu — 3 niveaux de réponse (culture générale / association depuis knowledge.txt / refus avec explication pour météo et internet)
- `backend/main.py` : charge knowledge.txt au démarrage et l'injecte dans le system prompt via build_system_prompt()
- `scripts/start-kiosk.sh` : Firefox → Chromium (synchronisation Windows/Linux)
- `.claude/CLAUDE.md` : section "Synchronisation Windows→Linux" ajoutée — protocole Windows first + scp

## v1.4 — 2026-06-22

### Modifié
- `.claude/CLAUDE.md` : section "Contrôle SSH du PC Linux" ajoutée — Claude exécute les commandes Linux automatiquement via SSH sans copier-coller

## v1.3 — 2026-06-21

### Ajouté
- `frontend/src/screens/Chat.jsx` : modale inactivité après 10 min, countdown 30s, retour accueil automatique
- `frontend/src/screens/Chat.css` : styles modale idle

### Modifié
- RustDesk autostart activé sur PC Linux (daemon-reload rustdesk.service)
- Frontend déployé sur PC Linux (chemin corrigé : /opt/robert-ia/app/frontend/dist/)

## v1.2 — 2026-06-21

### Ajouté
- `scripts/analyse_conversations.py` : export CSV + stats console (stdlib Python, compatible Windows)
- `docs/PROTOCOLE_ANALYSE_CONVERSATIONS.md` : protocole usage Windows pour animateurs
- `docs/GUIDE_RECUPERATION_ANALYSE.md` : guide complet Linux→USB→Windows avec checklist visite J+15

## v1.1 — 2026-06-21

### Modifié
- Hallucination chiffres (18/20) acceptée — pas de correction avant déploiement pilote
- Ajout Phase 4 : protocole analyse conversations (export disque dur → analyse Windows)
- Ajout Phase 4 : feature affichage eau économisée (Robert local vs IA cloud)
- Décisions structurantes archivées (archive_decisions.md) — seuil 10 entrées atteint

## v1.0 — 2026-06-21

### Ajouté
- Phases 1–3 complètes : socle projet, interface chat, déploiement air-gap
- Lifespan warmup via /api/generate + num_predict:0
- /api/ready stable via /api/ps
- OS cible corrigé : GNOME Shell / Wayland (pas XFCE)
- Fond d'écran SérénIA Tech déployé
- Dev Windows : override ?screen= + python dev.py
