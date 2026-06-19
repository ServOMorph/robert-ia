# Signals — robert-ia   (MAJ 2026-06-19)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote (non commencée)
- [P1] Valider gemma3:4b sur machine cible (RAM 4 Go — risque swap/crash)

## Questions ouvertes
- gemma3:4b tient-il dans 4 Go RAM sur i3-4130 avec Ollama keep_alive -1 ?

## Échéances

## Blocages

## Contexte chaud
- Mémoire conversationnelle implémentée (session 5) mais gemma3:1b insuffisant (score 4/20 aux tests)
- Modèle changé en gemma3:4b dans main.py — test en cours

## Dernière session (2026-06-19 — session 5)

### Décisions prises
- Mémoire conversationnelle intra-session activée : fenêtre glissante 8 messages, num_ctx 2048
- Migration /api/generate → /api/chat (Ollama natif messages[])
- gemma3:1b jugé non viable pour la mémoire contextuelle (score 4/20)
- Test de gemma3:4b en remplacement (décision provisoire, sous réserve RAM)

### Livrables produits ou modifiés
- `backend/database.py` : ajout `get_history(session_id, limit=8)`
- `backend/main.py` : migration /api/chat, injection historique, num_ctx 2048, MODEL=gemma3:4b
- `backend/tests/test_chat.py` : réécriture complète (mocks stream, parsing NDJSON, test injection historique)
- `backend/tests/test_database.py` : 3 tests ajoutés pour get_history
- `backend/test_manuels/test_contexte_conversation.md` : 20 prompts de test mémoire + grille d'évaluation

### Hypothèses validées / invalidées
- INVALIDE : gemma3:1b suffisant pour la mémoire contextuelle → score 4/20, confusion Marie/Paul, évasion sur faits précis
- VALIDE : injection historique fonctionne techniquement (test_chat_injects_history passe)
- EN ATTENTE : gemma3:4b viable sur 4 Go RAM — à valider sur machine cible

### Prochaine étape exacte
Tester gemma3:4b sur la machine de dev ou sur le PC Bistrot. Si RAM OK → Phase 4. Si swap/crash → évaluer phi3:mini (3,8b, ~2,3 Go).

### Question bloquante pour la session suivante
gemma3:4b tient-il en RAM sur i3-4130 / 4 Go avec keep_alive -1 ? (sinon : phi3:mini ou autre modèle ?)
