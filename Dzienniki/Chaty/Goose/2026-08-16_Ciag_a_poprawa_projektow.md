---
title: "Ciągła poprawa projektów"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260816_2
cwd: "/root"
messages: 96
tool_calls: 94
status: archived
---

# Ciągła poprawa projektów

> Zapis czatu **Goose** · sesja '20260816_2' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | # OPTYMALIZATOR — ciągła poprawa niedokończonych projektów |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 0 |
| Akcji narzędziowych | 94 |
| Narzędzia | 'tool'×47, 'result'×47 |
| Pliki | '/root/android-pipeline' · '/root/android-pipeline/.venv' · '/root/android-pipeline/.venv/bin/python' · '/root/android-pipeline/lib/classify_roles.py' · '/root/android-pipeline/tools' · '/root/obsidian-telegram-bot/.venv/bin/python' · '/root/obsidian-telegram-bot/alert_roles.py' · '/root/obsidian-telegram-bot/bot.py' · '/root/obsidian-telegram-bot/classify_roles.py' · '/root/obsidian-telegram-bot/dashboard.py' · '/root/obsidian-vault/Narzedzia/alert_roles.py' · '/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh' · '/root/obsidian-vault/Narzedzia/serve_dashboard.py' · '/root/samples' · '/root/samples/quarantine/' · '/root/samples/re_lab_latest' · '/root/samples/reports' · '/root/samples/reports/' · '/root/samples/reports/iocs.json' · '/root/samples/reports/sigma' |
| IP | '0.0.0.0' |
| Hosty | 'android.com' · 'apache.org' · 'example.com' · 'github.com' · 'google.com' · 'instagram.com' · 'mozilla.org' · 'oracle.com' · 'w3.org' |

## Pełny zapis

### 👤 Użytkownik — 2026-08-16T00:31:34Z

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

### 👤 Użytkownik — 2026-08-16T00:31:34Z

<turn-context>
<current-time>2026-08-16 00:31:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:39Z

Updated (532 chars)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:41Z

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


### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:41Z

bin/  [1K]
  batch_analyze.sh  [268]
  download_malwarebazaar.sh  [106]
  install.sh  [221]
  nightly_pipeline.sh  [298]
  osint_recon.sh  [140]
  pipeline.sh  [579]
  rat5_android_clean.sh  [180]
  rat5_clean_run.sh  [93]
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
  analyze_static.py  [487]
  classify_roles.py  [292]
  deep_re_pass.py  [223]
  enrich_cti.py  [571]
  extract_domains.py  [134]
  hunt_phishing_stealer.py  [216]
  sigma_generator.py  [358]
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

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:45Z

  2439 bot.py
   436 graj.py
   354 vault.py
   166 dashboard.py
   326 content.py
   257 alert_roles.py
   292 classify_roles.py
   432 instagram.py
    46 laik.py
    56 publish_channel.py
   565 render.py
   305 studio.py
    41 test_content.py
    64 test_instagram.py
    28 test_studio.py
    37 test_vault.py
  5844 total

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:45Z

   268 bin/batch_analyze.sh
   106 bin/download_malwarebazaar.sh
   221 bin/install.sh
   298 bin/nightly_pipeline.sh
   140 bin/osint_recon.sh
   579 bin/pipeline.sh
   180 bin/rat5_android_clean.sh
    93 bin/rat5_clean_run.sh
    91 bin/recon_osint.sh
   140 lib/aggregate_patterns.py
   188 lib/alert_takeovers.py
   454 lib/analyze_pe.py
   487 lib/analyze_static.py
   292 lib/classify_roles.py
   223 lib/deep_re_pass.py
   571 lib/enrich_cti.py
   134 lib/extract_domains.py
   216 lib/hunt_phishing_stealer.py
   358 lib/sigma_generator.py
   421 lib/yara_generator.py
     8 config/path.sh
    34 tools/detection/README.md
   119 tools/detection/all_lab.rules
    26 tools/detection/keylogger_exfil.rules
    13 tools/detection/laplas_clipper.rules
    18 tools/detection/lumma_digitden.rules
    61 tools/detection/phishing_tools.rules
    56 tools/detection/phishing_tools.zeek
    19 tools/detection/xworm_tuffman.rules
    34 tools/sigma-rules/README.md
    24 tools/sigma-rules/lumma_digitden_dns.yml
    24 tools/sigma-rules/xmask_network_hosts.yml
    25 tools/sigma-rules/xmask_pe_hashes_file.yml
    25 tools/sigma-rules/xmask_pe_hashes_process.yml
    25 tools/sigma-rules/xmask_role_backdoor_hashes.yml
    28 tools/sigma-rules/xmask_win_account_api_cluster.yml
    24 tools/sigma-rules/xworm_tuffman_dns.yml
    73 tools/yara-rules/index_gen.sh
  6096 total

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:47Z

  2390	    app.add_handler(CommandHandler("channel", cmd_kanal))
  2391	    app.add_handler(CommandHandler("klip", cmd_klip))
  2392	    app.add_handler(CallbackQueryHandler(on_klip_cb, pattern=r"^klip:"))
  2393	    app.add_handler(CommandHandler("graj", cmd_graj))
  2394	    app.add_handler(CommandHandler("gra", cmd_graj))
  2395	    app.add_handler(CommandHandler("play", cmd_graj))
  2396	    app.add_handler(CallbackQueryHandler(on_graj_cb, pattern=r"^graj"))
  2397	    app.add_handler(
  2398	        MessageHandler(
  2399	            filters.VIDEO
  2400	            | filters.VIDEO_NOTE
  2401	            | filters.VOICE
  2402	            | filters.AUDIO
  2403	            | filters.Document.VIDEO
  2404	            | filters.Document.AUDIO,
  2405	            on_studio_media,
  2406	        )
  2407	    )
  2408	    app.add_handler(new_note)
  2409	    app.add_handler(append_conv)
  2410	    app.add_handler(CallbackQueryHandler(on_obsidian_cb, pattern=r"^ob:"))
  2411	    app.add_handler(CallbackQueryHandler(on_wiedza_cb, pattern=r"^wiedza:"))
  2412	    app.add_handler(CallbackQueryHandler(on_ig_cb, pattern=r"^ig:"))
  2413	    app.add_handler(CallbackQueryHandler(on_kanal_cb, pattern=r"^kanal:"))
  2414	    app.add_handler(CallbackQueryHandler(on_callback, pattern=r"^(get|dash|xmask|laik|jobadd|jobcls):"))
  2415	    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_plain))
  2416	    app.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHan
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:49Z

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

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:52Z

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


