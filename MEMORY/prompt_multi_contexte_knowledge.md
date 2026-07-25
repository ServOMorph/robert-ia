# Prompt à donner à l'agent en charge de robert-ia

Contexte : robert-ia charge au démarrage un unique fichier `backend/knowledge.txt`
(chemin en dur dans `backend/main.py`, variable `KNOWLEDGE_PATH`) injecté dans le
system prompt. Ce fichier contient aujourd'hui la connaissance du Bistrot de
Nérigean (L'Invariable). Une démonstration a lieu le 25/07/2026 au Moulin du Sud
(Génissac) et nécessite un contexte différent, sans perdre celui de Nérigean.
Objectif : pouvoir choisir rapidement, par machine, quel contexte (quel lieu)
définit le comportement de robert-ia, sans réécrire de code à chaque changement
de lieu.

---

## Tâche

1. Créer un dossier `backend/knowledge/`.
2. Déplacer le contenu actuel de `backend/knowledge.txt` vers
   `backend/knowledge/nerigean.txt`, sans le modifier (préserver tel quel le
   travail déjà fait pour le Bistrot de Nérigean).
3. Créer `backend/knowledge/moulin_du_sud.txt` sur le même format que
   `nerigean.txt` (identité du lieu, ce qui y est proposé, horaires si
   pertinent, contact). Contenu à demander explicitement à l'utilisateur si les
   informations manquent — ne rien inventer. Éléments déjà connus : Moulin du
   Sud, 1141 route du Moulin du Sud, 33420 Génissac ; événement organisé à
   titre personnel ; possibilité de don pour « Le Moulin du Sud ».
4. Modifier `backend/main.py` : remplacer le chemin en dur de `KNOWLEDGE_PATH`
   par une résolution via une variable d'environnement `ROBERT_LIEU` (défaut :
   `nerigean`), pointant vers `backend/knowledge/{ROBERT_LIEU}.txt`. Garder le
   comportement de repli actuel (`"(aucune connaissance spécifique chargée)"`)
   si le fichier résolu n'existe pas.
5. Documenter dans le README (ou `docs/`) comment changer de contexte sur une
   machine donnée : définir `ROBERT_LIEU=moulin_du_sud` avant de lancer le
   service (variable d'environnement du service systemd sur le PC Linux, ou
   export local en dev).
6. Respecter la règle de synchronisation Windows → Linux du projet (`AGENTS.md`,
   section "Synchronisation Windows → Linux") : modifier d'abord sur Windows,
   puis déployer via `scp`, puis redémarrer le service si nécessaire.
7. Vérifier que le service démarre correctement avec `ROBERT_LIEU=nerigean`
   (comportement inchangé) et avec `ROBERT_LIEU=moulin_du_sud` (nouveau
   contexte) avant le 25/07/2026.

## Méta
- Produit par l'agent MEMORY de robert-ia, zone à rôle créée le 2026-07-20
  (Phase 2 de `roadmap_agents.md`, kit claude-vibecoding-kit).
- Ne pas exécuter directement dans MEMORY/ : ce prompt est destiné à l'agent
  qui a autorité sur `backend/` et `main.py` (hors périmètre de MEMORY).
