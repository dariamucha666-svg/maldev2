#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline auto-analizy PE/ELF (statyczna).

Kroki: pobranie (MalwareBazaar) -> triage -> naglowki PE (pefile) / ELF (parser wbudowany)
       -> sekcje + entropia -> importy/symbole -> strings -> IoC -> klasyfikacja roli
       -> YARA -> regula YARA -> karta Obsidian -> raport JSON -> iocs.json.

Format raportu JSON jest zgodny z pipeline APK (analyze_apk.py):
  - file.sha256 / file.name / analyzed_at / classification.role
  - dodatkowe sekcje: pe|elf, strings_ioc, suspicious_apis, yara, entropy, packer_hints

Uzycie:
  python3 analyze_pe.py --file /sciezka/plik.exe [--out /katalog/wynikow] [--yara-rules DIR]
  python3 analyze_pe.py --hash <sha256>            # pobiera z MalwareBazaar (klucz ~/.mb_api_key)
"""
from __future__ import annotations

import argparse, datetime, glob, hashlib, json, math, os, re, shutil, struct, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

try:
    import pefile
except ImportError:
    pefile = None

MB_KEY = os.path.expanduser("~/.mb_api_key")
YARA_BIN = os.environ.get("YARA_BIN", "/usr/bin/yara")
STRINGS_BIN = os.environ.get("STRINGS_BIN", "/usr/bin/strings")

SUSPICIOUS = {
    "injection": ["createremotethread", "virtualallocex", "writeprocessmemory", "setthreadcontext",
                  "ntcreatethreadex", "queueuserapc", "rtlcreateuserthread", "ntmapviewofsection"],
    "persistence": ["regsetvalueex", "createservice", "openscmanager", "scheduledtask"],
    "evasion": ["isdebuggerpresent", "checkremotedebuggerpresent", "virtualprotect", "ntsetinformationthread",
                "setunhandledexceptionfilter", "outputdebugstring", "ntqueryinformationprocess"],
    "crypto": ["cryptencrypt", "cryptdecrypt", "bcryptencrypt", "bcryptgenrandom", "cryptacquirecontext",
               "cryptgenkey", "cryptimportkey", "cryptexportkey"],
    "keylog": ["getasynckeystate", "setwindowshookex", "getkeystate", "mapvirtualkey", "getkeyboardstate"],
    "screenshot": ["bitblt", "getdc", "createdc", "createcompatibledc", "getsystemmetrics"],
    "network": ["wsastartup", "connect", "send", "recv", "winhttpopen", "urldownloadtofile", "internetopen",
                "httpsendrequest", "wininet", "getaddrinfo", "socket"],
    "shell": ["createprocess", "winexec", "shellexecute", "cmd.exe", "powershell", "ntcreatesection"],
    "steal": ["getclipboarddata", "openclipboard", "enumprocesses", "readprocessmemory", "findfirstfile",
              "credentials", "password", "login", "cookies", "autofill"],
}
# kanoniczne (bez przyrostka W/A) nazwy API -> kategoria
_API_CAT = {}
for _cat, _apis in SUSPICIOUS.items():
    for _a in _apis:
        _API_CAT[_a.rstrip("wa")] = _cat

IP_RE = re.compile(r"(?<!\d)(\d{1,3}\.){3}\d{1,3}(?!\d)")
URL_RE = re.compile(r"https?://[A-Za-z0-9./_?=&:%+~#@-]+")
TLDS = ("com net org io ru xyz top cyou online site app lol gg click link space monster life store shop biz info "
        "co uk de fr pl eu in cf gq ml tk ga press world vip club fun me tv cc su pro cloud dev app tech").split()
DOM_RE = re.compile(r"(?<![A-Za-z0-9.])([a-z0-9][a-z0-9-]{0,62}\.)+([a-z]{2,63})(?![A-Za-z0-9.-])")
INTEREST_RE = re.compile(r"(http|https|api|token|secret|key|passw|login|onion|wallet|pool|xmr|monero|stratum|"
                         r"cryptonight|randomx|\.exe|powershell|cmd\.exe|/bin/sh|/bin/bash|reverse|bind|listen|"
                         r"upload|download|screenshot|keylog|bot|telegram|discord|mysql|postgres|ssh|rdp)", re.I)

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return ((r.stdout or "") + (r.stderr or "")).strip()

def log(msg):
    print("[*] " + msg, flush=True)

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def shannon(data):
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    e = 0.0
    for c in counts:
        if c:
            p = c / n
            e -= p * math.log2(p)
    return round(e, 4)

def valid_ip(s):
    try:
        parts = s.split(".")
        if len(parts) != 4:
            return False
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False

def download_mb(sha):
    """Pobiera probke z MalwareBazaar (dziala tez dla PE; zwraca rozpakowany plik)."""
    log("pobieram " + sha[:12] + " z MalwareBazaar")
    key = open(MB_KEY).read().strip()
    data = urllib.parse.urlencode({"query": "get_file", "sha256_hash": sha}).encode()
    req = urllib.request.Request("https://mb-api.abuse.ch/api/v1/", data=data, headers={"Auth-Key": key})
    r = urllib.request.urlopen(req, timeout=60).read()
    wp = "/tmp/_mb_wrap_pe.zip"
    open(wp, "wb").write(r)
    if os.path.exists("/tmp/_mb_x"):
        shutil.rmtree("/tmp/_mb_x")
    os.makedirs("/tmp/_mb_x")
    sh("cd /tmp/_mb_x && 7z x -pinfected -y " + wp + " >/dev/null 2>&1")
    inner = glob.glob("/tmp/_mb_x/*")
    if not inner:
        raise SystemExit("brak pliku w archiwum MalwareBazaar — sprawdz hash")
    dst = "/tmp/" + sha + ".bin"
    shutil.move(inner[0], dst)
    return dst

# ---------------------------------------------------------------- PE
def pe_flags(chars):
    flag_bits = [
        (0x00000020, "CODE"), (0x00000040, "IDATA"), (0x00000080, "UDATA"),
        (0x00000004, "INIT"), (0x00000008, "UNINIT"), (0x20000000, "EXEC"),
        (0x80000000, "WRITE"), (0x40000000, "READ"),
    ]
    return " ".join(n for b, n in flag_bits if chars & b)

def analyze_pe(path):
    pe = pefile.PE(path, fast_load=True)
    info = {}
    fh = pe.FILE_HEADER
    info["machine"] = pefile.MACHINE_TYPE.get(fh.Machine, hex(fh.Machine))
    info["timestamp"] = datetime.datetime.fromtimestamp(fh.TimeDateStamp, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if fh.TimeDateStamp else ""
    info["is_dll"] = bool(pe.is_dll())
    oh = pe.OPTIONAL_HEADER
    info["subsystem"] = pefile.SUBSYSTEM_TYPE.get(getattr(oh, "Subsystem", 0), "?")
    try:
        info["entrypoint"] = hex(oh.AddressOfEntryPoint)
    except Exception:
        info["entrypoint"] = "?"

    pe.parse_data_directories()

    sections = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("utf-8", errors="replace")
        try:
            ent = shannon(s.get_data())
        except Exception:
            ent = 0.0
        sections.append({
            "name": name, "virtual_size": int(s.Misc_VirtualSize), "raw_size": int(s.SizeOfRawData),
            "entropy": ent, "flags": pe_flags(s.Characteristics),
            "executable": bool(s.Characteristics & 0x20000000),
            "writable": bool(s.Characteristics & 0x80000000),
        })
    info["sections"] = sections

    imports = {}
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode("utf-8", errors="replace") if isinstance(entry.dll, bytes) else str(entry.dll)
            apis = []
            for imp in entry.imports:
                if imp.name:
                    apis.append(imp.name.decode("utf-8", errors="replace"))
            imports[dll] = sorted(set(apis))
    info["imports"] = imports

    exports = []
    if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if sym.name:
                exports.append(sym.name.decode("utf-8", errors="replace"))
    info["exports"] = sorted(set(exports))[:200]

    try:
        ov = pe.get_overlay_data_start_offset()
        info["overlay_size"] = max(0, os.path.getsize(path) - ov) if ov else 0
    except Exception:
        info["overlay_size"] = 0

    info["tls_callbacks"] = 0
    if hasattr(pe, "DIRECTORY_ENTRY_TLS") and pe.DIRECTORY_ENTRY_TLS:
        try:
            info["tls_callbacks"] = 1 if pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks else 0
        except Exception:
            pass

    cats = {}
    for dll, apis in imports.items():
        for api in apis:
            cat = _API_CAT.get(api.rstrip("WAwa").lower())
            if cat:
                cats.setdefault(cat, []).append(api)
    for k in cats:
        cats[k] = sorted(set(cats[k]))
    info["suspicious_api"] = cats

    hints = []
    names = [s["name"].lower() for s in sections]
    if any(n.startswith(".upx") for n in names):
        hints.append("UPX (sekcje .UPX*)")
    if info["overlay_size"] > 200 * 1024:
        hints.append("duzy overlay (%d B — dane doklejone po ostatniej sekcji)" % info["overlay_size"])
    if sections and max(s["entropy"] for s in sections) > 7.2:
        hints.append("wysoka entropia sekcji (>7.2 — prawdopodobnie pakowane/szyfrowane)")
    if imports and len(imports) < 4:
        hints.append("malo importow (%d DLL) — mozliwy packer" % len(imports))
    if info["tls_callbacks"]:
        hints.append("TLS callbacks — anty-debug / wczesny kod")
    info["packer_hints"] = hints
    pe.close()
    return info

# ---------------------------------------------------------------- ELF
ELF_MACHINES = {
    0x02: "SPARC", 0x03: "i386", 0x08: "MIPS", 0x14: "PowerPC", 0x16: "S390", 0x28: "ARM",
    0x2A: "SuperH", 0x3E: "x86-64", 0xB7: "AArch64", 0xF3: "RISC-V",
}

def analyze_elf(path):
    data = open(path, "rb").read()
    if data[:4] != b"\x7fELF":
        raise ValueError("to nie jest ELF")
    is64 = data[4] == 2
    endian = "<" if data[5] == 1 else ">"
    info = {}
    info["class"] = "ELF64" if is64 else "ELF32"
    info["endian"] = "LE" if endian == "<" else "BE"
    e_type = struct.unpack_from(endian + "H", data, 16)[0]
    info["type"] = {1: "REL", 2: "EXEC", 3: "DYN", 4: "CORE"}.get(e_type, hex(e_type))
    info["machine"] = ELF_MACHINES.get(struct.unpack_from(endian + "H", data, 18)[0], "?")
    info["entrypoint"] = hex(struct.unpack_from(endian + ("Q" if is64 else "I"), data, 0x18)[0])

    if is64:
        shoff = struct.unpack_from(endian + "Q", data, 0x28)[0]
        shentsize = struct.unpack_from(endian + "H", data, 0x3A)[0]
        shnum = struct.unpack_from(endian + "H", data, 0x3C)[0]
        shstrndx = struct.unpack_from(endian + "H", data, 0x3E)[0]
        ents = 64
    else:
        shoff = struct.unpack_from(endian + "I", data, 0x20)[0]
        shentsize = struct.unpack_from(endian + "H", data, 0x2E)[0]
        shnum = struct.unpack_from(endian + "H", data, 0x30)[0]
        shstrndx = struct.unpack_from(endian + "H", data, 0x32)[0]
        ents = 40

    sections = []
    shstr = None
    if shnum and shentsize:
        if shstrndx < shnum:
            base = shoff + shstrndx * ents
            off = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x18 if is64 else 0x10))[0]
            size = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x20 if is64 else 0x14))[0]
            shstr = data[off:off + size]
        for i in range(shnum):
            base = shoff + i * ents
            name_off = struct.unpack_from(endian + "I", data, base)[0]
            name = "?"
            if shstr is not None:
                end = shstr.find(b"\x00", name_off)
                name = shstr[name_off:end].decode("utf-8", errors="replace") if end > name_off else "?"
            flags = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + 0x08)[0]
            sec_off = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x18 if is64 else 0x10))[0]
            sec_size = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x20 if is64 else 0x14))[0]
            ent = shannon(data[sec_off:sec_off + sec_size]) if 0 < sec_size < 100 * 1024 * 1024 else 0.0
            sections.append({
                "name": name, "size": sec_size, "entropy": ent,
                "executable": bool(flags & 0x4), "writable": bool(flags & 0x1),
            })
    info["sections"] = sections

    sym_off = sym_size = str_off = str_size = dyn_off = dyn_size = None
    for i in range(shnum):
        base = shoff + i * ents
        name_off = struct.unpack_from(endian + "I", data, base)[0]
        name = "?"
        if shstr is not None:
            end = shstr.find(b"\x00", name_off)
            name = shstr[name_off:end].decode("utf-8", errors="replace") if end > name_off else "?"
        sec_off = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x18 if is64 else 0x10))[0]
        sec_size = struct.unpack_from(endian + ("Q" if is64 else "I"), data, base + (0x20 if is64 else 0x14))[0]
        if name == ".dynsym":
            sym_off, sym_size = sec_off, sec_size
        elif name == ".dynstr":
            str_off, str_size = sec_off, sec_size
        elif name == ".dynamic":
            dyn_off, dyn_size = sec_off, sec_size

    libs = []
    if dyn_off is not None and str_off is not None:
        dtag = 8 if is64 else 4
        for p in range(dyn_off, dyn_off + dyn_size, dtag):
            tag, val = struct.unpack_from(endian + ("q" if is64 else "i") + ("Q" if is64 else "I"), data, p)
            if tag == 1:  # DT_NEEDED
                end = data.find(b"\x00", str_off + val)
                if end > str_off + val:
                    libs.append(data[str_off + val:end].decode("utf-8", errors="replace"))

    imports = []
    if sym_off is not None and str_off is not None:
        ents2 = 24 if is64 else 16
        for p in range(sym_off, sym_off + sym_size, ents2):
            name_off = struct.unpack_from(endian + "I", data, p)[0]
            st_info = data[p + (4 if is64 else 12)]
            shndx = struct.unpack_from(endian + "H", data, p + (6 if is64 else 14))[0]
            if name_off and shndx == 0 and (st_info & 0xF) in (2, 10):
                end = data.find(b"\x00", str_off + name_off)
                if end > str_off + name_off:
                    imports.append(data[str_off + name_off:end].decode("utf-8", errors="replace"))
    info["imports"] = sorted(set(imports))
    info["linked_libs"] = libs

    hints = []
    secnames = [s["name"].lower() for s in sections]
    if any(n.startswith(".upx") for n in secnames) or b"UPX!" in data[0x100:0x200]:
        hints.append("UPX")
    if sections and max((s["entropy"] for s in sections), default=0) > 7.2:
        hints.append("wysoka entropia sekcji (>7.2)")
    if "go build" in data[:2_000_000].decode("utf-8", errors="ignore"):
        hints.append("Go runtime (nazwy pakietow w .rdata)")
    info["packer_hints"] = hints

    m = re.search(rb"GNU\x00\x02\x00\x00\x00(\x01|\x03)\x00\x00\x00(.{16})", data[:65536], re.S)
    info["build_id"] = m.group(2).hex() if m else ""
    return info

# ---------------------------------------------------------------- wspolne
def extract_strings(path, minlen):
    out = sh("'%s' -n %d '%s'" % (STRINGS_BIN, minlen, path))
    return [l for l in out.splitlines() if l]

def extract_iocs(strings):
    ips, urls, doms = [], [], []
    for s in strings:
        for m in IP_RE.finditer(s):
            ip = m.group(0)
            if valid_ip(ip):
                ips.append(ip)
        for m in URL_RE.finditer(s):
            urls.append(m.group(0))
        for m in DOM_RE.finditer(s):
            d = m.group(0).lower().rstrip(".")
            if d.split(".")[-1] in TLDS and not d.startswith(("http://", "https://")) and not valid_ip(d):
                doms.append(d)
    return {
        "ips": sorted(set(ips)),
        "urls": sorted(set(urls)),
        "domains": sorted(set(doms)),
    }

def interesting_strings(strings, limit=60):
    out = []
    for s in strings:
        if INTEREST_RE.search(s) and len(s) < 200:
            out.append(s)
        if len(out) >= limit:
            break
    return out

def classify(pe, elf, iocs, strings):
    """Zwraca (rola, confidence, powody). Prosty klasyfikator regulowy."""
    blob = " ".join(strings).lower()
    reasons = []
    cats = (pe or {}).get("suspicious_api", {})
    has = lambda k: k in cats and bool(cats[k])

    if any(w in blob for w in ("stratum", "xmr", "monero", "randomx", "cryptonight", "pool.mine", "nicehash")):
        return "cryptominer", 0.9, ["markery miningu w stringach"]
    if has("keylog") and (has("network") or has("injection")):
        reasons.append("keylogger + siec/injection")
        return "rat", 0.85, reasons
    if has("screenshot") and has("network"):
        reasons.append("screenshot + siec")
        return "rat", 0.8, reasons
    if has("keylog"):
        reasons.append("keylogger (bez sieci)")
        return "keylogger", 0.7, reasons
    if "reverse shell" in blob or ("cmd.exe" in blob and has("network")):
        reasons.append("reverse-shell markery")
        return "backdoor", 0.85, reasons
    if has("injection") and has("network"):
        reasons.append("injection + API sieciowe")
        return "backdoor", 0.7, reasons
    if has("injection") and has("persistence"):
        reasons.append("injection + persistence")
        return "backdoor", 0.65, reasons
    if has("network") and (has("shell") or has("persistence")):
        reasons.append("siec + shell/persistence")
        return "backdoor", 0.6, reasons
    if has("crypto") and has("steal"):
        reasons.append("krypto + kradziez danych")
        return "stealer", 0.8, reasons
    if any(w in blob for w in ("wallet", "bitcoin", "ethereum", "bip39", "seed phrase")):
        return "clipper", 0.6, ["markery portfela"]
    if has("network") and ("urldownloadtofile" in blob or "download" in blob):
        reasons.append("pobieranie plikow")
        return "dropper", 0.6, reasons
    if iocs and (iocs["urls"] or iocs["ips"]) and not cats:
        return "unknown", 0.3, ["IoC sieciowe, brak sygnatur API"]
    return "unknown", 0.2, ["brak silnych sygnatur"]

def scan_yara(rules_dir, path):
    if not os.path.isdir(rules_dir):
        return []
    results = []
    for yf in sorted(glob.glob(os.path.join(rules_dir, "*.yar"))):
        out = sh("%s -s -w '%s' '%s'" % (YARA_BIN, yf, path))
        if not out:
            continue
        rule = None
        for line in out.splitlines():
            if re.match(r"^0x[0-9a-f]+:", line):
                m = re.search(r"\$([A-Za-z0-9_]+):", line)
                if rule is not None:
                    results[-1]["strings"].append(m.group(1) if m else line.strip())
            elif line.strip():
                rule = line.split()[0].strip()
                results.append({"rule": rule, "file": yf, "strings": []})
    return results

def gen_yara_rule(name, sha, strings, kind, family=""):
    """Generuje regule YARA dla probki (markery + magic). Zwraca tekst reguly albo None."""
    markers = []
    seen = set()
    for s in strings:
        s2 = s.strip()
        if not s2 or len(s2) < 5 or len(s2) > 120:
            continue
        key = s2.lower()
        if key in seen:
            continue
        seen.add(key)
        markers.append(s2)
        if len(markers) >= 8:
            break
    if len(markers) < 2:
        return None
    magic = ("uint16(0) == 0x5A4D and uint32(uint32(0x3C)) == 0x00004550"
             if kind == "pe" else "uint32(0) == 0x464C457F")
    lines = []
    for i, m in enumerate(markers, 1):
        esc = m.replace("\\", "\\\\").replace('"', '\\"')
        lines.append("        $a%d = \"%s\" ascii wide" % (i, esc))
    n = max(2, (len(markers) + 1) // 2)
    meta = ["description = \"Auto-detekcja: %s\"" % name,
            "hash = \"%s\"" % sha,
            "author = \"XMask lab\"",
            "date = \"%s\"" % datetime.date.today().isoformat()]
    if family:
        meta.insert(1, "family = \"%s\"" % family)
    return ("rule Auto_%s_%s\n{\n    meta:\n%s\n    strings:\n%s\n    condition:\n"
            "        %s and %d of ($a*)\n}\n" %
            (("PE" if kind == "pe" else "ELF"), sha[:12],
             "".join("        %s\n" % x for x in meta),
             "\n".join(lines) + "\n", magic, n))

def write_card(out, name, sha, kind, ftype, size,
               pe, elf, iocs, role, family,
               yara, strings_sample, reasons):
    d = datetime.date.today().isoformat()
    lines = []
    lines.append("---\ntitle: \"%s — auto-analiza\"\ndate: %s\ntags: [sample, %s, auto, malware, analysis]\n"
                 "status: pending\nsha256: %s\nrole: %s\n---\n" % (name, d, kind, sha, role))
    lines.append("# %s (auto)\n" % name)
    lines.append("| Pole | Wartosc |\n|------|---------|")
    lines.append("| SHA256 | %s |" % sha)
    lines.append("| Typ | %s |" % ftype)
    lines.append("| Rozmiar | %d B |" % size)
    lines.append("| Rola | %s |" % role)
    if family:
        lines.append("| Rodzina | %s |" % family)
    lines.append("| Analizowane | %s |\n" % utc_now())

    if pe:
        lines.append("## PE\n")
        lines.append("- Maszyna: %s | DLL: %s | Subsystem: %s" % (pe["machine"], pe["is_dll"], pe["subsystem"]))
        lines.append("- Kompilacja: %s | EntryPoint: %s | Overlay: %d B" % (pe["timestamp"], pe["entrypoint"], pe["overlay_size"]))
        lines.append("- Sekcje:")
        for s in pe["sections"]:
            lines.append("  - **%s** ent=%s exec=%s wr=%s (%d B)" % (s["name"], s["entropy"], s["executable"], s["writable"], s["raw_size"]))
        lines.append("- Importy (%d DLL):" % len(pe["imports"]))
        for dll, apis in sorted(pe["imports"].items())[:10]:
            lines.append("  - %s: %s" % (dll, ", ".join(apis[:12])))
        if pe["exports"]:
            lines.append("- Eksporty: %s" % ", ".join(pe["exports"][:15]))
        if pe.get("suspicious_api"):
            lines.append("- Podejrzane API:")
            for cat, apis in pe["suspicious_api"].items():
                lines.append("  - **%s**: %s" % (cat, ", ".join(apis[:12])))
        lines.append("")
    elif elf:
        lines.append("## ELF\n")
        lines.append("- Klasa: %s (%s) | Maszyna: %s | Typ: %s | Entry: %s" % (elf["class"], elf["endian"], elf["machine"], elf["type"], elf["entrypoint"]))
        lines.append("- Sekcje:")
        for s in elf["sections"]:
            if s["size"] > 0:
                lines.append("  - **%s** ent=%s exec=%s wr=%s (%d B)" % (s["name"], s["entropy"], s["executable"], s["writable"], s["size"]))
        if elf["imports"]:
            lines.append("- Symbole UND (importy): %s" % ", ".join(elf["imports"][:40]))
        if elf["linked_libs"]:
            lines.append("- Biblioteki: %s" % ", ".join(elf["linked_libs"]))
        lines.append("")

    hints = (pe or elf or {}).get("packer_hints", [])
    if hints:
        lines.append("## Packer / heurystyki\n")
        lines.append("\n".join("- " + h for h in hints) + "\n")

    lines.append("## Klasyfikacja\n")
    lines.append("- Rola: **%s**" % role)
    lines.append("- Powody: " + "; ".join(reasons) + "\n")

    lines.append("## IoC\n")
    lines.append("- IP: " + ", ".join(iocs["ips"][:20]) if iocs["ips"] else "- IP: brak")
    lines.append("- URL: " + ", ".join(iocs["urls"][:20]) if iocs["urls"] else "- URL: brak")
    lines.append("- Domeny: " + ", ".join(iocs["domains"][:20]) if iocs["domains"] else "- Domeny: brak")
    lines.append("")

    if yara:
        lines.append("## YARA (istniejace reguly)\n")
        for m in yara:
            lines.append("- **%s** (%d stringow)" % (m["rule"], len(m["strings"])))
        lines.append("")

    if strings_sample:
        lines.append("## Ciekawe stringi\n")
        lines.append("~~~\n" + "\n".join(strings_sample[:40]) + "\n~~~\n")
    return "\n".join(lines) + "\n"

def upsert_iocs(out, report):
    """Dopisz/uzupelnij raport w iocs.json (agregat). Zwraca zaktualizowany agregat."""
    ioc_path = Path(out) / "iocs.json"
    agg = {"generated": utc_now(), "samples": []}
    if ioc_path.exists():
        try:
            agg = json.loads(ioc_path.read_text(encoding="utf-8"))
        except Exception:
            agg = {"generated": utc_now(), "samples": []}
    if "samples" not in agg:
        agg["samples"] = []
    f = report["file"]
    entry = {
        "sha256": f["sha256"],
        "name": f["name"],
        "kind": report.get("kind"),
        "analyzed_at": report.get("analyzed_at", ""),
        "role": (report.get("classification") or {}).get("role", "unknown"),
        "family": (report.get("classification") or {}).get("family", ""),
        "iocs": report.get("strings_ioc", {}),
        "yara": [m["rule"] for m in report.get("yara", [])],
        "packer": report.get("packer_hints", [])[:3],
    }
    agg["samples"] = [s for s in agg["samples"] if s.get("sha256") != f["sha256"]]
    agg["samples"].append(entry)
    agg["generated"] = utc_now()
    ioc_path.write_text(json.dumps(agg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return agg

def main():
    ap = argparse.ArgumentParser(description="Auto-analiza PE/ELF (statyczna)")
    ap.add_argument("--file", help="sciezka do probki")
    ap.add_argument("--hash", help="sha256 — pobiera z MalwareBazaar")
    ap.add_argument("--out", default="/tmp/pe_analysis", help="katalog wynikow")
    ap.add_argument("--yara-rules", default=os.path.dirname(os.path.abspath(__file__)),
                    help="katalog z regulami *.yar do skanowania")
    ap.add_argument("--min-strings", type=int, default=5)
    ap.add_argument("--no-yara", action="store_true")
    a = ap.parse_args()

    if a.hash:
        path = download_mb(a.hash)
    elif a.file:
        path = a.file
    else:
        print("podaj --file lub --hash"); return 1
    if not os.path.isfile(path):
        print("brak pliku: " + path); return 1

    sha = sha256_file(path)
    size = os.path.getsize(path)
    ftype = sh("file -b '" + path + "'")
    kind = "pe" if ("PE32" in ftype or "PE32+" in ftype) else ("elf" if "ELF" in ftype else "?")
    out = a.out
    os.makedirs(out, exist_ok=True)
    log("triage: sha256=%s | typ: %s | rozmiar: %d" % (sha, ftype, size))
    sh("file '" + path + "' > " + out + "/file.txt")

    pe = elf = None
    if kind == "pe":
        if pefile is None:
            print("brak modulu pefile — zainstaluj: pip install pefile"); return 1
        log("analiza PE (pefile)")
        try:
            pe = analyze_pe(path)
        except Exception as e:
            log("UWAGA: pefile nie poradzil sobie: %s" % e)
    elif kind == "elf":
        log("analiza ELF (parser wbudowany)")
        try:
            elf = analyze_elf(path)
        except Exception as e:
            log("UWAGA: parser ELF: %s" % e)
    else:
        log("UWAGA: nieznany format — tylko strings + YARA")

    log("strings + IoC")
    strings = extract_strings(path, a.min_strings)
    iocs = extract_iocs(strings)
    log("IoC: %d IP | %d URL | %d domen" % (len(iocs["ips"]), len(iocs["urls"]), len(iocs["domains"])))

    role, conf, reasons = classify(pe, elf, iocs, strings)
    log("rola: %s (conf %.2f)" % (role, conf))

    yara_matches = []
    if not a.no_yara:
        log("YARA (reguly z %s)" % a.yara_rules)
        yara_matches = scan_yara(a.yara_rules, path)
        log("dopasowania: %d" % len(yara_matches))

    family = ""
    for m in yara_matches:
        fam = re.search(r"family\s*=\s*['\"]([^'\"]+)['\"]", open(m["file"], errors="replace").read())
        if fam:
            family = fam.group(1); break

    name = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.basename(path))
    # do reguly YARA preferuj stringi z markerami (URL/IP/API), generyczne jako fallback
    markers = interesting_strings(strings, 40) or strings
    rule = gen_yara_rule(name, sha, markers, kind, family)
    if rule:
        open(os.path.join(out, "Auto_%s_%s.yar" % ("PE" if kind == "pe" else "ELF", sha[:12])), "w").write(rule)
        log("regula YARA zapisana")

    report = {
        "analyzed_at": utc_now(),
        "file": {"name": os.path.basename(path), "sha256": sha, "size": size, "type": ftype},
        "kind": kind,
        "classification": {"role": role, "family": family, "confidence": conf, "reasons": reasons},
        "strings_ioc": iocs,
        "yara": [{"rule": m["rule"], "strings": m["strings"][:20]} for m in yara_matches],
        "suspicious_apis": (pe or {}).get("suspicious_api", {}),
        "packer_hints": (pe or elf or {}).get("packer_hints", []),
        "entropy_max": max([s["entropy"] for s in (pe or elf or {}).get("sections", [])], default=0.0),
        "interesting_strings": interesting_strings(strings),
    }
    if pe:
        report["pe"] = pe
    if elf:
        report["elf"] = elf

    rpath = os.path.join(out, sha[:12] + ".json")
    open(rpath, "w").write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    card = write_card(out, name, sha, kind, ftype, size, pe, elf, iocs, role, family,
                      yara_matches, report["interesting_strings"], reasons)
    open(os.path.join(out, sha[:12] + ".md"), "w").write(card)
    upsert_iocs(out, report)

    log("WYNIKI: %s" % out)
    log("raport: %s | karta: %s.md | iocs.json zaktualizowany" % (rpath, os.path.join(out, sha[:12])))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
