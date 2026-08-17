#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""target_profile.py — orchestrator recon I-V-E dla jednej domeny.

Realizuje flow z [[Model_IVE/IVE_MOC]]:

  I  Informacja   theHarvester (OSINT: emaile, hosty/subdomeny, IP)
  V  Podatnosci   nuclei tech-detect (13k szablonow) + nmap -sV (skrypty,
                  jak w Model_IVE/_analiza_dynamiczna/live_demo/i1_nmap_sV.txt)
                  + sqlmap / nuclei na wykrytych celach webowych
  E  Eksploatacja korelacja CVE <-> exploit (cve_correlator.py) -> karty
                  z gotowym planem

Wynik: karta Obsidian "dossier" z sekcjami I/V/E:
    <VAULT>/Projekty/Recon/<domain>.md
surowe outputy:
    <VAULT>/Projekty/Recon/<domain>/raw/

Narzedzia wykrywane automatycznie: najpierw w PATH, potem w kontenerze Kali
(docker exec <KALI_CONTAINER> ...). Bezpieczne domysly: tylko pasywne zrodla
OSINT, skan bez agresywnych opcji, sqlmap tylko na URL z parametrami.

Uzycie:
  python3 target_profile.py --domain xmask.lab
  python3 target_profile.py --domain xmask.lab --skip nmap --dry-run
  python3 target_profile.py --domain example.com --check-tools

Env:
  OBSIDIAN_VAULT     sciezka do vaultu (auto-wykrywany)
  KALI_CONTAINER     nazwa kontenera Kali (domyslnie "kali")
  NUCLEI_TEMPLATES   katalog szablonow nuclei (domyslnie auto /root/nuclei-templates)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------- konfiguracja

HERE = Path(__file__).resolve().parent
KALI_CONTAINER = os.environ.get("KALI_CONTAINER", "kali")
HARVESTER_SOURCES_DEFAULT = "crtsh,hackertarget,otx,rapiddns"
TECH_DETECT = "http/technologies/tech-detect.yaml"

TOOLS = ("theHarvester", "nuclei", "nmap", "sqlmap", "docker")

_tool_cache: dict[str, list[str] | None] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[*] {msg}", flush=True)


