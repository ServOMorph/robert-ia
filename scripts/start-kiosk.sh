#!/bin/bash

LOG_DIR="/opt/robert-ia/logs"
mkdir -p "$LOG_DIR"
KIOSK_LOG="$LOG_DIR/kiosk.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$KIOSK_LOG"; }

log "Attente du backend..."
for i in $(seq 1 60); do
    if curl -s http://localhost:8001/health &>/dev/null; then
        log "Backend prêt après ${i}s"
        break
    fi
    sleep 1
done

rm -f ~/.mozilla/firefox/*/lock ~/.mozilla/firefox/*/.parentlock 2>/dev/null || true

log "Lancement Firefox kiosk..."
exec firefox --new-instance --kiosk "http://localhost:8001" --no-remote >> "$KIOSK_LOG" 2>&1
