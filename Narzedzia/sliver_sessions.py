#!/usr/bin/env python3
"""Read-only snapshot of Sliver sessions/beacons/jobs via the operator gRPC API.

Uses sliver-py (GetSessions / GetBeacons / GetJobs). Does not generate implants,
task sessions, dump credentials, or kill anything.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

CONFIG = Path(
    os.environ.get(
        "SLIVER_CLIENT_CONFIG",
        "/root/.sliver-client/configs/local_127.0.0.1.cfg",
    )
)
CACHE_TTL = float(os.environ.get("SLIVER_CACHE_TTL", "10"))
_LOCK = threading.Lock()
_CACHE: dict = {"ts": 0.0, "data": None}
_BG_STARTED = False


def _unix(value) -> float:
    if not value:
        return 0.0
    try:
        n = float(value)
    except (TypeError, ValueError):
        return 0.0
    if n > 1e12:
        n /= 1e9
    return n


def _iso(value) -> str:
    ts = _unix(value)
    if ts <= 0:
        return ""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ago(value) -> str:
    ts = _unix(value)
    if ts <= 0:
        return "brak"
    delta = max(0, int(time.time() - ts))
    if delta < 45:
        return "przed chwilą"
    if delta < 3600:
        return f"{delta // 60} min temu"
    if delta < 86400:
        hours = delta // 3600
        mins = (delta % 3600) // 60
        return f"{hours} godz. {mins} min temu" if mins else f"{hours} godz. temu"
    days = delta // 86400
    hours = (delta % 86400) // 3600
    return f"{days} d. {hours} godz. temu" if hours else f"{days} d. temu"


def _duration_s(value) -> float:
    try:
        n = float(value or 0)
    except (TypeError, ValueError):
        return 0.0
    if n <= 0:
        return 0.0
    return n / 1e9 if n > 1e6 else n


def _health(dead: bool, last, interval_ns: int = 0, jitter_ns: int = 0, session: bool = True) -> str:
    if dead:
        return "dead"
    ts = _unix(last)
    if ts <= 0:
        return "stale"
    age = time.time() - ts
    if session:
        return "live" if age <= 180 else "stale"
    interval = _duration_s(interval_ns) or 60.0
    jitter = _duration_s(jitter_ns)
    limit = max(180.0, 3.0 * interval + jitter)
    return "live" if age <= limit else "stale"


def _short_id(value: str) -> str:
    value = (value or "").strip()
    return value.split("-", 1)[0] if value else ""


def _session_row(obj, kind: str) -> dict:
    dead = bool(getattr(obj, "IsDead", False))
    last = getattr(obj, "LastCheckin", 0)
    interval = int(getattr(obj, "Interval", 0) or 0)
    jitter = int(getattr(obj, "Jitter", 0) or 0)
    health = _health(dead, last, interval, jitter, session=(kind == "session"))
    process = getattr(obj, "Filename", "") or ""
    return {
        "id": _short_id(getattr(obj, "ID", "")),
        "id_full": getattr(obj, "ID", "") or "",
        "name": getattr(obj, "Name", "") or "",
        "hostname": getattr(obj, "Hostname", "") or "",
        "username": getattr(obj, "Username", "") or "",
        "os": getattr(obj, "OS", "") or "",
        "arch": getattr(obj, "Arch", "") or "",
        "transport": getattr(obj, "Transport", "") or "",
        "remote": getattr(obj, "RemoteAddress", "") or "",
        "pid": int(getattr(obj, "PID", 0) or 0),
        "process": process,
        "locale": getattr(obj, "Locale", "") or "",
        "active_c2": getattr(obj, "ActiveC2", "") or "",
        "os_version": getattr(obj, "Version", "") or "",
        "first_contact": _iso(getattr(obj, "FirstContact", 0)),
        "last_checkin": _iso(last),
        "last_ts": _unix(last),
        "last_ago": _ago(last),
        "next_checkin": _iso(getattr(obj, "NextCheckin", 0)),
        "dead": dead,
        "health": health,
        "kind": kind,
    }


def _job_row(obj) -> dict:
    domains = [d for d in (getattr(obj, "Domains", None) or []) if d]
    return {
        "id": int(getattr(obj, "ID", 0) or 0),
        "name": getattr(obj, "Name", "") or "",
        "description": getattr(obj, "Description", "") or "",
        "protocol": getattr(obj, "Protocol", "") or "",
        "port": int(getattr(obj, "Port", 0) or 0),
        "domains": domains,
    }


async def _connect():
    from sliver import SliverClient, SliverClientConfig

    if not CONFIG.is_file():
        raise FileNotFoundError(f"brak operator cfg: {CONFIG}")
    client = SliverClient(SliverClientConfig.parse_config_file(str(CONFIG)))
    await client.connect()
    return client


async def _pull_with(client) -> dict:
    version = await client.version()
    sessions = [_session_row(s, "session") for s in (await client.sessions() or [])]
    beacons = [_session_row(b, "beacon") for b in (await client.beacons() or [])]
    jobs = [_job_row(j) for j in (await client.jobs() or [])]
    rank = {"live": 0, "stale": 1, "dead": 2}
    sessions.sort(key=lambda r: (rank.get(r["health"], 9), -(r.get("last_ts") or 0)))
    beacons.sort(key=lambda r: (rank.get(r["health"], 9), -(r.get("last_ts") or 0)))
    live_sessions = sum(1 for s in sessions if s["health"] == "live")
    live_beacons = sum(1 for b in beacons if b["health"] == "live")
    return {
        "ok": True,
        "source": "sliver-py",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "server": {
            "version": f"{version.Major}.{version.Minor}.{version.Patch}",
            "commit": version.Commit or "",
            "os": version.OS or "",
            "arch": version.Arch or "",
        },
        "counts": {
            "sessions": len(sessions),
            "sessions_live": live_sessions,
            "beacons": len(beacons),
            "beacons_live": live_beacons,
            "jobs": len(jobs),
        },
        "sessions": sessions,
        "beacons": beacons,
        "jobs": jobs,
    }


def _empty(error: str) -> dict:
    return {
        "ok": False,
        "source": "sliver-py",
        "error": error,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "server": {},
        "counts": {
            "sessions": 0,
            "sessions_live": 0,
            "beacons": 0,
            "beacons_live": 0,
            "jobs": 0,
        },
        "sessions": [],
        "beacons": [],
        "jobs": [],
    }


async def _pull() -> dict:
    client = await _connect()
    return await _pull_with(client)


def _store(payload: dict) -> dict:
    with _LOCK:
        _CACHE["ts"] = time.time()
        _CACHE["data"] = payload
    return payload


async def _bg_loop() -> None:
    client = None
    while True:
        try:
            if client is None:
                client = await _connect()
            _store(await _pull_with(client))
        except Exception as exc:  # noqa: BLE001
            client = None
            with _LOCK:
                if _CACHE["data"] is None:
                    _CACHE["data"] = _empty(f"{type(exc).__name__}: {exc}")
                    _CACHE["ts"] = time.time()
        await __import__("asyncio").sleep(CACHE_TTL)


def _start_bg() -> None:
    global _BG_STARTED
    with _LOCK:
        if _BG_STARTED:
            return
        _BG_STARTED = True

    def runner() -> None:
        import asyncio

        asyncio.run(_bg_loop())

    threading.Thread(target=runner, name="sliver-cache", daemon=True).start()


def fetch_snapshot() -> dict:
    import asyncio

    try:
        return asyncio.run(_pull())
    except Exception as exc:  # noqa: BLE001
        return _empty(f"{type(exc).__name__}: {exc}")


def get_snapshot() -> dict:
    _start_bg()
    with _LOCK:
        data = _CACHE["data"]
    if data is not None:
        return data
    return _store(fetch_snapshot())


def main() -> int:
    payload = fetch_snapshot()
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
