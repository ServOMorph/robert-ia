#!/bin/bash

# Installation de la configuration systemd pour démarrage automatique Robert-IA

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$APP_DIR/config"

if [ "$EUID" -ne 0 ]; then
    echo "❌ Ce script doit être exécuté en tant que root (sudo)"
    exit 1
fi

echo "🔧 Installation Robert-IA comme service systemd..."
echo ""

# 1. Copier le service
echo "📋 Installation du fichier de service..."
cp "$CONFIG_DIR/robert-ia.service" /etc/systemd/system/
chmod 644 /etc/systemd/system/robert-ia.service
echo "   ✅ /etc/systemd/system/robert-ia.service"

# 2. Rendre le script exécutable
echo "🔓 Configuration des permissions..."
chmod +x "$APP_DIR/scripts/start-kiosk.sh"
chmod +x "$APP_DIR/scripts/start.sh"

# 3. Créer le répertoire de logs
mkdir -p "$APP_DIR/logs"
chmod 755 "$APP_DIR/logs"

# 4. Créer l'environnement virtuel Python (si nécessaire)
if ! [ -d "$APP_DIR/.venv" ]; then
    echo "🐍 Création de l'environnement virtuel Python..."
    python3 -m venv "$APP_DIR/.venv"
    source "$APP_DIR/.venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$APP_DIR/app/backend/requirements.txt"
    echo "   ✅ Dépendances installées"
fi

# 5. Recharger systemd
echo "♻️  Rechargement de systemd..."
systemctl daemon-reload
echo "   ✅ systemd rechargé"

echo ""
echo "✅ Installation terminée!"
echo ""
echo "Commandes utiles:"
echo ""
echo "  Démarrer le service :"
echo "    sudo systemctl start robert-ia"
echo ""
echo "  Arrêter le service :"
echo "    sudo systemctl stop robert-ia"
echo ""
echo "  Voir le statut :"
echo "    sudo systemctl status robert-ia"
echo ""
echo "  Voir les logs :"
echo "    journalctl -u robert-ia -f"
echo ""
echo "  Démarrage automatique (à chaque reboot) :"
echo "    sudo systemctl enable robert-ia"
echo ""
echo "  Désactiver le démarrage automatique :"
echo "    sudo systemctl disable robert-ia"
echo ""
