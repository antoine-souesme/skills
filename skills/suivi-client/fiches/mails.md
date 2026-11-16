# Mails

## Ranger un mail

Chaque mail, reçu ou envoyé, a son fichier dans `04-echanges-client/`, avec le texte intégral :

- `AAAA-MM-JJ_recu_<sujet>.md` : mail du client, daté du jour où Antoine le colle (ou de la date du mail si elle est visible)
- `AAAA-MM-JJ_brouillon_<sujet>.md` : réponse en cours de rédaction
- `AAAA-MM-JJ_envoye_<sujet>.md` : réponse envoyée, renommée le jour de l'envoi

Un fichier commence par l'objet sur la première ligne. Pour un mail reçu, ajoute en tête `De : <client>` et la date. Si Antoine a modifié le brouillon avant l'envoi (il te montre souvent une capture), le fichier envoyé reprend le texte réellement envoyé.

## Analyser un mail du client

Quand Antoine colle un mail :

1. Range-le.
2. Découpe-le en demandes. Pour chacune, cherche dans le cadrage et le devis en vigueur (`grep`) si elle est déjà couverte.
3. Inscris chaque demande dans `_assistant/DEMANDES.md` : « incluse » si le cadrage ou le devis la couvre, « à arbitrer » sinon, « contenu à fournir » quand c'est au client de fournir quelque chose.
4. Si le client joint des images, Antoine les range dans `piece-jointes-envoyees/<date>/`. Lis-les : elles précisent souvent une demande ou règlent une question ouverte du cadrage.
5. Résume à Antoine en trois groupes : **déjà prévu**, **petits ajouts** qui entrent dans un bloc existant, **vrais changements** (un nouveau livrable, ce qui était hors devis). Le client demande souvent beaucoup avant de signer : dire que la plupart est déjà prévue rassure Antoine.
6. Pour chaque petit ajout ou vrai changement, demande à Antoine avec AskUserQuestion : inclus sans changer le prix, offert, payant (devis d'évolutions), hors devis, ou fait plus tard avec la maquette.
7. Reporte ses décisions : DEMANDES (statut, suite), JOURNAL, cadrage (bon bloc, détail donné par le client), annexe si ce qui est inclus ou hors devis change.
8. Propose une réponse si le mail en attend une.

## Rédiger une réponse

Écris-la dans un fichier `_brouillon_` et retravaille-la avec Antoine jusqu'à l'envoi. Objet en première ligne.

- Commence par ce qui est déjà prévu, puis ce qu'Antoine ajoute « sans modifier le prix », puis ce qu'il offre.
- Ne demande pas au client des informations de détail (libellés, listes de réponses, textes) : écris qu'elles seront arrêtées ensemble lors de la validation de la maquette de l'écran concerné.
- Avant la signature : le détail de chaque écran est calé étape par étape une fois le contrat de prestation de service signé, et le client valide chaque maquette avant sa réalisation. Termine en disant qu'il faut maintenant se mettre d'accord sur le fait de travailler ensemble, et qu'Antoine enverra ensuite le contrat. Ne demande pas de signer le devis : le contrat reprend le devis et l'annexe, une seule signature suffit.
- Si l'annexe a changé : « Vous trouverez ci-joint l'annexe au devis mise à jour : <changements>. Elle remplace la précédente et fait partie intégrante du devis. »
- Le mail liste ce que contient le devis, puis ce que détaille l'annexe, puis les pièces jointes.
- Si le client a envoyé un autre mail entre-temps, Antoine répond dans la même conversation : « J'ai bien pris connaissance de votre autre email, je reste sur cette conversation par souci de simplicité. »
- Avant l'envoi, donne à Antoine la liste à cocher des pièces jointes, avec le chemin exact de la bonne version de chaque fichier.

## Repères qui ont servi

- **Face à un concurrent moins cher** : ne nomme pas le concurrent. Montre les coûts qu'il ne précise pas (logiciel de facturation payant, entretien des serveurs loués, serveur de base de données supplémentaire). Mets en avant la réactivité de l'hébergement géré : correction en ligne en une à deux minutes, une adresse de test par modification, retour en arrière en un clic.
- **Hébergement** : formules gratuites pendant le développement, puis passage aux formules payantes selon le nombre d'utilisateurs.
- **Déroulement du projet**, pour rassurer : contrat de prestation de service, réalisation étape par étape visible sur l'adresse de test, recette avec procès-verbal, garantie de 3 mois sur les bugs et les petites retouches. Les nouvelles fonctionnalités font l'objet d'un devis à part.
- **Prix** : explique pourquoi il est déjà serré, sans détailler la méthode interne.
- **Relation durable** : si le client la demande, réponds-y explicitement (interlocuteur unique, suivi régulier, engagements écrits).
- **Logos de médias** (« Vu à la TV ») : demande au client de les fournir, il reste responsable de leur utilisation.

## Pendant et après le projet

Les mêmes règles s'appliquent : chaque mail est rangé et découpé en demandes. Une demande hors périmètre devient une évolution « à arbitrer », un défaut sur ce qui est livré devient un bug (couvert par la garantie de 3 mois après le PV de recette, puis payant). Les évolutions s'accumulent dans DEMANDES jusqu'à ce qu'Antoine demande un devis (`fiches/devis.md`).
