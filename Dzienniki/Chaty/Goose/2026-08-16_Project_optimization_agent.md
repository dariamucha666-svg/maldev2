---
title: "Project optimization agent"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_24
cwd: "/root"
messages: 100
tool_calls: 98
status: archived
---

# Project optimization agent

> Zapis czatu **Goose** · sesja '20260815_24' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | # OPTYMALIZATOR — ciągła poprawa niedokończonych projektów |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 0 |
| Akcji narzędziowych | 98 |
| Narzędzia | 'tool'×49, 'result'×49 |
| Pliki | '/home/kali/Desktop/obsidian-telegram-bot' · '/root/.mb_api_key' · '/root/android-pipeline/config/path.sh' · '/root/android-pipeline/config/path.sh.bak.rat5run' · '/root/android-pipeline/config/secrets.env' · '/root/android-pipeline/tools/jadx/bin' · '/root/android-pipeline/tools/yara-rules/custom/auto_rules.yar' · '/root/obsidian-telegram-bot/.env' · '/root/obsidian-telegram-bot/.owner_id' · '/root/obsidian-telegram-bot/.venv/bin/python' · '/root/obsidian-telegram-bot/state/alerted.json' · '/root/obsidian-vault' · '/root/osint' · '/root/osint_' · '/root/samples' · '/root/samples/quarantine/' · '/root/samples/rat5_' · '/root/samples/rat5_latest' · '/root/samples/rat5_latest.pid' · '/root/samples/re_lab_latest' |
| IP | '5.175.189.133' · '5.175.189.139' |
| Hosty | 'akamai.net' · 'akamaiedge.net' · 'amazonaws.com' · 'android.com' · 'androidx.com' · 'apache.org' · 'appspot.com' · 'cloudflare.com' · 'cloudfront.net' · 'comodoca.com' · 'digicert.com' · 'example.com' |

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T18:31:22Z

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

### 👤 Użytkownik — 2026-08-15T18:31:22Z

<turn-context>
<current-time>2026-08-15 18:31:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

Updated (301 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

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


### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:27Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:32Z

  2437 bot.py
   436 graj.py
   354 vault.py
   166 dashboard.py
   326 content.py
   565 render.py
   305 studio.py
    56 publish_channel.py
   257 alert_roles.py
   292 classify_roles.py
   432 instagram.py
    46 laik.py
  5672 total
---ANDROID---
   268 bin/batch_analyze.sh
   106 bin/download_malwarebazaar.sh
   221 bin/install.sh
   298 bin/nightly_pipeline.sh
   140 bin/osint_recon.sh
   580 bin/pipeline.sh
   180 bin/rat5_android_clean.sh
    94 bin/rat5_clean_run.sh
    91 bin/recon_osint.sh
   140 lib/aggregate_patterns.py
   188 lib/alert_takeovers.py
   454 lib/analyze_pe.py
   488 lib/analyze_static.py
   292 lib/classify_roles.py
   223 lib/deep_re_pass.py
   571 lib/enrich_cti.py
   134 lib/extract_domains.py
   216 lib/hunt_phishing_stealer.py
   351 lib/sigma_generator.py
   421 lib/yara_generator.py
    89 web/serve.py
  5545 total

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:32Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:35Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:37Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:39Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:41Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:43Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:43Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:31:46Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:05Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:05Z

lrwxrwxrwx 1 root root 7 Aug 14 23:12 .venv/bin/python -> python3
Python 3.12.3
---AST all---
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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:08Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:08Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:11Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:11Z

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
                "published": None,
            },

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:26Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:26Z

