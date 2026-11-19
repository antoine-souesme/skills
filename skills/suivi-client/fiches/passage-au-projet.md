# Passage au projet

Quand le client a accepté, Antoine crée le dossier du code à côté du dossier de suivi (par exemple `~/dev/projets/<projet>/`). Le dossier de suivi reste séparé : rien de commercial ne va dans le dépôt de code.

## Préparer le dépôt de code

Dans `<projet>/docs/suivi/`, dossier ignoré par git :

- copie le cahier des charges et le brief ;
- copie le cadrage sous le nom `CADRAGE.md`, nettoyé de tout ce qui touche à la vente : lignes de devis, « offert », « hors devis », pénalités, contrat, prix de la prestation (les prix du produit du client restent) ;
- copie les exemples envoyés par le client (`exemples-client/`) et l'échantillon de maquettes (`maquette-echantillon/`) si le client en aime le style ;
- écris `DEMARRAGE.md` pour un nouvel agent, sans aucune notion de vente : le projet en bref, où trouver les informations, les tâches dans l'ordre, les choix techniques, la règle des comptes, ce que le client fournit. Tous les documents qu'il produira vont dans `docs/suivi/`, jamais à la racine.

Tâches habituelles à mettre dans DEMARRAGE, selon ce qu'Antoine a noté :

1. Étude de la concurrence : les plateformes du même métier, leurs parcours, leur modèle économique, leurs points forts et faibles. But : bien se démarquer, ne rien copier. Ne cite que des concurrents dont tu as vérifié l'existence.
2. Maquette complète, à partir de l'échantillon et de l'ambiance voulue par le client, chaque écran validé par lui avant sa réalisation.
3. Blocs qui ne dépendent pas des maquettes (projet, environnements, base de données, comptes, paiement), pendant la validation.

Note au journal que le projet a démarré, et dans ETAT le chemin du dépôt de code.

## Pendant le développement : reporter les demandes du client

Quand un échange avec le client change le projet, écris dans `<projet>/docs/suivi/` un document `AJOUTS_MODIFS_CLIENT_<date>.md` : ce qui change, les specs et les écrans de la maquette concernés, les numéros D-x du registre. Un nouveau mail le même jour complète le même document, dans une nouvelle partie. Puis donne à Antoine le prompt à passer à l'agent du dépôt pour l'appliquer.

Le document et le prompt ne parlent jamais de la relation client : pas de prix du projet, pas de « inclus » ou « hors devis », pas de décision commerciale d'Antoine, pas d'appel ni de mail à venir avec le client, pas de chemin vers le dossier de suivi. Ils disent seulement quoi changer dans le projet. Les textes fournis par le client sont copiés dans `<projet>/docs/suivi/exemples-client/`.

Le document et le prompt disent toujours à l'agent : si une modification touche une spec déjà développée, il ne reprend pas cette spec ; il ajoute la modification dans le bloc « fourre-tout » prévu pour la fin du développement (à créer s'il n'existe pas), avec la référence du document et de la spec concernée.

Le prompt demande toujours à l'agent de mettre à jour l'artifact du projet s'il y en a un (par exemple le canevas publié de la maquette), après ses changements.

## Renommer un dossier

Antoine renomme parfois un dossier (par exemple `<projet>-avant-vente` en `<projet>-suivi-client`). L'historique de Claude Code est rangé selon le chemin du dossier : pour qu'il puisse reprendre la conversation avec `claude --resume` depuis le nouveau nom, crée dans `~/.claude/projects/` un lien symbolique du nouveau nom encodé (les `/` deviennent des `-`) vers le dossier d'historique réel. Vérifie d'abord que la cible n'existe pas. Si la session tourne dans le dossier renommé, fais-le en dernier.
