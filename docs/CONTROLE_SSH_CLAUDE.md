# Contrôle SSH du PC Linux depuis Claude Code (Windows)

Permet à Claude Code (tournant sur le PC Windows) d'exécuter des commandes directement sur le PC Linux sans copier-coller manuel.

---

## Prérequis

| Élément | Valeur |
|---|---|
| Hostname du PC Linux (mDNS) | `robert-ia-H81M-S2PV.local` |
| Utilisateur SSH | `root` |
| Clé privée SSH | `C:\Users\raph6\.ssh\robert-ia_ed25519` |
| Accès root SSH | Actif (`PermitRootLogin yes` dans sshd_config) |

> Le hostname mDNS (`.local`, via Avahi) est utilisé plutôt que l'IP DHCP, qui peut changer selon le réseau (ancien partage ICS `192.168.137.x`, désormais switch/Freebox `192.168.1.x`).

> **Note :** L'accès root SSH est temporaire (phase dev). Le désactiver avant déploiement final (voir signal P3 dans `_contexte/signals.md`).

---

## Condition préalable à chaque session

Les deux PC doivent être sur le même réseau local (actuellement via switch/Freebox).

**Vérifier que le Linux est joignable :**
```
ping robert-ia-H81M-S2PV.local
```
→ Si pas de réponse : vérifier que le PC Linux est allumé et connecté au réseau Windows.

---

## Comment demander à Claude Code de prendre le contrôle

Il suffit de dire explicitement :

> "Prends le contrôle du Linux et fais X"

Claude Code dispose des outils pour exécuter des commandes SSH depuis ce projet Windows. Il n'y a rien à installer ni configurer — la clé et l'IP sont déjà connues.

---

## Ce que Claude Code peut faire via SSH

- Lire des fichiers de config sur le Linux
- Modifier des services systemd (`daemon-reload`, `restart`)
- Vérifier l'état de la RAM, des processus, des logs
- Redémarrer des services (ollama, robert-ia, rustdesk)
- Modifier des fichiers de configuration
- Exécuter des scripts

---

## Commande SSH de référence (pour vérification manuelle)

```powershell
ssh -i "C:\Users\raph6\.ssh\robert-ia_ed25519" -o StrictHostKeyChecking=no root@robert-ia-H81M-S2PV.local "commande"
```

---

## Limites

- **Commandes interactives impossibles** : nano, vim, htop, tout ce qui requiert une TTY interactive. Claude Code passe par des commandes non-interactives uniquement.
- **Réseau requis** : fonctionne uniquement quand les deux PC sont connectés (ex: partage connexion Windows actif).
- **Accès root** : à désactiver avant déploiement en production (P3).

---

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Connection refused` | SSH non démarré sur Linux | `sudo systemctl start ssh` depuis le Linux |
| `Permission denied` | Mauvaise clé ou clé non autorisée | Vérifier `/root/.ssh/authorized_keys` sur Linux |
| `No route to host` | Linux pas sur le réseau | Vérifier le câblage / switch |
| Timeout | mDNS non résolu | Vérifier Avahi sur Linux, ou lire l'IP avec `ip a` |
