# Signals — robert-ia   (MAJ 2026-06-20)

## Actions ouvertes
- [P1] Repackager USB et valider démarrage automatique complet (backend + Firefox kiosk) sur PC Linux
- [P1] Phase 4 — Déploiement pilote Bistrot de Nérigean (en cours)
- [P2] Corriger hallucination des chiffres précis (budget 200€ → modèle invente 500€, 5000€)

## Questions ouvertes
- Firefox kiosk se lance-t-il automatiquement au démarrage avec User=robert-ia + XAUTHORITY ?
- Hallucination chiffres : accepter 18/20 ou corriger avant déploiement pilote ?

## Échéances

## Blocages

## Contexte chaud
- Session 7 (2026-06-20) : déploiement USB testé sur PC Linux (i3-4130, 4 Go RAM) — chat fonctionnel
- gemma3:4b validé sur machine cible : swap léger (~200 Mo), fonctionnel
- Backend sert maintenant le frontend via FastAPI (StaticFiles) — file:// abandonné
- Port 8001 confirmé en production

## Dernière session (2026-06-20 — session 7)

### Décisions prises
- FastAPI sert le frontend statique (StaticFiles + routes) — plus de `file://` nécessaire
- Port 8001 confirmé en production
- Service systemd : `User=robert-ia` (pas root), `MemoryLimit=3G`, `XAUTHORITY` ajouté
- Protocole déploiement USB validé en conditions réelles

### Livrables produits ou modifiés
- `backend/main.py` : service frontend statique via FastAPI (StaticFiles + catch-all)
- `scripts/start-kiosk.sh` : port 8001, gemma3:4b, URL Firefox→`http://localhost:8001`
- `config/robert-ia.service` : User/Group robert-ia, HOME, XAUTHORITY, MemoryLimit 3G
- `scripts/setup-airgap.sh` : `app/backend/data/` + `logs/` créés au packaging
- `scripts/install-systemd.sh` : permissions `logs/` et `app/backend/data/` fixées pour robert-ia
- `docs/GUIDE_INSTALLATION_AIRGAP.md` : gemma3:4b, port 8001

### Hypothèses validées / invalidées
- VALIDE : gemma3:4b tient sur 4 Go RAM (i3-4130) — swap ~200 Mo, fonctionnel
- VALIDE : protocole déploiement USB fonctionne (testé en conditions réelles)
- VALIDE : interface Robert-IA fonctionne sur PC Linux (chat complet opérationnel)
- EN ATTENTE : Firefox kiosk auto via systemd — corrigé dans les fichiers, non retesté

### Prochaine étape exacte
Repackager via `setup-airgap.sh`, redéployer sur le PC Linux via USB, redémarrer la machine et valider le démarrage automatique complet (backend + Firefox kiosk).

### Question bloquante pour la session suivante
Firefox kiosk se lance-t-il automatiquement au démarrage avec les corrections `User=robert-ia` + `XAUTHORITY` ?
