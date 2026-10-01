---
name: deploy-production
description: Mise en production du projet
disable-model-invocation: true
---

# Mise en production

Orchestration d'une release en deux temps : préparation et ouverture d'une pull request `develop` → `main`, puis, sur feu vert de l'utilisateur, déploiement Supabase distant, fusion de la pull request et réintégration dans develop.

## Principe central

**On ne fusionne jamais la pull request dans `main` tant que la mise en prod Supabase n'a pas réussi.** L'ordre des étapes est une garantie : le code public (`main`) ne doit jamais être en avance sur la base de prod.

## Règles absolues

- Ne jamais demander d'autorisation pour les opérations git (conformément aux conventions du projet).
- Suivre l'ordre des étapes **exactement**. Ne pas fusionner la pull request avant l'étape 8.
- **Toujours fusionner avec un commit de fusion (`gh pr merge --merge`). Jamais `--squash` ni `--rebase` : l'historique de `develop` doit être conservé tel quel dans `main`.**
- Ne jamais pousser directement sur `main` : tout passe par la pull request.
- La source de vérité du schéma reste `supabase/migrations/*.sql`. Jamais le dashboard.
- Si une étape échoue, s'arrêter, analyser, et ne pas enchaîner la suivante.

## Détecter la phase

- Si aucune pull request ouverte `develop` → `main` n'existe : **phase 1**.
- Si une pull request ouverte `develop` → `main` existe et que l'utilisateur donne son feu vert : **phase 2**.
- Si l'utilisateur dit « automerge » ou « auto merge » après la phase 1 : **phase 2 en mode automerge** (voir étape 6).

```bash
gh pr list --base main --head develop --state open
```

## Phase 1 - Préparer la release et ouvrir la pull request

### Étape 1 - Vérifier l'état git

```bash
git status --porcelain
```

- Si l'arbre de travail **n'est pas propre** (modifications non commitées, fichiers non suivis pertinents) : **STOP**, demander à l'utilisateur quoi faire (commit, stash, ignorer). Ne rien faire d'autre avant sa réponse.
- Si propre : continuer.

### Étape 2 - Mettre develop à jour

```bash
git checkout develop
git pull origin develop
```

### Étape 3 - Bump de version sur develop

