---
title: "Sherlock — wyszukiwanie nicków (300+ platform)"
date: 2026-08-16
tags: [ive, i, osint, narzedzie]
category: narzedzie
status: active
---

# Sherlock

**TL;DR**: sprawdza, czy dany **username** istnieje na **300+ platformach** (social,
fora, usługi) — do śledzenia tożsamości/operatora.

## Co to / do czego

Projekt sherlock-project. Python, MIT. Wysyła zapytania HTTP do setek serwisów i
raportuje, gdzie nick istnieje (kod statusu + czas odpowiedzi).

| Cecha | Wartość |
|-------|---------|
| Język / licencja | Python 3 · MIT |
| Platformy | 300+ (GitHub, Twitter/X, Instagram, Reddit, fora…) |
| Output | konsola + CSV (`--csv`) |
| Tor | opcjonalnie przez `stem` |

## Instalacja (vserver959630)

```bash
git clone --depth 1 https://github.com/sherlock-project/sherlock /opt/ive/sherlock
/opt/ive/venv/bin/pip install /opt/ive/sherlock
# binarka: /opt/ive/venv/bin/sherlock
```

## Analiza dynamiczna (2026-08-16)

**Wersja**: Sherlock **0.16.1**.

**Demo** (1 strona, GitHub, nieistniejący nick — bezpieczne):

```
[*] Checking username nonexistent_test_user_9f8e7d on:
[*] Search completed with 0 results
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`sherlock_help.txt\`,
\`sherlock_demo.txt\`, \`sherlock_demo.csv\`).

## Użycie

```bash
sherlock jakisnick
sherlock jakisnick --csv wyniki.csv
sherlock jakisnick --site GitHub --site Reddit   # tylko wybrane strony
sherlock jakisnick --timeout 3                    # szybsze (mniej pewne)
```

## Wynik → gdzie dalej

- Znaleziony nick → szukaj e-maili/domen ([[Model_IVE/I_Informacja/theHarvester]]),
  profilów ([[Model_IVE/I_Informacja/Maltego]]).

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[OSINT_Toolkit]]
