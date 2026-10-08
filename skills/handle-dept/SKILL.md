---
name: handle-dept
description: Permet de s'occuper des points de dettes qui ont été mis de coté par l'agent lors de l'exécution du plan.
disable-model-invocation: true
---

# Handle Dept

Analyse le fichier @docs/suivi/DETTE.md et traite les points de dettes qui y sont consignés.

## Avant le traitement

- Analyse les points à traiter et garde uniquement ceux qui sont absolument indispensables pour le fonctionnement de l'application.
- Les problèmes d'UI sont à corriger.
- Les problèmes de typographie sont à corriger.
- Supprimes les autres points avant de commencer le traitement.
- Si un des points que tu as gardé demande une décision de ma part, on décide ensemble de la marche à suivre avant que tu commences.

## Après le traitement

- Pas besoin de me résumer ce que tu as fait. Sauf point critique.
- Fais une pr sur develop.