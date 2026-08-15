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


## Od 15.08 wieczór — zakładka Obsidian

Klawiatura bota (po `/start`):

| Przycisk / komenda | Co robi |
|--------------------|---------|
| **📚 OBSIDIAN** `/obsidian` `/vault` | Foldery vaultu, liczby notatek, wejście w plik |
| **📋 PODSUMOWANIE \| Co już umiem?** `/podsumowanie` `/umiem` | Żywe podsumowanie: rodziny XMask, karty `Analizy/Malware`, backlog, stos RE |
| 🕒 Ostatnie | Notatki od najnowszych |
| `/szukaj fraza` | Pełnotekstowo |

Podsumowanie linkuje: [[Dla_Laika_Powtorka]] · [[Droga_przez_cyberbezpieczenstwo]] · [[Lab/Recap 2026-08-15]] · [[Backlog]].

Produkcja: `.133`, unit `obsidian-telegram-bot.service`, vault `/root/obsidian-vault`.
Username: `@Xmaskapp_bot`.

Recap sesji: [[Lab/Recap 2026-08-15]].

## Instagram (2026-08-15)

`/ig` — liczby / demografy / delta własnego konta Professional. [[Instagram_Graph_Bot]]

## Kanał — Z warsztatu (2026-08-15)

Regularny content marketing dla ludzi. `/kanal`. Kolejka w `state/channel_queue.json`. Cron `xmask-channel` 16:00 UTC.
Jak bot jest adminem kanału: `TELEGRAM_CHANNEL_ID=-100…` w `.env`.
Editorial: [[Warsztat/README]].
