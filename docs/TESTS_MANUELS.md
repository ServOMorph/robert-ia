# Tests manuels — Robert-IA

## Prérequis
- Ollama lancé avec `ollama serve` et le modèle `gemma3:1b` disponible
- Backend lancé : `cd backend && source .venv/bin/activate && uvicorn main:app --reload`
- Frontend lancé : `cd frontend && npm run dev`
- Navigateur sur `http://localhost:5173`

---

## Parcours nominal

| # | Action | Résultat attendu |
|---|--------|-----------------|
| 1 | Ouvrir l'app | Écran Welcome affiché, bouton "Commencer" désactivé |
| 2 | Lire la notice RGPD | 4 points listés avec coche, section bleue visible |
| 3 | Cocher la case | Bouton "Commencer" s'active |
| 4 | Cliquer "Commencer" | Écran Pseudo affiché, champ texte avec focus |
| 5 | Laisser le champ vide et valider | Bouton affiche "Continuer anonymement", navigation vers Chat |
| 6 | Sur l'écran Chat | Message de bienvenue "Bonjour ! Je suis Robert…" visible |
| 7 | Saisir un message et envoyer | Indicateur de frappe (3 points animés), puis réponse Ollama |
| 8 | Cliquer "Terminer" | Retour à l'écran Welcome, checkbox décochée |

---

## Parcours avec pseudo

| # | Action | Résultat attendu |
|---|--------|-----------------|
| 1 | Consentir, écran Pseudo | - |
| 2 | Saisir "Alice" | Bouton affiche "Bonjour, Alice !" |
| 3 | Valider | Écran Chat avec message "Bonjour Alice ! Je suis Robert…" |

---

## Cas limites

| # | Scénario | Résultat attendu |
|---|----------|-----------------|
| 1 | Pseudo > 32 caractères | Saisie bloquée à 32 caractères (maxLength) |
| 2 | Envoyer message vide | Bouton "Envoyer" désactivé, rien ne se passe |
| 3 | Ollama arrêté pendant la conversation | Message d'erreur "Ollama non disponible" dans le chat |
| 4 | Double-clic sur "Envoyer" | Un seul message envoyé (bouton désactivé pendant le chargement) |
| 5 | Appuyer sur Entrée dans le champ | Message envoyé (submit form) |

---

## Vérification SQLite

Après une conversation :

```bash
sqlite3 backend/data/robert.db "SELECT session_id, pseudo, role, substr(content,1,40), created_at FROM messages LIMIT 10;"
```

Attendu : les messages utilisateur et assistant listés avec timestamp.

---

## Tests automatiques

```bash
# Backend
cd backend
source .venv/bin/activate
pytest tests/ -v

# Frontend
cd frontend
npm test
```

Résultats attendus : 8 tests backend, 14 tests frontend, tous verts.
