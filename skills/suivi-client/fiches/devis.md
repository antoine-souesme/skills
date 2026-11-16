# Devis

## Devis initial

Écris `03-devis/DEVIS_Vn.md`.

Base de chiffrage, interne seulement :

- 5 blocs par jour, 400 € par jour, soit **80 € par bloc**.
- Prix d'une vague = nombre de blocs × prix du bloc.
- Une marge éventuelle (par exemple 500 €) reste interne : elle ne figure jamais comme ligne visible par le client.

Pour le client :

- Une ligne par vague : intitulé, contenu en langage simple, prix. Pas de colonne « blocs » ni « jours ».
- Un total, puis la mention 293 B.
- Une ligne offerte reste visible, avec « (offert) » dans l'intitulé et un prix à 0 €.
- Pour atteindre un prix négocié, augmente le nombre de blocs par jour (par exemple 6), puis arrondis chaque ligne à 5 € et ajuste pour que le total tombe juste. Vérifie la somme.

Antoine saisit ensuite le devis dans son logiciel de facturation. Le fichier markdown n'est qu'une source : **le devis qui fait foi est le PDF qu'il a envoyé**, rangé dans `03-devis/`. Note dans ETAT lequel est en vigueur, et relis toujours ce PDF (pas le brouillon) avant de comparer un autre document au devis.

## Négociation

- Le prix accepté, la remise et le prix plancher sont des décisions d'Antoine.
- Face à une contre-proposition, explique pourquoi le prix est déjà serré au regard du périmètre, sans détailler la méthode interne.
- Une concession se marque au journal avec ce qu'elle couvre (par exemple « 4 750 €, création des comptes de réseaux sociaux hors devis »).

## Vérifier un devis avant l'envoi

Antoine t'envoie le PDF ou une capture. Vérifie :

- que la somme des lignes donne le total ;
- que le devis a un numéro, et que l'annexe et le contrat reprennent ce numéro ;
- que la mention de l'annexe correspond à son contenu actuel ;
- que la ligne offerte est lisible comme offerte ;
- les conditions de paiement (délai, pénalité de retard), pour que le contrat dise la même chose.

Réponds « oui, tu peux envoyer » ou « pas encore », puis liste seulement ce qu'il faut corriger.

## Devis d'évolutions

Quand Antoine demande un devis à partir des demandes du client :

1. Filtre `_assistant/DEMANDES.md` : type évolution (ou ce qu'il précise), statut nouvelle, à arbitrer ou acceptée et pas encore chiffrée. Jamais une demande livrée, refusée, incluse ou offerte.
2. Montre-lui la liste (numéro, date, demande) et laisse-le retirer ou regrouper.
3. Pour chaque demande retenue, estime le nombre de blocs avec le cadrage comme référence, et pose les questions de périmètre qui changent le prix.
4. Écris `03-devis/DEVIS_EVOLUTIONS_<n>.md` : une ligne par évolution ou par groupe cohérent, prix au bloc, total, mention 293 B. Indique la date du mail d'origine dans le libellé si ça aide le client à s'y retrouver.
5. Une fois le devis envoyé, passe chaque demande au statut « chiffrée (devis n°X) », et note l'envoi au journal. À l'accord du client : « acceptée ».
