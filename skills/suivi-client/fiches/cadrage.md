# Cadrage

## Comprendre et remettre en forme

1. Lis le brief et le cahier des charges fournis, range-les dans `01-sources/`.
2. Remets le cahier des charges en markdown propre : titres, listes, citations, tableaux. Corrige seulement les fautes de frappe, ne change pas le fond.
3. Liste les incohérences relevées et rends la main.

## Découper en blocs et en vagues

Écris `02-cadrage/CADRAGE_V1.md` :

- Une partie « Comprendre le produit » : rôles, parcours, modèle économique.
- **1 bloc = 1 session Claude Code** (spec, plan, implémentation). Un bloc doit tenir dans une session : découpe plus fin si besoin. Numérote les blocs N.n.
- **1 vague = un ensemble de blocs qui forment un tout logique**, dans l'ordre de construction. Chaque vague deviendra une ligne du devis.
- Commence par une vague « Fondations » (projet, environnements, déploiement, e-mails, identité visuelle, design system) et termine par « Recette et mise en production ».
- Une partie « Questions » : celles auxquelles le cahier des charges répond déjà, puis les questions ouvertes, numérotées.
- En fin de fichier, un tableau résumé : vague, nombre de blocs, total.

Nomme clairement les vagues qui pourraient être mal comprises. Par exemple, une vague de publicité vendue aux prestataires s'appelle « Offres publicitaires payantes pour les prestataires », pour qu'on ne croie pas qu'Antoine gère la publicité du client.

Le cadrage est interne : il peut parler de blocs et de vagues. Il ne part jamais tel quel chez le client.

## Faire vivre le cadrage

- Chaque précision du client qui change le contenu d'un bloc y est reportée, avec le détail qu'il a donné (listes de réponses, libellés, exemples).
- Quand une question ouverte est réglée (par un mail, un appel, une image du client), barre-la et écris la réponse avec la date : `~~**Question**~~ : réglé le 13/11. <réponse>`.
- Après un appel, Antoine écrit ses notes dans `APPEL.md`. Reporte dans le cadrage la partie qu'il marque « à ajouter au cadrage », et rien d'autre sans qu'il le demande.
- Rythme réaliste à garder en tête pour les délais : 5 à 6 blocs par jour de travail. Tout ce qui ne se voit pas (projet, environnements, base de données, comptes, paiement) peut démarrer avant la validation des maquettes.
