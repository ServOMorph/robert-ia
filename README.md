# Robert-IA

Une IA locale conversationnelle pour les espaces associatifs.

## Vision

Déployer une IA accessible, autonome et confidentielle dans des environnements associatifs (air-gap, sessions anonymes, données 100 % locales). Pas de cloud, pas de tracking, pas de dépendance réseau.

## Stack technique

- **OS cible** : Ubuntu 24.04 LTS (GNOME Shell / Wayland)
- **IA** : Ollama + gemma3:4b
- **Backend** : Python + FastAPI
- **Base de données** : SQLite
- **Frontend** : React + Vite (build statique)
- **Affichage** : Navigateur kiosk (mono-onglet)
- **Déploiement** : Disque dur (air-gap)

## Installation (environnement développement)

### Prérequis
- Python 3.10+
- Node.js 18+
- Ollama (avec modèle gemma3:4b)

### Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sous Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
npm run dev
```

Ollama doit tourner en local sur `http://localhost:11434`.

## Roadmap

- **Phase 1** ✅ : Structure projet, environnement dev, repo public
- **Phase 2** ✅ : Interface chat (Welcome/RGPD, Pseudo, Chat), historique SQLite, streaming NDJSON
- **Phase 3** ✅ : Build statique frontend, packaging air-gap, systemd kiosk, protocole export données
- **Phase 4 (en cours)** : Pilote Bistrot de Nérigean — feature inactivité déployée, RustDesk autostart actif. Avant déploiement : test protocole récupération données, feature eau économisée, retrait accès root SSH

Voir [roadmap_robert-ia.md](roadmap_robert-ia.md) pour le détail.

## Contribution

Consultez [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT — voir [LICENSE](LICENSE)

## Contact

[servomorph14@gmail.com](mailto:servomorph14@gmail.com)
e 