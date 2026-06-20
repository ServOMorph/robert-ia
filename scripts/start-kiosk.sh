#!/bin/bash

set -e

# Script de lancement Robert-IA avec navigateur kiosk (démarrage automatique)
# À utiliser via systemd pour démarrage automatique à l'allumage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$APP_DIR/app/backend"
FRONTEND_DIR="$APP_DIR/app/frontend/dist"
VENV_DIR="$APP_DIR/.venv"

LOG_DIR="$APP_DIR/logs"
mkdir -p "$LOG_DIR"

OLLAMA_LOG="$LOG_DIR/ollama.log"
BACKEND_LOG="$LOG_DIR/backend.log"
STARTUP_LOG="$LOG_DIR/startup.log"

{
    echo "===== Démarrage Robert-IA ====="
    echo "Timestamp: $(date)"
    echo "PWD: $APP_DIR"
    echo ""

    # 1. Attendre que le réseau soit prêt (optionnel, pour cas où ethernet commence lentement)
    echo "⏳ Attente stabilité système..."
    sleep 3

    # 2. Vérifier Ollama
    echo "🤖 Vérification d'Ollama..."
    if ! command -v ollama &> /dev/null; then
        echo "❌ ERREUR : Ollama n'est pas dans le PATH"
        echo "   Installer Ollama ou ajouter au PATH"
        exit 1
    fi

    # 3. Attendre que Ollama soit disponible (test connec)
    echo "⏳ Attente d'Ollama..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags &>/dev/null; then
            echo "✅ Ollama répondu après $i secondes"
            break
        fi
        sleep 1
    done

    # 4. Vérifier le modèle gemma3:4b
    echo "📦 Vérification du modèle..."
    if ! curl -s http://localhost:11434/api/tags | grep -q "gemma3:4b"; then
        echo "⚠️  AVERTISSEMENT : Modèle gemma3:4b non trouvé"
        echo "   À pré-charger avant déploiement : ollama pull gemma3:4b"
    fi

    # 5. Activer l'environnement virtuel Python (si utilisé)
    if [ -d "$VENV_DIR" ]; then
        echo "🐍 Activation de l'environnement virtuel..."
        source "$VENV_DIR/bin/activate"
    fi

    # 6. Démarrer le backend FastAPI
    echo "🔙 Démarrage du backend..."
    cd "$BACKEND_DIR"
    python -m uvicorn main:app --host 0.0.0.0 --port 8001 --log-level warning >> "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
    echo "   PID: $BACKEND_PID"
    sleep 2

    # Vérifier que le backend s'est bien lancé
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ ERREUR : Backend n'a pas pu démarrer"
        cat "$BACKEND_LOG"
        exit 1
    fi

    # 7. Vérifier que le backend répond
    echo "⏳ Attente du backend..."
    for i in {1..10}; do
        if curl -s http://localhost:8001/health &>/dev/null; then
            echo "✅ Backend prêt"
            break
        fi
        sleep 1
    done

    # 8. Lancer le navigateur en mode kiosk
    echo "🌐 Démarrage du navigateur kiosk..."

    # Nettoyer les lockfiles Firefox (parfois cassés au redémarrage)
    rm -rf ~/.mozilla/firefox/*.default-*/lock ~/.mozilla/firefox/*.default-*/.parentlock 2>/dev/null || true

    # Lancer Firefox en kiosk fullscreen
    # Note: --new-instance empêche Firefox de se connecter à une instance existante
    firefox \
        --new-instance \
        --kiosk \
        "http://localhost:8001" \
        --no-remote \
        >> "$LOG_DIR/browser.log" 2>&1 &
    BROWSER_PID=$!
    echo "   PID: $BROWSER_PID"

    echo ""
    echo "✅ Robert-IA démarré avec succès"
    echo "   Backend: http://localhost:8001"
    echo "   Frontend: kiosk fullscreen"
    echo "   Logs: $LOG_DIR/"
    echo ""

    # 9. Attendre et gérer les processus
    # Si Ctrl+C ou fermeture navigateur -> on arrête tout proprement
    trap "echo '🛑 Arrêt en cours...'; kill $BACKEND_PID $BROWSER_PID 2>/dev/null || true; exit 0" INT TERM

    # Attendre que l'un des processus principaux s'arrête
    wait -n

    echo ""
    echo "⚠️  Un processus s'est arrêté. Nettoyage..."
    kill $BACKEND_PID $BROWSER_PID 2>/dev/null || true
    exit 1

} | tee -a "$STARTUP_LOG"
