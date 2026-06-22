# Optimisation RAM — Robert-IA (2026-06-22)

Contexte : i3-4130, 4 Go RAM, Ubuntu 24.04 GNOME Shell/Wayland, gemma3:4b.

---

## Résultat des optimisations

| Avant | Après |
|---|---|
| 2,8 Go RAM utilisés | 1,4–2,7 Go selon état |
| 2,9 Go swap utilisés | 400 Mo–2,8 Go selon état |
| 938 Mo disponibles | 1,0–2,3 Go disponibles |

---

## 1. Ollama — désactiver le chargement complet en RAM (gain : +1,4 Go)

Par défaut, Ollama charge les 2,5 Go du modèle entièrement en RAM/swap (`--no-mmap`).
Avec `OLLAMA_NO_MMAP=false`, le système charge les pages du modèle à la demande (mmap).

Éditer `/etc/systemd/system/ollama.service` :

```ini
[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=..."
Environment="OLLAMA_NO_MMAP=false"
Environment="OLLAMA_KEEP_ALIVE=5m"
```

Appliquer :
```bash
sudo systemctl daemon-reload && sudo systemctl restart ollama
```

`OLLAMA_KEEP_ALIVE=5m` décharge le modèle de la RAM 5 minutes après la dernière conversation,
libérant ~1,3 Go supplémentaires entre les sessions.

---

## 2. Désactiver les services GNOME inutiles (gain : ~150 Mo)

```bash
systemctl --user mask tracker-miner-fs-3.service \
  tracker-writeback-3.service \
  evolution-source-registry.service \
  evolution-calendar-factory.service \
  evolution-addressbook-factory.service
```

Ces services (indexation fichiers, données calendrier) sont inutiles en contexte kiosk.

---

## 3. Navigateur kiosk : Chromium au lieu de Firefox snap (gain : ~200 Mo)

Firefox snap utilisait ~1,15 Go avec de nombreux processus. Remplacé par Chromium snap
avec flags de limitation :

Fichier : `/opt/robert-ia/scripts/start-kiosk.sh`

```bash
exec chromium-browser --kiosk \
  --no-sandbox \
  --disable-extensions \
  --disable-background-networking \
  --disable-default-apps \
  --no-first-run \
  --renderer-process-limit=1 \
  --disable-features=Translate \
  "http://localhost:8001"
```

Chromium utilise ~960 Mo RSS en kiosk.

---

## 4. RustDesk — désactivé au démarrage automatique (gain : ~238 Mo)

RustDesk (accès distant graphique) était lancé automatiquement. Désactivé car le PC Linux
est utilisé avec son propre clavier/souris sur site.

```bash
sudo systemctl stop rustdesk
sudo systemctl disable rustdesk
```

L'accès SSH reste disponible pour la maintenance à distance (voir `CONTROLE_SSH_CLAUDE.md`).

Pour relancer RustDesk ponctuellement si besoin :
```bash
sudo systemctl start rustdesk
```

---

## État mémoire de référence (au boot, kiosk chargé)

```
Mem:   3,7Gi   2,7Gi utilisés   1,0Gi disponibles
Swap:  3,7Gi   2,8Gi utilisés
```

Quand le modèle Ollama se décharge (après 5 min d'inactivité) :
```
Mem:   3,7Gi   1,4Gi utilisés   2,3Gi disponibles
Swap:  3,7Gi   400Mi utilisés
```
