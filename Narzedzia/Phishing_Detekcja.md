---
title: "Phishing tools — analiza dynamiczna + reguły detekcji"
date: 2026-08-15
updated: 2026-08-15
tags: [phishing, dynamic-analysis, detection, suricata, yara, zeek]
status: analysis
category: narzedzia
---

# Phishing tools — analiza dynamiczna i detekcja

Powiązane: [[Narzedzia/Phishing_Deep_Dive]] (kod źródłowy) · [[Lab/Phishing_Sim_Lab]] (instancja)

## Analiza dynamiczna (15.08, `.139`)

### SET Credential Harvester (na żywo, tshark na loopback)

```
GET  /                    → 200  (Server: BaseHTTP/0.6 Python/3.11.2)
POST /index.html          → (bez poprawnej odpowiedzi HTTP — curl raportuje "000")
  body: username=victim.user&password=Hunter2%21   ← plaintext!
```

- **Przechwycone w `src/logs/harvester.log`:** `username=victim.user`, `password=Hunter2!`.
- **Wskaźnik #1:** `Server: BaseHTTP/0.6 Python/3.11.2` — SET to prosty `http.server` (nie nginx/apache).
- **Wskaźnik #2:** POST z **plaintext login+hasło** (brak TLS) → `username=` + `password=`.
- **Wskaźnik #3:** serwer **nie wysyła poprawnej odpowiedzi** na POST (curl `000`).

### GoPhish (na żywo, tshark na loopback)

```
GET  /?rid=hJ58013       → 200  (landing page, redirect)
POST /?rid=hJ58013       → 200  (capture credentials)
```

- **Przechwycone w DB GoPhish:** `user1@acmecorp.local -> Submitted Data`
  (payload: `username=demo.user`, `password=DemoPass1`).
- **Wskaźnik #1:** tracking link **`?rid=<id>`** (unikalny per ofiara).
- **Wskaźnik #2:** email **`X-Mailer: gophish`** (SMTP).
- **Wskaźnik #3:** pełny cykl: `Email Sent → Clicked Link → Submitted Data` + webhook.
- **Różnica vs SET:** GoPhish ma **poprawny serwer HTTP (Go)** — brak bannera `BaseHTTP/Python`.

---

## Reguły detekcji (napisałem 15.08)

### YARA — `/root/android-pipeline/tools/yara-rules/custom/phishing_tools.yar`

| Reguła | Cel | Zweryfikowana |
|--------|-----|---------------|
| `Phish_SET_Harvester_Source` | SET harvester ("WE GOT A HIT!", "POSSIBLE USERNAME FIELD") | ✅ harvester.py |
| `Phish_SET_Cloner_Wget` | SET Site Cloner (`wget -H -N -k -p -l 2`) | ✅ cloner.py |
| `Phish_SocialFish_JSInjection` | SocialFish JS injection (tab-jack/keylogger/stealer) | ✅ advanced_attacks.py |
| `Phish_SocialFish_Playwright` | SocialFish Playwright/Selenium recorder | — |
| `Phish_Evilginx2_Binary` | Evilginx2 (evilginx/phishlet/auth_tokens) | ✅ http_proxy.go |
| `Phish_Evilginx2_Phishlet` | plik phishlet (proxy_hosts/auth_tokens) | ✅ example.yaml |
| `Phish_GoPhish_Binary` | GoPhish binary | — |

### Suricata — `/root/android-pipeline/tools/detection/phishing_tools.rules`

- `9000101` SET: banner `Server: BaseHTTP/0.6 Python`.
- `9000102` SET: POST `username=` + `password=` (plaintext).
- `9000201` GoPhish: URI `?rid=`.
- `9000202` GoPhish: SMTP `X-Mailer: gophish`.
- `9000301/2` SocialFish: DNS `ngrok-free.app` / `trycloudflare.com`.
- `9000401` Evilginx2: reverse proxy (`Set-Cookie` + `X-Forwarded-For`).

### Zeek — `/root/android-pipeline/tools/detection/phishing_tools.zeek`

Notices: `SET_Harvester` · `GoPhish_Tracking` · `SocialFish_Tunnel` · `Evilginx_Proxy`.

---

## Tabela detekcyjna (skrót)

| Narzędzie | Sieć (najsilniejszy sygnał) | Plik (YARA) |
|-----------|------------------------------|-------------|
| SET | `Server: BaseHTTP/0.6 Python` + plaintext POST | `Phish_SET_Harvester_Source` |
| GoPhish | `?rid=` + `X-Mailer: gophish` | `Phish_GoPhish_Binary` |
| SocialFish | DNS `*.ngrok-free.app` / webdriver stealth | `Phish_SocialFish_JSInjection` |
| Evilginx2 | lookalike domena + LE cert + reverse proxy | `Phish_Evilginx2_Phishlet` |

## Suricata IDS — uruchomione na `.139` (15.08)

Zainstalowany **Suricata 7.0.10** (backports). Konfiguracja:
- `HOME_NET="[127.0.0.0/8,5.175.189.139/32]"`, `EXTERNAL_NET="any"` (suricata.yaml).
- Reguły: `/etc/suricata/rules/phishing_tools.rules`.

```bash
suricata -i lo -S /etc/suricata/rules/phishing_tools.rules \
  -l /var/log/suricata/phish-ids --runmode=workers
```

**Wynik na żywo (fast.log):**
```
[1:9000102] PHISHING SET - plaintext credentials POST    127.0.0.1 -> 127.0.0.1:8081
[1:9000201] PHISHING GoPhish - tracking link (?rid=)     127.0.0.1 -> 127.0.0.1:8080
[1:9000101] PHISHING SET - Python BaseHTTP banner        127.0.0.1:9999 -> ...
```

3 alerty potwierdzone na żywym ruchu laba.

✅ **False positive naprawiony (rev 2):** reguła 9000101 wymaga teraz `Server: BaseHTTP/0.6 Python`
**+** ciała odpowiedzi z formularzem logowania (`<form` + `password`). Dzięki temu **nie łapie**
już `webhook_telegram.py` (py-http, ale bez formularza). Zweryfikowane: po refine 9000101 odpala
tylko na SET, nie na webhook.

## Uwagi

- Suricata **zainstalowana i działa na `.139`** (IDS na `lo`). Zeek — reguły gotowe, brak binarnego.
- YARA **zweryfikowana na żywych plikach** (wszystkie trafienia potwierdzone).
- Reguła Evilginx2 (9000401) to heurystyka reverse-proxy — korelować z CT/cert.
