---
name: suivi-github
description: Traiter les issues ouvertes du dépôt, déposées par l'agent correspondant. Trie chaque ticket entre question fonctionnelle, question technique et implémentation, puis enchaîne sur le plan d'implémentation.
---

# Suivi GitHub

Traite les issues ouvertes du dépôt courant, en général déposées par l'agent
« correspondant » au nom du responsable produit.

## Le tri

Chaque issue tombe dans une seule des trois catégories.

| Catégorie | Signe | Ce qu'on fait |
|---|---|---|
| Question fonctionnelle | Le comportement attendu est ambigu, ou plusieurs lectures mènent à des produits différents | Commentaire sur le ticket + label `question`. Jamais de question au responsable produit. |
| Question technique | Le comportement est clair, mais la façon de le modéliser ou de le brancher ne l'est pas | Question au responsable produit avec l'outil de question, avant de planifier |
| Acceptée | Le besoin est clair et le code à écrire l'est aussi | Label `accepted`, plan d'implémentation, puis exécution |
| Acceptée et petite | Le besoin est clair et la modification tient en quelques fichiers évidents | Label `accepted`, pas de spec ni de plan : traitement direct avec `/launching-agent-below` |

Une issue peut d'abord poser une question technique, puis devenir acceptée une
fois la réponse obtenue. C'est le cas normal.

## Le déroulé

1. **Lister** les issues ouvertes avec leur auteur, leurs labels et leur date.

   ```bash
   gh issue list --state open --limit 50 --json number,title,labels,author,createdAt
   ```

2. **Lire** chaque issue avec ses commentaires — un ticket déjà commenté a
   peut-être déjà reçu sa réponse.

   ```bash
   gh issue view <n> --json title,body,comments -q '.title, .body, (.comments[] | "--- \(.author.login):\n\(.body)")'
   ```

3. **Vérifier dans la base de connaissance** (`docs/knowledge/`) et dans le code
   ce que l'issue affirme de l'existant. Le correspondant a déjà fait ce travail,
   mais il décrit le produit, pas le modèle de données : c'est là que se cachent
   les questions techniques.

4. **Repérer les dépendances entre issues.** Une issue qui dit dépendre d'une
   autre non tranchée n'est pas acceptable, même si son besoin est limpide.
   Elle part en commentaire.

5. **Traiter** chaque issue selon sa catégorie, en commençant par les questions
   techniques : leur réponse change ce qui devient acceptable.

6. **Planifier** les issues acceptées avec `/spec-to-implementation`.

## Les labels

Une issue traitée porte toujours exactement un des deux labels.

- `question` : un commentaire a été déposé, la balle est dans le camp du
  correspondant.
- `accepted` : l'issue part en implémentation.

Poser le label au moment où la décision est prise, pas en fin de session.

```bash
gh issue edit <n> --add-label question
gh issue edit <n> --add-label accepted
```

Si une issue devient acceptée après avoir reçu une réponse à une question,
retirer l'ancien label :

```bash
gh issue edit <n> --remove-label question --add-label accepted
```

Les deux labels doivent exister dans le dépôt. `question` est fourni par
défaut par GitHub, `accepted` non : le créer la première fois.

```bash
gh label create accepted --description "Issue validee, partie en implementation" --color 0e8a16
```

## Écrire un commentaire de question

Le commentaire s'adresse au correspondant, pas à un développeur.

- Quatre à cinq questions au maximum, numérotées, chacune en deux ou trois
  phrases.
- Une question par point de décision, jamais deux questions dans la même.
- Formuler en termes de produit : ce que voit un utilisateur, ce qui se passe
  dans tel cas. Aucun nom de table, de colonne, de composant ou d'endpoint.
- Poser l'alternative concrètement (« tout comme aujourd'hui, ou plus rien ? »)
  plutôt qu'en ouvert (« comment gérer ce cas ? »).
- Si l'issue dépend d'une autre non tranchée, le dire en une phrase d'ouverture.
- Rien d'autre : pas de résumé du ticket, pas de proposition de conception,
  pas de signature.

```bash
gh issue comment <n> --body "$(cat <<'EOF'
...
EOF
)"
gh issue edit <n> --add-label question
```

Le label `question` est posé **à chaque fois** qu'un commentaire est déposé.

## Poser une question technique

Elle va au responsable produit, avec l'outil de question, une seule fois et
avant d'écrire le plan. Elle porte sur la modélisation ou le branchement :
sur quelle entité existante brancher un nouveau concept, quelle table porte
quoi, quel mécanisme réutiliser.

Donner deux ou trois options concrètes, la recommandation en premier, et dire
pour chacune ce qu'elle implique pour la suite.

## Avant de planifier

