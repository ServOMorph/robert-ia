# Protocole d'export données air-gap

## Vue d'ensemble

Robert-IA fonctionne en mode air-gap (sans Internet) avec une base de données SQLite locale. Les données de session (conversations, pseudos, timestamps) restent sur la machine physique. Ce protocole décrit comment récupérer et traiter ces données.

---

## Architecture de stockage

### Localisation
- **Chemin** : `data/robert.db` (relatives au répertoire d'installation)
- **Permissions** : Lecture/écriture par l'application FastAPI
- **Sauvegarde automatique** : Synchronisation disque à chaque message enregistré

### Schéma
```sql
messages (
  id INTEGER PRIMARY KEY,
  session_id TEXT,
  pseudo TEXT,
  role TEXT ('user' ou 'assistant'),
  content TEXT,
  timestamp DATETIME
)
```

---

## Phase 1 : Préparation avant export

### Sur la machine associative (air-gap)

1. **Arrêter l'application** (sinon SQLite est verrouillé)
   ```bash
   sudo systemctl stop robert-ia
   # ou Ctrl+C si lancement manuel
   ```

2. **Vérifier que la BD est accessible**
   ```bash
   ls -lh /opt/robert-ia/data/robert.db
   ```

3. **(Optionnel) Compacter la BD**
   ```bash
   sqlite3 /opt/robert-ia/data/robert.db "VACUUM;"
   ```

4. **Monter le disque dur USB** (où on va copier les données)
   ```bash
   sudo mkdir -p /mnt/usb
   sudo mount /dev/sdX1 /mnt/usb
   ```

---

## Phase 2 : Export sur disque dur

### Copier la BD
```bash
sudo cp /opt/robert-ia/data/robert.db /mnt/usb/robert_YYYYMMDD.db
sudo chown $USER:$USER /mnt/usb/robert_YYYYMMDD.db
```

### Copier la sauvegarde de configuration
```bash
sudo cp /opt/robert-ia/config/robert-ia.service /mnt/usb/
```

### Créer un manifeste d'export
```bash
cat > /mnt/usb/export_manifest.json << 'EOF'
{
  "export_date": "2026-06-18T15:30:00Z",
  "machine": "Bistrot de Nérigean",
  "location": "Localité",
  "accumulated_messages": 157,
  "database_size": 45056,
  "database_file": "robert_20260618.db",
  "app_version": "1.0.0",
  "notes": "Export fin de semaine. Aucun incident."
}
EOF
```

### Synchroniser le disque
```bash
sync
```

### Démonter le disque
```bash
sudo umount /mnt/usb
```

---

## Phase 3 : Transport et intégration serveur

### Transport
- **Médium** : Disque dur USB ou clé USB (amovible)
- **Sécurité** : Les données sont anonymes (pas de données personnelles identifiantes, pseudos seuls)
- **Conservation** : Disque gardé hors ligne pour éviter contamination réseau

### À la réception (serveur central)

1. **Monter le disque**
   ```bash
   sudo mkdir -p /mnt/airgap-exports
   sudo mount /dev/sdY1 /mnt/airgap-exports
   ```

2. **Vérifier l'intégrité**
   ```bash
   sqlite3 /mnt/airgap-exports/robert_*.db ".tables"
   # doit afficher "messages"
   ```

3. **Copier vers archivage central**
   ```bash
   cp /mnt/airgap-exports/robert_*.db /var/lib/robert-ia/exports/
   cp /mnt/airgap-exports/export_manifest.json /var/lib/robert-ia/exports/
   ```

4. **Analyser les données (optionnel)**
   ```bash
   sqlite3 /var/lib/robert-ia/exports/robert_*.db << 'EOF'
   SELECT COUNT(*) as total_messages FROM messages;
   SELECT COUNT(DISTINCT session_id) as unique_sessions FROM messages;
   SELECT AVG(LENGTH(content)) as avg_message_length FROM messages;
   EOF
   ```

5. **Archiver et formater**
   ```bash
   gzip /var/lib/robert-ia/exports/robert_*.db
   mv /var/lib/robert-ia/exports/robert_*.db.gz /archive/robert-ia/$(date +%Y%m%d)_export.db.gz
   ```

---

## Phase 4 : Nettoyage et redémarrage

### Sur la machine associative

1. **Démonter le disque**
   ```bash
   sudo umount /mnt/usb
   ```

2. **Redémarrer l'application**
   ```bash
   sudo systemctl start robert-ia
   ```

3. **Vérifier le bon démarrage**
   ```bash
   sudo systemctl status robert-ia
   curl http://localhost:8000/health
   ```

4. **(Optionnel) Purger l'historique local** (si mandat = pas de conservation)
   ```bash
   rm /opt/robert-ia/data/robert.db
   # BD sera recréée à la réexécution
   ```

---

## Considérations légales et éthiques

### RGPD
- ✅ **Consentement** : Écran RGPD au démarrage, acceptation requise
- ✅ **Stockage** : Données restent en local (aucun transfert cloud)
- ✅ **Anonymat** : Pas d'email, pas de mot de passe, pseudo uniquement
- ⚠️ **Droit à l'oubli** : À implémenter si demande d'un utilisateur

### Processus d'anonymisation (avant export central)
Pour conformité maximale :
```bash
# Aléatoriser les pseudos (optionnel)
sqlite3 /var/lib/robert-ia/exports/robert_*.db << 'EOF'
UPDATE messages SET pseudo = 'user_' || SUBSTR(HEX(RANDOM()), 1, 6);
PRAGMA optimize;
EOF
```

---

## Checklist d'export

- [ ] Arrêter l'application
- [ ] Vérifier la présence de `robert.db`
- [ ] Compacter la BD (optionnel)
- [ ] Monter le disque USB
- [ ] Copier `robert.db` avec timestamp
- [ ] Créer `export_manifest.json`
- [ ] Synchroniser le disque (`sync`)
- [ ] Démonter le disque
- [ ] Vérifier le manifeste à la réception
- [ ] Archiver au format gzip
- [ ] Redémarrer l'application
- [ ] Purger l'historique (si mandat)

---

## Troubleshooting

### Erreur: "database is locked"
**Cause** : L'application FastAPI tient toujours la connexion.
**Solution** :
```bash
sudo systemctl stop robert-ia  # ou Ctrl+C
sleep 2
# Réessayer l'export
```

### Erreur: "database disk image is malformed"
**Cause** : Corruption possible due à un redémarrage brusque.
**Solution** :
```bash
sqlite3 /opt/robert-ia/data/robert.db ".recover" | sqlite3 /tmp/robert_recovered.db
cp /tmp/robert_recovered.db /opt/robert-ia/data/robert.db
```

### Le disque USB ne monte pas
**Diagnostic** :
```bash
lsblk  # identifier le périphérique
sudo dmesg | tail -20  # vérifier les erreurs kernel
```

---

## Évolutions futures

- [ ] Export chiffré (AES-256) pour sécurité accrue
- [ ] Synchronisation automatique toutes les 24h (si mode semi-connecté ajouté)
- [ ] Dashboard d'analyse des données (pseudonyme + timestamp + statistiques)
- [ ] Backup automatique sur disque interne (mode paranoia)
