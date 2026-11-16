# Skill `/antoine:suivi-client` : conception

## Intention

Antoine (développeur web indépendant, micro-entreprise en franchise de TVA) veut un assistant de suivi de la relation client qui l'accompagne comme l'a fait la session QuiPeutMaider : du premier brief jusqu'après la livraison. Il produit les documents (cadrage, devis, annexe, réponses, maquettes, contrat, factures) et surtout **n'oublie rien d'une session à l'autre** : chaque mail du client est rangé, chaque demande inscrite, chaque décision datée. Antoine doit pouvoir dire « liste-moi toutes les évolutions demandées et fais-moi un devis avec tout ça ».

Il remplace le skill `avant-vente`, qui sait produire les documents jusqu'au contrat mais n'a pas de mémoire entre les sessions.

## Objectifs

- Une seule commande : `/antoine:suivi-client`, lancée dans le dossier de suivi d'un client.
- À chaque lancement, l'assistant lit son suivi et sait où on en est, sans qu'Antoine réexplique.
- Tout mail collé par Antoine (reçu ou envoyé) est rangé et analysé : évolution, bug, question, décision, information.
- Un registre des demandes du client, interrogeable (« toutes les évolutions non chiffrées ») et utilisable pour un devis.
- Toutes les tâches de l'avant-vente actuel restent possibles, plus le contrat, la facturation (acompte, solde) et le suivi après la livraison (recette, garantie, nouvelles demandes).
- Avant un envoi important (devis, contrat, gros mail), l'assistant propose une relecture par un agent neuf, sans l'imposer.

## Non-objectifs

- Il n'envoie aucun mail et ne touche à aucun service externe : il rédige, Antoine envoie.
- Il ne crée pas les factures : Antoine les fait dans son logiciel de facturation. L'assistant lui dit quoi y mettre.
- Il ne développe pas le projet du client et n'écrit rien dans le dépôt de code.
- Pas de base de données ni de format machine : tout reste en markdown lisible et modifiable à la main.

## Anti-objectifs (échec même si ça marche)

- Une nouvelle session qui repose des questions déjà tranchées, ou qui ignore une décision du journal.
- Une demande du client perdue, ou un statut faux (une évolution marquée « livrée » alors qu'elle ne l'est pas).
- Du vocabulaire interne qui sort vers le client (bloc, vague, marge, session Claude Code).
- Une décision commerciale prise par l'assistant à la place d'Antoine.
- Un `SKILL.md` si long que la session s'y noie.

## Contraintes

- Plugin `antoine` dans `~/dev/projets/claude-plugin` : la commande est préfixée `antoine:`.
- Un sous-agent ne peut pas poser de questions à Antoine en cours de route : l'accompagnement se fait donc par la session principale qui endosse le rôle. Seule la relecture neuve est confiée à un sous-agent.
- Consignes d'Antoine : tutoiement avec lui, réponses courtes, pas de tiret cadratin dans ce qui va au client, pas de ponctuation en fin de puce, accents.
- Le script PDF exige reportlab (4.2.5 si Python 3.9).

## Approches envisagées

1. **Un seul skill avec une fiche par tâche** : `SKILL.md` court (rôle, règles, suivi), et des fiches chargées à la demande.
2. **La même chose, avec un relecteur neuf en option avant les envois importants.** **Choisie par Antoine.**
3. Plusieurs commandes séparées (`/devis`, `/contrat`…) : écartée, perte du point d'entrée unique et chaque commande relirait tout le suivi.

## Ce qui est décidé

### Dossier de suivi d'un client

Un dossier par client, à côté du dépôt de code, nommé `<projet>-suivi-client/` :

```
<projet>-suivi-client/
├── _assistant/
│   ├── ETAT.md        où on en est, ce qui attend qui, prochaines actions (lu en premier)
│   ├── DEMANDES.md    registre numéroté des demandes du client
│   └── JOURNAL.md     décisions et événements datés, du plus récent au plus ancien
├── 01-sources/        brief, cahier des charges remis en forme
├── 02-cadrage/        CADRAGE_V1.md
├── 03-devis/          devis, annexe, PDF
├── 04-echanges-client/ mails reçus et envoyés, un fichier par mail
├── 05-maquettes/      inspiration, échantillon, sources
├── 06-contrat/        contrat et PDF
├── 07-facturation/    suivi des factures (acompte, solde)
├── APPEL.md           notes d'appel d'Antoine (facultatif)
└── piece-jointes-envoyees/<date>/  images du client
```