Présenter le design en quelques paragraphes dans le fil — base, backend, front,
plus ce qui est décidé par défaut — et attendre le feu vert. Poser le label
`accepted` sur l'issue, puis enchaîner sur `/spec-to-implementation`.

## Où vivent les specs et les plans

Une spec ou un plan ne se commite jamais sur `develop`, ni sur `main`. Il part
sur la branche de l'issue, créée avant d'écrire quoi que ce soit. Si la branche
n'existe pas encore, la créer depuis `develop` et s'y placer avant de lancer
`/spec-to-implementation`.

## La pull request

La description de la PR contient toujours `Closes #<numéro de l'issue>`, sur sa
propre ligne. C'est ce qui referme le ticket au moment de la fusion. Le dire
dans le prompt donné à l'agent qui implémente, pour qu'il ne l'oublie pas.

## Les tickets qui ne méritent ni spec ni plan

Certaines issues acceptées sont trop petites pour tout l'appareil : une
correction de libellé, un champ à afficher, une règle déjà écrite ailleurs à
recopier. Signes : la modification tient en quelques fichiers qu'on sait déjà
nommer, aucune décision de modélisation, rien à trancher avec le responsable
produit.

Dans ce cas, pas de `/spec-to-implementation`. Poser le label `accepted`, puis
lancer directement le travail avec `/launching-agent-below`, en décrivant dans
le prompt le numéro de l'issue, ce qu'il faut changer et où.

Au moindre doute, repasser par la spec : une petite issue mal jugée coûte plus
cher qu'un plan inutile.

## Enchaîner plusieurs tickets

Quand plusieurs issues sont acceptées, elles partent une par une, jamais en
parallèle : deux implémentations simultanées sur le même dépôt se marchent
dessus.

1. Trier les issues acceptées dans l'ordre où elles doivent être faites : celles
   dont d'autres dépendent d'abord.
2. Lancer la première — `/spec-to-implementation`, ou `/launching-agent-below`
   si le ticket ne mérite ni spec ni plan.
3. Une fois le lancement effectif, proposer le suivant en une ligne : son numéro,
   son titre, et la façon dont il sera traité. Attendre la réponse.
4. Sur un feu vert, lancer le suivant et recommencer. Sur un refus ou un report,
   passer au ticket d'après, ou s'arrêter s'il n'en reste plus.
5. Quand la liste est vide, écrire le rapport final.

Ne jamais lancer le ticket suivant sans avoir demandé. Ne jamais enchaîner en
silence.

## Pièges

| Piège | Réalité |
|---|---|
| Poser une question fonctionnelle au responsable produit | Elle va dans le ticket, c'est le correspondant qui y répond. |
| Commenter sans poser le label `question` | Le ticket se perd dans la liste. |
| Lancer l'implémentation sans poser le label `accepted` | Plus rien ne distingue une issue en cours d'une issue jamais lue. |
| Laisser `question` et `accepted` ensemble sur un ticket | Un seul des deux à la fois : le second remplace le premier. |
| Traiter une issue qui dépend d'une autre encore ouverte | Le plan sera à réécrire. Commentaire et on attend. |
| Écrire le commentaire en langage technique | Le correspondant ne lit pas le code, il ne saura pas répondre. |
| Trancher seul une ambiguïté structurante pour avancer | Un mauvais choix ici se paie sur toutes les issues qui suivent. |
| PR ouverte sans `Closes #<n>` | L'issue reste ouverte après la fusion et repasse dans la liste à la session suivante. |
| Commiter une spec ou un plan sur `develop` | Ces fichiers vivent sur la branche de l'issue, jamais sur la branche d'intégration. |
| Lancer plusieurs tickets acceptés en même temps | Les implémentations se marchent dessus. Un ticket à la fois, et on demande avant de passer au suivant. |
| Enchaîner sur le ticket suivant sans demander | Le choix de continuer appartient au responsable produit, pas à l'agent. |
| Écrire une spec pour un changement de libellé | Traitement direct avec `/launching-agent-below`. |

## Le rapport final

Tout à la fin, une fois le dernier ticket lancé ou la liste épuisée, terminer
par ce rapport et rien d'autre. Pas de résumé des tickets, pas de rappel de ce qui a
été fait.

```
---
⚒️ Rapport d'analyse des tickets <DD/MM/YYYY> :
- <nb> ticket(s) acceptés et en cours d'implémentation.
- <nb> ticket(s) mis en attente de réponse.
- <nb> ticket(s) toujours en attente de réponse.
---
```

Les deux premiers nombres sont ceux de la session en cours : les tickets passés en
`accepted` d'un côté, ceux passés en `question` de l'autre. Le troisième est le nombre de tickets qui étaient en attente de question avant la session et qui le sont encore.
