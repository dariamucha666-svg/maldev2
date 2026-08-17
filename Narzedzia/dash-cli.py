#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI do dashboardu IOC — statystyki, os czasu, filtry, wykresy ASCII, raporty.

Dane: katalog raportow pipeline (te same *.json co build_dashboard_history.py).
Jesli w katalogu jest history.json, timeline go uzywa.

Uzycie:
  python3 dash-cli.py stats   --reports DIR
  python3 dash-cli.py timeline [--days N] --reports DIR
  python3 dash-cli.py filter  [--role rat] [--kind pe] [--family F] [--packer P]
                             [--since 2026-08-01] [--until 2026-08-16] [--ioc 1.2.3.4]
                             [--limit 30] [--json] --reports DIR
  python3 dash-cli.py chart   --metric roles|kind|family|daily|packer [--top 8] --reports DIR
  python3 dash-cli.py iocs    [--type ip|url|domain|hash] [--top 15] --reports DIR
  python3 dash-cli.py report  <sha256|name> [--html] [--pdf] [--out plik] --reports DIR

PDF: raport HTML konwertowany, gdy dostepny jest wkhtmltopdf / weasyprint / chromium.
"""
from __future__ import annotations

import argparse, json, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

IP_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path):
    try:
        d = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        return d if isinstance(d, dict) else None
    except Exception:
        return None

def collect(reports_dir: Path):
    """Zwraca liste probek (dict) z raportow; dopelnia z iocs.json."""
    samples = []
    if not reports_dir.is_dir():
        print("brak katalogu raportow: %s" % reports_dir)
        return samples
    for path in sorted(reports_dir.glob("*.json")):
        if path.name == "iocs.json" or ".features" in path.name:
            continue
        data = load_json(path)
        if not data:
            continue
        f = data.get("file") or {}
        sha = (f.get("sha256") or "").lower() if isinstance(f, dict) else ""
        if not sha:
            continue
        cls = data.get("classification") or {}
        samples.append({
            "sha256": sha,
            "name": (f.get("name") or path.stem) if isinstance(f, dict) else path.stem,
            "analyzed_at": str(data.get("analyzed_at") or ""),
            "day": str(data.get("analyzed_at") or "")[:10],
            "kind": data.get("kind") or (str(f.get("type") or "")[:4]),
            "role": cls.get("role") or data.get("role") or "unknown",
            "family": cls.get("family") or "",
            "reasons": cls.get("reasons") or [],
            "yara": [m["rule"] for m in (data.get("yara") or []) if isinstance(m, dict)],
            "packer": data.get("packer_hints") or [],
            "iocs": data.get("strings_ioc") or {},
            "suspicious": data.get("suspicious_apis") or {},
        })
    agg = load_json(reports_dir / "iocs.json")
    if agg and isinstance(agg.get("samples"), list):
        known = {s["sha256"] for s in samples}
        for e in agg["samples"]:
            sha = str(e.get("sha256") or "").lower()
            if not sha or sha in known:
                continue
            samples.append({
                "sha256": sha, "name": str(e.get("name") or sha[:12]),
                "analyzed_at": str(e.get("analyzed_at") or ""),
                "day": str(e.get("analyzed_at") or "")[:10],
                "kind": str(e.get("kind") or "?"),
                "role": str(e.get("role") or "unknown"),
                "family": str(e.get("family") or ""),
                "reasons": [], "yara": e.get("yara") or [], "packer": e.get("packer") or [],
                "iocs": e.get("iocs") or {}, "suspicious": {},
            })
    return samples

def bar(value, maxv, width=30):
    if maxv <= 0:
        return ""
    n = int(round(value / maxv * width))
    return "#" * n

def fmt_day(day):
    return day if day else "????-??-??"

# ---------------------------------------------------------------- subcommands
def cmd_stats(a, samples):
    total = len(samples)
    roles = Counter(s["role"] for s in samples)
    kinds = Counter(s["kind"] for s in samples)
    fams = Counter(s["family"] for s in samples if s["family"])
    packers = Counter()
    for s in samples:
        for p in s["packer"]:
            packers[p.split("(")[0].strip()] += 1
    ioc_count = Counter()
    for s in samples:
        for t, vals in s["iocs"].items():
            ioc_count[t] += len(vals)
    yara_hits = sum(1 for s in samples if s["yara"])
    print("=== Statystyki pipeline ===\n")
    print("Probki: %d | z dopasowaniem YARA: %d | z IoC: %d" % (total, yara_hits, sum(1 for s in samples if any(s["iocs"].values()))))
    print("\nRole:")
    for k, v in roles.most_common():
        print("  %-14s %3d  %s" % (k, v, bar(v, max(roles.values()))))
    print("\nTyp (kind):")
    for k, v in kinds.most_common():
        print("  %-6s %3d  %s" % (str(k)[:6], v, bar(v, max(kinds.values()))))
    if fams:
        print("\nRodziny:")
        for k, v in fams.most_common(10):
            print("  %-20s %3d" % (k[:20], v))
    if packers:
        print("\nPacker heurystyki:")
        for k, v in packers.most_common(10):
            print("  %-30s %3d" % (k[:30], v))
    if ioc_count:
        print("\nIoC typy:")
        for k, v in ioc_count.most_common():
            print("  %-10s %3d" % (k, v))
    return 0

def cmd_timeline(a, samples):
    days = Counter(s["day"] for s in samples)
    if not days:
        print("brak danych"); return 0
    mx = max(days.values())
    print("=== Os czasu (ostatnie %s dni) ===" % (a.days if a.days else "wszystkie"))
    for day in sorted(days):
        if a.days and (datetime.now().date() - datetime.strptime(day, "%Y-%m-%d").date()).days > a.days:
            continue
        print("  %s | %s %d" % (day, bar(days[day], mx), days[day]))
    return 0

def cmd_filter(a, samples):
    def ok(s):
        if a.role and s["role"] != a.role:
            return False
        if a.kind and s["kind"] != a.kind:
            return False
        if a.family and a.family.lower() not in s["family"].lower():
            return False
        if a.packer and not any(a.packer.lower() in p.lower() for p in s["packer"]):
            return False
        if a.since and s["day"] < a.since:
            return False
        if a.until and s["day"] > a.until:
            return False
        if a.ioc:
            blob = json.dumps(s["iocs"], ensure_ascii=False)
            if a.ioc.lower() not in blob.lower():
                return False
        return True
    hits = [s for s in samples if ok(s)]
    if a.json:
        slim = [{k: s[k] for k in ("sha256", "name", "role", "kind", "day", "family", "yara", "packer")} for s in hits[:a.limit]]
        print(json.dumps(slim, ensure_ascii=False, indent=2))
        return 0
    print("=== Filtr: %d probek ===" % len(hits))
    print("%-13s %-28s %-12s %-6s %-10s %s" % ("sha256", "nazwa", "rola", "kind", "dzien", "yara"))
    for s in hits[:a.limit]:
        print("%-13s %-28s %-12s %-6s %-10s %s" % (s["sha256"][:12], s["name"][:28], s["role"][:12],
                                                   str(s["kind"])[:6], fmt_day(s["day"]),
                                                   ",".join(s["yara"][:2])))
    return 0

def cmd_chart(a, samples):
    if a.metric == "roles":
        data = Counter(s["role"] for s in samples)
    elif a.metric == "kind":
        data = Counter(str(s["kind"]) for s in samples)
    elif a.metric == "family":
        data = Counter(s["family"] for s in samples if s["family"])
    elif a.metric == "packer":
        data = Counter()
        for s in samples:
            for p in s["packer"]:
                data[p.split("(")[0].strip()] += 1
    elif a.metric == "daily":
        data = Counter(s["day"] for s in samples)
    else:
        print("nieznana metryka"); return 1
    if not data:
        print("brak danych"); return 0
    mx = max(data.values())
    print("=== Wykres: %s ===" % a.metric)
    for k, v in data.most_common(a.top):
        print("  %-24s %s %d" % (str(k)[:24], bar(v, mx), v))
    return 0

def cmd_iocs(a, samples):
    bucket = defaultdict(list)
    type_map = {"ip": "ips", "url": "urls", "domain": "domains", "hash": "sha256"}
    for s in samples:
        for t, vals in s["iocs"].items():
            if a.type and type_map.get(a.type) != t:
                continue
            for v in vals:
                bucket[t].append((v, s["role"], s["sha256"][:12], s["day"]))
    print("=== Najczestsze IoC ===")
    for t, rows in bucket.items():
        print("\n[%s] (%d unikalnych)" % (t, len(set(r[0] for r in rows))))
        for v, role, sha, day in sorted(rows, key=lambda r: -1)[:a.top]:
            print("  %-45s %-12s %s %s" % (str(v)[:45], role, sha, day))
    return 0

def cmd_report(a, samples):
    needle = a.needle.lower()
    hit = None
    for s in samples:
        if s["sha256"].startswith(needle) or needle in s["name"].lower() or needle in s["sha256"]:
            hit = s
            break
    if not hit:
        print("brak probki: %s" % a.needle); return 1
    if a.html or a.pdf:
        html = render_html(hit)
        out = Path(a.out or (hit["sha256"][:12] + ".html"))
        out.write_text(html, encoding="utf-8")
        print("[*] HTML -> %s" % out)
        if a.pdf:
            conv = None
            for cand in ("wkhtmltopdf", "weasyprint", "chromium", "chromium-browser", "google-chrome"):
                if shutil.which(cand):
                    conv = cand
                    break
            if conv in ("wkhtmltopdf",):
                r = subprocess.run([conv, str(out), str(out.with_suffix(".pdf"))], capture_output=True, text=True)
                print("[*] PDF -> %s" % out.with_suffix(".pdf") if r.returncode == 0 else "[!] wkhtmltopdf: %s" % r.stderr[:300])
            elif conv in ("chromium", "chromium-browser", "google-chrome"):
                r = subprocess.run([conv, "--headless", "--disable-gpu", "--print-to-pdf=" + str(out.with_suffix(".pdf")), str(out)], capture_output=True, text=True)
                print("[*] PDF -> %s" % out.with_suffix(".pdf") if r.returncode == 0 else "[!] %s" % r.stderr[:300])
            elif conv == "weasyprint":
                r = subprocess.run([conv, str(out), str(out.with_suffix(".pdf"))], capture_output=True, text=True)
                print("[*] PDF -> %s" % out.with_suffix(".pdf") if r.returncode == 0 else "[!] %s" % r.stderr[:300])
            else:
                print("[!] brak konwertera PDF — zainstaluj wkhtmltopdf albo otworz HTML w przegladarce i wydrukuj")
        return 0
    print(render_md(hit))
    return 0

# ---------------------------------------------------------------- render
def render_md(s):
    L = []
    L.append("# %s (raport)\n" % s["name"])
    L.append("| Pole | Wartosc |")
    L.append("|------|---------|")
    L.append("| SHA256 | %s |" % s["sha256"])
    L.append("| Rola | %s |" % s["role"])
    L.append("| Rodzina | %s |" % (s["family"] or "-"))
    L.append("| Kind | %s |" % s["kind"])
    L.append("| Dzien | %s |" % fmt_day(s["day"]))
    L.append("| YARA | %s |" % (", ".join(s["yara"]) or "-"))
    L.append("| Packer | %s |" % ("; ".join(s["packer"][:3]) or "-"))
    L.append("")
    L.append("## Powody klasyfikacji")
    L.append("")
    for r in s["reasons"]:
        L.append("- " + r)
    L.append("")
    L.append("## IoC")
    for t, vals in s["iocs"].items():
        L.append("- **%s** (%d): %s" % (t, len(vals), ", ".join(str(v) for v in vals[:20])))
    if s["suspicious"]:
        L.append("")
        L.append("## Podejrzane API")
        for cat, apis in s["suspicious"].items():
            L.append("- **%s**: %s" % (cat, ", ".join(apis[:12])))
    return "\n".join(L) + "\n"

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def render_html(s):
    md = render_md(s)
    body = []
    body.append("<h1>%s</h1>" % esc(s["name"]))
    body.append("<table>")
    for k in ("sha256", "role", "family", "kind", "day"):
        body.append("<tr><th>%s</th><td>%s</td></tr>" % (k, esc(s[k]) if k != "day" else esc(fmt_day(s[k]))))
    body.append("<tr><th>YARA</th><td>%s</td></tr>" % esc(", ".join(s["yara"]) or "-"))
    body.append("<tr><th>Packer</th><td>%s</td></tr>" % esc("; ".join(s["packer"][:3]) or "-"))
    body.append("</table>")
    body.append("<h2>Powody klasyfikacji</h2><ul>")
    for r in s["reasons"]:
        body.append("<li>%s</li>" % esc(r))
    body.append("</ul>")
    body.append("<h2>IoC</h2>")
    for t, vals in s["iocs"].items():
        body.append("<h3>%s (%d)</h3><ul>" % (esc(t), len(vals)))
        for v in vals[:30]:
            body.append("<li><code>%s</code></li>" % esc(v))
        body.append("</ul>")
    if s["suspicious"]:
        body.append("<h2>Podejrzane API</h2>")
        for cat, apis in s["suspicious"].items():
            body.append("<p><b>%s</b>: %s</p>" % (esc(cat), esc(", ".join(apis[:12]))))
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'><title>%s</title>"
            "<style>body{font-family:monospace;margin:40px;color:#111}"
            "table{border-collapse:collapse}td,th{border:1px solid #999;padding:4px 8px;text-align:left}"
            "code{background:#eee;padding:1px 3px}</style></head><body>%s</body></html>"
            % (esc(s["name"]), "\n".join(body)))
    return html

def main():
    ap = argparse.ArgumentParser(description="CLI dashboardu IOC")
    ap.add_argument("--reports", default=os.environ.get("PIPELINE_REPORTS", "reports"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("stats")
    p2 = sub.add_parser("timeline"); p2.add_argument("--days", type=int, default=0)
    p3 = sub.add_parser("filter"); p3.add_argument("--role"); p3.add_argument("--kind")
    p3.add_argument("--family"); p3.add_argument("--packer"); p3.add_argument("--since"); p3.add_argument("--until")
    p3.add_argument("--ioc"); p3.add_argument("--limit", type=int, default=30); p3.add_argument("--json", action="store_true")
    p4 = sub.add_parser("chart"); p4.add_argument("--metric", choices=["roles", "kind", "family", "daily", "packer"], required=True)
    p4.add_argument("--top", type=int, default=8)
    p5 = sub.add_parser("iocs"); p5.add_argument("--type", choices=["ip", "url", "domain", "hash"]); p5.add_argument("--top", type=int, default=15)
    p6 = sub.add_parser("report"); p6.add_argument("needle"); p6.add_argument("--html", action="store_true")
    p6.add_argument("--pdf", action="store_true"); p6.add_argument("--out")
    a = ap.parse_args()
    samples = collect(Path(a.reports))
    if not samples:
        print("brak probek w %s" % a.reports); return 1
    if a.cmd == "stats":
        return cmd_stats(a, samples)
    if a.cmd == "timeline":
        return cmd_timeline(a, samples)
    if a.cmd == "filter":
        return cmd_filter(a, samples)
    if a.cmd == "chart":
        return cmd_chart(a, samples)
    if a.cmd == "iocs":
        return cmd_iocs(a, samples)
    if a.cmd == "report":
        return cmd_report(a, samples)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
