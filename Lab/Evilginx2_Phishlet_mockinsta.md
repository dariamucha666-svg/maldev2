---
title: "Evilginx2 Phishlet: mockinsta (insta.local, 2FA verificationCode)"
date: 2026-08-16
tags: [evilginx2, phishlet, aitm, 2fa, instagram, mock, lab]
status: active
category: lab
---

# Evilginx2 Phishlet: mockinsta

Mock Instagram-like z dwuetapowym logowaniem (login ajax → two_factor → feed).
**Nie** klon prawdziwego Instagrama — lokalna atrapa na loopback (reguła laba:
tylko własne/autoryzowane środowiska, bez realnych serwisów). Powiązane: [[Evilginx2_Lab]] ·
[[Evilginx2_2FA_TwoStep]] · [[Evilginx2_Telegram_Bot]].

## Komponenty

| Element | Wartość |
|---|---|
| Phishlet | `/opt/evilginx2/phishlets/mockinsta.yaml` |
| Mock origin | `/opt/evilginx2/mock_insta_origin.py` — HTTPS na **127.0.0.5:443** (`insta.local`) |
| Cert | `insta.local.{crt,key}` (SAN: insta.local, IP 127.0.0.5) |
| Hosts | `127.0.0.5 insta.local` |
| Lure | `/jqwiZOlG` |

## Flow (jak prawdziwy IG, ale mock)

1. `GET /jqwiZOlG` (lure) → 302 `/accounts/login/ajax/` + cookie śledzące
2. `GET /accounts/login/` → form (username+password)
3. **KROK 1:** `POST /accounts/login/ajax/` → 302 `/accounts/login/two_factor/`
4. `GET /accounts/login/two_factor/` → form (`verificationCode`)
5. **KROK 2:** `POST /accounts/login/two_factor/` → 302 `/` + cookie `session=MOCKINSTA_...; Domain=insta.local`
6. `GET /` → 200 feed (authenticated)

## Przechwycenie (sesja 25-26, zweryfikowane)

```
[+++] Username: [user@insta.local]
[+++] Password: [InstaPass123]
[+++] Custom: [verificationCode] = [777888]
[+++] all authorization tokens intercepted!
```

`[ custom ]` w `sessions`: `verificationCode : 777888`. Cookie do importu (StorageAce).

## ⚠️ Mapa: Twój format → format CE 3.x

Wysłany plik `instagram.yaml` (hosts/subdomains/phishlets/on_auth/two_factor)
**nie jest formatem evilginx2 CE** — prawdopodobnie format innego narzędzia lub
AI-generowany. Mapowanie na realne klucze:

| Twój klucz | Odpowiednik CE | Uwagi |
|---|---|---|
| `hosts` / `subdomains` | `proxy_hosts` (phish_sub/orig_sub/domain) + `phishlets hostname` | hostname to phish domena |
| `phishlets.login.auth_url` | `login: {domain, path}` | ścieżka POST logowania |
| `login_urls` | `login.path` + proxy (origin decyduje) | CE nie ma listy; origin redirectuje |
| `params` (username/password/...) | `credentials.{username,password,custom}` | key = nazwa pola POST |
| `redirect_url` | origin (Set-Cookie + 302) | CE nie konfiguruje redirectu phishleta |
| `on_auth` (shell hook) | **brak w CE** — AlertMonitor bota (poll data.db) | `on_auth_url` to funkcja Pro |
| `two_factor.param` | `credentials.custom: [{key: verificationCode}]` | patrz [[Evilginx2_2FA_TwoStep]] |

## Alert push (verificationCode)

AlertMonitor bota rozpoznaje 2FA po nazwie pola: filtr `2fa|otp|code|mfa|token`
(rozszerzony o `verificationCode`). Alert: `tfa: 777888`. Patrz [[Evilginx2_Telegram_Bot]].

## Uwagi

- Bug w originie: kolejność warunków path — `/accounts/login/two_factor/` musi
  być sprawdzany PRZED `/accounts/login/` (inaczej zwraca login form).
- 2FA w dwóch krokach — dane kumulują się w jednej sesji (jak mockbank2).
- Reguła: tylko loopback, atrapa, bez realnych serwisów.
