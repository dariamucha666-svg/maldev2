---
title: "Phishing tools — reverse engineering (SET, SocialFish, Evilginx2)"
date: 2026-08-15
updated: 2026-08-15
tags: [phishing, reverse-engineering, source-code, set, socialfish, evilginx2, aitm]
status: analysis
category: narzedzia
---

# Phishing tools — analiza kodu źródłowego (deep dive)

Reverse engineering kodu 3 narzędzi (15.08). Źródła sklonowane na `.139`:
`/opt/set`, `/opt/socialfish`, `/opt/evilginx2`.

Powiązane: [[Narzedzia/Phishing_Toolkit]] (przegląd) · [[Lab/Phishing_Sim_Lab]] (instancja GoPhish/SET)

---

## 1. SET — Social-Engineer Toolkit (Python, `src/`)

### Credential Harvester — `src/webattack/harvester/harvester.py`

Mechanizm (z kodu):

```
harvester.py  →  prosty http.server (do_GET / do_POST)
   ├─ do_GET:  serwuje web_clone/index.html  (sklonowaną stronę)
   │           + licznik wizyt ("hit")
   └─ do_POST: przechwytuje WSZYSTKIE POSTy → parsuje pola
```

- **Wykrywanie pól** (regex, nie struktura formularza):
  - username: `Email|email|login|logon|user|username|User`
  - password: `pwd|pass|uid|uname|userid|PIN|password|secret|Pass`
- **Logowanie haseł** zależy od `HARVESTER_LOG_PASSWORDS=` (ON/OFF) — „not an exact science".
- **Wynik**: `WE GOT A HIT! POSSIBLE USERNAME/PASSWORD FIELD FOUND` + zapis do
  `src/logs/harvester.log` i `HARVESTER_LOG` (domyślnie `/var/www`).

### Klonowanie — `src/webattack/web_clone/cloner.py`

- Preferuje `wget -H -N -k -p -l 2` (mirror, -k = konwersja linków), fallback `urllib`.
- Zapisuje do `web_clone/index.html`; przepisuje formularz (`action`).
- **Ograniczenie:** klon statyczny (HTML/CSS/JS z wget), bez dynamicznego JS — dlatego
  nowoczesne SPA (React/Vue) klonują się źle.

### Detekcja SET (artefakty z kodu)

- `X-Mailer`/server: prosty `http.server` (banner w odpowiedzi).
- Plik klonu: `web_clone/index.html` + User-Agent wget: `Wget/…`.
- Regex-owa heurystyka pól (SET szuka `user`/`pass` — nie struktury form).
- Port domyślny 80/443 (config `WEB_PORT`), logi `harvester.log`.

---

## 2. SocialFish (Python) — ewoluował w mini-AiTM

**To już nie jest prosty script-kid phishing.** Obecny `master` to framework z automatyzacją
przeglądarki i przechwytywaniem cookie — zbliżony do Evilginx.

### Kluczowe moduły (`core/`)

| Moduł | Rola |
|-------|------|
| `recorder_playwright.py` / `recorder_selenium.py` | **automatyzacja przeglądarki** — nagrywanie/odtwarzanie dynamicznych loginów (SPA) |
| `cookie_inspector.py` | `analyze_cookies` / `_scrape_all_cookies` — przechwytuje i analizuje cookie |
| `advanced_attacks.py` | **JS injection**: keylogger, tab-jacking, window-hijack, form-hijack, fake-logout, clipboard-steal (kody 2FA) |
| `mock_server.py` | serwer-mock do odtwarzania nagranych flow |
| `tunnel_manager.py` | ngrok / cloudflared |
| `report.py`, `genReport.py` | raporty (pylatex) |
| `tracegeoIp.py` | geo-IP ofiary |

### Mechanizm (z kodu)

```
SocialFish → uruchamia prawdziwą przeglądarkę (Playwright/Selenium)
  ├─ _detect_forms / _detect_all_forms   (znajduje formularze w DOM)
  ├─ _fill_and_submit_form               (automatycznie wypełnia)
  ├─ _inject_stealth_js                  (ukrywa ślady webdrivera)
  ├─ _inject_keylogger                   (keylogger w DOM)
  ├─ _scrape_all_cookies + _capture_cookies   (przechwytuje sesje)
  ├─ _take_screenshot / _save_screenshot  (dowód)
  └─ _mfa_html / _oauth_consent_html      (obsługa MFA/OAuth)
```

