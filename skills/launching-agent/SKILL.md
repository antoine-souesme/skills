---
name: launching-agent
description: Use when asked to launch, dispatch or delegate a Claude Code agent that works in the background on a self-contained prompt (an execution agent, a small ticket, a handoff prompt) while the current session keeps the hand. Launches a sub-agent with the Agent tool. Not for quick searches or reviews done inline.
---

# Lancer un agent

Lance un sous-agent avec l'outil `Agent`, en arrière-plan, sur un prompt autoportant.
On rend la main immédiatement : le sous-agent travaille en parallèle, et sa réponse
finale revient toute seule dans la session quand il a fini.

## Utilisation

Un seul appel à l'outil `Agent` :

- `subagent_type` : `general-purpose`. Il a tous les outils, y compris `Agent` :
  il peut lui-même lancer ses propres sous-agents (exécution par sous-agents d'un plan).
- `description` : trois à cinq mots, par exemple « Exécution plan facturation ».
- `prompt` : le prompt complet, tel quel.
- Pas d'`isolation` : le sous-agent travaille dans le même dossier que la session.
  Une copie à part du dépôt n'a ni `.env.local` (identifiants du compte de test) ni
  les dépendances installées, et casserait la vérification visuelle.

Le prompt est rédigé par la session appelante. Il doit être autoportant : le sous-agent
ne connaît rien de la conversation courante. Donne-lui le but, le dossier concerné, la
branche, et ce qu'on attend dans sa réponse finale.

## Ce que le prompt dit toujours

- **Pas de question en cours de route.** Le sous-agent ne peut pas parler au
  responsable produit. Face à un blocage critique (serveur de dev à lancer, Docker
  arrêté, information manquante), il s'arrête et met la question dans sa réponse finale.
- **La réponse finale est le compte rendu.** Elle arrive telle quelle dans la session
  appelante : courte, sans raconter ce qui a été fait.

## Après le lancement

N'attends pas, ne boucle pas, ne lis pas son travail en rafale. Annonce en une ligne
la description de l'agent et son identifiant. La notification de fin arrive toute seule.

Pour lui parler pendant qu'il travaille, ou le relancer après sa réponse avec son
contexte intact : `SendMessage` avec son identifiant.

## Pièges

| Piège | Réalité |
|---|---|
| Fermer la session qui a lancé l'agent | Le sous-agent vit dans cette session : il s'arrête avec elle. |
| Lancer avec `isolation: "worktree"` pour ne plus bloquer le dossier | La copie n'a pas `.env.local` ni les dépendances : la vérification visuelle échoue. |
| Laisser l'agent poser ses questions au fil de l'eau | Il ne peut pas : il s'arrête et rend sa question dans sa réponse finale. |
| Lancer un deuxième agent pour « vérifier » le premier | Deux agents dans le même dossier se marchent dessus. On attend la notification. |
| Vérifier en parallèle ce que l'agent est en train de faire | Le travail est délégué : on attend son résultat, on ne le refait pas. |
