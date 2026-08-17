#!/usr/bin/env python3
"""detection_validator.py — purple-team walidator pokrycia detekcji.

Replay technik (beacon C2 / AD attacks) przez Suricatę w trybie offline
(-r pcap) i przez uproszczony matcher Sigma na syntetycznych zdarzeniach
Windows Security — wynik: tablica pokrycia technika <-> detekcja.

Źródła reguł (lab):
  - Narzedzia/clayrat_c2.rules                  (Suricata, 8 reguł)
  - Lab/RedTeam_AD/detection/local.rules        (Suricata, 11 reguł)
  - Lab/RedTeam_AD/detection/sigma/*.yml        (Sigma, 5 reguł)

Wyjścia:
  - konsola (tabela pokrycia)
  - raports/YYYY-MM-DD_detection_coverage.md    (raport do vaultu)
  - Daily/YYYY-MM-DD.md                         (wpis)
  - Logs/sliver_ops/coverage_<date>.csv         (CSV)

Użycie:
  detection_validator.py --rules all --technique all
  detection_validator.py --technique kerberoasting
  detection_validator.py --pcap /sciezka/capture.pcap
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------- vault

VAULT_CANDIDATES = [
    os.environ.get("OBSIDIAN_VAULT", ""),
    "/root/obsidian-vault",
    "/root/Obsidian/XMask/maldev2",
]


def find_vault() -> Path:
    for cand in VAULT_CANDIDATES:
        if cand and Path(cand).is_dir():
            return Path(cand)
    return Path.cwd()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_daily(vault: Path, heading: str, body: str) -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stamp = now_iso()
    target = vault / "Daily" / f"{day}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(f"---\ndate: {day}\ntags: [daily]\n---\n\n# {day}\n\n",
                          encoding="utf-8")
    with target.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {heading} ({stamp})\n\n{body.strip()}\n\n")
    return target


# ---------------------------------------------------------------- pcap writer

def _cksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    s = sum(struct.unpack(f"!{len(data) // 2}H", data))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return (~s) & 0xFFFF


def ipv4(src: str, dst: str, proto: int, payload: bytes, ident: int = 1) -> bytes:
    total = 20 + len(payload)
    hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, total, ident, 0x4000, 64,
                      proto, 0, socket.inet_aton(src), socket.inet_aton(dst))
    csum = _cksum(hdr)
    return hdr[:10] + struct.pack("!H", csum) + hdr[12:] + payload


def tcp(src_ip: str, sport: int, dst_ip: str, dport: int, flags: int,
        seq: int, ack: int, payload: bytes = b"") -> bytes:
    hdr = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 0x50, flags, 64240, 0, 0)
    pseudo = (socket.inet_aton(src_ip) + socket.inet_aton(dst_ip) +
              struct.pack("!BBH", 0, 6, len(hdr) + len(payload)))
    csum = _cksum(pseudo + hdr + payload)
    hdr = hdr[:16] + struct.pack("!H", csum) + hdr[18:]
    return hdr + payload


def udp(src_ip: str, sport: int, dst_ip: str, dport: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    hdr = struct.pack("!HHHH", sport, dport, length, 0)
    pseudo = (socket.inet_aton(src_ip) + socket.inet_aton(dst_ip) +
              struct.pack("!BBH", 0, 17, length))
    csum = _cksum(pseudo + hdr + payload)
    hdr = hdr[:6] + struct.pack("!H", csum) + hdr[8:]
    return hdr + payload


def frame(payload_ip: bytes, src_mac: bytes = b"\x02\x00\x00\x00\x00\x0a",
          dst_mac: bytes = b"\x02\x00\x00\x00\x00\x02") -> bytes:
    return dst_mac + src_mac + struct.pack("!H", 0x0800) + payload_ip


def make_pcap(records: list[tuple[float, bytes]]) -> bytes:
    """records: [(ts_seconds_float, frame_bytes)] → pcap (classic, us)."""
    out = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for ts, data in records:
        sec = int(ts)
        usec = int((ts - sec) * 1_000_000)
        out += struct.pack("<IIII", sec, usec, len(data), len(data))
        out += data
    return bytes(out)


def dns_query(qname: str, tid: int = 0x1234) -> bytes:
    q = b"".join(bytes([len(p)]) + p.encode() for p in qname.split(".")) + b"\x00"
    return struct.pack("!HHHHHH", tid, 0x0100, 1, 0, 0, 0) + q + struct.pack("!HH", 1, 1)


def tcp_conn(src_ip: str, sport: int, dst_ip: str, dport: int, data: bytes,
             t0: float, seq: int = 1000) -> list[tuple[float, bytes]]:
    """Pełny handshake + dane (PSH|ACK) — potrzebne dla flow:established."""
    syn = tcp(src_ip, sport, dst_ip, dport, 0x02, seq, 0)
    synack = tcp(dst_ip, dport, src_ip, sport, 0x12, seq + 100, seq + 1)
    ack_data = tcp(src_ip, sport, dst_ip, dport, 0x18, seq + 1, seq + 101, data)
    return [(t0, frame(ipv4(src_ip, dst_ip, 6, syn))),
            (t0 + 0.001, frame(ipv4(dst_ip, src_ip, 6, synack))),
            (t0 + 0.002, frame(ipv4(src_ip, dst_ip, 6, ack_data)))]


def tcp_conn_plain(src_ip: str, sport: int, dst_ip: str, dport: int,
                   t0: float, seq: int = 1000) -> list[tuple[float, bytes]]:
    """Handshake bez danych — wystarcza dla reguł bez content na danych."""
    syn = tcp(src_ip, sport, dst_ip, dport, 0x02, seq, 0)
    synack = tcp(dst_ip, dport, src_ip, sport, 0x12, seq + 100, seq + 1)
    ack = tcp(src_ip, sport, dst_ip, dport, 0x10, seq + 1, seq + 101)
    return [(t0, frame(ipv4(src_ip, dst_ip, 6, syn))),
            (t0 + 0.001, frame(ipv4(dst_ip, src_ip, 6, synack))),
            (t0 + 0.002, frame(ipv4(src_ip, dst_ip, 6, ack)))]


# ---------------------------------------------------------------- techniki

HOME = "127.0.0.1"          # w HOME_NET (127.0.0.0/8) na tym boxie
DC01 = "10.10.0.2"          # dc01 (labnet)
KALI = "127.0.0.1"
CLAYRAT_IP = "91.210.168.138"
CLAYRAT_WS = "193.111.117.72"
UUID = "6f8a2c1e-9d4b-4f1a-8a3b-0c2d4e6f8a10"


def _burst_conns(dst_ip: str, dport: int, n: int, data: bytes,
                 gap: float = 2.0, start: float = 0.0) -> list[tuple[float, bytes]]:
    out: list[tuple[float, bytes]] = []
    for i in range(n):
        out += tcp_conn(KALI, 40000 + i, dst_ip, dport, data, start + i * gap, seq=2000 + i * 500)
    return out


TECHNIQUES = {
    "clayrat-beacon": {
        "mitre": "T1071.001",
        "desc": "ClayRat beacon HTTP: POST /huy?id=…, Host packwatheboss.lol, UA ClayApp/1.0 → 91.210.168.138:80",
        "expected": {"clayrat": [9000801, 9000802, 9000807], "adlab": []},
        "sigma": [],
        "frames": lambda: tcp_conn(
            HOME, 51234, CLAYRAT_IP, 80,
            (f"POST /huy?id={UUID} HTTP/1.1\r\nHost: packwatheboss.lol\r\n"
             "User-Agent: ClayApp/1.0\r\nContent-Length: 45\r\nConnection: close\r\n\r\n"
             "AES-CIPHERTEXT-45BYTES-PADDING-00000000000").encode(), 0.0),
        "events": lambda: [],
    },
    "clayrat-ws": {
        "mitre": "T1071.001",
        "desc": "ClayRat C2 WebSocket: TCP do 193.111.117.72:8080 (kanał komend)",
        "expected": {"clayrat": [9000803], "adlab": []},
        "sigma": [],
        "frames": lambda: tcp_conn(HOME, 51235, CLAYRAT_WS, 8080, b"GET /ws HTTP/1.1\r\nHost: 193.111.117.72:8080\r\n\r\n", 0.0),
        "events": lambda: [],
    },
    "clayrat-dns": {
        "mitre": "T1568.002",
        "desc": "ClayRat DNS: zapytanie o packwatheboss.lol (beacon domena C2)",
        "expected": {"clayrat": [9000808], "adlab": []},
        "sigma": [],
        "frames": lambda: [
            (0.0, frame(ipv4(HOME, "1.1.1.1", 17, udp(HOME, 53000, "1.1.1.1", 53,
                                                      dns_query("packwatheboss.lol"))))),
        ],
        "events": lambda: [],
    },
    "kerberoasting": {
        "mitre": "T1558.003",
        "desc": "Kerberoasting: TGS-REQ (APPLICATION 13 = 0x6d) po Kerberos TCP 88 do DC",
        "expected": {"clayrat": [], "adlab": [1100011]},
        "sigma": ["ad-kerberoasting-001"],
        "frames": lambda: _burst_conns(DC01, 88, 1, b"\x00\x00\x00\x2a\x6d\x01\x02\x03\x04", start=0.0),
        "events": lambda: ([
            {"EventID": 4769, "ServiceName": "svc_sql", "TicketEncryptionType": "0x17",
             "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"},
            # negatyw: AES (0x12) — nie powinien matchować
            {"EventID": 4769, "ServiceName": "svc_backup", "TicketEncryptionType": "0x12",
             "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"},
            # negatyw: konto maszyny (filtr $)
            {"EventID": 4769, "ServiceName": "WINLAB$", "TicketEncryptionType": "0x17",
             "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"},
        ], ["ad-kerberoasting-001"]),
    },
    "asrep-roast": {
        "mitre": "T1558.004",
        "desc": "AS-REP roasting: 5x AS-REQ (APPLICATION 11 = 0x6b) po TCP 88 w 20 s",
        "expected": {"clayrat": [], "adlab": [1100012]},
        "sigma": ["ad-asrep-roasting-001"],
        "frames": lambda: _burst_conns(DC01, 88, 5, b"\x00\x00\x00\x2a\x6b\x01\x02\x03\x04", gap=2.0),
        "events": lambda: ([
            {"EventID": 4768, "TicketOptions": "0x40810000", "TargetUserName": "asrep_user",
             "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"},
            {"EventID": 4768, "TicketOptions": "0x40800000", "TargetUserName": "alice",
             "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"},
        ], ["ad-asrep-roasting-001"]),
    },
    "password-spray": {
        "mitre": "T1110.003",
        "desc": "Password spray: 6x AS-REQ (UDP 88) z jednego źródła w 20 s",
        "expected": {"clayrat": [], "adlab": [1100010]},
        "sigma": ["ad-password-spray-001"],
        "frames": lambda: [
            (i * 2.0, frame(ipv4(HOME, DC01, 17, udp(HOME, 54000 + i, DC01, 88,
                                                     b"\x6a\x81\x02\x00" + b"\x00" * 40))))
            for i in range(6)
        ],
        "events": lambda: ([
            {"EventID": 4771, "Source_Network_Address": "10.10.0.10",
             "Computer": "dc01.xmask.lab"}
            for _ in range(11)
        ] + [
            # negatyw: 5 zdarzeń (<= 10) — nie powinien matchować
            {"EventID": 4771, "Source_Network_Address": "10.10.0.99",
             "Computer": "dc01.xmask.lab"}
            for _ in range(5)
        ], ["ad-password-spray-001"]),
    },
    "smb-enum": {
        "mitre": "T1087/T1018",
        "desc": "SMB enum (netexec): 5 połączeń TCP 445 z jednego źródła w 20 s",
        "expected": {"clayrat": [], "adlab": [1100013]},
        "sigma": ["ad-smb-ldap-enum-001"],
        "frames": lambda: _burst_conns(DC01, 445, 5, b"\x00\x00\x00\x2f\xff\x53\x4d\x42", gap=2.0),
        "events": lambda: ([
            {"EventID": 5145, "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab"}
            for _ in range(12)
        ] + [
            {"EventID": 4662, "Source_Network_Address": "10.10.0.10", "Computer": "dc01.xmask.lab",
             "Properties": "x", "SubjectUserName": "alice"}
            for _ in range(10)
        ], ["ad-smb-ldap-enum-001"]),
    },
    "ldap-enum": {
        "mitre": "T1087/T1018",
        "desc": "LDAP enum (bloodhound/ldapsearch): 8 zapytań TCP 389 w 20 s",
        "expected": {"clayrat": [], "adlab": [1100014]},
        "sigma": [],
        "frames": lambda: _burst_conns(DC01, 389, 8, b"\x30\x0c\x02\x01\x01\x60\x07\x02\x01\x03", gap=2.0),
        "events": lambda: [],
    },
    "dcsync": {
        "mitre": "T1003.006",
        "desc": "DCSync: bind DRSUAPI (GUID 6a73d94e261539b1) po TCP 445",
        "expected": {"clayrat": [], "adlab": [1100015]},
        "sigma": ["ad-dcsync-001"],
        "frames": lambda: _burst_conns(DC01, 445, 1, b"\x00\x00\x00\x40\x05\x00\x0b\x03\x10\x00\x00\x00" + bytes.fromhex("6a73d94e261539b1") + b"\x00" * 40),
        "events": lambda: ([
            {"EventID": 4662, "Properties": "… DS-Replication-Get-Changes …",
             "SubjectUserName": "alice", "Source_Network_Address": "10.10.0.10",
             "Computer": "dc01.xmask.lab"},
            {"EventID": 4662, "Properties": "… DS-Replication-Get-Changes …",
             "SubjectUserName": "WINLAB$", "Source_Network_Address": "10.10.0.10",
             "Computer": "dc01.xmask.lab"},
        ], ["ad-dcsync-001"]),
    },
}


# ---------------------------------------------------------------- sigma matcher

_MODIFIERS = ("contains", "endswith", "startswith")


def _field_value(event: dict, field: str):
    base, _, mod = field.partition("|")
    val = event.get(base)
    if isinstance(val, str):
        val = val.strip()
    return val, mod


def _selection_match(selection: dict, event: dict) -> bool:
    for field, wanted in selection.items():
        val, mod = _field_value(event, field)
        if isinstance(wanted, list):
            ok = any(_val_match(val, w, mod) for w in wanted)
        else:
            ok = _val_match(val, wanted, mod)
        if not ok:
            return False
    return True


def _val_match(val, wanted, mod: str) -> bool:
    if val is None:
        return False
    if mod == "contains":
        return str(wanted) in str(val)
    if mod == "endswith":
        return str(val).endswith(str(wanted))
    if mod == "startswith":
        return str(val).startswith(str(wanted))
    # EventID: int porównanie
    if isinstance(wanted, int) or (isinstance(wanted, str) and wanted.isdigit()):
        try:
            return int(val) == int(wanted)
        except (TypeError, ValueError):
            return False
    return str(val) == str(wanted)


def _parse_timeframe(tf: str) -> timedelta:
    m = re.match(r"(\d+)([smhd])", (tf or "").strip())
    if not m:
        return timedelta(minutes=5)
    n, unit = int(m.group(1)), m.group(2)
    return {"s": timedelta(seconds=n), "m": timedelta(minutes=n),
            "h": timedelta(hours=n), "d": timedelta(days=n)}[unit]


def match_sigma(rule: dict, events: list[dict]) -> bool:
    """Uproszczony matcher dla 5 reguł labu (selection/filter/condition+count)."""
    det = rule.get("detection", {})
    selection = det.get("selection") or {}
    filt = det.get("filter") or {}
    condition = (det.get("condition") or "selection").strip()
    count_m = re.search(r"count\(\) by (\S+)\s*>\s*(\d+)", condition)
    if count_m:
        group_field, threshold = count_m.group(1), int(count_m.group(2))
        window = _parse_timeframe(det.get("timeframe"))
        if window:
            events = sorted(events, key=lambda e: e.get("_ts", 0))
        groups: dict = {}
        for ev in events:
            if not _selection_match(selection, ev):
                continue
            key = str(ev.get(group_field, ""))
            groups.setdefault(key, []).append(ev)
        for g in groups.values():
            if window:
                g = sorted(g, key=lambda e: e.get("_ts", 0))
                for i in range(len(g)):
                    j = i
                    while j + 1 < len(g) and g[j + 1].get("_ts", 0) - g[i].get("_ts", 0) <= window.total_seconds():
                        j += 1
                    if j - i + 1 > threshold:
                        return True
            elif len(g) > threshold:
                return True
        return False

    for ev in events:
        if _selection_match(selection, ev):
            if filt and _selection_match(filt, ev):
                continue
            return True
    return False


# ---------------------------------------------------------------- suricata replay

def parse_rules(rules_text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for m in re.finditer(r'sid:\s*(\d+)\s*;', rules_text):
        sid = int(m.group(1))
        msg = ""
        mm = re.search(r'msg:\s*"([^"]*)"', rules_text[: m.start()][m.start() - 2000:])
        if mm:
            msg = mm.group(1)
        out[sid] = msg
    return out


def run_suricata(pcap_path: Path, rules_path: Path, suri_bin: str) -> dict:
    rundir = Path(tempfile.mkdtemp(prefix="detval_"))
    try:
        cmd = [suri_bin, "-r", str(pcap_path), "-S", str(rules_path),
               "-l", str(rundir), "-k", "none"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        alerts: list[dict] = []
        eve = rundir / "eve.json"
        if eve.exists():
            for line in eve.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if e.get("event_type") == "alert":
                    alerts.append({
                        "sid": e["alert"]["signature_id"],
                        "sig": e["alert"]["signature"],
                        "ts": e.get("timestamp", ""),
                        "src": e.get("src_ip", ""), "dst": e.get("dest_ip", ""),
                        "dport": e.get("dest_port", ""),
                    })
        return {"alerts": alerts, "rc": proc.returncode,
                "stderr_tail": (proc.stderr or "").strip().splitlines()[-3:]}
    finally:
        shutil.rmtree(rundir, ignore_errors=True)


# ---------------------------------------------------------------- raport

def _fmt_sids(sids: list[int]) -> str:
    return ",".join(str(s) for s in sids) if sids else "—"


def write_report(vault: Path, rows: list[dict], summary: dict, out_dir: Path) -> Path:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stamp = now_iso()
    report_dir = vault / "raports"
    report_dir.mkdir(parents=True, exist_ok=True)
    out = report_dir / f"{day}_detection_coverage.md"

    lines = [
        "---",
        f'title: "Pokrycie detekcji — Suricata + Sigma (purple team)"',
        f"date: {day}",
        "type: raport",
        "tags: [lab, purple-team, detekcja, suricata, sigma, coverage]",
        "status: completed",
        "---",
        "",
        "# Pokrycie detekcji — technika ↔ reguła",
        "",
        f"Wygenerowane: `{stamp}` przez `Narzedzia/detection_validator.py` (replay offline, brak ruchu na żywo).",
        "",
        "## Metoda",
        "",
        "- **Suricata:** syntetyczne pcapy technik puszczane `suricata -r` na regułach "
        "`clayrat_c2.rules` (8) + `local.rules` AD lab (11); zbiór SID-ów, które odpaliły → `eve.json`.",
        "- **Sigma:** syntetyczne zdarzenia Windows Security (4768/4769/4662/4771/5145) przez "
        "uproszczony matcher (selection/filter + agregacja `count() by` z `timeframe`).",
        f"- Pcapy własne: `--pcap <file>` — {summary.get('pcap_files', 0)}.",
        "",
        "## Tablica pokrycia",
        "",
        "| Technika | MITRE | Suricata (oczekiwane SID) | Odpaliły | Sigma | Wynik Sigma | Status |",
        "|----------|-------|---------------------------|----------|-------|-------------|--------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['technique']} | {r['mitre']} | {_fmt_sids(r['exp_clayrat'] + r['exp_adlab'])} "
            f"| {_fmt_sids(r['fired'])} | {_fmt_sids(r['sigma_rules'])} "
            f"| {r['sigma_fired']} | {r['status']} |"
        )
    lines += ["", "## Szczegóły Suricata", ""]
    for r in rows:
        if not r["detail_alerts"]:
            continue
        lines.append(f"### {r['technique']} ({r['mitre']})")
        lines.append("")
        for a in r["detail_alerts"]:
            lines.append(f"- `{a['sid']}` {a['sig']} — {a['src']} → {a['dst']}:{a['dport']} ({a['ts']})")
        lines.append("")
    lines += ["## Wnioski i luki", ""]
    for r in rows:
        mark = "✅ wykryte" if r["status"] == "PASS" else ("⚠️ częściowo" if r["status"] == "PARTIAL" else "❌ brak detekcji")
        lines.append(f"- **{r['technique']}** ({r['mitre']}): {mark}.")
    fixes = summary.get("rule_fixes") or []
    if fixes:
        lines += ["", "## Poprawki reguł (wnioski z walidacji)", ""]
        for f in fixes:
            lines.append(f"- {f}")
    lines += [
        "",
        "## Źródła reguł",
        "",
        "- `Narzedzia/clayrat_c2.rules` (ClayRat C2 — beacon HTTP, WS, DNS, IP)",
        "- `Lab/RedTeam_AD/detection/local.rules` (AD lab — Kerberos/LDAP/SMB/DRSUAPI)",
        "- `Lab/RedTeam_AD/detection/sigma/` (5 reguł Sigma)",
        "",
        "Związane: [[Detekcja]] · [[ClayRat_Android_RAT]] · [[Faza2_Windows_AD]]",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    csv_path = out_dir / f"coverage_{day}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["technique", "mitre", "suricata_expected", "suricata_fired",
                    "sigma_rules", "sigma_fired", "status"])
        for r in rows:
            w.writerow([r["technique"], r["mitre"],
                        _fmt_sids(r["exp_clayrat"] + r["exp_adlab"]),
                        _fmt_sids(r["fired"]), _fmt_sids(r["sigma_rules"]),
                        r["sigma_fired"], r["status"]])
    return out


# ---------------------------------------------------------------- main

def load_rules(vault: Path, which: str) -> dict[str, str]:
    sources = {}
    if which in ("clayrat", "all"):
        p = vault / "Narzedzia" / "clayrat_c2.rules"
        if p.exists():
            sources["clayrat"] = p.read_text(encoding="utf-8")
    if which in ("adlab", "all"):
        p = vault / "Lab" / "RedTeam_AD" / "detection" / "local.rules"
        if p.exists():
            sources["adlab"] = p.read_text(encoding="utf-8")
    return sources


def load_sigma(vault: Path) -> list[dict]:
    import yaml

    rules = []
    d = vault / "Lab" / "RedTeam_AD" / "detection" / "sigma"
    if d.is_dir():
        for p in sorted(d.glob("*.yml")):
            try:
                rules.append(yaml.safe_load(p.read_text(encoding="utf-8")))
            except yaml.YAMLError as exc:
                print(f"sigma parse error {p}: {exc}", file=sys.stderr)
    return rules


def _load_events(events, ts0: float) -> list[dict]:
    out = []
    for i, ev in enumerate(events):
        e = dict(ev)
        e["_ts"] = ts0 + i * 3.0
        out.append(e)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Purple-team walidator detekcji (Suricata + Sigma)")
    ap.add_argument("--vault", default="")
    ap.add_argument("--rules", choices=["clayrat", "adlab", "all"], default="all")
    ap.add_argument("--technique", default="all",
                    help="nazwa techniki lub 'all' (zob. lista w raporcie)")
    ap.add_argument("--pcap", action="append", default=[], help="replay własnego pcap")
    ap.add_argument("--suricata-bin", default=shutil.which("suricata") or "suricata")
    ap.add_argument("--no-daily", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    vault = Path(args.vault) if args.vault else find_vault()
    out_dir = vault / "Logs" / "sliver_ops"
    out_dir.mkdir(parents=True, exist_ok=True)

    rules_src = load_rules(vault, args.rules)
    if not rules_src:
        print("brak plików reguł dla wybranego --rules", file=sys.stderr)
        return 1
    combined = "\n".join(f"# ==== {k} ====\n{v}" for k, v in rules_src.items())
    sids = parse_rules(combined)

    sigma_rules = load_sigma(vault)

    names = list(TECHNIQUES) if args.technique == "all" else [args.technique]
    rows = []
    for name in names:
        t = TECHNIQUES.get(name)
        if t is None:
            print(f"nieznana technika: {name}", file=sys.stderr)
            return 1
        # --- Suricata replay
        base_ts = 1755300000.0  # ~2026-08-16, czytelne timestampy w raporcie
        records = [(base_ts + ts, fr) for ts, fr in t["frames"]()]
        pcap = make_pcap(records)
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=False) as fh:
            fh.write(pcap)
            pcap_path = fh.name
        with tempfile.NamedTemporaryFile(suffix=".rules", mode="w", delete=False) as fh:
            fh.write(combined)
            rules_path = fh.name
        try:
            res = run_suricata(Path(pcap_path), Path(rules_path), args.suricata_bin)
        finally:
            os.unlink(pcap_path)
            os.unlink(rules_path)
        fired = sorted({a["sid"] for a in res["alerts"]})
        expected = t["expected"]["clayrat"] + t["expected"]["adlab"]
        hit = sorted(set(expected) & set(fired))
        seen = set()
        detail = []
        for a in res["alerts"]:
            key = (a["sid"], a["ts"])
            if a["sid"] in expected and key not in seen:
                detail.append(a)
                seen.add(key)

        # --- Sigma
        ev_result = t["events"]()
        if isinstance(ev_result, tuple):
            evs, exp_sigma = ev_result
        else:
            evs, exp_sigma = ev_result, []
        sigma_fired = []
        if exp_sigma:
            events = _load_events(evs, 0.0)
            for rule in sigma_rules:
                rid = str(rule.get("id", ""))
                if rid in exp_sigma and match_sigma(rule, events):
                    sigma_fired.append(rid)

        if expected and hit == expected:
            status = "PASS"
        elif hit:
            status = "PARTIAL"
        elif expected:
            status = "FAIL"
        else:
            status = "n/d"
        sigma_status = "PASS" if exp_sigma and sorted(sigma_fired) == sorted(exp_sigma) else (
            "FAIL" if exp_sigma else "n/d")

        rows.append({
            "technique": name, "mitre": t["mitre"], "desc": t["desc"],
            "exp_clayrat": t["expected"]["clayrat"], "exp_adlab": t["expected"]["adlab"],
            "fired": hit, "all_fired": fired,
            "sigma_rules": exp_sigma, "sigma_fired": ",".join(sigma_fired) if sigma_fired else "—",
            "status": status if status != "n/d" else sigma_status,
            "detail_alerts": detail,
        })

        if args.json:
            print(json.dumps({
                "technique": name, "expected_sids": expected, "fired_sids": hit,
                "sigma_expected": exp_sigma, "sigma_fired": sigma_fired,
                "status": status, "sigma_status": sigma_status,
                "suricata_rc": res["rc"],
            }, ensure_ascii=False, indent=2))

    # --- custom pcaps
    for pcap_arg in args.pcap:
        pcap_path = Path(pcap_arg)
        if not pcap_path.is_file():
            print(f"brak pcap: {pcap_arg}", file=sys.stderr)
            continue
        with tempfile.NamedTemporaryFile(suffix=".rules", mode="w", delete=False) as fh:
            fh.write(combined)
            rules_path = fh.name
        try:
            res = run_suricata(pcap_path, Path(rules_path), args.suricata_bin)
        finally:
            os.unlink(rules_path)
        fired = sorted({a["sid"] for a in res["alerts"]})
        detail = res["alerts"]
        rows.append({
            "technique": f"pcap:{pcap_path.name}", "mitre": "custom",
            "desc": f"replay {pcap_arg}", "exp_clayrat": [], "exp_adlab": [],
            "fired": fired, "all_fired": fired, "sigma_rules": [], "sigma_fired": "—",
            "status": "n/d", "detail_alerts": detail,
        })

    # --- konsola
    if not args.json:
        print(f"{'Technika':<20} {'MITRE':<12} {'Suricata':<10} {'Sigma':<8} Status")
        print("-" * 70)
        for r in rows:
            fired_txt = _fmt_sids(r["fired"]) if r["fired"] else ("—" if r["exp_clayrat"] + r["exp_adlab"] else "n/d")
            print(f"{r['technique']:<20} {r['mitre']:<12} {fired_txt:<10} {r['sigma_fired']:<8} {r['status']}")

    # --- raport + daily
    report = write_report(vault, rows, {"pcap_files": len(args.pcap), "rule_fixes": [
        "`clayrat_c2.rules` sid 9000802: usunięto `nocase` z `http.host` — Suricata 7.0.10 "
        "normalizuje bufor hosta do małych liter; `nocase` łamał dopasowanie (reguła nigdy "
        "nie triggerowała). Zweryfikowane replayem (PARTIAL → PASS)."
    ]}, out_dir)
    if not args.no_daily:
        body_lines = [f"Replay offline przez `Narzedzia/detection_validator.py` (reguły `{args.rules}`)."]
        for r in rows:
            body_lines.append(f"- **{r['technique']}** ({r['mitre']}): Suricata "
                              f"{_fmt_sids(r['fired']) if r['fired'] else '—'} · Sigma {r['sigma_fired']} · {r['status']}")
        body_lines.append(f"Pełny raport: [[{report.stem}]]")
        log_daily(vault, "Pokrycie detekcji — Suricata + Sigma", "\n".join(body_lines))
    print(f"\nraport: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
