#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cve_correlator.py — korelator CVE <-> exploit.

Wejscie: wersje uslug z outputu nmap (jak live_demo/i1_nmap_sV.txt) oraz
znaleziska nuclei (JSONL, pola info.classification.cve-id) — albo wprost
pary "produkt wersja".

Proces:
  1. zebranie wersji (nmap: "Apache httpd 2.4.49", "OpenSSH 8.9p1"; nuclei: cve-id)
  2. wersja -> CVE (lokalna baza wiedzy + opcjonalnie API cve.circl.lu --online)
  3. CVE -> dostepnosc exploita:
       - searchsploit --cve <CVE>   (Exploit-DB)
       - msfconsole -q -x "search cve:<CVE>"   (wzorzec: msf_search_ms17010.txt)
  4. karta Obsidian z gotowym planem: <out>/<domain>/cve_<CVE>.md
     + podsumowanie <out>/<domain>/exploit_plan.md

Uzycie:
  python3 cve_correlator.py --nmap raw/nmap.txt --nuclei raw/nuclei_tech.jsonl \\
      --domain xmask.lab --out Projekty/Recon [--msf] [--online] [--dry-run]
  python3 cve_correlator.py --version "Apache httpd 2.4.49" --domain t --out /tmp/o
  python3 cve_correlator.py --kb moja_baza.json --nmap nmap.txt ...

Env:
  OBSIDIAN_VAULT     sciezka do vaultu (auto-wykrywany)
  KALI_CONTAINER     kontener Kali dla searchsploit/msfconsole (domyslnie "kali")
  CVE_STATE          plik stanu (cache wynikow searchsploit/msf)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
KALI_CONTAINER = os.environ.get("KALI_CONTAINER", "kali")
STATE_FILE = Path(os.environ.get("CVE_STATE", "/root/obsidian-cve-state.json"))
CIRCL_BASE = "https://cve.circl.lu/api"

# ---------------------------------------------------------------- lokalna baza

# (regex_produkt, regex_wersji|None, [CVE,...], notatka)
KB: list[tuple[str, str | None, list[str], str]] = [
    (r"apache httpd", r"2\.4\.49", ["CVE-2021-41773", "CVE-2021-42013"],
     "Path traversal + RCE (Apache 2.4.49/2.4.50, cgi-bin)"),
    (r"apache httpd", r"2\.4\.50", ["CVE-2021-42013"], "path traversal bypass (2.4.50)"),
    (r"openssh", r"8\.[5-7]", ["CVE-2021-41617"], "privsep user enumeration / DoS"),
    (r"openssh", r"(?:8\.[5-9]|9\.[0-7])p?\d*", ["CVE-2024-6387"],
     "regreSSHion — RCE bez uwierzytelnienia (glibc, 8.5p1–9.7p1)"),
    (r"microsoft-ds|smb", None, ["CVE-2017-0143", "CVE-2017-0144", "CVE-2017-0145"],
     "MS17-010 EternalBlue — SMB RCE (demo: msf_search_ms17010.txt)"),
    (r"netbios-ssn", None, ["CVE-2017-0143", "CVE-2017-0144"],
     "MS17-010 — sprawdz przez auxiliary/scanner/smb/smb_ms17_010"),
    (r"vsftpd", r"2\.3\.4", ["CVE-2011-2523"], "vsftpd 2.3.4 backdoor (port 6200)"),
    (r"proftpd", r"1\.3\.3c", ["CVE-2010-4221"], "ProFTPD 1.3.3c — komenda exec"),
    (r"exim", r"4\.9[0-2]", ["CVE-2019-15846"], "Exim 4.92 — RCE (string expansion)"),
    (r"samba", r"3\.5\.[0-9]|4\.[0-6]\.[0-9]", ["CVE-2017-7494"], "SambaCry — RCE (smb.conf)"),
    (r"nginx", r"1\.21\.[0-4]", ["CVE-2021-23017"], "nginx resolver off-by-one (DNS)"),
    (r"php", r"7\.[0-3]\.\d+", ["CVE-2019-11043"], "PHP-FPM env_path_info RCE (CVE-2019-11043)"),
    (r"tomcat", r"9\.0\.\d+", ["CVE-2020-1938"], "Ghostcat — AJP RCE (8009)"),
    (r"jenkins", r"2\.\d+", ["CVE-2018-1000861"], "Jenkins RCE (Groovy, CVE-2018-1000861)"),
]

