---
title: "Evilginx2 Lab (.139)"
date: 2026-08-16
tags: [phishing, evilginx2, aitm, lab, symulacja]
status: active
category: lab
---

# Evilginx2 Lab na .139

Evilginx2 (Community Edition) zbudowany i skonfigurowany na 5.175.189.139 (host RE/phishing).
AiTM reverse-proxy — **do symulacji i detekcji, nie do ataków na realne cele**.

Powiązane: [[Phishing_Sim_Lab]] · [[Narzedzia/Phishing_Toolkit]] · [[Narzedzia/Phishing_Deep_Dive]] · [[Lab/Hosts]] · [[Evilginx2_Phishlet_mockbank]] · [[Evilginx2_Phishlet_mocksso]] · [[Evilginx2_2FA_TwoStep]] · [[Evilginx2_Telegram_Bot]] · [[Evilginx2_Phishlet_mockinsta]]

## Stan (zbudowane 2026-08-16)

| | |
|--|--|
| Źródło | /opt/evilginx2 (git, kgretzky/evilginx2, commit 4c0988a) |
| Wersja | **3.3.0** (Community Edition) |
| Binary | /opt/evilginx2/build/evilginx (15.4 MB, Go 1.22.10) |
| Go | /usr/local/go (go1.22.10, tarball z go.dev) |
| Uruchomienie | /opt/evilginx2/run.sh |

## Build

    tar -C /usr/local -xzf go1.22.10.linux-amd64.tar.gz
    cd /opt/evilginx2 && /usr/local/go/bin/go build -o build/evilginx -mod=vendor main.go

## Konfiguracja (config/config.json)

Struktura jest **zagnieżdżona** (viper, klucz "general") — pola na top-level nie działają.

    {
      "general": {
        "domain": "breakdev.org",
        "external_ipv4": "127.0.0.1",
        "bind_ipv4": "127.0.0.1",
        "unauth_url": "https://www.google.com",
        "https_port": 8443,
        "dns_port": 5053,
        "autocert": false
      }
    }

- **bind_ipv4 127.0.0.1** → proxy + DNS tylko lokalnie (jak GoPhish/SET).
- **https_port 8443** → 443 zajęty przez sliver-server.
- **dns_port 5053** → 5353 zajęty przez avahi-daemon.
- **autocert false + flaga -developer** → certy self-signed, bez Let's Encrypt / domeny lookalike.

## Uruchomienie

    /opt/evilginx2/run.sh
    # = ./build/evilginx -developer -c config -p phishlets -t redirectors

## Weryfikacja (zrobiona)

- Start czysty, phishlet **example** wczytany.
- phishlets hostname example academy.breakdev.org + phishlets enable example → enabled.
- lures create example → lure z path (np. /FJuNLjdF).
- Nasłuch: **tcp 127.0.0.1:8443** (proxy) + **udp 127.0.0.1:5053** (nameserver).

## Automatyzacja: pakiet narzędzi laba (16.08)

Pakiet skryptów w `/opt/evilginx2/` — wszystkie loopback, stdlib Python (bez zależności):

| Skrypt | Funkcja | Wyjście |
|---|---|---|
| `generate_lures.py` | lure dla włączonych phishletów | `lures_active.txt` + tabela |
| `export_sessions.py` | eksport sesji z **data.db** (buntdb) | `sessions_export.json` + `.csv` |
| `obsidian_session_notes.py` | auto-notatki z nowych sesji | `Lab/Sessions/Evilginx2_Session_<id>.md` |
| `dashboard.py` | webowy podgląd (127.0.0.1:5000) | HTML + `/api/data` |
| `telegram_bot.py` | zarządzanie przez Telegram (@Maldevmass_bot) | [[Evilginx2_Telegram_Bot]] |

**export_sessions.py — kluczowe ustalenie:**
- Sesje CE są w `/opt/evilginx2/config/data.db` (buntdb, klucze `sessions:<id>`) — pełne JSON-y (username, password, custom/2FA, tokens). Czystsze źródło niż konsola.
- Format buntdb to RESP; klucze danych `sessions:N`, indeksy `sessions:N:id` — regex musi kotwiczyć koniec linii (`sessions:(\d+)\r?\n`), inaczej duplikaty.
- **Dedup:** plik stanu `.sessions_state.json` (ostatni wyeksportowany id); domyślnie tylko nowe, `--all` pełny.
- CSV z BOM (utf-8-sig) — otwiera się w Excelu.

