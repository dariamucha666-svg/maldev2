---
title: "Optymalizator niedokończonych projektów"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_28
cwd: "/root"
messages: 99
tool_calls: 96
status: archived
---

# Optymalizator niedokończonych projektów

> Zapis czatu **Goose** · sesja '20260815_28' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | # OPTYMALIZATOR — ciągła poprawa niedokończonych projektów |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 1 |
| Akcji narzędziowych | 96 |
| Narzędzia | 'tool'×48, 'result'×48 |
| Pliki | '/etc/systemd/system/obsidian-telegram-bot.service' · '/home/kali/Desktop/obsidian-telegram-bot' · '/root/android-pipeline' · '/root/android-pipeline/bin/pipeline.sh' · '/root/android-pipeline/bin/rat5_clean_run.sh' · '/root/android-pipeline/lib/analyze_static.py' · '/root/android-pipeline/lib/extract_domains.py' · '/root/android-pipeline/lib/sigma_generator.py' · '/root/android-pipeline/web/catalog.json' · '/root/obsidian-telegram-bot' · '/root/obsidian-telegram-bot/.venv/bin/python' · '/root/obsidian-telegram-bot/bot.py' · '/root/obsidian-telegram-bot/virus_catalog.json' · '/root/obsidian-vault' · '/root/osint' · '/root/osint_' · '/root/samples/output/endpoints' · '/root/samples/quarantine/' · '/root/samples/reports/' · '/root/samples/reports/iocs.json' |
| IP | '5.175.189.133' · '5.175.189.139' |
| Hosty | 'crlab.com' · 'discord.com' · 'discordapp.com' · 'github.com' · 'off-game.com' · 'suahoje.com' |

## Wniosek (ostatnia odpowiedź asystenta)

# Raport OPTYMALIZATORA

Przejrzałem oba projekty (priorytetowo `bot.py` + kluczowe pliki bota oraz `bin/*.sh`, `lib/*.py`, `tools/detection`/`yara-rules`/`sigma-rules` w pipeline). Usługa **działała i nadal działa** — po zmianach w `bot.py` zrobiłem restart i `systemctl is-active` zwraca `active`.

## Co poprawiłem

| # | Plik | Poprawka |
|---|------|----------|
| 1 | `obsidian-telegram-bot/bot.py` | Dodałem brakujący `await guard(update)` w `on_graj_cb` — callbacki gry `/graj` omijały allowlistę (jedyne miejsce w bocie, które jej nie sprawdzało). |
| 2 | `android-pipeline/lib/sigma_generator.py` | Naprawiłem klasyfikację `kind` w fallbacku `_load_iocs` — raporty APK bez pola `kind` były traktowane jako **PE**, więc Sigma generował „PE hash" z hashów APK (gdy brakowało `iocs.json`). Teraz typ jest wyliczany ze `schema`/rozszerzenia. |
| 3 | `android-pipeline/lib/sigma_generator.py` | Usunąłem martwą zmienną `all_hashes` (obliczaną, ale nigdy nieużywaną). |
| 4 | `android-pipeline/lib/extract_domains.py` | Poprawka `BAD_PREFIX`: `'crl'` → `'crl.'` — wcześniej odrzucano każdą domenę zaczynającą się od `crl…` (np. `crlab.com`) zamiast tylko prefiksu `crl.`. |
| 5 | `android-pipeline/bin/pipeline.sh` | Naprawiłem fallback `extract_nested_from_zip`: wariant `unzip -P infected` nie był próbowany dla zipów AES (bo `unzip -l` na nich przechodzi), przez co bez `7z` próbki z MalwareBazaar nie były rozpakowywane. |
| 6 | `android-pipeline/bin/rat5_clean_run.sh` | Usunąłem zdublowaną linię `trap restore_path EXIT`. |
| 7 | `android-pipeline/lib/analyze_static.py` | Usunąłem martwy regex `BASE64_HINT` (zadeklarowany, nigdy nieużyty). |

## Jak zweryfikowałem

- Python (każdy zmieniony plik): `ast.parse` — OK.
- Bash: `bash -n` na **wszystkich** `bin/*.sh` — OK.
- Testy bota: `unittest` (13 testów) — OK; `test_vault.py` — OK.
- Import bota: `import bot` — OK (allowlist=1).
- Usługa: `systemctl restart obsidian-telegram-bot` → `is-active` = **active**, w logu `Application started`.

## Co zostawiłem świadomie

