---
date: 2026-08-14
tags: [telegram, obsidian, workflow]
source: local
updated: 2026-08-15
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
| `/status` | Liczby: próbki, role, sesje Sliver |
| `/pobierz <hash>` | Ściąga próbkę (MalwareBazaar → kwarantanna), śledzi job |
| `/klasyfikuj <hash>` | Pokazuje rolę albo odpala pipeline |
| `/alerty` | Ostatnie RAT/stealer. Pipeline sam pisze przy nowym trafieniu. |
| `/xmask` `/post` | Gotowce na kanał XMask |
| `/nowa` | Nowa notatka (tytuł, folder, treść) |
| `/dziennik tekst` | Dopisek do [[Daily]] |
| zwykła wiadomość | Plik w `Inbox/` **oraz** dopisek w `Dzienniki/Telegram/YYYY-MM-DD.md` |
| `/notatki` `/szukaj` `/otworz` | Przeglądanie |
| `/dopisz` | Akapit do istniejącej notatki |
| `/foldery` | Katalogi |

Hasła i tokeny **nie** idą do vaultu — token bota siedzi w `.env` poza sejfem.

Od 2026-08-15: IoC czytane z lokalnego `iocs.json` (cache 20 s), indeks vaultu 5 s, `httpx` nie loguje getUpdates (token nie wylewa się do journald).

Karta sesji 15.08 (UI, joby, alerty): [[Dashboard_Bot_Lab]].

Zobacz też [[Obsidian_Workflow]].
