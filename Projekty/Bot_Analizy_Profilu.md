---
tags: [projekt, osint, telegram, googlebot]
date: 2026-08-16
updated: 2026-08-16
status: active
priority: medium
category: osint
---

# Bot analizy profilu publicznego

Powiązane: [[Dashboard]] · [[Backlog]] · [[Telegram_Obsidian_Bot]] · [[Instagram_Graph_Bot]]

Analizator publicznego profilu w serwisie społecznościowym — pobiera stronę jak Googlebot i zwraca tytuł, opis/bio, zdjęcie profilowe, domenę i status HTTP. Wyłącznie publiczne dane, bez logowania.

**Status:** ✅ wdrożony jako komenda `/profil` w głównym bocie XMask (`@Xmaskapp_bot`). Serwis `obsidian-telegram-bot.service` działa, logi czyste, przetestowany na żywym publicznym profilu (status 200, zdjęcie pobrane).

## Gdzie to jest

- moduł: `/root/obsidian-telegram-bot/profile_analyzer.py`
- handler `/profil` (+ alias `/profile`) w `/root/obsidian-telegram-bot/bot.py`
- zależności `requests` + `beautifulsoup4` doinstalowane do venv bota
- token: ten sam co główny bot, już w `/root/obsidian-telegram-bot/.env` (poza vaultem)

## Co robi `/profil`

- pobiera stronę nagłówkami Googlebota (User-Agent + Accept + Accept-Language + Accept-Encoding)
- wyciąga:
  - tytuł: `og:title` → `twitter:title` → fallback `<title>`
  - opis/bio: `og:description` → `twitter:description` → `description`
  - zdjęcie: `og:image` → `twitter:image` → `twitter:image:src` (względne adresy przez `urljoin`)
  - domena: `urlparse(final_url).netloc` (po redirectach)
  - status HTTP
- wysyła zdjęcie jako obrazek z podpisem (weryfikacja `Content-Type: image/*`, limit 10 MB)
- bez zdjęcia odpowiada samym tekstem

Komenda: `/profil <link>`.

## Status

- [x] Kod (moduł + handler)
- [x] Zależności w venv bota
- [x] Restart serwisu + logi czyste
- [x] Test na żywym publicznym profilu
- [x] `/profil` w menu komend bota

## Powiązane

- [[Dashboard]]
- [[Backlog]]
- [[Telegram_Obsidian_Bot]]
- [[Instagram_Graph_Bot]]

