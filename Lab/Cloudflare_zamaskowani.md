---
tags: [lab, cloudflare, dns]
updated: 2026-08-15
---

# Cloudflare — zamaskowani.eu

Powiązane: [[Daily/2026-08-15]] · maskencrypt.eu już na CF.

## Stan 2026-08-15

| Pole | Wartość |
|------|---------|
| Registrar | nazwa.pl (NetArt) |
| Zone | `zamaskowani.eu` |
| Status | pending (czekamy na NS) |
| Zone ID | `236cdbce95e3afd8aa12b3dc6bd07ff7` |
| Nameservery | `raegan.ns.cloudflare.com` / `shane.ns.cloudflare.com` |
| Origin | `85.128.197.150` (CloudHosting nazwa) |

## Co kliknąć w nazwa.pl

Nie używać „Przekierowanie na usługę w nazwa.pl”.

1. Usługi → Domeny → `zamaskowani.eu` → konfiguruj
2. Zakładka **Zewnętrzne serwery DNS**
3. Serwer DNS 1: `raegan.ns.cloudflare.com`
4. Serwer DNS 2: `shane.ns.cloudflare.com`
5. ZMIEŃ

Przełączenie wyłącza pakiet „Bezpieczna domena” (DNSSEC / Anycast / SPF-DKIM-DMARC w nazwa). Rekordy poczty są już w Cloudflare.

## Rekordy w CF (skrót)

- A proxied: `@`, `www`, `*` → 85.128.197.150
- A DNS-only: `mail`, `smtp`, `pop`, `pop3`, `imap`, `ftp`
- MX 10 → `mail.zamaskowani.eu` (żeby poczta nie szła na anycast CF)
- TXT SPF / DMARC / DKIM (`1584650178.internal._domainkey`)
- CAA: letsencrypt.org + certum.pl (issue + issuewild)

Po Active: można włączyć DNSSEC w CF i wkleić DS z powrotem u rejestratora.
