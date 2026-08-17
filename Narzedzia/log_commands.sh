#!/usr/bin/env bash
# =============================================================================
# log_commands.sh — zapisuje DOSŁOWNIE KAŻDĄ LINIĘ komend z terminala.
#
# Hook w PROMPT_COMMAND (.bashrc) dopisuje po KAŻDEJ wpisanej komendzie linię:
#
#   2026-08-16T14:45:01Z  host  /katalog  $ komenda
#
# do  Logs/commands_YYYY-MM-DD.log  — surowy, pełny rejestr tego co piszemy.
# (pełny transkrypt z outputem daje log_session.sh → Logs/terminal_*.log)
#
#   log_commands.sh hook      # wypisz snippet do .bashrc
#   log_commands.sh install   # dodaj hook do ~/.bashrc (raz)
#   log_commands.sh status    # czy hook jest aktywny
#   log_commands.sh test      # test zapisu do Logs (bez .bashrc)
#
# Surowe logi są w .gitignore (mogą zawierać hasła/infra) — nie idą na git.
# =============================================================================
set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd 2>/dev/null || echo "$(dirname -- "${BASH_SOURCE[0]}")")"
VAULT="${OBSIDIAN_VAULT:-$(dirname -- "$SCRIPT_DIR")}"
LOG_DIR="$(readlink -f "$VAULT/Logs" 2>/dev/null || echo "$VAULT/Logs")"

# --- rdzeń: dopisz jedną linię komendy -----------------------------------------
log_line() {  # $1 = linia komendy
  local line="$1" ts day f
  [[ -z "$line" ]] && return 0
  line="${line#	}"
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  day="$(date -u +%Y-%m-%d)"
  f="$LOG_DIR/commands_${day}.log"
  mkdir -p "$LOG_DIR" 2>/dev/null || return 1
  { printf '%s  %s  %s  $ %s\n' "$ts" "${HOSTNAME:-?}" "$PWD" "$line"; } >> "$f" 2>/dev/null || return 1
  echo "log: $f"
}

# --- snippet do .bashrc ---------------------------------------------------------
snippet() {
  cat <<EOF
# --- obsidian-log-commands: dosłownie każda linia komend → Logs/commands_*.log ---
if [[ -z "\${OBSIDIAN_LOG_CMD:-}" ]]; then
  export OBSIDIAN_LOG_CMD=1
  _obsidian_log_cmd() {
    local line ts day f
    line="\$(fc -ln -1 2>/dev/null)"
    [[ -z "\$line" ]] && return 0
    line="\${line#	}"
    ts="\$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    day="\$(date -u +%Y-%m-%d)"
    f="$LOG_DIR/commands_\${day}.log"
    mkdir -p "$LOG_DIR" 2>/dev/null
    { printf '%s  %s  %s  \$ %s\n' "\$ts" "\${HOSTNAME:-?}" "\$PWD" "\$line"; } >> "\$f" 2>/dev/null || true
  }
  PROMPT_COMMAND="_obsidian_log_cmd;\${PROMPT_COMMAND:+ \$PROMPT_COMMAND}"
fi
EOF
}

# --- komendy ---------------------------------------------------------------------
case "${1:-hook}" in
  hook)
    snippet
    ;;
  install)
    RC="$HOME/.bashrc"
    if grep -q 'obsidian-log-commands' "$RC" 2>/dev/null; then
      echo "hook już jest w $RC"
    else
      { echo; snippet; } >> "$RC" && echo "✓ dodano hook do $RC — nowe terminale logują każdą komendę"
    fi
    ;;
  status)
    if grep -q 'obsidian-log-commands' "$HOME/.bashrc" 2>/dev/null; then
      echo "hook AKTYWNY w ~/.bashrc (nowe terminale logują)"
    else
      echo "brak hooka — odpal: $(basename "$0") install"
    fi
    ;;
  test)
    log_line "echo 'test log_commands.sh'"
    log_line "ls -la /root"
    log_line "ssh root@5.175.189.133"
    ;;
  *)
    echo "usage: $0 {hook|install|status|test}" >&2
    exit 2
    ;;
esac
