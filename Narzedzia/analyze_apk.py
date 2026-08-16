#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline auto-analizy APK (statyczna).
Kroki: pobranie (MalwareBazaar) -> triage -> packer (apkid) -> odzysk manifestu (fake-encryption)
       -> manifest (androguard) -> dekompilacja (jadx) -> IoC (IP/URL/domeny) -> YARA -> karta Obsidian.

Uzycie:
  python3 analyze_apk.py --apk /sciezka/plik.apk [--out /katalog/wynikow]
  python3 analyze_apk.py --hash <sha256>            # pobiera z MalwareBazaar (klucz ~/.mb_api_key)
"""
import argparse, base64, datetime, glob, hashlib, os, re, shutil, struct, subprocess, sys, urllib.parse, urllib.request, zipfile, zlib

TOOLS = {"apkid": "/opt/retools/bin/apkid", "androguard": "/opt/retools/bin/androguard", "jadx": "/opt/jadx/bin/jadx"}
MB_KEY = os.path.expanduser("~/.mb_api_key")

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

def gen_yara(pkg, out, apkname):
    pkg16 = " ".join("%02x 00" % ord(c) for c in pkg)
    rule = ("rule " + apkname + "\n{\n"
            "    meta:\n        description = \"Auto-detekcja: " + pkg + "\"\n        package = \"" + pkg + "\"\n        date = \"" + datetime.date.today().isoformat() + "\"\n"
            "    strings:\n        $pkg16 = { " + pkg16 + " }\n"
            "    condition:\n        $pkg16\n}\n")
    open(out + "/" + apkname + ".yar", "w").write(rule)

def write_card(out, apkname, sha, pkg, perms, svc, recv, acts, ips, urls, doms):
    c = ("---\ntitle: \"" + apkname + " — auto-analiza\"\ndate: " + datetime.date.today().isoformat() +
         "\ntags: [sample, apk, auto, malware, analysis]\nstatus: pending\nsha256: " + sha + "\npackage: " + pkg + "\n---\n\n"
         "# " + apkname + " (auto)\n\n"
         "| Pole | Wartosc |\n|------|---------|\n| SHA256 | " + sha + " |\n| Pakiet | " + pkg + " |\n\n"
         "## Uprawnienia (" + str(len(perms)) + ")\n\n" + " ".join(x for x in perms) + "\n\n"
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
    print(sh(TOOLS["apkid"] + " " + apk + " 2>&1 | grep -v -i exception | head -20"))
    extract(apk, out + "/ex")
    mf = decode_manifest(out + "/ex/AndroidManifest.xml", out) if os.path.exists(out + "/ex/AndroidManifest.xml") else ""
    pkg, perms, svc, recv, acts = parse_manifest(mf) if mf and os.path.exists(mf) and os.path.getsize(mf) > 0 else ("?", [], [], [], [])
    log("pakiet: " + pkg + " | uprawnien: " + str(len(perms)))
    log("jadx (dekompilacja)")
    sh(TOOLS["jadx"] + " -q -d " + out + "/jadx_out " + out + "/ex/classes.dex 2>/dev/null")
    njava = len(glob.glob(out + "/jadx_out/sources/**/*.java", recursive=True)) if os.path.exists(out + "/jadx_out/sources") else 0
    log("plikow Java: " + str(njava))
    ips, urls, doms = ioc_from_strings(out + "/ex")
    apkname = re.sub(r'[^A-Za-z0-9_]', '_', pkg.replace('.', '_'))
    if pkg != "?":
        gen_yara(pkg, out, apkname)
    write_card(out, apkname, sha, pkg, perms, svc, recv, acts, ips, urls, doms)
    log("WYNIKI: " + out)
    log("karta: " + out + "/" + apkname + ".md | yara: " + out + "/" + apkname + ".yar")

if __name__ == "__main__":
    main()
