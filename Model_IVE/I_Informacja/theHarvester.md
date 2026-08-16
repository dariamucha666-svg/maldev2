---
title: "theHarvester — e-maile, subdomeny, IP z OSINT"
date: 2026-08-16
tags: [ive, i, osint, recon, narzedzie]
category: narzedzie
status: active
---

# theHarvester

**TL;DR**: zbiera e-maile, subdomeny, hosty, IP, URL i profile (ludzi) z publicznych
źródeł (wyszukiwarki, crt.sh, Shodan, VirusTotal…) — do fazy I (recon).

## Co to / do czego

Autor: Christian Martorella (Edge-Security). Python, GPL-2.0. Pyta wiele backendów
i scala wyniki w jeden raport. W nowych wersjach (4.x) ma też własne API (FastAPI)
i tryb screenshotów (playwright).

| Cecha | Wartość |
|-------|---------|
| Język / licencja | Python ≥3.12 · GPL-2.0 |
| Źródła (backendy `-b`) | crtsh, anubis, baidu, bing, brave, censys, dnsdumpster, duckduckgo, google, hunter, intelx, linkedin, netcraft, otx, rapiddns, shodan, threatminer, trello, urlscan, virustotal, yahoo |
| Bez klucza API | crtsh, duckduckgo, anubis (część) |
| Klucze API | shodan, censys, hunter, intelx, virustotal, otx… |

## Instalacja (vserver959630)

```bash
git clone --depth 1 https://github.com/laramies/theHarvester /opt/ive/theHarvester
python3 -m venv /opt/ive/venv-harvester
/opt/ive/venv-harvester/bin/pip install /opt/ive/theHarvester
# binarka: /opt/ive/venv-harvester/bin/theHarvester
```

> Uwaga: repo nie ma już `requirements/base.txt` — instalacja idzie przez
> `pyproject.toml` (`pip install .`).

## Analiza dynamiczna (2026-08-16)

**Wersja**: theHarvester **4.11.1** (z bannera demo).

**Help** (`theHarvester -h`):

```
usage: theHarvester [-h] -d DOMAIN [-l LIMIT] [-S START] [-p] [-s]
                    [--screenshot SCREENSHOT] [-e DNS_SERVER] [-t]
                    [-r [DNS_RESOLVE]] [-n] [-c] [-f FILENAME] [-w WORDLIST]
```

**Demo** (`theHarvester -d example.com -b crtsh -l 30`) — pasywny backend crt.sh,
bez klucza:

```
* theHarvester 4.11.1
[*] Target: example.com
[*] Searching CRTsh.
[*] No IPs found.
[*] No emails found.
[*] No people found.
[*] Hosts found: 0
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`theharvester_help.txt\`,
\`theharvester_demo_crtsh.txt\`).

## Użycie

```bash
# pasywnie (crt.sh), bez kluczy
theHarvester -d cel.com -b crtsh -l 300

# kilka źródeł naraz
theHarvester -d cel.com -b crtsh,anubis,duckduckgo -l 200

# z kluczem Shodan
theHarvester -d cel.com -b shodan -s

# port scan hostów (-p) + dns brute (-c) + dns resolve (-r)
theHarvester -d cel.com -b crtsh -l 500 -p -c -r
```

## Wynik → gdzie dalej

- Domena/subdomeny → [[Model_IVE/I_Informacja/Recon-ng]] (pivot host↔domena),
  [[Model_IVE/I_Informacja/SpiderFoot]] (głębszy skan).
- IP/usługi → [[Model_IVE/V_Podatnosci/Nmap]] (faza V).

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[OSINT_Toolkit]] · [[Recon_ng_Analiza]]
