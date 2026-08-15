---
tags: [lab, cloudflare, dns]
updated: 2026-08-15
---

# Cloudflare — casinomask.eu

Powiazane: [[Daily/2026-08-15]] · [[Lab/Cloudflare_zamaskowani]]

## Stan 2026-08-15

| Pole | Wartosc |
|------|---------|
| Registrar | nazwa.pl (NetArt) |
| Zone | casinomask.eu |
| Status | pending (czekamy na NS) |
| Zone ID | ab571cabfb64ef02fe00a119e76942fd |
| Nameservery | raegan.ns.cloudflare.com / shane.ns.cloudflare.com |
| Origin | 85.128.197.150 (CloudHosting nazwa) |

## Co kliknac w nazwa.pl

Nie uzywac "Przekierowanie na usluge w nazwa.pl".

1. Uslugi -> Domeny -> casinomask.eu -> konfiguruj
2. Zakladka **Zewnetrzne serwery DNS**
3. Serwer DNS 1: raegan.ns.cloudflare.com
4. Serwer DNS 2: shane.ns.cloudflare.com
5. ZMIEN

Przelaczenie wylacza pakiet "Bezpieczna domena". Rekordy WWW/SPF/DMARC/CAA sa juz w Cloudflare.

## Rekordy w CF (skrot)

- A proxied: apex, www, wildcard -> 85.128.197.150
- A DNS-only: mail, smtp, pop, pop3, imap, ftp
- MX 10 -> mail.casinomask.eu
- TXT SPF / DMARC
- CAA: letsencrypt.org + certum.pl
- DKIM nie znaleziony publicznie — dodac recznie z panelu nazwa, jesli poczta jest w uzyciu
