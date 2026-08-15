---
title: "OSINT toolkit (.139)"
date: 2026-08-15
tags: [osint, recon, narzedzia, cti, lab]
status: active
category: narzedzia
---

# OSINT toolkit na `.139`

Zestaw narzędzi OSINT/recon do mapowania infrastruktury C2 — zainstalowany
na **`5.175.189.139`** (`vserver580088`, Debian 12, 5.1 GiB RAM wolne).
Uzupełnienie [[Recon_ng_Analiza]] i [[Pipeline_Analizy]].

## Zainstalowane (15.08)

| Narzędzie | Wersja | Typ | Instalacja | Do czego |
|-----------|--------|-----|------------|----------|
| **Recon-ng** | 5.1.2 | framework OSINT (moduły+SQLite) | venv `/opt/recon-ng` + git | pivot domen/hostów, atrybucja |
| **amass** (OWASP) | 5.1.1 | passive DNS/subdomeny/certyfikaty | binary `/usr/local/bin/amass` | głęboka enumeracja domeny |
| **subfinder** | 2.15.0 | passive subdomain enum | binary `/usr/local/bin/subfinder` | szybka lista subdomen |
| **nuclei** | 3.11.1 | skaner podatności (szablony) | binary `/usr/local/bin/nuclei` | sprawdzenie hostów C2 |
| **httpx** | 1.10.0 | probe HTTP + tech-detect | binary `/usr/local/bin/httpx` | kto żyje z listy hostów |
| **theHarvester** | git (py3.12) | e‑maile + subdomeny | venv `/opt/osint/theHarvester/.venv` | atrybucja operatora |
| **SpiderFoot** | 4.0.0 | automatyczny OSINT (100+ modułów) | venv `/opt/osint/.venv` | jeden skan „o wszystkim" |
| **sherlock** | 0.16.0 | username search | venv `/opt/osint/.venv` | śledzenie nicku operatora |

Wspólne venv Pythona: `/opt/osint/.venv` (spiderfoot, sherlock).
theHarvester ma własne venv (wymaga **Python ≥3.12** → przez `uv`).
Narzędzia Go (amass/subfinder/nuclei/httpx) → gotowe binary w `/usr/local/bin`.

## Flow w pipeline

```
pipeline.sh (RE)              enrich_cti.py (hash/URL/IP → abuse.ch/VT/OTX)
      │                              │
      └────────── domeny C2 ─────────┘
                     │
        ┌────────────┼─────────────────────┐
   recon_osint.sh  osint_recon.sh    (manualnie)
   (Recon-ng)      (subfinder+amass   theHarvester / SpiderFoot / sherlock
                     +httpx+nuclei)
```

## Wrappery (na `.133`)

```bash
# Recon-ng (hackertarget) — pivot host→IP
bash ~/android-pipeline/bin/recon_osint.sh suahoje.com off-game.com

# subfinder + amass + httpx + nuclei — enumeracja subdomen + probe + delikatny skan
bash ~/android-pipeline/bin/osint_recon.sh off-game.com
SKIP_AMASS=1 bash ~/android-pipeline/bin/osint_recon.sh   # szybko (tylko subfinder)
SKIP_NUCLEI=1 bash ~/android-pipeline/bin/osint_recon.sh  # bez nuclei
```

Wyniki: `/root/samples/reports/osint/` (`subs_*`, `httpx_*`, `nuclei_*`).

**Podpięte do nightly** (`nightly_pipeline.sh`, krok 3d — po CTI enrichment i export):
`osint_recon.sh` (z `SKIP_AMASS=1`) + `recon_osint.sh`. Flaga `SKIP_OSINT=1` w `pipeline.env`
wyłącza cały krok. Sekcje `## OSINT` i `## Nuclei` lądują w `daily_summary_YYYYMMDD.md`.

**Nuclei** (delikatnie): `http/technologies/ + http/exposures/ + http/misconfiguration/ +
http/exposed-panels/ + http/takeovers/ + ssl/`, na żywych hostach z httpx.
Szablony w `~/nuclei-templates` na `.139` (pobrane `-update-templates`).
`takeovers` łapie przejęte subdomeny C2 (krytyczne dla OSINT).

## Ręcznie (na `.139`)

```bash
ssh root@5.175.189.139

# subdomeny
subfinder -d off-game.com -silent
amass enum -passive -d off-game.com

# probe
subfinder -d off-game.com -silent | httpx -silent -status-code -title -tech-detect

# e-maile / subdomeny (crtsh nie wymaga klucza)
theHarvester -d off-game.com -b crtsh -l 300

# SpiderFoot (web UI na localhost:5001)
spiderfoot -l 127.0.0.1:5001

# nick operatora
sherlock someusername
```

## Uwagi

- **Bez kluczy API** działa trzon pasywny: subfinder (crt.sh, wayback), amass passive,
  theHarvester `crtsh`, SpiderFoot (część modułów), Recon-ng `hackertarget`.
- Po dodaniu kluczy (Shodan, VirusTotal, SecurityTrails, BinaryEdge…) wyniki są dużo
  bogatsze — klucze trzymamy w `.139` (nie w vaultcie).
- `nuclei` na C2 wymaga ostrożności (aktywne żądania) — tylko w izolowanym labie.
- amass potrafi wisieć ~60 s na domenie bez danych → w wrapperze `AMASS_TIMEOUT=60`, `SKIP_AMASS=1`.

Powiązane: [[Lab/Hosts]] · [[Recon_ng_Analiza]] · [[Pipeline_Analizy]] · [[Dashboard_IOC]]
