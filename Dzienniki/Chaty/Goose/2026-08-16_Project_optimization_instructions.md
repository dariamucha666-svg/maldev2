---
title: "Project optimization instructions"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_18
cwd: "/root"
messages: 169
tool_calls: 166
status: archived
---

# Project optimization instructions

> Zapis czatu **Goose** · sesja '20260815_18' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | # OPTYMALIZATOR — ciągła poprawa niedokończonych projektów |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 1 |
| Akcji narzędziowych | 166 |
| Narzędzia | 'tool'×83, 'result'×83 |
| Pliki | '/root/.mb_api_key' · '/root/android-pipeline' · '/root/android-pipeline/bin/rat5_clean_run.sh' · '/root/android-pipeline/config/path.sh' · '/root/android-pipeline/config/path.sh.bak.rat5run' · '/root/android-pipeline/config/secrets.env' · '/root/android-pipeline/lib/alert_roles.py' · '/root/android-pipeline/lib/analyze_pe.py' · '/root/android-pipeline/lib/analyze_static.py' · '/root/android-pipeline/lib/deep_re_pass.py' · '/root/android-pipeline/lib/enrich_cti.py' · '/root/android-pipeline/lib/extract_domains.py' · '/root/android-pipeline/lib/yara_generator.py' · '/root/android-pipeline/tools/jadx/bin' · '/root/android-pipeline/tools/yara-rules/custom/auto_rules.yar' · '/root/android-pipeline/web/catalog.json' · '/root/obsidian-telegram-bot' · '/root/obsidian-telegram-bot/.env' · '/root/obsidian-telegram-bot/.owner_id' · '/root/obsidian-telegram-bot/alert_roles.py' |
| IP | '1.1.1.1' · '5.175.189.133' · '5.175.189.139' · '8.8.8.8' |
| Hosty | 'akamai.net' · 'akamaiedge.net' · 'amazonaws.com' · 'android.com' · 'apache.org' · 'appspot.com' · 'cloudflare.com' · 'cloudfront.net' · 'comodoca.com' · 'digicert.com' · 'discord.com' · 'discordapp.com' |
| Hashe | 'aaaaaaaaaaaa…' |

## Wniosek (ostatnia odpowiedź asystenta)

# Raport OPTYMALIZATORA

Przeanalizowałem oba projekty i wprowadziłem poprawki. Żadnego pliku `.env`, tokenów ani haseł nie dotykałem.

## Co poprawiłem

### Android pipeline (`/root/android-pipeline`)

1. **`lib/extract_domains.py` — naprawa gubienia domen**
   - Wcześniej `urls = urls or pat.get('urls') or []` nadpisywał URL z `patterns` gdy istniały URL top-level (raporty PE). Teraz karmimy oba źródła (top-level + `patterns.urls` + `patterns.websockets`).
   - Weryfikacja: test na syntetycznym raporcie zwraca `top.cyou`, `nested.cyou`, `ws.cyou`.

2. **`lib/enrich_cti.py` — naprawa gubienia URL/IP**
   - Analogiczna wada: `urls_field = urls_field or pat.get("urls")`. Teraz listy są łączone, więc CTI widzi zarówno top-level (PE), jak i `patterns` (APK).
   - Weryfikacja: test `collect_iocs()` zwrócił oba URL-e i oba IP.

3. **`lib/yara_generator.py` — pomijanie zagregowanych plików**
   - `iter_report_json()`/`process_report()` przetwarzały `iocs.json` jako raport i generowały „ducha” z hashem `unknown`. Dodałem do `SKIP_JSON_NAMES`: `iocs.json`, `cti_enrichment.json`, `sigma_index.json`.
   - Weryfikacja: `iter_report_json()` na katalogu z `iocs.json` + próbką zwraca już tylko próbkę.

4. **`lib/deep_re_pass.py` — złe wyciąganie SHA256**
   - `sha = sid.split("_", 1)[-1]` brało nazwę (np. `MyApp`) zamiast hasha dla katalogów z `batch_analyze.sh` (`<16hex>_<nazwa>`). Poprawione na `[0]`.
   - Dodałem fallback `reports_root.glob(f"{sha}*.md")`, bo dla katalogów batch mamy tylko prefiks hasha, a raport jest pełnym SHA256.

5. **`lib/analyze_static.py` — optymalizacja pamięci**
   - `zf.read(name)[:max_bytes]` czytał cały plik do RAM i dopiero ucinał. Teraz `zf.open(name).read(max_bytes)` czyta tylko do limitu (istotne przy dużych `classes.dex`).

6. **`lib/analyze_pe.py` — usunięcie martwego kodu**
   - Usunięto nieużywaną funkcję `run_cmd()` (potwierdzone grepem, że nigdzie nie jest wołana).

7. **`bin/rat5_clean_run.sh` — gwarancja przywrócenia `path.sh`**
   - Skrypt tymczasowo podmienia `SAMPLES_ROOT` w `config/path.sh`, ale nie miał pułapki `EXIT` (w przeciwieństwie do `rat5_android_clean.sh`). Przy niespodziewanym błędzie (`set -e`) `path.sh` mógł zostać zepsuty. Dodałem `trap restore_path EXIT` i bezpieczne `${LOG:-/tmp/rat5_restore.log}`.

### Bot Telegram (`/root/obsidian-telegram-bot`)

8. **`content.py` — naprawa uszkodzonej kolejki na dysku**
   - `load_queue()` przy uszkodzonym JSON lub złym kształcie zwracał domyślną kolejkę w pamięci, ale nie zapisywał naprawy. Po restarcie problem wracał. Teraz naprawiona kolejka jest od razu zapisywana.
   - Weryfikacja: test na uszkodzonym `channel_queue.json` — `load_queue()` zwrócił 9 wpisów i zapisał plik.

9. **Restart usługi** (bo `content.py` jest importowany przez bota):
   - `systemctl restart obsidian-telegram-bot` → `systemctl is-active` = **active**.

## Co zostawiłem świadomie

- **`bot.py: remember_owner()`** — pusta/no-op funkcja z komentarzem „First-writer-wins is disabled. Allowlist must be in .env”. To martwy kod, ale pełni rolę dokumentacji decyzji projektowej; nie jest nigdzie wołana i nie psuje działania. Nie kasowałem.
- **`bot.py`** — poza tym nie wymagał poprawek (logika była spójna; nie znalazłem TODO/niepodpiętych komend).
- **`nightly_pipeline.sh` fallback `URL_RANKED`** — zostawiłem starą ścieżkę fallback (`endpoints/all_urls_ranked.txt`); jest nieszkodliwa, a obecna ścieżka `reports/...` jest sprawdzana jako pierwsza i działa.
- **Zewnętrzne zestawy** (`tools/yara-rules`, `NusantaraScan`, `android-mcp`, `jadx`, `apktool`, `capa`) — nie ruszałem, to sygnatury/narzędzia, nie kod do refaktoru.
- **`.env`, `secrets.env`, tokeny, klucze API** — nietknięte.

## Jak zweryfikować

