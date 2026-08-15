---
tags:
  - obsidian
  - workflow
  - logs
updated: 2026-08-14
---

# Auto-log Obsidian (.133)

Powiązane: [[Obsidian_Workflow]] · [[Telegram_Obsidian_Bot]] · [[Pipeline_Analizy]]

Na `5.175.189.133` vault `/root/obsidian-vault` zbiera logi sam.

## Katalogi

| Folder | Treść |
|--------|--------|
| `Logs/` | terminal, pipeline, sliver journal |
| `Analizy/Raporty/` | sklejone `.md` z `/root/samples/reports` |
| `Screenshots/` | zrzuty (na Linux prawie puste; pełne na `.57`) |

## Terminal

`.bashrc` odpala `script -aqf` tylko gdy:

- sesja interaktywna (`$-` zawiera `i`)
- jest TTY
- nie ustawiono `UNDER_OBSIDIAN_SCRIPT` / `SCRIPT`

Plik dnia: `Logs/terminal_YYYY-MM-DD.log`.

Wyłączenie na jedną sesję:

```bash
UNDER_OBSIDIAN_SCRIPT=1 bash
```

## Pipeline

`/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh` jest wołany na końcu `pipeline.sh`.

## Sliver

Unit `sliver.service` **nie jest ruszany** (zostaje `sliver-server daemon`). Journald nie ma wpisów — log jest w `/root/.sliver/logs/sliver.log` (~75 MB).

| Cron | Co |
|------|-----|
| `obsidian-sliver-log` | ostatnie 80 linii `sliver.log` → `Logs/sliver_YYYY-MM-DD.log` |
| `obsidian-sliver-sessions` | `export_sliver_to_obsidian.sh` → [[sessions]] |

Całego `sliver.log` / `audit.json` / tabeli `credentials` nie kopiujemy.

## Telegram

Bot dopisuje do `Dzienniki/Telegram/YYYY-MM-DD.md` (patrz [[Automatyzacja]]).

Hasła i tokeny nadal **poza** vaultem.

## Haczyk sesji (Grok / Goose)

Ręczne / agentowe dopiski do Daily (to, czego cron nie widzi: czat, werdykt, nowa sesja):

`Narzedzia/log_to_obsidian.sh` → `Daily/YYYY-MM-DD.md` (`--recap` też `Lab/Recap YYYY-MM-DD.md`).

Goose: env `GOOSE_MOIM_MESSAGE_FILE=/root/.config/goose/top_of_mind.md` (w `deepseek.env`). Nowe sesje to łapią; stara sesja Goose wymaga restartu okna, żeby wczytać tom.