#!/usr/bin/env python3
"""Official Instagram Graph analytics for the connected Professional account.

Counts, demographics, and deltas only. No follower/following nick lists.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("obsidian-bot.instagram")

STATE_DIR = Path(__file__).resolve().parent / "state" / "instagram"
DEFAULT_BASE = "https://graph.instagram.com"
DEFAULT_VERSION = "v25.0"
PROFILE_FIELDS = (
    "id,user_id,username,name,account_type,followers_count,follows_count,"
    "media_count,profile_picture_url"
)
DEMO_BREAKDOWNS = ("gender", "age", "country")
TOP_N = 8


class InstagramError(RuntimeError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def config() -> dict[str, str]:
    return {
        "token": os.getenv("IG_ACCESS_TOKEN", "").strip(),
        "user_id": os.getenv("IG_USER_ID", "").strip(),
        "username": os.getenv("IG_USERNAME", "").strip().lstrip("@").lower(),
        "base": (os.getenv("IG_GRAPH_BASE", DEFAULT_BASE).strip() or DEFAULT_BASE).rstrip("/"),
        "version": (os.getenv("IG_GRAPH_VERSION", DEFAULT_VERSION).strip() or DEFAULT_VERSION),
    }


def is_configured() -> bool:
    return bool(config()["token"])


def parse_command(args: list[str] | None) -> str:
    """Return action: snapshot | last | setup
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:30Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:30Z

"""Layperson recap built from Obsidian XMask / analysis notes."""

from __future__ import annotations

from vault import Vault

MAIN_NOTE = "XMask/Dla_Laika_Powtorka.md"

# callback id -> (button label, vault path)
CHAPTERS: list[tuple[str, str, str]] = [
    ("cala", "Cała powtórka", "XMask/Dla_Laika_Powtorka.md"),
    ("kira", "1. Kira", "XMask/Laik_kira.md"),
    ("chrome", "2. Chrome / bank", "XMask/Laik_chrome.md"),
    ("nano", "3. Windows .NET", "XMask/Laik_dotnet.md"),
    ("zirex", "4. Zirex / Digikala", "XMask/Laik_zirex.md"),
]

BUTTON_LABELS = (
    "🧒 Dla Laika — Powtórka",
    "Dla Laika - Powtorka",
    "Dla Laika — Powtórka",
    "/laik",
    "/powtorka",
)


def is_laik_button(text: str) -> bool:
    t = (text or "").strip()
    if t in BUTTON_LABELS:
        return True
    low = t.lower().replace("—", "-").replace("–", "-")
    return "dla laika" in low and "powtork" in low.replace("ó", "o")


def recap_body(vault: Vault, chapter_id: str | None = None) -> str:
    rel = MAIN_NOTE
    if chapter_id:
        for cid, _label, path in CHAPTERS:
            if cid == chapter_id:
                rel = path
                break
    note = vault.find(rel)
    if not note:
        return "Brak notatki w vaultcie. Szukam: " + rel
    body = vault.post_body(note).strip()
    return body
=====PUBLISH=====
#!/usr/bin/env python3
"""Publish the next due XMask Warsztat post."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:30Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:30Z

#!/usr/bin/env python3
"""Notify Telegram when pipeline classifies a new RAT or stealer.

