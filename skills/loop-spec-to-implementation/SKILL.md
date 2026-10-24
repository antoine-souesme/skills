---
name: loop-spec-to-implementation
description: Enchaîne plusieurs specs l'une après l'autre avec /antoine:spec-to-implementation. Chaque agent d'exécution fusionne sa PR dans develop puis rend la main par sa réponse finale, et la session lance alors la spec suivante.
---

# Boucle spec to implementation

Lance `/antoine:spec-to-implementation` sur une liste de specs, **une par une**,
sans redemander entre deux : la session attend que l'agent d'exécution ait
fusionné sa PR dans `develop`, puis passe à la spec suivante. C'est le mode
automatique de `/antoine:suivi-github`, appliqué à une liste de specs au lieu
d'une liste de tickets.

## L'entrée

Les specs sont données en argument : des chemins de fichiers, ou un dossier.
L'ordre est celui donné. Pour un dossier, l'ordre alphabétique des fichiers.

Avant de commencer, annoncer la liste numérotée en une ligne par spec (chemin et
branche prévue), puis démarrer sans attendre de réponse.

## Avant de commencer

1. Vérifier que le dossier de travail est propre et à jour sur `develop`
   (`git status`, `git checkout develop && git pull`). S'il ne l'est pas, s'arrêter
   et le dire en une ligne.
2. Écarter les specs déjà livrées : une spec dont la branche a une PR fusionnée
   (`gh pr list --head <branche> --state merged`) sort de la liste. C'est ce qui
   permet de relancer la boucle après une interruption avec la même liste.

## La branche

Chaque spec a sa branche, créée depuis `develop` à jour : `feature/<nom-du-fichier-de-spec>`,
sans extension. La spec et le plan se commitent sur cette branche, jamais sur
`develop` ni sur `main`.

La session crée la branche et s'y place **avant** de lancer
`/antoine:spec-to-implementation`, puisque c'est elle qui écrit le plan.

## Un tour de boucle

1. Créer la branche de la spec depuis `develop` à jour.
2. Lancer `/antoine:spec-to-implementation` sur la spec, en appliquant ses
   instructions intégralement. **Avant le lancement**, ajouter au prompt de
   handoff le bloc « Fusion et message » ci-dessous.
3. Attendre la réponse finale de l'agent (voir « Attendre la fusion »).
4. À la fusion : `git checkout develop && git pull`, annoncer la spec suivante en
   une ligne (chemin, branche), et recommencer.

Quand la liste est vide, terminer par le rapport final.

## Le bloc « Fusion et message »

À ajouter tel quel à la fin du prompt de handoff :

```
## Fusion et message

- La PR vers develop est créée depuis la branche courante.
- Surveille ses contrôles jusqu'au bout : `gh pr checks <n> --watch --interval 30`.
- Tout est vert : fusionne avec `gh pr merge <n> --squash`, sans `--delete-branch`.
  Ne supprime jamais la branche locale, reste dessus après la fusion.
- Un contrôle échoue : lis le journal (`gh run view <id> --log-failed`), corrige sur
  la branche, pousse, et surveille à nouveau.
- Trois échecs de suite, ou un échec qui ne vient pas de ton travail : ne fusionne pas.
- Ne fusionne jamais une PR dont un contrôle est rouge ou en cours, ne contourne
  jamais un contrôle (pas de `--admin`, pas de test désactivé).
- Ta réponse finale commence par « <branche> fusionnée », ou par
  « <branche> non fusionnée : <raison> ». Les actions manuelles viennent après.
```

## Attendre la fusion

Pas de script de surveillance, pas de `sleep`, pas de réveil programmé :
l'agent d'exécution est un sous-agent de la session, **sa réponse finale arrive
toute seule** dans la conversation quand il a fini. La session ne fait rien en
attendant, et ne se ferme pas : l'agent s'arrêterait avec elle.

À la réception, vérifier l'état de la PR avec `gh pr list --head <branche> --state all`
avant d'enchaîner.

## Pendant qu'un agent travaille

L'agent d'exécution travaille **dans le même dossier** que la session. Tant qu'il
tourne, ce dossier lui appartient : pas de `git checkout`, `git switch`,
`git pull`, `git stash`, ni de commit. La spec suivante ne se prépare qu'après la
fusion.

## Ce que la boucle ne fait pas

Elle enchaîne les lancements, **elle ne tranche rien**. Une question prévue par
`/antoine:spec-to-plan` (« AJOUT DESIGN : … », compte de test) reste une
question : la session la pose, attend la réponse, puis reprend la boucle.

## Quand s'arrêter

La session s'arrête et prévient en une ligne, sans lancer la suite, si :

- l'agent s'arrête sans avoir fusionné ;
- la PR est fermée sans être fusionnée ;
- l'agent signale une action à faire à la main avant que la suite puisse marcher
  (une variable d'environnement, un compte à créer) ;
- le dossier de travail n'est pas propre au moment de revenir sur `develop`.

La boucle s'arrête aussi quand le responsable produit le demande.

## Le rapport final

Quand la liste est vide, ou que la boucle s'arrête, terminer par ce rapport et
rien d'autre :

```
---
🔁 Boucle spec to implementation <DD/MM/YYYY> :
- <nb> spec(s) fusionnée(s).
- <nb> spec(s) restante(s) : <chemins>
- Actions à faire à la main : <liste, ou « aucune »>
---
```

## Pièges

| Piège | Réalité |
|---|---|
| Lancer deux specs en même temps | Les implémentations se marchent dessus dans le même dossier. Une à la fois. |
| Oublier le bloc « Fusion et message » dans le prompt | La PR reste ouverte et la boucle s'arrête sur une branche non fusionnée. |
| Attendre la fusion avec un script, `sleep` ou un réveil | La réponse finale du sous-agent arrive toute seule. |
| Fermer la session pendant qu'un agent tourne | L'agent est un sous-agent de la session : il s'arrête avec elle. |
| Lancer la suite alors que l'agent n'a pas fusionné | La spec suivante part d'un `develop` qui n'a pas la précédente. On s'arrête et on prévient. |
| Répondre seul à une question de `spec-to-plan` pour ne pas bloquer | La boucle ne décide rien. On pose la question et on attend. |
| Préparer la spec suivante pendant que l'agent tourne | Changer de branche fait bouger ses fichiers sous ses pieds. On attend la fusion. |
| Fusionner avec `--delete-branch` | La branche locale reste toujours en place. `gh pr merge <n> --squash`, rien de plus. |
| Relancer une spec déjà fusionnée après une interruption | On écarte au départ les specs dont la branche a une PR fusionnée. |
