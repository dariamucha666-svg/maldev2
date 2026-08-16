---
title: "I-V-E — surowe outputy analizy dynamicznej"
date: 2026-08-16
tags: [ive, analiza-dynamiczna, raw, output]
category: pentest
status: active
---

# Surowe outputy analizy dynamicznej (każda linia)

W tym folderze leżą **pełne zrzuty** wyjścia każdego narzędzia, wykonane
2026-08-16 na hoście vserver959630 (Ubuntu 24.04). To jest warstwa "zapisz
wszystko, każdą linię".

## Indeks plików

### I — Informacja
| Plik | Treść |
|------|-------|
| `theharvester_help.txt` | `theHarvester -h` (64 linie) |
| `theharvester_demo_crtsh.txt` | demo: `-d example.com -b crtsh -l 30` (theHarvester 4.11.1) |
| `reconng_version.txt` | `recon-ng --version` → 5.1.2 |
| `reconng_help.txt` | `recon-ng -h` |
| `reconng_demo_hackertarget.txt` | demo: marketplace install + `hackertarget` na example.com (2 hosty) |
| `sherlock_help.txt` | `sherlock --help` |
| `sherlock_demo.txt` | demo: GitHub check (0 wyników) |
| `sherlock_demo.csv` | CSV demo (nagłówek) |
| `spiderfoot_version.txt` | `sf.py -V` → SpiderFoot 4.0.0 |
| `spiderfoot_help.txt` | `sf.py -h` |
| `spiderfoot_demo_dns.txt` | demo: `sfp_dns` na example.com |
| `shodan_version.txt` | `shodan version` → 1.31.0 |
| `shodan_help.txt` | `shodan -h` |
| `shodan_info_noapikey.txt` | `shodan info` bez klucza → błąd "shodan init" |

### V — Podatności
| Plik | Treść |
|------|-------|
| `nmap_version.txt` | `nmap --version` → 7.94SVN |
| `nmap_help.txt` | `nmap -h` (115 linii) |
| `nmap_scanme.txt` | demo: `-sV -Pn -p 22,80,443 scanme.nmap.org` (OpenSSH 6.6.1, Apache 2.4.7) |
| `nmap_localhost.txt` | demo: `-sV localhost` |
| `nuclei_help.txt` | `nuclei -h` (261 linii) |
| `nuclei_templates_count.txt` | liczba szablonów → 13094 |
| `nuclei_templates_sample.txt` | próbka 25 szablonów |
| `nuclei_demo_example_headers.txt` | demo: missing-security-headers na example.com (10 braków) |
| `nuclei_demo_techdetect.txt` | demo: tech-detect na scanme.nmap.org |

### E — Eksploatacja
| Plik | Treść |
|------|-------|
| `msf_version.txt` | `msfconsole --version` → 6.5.2-dev |
| `msf_search_ms17010.txt` | `search ms17_010` |
| `msf_info_ssh_version.txt` | `info auxiliary/scanner/ssh/ssh_version` |
| `sqlmap_version.txt` | `sqlmap --version` → 1.8.4 |
| `sqlmap_help.txt` | `sqlmap -hh` (291 linii) |

## Uwagi

- ANSI kolory w outputach recon-ng/nuclei nie zostały usunięte (surowe zrzuty).
- Demo było **bezpieczne**: cele pasywne/autoryzowane (`example.com` — domena
  zarezerwowana IANA, `scanme.nmap.org` — oficjalny cel testowy Nmapa). Zero
  skanowania/eksploatacji cudzych systemów.
- Shodan i część modułów theHarvester/SpiderFoot/Recon-ng wymagają **kluczy API** —
  bez nich działa tylko trzon pasywny (crt.sh, hackertarget, wayback…).

## Powiązane

- [[Model_IVE/IVE_MOC]]