def _ob_folder_markup(vault: Vault, folder: str, page: int = 0) -> InlineKeyboardMarkup:
    subs, notes = vault.browse(folder)
    rows: list[list[Inlin
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:54Z

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

async def cmd_graj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await g
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:55Z

    lines = [
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
    with urllib.request.urlop
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:31:57Z

        return
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
    if action in {"v",
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:00Z

    target = update.callback_query.message if via_callback else update.message
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
    if not await
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:18Z

     1	"""Gra edukacyjna dla studentów cyberbezpieczeństwa (nauka obrony).
     2	
     3	Przepływ: /graj → poziom → atak (historia) → metoda → ATAK → OBRONA → quiz.
     4	
     5	Każdy atak ma: historię (scenariusz SOC), metody ataku (pełne kroki),
     6	sposoby obrony (pełne kroki) i quiz sprawdzający.
     7	"""
     8	from __future__ import annotations
     9	
    10	from telegram import InlineKeyboardButton
    11	
    12	LEVELS: list[dict] = [
    13	    {"id": "easy", "label": "🟢 ŁATWY", "desc": "socjotechnika i proste techniki (phishing, keylogger, clipper)"},
    14	    {"id": "medium", "label": "🟡 ŚREDNI", "desc": "stealery i przejęcia kont (Lumma, Telegram, OSINT)"},
    15	    {"id": "hard", "label": "🔴 TRUDNY", "desc": "AiTM, RAT i obfuskacja (Evilginx, XWorm, garble)"},
    16	]
    17	
    18	ATTACKS: dict[str, dict] = {
    19	    # ================= 🟢 EASY =================
    20	    "phishing": {
    21	        "name": "Phishing",
    22	        "level": "easy",
    23	        "meta": "Niska trudność · Wysoki zasięg · Socjotechnika",
    24	        "story": (
    25	            "Jesteś analitykiem SOC w firmie Acme Corp. Pracownicy co tydzień zgłaszają "
    26	            "podejrzane maile i linki. Twoje zadanie: rozpoznać każdą metodę phishingu, "
    27	            "zrozumieć jak działa i wiedzieć, jak przed nią bronić."
    28	        ),
    29	        "methods": [
    30	            {
    31	                "name": "Klon strony (SET Credential Harves
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:18Z

     1	"""Safe read/write/search helpers for a local Obsidian vault."""
     2	
     3	from __future__ import annotations
     4	
     5	import re
     6	import time
     7	from dataclasses import dataclass
     8	from datetime import datetime, timezone
     9	from pathlib import Path
    10	
    11	
    12	SKIP_DIRS = {".obsidian", ".trash", ".git", ".smart-env", "node_modules", "__pycache__"}
    13	TELEGRAM_LIMIT = 3900
    14	
    15	
    16	@dataclass(frozen=True)
    17	class Note:
    18	    path: Path
    19	    rel: str
    20	    title: str
    21	    mtime: float
    22	
    23	    @property
    24	    def wiki(self) -> str:
    25	        return f"[[{self.path.stem}]]"
    26	
    27	    @property
    28	    def folder(self) -> str:
    29	        parent = str(Path(self.rel).parent)
    30	        return "" if parent == "." else parent
    31	
    32	
    33	def utc_now() -> datetime:
    34	    return datetime.now(timezone.utc)
    35	
    36	
    37	def slug_title(title: str) -> str:
    38	    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", title).strip().strip(".")
    39	    cleaned = re.sub(r"\s+", " ", cleaned)
    40	    return cleaned[:120] or "notatka"
    41	
    42	
    43	class Vault:
    44	    def __init__(
    45	        self,
    46	        root: Path,
    47	        inbox: str = "Inbox",
    48	        telegram_log: str = "Dzienniki/Telegram",
    49	    ) -> None:
    50	        self.root = Path(root).expanduser().resolve()
    51	        self.inbox = 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:30Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:30Z

     1	"""Fetch pipeline IOC dashboard and attach virus descriptions."""
     2	
     3	from __future__ import annotations
     4	
     5	import json
     6	import os
     7	import time
     8	import urllib.error
     9	import urllib.request
    10	from pathlib import Path
    11	from typing import Any
    12	
    13	
    14	CATALOG_PATH = Path(__file__).resolve().parent / "virus_catalog.json"
    15	DEFAULT_DASHBOARD = "http://127.0.0.1:8080/iocs.json"
    16	_CATALOG: dict[str, Any] = {"mtime": None, "data": None}
    17	_IOC: dict[str, Any] = {"ts": 0.0, "data": None}
    18	_IOC_TTL = 20.0
    19	
    20	
    21	def _local_iocs_path() -> Path | None:
    22	    env = os.getenv("IOC_JSON", "").strip()
    23	    candidates = []
    24	    if env:
    25	        candidates.append(Path(env))
    26	    candidates.extend(
    27	        (
    28	            Path("/var/www/ioc-dashboard/iocs.json"),
    29	            Path("/root/samples/reports/iocs.json"),
    30	        )
    31	    )
    32	    for path in candidates:
    33	        if path.is_file():
    34	            return path
    35	    return None
    36	
    37	
    38	def load_catalog(path: Path | None = None) -> dict[str, Any]:
    39	    target = path or CATALOG_PATH
    40	    if not target.is_file():
    41	        alt = Path("/var/www/ioc-dashboard/catalog.json")
    42	        target = alt if alt.is_file() else target
    43	    if not target.is_file():
    44	        return {"samples": {}, "families": {}}
 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:45Z

     1	#!/usr/bin/env python3
     2	"""Job store for /klip: counts → prompt → files → render → channel."""
     3	
     4	from __future__ import annotations
     5	
     6	import json
     7	import os
     8	import re
     9	import shutil
    10	import subprocess
    11	import sys
    12	import uuid
    13	from datetime import datetime, timezone
    14	from pathlib import Path
    15	from typing import Any
    16	
    17	ROOT = Path(os.getenv("XMASK_STUDIO", "/root/xmask-studio"))
    18	RENDER = Path(__file__).resolve().parent / "render.py"
    19	MAX_FILE = int(os.getenv("XMASK_MAX_UPLOAD_MB", "19")) * 1024 * 1024
    20	MAX_SLOTS = 5
    21	SERIES = {
    22	    "hackplug": "hackplug",
    23	    "hp": "hackplug",
    24	    "hacker": "hackplug",
    25	    "opsec": "opsec",
    26	    "ox": "opsec",
    27	    "opsec.exe": "opsec",
    28	    "intro": "intro",
    29	}
    30	CAPTION_PREFIX = {
    31	    "hackplug": "XMASK - HACKPLUG",
    32	    "opsec": "xmask_opsec.exe",
    33	    "intro": "XMask",
    34	}
    35	
    36	
    37	def utc_now() -> str:
    38	    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    39	
    40	
    41	def user_dir(user_id: int) -> Path:
    42	    path = ROOT / "jobs" / str(user_id)
    43	    path.mkdir(parents=True, exist_ok=True)
    44	    return path
    45	
    46	
    47	def _meta(path: Path) -> dict[str, Any]:
    48	    return json.loads(path.read_text(encoding="utf-8"))
    49	
    50	
    51	def _write(path:
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:32:54Z

     1	#!/usr/bin/env python3
     2	"""Official Instagram Graph analytics for the connected Professional account.
     3	
     4	Counts, demographics, and deltas only. No follower/following nick lists.
     5	"""
     6	
     7	from __future__ import annotations
     8	
     9	import json
    10	import logging
    11	import os
    12	import urllib.error
    13	import urllib.parse
    14	import urllib.request
    15	from datetime import datetime, timezone
    16	from pathlib import Path
    17	from typing import Any
    18	
    19	log = logging.getLogger("obsidian-bot.instagram")
    20	
    21	STATE_DIR = Path(__file__).resolve().parent / "state" / "instagram"
    22	DEFAULT_BASE = "https://graph.instagram.com"
    23	DEFAULT_VERSION = "v25.0"
    24	PROFILE_FIELDS = (
    25	    "id,user_id,username,name,account_type,followers_count,follows_count,"
    26	    "media_count,profile_picture_url"
    27	)
    28	DEMO_BREAKDOWNS = ("gender", "age", "country")
    29	TOP_N = 8
    30	
    31	
    32	class InstagramError(RuntimeError):
    33	    pass
    34	
    35	
    36	def utc_now() -> datetime:
    37	    return datetime.now(timezone.utc)
    38	
    39	
    40	def config() -> dict[str, str]:
    41	    return {
    42	        "token": os.getenv("IG_ACCESS_TOKEN", "").strip(),
    43	        "user_id": os.getenv("IG_USER_ID", "").strip(),
    44	        "username": os.getenv("IG_USERNAME", "").strip().lstrip("@").lower(),
    45	        "base": (os.getenv("IG_GRAPH_BASE", DE
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:00Z

     1	#!/usr/bin/env bash
     2	# One-shot batch malware analysis pipeline (defensive research lab).
     3	# Android APK + Windows PE (quarantine / raw).
     4	# Usage:
     5	#   pipeline.sh                  # process APK+PE in ~/samples/raw and ~/samples/quarantine
     6	#   pipeline.sh /path/to/sample  # single file (apk/exe/dll/zip)
     7	#   pipeline.sh --pe-only /root/samples/quarantine/  # PE w katalogu
     8	#   pipeline.sh --aggregate-only # only rebuild CSV/patterns from existing reports
     9	#   pipeline.sh --pe-only        # skip APK
    10	#   pipeline.sh --apk-only       # skip PE
    11	set -euo pipefail
    12	
    13	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    14	# shellcheck disable=SC1091
    15	[[ -f "$PIPELINE_HOME/config/path.sh" ]] && source "$PIPELINE_HOME/config/path.sh"
    16	[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"
    17	
    18	SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
    19	RAW_DIR="${RAW_DIR:-$SAMPLES_ROOT/raw}"
    20	DECOMPILED_DIR="${DECOMPILED_DIR:-$SAMPLES_ROOT/decompiled}"
    21	SOURCES_DIR="${SOURCES_DIR:-$SAMPLES_ROOT/sources}"
    22	REPORTS_DIR="${REPORTS_DIR:-$SAMPLES_ROOT/reports}"
    23	FEATURES_DIR="${FEATURES_DIR:-$SAMPLES_ROOT/features}"
    24	NATIVE_DIR="${NATIVE_DIR:-$SAMPLES_ROOT/native}"
    25	QUARANTINE_DIR="${QUARANTINE_DIR:-$SAMPLES_ROOT/quarantine}"
    26	LOGS_DIR="${LOGS_DIR:-$SAMPLES_ROOT/logs}"
    27	PE_DIR="${PE_DIR:-$SAMPLES_ROO
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:41Z

lrwxrwxrwx 1 root root 7 Aug 14 23:12 .venv/bin/python -> python3
---
OK bot.py
OK graj.py
OK vault.py
OK dashboard.py
OK content.py
OK instagram.py
OK laik.py
OK publish_channel.py
OK render.py
OK studio.py
OK alert_roles.py
OK classify_roles.py
OK test_content.py
OK test_instagram.py
OK test_studio.py
OK test_vault.py

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:41Z

OK bin/batch_analyze.sh
OK bin/download_malwarebazaar.sh
OK bin/install.sh
OK bin/nightly_pipeline.sh
OK bin/osint_recon.sh
OK bin/pipeline.sh
OK bin/rat5_android_clean.sh
OK bin/rat5_clean_run.sh
OK bin/recon_osint.sh
--- python ---
using /root/android-pipeline/.venv/bin/python
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

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:47Z

-rwxr-xr-x 1 root   root   8404 Aug 15 03:25 /root/obsidian-vault/Narzedzia/alert_roles.py
-rwxr-xr-x 1 ubuntu ubuntu 4052 Aug 15 09:11 /root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh
--- bot alert_roles ---
-rwxr-xr-x 1 root root 8404 Aug 15 03:25 /root/obsidian-telegram-bot/alert_roles.py
--- android-pipeline lib classify_roles vs bot ---
-rwxr-xr-x 1 root   root   9845 Aug 15 09:16 /root/android-pipeline/lib/classify_roles.py
-rw-rw-r-- 1 ubuntu ubuntu 9825 Aug 15 09:15 /root/obsidian-telegram-bot/classify_roles.py

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:47Z

     1	#!/usr/bin/env bash
     2	# Download Android APK samples from MalwareBazaar into ~/samples/raw/
     3	# Requires: MB_API_KEY from https://bazaar.abuse.ch/api/
     4	# Usage:
     5	#   export MB_API_KEY=...
     6	#   download_malwarebazaar.sh              # recent apk by tag
     7	#   download_malwarebazaar.sh SHA256...    # specific hash
     8	set -euo pipefail
     9	
    10	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    11	# shellcheck disable=SC1091
    12	[[ -f "$PIPELINE_HOME/config/path.sh" ]] && source "$PIPELINE_HOME/config/path.sh"
    13	[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"
    14	
    15	RAW_DIR="${RAW_DIR:-$HOME/samples/raw}"
    16	QUARANTINE_DIR="${QUARANTINE_DIR:-$HOME/samples/quarantine}"
    17	MB_API_KEY="${MB_API_KEY:-}"
    18	MB_TAG="${MB_TAG:-apk}"
    19	MB_LIMIT="${MB_LIMIT:-20}"
    20	API="https://mb-api.abuse.ch/api/v1/"
    21	
    22	mkdir -p "$RAW_DIR" "$QUARANTINE_DIR"
    23	
    24	if [[ -z "$MB_API_KEY" ]]; then
    25	  echo "Set MB_API_KEY (MalwareBazaar API key)." >&2
    26	  exit 1
    27	fi
    28	
    29	download_hash() {
    30	  local h="$1"
    31	  local out="$QUARANTINE_DIR/${h}.zip"
    32	  echo "[+] get_file $h"
    33	  curl -fsS -X POST "$API" \
    34	    -d "query=get_file" \
    35	    -d "sha256_hash=${h}" \
    36	    -H "Auth-Key: ${MB_API_KEY}" \
    37	    -o "$out" || {
    38	      # older API style
    39	      curl -fsS -X POST "$A
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:33:54Z

     1	#!/usr/bin/env python3
     2	"""Static feature extraction for Windows PE (defensive malware research).
     3	
     4	Outputs JSON + Markdown + HTML reports. Uses pefile when available;
     5	falls back to header/string heuristics.
     6	"""
     7	from __future__ import annotations
     8	
     9	import argparse
    10	import hashlib
    11	import json
    12	import math
    13	import os
    14	import re
    15	import shutil
    16	import struct
    17	import subprocess
    18	import sys
    19	from collections import Counter
    20	from datetime import datetime, timezone
    21	from pathlib import Path
    22	from typing import Any
    23	
    24	SUSPICIOUS_STRING_RE = re.compile(
    25	    r"(https?://|wss?://|\bapi\b|\bbot\b|\btoken\b|exodus|metamask|trustwallet|"
    26	    r"wallet|cmd\.exe|powershell|pwsh|reg add|schtasks|bitsadmin|certutil|"
    27	    r"rundll32|regsvr32|mshta|wscript|cscript|AppData|\\Temp\\|VirtualAlloc|"
    28	    r"WriteProcessMemory|CreateRemoteThread|NtUnmapViewOfSection|"
    29	    r"HKEY_|SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run|"
    30	    r"telegram|discord|webhook|steal|inject|ransom|bitcoin|mnemonic)",
    31	    re.I,
    32	)
    33	URL_RE = re.compile(r"https?://[^\s\"'<>\\]{4,200}", re.I)
    34	IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    35	SUSPICIOUS_IMPORTS = {
    36	    "virtualalloc",
    37	    "virtualallocex",
    38	    "virtualprotect",
    39	    "writeprocessmemory",
    40	    "createrem
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:06Z

     1	#!/usr/bin/env python3
     2	"""Generate Sigma (SIEM) rules from pipeline IOC reports.
     3	
     4	Companion to yara_generator.py. Reads reports/*.json or iocs.json and writes
     5	YAML rules a SOC can drop into Sigma → Splunk/Elastic/Microsoft Sentinel.
     6	
     7	Usage:
     8	  sigma_generator.py /root/samples/reports
     9	  sigma_generator.py /root/samples/reports /root/samples/reports/sigma
    10	"""
    11	
    12	from __future__ import annotations
    13	
    14	import json
    15	import re
    16	import sys
    17	import uuid
    18	from collections import defaultdict
    19	from datetime import date
    20	from pathlib import Path
    21	
    22	SKIP_JSON = {
    23	    "iocs.json",
    24	    "patterns_summary.json",
    25	    "re_static_iocs.json",
    26	    "features.json",
    27	    "summary.json",
    28	    "sigma_index.json",
    29	}
    30	
    31	NOISE_HOST = re.compile(
    32	    r"(schemas\.android\.com|www\.w3\.org|xmlns|mozilla\.org|apache\.org|"
    33	    r"opensource\.org|play\.google\.com|googleapis\.com|localhost|"
    34	    r"publicsuffix\.org|youtrack\.jetbrains|react\.dev|tailwindcss)",
    35	    re.I,
    36	)
    37	
    38	NS = uuid.UUID("8f3a1c2e-5b7d-4a9e-9c0b-2f6d1e8a4b01")
    39	
    40	
    41	def _yaml_escape(s: str) -> str:
    42	    return s.replace("'", "''")
    43	
    44	
    45	def _ident(name: str) -> str:
    46	    ident = re.sub(r"[^A-Za-z0-9_.-]+", "-", name or "sample").strip("-")
    47	    retu
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:14Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:14Z

     1	#!/usr/bin/env python3
     2	"""
     3	enrich_cti.py — wzbogacanie IOC z baz danych o wirusach / threat-intel.
     4	
     5	Czyta raporty pipeline'a (/root/samples/reports/<SHA256>/*.json + iocs.json),
     6	wyciąga IoC (hash, URL, domena, IP) i odpytuje zewnętrzne bazy:
     7	
     8	  * MalwareBazaar  (abuse.ch)  — hash  -> get_info        (klucz: MB_API_KEY)
     9	  * URLhaus        (abuse.ch)  — URL/domain -> /url/,/host/(ten sam klucz abuse.ch)
    10	  * VirusTotal     (v3)        — hash  -> /files/{id}     (klucz: VT_API_KEY)
    11	  * AbuseIPDB      (v2)        — IP    -> /check          (klucz: ABUSEIPDB_KEY)
    12	  * AlienVault OTX             — IP/domain/hash -> indicators (klucz: OTX_KEY)
    13	
    14	Bazy bez klucza są pomijane (nie krytyczne). Wynik:
    15	  <reports>/cti_enrichment.json   — pełne dane
    16	  <reports>/cti_enrichment.md     — podsumowanie trafień
    17	
    18	Użycie:
    19	  python3 enrich_cti.py [REPORTS_DIR] [--limit N] [--offline]
    20	"""
    21	from __future__ import annotations
    22	
    23	import argparse
    24	import json
    25	import os
    26	import re
    27	import sys
    28	import threading
    29	import time
    30	from concurrent.futures import ThreadPoolExecutor, as_completed
    31	from urllib.error import URLError
    32	from urllib.parse import urlencode, urlparse
    33	from urllib.request import Request, urlopen
    34	
    35	UA = {"User-Agent": "android-pipeline/1.0 (defensive lab)"}
    36	R
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:22Z

     1	#!/usr/bin/env python3
     2	import re, json, sys
     3	from pathlib import Path
     4	from collections import defaultdict
     5	
     6	lab = Path(sys.argv[1] if len(sys.argv) > 1 else "/root/samples/re_lab_latest").resolve()
     7	src_root = lab / "output" / "sources"
     8	reports_root = Path("/root/samples/reports")
     9	
    10	re_url = re.compile(r"https?://[^\s\"'<>]{6,200}", re.I)
    11	re_ip = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")
    12	re_host = re.compile(
    13	    r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|ru|cn|br|io|xyz|top|cc|su|info|biz|invalid|internal|tk|pw|me|co)(?::\d{2,5})?\b",
    14	    re.I,
    15	)
    16	
    17	noise = (
    18	    "schemas.android", "apache.org", "w3.org", "mozilla.org", "googlesource", "github.com",
    19	    "example.com", "google.com", "creativecommons", "jetbrains", "kotlinlang", "android.com",
    20	    "play.google", "maven.", "gradle", "sourceforge", "oracle.com", "openjdk", "junit",
    21	)
    22	
    23	lib_noise = (
    24	    "androidx/", "android/support/", "kotlin/", "okhttp3/", "com/google/", "org/apache/",
    25	    "com/squareup/", "retrofit2/", "io/reactivex/", "javax/", "org/json/", "okio/",
    26	)
    27	
    28	keywords = [
    29	    "Socket", "HttpURLConnection", "OkHttp", "WebSocket", "SmsManager", "sendTextMessage",
    30	    "AccessibilityService", "DeviceAdminReceiver", "Camera", "MediaProjection",
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:47Z

     1	#!/usr/bin/env python3
     2	from __future__ import annotations
     3	
     4	import tempfile
     5	import unittest
     6	from pathlib import Path
     7	from unittest import mock
     8	
     9	import content as ch
    10	
    11	
    12	class QueueTests(unittest.TestCase):
    13	    def test_next_due_picks_oldest_overdue(self):
    14	        data = {
    15	            "posts": [
    16	                {"id": "b", "file": "b.md", "due": "2026-08-17", "published": None},
    17	                {"id": "a", "file": "a.md", "due": "2026-08-15", "published": None},
    18	            ]
    19	        }
    20	        nxt = ch.next_due(data, now="2026-08-16")
    21	        self.assertEqual(nxt["id"], "a")
    22	
    23	    def test_skips_published(self):
    24	        data = {
    25	            "posts": [
    26	                {"id": "a", "file": "a.md", "due": "2026-08-15", "published": "2026-08-15T10:00:00Z"},
    27	                {"id": "b", "file": "b.md", "due": "2026-08-17", "published": None},
    28	            ]
    29	        }
    30	        nxt = ch.next_due(data, now="2026-08-16")
    31	        self.assertEqual(nxt["id"], "b")
    32	
    33	    def test_html_escape(self):
    34	        html = ch.to_html("hasło a < b i **grube** plus `kod`")
    35	        self.assertIn("&lt;", html)
    36	        self.assertIn("<b>grube</b>", html)
    37	        self.assertIn("<code>kod</code>", html)
    38	
    39	
    40	if __name__ == "__main__":
    41	 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:52Z

/root/obsidian-telegram-bot/.venv/bin/python: No module named pytest

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:34:55Z

...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
=== instagram ===
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
=== studio ===
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
=== vault ===
ok

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:23Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:23Z

=== TODO/FIXME/pass/NotImplemented in bot ===
./publish_channel.py:32:            print(f"brak id {args.post_id}", file=sys.stderr)
./.venv/lib/python3.12/site-packages/anyio/to_interpreter.py:149:            raise NotImplementedError
./.venv/lib/python3.12/site-packages/anyio/to_interpreter.py:152:            pass
./.venv/lib/python3.12/site-packages/anyio/to_process.py:88:                pass
./.venv/lib/python3.12/site-packages/anyio/lowlevel.py:221:                pass
./.venv/lib/python3.12/site-packages/anyio/streams/file.py:54:            pass
./.venv/lib/python3.12/site-packages/anyio/streams/tls.py:269:                raise NotImplementedError(
./.venv/lib/python3.12/site-packages/anyio/streams/tls.py:274:        raise NotImplementedError(
./.venv/lib/python3.12/site-packages/anyio/streams/tls.py:348:            # any asyncio implementation, so we explicitly pass the exception to log
./.venv/lib/python3.12/site-packages/anyio/from_thread.py:558:                pass
./.venv/lib/python3.12/site-packages/anyio/_backends/_trio.py:117:            # The user violated the type annotations. Still, we should pass this on to
./.venv/lib/python3.12/site-packages/anyio/_backends/_trio.py:1041:            pass
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:853:                    pass
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:1056:            pass
./.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:1200:        except NotImple
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:23Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:23Z

=== TODO/FIXME/pass/NotImplemented in pipeline ===
./bin/nightly_pipeline.sh:251:  echo "${URL_TOP:-'(brak — uruchom batch_analyze)'}"
./bin/nightly_pipeline.sh:257:  echo "${PERM_STATS:-'(brak)'}"
./bin/nightly_pipeline.sh:277:  head -30 "$OSINT_HTTPX" 2>/dev/null || echo '(brak — SKIP_OSINT=1 albo brak domen C2)'
./bin/nightly_pipeline.sh:283:  head -30 "$OSINT_NUCLEI" 2>/dev/null || echo '(brak — brak żywych hostów C2)'
./bin/osint_recon.sh:124:    echo "NUCLEI=0 (brak żywych hostów)"
./bin/batch_analyze.sh:179:    echo "        SKIP (brak jadx)"
./bin/batch_analyze.sh:245:  echo "Ostrzeżenie: brak jadx/apktool — APK będą niepełne. source ~/android-pipeline/config/path.sh" >&2
./tools/android-reverse-engineering-claude-skill/plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/decompile.sh:105:  XAPK_EXTRACTED_DIR=$(mktemp -d "${TMPDIR:-/tmp}/xapk-extract-XXXXXX")
./tools/android-reverse-engineering-claude-skill/plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/decompile.sh:165:  AAB_TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/aab-extract-XXXXXX")
./tools/android-reverse-engineering-claude-skill/plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/adb-crash-capture.sh:150:LOGCAT_TMP=$(mktemp /tmp/logcat-XXXXXX.log)
./tools/android-reverse-engineering-claude-skill/plugins/android-reverse-engineering/skills/android-reverse-engineering/scripts/install-dep.sh:229:  tmp_zip=$(mktemp /tmp/jadx-XXXXXX.zip)

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:27Z

./vault.py:119:            pass
./instagram.py:33:    pass
./instagram.py:431:        pass
./bot.py:312:            pass
./bot.py:657:            pass
./bot.py:1318:                pass
./bot.py:1590:        pass
./alert_roles.py:70:            pass
./render.py:299:    # dynaudnorm is ~10x faster than loudnorm two-pass

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:27Z

./lib/extract_domains.py:113:            pass
./lib/deep_re_pass.py:215:    "5. Packed samples (few first-party classes) need second-pass unpacking.",
./lib/analyze_static.py:185:        pass
./lib/analyze_static.py:224:        pass
./lib/analyze_static.py:274:        pass
./lib/analyze_static.py:457:        pass
./lib/analyze_static.py:463:        pass
./lib/alert_takeovers.py:107:            pass
./lib/analyze_pe.py:132:            pass
./lib/analyze_pe.py:258:        pass
./lib/sigma_generator.py:63:            pass
./lib/sigma_generator.py:352:            pass
./lib/enrich_cti.py:368:            pass
./lib/hunt_phishing_stealer.py:48:                pass
./lib/yara_generator.py:41:    "pass",

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:41Z

     1	#!/usr/bin/env python3
     2	"""IOC dashboard HTTP server.
     3	
     4	    python3 ~/android-pipeline/web/serve.py
     5	    python3 ~/android-pipeline/web/serve.py --port 8766 --bind 127.0.0.1
     6	
     7	GET /              → dashboard.html
     8	GET /api/iocs      → JSON z reports/iocs.json (albo świeżo z generatora)
     9	GET /iocs.json     → to samo
    10	"""
    11	
    12	from __future__ import annotations
    13	
    14	import argparse
    15	import json
    16	import sys
    17	from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    18	from pathlib import Path
    19	
    20	WEB_DIR = Path(__file__).resolve().parent
    21	PIPELINE_HOME = WEB_DIR.parent
    22	REPORTS_DIR = Path("/root/samples/reports")
    23	IOC_CANDIDATES = (
    24	    WEB_DIR / "iocs.json",
    25	    REPORTS_DIR / "iocs.json",
    26	)
    27	
    28	
    29	def load_iocs() -> bytes:
    30	    for path in IOC_CANDIDATES:
    31	        if path.is_file():
    32	            return path.read_bytes()
    33	    yara_py = PIPELINE_HOME / "lib" / "yara_generator.py"
    34	    if yara_py.is_file() and REPORTS_DIR.is_dir():
    35	        sys.path.insert(0, str(PIPELINE_HOME / "lib"))
    36	        from yara_generator import YARAGenerator, iter_report_json  # type: ignore
    37	
    38	        gen = YARAGenerator(REPORTS_DIR)
    39	        for json_file in iter_report_json(REPORTS_DIR):
    40	            gen.process_report(json_file)
    41	        payload = {

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:53Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:35:53Z

LISTEN 0      5            0.0.0.0:8080       0.0.0.0:*    users:(("python",pid=1012,fd=3))                        
--- search for api/boot and api/job servers ---
/root/obsidian-vault/Narzedzia/serve_dashboard.py
/root/obsidian-telegram-bot/bot.py

### 🛠️ Akcja/narzędzie — 2026-08-16T00:36:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:36:39Z

     1	#!/usr/bin/env bash
     2	# Install Android malware analysis pipeline on Ubuntu 24.04 (VPS-friendly).
     3	# Defensive research only. Does NOT install Docker by default (saves disk/RAM).
     4	set -euo pipefail
     5	
     6	export DEBIAN_FRONTEND=noninteractive
     7	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
     8	SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
     9	TOOLS_DIR="${PIPELINE_HOME}/tools"
    10	VENV_DIR="${PIPELINE_HOME}/.venv"
    11	INSTALL_GHIDRA="${INSTALL_GHIDRA:-0}"
    12	INSTALL_DOCKER="${INSTALL_DOCKER:-0}"
    13	
    14	log() { echo -e "[\e[32m+\e[0m] $*"; }
    15	warn() { echo -e "[\e[33m!\e[0m] $*"; }
    16	err() { echo -e "[\e[31m-\e[0m] $*" >&2; }
    17	
    18	mkdir -p "$PIPELINE_HOME"/{bin,lib,config,tools,docs} \
    19	  "$SAMPLES_ROOT"/{raw,decompiled,sources,reports,features,native,quarantine,logs} \
    20	  "$TOOLS_DIR"
    21	
    22	# Sync scripts if run from repo checkout
    23	SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    24	REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    25	if [[ -f "$REPO_ROOT/lib/analyze_static.py" ]]; then
    26	  cp -a "$REPO_ROOT/lib/"*.py "$PIPELINE_HOME/lib/" 2>/dev/null || true
    27	  cp -a "$REPO_ROOT/bin/"*.sh "$PIPELINE_HOME/bin/" 2>/dev/null || true
    28	  cp -a "$REPO_ROOT/config/"* "$PIPELINE_HOME/config/" 2>/dev/null || true
    29	  chmod +x "$PIPELINE_HOME/bin/"*.sh || true
    30	fi
    31	
    32	log "System packages..."
    33	apt-get update -qq

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:28Z

Edited /root/obsidian-telegram-bot/bot.py (10 lines -> 10 lines)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:32Z

Edited /root/obsidian-telegram-bot/bot.py (4 lines -> 7 lines)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:40Z

Edited /root/obsidian-telegram-bot/dashboard.py (10 lines -> 13 lines)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:37:44Z

AST OK

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:12Z

=== path.sh ===
     1	export PIPELINE_HOME="/root/android-pipeline"
     2	export SAMPLES_ROOT="/root/samples"
     3	export TOOLS_DIR="/root/android-pipeline/tools"
     4	export VENV_DIR="/root/android-pipeline/.venv"
     5	export PATH="$TOOLS_DIR/jadx/bin:$TOOLS_DIR/apktool:$TOOLS_DIR/capa:$PIPELINE_HOME/bin:$PATH"
     6	# shellcheck disable=SC1091
     7	source "$VENV_DIR/bin/activate"
     8	[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"
=== pipeline.env ===
     1	# Android malware analysis pipeline — configuration
     2	# Copy to ~/android-pipeline/config/pipeline.env and edit.
     3	
     4	export PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
     5	export SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
     6	
     7	export RAW_DIR="${SAMPLES_ROOT}/raw"
     8	export DECOMPILED_DIR="${SAMPLES_ROOT}/decompiled"
     9	export SOURCES_DIR="${SAMPLES_ROOT}/sources"
    10	export REPORTS_DIR="${SAMPLES_ROOT}/reports"
    11	export FEATURES_DIR="${SAMPLES_ROOT}/features"
    12	export NATIVE_DIR="${SAMPLES_ROOT}/native"
    13	export QUARANTINE_DIR="${SAMPLES_ROOT}/quarantine"
    14	export LOGS_DIR="${SAMPLES_ROOT}/logs"
    15	
    16	export TOOLS_DIR="${PIPELINE_HOME}/tools"
    17	export VENV_DIR="${PIPELINE_HOME}/.venv"
    18	export YARA_RULES_DIR="${TOOLS_DIR}/yara-rules"
    19	
    20	# Concurrency (VPS 6GB RAM / 2 vCPU → keep low)
    21	export MAX_PARALLEL="${MAX_PARALLEL:-1}"
    22	export JADX_THREADS
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:26Z

active
active

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:31Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:31Z

Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO apscheduler.scheduler: Added job "daily_summary" to job store "default"
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO apscheduler.scheduler: Scheduler started
Aug 15 22:36:45 vserver959630 python[69456]: 2026-08-15 22:36:45,202 INFO telegram.ext.Application: Application started
Aug 16 00:38:26 vserver959630 systemd[1]: Stopping obsidian-telegram-bot.service - XMask Obsidian Telegram bot...
Aug 16 00:38:26 vserver959630 python[69456]: 2026-08-16 00:38:26,073 INFO telegram.ext.Application: Application is stopping. This might take a moment.
Aug 16 00:38:26 vserver959630 python[69456]: 2026-08-16 00:38:26,073 INFO apscheduler.scheduler: Scheduler has been shut down
Aug 16 00:38:26 vserver959630 python[69456]: 2026-08-16 00:38:26,083 INFO telegram.ext.Application: Application.stop() complete
Aug 16 00:38:26 vserver959630 systemd[1]: obsidian-telegram-bot.service: Deactivated successfully.
Aug 16 00:38:26 vserver959630 systemd[1]: Stopped obsidian-telegram-bot.service - XMask Obsidian Telegram bot.
Aug 16 00:38:26 vserver959630 systemd[1]: obsidian-telegram-bot.service: Consumed 1.620s CPU time, 35.5M memory peak, 0B memory swap peak.
Aug 16 00:38:26 vserver959630 systemd[1]: Started obsidian-telegram-bot.service - XMask Obsidian Telegram bot.
Aug 16 00:38:26 vserver959630 python[77941]: /root/obsidian-telegram-bot/bot.py:2325: PTBUserWarning: If 'per_message=False', 'CallbackQuery
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:37Z

iocs type: list count: 9

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:41Z

(no output)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:50Z

     1	#!/bin/bash
     2	
     3	function get_folders {
     4	    local INDECES=()
     5	    AVOID="utils|deprecated"
     6	    for folder in $(ls -d */ | grep -vE $AVOID); do
     7	        INDECES+="$folder "
     8	    done
     9	    INDECES+=". "
    10	    echo "$INDECES"
    11	}
    12	
    13	function gen_index {
    14	    IDX_NAME=$1
    15	    BASE=$2
    16	    INC_MOBILE=$3
    17	    > $IDX_NAME
    18	    if [ x"$4" != x ]; then
    19	        echo -e "/*$4*/" > $IDX_NAME
    20	    fi
    21	    OS=$(uname)
    22	    AVOID="_?index.yara?|index_|utils|deprecated"
    23	    if [ x"$BASE" == x"." ]; then
    24	        if [ $INC_MOBILE == false ]; then
    25	            AVOID+="|Mobile"
    26	        fi
    27	        if [ $OS == "Darwin" ]; then
    28	            find -E $BASE -regex ".*\.yara?" | grep -vE "$AVOID" | sort | awk '{print "include \"" $0 "\""}' >> $IDX_NAME
    29	        else
    30	            # Linux version and potentialy Cygwin
    31	            find $BASE -regex ".*\.yara?" | grep -vE "$AVOID" | sort | awk '{print "include \"" $0 "\""}' >> $IDX_NAME
    32	        fi
    33	    else
    34	        if [ $OS == "Darwin" ]; then
    35	            find -E $BASE -regex ".*\.yara?" | grep -vE "$AVOID" | sort | awk '{print "include \"./" $0 "\""}' >> $IDX_NAME
    36	        else
    37	            # Linux version and potentialy Cygwin
    38	            find $BASE -regex ".*\.yara?" | grep -vE "$AVOID" | sort | awk '{print "include \"./
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-16T00:38:55Z

OK  tools/sigma-rules/lumma_digitden_dns.yml
OK  tools/sigma-rules/xmask_network_hosts.yml
OK  tools/sigma-rules/xmask_pe_hashes_file.yml
OK  tools/sigma-rules/xmask_pe_hashes_process.yml
OK  tools/sigma-rules/xmask_role_backdoor_hashes.yml
OK  tools/sigma-rules/xmask_win_account_api_cluster.yml
OK  tools/sigma-rules/xworm_tuffman_dns.yml
