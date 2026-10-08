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
| Acceptée et petite | Le besoin est clair et la modification tient en quelques fichiers évidents | Label `accepted`, pas de spec ni de plan : traitement direct avec `/antoine:launching-agent-below` |

Une issue peut d'abord poser une question technique, puis devenir acceptée une
fois la réponse obtenue. C'est le cas normal.

## Grouper des tickets

Deux tickets acceptés partent parfois ensemble, en une seule spec, un seul plan
et une seule implémentation. C'est l'exception, pas la règle — mais quand elle
s'applique, la refuser fait payer deux fois le même travail, et la deuxième
implémentation défait souvent des choix de la première.

### Quand grouper

Il faut **les deux** conditions :

- **Ils touchent le même endroit du code.** Pas le même domaine — le même
  fichier, la même règle, la même table. Deux tickets de facturation qui ne se
  croisent nulle part ne se groupent pas.
- **Faire le second après le premier obligerait à revenir sur le premier.** Si
  l'ordre est indifférent, ce sont deux tickets, et ils partent l'un après
  l'autre.

Signes concrets : les deux ont besoin de la même colonne, du même point de
passage, du même écran ; ou l'un des deux tickets dit lui-même qu'il « touche la
même règle » que l'autre.

### Quand ne pas grouper

- **Deux tickets simplement voisins.** Un même écran touché à deux endroits
  différents, deux sujets du même domaine : ça ne suffit pas.
- **Dès que le total devient lourd.** Un groupe reste raisonnable. Au-delà de
  deux tickets, ou si le plan combiné dépasse une douzaine de tâches, on
  sépare : une grosse implémentation qui casse coûte plus cher que deux petites.
  Mieux vaut un socle commun livré d'abord, puis le second ticket par-dessus.
- **Si l'un des deux a encore une question ouverte.** On ne groupe jamais un
  ticket accepté avec un ticket en attente de réponse.

### Ce qu'il faut faire ensuite

Le groupement se dit au responsable produit au moment de présenter le design,
avec ce que les tickets partagent — c'est ça qui justifie le regroupement, pas
leur proximité de sujet. Une fois retenu, il s'écrit dans `docs/suivi/GITHUB.md`,
parce qu'une session suivante n'a aucun moyen de le redeviner.

La branche et la PR portent alors les deux numéros, et la description referme les
deux : une ligne `Closes #<n>` par ticket.

## Le déroulé

0. **Lire `docs/suivi/GITHUB.md`** avant toute autre chose. Il porte l'état
   courant du traitement : l'ordre retenu, les groupements décidés, les
   périmètres réduits, les dépendances à surveiller. C'est ce qui permet de
   reprendre une session interrompue sans redécider ce qui l'a déjà été.

   S'il n'existe pas, c'est une première session : il se crée à l'étape 7.

1. **Lister** les issues ouvertes avec leur auteur, leurs labels et leur date.

   ```bash
   gh issue list --state open --limit 50 --json number,title,labels,author,createdAt
   ```

   Croiser avec le fichier de suivi : un ticket qui y figure mais n'est plus
   ouvert est livré, il sort du fichier. Un ticket ouvert qui n'y figure pas est
   nouveau, il passe au tri.

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

   Au passage, repérer aussi les issues qui **partagent un socle** et gagneraient
   à partir ensemble. Voir « Grouper des tickets ».

5. **Traiter** chaque issue selon sa catégorie, en commençant par les questions
   techniques : leur réponse change ce qui devient acceptable.

6. **Planifier** les issues acceptées avec `/antoine:spec-to-implementation`.

7. **Mettre à jour `docs/suivi/GITHUB.md`** dès qu'une décision est prise, pas en
   fin de session : un groupement retenu, un ordre arrêté, un périmètre réduit,
   une dépendance repérée, un ticket passé en attente. Voir « Le fichier de
   suivi » plus bas.

## Le fichier de suivi

`docs/suivi/GITHUB.md` est le point de reprise entre deux sessions. Il répond à
une seule question : **par quoi on continue, et qu'est-ce qui a déjà été décidé ?**

### Ce qu'il contient

- L'ordre de traitement retenu, et pourquoi.
- Les groupements décidés : quels tickets partent ensemble, et ce qu'ils
  partagent.
- La liste des tickets à implémenter, rangés par domaine.
- Les tickets en attente de réponse, avec **en une ligne ce qui bloque** — pour
  ne pas avoir à relire le commentaire déposé sur GitHub.
- Les dépendances à surveiller, et le ticket le plus bloquant s'il y en a un.
- Les décisions de périmètre : un ticket livré en version réduite, la partie
  laissée de côté et ce qu'elle attend.

### Ce qu'il ne contient jamais

- **Aucun historique.** Pas de « livré », pas de numéros de PR, pas de dates de
  fusion, pas de récapitulatif de ce qui a été fait. Tout cela se retrouve en une
  commande avec `git log` et `gh issue list --state closed`. Un ticket livré
  disparaît du fichier.
