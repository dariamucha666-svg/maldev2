---
title: "Jesteś maszyną optymalizującą. Przeglądaj i poprawiaj nie..."
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_16
cwd: "/root"
messages: 100
tool_calls: 98
status: archived
---

# Jesteś maszyną optymalizującą. Przeglądaj i poprawiaj nie...

> Zapis czatu **Goose** · sesja '20260815_16' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | Jesteś maszyną optymalizującą. Przeglądaj i poprawiaj niedokończone projekty. |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 0 |
| Akcji narzędziowych | 98 |
| Narzędzia | 'tool'×49, 'result'×49 |
| Pliki | '/root/.mb_api_key' · '/root/android-pipeline/' · '/root/android-pipeline/bin/nightly_pipeline.sh' · '/root/android-pipeline/bin/pipeline.sh' · '/root/android-pipeline/bin/rat5_android_clean.sh' · '/root/android-pipeline/bin/rat5_clean_run.sh' · '/root/android-pipeline/config/path.sh' · '/root/android-pipeline/config/path.sh.bak.rat5run' · '/root/android-pipeline/config/secrets.env' · '/root/android-pipeline/tools/jadx/bin' · '/root/obsidian-telegram-bot' · '/root/obsidian-telegram-bot/' · '/root/obsidian-telegram-bot/state/alerted.json' · '/root/obsidian-vault' · '/root/obsidian-vault/Narzedzia/alert_roles.py' · '/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh' · '/root/samples' · '/root/samples/quarantine/' · '/root/samples/rat5_' · '/root/samples/rat5_latest' |
| Hosty | 'instagram.com' |

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T16:30:52Z

Jesteś maszyną optymalizującą. Przeglądaj i poprawiaj niedokończone projekty.

