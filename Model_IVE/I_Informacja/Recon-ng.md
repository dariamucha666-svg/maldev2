---
title: "Recon-ng — framework OSINT (moduły + SQLite)"
date: 2026-08-16
tags: [ive, i, osint, recon, narzedzie]
category: narzedzie
status: active
---

# Recon-ng

**TL;DR**: "Metasploit dla reconu" — modułowy framework OSINT z lokalną bazą SQLite.
Moduły (z marketplace) wrzucają wyniki do tabel (hosts, domains, contacts, ports…).

## Co to / do czego

Autor: Tim Tomes (@lanmaster53, Black Hills Information Security). Python, GPL-3.0.
W v5 moduły **nie są w repo** — instaluje się je z marketplace (osobny git).

| Cecha | Wartość |
|-------|---------|
| Język / licencja | Python 3 · GPL-3.0 |
| Model | moduły + marketplace + workspace (SQLite) |
| Dane | `hosts`, `domains`, `contacts`, `ports`, `vulnerabilities`, `netblocks`… |
| Klucze API | `keys add <name> <value>` (Shodan, VT, Bing…) |
| Raporty | `reporting/json`, `reporting/csv`, `reporting/html` |

## Instalacja (vserver959630)

```bash
git clone --depth 1 https://github.com/lanmaster53/recon-ng /opt/ive/recon-ng
python3 -m venv /opt/ive/venv-recon
/opt/ive/venv-recon/bin/pip install -r /opt/ive/recon-ng/REQUIREMENTS
/opt/ive/venv-recon/bin/python /opt/ive/recon-ng/recon-ng --version
```

## Analiza dynamiczna (2026-08-16)

**Wersja**: recon-ng **5.1.2**.

**Help** (`recon-ng -h`):

```
usage: recon-ng [-h] [-w workspace] [-r filename] [--no-version]
                [--no-analytics] [--no-marketplace] [--stealth] [--accessible]
                [--version]
```

**Demo** — instalacja modułu z marketplace + uruchomienie `hackertarget` na example.com
(`-r` plik zasobów, bo v5 nie ma już `-x`):

```
[recon-ng][default] > marketplace install recon/domains-hosts/hackertarget
[*] Module installed: recon/domains-hosts/hackertarget
[recon-ng][default][hackertarget] > options set SOURCE example.com
[recon-ng][default][hackertarget] > run
  Host: example.com     Ip_Address: 104.20.23.154
  Host: www.example.com Ip_Address: 172.66.147.243
[*] 2 total (2 new) hosts found.
```

Pełny zrzut: [[Model_IVE/_analiza_dynamiczna/README]] (\`reconng_demo_hackertarget.txt\`).

## Użycie

```bash
recon-ng -w ive_demo          # nowy workspace
# interaktywnie:
marketplace search domains-hosts
marketplace install recon/domains-hosts/brute_hosts
modules load recon/domains-hosts/brute_hosts
options set SOURCE example.com
run
show hosts
reporting/json --filename recon.json
```

## Wynik → gdzie dalej

- Pivot domena↔host↔domena (atrybucja C2) — patrz [[Recon_ng_Analiza]] (pełna analiza + miejsce w pipeline).
- Hosty/IP → [[Model_IVE/V_Podatnosci/Nmap]] · [[Model_IVE/E_Eksploatacja/Nuclei]].

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[Recon_ng_Analiza]] · [[OSINT_Toolkit]] · [[Pipeline_Analizy]]
