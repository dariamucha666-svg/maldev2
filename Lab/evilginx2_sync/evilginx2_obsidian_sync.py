#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evilginx2_obsidian_sync.py — automatyczny sync sesji Evilginx2 (AiTM) do Obsidiana.

Zrodlo danych (wazne — v3.3.0 CE):
  Evilginx2 v3.3.0 CE przechowuje przechwycone sesje w bazie buntdb:
      /opt/evilginx2/config/data.db
  (plik to strumien rekordow RESP:  set sessions:<id> <json>  — ostatni rekord
  dla danego klucza wygrywa). Logi terminalowe NIE sa zapisywane do plikow,
  dlatego glownym zrodlem jest data.db.

  Dodatkowo skrypt potrafi tailowac katalog logow (~/.evilginx2/logs/*.log)
  jako zrodlo triggerow — dziala, gdy evilginx jest uruchamiany z tee/script
  (patrz run-with-log.sh). Jesli katalog nie istnieje, tailowanie jest pomijane.

Wyjscie:
  Notatka Markdown per sesja w katalogu:
      <vault>/XMask/maldev2/Lab/Sessions/Sesja_<id>.md

Uzycie:
  ./evilginx2_obsidian_sync.py                  # tryb ciagly (daemon)
  ./evilginx2_obsidian_sync.py --once           # jeden przebieg i wyjscie
  ./evilginx2_obsidian_sync.py --reset-state    # wyczysc stan -> odtworz notatki
  ./evilginx2_obsidian_sync.py --db /path/data.db --notes-dir /path/Sessions

Wymagania: Python 3.8+ (tylko standard library).
"""

import argparse
import json
import os
import re
import signal
import sys
import time
from datetime import datetime

# --------------------------------------------------------------------------
# Domyslne sciezki (host .139 / vserver580088)
# --------------------------------------------------------------------------
DEFAULT_DB = "/opt/evilginx2/config/data.db"
DEFAULT_VAULT = "/root/Obsidian"
DEFAULT_NOTES_DIR = os.path.join(DEFAULT_VAULT, "XMask", "maldev2", "Lab", "Sessions")
DEFAULT_LOGS_DIR = os.path.expanduser("~/.evilginx2/logs")
DEFAULT_INTERVAL = 2.0  # sekundy miedzy skanami data.db

RE_SESSION_KEY = re.compile(r"^sessions:(\d+)$")

# Markery w logu evilginx, po ktorych wymuszamy natychmiastowy rescan DB.
RE_LOG_TRIGGER = re.compile(
    r"all authorization tokens intercepted|session data saved|tokens captured|sess:[a-f0-9]+",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------
# Parser strumienia RESP (format buntdb)
# --------------------------------------------------------------------------
def iter_resp_records(data):
    """Yields list of byte-args for each RESP array command in `data`."""
    i, n = 0, len(data)
    while i < n:
        # pomijaj biale znaki / uszkodzone poczatki
        while i < n and data[i] in (0x0D, 0x0A):
            i += 1
        if i >= n:
            break
        if data[i] != ord("*"):
            j = data.find(b"\r\n", i)
            if j == -1:
                break
            i = j + 2
            continue
        j = data.find(b"\r\n", i)
        if j == -1:
            break
        try:
            nargs = int(data[i + 1:j])
        except ValueError:
            break
        i = j + 2
        args = []
        ok = True
        for _ in range(nargs):
            if i >= n or data[i] != ord("$"):
                ok = False
                break
            j = data.find(b"\r\n", i)
            if j == -1:
                ok = False
                break
            try:
                ln = int(data[i + 1:j])
            except ValueError:
                ok = False
                break
            i = j + 2
            val = data[i:i + ln]
            i += ln
            if data[i:i + 2] == b"\r\n":
                i += 2
            args.append(val)
        if not ok:
            break
        yield args


def parse_db(path):
    """Zwraca {klucz_rekordu: dict-sesji} — ostatni zapis na klucz wygrywa."""
    sessions = {}
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        return sessions
    except OSError as e:
        log("warn", "nie moge odczytac %s: %s", path, e)
        return sessions

    for args in iter_resp_records(data):
        if len(args) < 3 or args[0] != b"set":
            continue
        key, value = args[1], args[2]
        try:
            key_s = key.decode("utf-8")
        except UnicodeDecodeError:
            continue
        m = RE_SESSION_KEY.match(key_s)
        if not m:
            continue
        try:
            obj = json.loads(value.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(obj, dict):
            continue
        sessions[key_s] = obj
    return sessions


# --------------------------------------------------------------------------
# Konwersja sesji -> notatka Markdown
# --------------------------------------------------------------------------
def _fmt_time(ts):
    if not ts:
        return "-"
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "-"


def _fmt_iso(ts):
    if not ts:
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%dT%H:%M:%S")
    except (ValueError, OSError):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def session_note_markdown(s):
    """Buduje tresc notatki Obsidian dla sesji z data.db."""
    session_id = s.get("session_id", "") or ""
    short_id = session_id[:12] or "db_%s" % s.get("id", "?")

    username = s.get("username", "") or ""
    password = s.get("password", "") or ""
    landing_url = s.get("landing_url", "") or ""
    phishlet = s.get("phishlet", "") or ""

    # tokens: {domain: {name: {Name, Value, Path, HttpOnly}}}
    tokens = s.get("tokens", {}) or {}
    token_lines = []
    for domain in sorted(tokens.keys()):
        for tname in sorted((tokens[domain] or {}).keys()):
            t = tokens[domain][tname] or {}
            val = t.get("Value", "")
            attrs = ["domain `%s`" % domain]
            if t.get("Path"):
                attrs.append("path `%s`" % t["Path"])
            if t.get("HttpOnly"):
                attrs.append("http_only")
            token_lines.append(
                "  - `%s` = `%s` (%s)" % (tname, val, ", ".join(attrs))
            )
    if not token_lines:
        token_lines.append("  - (brak)")

    custom = s.get("custom", {}) or {}
    custom_lines = []
    for k in sorted(custom.keys()):
        custom_lines.append("  - `%s` = `%s`" % (k, custom[k]))

    has_data = bool(username or password or tokens)
    status = (
        "Pełne przechwycenie (creds + tokens)"
        if (username or password) and tokens
        else (
            "Przechwycono dane"
            if has_data
            else "Niekompletna — tylko wejście na lure (brak creds/tokens)"
        )
    )

    lines = []
    lines.append("---")
    lines.append("date: %s" % _fmt_iso(s.get("create_time")))
    lines.append("tags: [evilginx2, phish, aitm]")
    lines.append("---")
    lines.append("")
    lines.append("# Sesja %s" % short_id)
    lines.append("")
    lines.append("- **Username**: %s" % (username or "—"))
    lines.append("- **Password**: %s" % (password or "—"))
    lines.append("- **Tokens**:")
    lines.extend(token_lines)
    lines.append("- **Lure**: %s" % (landing_url or "—"))
    lines.append("")
    lines.append("> [!info] %s" % status)
    lines.append("")
    lines.append("## Szczegóły")
    lines.append("")
    lines.append("- **DB id**: %s" % s.get("id", "—"))
    lines.append("- **Phishlet**: %s" % (phishlet or "—"))
    lines.append("- **Remote addr**: %s" % (s.get("remote_addr", "") or "—"))
    lines.append("- **User-Agent**: %s" % (s.get("useragent", "") or "—"))
    lines.append("- **Created**: %s" % _fmt_time(s.get("create_time")))
    lines.append("- **Updated**: %s" % _fmt_time(s.get("update_time")))
    if custom_lines:
        lines.append("- **Custom**:")
        lines.extend(custom_lines)
    lines.append("")
    return "\n".join(lines)


def note_filename(s):
    session_id = s.get("session_id", "") or ""
    short_id = session_id[:12] or "db_%s" % s.get("id", "?")
    return "Sesja_%s.md" % short_id


# --------------------------------------------------------------------------
# Stan przetworzonych sesji (dedupe przez restart)
# --------------------------------------------------------------------------
def load_state(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            st = json.load(f)
        return set(st.get("processed", []))
    except (OSError, ValueError):
        return set()


def save_state(path, processed):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"processed": sorted(processed)}, f, indent=1)
    os.replace(tmp, path)


# --------------------------------------------------------------------------
# Tailer logow (opcjonalny trigger; nie zrodlo danych)
# --------------------------------------------------------------------------
class LogTailer:
    def __init__(self, logs_dir):
        self.logs_dir = logs_dir
        self._path = None
        self._ino = None
        self._offset = 0

    def _newest_log(self):
        try:
            files = [
                os.path.join(self.logs_dir, f)
                for f in os.listdir(self.logs_dir)
                if f.endswith(".log")
            ]
        except OSError:
            return None
        if not files:
            return None
        return max(files, key=lambda p: os.path.getmtime(p))

    def poll(self):
        """Czyta nowe linie z najnowszego pliku logu.
        Zwraca True, gdy pojawil sie marker sesji (wymus rescan DB)."""
        if not self.logs_dir or not os.path.isdir(self.logs_dir):
            return False
        path = self._newest_log()
        if path is None:
            self._path, self._ino, self._offset = None, None, 0
            return False
        try:
            st = os.stat(path)
            ino = st.st_ino
            size = st.st_size
            if self._path != path or self._ino != ino:
                # nowy plik / rotacja -> czytaj od poczatku
                self._path, self._ino, self._offset = path, ino, 0
            if size < self._offset:  # plik przyciety
                self._offset = 0
            with open(path, "rb") as f:
                f.seek(self._offset)
                chunk = f.read()
                self._offset = f.tell()
        except OSError:
            return False
        if not chunk:
            return False
        return bool(RE_LOG_TRIGGER.search(chunk.decode("utf-8", "replace")))


# --------------------------------------------------------------------------
# Logowanie
# --------------------------------------------------------------------------
def log(level, fmt, *args):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[%s] [%s] %s" % (ts, level, fmt % args if args else fmt), flush=True)


# --------------------------------------------------------------------------
# Glowna petla
# --------------------------------------------------------------------------
def process_new_sessions(parsed, processed, notes_dir):
    """Tworzy notatki dla nowych sesji. Zwraca liczbe utworzonych."""
    created = 0
    for key in sorted(parsed.keys(), key=lambda k: int(k.split(":")[1])):
        s = parsed[key]
        sid = s.get("session_id", "") or key
        if sid in processed:
            continue
        try:
            os.makedirs(notes_dir, exist_ok=True)
            fname = note_filename(s)
            fpath = os.path.join(notes_dir, fname)
            tmp = fpath + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(session_note_markdown(s))
            os.replace(tmp, fpath)
            processed.add(sid)
            created += 1
            log(
                "info",
                "zapisano sesje %s (db id %s, phishlet %s) -> %s",
                sid[:12], s.get("id", "?"), s.get("phishlet", "?"), fpath,
            )
        except OSError as e:
            log("error", "blad zapisu notatki dla %s: %s", sid[:12], e)
    return created


def main():
    ap = argparse.ArgumentParser(
        description="Sync sesji Evilginx2 (buntdb) do Obsidiana"
    )
    ap.add_argument("--db", default=os.environ.get("EVILGINX2_DB", DEFAULT_DB))
    ap.add_argument(
        "--notes-dir",
        default=os.environ.get("OBSIDIAN_NOTES_DIR", DEFAULT_NOTES_DIR),
    )
    ap.add_argument(
        "--state",
        default=None,
        help="plik stanu (domyslnie <notes-dir>/.sync_state.json)",
    )
    ap.add_argument(
        "--logs-dir",
        default=os.environ.get("EVILGINX2_LOGS_DIR", DEFAULT_LOGS_DIR),
        help="katalog logow evilginx do tailowania (opcjonalny)",
    )
    ap.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("EVILGINX2_SYNC_INTERVAL", DEFAULT_INTERVAL)),
    )
    ap.add_argument("--once", action="store_true", help="jeden przebieg i wyjscie")
    ap.add_argument("--reset-state", action="store_true",
                    help="wyczysc stan (odtworzy notatki z data.db)")
    args = ap.parse_args()

    state_path = args.state or os.path.join(args.notes_dir, ".sync_state.json")
    if args.reset_state and os.path.exists(state_path):
        os.remove(state_path)
        log("info", "stan wyczyszczony: %s", state_path)

    processed = load_state(state_path)
    tailer = LogTailer(args.logs_dir)

    log("info", "evilginx2 -> Obsidian sync start")
    log("info", "  db        : %s", args.db)
    log("info", "  notes dir : %s", args.notes_dir)
    log("info", "  state     : %s", state_path)
    log("info", "  logs dir  : %s (%s)", args.logs_dir,
        "tail aktywny" if os.path.isdir(args.logs_dir) else "brak - pominiete")
    log("info", "  interval  : %ss", args.interval)

    def handle_signal(signum, frame):
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        while True:
            parsed = parse_db(args.db)
            changed = process_new_sessions(parsed, processed, args.notes_dir)
            if changed:
                save_state(state_path, processed)
            if args.once:
                log("info", "przebieg jednorazowy zakonczony (%d nowych)", changed)
                return 0
            time.sleep(args.interval)
            tailer.poll()  # trigger — rescan i tak nastepuje w petli
    except KeyboardInterrupt:
        log("info", "zatrzymano")
    return 0


if __name__ == "__main__":
    sys.exit(main())
