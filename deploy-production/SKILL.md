---
name: deploy-production
description: Mise en production du projet
disable-model-invocation: true
---

# Mise en production

Orchestration complète d'une release : git (develop → main), versioning, déploiement Supabase distant, puis réintégration dans develop. Ce skill remplace et englobe l'ancienne procédure de déploiement Supabase seul.

## Principe central

**On ne pousse jamais `main` tant que la mise en prod Supabase n'a pas réussi.** L'ordre des étapes est une garantie : le code public (`main` poussé) ne doit jamais être en avance sur la base de prod.

## Règles absolues

- Ne jamais demander d'autorisation pour les opérations git (conformément aux conventions du projet).
- Suivre l'ordre des étapes **exactement**. Ne pas pousser `main` avant l'étape 6.
- La source de vérité du schéma reste `supabase/migrations/*.sql`. Jamais le dashboard.
- Si une étape échoue, s'arrêter, analyser, et ne pas enchaîner la suivante.

## Procédure (ordre impératif)

### Étape 1 - Vérifier l'état git

```bash
git status --porcelain
```

- Si l'arbre de travail **n'est pas propre** (modifications non commitées, fichiers non suivis pertinents) : **STOP**, demander à l'utilisateur quoi faire (commit, stash, ignorer). Ne rien faire d'autre avant sa réponse.
- Si propre : continuer.

### Étape 2 - Merge develop dans main (sans push)

```bash
git checkout main
git merge develop
```

- **Ne pas pousser `main`.**
- En cas de conflit : s'arrêter et le signaler.

### Étape 3 - Bump de version sur main

La version est fournie par l'utilisateur quand il invoque ce skill. **Si elle n'a pas été donnée, la demander avant de continuer** (utiliser l'outil de question).

```bash
npm version <version>
```

- `npm version` crée le commit de bump **et** le tag `v<version>` sur `main`.
- `<version>` peut être un numéro explicite (`0.2.0`) ou un incrément (`patch`/`minor`/`major`).

### Étape 4 - Pousser le tag uniquement

```bash
git push origin v<version>
```

- **`main` n'est toujours pas poussé.** On ne pousse que le tag créé à l'étape 3.

### Étape 5 - Mettre la base Supabase en prod

Appliquer sur le projet distant de production les migrations déjà créées et validées en local.

**Préchecks (doivent déjà être verts) :** migration dans `supabase/migrations/`, `npx supabase db reset`, `npx supabase db lint`, `npm run supabase:gen-types` si le schéma touche les types, `npm run lint`, `npm run build:local`. Si un de ces points n'est pas validé, ne pas pousser.

```bash
npx supabase link --project-ref <production-ref>   # confirmer que c'est bien la PROD
npx supabase db push
npx supabase db diff --linked                      # contrôle : aucune dérive attendue
npm run supabase:dump                              # si le schéma a changé sur le remote
```

- Toujours vérifier que `<production-ref>` correspond bien au projet de production avant `db push`.
- Si `db push` échoue ou que `db diff --linked` remonte une dérive : **STOP**, traiter avant de continuer. Ne pas passer à l'étape 6.
- S'il n'y a aucune migration à appliquer, `db push` ne fait rien : c'est normal, continuer.

### Étape 6 - Pousser main

Seulement si l'étape 5 s'est terminée sans erreur :

```bash
git push origin main
```

### Étape 7 - Réintégrer main dans develop

```bash
git checkout develop
git merge main
```

- Terminer sur la branche `develop`.

### Étape 8 - Listing des commits de la release

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
git status --porcelain                              # 1. doit être propre
git checkout main && git merge develop              # 2. pas de push
npm version <version>                               # 3. commit + tag v<version>
git push origin v<version>                          # 4. tag seul
# 5. Supabase prod :
npx supabase link --project-ref <production-ref>
npx supabase db push
npx supabase db diff --linked
npm run supabase:dump                               # si nécessaire
git push origin main                                # 6. uniquement si étape 5 OK
git checkout develop && git merge main              # 7. fin sur develop
```

## Règles de décision

- **Arbre git non propre** → STOP, demander à l'utilisateur.
- **Version non fournie** → demander avant `npm version`.
- **Conflit de merge** → STOP, signaler.
- **`db push` échoue / dérive `db diff --linked`** → STOP, ne pas pousser `main`.
- **Projet distant non confirmé comme la prod** → ne pas `db push`.
