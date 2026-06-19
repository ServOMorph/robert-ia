# Test manuel — Mémoire conversationnelle

Envoyer les prompts dans l'ordre, dans la même session.
Vérifier la colonne "Attendu" après chaque réponse.

---

## Séquence

| # | Prompt à envoyer | Attendu |
|---|---|---|
| 1 | Bonjour ! Je m'appelle Marie. Je suis bénévole ici depuis 3 ans. | Robert accuse réception du prénom et du contexte. |
| 2 | Qu'est-ce que tu peux faire pour m'aider dans mon rôle ? | Réponse cohérente avec le contexte "bénévole en association". |
| 3 | J'ai un problème avec notre planning de permanences de novembre. On a 5 créneaux non couverts les mercredis après-midi. | Robert note le problème et le chiffre (5 créneaux, mercredis). |
| 4 | On a aussi un budget serré : 200 € max pour recruter de nouveaux bénévoles. | Robert intègre la contrainte budgétaire. |
| 5 | Parlons d'autre chose. Je cherche des idées d'activités pour nos adhérents seniors. | Robert change de sujet sans perdre le fil du planning. |
| 6 | Revenons au planning. Tu te souviens du nombre de créneaux manquants ? | **[Clé mémoire]** Robert doit citer "5 créneaux" sans que l'utilisateur le répète. |
| 7 | Et pour les seniors, tu avais des suggestions ? | Robert reprend le second sujet sans confondre avec le planning. |
| 8 | Notre président s'appelle Paul. Il ne peut pas venir le vendredi. | Robert enregistre Paul et sa contrainte. |
| 9 | Ça complique encore plus le planning du coup, non ? | **[Référence implicite "ça"]** Robert comprend que "ça" = la contrainte de Paul sur le planning, pas les seniors. |
| 10 | Lui par contre, il serait partant pour animer un atelier seniors. | **[Référence implicite "lui"]** Robert comprend que "lui" = Paul. |
| 11 | Tu peux me rappeler mon prénom ? | **[Clé mémoire]** Robert doit dire "Marie" sans hésitation. |
| 12 | Et mon rôle dans l'association, tu t'en souviens ? | **[Clé mémoire]** Robert doit dire "bénévole". |
| 13 | Comme je te l'avais dit, le budget est vraiment limité. C'est quoi la contrainte exacte ? | **[Référence implicite + mémoire]** Robert doit citer "200 €" sans que l'utilisateur le répète. |
| 14 | Récapitule tout ce qu'on a abordé depuis le début de notre échange. | **[Cohérence globale]** Le résumé doit couvrir : planning, créneaux, budget, seniors, Paul — sans inventer. |
| 15 | Quel était le premier problème dont je t'avais parlé ? | **[Ordre chronologique]** Robert doit citer le planning / les créneaux, pas les seniors. |
| 16 | Et la personne dont j'avais mentionné les contraintes d'agenda, c'était qui ? | **[Mémoire nominative]** Robert doit citer Paul. |
| 17 | Les deux sujets dont on a parlé, c'est bien deux choses distinctes ? Tu ne les mélangeras pas ? | **[Dissociation]** Robert doit confirmer clairement : planning bénévoles ≠ activités seniors. |
| 18 | Donne-moi une solution concrète pour les 5 créneaux de novembre. | Robert propose quelque chose d'actionnable, ancré dans les contraintes réelles (budget 200 €, Paul indisponible vendredi). |
| 19 | Et Paul, est-ce qu'il pourrait prendre un des créneaux du mercredi à la place du vendredi ? | Robert s'appuie sur la contrainte de Paul (vendredi) pour répondre de façon cohérente. |
| 20 | Si on arrête la conversation maintenant et que je reviens demain, tu te souviendras de tout ça ? | **[Honnêteté]** Robert doit expliquer honnêtement que la mémoire est limitée à la session courante (pas de persistance inter-sessions en v1). |

---

## Grille d'évaluation

| Catégorie | Prompts concernés |
|---|---|
| Mémoire prénom/rôle | 1, 11, 12 |
| Mémoire chiffre/fait précis | 3, 6, 13 |
| Référence implicite (ça, lui, comme je t'ai dit) | 9, 10, 13 |
| Non-confusion entre deux sujets | 6, 7, 17 |
| Cohérence sur longue session | 14, 15, 16 |
| Honnêteté sur les limites | 20 |

## Résultat attendu global

- Tours 1–7 : aucune régression, Robert suit deux sujets en parallèle.
- Tours 8–13 : références implicites résolues sans ambiguïté.
- Tours 14–17 : résumé exact, pas d'hallucination sur des détails non mentionnés.
- Tours 18–19 : réponses ancrées dans les contraintes réelles données.
- Tour 20 : Robert répond honnêtement (pas de fausse promesse de mémoire persistante).
