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

## Renommer un dossier

Antoine renomme parfois un dossier (par exemple `<projet>-avant-vente` en `<projet>-suivi-client`). L'historique de Claude Code est rangé selon le chemin du dossier : pour qu'il puisse reprendre la conversation avec `claude --resume` depuis le nouveau nom, crée dans `~/.claude/projects/` un lien symbolique du nouveau nom encodé (les `/` deviennent des `-`) vers le dossier d'historique réel. Vérifie d'abord que la cible n'existe pas. Si la session tourne dans le dossier renommé, fais-le en dernier.
