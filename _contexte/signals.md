# Signals — robert-ia   (MAJ 2026-06-18)

## Actions ouvertes
- [P1] Phase 4 — Déploiement pilote (non commencée)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud

## Dernière session (2026-06-18 — session 4)

### Décisions prises
- Script packaging `setup-airgap.sh` : structure disque complète (app + data + config + scripts)
- Lancement automatique via systemd (start-kiosk.sh)
- Protocole export air-gap : USB + SQLite + manifeste JSON (RGPD-compliant)

### Livrables produits ou modifiés
- **Nouveaux fichiers** :
  - `scripts/setup-airgap.sh` : packaging disque dur
  - `scripts/start-kiosk.sh` : démarrage kiosk + backend + Ollama
  - `scripts/install-systemd.sh` : setup service automatique
  - `config/robert-ia.service` : configuration systemd
  - `docs/GUIDE_INSTALLATION_AIRGAP.md` : 7 phases installation
  - `docs/PROTOCOLE_EXPORT_DONNEES.md` : export air-gap + RGPD
  - `docs/PHASE3_SUMMARY.md` : synthèse Phase 3
- **Build frontend** : `frontend/dist/` compilé (149 kB JS, 8.96 kB CSS)

### Hypothèses validées / invalidées
- ✅ Script packaging fonctionne : structure testée sur `/tmp/test-airgap-v2/`
- ✅ Fichiers Python accessibles et copiables
- ⏳ EN ATTENTE : test end-to-end sur Ubuntu réel (Phase 4 — déploiement pilote)

### Prochaine étape exacte
Phase 4 — Déploiement pilote : installer sur PC Bistrot de Nérigean, tester démarrage auto + conversation + export données, analyse retours J+15.

### Question bloquante pour la session suivante
Aucune