- Pas de recopie du contenu des tickets : le ticket est sur GitHub, on n'en
  garde ici que le numéro, le titre et la décision.
- Pas de détail d'implémentation : ça vit dans le plan, sur la branche du ticket.

Règle de tri : si l'information se retrouve avec `gh` ou `git`, elle n'a pas sa
place ici. Ce qui reste, c'est ce qui n'existe nulle part ailleurs — les
décisions.

### Quand l'écrire

À chaque décision, au fil de la session. Un fichier mis à jour seulement à la fin
est un fichier perdu si la session s'interrompt.

### Versionning du fichier

Si tu commit le fichier sur develop, n'oublie pas de push develop.

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
`accepted` sur l'issue, puis enchaîner sur `/antoine:spec-to-implementation`.

## Où vivent les specs et les plans

Une spec ou un plan ne se commite jamais sur `develop`, ni sur `main`. Il part
sur la branche de l'issue, créée avant d'écrire quoi que ce soit. Si la branche
n'existe pas encore, la créer depuis `develop` et s'y placer avant de lancer
`/antoine:spec-to-implementation`.

## La pull request

La description de la PR contient toujours `Closes #<numéro de l'issue>`, sur sa
propre ligne. C'est ce qui referme le ticket au moment de la fusion. Le dire
dans le prompt donné à l'agent qui implémente, pour qu'il ne l'oublie pas.

Exception : un ticket livré en plusieurs lots. Chaque lot a sa PR, qui porte
`Refs #<n>` et pas `Closes`, sauf la PR du dernier lot, qui porte
`Closes #<n>`. Sinon le ticket se referme dès le premier lot fusionné.

## Les tickets livrés en plusieurs lots

Un ticket trop lourd pour une seule implémentation se découpe en lots, chacun
avec son plan et sa PR. Le découpage se décide avec le responsable produit au
moment de présenter le design, et s'écrit dans `docs/suivi/GITHUB.md`.

Une fois le lancement d'un lot effectif, **proposer le lot suivant** en une
ligne, avant tout autre ticket : le numéro du ticket, le lot, ce qu'il contient
et la façon dont il sera traité. Attendre la réponse.

Sur un feu vert, le lot suivant se prépare tout de suite (spec, plan, handoff),
sur une branche créée depuis celle du lot précédent, puisqu'il s'appuie dessus.
Si l'agent du lot précédent tourne encore, cette préparation se fait dans un
worktree séparé, jamais dans le dossier de travail (voir « Pendant qu'un agent
travaille »).
Il ne se lance en revanche qu'une fois l'agent du lot précédent terminé : deux
implémentations simultanées sur le même dépôt se marchent dessus. Le dire au
responsable produit, et donner le prompt de reprise prêt à lancer.

## Les tickets qui ne méritent ni spec ni plan

Certaines issues acceptées sont trop petites pour tout l'appareil : une
correction de libellé, un champ à afficher, une règle déjà écrite ailleurs à
recopier. Signes : la modification tient en quelques fichiers qu'on sait déjà
nommer, aucune décision de modélisation, rien à trancher avec le responsable
produit.

Dans ce cas, pas de `/antoine:spec-to-implementation`. Poser le label `accepted`, puis
lancer directement le travail avec `/antoine:launching-agent-below`, en décrivant dans
le prompt le numéro de l'issue, ce qu'il faut changer et où.

Sauter la spec ne fait pas sauter les garanties de `/antoine:spec-to-plan` et de
`/antoine:handoff` : c'est le prompt qui doit les porter, puisqu'aucun plan ne le fera.
Le prompt contient donc toujours :

- **la branche** à créer depuis `develop` à jour, et dans laquelle travailler.
  C'est l'agent qui la crée, pas la session qui le lance (voir « Pendant qu'un
  agent travaille ») ;
