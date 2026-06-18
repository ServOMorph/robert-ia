# Guide complet d'installation Robert-IA (air-gap)

## Prérequis

### Matériel
- **CPU** : i3-4130 ou équivalent (Quad-core 3 GHz)
- **RAM** : 4 Go minimum (+ 2-3 Go pour Ollama gemma3:1b)
- **Disque** : 120 Go SSD recommandé
- **GPU** : Non requis (CPU suffisant pour gemma3:1b)

### Système d'exploitation
- **Ubuntu 24.04.1 LTS** (XFCE Desktop)
- Accès root ou sudo
- Connexion Internet (pour phase d'installation seulement)

### Logiciels
- Ollama (avec modèle gemma3:1b pré-téléchargé)
- Python 3.11+
- Firefox ou Chromium (navigateur kiosk)

---

## Phase 1 : Préparation du système

### 1.1 Mise à jour du système
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Installation des dépendances
```bash
sudo apt install -y \
    python3.11 \
    python3-venv \
    python3-pip \
    curl \
    firefox \
    xfce4 \
    xfce4-goodies \
    sqlite3 \
    git
```

### 1.3 Installation d'Ollama
```bash
# Télécharger le script d'installation
curl -fsSL https://ollama.ai/install.sh | sh

# Vérifier l'installation
ollama --version
```

### 1.4 Pré-télécharger le modèle (TRÈS IMPORTANT)
**Cette étape doit être faite avant le déploiement air-gap.**

```bash
# Lancer Ollama en arrière-plan
ollama serve &

# Attendre quelques secondes
sleep 3

# Télécharger le modèle (400-500 MB)
ollama pull gemma3:1b

# Vérifier
ollama list | grep gemma3:1b
```

**Résultat attendu :**
```
gemma3:1b      0acb3e0f30e7   1.0 GB
```

### 1.5 Vérifier la disponibilité d'Ollama
```bash
curl http://localhost:11434/api/tags
# Doit retourner du JSON avec le modèle listés
```

---

## Phase 2 : Préparation du disque de déploiement

### 2.1 Préparer le packaging sur machine de développement
```bash
# Sur la machine de développement (avec Internet)
cd /path/to/robert-ia

# Compiler le frontend
cd frontend && npm run build && cd ..

# Générer le packaging complet
./scripts/setup-airgap.sh /tmp/deployment

# Copier vers disque USB
sudo mount /dev/sdX1 /mnt/usb
sudo cp -r /tmp/deployment/robert-ia /mnt/usb/
sudo umount /mnt/usb
```

### 2.2 Transférer le disque USB vers la machine air-gap
- Brancher le disque USB
- Créer un point de montage

---

## Phase 3 : Installation sur la machine air-gap

### 3.1 Monter le disque USB
```bash
# Identifier le disque
lsblk

# Créer un point de montage
sudo mkdir -p /mnt/usb
sudo mount /dev/sdX1 /mnt/usb

# Vérifier
ls /mnt/usb/robert-ia/
```

### 3.2 Copier l'application
```bash
# Copier vers /opt/
sudo cp -r /mnt/usb/robert-ia /opt/

# Fixer les permissions
sudo chown -R root:root /opt/robert-ia
sudo chmod -R 755 /opt/robert-ia
```

### 3.3 Installer les dépendances Python
```bash
cd /opt/robert-ia/app/backend

# Créer l'environnement virtuel (si pas déjà fait)
python3 -m venv /opt/robert-ia/.venv
source /opt/robert-ia/.venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.4 Vérifier le déploiement
```bash
# Tester que tout est accessible
ls -la /opt/robert-ia/app/backend/main.py
ls -la /opt/robert-ia/app/frontend/dist/index.html
ls -la /opt/robert-ia/config/robert-ia.service
```

---

## Phase 4 : Configuration du démarrage automatique

### 4.1 Installer le service systemd
```bash
sudo bash /opt/robert-ia/scripts/install-systemd.sh
```

**Résultat attendu :**
```
✅ Installation terminée!
```

### 4.2 Activer le démarrage automatique
```bash
# Faire démarrer le service à chaque reboot
sudo systemctl enable robert-ia

# Vérifier
sudo systemctl is-enabled robert-ia
# Retour: "enabled"
```

### 4.3 Démarrer le service
```bash
# Lancer manuellement
sudo systemctl start robert-ia

# Vérifier le statut
sudo systemctl status robert-ia

# Voir les logs en temps réel
journalctl -u robert-ia -f
```

---

## Phase 5 : Vérification fonctionnelle

### 5.1 Vérifier les services
```bash
# Vérifier Ollama
curl http://localhost:11434/api/tags

# Vérifier le backend
curl http://localhost:8000/health
# Résultat attendu: {"status":"ok"}
```

### 5.2 Vérifier l'interface utilisateur
- Le navigateur Firefox doit s'ouvrir en kiosk (fullscreen)
- Écran Welcome/RGPD → bouton "J'accepte"
- Écran de saisie du pseudo
- Écran de chat fonctionnel

### 5.3 Tester une conversation
1. Entrer un pseudo (ex: "Test")
2. Envoyer un message : "Bonjour"
3. Vérifier que le modèle répond (quelques secondes d'attente)
4. Vérifier que le message apparaît dans la base de données :
   ```bash
   sqlite3 /opt/robert-ia/data/robert.db "SELECT COUNT(*) FROM messages;"
   ```

---

## Phase 6 : Configuration avancée

### 6.1 Configurer le XFCE pour démarrage automatique
Pour que le service démarre APRÈS le login XFCE (optionnel) :

1. Accéder aux paramètres XFCE (Settings → Session and Startup)
2. Onglet "Application Autostart"
3. Ajouter une nouvelle application :
   ```
   Name: Robert-IA
   Description: Interface IA locale
   Command: systemctl start robert-ia
   ```

### 6.2 Rediriger le port pour accès distant (seulement si nécessaire)
```bash
# Éditer /opt/robert-ia/app/backend/main.py
# Changer allow_origins pour ajouter l'IP distante
```

### 6.3 Augmenter les limites de mémoire
```bash
# Si Ollama prend trop de RAM
sudo vi /etc/systemd/system/robert-ia.service
# Modifier MemoryLimit=1G → MemoryLimit=2G
```

---

## Phase 7 : Opérations courantes

### Arrêter le service
```bash
sudo systemctl stop robert-ia
```

### Redémarrer
```bash
sudo systemctl restart robert-ia
```

### Voir les logs
```bash
# Les 50 dernières lignes
journalctl -u robert-ia -n 50

# Suivi en temps réel
journalctl -u robert-ia -f

# Entre deux timestamps
journalctl -u robert-ia --since "2026-06-18 10:00" --until "2026-06-18 11:00"
```

### Vérifier l'espace disque
```bash
df -h /opt/robert-ia
du -sh /opt/robert-ia/data/
du -sh /opt/robert-ia/app/frontend/
```

---

## Troubleshooting

### Problème: Firefox ne se lance pas
```bash
# Cause possible: Xvfb/DISPLAY non configuré
# Solution:
DISPLAY=:0 firefox --kiosk file:///opt/robert-ia/app/frontend/dist/index.html
```

### Problème: "Ollama non disponible" dans l'interface
```bash
# Vérifier que Ollama écoute
netstat -tuln | grep 11434

# Ou directement:
curl -i http://localhost:11434/api/tags
```

### Problème: Backend plante au démarrage
```bash
# Voir les logs détaillés
journalctl -u robert-ia -n 100

# Tester le backend directement
cd /opt/robert-ia/app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Problème: BD corrompue
```bash
# Vérifier l'intégrité
sqlite3 /opt/robert-ia/data/robert.db "PRAGMA integrity_check;"

# Récupérer si corruption
sqlite3 /opt/robert-ia/data/robert.db ".recover" | sqlite3 /tmp/robert_fixed.db
sudo cp /tmp/robert_fixed.db /opt/robert-ia/data/robert.db
```

### Problème: Port 8000 déjà occupé
```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus (si besoin)
sudo kill -9 <PID>

# Ou changer le port dans main.py
```

---

## Checklist d'installation complète

- [ ] Ubuntu 24.04.1 LTS installé
- [ ] Dépendances système installées (Python, Firefox, etc.)
- [ ] Ollama installé et modèle `gemma3:1b` pré-téléchargé
- [ ] Application copiée dans `/opt/robert-ia/`
- [ ] Dépendances Python installées (`.venv`)
- [ ] Service systemd installé
- [ ] Service activé pour démarrage automatique
- [ ] Vérification: Ollama, Backend, Frontend fonctionnent
- [ ] Test: Conversation complète fonctionne
- [ ] Vérification: BD SQLite enregistre les messages
- [ ] Configuration XFCE (optionnel)
- [ ] Documentation locale (ce guide) sauvegardée

---

## Support et documentation

- **Logs**: `journalctl -u robert-ia -f`
- **Documentation**: `/opt/robert-ia/DEPLOIEMENT.md`
- **Protocole export**: `/opt/robert-ia/../PROTOCOLE_EXPORT_DONNEES.md`
- **Backend logs**: `/opt/robert-ia/logs/backend.log`
- **Startup logs**: `/opt/robert-ia/logs/startup.log`

Pour assistance supplémentaire, consulter l'équipe technique ou GitHub.
