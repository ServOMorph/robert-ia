# Signals — jeux   (MAJ 2026-08-11)

## Actions ouvertes
- [P2|ouvert] Déplacer `pong.py` (racine du projet) vers `JEUX/`
  fait quand: fichier déplacé dans JEUX/, plus aucun résidu à la racine
  réf: d:\ServOMorph\robert-ia\pong.py
- [P2|ouvert] Choisir le modèle Ollama final pour la génération de jeux et corriger le bug de rebond identifié sur gemma4:12b (vitesses constantes jamais inversées)
  fait quand: un des deux modèles produit un Pong jouable sans intervention manuelle, ou décision explicite de changer d'approche
  réf: C:\Users\raph6\.config\opencode\opencode.json, pong.py (racine, généré par gemma4:12b)

## Contexte chaud
- opencode configuré avec provider Ollama local (`~/.config/opencode/opencode.json`), 3 modèles déclarés : qwen2.5-coder:7b, qwen3.5:latest, gemma4:12b — modèle actif actuellement gemma4:12b
- Test comparatif qwen2.5-coder:7b vs gemma4:12b sur génération de Pong : qwen2.5-coder a échoué sur 3 itérations (hallucination hors-sujet, puis bugs logiques successifs) ; gemma4:12b a produit un code plus mature (pygame.Rect, colliderect) mais avec un bug de gameplay confirmé par simulation (balle qui oscille au lieu de rebondir, vitesses jamais inversées de signe)
- opencode écrit les fichiers dans le dossier depuis lequel il est lancé, pas automatiquement dans JEUX/ — à surveiller lors des prochains tests (lancer opencode depuis JEUX/ directement)

## Dernière session (2026-08-11)
### Décisions prises
- Modèle par défaut opencode fixé à gemma4:12b après comparatif (meilleure structure de code que qwen2.5-coder:7b, malgré bug de rebond non résolu)

### Livrables produits ou modifiés
- `C:\Users\raph6\.config\opencode\opencode.json` : provider Ollama configuré, 3 modèles déclarés
- `pong.py` (racine du projet, hors JEUX/) : généré par gemma4:12b, fonctionnel sans crash mais bug de gameplay (pas de vrai rebond)

### Hypothèses validées / invalidées
- INVALIDE : qwen2.5-coder:7b suffisant pour générer du code de jeu jouable en 1-2 passes -> échec sur 3 itérations
- EN ATTENTE : gemma4:12b viable pour ce cas d'usage -> code structurellement correct mais bug de gameplay non corrigé

### Prochaine étape exacte
Corriger le bug de rebond sur la version gemma4:12b (inverser le signe des vitesses au lieu de corriger la position), déplacer pong.py dans JEUX/, puis décider si le workflow (LLM local + relecture humaine) est viable pour la suite.

### Question bloquante pour la session suivante
Aucune
