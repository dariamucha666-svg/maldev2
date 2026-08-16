---
title: "Weryfikacja zmian optymalizatora"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_29
cwd: "/root"
messages: 110
tool_calls: 108
status: archived
---

# Weryfikacja zmian optymalizatora

> Zapis czatu **Goose** · sesja '20260815_29' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | # WERYFIKATOR — sprawdzanie pracy optymalizatora |
| Wiadomości użytkownika | 2 |
| Odpowiedzi asystenta | 0 |
| Akcji narzędziowych | 108 |
| Narzędzia | 'tool'×54, 'result'×54 |
| Pliki | '/etc/systemd/system/obsidian-telegram-bot.service' · '/home/kali/obsidian-vault' · '/root/.bashrc.bak.1786119677' · '/root/.cloudflared/config.yml.bak.dash' · '/root/.mb_api_key' · '/root/.pm2/dump.pm2.bak' · '/root/MaskEncrypt/wrangler.toml.bak.1786298199' · '/root/MaskEncrypt/wrangler.toml.bak_fix' · '/root/MaskGram/src/index.ts.bak.1786189073' · '/root/OpenManus/config/config.toml.bak.20260809200922' · '/root/OpenManus/config/config.toml.bak.deepseek-proxy' · '/root/android-malware-pipeline/bin/pipeline.sh' · '/root/android-malware-pipeline/lib/analyze_static.py' · '/root/android-pipeline' · '/root/android-pipeline/.venv' · '/root/android-pipeline/.venv/bin/python' · '/root/android-pipeline/bin/nightly_pipeline.sh' · '/root/android-pipeline/bin/pipeline.sh' · '/root/android-pipeline/bin/rat5_clean_run.sh' · '/root/android-pipeline/config/path.sh' |
| Hosty | 'akamai.net' · 'akamaiedge.net' · 'amazonaws.com' · 'android.com' · 'apache.org' · 'appspot.com' · 'cloudflare.com' · 'cloudfront.net' · 'comodoca.com' · 'digicert.com' · 'example.com' · 'fastly.net' |
| Hashe | '00d3f42dc0c6…' · '0fa3360a6a00…' · '141935c46a5c…' · '178cb931cc84…' · '184ed09b7a83…' · '2b9b0ca7aeb2…' · '410a5cbaabc1…' · 'b5e8b4ae37f1…' · 'cdab250ea90f…' · 'd5b948179c8c…' · 'f19df82abf0d…' · 'f651876e9185…' |

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T22:38:09Z

# WERYFIKATOR — sprawdzanie pracy optymalizatora

Jesteś maszyną sprawdzającą. Twoje zadanie: zweryfikuj zmiany wprowadzone przez optymalizatora.

## Zakres
1. `/root/obsidian-telegram-bot/` — bot.py, graj.py i inne zmienione pliki.
2. `/root/android-pipeline/` — zmienione skrypty.

## Co robić
1. **Sprawdź składnię** wszystkich zmienionych plików:
   - Python: `.venv/bin/python -c "import ast; ast.parse(open('X').read())"` (bot) lub `python3 -m py_compile` (pipeline).
   - Bash: `bash -n`.
2. **Sprawdź logikę** — czy zmiany nie psują istniejących funkcji (np. odwołania do usuniętych/zmienionych nazw funkcji).
3. **Sprawdź, czy usługa działa**: `systemctl is-active obsidian-telegram-bot` (bot), `bash -n` na skryptach pipeline.
4. **Znajdź problemy**: niespójności, regresje, błędy które optymalizator mógł wprowadzić.

## Raport
Wypisz: co sprawdziłeś, jakie błędy znalazłeś (jeśli są), czy zmiany są bezpieczne.
Jeśli znajdziesz błąd — podaj dokładną lokalizację (plik:linia) i proponowaną poprawkę.

### 👤 Użytkownik — 2026-08-15T22:38:09Z

<turn-context>
<current-time>2026-08-15 22:38:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:13Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:13Z

