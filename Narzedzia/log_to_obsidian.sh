#!/usr/bin/env bash
# =============================================================================
# log_to_obsidian.sh — dopisuje wpis do dziennika Obsidian (Daily [+ Recap]).
#
# Zapisuje "wszystko co robimy": każda komenda / skrypt / agent / sesja woła ten
# hook i wpis ląduje w Daily/YYYY-MM-DD.md (a z --recap też w recapie dnia).
#
#   * SAM wykrywa katalog vaultu: skrypt mieszka w <vault>/Narzedzia/,
#     więc działa na każdym komputerze (nadpisz przez env OBSIDIAN_VAULT)
#   * tworzy Daily/YYYY-MM-DD.md, gdy nie istnieje (frontmatter + nagłówek
#     jak w szablonie Dziennik_Lab)
#   * dedupe: identyczny nagłówek + treść już w dzienniku → skip (--force omija)
#   * atomowy zapis pod flockiem — bezpieczne, gdy DSH / Goose / Grok / cron
#     piszą jednocześnie
#   * czyści wpisy z sekretów (hasła / tokeny / klucze API) — polityka vaultu
#   * --tag dopisuje tagi do frontmatteru dnia
#   * --commit robi dodatkowo git commit (jeśli vault siedzi w repo)
#
# Użycie:
#   log_to_obsidian.sh "Nagłówek" "treść..."
#   echo "treść" | log_to_obsidian.sh "Nagłówek"
#   log_to_obsidian.sh --recap "Nagłówek" "treść"
#   log_to_obsidian.sh --tag "lab,redteam" "Nagłówek" "treść"
#   log_to_obsidian.sh --force "Nagłówek" "treść"
#   log_to_obsidian.sh --commit "Nagłówek" "treść"
# =============================================================================
set -u

# --- lokalizacja vaultu --------------------------------------------------------
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd 2>/dev/null || echo "$(dirname -- "${BASH_SOURCE[0]}")")"
VAULT="${OBSIDIAN_VAULT:-$(dirname -- "$SCRIPT_DIR")}"

# --- opcje ----------------------------------------------------------------------
RECAP=0; TAGS=""; FORCE=0; COMMIT=0
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --recap)  RECAP=1; shift ;;
    --tag)    TAGS="${2:-}"; shift 2 ;;
    --force)  FORCE=1; shift ;;
    --commit) COMMIT=1; shift ;;
    --help|-h)
      sed -n '2,45s/^# \{0,1\}//p' "$0"
      exit 0 ;;
    *) echo "nieznana opcja: $1 (--help)" >&2; exit 2 ;;
  esac
done

HEADING="${1:-}"
if [[ -z "$HEADING" ]]; then
  echo "usage: $0 [--recap] [--tag t] [--force] [--commit] \"Nagłówek\" [treść]" >&2
  exit 2
fi
shift || true
if [[ -n "${1:-}" ]]; then
  BODY="$*"
else
  BODY="$(cat 2>/dev/null || true)"
fi

# --- redakcja sekretów -----------------------------------------------------------
BODY="$(printf '%s\n' "$BODY" | sed -E \
  -e '/[Pp]assw(or)?d/d' \
  -e '/[Hh]asl[oa]/d' \
  -e '/[Tt]oken/d' \
  -e '/API[_-]?KEY/d' \
  -e '/BEGIN (OPENSSH|RSA|EC|DSA|PGP) PRIVATE KEY/d' \
  -e '/sk-[A-Za-z0-9]{20,}/d' \
  -e '/xox[baprs]-[A-Za-z0-9-]+/d' \
  -e '/AKIA[0-9A-Z]{16}/d' \
  -e '/Bearer [A-Za-z0-9._~+/-]+=*/d' \
)"

# --- ścieżki / znaczniki czasu (UTC, jak reszta vaultu) ----------------------------
DAY="$(date -u +%Y-%m-%d)"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DAILY="$VAULT/Daily/${DAY}.md"

# --- utwórz dziennik dnia, gdy nie istnieje ----------------------------------------
if [[ ! -f "$DAILY" ]]; then
  if [[ -n "$TAGS" ]]; then T="[daily, ${TAGS}]"; else T="[daily]"; fi
  mkdir -p "$VAULT/Daily"
  cat > "$DAILY" <<EOF
---
date: ${DAY}
tags: ${T}
---

# ${DAY}

EOF
  echo "daily: utworzono $DAILY"