**Pipeline (demo → dokumentacja):**
```
python3 export_sessions.py            # nowe sesje -> JSON+CSV (dedup)
python3 obsidian_session_notes.py     # notatki dla sesji z danymi
python3 dashboard.py --port 5000      # dashboard w tle
```

**Pipeline (phishlety):**
```
python3 generate_lures.py             # nowe lure + lures_active.txt
```

**Uwagi:**
- `obsidian_session_notes.py` pomija sesje bez danych (puste loginy); `--all` nadpisuje.
- Dashboard bez Flask — stdlib `http.server`; odświeżanie przez `fetch('/api/data')`.
- Notatki sesji: `XMask/maldev2/Lab/Sessions/Evilginx2_Session_<id>.md` (auto, nie edytować ręcznie).

## Automatyzacja: generate_lures.py (16.08)

Skrypt `/opt/evilginx2/generate_lures.py` — generuje lure dla każdego **włączonego** phishleta i zapisuje aktywne lure.

- CE nie ma API — interakcja przez `tmux send-keys` (sesja `evilginx`), dane czytane z `config/config.json` (AddLure zapisuje config po każdym `lures create`).
- **id lure = indeks w tablicy lures** (config.json nie trzyma id — tak samo liczy konsola).
- URL: `https://<hostname><path>` — bez portu (format `GetLureUrl`).
- Wyjście: `/opt/evilginx2/lures_active.txt` w formacie `[id] → URL: https://<domena>/<ścieżka>` + tabela na stdout.
- Użycie: `python3 /opt/evilginx2/generate_lures.py` (generuje) · `--list` (tylko tabela) · `--phishlet <nazwa>` (jeden).
- "Aktywne" = lure phishletów `enabled` + `hostname` (lure example/disabled pomijane).

## Konsola (komendy)

    phishlets                          # tabela phishletów
    phishlets hostname <n> <domena>    # ustaw hostname
    phishlets enable <n>               # włącz
    lures create <n>                   # utwórz lure
    lures get-url <id>                 # pełny URL
    sessions                           # przechwycone sesje (tutaj puste)
    config domain <d>                  # ustaw domenę

## Firewall (hardening)

Zaktualizowany /usr/local/bin/phish-lab-hardening.sh — dołożone **8443/tcp**, **5053/udp**, **5053/tcp** (DENY z zewnątrz). Wszystko binduje 127.0.0.1, więc i tak niepubliczne.

## Phishlet

Repo oficjalne ma tylko **example.yaml** (demo na breakdev.org — domena autora do szkoleń).
Realne phishlety (Microsoft/Google/…) nie są w repo CE (prawne) — są w Evilginx Pro lub repo społeczności.
Dla laba wystarczy example + ewentualnie własny phishlet pod lokalną stronę testową.

## Bezpieczeństwo / reguły

1. **Tylko 127.0.0.1**, flaga -developer, bez realnej domeny i bez LE.
2. Odpalać wyłącznie na własnych/autoryzowanych środowiskach (mocki, loopback) — nigdy na realne cele ani realne serwisy.
3. AiTM obchodzi 2FA — najwyższa ostrożność; użytek wyłącznie symulacyjny/awareness.
4. Przechwycone sesje (sessions) = dane wrażliwe — czyścić po demie.

## Demo AiTM (dynamiczna, 2026-08-16)

Symulacja AiTM: mock origin (HTTPS login) + własny phishlet + victim-script.

- **Mock origin:** /opt/evilginx2/mock_origin.py — HTTPS na 127.0.0.2:443 (mock.local), login ustawia Set-Cookie session=...
- **Phishlet:** /opt/evilginx2/phishlets/mocklogin.yaml — proxy_hosts mock.local, auth_tokens keys ['session'] (domain .mock.local), credentials email/password (post), login /login.
- **Phish domena:** evil.local (127.0.0.1, /etc/hosts), evilginx na 127.0.0.1:8443.

