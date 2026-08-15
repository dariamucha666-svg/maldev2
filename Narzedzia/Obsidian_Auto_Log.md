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

Cron `obsidian-sliver-log` dopisuje **ostatnie 80 linii** do `Logs/sliver_YYYY-MM-DD.log`. Całego `sliver.log` / `audit.json` nie kopiujemy (dysk 78%).

Hasła i tokeny nadal **poza** vaultem.
