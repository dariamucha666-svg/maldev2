---
title: "Google Dorks — operatory wyszukiwania"
date: 2026-08-16
tags: [ive, i, osint, technika]
category: narzedzie
status: documented
---

# Google Dorks

**TL;DR**: zaawansowane **operatory wyszukiwania Google**, które odkrywają publicznie
dostępne, wrażliwe dane (logi, panele, pliki, kamery) — to technika, nie program.

## Co to / do czego

Google indeksuje ogrom sieci. Odpowiednie operatory pozwalają wyciągnąć z indeksu
rzeczy, których właściciele nie zamierzali publikować.

## Najważniejsze operatory

| Operator | Działanie |
|----------|-----------|
| `site:cel.com` | tylko ta domena/subdomeny |
| `filetype:pdf` / `ext:sql` | konkretny typ pliku |
| `intitle:` / `inurl:` | fraza w tytule / URL |
| `intext:` | fraza w treści |
| `cache:` | wersja z cache |
| `-` | wykluczenie (np. `-site:github.com`) |
| `"` | dokładna fraza |

## Przykłady dorków

```
site:cel.com filetype:pdf
site:cel.com intitle:"index of"
site:cel.com inurl:admin
filetype:env "DB_PASSWORD"
intitle:"webcam" inurl:view
```

## Baza dorków

- **GHDB** (Google Hacking Database) — exploit-db.com/google-hacking-database (kategorie: files, passwords, webcams…).
- **osintframework.com** — index (patrz [[Model_IVE/I_Informacja/OSINT_Framework]]).

## Uwagi

- Używaj **tylko do własnych assetów / autoryzowanego reconu**.
- Google limituje zapytania (CAPTCHA) — rozłóż je w czasie.

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[Model_IVE/I_Informacja/Shodan]] · [[Model_IVE/I_Informacja/OSINT_Framework]]
