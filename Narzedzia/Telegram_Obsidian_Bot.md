---
date: 2026-08-14
tags: [telegram, obsidian, workflow]
source: local
updated: 2026-08-14
---

# Telegram ↔ Obsidian Bot

Kod: `/home/kali/Desktop/obsidian-telegram-bot`

Bot na Telegramie zapisuje i czyta ten vault (`/home/kali/obsidian-vault`).

## Start

```bash
cd /home/kali/Desktop/obsidian-telegram-bot
# token od @BotFather do .env jako TELEGRAM_BOT_TOKEN=
./run.sh
```

## 24/7

Na VPS `.133`: `systemctl enable --now obsidian-telegram-bot`  
Jedna instancja pollingu — nie odpalaj równolegle na Kali.

## Komendy

| Komenda | Co robi |
|---------|---------|
| `/dashboard` `/wirus` | Pipeline + opis wirusa |
| `/xmask` `/post` | Gotowce na kanał XMask |
| `/nowa` | Nowa notatka (tytuł, folder, treść) |
| `/dziennik tekst` | Dopisek do [[Daily]] |
| zwykła wiadomość | Plik w `Inbox/` |
| `/notatki` `/szukaj` `/otworz` | Przeglądanie |
| `/dopisz` | Akapit do istniejącej notatki |
| `/foldery` | Katalogi |

Hasła i tokeny **nie** idą do vaultu — token bota siedzi w `.env` poza sejfem.

Zobacz też [[Obsidian_Workflow]].
