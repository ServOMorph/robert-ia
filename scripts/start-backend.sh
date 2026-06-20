#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$APP_DIR/app/backend"
VENV_DIR="$APP_DIR/.venv"
LOG_DIR="$APP_DIR/logs"

mkdir -p "$LOG_DIR"
BACKEND_LOG="$LOG_DIR/backend.log"
STARTUP_LOG="$LOG_DIR/startup.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$STARTUP_LOG"; }

log "===== Démarrage Robert-IA backend ====="

log "Attente stabilité système..."
sleep 3

if ! command -v ollama &>/dev/null; then
    log "ERREUR : Ollama absent du PATH"
    exit 1
fi

log "Attente d'Ollama..."
for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/tags &>/dev/null; then
        log "Ollama prêt après ${i}s"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:11434/api/tags | grep -q "gemma3:4b"; then
    log "AVERTISSEMENT : modèle gemma3:4b non trouvé"
fi

if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
fi

log "Démarrage du backend FastAPI..."
cd "$BACKEND_DIR"
exec python -m uvicorn main:app --host 0.0.0.0 --port 8001 --log-level warning >> "$BACKEND_LOG" 2>&1