La version est fournie par l'utilisateur quand il invoque ce skill. **Si elle n'a pas été donnée, la demander avant de continuer** (utiliser l'outil de question).

```bash
npm version <version>
```

- `npm version` crée le commit de bump **et** le tag `v<version>` en local.
- `<version>` peut être un numéro explicite (`0.2.0`) ou un incrément (`patch`/`minor`/`major`).
- **Le tag n'est pas poussé à cette étape.**

### Étape 4 - Pousser develop (sans le tag)

```bash
git push --no-follow-tags origin develop
```

### Étape 5 - Ouvrir la pull request develop → main

```bash
gh pr create --base main --head develop --title "Release v<version>" --body "<liste des commits de la release>"
```

- Le corps de la pull request reprend la liste des commits entre le dernier tag et `v<version>`, au format de l'étape 10.
- Afficher le lien de la pull request à l'utilisateur.
- **STOP.** Attendre le feu vert de l'utilisateur pour passer à la phase 2 (relecture, workflows GitHub de la pull request au vert), ou « automerge » / « auto merge » pour que l'agent surveille lui-même les workflows.

## Phase 2 - Mise en production (sur feu vert)

### Étape 6 - Vérifier la pull request et pousser le tag

```bash
gh pr checks <numero>           # les workflows doivent être au vert
git push origin v<version>
```

- Si un workflow est en échec ou en cours : **STOP**, le signaler.

**Mode automerge** (l'utilisateur a dit « automerge » ou « auto merge ») : au lieu de s'arrêter sur des workflows en cours, l'agent les surveille lui-même jusqu'à leur fin.

```bash
gh pr checks <numero> --watch --fail-fast   # en arrière-plan, délai long (les e2e peuvent être longs)
```

- Si aucun workflow n'est encore apparu sur la pull request, attendre qu'ils apparaissent avant de lancer la surveillance : une liste vide n'est pas un succès.
- Enchaîner sur la suite de la phase 2 **UNIQUEMENT si tous les workflows sont au vert** (succès ou volontairement ignorés).
- Au moindre workflow en échec, annulé ou bloqué : **STOP**, le signaler avec le nom du workflow et le lien, ne rien pousser, ne rien fusionner, ne pas toucher à Supabase.
- Le mode automerge ne dispense d'aucune autre règle : les arrêts des étapes 7 et 8 restent obligatoires.
- Si le tag n'existe pas en local (nouvelle session, autre machine) : le recréer sur le commit de bump de develop (`git tag v<version> <commit de bump>`) avant de le pousser.
- **Ne pas fusionner la pull request à cette étape.** On ne pousse que le tag.

### Étape 7 - Mettre la base Supabase en prod

Appliquer sur le projet distant de production les migrations déjà créées et validées en local.

**Préchecks (doivent déjà être verts) :** migration dans `supabase/migrations/`, `npx supabase db reset`, `npx supabase db lint`, `npm run supabase:gen-types` si le schéma touche les types, `npm run lint`, `npm run build:local`. Si un de ces points n'est pas validé, ne pas pousser.

```bash
npx supabase link --project-ref <production-ref>   # confirmer que c'est bien la PROD
npx supabase db push
npx supabase db diff --linked                      # contrôle : aucune dérive attendue
npm run supabase:dump                              # si le schéma a changé sur le remote
```

- Toujours vérifier que `<production-ref>` correspond bien au projet de production avant `db push`.
- Si `db push` échoue ou que `db diff --linked` remonte une dérive : **STOP**, traiter avant de continuer. Ne pas passer à l'étape 8.
- S'il n'y a aucune migration à appliquer, `db push` ne fait rien : c'est normal, continuer.

### Étape 8 - Fusionner la pull request (commit de fusion)

Seulement si l'étape 7 s'est terminée sans erreur :

```bash
gh pr merge <numero> --merge
```

- **Jamais `--squash` ni `--rebase`.**
- Ne pas utiliser `--delete-branch` : `develop` doit rester.

### Étape 9 - Réintégrer main dans develop

```bash
git checkout main
git pull origin main
git checkout develop
git merge main
git push origin develop
```

- Terminer sur la branche `develop`.

### Étape 10 - Listing des commits de la release

À la toute fin, affiche moi la liste des commits de la release (entre le dernier tag et le nouveau tag) pour que je puisse rédiger le changelog.

Le format doit être le suivant :

```
📄 Version <numero de version> livrée :
- Correction : <commit 1>
- Fonctionnalité : <commit 2>
- <etc...>
```

## Résumé opératoire

```bash
# Phase 1
git status --porcelain                              # 1. doit être propre
git checkout develop && git pull origin develop     # 2.
npm version <version>                               # 3. commit + tag v<version> en local
git push --no-follow-tags origin develop            # 4. sans le tag
gh pr create --base main --head develop ...         # 5. puis STOP, attendre le feu vert

# Phase 2 (sur feu vert)
gh pr checks <numero>                               # 6. workflows au vert
git push origin v<version>                          #    tag seul
# 7. Supabase prod :
npx supabase link --project-ref <production-ref>
npx supabase db push
npx supabase db diff --linked
npm run supabase:dump                               # si nécessaire
gh pr merge <numero> --merge                        # 8. uniquement si étape 7 OK, jamais squash
git checkout main && git pull origin main           # 9.
git checkout develop && git merge main && git push origin develop
```

## Règles de décision

- **Arbre git non propre** → STOP, demander à l'utilisateur.
- **Version non fournie** → demander avant `npm version`.
- **Pull request ouverte et pas de feu vert** → ne rien faire, attendre.
- **Workflows de la pull request en échec ou en cours** → STOP, signaler (en mode automerge : attendre la fin s'ils sont en cours, STOP s'ils échouent).
- **Conflit de merge** → STOP, signaler.
- **`db push` échoue / dérive `db diff --linked`** → STOP, ne pas fusionner la pull request.
- **Projet distant non confirmé comme la prod** → ne pas `db push`.
- **Fusion refusée par GitHub (mode de fusion non autorisé)** → STOP, signaler, ne jamais basculer sur `--squash` ou `--rebase`.