Updated (327 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:15Z

=== GIT STATUS ===
not a git repo
=== TREE ===
total 336
drwxrwxr-x  6 ubuntu ubuntu  4096 Aug 15 17:13 .
drwx------ 65 root   root    4096 Aug 15 22:30 ..
-rw-------  1 root   root     497 Aug 15 11:09 .env
-rw-rw-r--  1 ubuntu ubuntu   448 Aug 15 11:07 .env.example
drwxr-xr-x  8 root   root    4096 Aug 15 22:30 .git
-rw-rw-r--  1 ubuntu ubuntu    48 Aug 15 03:25 .gitignore
-rw-------  1 root   root      10 Aug 14 23:11 .owner_id
drwxr-xr-x  5 root   root    4096 Aug 14 23:12 .venv
-rw-rw-r--  1 ubuntu ubuntu  1679 Aug 15 10:41 README.md
drwxr-xr-x  2 root   root    4096 Aug 15 22:36 __pycache__
-rwxr-xr-x  1 root   root    8404 Aug 15 03:25 alert_roles.py
-rw-r--r--  1 root   root   86991 Aug 15 22:35 bot.py
-rw-rw-r--  1 ubuntu ubuntu  9825 Aug 15 09:15 classify_roles.py
-rw-r--r--  1 root   root   10945 Aug 15 16:39 content.py
-rw-r--r--  1 root   root    6174 Aug 15 02:53 dashboard.py
-rwxr-xr-x  1 root   root     856 Aug 15 17:13 git_autocommit.sh
-rw-r--r--  1 root   root   31767 Aug 15 16:09 graj.py
-rw-r--r--  1 root   root    2020 Aug 15 11:17 harden_telegram.py
-rw-r--r--  1 root   root   15862 Aug 15 10:43 instagram.py
-rw-r--r--  1 root   root    1333 Aug 15 01:31 laik.py
-rw-rw-r--  1 ubuntu ubuntu   394 Aug 14 23:11 obsidian-telegram-bot.service
-rwxr-xr-x  1 root   root    1782 Aug 15 11:07 publish_channel.py
-rw-r--r--  1 root   root   15627 Aug 15 11:58 render.py
-rw-rw-r--  1 ubuntu ubuntu    48 Aug 14 22:56 requirements.txt
-rwxrwxr-x  1 ubuntu ubuntu   54
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:15Z

=== GIT STATUS ===
not a git repo
=== TREE ===
total 36
drwxr-xr-x  9 root root 4096 Aug 14 22:15 .
drwx------ 65 root root 4096 Aug 15 22:30 ..
drwxr-xr-x  6 root root 4096 Aug  8 11:19 .venv
drwxr-xr-x  2 root root 4096 Aug 15 16:43 bin
drwxr-xr-x  2 root root 4096 Aug 10 11:16 config
drwxr-xr-x  2 root root 4096 Aug  8 11:37 docs
drwxr-xr-x  3 root root 4096 Aug 15 11:39 lib
drwxr-xr-x 11 root root 4096 Aug 15 12:58 tools
drwxr-xr-x  3 root root 4096 Aug 15 02:53 web

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:19Z

fatal: detected dubious ownership in repository at '/root/obsidian-telegram-bot'
To add an exception for this directory, call:

	git config --global --add safe.directory /root/obsidian-telegram-bot
---EXIT: 0---

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:19Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:19Z

bin:
total 88
drwxr-xr-x 2 root   root    4096 Aug 15 16:43 .
drwxr-xr-x 9 root   root    4096 Aug 14 22:15 ..
-rwxr-xr-x 1 root   root    8809 Aug 14 19:35 batch_analyze.sh
-rwxrwxr-x 1 ubuntu ubuntu  3099 Aug  8 12:39 download_malwarebazaar.sh
-rwxrwxr-x 1 ubuntu ubuntu  8095 Aug  8 11:17 install.sh
-rwxr-xr-x 1 root   root    9932 Aug 15 16:34 nightly_pipeline.sh
-rwxr-xr-x 1 root   root    6051 Aug 15 11:39 osint_recon.sh
-rwxr-xr-x 1 root   root   20136 Aug 15 22:35 pipeline.sh
-rwxr-xr-x 1 root   root    5623 Aug 10 11:14 rat5_android_clean.sh
-rwxr-xr-x 1 root   root    2762 Aug 15 22:35 rat5_clean_run.sh
-rwxr-xr-x 1 root   root    3330 Aug 15 11:27 recon_osint.sh

config:
total 28
drwxr-xr-x 2 root   root   4096 Aug 10 11:16 .
drwxr-xr-x 9 root   root   4096 Aug 14 22:15 ..
-rw-r--r-- 1 root   root    158 Aug  8 12:39 crontab.example
-rw-r--r-- 1 root   root    424 Aug  8 11:19 path.sh
-rw-rw-r-- 1 ubuntu ubuntu 2362 Aug 15 11:42 pipeline.env
-rw------- 1 root   root    105 Aug  9 20:43 secrets.env
-rwxr-xr-x 1 root   root    562 Aug 15 10:04 secrets.env.example

docs:
total 16
drwxr-xr-x 2 root root 4096 Aug  8 11:37 .
drwxr-xr-x 9 root root 4096 Aug 14 22:15 ..
-rwxr-xr-x 1 root root 4949 Aug  8 11:37 GUIDE_PL.md

lib:
total 164
drwxr-xr-x 3 root   root    4096 Aug 15 11:39 .
drwxr-xr-x 9 root   root    4096 Aug 14 22:15 ..
drwxr-xr-x 2 root   root    4096 Aug 15 20:36 __pycache__
-rw-rw-r-- 1 ubuntu ubuntu  4823 Aug  8 11:16 aggregate_patterns.py
-rw-r--r-- 1 root
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:22Z

fatal: $HOME not set

Command exited with code 128

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:22Z

---

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:24Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:24Z

On branch main
Your branch is up to date with 'local/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   bot.py

no changes added to commit (use "git add" and/or "git commit -a")

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:27Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:27Z

=== RECENT LOG ===
fad2af2 Auto-sync: 2026-08-15 17:13:38 UTC
2b9b0ca Inicjalny commit bota XMask (obsidian-telegram-bot) — kod + /wiedza
=== DIFF STAT (unstaged) ===
 bot.py | 2 ++
 1 file changed, 2 insertions(+)
=== UNTRACKED ===
 M bot.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:31Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:31Z

=== LAST COMMIT FILES ===
fad2af2 Auto-sync: 2026-08-15 17:13:38 UTC
 git_autocommit.sh | 27 +++++++++++++++++++++++++++
 1 file changed, 27 insertions(+)
=== FULL DIFF bot.py (unstaged) ===
diff --git a/bot.py b/bot.py
index c22e908..b842f5a 100644
--- a/bot.py
+++ b/bot.py
@@ -855,6 +855,8 @@ async def cmd_graj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 
 
 async def on_graj_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
+    if not await guard(update):
+        return
     query = update.callback_query
     if not query:
         return

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:39Z

fad2af2b4e914a0670f45df8444be72004020686 2026-08-15 17:13:38 +0000 Auto-sync: 2026-08-15 17:13:38 UTC
2b9b0ca7aeb283061718c67409d82fb02f17cc79 2026-08-15 17:13:12 +0000 Inicjalny commit bota XMask (obsidian-telegram-bot) — kod + /wiedza
=== diff HEAD vs init (names) ===
 git_autocommit.sh | 27 +++++++++++++++++++++++++++
 1 file changed, 27 insertions(+)
=== current file mtimes ===
2026-08-15 22:35:55.746984647 +0000 bot.py
2026-08-15 16:09:52.878286964 +0000 graj.py
2026-08-15 16:39:28.329898951 +0000 content.py
2026-08-15 15:51:32.357213891 +0000 vault.py
2026-08-15 11:58:31.814232445 +0000 render.py
2026-08-15 11:58:31.814232445 +0000 studio.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

OK   alert_roles.py
OK   bot.py
OK   classify_roles.py
OK   content.py
OK   dashboard.py
OK   graj.py
OK   harden_telegram.py
OK   instagram.py
OK   laik.py
OK   publish_channel.py
OK   render.py
OK   studio.py
OK   test_content.py
OK   test_instagram.py
OK   test_studio.py
OK   test_vault.py
OK   vault.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

OK   git_autocommit.sh
OK   run.sh

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:50Z

OK   bin/batch_analyze.sh
OK   bin/download_malwarebazaar.sh
OK   bin/install.sh
OK   bin/nightly_pipeline.sh
OK   bin/osint_recon.sh
OK   bin/pipeline.sh
OK   bin/rat5_android_clean.sh
OK   bin/rat5_clean_run.sh
OK   bin/recon_osint.sh
OK   config/path.sh
OK   config/crontab.example
OK   config/secrets.env.example
--- py ---
OK   lib/aggregate_patterns.py
OK   lib/alert_takeovers.py
OK   lib/analyze_pe.py
OK   lib/analyze_static.py
OK   lib/classify_roles.py
OK   lib/deep_re_pass.py
OK   lib/enrich_cti.py
OK   lib/extract_domains.py
OK   lib/hunt_phishing_stealer.py
OK   lib/sigma_generator.py
OK   lib/yara_generator.py
OK   web/serve.py
FAIL tools/detection/*.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:53Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:53Z

active
exit=0
● obsidian-telegram-bot.service - XMask Obsidian Telegram bot
     Loaded: loaded (/etc/systemd/system/obsidian-telegram-bot.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-08-15 22:36:44 UTC; 2min 8s ago
   Main PID: 69456 (python)
      Tasks: 2 (limit: 7065)
     Memory: 35.0M (peak: 35.5M)
        CPU: 295ms
     CGroup: /system.slice/obsidian-telegram-bot.service
             └─69456 /root/obsidian-telegram-bot/.venv/bin/python /root/obsidian-telegram-bot/bot.py

Aug 15 22:36:44 vserver959630 systemd[1]: Started obsidian-telegram-bot.service - XMask Obsidian Telegram bot.
Aug 15 22:36:45 vserver959630 python[69456]: /root/obsidian-telegram-bot/bot.py:2322: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
Aug 15 22:36:45 vserver959630 python[69456]:   new_note = ConversationHandler(
Aug 15 22:36:45 vserver959630 python[69456]: /root/obsidian-telegram-bot/bot.py:2335: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
Aug 15 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:53Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:53Z

total 44
drwxr-xr-x  2 root root 4096 Aug 15 16:43 .
drwxr-xr-x 11 root root 4096 Aug 15 12:58 ..
-rw-r--r--  1 root root 1369 Aug 15 16:43 README.md
-rw-r--r--  1 root root 5692 Aug 15 14:33 all_lab.rules
-rw-r--r--  1 root root 1271 Aug 15 13:19 keylogger_exfil.rules
-rw-r--r--  1 root root  644 Aug 15 14:42 laplas_clipper.rules
-rw-r--r--  1 root root  810 Aug 15 14:39 lumma_digitden.rules
-rw-r--r--  1 root root 3113 Aug 15 13:11 phishing_tools.rules
-rw-r--r--  1 root root 2119 Aug 15 12:58 phishing_tools.zeek
-rw-r--r--  1 root root  799 Aug 15 13:37 xworm_tuffman.rules
--- find py in tools ---
tools/NusantaraScan/main.py
tools/NusantaraScan/setup.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:57Z

301:async def guard(update: Update) -> bool:
328:    if not await guard(update):
345:    if not await guard(update):
351:    if not await guard(update):
664:    if not await guard(update):
674:    if not await guard(update):
684:    if not await guard(update):
765:    if not await guard(update):
775:    if not await guard(update):
790:    if not await guard(update):
839:    if not await guard(update):
858:    if not await guard(update):
1004:    if not await guard(update):
1078:    if not await guard(update):
1101:    if not await guard(update):
1160:    if not await guard(update):
1170:    if not await guard(update):
1424:    if not await guard(update):
1464:    if not query or not await guard(update):
1595:    if not await guard(update):
1624:    if not query or not await guard(update):
1712:    if not await guard(update):
1773:    if not await guard(update):
1791:    if not query or not await guard(update):
1805:    if not await guard(update):
1840:    if not await guard(update):
1881:    if not await guard(update):
1912:    if not await guard(update):
1918:    if not await guard(update):
1924:    if not await guard(update):
1973:    if not await guard(update):
2008:    if not await guard(update):
2021:    if not await guard(update):
2031:    if not await guard(update):
2043:    if not await guard(update):
2075:    if not await guard(update):
2086:    if not await guard(update):
2113:    if not await guard(update):
2137:    if not await guard(update):
2148:    if not await
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:57Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:57Z

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
    if not await guard(update):
        return
    text = (
        "🎮 *GRAJ — misje obronne*\n"
        "_Uczysz się bronić, myśląc jak atakujący._\n\n"
        "🟢 ŁATWY — socjotechnika i proste techniki\n"
        "🟡 ŚREDNI — stealery i przejęcia kont\n"
        "🔴 TRUDNY — AiTM, RAT i obfuskacja\n\n"
        "*Wybierz poziom:*"
    )
    kb = graj.level_keyboard()
    kb.append([InlineKeyboardButton("📋 Katalog misji", callback_data="graj:catalog")])
    await update.effective_message.reply_markdown(
        text,
        reply_markup=InlineKeyboardMarkup(kb),
    )


async def on_graj_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    query = update.callback_query
    if not query:
        return
    await query.answe
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:38:59Z


def get_vault() -> Vault:
    global _VAULT
    if _VAULT is None:
        root = Path(os.getenv("VAULT_PATH", "/home/kali/obsidian-vault")).expanduser()
        inbox = os.getenv("INBOX_FOLDER", "Inbox")
        telegram_log = os.getenv("TELEGRAM_LOG_FOLDER", "Dzienniki/Telegram")
        _VAULT = Vault(root, inbox=inbox, telegram_log=telegram_log)
    return _VAULT


async def guard(update: Update) -> bool:
    chat = update.effective_chat
    if chat and chat.type in {Chat.GROUP, Chat.SUPERGROUP}:
        return False
    user = update.effective_user
    if user and is_allowed(user.id):
        return True
    if update.callback_query:
        try:
            await update.callback_query.answer()
        except Exception:
            pass
    return False


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not chat or chat.type not in {Chat.GROUP, Chat.SUPERGROUP}:
        return
    log.warning("leaving unexpected group chat_id=%s", chat.id)
    try:
        await context.bot.leave_chat(chat.id)
    except Exception as exc:  # noqa: BLE001
        log.warning("leave_chat failed: %s", exc)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    await update.message.reply_markdown(
        "👋 *Cześć!* To Twój prywatny bot — lab, notatki i gra.\n\n"
        "🎮 */graj* — misje obronne\n"
        "📚 */obsidian* — notatki 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:07Z

2026-08-15 22:35:01.1871647880 /root/android-pipeline/web/history.json
2026-08-15 22:35:55.7479846440 /root/android-pipeline/bin/pipeline.sh
2026-08-15 22:35:55.7479846440 /root/android-pipeline/bin/rat5_clean_run.sh
2026-08-15 22:35:55.7479846440 /root/android-pipeline/lib/analyze_static.py
2026-08-15 22:35:55.7479846440 /root/android-pipeline/lib/extract_domains.py
2026-08-15 22:37:16.1467192220 /root/android-pipeline/lib/sigma_generator.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:07Z

2026-08-15 22:35:55.7469846470 /root/obsidian-telegram-bot/bot.py

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:14Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:14Z

  579 bin/pipeline.sh
   93 bin/rat5_clean_run.sh
  487 lib/analyze_static.py
  134 lib/extract_domains.py
  358 lib/sigma_generator.py
 1651 total

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:14Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:14Z

===== bin/rat5_clean_run.sh =====
     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3	
     4	STAMP=$(date -u +%Y%m%dT%H%M%SZ)
     5	ROOT="/root/samples/rat5_${STAMP}"
     6	PATH_SH="/root/android-pipeline/config/path.sh"
     7	PATH_BAK="/root/android-pipeline/config/path.sh.bak.rat5run"
     8	PIDFILE="/root/samples/rat5_latest.pid"
     9	
    10	mkdir -p "$ROOT"/{raw,quarantine,decompiled,sources,reports,features,native,logs,output}
    11	ln -sfn "$ROOT" /root/samples/rat5_latest
    12	
    13	# API key
    14	MB_API_KEY=""
    15	if [[ -f /root/android-pipeline/config/secrets.env ]]; then
    16	  # shellcheck disable=SC1090
    17	  source /root/android-pipeline/config/secrets.env
    18	fi
    19	if [[ -z "${MB_API_KEY:-}" && -f /root/.mb_api_key ]]; then
    20	  MB_API_KEY=$(tr -d ' \t\r\n' < /root/.mb_api_key)
    21	  export MB_API_KEY
    22	fi
    23	if [[ -z "${MB_API_KEY:-}" ]]; then
    24	  echo "NO MB_API_KEY" >&2
    25	  exit 1
    26	fi
    27	export MB_API_KEY
    28	
    29	# Temporarily retarget path.sh
    30	cp -a "$PATH_SH" "$PATH_BAK"
    31	sed -i "s|export SAMPLES_ROOT=\"/root/samples\"|export SAMPLES_ROOT=\"$ROOT\"|" "$PATH_SH"
    32	
    33	restore_path() {
    34	  if [[ -f "$PATH_BAK" ]]; then
    35	    mv -f "$PATH_BAK" "$PATH_SH"
    36	    echo "[restore] path.sh -> /root/samples" | tee -a "${LOG:-/tmp/rat5_restore.log}" || true
    37	  fi
    38	}
    39	trap restore_path EXIT
    40	
    41	export MB_TAG=rat
    42	export M
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:25Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:25Z

     1	export PIPELINE_HOME="/root/android-pipeline"
     2	export SAMPLES_ROOT="/root/samples"
     3	export TOOLS_DIR="/root/android-pipeline/tools"
     4	export VENV_DIR="/root/android-pipeline/.venv"
     5	export PATH="$TOOLS_DIR/jadx/bin:$TOOLS_DIR/apktool:$TOOLS_DIR/capa:$PIPELINE_HOME/bin:$PATH"
     6	# shellcheck disable=SC1091
     7	source "$VENV_DIR/bin/activate"
     8	[[ -f "$PIPELINE_HOME/config/pipeline.env" ]] && source "$PIPELINE_HOME/config/pipeline.env"

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:25Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:25Z

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
    22	export JADX_THREADS="${JADX_THREADS:-2}"
    23	export SKIP_GHIDRA="${SKIP_GHIDRA:-1}"          # 1 = skip heavy Ghidra (recommended on 6GB)
    24	export SKIP_NATIVE="${SKIP_NATIVE:-0}"          # 0 = extract & triage .so
    25	export SKIP_NUSANTARA="${SKIP_NUSANTARA:-0}"
    26	export KEEP_DECOMPILED="${KEEP_DECOMPILED:-1}"  # 0 = delete apktool output to save disk
    27	
    28	# MalwareBazaar (optional)
    29	export MB_API_KEY="${MB_API_KEY:-}"
    30	export MB_TAG="${MB_TAG:-apk}"                  # tag filter for recent s
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:28Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:49Z

/root/android-pipeline/.venv/bin/python: No module named pyflakes

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:49Z

/usr/bin/python3: No module named pyflakes

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:51Z

(no output)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:54Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:39:54Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:00Z

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
    25	
    26	# High-signal Android / malware-related API substrings
    27	SUSPICIOUS_APIS = [
    28	    "Runtime.exec",
    29	    "ProcessBuilder",
    30	    "DexClassLoader",
    31	    "PathClassLoader",
    32	    "InMemoryDexClassLoader",
    33	    "System.loadLibrary",
    34	    "Runtime.getRuntime",
    35	    "TelephonyManager",
    36	    "getDeviceId",
    37	    "getSubscriberId",
    38	    "SmsManager",
    39	    "sendTextMessage",
    40	    "AccessibilityService",
    41	    "MediaProjection",
    42	    "Camera",
    43	    "getInstalledPackages",
    44	    "PackageManager",
    
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:09Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:09Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:29Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:29Z

===== lib/analyze_pe.py =====
9:import argparse
429:def main() -> int:
430:    parser = argparse.ArgumentParser(description="Static PE analyzer")
431:    parser.add_argument("sample", type=Path)
432:    parser.add_argument("-o", "--outdir", type=Path, required=True)
453:if __name__ == "__main__":
===== lib/aggregate_patterns.py =====
5:import argparse
27:def main() -> int:
28:    ap = argparse.ArgumentParser()
29:    ap.add_argument("--reports", type=Path, required=True)
30:    ap.add_argument("--features-out", type=Path, required=True)
31:    ap.add_argument("--patterns-out", type=Path, required=True)
139:if __name__ == "__main__":
===== lib/yara_generator.py =====
377:def main(argv: list[str] | None = None) -> int:
378:    args = list(sys.argv[1:] if argv is None else argv)
420:if __name__ == "__main__":
===== lib/classify_roles.py =====
260:def main() -> int:
261:    root = Path(sys.argv[1] if len(sys.argv) > 1 else "/root/samples/reports")
291:if __name__ == "__main__":
===== lib/hunt_phishing_stealer.py =====
61:def main() -> int:
215:if __name__ == "__main__":
===== lib/enrich_cti.py =====
23:import argparse
528:def main() -> int:
529:    ap = argparse.ArgumentParser(description="Enrich pipeline IOCs with threat-intel databases")
530:    ap.add_argument("reports_dir", nargs="?", default=os.environ.get("REPORTS_DIR") or os.path.expanduser("~/samples/reports"))
531:    ap.add_argument("--limit", type=int, default=None, help="ogranicz liczbę hashów (szybki test)")
532:    
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:32Z

def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print(
            "Użycie: yara_generator.py <katalog_z_raportami> [plik_wyjściowy.yar] [--iocs-out FILE]\n"
            "Przykład: yara_generator.py /root/samples/reports "
            "/root/samples/reports/auto_rules.yar"
        )
        return 0 if args and args[0] in {"-h", "--help"} else 1

    iocs_out = None
    if "--iocs-out" in args:
        idx = args.index("--iocs-out")
        if idx + 1 >= len(args):
            print("[!] --iocs-out wymaga ścieżki")
            return 1
        iocs_out = Path(args[idx + 1])
        del args[idx : idx + 2]

    positional = [a for a in args if not a.startswith("-")]
    if not positional:
        print("[!] Brak katalogu z raportami")
        return 1

    report_dir = Path(positional[0])
    if not report_dir.exists():
        print(f"[!] Nie istnieje: {report_dir}")
        return 1

    output = Path(positional[1]) if len(positional) > 1 else report_dir / "auto_rules.yar"
    if iocs_out is None:
        iocs_out = (report_dir if report_dir.is_dir() else report_dir.parent) / "iocs.json"

    gen = YARAGenerator(report_dir if report_dir.is_dir() else report_dir.parent)
    for json_file in iter_report_json(report_dir):
        gen.process_report(json_file)
    gen.save_rules(str(output))
    gen.save_iocs(str(iocs_out))
    if not gen.rules:
        print("[!] Nie 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:37Z

def main() -> int:
    parser = argparse.ArgumentParser(description="Static PE analyzer")
    parser.add_argument("sample", type=Path)
    parser.add_argument("-o", "--outdir", type=Path, required=True)
    args = parser.parse_args()
    sample = args.sample.expanduser().resolve()
    if not sample.is_file():
        print(f"not a file: {sample}", file=sys.stderr)
        return 2
    outdir = args.outdir.expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    report = analyze_pe(sample)
    sha = report["hashes"]["sha256"]
    json_path = outdir / f"{sha}.json"
    md_path = outdir / "summary.md"
    html_path = outdir / "summary.html"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    write_html(report, html_path)
    print(json.dumps({"ok": True, "sha256": sha, "json": str(json_path), "md": str(md_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
=== output naming ===
96:def sha256_file(path: Path) -> str:
97:    h = hashlib.sha256()
106:    sha1 = hashlib.sha1()
107:    sha256 = hashlib.sha256()
111:            sha1.update(chunk)
112:            sha256.update(chunk)
115:        "sha1": sha1.hexdigest(),
116:        "sha256": sha256.hexdigest(),
136:def shannon_entropy(data: bytes) -> float:
212:        ent = round(shannon_entropy(data), 4)
317:    file_entropy = round(shannon_entropy(whole), 4) if whole else None
348:        f"- sha256: 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:44Z

            | filters.VIDEO_NOTE
            | filters.VOICE
            | filters.AUDIO
            | filters.Document.VIDEO
            | filters.Document.AUDIO,
            on_studio_media,
        )
    )
    app.add_handler(new_note)
    app.add_handler(append_conv)
    app.add_handler(CallbackQueryHandler(on_obsidian_cb, pattern=r"^ob:"))
    app.add_handler(CallbackQueryHandler(on_wiedza_cb, pattern=r"^wiedza:"))
    app.add_handler(CallbackQueryHandler(on_ig_cb, pattern=r"^ig:"))
    app.add_handler(CallbackQueryHandler(on_kanal_cb, pattern=r"^kanal:"))
    app.add_handler(CallbackQueryHandler(on_callback, pattern=r"^(get|dash|xmask|laik|jobadd|jobcls):"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_plain))
    app.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))

    # Codzienne automatyczne podsumowanie (09:00 czasu serwera)
    try:
        app.job_queue.run_daily(
            daily_summary_job,
            time=datetime.time(hour=9, minute=0),
            name="daily_summary",
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("daily summary job setup failed: %s", exc)

    return app


def main() -> None:
    require_allowlist()
    app = build_app()
    log.info("starting bot, allowlist=%s", len(allowed_ids()))
    app.run_polling(allowed_updates=["message", "callback_query", "my_chat_member"])


if __name__ == "__main__":
    main()

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:44Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:44Z

2431:def main() -> None:
2435:    app.run_polling(allowed_updates=["message", "callback_query", "my_chat_member"])
2438:if __name__ == "__main__":

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:46Z

838:async def cmd_graj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
850:    kb.append([InlineKeyboardButton("📋 Katalog misji", callback_data="graj:catalog")])
857:async def on_graj_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
912:                [[InlineKeyboardButton("🛡️ Zobacz obronę", callback_data=f"graj:def:{attack_id}:{idx}")]]
929:                [[InlineKeyboardButton("▶️ Rozpocznij quiz", callback_data=f"graj:go:{attack_id}:{idx}")]]
997:        kb.append([InlineKeyboardButton("📋 Katalog misji", callback_data="graj:catalog")])
2223:        await cmd_graj(update, context)
2393:    app.add_handler(CommandHandler("graj", cmd_graj))
2394:    app.add_handler(CommandHandler("gra", cmd_graj))
2395:    app.add_handler(CommandHandler("play", cmd_graj))
2396:    app.add_handler(CallbackQueryHandler(on_graj_cb, pattern=r"^graj"))

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:52Z

===== test_content.py =====
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit=0
===== test_instagram.py =====
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
exit=0
===== test_studio.py =====
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit=0
===== test_vault.py =====
ok
exit=0

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:56Z

12:LEVELS: list[dict] = [
18:ATTACKS: dict[str, dict] = {
393:def catalog_text() -> str:
409:def level_keyboard() -> list[list[InlineKeyboardButton]]:
413:def attack_keyboard(level_id: str) -> list[list[InlineKeyboardButton]]:
420:def method_keyboard(attack_id: str) -> list[list[InlineKeyboardButton]]:
428:def question_keyboard(attack_id: str, method_idx: int, q_idx: int, score: int) -> list[list[InlineKeyboardButton]]:

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:58Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:40:58Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:08Z

<class 'dict'>
['generated', 'count', 'rules', 'iocs']
{
  "generated": "2026-08-14",
  "count": 15,
  "rules": 3,
  "iocs": [
    {
      "hash": "0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a",
      "strings": [],
      "family": "Android.Dropper.Porntok",
      "date": "2026-08-14",
      "kind": "apk",
      "name": "0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a.apk",
      "urls": [
        "http://schemas.android.com/apk/res/android",
        "https://localhost"
      ],
      "rule": false,
      "role": "dropper",
      "tags": [
        "pipeline",
        "apk",
        "dropper",
        "android"
      ]
    },
    {
      "hash": "178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4",
      "strings": [
        "LogonUserW",
        "NetUserAdd",
        "NetUserDel",
        "NetShareAdd",
        "NetShareDel"
      ],
      "family": "Backdoor.Win64.EASportsGo",
      "date": "2026-08-14",
      "kind": "pe",
      "name": "141935c46a5c4ff1b84b433e84f36e61.exe",
      "urls": [],
      "rule": true,
      "role": "backdoor",
      "tags": [
        "pipeline",
        "pe",
        "backdoor"
      ]
    },
    {
      "hash": "410a5cbaabc1cdee003ac2fd1d6c1ca8b58c9eb75cd7c671dfa163653b5ae712",
      "strings": [],
      "family": "Android.Lab.MalwareAPK",
      "date": "2026-08-14",
      "kind": "apk",
      "name": "410a5cbaabc1cdee003ac2fd1d6c1ca8b58c9eb75cd7c671dfa163653b5ae712.apk",
      "urls": [
      
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:11Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:11Z

no shellcheck

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:17Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:17Z

=== import lib/analyze_static.py ===
OK m
=== import lib/extract_domains.py ===
OK m
=== import lib/sigma_generator.py ===
OK m
=== import lib/analyze_pe.py ===
OK m
=== import lib/yara_generator.py ===
OK m
=== import lib/enrich_cti.py ===
OK m
=== import lib/classify_roles.py ===
OK m
=== import lib/hunt_phishing_stealer.py ===
OK m
=== import lib/aggregate_patterns.py ===
OK m

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:20Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:20Z

total 940
drwxr-xr-x 40 root root  20480 Aug 15 10:21 .
drwxr-xr-x 15 root root   4096 Aug 14 23:03 ..
drwxr-xr-x  2 root root   4096 Aug 15 02:08 00d3f42dc0c6527d375f8b5430915ca27f0da7b9608e446d3e5f6c17082577a5
-rw-r--r--  1 root root   8894 Aug 15 11:40 00d3f42dc0c6527d375f8b5430915ca27f0da7b9608e446d3e5f6c17082577a5.json
drwxr-xr-x  2 root root   4096 Aug 12 02:02 0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a
-rw-r--r--  1 root root    651 Aug 15 04:18 0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a.features.json
-rw-r--r--  1 root root   4342 Aug 15 11:40 0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a.json
-rw-r--r--  1 root root   1037 Aug 15 04:18 0fa3360a6a00ec8d3c988f4f81be8e79674bb8cf58c9350237062eb60f54bf4a.md
drwxr-xr-x  2 root root   4096 Aug 14 19:34 178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4
-rw-r--r--  1 root root   8811 Aug 15 11:40 178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4.json
drwxr-xr-x  2 root root   4096 Aug 15 02:07 184ed09b7a83640f182566d2cc4bc2d30c8a67f33715e4db1e61642e2c168d12
-rw-r--r--  1 root root    635 Aug 15 02:07 184ed09b7a83640f182566d2cc4bc2d30c8a67f33715e4db1e61642e2c168d12.features.json
-rw-r--r--  1 root root   4724 Aug 15 11:40 184ed09b7a83640f182566d2cc4bc2d30c8a67f33715e4db1e61642e2c168d12.json
-rw-r--r--  1 root root    711 Aug 15 02:07 184ed09b7a83640f182566d2cc4bc2d30c8a67f33715e4db1e61642e2c168d12.md
drwxr-xr-x  2 root root   4096 Aug 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:24Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:24Z

=== extract_domains ===
off-game.com
suahoje.com
exit=0

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:24Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:24Z

=== sigma_generator ===
[+] xmask_pe_hashes_process.yml
[+] xmask_pe_hashes_file.yml
[+] xmask_role_backdoor_hashes.yml
[+] xmask_win_account_api_cluster.yml
[+] xmask_network_hosts.yml
[+] 5 reguł Sigma → /tmp/sigma_test  (samples=15)
exit=0
total 80
drwxr-xr-x  2 root root  4096 Aug 15 22:41 .
drwxrwxrwt 41 root root 49152 Aug 15 22:41 ..
-rw-r--r--  1 root root   792 Aug 15 22:41 README.md
-rw-r--r--  1 root root   726 Aug 15 22:41 xmask_network_hosts.yml
-rw-r--r--  1 root root   812 Aug 15 22:41 xmask_pe_hashes_file.yml
-rw-r--r--  1 root root   819 Aug 15 22:41 xmask_pe_hashes_process.yml
-rw-r--r--  1 root root   798 Aug 15 22:41 xmask_role_backdoor_hashes.yml
-rw-r--r--  1 root root   878 Aug 15 22:41 xmask_win_account_api_cluster.yml

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:28Z

=== yara_generator ===
[-] Brak stringów IoC: b5e8b4ae37f13f2f0d5395712afb4c8f8b71034915d2a76ef2bbc0297b555aa0.json
[+] pe bc8d75d9c7ac…  11 stringów
[-] Brak stringów IoC: cdab250ea90f79efb405d13c4f77fff2876b21392ddc0849737d2ab86e308189.json
[-] Brak stringów IoC: d5b948179c8cc33e4cbeebe0369c7dca452d968646a588d730341c3879d64880.json
[+] pe e86fc24e1881…  5 stringów
[-] Brak stringów IoC: f19df82abf0d66389467746f519557e81ca5b373a97e23da7e414204e4931242.json
[+] pe f53ceeb84e15…  1 stringów
[-] Brak stringów IoC: f651876e9185c206d770229b0cb312b7ae620225e0e6768709b93d4258bbbced.json
[-] Brak stringów IoC: fdbee28882e9c13941fc4fc4575935af1ab37ca84114ec4bc039b50f770ce218.json
[-] Brak stringów IoC: fea8e251a380ba27de9e85966a7b8c31f5e48641414a4f9d933546bdd2480752.json
[-] Brak stringów IoC: osint_20260815T102155Z.json
[-] Brak stringów IoC: osint_20260815T102323Z.json
[-] Brak stringów IoC: osint_20260815T105834Z.json
[-] Brak stringów IoC: osint_20260815T110127Z.json
[-] Brak stringów IoC: osint_20260815T110346Z.json
[-] Brak stringów IoC: osint_20260815T111529Z.json
[-] Brak stringów IoC: osint_20260815T113026Z.json
[-] Brak stringów IoC: osint_20260815T114152Z.json
[+] Zapisano 15 reguł do /tmp/test_auto_rules.yar
[+] Zapisano 41 IOC do /tmp/test_iocs.json
exit=0
-rw-r--r-- 1 root root  8475 Aug 15 22:41 /tmp/test_auto_rules.yar
-rw-r--r-- 1 root root 19668 Aug 15 22:41 /tmp/test_iocs.json

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:28Z

total 8
drwxr-xr-x  2 root root 4096 Aug 15 09:54 .
drwxr-xr-x 15 root root 4096 Aug 14 23:03 ..
--- pe ---
total 8
drwxr-xr-x  2 root root 4096 Aug 15 09:54 .
drwxr-xr-x 15 root root 4096 Aug 14 23:03 ..
--- quarantine ---
total 8
drwxr-xr-x  2 root root 4096 Aug 15 09:54 .
drwxr-xr-x 15 root root 4096 Aug 14 23:03 ..

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:34Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:34Z

---
--- rat5 dirs ---
--- recent logs ---
total 504
-rw-r--r--  1 root root 111488 Aug 15 11:41 nightly_20260815.log
-rw-r--r--  1 root root   5222 Aug 15 10:00 r2_archive_20260815_095202Z_resume.log
-rw-r--r--  1 root root   5222 Aug 15 10:00 r2_archive_resume_nohup.out
drwxr-xr-x  2 root root   4096 Aug 15 09:57 .
-rw-r--r--  1 root root   3224 Aug 15 09:54 r2_archive_20260815_095202Z.log
-rw-r--r--  1 root root   3224 Aug 15 09:54 r2_archive_nohup.out
-rw-r--r--  1 root root   3753 Aug 15 04:18 pipeline_20260815T041825Z.log
-rw-r--r--  1 root root   3753 Aug 15 03:31 pipeline_20260815T033101Z.log
-rw-r--r--  1 root root   3672 Aug 15 02:55 pipeline_20260815T025526Z.log
-rw-r--r--  1 root root   3672 Aug 15 02:46 pipeline_20260815T024650Z.log
-rw-r--r--  1 root root   3425 Aug 15 02:12 cron.log
-rw-r--r--  1 root root  52845 Aug 15 02:12 pipeline_20260815T020701Z.log
drwxr-xr-x 15 root root   4096 Aug 14 23:03 ..
-rw-r--r--  1 root root    162 Aug 14 22:16 ioc_dashboard.log
-rw-r--r--  1 root root  13163 Aug 14 22:15 pipeline_20260814T221526Z.log
-rw-r--r--  1 root root   1869 Aug 14 21:32 pipeline_20260814T213132Z.log
-rw-r--r--  1 root root   1623 Aug 14 19:34 pipeline_20260814T193322Z.log
-rw-r--r--  1 root root   1197 Aug 14 19:29 pipeline_20260814T192953Z.log
-rw-r--r--  1 root root  16957 Aug 14 02:02 nightly_20260814.log

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:50Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:41:50Z

=== run.sh ===
     1	#!/usr/bin/env bash
     2	set -euo pipefail
     3	cd "$(dirname "$0")"
     4	
     5	if [[ ! -d .venv ]]; then
     6	  python3 -m venv .venv
     7	  .venv/bin/pip install -U pip
     8	  .venv/bin/pip install -r requirements.txt
     9	fi
    10	
    11	if [[ ! -f .env ]]; then
    12	  cp .env.example .env
    13	  echo "Utworzyłem .env — wklej TELEGRAM_BOT_TOKEN od @BotFather i uruchom ponownie."
    14	  exit 1
    15	fi
    16	
    17	if grep -q '^TELEGRAM_BOT_TOKEN=$' .env || grep -q '^TELEGRAM_BOT_TOKEN=PASTE' .env; then
    18	  echo "Wpisz token do .env (TELEGRAM_BOT_TOKEN=...) i uruchom ponownie."
    19	  exit 1
    20	fi
    21	
    22	exec .venv/bin/python bot.py
=== service ===
     1	[Unit]
     2	Description=XMask Obsidian Telegram bot
     3	After=network-online.target
     4	Wants=network-online.target
     5	
     6	[Service]
     7	Type=simple
     8	WorkingDirectory=/root/obsidian-telegram-bot
     9	EnvironmentFile=/root/obsidian-telegram-bot/.env
    10	ExecStart=/root/obsidian-telegram-bot/.venv/bin/python /root/obsidian-telegram-bot/bot.py
    11	Restart=always
    12	RestartSec=5
    13	TimeoutStopSec=20
    14	
    15	[Install]
    16	WantedBy=multi-user.target
=== git_autocommit.sh ===
     1	#!/usr/bin/env bash
     2	# Commit zmiany kodu bota i push do bare repo (local). Opcjonalnie origin (GitHub).
     3	set -u
     4	cd /root/obsidian-telegram-bot || exit 1
     5	git config --global --add safe.directory /root/obsidia
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:08Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:08Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:15Z

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

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:22Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T22:42:22Z

/root/nightly_pipeline.sh
/root/openmanus-config.toml.bak
/root/MaskEncrypt/wrangler.toml.bak_fix
/root/MaskEncrypt/wrangler.toml.bak.1786298199
/root/android-pipeline/bin/nightly_pipeline.sh
/root/android-pipeline/bin/pipeline.sh
/root/android-pipeline/lib/analyze_static.py
/root/android-pipeline/lib/sigma_generator.py
/root/.cloudflared/config.yml.bak.dash
/root/payload_win_debug.exe.bak.1786545939
/root/android-malware-pipeline/bin/pipeline.sh
/root/android-malware-pipeline/lib/analyze_static.py
/root/OpenManus/config/config.toml.bak.deepseek-proxy
/root/OpenManus/config/config.toml.bak.20260809200922
/root/payload_win_debug.exe.bak.1786545529
/root/rat-c2/server.py.bak.20260815_054724
/root/obsidian-vault/Narzedzia/export_pipeline_to_obsidian.sh.bak.20260815
/root/MaskGram/src/index.ts.bak.1786189073
/root/.bashrc.bak.1786119677
/root/pipeline.sh
/root/.pm2/dump.pm2.bak
