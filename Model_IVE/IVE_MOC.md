---
title: "Model I-V-E (Informacja → Podatności → Eksploatacja)"
date: 2026-08-16
tags: [ive, metodologia, pentest, osint, recon, model]
category: pentest
status: active
---

# Model I-V-E

> Model procesu ofensywnego rozbity na 3 fazy. Każdej fazie odpowiada zestaw
> narzędzi. Punktem końcowym jest **cel (C)** — wykorzystanie podatności do
> osiągnięcia efektu (dostęp, dane, wpływ, raport).

| Faza | Nazwa | Co robi | MOC |
|------|-------|---------|-----|
| **I** | Informacja (OSINT / Recon) | zbieranie danych o celu: domeny, subdomeny, e-maile, nicki, IP, usługi, ludzie, powierzchnia internetowa | [[Model_IVE/I_Informacja/I_MOC]] |
| **V** | Podatności (Vulnerabilities) | skanowanie/identyfikacja luk w celu (CVE, misconfig, weak creds) | [[Model_IVE/V_Podatnosci/V_MOC]] |
| **E** | Eksploatacja (Exploitation) | wykorzystanie znalezionych luk → osiągnięcie celu | [[Model_IVE/E_Eksploatacja/E_MOC]] |

## Flow

```
   I (Informacja)           V (Podatności)           E (Eksploatacja)         C (Cel)
 ──────────────────        ─────────────────        ──────────────────       ────────
 OSINT/recon daje          skanery identyfikują      exploity wykorzystują     dostęp,
 listę celów (domeny,      luki (CVSS, misconfig,    luki → shell / dane /     flagę,
 IP, usługi, ludzie) ───▶  weak creds, CVE)    ───▶  wpływ na system     ───▶  raport
```

- **I** mówi *co atakować* (powierzchnia).
- **V** mówi *gdzie jest słabo* (konkretna luka).
- **E** mówi *jak to wykorzystać* (exploit).
- **C** to *efekt końcowy* (cel kampanii).

## Narzędzia — stan (2026-08-16, host vserver959630)

Legenda: ✅ zainstalowane + analiza dynamiczna wykonana · 📚 udokumentowane (komercyjne / GUI / zbyt ciężkie dla tego hosta).

### I — Informacja
| Narzędzie | Stan | Notatka |
|-----------|------|---------|
| theHarvester 4.11.1 | ✅ | [[Model_IVE/I_Informacja/theHarvester]] |
| Recon-ng 5.1.2 | ✅ | [[Model_IVE/I_Informacja/Recon-ng]] |
| Sherlock 0.16.1 | ✅ | [[Model_IVE/I_Informacja/Sherlock]] |
| SpiderFoot 4.0.0 | ✅ | [[Model_IVE/I_Informacja/SpiderFoot]] |
| Shodan CLI 1.31.0 | ✅ | [[Model_IVE/I_Informacja/Shodan]] |
| Maltego | 📚 (CE płatna/graf GUI) | [[Model_IVE/I_Informacja/Maltego]] |
| Google Dorks | 📚 (technika) | [[Model_IVE/I_Informacja/Google_Dorks]] |
| OSINT Framework | 📚 (strona-index) | [[Model_IVE/I_Informacja/OSINT_Framework]] |

### V — Podatności
| Narzędzie | Stan | Notatka |
|-----------|------|---------|
| Nmap 7.94SVN | ✅ | [[Model_IVE/V_Podatnosci/Nmap]] |
| Nuclei 3.11.1 (13094 szablonów) | ✅ | [[Model_IVE/E_Eksploatacja/Nuclei]] |
| Nessus | 📚 (komercyjny) | [[Model_IVE/V_Podatnosci/Nessus]] |
| OpenVAS / Greenbone | 📚 (ciężkie) | [[Model_IVE/V_Podatnosci/OpenVAS]] |
| OWASP ZAP | 📚 (Java, GUI/headless) | [[Model_IVE/V_Podatnosci/OWASP_ZAP]] |
| Burp Suite | 📚 (GUI, patrz istniejąca nota) | [[Model_IVE/V_Podatnosci/Burp_Suite]] |
| Acunetix | 📚 (komercyjny) | [[Model_IVE/V_Podatnosci/Acunetix]] |

### E — Eksploatacja
| Narzędzie | Stan | Notatka |
|-----------|------|---------|
| Metasploit 6.5.2-dev | ✅ | [[Model_IVE/E_Eksploatacja/Metasploit]] |
| Sqlmap 1.8.4 | ✅ | [[Model_IVE/E_Eksploatacja/Sqlmap]] |
| Nuclei 3.11.1 | ✅ | [[Model_IVE/E_Eksploatacja/Nuclei]] |

> Nuclei jest technicznie **skanerem (V)**, ale autor umieścił go w **E** — tutaj
> zachowuję tę kategoryzację i linkuję obustronnie ([[Model_IVE/V_Podatnosci/V_MOC]]).

## Surowe outputy (każda linia)

Pełne zrzuty analizy dynamicznej leżą w [[Model_IVE/_analiza_dynamiczna/README]] —
tam są zapisane *wszystkie* linie wyjścia każdego narzędzia.

## Powiązane

- [[Pentest_MOC]] · [[Wiedza/Narzedzia]] · [[OSINT_Toolkit]] · [[Recon_ng_Analiza]] · [[Pipeline_Analizy]]
