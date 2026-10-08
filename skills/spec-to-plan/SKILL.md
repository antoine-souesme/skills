---
name: spec-to-plan
description: Permet de rédiger un plan d'implémentation à partir d'une spec.
---

# Spec to plan

Ce skill permet d'utiliser superpowers:writing-plans pour écrire un plan et ajoute des instructions.

## Instructions

- Lis la spec qui est données en entrée et utilise superpowers:writing-plans pour rédiger un plan d'implémentation.
- Pas d'over-engineering dans le plan.
- Si un lien de design est donné, tu dois le prendre en compte pour la rédaction du plan. (un lien de design n'est pas forcément donné).
- Assure toi que le plan contienne le lien vers le design si il est donné.
- Assure toi de ne faire que ce qui est demandé dans la spec. Si le design ajoute des fonctionnalités, tu dois demander si tu dois les inclure dans le plan (la question doit commencer par "AJOUT DESIGN : ").
- Assure toi que le plan contienne une étape de vérification visuelle pour les éléments de l'UI qui ont été ajoutés ou modifiés. La vérification se fait avec claude-in-chrome. Le plan doit contenir des identifiants de connexion pour le compte de test. Ces identifiants peuvent être ajoutés dans .env.local s'ils ne sont pas déjà présents.
- Si tu dois mettre un placeholder pour une fonctionnalité qui n'est pas dans la spec. Tu dois ajouter une note dans les fichiers de spec concernées.