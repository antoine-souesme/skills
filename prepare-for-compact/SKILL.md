---
name: prepare-for-compact
description: Capture l'état durable de la session pour qu'aucun travail en cours ne soit perdu à la compaction => mémoire, ledger, git, prochaine action.
disable-model-invocation: true
---

# Prepare for compact

But : rendre la compaction sans risque. Après un `/compact`, seuls survivent (a) le résumé de compaction, (b) les fichiers durables (mémoire, ledger, git, docs). Tout ce qui n'est écrit nulle part est perdu. Ce skill écrit l'état durable AVANT la compaction.

Ne demande pas de confirmation pour écrire ces fichiers : les écrire est le but. Reste bref dans le chat — le contenu va dans les fichiers.

## Checklist (créer une todo par item)

1. **Recenser l'état volatil** — ce qui n'existe que dans le contexte actuel :
   - branche git courante + `git log --oneline -1` (HEAD), changements non commités (`git status --short`), background tasks en cours, PR ouvertes en attente de merge.
   - la tâche en cours et **la prochaine action exacte** (pas « continuer » : le fichier à toucher, la commande à lancer, le bloc à exécuter).
   - décisions/contraintes de l'utilisateur prises cette session qui ne sont pas déjà dans le code/CLAUDE.md.
   - gotchas rencontrés (faux positifs, pièges de build, chemins d'outillage dans le scratchpad).

2. **Écrire dans le ledger de travail s'il en existe un** — si un ledger de session existe (ex `.superpowers/sdd/progress.md`, ou tout fichier de suivi que tu tiens), y ajouter un bloc `=== RESUME <sujet> (post-compaction) ===` contenant : état (fait / en attente / restant), prochaine action exacte, décisions constantes, outillage (chemins scratchpad), gotchas. Convertir les dates relatives en absolues.

3. **Mettre à jour la mémoire** (`.../memory/`) — si un fichier mémoire couvre le travail en cours, le rafraîchir (statut des PR/blocs, HEAD, ce qui reste). Sinon, si le travail est un projet en cours qui survivra à plusieurs sessions, en créer un (type `project`) + une ligne dans `MEMORY.md`. Ne pas dupliquer ce que le repo/git enregistre déjà.

4. **Ne rien laisser en l'air côté git** — si des changements significatifs ne sont pas commités et que l'utilisateur committe normalement à ce stade du workflow, les committer (sur une branche, jamais sur la branche par défaut sans accord) ; sinon noter dans le ledger qu'il y a des changements non commités et lesquels. Ne jamais `git clean`/reset qui détruirait le ledger (souvent git-ignored).

5. **Confirmer** — une ligne à l'utilisateur : où est l'état de reprise (ledger + mémoire), la prochaine action, et que la compaction est sans risque. Rappeler qu'après compaction il suffit de lire le bloc RESUME du ledger.

## Principes

- Écrire l'état durable, pas un roman : la prochaine action doit être exécutable sans le contexte perdu.
- La source de vérité de reprise = le ledger + la mémoire, pas le résumé de compaction (qui peut omettre des détails).
- Après compaction, faire confiance au ledger et à `git log` plutôt qu'à un souvenir.
- Si aucun travail volatil n'est en cours (conversation triviale), le dire et ne rien écrire.
