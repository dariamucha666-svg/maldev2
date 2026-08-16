---
title: "V — Podatności (Vulnerabilities)"
date: 2026-08-16
tags: [ive, v, podatnosci, skanery]
category: pentest
status: active
---

# V — Zestaw podatności (Vulnerabilities)

Faza **V** identyfikuje luki w celu, który wyznaczyła faza I. Skanery dają listę
luk (CVE, misconfig, słabe hasła, braki nagłówków, otwarte panele).

## Narzędzia

| Narzędzie | Typ | Notatka |
|-----------|-----|---------|
| Nessus | komercyjny skaner (65k+ pluginów) | [[Model_IVE/V_Podatnosci/Nessus]] |
| OpenVAS | darmowy, otwartoźródłowy (Greenbone) | [[Model_IVE/V_Podatnosci/OpenVAS]] |
| OWASP ZAP | darmowy skaner aplikacji web | [[Model_IVE/V_Podatnosci/OWASP_ZAP]] |
| Burp Suite | platforma testów web (proxy+scanner) | [[Model_IVE/V_Podatnosci/Burp_Suite]] |
| Nmap | porty, usługi, wersje (NSE) | [[Model_IVE/V_Podatnosci/Nmap]] |
| Acunetix | komercyjny skaner web | [[Model_IVE/V_Podatnosci/Acunetix]] |

> **Nuclei** (template'owy skaner) technicznie też tu należy — autor umieścił go w E.
> Zobacz [[Model_IVE/E_Eksploatacja/Nuclei]].

## Podział wg warstwy

- **Sieć / host**: Nmap (porty, NSE), Nessus/OpenVAS (CVE na usługach, misconfig).
- **Aplikacja web**: Burp Suite, OWASP ZAP, Acunetix (OWASP Top 10: SQLi, XSS, SSRF…).
- **Automatyka/DAST**: Nuclei (szablony YAML, 13k+), bardzo szybki.

## Wynik fazy V → wejście do E

```
luka (CVE / SQLi / weak creds)  ──▶  Metasploit / Sqlmap / Nuclei (E)
```

## Powiązane

- [[Model_IVE/IVE_MOC]] · [[Model_IVE/I_Informacja/I_MOC]] · [[Model_IVE/E_Eksploatacja/E_MOC]] · [[Techniki_i_Narzedzia]]