CVE_META: dict[str, str] = {
    "CVE-2021-41773": "Apache HTTP Server 2.4.49 — path traversal / RCE przez cgi-bin",
    "CVE-2021-42013": "Apache HTTP Server 2.4.50 — bypass path traversal",
    "CVE-2021-41617": "OpenSSH 8.5–8.7 — privilege separation / user enumeration",
    "CVE-2024-6387": "OpenSSH regreSSHion — zdalne RCE (glibc, SSHD)",
    "CVE-2017-0143": "MS17-010 EternalBlue — SMBv1 RCE",
    "CVE-2017-0144": "MS17-010 EternalBlue — SMBv1 RCE (kod wykonawczy)",
    "CVE-2017-0145": "MS17-010 EternalBlue — SMBv1 RCE",
    "CVE-2011-2523": "vsftpd 2.3.4 — backdoor w login (smiley face)",
    "CVE-2010-4221": "ProFTPD 1.3.3c — command execution",
    "CVE-2019-15846": "Exim 4.92 — RCE przez string expansion",
    "CVE-2017-7494": "Samba SambaCry — RCE przez komendy w share",
    "CVE-2021-23017": "nginx — off-by-one w resolver DNS",
    "CVE-2019-11043": "PHP-FPM — env_path_info RCE",
    "CVE-2020-1938": "Apache Tomcat Ghostcat — AJP file read/RCE",
    "CVE-2018-1000861": "Jenkins — RCE (Groovy script)",
}

# ---------------------------------------------------------------- pomoce

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[*] {msg}", flush=True)


def err(msg: str) -> None:
    print(f"[!] {msg}", file=sys.stderr, flush=True)


