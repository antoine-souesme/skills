#!/usr/bin/env bash
# Lance (ou relance) un Claude Code dans la pane Herdr située sous la pane courante,
# puis lui envoie un prompt sans attendre sa réponse.
#
# Usage: launch-below.sh [--name NOM] [--cwd CHEMIN] "prompt à envoyer"
#        launch-below.sh [--name NOM] [--cwd CHEMIN] --prompt-file CHEMIN
set -uo pipefail

NAME="below"
CWD="$PWD"
PROMPT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --name) NAME="$2"; shift 2 ;;
    --cwd)  CWD="$2";  shift 2 ;;
    --prompt-file)
      [ -r "$2" ] || { printf 'launch-below: fichier prompt illisible: %s\n' "$2" >&2; exit 1; }
      PROMPT=$(cat "$2"); shift 2 ;;
    --) shift; PROMPT="$*"; break ;;
    *) PROMPT="$1"; shift ;;
  esac
done

die() { printf 'launch-below: %s\n' "$1" >&2; exit 1; }
jq_py() { python3 -c "import sys,json
try: d=json.load(sys.stdin)
except Exception: sys.exit(1)
$1"; }

[ "${HERDR_ENV:-}" = "1" ] || die "pas dans une pane Herdr (HERDR_ENV != 1)"
[ -n "$PROMPT" ] || die "prompt manquant"
[ -n "${HERDR_PANE_ID:-}" ] || die "HERDR_PANE_ID absent"

# 1. Pane du dessous : neighbor_pane_id n'existe que s'il y a vraiment un voisin.
TARGET=$(herdr pane neighbor --pane "$HERDR_PANE_ID" --direction down 2>/dev/null \
  | jq_py "print(d['result']['neighbor'].get('neighbor_pane_id',''))")

if [ -z "$TARGET" ]; then
  TARGET=$(herdr pane split --pane "$HERDR_PANE_ID" --direction down --cwd "$CWD" --no-focus 2>&1 \
    | jq_py "print(d['result']['pane']['pane_id'])")
  [ -n "$TARGET" ] || die "échec du split vers le bas"
  sleep 1
  echo "launch-below: pane créée $TARGET"
else
  echo "launch-below: pane existante réutilisée $TARGET"
fi

# 1b. Garde-fou : ne jamais sortir du workspace ni du tab courant.
[ -n "${HERDR_WORKSPACE_ID:-}" ] || die "HERDR_WORKSPACE_ID absent"
[ -n "${HERDR_TAB_ID:-}" ] || die "HERDR_TAB_ID absent"
[ "$TARGET" != "$HERDR_PANE_ID" ] || die "cible = pane appelante, abandon"

read -r T_WS T_TAB <<EOF2
$(herdr pane get "$TARGET" 2>/dev/null | jq_py "p=d['result']['pane']
print(p['workspace_id'], p['tab_id'])")
EOF2
[ -n "$T_WS" ] || die "pane $TARGET introuvable"
[ "$T_WS" = "$HERDR_WORKSPACE_ID" ] || die "$TARGET est dans le workspace $T_WS, pas $HERDR_WORKSPACE_ID : abandon"
[ "$T_TAB" = "$HERDR_TAB_ID" ] || die "$TARGET est dans le tab $T_TAB, pas $HERDR_TAB_ID : abandon"

has_agent() {
  herdr agent list 2>/dev/null \
    | jq_py "print('yes' if '$TARGET' in [a['pane_id'] for a in d['result']['agents']] else 'no')"
}

foreground() {
  herdr pane process-info --pane "$TARGET" 2>/dev/null \
    | jq_py "ps=d['result']['process_info']['foreground_processes']
print(ps[0]['name'] if ps else '')"
}

# 2. Un agent occupe déjà la pane : on le coupe (2x ctrl+c rapprochés, jusqu'à 5 tentatives).
if [ "$(has_agent)" = "yes" ]; then
  echo "launch-below: agent en place, coupure..."
  for _ in 1 2 3 4 5; do
    [ "$(has_agent)" = "no" ] && break
    herdr pane send-keys "$TARGET" ctrl+c >/dev/null 2>&1
    sleep 0.3
    herdr pane send-keys "$TARGET" ctrl+c >/dev/null 2>&1
    sleep 1.5
  done
  [ "$(has_agent)" = "no" ] || die "impossible de couper l'agent de $TARGET, à traiter à la main"
fi

# 3. Un autre processus tient la pane : on ne touche à rien.
FG=$(foreground)
case "$FG" in
  zsh|bash|fish|sh|"") ;;
  *) die "la pane $TARGET exécute '$FG' (pas un agent) : demande à l'utilisateur avant de la réutiliser" ;;
esac

# 4. Nom déjà pris par un agent vivant ailleurs : on suffixe.
TAKEN=$(herdr agent list 2>/dev/null | jq_py "print('yes' if '$NAME' in [a.get('name') for a in d['result']['agents']] else 'no')")
if [ "$TAKEN" = "yes" ]; then
  NAME="$NAME-$(printf '%s' "$TARGET" | tr -c 'a-z0-9' '-' | sed 's/-*$//')"
  echo "launch-below: nom déjà pris, agent renommé '$NAME'"
fi

# 5. Démarrage de l'agent puis envoi du prompt, sans attendre.
herdr agent start "$NAME" --kind claude --pane "$TARGET" >/dev/null 2>&1 \
  || die "herdr agent start a échoué sur $TARGET"
herdr agent prompt "$TARGET" "$PROMPT" >/dev/null 2>&1 \
  || die "prompt non transmis à $TARGET (agent bloqué ?), vérifie avec: herdr agent get $TARGET"

echo "launch-below: agent '$NAME' lancé dans $TARGET, prompt envoyé"