## Zakres (priorytet)
1. /root/obsidian-telegram-bot/ — bot Telegram (bot.py ~2200 linii, graj.py, vault.py, dashboard.py).
2. /root/android-pipeline/ — pipeline malware/RE (bin/*.sh, lib/*.py, tools/detection, tools/yara-rules, tools/sigma-rules).

## Co robić
1. Znajdź bugi (niespójne nazwy funkcji, martwy kod, niedziałające ścieżki).
2. Znajdź niedokończone funkcje (TODO, puste bloki, niepodpięte komendy).
3. Znajdź okazje do optymalizacji (duplikacja, nieczytelny kod, brak obsługi błędów).
4. Wprowadź konkretne poprawki (edit/write). Po każdej zmianie zweryfikuj składnię:
   - Python: cd /root/obsidian-telegram-bot && .venv/bin/python -c "import ast; ast.parse(open('bot.py').read())"
   - Bash: bash -n skrypt.sh

## Zasady
- NIE psuj działającej usługi — bot działa jako systemd (obsidian-telegram-bot). Po zmianach w bot.py: systemctl restart obsidian-telegram-bot && systemctl is-active obsidian-telegram-bot.
- Nie dotykaj plików .env, tokenów, haseł.
- Nie kasuj działających funkcji — tylko poprawiaj.
- Pracuj w katalogu /root.

## Raport
Na końcu wypisz: co poprawiłeś (lista), co zostawiłeś, jak zweryfikować.

### 👤 Użytkownik — 2026-08-15T16:30:52Z

<turn-context>
<current-time>2026-08-15 16:30:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

Updated (707 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

README.md  [59]
alert_roles.py  [257]
bot.py  [2K]
bot.py.bak.ig-20260815104103  [1K]
bot.py.bak.kanal-20260815110710  [1K]
bot.py.bak.obsidian-tab  [1K]
classify_roles.py  [292]
content.py  [323]
dashboard.html  [818]
dashboard.py  [166]
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
vault.py.bak.obsidian-tab  [303]
virus_catalog.json  [565]


### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:30:58Z

bin/  [2K]
  batch_analyze.sh  [268]
  batch_analyze.sh.bak-pre-pe  [149]
  download_malwarebazaar.sh  [106]
  install.sh  [221]
  nightly_pipeline.sh  [298]
  nightly_pipeline.sh.bak.20260815  [201]
  osint_recon.sh  [140]
  pipeline.sh  [576]
  pipeline.sh.bak-pre-pe  [321]
  rat5_android_clean.sh  [180]
  rat5_clean_run.sh  [92]
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
    alert_takeovers.cpython-312.pyc  [0]
    enrich_cti.cpython-312.pyc  [0]
    yara_generator.cpython-312.pyc  [0]
  aggregate_patterns.py  [140]
  alert_takeovers.py  [188]
  analyze_pe.py  [464]
  analyze_static.py  [487]
  classify_roles.py  [292]
  deep_re_pass.py  [219]
  enrich_cti.py  [571]
  extract_domains.py  [134]
  hunt_phishing_stealer.py  [216]
  sigma_generator.py  [351]
  yara_generator.py  [418]
tools/  [185K]
  NusantaraScan/  [2K]
    nusantarascan/  [1K]
      analyzers/  [491]
        __init__.py  [18]
        base.py  [53]
        disassembler.py  [94]
        elf.py  [87]
        macho.py  [26]
        packer_detector.py  [44]
        pe.py  [81]
        strings.py  [88]
      formatters/  [61]
        __init__.py  [4]
        html_output.py  [38]
        json_output.py  [19]
      integrations/  [87]
        __init__.py  [3]
        virustotal.py  [84]
      scanners/  [95]
        __init__.py  [3]
        multi_file.p
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:04Z

  2283 bot.py
   436 graj.py
   354 vault.py
   166 dashboard.py
   323 content.py
   565 render.py
   305 studio.py
   432 instagram.py
    56 publish_channel.py
   257 alert_roles.py
   292 classify_roles.py
    46 laik.py
    55 harden_telegram.py
    41 test_content.py
    64 test_instagram.py
    28 test_studio.py
    37 test_vault.py
  5740 total

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:04Z

   268 bin/batch_analyze.sh
   106 bin/download_malwarebazaar.sh
   221 bin/install.sh
   298 bin/nightly_pipeline.sh
   140 bin/osint_recon.sh
   576 bin/pipeline.sh
   180 bin/rat5_android_clean.sh
    92 bin/rat5_clean_run.sh
    91 bin/recon_osint.sh
   140 lib/aggregate_patterns.py
   188 lib/alert_takeovers.py
   464 lib/analyze_pe.py
   487 lib/analyze_static.py
   292 lib/classify_roles.py
   219 lib/deep_re_pass.py
   571 lib/enrich_cti.py
   134 lib/extract_domains.py
   216 lib/hunt_phishing_stealer.py
   351 lib/sigma_generator.py
   418 lib/yara_generator.py
    89 web/serve.py
  5541 total
---detection---
  119 tools/detection/all_lab.rules
   26 tools/detection/keylogger_exfil.rules
   13 tools/detection/laplas_clipper.rules
   18 tools/detection/lumma_digitden.rules
   61 tools/detection/phishing_tools.rules
   56 tools/detection/phishing_tools.zeek
   19 tools/detection/xworm_tuffman.rules
  312 total
---sigma---
  34 tools/sigma-rules/README.md
  24 tools/sigma-rules/lumma_digitden_dns.yml
  24 tools/sigma-rules/xmask_network_hosts.yml
  25 tools/sigma-rules/xmask_pe_hashes_file.yml
  25 tools/sigma-rules/xmask_pe_hashes_process.yml
  25 tools/sigma-rules/xmask_role_backdoor_hashes.yml
  28 tools/sigma-rules/xmask_win_account_api_cluster.yml
  24 tools/sigma-rules/xworm_tuffman_dns.yml
 209 total

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:09Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:09Z

169:def _env_ids() -> set[int]:
181:def allowed_ids() -> set[int]:
190:def remember_owner(user_id: int) -> None:
195:def is_allowed(user_id: int | None) -> bool:
204:def require_allowlist() -> set[int]:
213:def public_dash_url(hash_prefix: str | None = None) -> str:
222:def phone_keyboard() -> ReplyKeyboardMarkup:
236:def _ob_id(path: str) -> str:
242:def _ob_path(key: str) -> str | None:
246:def _ob_icon(folder: str) -> str:
251:def _ob_label(folder: str) -> str:
256:def _ob_sort_folders(subs: list[tuple[str, int]]) -> list[tuple[str, int]]:
261:def open_dash_markup(hash_prefix: str | None = None) -> InlineKeyboardMarkup:
278:def laik_keyboard() -> InlineKeyboardMarkup:
291:def get_vault() -> Vault:
301:async def guard(update: Update) -> bool:
316:async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
327:async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
344:async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
350:async def cmd_folders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
363:def _ob_tabs_row() -> list[InlineKeyboardButton]:
375:def _ob_home_markup(vault: Vault) -> InlineKeyboardMarkup:
406:def _ob_all_markup(vault: Vault, page: int = 0) -> InlineKeyboardMarkup:
433:def _ob_folder_markup(vault: Vault, folder: str, page: int = 0) -> InlineKeyboardMarkup:
468:def _ob_recent_markup(vault: Vault, page: int = 0) -> InlineKeyboardMarkup:
490:def _ob_note_markup(note_
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:09Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:09Z

bot.py:312:            pass
bot.py:657:            pass
bot.py:1182:                pass
bot.py:1454:        pass
vault.py:119:            pass
render.py:299:    # dynaudnorm is ~10x faster than loudnorm two-pass
instagram.py:33:    pass
instagram.py:431:        pass

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:12Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:12Z



def _ob_path(key: str) -> str | None:
    return _OB_MAP.get(key)


def _ob_icon(folder: str) -> str:
    name = folder.rstrip("/").split("/")[-1] if folder else ""
    return OB_ICONS.get(name, "📂")


def _ob_label(folder: str) -> str:
    name = folder.rstrip("/").split("/")[-1] if folder else "vault"
    return name.replace("_", " ")


def _ob_sort_folders(subs: list[tuple[str, int]]) -> list[tuple[str, int]]:
    rank = {name: i for i, name in enumerate(OB_FOLDER_ORDER)}
    return sorted(subs, key=lambda kv: (rank.get(kv[0], 80), -kv[1], kv[0].lower()))


def open_dash_markup(hash_prefix: str | None = None) -> InlineKeyboardMarkup:
    url = public_dash_url(hash_prefix)
    rows: list[list[InlineKeyboardButton]] = []
    if url.startswith("https://"):
        rows.append(
            [InlineKeyboardButton("📱 Otwórz w Telegramie", web_app=WebAppInfo(url=url))]
        )
    rows.append([InlineKeyboardButton("🌐 Otwórz w przeglądarce", url=url)])
    all_url = url.split("?")[0].rstrip("/") + "/?tab=all"
    if hash_prefix:
        all_url += f"&hash={hash_prefix}"
    rows.append([InlineKeyboardButton("Katalog rodzin", url=all_url)])
    know = url.split("?")[0].rstrip("/") + "/?tab=know"
    rows.append([InlineKeyboardButton("Co krąży teraz", url=know)])
    return InlineKeyboardMarkup(rows)


def laik_keyboard() -> InlineKeyboardMarkup:
    rows = []
    row: list[InlineKeyboardButton] = []
    for cid, label, _path in CHAPTERS:
        row.append(InlineKeyboardButton(l
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:15Z

    xmask = [
        n
        for n in vault.list_xmask()
        if not _sum_skip(n.title)
    ]
    malware = [
        n
        for n in vault.iter_notes()
        if n.folder.replace("\\", "/") == "Analizy/Malware" and not _sum_skip(n.title)
    ]
    malware.sort(key=lambda n: n.title.lower())
    done, open_ = _backlog_counts(vault)

    def bullets(notes, limit: int = 8) -> str:
        lines = []
        for n in notes[:limit]:
            title = escape_markdown(n.title.replace("_", " "), version=1)
            lines.append(f"• {title}")
        extra = len(notes) - limit
        if extra > 0:
            lines.append(f"• _…i {extra} więcej_")
        return "\n".join(lines) or "• _(brak notatek)_"

    projekty = [n for n in vault.iter_notes() if n.folder.split("/")[0] == "Projekty"]
    lab = [n for n in vault.iter_notes() if n.folder.split("/")[0] == "Lab"]
    narz = [n for n in vault.iter_notes() if n.folder.split("/")[0] == "Narzedzia"]
    daily = [n for n in vault.iter_notes() if n.folder.split("/")[0] in {"Daily", "daily"}]
    parts = [
        "📋 *Co już umiem?*",
        "",
        f"*{total}* notatek · XMask *{len(xmask)}* · analizy *{len(malware)}* · projekty *{len(projekty)}*",
        "",
        "*XMask*",
        bullets(xmask, 8),
        "",
        "*Analizy / Malware*",
        bullets(malware, 6),
        "",
        "*Projekty*",
        bullets(sorted(projekty, key=lambda n: n.mtime, reverse=True), 5),
        "",
        "*Lab / Narzędzi
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:15Z


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    vault = get_vault()
    folder = " ".join(context.args).strip() if context.args else ""
    notes = vault.iter_notes()
    if folder:
        folder_l = folder.lower().rstrip("/")
        notes = [n for n in notes if n.folder.lower() == folder_l or n.folder.lower().startswith(folder_l + "/")]
        header = f"Notatki w `{folder}` ({len(notes)}):"
    else:
        header = f"Ostatnie notatki ({len(notes)} w vaultcie):"
        notes = notes[:10]
    if not notes:
        await update.message.reply_text("Brak notatek w tym miejscu.")
        return
    lines = [f"• `{n.rel}`" for n in notes[:20]]
    await update.message.reply_markdown(
        header + "\n" + "\n".join(lines),
        reply_markup=_note_keyboard(notes, "get"),
    )


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    query = " ".join(context.args).strip() if context.args else ""
    if not query:
        await update.message.reply_text("Użycie: /szukaj fraza")
        return
    await update.message.chat.send_action("typing")
    vault = get_vault()
    hits = await asyncio.to_thread(vault.search, query)
    if not hits:
        await update.message.reply_text(f"Nic nie znalazłem dla: {query}")
        return
    lines = []
    for note, snippet in hits:
        safe_rel = escape_markdown(note.re
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:18Z

    await query.answer()
    action = (query.data or "kanal:q").split(":", 1)[-1]
    if action == "q":
        await query.message.reply_markdown(channel.queue_summary(), reply_markup=_kanal_markup())
        return
    if action == "next":
        item = channel.next_due()
        if item is None:
            await query.message.reply_text("Kolejka pusta.")
            return
        path = channel.resolve_post(item)
        body = channel.post_body(path) if path.exists() else "(brak pliku)"
        await query.message.reply_text(
            f"NEXT {item['id']} (due {item.get('due')})\n\n{body}"[:4000]
        )
        return
    try:
        result = await asyncio.to_thread(channel.publish)
    except RuntimeError as exc:
        await query.message.reply_text(str(exc), reply_markup=_kanal_markup())
        return
    await query.message.reply_markdown(
        f"Wysłane: `{result['id']}` → {result['dest']}",
        reply_markup=_kanal_markup(),
    )


def _klip_series_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("HACKPLUG", callback_data="klip:hackplug"),
                InlineKeyboardButton("opsec.exe", callback_data="klip:opsec"),
            ],
            [InlineKeyboardButton("Anuluj", callback_data="klip:cancel")],
        ]
    )


def _klip_count_markup(kind: str) -> InlineKeyboardMarkup:
    row = [InlineKeyboardButton(str(i), callback_data=f"klip:{kind}:{i}") for i in range(6)
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:18Z

        d = ioc["desc"]
        short = (ioc.get("hash") or "")[:8]
        lines.append(f"• `{short}` [{d.get('role') or '?'}] *{d['title']}*")
    rows = list(open_dash_markup().inline_keyboard)
    rows.extend(_dash_keyboard(items).inline_keyboard)
    await update.message.reply_markdown(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup(rows),
    )


ALERT_STATE = Path("/root/obsidian-telegram-bot/state/alerted.json")


async def cmd_alerty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    if not ALERT_STATE.is_file():
        await update.message.reply_text("Alerty jeszcze nie zainicjowane (brak state).")
        return
    try:
        data = json.loads(ALERT_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        await update.message.reply_text("Uszkodzony plik alertów.")
        return
    items = list((data.get("hashes") or {}).items())
    items.sort(key=lambda kv: (kv[1] or {}).get("sent") or "", reverse=True)
    rats = sum(1 for _, m in items if (m or {}).get("role") == "rat")
    steal = sum(1 for _, m in items if (m or {}).get("role") == "stealer")
    lines = [
        "🔔 *Alerty RAT / stealer*",
        f"w pamięci: RAT *{rats}* · stealer *{steal}*",
        "Nowe z pipeline / nightly przychodzą same.",
        "",
    ]
    for digest, meta in items[:8]:
        meta = meta or {}
        mark = "RAT" if meta.get("role") == "rat" else "STL"
        fam = meta.
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:22Z

    BotCommand("klasyfikuj", "Rola / pipeline"),
    BotCommand("alerty", "Ostatnie RAT / stealer"),
    # 📣 Kanał i content
    BotCommand("xmask", "Gotowce na kanał"),
    BotCommand("laik", "🧒 Dla laika"),
    BotCommand("kanal", "Kolejka Z warsztatu"),
    BotCommand("klip", "Montaż → kanał"),
    BotCommand("ig", "Instagram"),
]


async def _post_init(app: Application) -> None:
    try:
        await app.bot.delete_webhook(drop_pending_updates=False)
    except Exception as exc:  # noqa: BLE001
        log.warning("delete_webhook skip: %s", exc)
    try:
        await app.bot.set_my_commands([], scope=BotCommandScopeDefault())
        for uid in allowed_ids():
            await app.bot.set_my_commands(
                BOT_COMMANDS, scope=BotCommandScopeChat(chat_id=uid)
            )
    except Exception as exc:  # noqa: BLE001
        log.warning("set_my_commands skip: %s", exc)
    try:
        await app.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    except Exception as exc:  # noqa: BLE001
        log.warning("default menu skip: %s", exc)
    url = public_dash_url()
    if url.startswith("https://"):
        for uid in allowed_ids():
            try:
                await app.bot.set_chat_menu_button(
                    chat_id=uid,
                    menu_button=MenuButtonWebApp(text="Dashboard", web_app=WebAppInfo(url=url)),
                )
            except Exception as exc:  # noqa: BLE001
                log.warning("owner menu skip: %s", exc
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:47Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:47Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:53Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:53Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:53Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:53Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:58Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:58Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

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
#!/usr/bin/env python3
from __future__ import annotations

import unittest

import instagram as ig


class ParseCommandTests(unittest.TestCase):
    def test_empty_is_snapshot(self):
        self.assertEqual(ig.parse_command([]), "snapshot")

    def test_me(self):
  
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:06Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:06Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:42Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:42Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:19Z

bot.py:190:def remember_owner(user_id: int) -> None:
---dashboard.html hash param---
114:    .hash {
118:    .hashrow-inline { display: flex; align-items: center; gap: 8px; }
143:    .hashrow { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; border: 1px solid var(--line); border-radius: 12px; padding: 10px; margin-top: 8px; background: var(--panel2); }
177:    <p class="lead" id="lead">Nasze próbki z pipeline. Nic tu nie jest odpalane — tylko odczyt i hash.</p>
256:      { title: "LockBit / Akira", role: "ransomware", kind: "pe", q: "lockbit", how: "Po wejściu w sieć szyfruje dyski. U nas tylko intel + hash, bez odpalania." },
276:      const inTg = !!(window.TelegramWebviewProxy || /tgWebApp/i.test(location.hash + location.search));
304:      const digest = (ioc.hash || "").toLowerCase();
313:      const hist = (history.samples || []).find(s => s.hash === digest);
321:        defense: meta.defense || "Nie uruchamiaj. Zablokuj hash.",
327:      return Object.entries(catalog.samples || {}).map(([hash, meta]) => ({ hash, ...meta }));
332:      const fromCat = catalogEntries().find(e => e.hash.startsWith(s) || s.startsWith((e.hash || "").slice(0, 12)));
334:      const ioc = iocs.find(i => (i.hash || "").toLowerCase().startsWith(s));
335:      return ioc ? { hash: ioc.hash, ...describe(ioc), kind: ioc.kind } : null;
390:          ? "Katalog rodzin z labu. Szukaj hasha albo otwórz szczegóły."
392:            ? "Co krąży teraz. Przy k
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:19Z

-rwxr-xr-x 1 root   root   8404 Aug 15 03:25 /root/obsidian-vault/Narzedzia/alert_roles.py
-rwxr-xr-x 1 ubuntu ubuntu 4052 Aug 15 09:11 /root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh
---
/root/android-pipeline/bin/rat5_android_clean.sh:32:trap restore_path EXIT
---bot state dir---
total 16
drwxr-xr-x 2 root   root   4096 Aug 15 11:07 .
drwxrwxr-x 5 ubuntu ubuntu 4096 Aug 15 15:51 ..
-rw-r--r-- 1 root   root   1448 Aug 15 03:25 alerted.json
-rw-r--r-- 1 root   root   1365 Aug 15 11:19 channel_queue.json

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:26Z

276:      const inTg = !!(window.TelegramWebviewProxy || /tgWebApp/i.test(location.hash + location.search));
294:    async function copyHash(h) {
295:      try { await navigator.clipboard.writeText(h); toast("Skopiowano " + h.slice(0, 12) + "…"); }
313:      const hist = (history.samples || []).find(s => s.hash === digest);
432:        const h = 10 + Math.round((t.count || 0) / max * 64);
437:          <div class="stack" style="height:${h}px">${t.count ? segs : ""}</div>
450:        const hash = ioc.hash || "";
495:        const g = groups.get(key) || { ...e, hashes: [] };
550:      const live = sessions.filter(s => s.health === "live");
611:        const h = (r.sha256 || "").toLowerCase();
612:        if (!h || seen.has(h)) return;
613:        seen.add(h); rows.push(r);
615:      watched = rows.map(r => r.sha256.toLowerCase()).filter(h => h.length === 64);
662:        Object.entries(map).forEach(([h, job]) => applyJob(h, job));
788:        const h = (ex.hash || "").toLowerCase();
789:        if (h && !seen.has(h)) { iocs.push(ex); seen.add(h); }
793:      if (u.searchParams.get("role")) filt.role = u.searchParams.get("role");
794:      if (u.searchParams.get("tab")) setTab(u.searchParams.get("tab"));
796:      const h = u.searchParams.get("hash") || u.searchParams.get("h");
797:      if (h) hunt(h);

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:26Z

276:      const inTg = !!(window.TelegramWebviewProxy || /tgWebApp/i.test(location.hash + location.search));
495:        const g = groups.get(key) || { ...e, hashes: [] };
793:      if (u.searchParams.get("role")) filt.role = u.searchParams.get("role");
794:      if (u.searchParams.get("tab")) setTab(u.searchParams.get("tab"));
796:      const h = u.searchParams.get("hash") || u.searchParams.get("h");
--- obsidian bot dashboard.html full param refs ---
180:      <button class="tab on" type="button" data-tab="lab">Próbki</button>
181:      <button class="tab" type="button" data-tab="all">Katalog</button>
182:      <button class="tab" type="button" data-tab="know">Co krąży</button>
183:      <button class="tab" type="button" data-tab="c2">Sliver</button>

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:33Z

OK bin/batch_analyze.sh
OK bin/download_malwarebazaar.sh
OK bin/install.sh
OK bin/nightly_pipeline.sh
OK bin/osint_recon.sh
OK bin/pipeline.sh
OK bin/rat5_android_clean.sh
OK bin/rat5_clean_run.sh
OK bin/recon_osint.sh

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:33Z

bot-only check:
bot.py OK

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:37Z

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
OK web/serve.py

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:37Z

465:  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
467:    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
468:  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
470:    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
472:  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
474:    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
477:  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
479:    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
554:if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
556:  "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
557:  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
559:    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
562:if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
564:  "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:40Z

log "Samples root:  $SAMPLES_ROOT"
log "Quarantine:    $QUARANTINE_DIR"
log "Python:        $PYTHON"
log "jadx:          ${JADX_BIN:-MISSING}"
log "apktool:       ${APKTOOL_BIN:-MISSING}"
log "analyze_pe.py: $ANALYZE_PE_PY"

if [[ "$AGG_ONLY" == "1" ]]; then
  aggregate
  generate_auto_yara
  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
    log "Tagging report roles (rat/stealer/backdoor/…)"
    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
    log "Hunt phishing/stealer IOCs"
    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
  fi
  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
    log "Alert RAT/stealer -> Telegram"
    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
  fi
  fi
  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
    log "CTI enrichment (MalwareBazaar/URLhaus/VT/…)"
    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
  fi
  exit 0
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  preprocess_raw
else
  dir_target=0
  for t in "${TARGETS[@]}"; do
    [[ -d "$t" ]] && dir_target=1
  done
  if [[ "$dir_target" -eq 1 ]]; then
    log "Directory target — running zip preprocess"
    preprocess_raw
  else
    log "Explicit t
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:54Z

19:CLASSIFY_PY="${PIPELINE_HOME}/lib/classify_roles.py"
135:# --- 3b) classify_roles ZAWSZE (nawet gdy pipeline.sh nie wszedł) ---
136:ROLE_COUNTS="{}"
138:  log "classify_roles.py → $REPORTS_DIR"
140:  ROLE_OUT="$("$PYTHON" "$CLASSIFY_PY" "$REPORTS_DIR" 2>>"$LOG_FILE")"
143:  log "classify_roles exit=$rc"
144:if [[ -f "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" ]]; then
146:  "$PYTHON" "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" >>"$LOG_FILE" 2>&1 || log "hunt failed (non-fatal)"
148:  echo "$ROLE_OUT" | tee -a "$LOG_FILE" >/dev/null
149:  ROLE_COUNTS="$(echo "$ROLE_OUT" | awk '/^counts /{sub(/^counts /,""); print; exit}')"
150:  [[ -n "$ROLE_COUNTS" ]] || ROLE_COUNTS="{}"
152:  log "BRAK classify_roles.py / python — pomijam tagging"
242:  echo "## Role tags (classify_roles.py)"
245:  echo "${ROLE_COUNTS}"

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:57Z

# --- 3b) classify_roles ZAWSZE (nawet gdy pipeline.sh nie wszedł) ---
ROLE_COUNTS="{}"
if [[ -f "$CLASSIFY_PY" && -x "$PYTHON" ]]; then
  log "classify_roles.py → $REPORTS_DIR"
  set +e
  ROLE_OUT="$("$PYTHON" "$CLASSIFY_PY" "$REPORTS_DIR" 2>>"$LOG_FILE")"
  rc=$?
  set -e
  log "classify_roles exit=$rc"
if [[ -f "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" ]]; then
  log "hunt phishing/stealer"
  "$PYTHON" "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" >>"$LOG_FILE" 2>&1 || log "hunt failed (non-fatal)"
fi
  echo "$ROLE_OUT" | tee -a "$LOG_FILE" >/dev/null
  ROLE_COUNTS="$(echo "$ROLE_OUT" | awk '/^counts /{sub(/^counts /,""); print; exit}')"
  [[ -n "$ROLE_COUNTS" ]] || ROLE_COUNTS="{}"
else
  log "BRAK classify_roles.py / python — pomijam tagging"
fi

# --- 3c) export do vault ---

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:33Z

./.venv/lib/python3.12/site-packages/anyio/to_interpreter.py:149:            raise NotImplementedError
./.venv/lib/python3.12/site-packages/anyio/streams/tls.py:269:                raise NotImplementedError(
./.venv/lib/python3.12/site-packages/anyio/streams/tls.py:274:        raise NotImplementedError(
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:1200:        except NotImplementedError:
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:1593:                    except (ValueError, NotImplementedError):
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:1618:            except (ValueError, NotImplementedError):
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:2925:        except NotImplementedError:
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:2978:        except NotImplementedError:
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:3023:                except NotImplementedError:
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:3045:                except NotImplementedError:
./.venv/lib/python3.12/site-packages/anyio/_core/_testing.py:40:        return NotImplemented
./.venv/lib/python3.12/site-packages/anyio/_core/_synchronization.py:93:        raise NotImplementedError
./.venv/lib/python3.12/site-packages/anyio/_core/_synchronization.py:97:        raise NotImplementedError
./.venv/lib/python3.12/site-packages/anyio/_core/_synchronization.py:107:        raise 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:33Z

lib/alert_takeovers.py:107:            pass
lib/analyze_pe.py:132:            pass
lib/analyze_pe.py:268:        pass
lib/analyze_static.py:185:        pass
lib/analyze_static.py:224:        pass
lib/analyze_static.py:274:        pass
lib/analyze_static.py:457:        pass
lib/analyze_static.py:463:        pass
lib/classify_roles.py:236:        return
lib/classify_roles.py:240:        return
lib/enrich_cti.py:277:            return
lib/enrich_cti.py:368:            pass
lib/enrich_cti.py:433:            return
lib/extract_domains.py:61:        return
lib/extract_domains.py:65:        return
lib/extract_domains.py:67:        return
lib/extract_domains.py:70:        return
lib/extract_domains.py:72:        return
lib/extract_domains.py:113:            pass
lib/hunt_phishing_stealer.py:48:                pass
lib/sigma_generator.py:63:            pass
lib/sigma_generator.py:345:            pass
lib/yara_generator.py:292:            return
lib/yara_generator.py:297:            return
lib/yara_generator.py:299:            return
lib/yara_generator.py:303:            return
lib/yara_generator.py:330:            return
lib/yara_generator.py:367:        return

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:44Z

Edited /root/android-pipeline/bin/pipeline.sh (13 lines -> 13 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:51Z

Edited /root/android-pipeline/bin/pipeline.sh (8 lines -> 12 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:56Z

Edited /root/android-pipeline/bin/nightly_pipeline.sh (11 lines -> 11 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:00Z

#!/usr/bin/env bash
set -euo pipefail

STAMP=$(date -u +%Y%m%dT%H%M%SZ)
ROOT="/root/samples/rat5_${STAMP}"
PATH_SH="/root/android-pipeline/config/path.sh"
PATH_BAK="/root/android-pipeline/config/path.sh.bak.rat5run"
PIDFILE="/root/samples/rat5_latest.pid"

mkdir -p "$ROOT"/{raw,quarantine,decompiled,sources,reports,features,native,logs,output}
ln -sfn "$ROOT" /root/samples/rat5_latest

# API key
MB_API_KEY=""
if [[ -f /root/android-pipeline/config/secrets.env ]]; then
  # shellcheck disable=SC1090
  source /root/android-pipeline/config/secrets.env
fi
if [[ -z "${MB_API_KEY:-}" && -f /root/.mb_api_key ]]; then
  MB_API_KEY=$(tr -d ' \t\r\n' < /root/.mb_api_key)
  export MB_API_KEY
fi
if [[ -z "${MB_API_KEY:-}" ]]; then
  echo "NO MB_API_KEY" >&2
  exit 1
fi
export MB_API_KEY

# Temporarily retarget path.sh
cp -a "$PATH_SH" "$PATH_BAK"
sed -i "s|export SAMPLES_ROOT=\"/root/samples\"|export SAMPLES_ROOT=\"$ROOT\"|" "$PATH_SH"

restore_path() {
  if [[ -f "$PATH_BAK" ]]; then
    mv -f "$PATH_BAK" "$PATH_SH"
    echo "[restore] path.sh -> /root/samples" | tee -a "$LOG" || true
  fi
}

export MB_TAG=rat
export MB_LIMIT=5
export FORCE=1
export SKIP_GHIDRA=1
export PATH="/root/android-pipeline/tools/jadx/bin:/root/android-pipeline/tools/apktool:/root/android-pipeline/bin:${PATH}"


### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:04Z

Edited /root/android-pipeline/bin/rat5_clean_run.sh (8 lines -> 9 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:08Z

pipeline.sh OK
nightly_pipeline.sh OK
rat5_clean_run.sh OK

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:11Z

if [[ "$AGG_ONLY" == "1" ]]; then
  aggregate
  generate_auto_yara
  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
    log "Tagging report roles (rat/stealer/backdoor/…)"
    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
  fi
  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
    log "Hunt phishing/stealer IOCs"
    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
  fi
  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
    log "Alert RAT/stealer -> Telegram"
    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
  fi
  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
    log "CTI enrichment (MalwareBazaar/URLhaus/VT/…)"
    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
  fi
  exit 0
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  preprocess_raw
=== main flow ===
generate_auto_yara
if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
  log "Tagging report roles (rat/stealer/backdoor/…)"
  "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
fi
if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
  log "Hunt phishing/stealer IOCs"
  "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stea
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:17Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:17Z

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
