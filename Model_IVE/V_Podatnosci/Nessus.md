---
title: "Nessus — skaner podatności (Tenable)"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, komercyjny]
category: narzedzie
status: documented
---

# Nessus

**TL;DR**: jeden z najpopularniejszych komercyjnych skanerów podatności — wykrywa
**65k+ luk** (CVE, misconfig, weak creds). Producent: Tenable.

## Co to / do czego

Skaner sieciowo-hostowy. Odpytuje usługi, porównuje banery/wersje z bazą pluginów
(65 000+), zwraca listę luk z CVSS i rekomendacjami.

| Cecha | Wartość |
|-------|---------|
| Producent | Tenable |
| Licencja | komercyjna; **Essentials** = darmowa (do **16 IP**, rejestracja) |
| Pluginy | 65k+ (rodziny: SSL, Web, DB, OS, misconfig…) |
| Interfejs | Web UI (https://localhost:8834) |
| Skan | credentialed / non-credentialed |

## Dlaczego nie instalowane tutaj

- Wymaga rejestracji (Essentials) lub licencji (Pro/Manager).
- Binarne pakiety, nie open-source.

## Jak używać (ogólnie)

1. Pobierz z tenable.com (Essentials/Pro), zainstaluj na maszynie/VM.
2. Web UI → New Scan → cel (z fazy I).
3. Credentialed scan (login) daje dużo głębsze wyniki (łatki, konfiguracja).
4. Raport → eksport (CSV/PDF) → wpisuj luki do fazy E.

## Wynik → gdzie dalej

- CVE na usłudze → [[Model_IVE/E_Eksploatacja/Metasploit]] (czy jest exploit).
- Web luki → [[Model_IVE/V_Podatnosci/Burp_Suite]] / [[Model_IVE/V_Podatnosci/OWASP_ZAP]].

## Open-source alternatywa

- [[Model_IVE/V_Podatnosci/OpenVAS]] (Greenbone) — darmowy odpowiednik.

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]]
