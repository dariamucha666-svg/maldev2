---
title: "Acunetix — komercyjny skaner web"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, web, komercyjny]
category: narzedzie
status: documented
---

# Acunetix

**TL;DR**: komercyjny **skaner podatności aplikacji web** (i API) — wykrywa SQLi, XSS,
SSRF i in. (OWASP Top 10), z ładnym raportowaniem i niską liczbą false-positive.

## Co to / do czego

Producent: Invicti (dawniej Acunetix). Automatyczny DAST — crawler + scan engine,
wykrywa luki web, weryfikuje je (proof), raportuje z rekomendacjami.

| Cecha | Wartość |
|-------|---------|
| Producent | Invicti |
| Licencja | komercyjna (trial dostępny) |
| Cel | aplikacje web + API (REST/SOAP) |
| Silnik | crawler + scanner + proof-of-exploit |

## Dlaczego nie instalowane tutaj

- Komercyjne, wymaga licencji/trialu.
- Open-source'owe odpowiedniki w labie: [[Model_IVE/V_Podatnosci/OWASP_ZAP]] i
  [[Model_IVE/E_Eksploatacja/Nuclei]].

## Jak używać (ogólnie)

1. Zainstaluj (Windows/Linux) → Web UI.
2. New Target → URL (z fazy I).
3. Skan (crawl + audit) → lista luk z dowodami.
4. Eksport raportu → wpisz luki do fazy E.

## Porównanie web-skanerów

| Narzędzie | Cena | Headless | Notatka |
|-----------|------|----------|---------|
| Acunetix | komercyjne | tak | [[Model_IVE/V_Podatnosci/Acunetix]] |
| Burp Suite Pro | komercyjne | ograniczone | [[Model_IVE/V_Podatnosci/Burp_Suite]] |
| OWASP ZAP | darmowe | tak | [[Model_IVE/V_Podatnosci/OWASP_ZAP]] |
| Nuclei | darmowe | tak | [[Model_IVE/E_Eksploatacja/Nuclei]] |

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]]