```bash
# Składnia bash (android-pipeline)
cd /root/android-pipeline
for f in bin/*.sh; do bash -n "$f" || echo "FAIL $f"; done

# Składnia Python (android-pipeline)
for f in lib/*.py web/*.py; do python3 -c "import ast; ast.parse(open('$f').read())" || echo "FAIL $f"; done

# Bo
…(obcięte)

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T16:31:21Z

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

### 👤 Użytkownik — 2026-08-15T16:31:21Z

<turn-context>
<current-time>2026-08-15 16:31:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:27Z

Updated (731 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:29Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:29Z

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


### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:29Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:29Z

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
    requirements.txt  [8]
    setup.py  [57]
  android-mcp/  [7K]
    src/  [0]
      android_mcp/  [0]
    tests/  [6K]
      test_adb.py  [669]
      test_apksigner.py  [432]
      test_composite_classify_behavior.py 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:35Z

   257 alert_roles.py
  2283 bot.py
   292 classify_roles.py
   323 content.py
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
    22 run.sh
    16 obsidian-telegram-bot.service
  5778 total

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:35Z

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
  5973 total

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:39Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:42Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:44Z

    raw = os.getenv("ALLOWED_USER_IDS", "").strip()
    if not raw:
        return set()
    ids: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return ids


def allowed_ids() -> set[int]:
    ids = _env_ids()
    if OWNER_FILE.exists():
        text = OWNER_FILE.read_text(encoding="utf-8").strip()
        if text.isdigit():
            ids.add(int(text))
    return ids


def remember_owner(user_id: int) -> None:
    # First-writer-wins is disabled. Allowlist must be in .env.
    return


def is_allowed(user_id: int | None) -> bool:
    if user_id is None:
        return False
    known = allowed_ids()
    if not known:
        return False
    return user_id in known


def require_allowlist() -> set[int]:
    ids = allowed_ids()
    if not ids:
        raise SystemExit(
            "Pusty ALLOWED_USER_IDS / .owner_id — bot nie startuje (fail-closed)."
        )
    return ids


def public_dash_url(hash_prefix: str | None = None) -> str:
    base = os.getenv("DASHBOARD_PUBLIC_URL", "http://5.175.189.133:8080/").strip()
    if not base.endswith("/"):
        base += "/"
    if hash_prefix:
        return f"{base}?h={hash_prefix}"
    return base


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🎮 GRAJ"), KeyboardButton("📋 PODSUMOWANIE")],
            [KeyboardButton(OBSIDIAN_BTN), KeyboardButton("🧒 Dla Laika")],
       
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:46Z

PAGE_SIZE = 10


def _ob_tabs_row() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton("📌", callback_data=f"ob:f:{_ob_id('XMask')}:0"),
        InlineKeyboardButton("🧠", callback_data=f"ob:f:{_ob_id('Analizy')}:0"),
        InlineKeyboardButton("📁", callback_data=f"ob:f:{_ob_id('Projekty')}:0"),
        InlineKeyboardButton("🔬", callback_data=f"ob:f:{_ob_id('Lab')}:0"),
        InlineKeyboardButton("🛠", callback_data=f"ob:f:{_ob_id('Narzedzia')}:0"),
        InlineKeyboardButton("📅", callback_data=f"ob:f:{_ob_id('Daily')}:0"),
        InlineKeyboardButton("🗂", callback_data="ob:all:0"),
    ]


def _ob_home_markup(vault: Vault) -> InlineKeyboardMarkup:
    subs, root_notes = vault.browse("")
    # pre-warm ids so callbacks survive
    for folder, _ in subs:
        _ob_id(folder)
    rows: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton("📋 PODSUMOWANIE", callback_data="ob:sum")],
        _ob_tabs_row(),
    ]
    row: list[InlineKeyboardButton] = []
    for folder, count in _ob_sort_folders(subs):
        label = f"{_ob_icon(folder)} {_ob_label(folder)} · {count}"
        if len(label) > 34:
            label = label[:31] + "…"
        row.append(InlineKeyboardButton(label, callback_data=f"ob:f:{_ob_id(folder)}:0"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    nav = [
        InlineKeyboardButton("🕒 Ostatnie", callback_data="ob:rec:0"),
        InlineKeyboardButton
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:48Z

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
        "*Lab / Narzędzia / Daily*",
        f"• Lab *{len(lab)}* · Narzędzia *{len(narz)}* · Daily *{len(daily)}*",
        "• zasada: oglądamy pliki, *nie odpalamy* ich w sieci",
        "",
        "*Detekcja i gra*",
        "• 🛡️ YARA / Suricata / Sigma / Zeek — walidowane na korpusie",
        "• 🚨 IDS na żywo (.139) + alerty Telegram",
        "• 🎮 /graj — misje obronne (3 poziomy, 8 ataków, 34 metody)",
        "",
        f"*Backlog:* zrobione *{done}* · otwarte *{open_}*",
    ]
    return "\n".join(parts)


def _ob_summary_markup(vault: Vault) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
   
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:50Z

            reply_markup=InlineKeyboardMarkup(graj.method_keyboard(attack_id)),
        )

    elif len(parts) >= 4 and parts[1] == "method":
        attack_id = parts[2]
        idx = int(parts[3])
        atk = graj.ATTACKS[attack_id]
        m = atk["methods"][idx]
        text = (
            f"🧩 *Metoda {idx + 1}: {esc(m['name'])}*\n\n"
            f"⚔️ *ATAK:*\n{esc(m['attack'])}\n\n"
            "Zobacz, jak się bronić:"
        )
        await msg.edit_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🛡️ Zobacz obronę", callback_data=f"graj:def:{attack_id}:{idx}")]]
            ),
        )

    elif len(parts) >= 4 and parts[1] == "def":
        attack_id = parts[2]
        idx = int(parts[3])
        atk = graj.ATTACKS[attack_id]
        m = atk["methods"][idx]
        text = (
            f"🧩 *Metoda {idx + 1}: {esc(m['name'])}*\n\n"
            f"🛡️ *OBRONA:*\n{esc(m['defense'])}\n\n"
            "Sprawdź się:"
        )
        await msg.edit_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("▶️ Rozpocznij quiz", callback_data=f"graj:go:{attack_id}:{idx}")]]
            ),
        )

    elif len(parts) >= 4 and parts[1] == "go":
        attack_id = parts[2]
        idx = int(parts[3])
        atk = graj.ATTACKS[attack_id]
        m = atk["methods"][idx]
        q = m["questions"][0]
        text = 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:52Z

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
        safe_rel = escape_markdown(note.rel, version=1)
        safe_snip = escape_markdown(snippet, version=1)
        lines.append(f"• `{safe_rel}`\n  _{safe_snip}_")
    safe_q = escape_markdown(query, version=1)
    await update.message.reply_markdown(
        f"Wyniki dla *{safe_q}*:\n\n" + "\n\n".join(lines),
        reply_markup=_note_keyboard([n for n, _ in hits], "get"),
    )


async def send_note(
    update: Update,
    rel: str,
    *,
    via_callback: bool = False,
    extra_markup: InlineKeyboardMarkup | None = None,
) -> None:
    vault = get_vault()
    note = vault.find(rel)
    if not note:
        text = f"Nie ma notatki: {rel}"
        if via_callback:
            await update.callback_query.message.reply_text(text)
        else:
            await update.message.reply_text(text)
        return
    body = vault.read(note)
    hea
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:54Z

        return None
    ioc = find_ioc(items, q)
    digest = (ioc or {}).get("hash") or ""
    return digest.lower() if HASH_RE.match(digest.lower()) else None


async def _follow_job(message, digest: str, action: str) -> None:
    terminal_add = {"added", "done", "error"}
    terminal_an = {"done", "error"}
    limit = 90 if action == "add" else 240
    last = ""
    for _ in range(limit):
        try:
            job = await asyncio.to_thread(_http_json, f"{JOB_API}?hash={digest}")
        except Exception as exc:  # noqa: BLE001
            await message.edit_text(f"API job: {exc}")
            return
        text = _job_text(digest, job)
        if text != last:
            try:
                await message.edit_markdown(text)
            except Exception:
                pass
            last = text
        state = job.get("state") or ""
        if action == "add" and state in terminal_add:
            return
        if action == "analyze" and state in terminal_an:
            return
        await asyncio.sleep(2)
    await message.reply_text("Timeout — sprawdź /status albo dashboard.")


async def _start_job(update: Update, query: str, action: str) -> None:
    target = update.effective_message
    if not query:
        await target.reply_text(
            "Użycie: /pobierz <sha256> albo /klasyfikuj <sha256>\nMoże być skrót z /wirus."
        )
        return
    digest = await _resolve_hash(query)
    if not digest:
        await target.reply_text("Podaj SHA256 (64 h
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:56Z

            [
                InlineKeyboardButton("HACKPLUG", callback_data="klip:hackplug"),
                InlineKeyboardButton("opsec.exe", callback_data="klip:opsec"),
            ],
            [InlineKeyboardButton("Anuluj", callback_data="klip:cancel")],
        ]
    )


def _klip_count_markup(kind: str) -> InlineKeyboardMarkup:
    row = [InlineKeyboardButton(str(i), callback_data=f"klip:{kind}:{i}") for i in range(6)]
    return InlineKeyboardMarkup([row, [InlineKeyboardButton("Anuluj", callback_data="klip:cancel")]])


def _klip_collect_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Montuj teraz", callback_data="klip:go")],
            [InlineKeyboardButton("Anuluj", callback_data="klip:cancel")],
        ]
    )


def _klip_status(job: dict) -> str:
    want_v = job.get("want_videos")
    want_a = job.get("want_audio")
    have_v = len(job.get("clips") or [])
    have_a = len(job.get("voices") or [])
    prompt = (job.get("prompt") or "").strip() or "—"
    return (
        f"*{job.get('series') or '?'}*\n"
        f"wideo: *{have_v}/{want_v}* · audio: *{have_a}/{want_a}*\n"
        f"prompt: {prompt[:180]}\n\n"
        "Bez znaku wodnego. Bez końcówki CapCut.\n"
        "Limit ~19 MB na plik."
    )


async def _klip_ask_videos(target, job: dict) -> None:
    await target.reply_text(
        "Ile wrzucasz video? (0–5)",
        reply_markup=_klip_count_markup("v"),
    )


async def _klip_ask_audi
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:31:59Z

        return True
    if status == "ask_prompt":
        job["prompt"] = text.strip()
        job["caption"] = text.strip()
        job["style"] = studio.parse_prompt(text)
        job["status"] = "collecting"
        studio.save_job(job)
        await update.message.reply_markdown(
            "Prompt zapisany.\n" + _klip_status(job) + "\n\nTeraz wrzucaj pliki.",
            reply_markup=_klip_collect_markup(),
        )
        return True
    return False


async def on_studio_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    msg = update.message
    if not msg:
        return
    user_id = update.effective_user.id
    job = studio.current(user_id)
    if not job or job.get("status") != "collecting":
        await msg.reply_text("Najpierw /klip: seria → ile wideo → ile audio → prompt.")
        return
    kind = "clip"
    file_id = None
    mime = None
    if msg.voice:
        kind, file_id, mime = "voice", msg.voice.file_id, "audio/ogg"
    elif msg.audio:
        kind, file_id, mime = "voice", msg.audio.file_id, msg.audio.mime_type
    elif msg.video:
        file_id, mime = msg.video.file_id, msg.video.mime_type or "video/mp4"
    elif msg.video_note:
        file_id, mime = msg.video_note.file_id, "video/mp4"
    elif msg.document:
        mime = msg.document.mime_type or ""
        file_id = msg.document.file_id
        if mime.startswith("audio"):
            kind = "voice"
        elif not (mime
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:01Z

        "🔔 *Alerty RAT / stealer*",
        f"w pamięci: RAT *{rats}* · stealer *{steal}*",
        "Nowe z pipeline / nightly przychodzą same.",
        "",
    ]
    for digest, meta in items[:8]:
        meta = meta or {}
        mark = "RAT" if meta.get("role") == "rat" else "STL"
        fam = meta.get("family") or "?"
        when = (meta.get("sent") or "")[:16].replace("T", " ")
        seed = " · seed" if meta.get("seed") else ""
        lines.append(f"• `{digest[:12]}` [{mark}] {fam}{seed}\n  _{when}_")
    await update.message.reply_markdown("\n".join(lines), reply_markup=open_dash_markup())


async def cmd_pobierz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    await _start_job(update, " ".join(context.args).strip() if context.args else "", "add")


async def cmd_klasyfikuj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    await _start_job(update, " ".join(context.args).strip() if context.args else "", "analyze")


async def cmd_virus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    query = " ".join(context.args).strip() if context.args else ""
    if not query:
        await cmd_dashboard(update, context)
        return
    if update.message:
        await update.message.chat.send_action("typing")
    try:
        items, _ = await _load_dashboard()
    except RuntimeError as exc
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:03Z

        folder=context.user_data.get("folder"),
    )
    context.user_data.clear()
    await update.message.reply_markdown(
        f"Zapisane.\n• {note.wiki}\n• `{note.rel}`"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    if update.message:
        await update.message.reply_text("Anulowane.")
    return ConversationHandler.END


async def append_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await guard(update):
        return ConversationHandler.END
    context.user_data.clear()
    seed = " ".join(context.args).strip() if context.args else ""
    vault = get_vault()
    if seed:
        note = vault.find(seed)
        if note:
            context.user_data["append_rel"] = note.rel
            await update.message.reply_text(f"Dopisuję do {note.rel}. Wyślij akapit.")
            return APPEND_BODY
        await update.message.reply_text(f"Nie znalazłem jednoznacznie: {seed}. Wybierz z listy.")
    notes = vault.iter_notes()[:10]
    if not notes:
        await update.message.reply_text("Brak notatek.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Do której notatki dopisać?",
        reply_markup=_note_keyboard(notes, "append"),
    )
    return APPEND_PICK


async def append_pick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await guard(update):
        return ConversationH
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:23Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:23Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:31Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:31Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:37Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:37Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:48Z

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
#!/usr/bin/env python3
"""Publish the next due XMask Warsztat post."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import loa
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:55Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:55Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:32:55Z

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
    r"(bank|sber|alfa|citi|visa|mastercard|paypal|revolut|"
    r"n26|wise\.com|
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:01Z


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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:03Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:06Z

  if command -v r2 >/dev/null 2>&1; then
    timeout 30 r2 -q -e bin.relocs.apply=true -c 'iI; iS; ii; iE' "$pe" > "$work/r2.txt" 2>/dev/null || true
  fi
  if [[ -n "${CAPA_BIN:-}" ]]; then
    log "  capa (timeout 45s)..."
    timeout 45 "$CAPA_BIN" "$pe" -q 2>/dev/null | head -200 > "$work/capa.txt" || true
  fi

  log "[3/4] Suspicious strings..."
  strings -n 8 "$pe" 2>/dev/null \
    | grep -Ei "http|https|api|bot|token|exodus|wallet|cmd|powershell|reg add|schtasks|webhook|telegram|discord" \
    > "$work/suspicious_strings.txt" || true

  log "[4/4] YARA (packers/malware/custom)..."
  run_yara "$pe" "$work/yara.txt"

  sync
  log "==== Done PE $name ===="
}

analyze_one() {
  local apk="$1"
  local name base h work
  name="$(basename "$apk")"
  h=$(sha256 "$apk")
  base="$h"
  work="$REPORTS_DIR/$base"
  mkdir -p "$work" "$SOURCES_DIR/$base" "$DECOMPILED_DIR/$base" "$NATIVE_DIR/$base"

  if [[ -f "$REPORTS_DIR/${base}.json" && "${FORCE:-0}" != "1" ]]; then
    log "SKIP (already analyzed): $name ($base)"
    return 0
  fi

  log "==== Analyzing $name ($base) ===="
  cp -f "$apk" "$work/sample.apk"

  if [[ -f "$ANALYZE_PY" ]]; then
    log "[1/6] Static features (androguard)..."
    "$PYTHON" "$ANALYZE_PY" "$apk" -o "$REPORTS_DIR" || fail "static analyze failed for $name"
  fi

  if [[ -n "${APKTOOL_BIN:-}" ]]; then
    log "[2/6] apktool decode..."
    if "$APKTOOL_BIN" d -f -o "$DECOMPILED_DIR/$base" "$apk" >"$work/apktool.log" 2>&1; then
      log "  apktool OK → $D
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:32Z

435:AGG_ONLY=0
442:    --aggregate-only) AGG_ONLY=1 ;;
448:      exit 0
462:if [[ "$AGG_ONLY" == "1" ]]; then
465:  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
467:    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
468:  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
470:    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
472:  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
474:    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
477:  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
479:    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
481:  exit 0
482:fi
498:fi
514:fi
528:fi
533:  exit 0
534:fi
552:fi
554:if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
556:  "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
557:  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
559:    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
561:fi
562:if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
564:  "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
565:fi
576:fi

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:35Z

     1	log "analyze_pe.py: $ANALYZE_PE_PY"
     2	
     3	if [[ "$AGG_ONLY" == "1" ]]; then
     4	  aggregate
     5	  generate_auto_yara
     6	  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
     7	    log "Tagging report roles (rat/stealer/backdoor/…)"
     8	    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
     9	  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
    10	    log "Hunt phishing/stealer IOCs"
    11	    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
    12	  fi
    13	  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
    14	    log "Alert RAT/stealer -> Telegram"
    15	    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
    16	  fi
    17	  fi
    18	  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
    19	    log "CTI enrichment (MalwareBazaar/URLhaus/VT/…)"
    20	    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
    21	  fi
    22	  exit 0
    23	fi
    24	
    25	if [[ ${#TARGETS[@]} -eq 0 ]]; then
    26	  preprocess_raw

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:45Z

-rwxr-xr-x 1 root   root   8404 Aug 15 03:25 /root/obsidian-telegram-bot/alert_roles.py
-rwxr-xr-x 1 root   root   8404 Aug 15 03:25 /root/obsidian-vault/Narzedzia/alert_roles.py
-rwxr-xr-x 1 ubuntu ubuntu 4052 Aug 15 09:11 /root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh
---
ls: cannot access '/root/android-pipeline/lib/alert_roles.py': No such file or directory

Command exited with code 2

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:45Z

pipeline.sh OK

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:50Z

    42	
    43	if [ "$#" -ge 1 ]; then
    44	    # domeny podane wprost (np. znane C2)
    45	    DOMAINS=("$@")
    46	else
    47	    # 1) Zbierz domeny z raportów (wspólny ekstraktor z filtrem infrastruktury)
    48	    "$PY" "$PIPELINE_HOME/lib/extract_domains.py" "$REPORTS_DIR" > "$DOMAINS_FILE"
    49	    mapfile -t DOMAINS < "$DOMAINS_FILE"
    50	    if [ "${#DOMAINS[@]}" -eq 0 ]; then
    51	        log "Brak domen do enumeracji (wszystkie odfiltrowane?). Wyjdę."
    52	        exit 0
    53	    fi
    54	    if [ "${#DOMAINS[@]}" -gt "$RECON_LIMIT" ]; then
    55	        DOMAINS=("${DOMAINS[@]:0:$RECON_LIMIT}")
    56	    fi
    57	fi
    58	
    59	log "Enumeracja ${#DOMAINS[@]} domen na $RECON_HOST (moduł $RECON_MODULE)"
    60	
    61	# 2) Zbuduj resource file dla Recon-ng
    62	{
    63	    echo "workspaces create $WS"
    64	    for d in "${DOMAINS[@]}"; do
    65	        echo "db insert domains ${d}~"
    66	    done
    67	    echo "marketplace install $RECON_MODULE"
    68	    echo "marketplace install reporting/json"
    69	    for d in "${DOMAINS[@]}"; do
    70	        echo "modules load $RECON_MODULE"
    71	        echo "options set SOURCE $d"
    72	        echo "run"
    73	    done
    74	    echo "modules load reporting/json"
    75	    echo "options set FILENAME /root/osint_${WS}.json"
    76	    echo "run"
    77	    echo "exit"
    78	} > "$RC"
    79	
    80	# 3) Wyślij rc + uruchom Recon-ng na zdalnym hoście
    81	scp -q "$RC" "$RECON_HOST:/
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:54Z

     1	#!/usr/bin/env bash
     2	# Lightweight batch static analysis (defensive lab).
     3	# APK: jadx/apktool/aapt. PE: pefile/strings/entropy/YARA/readpe.
     4	#
     5	# Usage:
     6	#   batch_analyze.sh <folder_z_probek> <folder_wynikowy>
     7	#   batch_analyze.sh ~/samples/raw ~/samples/output
     8	#   batch_analyze.sh ~/samples/quarantine ~/samples/output
     9	set -euo pipefail
    10	
    11	INPUT_DIR="${1:-}"
    12	OUTPUT_BASE="${2:-}"
    13	
    14	if [[ -z "$INPUT_DIR" || -z "$OUTPUT_BASE" ]]; then
    15	  echo "Użycie: $0 <folder_z_probek> <folder_wynikowy>"
    16	  exit 1
    17	fi
    18	
    19	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    20	if [[ -f "$PIPELINE_HOME/config/path.sh" ]]; then
    21	  # shellcheck disable=SC1091
    22	  source "$PIPELINE_HOME/config/path.sh" 2>/dev/null || true
    23	fi
    24	export PATH="${PIPELINE_HOME}/tools/jadx/bin:${PIPELINE_HOME}/tools/apktool:${PATH}"
    25	
    26	JADX_BIN="$(command -v jadx || true)"
    27	APKTOOL_BIN="$(command -v apktool || true)"
    28	AAPT_BIN="$(command -v aapt2 || true)"
    29	[[ -z "$AAPT_BIN" ]] && AAPT_BIN="$(command -v aapt || true)"
    30	PYTHON="${PIPELINE_HOME}/.venv/bin/python"
    31	[[ -x "$PYTHON" ]] || PYTHON="$(command -v python3)"
    32	ANALYZE_PE_PY="${ANALYZE_PE_PY:-$PIPELINE_HOME/lib/analyze_pe.py}"
    33	YARA_RULES="${YARA_RULES_DIR:-$PIPELINE_HOME/tools/yara-rules}"
    34	
    35	mkdir -p "$OUTPUT_BASE"/{decompiled,sources,reports,featur
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:33:57Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:00Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:03Z

     1	#!/usr/bin/env bash
     2	# Nocny pipeline: (opcjonalnie) MalwareBazaar → batch → pełna analiza → classify → daily summary
     3	# Usage:
     4	#   export MB_API_KEY='...'   # or put key in ~/android-pipeline/config/secrets.env
     5	#   ~/nightly_pipeline.sh
     6	#   ~/nightly_pipeline.sh --skip-download
     7	#   ~/nightly_pipeline.sh --skip-full
     8	#   ~/nightly_pipeline.sh --download-only
     9	set -euo pipefail
    10	
    11	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    12	SAMPLES_ROOT="${SAMPLES_ROOT:-$HOME/samples}"
    13	LOG_DIR="${SAMPLES_ROOT}/logs"
    14	RAW_DIR="${SAMPLES_ROOT}/raw"
    15	OUTPUT_DIR="${SAMPLES_ROOT}/output"
    16	REPORTS_DIR="${SAMPLES_ROOT}/reports"
    17	PE_DIR="${SAMPLES_ROOT}/pe"
    18	QUARANTINE_DIR="${SAMPLES_ROOT}/quarantine"
    19	CLASSIFY_PY="${PIPELINE_HOME}/lib/classify_roles.py"
    20	EXPORT_SH="${OBSIDIAN_EXPORT:-/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh}"
    21	
    22	SKIP_DOWNLOAD=0
    23	SKIP_BATCH=0
    24	SKIP_FULL=0
    25	DOWNLOAD_ONLY=0
    26	
    27	for arg in "$@"; do
    28	  case "$arg" in
    29	    --skip-download) SKIP_DOWNLOAD=1 ;;
    30	    --skip-batch) SKIP_BATCH=1 ;;
    31	    --skip-full) SKIP_FULL=1 ;;
    32	    --download-only) DOWNLOAD_ONLY=1; SKIP_BATCH=1; SKIP_FULL=1 ;;
    33	    -h|--help)
    34	      sed -n '1,16p' "$0"
    35	      exit 0
    36	      ;;
    37	  esac
    38	done
    39	
    40	mkdir -p "$LOG_DIR" "$RAW_DIR" "$OUTPUT_D
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:11Z

     1	#!/usr/bin/env bash
     2	# osint_recon.sh — pasywny OSINT sweep domen C2 na zdalnym hoście .139.
     3	#
     4	# Używa nowego zestawu narzędzi (subfinder + amass + theHarvester + httpx),
     5	# uzupełniającego recon_osint.sh (Recon-ng). Wyciąga domeny z raportów albo
     6	# przyjmuje je jako argumenty, robi pasywną enumerację subdomen i probe HTTP.
     7	#
     8	# Użycie:
     9	#   bash bin/osint_recon.sh                 # domeny z raportów
    10	#   bash bin/osint_recon.sh suahoje.com off-game.com
    11	#   OSINT_LIMIT=5 bash bin/osint_recon.sh
    12	set -euo pipefail
    13	
    14	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    15	REPORTS_DIR="${REPORTS_DIR:-$HOME/samples/reports}"
    16	RECON_HOST="${RECON_HOST:-root@5.175.189.139}"
    17	OSINT_LIMIT="${OSINT_LIMIT:-10}"
    18	AMASS_TIMEOUT="${AMASS_TIMEOUT:-60}"   # sekundy na pasywny amass (jest wolny)
    19	SKIP_AMASS="${SKIP_AMASS:-0}"          # 1 = tylko subfinder (szybciej)
    20	SKIP_NUCLEI="${SKIP_NUCLEI:-0}"        # 1 = pomiń nuclei (http/ssl)
    21	SUB_PARALLEL="${SUB_PARALLEL:-4}"      # równoległych subfinder
    22	CACHE_TTL_DAYS="${CACHE_TTL_DAYS:-7}"  # ważność cache subdomen (dni)
    23	
    24	OUT_DIR="${OUT_DIR:-$REPORTS_DIR/osint}"
    25	mkdir -p "$OUT_DIR"
    26	STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
    27	
    28	log() { echo "[osint_recon] $*"; }
    29	
    30	# fail-fast: bez połączenia z .139 pomiń cały krok (niekrytyczne)
    31	if ! ssh -o ConnectTimeout
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:16Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:16Z

     1	#!/usr/bin/env bash
     2	# recon_osint.sh — OSINT pivot z domen C2 wyciągniętych z raportów pipeline.
     3	#
     4	# Wyciąga "ciekawe" domeny (bez infrastruktury) przez lib/extract_domains.py,
     5	# wrzuca je do Recon-ng na zdalnym hoście i uruchamia moduł enumeracji hostów.
     6	# Wynik (JSON/log) ściąga z powrotem do reports/osint/.
     7	#
     8	# Można też podać domeny wprost (np. znane C2):
     9	#   bash bin/recon_osint.sh suahoje.com off-game.com
    10	#
    11	# Zależności:
    12	#   - Recon-ng na $RECON_HOST (patrz Narzedzia/Recon_ng_Analiza.md)
    13	#   - SSH z kluczem .133 -> $RECON_HOST
    14	#
    15	# Zmienne:
    16	#   RECON_HOST     host docelowy (default: root@5.175.189.139)
    17	#   RECON_MODULE   moduł recon (default: recon/domains-hosts/hackertarget)
    18	#   RECON_LIMIT    max domen do enumeracji (default: 20)
    19	set -euo pipefail
    20	
    21	PIPELINE_HOME="${PIPELINE_HOME:-$HOME/android-pipeline}"
    22	REPORTS_DIR="${REPORTS_DIR:-$HOME/samples/reports}"
    23	RECON_HOST="${RECON_HOST:-root@5.175.189.139}"
    24	RECON_MODULE="${RECON_MODULE:-recon/domains-hosts/hackertarget}"
    25	RECON_LIMIT="${RECON_LIMIT:-20}"
    26	PY="${PY:-python3}"
    27	
    28	OUT_DIR="${OUT_DIR:-$REPORTS_DIR/osint}"
    29	mkdir -p "$OUT_DIR"
    30	STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
    31	WS="osint_${STAMP}"
    32	RC="$OUT_DIR/recon_${STAMP}.rc"
    33	DOMAINS_FILE="$OUT_DIR/domains_${STAMP}.txt"
    34	
    35	log() { echo "[recon
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:19Z

     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3	
     4	STAMP=$(date -u +%Y%m%dT%H%M%SZ)
     5	ROOT="/root/samples/rat5_${STAMP}"
     6	export ROOT
     7	PATH_SH="/root/android-pipeline/config/path.sh"
     8	PATH_BAK="/root/android-pipeline/config/path.sh.bak.rat5run"
     9	API="https://mb-api.abuse.ch/api/v1/"
    10	
    11	mkdir -p "$ROOT"/{raw,quarantine,decompiled,sources,reports,features,native,logs,output,meta}
    12	ln -sfn "$ROOT" /root/samples/rat5_latest
    13	LOG="$ROOT/logs/rat5_clean_${STAMP}.log"
    14	echo $$ > /root/samples/rat5_latest.pid
    15	
    16	# shellcheck disable=SC1091
    17	source /root/android-pipeline/config/secrets.env 2>/dev/null || true
    18	if [[ -z "${MB_API_KEY:-}" && -f /root/.mb_api_key ]]; then
    19	  MB_API_KEY=$(tr -d " \t\r\n" < /root/.mb_api_key)
    20	fi
    21	export MB_API_KEY
    22	[[ -n "${MB_API_KEY:-}" ]] || { echo "NO MB_API_KEY"; exit 1; }
    23	
    24	cp -a "$PATH_SH" "$PATH_BAK"
    25	sed -i "s|export SAMPLES_ROOT=\"/root/samples\"|export SAMPLES_ROOT=\"$ROOT\"|" "$PATH_SH"
    26	restore_path() {
    27	  if [[ -f "$PATH_BAK" ]]; then
    28	    mv -f "$PATH_BAK" "$PATH_SH"
    29	    echo "[restore] path.sh" >>"$LOG" || true
    30	  fi
    31	}
    32	trap restore_path EXIT
    33	
    34	export PATH="/root/android-pipeline/tools/jadx/bin:/root/android-pipeline/tools/apktool:/root/android-pipeline/bin:${PATH}"
    35	export FORCE=1 SKIP_GHIDRA=1
    36	
    37	download_one() {
    38	  lo
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:36Z

     1	#!/usr/bin/env python3
     2	"""Aggregate per-sample JSON reports into CSV features + common pattern summary."""
     3	from __future__ import annotations
     4	
     5	import argparse
     6	import csv
     7	import json
     8	from collections import Counter
     9	from pathlib import Path
    10	from typing import Any
    11	
    12	
    13	def load_reports(reports_dir: Path) -> list[dict[str, Any]]:
    14	    out = []
    15	    for p in sorted(reports_dir.glob("*.json")):
    16	        if p.name.endswith(".features.json"):
    17	            continue
    18	        try:
    19	            data = json.loads(p.read_text(encoding="utf-8"))
    20	            if data.get("schema", "").startswith("android-malware-pipeline"):
    21	                out.append(data)
    22	        except Exception:
    23	            continue
    24	    return out
    25	
    26	
    27	def main() -> int:
    28	    ap = argparse.ArgumentParser()
    29	    ap.add_argument("--reports", type=Path, required=True)
    30	    ap.add_argument("--features-out", type=Path, required=True)
    31	    ap.add_argument("--patterns-out", type=Path, required=True)
    32	    args = ap.parse_args()
    33	
    34	    reports = load_reports(args.reports)
    35	    args.features_out.parent.mkdir(parents=True, exist_ok=True)
    36	    args.patterns_out.parent.mkdir(parents=True, exist_ok=True)
    37	
    38	    rows = [r["feature_row"] for r in reports if "feature_row" in r]
    39	    fieldnames =
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:36Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:42Z

     1	#!/usr/bin/env python3
     2	"""Static feature extraction for Android APK (defensive malware research).
     3	
     4	Outputs JSON report + feature row for CSV aggregation.
     5	Uses androguard when available; falls back to zip/manifest/string heuristics.
     6	"""
     7	from __future__ import annotations
     8	
     9	import argparse
    10	import hashlib
    11	import json
    12	import os
    13	import re
    14	import sys
    15	import zipfile
    16	from collections import Counter
    17	from datetime import datetime, timezone
    18	from pathlib import Path
    19	from typing import Any
    20	
    21	URL_RE = re.compile(r"https?://[^\s\"'<>\\]{4,200}", re.I)
    22	WS_RE = re.compile(r"wss?://[^\s\"'<>\\]{4,200}", re.I)
    23	IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    24	EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    25	BASE64_HINT = re.compile(r"(?:[A-Za-z0-9+/]{40,}={0,2})")
    26	
    27	# High-signal Android / malware-related API substrings
    28	SUSPICIOUS_APIS = [
    29	    "Runtime.exec",
    30	    "ProcessBuilder",
    31	    "DexClassLoader",
    32	    "PathClassLoader",
    33	    "InMemoryDexClassLoader",
    34	    "System.loadLibrary",
    35	    "Runtime.getRuntime",
    36	    "TelephonyManager",
    37	    "getDeviceId",
    38	    "getSubscriberId",
    39	    "SmsManager",
    40	    "sendTextMessage",
    41	    "AccessibilityService",
    42	    "MediaProjection",
    43	    "Camera",
   
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:34:54Z

     1	#!/usr/bin/env python3
     2	"""
     3	extract_domains.py — wyciąga "ciekawe" domeny (C2 / nie-infrastruktura)
     4	z raportów pipeline + katalogu rodzin do stdout (jedna na linię).
     5	
     6	Źródła:
     7	  * raporty JSON (urls, patterns.urls, patterns.websockets)
     8	  * reports/iocs.json (zagregowane URL-e)
     9	  * web/catalog.json (kuratorowane C2 z analiz, np. suahoje.com / off-game.com)
    10	
    11	Użycie:
    12	  python3 extract_domains.py /root/samples/reports
    13	"""
    14	import json
    15	import os
    16	import re
    17	import sys
    18	from urllib.parse import urlparse
    19	
    20	BLOCK = {
    21	    'localhost', 'example.com',
    22	    'android.com', 'google.com', 'googleapis.com', 'gstatic.com', 'gvt1.com',
    23	    'play.google.com', 'goo.gl', 'youtube.com', 'google-analytics.com',
    24	    'microsoft.com', 'mozilla.org', 'windows.com', 'windows.net',
    25	    'digicert.com', 'globalsign.com', 'sectigo.com', 'usertrust.com',
    26	    'ssl.com', 'identrust.com', 'letsencrypt.org', 'comodoca.com',
    27	    'apache.org', 'w3.org', 'xml.org', 'xmlsoap.org',
    28	    'github.com', 'githubusercontent.com', 'gitlab.com',
    29	    'jetbrains.com', 'kotlinlang.org', 'gradle.org',
    30	    'appspot.com', 'firebaseapp.com', 'firebaseio.com', 'googleapis.cn',
    31	    'amazonaws.com', 'cloudfront.net', 'akamai.net', 'akamaiedge.net',
    32	    'cloudflare.com', 'fastly.net', 'jsdelivr.net', 'unpkg.com',
    33	   
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:05Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:05Z

     1	#!/usr/bin/env python3
     2	"""
     3	alert_takeovers.py — alert Telegram + nota w vaultcie, gdy nuclei wykryje
     4	przejęte subdomeny C2 (takeover) w wynikach OSINT sweepu.
     5	
     6	Czyta najnowszy nuclei_*.txt z <reports>/osint/, szuka linii z "takeover",
     7	deduplikuje po celu (state) i wysyła alert. Stdlib only.
     8	
     9	Użycie:
    10	  python3 alert_takeovers.py [OSINT_DIR] [--test]
    11	"""
    12	from __future__ import annotations
    13	
    14	import json
    15	import os
    16	import re
    17	import sys
    18	import urllib.error
    19	import urllib.parse
    20	import urllib.request
    21	from datetime import datetime, timezone
    22	from pathlib import Path
    23	
    24	OSINT_DIR = Path(os.environ.get("OSINT_DIR", "/root/samples/reports/osint"))
    25	STATE = Path(os.environ.get("TAKEOVER_STATE", "/root/samples/reports/osint/takeover_state.json"))
    26	ENV_FILE = Path(os.environ.get("BOT_ENV", "/root/obsidian-telegram-bot/.env"))
    27	OWNER_FILE = Path("/root/obsidian-telegram-bot/.owner_id")
    28	VAULT_NOTE = Path(os.environ.get("TAKEOVER_NOTE", "/root/obsidian-vault/Analizy/Alerty"))
    29	
    30	RE_TAKEOVER = re.compile(r"takeover", re.I)
    31	
    32	
    33	def utc_now() -> str:
    34	    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    35	
    36	
    37	def load_env(path: Path) -> dict[str, str]:
    38	    out: dict[str, str] = {}
    39	    if not path.is_file():
    40	        return 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:22Z

./bin/nightly_pipeline.sh:if [[ -f "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" ]]; then
./bin/nightly_pipeline.sh:  "$PYTHON" "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" >>"$LOG_FILE" 2>&1 || log "hunt failed (non-fatal)"
./bin/nightly_pipeline.sh:  if [[ -f "${PIPELINE_HOME}/lib/alert_takeovers.py" ]]; then
./bin/nightly_pipeline.sh:    log "alert_takeovers.py (nuclei takeover check)..."
./bin/nightly_pipeline.sh:    "$PYTHON" "${PIPELINE_HOME}/lib/alert_takeovers.py" "$REPORTS_DIR/osint" >>"$LOG_FILE" 2>&1
./bin/nightly_pipeline.sh:    log "alert_takeovers exit=$rc"
./bin/recon_osint.sh:# Wyciąga "ciekawe" domeny (bez infrastruktury) przez lib/extract_domains.py,
./bin/recon_osint.sh:    "$PY" "$PIPELINE_HOME/lib/extract_domains.py" "$REPORTS_DIR" > "$DOMAINS_FILE"
./bin/install.sh:if [[ -f "$REPO_ROOT/lib/analyze_static.py" ]]; then
./bin/osint_recon.sh:    mapfile -t DOMAINS < <(python3 "$PIPELINE_HOME/lib/extract_domains.py" "$REPORTS_DIR")
./bin/batch_analyze.sh:ANALYZE_PE_PY="${ANALYZE_PE_PY:-$PIPELINE_HOME/lib/analyze_pe.py}"
./bin/batch_analyze.sh:analyze_pe() {
./bin/batch_analyze.sh:  analyze_pe "$pe"
./bin/pipeline.sh:ANALYZE_PY="$PIPELINE_HOME/lib/analyze_static.py"
./bin/pipeline.sh:ANALYZE_PE_PY="$PIPELINE_HOME/lib/analyze_pe.py"
./bin/pipeline.sh:AGG_PY="$PIPELINE_HOME/lib/aggregate_patterns.py"
./bin/pipeline.sh:    fail "analyze_pe.py missing"
./bin/pipeline.sh:  local yara_py="${PIPELINE_HOME}/lib/yara_generator.py"
./bin/pipeline.sh:    log "yara_gener
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:26Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:26Z

     1	#!/usr/bin/env python3
     2	"""
     3	YARA Generator – automatyczne tworzenie reguł YARA na podstawie analizy PE/APK.
     4	
     5	Czyta raporty pipeline'u:
     6	  /root/samples/reports/<SHA256>.json
     7	  /root/samples/reports/<SHA256>/{<SHA256>.json, suspicious_strings.txt}
     8	
     9	Użycie:
    10	  yara_generator.py <katalog_z_raportami>
    11	  yara_generator.py /root/samples/reports /root/android-pipeline/tools/yara-rules/custom/auto_rules.yar
    12	"""
    13	
    14	from __future__ import annotations
    15	
    16	import json
    17	import re
    18	import sys
    19	from datetime import date
    20	from pathlib import Path
    21	
    22	
    23	STRING_FILES = (
    24	    "strings.txt",
    25	    "suspicious_strings.txt",
    26	    "endpoints_grep.txt",
    27	)
    28	
    29	SKIP_JSON_NAMES = {
    30	    "patterns_summary.json",
    31	    "re_static_iocs.json",
    32	    "features.json",
    33	    "summary.json",
    34	}
    35	
    36	GENERIC_ALONE = {
    37	    "seed",
    38	    "pass",
    39	    "login",
    40	    "token",
    41	    "api",
    42	    "bot",
    43	    "wallet",
    44	    "password",
    45	}
    46	
    47	# Szum, który nie nadaje się na IoC (schematy Android, stdlib Go, Lorem).
    48	NOISE_RE = re.compile(
    49	    r"("
    50	    r"schemas\.android\.com|"
    51	    r"www\.w3\.org|"
    52	    r"xmlns|"
    53	    r"mozilla\.org/MPL|"
    54	    r"publicsuffix\.org|"
    55	    r"youtrack\.jetbrains|"

…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:42Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:35:48Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:36:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:36:35Z

obsidian-telegram-bot/graj.py:155:                    {"q": "Gdzie działa clipper jako rozszerzenie?", "options": ["W systemie", "W przeglądarce (monitoruje schowek)", "W BIOS"], "answer": 1, "explain": "Rozszerzenie działa w przeglądarce i monitoruje schowek."},
obsidian-telegram-bot/graj.py:200:                    {"q": "Dwie próbki → ten sam IP. Co to znaczy?", "options": ["Przypadek", "Ta sama kampania (wspólny C2)", "Błąd"], "answer": 1, "explain": "Wiele domen na jeden IP = ta sama kampania."},
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/to_interpreter.py:149:            raise NotImplementedError
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/to_interpreter.py:152:            pass
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/to_process.py:88:                pass
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/lowlevel.py:221:                pass
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/streams/file.py:54:            pass
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/streams/tls.py:269:                raise NotImplementedError(
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/streams/tls.py:274:        raise NotImplementedError(
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/from_thread.py:558:                pass
obsidian-telegram-bot/.venv/lib/python3.12/site-packages/anyio/_backends/_trio.py:1041:            pass
obsidian-telegram-bo
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:36:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:36:40Z

obsidian-telegram-bot/graj.py:155:                    {"q": "Gdzie działa clipper jako rozszerzenie?", "options": ["W systemie", "W przeglądarce (monitoruje schowek)", "W BIOS"], "answer": 1, "explain": "Rozszerzenie działa w przeglądarce i monitoruje schowek."},
obsidian-telegram-bot/bot.py:142:    "HACKPLUG": "⚡",
obsidian-telegram-bot/bot.py:1361:                InlineKeyboardButton("HACKPLUG", callback_data="klip:hackplug"),
obsidian-telegram-bot/bot.py:1499:    if action in {"hackplug", "opsec", "intro"}:
obsidian-telegram-bot/content.py:49:                "id": "hackplug-00",
obsidian-telegram-bot/content.py:50:                "file": "XMask/HACKPLUG/00_Co_to_jest.md",
obsidian-telegram-bot/content.py:61:                "id": "hackplug-01",
obsidian-telegram-bot/content.py:62:                "file": "XMask/HACKPLUG/01_Nie_zaczynaj_od_wirusa.md",
obsidian-telegram-bot/content.py:73:                "id": "hackplug-02",
obsidian-telegram-bot/content.py:74:                "file": "XMask/HACKPLUG/02_Terminal.md",
obsidian-telegram-bot/content.py:85:                "id": "hackplug-03",
obsidian-telegram-bot/content.py:86:                "file": "XMask/HACKPLUG/03_Lab_to_nie_cudzy_telefon.md",
obsidian-telegram-bot/content.py:157:        series = "HP" if str(item.get("id", "")).startswith("hackplug") else (
obsidian-telegram-bot/studio.py:22:    "hackplug": "hackplug",
obsidian-telegram-bot/studio.py:23:    "hp": "hackplug",
obsidian-telegram-bot/studio.py:24:    "hacker": "ha
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:36Z

AST check done

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:40Z

bash -n done

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:37:45Z

android-pipeline/lib/analyze_pe.py:def run_cmd(args: list[str], timeout: int = 30) -> str:
---remember_owner---
obsidian-telegram-bot/bot.py:def remember_owner(user_id: int) -> None:

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:01Z

     1	fi
     2	generate_auto_yara
     3	if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
     4	  log "Tagging report roles (rat/stealer/backdoor/…)"
     5	  "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
     6	fi
     7	if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
     8	  log "Hunt phishing/stealer IOCs"
     9	  "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
    10	fi
    11	if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
    12	  log "Alert RAT/stealer -> Telegram"
    13	  "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
    14	fi
    15	if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:09Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:09Z

552:fi
553:generate_auto_yara
554:if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
555:  log "Tagging report roles (rat/stealer/backdoor/…)"
556:  "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
557:fi
558:if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
559:  log "Hunt phishing/stealer IOCs"
560:  "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
561:fi
562:if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
563:  log "Alert RAT/stealer -> Telegram"
564:  "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
565:fi
566:if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:38:18Z

462:if [[ "$AGG_ONLY" == "1" ]]; then
463:  aggregate
464:  generate_auto_yara
465:  if [[ -f "${PIPELINE_HOME}/lib/classify_roles.py" ]]; then
466:    log "Tagging report roles (rat/stealer/backdoor/…)"
467:    "$PYTHON" "${PIPELINE_HOME}/lib/classify_roles.py" "$REPORTS_DIR" || log "classify_roles failed (non-fatal)"
468:  fi
469:  if [[ -f "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" ]]; then
470:    log "Hunt phishing/stealer IOCs"
471:    "$PYTHON" "${PIPELINE_HOME}/lib/hunt_phishing_stealer.py" || log "hunt phishing/stealer failed (non-fatal)"
472:  fi
473:  if [[ -f /root/obsidian-vault/Narzedzia/alert_roles.py ]]; then
474:    log "Alert RAT/stealer -> Telegram"
475:    "$PYTHON" /root/obsidian-vault/Narzedzia/alert_roles.py || log "role alerts failed (non-fatal)"
476:  fi
477:  if [[ -f "${PIPELINE_HOME}/lib/enrich_cti.py" && "${SKIP_CTI:-0}" != "1" ]]; then
478:    log "CTI enrichment (MalwareBazaar/URLhaus/VT/…)"
479:    "$PYTHON" "${PIPELINE_HOME}/lib/enrich_cti.py" "$REPORTS_DIR" || log "enrich_cti failed (non-fatal)"
480:  fi
481:  exit 0
482:fi
483:

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:04Z

173:def run_cmd(args: list[str], timeout: int = 30) -> str:
174-    try:
175-        proc = subprocess.run(
176-            args, check=False, capture_output=True, text=True, timeout=timeout
177-        )
178-        return (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
179-    except Exception as exc:
180-        return f"(failed: {exc})"
181-
182-
183-def pe_magic_ok(path: Path) -> bool:

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

Edited /root/android-pipeline/lib/analyze_static.py (5 lines -> 6 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

Edited /root/android-pipeline/lib/analyze_pe.py (11 lines -> 1 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

Edited /root/android-pipeline/lib/extract_domains.py (6 lines -> 6 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:12Z

Edited /root/android-pipeline/lib/enrich_cti.py (8 lines -> 8 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

Edited /root/android-pipeline/lib/yara_generator.py (6 lines -> 9 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

Edited /root/android-pipeline/lib/deep_re_pass.py (2 lines -> 2 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

Edited /root/android-pipeline/lib/deep_re_pass.py (7 lines -> 11 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:21Z

Edited /root/android-pipeline/bin/rat5_clean_run.sh (6 lines -> 7 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:28Z

Edited /root/obsidian-telegram-bot/content.py (7 lines -> 10 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:33Z

OK android-pipeline/lib/analyze_static.py
OK android-pipeline/lib/analyze_pe.py
OK android-pipeline/lib/extract_domains.py
OK android-pipeline/lib/enrich_cti.py
OK android-pipeline/lib/yara_generator.py
OK android-pipeline/lib/deep_re_pass.py
OK obsidian-telegram-bot/content.py

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:33Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:33Z

rat5_clean_run.sh OK

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:45Z

active
ast ok

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:39:49Z

active

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:06Z

135:# --- 3b) classify_roles ZAWSZE (nawet gdy pipeline.sh nie wszedł) ---
136:ROLE_COUNTS="{}"
137:if [[ -f "$CLASSIFY_PY" && -x "$PYTHON" ]]; then
138:  log "classify_roles.py → $REPORTS_DIR"
139:  set +e
140:  ROLE_OUT="$("$PYTHON" "$CLASSIFY_PY" "$REPORTS_DIR" 2>>"$LOG_FILE")"
141:  rc=$?
142:  set -e
143:  log "classify_roles exit=$rc"
144:  echo "$ROLE_OUT" | tee -a "$LOG_FILE" >/dev/null
145:  ROLE_COUNTS="$(echo "$ROLE_OUT" | awk '/^counts /{sub(/^counts /,""); print; exit}')"
146:  [[ -n "$ROLE_COUNTS" ]] || ROLE_COUNTS="{}"
147:else
148:  log "BRAK classify_roles.py / python — pomijam tagging"
149:fi
150:if [[ -f "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" ]]; then
151:  log "hunt phishing/stealer"
152:  "$PYTHON" "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" >>"$LOG_FILE" 2>&1 || log "hunt failed (non-fatal)"
153:fi
154:

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:24Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:24Z

# --- 3b) classify_roles ZAWSZE (nawet gdy pipeline.sh nie wszedł) ---
ROLE_COUNTS="{}"
if [[ -f "$CLASSIFY_PY" && -x "$PYTHON" ]]; then
  log "classify_roles.py → $REPORTS_DIR"
  set +e
  ROLE_OUT="$("$PYTHON" "$CLASSIFY_PY" "$REPORTS_DIR" 2>>"$LOG_FILE")"
  rc=$?
  set -e
  log "classify_roles exit=$rc"
  echo "$ROLE_OUT" | tee -a "$LOG_FILE" >/dev/null
  ROLE_COUNTS="$(echo "$ROLE_OUT" | awk '/^counts /{sub(/^counts /,""); print; exit}')"
  [[ -n "$ROLE_COUNTS" ]] || ROLE_COUNTS="{}"
else
  log "BRAK classify_roles.py / python — pomijam tagging"
fi
if [[ -f "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" ]]; then
  log "hunt phishing/stealer"
  "$PYTHON" "$PIPELINE_HOME/lib/hunt_phishing_stealer.py" >>"$LOG_FILE" 2>&1 || log "hunt failed (non-fatal)"
fi

# --- 3c) export do vault ---

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:36Z

off-game.com
suahoje.com

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:36Z

urls []
ips []
emails []

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:49Z

nested.cyou
off-game.com
suahoje.com
top.cyou
ws.cyou

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:49Z

urls ['https://nested.cyou/y', 'https://top.cyou/x']
ips ['1.1.1.1', '8.8.8.8']
emails ['a@b.co']

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:40:56Z

iter: ['aaaa.json']
[+] pe aaaaaaaaaaaa…  1 stringów
iocs: [('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'x.exe')]

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:02Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:02Z

posts 9 saved True

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:06Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:36Z

bash ok
py ok

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:41:42Z

ok True 100029

### 🛠️ Akcja/narzędzie — 2026-08-15T16:42:17Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T16:42:17Z

Updated (772 chars)

### 🤖 Asystent — 2026-08-15T16:42:19Z

# Raport OPTYMALIZATORA

Przeanalizowałem oba projekty i wprowadziłem poprawki. Żadnego pliku `.env`, tokenów ani haseł nie dotykałem.

## Co poprawiłem

### Android pipeline (`/root/android-pipeline`)

1. **`lib/extract_domains.py` — naprawa gubienia domen**
   - Wcześniej `urls = urls or pat.get('urls') or []` nadpisywał URL z `patterns` gdy istniały URL top-level (raporty PE). Teraz karmimy oba źródła (top-level + `patterns.urls` + `patterns.websockets`).
   - Weryfikacja: test na syntetycznym raporcie zwraca `top.cyou`, `nested.cyou`, `ws.cyou`.

2. **`lib/enrich_cti.py` — naprawa gubienia URL/IP**
   - Analogiczna wada: `urls_field = urls_field or pat.get("urls")`. Teraz listy są łączone, więc CTI widzi zarówno top-level (PE), jak i `patterns` (APK).
   - Weryfikacja: test `collect_iocs()` zwrócił oba URL-e i oba IP.

3. **`lib/yara_generator.py` — pomijanie zagregowanych plików**
   - `iter_report_json()`/`process_report()` przetwarzały `iocs.json` jako raport i generowały „ducha” z hashem `unknown`. Dodałem do `SKIP_JSON_NAMES`: `iocs.json`, `cti_enrichment.json`, `sigma_index.json`.
   - Weryfikacja: `iter_report_json()` na katalogu z `iocs.json` + próbką zwraca już tylko próbkę.

4. **`lib/deep_re_pass.py` — złe wyciąganie SHA256**
   - `sha = sid.split("_", 1)[-1]` brało nazwę (np. `MyApp`) zamiast hasha dla katalogów z `batch_analyze.sh` (`<16hex>_<nazwa>`). Poprawione na `[0]`.
   - Dodałem fallback `reports_root.glob(f"{sha}*.md")`, bo dla katalogów batch mamy tylko prefiks hasha, a raport jest pełnym SHA256.

5. **`lib/analyze_static.py` — optymalizacja pamięci**
   - `zf.read(name)[:max_bytes]` czytał cały plik do RAM i dopiero ucinał. Teraz `zf.open(name).read(max_bytes)` czyta tylko do limitu (istotne przy dużych `classes.dex`).

6. **`lib/analyze_pe.py` — usunięcie martwego kodu**
   - Usunięto nieużywaną funkcję `run_cmd()` (potwierdzone grepem, że nigdzie nie jest wołana).

7. **`bin/rat5_clean_run.sh` — gwarancja przywrócenia `path.sh`**
   - Skrypt tymczasowo podmienia `SAMPLES_ROOT` w `config/path.sh`, ale nie miał pułapki `EXIT` (w przeciwieństwie do `rat5_android_clean.sh`). Przy niespodziewanym błędzie (`set -e`) `path.sh` mógł zostać zepsuty. Dodałem `trap restore_path EXIT` i bezpieczne `${LOG:-/tmp/rat5_restore.log}`.

### Bot Telegram (`/root/obsidian-telegram-bot`)

8. **`content.py` — naprawa uszkodzonej kolejki na dysku**
   - `load_queue()` przy uszkodzonym JSON lub złym kształcie zwracał domyślną kolejkę w pamięci, ale nie zapisywał naprawy. Po restarcie problem wracał. Teraz naprawiona kolejka jest od razu zapisywana.
   - Weryfikacja: test na uszkodzonym `channel_queue.json` — `load_queue()` zwrócił 9 wpisów i zapisał plik.

9. **Restart usługi** (bo `content.py` jest importowany przez bota):
   - `systemctl restart obsidian-telegram-bot` → `systemctl is-active` = **active**.

## Co zostawiłem świadomie

- **`bot.py: remember_owner()`** — pusta/no-op funkcja z komentarzem „First-writer-wins is disabled. Allowlist must be in .env”. To martwy kod, ale pełni rolę dokumentacji decyzji projektowej; nie jest nigdzie wołana i nie psuje działania. Nie kasowałem.
- **`bot.py`** — poza tym nie wymagał poprawek (logika była spójna; nie znalazłem TODO/niepodpiętych komend).
- **`nightly_pipeline.sh` fallback `URL_RANKED`** — zostawiłem starą ścieżkę fallback (`endpoints/all_urls_ranked.txt`); jest nieszkodliwa, a obecna ścieżka `reports/...` jest sprawdzana jako pierwsza i działa.
- **Zewnętrzne zestawy** (`tools/yara-rules`, `NusantaraScan`, `android-mcp`, `jadx`, `apktool`, `capa`) — nie ruszałem, to sygnatury/narzędzia, nie kod do refaktoru.
- **`.env`, `secrets.env`, tokeny, klucze API** — nietknięte.

## Jak zweryfikować

```bash
# Składnia bash (android-pipeline)
cd /root/android-pipeline
for f in bin/*.sh; do bash -n "$f" || echo "FAIL $f"; done

# Składnia Python (android-pipeline)
for f in lib/*.py web/*.py; do python3 -c "import ast; ast.parse(open('$f').read())" || echo "FAIL $f"; done

# Bo
…(obcięte)
