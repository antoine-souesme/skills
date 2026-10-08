---
name: spec-to-implementation
description: Permet de passer d'une spec à l'exécution : rédige le plan, prépare le handoff, puis lance l'agent d'exécution dans la pane du dessous.
---

# Spec to implementation

Enchaîne trois étapes sans t'arrêter entre elles : le plan, le handoff, le lancement.

## Étape 1 — Le plan

Utilises `/antoine:spec-to-plan` et applique ses instructions intégralement
pour rédiger le plan d'implémentation à partir de la spec donnée en entrée.

Les questions prévues par ce skill (« AJOUT DESIGN : … », connexion au compte de test)
restent des questions : tu les poses et tu attends la réponse avant de continuer.

## Étape 2 — Le handoff

Utilises `/antoine:handoff` et applique ses instructions intégralement au
plan que tu viens d'écrire. Tu obtiens le prompt de reprise pour une nouvelle session.

Affiche ce prompt entouré de `---`, comme le prévoit le skill handoff. C'est la trace :
si le lancement échoue, il reste copiable à la main.

## Étape 3 — Le lancement

Écris le prompt dans un fichier temporaire (jamais en argument de commande : il contient
des guillemets et des backticks), puis lance l'agent d'exécution :

```bash
${CLAUDE_PLUGIN_ROOT}/skills/launching-agent-below/launch-below.sh --name exec --prompt-file <fichier>
```

Ce script est la seule façon de lancer l'agent : il gère la pane du dessous, coupe une
session en place et refuse de sortir du workspace courant. Ne bricole pas les commandes
`herdr` à la main. En cas de doute sur son comportement, utilises `/antoine:launching-agent-below`.

## Après le lancement

N'attends pas l'agent d'exécution, ne surveille pas sa pane. Termine en une ligne : la
pane utilisée et le nom de l'agent. Ne résume pas le plan, il est écrit dans le fichier.

## Pièges

| Piège | Réalité |
|---|---|
| Passer le prompt de handoff en argument shell | Guillemets et backticks le cassent. Toujours `--prompt-file`. |
| Demander confirmation avant de lancer | Le lancement est automatique. Le prompt affiché tient lieu de trace. |
| Attendre le résultat de l'agent d'exécution | Il travaille en parallèle. On rend la main. |
