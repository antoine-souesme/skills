---
name: handoff
description: Permet de s'assurer que le plan écrit peut être repris par un autre agent, dans une nouvelle session.
---

# Handoff

Analyse le plan que tu as écris lors de cette session et vérifie qu'il peut être exécuté par un agent dans une autre session.

## Avant l'exécution

- Si le plan comporte 10 étapes ou moins, l'agent peut passer directement à l'exécution inline, sinon il doit le faire en subagent-driven development. 
- Assure toi que l'agent sache dans quelle branche git travailler.
- Assure toi que l'agent reparte d'un ledger sdd propre.
- L'agent ne doit avoir aucune questions à poser et doit pouvoir passer directement à l'exécution du plan.
- L'agent doit être autonomme pour l'étape de vérification visuelle. Il doit savoir ou trouver les identifiants de connexion et NE DOIT PAS me demander de les fournir ou de me connecter.

## Pendant l'exécution

- Si l'agent met de coté une décision à voir plus tard, il doit la consigner dans le fichier docs/suivi/DETTE.md. Il doit consigner uniquement les décisions qu'il met de coté, pas les décisions qu'il prend.
- PAS d'OVER-ENGINEERING dans DETTE.md. On reste fonctionnel et on respect la specification. On ne met AUCUN points qui ne sont pas critiques.
- S'il y a des remontés critique (serveur de dev à lancer, docker qui ne tourne pas, problème qui bloque la suite de l'exécution), l'agent à le droit de poser une question.

## Après l'exécution

- L'agent NE DOIT PAS me dire ce qu'il a fait.
- L'agent DOIT me lister de façon claire et concise les choses que je dois faire manuellement. Par exemple, des variables d'environnement à ajouter. NE PAS MENTIONNER : vérifications manuelles ; manipulations git ; migrations à appliquer ; relectures de pull requests ; réglages à faire dans l'application.
- L'agent NE DOIT PAS me lister ce qu'il à consigné dans DETTE.md
- L'agent DOIT créer une pull request vers develop.

## Finalisation

- Quand tu as fini, tu me donneras le prompt que je pourrai copier/coller dans la nouvelle session. Entoure ton prompt de `---` que je puis le voir facilement.

Modèle :
```
---
<prompt>
---
```
