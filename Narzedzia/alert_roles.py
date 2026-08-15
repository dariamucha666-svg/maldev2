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
    raw = os.environ.get("ALERT_ROLES", ",".join(DEFAULT_ROLES))
    return {p.strip().lower() for p in raw.split(",") if p.strip()}


def chat_ids(env: dict[str, str]) -> list[int]:
    ids: list[int] = []
    for part in (env.get("ALLOWED_USER_IDS") or "").split(","):
        part = part.strip()
        if part.isdigit():
            ids.append(int(part))
    if OWNER_FILE.is_file():
        text = OWNER_FILE.read_text(encoding="utf-8").strip()
        if text.isdigit() and int(text) not in ids:
            ids.append(int(text))
    return ids


def load_state() -> dict:
    if STATE.is_file():
        try:
            data = json.loads(STATE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("hashes", {})
                return data
        except json.JSONDecodeError:
            pass
    return {"hashes": {}, "hello_sent": False}


def save_state(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE)


def digest_of(path: Path, report: dict) -> str:
    file_meta = report.get("file")
    if isinstance(file_meta, dict) and file_meta.get("sha256"):
        return str(file_meta["sha256"]).lower()
    hashes = report.get("hashes") or {}
    if hashes.get("sha256"):
        return str(hashes["sha256"]).lower()
    stem = path.stem.lower()
    return stem if len(stem) >= 16 else ""


def iter_hits(roles: set[str]) -> list[dict]:
    hits: list[dict] = []
    if not REPORTS.is_dir():
        return hits
    for path in sorted(REPORTS.glob("*.json")):
        if path.name in SKIP or ".features" in path.name or path.name.startswith("daily_"):
            continue
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(report, dict):
            continue
        cls = report.get("classification") if isinstance(report.get("classification"), dict) else {}
        role = (cls.get("role") or report.get("role") or "").lower()
        if role not in roles:
            continue
        digest = digest_of(path, report)
        if len(digest) < 16:
            continue
        hits.append(
            {
                "hash": digest,
                "role": role,
                "family": cls.get("family") or report.get("family") or "",
                "confidence": cls.get("confidence") or "",
                "source": cls.get("source") or "",
                "name": (report.get("file") or {}).get("name")
                if isinstance(report.get("file"), dict)
                else path.name,
            }
        )
    return hits


def send_telegram(token: str, chat_id: int, html: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = urllib.parse.urlencode(
        {
            "chat_id": str(chat_id),
            "text": html,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }
    ).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def format_alert(hit: dict) -> str:
    role = hit["role"].upper()
    emoji = "🐀" if hit["role"] == "rat" else "🎣"
    digest = hit["hash"]
    family = hit["family"] or "nieznana rodzina"
    extra = []
    if hit.get("confidence"):
        extra.append(f"pewność: {hit['confidence']}")
    if hit.get("source"):
        extra.append(f"źródło: {hit['source']}")
    meta = " · ".join(extra)
    link = f"{DASH}?h={digest[:12]}"
    return (
        f"{emoji} <b>Nowy {role}</b> w pipeline\n"
        f"{_esc(family)}\n"
        f"<code>{digest}</code>\n"
        f"{_esc(meta)}\n\n"
        f'<a href="{link}">Otwórz na dashboardzie</a>'
    )


def _esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def hello_text(n: int, roles: set[str]) -> str:
    watched = ", ".join(sorted(roles))
    return (
        f"🔔 Alerty <b>{_esc(watched)}</b> włączone.\n"
        f"W korpusie jest już {n} takich próbek — tych nie powtarzam.\n"
        f"Nowe trafienia z nightly / /klasyfikuj przyjdą tutaj."
    )


def main(argv: list[str]) -> int:
    args = set(argv[1:])
    dry = "--dry-run" in args
    seed = "--seed" in args
    hello = "--hello" in args
    env = load_env(ENV_FILE)
    for key, val in env.items():
        os.environ.setdefault(key, val)
    roles = alert_roles()
    token = (env.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    ids = chat_ids(env)
    state = load_state()
    hits = iter_hits(roles)
    new = [h for h in hits if h["hash"] not in state["hashes"]]

    if seed:
        for hit in hits:
            state["hashes"][hit["hash"]] = {
                "role": hit["role"],
                "family": hit["family"],
                "sent": utc_now(),
                "seed": True,
            }
        save_state(state)
        print(f"seeded {len(hits)} existing {sorted(roles)}")
        if hello and token and ids and not state.get("hello_sent"):
            text = hello_text(len(hits), roles)
            if not dry:
                for chat in ids:
                    send_telegram(token, chat, text)
                state["hello_sent"] = True
                save_state(state)
            print("hello sent" if not dry else "hello dry-run")
        return 0

    if hello and token and ids:
        text = hello_text(len(hits), roles)
        if dry:
            print("HELLO", text)
        else:
            for chat in ids:
                send_telegram(token, chat, text)
            state["hello_sent"] = True
            save_state(state)
            print("hello sent")

    print(f"watched={sorted(roles)} hits={len(hits)} new={len(new)}")
    if not new:
        return 0
    if not token or not ids:
        print("skip send: brak tokenu albo chat_id", file=sys.stderr)
        return 1
    sent = 0
    for hit in new:
        html = format_alert(hit)
        if dry:
            print("DRY", hit["role"], hit["hash"][:12], hit["family"])
            continue
        try:
            for chat in ids:
                send_telegram(token, chat, html)
            state["hashes"][hit["hash"]] = {
                "role": hit["role"],
                "family": hit["family"],
                "sent": utc_now(),
            }
            sent += 1
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"send fail {hit['hash'][:12]}: {exc}", file=sys.stderr)
    if not dry:
        save_state(state)
    print(f"sent {sent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
