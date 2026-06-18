# Signals — robert-ia   (MAJ 2026-06-18)

## Actions ouvertes
- [P1] Phase 3 — Déploiement air-gap (non commencée)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud

## Dernière session (2026-06-18)

### Décisions prises
- Charte graphique SéréniaTech appliquée à l'UI Robert (tokens CSS, pas de Google Fonts — air-gap)
- Navigation par machine d'état React (pas de router) — interface verrouillée par design
- Fonts Google exclues définitivement : fallback système suffisant pour kiosque

### Livrables produits ou modifiés
- `frontend/` : projet Vite + React initialisé (Vite 6, React 18)
- `frontend/src/styles/variables.css` + `global.css` : tokens charte SéréniaTech
- `frontend/src/screens/Welcome.jsx/.css` : accueil + consentement RGPD
- `frontend/src/screens/Pseudo.jsx/.css` : saisie pseudo (optionnel → Anonyme)
- `frontend/src/screens/Chat.jsx/.css` : interface chat + indicateur de frappe
- `frontend/src/App.jsx` + `main.jsx` : machine d'état, interface verrouillée
- `backend/main.py` : POST /api/chat → Ollama gemma3:1b + sauvegarde SQLite
- `backend/database.py` : init + écriture SQLite (`data/robert.db`)
- `backend/tests/` : 8 tests pytest (health, database, chat, erreur 503)
- `frontend/src/tests/` : 14 tests vitest (Welcome, Pseudo, App navigation)
- `docs/TESTS_MANUELS.md` : parcours nominal, cas limites, vérification SQLite
- `roadmap_robert-ia.md` : Phase 1 et Phase 2 marquées DONE

### Hypothèses validées / invalidées
- VALIDE : build Vite fonctionnel, 8+14 tests verts sans Ollama réel (mock)
- VALIDE : machine d'état suffit — pas besoin de react-router pour ce flux simple
- EN ATTENTE : test end-to-end avec Ollama réel sur Ubuntu (non testable depuis Windows)

### Prochaine étape exacte
Phase 3 — Déploiement air-gap : build statique frontend, script de packaging complet (app + modèle Ollama + SQLite) sur disque dur, protocole export données.

### Question bloquante pour la session suivante
Aucune
