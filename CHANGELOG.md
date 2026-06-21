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
