---
tags: [projekt, instagram, osint, telegram]
date: 2026-08-15
updated: 2026-08-16
status: waiting-token
priority: medium
category: social-graph
---

# Bot Instagram — obserwowani / obserwujący

Powiązane: [[Telegram_Obsidian_Bot]] · [[Daily/2026-08-15]] · [[Historia]] · [[Obsidian_Workflow]]

**Status:** konto **@zamaskowanyeu** (`zamaskowany`). Wpięte w `/ig`. Czeka na `IG_ACCESS_TOKEN`. Bez scrapera, bez listy nicków.

Publiczny profil istnieje (nazwa wyświetlana: zamaskowany). Token Graph nadal pusty — liczb z API nie ma.

> **Zweryfikowano 2026-08-16:** kod `instagram.py` (Graph API) i handlery `/ig` w `bot.py` są gotowe i działają offline (test: import OK, obcy nick odmówiony, formatowanie OK). `IG_ACCESS_TOKEN` pusty (długość 0) — brakuje tylko tokenu z Meta Developers. Po wklejeniu tokenu: restart bota + pierwszy snapshot do [[Historia]].

## Co robi `/ig`

- liczby: obserwujący / obserwowane / posty
- demografy (gender / age / country) jeśli API je odda (zwykle ≥100 followers)
- follows/unfollows jako agregat dnia
- delta vs poprzedni snapshot
- zapis: `Projekty/Instagram/Historia.md` + `Daily/`

Komendy: `/ig` `/ig last` `/ig setup`. Cudzy nick → odmowa.

Kod: `/root/obsidian-telegram-bot/instagram.py` · handlery w `bot.py`.
Snapshoty JSON: `/root/obsidian-telegram-bot/state/instagram/` (nie vault, mogą mieć ID).

## Setup tokenu (Twoje konto Professional)

1. IG → Professional (Creator/Business).
2. Meta app typu Business: https://developers.facebook.com/apps
3. Instagram → *API setup with Instagram business login* → Generate token (60 dni).
4. W `/root/obsidian-telegram-bot/.env`:

```
IG_ACCESS_TOKEN=...
IG_GRAPH_BASE=https://graph.instagram.com
IG_GRAPH_VERSION=v25.0
```

5. `systemctl restart obsidian-telegram-bot`
6. W TG: `/ig`

Token **poza** vaultem.

## Czego nie ma

- lista nicków followers/following
- analiza obcego `@user`
- instagrapi / instaloader / Selenium
