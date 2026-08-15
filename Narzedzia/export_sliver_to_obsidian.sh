#!/usr/bin/env bash
# Dump Sliver sessions/beacons/jobs into the vault.
# There is no `sessions --save` in Sliver — --save belongs to `generate`.
# This script talks to the local sliver-server (operator cfg) and SQLite.
# Does not generate implants, does not task sessions, does not dump credentials.
set -u
VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
OUT="${SLIVER_SESSIONS_MD:-$VAULT/Projekty/Infrastruktura_C2/sessions.md}"
CLIENT="${SLIVER_CLIENT:-/opt/tools/bin/sliver-client}"
DB="${SLIVER_DB:-/root/.sliver/sliver.db}"
TIMEOUT_SEC="${SLIVER_EXPORT_TIMEOUT:-25}"

mkdir -p "$(dirname "$OUT")"
stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
tmp=$(mktemp)
rc=$(mktemp)
trap 'rm -f "$tmp" "$rc"' EXIT

{
  echo "sessions"
  echo "beacons"
  echo "jobs"
  echo "exit"
} >"$rc"

if [[ -x "$CLIENT" ]]; then
  timeout "$TIMEOUT_SEC" "$CLIENT" --rc "$rc" >"$tmp" 2>&1 || true
  # drop ANSI / spinner leftovers
  sed -i -e 's/\x1b\[[0-9;?]*[a-zA-Z]//g' -e 's/\r//g' "$tmp" || true
else
  echo "(brak $CLIENT)" >"$tmp"
fi

{
  echo "---"
  echo "title: \"Sliver sessions\""
  echo "date: ${stamp:0:10}"
  echo "updated: $stamp"
  echo "tags: [sliver, c2, sessions, auto]"
  echo "status: active"
  echo "category: infra"
  echo "---"
  echo
  echo "# Sliver — sesje i beacon'y"
  echo
  echo "Wygenerowane: \`$stamp\` (auto, nie ręcznie z konsoli)."
  echo
  echo "Sliver **nie ma** \`sessions --save\`. Eksport: \`Narzedzia/export_sliver_to_obsidian.sh\`."
  echo
  echo "## Konsola (\`sessions\` / \`beacons\` / \`jobs\`)"
  echo
  echo '```'
  # keep the useful tail; drop the connecting banner noise if huge
  tail -n 200 "$tmp"
  echo '```'
  echo

  if command -v sqlite3 >/dev/null && [[ -f "$DB" ]]; then
    echo "## Beacon'y (SQLite, bez sekretów)"
    echo
    echo "| name | hostname | os | arch | transport | last_checkin |"
    echo "|------|----------|----|------|-----------|--------------|"
    sqlite3 -cmd ".timeout 2000" "$DB" \
      "SELECT printf('| %s | %s | %s | %s | %s | %s |',
        COALESCE(name,''), COALESCE(hostname,''), COALESCE(os,''),
        COALESCE(arch,''), COALESCE(transport,''), COALESCE(last_checkin,''))
       FROM beacons ORDER BY last_checkin DESC;" 2>/dev/null \
      || echo "| — | — | — | — | — | (db locked / empty) |"
    echo
    echo "## Hosty (SQLite)"
    echo
    echo "| hostname | os_version | locale | created_at |"
    echo "|----------|------------|--------|------------|"
    sqlite3 -cmd ".timeout 2000" "$DB" \
      "SELECT printf('| %s | %s | %s | %s |',
        COALESCE(hostname,''), COALESCE(os_version,''),
        COALESCE(locale,''), COALESCE(created_at,''))
       FROM hosts ORDER BY created_at DESC;" 2>/dev/null \
      || echo "| — | — | — | (db locked / empty) |"
    echo
    echo "## Listener jobs"
    echo
    echo "| job_id | type | created_at |"
    echo "|--------|------|------------|"
    sqlite3 -cmd ".timeout 2000" "$DB" \
      "SELECT printf('| %s | %s | %s |',
        COALESCE(job_id,''), COALESCE(type,''), COALESCE(created_at,''))
       FROM listener_jobs ORDER BY created_at DESC;" 2>/dev/null \
      || echo "| — | — | (db locked / empty) |"
    echo
  fi

  echo "Nie eksportujemy: \`credentials\`, kluczy implantu, \`audit.json\`."
} >"$OUT"

echo "sliver export: $OUT"
