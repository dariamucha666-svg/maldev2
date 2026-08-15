#!/usr/bin/env bash
# Append a lab note to the Obsidian vault (Daily + optional Recap).
# No passwords / tokens / keys in the body.
# Usage:
#   log_to_obsidian.sh "Heading" "body text"
#   log_to_obsidian.sh --recap "Heading" "body"
#   echo body | log_to_obsidian.sh "Heading"
set -u
VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
RECAP=0
if [[ "${1:-}" == "--recap" ]]; then
  RECAP=1
  shift
fi
HEADING="${1:-}"
if [[ -z "$HEADING" ]]; then
  echo "usage: $0 [--recap] \"Heading\" [body]" >&2
  exit 2
fi
shift || true
if [[ -n "${1:-}" ]]; then
  BODY="$*"
else
  BODY="$(cat || true)"
fi
BODY="$(printf '%s' "$BODY" | sed -E \
  -e '/[Pp]assw(or)?d/d' \
  -e '/[Tt]oken/d' \
  -e '/API[_-]?KEY/d' \
  -e '/BEGIN (OPENSSH|RSA|EC) PRIVATE/d')"
DAY="$(date -u +%Y-%m-%d)"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DAILY="$VAULT/Daily/${DAY}.md"
mkdir -p "$VAULT/Daily" "$VAULT/Lab"
if [[ ! -f "$DAILY" ]]; then
  cat > "$DAILY" <<EOF
---
date: ${DAY}
tags: [daily]
---

# ${DAY}

EOF
fi
{
  echo
  echo "## ${HEADING} (${STAMP})"
  echo
  printf '%s\n' "$BODY"
  echo
} >> "$DAILY"
echo "daily += $DAILY"

if [[ "$RECAP" -eq 1 ]]; then
  REC="$VAULT/Lab/Recap ${DAY}.md"
  if [[ ! -f "$REC" ]]; then
    cat > "$REC" <<EOF
---
tags: [recap, lab, session]
date: ${DAY}
---

# Recap — ${DAY}

EOF
  fi
  {
    echo
    echo "## ${HEADING} (${STAMP})"
    echo
    printf '%s\n' "$BODY"
    echo
  } >> "$REC"
  echo "recap += $REC"
fi
