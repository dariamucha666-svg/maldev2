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

## Chaty → Obsidian (auto, od 16.08)

Nowy automat: 'Narzedzia/chatlog_to_obsidian.py' zbiera transkrypty TRZECH czatów
(DSH / Goose / Grok) i zapisuje je do 'Dzienniki/Chaty/' z analizą 'co zrobiono'.
Cron '/etc/cron.d/obsidian-chatlog' co 10 minut. Folder 'Dzienniki/Chaty/' jest w
'.gitignore' (surowe outputy narzędzi nie idą na publiczny GitHub). Sekrety redagowane.
Szczegóły: [[Chaty/README]].

## Lokalne skrypty logowania (ten vault, od 16.08)

`Narzedzia/log_to_obsidian.sh` i `Narzedzia/log_session.sh` — **samo-lokalizujące**
(skrypt mieszka w `<vault>/Narzedzia/`, więc działają na każdym komputerze;
nadpisz katalog przez `OBSIDIAN_VAULT`).

### log_to_obsidian.sh — wpis do Daily

```bash
log_to_obsidian.sh "Nagłówek" "treść"                 # Daily/YYYY-MM-DD.md
echo "treść" | log_to_obsidian.sh "Nagłówek"          # treść ze stdin
log_to_obsidian.sh --recap "Nagłówek" "treść"         # + Recap dnia
log_to_obsidian.sh --tag "lab,redteam" "..."          # tagi do frontmatteru
log_to_obsidian.sh --force "..."                      # omiń dedupe
log_to_obsidian.sh --commit "..."                     # + git commit
```

- tworzy plik dnia, gdy nie ma (frontmatter jak `_Templates/Dziennik_Lab`)
- **dedupe**: ten sam nagłówek + treść już są → skip (koniec spamowania typu
  „Pokrycie detekcji" ×4)
- **flock**: bezpieczne przy równoległych loggerach (DSH / Goose / Grok / cron)
- **redakcja sekretów**: linie z hasłami/tokenami/kluczami API są wycinane
- timestamp UTC `(YYYY-MM-DDTHH:MM:SSZ)` — jak reszta dziennika

Alias w `.bashrc`:

```bash
alias log="~/Obsidian/XMask/maldev2/Narzedzia/log_to_obsidian.sh"
```

### log_session.sh — nagrywanie całej sesji terminala

```bash
log_session.sh start "etykieta"   # nagrywa do Logs/terminal_YYYY-MM-DD.log,
                                  # na koniec (exit) dopisuje podsumowanie do Daily
log_session.sh status             # czy coś nagrywa
log_session.sh hook               # snippet do .bashrc: nagrywaj KAŻDY terminal
```

Auto-nagrywanie każdego terminala (koniec `.bashrc`):

```bash
if [[ $- == *i* ]] && [[ -t 0 ]] && [[ -z "${UNDER_OBSIDIAN_SCRIPT:-}" ]]; then
  export UNDER_OBSIDIAN_SCRIPT=1
  exec script -aqf "$HOME/Obsidian/XMask/maldev2/Logs/terminal_$(date -u +%F).log"
fi
```

### log_commands.sh — DOSŁOWNIE KAŻDA LINIA komend

Hook w `PROMPT_COMMAND` dopisuje po **każdej wpisanej komendzie** linię do
`Logs/commands_YYYY-MM-DD.log`:

```
2026-08-16T14:45:01Z  host  /katalog  $ komenda
```

```bash
log_commands.sh install   # dodaj hook do ~/.bashrc (raz, nowe terminale)
log_commands.sh hook      # sam snippet
log_commands.sh status    # czy hook aktywny
log_commands.sh test      # test zapisu
```

- łapie **każdą** komendę z **każdego** terminala (nie trzeba pamiętać o `start`)
- pełny transkrypt z **outputem** daje `log_session.sh` → `Logs/terminal_*.log`
- `Logs/commands_*.log` i `Logs/terminal_*.log` są w `.gitignore` — surowe linie
  (mogą zawierać hasła/infra) zostają lokalnie, nie idą na git

`Logs/terminal_*.log` = surowy zapis (jak `script` na `.133`). Sekrety nadal
**poza** vaultem — hasła/tokeny nie lądują ani w Daily, ani w Logs.