### Co potwierdzone (działa)

- Lure → 302 → /login; login POST → 302 + cookie session=MOCKSESSION_victim@corp.local.
- **Cookie rewrite:** origin (mock.local) → phish (evil.local) — victim dostaje sesję pod domeną lookalike. To jest sedno AiTM.

### Ustalenie + FIX (domknięte 2026-08-16)

- **Root cause:** nagłówek **Host** ofiary zawierał port (evil.local:8443), a evilginx dopasowuje hostname lure/sesji **bez portu**. Dlatego lure nie triggerował sesji → ps.SessionId pusty → brak zapisu.
- **Fix:** Host bez portu. W curl: -H "Host: evil.local" (albo port 443). W realnym ataku ofiara łączy się na 443, więc Host i tak jest bez portu — to był artefakt laba (8443, bo 443 = sliver).
- **Wynik po fixie:** pełne przechwycenie — Username [victim@corp.local], Password [hunter2], token [session = MOCKSESSION_victim@corp.local], tabela sessions: id 1, tokens captured.

Mechanizm (z kodu http_proxy.go): sesja = ciasteczko śledzące (losowa nazwa 8 znaków) ustawione w OnResponse gdy ps.Created, Domain = GetBaseDomain(); auth_tokens łapane gdy ps.SessionId != "".

### Sprzątnięcie

- evilginx + mock zatrzymane. Wpisy /etc/hosts (mock.local, evil.local) zostawione jako lab artifact.

## Re-start 2026-08-16 (14:17) — włączone ponownie

Włączone ponownie do laba (bind 127.0.0.1, -developer). Konfiguracja bez zmian; lure `/AcjdXWys` (mocklogin) aktywny.

- **Procesy:** evilginx w tmux `evilginx` (`/opt/evilginx2/run.sh`), mock origin na 127.0.0.2:443 (log /tmp/mock_origin.log).
- **Nasłuch:** tcp 127.0.0.1:8443 (proxy), udp 127.0.0.1:5053 (DNS), tcp 127.0.0.2:443 (mock origin).
- **Weryfikacja (full AiTM):** lure → 302 /login → POST login → 302 /dashboard z Set-Cookie `session=MOCKSESSION_victim@corp.local; Domain=evil.local` → dashboard 200 (authenticated).
- **Sesja przechwycona:** id 6, username victim@corp.local, password hunter2, tokens captured (log: `[+++] all authorization tokens intercepted!`).

### Ustalenie: SNI wymagany (nowe, 14:19)

- **Objaw:** curl/wget/python na `https://127.0.0.1:8443` z `-H "Host: evil.local"` → wiszą na TLS handshake (timeout). openssl s_client bez `-servername` też nie łączy.
- **Root cause:** evilginx wybiera phishlet/certyfikat po **SNI**. Klient łączący się na IP (SNI=IP lub brak SNI) dostaje zawieszony handshake; SNI musi być `evil.local`.
- **Fix:** `curl -sk --resolve evil.local:8443:127.0.0.1 https://evil.local:8443/AcjdXWys` (albo python z HTTPSConnection("evil.local", 8443)). To artefakt laba na 8443 — w realnym ataku na 443 SNI jest normalnie wysyłany przez przeglądarkę.
- **Dodatkowo:** POST body musi mieć `Content-Type: application/x-www-form-urlencoded`, inaczej evilginx nie wyciągnie username/password (tokens łapie i tak).

### Ustalenie: domena bazowa `local` (14:34)

- Dla phishleta `mockbank` (bank.local) trzeba było zmienić domenę bazową: `config domain local` (walidacja: hostname musi kończyć się na `.<domain>`).
- Uwaga: zmiana domeny bazowej **czyści hostname wszystkich phishletów** — po niej ponownie: `phishlets hostname mocklogin evil.local` + enable. Patrz [[Evilginx2_Phishlet_mockbank]].

### Notatka z dema

- Skrypt klienta dema: /tmp/aitm_demo.py (lure → login → dashboard, z tracking cookie + content-type).