- **une vérification visuelle** avec claude-in-chrome de chaque élément d'interface
  ajouté ou modifié, en décrivant ce qu'il faut voir à l'écran. L'agent est
  autonome : il trouve les identifiants du compte de test dans `.env.local` (et
  les y ajoute s'ils manquent), il ne demande jamais de se connecter à sa place ;
- les vérifications du projet (lint, build) prévues par son `CLAUDE.md` ;
- la consigne de noter dans `docs/suivi/DETTE.md` une décision mise de côté, et
  seulement celle-là ;
- la PR vers `develop` avec `Closes #<n>` sur sa propre ligne ;
- le compte rendu final : ne pas raconter ce qui a été fait, lister seulement ce
  que le responsable produit doit faire à la main (hors vérifications, git,
  migrations, relecture de PR et réglages dans l'application).

Au moindre doute, repasser par la spec : une petite issue mal jugée coûte plus
cher qu'un plan inutile.

## Enchaîner plusieurs tickets

Quand plusieurs issues sont acceptées, elles partent une par une, jamais en
parallèle : deux implémentations simultanées sur le même dépôt se marchent
dessus.

1. Trier les issues acceptées dans l'ordre où elles doivent être faites : celles
   dont d'autres dépendent d'abord.
2. Lancer la première — `/antoine:spec-to-implementation`, ou `/antoine:launching-agent-below`
   si le ticket ne mérite ni spec ni plan.
3. Une fois le lancement effectif, proposer le suivant en une ligne : son numéro,
   son titre, et la façon dont il sera traité. Attendre la réponse. Si ce qui
   vient d'être lancé est un lot et qu'il en reste d'autres, le suivant proposé
   est le lot d'après (voir « Les tickets livrés en plusieurs lots »).
4. Sur un feu vert, lancer le suivant et recommencer. Sur un refus ou un report,
   passer au ticket d'après, ou s'arrêter s'il n'en reste plus.
5. Quand la liste est vide, écrire le rapport final.

Ne jamais lancer le ticket suivant sans avoir demandé. Ne jamais enchaîner en
silence.

## Pendant qu'un agent travaille

L'agent lancé avec `/antoine:launching-agent-below` ou `/antoine:spec-to-implementation`
travaille **dans le même dossier de travail** que la session qui l'a lancé.
Tant qu'il tourne, ce dossier lui appartient.

- **Ne jamais changer de branche** dans le dossier de travail : pas de
  `git checkout`, `git switch`, `git pull`, `git stash`, ni de commit. L'agent
  verrait ses fichiers changer sous ses pieds.
- Pour un petit ticket, **la branche est créée par l'agent lui-même**, au début
  de son travail : la session qui lance ne la crée pas.
- Mettre à jour `docs/suivi/GITHUB.md` sur `develop` pendant ce temps se fait
  dans un worktree séparé, supprimé juste après :

  ```bash
  git worktree add --detach <scratchpad>/wt-develop origin/develop
  # modifier, commiter, puis :
  git -C <scratchpad>/wt-develop push origin HEAD:develop
  git worktree remove <scratchpad>/wt-develop
  ```

  Si la mise à jour peut attendre, la faire une fois l'agent terminé.

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
| Lancer un lot sans proposer le lot suivant | Le ticket reste à moitié livré et personne ne pense à la suite. On propose le lot d'après tout de suite. |
| Mettre `Closes #<n>` sur la PR d'un lot qui n'est pas le dernier | Le ticket se referme alors qu'il reste des lots. `Refs #<n>` jusqu'au dernier. |
| Enchaîner sur le ticket suivant sans demander | Le choix de continuer appartient au responsable produit, pas à l'agent. |
| Écrire une spec pour un changement de libellé | Traitement direct avec `/antoine:launching-agent-below`. |
| Changer de branche ou commiter dans le dossier de travail pendant qu'un agent tourne | L'agent travaille dans ce même dossier : ses fichiers changent sous ses pieds. Worktree séparé, ou on attend qu'il ait fini. |
| Créer la branche d'un petit ticket avant de lancer l'agent | C'est l'agent qui la crée, dans son prompt. La session qui lance ne touche pas à git. |
| Lancer un petit ticket avec un prompt sans vérification visuelle | Sans plan, rien d'autre ne la demande : l'agent s'arrête au lint et au build. Le prompt reprend toutes les garanties du handoff. |
| Commencer une session sans lire `docs/suivi/GITHUB.md` | On redécide ce qui l'a déjà été, et on casse des groupements retenus. |
| Écrire dans le fichier de suivi ce qui a été livré | Ce n'est pas un historique. `git log` et `gh` le disent mieux. Un ticket livré en disparaît. |
| Ne mettre le fichier de suivi à jour qu'en fin de session | Une session interrompue perd alors toutes ses décisions. |
| Grouper deux tickets parce qu'ils parlent du même domaine | Il faut le même endroit du code, et un ordre qui obligerait sinon à revenir sur le premier. |
| Grouper trois tickets ou plus pour aller plus vite | Une grosse implémentation qui casse coûte plus cher que deux petites. On sépare. |
| Traiter deux tickets d'un même socle l'un après l'autre sans regarder | Le second défait des choix du premier, et on paie deux fois le même travail. |
| Grouper sans l'écrire dans le fichier de suivi | La session suivante n'a aucun moyen de le redeviner. |

## Le rapport final

Tout à la fin, une fois le dernier ticket lancé ou la liste épuisée, vérifier que
`docs/suivi/GITHUB.md` reflète bien l'état courant, puis terminer par ce rapport
et rien d'autre. Pas de résumé des tickets, pas de rappel de ce qui a été fait.

```
---
⚒️ Rapport d'analyse des tickets <DD/MM/YYYY> :
- <nb> ticket(s) acceptés et vont être implémentés.
- <nb> ticket(s) en attente de réponse.
---
```

Les nombres portent sur l'état du dépôt, pas sur la session : le premier compte
les tickets ouverts qui portent le label `accepted`, le second ceux qui portent
le label `question`.

```bash
gh issue list --state open --label accepted --limit 200 --json number -q 'length'
gh issue list --state open --label question --limit 200 --json number -q 'length'
```
