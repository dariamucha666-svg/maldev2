---
title: "Recon-ng — analiza i miejsce w pipeline"
date: 2026-08-15
tags: [osint, recon, narzedzia, pipeline, cti]
status: analysis
category: narzedzia
---

# Recon-ng — analiza narzędzia

Powiązane: [[Pipeline_Analizy]] · [[Status]] · [[Automatyzacja]] · [[Dashboard_IOC]]

## Co to jest

**Recon-ng** to framework **OSINT / web reconnaissance** autorstwa Tima Tomesa
(LaNMaSteR53, Black Hills Information Security), Python, open-source (GPL-3.0).
Działa jak „Metasploit dla reconu": interfejs CLI z modułami, workspace'ami i
lokalną bazą SQLite, do której moduły wrzucają wyniki (hosty, domeny, kontakty,
porty, certyfikaty, geolokalizacja, credentiale).

| Cecha | Opis |
|-------|------|
| Język / licencja | Python 3 · GPL-3.0 |
| Model | modułowy + marketplace (`marketplace install/search`) |
| Dane | SQLite per workspace (tabele: `domains`, `hosts`, `contacts`, `ports`, `vulnerabilities`, …) |
| Klucze API | `keys add <name> <value>` — Shodan, VirusTotal, Bing, Google, HaveIBeenPwned, … |
| Raporty | `reporting/json`, `reporting/csv`, `reporting/html` |

Kategorie modułów:

```
discovery/   exploitation/   import/   recon/domains-contacts/
recon/domains-hosts/   recon/hosts-domains/   recon/hosts-hosts/
recon/hosts-ports/     recon/netblocks-hosts/   reporting/
```

Przykłady:

```bash
pipx install recon-ng          # albo git clone + pip install -r REQUIREMENTS
recon-ng
[recon-ng] marketplace search domains-hosts
[recon-ng] marketplace install recon/domains-hosts/brute_hosts
[recon-ng] modules load recon/domains-hosts/brute_hosts
[recon-ng][brute_hosts] options set SOURCE example.com
[recon-ng][brute_hosts] run
[recon-ng][brute_hosts] reporting/json --filename recon.json
```

## Kluczowe rozróżnienie

Recon-ng **nie analizuje malware** i **nie reverse-enginuje binarek**. To nie
sandbox, nie detonator, nie dekompilator. To narzędzie do **mapowania
infrastruktury / OSINT** — czyli idealne uzupełnienie, a nie zamiennik,
pipeline'a statycznej analizy.

```
Pipeline (RE)                        Recon-ng / OSINT
─────────────                        ────────────────
APK/PE → hashe, URL, IP, C2          C2 domena → WHOIS, passive DNS,
→ rola (rat/stealer/backdoor)        SSL cert, reverse DNS, hosty sąsiednie,
→ YARA / Sigma / IOC                 kontakty, netblocki, „co jeszcze łączy się z C2"
```

## Gdzie pasuje w naszym pipeline

Pipeline daje **IoC** (np. `suahoje.com:3000`, `off-game.com:3000` z
[[Analizy/Malware/1b3ceba6 Chrome bank stealer]], IP z URLhaus, hashe).
Recon-ng dorzuca pivot, którego `enrich_cti.py` nie robi:

1. **domena → powiązane hosty/IP** (brute, passive DNS, certyfikaty),
2. **host → domeny** (reverse DNS),
3. **WHOIS / kontakty / ASN / netblock** (atrybucja infrastruktury),
4. **relacje** między naszymi próbkami przez wspólną infrastrukturę.

Proponowany flow (po `pipeline.sh`):

```bash
# wyciągnij domeny z raportów i wrzuć do Recon-ng
python3 - <<'PY'
import json,glob
from urllib.parse import urlparse
doms=set()
for f in glob.glob('/root/samples/reports/*.json'):
    if 'iocs.json' in f or 'features' in f or 'cti_' in f: continue
    try: j=json.load(open(f))
    except: continue
    urls=j.get('urls') or (j.get('patterns') or {}).get('urls') or []
    for u in urls:
        try: doms.add(urlparse(u).netloc.split(':')[0].lower())
        except: pass
print('\n'.join(sorted(d for d in doms if d and not d.startswith('schemas.'))))
PY
```

## Porównanie z podobnymi narzędziami

| Narzędzie | Typ | Kiedy użyć | U nas? |
|-----------|-----|-----------|--------|
| **Recon-ng** | framework OSINT (moduły + SQLite) | pivot domen/hostów, atrybucja C2 | analiza → tak |
| **theHarvester** | e‑maile/subdomeny (wyszukiwarki) | szybkie zbieranie kontaktów/subdomen | opcjonalnie |
| **SpiderFoot** | automatyczny OSINT (100+ modułów) | jeden skan „o wszystkim" dla domeny/IP | opcjonalnie |
| **Maltego** | graf + transformy (GUI) | wizualna mapa C2 (płatne) | nie |
| **Amass** (OWASP) | subdomeny/passive DNS/certyfikaty | głęboka enumeracja domen | warto |
| **subfinder** | subdomeny (szybkie) | szybka lista subdomen | warto |
| **sherlock** | username search | śledzenie operatora (nick) | opcjonalnie |
| **nuclei** | skaner podatności (szablony) | sprawdzenie C2 pod kątem podatności | już jest (`/usr/local/bin/nuclei`) |
| **Fierce/dnsenum** | DNS recon | szybki DNS brute | opcjonalnie |

## Wniosek

- **Dodać Recon-ng jako krok OSINT *po* RE** (ręczny / półautomatyczny), a nie
  do samego skanowania próbek.
- Największa wartość dla nas: **pivot z domen C2** wyciągniętych przez pipeline
  → mapowanie infrastruktury i łączenie próbek we wspólne kampanie.
- Wymaga sporej liczby darmowych kluczy API (Shodan, VT, Bing…) — bez nich
  część modułów nie działa; trzon (brute_hosts, hacksy, bing, crt.sh) działa.
- Instalacja w osobnym venv (dużo zależności) — nie do `.venv` pipeline'a.

## Instalacja (do potwierdzenia na VPS)

```bash
python3 -m venv /opt/recon-ng/.venv && source /opt/recon-ng/.venv/bin/activate
pip install recon-ng          # czysty pip (oficjalny sposób)
# albo:
# git clone https://github.com/lanmaster53/recon-ng /opt/recon-ng
# pip install -r /opt/recon-ng/REQUIREMENTS
```
