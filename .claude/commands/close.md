---
description: Clôture la session — synthèse, mise à jour du contexte, commit
model: sonnet
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
---

# /close

## Procédure

1. Produire une synthèse de session (< 25 lignes) :

```
# Session du AAAA-MM-JJ

## Décisions prises
- [décision actée, 1 ligne]

## Livrables produits ou modifiés
- [fichier] : [statut]

## Hypothèses validées / invalidées
- VALIDE : ...
- INVALIDE : ... -> pivot vers ...
- EN ATTENTE : ...

## Prochaine étape exacte
[1-3 lignes]

## Question bloquante pour la session suivante
[1 question, ou "Aucune"]
```

2. Mettre à jour `_contexte/signals.md` :
   - Reporter tout élément non résolu.
   - Écraser la section "Dernière session" avec la synthèse ci-dessus.
   - Mettre à jour les priorités [P1/P2] sur les actions ouvertes.
   - Sections sans contenu : laisser le titre sans puce.

3. Mettre à jour `_contexte/contexte.md` :
   - Réécrire intégralement la section "État actuel" (5 lignes max).
   - Ajouter les décisions actées à "Décisions structurantes" (append only).
   - Si rien n'a changé : ne pas toucher au fichier.

4. Mettre à jour `_contexte/_manifest.md` si nécessaire (ajout/retrait de la roadmap).

5. Vérifier que `roadmap_robert-ia.md` reflète l'état après session.

6. Mettre à jour `README.md` si nécessaire :
   - Section "État du projet" ou équivalent : refléter la phase en cours.
   - Si rien n'a changé côté README : ne pas toucher.

7. Effectuer un commit git :
   ```bash
   git diff --name-only
   git status
   git add _contexte/ roadmap_robert-ia.md README.md [autres fichiers modifiés]
   git commit -m "close(robert-ia): session AAAA-MM-JJ — <résumé 1 ligne>"
   ```

8. Afficher en fin de réponse en grand format : ✌️😎
