# Contribution à Robert-IA

Merci de votre intérêt ! Voici comment participer.

## Avant de commencer

- Lisez le [README.md](README.md) pour comprendre le projet
- Consultez la [roadmap](roadmap_robert-ia.md) pour voir l'état actuel
- Vérifiez les issues GitHub pour éviter les doublons

## Configuration environnement développement

```bash
git clone https://github.com/ServOMorph/robert-ia.git
cd robert-ia

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend (dans un autre terminal)
cd frontend
npm install
npm run dev
```

Ollama doit tourner en local : `ollama serve`

## Workflow

1. **Fork + branche** : Créez une branche depuis `main` avec un nom clair
   ```bash
   git checkout -b feature/description-courte
   ```

2. **Code** : Respectez le style du projet (voir sections ci-dessous)

3. **Test** : Testez localement avant de pousser

4. **Commit** : Messages clairs et concis
   ```bash
   git commit -m "Add/Fix/Refactor: description brève"
   ```

5. **PR** : Décrivez le changement et ouvrez une pull request vers `main`

## Style et conventions

### Python
- PEP 8 + Black formatter
- Type hints recommandés
- Tests unitaires pour les fonctions principales

### JavaScript/React
- ESLint + Prettier
- Pas de console.log en production
- Composants fonctionnels (hooks)

### Commit messages
- Impératif : "Add feature" plutôt que "Added feature"
- Première ligne ≤ 70 caractères
- Détail en paragraphes si nécessaire

## Focus actuellement

Phase 1 — Structure projet et environnement dev.

**Contributions bienvenues sur** :
- Documentation setup
- Scripts automatisation environnement
- Tests de déploiement air-gap
- Retours d'expérience Ubuntu 24.04 / i3-4130

**Non ouvert à contribution pour l'instant** :
- Changements majeurs d'architecture (attendez Phase 2+)
- Dépendances supplémentaires (discuter d'abord)

## Questions ?

Ouvrez une issue ou contactez servomorph14@gmail.com

## Licence

Toute contribution est sous licence MIT.
