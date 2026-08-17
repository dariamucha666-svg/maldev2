---
title: "Evilginx2: 2FA jako osobny krok (mockbank2, two-step)"
date: 2026-08-16
tags: [evilginx2, phishlet, aitm, 2fa, twostep, lab]
status: active
category: lab
---

# Evilginx2: 2FA jako osobny krok (mockbank2)

Scenariusz dwuetapowego logowania: ofiara robi **dwa POST-y** — `/login` (username+password), potem `/verify` (kod 2FA). Phishlet `mockbank2` (duplikat `mockbank`) + origin `bank.local`. Powiązane: [[Evilginx2_Phishlet_mockbank]] · [[Evilginx2_Lab]] · [[Lab/Hosts]].

## Komponenty

| Element | Wartość |
|---|---|
| Phishlet | `/opt/evilginx2/phishlets/mockbank2.yaml` (duplikat mockbank.yaml) |
| Phish domena | `bank2.local` → 127.0.0.1 (hosts), evilginx na 127.0.0.1:8443 |
| Origin | ten sam co mockbank: `mock_bank_origin.py` na **127.0.0.3:443** (`bank.local`) |
| Lure | id 8, path `/WRxJiMJx` |

Dlaczego `bank2.local` a nie `bank.local`: dwa phishlety nie mogą dzielić hostname (mockbank już ma `bank.local`). Origin zostaje ten sam — proxy_hosts wskazuje `bank.local` (127.0.0.3).

## Flow ofiary (dwa POST-y)

1. `GET /WRxJiMJx` (lure) → **302** → `https://bank.local/login` + cookie śledzące
2. `GET /login` → **200** (form username+password)
3. **KROK 1:** `POST /login` (username+password, **bez** 2fa_code) → **302** → `/verify`
4. `GET /verify` → **200** (form 2FA)
5. **KROK 2:** `POST /verify` (`2fa_code=654321`) → **302** → `/dashboard` + cookie `session=MOCKBANK_victim@corp.local; Domain=bank.local`
6. `GET /dashboard` → **200** `WELCOME`

## Przechwycenie (sesja 14, zweryfikowane)

```
[+++] Username: [victim@corp.local]
[+++] Password: [hunter2]
[+++] Custom: [2fa_code] = [654321]
[+++] all authorization tokens intercepted!
```

`[ custom ]` w `sessions 14`: `2fa_code : 654321` — kod złapany z POST **/verify**, username/password z POST **/login**. Jeden lure = jedna sesja z kompletem danych z dwóch kroków.

## Kluczowe ustalenie: brak path-scoping w CE 3.3.0

Próba "łapania 2fa_code tylko z POST /verify" przez phishlet **nie jest możliwa natywnie w CE**:

- `ConfigPostField` (core/phishlet.go:172-176) ma tylko `key`, `search`, `type` — **nie ma pola `path`**.
- Pętla przechwytywania (core/http_proxy.go:790-801) matchuje custom po **kluczu POST body** z dowolnego POST (`cp.key.MatchString(k)`), bez sprawdzenia `req.URL.Path`. Warunek wejścia: `ps.SessionId != ""` (ofiara przeszła przez lure).
- **Test negatywny (udokumentowany):** wysłanie `2fa_code` w POST `/login` (zła ścieżka) **też zostało przechwycone** — sesja 15: `Custom: [2fa_code] = [111222]`. Czyli scoping po ścieżce nie istnieje; liczy się tylko obecność klucza w body.

### Jak to osiągnąć w praktyce (origin-side)

"Tylko z /verify" uzyskuje się **konstrukcją origin**: formularz `/login` ma tylko username/password, formularz `/verify` ma tylko `2fa_code`. Ofiara (przeglądarka) wyśle kod wyłącznie w POST `/verify`, więc w realnym flow custom jest łapany właśnie tam. Phishlet pozostaje key-based — to standardowe zachowanie CE (realne phishlety MS/Google działają tak samo: OTP łapany z tego POST-a, w którym klucz występuje).

## Różnica mockbank vs mockbank2

| | mockbank | mockbank2 |
|---|---|---|
| Plik | mockbank.yaml | mockbank2.yaml (duplikat + komentarze) |
| Hostname | bank.local | bank2.local |
| Origin | bank.local (127.0.0.3:443) | ten sam |
| 2FA | `credentials.custom` → `2fa_code` (post) | identyczny |
| Scoping 2FA | key-based (dowolny POST) | key-based (dowolny POST) — path-scoping **niemożliwy w CE 3.3.0** |
| Lure | /IeCUvZpA | /WRxJiMJx |

## Wnioski dla red teamu

1. Dwuetapowy 2FA w CE działa bez dodatkowej konfiguracji phishleta — wystarczy `credentials.custom` z kluczem pola 2FA; każdy krok logowania to osobny POST, a dane kumulują się w jednej sesji.
2. Nie da się (w CE) ograniczyć łapania custom do ścieżki — projektując mock origin/atrapę, trzymaj pole 2FA tylko w formularzu drugiego kroku.
3. AiTM i tak obchodzi 2FA: atakujący ma login+hasło+kod (sesja 14) oraz cookie sesji do importu (StorageAce) — pełne przejęcie konta.