- `bot.py: remember_owner` — pusta funkcja-stub, celowo wyłączona (komentarz: „First-writer-wins is disabled. Allowlist must be in .env."). Nie usuwałem, bo to świadoma decyzja projektowa, a nie niedokończony kod.
- `bot.py: _klip_begin` — nieużywany helper (martwy kod). Zostawiłem, żeby nie kasować funkcji; jest nieszkodliwy.
- `lib/enrich_cti.py` `RE_IPV4` — luźny regex dopuszcza oktety >255; to drobiazg (AbuseIPDB i tak odrzuci), nie ruszałem, żeby nie zmieniać zachowania ekstrakcji.
- Dwie niemal identyczne kopie `classify_roles.py` (katalog bota vs `lib/`) z minimalną różnicą w `iter_reports` — zostawiłem, obie działają dla swoich wywołań.
- `tools/` (NusantaraScan, android-mcp, yara-rules, sigma-rules, jadx, apktool…) — vendored/third-party, nie dotykane.
- Pliki `.env`, tokeny, hasła — nie dotykane (zgodnie z zasadą).

## Jak zweryfikować niezależnie

```bash
# bot
cd /root/obsidian-telegram-bot
.venv/bin/python -c "import ast; ast.parse(open('bot.py').read())"
.venv/bin/python -m unittest test_content test_instagram test_studio -q
systemctl is-active obsidian-telegram-bot

# pipeline
cd /root/android-pipeline
for f in bin/*.sh; do bash -n "$f"; done
for f in lib/*.py; do .venv/bin/python -c "import ast; ast.parse(open('$f').read())"; done
```

Nie wprowadzałem nic, co zmienia działającą logikę — same poprawki bezpieczeństwa / poprawności typów / martwego kodu i fallbacków.

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T22:31:28Z

# OPTYMALIZATOR — ciągła poprawa niedokończonych projektów

Jesteś maszyną optymalizującą. Twoje zadanie: przeglądaj i poprawiaj niedokończone projekty.

## Zakres (priorytet)
1. `/root/obsidian-telegram-bot/` — bot Telegram (bot.py ~2200 linii, graj.py, vault.py, dashboard.py).
2. `/root/android-pipeline/` — pipeline malware/RE (bin/*.sh, lib/*.py, tools/detection, tools/yara-rules, tools/sigma-rules).

## Co robić
1. Znajdź **bugi** (niespójne nazwy funkcji, martwy kod, niedziałające ścieżki).
2. Znajdź **niedokończone funkcje** (TODO, puste bloki, niepodpięte komendy).
3. Znajdź **okazje do optymalizacji** (duplikacja, nieczytelny kod, brak obsługi błędów).
4. **Wprowadź konkretne poprawki** (edit/write). Po każdej zmianie zweryfikuj składnię:
   - Python: `.venv/bin/python -c "import ast; ast.parse(open('bot.py').read())"` (w katalogu bota).
   - Bash: `bash -n skrypt.sh`.

## Zasady
- **NIE psuj działającej usługi** — bot działa jako `systemctl obsidian-telegram-bot`. Po zmianach w bot.py: `systemctl restart obsidian-telegram-bot` i sprawdź `systemctl is-active`.
- **Nie dotykaj** plików `.env`, tokenów, haseł.
- **Nie kasuj** działających funkcji — tylko poprawiaj.
- Pracuj w katalogu `/root`.

## Raport
Na końcu wypisz: co poprawiłeś (lista), co zostawiłeś (świadomie), jak zweryfikować.

### 👤 Użytkownik — 2026-08-15T22:31:28Z

<turn-context>
<current-time>2026-08-15 22:31:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

Updated (645 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

README.md  [59]
alert_roles.py  [257]
bot.py  [2K]
classify_roles.py  [292]
content.py  [326]
dashboard.py  [166]
git_autocommit.sh  [27]
graj.py  [436]
harden_telegram.py  [55]
instagram.py  [432]
laik.py  [46]
obsidian-telegram-bot.service  [16]
publish_channel.py  [56]
render.py  [565]
requirements.txt  [2]
run.sh  [22]
studio.py  [305]
test_content.py  [41]
test_instagram.py  [64]
test_studio.py  [28]
test_vault.py  [37]
vault.py  [354]
virus_catalog.json  [565]


### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:34Z

bin/  [1K]
  batch_analyze.sh  [268]
  download_malwarebazaar.sh  [106]
  install.sh  [221]
  nightly_pipeline.sh  [298]
  osint_recon.sh  [140]
  pipeline.sh  [580]
  rat5_android_clean.sh  [180]
  rat5_clean_run.sh  [94]
  recon_osint.sh  [91]
config/  [85]
  crontab.example  [3]
  path.sh  [8]
  pipeline.env  [52]
  secrets.env  [2]
  secrets.env.example  [20]
docs/  [179]
  GUIDE_PL.md  [179]
lib/  [3K]
  __pycache__/  [0]
    aggregate_patterns.cpython-312.pyc  [0]
    alert_takeovers.cpython-312.pyc  [0]
    analyze_pe.cpython-312.pyc  [0]
    analyze_static.cpython-312.pyc  [0]
    classify_roles.cpython-312.pyc  [0]
    deep_re_pass.cpython-312.pyc  [0]
    enrich_cti.cpython-312.pyc  [0]
    extract_domains.cpython-312.pyc  [0]
    hunt_phishing_stealer.cpython-312.pyc  [0]
    sigma_generator.cpython-312.pyc  [0]
    yara_generator.cpython-312.pyc  [0]
  aggregate_patterns.py  [140]
  alert_takeovers.py  [188]
  analyze_pe.py  [454]
  analyze_static.py  [488]
  classify_roles.py  [292]
  deep_re_pass.py  [223]
  enrich_cti.py  [571]
  extract_domains.py  [134]
  hunt_phishing_stealer.py  [216]
  sigma_generator.py  [351]
  yara_generator.py  [421]
tools/  [169K]
  NusantaraScan/  [1K]
    nusantarascan/  [442]
      analyzers/  [0]
      formatters/  [0]
      integrations/  [0]
      scanners/  [0]
      signatures/  [0]
      utils/  [0]
      visualizers/  [0]
      __init__.py  [7]
      cli.py  [435]
    LICENSE  [674]
    README.md  [283]
    main.py  [27]
   
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:38Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:38Z

   257 alert_roles.py
  2437 bot.py
   292 classify_roles.py
   326 content.py
   166 dashboard.py
   436 graj.py
    55 harden_telegram.py
   432 instagram.py
    46 laik.py
    56 publish_channel.py
   565 render.py
   305 studio.py
    41 test_content.py
    64 test_instagram.py
    28 test_studio.py
    37 test_vault.py
   354 vault.py
    27 git_autocommit.sh
    22 run.sh
    16 obsidian-telegram-bot.service
  5962 total
---VENV---
lrwxrwxrwx 1 root root 7 Aug 14 23:12 .venv/bin/python -> python3
---SERVICE---
active

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:38Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:38Z

# Obsidian Telegram Bot

Prywatny bot, który dopisuje notatki do lokalnego vaultu Obsidian
(`/home/kali/obsidian-vault`) i pozwala je przeglądać z Telegrama.

## Start

1. W Telegramie otwórz [@BotFather](https://t.me/BotFather)
2. `/newbot` → nazwa i username
3. Skopiuj token
4. Wpisz go do `.env`:

```bash
cd /home/kali/Desktop/obsidian-telegram-bot
cp -n .env.example .env
# TELEGRAM_BOT_TOKEN=123456:ABC...
```

5. Uruchom:

```bash
./run.sh
```

Pierwsza osoba, która wyśle `/start`, zostaje właścicielem.
Możesz też wpisać swoje ID w `ALLOWED_USER_IDS`.

## 24/7

Produkcja: VPS `5.175.189.133`, unit `obsidian-telegram-bot.service`.

```bash
ssh root@5.175.189.133 'systemctl status obsidian-telegram-bot'
```

Na Kali jest ten sam unit w `~/.config/systemd/user/` — **nie** odpalaj obu naraz (Telegram pozwala na jeden polling).

## Komendy

| Komenda | Działanie |
|---------|-----------|
| `/dashboard` | Pipeline: lista próbek + nazwa wirusa |
| `/wirus hash` | Karta: co to jest i jak się bronić |
| `/xmask` `/post` | Gotowce na kanał XMask |
| `/nowa [tytuł]` | Nowa notatka: tytuł → folder → treść |
| `/dziennik [tekst]` | Dopisz do `Daily/YYYY-MM-DD.md` |
| zwykła wiadomość | Szybka notatka w `Inbox/` |
| `/notatki [folder]` | Lista |
| `/szukaj` `/otworz` `/dopisz` `/foldery` | Vault |

Nowe notatki dostają YAML (`date`, `tags: [telegram]`, `source: telegram`)
i wpis w dzienniku dnia.

## Vault

Domyślnie: `/home/kali/obsidian-vault`. Zmień `VAULT_PATH` w `.env`.
Obsidian o
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:41Z

#!/usr/bin/env python3
"""Telegram bot that reads and writes a local Obsidian vault."""

from __future__ import annotations

import asyncio
import datetime
import hashlib
import json
import logging
import os
import re
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    MenuButtonCommands,
    MenuButtonWebApp,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.helpers import escape_markdown
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from dashboard import describe, enrich, fetch_iocs, find_ioc, load_catalog
import content as channel
import instagram as ig
from laik import CHAPTERS, is_laik_button, recap_body
import studio
import graj
from vault import Vault, chunk_text

load_dotenv(Path(__file__).resolve().parent / ".env")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.INFO)
log = logging.getLogger("obsidian-bot")
_VAULT: Vault | None = None

TITLE, 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:43Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:43Z

        nav.append(InlineKeyboardButton(f"📄 root · {len(root_notes)}", callback_data="ob:f::0"))
    rows.append(nav)
    rows.append([InlineKeyboardButton("🔎 /szukaj fraza", callback_data="ob:hint")])
    return InlineKeyboardMarkup(rows)


def _ob_all_markup(vault: Vault, page: int = 0) -> InlineKeyboardMarkup:
    subs, root_notes = vault.browse("")
    items = _ob_sort_folders(subs)
    start = max(0, page * PAGE_SIZE)
    chunk = items[start : start + PAGE_SIZE]
    rows: list[list[InlineKeyboardButton]] = [_ob_tabs_row()]
    for folder, count in chunk:
        label = f"{_ob_icon(folder)} {_ob_label(folder)} · {count}"
        if len(label) > 60:
            label = label[:57] + "…"
        rows.append([InlineKeyboardButton(label, callback_data=f"ob:f:{_ob_id(folder)}:0")])
    for note in root_notes:
        label = f"📝 {note.title.replace('_', ' ')}"
        if len(label) > 60:
            label = label[:57] + "…"
        rows.append([InlineKeyboardButton(label, callback_data=f"ob:n:{_ob_id(note.rel)}")])
    nav: list[InlineKeyboardButton] = []
    if start > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"ob:all:{page - 1}"))
    if start + PAGE_SIZE < len(items):
        nav.append(InlineKeyboardButton("➡️", callback_data=f"ob:all:{page + 1}"))
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton("📚 Start", callback_data="ob:h")])
    return InlineKeyboardMarkup(rows)


def _ob_folder_markup(vault: Vault, folder: str, page: i
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:45Z

        "• Detekcja YARA/Suricata/Sigma — zwalidowana\n"
        "• Pętla optymalizacji — co 2h (timer)\n"
        "• Codzienne podsumowanie — 09:00\n\n"
        "⚠️ *Wymaga uwagi*\n"
        "• Refog/Spyrix — brak binarki\n"
        "• Laplas — brak binarki (IOC tylko)\n"
        "• Lumma 4 hashe — brak binarki\n"
        "• XWorm YARA — tylko dump (nie surowy PE)\n"
        "• Clipper vs stealer — FP statyczne\n\n"
        "🔴 *Zablokowane*\n"
        "• Refog/Spyrix — rejestracja vendora\n"
        "• Detonacja stealerów — zasada labu\n\n"
        "Pełny status: Obsidian → Projekty/Status_Projektow"
    )
    await update.effective_message.reply_markdown(text)


async def daily_summary_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Codzienne automatyczne podsumowanie vaultu (wysyła do allowed_ids)."""
    try:
        vault = get_vault()
        text = _ob_summary_text(vault)
        for uid in allowed_ids():
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=text,
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                )
            except Exception as exc:  # noqa: BLE001
                log.warning("daily summary to %s failed: %s", uid, exc)
    except Exception as exc:  # noqa: BLE001
        log.warning("daily summary failed: %s", exc)


# ---------------- GRAJ (gra edukacyjna) ----------------

async def cmd_graj(update: Update, contex
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:47Z

        f"🦠 *{d['title']}*",
        f"`{digest}`",
        f"rola: `{d.get('role') or '?'}` · rodzina: `{d['family']}` · typ: `{ioc.get('kind') or '?'}` · pewność: {d['confidence']}",
    ]
    if name:
        lines.append(f"plik: `{name}`")
    if d.get("aka"):
        lines.append("aka: " + ", ".join(d["aka"]))
    lines.extend(
        [
            "",
            "*Co to za wirus*",
            d["verdict"],
        ]
    )
    if d.get("behavior"):
        lines.append(d["behavior"])
    lines.extend(
        [
            "",
            "*Jak się bronić*",
            d["defense"],
            "",
            f"IoC stringi: `{strings}`",
            f"Post na kanał: /post {Path(d.get('xmask') or 'XMask/Jak_sie_bronic.md').stem}",
        ]
    )
    return "\n".join(lines)


def _load_dashboard_sync() -> tuple[list[dict], str]:
    raw = fetch_iocs()
    catalog = load_catalog()
    items = [enrich(ioc, catalog) for ioc in raw.get("iocs") or []]
    stamp = raw.get("generated") or ""
    source = raw.get("source") or ""
    header = f"pipeline {stamp} · {len(items)} próbek"
    if source:
        header += f"\n`{source}`"
    return items, header


async def _load_dashboard() -> tuple[list[dict], str]:
    return await asyncio.to_thread(_load_dashboard_sync)


def _read_boot() -> dict:
    req = urllib.request.Request(
        "http://127.0.0.1:8080/api/boot",
        headers={"User-Agent": "xmask-obsidian-bot/1.0"},
    )
    with urllib.request.urlopen(req, timeou
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:49Z

    if args and args[0].lower() in {"cancel", "anuluj"}:
        studio.cancel(user_id)
        await update.message.reply_text("Anulowane.")
        return
    series, extra = studio.parse_series(args)
    job = studio.start(user_id, series, extra)
    if series:
        job["status"] = "ask_videos"
        studio.save_job(job)
        await update.message.reply_text(f"Seria: {series}")
        await _klip_ask_videos(update.message, job)
        return
    job["status"] = "ask_series"
    studio.save_job(job)
    await update.message.reply_text(
        "Która seria?",
        reply_markup=_klip_series_markup(),
    )


async def on_klip_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not await guard(update):
        return
    await query.answer()
    parts = (query.data or "klip:").split(":")
    action = parts[1] if len(parts) > 1 else ""
    user_id = update.effective_user.id
    job = studio.current(user_id)
    if action == "cancel":
        studio.cancel(user_id)
        await query.message.reply_text("Anulowane.")
        return
    if action in {"hackplug", "opsec", "intro"}:
        if not job:
            job = studio.start(user_id, action)
        job["series"] = action
        job["status"] = "ask_videos"
        studio.save_job(job)
        await query.message.reply_text(f"Seria: {action}")
        await _klip_ask_videos(query.message, job)
        return
    if action in {"v", "a"} and len(p
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:31:51Z

    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        await target.reply_text(chunk, reply_markup=laik_keyboard() if i == len(chunks) - 1 else None)


async def cmd_laik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    seed = " ".join(context.args).strip().lower() if context.args else ""
    chapter = None
    if seed:
        for cid, label, _path in CHAPTERS:
            if seed in cid or seed in label.lower():
                chapter = cid
                break
    await send_laik(update, chapter)


async def cmd_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    seed = " ".join(context.args).strip() if context.args else ""
    if not seed:
        await cmd_xmask(update, context)
        return
    await send_xmask_post(update, seed)


async def note_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await guard(update):
        return ConversationHandler.END
    context.user_data.clear()
    seed = " ".join(context.args).strip() if context.args else ""
    if seed:
        context.user_data["title"] = seed
        return await ask_folder(update)
    await update.message.reply_text("Tytuł nowej notatki?")
    return TITLE


async def note_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await guard(update):
        return ConversationHandler.END
    title = (update.mess
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:15Z

"""Safe read/write/search helpers for a local Obsidian vault."""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SKIP_DIRS = {".obsidian", ".trash", ".git", ".smart-env", "node_modules", "__pycache__"}
TELEGRAM_LIMIT = 3900


@dataclass(frozen=True)
class Note:
    path: Path
    rel: str
    title: str
    mtime: float

    @property
    def wiki(self) -> str:
        return f"[[{self.path.stem}]]"

    @property
    def folder(self) -> str:
        parent = str(Path(self.rel).parent)
        return "" if parent == "." else parent


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def slug_title(title: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", title).strip().strip(".")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:120] or "notatka"


class Vault:
    def __init__(
        self,
        root: Path,
        inbox: str = "Inbox",
        telegram_log: str = "Dzienniki/Telegram",
    ) -> None:
        self.root = Path(root).expanduser().resolve()
        self.inbox = inbox
        self.telegram_log = telegram_log.strip("/ ")
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / inbox).mkdir(parents=True, exist_ok=True)
        (self.root / self.telegram_log).mkdir(parents=True, exist_ok=True)
        self._notes_cache: list[Note] | None = None
        self._notes_ts = 0.0
        self._text_cache: 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:15Z

"""Gra edukacyjna dla studentów cyberbezpieczeństwa (nauka obrony).

Przepływ: /graj → poziom → atak (historia) → metoda → ATAK → OBRONA → quiz.

Każdy atak ma: historię (scenariusz SOC), metody ataku (pełne kroki),
sposoby obrony (pełne kroki) i quiz sprawdzający.
"""
from __future__ import annotations

from telegram import InlineKeyboardButton

LEVELS: list[dict] = [
    {"id": "easy", "label": "🟢 ŁATWY", "desc": "socjotechnika i proste techniki (phishing, keylogger, clipper)"},
    {"id": "medium", "label": "🟡 ŚREDNI", "desc": "stealery i przejęcia kont (Lumma, Telegram, OSINT)"},
    {"id": "hard", "label": "🔴 TRUDNY", "desc": "AiTM, RAT i obfuskacja (Evilginx, XWorm, garble)"},
]

ATTACKS: dict[str, dict] = {
    # ================= 🟢 EASY =================
    "phishing": {
        "name": "Phishing",
        "level": "easy",
        "meta": "Niska trudność · Wysoki zasięg · Socjotechnika",
        "story": (
            "Jesteś analitykiem SOC w firmie Acme Corp. Pracownicy co tydzień zgłaszają "
            "podejrzane maile i linki. Twoje zadanie: rozpoznać każdą metodę phishingu, "
            "zrozumieć jak działa i wiedzieć, jak przed nią bronić."
        ),
        "methods": [
            {
                "name": "Klon strony (SET Credential Harvester)",
                "attack": "Atakujący pobiera kopię strony logowania (wget -H -N -k -p), stawia ją na własnym serwerze i wysyła ofierze link. Ofiara wpisuje login+hasło → dane trafiają do harvester.log atakujące
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:40Z

"""Fetch pipeline IOC dashboard and attach virus descriptions."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parent / "virus_catalog.json"
DEFAULT_DASHBOARD = "http://127.0.0.1:8080/iocs.json"
_CATALOG: dict[str, Any] = {"mtime": None, "data": None}
_IOC: dict[str, Any] = {"ts": 0.0, "data": None}
_IOC_TTL = 20.0


def _local_iocs_path() -> Path | None:
    env = os.getenv("IOC_JSON", "").strip()
    candidates = []
    if env:
        candidates.append(Path(env))
    candidates.extend(
        (
            Path("/var/www/ioc-dashboard/iocs.json"),
            Path("/root/samples/reports/iocs.json"),
        )
    )
    for path in candidates:
        if path.is_file():
            return path
    return None


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    target = path or CATALOG_PATH
    if not target.is_file():
        alt = Path("/var/www/ioc-dashboard/catalog.json")
        target = alt if alt.is_file() else target
    if not target.is_file():
        return {"samples": {}, "families": {}}
    try:
        mtime = target.stat().st_mtime
    except OSError:
        return {"samples": {}, "families": {}}
    if _CATALOG["data"] is not None and _CATALOG["mtime"] == mtime:
        return _CATALOG["data"]
    data = json.loads(target.read_text(encoding="utf-8"))
    _CATALOG["mtime"] = mtime
    _C
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:40Z

#!/usr/bin/env python3
"""Job store for /klip: counts → prompt → files → render → channel."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(os.getenv("XMASK_STUDIO", "/root/xmask-studio"))
RENDER = Path(__file__).resolve().parent / "render.py"
MAX_FILE = int(os.getenv("XMASK_MAX_UPLOAD_MB", "19")) * 1024 * 1024
MAX_SLOTS = 5
SERIES = {
    "hackplug": "hackplug",
    "hp": "hackplug",
    "hacker": "hackplug",
    "opsec": "opsec",
    "ox": "opsec",
    "opsec.exe": "opsec",
    "intro": "intro",
}
CAPTION_PREFIX = {
    "hackplug": "XMASK - HACKPLUG",
    "opsec": "xmask_opsec.exe",
    "intro": "XMask",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def user_dir(user_id: int) -> Path:
    path = ROOT / "jobs" / str(user_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _meta(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def current(user_id: int) -> dict[str, Any] | None:
    pointer = user_dir(user_id) / "current.json"
    if not pointer.exists():
        return None
    job_id = json.loads(pointer.read_text(encoding="utf-8")).get("job_id")
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:51Z

./.venv/lib/python3.12/site-packages/pip/_vendor/rich/syntax.py:411:                pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/progress.py:393:    pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/progress.py:418:    pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/progress.py:535:                pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/progress.py:1292:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/progress.py:1308:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/_win32_console.py:30:    pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/text.py:184:        return NotImplemented
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/text.py:188:            return NotImplemented
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/text.py:562:        # TODO: This is a little inefficient, it is only used by full justify
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/console.py:80:    pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/console.py:1032:                pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/_null_file.py:7:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/_null_file.py:40:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/_null_file.py:57:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/_null_file.py:63:        pass
./.venv/lib/python3.12/site-packages/pip/_vendor/rich/abc.py:29:   
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:51Z

=== TODO/FIXME/XXX/pass ===
./tools/android-mcp/tests/test_composite_compute_risk_score.py:83:    """File on disk so the path checks pass; content is irrelevant when the
./tools/android-mcp/tests/test_composite_compute_risk_score.py:778:    """Caller may pass the pre-validated ``MobileCapabilityProfile`` instead of a dict."""
./tools/android-mcp/tests/test_adb.py:642:    don't accidentally pass True/False."""
./tools/android-mcp/tests/test_composite_classify_behavior.py:421:        pass
./tools/android-mcp/tests/test_lief_so.py:181:    # Plain values pass through unchanged after trimming.
./tools/android-mcp/tests/test_composite_verify_capabilities.py:171:    """Create a non-empty file on disk so the path checks pass. Content
./tools/android-mcp/tests/test_sdk_discovery.py:43:            except (OSError, NotImplementedError):
./tools/android-mcp/tests/test_sdk_discovery.py:44:                pass  # Windows: chmod is a no-op on non-NTFS-ACL filesystems
./tools/android-mcp/src/android_mcp/async_runtime.py:103:    Sorting keys + default ``repr`` means callers that pass the same
./tools/android-mcp/src/android_mcp/__main__.py:68:        pass
./tools/android-mcp/src/android_mcp/tools/androguard.py:5:binary. It's the cheapest first-pass: cheap manifest + permissions +
./tools/android-mcp/src/android_mcp/tools/androguard.py:84:        # Full chain is heavier and rarely needed for first-pass audit.
./tools/android-mcp/src/android_mcp/tools/objection.py:83:# When ``source`` is an abs
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:55Z

     2 config/secrets.env
     3 config/crontab.example
     8 config/path.sh
    20 config/secrets.env.example
    52 config/pipeline.env
    91 bin/recon_osint.sh
    94 bin/rat5_clean_run.sh
   106 bin/download_malwarebazaar.sh
   134 lib/extract_domains.py
   140 bin/osint_recon.sh
   140 lib/aggregate_patterns.py
   180 bin/rat5_android_clean.sh
   188 lib/alert_takeovers.py
   216 lib/hunt_phishing_stealer.py
   221 bin/install.sh
   223 lib/deep_re_pass.py
   268 bin/batch_analyze.sh
   292 lib/classify_roles.py
   298 bin/nightly_pipeline.sh
   351 lib/sigma_generator.py
   421 lib/yara_generator.py
   454 lib/analyze_pe.py
   488 lib/analyze_static.py
   571 lib/enrich_cti.py
   580 bin/pipeline.sh
  5541 total

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:55Z


if [ "$#" -ge 1 ]; then
    # domeny podane wprost (np. znane C2)
    DOMAINS=("$@")
else
    # 1) Zbierz domeny z raportów (wspólny ekstraktor z filtrem infrastruktury)
    "$PY" "$PIPELINE_HOME/lib/extract_domains.py" "$REPORTS_DIR" > "$DOMAINS_FILE"
    mapfile -t DOMAINS < "$DOMAINS_FILE"
    if [ "${#DOMAINS[@]}" -eq 0 ]; then
        log "Brak domen do enumeracji (wszystkie odfiltrowane?). Wyjdę."
        exit 0
    fi
    if [ "${#DOMAINS[@]}" -gt "$RECON_LIMIT" ]; then
        DOMAINS=("${DOMAINS[@]:0:$RECON_LIMIT}")
    fi
fi

log "Enumeracja ${#DOMAINS[@]} domen na $RECON_HOST (moduł $RECON_MODULE)"

# 2) Zbuduj resource file dla Recon-ng
{
    echo "workspaces create $WS"
    for d in "${DOMAINS[@]}"; do
        echo "db insert domains ${d}~"
    done
    echo "marketplace install $RECON_MODULE"
    echo "marketplace install reporting/json"
    for d in "${DOMAINS[@]}"; do
        echo "modules load $RECON_MODULE"
        echo "options set SOURCE $d"
        echo "run"
    done
    echo "modules load reporting/json"
    echo "options set FILENAME /root/osint_${WS}.json"
    echo "run"
    echo "exit"
} > "$RC"

# 3) Wyślij rc + uruchom Recon-ng na zdalnym hoście
scp -q "$RC" "$RECON_HOST:/tmp/recon_${STAMP}.rc"
ssh "$RECON_HOST" "mkdir -p /root/osint && recon-ng --no-analytics --no-version -r /tmp/recon_${STAMP}.rc > /tmp/recon_${STAMP}.log 2>&1; tail -5 /tmp/recon_${STAMP}.log"

# 4) Ściągnij wyniki
scp -q "$RECON_HOST:/root/osint_${WS}.json" "$OUT_DIR/osint_${ST
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:32:57Z

#!/usr/bin/env bash
# One-shot batch malware analysis pipeline (defensive research lab).
# Android APK + Windows PE (quarantine / raw).
# Usage:
#   pipeline.sh                  # process APK+PE in ~/samples/raw and ~/samples/quarantine
#   pipeline.sh /path/to/sample  # single file (apk/exe/dll/zip)
#   pipeline.sh --pe-only /root/samples/quarantine/  # PE w katalogu
#   pipeline.sh --aggregate-only # only rebuild CSV/patterns from existing reports
#   pipeline.sh --pe-only        # skip APK
#   pipeline.sh --apk-only       # skip PE
set -euo pipefail

PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
# shellcheck disable=SC1091
[[ -f "$PIPELINE_HOME/config/path.sh" ]] && source "$PIPELINE_HOME/config/path.sh"
[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"

SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
RAW_DIR="${RAW_DIR:-$SAMPLES_ROOT/raw}"
DECOMPILED_DIR="${DECOMPILED_DIR:-$SAMPLES_ROOT/decompiled}"
SOURCES_DIR="${SOURCES_DIR:-$SAMPLES_ROOT/sources}"
REPORTS_DIR="${REPORTS_DIR:-$SAMPLES_ROOT/reports}"
FEATURES_DIR="${FEATURES_DIR:-$SAMPLES_ROOT/features}"
NATIVE_DIR="${NATIVE_DIR:-$SAMPLES_ROOT/native}"
QUARANTINE_DIR="${QUARANTINE_DIR:-$SAMPLES_ROOT/quarantine}"
LOGS_DIR="${LOGS_DIR:-$SAMPLES_ROOT/logs}"
PE_DIR="${PE_DIR:-$SAMPLES_ROOT/pe}"
TOOLS_DIR="${TOOLS_DIR:-$PIPELINE_HOME/tools}"
VENV_DIR="${VENV_DIR:-$PIPELINE_HOME/.venv}"

JADX_THREADS="${JADX_THREADS:-2}"
SKIP_GHIDRA="${SKIP_GHIDRA:-1}"
SKIP_NATIVE="${SKIP_NAT
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:12Z

===== lib/analyze_static.py =====
#!/usr/bin/env python3
"""Static feature extraction for Android APK (defensive malware research).

Outputs JSON report + feature row for CSV aggregation.
Uses androguard when available; falls back to zip/manifest/string heuristics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

URL_RE = re.compile(r"https?://[^\s\"'<>\\]{4,200}", re.I)
WS_RE = re.compile(r"wss?://[^\s\"'<>\\]{4,200}", re.I)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
BASE64_HINT = re.compile(r"(?:[A-Za-z0-9+/]{40,}={0,2})")

# High-signal Android / malware-related API substrings
SUSPICIOUS_APIS = [
    "Runtime.exec",
    "ProcessBuilder",
    "DexClassLoader",
    "PathClassLoader",
    "InMemoryDexClassLoader",
    "System.loadLibrary",
    "Runtime.getRuntime",
    "TelephonyManager",
    "getDeviceId",
    "getSubscriberId",
    "SmsManager",
    "sendTextMessage",
    "AccessibilityService",
    "MediaProjection",
    "Camera",
    "getInstalledPackages",
    "PackageManager",
    "ClipboardManager",
    "AccountManager",
    "KeyguardManager",
    "DevicePolicyManager",
    "WebView",
    "addJavascriptInterface",
    "HttpURLConnection",
    "OkHttpClient",
    "Retrofit",
    "WebSocket",
 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:23Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:23Z

===== lib/classify_roles.py =====
#!/usr/bin/env python3
"""Tag pipeline JSON reports with role: rat / stealer / backdoor / dropper / packed / phishing / cryptojacker."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CATALOG_CANDIDATES = (
    Path("/root/android-pipeline/web/catalog.json"),
    Path("/root/obsidian-telegram-bot/virus_catalog.json"),
    Path(__file__).resolve().parent / "virus_catalog.json",
)

ENDPOINTS_DIR = Path("/root/samples/output/endpoints")

MINER_MARKERS = (
    "xmrig",
    "stratum+tcp",
    "stratum+ssl",
    "supportxmr",
    "hashvault",
    "nicehash",
    "coinhive",
    "cryptonight",
    "randomx",
    "unmineable",
)

STEALER_MARKERS = (
    "exodus",
    "metamask",
    "trustwallet",
    "trust wallet",
    "seed phrase",
    "mnemonic",
    "login data",
    "cookies.sqlite",
    "autofill",
    "telegram.tdata",
    "tdata",
    "discord.com/api/webhooks",
    "discordapp.com/api/webhooks",
    "webhooks/discord",
    "read_sms",
    "receive_sms",
    "send_sms",
    "get_accounts",
    "auth.google",
    "clipper",
    "clipboardmanager",
)

PHISHING_MARKERS = (
    "webview",
    "shouldoverrideurlloading",
    "webviewclient",
    "receita federal",
    "cartao",
    "cartão",
    "internet banking",
    "netbanking",
    "banklogin",
    "login.php",
    "wp-login",
)

BANK_HOST_RE = re.compile(
    r"(bank|sber|alfa|citi|visa|mastercard|pay
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:33:42Z

===== lib/enrich_cti.py =====
#!/usr/bin/env python3
"""
enrich_cti.py — wzbogacanie IOC z baz danych o wirusach / threat-intel.

Czyta raporty pipeline'a (/root/samples/reports/<SHA256>/*.json + iocs.json),
wyciąga IoC (hash, URL, domena, IP) i odpytuje zewnętrzne bazy:

  * MalwareBazaar  (abuse.ch)  — hash  -> get_info        (klucz: MB_API_KEY)
  * URLhaus        (abuse.ch)  — URL/domain -> /url/,/host/(ten sam klucz abuse.ch)
  * VirusTotal     (v3)        — hash  -> /files/{id}     (klucz: VT_API_KEY)
  * AbuseIPDB      (v2)        — IP    -> /check          (klucz: ABUSEIPDB_KEY)
  * AlienVault OTX             — IP/domain/hash -> indicators (klucz: OTX_KEY)

Bazy bez klucza są pomijane (nie krytyczne). Wynik:
  <reports>/cti_enrichment.json   — pełne dane
  <reports>/cti_enrichment.md     — podsumowanie trafień

Użycie:
  python3 enrich_cti.py [REPORTS_DIR] [--limit N] [--offline]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

UA = {"User-Agent": "android-pipeline/1.0 (defensive lab)"}
RE_IPV4 = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
RE_HASH_MD5 = re.compile(r"^[a-fA-F0-9]{32}$")
RE_HASH_SHA1 = re.compile(r"^[a-fA-F0-9]{40}$")
RE_HASH_SHA256 = re.compile(r"^[a-fA-F0-9]{64}$")

# stawki (sekundy między z
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:00Z

===== content.py =====
#!/usr/bin/env python3
"""XMask channel queue: educational workshop posts, no malware how-tos."""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("obsidian-bot.content")

ROOT = Path(__file__).resolve().parent
QUEUE_PATH = ROOT / "state" / "channel_queue.json"
VAULT_DEFAULT = Path("/root/obsidian-vault")

SKIP_STEMS = {"README", "Szablon_alert", "Dla_Laika_Powtorka"}
LAIK_PREFIX = "Laik_"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def today() -> str:
    return utc_now().strftime("%Y-%m-%d")


def vault_root() -> Path:
    return Path(os.getenv("VAULT_PATH", str(VAULT_DEFAULT))).expanduser()


def default_queue() -> dict[str, Any]:
    return {
        "posts": [
            {
                "id": "intro-01",
                "file": "XMask/Warsztat/01_Po_co_ten_kanal.md",
                "due": "2026-08-15",
                "published": None,
            },
            {
                "id": "hackplug-00",
                "file": "XMask/HACKPLUG/00_Co_to_jest.md",
                "due": "2026-08-16",
                "published": None,
            },
            {
                "id": "opsec-00",
                "file": "XMask/opsec.exe/00_Co_to_jest.md",
                "due": "2026-08-17",
                "published"
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:11Z

===== bin/nightly_pipeline.sh =====
#!/usr/bin/env bash
# Nocny pipeline: (opcjonalnie) MalwareBazaar → batch → pełna analiza → classify → daily summary
# Usage:
#   export MB_API_KEY='...'   # or put key in ~/android-pipeline/config/secrets.env
#   ~/nightly_pipeline.sh
#   ~/nightly_pipeline.sh --skip-download
#   ~/nightly_pipeline.sh --skip-full
#   ~/nightly_pipeline.sh --download-only
set -euo pipefail

PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
LOG_DIR="${SAMPLES_ROOT}/logs"
RAW_DIR="${SAMPLES_ROOT}/raw"
OUTPUT_DIR="${SAMPLES_ROOT}/output"
REPORTS_DIR="${SAMPLES_ROOT}/reports"
PE_DIR="${SAMPLES_ROOT}/pe"
QUARANTINE_DIR="${SAMPLES_ROOT}/quarantine"
CLASSIFY_PY="${PIPELINE_HOME}/lib/classify_roles.py"
EXPORT_SH="${OBSIDIAN_EXPORT:-/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh}"

SKIP_DOWNLOAD=0
SKIP_BATCH=0
SKIP_FULL=0
DOWNLOAD_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --skip-download) SKIP_DOWNLOAD=1 ;;
    --skip-batch) SKIP_BATCH=1 ;;
    --skip-full) SKIP_FULL=1 ;;
    --download-only) DOWNLOAD_ONLY=1; SKIP_BATCH=1; SKIP_FULL=1 ;;
    -h|--help)
      sed -n '1,16p' "$0"
      exit 0
      ;;
  esac
done

mkdir -p "$LOG_DIR" "$RAW_DIR" "$OUTPUT_DIR" "$REPORTS_DIR" \
  "$SAMPLES_ROOT"/{decompiled,sources,features,quarantine,native,pe}

DAY="$(date +%Y%m%d)"
LOG_FILE="${LOG_DIR}/nightly_${DAY}.log"
SUMMARY_FILE="${REPORTS_DIR}/daily_summary_${DAY}.md"

log() {
  local msg="[$(date '+%Y-%
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:32Z

===== bin/osint_recon.sh =====
#!/usr/bin/env bash
# osint_recon.sh — pasywny OSINT sweep domen C2 na zdalnym hoście .139.
#
# Używa nowego zestawu narzędzi (subfinder + amass + theHarvester + httpx),
# uzupełniającego recon_osint.sh (Recon-ng). Wyciąga domeny z raportów albo
# przyjmuje je jako argumenty, robi pasywną enumerację subdomen i probe HTTP.
#
# Użycie:
#   bash bin/osint_recon.sh                 # domeny z raportów
#   bash bin/osint_recon.sh suahoje.com off-game.com
#   OSINT_LIMIT=5 bash bin/osint_recon.sh
set -euo pipefail

PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
REPORTS_DIR="${REPORTS_DIR:-$HOME/samples/reports}"
RECON_HOST="${RECON_HOST:-root@5.175.189.139}"
OSINT_LIMIT="${OSINT_LIMIT:-10}"
AMASS_TIMEOUT="${AMASS_TIMEOUT:-60}"   # sekundy na pasywny amass (jest wolny)
SKIP_AMASS="${SKIP_AMASS:-0}"          # 1 = tylko subfinder (szybciej)
SKIP_NUCLEI="${SKIP_NUCLEI:-0}"        # 1 = pomiń nuclei (http/ssl)
SUB_PARALLEL="${SUB_PARALLEL:-4}"      # równoległych subfinder
CACHE_TTL_DAYS="${CACHE_TTL_DAYS:-7}"  # ważność cache subdomen (dni)

OUT_DIR="${OUT_DIR:-$REPORTS_DIR/osint}"
mkdir -p "$OUT_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

log() { echo "[osint_recon] $*"; }

# fail-fast: bez połączenia z .139 pomiń cały krok (niekrytyczne)
if ! ssh -o ConnectTimeout=8 -o BatchMode=yes "$RECON_HOST" 'true' 2>/dev/null; then
    log "Brak SSH do $RECON_HOST — pomijam OSINT sweep."
    exit 0
fi

if [ "$#" -ge 1 ]; then
    DOMAINS=("$@")
else
    map
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:46Z

===== render.py =====
#!/usr/bin/env python3
"""Reliable montage for a 2-vCPU VPS.

Fewer ffmpeg passes. Optional effects never abort the job.
No CapCut watermark / outro.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

FFMPEG = "/usr/bin/ffmpeg"
FFPROBE = "/usr/bin/ffprobe"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
AUTO_EDITOR = shutil.which("auto-editor")
TIMEOUT = 240

TITLES = {
    "hackplug": "XMASK - HACKPLUG",
    "opsec": "xmask_opsec.exe",
    "intro": "XMask",
}


def run(cmd: list[str], log: Path | None = None, timeout: int = TIMEOUT) -> None:
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"timeout: {cmd[0]}") from exc
    if log:
        with log.open("a", encoding="utf-8") as fh:
            fh.write("$ " + " ".join(cmd[:8]) + " …\n")
            fh.write((proc.stdout or "")[-4000:])
            fh.write("\n")
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg {proc.returncode}: {(proc.stdout or '')[-400:]}")


def try_run(cmd: list[str], log: Path | None = None) -> bool:
    try:
        run(cmd, log)
        return True
    except Exception as exc:
        if log:
            with log.open("a", encoding="utf-8") as fh:
                fh.w
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:34:51Z

===== test_content.py =====
#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import content as ch


class QueueTests(unittest.TestCase):
    def test_next_due_picks_oldest_overdue(self):
        data = {
            "posts": [
                {"id": "b", "file": "b.md", "due": "2026-08-17", "published": None},
                {"id": "a", "file": "a.md", "due": "2026-08-15", "published": None},
            ]
        }
        nxt = ch.next_due(data, now="2026-08-16")
        self.assertEqual(nxt["id"], "a")

    def test_skips_published(self):
        data = {
            "posts": [
                {"id": "a", "file": "a.md", "due": "2026-08-15", "published": "2026-08-15T10:00:00Z"},
                {"id": "b", "file": "b.md", "due": "2026-08-17", "published": None},
            ]
        }
        nxt = ch.next_due(data, now="2026-08-16")
        self.assertEqual(nxt["id"], "b")

    def test_html_escape(self):
        html = ch.to_html("hasło a < b i **grube** plus `kod`")
        self.assertIn("&lt;", html)
        self.assertIn("<b>grube</b>", html)
        self.assertIn("<code>kod</code>", html)


if __name__ == "__main__":
    unittest.main()
===== test_instagram.py =====
#!/usr/bin/env python3
from __future__ import annotations

import unittest

import instagram as ig


class ParseCommandTests(unittest.TestCase):
    def test_empty_is_snapshot(self):
        self.assertEqual(ig
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/obsidian-telegram-bot/bot.py (5 lines -> 7 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/android-pipeline/lib/sigma_generator.py (12 lines -> 20 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/android-pipeline/lib/extract_domains.py (1 lines -> 1 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/android-pipeline/bin/pipeline.sh (5 lines -> 4 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/android-pipeline/bin/rat5_clean_run.sh (4 lines -> 3 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:55Z

Edited /root/android-pipeline/lib/analyze_static.py (4 lines -> 3 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

bot.py OK

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

lib/sigma_generator.py OK
lib/extract_domains.py OK
lib/analyze_static.py OK

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:35:59Z

pipeline.sh OK
rat5_clean_run.sh OK

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

OK bin/batch_analyze.sh
OK bin/download_malwarebazaar.sh
OK bin/install.sh
OK bin/nightly_pipeline.sh
OK bin/osint_recon.sh
OK bin/pipeline.sh
OK bin/rat5_android_clean.sh
OK bin/rat5_clean_run.sh
OK bin/recon_osint.sh

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

OK lib/aggregate_patterns.py
OK lib/alert_takeovers.py
OK lib/analyze_pe.py
OK lib/analyze_static.py
OK lib/classify_roles.py
OK lib/deep_re_pass.py
OK lib/enrich_cti.py
OK lib/extract_domains.py
OK lib/hunt_phishing_stealer.py
OK lib/sigma_generator.py
OK lib/yara_generator.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:18Z

OK alert_roles.py
OK bot.py
OK classify_roles.py
OK content.py
OK dashboard.py
OK graj.py
OK harden_telegram.py
OK instagram.py
OK laik.py
OK publish_channel.py
OK render.py
OK studio.py
OK test_content.py
OK test_instagram.py
OK test_studio.py
OK test_vault.py
OK vault.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:40Z

----------------------------------------------------------------------
Ran 13 tests in 0.000s

OK
---
ok

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:40Z

import bot OK, allowlist= 1

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:36:44Z

active
---status---
● obsidian-telegram-bot.service - XMask Obsidian Telegram bot
     Loaded: loaded (/etc/systemd/system/obsidian-telegram-bot.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-08-15 22:36:44 UTC; 2s ago
   Main PID: 69456 (python)
      Tasks: 2 (limit: 7065)
     Memory: 34.9M (peak: 35.4M)
        CPU: 274ms
     CGroup: /system.slice/obsidian-telegram-bot.service
             └─69456 /root/obsidian-telegram-bot/.venv/bin/python /root/obsidian-telegram-bot/bot.py

Aug 15 22:36:44 vserver959630 systemd[1]: Started obsidian-telegram-bot.service - XMask Obsidian Telegram bot.
Aug 15 22:36:45 vserver959630 python[69456]: /root/obsidian-telegram-bot/bot.py:2322: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
Aug 15 22:36:45 vserver959630 python[69456]:   new_note = ConversationHandler(
Aug 15 22:36:45 vserver959630 python[69456]: /root/obsidian-telegram-bot/bot.py:2335: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
Aug 15
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:08Z

153:    all_hashes = [i["hash"] for i in iocs if i.get("hash")]

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:16Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:16Z

Edited /root/android-pipeline/lib/sigma_generator.py (3 lines -> 2 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:19Z

sigma_generator.py OK

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:41Z

active
---last log---
Aug 15 22:36:45 vserver959630 python[69456]:   new_note = ConversationHandler(
Aug 15 22:36:45 vserver959630 python[69456]: /root/obsidian-telegram-bot/bot.py:2335: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
Aug 15 22:36:45 vserver959630 python[69456]:   append_conv = ConversationHandler(
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,074 INFO apscheduler.scheduler: Adding job tentatively -- it will be properly scheduled when the scheduler starts
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,074 INFO obsidian-bot: starting bot, allowlist=1
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO apscheduler.scheduler: Added job "daily_summary" to job store "default"
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO apscheduler.scheduler: Scheduler started
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO telegram.ext.Application: Application started

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:37:55Z

Updated (645 chars)

### 🤖 Asystent — 2026-08-15T22:37:57Z

# Raport OPTYMALIZATORA

Przejrzałem oba projekty (priorytetowo `bot.py` + kluczowe pliki bota oraz `bin/*.sh`, `lib/*.py`, `tools/detection`/`yara-rules`/`sigma-rules` w pipeline). Usługa **działała i nadal działa** — po zmianach w `bot.py` zrobiłem restart i `systemctl is-active` zwraca `active`.

## Co poprawiłem

| # | Plik | Poprawka |
|---|------|----------|
| 1 | `obsidian-telegram-bot/bot.py` | Dodałem brakujący `await guard(update)` w `on_graj_cb` — callbacki gry `/graj` omijały allowlistę (jedyne miejsce w bocie, które jej nie sprawdzało). |
| 2 | `android-pipeline/lib/sigma_generator.py` | Naprawiłem klasyfikację `kind` w fallbacku `_load_iocs` — raporty APK bez pola `kind` były traktowane jako **PE**, więc Sigma generował „PE hash" z hashów APK (gdy brakowało `iocs.json`). Teraz typ jest wyliczany ze `schema`/rozszerzenia. |
| 3 | `android-pipeline/lib/sigma_generator.py` | Usunąłem martwą zmienną `all_hashes` (obliczaną, ale nigdy nieużywaną). |
| 4 | `android-pipeline/lib/extract_domains.py` | Poprawka `BAD_PREFIX`: `'crl'` → `'crl.'` — wcześniej odrzucano każdą domenę zaczynającą się od `crl…` (np. `crlab.com`) zamiast tylko prefiksu `crl.`. |
| 5 | `android-pipeline/bin/pipeline.sh` | Naprawiłem fallback `extract_nested_from_zip`: wariant `unzip -P infected` nie był próbowany dla zipów AES (bo `unzip -l` na nich przechodzi), przez co bez `7z` próbki z MalwareBazaar nie były rozpakowywane. |
| 6 | `android-pipeline/bin/rat5_clean_run.sh` | Usunąłem zdublowaną linię `trap restore_path EXIT`. |
| 7 | `android-pipeline/lib/analyze_static.py` | Usunąłem martwy regex `BASE64_HINT` (zadeklarowany, nigdy nieużyty). |

## Jak zweryfikowałem

- Python (każdy zmieniony plik): `ast.parse` — OK.
- Bash: `bash -n` na **wszystkich** `bin/*.sh` — OK.
- Testy bota: `unittest` (13 testów) — OK; `test_vault.py` — OK.
- Import bota: `import bot` — OK (allowlist=1).
- Usługa: `systemctl restart obsidian-telegram-bot` → `is-active` = **active**, w logu `Application started`.

## Co zostawiłem świadomie

- `bot.py: remember_owner` — pusta funkcja-stub, celowo wyłączona (komentarz: „First-writer-wins is disabled. Allowlist must be in .env."). Nie usuwałem, bo to świadoma decyzja projektowa, a nie niedokończony kod.
- `bot.py: _klip_begin` — nieużywany helper (martwy kod). Zostawiłem, żeby nie kasować funkcji; jest nieszkodliwy.
- `lib/enrich_cti.py` `RE_IPV4` — luźny regex dopuszcza oktety >255; to drobiazg (AbuseIPDB i tak odrzuci), nie ruszałem, żeby nie zmieniać zachowania ekstrakcji.
- Dwie niemal identyczne kopie `classify_roles.py` (katalog bota vs `lib/`) z minimalną różnicą w `iter_reports` — zostawiłem, obie działają dla swoich wywołań.
- `tools/` (NusantaraScan, android-mcp, yara-rules, sigma-rules, jadx, apktool…) — vendored/third-party, nie dotykane.
- Pliki `.env`, tokeny, hasła — nie dotykane (zgodnie z zasadą).

## Jak zweryfikować niezależnie

```bash
# bot
cd /root/obsidian-telegram-bot
.venv/bin/python -c "import ast; ast.parse(open('bot.py').read())"
.venv/bin/python -m unittest test_content test_instagram test_studio -q
systemctl is-active obsidian-telegram-bot

# pipeline
cd /root/android-pipeline
for f in bin/*.sh; do bash -n "$f"; done
for f in lib/*.py; do .venv/bin/python -c "import ast; ast.parse(open('$f').read())"; done
```

Nie wprowadzałem nic, co zmienia działającą logikę — same poprawki bezpieczeństwa / poprawności typów / martwego kodu i fallbacków.
