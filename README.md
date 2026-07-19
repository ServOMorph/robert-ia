# Robert-IA — Assistant conversationnel 100% local et déconnecté pour espaces associatifs

Robert-IA est un assistant virtuel conversationnel, confidentiel et autonome, conçu pour être déployé en mode *air-gap* (sans accès Internet) dans des tiers-lieux, bistrots associatifs ou espaces publics. Grâce à une exécution purement locale du modèle de langage, Robert-IA offre une expérience interactive interactive tout en garantissant un respect absolu de la vie privée et de la confidentialité (zéro tracking, aucune fuite de données vers des serveurs tiers).

---

## 🛠 Stack technique

* **OS cible** : Ubuntu 24.04 LTS (GNOME Shell / Chromium Kiosk)
* **IA locale** : [Ollama](https://ollama.com/) avec le modèle de langage `gemma3:4b`
* **Serveur Backend** : Python (FastAPI) pour l'API locale, le streaming NDJSON et le RAG léger
* **Base de données** : SQLite (persistance locale de l'historique des conversations anonymisées)
* **Interface Frontend** : React + Vite (compilé statiquement pour un chargement instantané)
* **Affichage** : Mode Kiosk plein écran verrouillé
* **Déploiement** : Packaging disque dur / clé USB pour environnements isolés du réseau

---

## 📐 Architecture et fonctionnement

Robert-IA s'exécute intégralement sur une unique machine physique sans aucune carte réseau active.

```mermaid
flowchart TD
    subgraph PC_Local ["PC Local (Air-Gap / Sans Internet)"]
        direction TB
        Chromium["Chromium Kiosk (Interface React)"] <-->|HTTP / NDJSON Stream| FastAPI["Backend FastAPI (Python)"]
        FastAPI <-->|Lecture & Écriture| SQLite[("Base SQLite (Historique)")]
        FastAPI <-->|Système Prompt & RAG| Knowledge["Base de connaissances (knowledge.txt)"]
        FastAPI <-->|Requêtes LLM locales (port 11434)| Ollama["Ollama (Modèle gemma3:4b)"]
    end
```

### Principes clés :
1. **RAG Local de niveau 2** : Le serveur backend FastAPI charge au démarrage une base de connaissances textuelle locale (`knowledge.txt`, contenant les détails du lieu comme le Bistrot de Nérigean / L'Invariable). Ce contexte est injecté dynamiquement dans le System Prompt.
2. **System Prompt à 3 niveaux** :
   * **Niveau 1** : Culture générale (Gemma 3).
   * **Niveau 2** : Réponses spécifiques basées sur le contexte local de l'association.
   * **Niveau 3** : Refus poli avec explication pédagogique pour les requêtes dépendantes d'Internet (ex: météo en direct, actualités récentes).
3. **Sécurité et RGPD** :
   * Consentement explicite à l'accueil de l'interface.
   * Modale de détection d'inactivité : après 10 minutes sans interaction, une alerte s'affiche avec un compte à rebours de 30 secondes pour réinitialiser la session et effacer l'historique visuel.
   * Script d'export (`analyse_conversations.py`) pour générer des statistiques anonymisées sous forme de CSV pour les animateurs de l'espace.

---

## 🚀 Installation (Environnement de développement)

### Prérequis
* Python 3.10+
* Node.js 18+
* Ollama configuré avec le modèle `gemma3:4b`

### Initialisation du projet

#### 1. Lancement du Backend
```bash
# Se positionner dans le dossier backend
cd backend

# Créer l'environnement virtuel et l'activer
python -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur backend
python main.py
```
Le serveur backend FastAPI écoute par défaut sur le port `8000`.

#### 2. Lancement du Frontend
```bash
# Se positionner dans le dossier frontend
cd ../frontend

# Installer les dépendances Node
npm install

# Lancer le serveur de développement Vite
npm run dev
```
Ouvrez votre navigateur sur l'adresse indiquée par Vite (généralement `http://localhost:5173`).

---

## 🗺️ Roadmap du projet

* **Phase 1** ✅ : Initialisation de la structure du projet, configuration de l'environnement de dev, dépôt public.
* **Phase 2** ✅ : Interface de chat (Welcome/RGPD, choix du Pseudo, Chat), historique SQLite local, streaming NDJSON.
* **Phase 3** ✅ : Compilations statiques, empaquetage air-gap, configuration du service systemd de Kiosk, script d'export.
* **Phase 4 [EN COURS]** : Déploiement pilote au *Bistrot de Nérigean*. Intégration du mini-RAG avec `knowledge.txt` (L'Invariable), prompt à 3 niveaux, configuration du script Windows ↔ Linux. Tests en cours de la fonctionnalité de calcul d'économie d'eau (comparaison impact écologique local vs cloud) et suppression de l'accès root SSH.

Pour plus de détails, consultez la feuille de route complète : [roadmap_robert-ia.md](roadmap_robert-ia.md).

---

## 🤝 Contribution

Les contributions ou retours sur les déploiements air-gap sont les bienvenus. Veuillez consulter le guide [CONTRIBUTING.md](CONTRIBUTING.md) pour plus d'informations.

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Pour plus de détails, reportez-vous au fichier [LICENSE](LICENSE) à la racine du dépôt.

---

## 📬 Contact

Pour toute question ou demande d'accompagnement à l'installation dans un tiers-lieu : [servomorph14@gmail.com](mailto:servomorph14@gmail.com)