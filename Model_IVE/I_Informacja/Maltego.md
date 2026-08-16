---
title: "Maltego — graf powiązań (OSINT)"
date: 2026-08-16
tags: [ive, i, osint, narzedzie, gui]
category: narzedzie
status: documented
---

# Maltego

**TL;DR**: narzędzie do **wizualizacji powiązań** między osobami, firmami, domenami,
IP, adresami e-mail — jako interaktywny graf (GUI). Nie instalowane tutaj (komercyjne/CE).

## Co to / do czego

Producent: Maltego Technologies. Dostępne wersje:

| Wersja | Cena | Uwagi |
|--------|------|-------|
| **Community Edition (CE)** | darmowa (rejestracja) | ograniczona liczba wyników/transform, do nauki |
| **Pro / Enterprise** | płatna | pełne transformy, zespoły, integracje |

- **Encje (Entities)**: Domain, IP, Email, Person, Phone, Company, Document…
- **Transformy**: zbierają dane z źródeł (DNS, WHOIS, Shodan, social, Threat Intelligence).
- **Graf**: łączy encje relacjami → mapa ataku / mapowanie kampanii.

## Typowy workflow

1. Startujesz od encji (np. domena C2).
2. Uruchamiasz transformy (DNS → subdomeny → IP → netblock → kontakty).
3. Graf pokazuje, **co jest powiązane z czym**.
4. Eksportujesz mapę do raportu.

## Dlaczego nie tutaj

- GUI (bez wyświetlacza na tym hoście), CE wymaga rejestracji.
- Dla automatyzacji w labie mamy [[Recon_ng_Analiza]] i [[Model_IVE/I_Informacja/SpiderFoot]]
  (headless), które robią podobny pivot bez GUI.

## Alternatywy headless

| Narzędzie | Notatka |
|-----------|---------|
| Recon-ng | [[Model_IVE/I_Informacja/Recon-ng]] |
| SpiderFoot | [[Model_IVE/I_Informacja/SpiderFoot]] |
| Maltego | to (GUI) |

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[OSINT_Toolkit]]
