# Contexte — jeux

## Objectif (immuable sauf décision explicite)
Créer des jeux vidéo vintage.

## Stack / contraintes techniques (stable, rarement modifié)
Hérite de la stack du projet parent (robert-ia). Aucune stack spécifique au jeu vidéo trouvée
dans le projet parent — celui-ci est un assistant conversationnel air-gap (Python/FastAPI,
React/Vite), sans rapport avec le développement de jeux.

## État actuel (réécrit intégralement à chaque /close)
opencode configuré avec un provider Ollama local (3 modèles déclarés : qwen2.5-coder:7b, qwen3.5:latest,
gemma4:12b). Premier test de génération de code (Pong) réalisé en comparatif entre qwen2.5-coder:7b
(échec sur 3 itérations) et gemma4:12b (code structurellement correct, un bug de gameplay non corrigé).
Aucun jeu jouable livré à ce stade. `pong.py` généré mais mal placé (racine du projet au lieu de JEUX/).

## Décisions structurantes (append only — 10 entrées max, 5 lignes max/entrée, archiver au-delà)
- 2026-08-10 : Initialisation du protocole vibecoding.
- 2026-08-11 : opencode retenu comme interface pour piloter un LLM local (Ollama) sur cette zone.
- 2026-08-11 : gemma4:12b choisi comme modèle par défaut après comparatif avec qwen2.5-coder:7b
  (meilleure structure de code malgré un bug de rebond non résolu).
