---
title: "I — Informacja (OSINT / Recon)"
date: 2026-08-16
tags: [ive, i, osint, recon]
category: pentest
status: active
---

# I — Zbiór informacji o celu (OSINT / Recon)

Faza **I** zbiera dane o celu, które potem zasilają fazy V i E. Im lepszy recon,
tym precyzyjniejszy skan i eksploatacja.

## Narzędzia

| Narzędzie | Typ | Notatka |
|-----------|-----|---------|
| theHarvester | e-maile, subdomeny, IP (wyszukiwarki/API) | [[Model_IVE/I_Informacja/theHarvester]] |
| Recon-ng | framework OSINT (moduły + SQLite) | [[Model_IVE/I_Informacja/Recon-ng]] |
| Maltego | graf powiązań + transformy (GUI) | [[Model_IVE/I_Informacja/Maltego]] |
| SpiderFoot | automatyczny OSINT (100+ modułów) | [[Model_IVE/I_Informacja/SpiderFoot]] |
| Shodan | wyszukiwarka urządzeń w internecie | [[Model_IVE/I_Informacja/Shodan]] |
| Google Dorks | operatory wyszukiwania Google | [[Model_IVE/I_Informacja/Google_Dorks]] |
| OSINT Framework | index narzędzi OSINT (strona) | [[Model_IVE/I_Informacja/OSINT_Framework]] |
| Sherlock | szukanie nicku na 300+ platformach | [[Model_IVE/I_Informacja/Sherlock]] |

## Co zbieramy (typowy output fazy I)

- **Domeny / subdomeny** (crt.sh, wayback, certyfikaty, DNS brute) — powierzchnia ataku.
- **E-maile / kontakty / ludzie** — cele phishingu i atrybucja.
- **IP / netblocki / ASN / hosting** — skąd stoi cel, co jest obok.
- **Usługi / porty / technologie** (banner, tech-detect) — most do fazy V.
- **Nicki / profile operatorów** (Sherlock) — śledzenie tożsamości.

## Wynik fazy I → wejście do V

```
domeny + IP + usługi  ──▶  Nmap / Nuclei / Nessus (V)
```

## Powiązane

- [[Model_IVE/IVE_MOC]] · [[Model_IVE/V_Podatnosci/V_MOC]] · [[OSINT_Toolkit]] · [[Recon_ng_Analiza]]
