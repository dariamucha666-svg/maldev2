#!/usr/bin/env bash
# Aktualizuje bazę Wiedza/ świeżymi danymi z trzech źródeł:
#   1. MalwareBazaar — najnowsze próbki (klucz abuse.ch)
#   2. CISA KEV        — luki aktualnie eksploatowane (bez klucza)
#   3. ThreatFox       — świeże IoC (ten sam klucz abuse.ch)
# Nadpisuje Wiedza/Feed_*.md i dopisuje jeden wpis do Wiedza/Aktualizacje.md.
# Usage: update_wiedza.sh [limit_próbek] [limit_cve] [limit_ioc]
set -euo pipefail

VAULT="${OBSIDIAN_VAULT:-/root/obsidian-vault}"
MB_LIMIT="${1:-10}"
KEV_LIMIT="${2:-10}"
TF_LIMIT="${3:-10}"

MB_API="https://mb-api.abuse.ch/api/v1/"
TF_API="https://threatfox-api.abuse.ch/api/v1/"
KEV_URL="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
KEY_FILE="${MB_API_KEY_FILE:-/root/.mb_api_key}"

ABUSE_KEY="${MB_API_KEY:-$(tr -d '\n' < "$KEY_FILE" 2>/dev/null || true)}"
if [[ -z "$ABUSE_KEY" ]]; then
  echo "Brak klucza abuse.ch ($KEY_FILE / MB_API_KEY)." >&2
  exit 1
fi

TMP_MB="$(mktemp)"; TMP_KEV="$(mktemp)"; TMP_TF="$(mktemp)"
trap 'rm -f "$TMP_MB" "$TMP_KEV" "$TMP_TF"' EXIT

# 1. MalwareBazaar (recent samples)
curl -fsS -m 30 -X POST "$MB_API" -H "Auth-Key: ${ABUSE_KEY}" \
  -d "query=get_recent&selector=time" -o "$TMP_MB" || echo "{}" > "$TMP_MB"

# 2. CISA KEV (bez klucza)
curl -fsS -m 30 "$KEV_URL" -o "$TMP_KEV" || echo "{}" > "$TMP_KEV"

# 3. ThreatFox (IoC z ostatnich 24h)
curl -fsS -m 30 -X POST "$TF_API" -H "Auth-Key: ${ABUSE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"get_iocs","days":1}' -o "$TMP_TF" || echo "{}" > "$TMP_TF"

export VAULT MB_LIMIT KEV_LIMIT TF_LIMIT TMP_MB TMP_KEV TMP_TF
python3 <<'PY'
import sys, json, datetime, os

vault = os.environ["VAULT"]
mb_limit = int(os.environ["MB_LIMIT"])
kev_limit = int(os.environ["KEV_LIMIT"])
tf_limit = int(os.environ["TF_LIMIT"])

def now():
    return datetime.datetime.now(datetime.timezone.utc)
ts = now().strftime("%Y-%m-%d %H:%M:%S UTC")
today = now().strftime("%Y-%m-%d")

os.makedirs(f"{vault}/Wiedza", exist_ok=True)
summary = []

# ---- MalwareBazaar ----
try:
    d = json.load(open(os.environ["TMP_MB"]))
    data = (d.get("data") or [])[:mb_limit] if d.get("query_status") == "ok" else []
except Exception:
    data = []
rows = []
for s in data:
    sha = s.get("sha256_hash", "")
    fam = (s.get("signature") or "unknown").strip() or "unknown"
    ftype = s.get("file_type") or "?"
    tags = ",".join(s.get("tags", [])[:5])
    name = (s.get("file_name") or "").strip()
    rows.append(f"| `{sha[:16]}…` | {fam} | {ftype} | {tags} | {name} |")
    summary.append(f"{fam} ({ftype})")
feed = f"""---
title: "Feed — MalwareBazaar recent"
date: {today}
tags: [wiedza, feed, malwarebazaar]
---

# Feed — MalwareBazaar (recent {mb_limit})

Wygenerowano: {ts} · źródło: `mb-api.abuse.ch` · skrypt `Narzedzia/update_wiedza.sh`

| SHA256 | Rodzina | Typ | Tagi | Nazwa |
|--------|---------|-----|------|-------|
""" + ("\n".join(rows) if rows else "| *(brak danych)* |") + "\n"
open(f"{vault}/Wiedza/Feed_MalwareBazaar.md", "w").write(feed)
mb_count = len(rows)

