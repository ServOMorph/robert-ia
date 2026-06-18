# Phase 3 — Déploiement air-gap : Résumé complet

**Date** : 2026-06-18  
**Status** : ✅ COMPLÉTÉE

---

## Objectif de la Phase 3

Préparer Robert-IA pour déploiement air-gap sur machine isolée (Bistrot de Nérigean), avec :
- ✅ Build frontend statique compilé
- ✅ Packaging complet sur disque dur
- ✅ Protocole d'export données
- ✅ Configuration démarrage automatique (systemd + kiosk)

---

## Livrables produits

### 1. Build statique frontend (dist/)
**Fichier** : `frontend/dist/`  
**Contenu** :
- `index.html` (0.41 kB)
- `assets/index-*.css` (8.96 kB minifiée, 2.30 kB gzip)
- `assets/index-*.js` (149.30 kB minifiée, 48.35 kB gzip)
- Logo, icones, assets (PNG/SVG)

**Production** : `npm run build` dans `frontend/`

---

### 2. Script de packaging (`scripts/setup-airgap.sh`)
**Utilisation** :
```bash
./scripts/setup-airgap.sh /path/to/disk
```

**Produit** :
```
robert-ia/
├── app/backend/      (main.py, database.py, prompt.py, requirements.txt)
├── app/frontend/dist (React compilée)
├── data/             (SQLite — crée à runtime)
├── config/           (robert-ia.service, configurations systemd)
├── scripts/          (start.sh, start-kiosk.sh, install-systemd.sh)
└── DEPLOIEMENT.md    (guide court)
```

**Tests** :
- ✅ Packaging testé avec succès vers `/tmp/test-airgap-v2/`
- ✅ Structure complète vérifiée
- ✅ Tous les fichiers présents et accessibles

---

### 3. Scripts de lancement

#### `scripts/start-kiosk.sh`
**Mode** : Kiosk automatique (démarrage système)  
**Fonctionnalités** :
- Attente stabilité système (3 sec)
- Vérification Ollama disponible
- Vérification modèle gemma3:1b présent
- Activation venv Python (si créé)
- Démarrage backend FastAPI (port 8000)
- Lancement Firefox en mode kiosk fullscreen
- Gestion des logs dans `logs/`
- Cleanup propre à l'arrêt

**Usage** :
```bash
./scripts/start-kiosk.sh
# Ou via systemd:
sudo systemctl start robert-ia
```

#### `scripts/install-systemd.sh`
**Fonction** : Installation automatique du service systemd  
**Fait** :
- Copie `robert-ia.service` vers `/etc/systemd/system/`
- Crée `.venv` Python et installe dépendances
- Recharge systemd
- Affiche les commandes utiles

**Usage** :
```bash
sudo ./scripts/install-systemd.sh
```

---

### 4. Configuration systemd (`config/robert-ia.service`)
**Démarrage automatique** :
- Type: `simple`
- User: `root`
- ExecStart: `/opt/robert-ia/scripts/start-kiosk.sh`
- Redémarrage automatique en cas d'erreur (10 sec)
- Timeout 120 sec (Ollama peut être lent)
- Limites: CPU 80%, Mémoire 1 Go
- Logs: journal systemd

**Installation** :
```bash
sudo systemctl enable robert-ia     # démarrage auto
sudo systemctl start robert-ia      # lancement immédiat
journalctl -u robert-ia -f          # logs
```

---

### 5. Documentation

#### `docs/GUIDE_INSTALLATION_AIRGAP.md`
Guide complet 7 phases :
1. Préparation système (Ubuntu 24.04.1 LTS)
2. Installation dépendances (Python, Firefox, Ollama)
3. **Pré-téléchargement modèle gemma3:1b** (CRITIQUE)
4. Préparation disque USB
5. Copie et installation `/opt/robert-ia/`
6. Configuration systemd + démarrage automatique
7. Vérification fonctionnelle + troubleshooting

**Détails** :
- Checklist complète
- Commandes prêtes à copier-coller
- Troubleshooting pour erreurs courantes

#### `docs/PROTOCOLE_EXPORT_DONNEES.md`
Protocole complet d'export air-gap (4 phases) :
1. **Préparation** : Arrêt app, montage USB
2. **Export** : Copie `robert.db`, manifeste JSON, sync
3. **Transport & intégrité** : Montage serveur, vérification SQLite
4. **Nettoyage** : Archivage, purge optionnelle

