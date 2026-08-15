#!/usr/bin/env bash
# Copy pipeline markdown into the Obsidian vault. Safe to call from pipeline.sh.
set -u
VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
REPORTS_DIR="${REPORTS_DIR:-/root/samples/reports}"
RUN_LOG="${RUN_LOG:-}"
RAPORTY="${OBSIDIAN_RAPORTY:-$VAULT/Analizy/Raporty}"
LOGS="$VAULT/Logs"

if [[ ! -d "$VAULT" ]]; then
  echo "obsidian export: no vault at $VAULT" >&2
  exit 0
fi

mkdir -p "$RAPORTY" "$LOGS"
stamp=$(date +%Y-%m-%d_%H-%M)
dest="$RAPORTY/analiza_${stamp}.md"
{
  echo "# Raport z analizy $(date -u -Iseconds)"
  echo
  echo "Źródło: \`$REPORTS_DIR\`"
  echo
  echo "## Wyniki"
  echo
  shopt -s nullglob
  files=("$REPORTS_DIR"/daily_summary_*.md "$REPORTS_DIR"/*.md "$REPORTS_DIR"/*/summary.md)
  seen=""
  for f in "${files[@]}"; do
    [[ -f "$f" ]] || continue
    case " $seen " in
      *" $f "*) continue ;;
    esac
    seen+=" $f"
    echo "### ${f#"$REPORTS_DIR"/}"
    echo
    cat "$f"
    echo
    echo "---"
    echo
  done
} >"$dest"

if [[ -n "$RUN_LOG" && -f "$RUN_LOG" ]]; then
  cp -f "$RUN_LOG" "$LOGS/pipeline_$(date +%Y-%m-%d).log"
fi

echo "obsidian export: $dest"

# refresh public dashboard history
[ -x /root/obsidian-vault/Narzedzia/build_dashboard_history.py ] && python3 /root/obsidian-vault/Narzedzia/build_dashboard_history.py || true
