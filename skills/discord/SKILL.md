---
name: discord
description: Permet d'envoyer un message dans le canal Discord normal d'un ERP GKFA (jamais dans le canal de logs), depuis n'importe quelle session.
---

# Discord

## But

Publier un message dans le canal Discord normal d'un ERP, via le bot GKFA. Les canaux de logs sont réservés au webhook GitHub : ce skill n'y écrit jamais.

## Dépôts connus

| ERP | Dépôt |
|---|---|
| ERP Ménage | `gkfa-erp-menage` |
| ERP GKFA | `erp-gkfa` |
| ERP Industrie | `erp-industrie` |

## Personnes à mentionner

Pour qu'une mention prévienne quelqu'un, écris `<@identifiant>` dans le message (un simple `@pseudo` ne prévient personne). `@everyone`, `@here` et les rôles ne notifient jamais.

| Personne | Identifiant Discord |
|---|---|
| Filipe (« @ROSA ») | `1471819992965316648` |

Si l'utilisateur veut mentionner quelqu'un d'absent de cette table, demande-lui l'identifiant (mode développeur de Discord, clic droit sur la personne, « Copier l'identifiant ») et ajoute la ligne ici.

## Émojis

Commence le message par un émoji qui correspond à son type, pour le rendre plus vivant. Un seul émoji en tête suffit, ajoutes-en au fil du texte seulement si ça aide à lire (par exemple devant chaque élément d'une liste).

| Type de message | Émoji |
|---|---|
| À faire, TODO | 📝 |
| Terminé, validé | ✅ |
| Bug, problème | 🐛 |
| Urgent, bloquant | 🚨 |
| Mise en ligne, livraison | 🚀 |
| Nouvelle fonctionnalité | ✨ |
| Question | ❓ |
| Information, annonce | 📢 |
| Rappel, réunion, échéance | ⏰ |
| Remerciement, bravo | 🎉 |

Si aucun type ne colle, choisis l'émoji le plus parlant. Si le message commence déjà par un émoji, n'en ajoute pas.

## Étapes

1. Récupère le message demandé. S'il manque, demande-le.
2. Ajoute l'émoji qui correspond au type du message (voir « Émojis »).
3. Remplace chaque personne à mentionner par `<@identifiant>`, grâce à la table ci-dessus.
4. Choisis le dépôt : celui que l'utilisateur nomme, sinon celui du dossier courant s'il est dans la table ci-dessus. Sinon, demande lequel.
5. Envoie avec le script, qui passe par `/api/notify` (canaux normaux uniquement) :

   ```bash
   ~/.claude/scripts/discord-notify.sh "<message>" <dépôt>
   ```

6. Dis en une phrase si c'est parti, ou recopie l'erreur du script.

## Règles

- N'envoie jamais le message par un autre moyen (pas d'appel direct à l'API Discord, pas de `/api/github`).
- Garde le texte du message tel quel : ajoute seulement les émojis et les mentions, sans reformuler, sauf si l'utilisateur te demande de le rédiger.
