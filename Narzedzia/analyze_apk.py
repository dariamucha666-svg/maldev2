#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline auto-analizy APK (statyczna).
Kroki: pobranie (MalwareBazaar) -> triage -> packer (apkid) -> odzysk manifestu (fake-encryption)
       -> manifest (androguard) -> dekompilacja (jadx) -> IoC (IP/URL/domeny)
       -> podejrzane API -> scoring ryzyka -> YARA -> karta Obsidian ("co robi ta apka").

Uzycie:
  python3 analyze_apk.py --apk /sciezka/plik.apk [--out /katalog/wynikow]
  python3 analyze_apk.py --hash <sha256>            # pobiera z MalwareBazaar (klucz ~/.mb_api_key)
"""
import argparse, base64, datetime, glob, hashlib, os, re, shutil, struct, subprocess, sys, urllib.parse, urllib.request, zipfile, zlib

TOOLS = {"apkid": "/opt/retools/bin/apkid", "androguard": "/opt/retools/bin/androguard", "jadx": "/opt/jadx/bin/jadx"}
MB_KEY = os.path.expanduser("~/.mb_api_key")

# ---------------------------------------------------------------- sygnatury API
# (wzor, opis) — co dana konstrukcja robi w praktyce (na bazie notatek dropperow/bankerow).
API_SIGNATURES = [
    ("addJavascriptInterface", "WebView: mostek JS<->Java — typowy mechanizm phishingu / overlay (droppery WebView)"),
    ("setJavaScriptEnabled", "WebView z JS — wymagane do phishingu / overlay / wstrzykiwania JS"),
    (r"loadUrl\s*\(\s*\"javascript:", "wstrzykiwanie JS przez loadUrl(javascript:...)"),
    ("DexClassLoader", "dynamiczne ladowanie kodu — drugi etap / dropper"),
    ("PathClassLoader", "dynamiczne ladowanie klas — loader"),
    (r"Runtime\.getRuntime\(\).*exec|Runtime\.exec", "wykonywanie komend powloki"),
    ("ProcessBuilder", "uruchamianie procesow systemowych"),
    ("getDeviceId", "zbieranie IMEI / identyfikatora urzadzenia"),
    ("getSubscriberId", "zbieranie IMSI"),
    ("getLine1Number", "zbieranie numeru telefonu"),
    ("sendTextMessage", "wysylanie SMS — stealer OTP / premium SMS"),
    ("SmsManager", "dostep do SMS (czytanie/wysylanie)"),
    ("REQUEST_INSTALL_PACKAGES", "instalacja APK z zewnatrz — dropper"),
    ("PackageInstaller", "instalacja APK z poziomu apki — dropper"),
    ("AccessibilityService", "usluga dostepnosci — RAT/banker: overlay, czytanie ekranu, keylog"),
    ("onAccessibilityEvent", "obsluga zdarzen dostepnosci"),
    ("TYPE_APPLICATION_OVERLAY", "overlay nad innymi apkami — banker (fake login)"),
    ("FLAG_WINDOW_OVERLAY", "okno nakladkowe — overlay"),
    ("ClipboardManager", "dostep do schowka"),
    ("OnPrimaryClipChangedListener", "monitorowanie schowka — clipper"),
    ("NfcAdapter", "dostep do NFC — skimmer (a710209e)"),
    ("enableReaderMode", "tryb czytnika NFC — skimmer"),
    (r"Cipher\.getInstance", "kryptografia — ukrywanie payload / konfiguracji / C2"),
    ("Base64.decode", "dekodowanie danych — payload / konfig / C2"),
    ("SecretKeySpec", "klucze AES — szyfrowanie danych"),
    (r"new Socket\s*\(", "surowy socket — niestandardowa komunikacja C2"),
    ("HttpURLConnection", "siec (HTTP)"),
    ("OkHttpClient", "siec (OkHttp/Retrofit) — REST C2"),
    ("WebSocket", "WebSocket — C2 (kira/clayrat)"),
    ("ptrace", "anty-debug / anty-RE (Zirex-style)"),
    ("Frida", "wykrywanie Frida / anty-RE"),
    (r"/proc/self/maps", "czytanie map pamieci — anty-RE / unpacking"),
    ("loadLibrary", "ladowanie natywnych bibliotek (.so)"),
    ("TelephonyManager", "dostep do telefonii — fingerprint urzadzenia"),
    ("getInstalledPackages", "enumeracja zainstalowanych apki — target list bankera"),
    ("queryIntentActivities", "enumeracja apki — wybor celu overlay"),
    ("KeyChain", "dostep do keystore / certyfikatow"),
    ("setFlags(FLAG_SECURE", "blokada zrzutow ekranu — anty-analiza"),
    ("takePicture", "zdjecia z kamery"),
    ("MediaRecorder", "nagrywanie audio / wideo"),
]

# ------------------------------------------------------------- wagi uprawnien
# nazwa (bez android.permission.) -> punkty ryzyka
PERM_RISK = {
    "SMS": 8, "READ_SMS": 8, "RECEIVE_SMS": 8, "SEND_SMS": 7,
    "READ_PHONE_STATE": 5, "READ_PHONE_NUMBERS": 5,
    "READ_CONTACTS": 5, "READ_CALL_LOG": 6,
    "RECORD_AUDIO": 8, "CAMERA": 6,
    "ACCESS_FINE_LOCATION": 6, "ACCESS_COARSE_LOCATION": 4,
    "READ_EXTERNAL_STORAGE": 4, "WRITE_EXTERNAL_STORAGE": 5,
    "MANAGE_EXTERNAL_STORAGE": 9, "SYSTEM_ALERT_WINDOW": 9,
    "REQUEST_INSTALL_PACKAGES": 9, "QUERY_ALL_PACKAGES": 6,
    "PACKAGE_USAGE_STATS": 7, "BIND_ACCESSIBILITY_SERVICE": 9,
    "FOREGROUND_SERVICE": 3, "GET_ACCOUNTS": 5,
    "RECEIVE_BOOT_COMPLETED": 3, "NFC": 5,
    "INTERNET": 1, "ACCESS_NETWORK_STATE": 1, "ACCESS_WIFI_STATE": 1,
    "VIBRATE": 1, "WAKE_LOCK": 1, "POST_NOTIFICATIONS": 1,
    "REQUEST_IGNORE_BATTERY_OPTIMIZATIONS": 6, "GET_TASKS": 4,
    "USE_BIOMETRIC": 2, "USE_FINGERPRINT": 3,
    "READ_MEDIA_IMAGES": 2, "READ_MEDIA_VIDEO": 2, "READ_MEDIA_AUDIO": 2,
}

def risk_level(score):
    if score >= 35: return "KRYTYCZNY"
    if score >= 20: return "wysoki"
    if score >= 10: return "sredni"
    return "niski"

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return ((r.stdout or "") + (r.stderr or "")).strip()

def log(msg):
    print("[*] " + msg, flush=True)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def download_mb(sha):
    log("pobieram " + sha[:12] + " z MalwareBazaar")
    key = open(MB_KEY).read().strip()
    data = urllib.parse.urlencode({"query": "get_file", "sha256_hash": sha}).encode()
    req = urllib.request.Request("https://mb-api.abuse.ch/api/v1/", data=data, headers={"Auth-Key": key})
    r = urllib.request.urlopen(req, timeout=60).read()
    wp = "/tmp/_mb_wrap.zip"
    open(wp, "wb").write(r)
    if os.path.exists("/tmp/_mb_x"):
        shutil.rmtree("/tmp/_mb_x")
    os.makedirs("/tmp/_mb_x")
    sh("cd /tmp/_mb_x && 7z x -pinfected -y " + wp + " >/dev/null 2>&1")
    inner = glob.glob("/tmp/_mb_x/*")[0]
    dst = "/tmp/" + sha + ".apk"
    shutil.move(inner, dst)
    return dst

def recover_manifest(apk):
    z = zipfile.ZipFile(apk)
    try:
        return z.read("AndroidManifest.xml"), True
    except Exception:
        pass
    info = z.getinfo("AndroidManifest.xml")
    with open(apk, "rb") as f:
        f.seek(info.header_offset)
        lh = f.read(30)
        nlen = struct.unpack("<H", lh[26:28])[0]
        elen = struct.unpack("<H", lh[28:30])[0]
        f.seek(info.header_offset + 30 + nlen + elen)
        raw = f.read(info.compress_size)
    for data in (raw, raw[12:]):
        try:
            return zlib.decompress(data, -15), False
        except Exception:
            continue
    return None, False

def extract(apk, out):
    log("rozpakowuje APK")
    os.makedirs(out, exist_ok=True)
    sh("cd " + out + " && unzip -o -q " + apk + " 2>/dev/null")
    axml, ok = recover_manifest(apk)
    if not ok and axml:
        open(out + "/AndroidManifest.xml", "wb").write(axml)
        log("  -> manifest odzyskany (fake-encryption trick)")
    elif axml is None:
        log("  -> UWAGA: manifest nieczytelny (prawdziwy packer?)")

def decode_manifest(axml, out):
    sh(TOOLS["androguard"] + " axml " + axml + " > " + out + "/manifest.xml 2>/dev/null")
    return out + "/manifest.xml"

def parse_manifest(mf):
    t = open(mf, errors="replace").read()
    pkg = re.search(r'package="([^"]+)"', t)
    perms = sorted(set(re.findall(r'android.permission.([A-Z_]+)', t)))
    svc = sorted(set(re.findall(r'<service[^>]*android:name="([^"]+)"', t)))
    recv = sorted(set(re.findall(r'<receiver[^>]*android:name="([^"]+)"', t)))
    acts = sorted(set(re.findall(r'<activity[^>]*android:name="([^"]+)"', t)))
    return (pkg.group(1) if pkg else "?"), perms, svc, recv, acts

def ioc_from_strings(out):
    alls = sh("cd " + out + " && (cat classes*.dex 2>/dev/null || cat classes.dex 2>/dev/null) | strings -n 5 2>/dev/null")
    ips = sorted(set(re.findall(r'\b(\d{1,3}\.){3}\d{1,3}\b', alls)))
    urls = sorted(set(re.findall(r'https?://[a-zA-Z0-9./_?=&:%-]+', alls)))
    doms = sorted(set(re.findall(r'[a-z0-9.-]+\.(com|net|io|ru|xyz|top|cyou|online|site|app|lol|gg|click|link|space|monster|life|store|shop)', alls)))
    return ips, urls, doms

# ------------------------------------------------------------------ nowe: API
def scan_apis(out):
    """Szuka podejrzanych konstrukcji w kodzie. Zrodlo: java z jadx, fallback: strings na DEX."""
    hits = []
    src_dir = out + "/jadx_out/sources"
    if os.path.exists(src_dir):
        for pat, desc in API_SIGNATURES:
            r = sh("grep -rhoE --include='*.java' '" + pat + "' " + src_dir + " 2>/dev/null | head -1")
            n = sh("grep -rEo --include='*.java' '" + pat + "' " + src_dir + " 2>/dev/null | wc -l")
            if r:
                hits.append((pat, desc, int(n.strip() or 0)))
    else:
        alls = sh("cd " + out + " && (cat classes*.dex 2>/dev/null || cat classes.dex 2>/dev/null) | strings -n 5 2>/dev/null")
        for pat, desc in API_SIGNATURES:
            m = re.findall(pat, alls)
            if m:
                hits.append((pat, desc, len(m)))
    return hits

# ------------------------------------------------------------------ nowe: scoring
def score_perms(perms):
    """Wagi uprawnien -> suma punktow + poziom + lista top ryzykownych."""
    scored = []
    total = 0
    for p in perms:
        w = PERM_RISK.get(p, 0)
        if w:
            scored.append((p, w))
            total += w
    scored.sort(key=lambda x: -x[1])
    return total, risk_level(total), scored

# ------------------------------------------------------------- nowe: "co robi"
def what_it_does(perms, api_hits, packer_lines):
    """Generuje sekcje 'Co robi ta apka' na podstawie manifestu + API + packera."""
    s = []
    api = set(p for p, _, _ in api_hits)
    permset = set(perms)

    if {"addJavascriptInterface", "setJavaScriptEnabled"} & api:
        s.append("- **WebView z mostkiem JS** (`addJavascriptInterface`/`setJavaScriptEnabled`) — typowy mechanizm phishingu / overlay / droppera WebView.")
    if "AccessibilityService" in api or "onAccessibilityEvent" in api:
        s.append("- **Usluga dostepnosci** — RAT/banker: czyta ekran, klika za uzytkownika, naklada overlay.")
    if {"TYPE_APPLICATION_OVERLAY", "FLAG_WINDOW_OVERLAY"} & api:
        s.append("- **Overlay** — rysuje okna nad innymi apkami (fake loginy bankowe).")
    if {"sendTextMessage", "SmsManager"} & api or {"SMS", "READ_SMS", "RECEIVE_SMS", "SEND_SMS"} & permset:
        s.append("- **SMS** — czyta/wysyla wiadomosci: stealer OTP / premium SMS.")
    if {"REQUEST_INSTALL_PACKAGES", "PackageInstaller"} & api or "REQUEST_INSTALL_PACKAGES" in permset:
        s.append("- **Instalacja APK** — dropper: moze dolaczyc kolejny zlosliwy pakiet.")
    if {"DexClassLoader", "PathClassLoader"} & api:
        s.append("- **Dynamiczne ladowanie kodu** — drugi etap / loader.")
    if {"NfcAdapter", "enableReaderMode"} & api:
        s.append("- **NFC** — tryb czytnika: mozliwy skimmer kart (a710209e).")
    if {"ClipboardManager", "OnPrimaryClipChangedListener"} & api:
        s.append("- **Schowek** — monitoruje clipboard: clipper (kradziez adresow/kopii).")
    if {"getDeviceId", "getSubscriberId", "getLine1Number"} & api:
        s.append("- **Fingerprint urzadzenia** — zbiera IMEI/IMSI/numer (anty-bot, targetowanie).")
    if {"new Socket(", "WebSocket"} & api:
        s.append("- **Niestandardowa komunikacja** (socket/WebSocket) — mozliwy C2.")
    if {"ptrace", "Frida", "/proc/self/maps"} & api:
        s.append("- **Anty-RE** — wykrywanie debuggera/Fridy: packer/loader (Zirex-style).")
    if {"Cipher.getInstance", "SecretKeySpec", "Base64.decode"} & api:
        s.append("- **Kryptografia/base64** — ukrywanie payloadu lub konfiguracji C2.")
    if {"takePicture", "MediaRecorder"} & api:
        s.append("- **Kamera/mikrofon** — nagrywanie audio/wideo.")
    if "RECORD_AUDIO" in permset:
        s.append("- **Mikrofon** — mozliwe podsłuchy.")
    if "CAMERA" in permset:
        s.append("- **Kamera** — mozliwe nagrywanie/szpiegowanie.")

    if packer_lines:
        s.append("- **Spakowane** (apkid: `" + ", ".join(packer_lines) + "`) — wlasciwy payload odszyfrowywany dopiero w runtime.")
    if not s:
        s.append("- Brak silnych sygnalow zlowrogiego zachowania w statyce (mozliwy czysty bloat / FP).")
    return s

def gen_yara(pkg, out, apkname):
    pkg16 = " ".join("%02x 00" % ord(c) for c in pkg)
    rule = ("rule " + apkname + "\n{\n"
            "    meta:\n        description = \"Auto-detekcja: " + pkg + "\"\n        package = \"" + pkg + "\"\n        date = \"" + datetime.date.today().isoformat() + "\"\n"
            "    strings:\n        $pkg16 = { " + pkg16 + " }\n"
            "    condition:\n        $pkg16\n}\n")
    open(out + "/" + apkname + ".yar", "w").write(rule)

def write_card(out, apkname, sha, pkg, perms, svc, recv, acts, ips, urls, doms, score, level, top_perms, api_hits, what):
    perms_str = " ".join(x for x in perms)
    api_lines = "\n".join("- `%s` (%d×) — %s" % (p, n, d) for p, d, n in api_hits)
    top_str = ", ".join("%s(%d)" % (p, w) for p, w in top_perms[:8])
    what_str = "\n".join(what)
    c = ("---\ntitle: \"" + apkname + " — auto-analiza\"\ndate: " + datetime.date.today().isoformat() +
         "\ntags: [sample, apk, auto, malware, analysis]\nstatus: pending\nsha256: " + sha + "\npackage: " + pkg + "\nrisk: " + level + "\n---\n\n"
         "# " + apkname + " (auto)\n\n"
         "| Pole | Wartosc |\n|------|---------|\n| SHA256 | " + sha + " |\n| Pakiet | " + pkg + " |\n"
         "| Ryzyko | **" + level.upper() + "** (" + str(score) + " pkt) |\n\n"
         "## Co robi ta apka\n\n" + what_str + "\n\n"
         "## Uprawnienia (" + str(len(perms)) + ") — ryzyko " + level.upper() + " (" + str(score) + " pkt)\n\n"
         "Top ryzykowne: " + top_str + "\n\n" + perms_str + "\n\n"
         "## Podejrzane API (" + str(len(api_hits)) + ")\n\n" + api_lines + "\n\n"
         "## Serwisy\n\n" + "\n".join("- " + x for x in svc) + "\n\n"
         "## Receivery\n\n" + "\n".join("- " + x for x in recv) + "\n\n"
         "## Activity\n\n" + "\n".join("- " + x for x in acts) + "\n\n"
         "## IoC\n\n- IP: " + ", ".join(ips[:15]) + "\n- URL: " + ", ".join(urls[:15]) + "\n- Domeny: " + ", ".join(doms[:20]) + "\n")
    open(out + "/" + apkname + ".md", "w").write(c)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apk"); ap.add_argument("--hash"); ap.add_argument("--out", default="/tmp/apk_analysis")
    a = ap.parse_args()
    if a.hash:
        apk = download_mb(a.hash)
    elif a.apk:
        apk = a.apk
    else:
        print("podaj --apk lub --hash"); sys.exit(1)
    sha = sha256_file(apk)
    out = a.out + "/" + sha[:12]
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    log("triage: sha256=" + sha)
    log("rozmiar: " + str(os.path.getsize(apk)))
    sh("file " + apk + " > " + out + "/file.txt")
    log("apkid (packer)")
    apkid_raw = sh(TOOLS["apkid"] + " " + apk + " 2>&1 | grep -v -i exception | head -20")
    print(apkid_raw)
    packer_lines = re.findall(r'packer\s*:\s*([^\n]+)', apkid_raw)
    packer_lines = [p.strip() for p in packer_lines if p.strip()]
    extract(apk, out + "/ex")
    mf = decode_manifest(out + "/ex/AndroidManifest.xml", out) if os.path.exists(out + "/ex/AndroidManifest.xml") else ""
    pkg, perms, svc, recv, acts = parse_manifest(mf) if mf and os.path.exists(mf) and os.path.getsize(mf) > 0 else ("?", [], [], [], [])
    log("pakiet: " + pkg + " | uprawnien: " + str(len(perms)))
    log("jadx (dekompilacja)")
    sh(TOOLS["jadx"] + " -q -d " + out + "/jadx_out " + out + "/ex/classes.dex 2>/dev/null")
    njava = len(glob.glob(out + "/jadx_out/sources/**/*.java", recursive=True)) if os.path.exists(out + "/jadx_out/sources") else 0
    log("plikow Java: " + str(njava))
    ips, urls, doms = ioc_from_strings(out + "/ex")
    log("skan podejrzanych API")
    api_hits = scan_apis(out)
    for p, d, n in api_hits:
        print("  [%d] %s" % (n, p))
    log("scoring ryzyka uprawnien")
    score, level, top_perms = score_perms(perms)
    print("  wynik: %d (%s)" % (score, level.upper()))
    what = what_it_does(perms, api_hits, packer_lines)
    apkname = re.sub(r'[^A-Za-z0-9_]', '_', pkg.replace('.', '_'))
    if pkg != "?":
        gen_yara(pkg, out, apkname)
    write_card(out, apkname, sha, pkg, perms, svc, recv, acts, ips, urls, doms, score, level, top_perms, api_hits, what)
    log("WYNIKI: " + out)
    log("karta: " + out + "/" + apkname + ".md | yara: " + out + "/" + apkname + ".yar")

if __name__ == "__main__":
    main()
