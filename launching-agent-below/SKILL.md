---
name: launching-agent-below
description: Use when asked to launch, dispatch or delegate a Claude Code agent in the Herdr pane below the current one, to give work to "the pane below", or to send a prompt to a neighbouring agent pane. Requires HERDR_ENV=1. Not for in-process subagents (Agent tool) or plain background commands.
---

# Lancer un agent dans la pane du dessous

Ouvre (ou recycle) la pane Herdr située juste sous la pane courante, y démarre une
session Claude Code fraîche, et lui envoie un prompt. On rend la main immédiatement :
l'agent du dessous travaille en parallèle, le focus reste dans la pane appelante.

## Utilisation

```bash
skills/launching-agent-below/launch-below.sh [--name NOM] [--cwd CHEMIN] "le prompt"
skills/launching-agent-below/launch-below.sh [--name NOM] [--cwd CHEMIN] --prompt-file CHEMIN
```

Le chemin absolu du script est `~/.claude/skills/launching-agent-below/launch-below.sh`.
`--name` (défaut `below`) est le nom Herdr de l'agent, `--cwd` (défaut `$PWD`) le dossier
de travail utilisé seulement à la création de la pane. `--prompt-file` lit le prompt dans
un fichier : à préférer dès que le prompt est long ou contient des guillemets, des
backticks ou des `$`, qu'un argument shell abîmerait.

Le prompt est rédigé par l'agent appelant. Il doit être autoportant : la session du
dessous ne connaît rien de la conversation courante. Donne-lui le but, le dossier
concerné et ce qu'on attend en retour.

## Ce que fait le script

1. Refuse de tourner hors d'une pane Herdr (`HERDR_ENV=1`).
2. Cherche la pane du dessous avec `herdr pane neighbor --pane "$HERDR_PANE_ID"` ;
   s'il n'y en a pas, la crée avec `herdr pane split --pane "$HERDR_PANE_ID" --direction down --no-focus`.
3. Vérifie que la pane visée est bien dans le workspace et le tab de la pane appelante,
   et qu'elle n'est pas la pane appelante elle-même. Sinon : abandon.
4. Si un agent occupe déjà cette pane, le coupe (deux `ctrl+c` rapprochés, jusqu'à
   5 tentatives) pour repartir sur une session neuve.
5. Si un autre processus tient la pane (serveur, éditeur, commande longue), s'arrête
   sans rien casser : c'est à l'utilisateur de trancher.
6. `herdr agent start <nom> --kind claude --pane <cible>`, puis
   `herdr agent prompt <cible> "<prompt>"` sans `--wait` — ciblage par `pane_id`, jamais par nom.

## Après le lancement

N'attends pas, ne boucle pas, n'interroge pas la pane en rafale. Annonce simplement la
pane et le nom de l'agent. Pour reprendre contact plus tard :

```bash
herdr agent get <nom>
herdr agent read <nom> --source recent-unwrapped --lines 120
```

## Pièges

| Piège | Réalité |
|---|---|
| `--current` désigne la pane appelante | Faux pour `pane neighbor` : il retombe sur la pane focalisée dans l'interface, qui peut être dans un **autre workspace**. Toujours passer `--pane "$HERDR_PANE_ID"`. |
| `herdr pane neighbor` renvoie toujours un `pane_id` | C'est la pane source. Le voisin est `neighbor_pane_id`, absent s'il n'y a pas de voisin. |
| Cibler un agent par son nom | Un homonyme peut vivre dans un autre workspace. On cible par `pane_id`. |
| Tester le processus au premier plan pour savoir si un agent tourne | Claude Code affiche `caffeinate` au premier plan. La source fiable est `herdr agent list`. |
| Un seul `ctrl+c` pour quitter Claude Code | Le premier interrompt le travail en cours, il en faut deux rapprochés pour sortir. |
| Fermer la pane du dessous pour la remettre à neuf | On ne ferme pas une pane qu'on n'a pas créée. On coupe l'agent, c'est tout. |
| Relancer le script pour « vérifier » | Chaque appel tue la session en place. Un lancement, un prompt. |
