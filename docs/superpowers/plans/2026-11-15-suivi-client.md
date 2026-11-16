# Skill suivi-client : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Exécuté dans la session QuiPeutMaider, qui a la conversation en mémoire.

**Goal:** remplacer `avant-vente` par `/antoine:suivi-client`, un assistant de suivi de la relation client avec mémoire dans `_assistant/`, et migrer QuiPeutMaider.

**Architecture:** un `SKILL.md` court (rôle, règles, suivi, démarrage) qui renvoie vers des fiches par tâche dans `fiches/`, des modèles dans `modeles/`, le script PDF existant.

**Tech Stack:** markdown, plugin Claude Code, Python reportlab pour les PDF.

**Spec:** `docs/superpowers/specs/2026-11-15-suivi-client-design.md`

## Global Constraints

- Commande `/antoine:suivi-client`, dossier `skills/suivi-client/`
- `SKILL.md` sous ~150 lignes
- Dossier client `<projet>-suivi-client/`, suivi dans `_assistant/` (ETAT.md, DEMANDES.md, JOURNAL.md)
- Mails : `04-echanges-client/AAAA-MM-JJ_recu_<sujet>.md`, `_envoye_`, `_brouillon_`
- Statuts DEMANDES : nouvelle, à arbitrer, incluse, offerte, chiffrée, acceptée, livrée, refusée, répondue ; numéros D-n jamais réutilisés
- Côté client : pas de tiret cadratin, pas de ponctuation en fin de puce, pas de vocabulaire interne
- Aucun commit sans accord d'Antoine ; version 1.3.0

## Review Focus

- Nouvelle session dans le dossier migré : l'assistant doit annoncer l'état exact (contrat prêt, points de relecture en réflexion) sans reposer de question tranchée. Vérifié à la tâche 4 en relisant ETAT comme une session neuve.
- Dossier sans `_assistant/` : proposition d'initialisation, pas d'erreur. Écrit dans SKILL.md (tâche 1).
- Mail contenant une demande déjà couverte par le cadrage : statut « incluse », pas « à arbitrer ». Écrit dans fiches/mails.md (tâche 2).
- Devis d'évolutions : ne prendre que les demandes au statut adapté (à arbitrer, acceptée non chiffrée), jamais les livrées. Écrit dans fiches/devis.md (tâche 2).
- Relecture neuve : constats vérifiés contre le PDF réellement envoyé, pas le brouillon. Écrit dans fiches/relecture.md (tâche 2).

---

### Task 1 : squelette du skill

**Files:**
- Create: `skills/suivi-client/SKILL.md`, `skills/suivi-client/modeles/ETAT.md`, `DEMANDES.md`, `JOURNAL.md`
- Move: `skills/avant-vente/scripts/annexe_pdf.py` → `skills/suivi-client/scripts/`, `skills/avant-vente/modeles/CONTRAT_PRESTATION.md` → `skills/suivi-client/modeles/`
- Delete: `skills/avant-vente/`

- [ ] Écrire SKILL.md : frontmatter (name suivi-client, description), rôle, règles générales (reprises d'avant-vente), arborescence du dossier client, démarrage (initialisation ou lecture du suivi + résumé en trois lignes), mise à jour du suivi après chaque action, table des fiches.
- [ ] Écrire les trois modèles avec leurs sections et l'en-tête du tableau DEMANDES.
- [ ] Vérifier : `wc -l skills/suivi-client/SKILL.md` < 150.

### Task 2 : fiches

**Files:** Create `skills/suivi-client/fiches/` : `cadrage.md`, `devis.md`, `annexe.md`, `mails.md`, `maquettes.md`, `contrat.md`, `facturation.md`, `relecture.md`, `passage-au-projet.md`

- [ ] Reprendre le fond d'avant-vente (étapes 1 à 10) dans les fiches correspondantes, chemins sans `docs/cadrage/`.
- [ ] Ajouter : traitement d'un mail (fiche mails), devis d'évolutions depuis DEMANDES (fiche devis), relecture neuve avec prompt (fiche relecture), passage au projet (docs/suivi, DEMARRAGE sans vente, renommage et lien d'historique), Stripe sur invitation, signature électronique, cohérence avec le PDF réellement envoyé (fiche contrat).
- [ ] Vérifier : `grep -rn "docs/cadrage\|avant-vente" skills/suivi-client` ne renvoie rien.

### Task 3 : modèle de contrat et plugin

**Files:** Modify `skills/suivi-client/modeles/CONTRAT_PRESTATION.md`, `README.md`, `.claude-plugin/plugin.json`

- [ ] Régénérer le modèle depuis la version finale du contrat QuiPeutMaider, valeurs client remplacées par des `<...>`.
- [ ] README : ligne suivi-client à la place d'avant-vente. plugin.json : 1.3.0.
- [ ] Vérifier : `grep -n "QuiPeut\|GOUROD\|4 750" modeles/CONTRAT_PRESTATION.md` vide ; `claude plugin validate .` passe ; le script génère un PDF depuis le modèle.

### Task 4 : migration QuiPeutMaider

**Files:** dans `~/dev/projets/quipeutmaider-avant-vente/` : créer `_assistant/` (ETAT, DEMANDES, JOURNAL), `07-facturation/`, renommer les mails, ajouter les mails du client.

- [ ] Renommer les mails : `2026-11-12_envoye_reponse-technique.md`, `2026-11-12_envoye_accord-prix.md`, `2026-11-13_envoye_precisions.md`, `2026-11-15_brouillon_envoi-contrat.md`.
- [ ] Ajouter les mails du client collés en séance (texte intégral) : proposition 4 750 € (12/11), précisions et exemples (13/11), précision consentements et pubs (13/11).
- [ ] Remplir JOURNAL, DEMANDES, ETAT depuis la conversation.
- [ ] Vérifier en lisant ETAT comme une session neuve : étape actuelle, documents en vigueur, attentes, prochaines actions sont exacts.

### Task 5 : renommage du dossier et validation

- [ ] Renommer `quipeutmaider-avant-vente` en `quipeutmaider-suivi-client`, lien d'historique `~/.claude/projects/-Users-antoinesouesme-dev-projets-quipeutmaider-suivi-client` vers le dossier d'historique réel.
- [ ] Vérifier : `ls` du nouveau dossier, `ls -la` du lien.
