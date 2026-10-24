---
name: spec-to-implementation
description: Permet de passer d'une spec à l'exécution : rédige le plan, prépare le handoff, puis lance l'agent d'exécution en sous-agent.
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

Utilises `/antoine:launching-agent` et applique ses instructions intégralement pour
lancer l'agent d'exécution avec le prompt de handoff, tel quel, en description
« Exécution <nom du plan> ».

## Après le lancement

N'attends pas l'agent d'exécution, ne lis pas son travail en cours. Termine en une
ligne : la description de l'agent et son identifiant. Ne résume pas le plan, il est
écrit dans le fichier.

Sa réponse finale arrive toute seule dans la session quand il a fini.

## Pièges

| Piège | Réalité |
|---|---|
| Raccourcir ou reformuler le prompt de handoff en le passant à l'agent | Il ne connaît rien de la conversation. Le prompt part tel quel. |
| Demander confirmation avant de lancer | Le lancement est automatique. Le prompt affiché tient lieu de trace. |
| Attendre le résultat de l'agent d'exécution | Il travaille en parallèle. On rend la main. |
| Fermer la session juste après le lancement | L'agent d'exécution vit dans cette session : il s'arrête avec elle. |