### `_assistant/ETAT.md`

Court (une page). Sections : client et projet en deux lignes, étape actuelle, documents en vigueur (la version à jour de chaque document envoyé ou à envoyer), ce qui attend Antoine, ce qui attend le client, questions ouvertes, prochaines actions. Réécrit (pas allongé) à chaque changement.

### `_assistant/DEMANDES.md`

Un tableau, une ligne par demande :

| N° | Date | Type | Demande | Source | Statut | Suite |
|---|---|---|---|---|---|---|

- Type : évolution, bug, question, contenu à fournir, administratif.
- Source : le fichier du mail dans `04-echanges-client/` ou l'appel.
- Statut : nouvelle, à arbitrer, incluse (dans le périmètre actuel), offerte, chiffrée (devis n°X), acceptée, livrée, refusée, répondue.
- Suite : décision d'Antoine, référence du devis ou de la réponse.
- Numérotation D-1, D-2… jamais réutilisée.

### `_assistant/JOURNAL.md`

Une entrée datée par décision ou événement : « 2026-11-13 · Ouverture des comptes de réseaux sociaux offerte (D-4) ». Ce qu'Antoine a décidé, pas ce que l'assistant a fait.

### Comportement à chaque lancement

1. Si `_assistant/` n'existe pas : proposer de l'initialiser (créer l'arborescence, puis remplir ETAT à partir des documents présents s'il y en a).
2. Sinon : lire ETAT, puis JOURNAL (entrées récentes) et DEMANDES (statuts ouverts). Annoncer en trois lignes où on en est et ce qui est en attente, puis attendre la demande d'Antoine.
3. Après chaque action qui change l'état (document produit, mail rangé, décision prise), mettre à jour ETAT, DEMANDES et JOURNAL avant de rendre la main.

### Mail collé par Antoine

1. Le ranger dans `04-echanges-client/AAAA-MM-JJ_recu_<sujet>.md` (ou `_envoye_`), texte intégral.
2. Le découper en demandes : chacune devient une ligne de DEMANDES, avec un statut proposé (incluse si déjà dans le cadrage ou le devis, à arbitrer sinon).
3. Résumer à Antoine : ce qui est déjà prévu, ce qui est nouveau, ce qu'il doit trancher (AskUserQuestion pour les décisions commerciales).
4. Proposer une réponse si le mail en attend une.

### Fiches par tâche (chargées à la demande)

`fiches/` dans le skill :

