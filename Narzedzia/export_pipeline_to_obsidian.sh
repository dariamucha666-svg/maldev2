#!/usr/bin/env bash
# Compact pipeline → Obsidian export. Safe to call from pipeline.sh / nightly.
set -u
VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
REPORTS_DIR="${REPORTS_DIR:-/root/samples/reports}"
RUN_LOG="${RUN_LOG:-}"
RAPORTY="${OBSIDIAN_RAPORTY:-$VAULT/Analizy/Raporty}"
LOGS="$VAULT/Logs"
PYTHON="${PYTHON:-/root/android-pipeline/.venv/bin/python}"
[[ -x "$PYTHON" ]] || PYTHON="$(command -v python3)"

if [[ ! -d "$VAULT" ]]; then
  echo "obsidian export: no vault at $VAULT" >&2
  exit 0
fi

mkdir -p "$RAPORTY" "$LOGS"
stamp=$(date +%Y-%m-%d_%H-%M)
dest="$RAPORTY/analiza_${stamp}.md"
day=$(date +%Y-%m-%d)
latest_daily="$(ls -1t "$REPORTS_DIR"/daily_summary_*.md 2>/dev/null | head -n 1 || true)"

# Role table from existing JSON (classify should already have run).
role_md="$("$PYTHON" - <<'PY' "$REPORTS_DIR"
import json, sys
from pathlib import Path
from collections import Counter
root = Path(sys.argv[1])
roles = Counter()
rows = []
for path in sorted(root.glob("*.json")):
    name = path.name
    if name.endswith(".features.json") or name in {"iocs.json", "patterns_summary.json"}:
        continue
    if name.startswith("daily_") or name.startswith("DEEP_"):
        continue
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(data, dict):
        continue
    cls = data.get("classification") or {}
    role = cls.get("role") or (data.get("tags") or ["?"])[0] if isinstance(data.get("tags"), list) else cls.get("role") or "?"
    if isinstance(role, list):
        role = role[0] if role else "?"
    roles[str(role)] += 1
    digest = (data.get("hashes") or {}).get("sha256") or path.stem
    fam = cls.get("family") or ""
    src = cls.get("source") or ""
    rows.append((str(digest)[:12], str(role), str(fam)[:40], str(src)[:40]))
print("| role | n |")
print("|------|--:|")
for k, v in sorted(roles.items(), key=lambda kv: (-kv[1], kv[0])):
    print(f"| {k} | {v} |")
print()
print("| hash | role | family | source |")
print("|------|------|--------|--------|")
for digest, role, fam, src in rows[:40]:
    print(f"| `{digest}` | {role} | {fam} | {src} |")
if len(rows) > 40:
    print(f"| … | {len(rows)-40} more | | |")
print("TOTAL", sum(roles.values()), file=sys.stderr)
PY
)"

{
  echo "---"
  echo "title: \"Raport pipeline ${stamp}\""
  echo "date: ${day}"
  echo "tags: [pipeline, raport]"
  echo "source: pipeline"
  echo "---"
  echo
  echo "# Raport z analizy ${stamp}"
  echo
  echo "Źródło: \`$REPORTS_DIR\`"
  echo
  echo "Powiązane: [[Pipeline_Analizy]] · [[Status]] · [[Klasyfikacja_Korpus]] · [[Daily/${day}]]"
  echo
  echo "## Role (JSON po classify_roles.py)"
  echo
  echo "$role_md"
  echo
  if [[ -n "$latest_daily" && -f "$latest_daily" ]]; then
    echo "## Daily summary (ostatni)"
    echo
    echo "Plik: \`${latest_daily}\`"
    echo
    # only first 80 lines — not the entire history dump
    head -n 80 "$latest_daily"
    echo
  fi
  echo
  echo "## Indeks raportów MD"
  echo
  shopt -s nullglob
  n=0
  for f in "$REPORTS_DIR"/*/summary.md "$REPORTS_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    base="${f#"$REPORTS_DIR"/}"
    case "$base" in
      daily_summary_*) continue ;;
    esac
    echo "- \`$base\`"
    n=$((n + 1))
    [[ "$n" -ge 30 ]] && { echo "- …"; break; }
  done
  echo
  if [[ -f "$REPORTS_DIR/sigma_index.json" ]]; then
    echo
    echo "## Sigma"
    echo
    echo "Reguły: \`$REPORTS_DIR/sigma/\` · indeks vault: [[detections/generated]]"
    echo
  fi
  echo "Pełne JSON-y zostają w \`$REPORTS_DIR\` — nie kopiujemy ich w całości do vaultu."
} >"$dest"

# keep only last 8 compact reports in vault
ls -1t "$RAPORTY"/analiza_*.md 2>/dev/null | tail -n +9 | xargs -r rm -f

if [[ -n "$RUN_LOG" && -f "$RUN_LOG" ]]; then
  cp -f "$RUN_LOG" "$LOGS/pipeline_$(date +%Y-%m-%d).log"
fi

echo "obsidian export: $dest"

[ -x /root/obsidian-vault/Narzedzia/build_dashboard_history.py ] && python3 /root/obsidian-vault/Narzedzia/build_dashboard_history.py || true
