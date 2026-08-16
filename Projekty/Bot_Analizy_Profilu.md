---
tags: [projekt, osint, telegram, googlebot]
date: 2026-08-16
updated: 2026-08-16
status: waiting-token
priority: medium
category: osint
---

# Bot analizy profilu publicznego

Powiązane: [[Dashboard]] · [[Backlog]] · [[Telegram_Obsidian_Bot]] · [[Instagram_Graph_Bot]]

Bot Telegram, który przyjmuje link do profilu publicznego w serwisie społecznościowym i analizuje stronę tak, jak robi to Googlebot. Zwraca tytuł, opis/bio, zdjęcie profilowe, domenę i status HTTP — wyłącznie na danych publicznych, bez logowania.

**Status:** kod gotowy, składnia zweryfikowana (`python -m py_compile` OK). Czeka na `TELEGRAM_BOT_TOKEN` z @BotFather.

> W vault jest już wcześniejszy, prostszy wariant: `Narzedzia/profile_analyzer_bot.py` (token `PROFILE_ANALYZER_BOT_TOKEN`). Ten projekt to samodzielna, pełniejsza wersja: nagłówki Googlebota, pobieranie zdjęcia jako obrazka, status HTTP, obsługa redirectów.

## Co robi

- Pobiera stronę z nagłówkami Googlebota (User-Agent + Accept + Accept-Language + Accept-Encoding)
- Wyciąga:
  - tytuł: `og:title` → `twitter:title` → fallback `<title>`
  - opis/bio: `og:description` → `twitter:description` → `description`
  - zdjęcie: `og:image` → `twitter:image` → `twitter:image:src` (rozwiązuje względne adresy przez `urljoin`)
  - domena: `urlparse(final_url).netloc` (po redirectach)
  - status HTTP z odpowiedzi `requests`
- Wysyła zdjęcie profilowe jako obrazek z podpisem (jeśli jest; weryfikacja `Content-Type: image/*`, limit 10 MB)
- Gdy brak zdjęcia — odpowiada samym tekstem

Komendy: `/start`, `/help`, plus dowolny link lub sama domena.

## Kod

- `telegram-profil-bot/bot.py` — główny bot
- `telegram-profil-bot/requirements.txt` — `requests`, `beautifulsoup4`, `python-telegram-bot`
- `telegram-profil-bot/README.md` — instrukcja
- `telegram-profil-bot/.env.example` — szablon tokena

Token **poza** vaultem (repo może być publiczne):

```bash
export TELEGRAM_BOT_TOKEN="..."
```

## Uruchomienie

```bash
cd telegram-profil-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

## Status

- [x] Kod bota
- [x] Składnia (`py_compile`)
- [ ] Token + pierwszy test na żywo

## Powiązane

- [[Dashboard]]
- [[Backlog]]
- [[Telegram_Obsidian_Bot]]
- [[Instagram_Graph_Bot]]

