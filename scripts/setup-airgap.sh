#!/bin/bash

set -e

# script de packaging pour déploiement air-gap
# Usage: ./scripts/setup-airgap.sh /path/to/target/disk

TARGET_DIR="${1:-.}"
APP_DIR="$TARGET_DIR/robert-ia"

echo "📦 Packaging Robert-IA pour déploiement air-gap..."
echo "   Destination: $APP_DIR"

# 1. Créer la structure de répertoires
echo "🗂️  Création de la structure..."
mkdir -p "$APP_DIR/app/backend"
mkdir -p "$APP_DIR/app/backend/data"
mkdir -p "$APP_DIR/app/frontend/dist"
mkdir -p "$APP_DIR/config"
mkdir -p "$APP_DIR/scripts"
mkdir -p "$APP_DIR/logs"

# 2. Copier le frontend compilé
echo "📄 Copie du frontend compilé..."
cp -r ./frontend/dist/* "$APP_DIR/app/frontend/dist/"

# 3. Copier les fichiers backend
echo "🐍 Copie du backend Python..."
cp ./backend/main.py "$APP_DIR/app/backend/"
cp ./backend/database.py "$APP_DIR/app/backend/"
cp ./backend/prompt.py "$APP_DIR/app/backend/"
cp ./backend/requirements.txt "$APP_DIR/app/backend/"

# 4. Copier les scripts de lancement
echo "🚀 Installation des scripts de lancement..."
cp ./scripts/start-kiosk.sh "$APP_DIR/scripts/start-kiosk.sh"
chmod +x "$APP_DIR/scripts/start-kiosk.sh"

# Script de démarrage manuel (simple)
cat > "$APP_DIR/scripts/start.sh" << 'EOF'
#!/bin/bash
# Script de lancement simple (mode manuel, sans kiosk)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$APP_DIR/app/backend"

echo "🚀 Démarrage du backend Robert-IA..."

# 1. Vérifier Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Erreur : Ollama n'est pas installé"
    exit 1
fi

# 2. Démarrer le backend FastAPI
cd "$BACKEND_DIR"
python -m uvicorn main:app --host 0.0.0.0 --port 8001

EOF

chmod +x "$APP_DIR/scripts/start.sh"

# 5. Copier la configuration systemd et le script d'installation
echo "⚙️  Installation de la configuration systemd..."
cp ./config/robert-ia.service "$APP_DIR/config/robert-ia.service"
cp ./scripts/install-systemd.sh "$APP_DIR/scripts/install-systemd.sh"
chmod +x "$APP_DIR/scripts/install-systemd.sh"

# 6. Créer le README de déploiement
echo "📝 Création du README de déploiement..."
cat > "$APP_DIR/DEPLOIEMENT.md" << 'EOF'
# Déploiement air-gap de Robert-IA

## Structure

```
robert-ia/
├── app/
│   ├── backend/       # Serveur FastAPI
│   └── frontend/dist/ # Interface React compilée
├── data/              # Données SQLite (générées à l'exécution)
├── config/            # Configuration systemd
└── scripts/           # Scripts de lancement
```

## Prérequis
- Ubuntu 24.04.1 LTS
- Ollama installé avec modèle `gemma3:4b` pré-téléchargé
- Python 3.11+

## Installation
1. Copier le dossier `robert-ia/` vers `/opt/robert-ia/`
2. Installer les dépendances Python :
   ```bash
   cd /opt/robert-ia/app/backend
   pip install -r requirements.txt
   ```
3. (Optionnel) Copier la config systemd :
   ```bash
   sudo cp config/robert-ia.service /etc/systemd/system/
   sudo systemctl daemon-reload
   ```

## Lancement
- **Mode manuel** : `./scripts/start.sh`
- **Mode systemd** : `sudo systemctl start robert-ia`
- **Logs systemd** : `journalctl -u robert-ia -f`

## Export des données
Les données (messages, sessions) sont sauvegardées dans `data/robert.db`.
Pour récupérer les données :
1. Arrêter l'application
2. Copier `data/robert.db` vers clé USB
3. Transférer vers le serveur central

## Troubleshooting
- Si le navigateur ne se lance pas : vérifier que `firefox` est installé
- Si Ollama n'est pas disponible : vérifier `ollama serve` et `ollama list`
- Si le port 8000 est occupé : modifier `scripts/start.sh` et changer le port
EOF

# 7. Résumé
echo ""
echo "✅ Packaging terminé!"
echo ""
echo "Structure créée:"
echo "  $APP_DIR/"
echo "  ├── app/backend/  (FastAPI + BD)"
echo "  ├── app/frontend/ (React compilée)"
echo "  ├── data/         (SQLite)"
echo "  ├── config/       (systemd)"
echo "  └── scripts/      (lancement)"
echo ""
echo "Prochaines étapes:"
echo "  1. Pré-télécharger le modèle Ollama: ollama pull gemma3:4b"
echo "  2. Copier le dossier sur disque dur"
echo "  3. Lancer sur machine air-gap: ./scripts/start.sh"
echo ""
