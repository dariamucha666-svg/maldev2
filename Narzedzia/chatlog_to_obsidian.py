#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chatlog_to_obsidian.py — automatyczne archiwum czatów do vaultu Obsidian.

Zbiera transkrypty TRZECH źródeł czatu i zapisuje je do Obsidiana:
  1. DSH   (DeepSeek Harness, ten Web GUI)  -> /root/.dsh/sessions/*/session-*/session.jsonl.zstd
  2. Goose (agent DeepSeek)                 -> /root/.local/share/goose/sessions/sessions.db
  3. Grok  (CLI xAI)                        -> /root/.grok/sessions/*/*/chat_history.jsonl

Co robi:
  - pełny (zredagowany) zapis każdego czatu: Dzienniki/Chaty/<Zrodlo>/<data>_<slug>.md
  - ANALIZA "co zrobiono": cel, narzędzia/komendy, pliki, hosty/IP/hashe, statystyki
  - dzienny indeks: Dzienniki/Chaty/<data>.md
  - krótki dopisek do Daily/<data>.md (jak reszta automatu)

Działa w automacie (cron). Idempotentne: eksportuje tylko sesje, które się zmieniły.
Sekrety (hasła/tokeny/klucze) są redagowane przed zapisem.

Bezpieczeństwo: NIE woła żadnego LLM — analiza jest deterministyczna (regex/liczniki).
"""
import os
import re
import sys
import json
import glob
import sqlite3
import subprocess
import hashlib
import unicodedata
from collections import Counter
from datetime import datetime, timezone

VAULT      = os.environ.get("OBSIDIAN_VAULT", "/root/obsidian-vault")
CHAT_DIR   = os.path.join(VAULT, "Dzienniki", "Chaty")
STATE_DIR  = os.environ.get("CHATLOG_STATE_DIR", "/root/.config/obsidian-chatlog")
STATE_FILE = os.path.join(STATE_DIR, "state.json")
DSH_ROOT   = os.environ.get("DSH_SESSIONS", "/root/.dsh/sessions")
GOOSE_DB   = os.environ.get("GOOSE_DB", "/root/.local/share/goose/sessions/sessions.db")
GROK_ROOT  = os.environ.get("GROK_SESSIONS", "/root/.grok/sessions")

TRUNC_TOOL  = int(os.environ.get("CHATLOG_TRUNC_TOOL", "1500"))
TRUNC_TEXT  = int(os.environ.get("CHATLOG_TRUNC_TEXT", "4000"))

_PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----", re.I)
_REDACT = [
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|client[_-]?secret|token|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|refresh[_-]?token|bot[_-]?token)\b\s*[:=]\s*\S+"),
     r"\1=<REDACTED>"),
    (re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z0-9 ]*PRIVATE KEY-----"),
     "[REDACTED PRIVATE KEY]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"), "sk-<REDACTED>"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "ghp_<REDACTED>"),
    (re.compile(r"\bgho_[A-Za-z0-9]{20,}"), "gho_<REDACTED>"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "xox-<REDACTED>"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}"), "Bearer <REDACTED>"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AKIA<REDACTED>"),
]


_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize(text):
    if not text:
        return ""
    text = str(text)
    text = _CONTROL.sub(" ", text)
    return text.encode("utf-8", "replace").decode("utf-8", "replace")


def redact(text):
    if not text:
        return ""
    text = sanitize(text)
    if _PRIVATE_KEY.search(text):
        text = _PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", text)
    for rx, repl in _REDACT:
        text = rx.sub(repl, text)
    return text


def trunc(text, limit, suffix="\n…(obcięte)"):
    if text is None:
        return ""
    text = str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + suffix


def slugify(s, maxlen=64):
    if not s:
        return "sesja"
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("._-")
    s = re.sub(r"_+", "_", s)
    return (s[:maxlen] or "sesja")


def to_iso(ts):
    if not ts:
        return None
    try:
        ts = float(ts)
    except (TypeError, ValueError):
        return None
    if ts > 1e12:
        ts /= 1000.0
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, OSError, OverflowError):
        return None


def today_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def uniq(source, sid):
    return hashlib.sha1((source + ":" + sid).encode("utf-8")).hexdigest()[:8]


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def block_text(blocks):
    out = []
    if isinstance(blocks, list):
        for b in blocks:
            if isinstance(b, dict) and b.get("type") == "text":
                out.append(b.get("text", ""))
    return "\n".join(x for x in out if x)


def _flatten(x):
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return "\n".join(_flatten(i) for i in x if _flatten(i))
    if isinstance(x, dict):
        return _flatten(x.get("text") or x.get("content") or "")
    return ""


def tool_result_text(blocks):
    parts = []
    if isinstance(blocks, list):
        for b in blocks:
            if isinstance(b, dict):
                inner = b.get("content")
                if inner is None:
                    inner = b.get("text")
                t = _flatten(inner)
                if t:
                    parts.append(t)
    return "\n".join(parts)


def dsh_sessions():
    res = []
    for f in sorted(glob.glob(os.path.join(DSH_ROOT, "*", "session-*", "session.jsonl.zstd"))):
        sid = os.path.basename(os.path.dirname(f))
        res.append((sid, f))
    return res


def dsh_events(path):
    try:
        raw = subprocess.run(["zstd", "-dc", path], capture_output=True, check=True).stdout.decode("utf-8", "replace")
    except Exception as e:
        return [], 0, None, None, "zstd: %s" % e
    events = []
    max_seq = -1
    title = None
    cwd = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        t = o.get("type")
        seq = o.get("seq", 0)
        max_seq = max(max_seq, seq)
        data = o.get("data") or {}
        if t == "session":
            cwd = o.get("cwd")
            continue
        if t == "session/title":
            title = (data.get("title") or "").strip() or title
            continue
        if t == "user/message":
            msg = data.get("message") or data
            txt = block_text(msg.get("content"))
            if txt:
                events.append({"role": "user", "ts": to_iso(o.get("time")), "text": txt})
            continue
        if t == "assistant/message":
            msg = data.get("message") or data
            txt = block_text(msg.get("content"))
            if txt:
                events.append({"role": "assistant", "ts": to_iso(o.get("time")), "text": txt})
            continue
        if t == "tool/call":
            name = data.get("name", "tool")
            args = data.get("arguments", "")
            txt = "tool: %s\n%s" % (name, trunc(args, 600)) if args else "tool: %s" % name
            events.append({"role": "tool", "ts": to_iso(o.get("time")), "text": txt, "tool": name})
            continue
        if t == "tool/code-dispatch":
            name = data.get("name", "bash")
            args = data.get("arguments") or {}
            cmd = args.get("command", "") if isinstance(args, dict) else ""
            txt = "bash: %s" % cmd if cmd else "bash: %s" % name
            events.append({"role": "tool", "ts": to_iso(o.get("time")), "text": trunc(txt, 600), "tool": name})
            continue
        if t == "tool/result":
            msg = data.get("message") or {}
            txt = tool_result_text(msg.get("content"))
            events.append({"role": "tool", "ts": to_iso(o.get("time")), "text": trunc(txt, TRUNC_TOOL), "tool": "result"})
            continue
    return events, max_seq, title, cwd, None


def goose_sessions():
    if not os.path.exists(GOOSE_DB):
        return []
    try:
        con = sqlite3.connect("file:" + GOOSE_DB + "?mode=ro", uri=True, timeout=5)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id, name, working_dir, created_at, updated_at FROM sessions ORDER BY updated_at ASC"
        ).fetchall()
        con.close()
        return rows
    except Exception as e:
        sys.stderr.write("[goose] nie mogę czytać DB: %s\n" % e)
        return []


def goose_events(sid):
    try:
        con = sqlite3.connect("file:" + GOOSE_DB + "?mode=ro", uri=True, timeout=5)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id, role, content_json, created_timestamp FROM messages WHERE session_id=? ORDER BY id ASC",
            (sid,),
        ).fetchall()
        con.close()
    except Exception as e:
        return [], 0, "sqlite: %s" % e
    events = []
    max_id = 0
    for r in rows:
        max_id = max(max_id, r["id"])
        role = r["role"]
        try:
            blocks = json.loads(r["content_json"] or "[]")
        except Exception:
            blocks = []
        if not isinstance(blocks, list):
            blocks = []
        for b in blocks:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text":
                txt = b.get("text", "")
                if txt:
                    events.append({"role": "user" if role == "user" else "assistant",
                                   "ts": to_iso(r["created_timestamp"]), "text": txt})
            elif bt == "thinking":
                continue
            elif bt == "toolRequest":
                tc = b.get("toolCall") or {}
                name = tc.get("name", "tool")
                args = tc.get("arguments") or {}
                cmd = args.get("command", "") if isinstance(args, dict) else ""
                txt = "bash: %s" % cmd if cmd else "tool: %s" % name
                events.append({"role": "tool", "ts": to_iso(r["created_timestamp"]),
                               "text": trunc(txt, 600), "tool": name})
            elif bt == "toolResponse":
                tr = b.get("toolResult") or {}
                val = tr.get("value") or tr.get("content") or tr
                txt = _tool_result_text(val)
                events.append({"role": "tool", "ts": to_iso(r["created_timestamp"]),
                               "text": trunc(txt, TRUNC_TOOL), "tool": "result"})
    return events, max_id, None


def _tool_result_text(val):
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        for k in ("text", "content", "value", "output", "result"):
            if k in val:
                v = val[k]
                if isinstance(v, str):
                    return v
                if isinstance(v, list):
                    parts = []
                    for it in v:
                        if isinstance(it, dict) and "text" in it:
                            parts.append(it["text"])
                        elif isinstance(it, str):
                            parts.append(it)
                    return "\n".join(parts)
        return json.dumps(val, ensure_ascii=False)[:TRUNC_TOOL]
    if isinstance(val, list):
        return _tool_result_text({"content": val})
    return str(val)


def grok_sessions():
    return sorted(glob.glob(os.path.join(GROK_ROOT, "*", "*", "chat_history.jsonl")))


def grok_events(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except Exception as e:
        return [], 0, None, "read: %s" % e
    events = []
    title = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        t = o.get("type")
        if t == "system":
            continue
        if t == "user":
            c = o.get("content")
            if isinstance(c, str) and c.strip():
                events.append({"role": "user", "ts": None, "text": c})
                if title is None:
                    title = c.strip().splitlines()[0][:80]
            continue
        if t == "reasoning":
            continue
        if t == "assistant":
            c = o.get("content")
            if isinstance(c, str) and c.strip():
                events.append({"role": "assistant", "ts": None, "text": c})
            for tc in o.get("tool_calls") or []:
                name = tc.get("name", "tool")
                args = tc.get("arguments", "")
                txt = "tool: %s\n%s" % (name, trunc(args, 600)) if args else "tool: %s" % name
                events.append({"role": "tool", "ts": None, "text": txt, "tool": name})
            continue
        if t == "tool_result":
            c = o.get("content")
            if isinstance(c, str) and c.strip():
                events.append({"role": "tool", "ts": None, "text": trunc(c, TRUNC_TOOL), "tool": "result"})
            continue
        if t == "backend_tool_call":
            name = o.get("name") or o.get("tool_name", "tool")
            events.append({"role": "tool", "ts": None, "text": "tool: %s" % name, "tool": name})
            continue
    return events, len(lines), title, None


FILE_RE = re.compile(r"(?:^|[\s'\"(])(/(?:root|home|etc|opt|usr|var|srv)/[A-Za-z0-9_./@-]+)")
MD_RE   = re.compile(r"\b[A-Za-z0-9_/-]+\.md\b")
IP_RE   = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HOST_RE = re.compile(r"\b[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.(?:eu|com|org|net|io|cyou|host|portmap|workers\.dev|app|gg)\b", re.I)
HASH_RE = re.compile(r"\b[a-f0-9]{32}\b|\b[a-f0-9]{40}\b|\b[a-f0-9]{64}\b", re.I)
PRIVATE_IP = re.compile(r"\b(?:10|127|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")


def analyze(events):
    goal = ""
    for e in events:
        if e["role"] == "user":
            goal = sanitize(e["text"].strip().splitlines()[0][:200])
            break
    counters = Counter(e["role"] for e in events)
    tools = Counter()
    files = set()
    hosts = set()
    ips = set()
    hashes = set()
    for e in events:
        txt = e.get("text", "") or ""
        if e.get("tool"):
            tools[e["tool"]] += 1
        for m in FILE_RE.findall(txt):
            files.add(m)
        for m in MD_RE.findall(txt):
            files.add(m)
        for m in HOST_RE.findall(txt):
            hosts.add(m.lower())
        for m in IP_RE.findall(txt):
            if PRIVATE_IP.search(m):
                continue
            ips.add(m)
        for m in HASH_RE.findall(txt):
            hashes.add(m.lower())
    return {
        "goal": goal,
        "n_user": counters.get("user", 0),
        "n_assistant": counters.get("assistant", 0),
        "n_tool": counters.get("tool", 0),
        "tools": tools,
        "files": sorted(files)[:40],
        "hosts": sorted(hosts)[:20],
        "ips": sorted(ips)[:20],
        "hashes": sorted(hashes)[:20],
    }


def _last_assistant_text(events):
    for e in reversed(events):
        if e["role"] == "assistant":
            return sanitize(e["text"].strip())
    return ""


ROLE_ICON = {"user": "👤", "assistant": "🤖", "tool": "🛠️"}
ROLE_NAME = {"user": "Użytkownik", "assistant": "Asystent", "tool": "Akcja/narzędzie"}


def render_session(source, sid, title, cwd, day, events):
    a = analyze(events)
    heading = sanitize(title or sid)
    last = trunc(_last_assistant_text(events), TRUNC_TEXT)
    lines = []
    lines.append("---")
    lines.append('title: "' + heading.replace('"', "") + '"')
    lines.append("date: " + day)
    lines.append("tags: [chatlog, czat, " + source.lower() + "]")
    lines.append("source: " + source)
    lines.append("session: " + sid)
    if cwd:
        lines.append('cwd: "' + cwd + '"')
    lines.append("messages: " + str(len(events)))
    lines.append("tool_calls: " + str(a["n_tool"]))
    lines.append("status: archived")
    lines.append("---")
    lines.append("")
    lines.append("# " + heading)
    lines.append("")
    lines.append("> Zapis czatu **" + source + "** · sesja '" + sid + "'" + (" · '" + cwd + "'" if cwd else "") + " · wygenerowano " + today_utc())
    lines.append("")
    lines.append("## Analiza")
    lines.append("")
    lines.append("| Pole | Wartość |")
    lines.append("|------|---------|")
    if a["goal"]:
        lines.append("| Cel | " + a["goal"] + " |")
    lines.append("| Wiadomości użytkownika | " + str(a["n_user"]) + " |")
    lines.append("| Odpowiedzi asystenta | " + str(a["n_assistant"]) + " |")
    lines.append("| Akcji narzędziowych | " + str(a["n_tool"]) + " |")
    if a["tools"]:
        lines.append("| Narzędzia | " + ", ".join("'" + k + "'×" + str(v) for k, v in a["tools"].most_common(12)) + " |")
    if a["files"]:
        lines.append("| Pliki | " + " · ".join("'" + f + "'" for f in a["files"][:20]) + " |")
    if a["ips"]:
        lines.append("| IP | " + " · ".join("'" + x + "'" for x in a["ips"][:12]) + " |")
    if a["hosts"]:
        lines.append("| Hosty | " + " · ".join("'" + x + "'" for x in a["hosts"][:12]) + " |")
    if a["hashes"]:
        lines.append("| Hashe | " + " · ".join("'" + x[:12] + "…'" for x in a["hashes"][:12]) + " |")
    lines.append("")
    if last:
        lines.append("## Wniosek (ostatnia odpowiedź asystenta)")
        lines.append("")
        lines.append(last)
        lines.append("")
    lines.append("## Pełny zapis")
    lines.append("")
    for e in events:
        icon = ROLE_ICON.get(e["role"], "•")
        name = ROLE_NAME.get(e["role"], e["role"])
        ts = e.get("ts") or ""
        lines.append("### " + icon + " " + name + (" — " + ts if ts else ""))
        lines.append("")
        lines.append(redact(trunc(e.get("text", ""), TRUNC_TEXT)))
        lines.append("")
    return "\n".join(lines)


def write_if_changed(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == content:
                return False
    except Exception:
        pass
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)
    return True


def _file_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if lines and lines[0].strip() == "---":
            for ln in lines[1:]:
                if ln.strip() == "---":
                    break
                if ln.startswith("title:"):
                    t = ln[len("title:"):].strip()
                    return t.strip('"').strip("'")
    except Exception:
        pass
    return os.path.basename(path)


def render_index(source_files):
    by_day = {}
    for source, path, title, day in source_files:
        by_day.setdefault(day, []).append((source, title, os.path.relpath(path, CHAT_DIR)))
    for day, items in by_day.items():
        items.sort(key=lambda x: (x[0], x[1]))
        lines = []
        lines.append("---")
        lines.append("date: " + day)
        lines.append("tags: [chatlog, czat, index]")
        lines.append("---")
        lines.append("")
        lines.append("# Czaty — " + day)
        lines.append("")
        lines.append("Automatyczny indeks sesji czatu zapisanych w Obsidianie.")
        lines.append("")
        lines.append("| Źródło | Sesja |")
        lines.append("|--------|-------|")
        for source, title, rel in items:
            safe = title.replace("|", " ").replace("[", "").replace("]", "").replace("#", "")
            lines.append("| " + source + " | [[" + rel.replace(".md", "") + "|" + safe + "]] |")
        lines.append("")
        write_if_changed(os.path.join(CHAT_DIR, day + ".md"), "\n".join(lines))


def main():
    state = load_state()
    os.makedirs(CHAT_DIR, exist_ok=True)
    day = today_utc()
    changed = []
    daily_new = []

    for sid, path in dsh_sessions():
        events, max_seq, title, cwd, err = dsh_events(path)
        if err:
            sys.stderr.write("[dsh:%s] %s\n" % (sid, err))
            continue
        key = "dsh:" + sid
        prev = state.get(key, {}).get("seq", -1)
        if max_seq <= prev:
            continue
        source = "DSH"
        title = title or sid
        out = os.path.join(CHAT_DIR, source, day + "_" + slugify(title) + "-" + uniq(source, sid) + ".md")
        content = render_session(source, sid, title, cwd, day, events)
        if write_if_changed(out, content):
            changed.append((source, out, title, day))
        state[key] = {"seq": max_seq, "title": title}
        daily_new.append((source, out, title))

    for row in goose_sessions():
        sid = row["id"]
        events, max_id, err = goose_events(sid)
        if err:
            sys.stderr.write("[goose:%s] %s\n" % (sid, err))
            continue
        key = "goose:" + sid
        prev = state.get(key, {}).get("id", -1)
        if max_id <= prev:
            continue
        source = "Goose"
        title = (row["name"] or sid).strip()
        out = os.path.join(CHAT_DIR, source, day + "_" + slugify(title) + "-" + uniq(source, sid) + ".md")
        content = render_session(source, sid, title, row["working_dir"], day, events)
        if write_if_changed(out, content):
            changed.append((source, out, title, day))
        state[key] = {"id": max_id, "title": title}
        daily_new.append((source, out, title))

    for path in grok_sessions():
        events, nlines, title, err = grok_events(path)
        if err:
            sys.stderr.write("[grok:%s] %s\n" % (path, err))
            continue
        key = "grok:" + path
        prev = state.get(key, {}).get("lines", -1)
        if nlines <= prev:
            continue
        sid = os.path.basename(os.path.dirname(path))
        source = "Grok"
        title = title or sid
        out = os.path.join(CHAT_DIR, source, day + "_" + slugify(title) + "-" + uniq(source, sid) + ".md")
        content = render_session(source, sid, title, None, day, events)
        if write_if_changed(out, content):
            changed.append((source, out, title, day))
        state[key] = {"lines": nlines, "title": title}
        daily_new.append((source, out, title))

    save_state(state)

    all_files = []
    for f in sorted(glob.glob(os.path.join(CHAT_DIR, "*", "*.md"))):
        source = os.path.basename(os.path.dirname(f))
        base = os.path.basename(f)
        m = re.match(r"(\d{4}-\d{2}-\d{2})_", base)
        if not m:
            continue
        fday = m.group(1)
        all_files.append((source, f, _file_title(f), fday))
    render_index(all_files)

    appended = state.setdefault("daily_appended", {})
    lines = []
    for source, out, title in daily_new:
        stamp = "chatlog:" + source + ":" + os.path.basename(out)
        bucket = appended.setdefault(day, [])
        if stamp in bucket:
            continue
        rel = os.path.relpath(out, VAULT)
        lines.append("- [" + source + "] [[" + rel.replace(".md", "") + "|" + title + "]]")
        bucket.append(stamp)
    if lines:
        save_state(state)
        daily_file = os.path.join(VAULT, "Daily", day + ".md")
        os.makedirs(os.path.dirname(daily_file), exist_ok=True)
        if not os.path.exists(daily_file):
            with open(daily_file, "w", encoding="utf-8") as f:
                f.write("---\ndate: " + day + "\ntags: [daily]\n---\n\n# " + day + "\n")
        block = "\n## Czaty (auto)\n\n" + "\n".join(lines) + "\n"
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write(block)

    print("[chatlog] %s — nowych/zmienionych sesji: %d" % (today_utc(), len(changed)))
    for source, out, title, d in changed:
        print("  + %s: %s" % (source, os.path.relpath(out, VAULT)))


if __name__ == "__main__":
    main()
