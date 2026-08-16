---
title: "OpenVAS / Greenbone — darmowy skaner podatności"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, open-source]
category: narzedzie
status: documented
---

# OpenVAS (Greenbone Community Edition)

**TL;DR**: darmowy, otwartoźródłowy skaner podatności — open-source'owy odpowiednik
Nessusa. Najprościej stawia się go przez **Docker**.

## Co to / do czego

Greenbone Vulnerability Management (dawniej OpenVAS). Skanuje hosty/sieci, używa
codziennie aktualizowanych **Network Vulnerability Tests (NVT)** (~100k+ testów).

| Cecha | Wartość |
|-------|---------|
| Licencja | AGPL (open-source) |
| Komponenty | gvmd, openvas-scanner, ospd, notus, PostgreSQL |
| Interfejs | Web UI (Greenbone Security Assistant, https://localhost:9392) |
| Feed | NVTs + SCAP + CERT |

## Instalacja (Docker — zalecana)

```bash
git clone https://greenbone.github.io/docs/latest/_static/docker-compose.yml
docker compose -f docker-compose.yml up -d
# UI: https://127.0.0.1:9392  (admin / admin — zmień od razu!)
```

> ⚠️ **Nie instalowane tutaj**: pełny stack Greenbone (PostgreSQL + scanner + gvmd)
> potrzebuje **kilku GB RAM** i długiej inicjalizacji feedu. Ten host (vserver959630,
> ~5.8 GiB RAM, ~1.5 GiB wolne) to za mało — zostawiam jako dokumentację. W razie
> potrzeby postaw na dedykowanym VM/dużym VPS.

## Jak używać (ogólnie)

1. Poczekaj na pobranie/aktualizację feedu (pierwszy raz potrafi trwać godzinę).
2. Web UI → Scans → New Task → cel (z fazy I).
3. Wynik: luki (CVSS, opis, rozwiązanie) → eksport do fazy E.

## Wynik → gdzie dalej

- CVE → [[Model_IVE/E_Eksploatacja/Metasploit]].
- Porównanie z [[Model_IVE/V_Podatnosci/Nessus]].

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]]