**Wniosek:** SocialFish = **AiTM z prawdziwą przeglądarką** (a nie reverse-proxy jak Evilginx).
To różnica: Evilginx przepisuje ruch HTTP, SocialFish **steruje przeglądarką** i czyta DOM/cookie.

### Detekcja SocialFish

- Ślady automatyzacji: `webdriver` flagi (choć `_inject_stealth_js` je usuwa), nagłówki
  Chrome/Playwright, `navigator.webdriver`.
- Tunel: `*.ngrok-free.app` / cloudflared.
- Artefakty: screenshoty, `database.db` (SQLite z sesjami/cookie), raporty pylatex.

---

## 3. Evilginx2 (Go) — reverse-proxy AiTM

### Architektura (`core/`)

| Plik | Rola |
|------|------|
| `http_proxy.go` | **rdzeń**: reverse proxy, przechwytywanie cookie, JS injection |
| `phishlet.go` | parser phishletów (YAML) |
| `session.go` | przechowywanie przechwyconych sesji |
| `certdb.go` | certyfikaty (Let's Encrypt) |
| `nameserver.go` | DNS (subdomeny) |
| `gophish.go` | integracja z GoPhish |

### Phishlet (YAML) — kluczowy format

```yaml
proxy_hosts:
  - {phish_sub: 'academy', orig_sub: 'academy', domain: 'breakdev.org', session: true, is_landing: true}
sub_filters:
  - {triggers_on: 'breakdev.org', search: 'coś', replace: 'zastąp', mimes: ['text/html']}
auth_tokens:            # ← CO PRZECHWYTUJE (cookie sesyjne)
  - domain: '.academy.breakdev.org'
    keys: ['cookie_name']
credentials:
  username: {key: 'email', type: 'post'}
  password: {key: 'password', type: 'post'}
login:
  domain: 'academy.breakdev.org'
  path: '/evilginx-mastery'
```

### Przechwytywanie sesji (z `http_proxy.go`)

```go
resp.Header.Del("Set-Cookie")            // usuń oryginalne cookie
...                                       // zapisz auth_tokens
resp.Header.Add("Set-Cookie", ck.String()) // dodaj z powrotem (przepuść do ofiary)
...
s.AllCookieAuthTokensCaptured(auth_tokens)  // gdy wszystkie tokeny → sesja kompletna
```

Mechanizm: Evilginx **nie klonuje** — jest **reverse proxy**. Ofiara loguje się do *prawdziwego*
serwisu *przez* Evilginx, który po drodze kopiuje `Set-Cookie` (tokeny sesyjne). Efekt: **sesja
po 2FA trafia do atakującego**.

### Detekcja Evilginx2

- Domena lookalike (typosquat/punycode) + cert LE wystawiony tuż przed kampanią.
- Cookie sesyjne dostarczone z IP/domeny atakującego (nie oryginalnego serwisu).
- `sub_filters` podmieniają `breakdev.org`→domena phish (search/replace w HTML) — widać w źródle
  strony (zmienione originy).
- Nagłówki reverse-proxy (`Via`, `X-Forwarded-*`) — choć Evilginx je częściowo ukrywa.

---

## Porównanie techniczne

| | SET | SocialFish | Evilginx2 |
|--|--|--|--|
| Język | Python | Python | Go |
| Mechanizm | klon statyczny + prosty http.server | **prawdziwa przeglądarka** (Playwright/Selenium) | **reverse proxy** |
| Co łapie | login+hasło (POST) | cookie + DOM + screenshot + keylog | **cookie sesyjne (post-2FA)** |
| 2FA | ❌ nie obchodzi | częściowo (MFA/OAuth flow) | ✅ obchodzi |
| Dynamiczne SPA | ❌ (wget klon) | ✅ (przeglądarka) | ✅ (proxy) |
| Złożoność | niska | wysoka | średnia |
| Detekcja | wget/static clone, prosty banner | webdriver/stealth, ngrok | lookalike domena + LE cert |

## Wnioski detekcyjne

1. **SET** = najłatwiejszy do wykrycia (statyczny klon, `wget`, prosty serwer, regex `user`/`pass`).
2. **SocialFish** = najtrudniejszy do wykrycia sieciowo (steruje prawdziwą przeglądarką), ale zostawia
   artefakty automatyzacji (webdriver/stealth JS, ngrok).
3. **Evilginx2** = najgroźniejszy (kradnie sesje, obchodzi MFA); detekcja = domena lookalike +
   cert transparency + cookie z IP atakującego.

Powiązane: [[OSINT_Toolkit]] · [[Recon_ng_Analiza]] · [[Lab/Phishing_Sim_Lab]]
