---
title: "Evilginx2 Telegram Bot (Maldevmass_bot)"
date: 2026-08-16
tags: [evilginx2, telegram, bot, automation, lab]
status: active
category: lab
---

# Evilginx2 Telegram Bot

Zarządzanie labem evilginx2 przez Telegram — bez logowania na VPS.
Bot: **@Maldevmass_bot** (id 8416294860). Powiązane: [[Evilginx2_Lab]] · [[Evilginx2_Phishlet_mockbank]] · [[Lab/Hosts]].

## Architektura

| Element | Wartość |
|---|---|
| Skrypt | `/opt/evilginx2/telegram_bot.py` (stdlib, zero zależności) |
| Config | `/opt/evilginx2/bot_config.json` (token + allowlist, **chmod 600**) |
| Tryb | **Long-polling** (getUpdates) — bot sam łączy się do `api.telegram.org` |
| Nasłuch | brak publicznego portu — zgodne z regułą loopback (webhook wymagałby otwartego portu + certu) |
| Sterowanie evilginx | `tmux send-keys` (sesja `evilginx`) + odczyt `config/config.json` |
| Dane sesji | `sessions_export.json` (z export_sessions.py); fallback: `config/data.db` (buntdb) |

## Komendy

| Komenda | Działanie |
|---|---|
| `/start`, `/help` | lista komend |
| `/status` | aktywne phishlety + hostname + lure URL-e |
| `/enable <nazwa>` | `phishlets enable` |
| `/disable <nazwa>` | `phishlets disable` |
| `/lure <nazwa>` | `lures create` + URL nowego lura |
| `/sessions [n]` | ostatnie n sesji (username, password, 2FA; domyślnie 5, max 20) |
| `/export` | eksport nowych sesji (`export_sessions.py --format telegram`; tekst lub dokument) |
| `/health` | status bota, evilginx, wątku alertów, kolejki |

## Powiadomienia push (AlertMonitor) — v2 (16.08, 15:20)

CE 3.3.0 **nie ma natywnego `on_auth_url`** (to funkcja Evilginx Pro — brak w config.go/http_proxy.go CE). Dlatego:

1. Wątek `AlertMonitor` w bocie **polluje `data.db` co 2 s** i wykrywa nowe sesje z danymi (username/password).
2. Dla każdej wywołuje **`/opt/evilginx2/hooks/on_auth.sh`** (hook zapisuje jsonl + `captured_sessions.log`).
3. Wysyła alert Markdown do właściciela (tylko gdy `owner_chat_id` ustawiony — przez bootstrap `/start`).

Pliki: `/tmp/evilginx_alerts.jsonl` (bufory), `/tmp/evilginx_alerts_sent.txt` (dedup po id sesji).

**Ustalenia techniczne (debug 15:20):**
- `subprocess.run` z hookiem wymaga **stringów** — `create_time` z data.db to unix int → `TypeError: expected str ... not int` (naprawione, `str()`).
- Python buforuje stdout przy `nohup` — logi widać dopiero z `python3 -u` (lub flush).
- Hook zapisuje jsonl nawet gdy `captured_sessions.log` jest poza uprawnieniami sandboxa (stderr ignorowany).

## Bezpieczeństwo

1. **Allowlist chatów** w configu (`allowed_chats`); gdy pusta — **bootstrap**: pierwszy chat z `/start` zostaje właścicielem i jest dopisywany do configu. Pozostali dostają `⛔ brak uprawnień`.
2. Token **nie jest w vaultcie** — tylko w `bot_config.json` (chmod 600) na .139.
3. Jedyna komunikacja zewnętrzna: wychodzące do `api.telegram.org` (polling). Brak nasłuchu publicznego.
4. Wszystkie dane (sesje, phishlety) pochodzą z laba loopback.

## Uruchomienie

```bash
python3 /opt/evilginx2/telegram_bot.py --init <TOKEN>   # jednorazowo (chmod 600)
nohup python3 /opt/evilginx2/telegram_bot.py > /tmp/telegram_bot.log 2>&1 &
# test handlerów bez Telegrama:
python3 /opt/evilginx2/telegram_bot.py --test "/status"
```

Bot działa w tle (pid 40988, start 16.08 ~15:12). Po napisaniu `/start` do @Maldevmass_bot pierwszy chat jest autoryzowany.

## Ustalenia techniczne

- **Long-polling zamiast webhooka**: webhook wymaga publicznego HTTPS + certu — łamie regułę "tylko loopback". Polling łączy się wychodząco z `getUpdates?timeout=50&offset=...`, zero portów na zewnątrz.
- **buntdb = journal**: `data.db` trzyma każdą aktualizację sesji jako osobny wpis klucza `sessions:N` (7 wpisów dla jednej sesji). Czytanie przez słownik `{id: obj}` — ostatni wpis w journalu = aktualny stan (to samo co w `export_sessions.py`).
- `sessions_export.json` trzyma `custom` jako string JSON, `data.db` jako obiekt — bot normalizuje obie formy.

## Status

- [x] Token zweryfikowany (getMe: ok, @Maldevmass_bot)
- [x] Handlery przetestowane lokalnie (`--test`): /status, /lure, /sessions, /export, /health
- [x] Long-polling działa (`getUpdates` → `{"ok":true,"result":[]}`)
- [x] **AlertMonitor działa** — live: wykrył sesję 23 w 2 s, hook → jsonl + log (v2)
- [x] Hook `on_auth.sh` — jsonl + captured_sessions.log
- [ ] Pierwszy live `/start` od użytkownika (bootstrap allowlist + owner)
- [ ] Alert push na żywo (wymaga owner_chat_id ustawionego przez /start)
