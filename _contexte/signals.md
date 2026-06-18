# Signals — robert-ia   (MAJ 2026-06-18)

## Actions ouvertes
- [P1] Phase 3 — Déploiement air-gap (non commencée)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud

## Dernière session (2026-06-18 — session 3)

### Décisions prises
- keep_alive Ollama mis à -1 : modèle chargé indéfiniment en RAM
- Préchargement du modèle au démarrage du serveur (requête vide dans lifespan FastAPI)

### Livrables produits ou modifiés
- `backend/main.py` : keep_alive -1 dans le payload + préchargement lifespan

### Hypothèses validées / invalidées
- EN ATTENTE : test end-to-end avec Ollama réel sur Ubuntu (non testable depuis Windows)

### Prochaine étape exacte
Phase 3 — Déploiement air-gap : build statique frontend, script de packaging complet (app + modèle Ollama + SQLite) sur disque dur, protocole export données.

### Question bloquante pour la session suivante
Aucune