# ---- CISA KEV ----
try:
    d = json.load(open(os.environ["TMP_KEV"]))
    vulns = (d.get("vulnerabilities") or [])[:kev_limit]
except Exception:
    vulns = []
rows = []
for v in vulns:
    cve = v.get("cveID", "")
    vendor = (v.get("vendorProject") or "")[:28]
    product = (v.get("product") or "")[:28]
    added = v.get("dateAdded", "")
    rw = v.get("knownRansomwareCampaignUse", "") or ""
    act = (v.get("requiredAction") or "")[:60]
    rows.append(f"| {cve} | {vendor} | {product} | {added} | {rw} | {act} |")
    summary.append(f"{cve} {vendor}")
feed = f"""---
title: "Feed — CISA KEV"
date: {today}
tags: [wiedza, feed, cisa, kev, cve]
---

# Feed — CISA KEV (Known Exploited Vulnerabilities, {kev_limit} najnowszych)

Wygenerowano: {ts} · źródło: `cisa.gov/known-exploited-vulnerabilities-catalog.json` · skrypt `Narzedzia/update_wiedza.sh`

Luki **aktywnie eksploatowane** — patch najpierw te (patrz [[Obrona/Obrona_MOC]]).

| CVE | Vendor | Produkt | Dodano | Ransomware | Wymagane działanie |
|-----|--------|---------|--------|------------|--------------------|
""" + ("\n".join(rows) if rows else "| *(brak danych)* |") + "\n"
open(f"{vault}/Wiedza/Feed_CISA_KEV.md", "w").write(feed)
kev_count = len(rows)

# ---- ThreatFox ----
try:
    d = json.load(open(os.environ["TMP_TF"]))
    data = (d.get("data") or [])[:tf_limit] if d.get("query_status") == "ok" else []
except Exception:
    data = []
rows = []
for i in data:
    ioc = (i.get("ioc") or "")[:44]
    tt = (i.get("threat_type") or "?")
    it = (i.get("ioc_type") or "?")
    mal = (i.get("malware_printable") or i.get("malware") or "unknown")[:30]
    conf = i.get("confidence_level", "")
    fs = (i.get("first_seen") or "")[:19]
    rows.append(f"| `{ioc}` | {tt} | {it} | {mal} | {conf} | {fs} |")
    summary.append(f"{mal} [{tt}]")
feed = f"""---
title: "Feed — ThreatFox IoC"
date: {today}
tags: [wiedza, feed, threatfox, ioc]
---

# Feed — ThreatFox (świeże IoC, 24h, {tf_limit})

Wygenerowano: {ts} · źródło: `threatfox-api.abuse.ch` · skrypt `Narzedzia/update_wiedza.sh`

| IoC | Typ zagrożenia | Typ IoC | Malware | Conf. | Pierwsze |
|-----|----------------|---------|---------|-------|----------|
""" + ("\n".join(rows) if rows else "| *(brak danych)* |") + "\n"
open(f"{vault}/Wiedza/Feed_ThreatFox.md", "w").write(feed)
tf_count = len(rows)

# ---- Aktualizacje.md ----
changelog = f"{vault}/Wiedza/Aktualizacje.md"
top = "; ".join(summary[:6]) or "—"
entry = (f"- `{ts}` Feedy: MalwareBazaar ({mb_count}) · CISA KEV ({kev_count}) · "
         f"ThreatFox ({tf_count}) — m.in. {top}\n")
if os.path.exists(changelog):
    txt = open(changelog).read()
    marker = "### Auto\n"
    if marker in txt:
        txt = txt.replace(marker, marker + entry, 1)
    else:
        txt = txt.rstrip() + "\n\n### Auto\n" + entry
    open(changelog, "w").write(txt)

print(f"ok: MB={mb_count} KEV={kev_count} TF={tf_count} -> Feed_*.md + Aktualizacje.md")
PY