def sh(cmd: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, ""
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def find_tool(name: str) -> list[str] | None:
    if shutil.which(name):
        return []
    if shutil.which("docker"):
        probe = subprocess.run(
            ["docker", "exec", KALI_CONTAINER, "sh", "-lc", f"command -v {name}"],
            capture_output=True, text=True, timeout=30)
        if probe.returncode == 0:
            return ["docker", "exec", KALI_CONTAINER]
    return None


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


# ---------------------------------------------------------------- parsowanie

def parse_nmap(path: Path) -> list[dict]:
    """-oN i -oG -> [{'service','version','port','proto'}]."""
    text = path.read_text(encoding="utf-8", errors="replace")
    out: list[dict] = []
    for m in re.finditer(r"^(\d+)/tcp\s+open\s+(\S+)\s+(.+)$", text, re.M):
        ver = m.group(3).strip()
        out.append({"service": m.group(2), "version": ver.split("(")[0].strip(),
                    "port": m.group(1), "proto": "tcp"})
    for m in re.finditer(r"Ports:\s*([^\n]+)", text):
        for part in m.group(1).split(","):
            f = part.split("/")
            if len(f) >= 6 and f[1] == "open":
                out.append({"service": f[4], "version": f[5], "port": f[0], "proto": f[2]})
    seen, uniq = set(), []
    for s in out:
        k = (s["port"], s["proto"], s["service"], s["version"])
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq


def parse_nuclei(path: Path) -> list[dict]:
    """JSONL -> [{cves, name, severity, url, matcher}] (fallback: kolorowany tekst)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        j = None
        try:
            j = json.loads(line)
        except json.JSONDecodeError:
            pass
        if isinstance(j, dict):
            info = j.get("info") or {}
            cves = (info.get("classification") or {}).get("cve-id") or []
            findings.append({
                "cves": [str(c) for c in cves],
                "name": info.get("name") or "",
                "severity": info.get("severity") or "info",
                "url": j.get("matched-at") or j.get("url") or "",
                "matcher": j.get("matcher-name") or "",
            })
        else:
            # kolorowany output: [template:matcher] [proto] [severity] url
            clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
            m = re.match(r"^\[([^\]]+)\]\s*\[([^\]]+)\]\s*\[([^\]]+)\]\s*(.*)$", clean)
            cves = re.findall(r"CVE-\d{4}-\d{4,7}", clean, re.I)
            findings.append({
                "cves": [c.upper() for c in cves],
                "name": m.group(1).strip() if m else "",
                "severity": m.group(3).strip() if m else "",
                "url": m.group(4).strip() if m else clean,
                "matcher": "",
            })
    return findings


def load_kb(custom: str | None) -> list[tuple[str, str | None, list[str], str]]:
    kb = list(KB)
    if custom and Path(custom).is_file():
        try:
            data = json.loads(Path(custom).read_text(encoding="utf-8"))
            for e in data if isinstance(data, list) else data.get("entries", []):
                kb.append((e["product"], e.get("version"), list(e["cves"]), e.get("note", "")))
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            err(f"baza --kb nieczytelna: {exc}")
    return kb


def version_to_cves(service: str, version: str, kb) -> list[tuple[str, str]]:
    """Zwraca [(cve, notatka)] dla pary usluga+wersja."""
    hay = f"{service} {version}".strip().lower()
    hits: list[tuple[str, str]] = []
    for prod_re, ver_re, cves, note in kb:
        if not re.search(prod_re, hay):
            continue
        if ver_re:
            ver_hay = f"{service} {version}".lower()
            if not re.search(ver_re, ver_hay):
                continue
        for c in cves:
            hits.append((c, note))
    return hits


# ---------------------------------------------------------------- exploity

def load_state() -> dict:
    if STATE_FILE.is_file():
        try:
            d = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                d.setdefault("cves", {})
                return d
        except json.JSONDecodeError:
            pass
    return {"cves": {}}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE_FILE)


def searchsploit_cve(cve: str, dry: bool) -> list[dict]:
    prefix = find_tool("searchsploit")
    if not prefix:
        return []
    rows: list[dict] = []
    cmd = prefix + ["searchsploit", "--cve", cve]
    if dry:
        log("  $ " + " ".join(cmd))
        return rows
    rc, out = sh(cmd, timeout=120)
    in_rows = False
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("Exploit Title"):
            in_rows = True
            continue
        if in_rows and s and "|" in s and not s.startswith("-"):
            parts = [p.strip() for p in s.split("|")]
            if len(parts) >= 2:
                rows.append({"title": parts[0], "path": parts[1],
                             "type": parts[2] if len(parts) > 2 else ""})
    return rows


def msf_search_cve(cve: str, dry: bool) -> list[str]:
    prefix = find_tool("msfconsole")
    if not prefix:
        return []
    cmd = prefix + ["msfconsole", "-q", "-x", f"search cve:{cve}; exit"]
    if dry:
        log("  $ " + " ".join(cmd))
        return []
    rc, out = sh(cmd, timeout=300)
    modules: list[str] = []
    in_match = False
    for line in out.splitlines():
        s = line.strip()
        if "Matching Modules" in s:
            in_match = True
            continue
        if in_match:
            m = re.match(r"^\d+\s+(\S+)\s+", s)
            if m and "/" in m.group(1):
                modules.append(m.group(1))
    return modules


def circl_cve(cve: str) -> dict:
    """Dane CVE z cve.circl.lu (--online). Zwraca {} przy bledzie."""
    try:
        req = urllib.request.Request(f"{CIRCL_BASE}/cve/{cve}",
                                     headers={"User-Agent": "ive-automation/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return {}


# ---------------------------------------------------------------- karty

def esc_md(text: str) -> str:
    return (str(text).replace("|", "\\|").replace("\n", " ").strip())


def write_cve_card(out_dir: Path, domain: str, cve: str, note: str,
                   affected: str, sploit: list[dict], msf: list[str],
                   online: dict, sploit_avail: bool, msf_avail: bool,
                   dry: bool) -> Path:
    if dry:
        return out_dir / f"cve_{cve}.md"
    meta = online if online else {}
    summary = (meta.get("summary") or note or "").strip()
    cvss = ""
    if isinstance(meta.get("cvss"), dict):
        cvss = str(meta["cvss"].get("score", ""))
    elif meta.get("cvss"):
        cvss = str(meta["cvss"])

    L: list[str] = []
    L.append("---")
    L.append(f'title: "{cve} — plan exploita"')
    L.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    L.append("tags: [cve, exploit, plan, auto, pentest]")
    L.append(f"cve: {cve}")
    L.append(f"domain: {domain}")
    L.append("status: active")
    L.append("---")
    L.append("")
    L.append(f"# {cve} — plan exploita")
    L.append("")
    L.append(f"> Cel: `{domain}` · podatny komponent: `{affected}`")
    L.append("")
    L.append("## Opis")
    L.append("")
    L.append(summary or "_Brak opisu (uzupełnij ręcznie)._")
    L.append("")
    if cvss:
        L.append(f"- **CVSS:** {cvss}")
        L.append("")
    L.append("## Dostępne exploity")
    L.append("")
    if sploit:
        L.append("### Exploit-DB (searchsploit)")
        L.append("")
        L.append("| Tytuł | Ścieżka | Typ |")
        L.append("|-------|---------|-----|")
        for e in sploit:
            L.append(f"| {esc_md(e['title'])} | `{e['path']}` | {esc_md(e['type'])} |")
        L.append("")
        L.append("```bash")
        L.append(f"searchsploit -x {sploit[0]['path']}")
        L.append("```")
        L.append("")
    else:
        L.append(("_searchsploit niedostępny na tym hoście — sprawdź "
                  "Exploit-DB ręcznie._") if not sploit_avail
                 else "_Brak wpisów w Exploit-DB dla tego CVE (searchsploit --cve)._")
        L.append("")
    if msf:
        L.append("### Metasploit (msfconsole)")
        L.append("")
        for mod in msf:
            L.append(f"- `{mod}`")
        L.append("")
        L.append("```bash")
        L.append(f"msfconsole -q -x \"use {msf[0]}; set RHOSTS {domain}; run\"")
        L.append("```")
        L.append("")
    else:
        L.append(("_msfconsole niedostępny — sprawdź `search cve:<CVE>` "
                  "ręcznie w Metasploit._") if not msf_avail
                 else "_Brak modułów Metasploit (search cve:<CVE>)._")
        L.append("")
    L.append("## Kroki")
    L.append("")
    L.append("1. Potwierdź wersję podatnego komponentu na celu (nmap -sV / nuclei).")
    L.append("2. Wykonaj exploit tylko w autoryzowanym zakresie (lab / zgoda klienta).")
    L.append("3. Po uzyskaniu dostępu: zbierz dowody, udokumentuj, posprzątaj.")
    L.append("")
    L.append("## Źródła")
    L.append("")
    L.append(f"- https://nvd.nist.gov/vuln/detail/{cve}")
    L.append(f"- https://cve.circl.lu/cve/{cve}")
    L.append("")
    card = out_dir / f"cve_{cve}.md"
    tmp = card.with_suffix(".md.tmp")
    tmp.write_text("\n".join(L), encoding="utf-8")
    tmp.replace(card)
    return card


def write_plan(out_dir: Path, domain: str, rows: list[dict], dry: bool) -> Path:
    plan = out_dir / "exploit_plan.md"
    if dry:
        return plan
    L: list[str] = []
    L.append("---")
    L.append(f'title: "{domain} — plan exploitacji (auto)"')
    L.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    L.append("tags: [exploit, plan, auto, pentest]")
    L.append(f"domain: {domain}")
    L.append("status: active")
    L.append("---")
    L.append("")
    L.append(f"# {domain} — plan exploitacji")
    L.append("")
    L.append(f"> Wygenerowano: {utc_now()} · korelator CVE <-> exploit.")
    L.append("")
    L.append("| CVE | Komponent | Exploit-DB | Metasploit | Karta |")
    L.append("|-----|-----------|:----------:|:----------:|-------|")
    for r in rows:
        cve = r["cve"]
        sploit_yes = "✅" if r["sploit"] else "—"
        msf_yes = "✅" if r["msf"] else "—"
        link = f"cve_{cve}"
        try:
            rel = out_dir.resolve().relative_to(find_vault().resolve())
            link = str(rel / f"cve_{cve}")
        except ValueError:
            pass
        L.append(f"| `{cve}` | {esc_md(r['affected'])} | {sploit_yes} | {msf_yes} | "
                 f"[[{link}|plan]] |")
    L.append("")
    L.append("## Następne kroki")
    L.append("")
    L.append("- Wykonaj kroki z kart `cve_*` (potwierdź wersję → exploit → dowody).")
    L.append("- Aktualizuj po każdym skanie: `python3 Narzedzia/cve_correlator.py --nmap ...`")
    L.append("")
    tmp = plan.with_suffix(".md.tmp")
    tmp.write_text("\n".join(L), encoding="utf-8")
    tmp.replace(plan)
    return plan


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Korelator CVE <-> exploit -> karty Obsidian.")
    ap.add_argument("--nmap", help="plik outputu nmap (-oN lub -oG)")
    ap.add_argument("--nuclei", help="plik outputu nuclei (JSONL lub tekst)")
    ap.add_argument("--version", action="append", default=[],
                    help='para "Produkt Wersja" (powtarzalna)')
    ap.add_argument("--domain", required=True)
    ap.add_argument("--out", help="katalog kart (domyślnie <vault>/Projekty/Recon)")
    ap.add_argument("--kb", help="dodatkowa baza wiedzy JSON")
    ap.add_argument("--online", action="store_true",
                    help="pobierz metadane CVE z cve.circl.lu")
    ap.add_argument("--msf", action="store_true",
                    help="szukaj modułów w msfconsole (wolne)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not (a.nmap or a.nuclei or a.version):
        err("podaj --nmap, --nuclei albo --version")
        return 2

    vault = find_vault()
    out_dir = Path(a.out) if a.out else vault / "Projekty" / "Recon" / a.domain
    out_dir.mkdir(parents=True, exist_ok=True)
    kb = load_kb(a.kb)
    state = load_state()
    dry = a.dry_run

    # 1. zebranie wersji
    findings: list[dict] = []  # {"affected","cves":[(cve,note)]}
    if a.nmap and Path(a.nmap).is_file():
        for s in parse_nmap(Path(a.nmap)):
            cves = version_to_cves(s["service"], s["version"], kb)
            if cves:
                affected = f"{s['service']} {s['version']}".strip()
                findings.append({"affected": affected, "cves": cves,
                                 "src": f"nmap:{s['port']}/{s['proto']}"})
                log(f"nmap: {affected} -> {', '.join(c for c, _ in cves)}")
    if a.nuclei and Path(a.nuclei).is_file():
        for f_ in parse_nuclei(Path(a.nuclei)):
            if f_["cves"]:
                cves = [(c, "") for c in f_["cves"]]
                findings.append({"affected": f_["name"] or f_["url"], "cves": cves,
                                 "src": f_["url"]})
                log(f"nuclei: {f_['name']} -> {', '.join(c for c, _ in cves)}")
    for v in a.version:
        parts = v.split(None, 1)
        if len(parts) == 2:
            cves = version_to_cves(parts[0], parts[1], kb)
            if cves:
                findings.append({"affected": v, "cves": cves, "src": "cli"})
                log(f"cli: {v} -> {', '.join(c for c, _ in cves)}")
        else:
            err(f"--version wymaga 'Produkt Wersja': {v!r}")

    if not findings:
        log("brak dopasowan w lokalnej bazie — spróbuj --online (API) albo rozszerz --kb")
        return 0

    # 2-3. CVE -> exploity
    rows: list[dict] = []
    seen_cves: set[str] = set()
    sploit_avail = bool(find_tool("searchsploit"))
    msf_avail = bool(find_tool("msfconsole"))
    if not sploit_avail:
        log("searchsploit niedostępny (PATH/kontener) — pominę Exploit-DB")
    if not msf_avail and a.msf:
        log("msfconsole niedostępny — pominę szukanie modułów")
    for f_ in findings:
        for cve, note in f_["cves"]:
            if cve in seen_cves:
                continue
            seen_cves.add(cve)
            cached = state["cves"].get(cve, {})
            sploit = cached.get("sploit") or searchsploit_cve(cve, dry)
            msf = cached.get("msf") or (msf_search_cve(cve, dry) if a.msf else [])
            online = circl_cve(cve) if a.online and not dry else {}
            state["cves"][cve] = {"sploit": sploit, "msf": msf, "checked": utc_now()}
            rows.append({"cve": cve, "affected": f_["affected"], "note": note,
                         "sploit": sploit, "msf": msf, "online": online})
            log(f"CVE {cve}: searchsploit={len(sploit)} msf={len(msf)}")
            if not dry:
                write_cve_card(out_dir, a.domain, cve, note, f_["affected"],
                               sploit, msf, online, sploit_avail, msf_avail, dry)

    if not dry:
        save_state(state)
        write_plan(out_dir, a.domain, rows, dry)
        print(f"\nGOTOWE: karty w {out_dir}")
        print(f"  podsumowanie: {out_dir / 'exploit_plan.md'}")
    else:
        print("\n(dry-run — nic nie zapisano)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
