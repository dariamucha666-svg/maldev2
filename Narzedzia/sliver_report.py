#!/usr/bin/env python3
"""sliver_report.py — generator raportu engagement ze Slivera.

Parsuje sesje/beacony (sliver-py + SQLite /root/.sliver/sliver.db), log
operacji operatora (audit.json) i log operacji sliver_ops.py (ops.jsonl),
a następnie generuje raport:
  - timeline działań,
  - artefakty (lokalne + zdalne),
  - co zostało na hostach (sprzątanie / OPSEC),
  - checklist sprzątania,
oraz wpis w Daily/.

Użycie:
  sliver_report.py                              # raport z dziś, auto-nazwa
  sliver_report.py --engagement kerberoast-01   # własna nazwa engagementu
  sliver_report.py --offline                    # tylko db+audit+ops (bez gRPC)
  sliver_report.py --json                       # surowy zbiór danych
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

VAULT_CANDIDATES = [
    os.environ.get("OBSIDIAN_VAULT", ""),
    "/root/obsidian-vault",
    "/root/Obsidian/XMask/maldev2",
]
SLIVER_DB = os.environ.get("SLIVER_DB", "/root/.sliver/sliver.db")
SLIVER_AUDIT = os.environ.get("SLIVER_AUDIT_LOG", "/root/.sliver/logs/audit.json")


def find_vault() -> Path:
    for cand in VAULT_CANDIDATES:
        if cand and Path(cand).is_dir():
            return Path(cand)
    return Path.cwd()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _iso(ts) -> str:
    if not ts:
        return ""
    try:
        n = float(ts)
    except (TypeError, ValueError):
        return str(ts)
    if n > 1e12:
        n /= 1e9
    if n <= 0:
        return ""
    return datetime.fromtimestamp(n, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ago(ts) -> str:
    if not ts:
        return "—"
    try:
        n = float(ts)
    except (TypeError, ValueError):
        return "—"
    if n > 1e12:
        n /= 1e9
    delta = max(0, int(datetime.now(timezone.utc).timestamp() - n))
    if delta < 3600:
        return f"{delta // 60} min"
    if delta < 86400:
        return f"{delta // 3600} h"
    return f"{delta // 86400} d"


# ---------------------------------------------------------------- sources

def load_db_data(db_path: Path) -> dict:
    if not db_path.is_file():
        return {"error": f"brak db: {db_path}"}
    out = {}
    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=3)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        def rows(table, order="1"):
            try:
                return [dict(r) for r in cur.execute(
                    f"SELECT * FROM {table} ORDER BY {order}")]
            except sqlite3.Error as exc:
                return [{"_err": str(exc)}]

        out["beacons"] = rows("beacons", "created_at")
        out["hosts"] = rows("hosts", "created_at DESC")
        out["beacon_tasks"] = rows("beacon_tasks", "created_at")
        out["iocs"] = rows("iocs", "created_at DESC")
        out["loots"] = rows("loots", "created_at DESC")
        out["extension_data"] = rows("extension_data", "created_at DESC")
        out["listener_jobs"] = rows("listener_jobs", "created_at DESC")
        out["http_listeners"] = rows("http_listeners")
        out["builds"] = rows("implant_builds", "created_at DESC")
        out["configs"] = rows("implant_configs", "created_at DESC")
        out["c2s"] = rows("implant_c2", "priority")
        out["profiles"] = rows("implant_profiles", "created_at DESC")
        con.close()
    except sqlite3.Error as exc:
        out["error"] = str(exc)
    return out


_NOISE_METHODS = (
    "GetVersion", "GetSessions", "GetBeacons", "GetJobs", "ImplantProfiles",
    "ImplantBuilds", "GetOperators", "GetCanaries", "GetWebsites", "GetLoots",
    "GetCredentials", "GetHosts", "GetDnsCanaries", "GetMonitoringProviders",
    "GetCrackFiles", "GetCrackJobs", "GetBenchmarks", "GetPortfwd",
    "GetExtensionData", "GetIOCs", "GetBeaconTasks",
)


def _is_action_method(method: str) -> bool:
    if not method:
        return False
    name = method.rsplit("/", 1)[-1]
    if name in _NOISE_METHODS:
        return False
    return True


def load_audit(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    events = []
    seen = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = ""
        try:
            inner = json.loads(e.get("msg") or "{}")
            method = inner.get("method", "")
            req = inner.get("request", "")
        except json.JSONDecodeError:
            req = ""
        if not _is_action_method(method):
            continue
        key = (e.get("time", ""), method)
        if key in seen:
            continue
        seen.add(key)
        events.append({
            "ts": e.get("time", ""), "src": "audit",
            "event": f"operator: {method}", "detail": req or "",
            "user": e.get("user", ""), "remote": e.get("remote_ip", ""),
        })
    return events


def load_opslog(vault: Path) -> list[dict]:
    p = vault / "Logs" / "sliver_ops" / "ops.jsonl"
    if not p.is_file():
        return []
    events = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        op = e.get("op", "")
        target = e.get("target", "")
        target_txt = f" → {target}" if target else ""
        events.append({
            "ts": e.get("ts", ""), "src": "sliver-ops",
            "event": f"{op}{target_txt}", "detail": e.get("note", ""),
            "op": op, "target": target, "detail_full": e.get("detail", {}),
            "user": "", "remote": "",
        })
    return events


async def load_live(vault: Path, offline: bool) -> dict:
    if offline:
        return {"error": "offline"}
    try:
        from sliver import SliverClient, SliverClientConfig
    except ImportError:
        return {"error": "brak sliver-py"}
    cfg_candidates = [
        os.environ.get("SLIVER_CLIENT_CONFIG", ""),
        "/root/.sliver-client/configs/root_127.0.0.1.cfg",
        "/root/.sliver-client/configs/local_127.0.0.1.cfg",
    ]
    cfg_path = next((c for c in cfg_candidates if c and Path(c).is_file()), None)
    if not cfg_path:
        return {"error": "brak operator cfg"}
    import asyncio

    try:
        client = SliverClient(SliverClientConfig.parse_config_file(cfg_path))
        await client.connect()
        v = await client.version()
        sessions = await client.sessions() or []
        beacons = await client.beacons() or []
        jobs = await client.jobs() or []
        out = {
            "version": f"{v.Major}.{v.Minor}.{v.Patch} ({v.Commit}) {v.OS}/{v.Arch}",
            "sessions": [{
                "id": s.ID, "name": s.Name, "hostname": s.Hostname,
                "username": s.Username, "os": s.OS, "arch": s.Arch,
                "transport": s.Transport, "remote": s.RemoteAddress,
                "pid": s.PID, "process": s.Filename,
                "first_contact": _iso(s.FirstContact), "last_checkin": _iso(s.LastCheckin),
                "last_ts": s.LastCheckin, "dead": s.IsDead,
            } for s in sessions],
            "beacons": [{
                "id": b.ID, "name": b.Name, "hostname": b.Hostname,
                "username": b.Username, "os": b.OS, "arch": b.Arch,
                "transport": b.Transport, "remote": b.RemoteAddress,
                "pid": b.PID, "process": b.Filename,
                "first_contact": _iso(b.FirstContact), "last_checkin": _iso(b.LastCheckin),
                "last_ts": b.LastCheckin, "dead": b.IsDead,
                "interval_s": (b.Interval or 0) / 1e9, "jitter_s": (b.Jitter or 0) / 1e9,
            } for b in beacons],
            "jobs": [{"id": j.ID, "name": j.Name, "protocol": j.Protocol,
                      "port": j.Port} for j in jobs],
        }
        await client._channel.close()
        return out
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


# ---------------------------------------------------------------- raport

def _fmt_list(items) -> str:
    return ", ".join(str(i) for i in items) if items else "—"


def _mk_timeline(db: dict, audit: list[dict], ops: list[dict], live: dict) -> list[dict]:
    tl: list[dict] = []
    for e in audit:
        tl.append({"ts": e["ts"], "src": "audit", "event": e["event"],
                   "detail": e.get("detail", "")[:120]})
    for e in ops:
        tl.append({"ts": e["ts"], "src": "sliver-ops", "event": e["event"],
                   "detail": e.get("detail", "")[:120]})
    for b in db.get("beacons", []) or []:
        if b.get("_err"):
            continue
        if b.get("created_at"):
            tl.append({"ts": str(b["created_at"]), "src": "beacon",
                       "event": f"beacon {b.get('name','')} rejestracja",
                       "detail": f"{b.get('hostname','')} {b.get('os','')}/{b.get('arch','')}"})
        if b.get("last_checkin"):
            tl.append({"ts": str(b["last_checkin"]), "src": "beacon",
                       "event": f"beacon {b.get('name','')} ostatni check-in",
                       "detail": f"transport {b.get('transport','')}"})
    for t in db.get("beacon_tasks", []) or []:
        if t.get("_err"):
            continue
        tl.append({"ts": str(t.get("created_at", "")), "src": "beacon-task",
                   "event": f"task {t.get('description','')} [{t.get('state','')}]",
                   "detail": ""})
    tl.sort(key=lambda e: e["ts"] or "")
    return tl


def _artifacts_from_ops(ops: list[dict]) -> list[dict]:
    arts = []
    for e in ops:
        op = e.get("op", "")
        d = e.get("detail_full") or e.get("detail") or {}
        if op in ("generate", "regenerate") and d.get("path"):
            arts.append({"file": d["path"], "size": d.get("size", "?"),
                         "type": "implant", "src": "sliver-ops", "sha": d.get("sha256", "")})
        elif op == "task-screenshot" and d.get("path"):
            arts.append({"file": d["path"], "size": d.get("size", "?"),
                         "type": "screenshot", "src": "sliver-ops", "sha": d.get("sha256", "")})
        elif op == "task-keylog" and d.get("path"):
            arts.append({"file": d["path"], "size": d.get("size", "?"),
                         "type": "keylog", "src": "sliver-ops", "sha": d.get("sha256", "")})
        elif op == "task-download" and d.get("path"):
            arts.append({"file": d["path"], "size": d.get("size", "?"),
                         "type": "download", "src": "sliver-ops", "sha": d.get("sha256", "")})
    return arts


def _hosts_leftover(db: dict, live: dict, ops: list[dict]) -> list[dict]:
    """Co zostało na hostach — per host."""
    hosts: dict[str, dict] = {}
    for b in db.get("beacons", []) or []:
        if b.get("_err"):
            continue
        h = hosts.setdefault(b.get("hostname") or "?", {"implant": [], "tasks": [], "persist": []})
        h["implant"].append(f"{b.get('filename') or '?'} (pid {b.get('p_id') or '?'}, "
                            f"{b.get('os','')}/{b.get('arch','')}, {b.get('transport','')})")
    for s in live.get("sessions", []) or []:
        h = hosts.setdefault(s.get("hostname") or "?", {"implant": [], "tasks": [], "persist": []})
        h["implant"].append(f"{s.get('process') or '?'} (pid {s.get('pid') or '?'}, session {s.get('name')})")
    for b in live.get("beacons", []) or []:
        h = hosts.setdefault(b.get("hostname") or "?", {"implant": [], "tasks": [], "persist": []})
        h["implant"].append(f"{b.get('process') or '?'} (pid {b.get('pid') or '?'}, beacon {b.get('name')})")
    for ioc in db.get("iocs", []) or []:
        if ioc.get("_err"):
            continue
        host = next((x.get("hostname", "?") for x in db.get("hosts", []) or []
                     if str(x.get("id")) == str(ioc.get("host_id"))), "?")
        h = hosts.setdefault(host, {"implant": [], "tasks": [], "persist": []})
        h["tasks"].append(f"IOC: {ioc.get('path')} (sha {ioc.get('file_hash') or '—'})")
    for e in ops:
        op, d = e.get("op", ""), e.get("detail_full") or e.get("detail") or {}
        if op == "task-keylog" and d.get("source"):
            h = hosts.setdefault(e.get("target") or "?", {"implant": [], "tasks": [], "persist": []})
            h["tasks"].append(f"keylog: {d['source']}")
        if op == "task-upload" and d.get("remote"):
            h = hosts.setdefault(e.get("target") or "?", {"implant": [], "tasks": [], "persist": []})
            h["tasks"].append(f"upload: {d['remote']}")
        if op == "task-exec":
            cmd = d.get("cmd", "")
            if any(k in cmd.lower() for k in ("reg ", "schtasks", "sc ", "net user", "wmic")):
                h = hosts.setdefault(e.get("target") or "?", {"implant": [], "tasks": [], "persist": []})
                h["persist"].append(f"exec: {cmd} (potencjalna persistencja)")
    return [{"host": h, **v} for h, v in hosts.items()]


def _cleanup_steps(hosts_left: list[dict], live: dict, db: dict) -> list[str]:
    steps = []
    targets = [f"{s.get('name','')} ({s.get('id','')[:8]})" for s in live.get("sessions", []) or []]
    targets += [f"{b.get('name','')} ({b.get('id','')[:8]})" for b in live.get("beacons", []) or []]
    if targets:
        steps.append("Kill aktywne obiekty: `sliver_ops.py kill <ID> --yes` — " + "; ".join(targets))
    for h in hosts_left:
        for impl in h.get("implant", []):
            steps.append(f"Usuń plik implantu na `{h['host']}`: {impl}")
        for t in h.get("tasks", []):
            steps.append(f"Usuń artefakt zdalny na `{h['host']}`: {t}")
        for p in h.get("persist", []):
            steps.append(f"Zweryfikuj/usun persistencję na `{h['host']}`: {p}")
    for j in db.get("listener_jobs", []) or []:
        if not j.get("_err"):
            steps.append(f"Zatrzymaj listener job {j.get('job_id')} ({j.get('type')}): "
                         f"`sliver_ops.py jobs-kill {j.get('job_id')} --yes`")
    steps.append("Zarchiwizuj lokalne artefakty i wyczyść `Logs/sliver_ops/artifacts/`.")
    steps.append("Obróć C2: nowe profile/listenery po sprzątnięciu (patrz [[Sliver_C2]]).")
    return steps


def write_report(vault: Path, name: str, live: dict, db: dict,
                 audit: list[dict], ops: list[dict]) -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stamp = now_iso()
    out_dir = vault / "raports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{day}_{name or 'sliver'}_engagement.md"

    timeline = _mk_timeline(db, audit, ops, live)
    arts = _artifacts_from_ops(ops)
    hosts_left = _hosts_leftover(db, live, ops)
    cleanup = _cleanup_steps(hosts_left, live, db)

    L = []
    L += ["---", f'title: "Raport engagement Sliver — {name or "bez nazwy"}"',
          f"date: {day}", "type: raport",
          "tags: [lab, sliver, c2, engagement, raport, opsec]",
          "status: completed", "---", "",
          f"# Raport engagement — {name or 'bez nazwy'}", "",
          f"Wygenerowane: `{stamp}` przez `Narzedzia/sliver_report.py`.", ""]

    L += ["## Środowisko", ""]
    ver = live.get("version", "—") if live else "—"
    live_err = (live or {}).get("error", "")
    L += [f"| Pole | Wartość |", "|------|---------|",
          f"| Sliver server | {ver} |",
          f"| Źródła | sliver-py{' (offline: ' + live_err + ')' if live_err else ''} + SQLite + audit.json + ops.jsonl |",
          f"| Engagement | {name or '—'} |", ""]

    L += ["## Timeline działań", ""]
    if timeline:
        L += ["| Czas | Źródło | Zdarzenie | Detal |", "|------|--------|-----------|-------|"]
        for e in timeline[-40:]:
            L += [f"| {e['ts']} | {e['src']} | {e['event']} | {e.get('detail','')} |"]
    else:
        L += ["Brak zdarzeń w logach."]
    L += [""]

    L += ["## Sesje / Beacony (stan live)", ""]
    beacons = (live or {}).get("beacons", []) or []
    sessions = (live or {}).get("sessions", []) or []
    if beacons or sessions:
        L += ["| Typ | Name | Host | User | OS/Arch | Transport | Proces (PID) | Ostatni check-in |", 
              "|-----|------|------|------|---------|-----------|---------------|------------------|"]
        for b in beacons:
            L += [f"| beacon | {b['name']} | {b['hostname']} | {b['username']} | {b['os']}/{b['arch']} "
                  f"| {b['transport']} | {b['process']} ({b['pid']}) | {b['last_checkin']} |"]
        for s in sessions:
            L += [f"| session | {s['name']} | {s['hostname']} | {s['username']} | {s['os']}/{s['arch']} "
                  f"| {s['transport']} | {s['process']} ({s['pid']}) | {s['last_checkin']} |"]
    else:
        L += ["Brak aktywnych sesji/beaconów (live)."]
    L += [""]

    L += ["## Artefakty", ""]
    if arts:
        L += ["| Plik | Rozmiar | Typ | Źródło | SHA256 |", "|------|---------|-----|--------|--------|"]
        for a in arts:
            L += [f"| `{a['file']}` | {a['size']} | {a['type']} | {a['src']} | {a.get('sha','')[:16]}… |"]
    else:
        L += ["Brak artefaktów w ops.jsonl."]
    L += [""]

    L += ["## Co zostało na hostach (sprzątanie / OPSEC)", ""]
    if hosts_left:
        for h in hosts_left:
            L += [f"### `{h['host']}`", ""]
            if h.get("implant"):
                L += ["- Implanty/beacony:"] + [f"  - {i}" for i in h["implant"]]
            if h.get("tasks"):
                L += ["- Artefakty zdalne:"] + [f"  - {t}" for t in h["tasks"]]
            if h.get("persist"):
                L += ["- Potencjalna persistencja:"] + [f"  - {p}" for p in h["persist"]]
            L += [""]
    else:
        L += ["Brak danych o hostach (db pusta)."]
    L += [""]

    L += ["## Checklist sprzątania", ""]
    for c in cleanup:
        L += [f"- [ ] {c}"]
    L += ["", "## Linki", "",
          "- [[Sliver_C2]] · [[Infrastruktura_C2]] · [[sessions]] · [[Detekcja]] · [[Playbook_AD]]"]

    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Raport engagement ze Slivera")
    ap.add_argument("--vault", default="")
    ap.add_argument("--engagement", default="", help="nazwa engagementu (np. kerberoast-01)")
    ap.add_argument("--offline", action="store_true", help="bez gRPC (db+audit+ops)")
    ap.add_argument("--no-daily", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    vault = Path(args.vault) if args.vault else find_vault()
    import asyncio

    live = asyncio.run(load_live(vault, args.offline))
    db = load_db_data(Path(SLIVER_DB))
    audit = load_audit(Path(SLIVER_AUDIT))
    ops = load_opslog(vault)

    if args.json:
        print(json.dumps({"live": live, "db_summary": {
            "beacons": len(db.get("beacons", []) or []),
            "hosts": len(db.get("hosts", []) or []),
            "beacon_tasks": len(db.get("beacon_tasks", []) or []),
            "iocs": len(db.get("iocs", []) or []),
            "builds": [b.get("name") for b in db.get("builds", []) or []],
            "listener_jobs": db.get("listener_jobs", []) or [],
        }, "audit_events": len(audit), "ops_events": len(ops)},
            ensure_ascii=False, indent=2))
        return 0

    name = args.engagement or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report = write_report(vault, name, live, db, audit, ops)

    if not args.no_daily:
        n_beacons = len((live or {}).get("beacons", []) or [])
        n_sessions = len((live or {}).get("sessions", []) or [])
        body = (f"Raport: [[{report.stem}]] · beacony live: {n_beacons} · sesje live: {n_sessions} · "
                f"zdarzenia timeline: {len(audit) + len(ops)} · artefakty: "
                f"{len(ops)} op w ops.jsonl.")
        if (live or {}).get("error"):
            body += f"\nUwaga: live niedostępne ({live['error']})."
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        target = vault / "Daily" / f"{day}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(f"---\ndate: {day}\ntags: [daily]\n---\n\n# {day}\n\n",
                              encoding="utf-8")
        stamp = now_iso()
        with target.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## Raport engagement Sliver — {name} ({stamp})\n\n{body}\n\n")

    print(f"raport: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