- `cadrage.md` : remise en forme du cahier des charges, blocs et vagues, questions (étapes 1 et 2 de l'avant-vente actuel).
- `devis.md` : chiffrage interne, présentation client, prix négocié ; devis d'évolutions à partir des demandes sélectionnées dans DEMANDES.
- `annexe.md` : technologies, frais, hors devis, génération PDF.
- `mails.md` : rangement et analyse d'un mail reçu, rédaction d'une réponse, repères (concurrent moins cher, hébergement, déroulement, prix, relation durable, précisions du client, tutoiement ou vouvoiement selon le client).
- `maquettes.md` : échantillon, inspiration sans copie, PDF professionnel, statut d'échantillon.
- `contrat.md` : questions à poser, clauses et leur raison, cas du client particulier, signature électronique, cohérence avec le devis réellement envoyé (le PDF, pas le brouillon).
- `facturation.md` : facture d'acompte, facture de solde, mentions, échéancier du contrat.
- `relecture.md` : quand proposer la relecture neuve, et le prompt du sous-agent (documents à lire, décisions d'Antoine à ne pas rediscuter, sortie : points classés avec correction prête à coller, 600 mots maximum). Rappel : vérifier ses constats contre les vrais documents envoyés avant de les relayer.
- `passage-au-projet.md` : préparer le dossier du dépôt de code (`docs/suivi/` ignoré par git, DEMARRAGE.md sans aucune notion de vente, copie du cadrage nettoyé, des sources et de l'échantillon), et renommage de dossier avec le lien d'historique.

Le contenu vient de l'actuel `skills/avant-vente/SKILL.md` et des enseignements de la session QuiPeutMaider (décisions et corrections d'Antoine).

### Fichiers conservés

- `modeles/CONTRAT_PRESTATION.md`, mis à jour avec la version finale du contrat QuiPeutMaider (périmètre qui n'inclut pas le cahier des charges, paiement sous 15 jours, comptes créés par le prestataire avec adresse dédiée, Stripe sur invitation, pas de « Fait à »).
- `scripts/annexe_pdf.py`, inchangé (annexe et contrat).
- Nouveaux modèles : `modeles/ETAT.md`, `modeles/DEMANDES.md`, `modeles/JOURNAL.md`.

### Migration de QuiPeutMaider

- Renommer `~/dev/projets/quipeutmaider-avant-vente` en `~/dev/projets/quipeutmaider-suivi-client`.
- Créer `_assistant/` rempli à partir de la session : ETAT (contrat prêt à envoyer avec devis et annexe du 15/11, message rédigé, points 2 à 5 de la relecture en réflexion, statut du client à confirmer, facture d'acompte à émettre après signature, projet démarré dans `~/dev/projets/quipeutmaider`), DEMANDES (toutes les demandes du client depuis le premier brief avec leur statut), JOURNAL (décisions datées : prix 4 750 €, ligne offerte, comptes offerts, pixels, pubs avec la maquette, date début janvier, propriété au paiement, Stripe sur invitation…).
- Renommer les mails existants de `04-echanges-client/` au nouveau format, et y ajouter les mails du client collés dans la session (texte intégral).
- Créer le lien d'historique `~/.claude/projects/` pour le nouveau nom.

### Plugin

- Supprimer `skills/avant-vente/`, créer `skills/suivi-client/`.
- README : remplacer la ligne avant-vente.
- `plugin.json` : version 1.3.0.
- `claude plugin validate .` doit passer.

### Précisions après relecture

- **Ordre de la migration** : elle est faite depuis la session QuiPeutMaider elle-même, qui a toute la conversation en mémoire. Le renommage du dossier est la toute dernière étape, suivi du lien d'historique. Antoine reprend ensuite avec `claude --resume` ou ouvre une nouvelle session avec `/antoine:suivi-client`.
- **Source des éléments de conversation** : les mails du client, les décisions et leurs dates sont tirés de la conversation par la session qui migre. En cas de doute, l'historique de la session peut être consulté par recherche ciblée, jamais lu en entier.
- **Mails existants** : `REPONSE_CLIENT_TECHNIQUE` envoyé le 12/11, `REPONSE_CLIENT_ACCORD` envoyé le 12/11 (version validée sur capture), `REPONSE_CLIENT_PRECISIONS` envoyé le 13/11 (version validée sur capture), `REPONSE_CLIENT_CONTRAT` pas encore envoyé (reste un brouillon, nommé `brouillon_`). Les mails du client sont datés du jour où Antoine les a collés.
- **Périmètre de DEMANDES** : le cahier des charges reste la référence du périmètre initial et n'est pas recopié ligne à ligne. DEMANDES contient seulement ce que le client a demandé en dehors ou en plus (précisions, ajouts, questions, contenus à fournir), et ce qu'il demandera ensuite. Une demande est « incluse » quand le cadrage ou le devis la couvre déjà.
- **Dépôt du plugin** : on part de l'état actuel non commité, sur `main`. `avant-vente` est remplacé, la version passe à 1.3.0. Aucun commit sans l'accord d'Antoine.

## Laissé au constructeur

- La rédaction exacte des fiches, en reprenant le fond de l'avant-vente actuel.
- Le découpage précis du contenu entre `SKILL.md` et les fiches, tant que `SKILL.md` reste sous ~150 lignes.
- La formulation du résumé de début de session.
