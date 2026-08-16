---
title: "Shodan — wyszukiwarka urządzeń w internecie"
date: 2026-08-16
tags: [ive, i, osint, narzedzie]
category: narzedzie
status: active
---

# Shodan

**TL;DR**: wyszukiwarka **urządzeń podłączonych do internetu** — skanuje świat i
indeksuje banery usług (porty, wersje, certyfikaty). Do fazy I (powierzchnia celu).

## Co to / do czego

shodan.io — "Google dla IoT/infrastruktury". Indeksuje: otwarte porty, banery
(SSH/HTTP/…), certyfikaty SSL, kamery, PLC (ICS), bazy, routery.

| Cecha | Wartość |
|-------|---------|
| CLI | `shodan` (Python, PyPI) |
| API | wymaga klucza (`shodan init <klucz>`) |
| Bez klucza | tylko przeglądanie shodan.io (limit) |

## Instalacja (vserver959630)

```bash
/opt/ive/venv/bin/pip install shodan setuptools
# uwaga: shodan 1.31.0 używa pkg_resources → potrzebny setuptools<81
```

## Analiza dynamiczna (2026-08-16)

**Wersja**: shodan CLI **1.31.0**.

**Demo** (`shodan info` bez klucza — pokazuje wymóg klucza):

```
Error: Please run "shodan init <api key>" before using this command
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`shodan_version.txt\`,
\`shodan_help.txt\`, \`shodan_info_noapikey.txt\`).

## Użycie

```bash
shodan init <klucz>
shodan host 8.8.8.8                 # wszystko o jednym IP
shodan search 'product:Apache'      # wyszukiwanie
shodan count 'port:3389 country:PL' # statystyki
shodan scan submit 8.8.8.8          # (wymaga uprawnień/scan credits)
```

## Przykładowe zapytania (dorks Shodan)

```
port:3389 country:PL
product:"MongoDB" -auth
http.title:"webcam"
```

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[Model_IVE/I_Informacja/Google_Dorks]] · [[Model_IVE/V_Podatnosci/Nmap]]
