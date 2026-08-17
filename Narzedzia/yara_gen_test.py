#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator + tester regul YARA.

generate — tworzy regule z probki (markery: URL/IP/API/ciekawe stringi) lub z raportu pipeline:
    python3 yara_gen_test.py generate --sample probka.exe [--name Nazwa] [--family Rodzina]
                                      [--c2 "host:port,host2:port"] [--markers "s1,s2"] [--out DIR]
    python3 yara_gen_test.py generate --report raport.json [--out DIR]

test — macierz pomylek (precision/recall/F1) dla regul z --rules na korpusie:
    python3 yara_gen_test.py test --rules DIR --corpus DIR
                                  [--labels labels.json]   # {"sha256": "family"} gdy korpus plaski
    Korpus w strukturze: corpus/<family>/*.exe ; katalog "benign"/"unknown" = oczekiwany brak dopasowania.

scan — pojedyncza probka vs reguly:
    python3 yara_gen_test.py scan --rules DIR --sample probka.exe
"""
from __future__ import annotations

import argparse, datetime, glob, hashlib, json, os, re, subprocess, sys
from pathlib import Path

YARA_BIN = os.environ.get("YARA_BIN", "/usr/bin/yara")
IP_RE = re.compile(r"(?<!\d)(\d{1,3}\.){3}\d{1,3}(?!\d)")
URL_RE = re.compile(r"https?://[A-Za-z0-9./_?=&:%+~#@-]+")
DOM_RE = re.compile(r"(?<![A-Za-z0-9.])([a-z0-9][a-z0-9-]{0,62}\.)+([a-z]{2,63})(?![A-Za-z0-9.-])")
INTEREST_RE = re.compile(r"(http|https|api|token|secret|key|passw|login|onion|wallet|pool|xmr|monero|stratum|"
                         r"cryptonight|randomx|\.exe|powershell|cmd\.exe|/bin/sh|/bin/bash|reverse|bind|listen|"
                         r"upload|download|screenshot|keylog|bot|telegram|discord|mysql|postgres|ssh|rdp|"
                         r"\.onion|bitcoin|ethereum|bip39|CreateProcess|VirtualAlloc|RegSetValue|GetAsyncKey|"
                         r"WriteProcessMemory|CreateRemoteThread|WinHttp|URLDownload)", re.I)
SKIP_STRINGS = {"!this program cannot be run in dos mode.", ".text", ".data", ".rdata", ".pdata", ".bss",
                ".idata", ".reloc", ".tls", ".rsrc", ".crt"}

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return ((r.stdout or "") + (r.stderr or "")).strip()

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def pick_markers(strings, limit=10, minlen=6):
    """Wybierz najlepsze markery: najpierw IoC/markery, potem dlugie unikalne stringi."""
    out, seen = [], set()
    def add(s):
        s2 = s.strip()
        low = s2.lower()
        if not s2 or len(s2) < minlen or len(s2) > 140 or low in seen or low in SKIP_STRINGS:
            return
        if any(ch.isspace() for ch in s2) and len(s2) > 60:
            return
        seen.add(low)
        out.append(s2)
    # priorytet: URL / IP / domena / markery
    for s in strings:
        if URL_RE.search(s) or IP_RE.search(s) or DOM_RE.search(s) or INTEREST_RE.search(s):
            add(s)
    if len(out) < 3:
        for s in sorted(strings, key=len, reverse=True):
            add(s)
    return out[:limit]

def rule_text(name, sha, kind, markers, family="", extra_meta=None, threshold=None):
    if len(markers) < 2:
        return None
    magic = ("uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550"
             if kind == "pe" else "uint32(0) == 0x464C457F")
    meta = ["description = \"Auto-detekcja: %s\"" % name,
            "hash = \"%s\"" % sha,
            "author = \"XMask lab\"",
            "date = \"%s\"" % datetime.date.today().isoformat()]
    if family:
        meta.insert(1, "family = \"%s\"" % family)
    if extra_meta:
        for k, v in extra_meta.items():
            meta.append("%s = \"%s\"" % (k, v))
    lines = []
    for i, m in enumerate(markers, 1):
        esc = m.replace("\\", "\\\\").replace('"', '\\"')
        lines.append("        $a%d = \"%s\" ascii wide" % (i, esc))
    if threshold is None:
        threshold = max(2, (len(markers) + 1) // 2)
    return ("rule %s\n{\n    meta:\n%s\n    strings:\n%s\n    condition:\n"
            "        %s and %d of ($a*)\n}\n" %
            (name, "".join("        %s\n" % x for x in meta), "\n".join(lines) + "\n",
             magic, threshold))

def kind_of(path):
    out = sh("file -b '" + path + "'")
    if "PE32" in out:
        return "pe"
    if "ELF" in out:
        return "elf"
    return "?"

def cmd_generate(a):
    strings, sha, family = [], "", a.family or ""
    kind = a.kind
    if a.report:
        data = json.loads(Path(a.report).read_text(encoding="utf-8", errors="replace"))
        sha = (data.get("file") or {}).get("sha256") or ""
        kind = a.kind if a.kind and a.kind != "auto" else data.get("kind", "?")
        family = family or (data.get("classification") or {}).get("family") or ""
        iocs = data.get("strings_ioc") or {}
        strings = list(iocs.get("urls") or []) + list(iocs.get("ips") or []) + list(iocs.get("domains") or [])
        strings += data.get("interesting_strings") or []
        if not a.name:
            a.name = re.sub(r"[^A-Za-z0-9_.-]", "_", (data.get("file") or {}).get("name") or "sample")
    elif a.sample:
        if not os.path.isfile(a.sample):
            print("brak pliku: " + a.sample); return 1
        sha = sha256_file(a.sample)
        kind = a.kind if a.kind and a.kind != "auto" else kind_of(a.sample)
        raw = sh("'" + os.environ.get("STRINGS_BIN", "/usr/bin/strings") + "' -n 5 '" + a.sample + "'")
        strings = [l for l in raw.splitlines() if l]
        if not a.name:
            a.name = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(a.sample))
    else:
        print("podaj --sample lub --report"); return 1

    markers = pick_markers(strings)
    if a.c2:
        markers = [m.strip() for m in a.c2.split(",") if m.strip()] + markers
    if a.markers:
        markers = [m.strip() for m in a.markers.split(",") if m.strip()] + markers
    markers = markers[:10]

    rname = a.rule_name or ("Auto_%s_%s" % ("PE" if kind == "pe" else "ELF", sha[:12]))
    text = rule_text(rname, sha, kind, markers, family, extra_meta=a.meta)
    if not text:
        print("za malo markerow — dodaj --markers lub --c2"); return 1
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / (rname + ".yar")
    dest.write_text(text, encoding="utf-8")
    print("[*] regula: %s" % dest)
    print("[*] markery (%d): %s" % (len(markers), ", ".join(markers[:10])))
    if sha:
        print("[*] sha256: %s" % sha)
    return 0

# ---------------------------------------------------------------- test
def load_labels(corpus: Path, labels_path) -> dict:
    """Zwraca {sha256: family}. Korpus <family>/* albo --labels json."""
    fam = {}
    if labels_path and Path(labels_path).exists():
        try:
            d = json.loads(Path(labels_path).read_text(encoding="utf-8"))
            for k, v in (d.items() if isinstance(d, dict) else []):
                fam[str(k).lower()] = str(v)
        except Exception as e:
            print("UWAGA: labels.json: %s" % e)
    if corpus.is_dir():
        for sub in sorted(p for p in corpus.iterdir() if p.is_dir()):
            for f in sub.iterdir():
                if f.is_file():
                    sha = sha256_file(str(f))
                    fam.setdefault(sha, sub.name)
    elif corpus.is_file():
        print("--corpus musi byc katalogiem (corpus/<family>/ lub plaski + --labels)")
        sys.exit(1)
    return fam

def rule_family(text: str, name: str) -> str:
    m = re.search(r"family\s*=\s*['\"]([^'\"]+)['\"]", text)
    if m:
        return m.group(1).lower()
    return name  # regula bez rodziny = jej wlasna "rodzina"

def cmd_test(a):
    rules_dir = Path(a.rules)
    corpus = Path(a.corpus)
    if not rules_dir.is_dir():
        print("brak katalogu regul: %s" % rules_dir); return 1
    if not corpus.is_dir():
        print("brak katalogu korpusu: %s" % corpus); return 1
    labels = load_labels(corpus, a.labels)
    rule_files = sorted(glob.glob(str(rules_dir / "*.yar")))
    if not rule_files:
        print("brak regul *.yar w %s" % rules_dir); return 1
    rules = []
    for rf in rule_files:
        text = Path(rf).read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"rule\s+([A-Za-z0-9_]+)\s*\{", text):
            rules.append({"file": rf, "name": m.group(1), "family": rule_family(text, m.group(1).lower()),
                          "text": text})
    if not rules:
        print("nie sparsowano zadnych regul"); return 1

    samples = sorted(f for f in corpus.rglob("*") if f.is_file() and not f.name.endswith((".json", ".md")))
    matched = {}   # rule_name -> set(sha)
    for s in samples:
        sha = sha256_file(str(s))
        out = sh("%s -w %s '%s'" % (YARA_BIN, " ".join("'%s'" % f for f in rule_files), s))
        for line in out.splitlines():
            rn = line.split()[0].strip()
            matched.setdefault(rn, set()).add(sha)

    print("[*] regul: %d | probek w korpusie: %d | z etykieta: %d" % (len(rules), len(samples), len(labels)))
    rows = []
    for r in rules:
        hits = matched.get(r["name"], set())
        fam_samps = {sha for sha, f in labels.items() if f.lower() == r["family"]}
        benign = {sha for sha, f in labels.items() if f.lower() in ("benign", "unknown", "clean")}
        tp = len(hits & fam_samps)
        fp = len(hits - fam_samps)
        fn = len(fam_samps - hits)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        rows.append({"name": r["name"], "family": r["family"], "tp": tp, "fp": fp, "fn": fn,
                     "precision": precision, "recall": recall, "f1": f1,
                     "fp_samples": sorted(hits - fam_samps)[:5]})
    rows.sort(key=lambda x: -x["f1"])

    lines = []
    lines.append("# Test regul YARA — %s\n" % datetime.date.today().isoformat())
    lines.append("| Regula | Rodzina | TP | FP | FN | Precision | Recall | F1 |")
    lines.append("|--------|---------|----|----|----|-----------|--------|----|")
    for r in rows:
        lines.append("| %s | %s | %d | %d | %d | %.2f | %.2f | %.2f |" %
                     (r["name"], r["family"], r["tp"], r["fp"], r["fn"],
                      r["precision"], r["recall"], r["f1"]))
        if r["fp_samples"]:
            lines.append("  FP: " + ", ".join(s[:12] for s in r["fp_samples"]))
    lines.append("")
    tp = sum(r["tp"] for r in rows); fp = sum(r["fp"] for r in rows); fn = sum(r["fn"] for r in rows)
    lines.append("**Suma**: TP=%d FP=%d FN=%d" % (tp, fp, fn))
    print("\n".join(lines))
    if a.out:
        Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("[*] wyniki -> %s" % a.out)
    return 0

def cmd_scan(a):
    rules_dir = Path(a.rules)
    if not os.path.isfile(a.sample):
        print("brak pliku: " + a.sample); return 1
    files = sorted(glob.glob(str(rules_dir / "*.yar")))
    if not files:
        print("brak regul"); return 1
    out = sh("%s -s -w %s '%s'" % (YARA_BIN, " ".join("'%s'" % f for f in files), a.sample))
    if not out:
        print("[*] brak dopasowan"); return 0
    for line in out.splitlines():
        print("  " + line)
    return 0

def main():
    ap = argparse.ArgumentParser(description="Generator + tester regul YARA")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--sample"); g.add_argument("--report")
    g.add_argument("--name"); g.add_argument("--family"); g.add_argument("--kind", choices=["pe", "elf", "auto"], default="auto")
    g.add_argument("--c2"); g.add_argument("--markers"); g.add_argument("--out", default="generated_rules")
    g.add_argument("--rule-name"); g.add_argument("--meta", action="append", default=[],
                                                  help="dodatkowe meta k=v (moze byc wielokrotnie)")
    t = sub.add_parser("test"); t.add_argument("--rules", required=True); t.add_argument("--corpus", required=True)
    t.add_argument("--labels"); t.add_argument("--out")
    s = sub.add_parser("scan"); s.add_argument("--rules", required=True); s.add_argument("--sample", required=True)
    a = ap.parse_args()
    if a.cmd == "generate":
        return cmd_generate(a)
    if a.cmd == "test":
        return cmd_test(a)
    if a.cmd == "scan":
        return cmd_scan(a)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
