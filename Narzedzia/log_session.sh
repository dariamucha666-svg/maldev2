#!/usr/bin/env bash
# =============================================================================
# log_session.sh — nagrywa CAŁĄ sesję terminala do Logs/ i dopisuje start/stop
# do dziennika Obsidian. Wpis z Daily: co robiliśmy w tej sesji.
#
#   log_session.sh start [etykieta]   # uruchom; po wyjściu (exit / Ctrl-D)
#                                     # dopisze podsumowanie do Daily
#   log_session.sh status             # czy coś nagrywa
#   log_session.sh hook               # wypisz snippet do .bashrc
#                                     # (auto-nagrywanie KAŻDEGO terminala)
#
# Nagranie:  Logs/terminal_YYYY-MM-DD.log  (script -aqf, append)
# Guard:     UNDER_OBSIDIAN_SCRIPT=1 zapobiega rekurencji.
# =============================================================================
set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd 2>/dev/null || echo "$(dirname -- "${BASH_SOURCE[0]}")")"
VAULT="${OBSIDIAN_VAULT:-$(dirname -- "$SCRIPT_DIR")}"
LOGDIR="$VAULT/Logs"
STATE="$LOGDIR/.session"

CMD="${1:-status}"; shift || true

# ---------------------------------------------------------------------------
hook() {
  cat <<'EOF'
# --- auto-log Obsidian: nagrywaj każdy terminal (na końcu .bashrc) ---
if [[ $- == *i* ]] && [[ -t 0 ]] && [[ -z "${UNDER_OBSIDIAN_SCRIPT:-}" ]]; then
  export UNDER_OBSIDIAN_SCRIPT=1
  exec script -aqf "$HOME/Obsidian/XMask/maldev2/Logs/terminal_$(date -u +%F).log"
fi
EOF
}

status() {
  if [[ -f "$STATE" ]]; then
    . "$STATE" 2>/dev/null
    if kill -0 "${SES_PID:-0}" 2>/dev/null; then
      echo "nagrywam: pid ${SES_PID} → ${SES_LOG}${SES_LABEL:+  (${SES_LABEL})}"
      return 0
    fi
    echo "osierocony stan ($STATE) — usuwam"; rm -f "$STATE"
  fi
  echo "nic nie nagrywa"
}

start() {
  local DAY LOG LABEL
  DAY="$(date -u +%Y-%m-%d)"
  LOG="$LOGDIR/terminal_${DAY}.log"
  LABEL="${1:-}"
  mkdir -p "$LOGDIR"

  # jeśli już nagrywamy (np. inny terminal) — nie startuj drugi raz
  if [[ -f "$STATE" ]]; then
    . "$STATE" 2>/dev/null
    if kill -0 "${SES_PID:-0}" 2>/dev/null; then
      echo "już nagrywam (pid ${SES_PID}) — ta sesja NIE będzie zapisana." >&2
      echo "Najpierw: log_session.sh status / zakończ tamtą sesję." >&2
      return 1
    fi
    rm -f "$STATE"
  fi

  printf 'SES_PID=%s\nSES_LOG=%s\nSES_LABEL=%s\nSES_START=%s\n' \
    "$$" "$LOG" "$LABEL" "$(date -u +%s)" > "$STATE"

  "${SCRIPT_DIR}/log_to_obsidian.sh" \
    "Sesja terminalowa — start${LABEL:+ (${LABEL})}" \
    "Nagrywanie: \`$LOG\`. Komendy tej sesji trafią do \`Logs/terminal_*.log\` i tego dziennika."

  echo "→ nagrywam całą sesję do: $LOG"
  echo "  (pracuj normalnie; na koniec wpisz  exit  lub Ctrl-D)"
  echo

  script -aqf "$LOG"

  local CODE=$?
  rm -f "$STATE"

  if [[ ! -f "$LOG" ]]; then
    echo "⚠ script nie utworzył logu (środowisko może blokować pty, np. sandbox)." >&2
    echo "  Na normalnym terminalu / Kali to działa — sprawdź: command -v script" >&2
    return "$CODE"
  fi

  local LINES SIZE
  LINES="$(wc -l < "$LOG" 2>/dev/null || echo 0)"
  SIZE="$(du -h "$LOG" 2>/dev/null | cut -f1)"

  "${SCRIPT_DIR}/log_to_obsidian.sh" \
    "Sesja terminalowa — stop${LABEL:+ (${LABEL})}" \
    "Koniec sesji (exit $CODE). Log: \`$LOG\` · linie: $LINES · rozmiar: $SIZE"

  echo "✓ sesja zapisana: $LOG (linie: $LINES, rozmiar: $SIZE)"
  return $CODE
}

case "$CMD" in
  start)  start "${1:-}" ;;
  status) status ;;
  hook)   hook ;;
  *) echo "usage: $0 {start [etykieta]|status|hook}" >&2; exit 2 ;;
esac
