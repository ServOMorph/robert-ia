# Rôle — MEMORY

## Rôle
Ajuster et maintenir le contexte/mémoire de robert-ia en vue de la démonstration du 25/07/2026 (Moulin du Sud) : cohérence des données de contexte, préparation des artefacts nécessaires à la démo.

## Périmètre
- Dossier de sortie : MEMORY/
- Peut lire : MEMORY/, racine du projet (backend/, frontend/, AGENTS.md) pour contexte
- Peut écrire : MEMORY/ et ses sous-dossiers (par défaut)
- Ne doit pas toucher : racine du projet, backend/, frontend/, _contexte/ d'autres zones (COM/, racine)

## Invariants
- Ne jamais committer hors de MEMORY/
- Les artefacts de préparation mémoire restent stockés dans MEMORY/

## Méta
- Zone parente : robert-ia
- Alias zones.md : memory
- Créé le : 2026-07-20
