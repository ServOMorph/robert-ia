# Protocole d'analyse des conversations — Robert-IA

Ce protocole couvre l'analyse des données de conversation récupérées depuis la machine associative (air-gap) sur un PC Windows.

**Prérequis :** avoir suivi le [PROTOCOLE_EXPORT_DONNEES.md](PROTOCOLE_EXPORT_DONNEES.md) et disposer du fichier `robert_YYYYMMDD.db` sur disque dur USB.

---

## Outillage requis

- Python 3.x installé sur le PC Windows ([python.org](https://python.org))
- Aucune dépendance externe (uniquement stdlib Python)

---

## Étape 1 — Récupérer les fichiers

Depuis le disque dur USB, copier sur le bureau Windows (ou tout dossier de travail) :
- `robert_YYYYMMDD.db` (base de données SQLite)
- `scripts/analyse_conversations.py` (depuis le repo Robert-IA)

---

## Étape 2 — Lancer l'analyse

Ouvrir un terminal Windows (PowerShell ou Invite de commandes) dans le dossier de travail :

```powershell
python analyse_conversations.py robert_YYYYMMDD.db
```

Le script produit automatiquement :
- Un affichage console avec les statistiques globales et le détail par session
- Un fichier CSV `conversations_YYYYMMDD_HHMM.csv` dans le même dossier

---

## Étape 3 — Lire le CSV

Le fichier CSV est encodé en UTF-8 avec BOM (compatible Excel sans manipulation).

**Colonnes :**

| Colonne | Description |
|---------|-------------|
| `id` | Identifiant unique du message |
| `session_id` | UUID de la session (anonyme) |
| `pseudo` | Pseudo saisi par l'utilisateur |
| `role` | `user` ou `assistant` |
| `content` | Texte du message |
| `created_at` | Horodatage UTC |

**Ouvrir dans Excel :**
Ouvrir Excel → Données → À partir d'un fichier texte/CSV → sélectionner le fichier.
Délimiteur : point-virgule (`;`).

---

## Étape 4 — Lecture rapide console

Le script affiche un tableau récapitulatif par session :

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
  SESSION                              PSEUDO       MSGS  DÉBUT
  ...
============================================================
```

---

## Étape 5 — Détection automatique du fichier .db

Si un seul fichier `.db` est présent dans le dossier courant, le script le détecte automatiquement :

```powershell
python analyse_conversations.py
# → Fichier détecté automatiquement : robert_20260621.db
```

---

## Checklist analyse

- [ ] Fichier `.db` copié depuis le disque USB sur le PC Windows
- [ ] Script `analyse_conversations.py` présent dans le même dossier ou accessible
- [ ] `python analyse_conversations.py <fichier.db>` exécuté sans erreur
- [ ] Statistiques relues (nombre de sessions, messages, dates)
- [ ] CSV ouvert dans Excel pour lecture détaillée si besoin
- [ ] Résultats consignés dans le rapport de visite J+15

---

## Troubleshooting

### "python n'est pas reconnu"
Python n'est pas installé ou pas dans le PATH. Installer depuis [python.org](https://python.org), cocher "Add Python to PATH" lors de l'installation.

### "Erreur : fichier introuvable"
Vérifier le chemin exact du fichier `.db`. Exemple :
```powershell
python analyse_conversations.py "C:\Users\MonNom\Desktop\robert_20260621.db"
```

### Colonnes illisibles dans Excel (caractères spéciaux)
Le fichier est encodé UTF-8-BOM, compatible Excel. Si les accents s'affichent mal, utiliser l'import via "Données → À partir d'un fichier texte/CSV" plutôt qu'un double-clic.
