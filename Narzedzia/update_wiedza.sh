#!/usr/bin/env bash
# Aktualizuje bazę Wiedza/ świeżymi danymi z MalwareBazaar.
# Nadpisuje Wiedza/Feed_MalwareBazaar.md i dopisuje wpis do Wiedza/Aktualizacje.md.
# Usage: update_wiedza.sh [limit]
set -euo pipefail

VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
LIMIT="${1:-10}"
API="https://mb-api.abuse.ch/api/v1/"
KEY_FILE="${MB_API_KEY_FILE:-/root/.mb_api_key}"

MB_API_KEY="${MB_API_KEY:-$(tr -d '\n' < "$KEY_FILE" 2>/dev/null || true)}"
if [[ -z "$MB_API_KEY" ]]; then
  echo "Brak klucza MalwareBazaar ($KEY_FILE / MB_API_KEY)." >&2
  exit 1
fi

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

curl -fsS -m 30 -X POST "$API" -H "Auth-Key: ${MB_API_KEY}" \
  -d "query=get_recent&selector=time" -o "$TMP"

export VAULT LIMIT TMP
python3 - "$TMP" "$VAULT" "$LIMIT" <<'PY'
import sys, json, datetime, os

tmp, vault, limit = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = json.load(open(tmp))
if d.get("query_status") != "ok":
    print("MB query_status:", d.get("query_status"), file=sys.stderr)
    sys.exit(1)
data = d.get("data", [])[:limit]
now_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

rows = []
summary = []
for s in data:
    sha = s.get("sha256_hash", "")
    fam = (s.get("signature") or "unknown").strip() or "unknown"
    ftype = s.get("file_type") or "?"
    tags = ",".join(s.get("tags", [])[:5])
    name = (s.get("file_name") or "").strip()
    rows.append(f"| `{sha[:16]}…` | {fam} | {ftype} | {tags} | {name} |")
    summary.append(f"{fam} ({ftype}) `{sha[:12]}…`")

feed = f"""---
title: "Feed — MalwareBazaar recent"
date: {today}
tags: [wiedza, feed, malwarebazaar]
---

# Feed — MalwareBazaar (recent {limit})

Wygenerowano: {now_ts} · źródło: `mb-api.abuse.ch` · skrypt `Narzedzia/update_wiedza.sh`

| SHA256 | Rodzina | Typ | Tagi | Nazwa |
|--------|---------|-----|------|-------|
""" + "\n".join(rows) + "\n"

os.makedirs(f"{vault}/Wiedza", exist_ok=True)
with open(f"{vault}/Wiedza/Feed_MalwareBazaar.md", "w") as f:
    f.write(feed)

# dopisz wpis do Aktualizacje.md (pod sekcją "### Auto")
changelog = f"{vault}/Wiedza/Aktualizacje.md"
entry = f"- `{now_ts}` MalwareBazaar recent: " + "; ".join(summary) + "\n"
if os.path.exists(changelog):
    txt = open(changelog).read()
    marker = "### Auto\n"
    if marker in txt:
        txt = txt.replace(marker, marker + entry, 1)
    else:
        txt = txt.rstrip() + "\n\n### Auto\n" + entry
    open(changelog, "w").write(txt)

print("napisał: Wiedza/Feed_MalwareBazaar.md + wpis w Aktualizacje.md")
PY