def err(msg: str) -> None:
    print(f"[!] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- narzedzia

def find_tool(name: str) -> list[str] | None:
    """Zwraca prefix polecenia (np. [] albo ["docker","exec","kali"])."""
    if name in _tool_cache:
        return _tool_cache[name]
    path = shutil.which(name)
    if path:
        _tool_cache[name] = []
        return []
    if shutil.which("docker"):
        probe = subprocess.run(
            ["docker", "exec", KALI_CONTAINER, "sh", "-lc", f"command -v {name}"],
            capture_output=True, text=True, timeout=30,
        )
        if probe.returncode == 0:
            _tool_cache[name] = ["docker", "exec", KALI_CONTAINER]
            return _tool_cache[name]
    _tool_cache[name] = None
    return None


def tool_missing(name: str) -> bool:
    return find_tool(name) is None


def sh(cmd: list[str], timeout: int = 300, check: bool = False) -> tuple[int, str]:
    """Uruchamia polecenie, zwraca (rc, stdout+stderr)."""
    log("$ " + " ".join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        err(f"timeout po {timeout}s: {' '.join(cmd)}")
        return 124, ""
    out = (r.stdout or "") + (r.stderr or "")
    if check and r.returncode != 0:
        err(f"polecenie zwrocilo rc={r.returncode}: {' '.join(cmd)}")
    return r.returncode, out


# ---------------------------------------------------------------- vault

def find_vault() -> Path:
    env = os.environ.get("OBSIDIAN_VAULT")
    if env:
        return Path(env)
    # szukamy w gore od katalogu skryptu katalogu z Daily/ i Narzedzia/
    p = HERE
    for _ in range(6):
        if (p / "Daily").is_dir() and (p / "Narzedzia").is_dir():
            return p
        p = p.parent
    return Path.home() / "obsidian-vault"


# ---------------------------------------------------------------- faza I

def parse_harvester_json(path: Path, text_out: str = "") -> dict:
    data = {"hosts": [], "ips": [], "emails": [], "people": [], "credentials": []}
    try:
        raw = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError) as exc:
        err(f"theHarvester JSON nieczytelny: {exc}")
        raw = None
    if isinstance(raw, dict):
        pass
    else:
        raw = {}
    # emaile bywaja tylko w outputcie tekstowym — fallback regex
    if text_out:
        for em in re.findall(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text_out, re.I):
            em = em.strip(".,;")
            if em.lower() not in [e.lower() for e in data["emails"]]:
                data["emails"].append(em)
    if not raw:
        return data
    for h in raw.get("hosts") or []:
        if isinstance(h, dict) and h.get("host"):
            data["hosts"].append(
                {"host": str(h["host"]).strip(), "ip": h.get("ip_address") or "",
                 "module": h.get("module") or ""})
            if h.get("ip_address"):
                data["ips"].append(str(h["ip_address"]).strip())
    for e in raw.get("emails") or []:
        if isinstance(e, dict):
            if e.get("email"):
                data["emails"].append(str(e["email"]).strip())
        elif isinstance(e, str):
            data["emails"].append(e.strip())
    for p in raw.get("people") or []:
        if isinstance(p, dict) and p.get("name"):
            data["people"].append(str(p["name"]).strip())
        elif isinstance(p, str):
            data["people"].append(p.strip())
    # niektore wersje wypisuja "ips" / "credentials"
    for ip in raw.get("ips") or []:
        if isinstance(ip, str):
            data["ips"].append(ip.strip())
    for c in raw.get("credentials") or []:
        if isinstance(c, dict) and (c.get("email") or c.get("username")):
            data["credentials"].append(str(c.get("email") or c.get("username")).strip())
    return data


def resolve_host(host: str) -> list[str]:
    ips: list[str] = []
    try:
        for info in socket.getaddrinfo(host, None):
            ip = info[4][0]
            if ip not in ips:
                ips.append(ip)
    except OSError:
        pass
    return ips


def phase_i(domain: str, args) -> dict:
    log(f"FAZA I — theHarvester ({domain})")
    if tool_missing("theHarvester"):
        err("brak theHarvester — pominieto faze I")
        return {"hosts": [], "ips": [], "emails": [], "people": [], "credentials": []}

    out_json = args.workdir / "theharvester.json"
    cmd = ["theHarvester", "-d", domain, "-b", args.sources, "-l", str(args.limit),
           "-t", "-f", str(out_json)]
    rc, out = sh(cmd, timeout=args.timeout)
    (args.workdir / "theharvester.txt").write_text(out or "", encoding="utf-8", errors="replace")
    if rc != 0 and not out_json.is_file():
        err("theHarvester nie zwrocil pliku JSON")
        return {"hosts": [], "ips": [], "emails": [], "people": [], "credentials": []}

    data = parse_harvester_json(out_json, out)
    # domyslna rozdzielczosc hostow -> IP (jesli theHarvester nie dal ip_address)
    resolved: dict[str, str] = {}
    for h in data["hosts"]:
        if not h["ip"]:
            ips = resolve_host(h["host"])
            if ips:
                h["ip"] = ips[0]
                resolved[h["host"]] = ips[0]
    for host, ip in resolved.items():
        if ip not in data["ips"]:
            data["ips"].append(ip)
    # dedupe
    data["hosts"] = [dict(t) for t in {tuple(sorted(h.items())) for h in data["hosts"]}]
    data["ips"] = sorted(set(data["ips"]))
    data["emails"] = sorted(set(data["emails"]))

    log(f"  hosty={len(data['hosts'])} ips={len(data['ips'])} "
        f"emaile={len(data['emails'])} ludzie={len(data['people'])}")
    if data["hosts"]:
        for h in data["hosts"][:15]:
            log(f"    - {h['host']} ({h['ip']}) [{h['module']}]")
    return data


# ---------------------------------------------------------------- faza V

def web_targets(domain: str, info: dict, args) -> list[str]:
    """Lista celow HTTP(S): domena + wykryte hosty z www/panel/api itd."""
    targets: list[str] = []
    for scheme in ("https", "http"):
        targets.append(f"{scheme}://{domain}")
    for h in info.get("hosts", []):
        host = h["host"]
        if host == domain or host.endswith("." + domain):
            targets.append(f"https://{host}")
            targets.append(f"http://{host}")
    # plik z dodatkowymi URL-ami
    if args.urls and Path(args.urls).is_file():
        for line in Path(args.urls).read_text(errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                targets.append(line)
    # dedupe, zachowujac kolejnosc
    seen: set[str] = set()
    out: list[str] = []
    for t in targets:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[: args.max_web_targets]


def phase_v_nuclei(domain: str, targets: list[str], args) -> dict:
    log(f"FAZA V — nuclei tech-detect ({len(targets)} celow)")
    if tool_missing("nuclei"):
        err("brak nuclei — pominieto tech-detect")
        return {"template": "tech-detect", "findings": []}

    templates_dir = args.nuclei_templates or "/root/nuclei-templates"
    tech = str(Path(templates_dir) / TECH_DETECT)
    out_jsonl = args.workdir / "nuclei_tech.jsonl"
    findings: list[dict] = []

    def scan(tmpl: str, out_file: Path, extra: list[str]) -> list[dict]:
        cmd = ["nuclei", "-jsonl", "-o", str(out_file)]
        for t in targets:
            cmd += ["-u", t]
        cmd += ["-t", tmpl] + extra
        sh(cmd, timeout=args.timeout)
        hits: list[dict] = []
        if out_file.is_file():
            for line in out_file.read_text(errors="replace").splitlines():
                try:
                    j = json.loads(line)
                except json.JSONDecodeError:
                    continue
                info = j.get("info") or {}
                hits.append({
                    "template": j.get("template-id") or j.get("template") or "",
                    "name": info.get("name") or "",
                    "severity": info.get("severity") or "info",
                    "matcher": j.get("matcher-name") or "",
                    "url": j.get("matched-at") or j.get("url") or "",
                    "cves": (info.get("classification") or {}).get("cve-id") or [],
                    "tags": info.get("tags") or [],
                })
        return hits

    if os.path.exists(tech):
        findings = scan(tech, out_jsonl, [])
    else:
        err(f"brak szablonu tech-detect: {tech} (sprawdz --nuclei-templates)")

    if args.nuclei_all and targets:
        log("FAZA V — nuclei full scan (wszystkie szablony, severity>=medium)")
        out_all = args.workdir / "nuclei_all.jsonl"
        findings += scan(
            str(templates_dir),
            out_all,
            ["-severity", "medium,high,critical", "-stats", "-silent"],
        )

    log(f"  znaleziska tech={len(findings)}")
    return {"template": "tech-detect", "findings": findings}


def parse_nmap(output: str) -> list[dict]:
    """Parsuje -oN i -oG nmap na liste {port, service, version, product}."""
    services: list[dict] = []
    # format -oN (jak i1_nmap_sV.txt)
    for m in re.finditer(r"^(\d+)/tcp\s+open\s+(\S+)\s+(.+)$", output, re.M):
        port, service, rest = m.group(1), m.group(2), m.group(3).strip()
        version = rest.split("(")[0].strip() if rest else ""
        services.append({"port": port, "proto": "tcp", "service": service,
                         "version": version, "raw": rest})
    # format -oG (greppable)
    for m in re.finditer(r"Ports:\s*([^\n]+)", output):
        for part in m.group(1).split(","):
            f = part.split("/")
            if len(f) >= 6 and f[1] == "open":
                services.append({"port": f[0], "proto": f[2], "service": f[4],
                                 "version": f[5], "raw": f[5]})
    # dedupe
    seen = set()
    out = []
    for s in services:
        key = (s["port"], s["proto"], s["service"], s["version"])
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out


def phase_v_nmap(info: dict, args) -> list[dict]:
    log("FAZA V — nmap -sV + skrypty")
    ips = sorted(set(info.get("ips", [])))
    if not ips:
        log("  brak IP do skanu — pomijam nmap")
        return []
    if tool_missing("nmap"):
        err("brak nmap — pominieto")
        return []

    ips_cap = ips[: args.max_ips]
    prefix = find_tool("nmap") or []
    out_n = args.workdir / "nmap.txt"
    out_g = args.workdir / "nmap.gnmap"
    cmd = prefix + ["nmap", "-Pn", "-sV", "--version-light",
                    "--script", "default,http-title,http-headers",
                    "-oN", str(out_n), "-oG", str(out_g)] + ips_cap
    sh(cmd, timeout=args.timeout)
    output = ""
    if out_n.is_file():
        output = out_n.read_text(errors="replace")
    services = parse_nmap(output)
    log(f"  uslugi={len(services)} ({len(ips_cap)} IP)")
    for s in services[:20]:
        log(f"    - {s['port']}/{s['proto']} {s['service']} {s['version']}")
    return services


def phase_v_sqlmap(targets: list[str], args) -> list[dict]:
    log("FAZA V — sqlmap (cele z parametrami GET)")
    if tool_missing("sqlmap"):
        err("brak sqlmap — pominieto")
        return []
    param_urls = [t for t in targets if "?" in t]
    if not param_urls:
        log("  brak URL z parametrami — pomijam sqlmap")
        return []
    prefix = find_tool("sqlmap") or []
    results: list[dict] = []
    for url in param_urls[: args.max_sqlmap]:
        out_dir = args.workdir / "sqlmap"
        cmd = prefix + ["sqlmap", "-u", url, "--batch", "--smart", "--banner",
                        "--timeout", "20", "--output-dir", str(out_dir)]
        rc, out = sh(cmd, timeout=args.timeout)
        banner = ""
        m = re.search(r"\[INFO\] (?:the back-end DBMS is|banner:)\s*'?([^\n']+)", out)
        if m:
            banner = m.group(1).strip()
        vulnerable = "is vulnerable" in out or "identified the following injection" in out
        results.append({"url": url, "vulnerable": vulnerable, "banner": banner, "rc": rc})
        if vulnerable:
            log(f"    !! {url} — podatny (banner: {banner})")
    return results


# ---------------------------------------------------------------- faza E

def phase_e(domain: str, args, services: list[dict], nuclei: dict) -> tuple[int, str]:
    log("FAZA E — korelacja CVE <-> exploit (cve_correlator.py)")
    corr = HERE / "cve_correlator.py"
    if not corr.is_file():
        err("brak cve_correlator.py obok target_profile.py — pomijam faze E")
        return 1, ""
    cmd = [sys.executable, str(corr), "--domain", domain,
           "--out", str(args.out / domain)]
    nmap_file = args.workdir / "nmap.txt"
    if nmap_file.is_file():
        cmd += ["--nmap", str(nmap_file)]
    nucl = args.workdir / "nuclei_tech.jsonl"
    if nucl.is_file():
        cmd += ["--nuclei", str(nucl)]
    if args.msf:
        cmd += ["--msf"]
    rc, out = sh(cmd, timeout=args.timeout)
    return rc, out


# ---------------------------------------------------------------- karta

def write_dossier(domain: str, info: dict, services: list[dict],
                  nuclei: dict, sqlmap: list[dict], args) -> Path:
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.workdir
    today = utc_now()

    lines: list[str] = []
    lines.append("---")
    lines.append(f'title: "{domain} — dossier I-V-E (auto)"')
    lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("tags: [ive, dossier, recon, pentest, autorun]")
    lines.append(f"domain: {domain}")
    lines.append("status: active")
    lines.append("---")
    lines.append("")
    lines.append(f"# {domain} — dossier I-V-E")
    lines.append("")
    lines.append(f"> Wygenerowane automatycznie przez `target_profile.py` — {today}.")
    lines.append("> Flow: [[Model_IVE/IVE_MOC]] · korelacja CVE: [[Narzedzia/IVE_Automatyzacja]]")
    lines.append("")

    # --- I
    lines.append("## I — Informacja")
    lines.append("")
    lines.append("| Źródło | Liczba |")
    lines.append("|--------|-------:|")
    lines.append(f"| Emails | {len(info['emails'])} |")
    lines.append(f"| Hosty / subdomeny | {len(info['hosts'])} |")
    lines.append(f"| IP | {len(info['ips'])} |")
    lines.append(f"| Ludzie | {len(info['people'])} |")
    lines.append(f"| Credentials (OSINT) | {len(info['credentials'])} |")
    lines.append("")
    if info["emails"]:
        lines.append("**Emaile:** " + ", ".join(info["emails"][:30]))
        lines.append("")
    if info["hosts"]:
        lines.append("**Hosty:**")
        lines.append("")
        lines.append("| Host | IP | Moduł |")
        lines.append("|------|----|-------|")
        for h in info["hosts"][:50]:
            lines.append(f"| {h['host']} | {h['ip']} | {h['module']} |")
        lines.append("")
    if info["ips"]:
        lines.append("**IP:** " + ", ".join(info["ips"][:30]))
        lines.append("")

    # --- V
    lines.append("## V — Podatności")
    lines.append("")
    if services:
        lines.append("### Otwarte usługi (nmap -sV)")
        lines.append("")
        lines.append("| Port | Service | Wersja |")
        lines.append("|------|---------|--------|")
        for s in services:
            lines.append(f"| {s['port']}/{s['proto']} | {s['service']} | {s['version']} |")
        lines.append("")
    techs = {f["matcher"] for f in nuclei.get("findings", []) if f.get("matcher")}
    if techs:
        lines.append("### Technologie (nuclei tech-detect)")
        lines.append("")
        lines.append(", ".join(sorted(techs)))
        lines.append("")
    sev = {}
    for f in nuclei.get("findings", []):
        sev[f["severity"]] = sev.get(f["severity"], 0) + 1
    if sev:
        lines.append("### Podsumowanie nuclei")
        lines.append("")
        lines.append("| Severity | Liczba |")
        lines.append("|----------|-------:|")
        for k in sorted(sev):
            lines.append(f"| {k} | {sev[k]} |")
        lines.append("")
    if sqlmap:
        lines.append("### Cele SQLi (sqlmap)")
        lines.append("")
        lines.append("| URL | Podatny | Banner |")
        lines.append("|-----|---------|--------|")
        for r in sqlmap:
            yes = "**TAK**" if r["vulnerable"] else "nie"
            lines.append(f"| `{r['url']}` | {yes} | {r['banner']} |")
        lines.append("")
    if not services and not techs and not sqlmap:
        lines.append("_Brak znalezisk — sprawdź surowe outputy w `raw/`._")
        lines.append("")

    # --- E
    lines.append("## E — Eksploatacja")
    lines.append("")
    plan = out_dir / domain / "exploit_plan.md"
    if plan.is_file():
        try:
            rel = plan.resolve().relative_to(args.vault.resolve())
            plan_link = str(rel.with_suffix(""))
        except ValueError:
            plan_link = f"{domain}/exploit_plan"
        lines.append(f"Karty z planem: zobacz [[{plan_link}]] oraz karty `cve_*` "
                     "w tym folderze.")
        lines.append("")
        lines.append("> Uruchom ponownie `cve_correlator.py` po każdej zmianie wersji "
                     "znalezionych w fazie V.")
        lines.append("")
    else:
        lines.append("_Brak kart exploit-plan (korelacja nie wykryła CVE albo nie "
                     "uruchomiono `cve_correlator.py`)._\n")

    # --- surowe outputy
    lines.append("## Surowe outputy")
    lines.append("")
    for p in sorted(raw_dir.iterdir(), key=lambda x: x.name):
        if not p.is_file():
            continue
        name = p.name
        try:
            rel = p.resolve().relative_to(args.vault.resolve())
            link = str(rel) if rel.suffix != ".md" else str(rel.with_suffix(""))
        except ValueError:
            link = f"raw/{name}"
        lines.append(f"- [[{link}|{name}]]")
    lines.append("")

    lines.append("## Polecenie")
    lines.append("")
    lines.append("```bash")
    lines.append(" ".join(sys.argv))
    lines.append("```")
    lines.append("")

    card = out_dir / f"{domain}.md"
    tmp = card.with_suffix(".md.tmp")
    tmp.write_text("\n".join(lines), encoding="utf-8")
    tmp.replace(card)
    log(f"dossier: {card}")
    return card


# ---------------------------------------------------------------- main

def check_tools() -> None:
    print("Narzędzia I-V-E:")
    for t in TOOLS:
        found = find_tool(t)
        where = "PATH" if found == [] else (f"docker:{KALI_CONTAINER}" if found else "BRAK")
        print(f"  {t:<14} {where}")
    vault = find_vault()
    print(f"vault: {vault}")
    print(f"katalog wynikow: {vault / 'Projekty' / 'Recon'}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Orchestrator recon I-V-E dla jednej domeny → karta Obsidian.")
    ap.add_argument("--domain", default=None, help="domena docelowa (np. xmask.lab)")
    ap.add_argument("--out", help="katalog kart Obsidian (domyślnie <vault>/Projekty/Recon)")
    ap.add_argument("--workdir", help="katalog surowych outputów (domyślnie <out>/<domain>/raw)")
    ap.add_argument("--sources", default=HARVESTER_SOURCES_DEFAULT,
                    help="źródła theHarvester (domyślnie %(default)s)")
    ap.add_argument("--limit", type=int, default=200, help="limit wyników theHarvester")
    ap.add_argument("--skip", action="append", default=[],
                    choices=["theharvester", "nuclei", "nmap", "sqlmap", "exploit"],
                    help="pomiń fazę/narzędzie")
    ap.add_argument("--nuclei-all", action="store_true",
                    help="dodatkowo pełny skan nuclei (severity>=medium) na celach web")
    ap.add_argument("--nuclei-templates", default=os.environ.get("NUCLEI_TEMPLATES", ""),
                    help="katalog szablonów nuclei")
    ap.add_argument("--urls", help="plik z dodatkowymi URL-ami (cele web/sqlmap)")
    ap.add_argument("--max-ips", type=int, default=32, help="maks. IP do nmap")
    ap.add_argument("--max-web-targets", type=int, default=12)
    ap.add_argument("--max-sqlmap", type=int, default=10)
    ap.add_argument("--timeout", type=int, default=600,
                    help="timeout (s) na pojedyncze narzędzie")
    ap.add_argument("--msf", action="store_true",
                    help="włącz szukanie modułów w msfconsole w fazie E")
    ap.add_argument("--dry-run", action="store_true",
                    help="tylko pokaż plan i sprawdź narzędzia")
    ap.add_argument("--check-tools", action="store_true",
                    help="sprawdź dostępność narzędzi i wyjdź")
    a = ap.parse_args()

    if a.check_tools:
        check_tools()
        return 0
    if not a.domain:
        ap.error("--domain jest wymagane (oprócz --check-tools)")

    vault = find_vault()
    out = Path(a.out) if a.out else vault / "Projekty" / "Recon"
    workdir = Path(a.workdir) if a.workdir else out / a.domain / "raw"
    a.vault = vault
    a.out = out
    a.workdir = workdir
    workdir.mkdir(parents=True, exist_ok=True)

    skip = set(a.skip)
    log(f"domena={a.domain} vault={vault}")
    log(f"karta:      {out / (a.domain + '.md')}")
    log(f"raw:        {workdir}")

    if a.dry_run:
        print("\nPlan (dry-run):")
        print(f"  I  theHarvester -d {a.domain} -b {a.sources} -l {a.limit} -t")
        print(f"  V  nuclei tech-detect  -> {workdir / 'nuclei_tech.jsonl'}")
        if not tool_missing("nmap"):
            print(f"  V  nmap -Pn -sV --script default,http-title,http-headers (do {a.max_ips} IP)")
        if not tool_missing("sqlmap"):
            print(f"  V  sqlmap --batch --smart --banner na URL z parametrami (max {a.max_sqlmap})")
        print(f"  E  cve_correlator.py --nmap raw/nmap.txt --nuclei raw/nuclei_tech.jsonl")
        return 0

    info: dict = {"hosts": [], "ips": [], "emails": [], "people": [], "credentials": []}
    if "theharvester" not in skip:
        info = phase_i(a.domain, a)
    else:
        log("pominięto theHarvester (--skip)")
    # domena zawsze w puli IP, jesli da sie ja rozwiazac
    for ip in resolve_host(a.domain):
        if ip not in info["ips"]:
            info["ips"].append(ip)

    targets: list[str] = []
    if "nuclei" not in skip or "sqlmap" not in skip:
        targets = web_targets(a.domain, info, a)
        log(f"cele web: {len(targets)}")

    nuclei: dict = {"template": "tech-detect", "findings": []}
    if "nuclei" not in skip:
        nuclei = phase_v_nuclei(a.domain, targets, a)
    else:
        log("pominięto nuclei (--skip)")

    services: list[dict] = []
    if "nmap" not in skip:
        services = phase_v_nmap(info, a)
    else:
        log("pominięto nmap (--skip)")

    sqlmap: list[dict] = []
    if "sqlmap" not in skip:
        sqlmap = phase_v_sqlmap(targets, a)
    else:
        log("pominięto sqlmap (--skip)")

    if "exploit" not in skip:
        phase_e(a.domain, a, services, nuclei)
    else:
        log("pominięto korelację CVE (--skip exploit)")

    card = write_dossier(a.domain, info, services, nuclei, sqlmap, a)
    print(f"\nGOTOWE: karta {card}")
    print(f"        surowe outputy: {workdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