**Spécificités** :
- RGPD complet (anonymat, consentement, droit à l'oubli)
- Anonymisation pseudos (optionnel)
- Format gzip pour archives
- Checklist 11 items

---

## Architecture finale

```
Machine air-gap (Ubuntu 24.04 LTS, i3-4130, 4 Go RAM, 120 Go SSD)

┌─────────────────────────────────────────────────────┐
│ /opt/robert-ia/                                     │
├─────────────────────────────────────────────────────┤
│ app/                                                │
│  ├── backend/ (main.py, database.py, prompt.py)    │
│  │    └── req: FastAPI, Ollama client              │
│  └── frontend/dist/ (React compilée, assets)       │
│                                                     │
│ data/robert.db  (SQLite, messages + sessions)      │
│                                                     │
│ scripts/                                            │
│  ├── start-kiosk.sh (démarrage auto systemd)       │
│  ├── start.sh (lancement manuel)                   │
│  └── install-systemd.sh (setup service)            │
│                                                     │
│ config/                                             │
│  └── robert-ia.service (systemd config)            │
│                                                     │
│ logs/                                               │
│  ├── startup.log                                    │
│  ├── backend.log                                    │
│  └── browser.log                                    │
└─────────────────────────────────────────────────────┘

Processus démarrage :
1. Système démarre → systemd lance robert-ia.service
2. start-kiosk.sh attend Ollama + backend
3. Firefox ouvre en kiosk fullscreen
4. SQLite synchronise à chaque message
5. Export données possibles par USB
```

---

## Tests réalisés

✅ **Build frontend** : Success (618 ms)  
✅ **Packaging** : Success (structure complète vérifiée)  
✅ **Scripts** : Exécutables et testés  
✅ **Systemd config** : Format valide  
✅ **Documentation** : Complète et prête  

⏳ **À tester en phase suivante** (Phase 4 — Déploiement pilote) :
- [ ] Démarrage complet sur machine réelle Ubuntu 24.04 LTS
- [ ] Vérification modèle Ollama chargé en RAM
- [ ] Conversation end-to-end via navigateur kiosk
- [ ] Export données par USB
- [ ] Redémarrage automatique après coupure électrique

---

## Points critiques pour déploiement

### ⚠️ Pré-télécharger le modèle AVANT air-gap
Le modèle gemma3:1b (1 Go) **doit être pré-téléchargé** sur la machine air-gap :
```bash
ollama pull gemma3:1b
```
Sinon, Ollama tentera de le télécharger → échouera sans Internet.

### ⚠️ Ollama en mode "serve" permanent
Ollama doit tourner en continu (systemd ou daemon) :
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### ⚠️ Firefox doit être installé
Le script `start-kiosk.sh` assume que `firefox` est présent.

### ⚠️ Ports 8000 et 11434 libres
- 8000 : Backend FastAPI
- 11434 : Ollama API

---

## Prochaines étapes (Phase 4)

**Déploiement pilote** au Bistrot de Nérigean :
1. [ ] Préparer machine air-gap avec Ubuntu 24.04
2. [ ] Installer dépendances (Python, Ollama, Firefox)
3. [ ] Pré-télécharger modèle gemma3:1b
4. [ ] Copier `/opt/robert-ia/` depuis disque USB
5. [ ] Exécuter `scripts/install-systemd.sh`
6. [ ] Vérifier démarrage automatique
7. [ ] Former animateurs + test utilisateurs
8. [ ] J+15 : récupérer données + analyse feedback
9. [ ] Itérations basées sur retours

---

## Références

- **Guide Installation** : `docs/GUIDE_INSTALLATION_AIRGAP.md`
- **Protocole Export** : `docs/PROTOCOLE_EXPORT_DONNEES.md`
- **Scripts** : `scripts/setup-airgap.sh`, `scripts/start-kiosk.sh`
- **Config** : `config/robert-ia.service`
- **Code** : `backend/main.py` (lifespan, keep_alive=-1, préchargement modèle)

---

## Checklist validation Phase 3

- [x] Frontend compilé (`frontend/dist/`)
- [x] Script packaging robuste et testé
- [x] Scripts lancement (manual + kiosk + systemd install)
- [x] Configuration systemd complète
- [x] Protocole export données RGPD-compliant
- [x] Guide installation 7 phases
- [x] Documentation troubleshooting
- [x] Tous les fichiers testés
- [ ] _(Phase 4)_ Test end-to-end machine réelle

---

**Status** : ✅ **PHASE 3 COMPLETE — Ready for Phase 4 (Pilot Deployment)**
