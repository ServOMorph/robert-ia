# Signals — robert-ia   (MAJ 2026-06-20)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote (non commencée)
- [P1] Valider gemma3:4b sur machine cible (RAM 4 Go — risque swap/crash)
- [P2] Corriger hallucination des chiffres précis (budget 200€ → modèle invente 500€, 5000€)

## Questions ouvertes
- gemma3:4b tient-il dans 4 Go RAM sur i3-4130 avec Ollama keep_alive -1 ?
- Hallucination chiffres : option system prompt, changer de modèle, ou accepter la limite ?

## Échéances

## Blocages

## Contexte chaud
- Session 6 (2026-06-20) : mémoire conversationnelle améliorée — score 18/20 (vs 8/20 avant)
- Backend tourne sur port 8001 (port 8000 en état fantôme Windows — socket bloqué sans process)
- Test automatique opérationnel : `python backend/test_manuels/run_test_memoire.py`

## Dernière session (2026-06-20 — session 6)

### Décisions prises
- HISTORY_WINDOW : 8 → 16 messages
- NUM_CTX : 2048 → 4096 tokens
- Architecture mémoire : fenêtre glissante seule → tête épinglée (HEAD_K=4) + fenêtre glissante (16)
- System prompt enrichi : règles mémoire + interdiction hallucination + honnêteté inter-session

### Livrables produits ou modifiés
- `backend/main.py` : HEAD_K=4, HISTORY_WINDOW=16, NUM_CTX=4096, logique head+tail dedupliquée
- `backend/database.py` : ajout `get_head(session_id, k=4)`, `get_history` retourne maintenant l'id pour déduplication
- `backend/prompt.py` : system prompt enrichi (4 règles mémoire + honnêteté)
- `backend/test_manuels/run_test_memoire.py` : script de test automatique créé (20 prompts, évaluation par critères, score/20)

### Résultats des tests
| Config | Score |
|--------|-------|
| gemma3:4b, fenêtre=8, num_ctx=2048, prompt minimal | 8/20 |
| gemma3:4b, fenêtre=16, num_ctx=4096, prompt minimal | 9/20 |
| gemma3:4b, fenêtre=16 + tête épinglée K=4, prompt enrichi | 18/20 |

### Analyse des 2 échecs restants (prompts 13 et 14)
- **Prompt 13** ("c'est quoi la contrainte budgétaire exacte ?") : modèle invente un chiffre (500€, 5000€) au lieu de lire le 200€ du contexte
- **Prompt 14** (récapitulatif global) : budget absent du résumé car mal mémorisé → critère raté
- **Cause** : gemma3:4b hallucine les chiffres précis quand la question est indirecte ("comme je te l'avais dit..."). Faiblesse connue des petits modèles.

### Options pour corriger les 2 échecs (à évaluer session suivante)
1. **System prompt** — ajouter : "Pour les chiffres, cite toujours le nombre exact tel qu'il a été donné. Ne génère jamais un chiffre de mémoire." → tenter en premier, coût nul
2. **Accepter la limite** — 18/20 suffisant pour le Bistrot de Nérigean (utilisateurs non-testeurs), passer directement à Phase 4
3. **Changer de modèle** — phi3:mini (~2,3 Go, viables sur 4 Go) ou llama3.2:3b potentiellement plus fiables sur chiffres ; nécessite nouveau cycle de tests complets

### Prochaine étape exacte
1. Décider si on corrige le score (option 1 ou 3) ou on accepte 18/20 et passe en Phase 4
2. Si option 1 : tester le system prompt enrichi et relancer `run_test_memoire.py`
3. Si Phase 4 : valider RAM gemma3:4b sur i3-4130, puis installation pilote Bistrot de Nérigean

### Question bloquante pour la session suivante
18/20 suffit-il pour le déploiement pilote, ou veut-on corriger les chiffres d'abord ?
