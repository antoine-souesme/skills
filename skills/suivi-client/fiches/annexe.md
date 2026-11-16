# Annexe du devis

Écris `03-devis/ANNEXE_DEVIS.md`, qui fait partie intégrante du devis :

1. **Technologies utilisées** : un tableau rôle / outil. Ne liste que ce qui est vraiment prévu, Antoine retire souvent des outils secondaires (suivi des erreurs, protection anti-robots…). Liste chaque outil de mesure d'audience demandé (Meta Pixel, pixel TikTok…).
2. **Frais à la charge du client, non compris dans le devis** : les abonnements payés directement aux fournisseurs, sans refacturation, avec un coût indicatif.
3. **Hors devis** : rédaction des contenus, campagnes publicitaires (Google Ads), données à fournir par le client (catégories, textes), toute fonctionnalité qui n'est pas prévue au devis. Écris « pas prévue au devis n°X », jamais « pas prévue au cahier des charges » : le cahier des charges ne doit pas élargir le périmètre.

Le titre reprend le numéro du devis (« Annexe au devis n°X ») et la date d'émission. Ce qui est offert en plus du devis (par exemple l'ouverture des comptes de réseaux sociaux) est écrit en tête de la partie hors devis.

## Comptes des services

Façon de faire habituelle d'Antoine, à rappeler dans l'annexe :

- Il crée tous les comptes (hébergement, base de données, e-mails, réseaux sociaux, mesure d'audience) avec une adresse e-mail dédiée au projet, qui appartient au client. Tous les accès sont remis au client au paiement complet.
- Le compte Stripe est créé de la même façon, puis le client y est invité comme administrateur et l'active lui-même avec ses informations (identité, SIRET, IBAN), à l'aide d'un mode d'emploi.
- Ne parle pas au client de changer ses mots de passe.

Repères sur les comptes : le Meta Pixel se crée dans le compte professionnel Meta qui gère les pages Facebook et Instagram, et une page Facebook doit être gérée par un vrai profil ; le pixel TikTok demande un compte publicitaire TikTok, distinct de la page ; Google Tag Manager et Analytics demandent un compte Google ; Tarteaucitron n'en demande aucun. Le Gmail dédié demande un numéro de téléphone de récupération : celui du client.

## PDF

```bash
python <dossier du skill>/scripts/annexe_pdf.py 03-devis/ANNEXE_DEVIS.md 03-devis/Annexe_Devis_<Projet>.pdf \
  --client "NOM Prénom" --adresse "Adresse du client" --pied "Annexe au devis n°X · <Projet>"
```

Le script demande reportlab. Si le Python du système est trop ancien, crée un environnement virtuel dans le dossier temporaire de la session et installe `reportlab==4.2.5`.

Rappelle à Antoine d'ajouter dans son devis : « Annexe jointe : <contenu>. Elle fait partie intégrante du devis. » Après chaque modification de l'annexe, regénère le PDF, mets la date du jour, vérifie que la mention du devis correspond toujours, et note dans ETAT que la nouvelle version est à envoyer. Une annexe modifiée après envoi doit être renvoyée avec une phrase qui dit qu'elle remplace la précédente.
