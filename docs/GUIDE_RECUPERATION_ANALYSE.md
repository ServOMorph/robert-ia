# Guide complet — Récupération et analyse des conversations

Ce guide couvre le flux complet : récupération des données depuis le PC Linux (air-gap) vers disque USB, puis analyse sur PC Windows.

---

## Vue d'ensemble

```
PC Linux (Bistrot)              Disque USB              PC Windows
┌─────────────────┐          ┌──────────┐          ┌──────────────┐
│ robert.db       │  copier  │          │  copier  │ CSV analysé  │
│ (SQLite local)  ├─────────>│ USB HDD  ├─────────>│ (Excel)      │
└─────────────────┘          └──────────┘          └──────────────┘
```

---

## Phase 1 — Récupération sur PC Linux

### Préparation

1. **Brancher le disque dur USB** sur le PC Linux
2. **Vérifier le device USB** :
   ```bash
   lsblk
   # Chercher la ligne avec le disque USB (ex: sdb 8GB)
   ```

### Récupération

3. **Arrêter Robert-IA** (sinon la BD est verrouillée)
   ```bash
   sudo systemctl stop robert-ia
   ```

4. **Monter le disque USB**
   ```bash
   sudo mkdir -p /mnt/usb
   sudo mount /dev/sdb1 /mnt/usb
   # Adapter sdb1 au device détecté à l'étape 2
   ```

5. **Copier la base de données**
   ```bash
   sudo cp /opt/robert-ia/backend/data/robert.db /mnt/usb/robert_$(date +%Y%m%d).db
   ```

6. **Synchroniser le disque**
   ```bash
   sync
   ```

7. **Démonter le disque**
   ```bash
   sudo umount /mnt/usb
   ```

8. **Redémarrer Robert-IA**
   ```bash
   sudo systemctl start robert-ia
   ```

9. **Vérifier le bon démarrage**
   ```bash
   curl http://localhost:8001/api/health
   # ou accéder au kiosk Firefox
   ```

### Résultat

Le disque USB contient maintenant `robert_YYYYMMDD.db` avec toutes les conversations.

---

## Phase 2 — Transport

- **Médium** : Disque dur USB (conserver hors ligne entre chaque récupération)
- **Sécurité** : Les données sont anonymes (pseudos uniquement, pas d'email ni identifiant)
- **Validation** : Vérifier que le fichier `.db` est présent et lisible sur le disque

---

## Phase 3 — Analyse sur PC Windows

### Préparation

1. **Brancher le disque dur USB** sur le PC Windows
2. **Créer un dossier de travail** (ex: `C:\Users\MonNom\Desktop\analyse`)
3. **Copier depuis le disque USB** :
   - `robert_YYYYMMDD.db` → le dossier de travail
   - `scripts/analyse_conversations.py` (depuis le repo robert-ia) → le dossier de travail

### Lancer l'analyse

4. **Ouvrir PowerShell dans ce dossier**
   - Shift + clic droit → "Ouvrir la fenêtre PowerShell ici"

5. **Exécuter le script**
   ```powershell
   python analyse_conversations.py robert_YYYYMMDD.db
   ```

### Résultat

Le script produit deux sorties :

**A. Affichage console** — stats globales et par session
```
============================================================
  ANALYSE CONVERSATIONS — ROBERT-IA
============================================================
  Fichier     : robert_20260621.db
  Export CSV  : conversations_20260621_1430.csv
  Généré le   : 2026-06-21 14:30
------------------------------------------------------------
  Total messages      : 157
  Sessions distinctes : 23
  Pseudos distincts   : 21
  Première session    : 2026-06-10 09:12:00
  Dernière session    : 2026-06-21 11:45:00
  Longueur moy. msg   : 142 caractères
------------------------------------------------------------
  [Détail par session...]
============================================================
```

**B. Fichier CSV** — `conversations_YYYYMMDD_HHMM.csv` (point-virgule, UTF-8-BOM)
- Colonnes : `id`, `session_id`, `pseudo`, `role`, `content`, `created_at`
- Ouvrable directement dans Excel

---

## Phase 4 — Lecture et exploitation

### Ouvrir le CSV dans Excel

1. Ouvrir Excel
2. Données → À partir d'un fichier texte/CSV
3. Sélectionner `conversations_YYYYMMDD_HHMM.csv`
4. Délimiteur : point-virgule (`;`)

### Analyser

Le CSV contient chaque message avec :
- **Qui** : le pseudo
- **Quand** : date et heure précise
- **Quoi** : le contenu du message (questions et réponses)

Cas d'usage courants :
- Identifier les sessions avec le plus d'interaction
- Chercher des patterns dans les questions posées
- Valider la qualité des réponses du modèle
- Évaluer le confort d'usage (longueur des messages, fréquence)

---

## Troubleshooting

### Phase 1 — Linux

| Erreur | Cause | Solution |
|--------|-------|----------|
| `database is locked` | Robert-IA tourne toujours | `sudo systemctl stop robert-ia` |
| `device not found` | Mauvais device USB | Relancer `lsblk` et adapter |
| `Permission denied` | Permissions de montage | Utiliser `sudo` pour mount/umount/cp |

### Phase 3 — Windows

| Erreur | Cause | Solution |
|--------|-------|----------|
| `python n'est pas reconnu` | Python non installé | Installer depuis [python.org](https://python.org), cocher "Add to PATH" |
| `Fichier introuvable` | Chemin incorrect | Vérifier le chemin exact : `dir robert_*.db` |
| Accents illisibles dans Excel | Encodage mal détecté | Utiliser l'import "À partir d'un fichier texte/CSV" plutôt que double-clic |

---

## Checklist de visite (J+15 Bistrot de Nérigean)

- [ ] Disque USB branché sur PC Linux
- [ ] `lsblk` lancé, device USB identifié
- [ ] `sudo systemctl stop robert-ia` exécuté
- [ ] Disque monté et copie effectuée
- [ ] `sync` exécuté, disque démonté
- [ ] Robert-IA redémarré et vérifié
- [ ] Disque transporté sur PC Windows
- [ ] `analyse_conversations.py` lancé sans erreur
- [ ] Statistiques console relues (sessions, messages, dates)
- [ ] CSV ouvert dans Excel (lecture visuelle)
- [ ] Observations consignées dans rapport de visite

---

## Évolutions possibles

- [ ] Automatiser export via cron (toutes les 24h) si mode semi-connecté
- [ ] Dashboard d'analyse temps réel (pseudonyme + stats)
- [ ] Chiffrement des données lors du transport (AES-256)
- [ ] Anonymisation des pseudos avant export central
