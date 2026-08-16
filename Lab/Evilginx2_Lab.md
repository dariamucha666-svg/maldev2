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

Powiązane: [[Phishing_Sim_Lab]] · [[Narzedzia/Phishing_Toolkit]] · [[Narzedzia/Phishing_Deep_Dive]] · [[Lab/Hosts]]

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
2. Nie odpalać na realne cele ani nie klonować realnych serwisów bez pisemnej zgody.
3. AiTM obchodzi 2FA — najwyższa ostrożność; użytek wyłącznie symulacyjny/awareness.
4. Przechwycone sesje (sessions) = dane wrażliwe — czyścić po demie.
