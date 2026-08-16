---
title: "Phishing simulation lab (.139)"
date: 2026-08-15
tags: [phishing, gophish, set, lab, symulacja]
status: active
category: lab
---

# Phishing simulation lab na `.139`

Narzędzia do **symulacji awareness** (nie do ataków na realne cele). Zainstalowane
na `5.175.189.139` (`vserver580088`), **związane wyłącznie z `127.0.0.1`** — dostęp
przez tunel SSH, zero ekspozycji publicznej.

## GoPhish 0.12.1

| | |
|--|--|
| Ścieżka | `/opt/gophish` |
| Service | `systemctl status gophish` (persystentny) |
| Admin UI | `https://127.0.0.1:3333` (TLS self-signed) |
| Phish server | `http://127.0.0.1:8080` |
| API key | `/opt/gophish/.api_key` (0600) — `Authorization: Bearer <key>` |
| SMTP sink | service `smtp-sink`, `127.0.0.1:2525`, maile → `/var/mail/gophish/` |
| Log | `journalctl -u gophish` / `-u smtp-sink` |

Hasło admina generowane przy **pierwszym uruchomieniu** → w logu (`Please login with the
username admin and the password …`). API key ustawiony w DB (`users.api_key`), plik `.api_key`.

## Kampania demo (skonfigurowana 15.08)

Idempotentny skrypt: `/opt/gophish/setup_campaign.py` (tworzy 5 encji przez API).

- **Sending Profile**: `Local SMTP Sink` → `it-security@acmecorp.local` (nie wysyła na świat).
- **Landing Page**: `Acme Corp - Employee Portal Login` (generyczny portal, capture creds).
- **Email Template**: `Password Expiration Notice (awareness)` (pretekst wygaśnięcia hasła).
- **Group**: `Awareness Test Group` — `user1..3@acmecorp.local` (tylko testowe).
- **Campaign**: `Awareness Test …` — **uruchomiona**, status `In progress`, 3/3 `Email Sent`.

Wynik przechwycony w SMTP sinku. Uwaga detekcyjna: mail ma `X-Mailer: gophish` i link
`…/?rid=…` — to dwa klasyczne wskaźniki GoPhish (patrz [[Narzedzia/Phishing_Toolkit]]).

## Webhook → Telegram (live feedback)

| | |
|--|--|
| Odbiornik | `/opt/gophish/webhook_telegram.py`, service `gophish-webhook` |
| Port | `127.0.0.1:9999` |
| Token | `/opt/gophish/.telegram.env` (0600, skopiowany z `.133`) |

GoPhish webhook (id=1, `Telegram alerts` → `http://127.0.0.1:9999/gophish`).
Zdarzenia (Email Sent / Clicked Link / Submitted Data / Campaign Created) → Telegram.
**Zweryfikowane**: `Clicked Link` dla `user1@acmecorp.local` dotarło do webhooka.

## Kampania B — porównanie GoPhish vs SET (15.08)

- **Page**: `Redirect -> SET Harvester` (meta-refresh → `http://127.0.0.1:8081/`).
- **Campaign**: `SET Harvester comparison …` (id=2) — ten sam template + group.
- Flow: mail → GoPhish tracking (click) → **redirect do SET** → SET łapie creds.

**SET Credential Harvester** uruchomiony:
- `setoolkit` → 1→2→3→2 (Social-Eng → Website → Credential Harvester → Site Cloner).
- Klon: `http://127.0.0.1:8090/` (lokalny serwer z `landing.html`).
- Harvester na **`0.0.0.0:8081`** (port zmieniony z 80 — 80 zajęty przez `inetsim`).
- Raport creds: `HARVESTER_LOG=/var/www` (do weryfikacji w przeglądarce).

**Porównanie:** GoPhish = pełny tracking (sent/clicked/submitted) + creds w DB;
SET = sam harvest creds do pliku, bez trackingu — klasyczna różnica framework vs script-kit.

### Dostęp (tunel SSH z `.133`)

```bash
# panel admina
ssh -L 3333:127.0.0.1:3333 root@5.175.189.139
# potem w przeglądarce: https://127.0.0.1:3333  (akceptuj cert self-signed)

# phish server (gdy konfigurujemy landing page dla testowej ofiary)
ssh -L 8080:127.0.0.1:8080 root@5.175.189.139
```

### Flow awareness (symulacja)

1. **Sending Profile** → SMTP (użyć testowego serwera, nie produkcyjnego).
2. **Landing Page** → klon strony logowania (tylko na cele demo).
3. **Email Template** → mail z linkiem do landing page.
4. **Group** → adresy **tylko wewnętrzne/testowe**.
5. **Campaign** → start; potem raport opened/clicked/submitted.

**Nigdy nie wysyłamy na realne adresy ani nie klonujemy realnych serwisów bez zgody.**

## SET (Social-Engineer Toolkit)

| | |
|--|--|
| Ścieżka | `/opt/set/setoolkit` |
| Uruchomienie | `cd /opt/set && python3 setoolkit` |

Pierwsze uruchomienie wymaga akceptacji ToS (`y`). Najczęstszy moduł do demo:
**Website Attack Vectors → Credential Harvester → Site Cloner** — klon lokalnej strony
i przechwycenie loginu+hasła do pliku (pokaz, nie realny phishing).

## Bezpieczeństwo

- GoPhish + SMTP sink + webhook **bindują `127.0.0.1`**; SET harvester na `0.0.0.0:8081`
  (domyślnie) — ale **UFW blokuje go z zewnątrz**.
- `.139` to host RE/REMnux — nie produkcyjny; i tak nie wystawiać na `0.0.0.0`.
- Domena/kampania tylko w izolowanym labie; bez realnych celów.

## Firewall (hardening 15.08)

Skrypt: `/usr/local/bin/phish-lab-hardening.sh` (idempotentny).

- UFW **default deny incoming** (już był aktywny) + jawne `DENY` dla portów laba:
  `3333, 8080, 8081, 2525, 9999, 8090` (IPv4+IPv6).
- Dozwolone z zewnątrz tylko: `22` (SSH, fail2ban), `443`, `31337` (Sliver).
- **Zweryfikowane:** z `.133` porty laba **BLOKOWANE** (timeout), z localhost na `.139` działają.

Powiązane: [[Narzedzia/Phishing_Toolkit]] · [[Lab/Hosts]] · [[Narzedzia/OSINT_Toolkit]] · [[Evilginx2_Lab]]