Dedupes by SHA256 in a local state file. Does not re-alert old korpus
samples after --seed. Stdlib only — safe to call from pipeline.sh.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPORTS = Path(os.environ.get("ALERT_REPORTS", "/root/samples/reports"))
STATE = Path(os.environ.get("ALERT_STATE", "/root/obsidian-telegram-bot/state/alerted.json"))
ENV_FILE = Path(os.environ.get("BOT_ENV", "/root/obsidian-telegram-bot/.env"))
OWNER_FILE = Path("/root/obsidian-telegram-bot/.owner_id")
DASH = os.environ.get("DASHBOARD_PUBLIC_URL", "https://dash.maskencrypt.eu/").rstrip("/") + "/"
DEFAULT_ROLES = ("rat", "stealer")
SKIP = {"iocs.json", "patterns_summary.json"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def alert_roles() -> set[str]:
    raw = os.environ.get("ALERT_ROL
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:32:33Z

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
                fh.write(f"SKIP {exc}\n")

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:04Z

./vault.py:119:            pass
./instagram.py:33:    pass
./instagram.py:431:        pass
./bot.py:312:            pass
./bot.py:657:            pass
./bot.py:1316:                pass
./bot.py:1588:        pass
./alert_roles.py:70:            pass
./render.py:299:    # dynaudnorm is ~10x faster than loudnorm two-pass

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:04Z

lib/extract_domains.py:113:            pass
lib/analyze_static.py:186:        pass
lib/analyze_static.py:225:        pass
lib/analyze_static.py:275:        pass
lib/analyze_static.py:458:        pass
lib/analyze_static.py:464:        pass
lib/alert_takeovers.py:107:            pass
lib/analyze_pe.py:132:            pass
lib/analyze_pe.py:258:        pass
lib/sigma_generator.py:63:            pass
lib/sigma_generator.py:345:            pass
lib/enrich_cti.py:368:            pass
lib/hunt_phishing_stealer.py:48:                pass

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:08Z


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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:11Z

===== bin/batch_analyze.sh =====
268 bin/batch_analyze.sh
===== bin/download_malwarebazaar.sh =====
106 bin/download_malwarebazaar.sh
===== bin/install.sh =====
221 bin/install.sh
===== bin/nightly_pipeline.sh =====
298 bin/nightly_pipeline.sh
===== bin/osint_recon.sh =====
140 bin/osint_recon.sh
===== bin/pipeline.sh =====
580 bin/pipeline.sh
===== bin/rat5_android_clean.sh =====
180 bin/rat5_android_clean.sh
===== bin/rat5_clean_run.sh =====
94 bin/rat5_clean_run.sh
===== bin/recon_osint.sh =====
91 bin/recon_osint.sh

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:13Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:13Z

#!/usr/bin/env bash
# Lightweight batch static analysis (defensive lab).
# APK: jadx/apktool/aapt. PE: pefile/strings/entropy/YARA/readpe.
#
# Usage:
#   batch_analyze.sh <folder_z_probek> <folder_wynikowy>
#   batch_analyze.sh ~/samples/raw ~/samples/output
#   batch_analyze.sh ~/samples/quarantine ~/samples/output
set -euo pipefail

INPUT_DIR="${1:-}"
OUTPUT_BASE="${2:-}"

if [[ -z "$INPUT_DIR" || -z "$OUTPUT_BASE" ]]; then
  echo "Użycie: $0 <folder_z_probek> <folder_wynikowy>"
  exit 1
fi

PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
if [[ -f "$PIPELINE_HOME/config/path.sh" ]]; then
  # shellcheck disable=SC1091
  source "$PIPELINE_HOME/config/path.sh" 2>/dev/null || true
fi
export PATH="${PIPELINE_HOME}/tools/jadx/bin:${PIPELINE_HOME}/tools/apktool:${PATH}"

JADX_BIN="$(command -v jadx || true)"
APKTOOL_BIN="$(command -v apktool || true)"
AAPT_BIN="$(command -v aapt2 || true)"
[[ -z "$AAPT_BIN" ]] && AAPT_BIN="$(command -v aapt || true)"
PYTHON="${PIPELINE_HOME}/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON="$(command -v python3)"
ANALYZE_PE_PY="${ANALYZE_PE_PY:-$PIPELINE_HOME/lib/analyze_pe.py}"
YARA_RULES="${YARA_RULES_DIR:-$PIPELINE_HOME/tools/yara-rules}"

mkdir -p "$OUTPUT_BASE"/{decompiled,sources,reports,features,endpoints,logs,pe_analysis}

is_apk_name() {
  local low
  low=$(echo "$1" | tr '[:upper:]' '[:lower:]')
  [[ "$low" == *.apk || "$low" == *.xapk || "$low" == *.apks ]]
}

is_pe_name() {
  local low
  low=$(echo "$1" | tr '[:upper:]' '[:lower
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:17Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:17Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:27Z

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
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$msg" |
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:32Z

#!/usr/bin/env bash
# Download Android APK samples from MalwareBazaar into ~/samples/raw/
# Requires: MB_API_KEY from https://bazaar.abuse.ch/api/
# Usage:
#   export MB_API_KEY=...
#   download_malwarebazaar.sh              # recent apk by tag
#   download_malwarebazaar.sh SHA256...    # specific hash
set -euo pipefail

PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
# shellcheck disable=SC1091
[[ -f "$PIPELINE_HOME/config/path.sh" ]] && source "$PIPELINE_HOME/config/path.sh"
[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"

RAW_DIR="${RAW_DIR:-$HOME/samples/raw}"
QUARANTINE_DIR="${QUARANTINE_DIR:-$HOME/samples/quarantine}"
MB_API_KEY="${MB_API_KEY:-}"
MB_TAG="${MB_TAG:-apk}"
MB_LIMIT="${MB_LIMIT:-20}"
API="https://mb-api.abuse.ch/api/v1/"

mkdir -p "$RAW_DIR" "$QUARANTINE_DIR"

if [[ -z "$MB_API_KEY" ]]; then
  echo "Set MB_API_KEY (MalwareBazaar API key)." >&2
  exit 1
fi

download_hash() {
  local h="$1"
  local out="$QUARANTINE_DIR/${h}.zip"
  echo "[+] get_file $h"
  curl -fsS -X POST "$API" \
    -d "query=get_file" \
    -d "sha256_hash=${h}" \
    -H "Auth-Key: ${MB_API_KEY}" \
    -o "$out" || {
      # older API style
      curl -fsS -X POST "$API" \
        -d "query=get_file&sha256_hash=${h}" \
        -d "api_key=<REDACTED> \
        -o "$out" || return 1
    }
  # Extract APK to raw (password=<REDACTED>
  local tmp
  tmp=$(mktemp -d)
  unzip -o -q -P infected "$out" -d "$tmp" 2>/dev/null \
    || 7z x -p"
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:36Z

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
    mapfile -t DOMAINS < <(python3 "$P
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:42Z

#!/usr/bin/env bash
set -euo pipefail

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
ROOT="/root/samples/rat5_${STAMP}"
export ROOT
PATH_SH="/root/android-pipeline/config/path.sh"
PATH_BAK="/root/android-pipeline/config/path.sh.bak.rat5run"
API="https://mb-api.abuse.ch/api/v1/"

mkdir -p "$ROOT"/{raw,quarantine,decompiled,sources,reports,features,native,logs,output,meta}
ln -sfn "$ROOT" /root/samples/rat5_latest
LOG="$ROOT/logs/rat5_clean_${STAMP}.log"
echo $$ > /root/samples/rat5_latest.pid

# shellcheck disable=SC1091
source /root/android-pipeline/config/secrets.env 2>/dev/null || true
if [[ -z "${MB_API_KEY:-}" && -f /root/.mb_api_key ]]; then
  MB_API_KEY=$(tr -d " \t\r\n" < /root/.mb_api_key)
fi
export MB_API_KEY
[[ -n "${MB_API_KEY:-}" ]] || { echo "NO MB_API_KEY"; exit 1; }

cp -a "$PATH_SH" "$PATH_BAK"
sed -i "s|export SAMPLES_ROOT=\"/root/samples\"|export SAMPLES_ROOT=\"$ROOT\"|" "$PATH_SH"
restore_path() {
  if [[ -f "$PATH_BAK" ]]; then
    mv -f "$PATH_BAK" "$PATH_SH"
    echo "[restore] path.sh" >>"$LOG" || true
  fi
}
trap restore_path EXIT

export PATH="/root/android-pipeline/tools/jadx/bin:/root/android-pipeline/tools/apktool:/root/android-pipeline/bin:${PATH}"
export FORCE=1 SKIP_GHIDRA=1

download_one() {
  local h="$1" label="$2"
  local out="$ROOT/quarantine/${h}.zip"
  echo "[+] get_file $h ($label)"
  curl -fsS -X POST "$API" \
    -d "query=get_file" -d "sha256_hash=${h}" \
    -H "Auth-Key: ${MB_API_KEY}" -o "$out"
  local tmp
  tmp=$(mktemp -d)
  7z x -p"infected"
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:52Z

#!/usr/bin/env python3
"""Aggregate per-sample JSON reports into CSV features + common pattern summary."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_reports(reports_dir: Path) -> list[dict[str, Any]]:
    out = []
    for p in sorted(reports_dir.glob("*.json")):
        if p.name.endswith(".features.json"):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("schema", "").startswith("android-malware-pipeline"):
                out.append(data)
        except Exception:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports", type=Path, required=True)
    ap.add_argument("--features-out", type=Path, required=True)
    ap.add_argument("--patterns-out", type=Path, required=True)
    args = ap.parse_args()

    reports = load_reports(args.reports)
    args.features_out.parent.mkdir(parents=True, exist_ok=True)
    args.patterns_out.parent.mkdir(parents=True, exist_ok=True)

    rows = [r["feature_row"] for r in reports if "feature_row" in r]
    fieldnames = [
        "sha256",
        "filename",
        "size",
        "package",
        "min_sdk",
        "target_sdk",
        "permission_count",
        "dangerous_permission_count",
        "activity_count",
        "service_count",
        "receiver_count",
        "nati
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:33:55Z

#!/usr/bin/env python3
"""Static feature extraction for Windows PE (defensive malware research).

Outputs JSON + Markdown + HTML reports. Uses pefile when available;
falls back to header/string heuristics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUSPICIOUS_STRING_RE = re.compile(
    r"(https?://|wss?://|\bapi\b|\bbot\b|\btoken\b|exodus|metamask|trustwallet|"
    r"wallet|cmd\.exe|powershell|pwsh|reg add|schtasks|bitsadmin|certutil|"
    r"rundll32|regsvr32|mshta|wscript|cscript|AppData|\\Temp\\|VirtualAlloc|"
    r"WriteProcessMemory|CreateRemoteThread|NtUnmapViewOfSection|"
    r"HKEY_|SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run|"
    r"telegram|discord|webhook|steal|inject|ransom|bitcoin|mnemonic)",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s\"'<>\\]{4,200}", re.I)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SUSPICIOUS_IMPORTS = {
    "virtualalloc",
    "virtualallocex",
    "virtualprotect",
    "writeprocessmemory",
    "createremotethread",
    "ntunmapviewofsection",
    "ntwritevirtualmemory",
    "rtldecompressbuffer",
    "winexec",
    "shellexecute",
    "shellexecutea",
    "shellexecutew",
    "createservice",
    "regsetvalue",
    "regsetvalueex",
    "internetopen",
    "internetconnect",
    
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:04Z

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
    "Socket",
    "Cipher",
    "Se
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:06Z

                nodes = list(am.iter())
                for node in nodes:
                    tagname = getattr(node, "tag", "") or ""
                    if not str(tagname).endswith(tag):
                        continue
                    attrib = getattr(node, "attrib", {}) or {}
                    name = exp = None
                    for k, v in attrib.items():
                        if str(k).endswith("name"):
                            name = v
                        if str(k).endswith("exported"):
                            exp = v
                    if name and exp in ("true", "1"):
                        exported.append({"type": tag, "name": name, "exported": exp})
    except Exception:
        pass

    return {
        "package": a.get_package(),
        "app_name": a.get_app_name(),
        "version_name": (getattr(a, "androidversion", {}) or {}).get("Name") or None,
        "version_code": (getattr(a, "androidversion", {}) or {}).get("Code") or None,
        "min_sdk": a.get_min_sdk_version(),
        "target_sdk": a.get_target_sdk_version(),
        "permissions": perms,
        "dangerous_permissions": dangerous,
        "permission_count": len(perms),
        "dangerous_permission_count": len(dangerous),
        "activities": activities[:200],
        "services": services[:200],
        "receivers": receivers[:200],
        "providers": providers[:100],
        "activity_count": len(activities),
        "service_count": len(services),
        "recei
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:11Z

--- obsidian-telegram-bot/classify_roles.py	2026-08-15 09:15:54.952718212 +0000
+++ android-pipeline/lib/classify_roles.py	2026-08-15 09:16:26.201569138 +0000
@@ -214,7 +214,7 @@
     out: list[Path] = []
     for path in sorted(root.glob("*.json")):
         name = path.name
-        if name.endswith(".features.json") or name in {"iocs.json", "patterns_summary.json"}:
+        if name.endswith(".features.json") or name in {"iocs.json", "patterns_summary.json", "sigma_index.json"}:
             continue
         if name.startswith("daily_") or name.startswith("DEEP_"):
             continue
DIFFERS

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:15Z

#!/usr/bin/env python3
"""
extract_domains.py — wyciąga "ciekawe" domeny (C2 / nie-infrastruktura)
z raportów pipeline + katalogu rodzin do stdout (jedna na linię).

Źródła:
  * raporty JSON (urls, patterns.urls, patterns.websockets)
  * reports/iocs.json (zagregowane URL-e)
  * web/catalog.json (kuratorowane C2 z analiz, np. suahoje.com / off-game.com)

Użycie:
  python3 extract_domains.py /root/samples/reports
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

BLOCK = {
    'localhost', 'example.com',
    'android.com', 'google.com', 'googleapis.com', 'gstatic.com', 'gvt1.com',
    'play.google.com', 'goo.gl', 'youtube.com', 'google-analytics.com',
    'microsoft.com', 'mozilla.org', 'windows.com', 'windows.net',
    'digicert.com', 'globalsign.com', 'sectigo.com', 'usertrust.com',
    'ssl.com', 'identrust.com', 'letsencrypt.org', 'comodoca.com',
    'apache.org', 'w3.org', 'xml.org', 'xmlsoap.org',
    'github.com', 'githubusercontent.com', 'gitlab.com',
    'jetbrains.com', 'kotlinlang.org', 'gradle.org',
    'appspot.com', 'firebaseapp.com', 'firebaseio.com', 'googleapis.cn',
    'amazonaws.com', 'cloudfront.net', 'akamai.net', 'akamaiedge.net',
    'cloudflare.com', 'fastly.net', 'jsdelivr.net', 'unpkg.com',
    'wikipedia.org', 'sourceforge.net', 'maven.org', 'react.dev',
    'tailwindcss.com', 'publicsuffix.org', 'docs.rs',
    'schemas.android.com', 'androidx.com',
    # biblioteki/bundlery JS (szum z minifikacji)
    'nodejs.org', 'np
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:19Z

#!/usr/bin/env python3
import re, json, sys
from pathlib import Path
from collections import defaultdict

lab = Path(sys.argv[1] if len(sys.argv) > 1 else "/root/samples/re_lab_latest").resolve()
src_root = lab / "output" / "sources"
reports_root = Path("/root/samples/reports")

re_url = re.compile(r"https?://[^\s\"'<>]{6,200}", re.I)
re_ip = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")
re_host = re.compile(
    r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|ru|cn|br|io|xyz|top|cc|su|info|biz|invalid|internal|tk|pw|me|co)(?::\d{2,5})?\b",
    re.I,
)

noise = (
    "schemas.android", "apache.org", "w3.org", "mozilla.org", "googlesource", "github.com",
    "example.com", "google.com", "creativecommons", "jetbrains", "kotlinlang", "android.com",
    "play.google", "maven.", "gradle", "sourceforge", "oracle.com", "openjdk", "junit",
)

lib_noise = (
    "androidx/", "android/support/", "kotlin/", "okhttp3/", "com/google/", "org/apache/",
    "com/squareup/", "retrofit2/", "io/reactivex/", "javax/", "org/json/", "okio/",
)

keywords = [
    "Socket", "HttpURLConnection", "OkHttp", "WebSocket", "SmsManager", "sendTextMessage",
    "AccessibilityService", "DeviceAdminReceiver", "Camera", "MediaProjection", "RECORD_AUDIO",
    "Runtime.getRuntime", "ProcessBuilder", "loadLibrary", "DexClassLoader", "PathClassLoader",
    "Cipher", "SecretKeySpec", "AES", "RSA", "Base64", "Telegram", "Firebase",
    "SYSTEM_ALERT_
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:22Z

#!/usr/bin/env python3
"""Generate Sigma (SIEM) rules from pipeline IOC reports.

Companion to yara_generator.py. Reads reports/*.json or iocs.json and writes
YAML rules a SOC can drop into Sigma → Splunk/Elastic/Microsoft Sentinel.

Usage:
  sigma_generator.py /root/samples/reports
  sigma_generator.py /root/samples/reports /root/samples/reports/sigma
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from collections import defaultdict
from datetime import date
from pathlib import Path

SKIP_JSON = {
    "iocs.json",
    "patterns_summary.json",
    "re_static_iocs.json",
    "features.json",
    "summary.json",
    "sigma_index.json",
}

NOISE_HOST = re.compile(
    r"(schemas\.android\.com|www\.w3\.org|xmlns|mozilla\.org|apache\.org|"
    r"opensource\.org|play\.google\.com|googleapis\.com|localhost|"
    r"publicsuffix\.org|youtrack\.jetbrains|react\.dev|tailwindcss)",
    re.I,
)

NS = uuid.UUID("8f3a1c2e-5b7d-4a9e-9c0b-2f6d1e8a4b01")


def _yaml_escape(s: str) -> str:
    return s.replace("'", "''")


def _ident(name: str) -> str:
    ident = re.sub(r"[^A-Za-z0-9_.-]+", "-", name or "sample").strip("-")
    return (ident or "sample")[:60]


def _uid(*parts: str) -> str:
    return str(uuid.uuid5(NS, "|".join(parts)))


def _load_iocs(report_dir: Path) -> list[dict]:
    iocs_path = report_dir / "iocs.json"
    if iocs_path.is_file():
        try:
            payload = json.loads(iocs_path.read_text(encoding="utf-8"))
            items
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:30Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:30Z

#!/usr/bin/env python3
"""
YARA Generator – automatyczne tworzenie reguł YARA na podstawie analizy PE/APK.

Czyta raporty pipeline'u:
  /root/samples/reports/<SHA256>.json
  /root/samples/reports/<SHA256>/{<SHA256>.json, suspicious_strings.txt}

Użycie:
  yara_generator.py <katalog_z_raportami>
  yara_generator.py /root/samples/reports /root/android-pipeline/tools/yara-rules/custom/auto_rules.yar
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


STRING_FILES = (
    "strings.txt",
    "suspicious_strings.txt",
    "endpoints_grep.txt",
)

SKIP_JSON_NAMES = {
    "patterns_summary.json",
    "re_static_iocs.json",
    "features.json",
    "summary.json",
    "iocs.json",
    "cti_enrichment.json",
    "sigma_index.json",
}

GENERIC_ALONE = {
    "seed",
    "pass",
    "login",
    "token",
    "api",
    "bot",
    "wallet",
    "password",
}

# Szum, który nie nadaje się na IoC (schematy Android, stdlib Go, Lorem).
NOISE_RE = re.compile(
    r"("
    r"schemas\.android\.com|"
    r"www\.w3\.org|"
    r"xmlns|"
    r"mozilla\.org/MPL|"
    r"publicsuffix\.org|"
    r"youtrack\.jetbrains|"
    r"apache\.org/licenses|"
    r"opensource\.org|"
    r"play\.google\.com|"
    r"googleapis\.com|"
    r"tailwindcss|"
    r"react\.dev|"
    r"^https?://localhost|"
    r"^0+\.0+\.0+\.0+$|"
    r"^127\.0\.0\.1$|"
    r"runtime:|"
    r"goroutine|"
    r"GOMEMLIMIT|"
    r"crypto/tls|"
    r"crypto/rsa|"
    r"c
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:36Z

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

# stawki (sekundy między zapytaniami) — darmowe limity
R
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:43Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:43Z

#!/usr/bin/env python3
"""IOC dashboard HTTP server.

    python3 ~/android-pipeline/web/serve.py
    python3 ~/android-pipeline/web/serve.py --port 8766 --bind 127.0.0.1

GET /              → dashboard.html
GET /api/iocs      → JSON z reports/iocs.json (albo świeżo z generatora)
GET /iocs.json     → to samo
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
PIPELINE_HOME = WEB_DIR.parent
REPORTS_DIR = Path("/root/samples/reports")
IOC_CANDIDATES = (
    WEB_DIR / "iocs.json",
    REPORTS_DIR / "iocs.json",
)


def load_iocs() -> bytes:
    for path in IOC_CANDIDATES:
        if path.is_file():
            return path.read_bytes()
    yara_py = PIPELINE_HOME / "lib" / "yara_generator.py"
    if yara_py.is_file() and REPORTS_DIR.is_dir():
        sys.path.insert(0, str(PIPELINE_HOME / "lib"))
        from yara_generator import YARAGenerator, iter_report_json  # type: ignore

        gen = YARAGenerator(REPORTS_DIR)
        for json_file in iter_report_json(REPORTS_DIR):
            gen.process_report(json_file)
        payload = {
            "generated": None,
            "count": len(gen.iocs),
            "rules": len(gen.rules),
            "iocs": gen.iocs,
        }
        return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode()
    return b'{"generated":null,"count":0,"rules":0,"iocs":[]
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:46Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:50Z

/root/obsidian-telegram-bot/.venv/bin/python: No module named pytest
---manual test_vault---
ok

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:54Z

test_html_escape (test_content.QueueTests.test_html_escape) ... ok
test_next_due_picks_oldest_overdue (test_content.QueueTests.test_next_due_picks_oldest_overdue) ... ok
test_skips_published (test_content.QueueTests.test_skips_published) ... ok
test_parse_gender (test_instagram.BreakdownTests.test_parse_gender) ... ok
test_first_snapshot (test_instagram.DeltaTests.test_first_snapshot) ... ok
test_numeric_delta (test_instagram.DeltaTests.test_numeric_delta) ... ok
test_empty_is_snapshot (test_instagram.ParseCommandTests.test_empty_is_snapshot) ... ok
test_last_and_setup (test_instagram.ParseCommandTests.test_last_and_setup) ... ok
test_me (test_instagram.ParseCommandTests.test_me) ... ok
test_rejects_foreign_username (test_instagram.ParseCommandTests.test_rejects_foreign_username) ... ok
test_count (test_studio.PromptTests.test_count) ... ok
test_never_watermark_even_if_asked (test_studio.PromptTests.test_never_watermark_even_if_asked) ... ok
test_prompt_look (test_studio.PromptTests.test_prompt_look) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.001s

OK

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:34:58Z

OK bin/batch_analyze.sh
OK bin/download_malwarebazaar.sh
OK bin/install.sh
OK bin/nightly_pipeline.sh
OK bin/osint_recon.sh
OK bin/pipeline.sh
OK bin/rat5_android_clean.sh
OK bin/rat5_clean_run.sh
OK bin/recon_osint.sh
---bot scripts---
OK git_autocommit.sh
OK run.sh

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:03Z

compile OK
compile pipeline OK

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:03Z

Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'pyflakes'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'pyflakes'
done

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T18:35:12Z

edit_markdown False
edit_text True
reply_markdown True
reply_text True
