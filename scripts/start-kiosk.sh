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

log "Lancement Chromium kiosk..."
exec chromium-browser --kiosk   --no-sandbox   --disable-extensions   --disable-background-networking   --disable-default-apps   --no-first-run   --renderer-process-limit=1   --disable-features=Translate   "http://localhost:8001" >> "$KIOSK_LOG" 2>&1