elif [[ -n "$TAGS" ]]; then
  # dopisz tagi do istniejącego frontmatteru (pierwsza linia 'tags:')
  awk -v add="$TAGS" '
    /^tags:/ && !done {
      line=$0
      sub(/^tags:[[:space:]]*\[?/, "", line)
      sub(/\]?[[:space:]]*$/, "", line)
      n=split(line, a, /[,[:space:]]+/)
      m=split(add, b, /[,[:space:]]+/)
      out=""
      for (j=1; j<=m; j++)
        if (b[j] != "" && !seen[b[j]]) { seen[b[j]]=1; out=(out=="" ? b[j] : out ", " b[j]) }
      for (i=1; i<=n; i++)
        if (a[i] != "" && !seen[a[i]]) { seen[a[i]]=1; out=(out=="" ? a[i] : out ", " a[i]) }
      print "tags: [" out "]"
      done=1; next
    }
    { print }
  ' "$DAILY" > "$DAILY.tmp" && mv "$DAILY.tmp" "$DAILY"
fi

# --- dedupe: ten sam nagłówek + ta sama treść już były → skip ------------------------
dup=0
if [[ "$FORCE" -eq 0 ]] && [[ -f "$DAILY" ]]; then
  if grep -qF -- "## ${HEADING} (" "$DAILY" 2>/dev/null && grep -qF -- "$BODY" "$DAILY" 2>/dev/null; then
    dup=1
  fi
fi

append_block() {  # $1 = plik
  { echo; echo "## ${HEADING} (${STAMP})"; echo; printf '%s\n' "$BODY"; echo; } >> "$1"
}

if [[ "$dup" -eq 1 ]]; then
  echo "daily: POMINIĘTO duplikat „${HEADING}” ($DAILY)"
else
  if command -v flock >/dev/null 2>&1; then
    mkdir -p "$VAULT/.logs"
    exec 9>>"$VAULT/.logs/log.lock"
    flock 9
    append_block "$DAILY"
    flock -u 9
    exec 9>&-
  else
    append_block "$DAILY"
  fi
  echo "daily += $DAILY  (## ${HEADING})"
fi

# --- recap dnia (opcjonalnie) --------------------------------------------------------
if [[ "$RECAP" -eq 1 ]]; then
  # konwencja tego vaultu: Recap_YYYY-MM-DD.md w katalogu głównym;
  # na .133 (gdzie nie ma takiego pliku, a jest Lab/) — Lab/Recap YYYY-MM-DD.md
  if [[ -f "$VAULT/Recap_${DAY}.md" ]]; then
    REC="$VAULT/Recap_${DAY}.md"
  elif [[ -d "$VAULT/Lab" ]]; then
    REC="$VAULT/Lab/Recap ${DAY}.md"
  else
    REC="$VAULT/Recap_${DAY}.md"
  fi
  if [[ ! -f "$REC" ]]; then
    cat > "$REC" <<EOF
---
tags: [recap, lab, session]
date: ${DAY}
---

# Recap — ${DAY}

EOF
    echo "recap: utworzono $REC"
  fi
  rdup=0
  if [[ "$FORCE" -eq 0 ]] && grep -qF -- "## ${HEADING} (" "$REC" 2>/dev/null && grep -qF -- "$BODY" "$REC" 2>/dev/null; then
    rdup=1
  fi
  if [[ "$rdup" -eq 1 ]]; then
    echo "recap: POMINIĘTO duplikat „${HEADING}” ($REC)"
  else
    if command -v flock >/dev/null 2>&1; then
      mkdir -p "$VAULT/.logs"
      exec 8>>"$VAULT/.logs/log.lock"
      flock 8
      append_block "$REC"
      flock -u 8
      exec 8>&-
    else
      append_block "$REC"
    fi
    echo "recap += $REC  (## ${HEADING})"
  fi
fi

# --- opcjonalny git commit ------------------------------------------------------------
if [[ "$COMMIT" -eq 1 ]]; then
  GITROOT="$(git -C "$VAULT" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$GITROOT" ]]; then
    git -C "$GITROOT" add -A -- "$VAULT" >/dev/null 2>&1
    if git -C "$GITROOT" commit -q -m "log($(date -u +%F)): ${HEADING}" >/dev/null 2>&1; then
      echo "git: commit OK"
    else
      echo "git: brak zmian do commita"
    fi
  else
    echo "git: brak repo, pomijam commit" >&2
  fi
fi
