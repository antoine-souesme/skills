# Contrat de prestation de service

## Accord du client

Quand le client accepte de travailler ensemble (souvent au téléphone), note-le au journal. Le contrat reprend le devis et son annexe : une seule signature suffit, on ne fait pas signer le devis à part.

## Questions à poser avant de rédiger

Avec AskUserQuestion, ce sont les décisions d'Antoine :

- **Échéancier** : 30 % d'acompte à la signature, puis le solde à la signature du procès-verbal de recette (son choix habituel), ou un paiement intermédiaire.
- **Délai** : date indicative sans pénalité (recommandé), ou date ferme. Si le cahier des charges prévoit des pénalités de retard, signale-le : le contrat les écarte explicitement.
- **Propriété** : cédée au paiement complet (recommandé) ou dès la livraison.
- **Statut du client** : société avec SIRET, entrepreneur, ou particulier. Ça change le contrat, voir plus bas.

## Rédaction

Pars de `modeles/CONTRAT_PRESTATION.md` et écris `06-contrat/CONTRAT_PRESTATION.md`. Avant d'écrire, relis le **PDF du devis réellement envoyé** (pas le brouillon markdown) : le contrat doit dire la même chose que lui sur le prix, le délai de paiement et la pénalité de retard.

Ce que le contrat doit contenir, et pourquoi :

- **Documents contractuels** : le contrat, puis le devis n°X et son annexe, puis le cahier des charges, dans cet ordre de priorité.
- **Périmètre** : le devis et son annexe, plus la liste explicite des ajouts promis par mail avant la signature (DEMANDES au statut incluse ou offerte qui ne sont pas au devis). Le cahier des charges sert seulement à préciser le devis : il n'ajoute aucune fonctionnalité, ni délai, ni pénalité, ni test. Sans cette phrase, le client peut exiger tout le cahier des charges pour le prix du devis.
- **Prix** ferme et forfaitaire, mention 293 B, abonnements tiers à la charge du client. Comptes créés par Antoine avec l'adresse dédiée, accès remis au paiement complet, Stripe activé par le client sur invitation (voir `fiches/annexe.md`).
- **Paiement** : tableau des échéances. Les travaux commencent à réception de l'acompte. Délai et pénalité identiques au devis. L'indemnité forfaitaire de 40 € seulement pour un client professionnel.
- **Déroulement** : maquettes validées par écrit, réalisation visible sur l'adresse de test, recette de 10 jours ouvrés avec acceptation tacite sans retour, une anomalie mineure ne bloque pas la recette, mise en production après le PV.
- **Délai** indicatif, reporté en cas de retard du client. « Les dates et pénalités figurant au cahier des charges ne s'appliquent pas. »
- **Obligations du client** : contenus, validations, droits sur ce qu'il fournit. **Obligation de moyens** pour Antoine.
- **Modifications** : tout ce qui sort du périmètre de l'article 2 fait l'objet d'un devis séparé.
- **Garantie** de 3 mois après le PV : anomalies et petites retouches.
- **Propriété intellectuelle** : sans clause de cession, le code reste à Antoine même payé. L'article L131-3 du Code de la propriété intellectuelle impose de nommer chaque droit cédé (reproduction, représentation, adaptation, distribution), le domaine d'exploitation, le territoire et la durée. Le droit moral ne se cède pas. Exclure les savoir-faire et outils génériques, l'open source et les contenus du client. Droit de citer le projet en référence, sauf refus écrit.
- **Données personnelles** : Antoine est sous-traitant au sens de l'article 28 du RGPD. Objet et durée, données et personnes concernées, traitement sur instruction, confidentialité, sécurité, sous-traitants autorisés (les services de l'annexe), aide au client, notification d'une violation sous 48 heures, suppression en fin de contrat, information pour vérifier.
- **Responsabilité** plafonnée au montant payé, pas de dommages indirects.
- **Résiliation** après mise en demeure de 15 jours, travail réalisé dû, acompte acquis.
- **Force majeure**, droit français, tribunal de la ville du ressort d'Antoine.
- **Signatures** : le client signe sur son ordinateur. Pas de « Fait en deux exemplaires, à… le… ». Tableau Prestataire / Client.

Services tiers (RGPD) : ils sont souscrits pour le compte et aux frais du client, qui les choisit comme sous-traitants directs ; Antoine ne répond pas de leur fonctionnement ; seule la base de données est hébergée en Europe ; en fin de contrat, suppression ou restitution des données au choix du client. Antoine a refusé, pour QuiPeutMaider, la clause « solde dû si la recette est acceptée sans signature » et la clause « projet bloqué plus de 30 jours » : ne les propose pas d'office.

## Client particulier ou petit professionnel

Un particulier n'agit pas pour son activité professionnelle : retire l'indemnité de 40 €. S'il signe hors des locaux d'Antoine, il peut avoir 14 jours pour se rétracter : ajoute l'information et le formulaire, sinon le délai passe à 12 mois. Les petits professionnels (5 salariés au plus) qui signent hors établissement pour un service hors de leur activité principale ont aussi ce droit (article L221-3 du code de la consommation). Sans SIRET, la propriété est cédée à la personne elle-même : demande à Antoine si une société est en création.

## PDF

```bash
python <dossier du skill>/scripts/annexe_pdf.py 06-contrat/CONTRAT_PRESTATION.md 06-contrat/Contrat_Prestation_<Projet>.pdf \
  --pied "Contrat de prestation de service · <Projet>"
```

Rends le PDF en images et vérifie chaque page avant de le donner. Propose ensuite la relecture neuve (`fiches/relecture.md`).

## Message d'envoi

Pièces jointes : le contrat, le devis n°X, l'annexe à jour. Le message dit ce que reprend le contrat, ce qui change dans l'annexe le cas échéant, les points principaux (acompte, date visée, maquettes, garantie), et annonce la facture d'acompte après la signature.
