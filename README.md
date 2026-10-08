# Plugin Claude Code « antoine »

Les skills d'Antoine Souesme pour travailler sur les ERP GKFA, réunis dans un plugin Claude Code.

## Installation

Dans Claude Code, ajouter la marketplace puis installer le plugin :

```
/plugin marketplace add antoine-souesme/skills
/plugin install antoine@antoine
```

Redémarrer ensuite Claude Code. Les skills s'appellent avec le préfixe `antoine:`, par exemple `/antoine:suivi-github`.

Les mêmes commandes existent hors de Claude Code :

```bash
claude plugin marketplace add antoine-souesme/skills
claude plugin install antoine@antoine
```

## Mise à jour

Une fois les modifications envoyées sur `main`, récupérer la nouvelle version puis redémarrer Claude Code :

```bash
claude plugin marketplace update antoine
claude plugin update antoine@antoine
```

Pensez à augmenter `version` dans `.claude-plugin/plugin.json` à chaque publication : sans changement de version, les postes déjà installés gardent l'ancienne.

## Skills inclus

| Skill | Rôle |
| --- | --- |
| `deploy-production` | Mise en production du projet. |
| `discord` | Envoie un message dans le canal Discord normal d'un ERP GKFA. |
| `handle-dept` | Traite les points de dette mis de côté pendant l'exécution d'un plan. |
| `handoff` | Vérifie qu'un plan peut être repris par un autre agent dans une nouvelle session. |
| `launching-agent-below` | Lance un agent Claude Code dans la pane Herdr du dessous (nécessite `HERDR_ENV=1`). |
| `prepare-for-compact` | Sauvegarde l'état de la session avant une compaction. |
| `spec-to-implementation` | Enchaîne plan, handoff et lancement de l'agent d'exécution à partir d'une spec. |
| `spec-to-plan` | Rédige un plan d'implémentation à partir d'une spec. |
| `suivi-github` | Trie et traite les issues ouvertes du dépôt. |

## Développement

Pour tester une modification sans la publier, lancer Claude Code avec le dossier local :

```bash
claude --plugin-dir /chemin/vers/ce/depot
```

Vérifier le plugin avant de l'envoyer :

```bash
claude plugin validate .
```
