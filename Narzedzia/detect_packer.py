#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detektor pakowania / obfuskacji — APK i .NET PE.

Na bazie notatek:
  - Android_packed.md / Android_native_packed.md (Zirex, hhcbcu/nvcgehin, perski WebView,
    blob dropper, Albiriox ZipCrypto, ClayRat fake-flag manifest)
  - Win_dotnet_packed.md / DotNet_cluster.md (NanoCore w .rsrc, loader ze zaszyfrowana
    sekcja, pojedynczy import mscoree)

Wykrywa packer (apkid / entropia / ZipCrypto / importy / sekcje) i SUGERUJE metode
unpackingu. Nie odpala probki.

Uzycie:
  python3 detect_packer.py <plik.apk|plik.exe> [--json] [--md karta.md] [--apkid /sciezka/apkid]

Wymagania: python3 (stdlib). apkid opcjonalny (APK), pefile opcjonalny (PE — bez niego
uzywa wlasnego minimalnego parsera sekcji PE).
"""
import argparse, json, math, os, re, struct, subprocess, sys, zipfile

DEFAULT_APKID = "/opt/retools/bin/apkid"
ENT_HIGH = 7.5          # powyzej tego sekcja/plik uznawana za zaszyfrowana/packed

# ---------------------------------------------------------------- narzedzia
def sh(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return ((r.stdout or "") + (r.stderr or "")).strip()
    except Exception:
        return ""

def entropy(data):
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    ln = len(data)
    return -sum((c / ln) * math.log2(c / ln) for c in freq if c)

def readable(name):
    return all(32 <= ord(c) < 127 for c in name)

# ------------------------------------------------------------------ APK
def analyze_apk(path, apkid_path, rep):
    rep["type"] = "apk"
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        rep["verdict"] = "UNKNOWN"
        rep["suggestions"] = ["Plik nie jest czytelnym ZIP/APK (%s)" % e]
        return rep

    names = z.namelist()
    rep["entries"] = len(names)
    rep["has_manifest"] = "AndroidManifest.xml" in names

    # apkid
    apkid_bin = apkid_path or (DEFAULT_APKID if os.path.exists(DEFAULT_APKID) else sh("command -v apkid").strip())
    if apkid_bin:
        out = sh('"%s" %s 2>&1 | grep -v -i exception' % (apkid_bin, path))
        rep["apkid"] = out.splitlines()
        m = re.findall(r'packer\s*:\s*([^\n]+)', out)
        rep["apkid_packers"] = [x.strip() for x in m]
    else:
        rep["apkid"] = ["apkid niedostepny — pomijam"]

    # ZipCrypto / flagi szyfrowania + duze wpisy + entropia zawartosci
    encrypted = []
    high_ent = []
    for info in z.infolist():
        if info.flag_bits & 0x1:
            encrypted.append(info.filename)
        if info.file_size > 512 * 1024:  # > 512 KB
            try:
                e = entropy(z.read(info.filename))
            except Exception:
                e = 0.0
            if e > ENT_HIGH:
                high_ent.append((info.filename, info.file_size, round(e, 3)))
    rep["zipcrypto_entries"] = encrypted
    rep["high_entropy_assets"] = high_ent
    if encrypted:
        rep.setdefault("markers", []).append("ZipCrypto: %d wpisow zaszyfrowanych (m.in. %s)" % (len(encrypted), encrypted[0]))

    # pakowane assety wg notatek
    for n in names:
        low = n.lower()
        if re.search(r'nvcgehin|dbliqgnjl|local_data\.db', low):
            try:
                e = entropy(z.read(n))
            except Exception:
                e = 0.0
            rep.setdefault("markers", []).append("asset `%s` (%d B) ent=%.2f — payload packera" % (n, z.getinfo(n).file_size, e))

    # .so — Dobby / shadowhook / bytehook / Zirex
    so_markers = []
    for n in names:
        if n.endswith(".so"):
            try:
                data = z.read(n)[:512 * 1024]
            except Exception:
                continue
            s = data.decode("latin1", "replace")
            for mk in ("DobbyHook", "shadowhook", "bytehook", "com.zirex", "nativeDecryptPayload", "nativeComposeUrl", "inflate", "mmap"):
                if mk in s:
                    so_markers.append("%s in %s" % (mk, os.path.basename(n)))
    rep["so_markers"] = sorted(set(so_markers))
    if any("Dobby" in x or "shadowhook" in x or "bytehook" in x for x in so_markers):
        rep.setdefault("markers", []).append("native hooking (Dobby/shadowhook/bytehook) — Zirex-style packer/anty-RE")

    # fake-encryption manifest (ClayRat trick)
    fake_enc = False
    try:
        info = z.getinfo("AndroidManifest.xml")
        if info.flag_bits & 0x1:
            fake_enc = True
    except Exception:
        pass
    rep["manifest_encrypted_flag"] = fake_enc
    if fake_enc:
        rep.setdefault("markers", []).append("manifest z flaga encrypted — to zwykle FAKE (ClayRat-style), nie packer")

    # obfuskacja DEX (jednoliterowe klasy)
    dex_obf = None
    for n in names:
        if re.match(r'^classes\d*\.dex$', n):
            try:
                s = z.read(n).decode("latin1", "replace")
                hits = re.findall(r'L[a-z0-9]{1,2};', s)
                dex_obf = len(hits)
            except Exception:
                pass
    rep["dex_short_class_refs"] = dex_obf
    if dex_obf and dex_obf > 500:
        rep.setdefault("markers", []).append("DEX zaciemniony: %d jednoliterowych referencji klas (R8 / obfuskator)" % dex_obf)

    verdict, sugg = _verdict_apk(rep)
    rep["verdict"] = verdict
    rep["suggestions"] = sugg
    return rep

def _verdict_apk(rep):
    m = " ".join(rep.get("markers", []))
    packers = rep.get("apkid_packers", [])
    markers = rep.get("markers", [])

    if "ZipCrypto" in m and not rep.get("zipcrypto_entries") == ["AndroidManifest.xml"]:
        return ("PACKED — ZipCrypto (Albiriox-style)",
                ["Caly APK (lub wiekszosc wpisow) zaszyfrowany ZipCrypto.",
                 "Metoda: bkcrack (known-plaintext) jesli masz kawalek plaintextu (np. AndroidManifest z innej apki tej samej rodziny).",
                 "Albo: klucz z droppera (np. PENNY com.example.myapplication) — bez niego statyka niemozliwa."])
    if any("Dobby" in x or "shadowhook" in x or "bytehook" in x for x in markers):
        return ("PACKED — native loader Zirex / anty-RE",
                ["Native loader + hooking (Dobby/shadowhook/bytehook), C2 skladane w native (nativeComposeUrl).",
                 "Metoda: emulator + Frida — hook nativeDecryptPayload / nativeComposeUrl, dump odszyfrowanego DEX (frida-dexdump).",
                 "W statyce: jadx na DEX + stringi .so; URL C2 nie bedzie w plaintext."])
    if any("nvcgehin" in x or "dbliqgnjl" in x or "local_data.db" in x for x in markers):
        return ("PACKED — payload w assets (hhcbcu / blob dropper)",
                ["Duzy asset o entropii ~8.0 — zaszyfrowany drugi etap (hhcbcu: nvcgehin; blob: dbliqgnjl.dat).",
                 "Metoda: dynamicznie na emulatorze (dropper deszyfruje w runtime) + Frida hook decrypt; porownaj buildy (dwa hashe hhcbcu).",
                 "Bez klucza statycznie nie odzyskasz payloadu."])
    if any("manifest z flaga encrypted" in x for x in markers):
        return ("FAKE-FLAG manifest (nie packer) — ClayRat-style",
                ["Manifest ma ustawiony bit encrypted, ale to zwykly deflate.",
                 "Metoda: zlib.decompress(raw[12:]) odzyskuje AXML (trick z analyze_apk.py / recover_manifest).",
                 "Reszte analizuj normalnie (jadx/apkid)."])
    if packers:
        return ("PACKED — apkid: %s" % ", ".join(packers),
                ["apkid wskazal packer/kompilator. Odszyfruj payload (emulator + Frida) albo sprawdz assety o wysokiej entropii.",
                 "Jesli to tylko obfuskacja DEX (R8) — klasy jednoliterowe, odczytaj smali/jadx."])
    if rep.get("dex_short_class_refs", 0) and rep["dex_short_class_refs"] > 500:
        return ("OBFUSKACJA DEX (R8/ProGuard) — niekoniecznie packer",
                ["Klasy jednoliterowe = zaciemnienie kodu, nie zaszyfrowany payload.",
                 "Metoda: jadx/smali + analiza przeplywu; sprawdz stringi i dostep do sieci."])
    return ("CZYSTY / niepacked w statyce",
            ["Brak sygnalow packera (apkid czysty, brak ZipCrypto, brak wysokiej entropii w duzych assetach).",
             "Przejdz do analizy zachowania: manifest, uprawnienia, IoC (analyze_apk.py)."])

# ------------------------------------------------------------------ PE / .NET
def _pe_sections(path, rep):
    """Minimalny parser PE (stdlib). Zwraca listy sekcji + flagi CLR. pefile jesli dostepny."""
    try:
        import pefile  # type: ignore
        pe = pefile.PE(path, fast_load=True)
        rep["tool"] = "pefile"
        sections = []
        for s in pe.sections:
            sections.append({
                "name": s.Name.rstrip(b"\x00").decode("latin1", "replace"),
                "vsize": s.Misc_VirtualSize,
                "rawsize": s.SizeOfRawData,
                "entropy": round(s.get_entropy(), 3) if s.SizeOfRawData else 0.0,
                "rwx": bool(s.Characteristics & 0xE0000000) and (s.Characteristics & 0x80000000),
            })
        clr = False
        try:
            clr = bool(pe.OPTIONAL_HEADER.DATA_DIRECTORY[14].VirtualAddress)
        except (IndexError, AttributeError):
            pass
        pe.close()
        return sections, clr
    except ImportError:
        rep["tool"] = "stdlib"
        return _pe_sections_stdlib(path), None

def _pe_sections_stdlib(path):
    with open(path, "rb") as f:
        d = f.read()
    if d[:2] != b"MZ":
        return []
    off = struct.unpack_from("<I", d, 0x3C)[0]
    if d[off:off + 4] != b"PE\x00\x00":
        return []
    nsec = struct.unpack_from("<H", d, off + 6)[0]
    optsz = struct.unpack_from("<H", d, off + 20)[0]
    sstart = off + 24 + optsz
    sections = []
    for i in range(nsec):
        base = sstart + i * 40
        if base + 40 > len(d):
            break
        name = d[base:base + 8].rstrip(b"\x00").decode("latin1", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, base + 8)
        chars = struct.unpack_from("<I", d, base + 36)[0]
        raw = d[rawptr:rawptr + rawsize] if rawptr and rawsize else b""
        sections.append({
            "name": name, "vsize": vsize, "rawsize": rawsize,
            "entropy": round(entropy(raw), 3) if raw else 0.0,
            "rwx": bool(chars & 0xE0000000) and bool(chars & 0x80000000),
        })
    return sections

def analyze_pe(path, rep):
    rep["type"] = "pe"
    sections, clr = _pe_sections(path, rep)
    rep["sections"] = sections

    if clr is None:
        # stdlib: wykryj CLR po importach mscoree
        with open(path, "rb") as f:
            d = f.read()
        clr = b"mscoree.dll" in d.lower() or b"_CorExeMain" in d
    rep["clr"] = bool(clr)

    # stringi (ograniczone do 4 MB)
    with open(path, "rb") as f:
        d = f.read(4 * 1024 * 1024)
    low = d.lower()

    rep["nano_core"] = b"nanocore client.exe" in low
    rep["fake_versioninfo"] = any(s in low for s in (b"audacity", b"lightroom", b"coreldraw", b"xampp", b"unreal")) and b"update.exe" in low

    # wysokie entropie sekcji + dziwne nazwy
    hi = [s for s in sections if s["entropy"] > ENT_HIGH]
    weird = [s for s in sections if not readable(s["name"])]
    rwx = [s for s in sections if s["rwx"]]
    rep["high_entropy_sections"] = [s["name"] for s in hi]
    rep["weird_section_names"] = [s["name"] for s in weird]
    rep["rwx_sections"] = [s["name"] for s in rwx]

    if rep["nano_core"]:
        rep.setdefault("markers", []).append("string `NanoCore Client.exe` — NanoCore RAT (payload w .rsrc)")
    if rep["fake_versioninfo"]:
        rep.setdefault("markers", []).append("pomieszany VERSIONINFO (Audacity/Lightroom/XAMPP/Unreal) — falszywy stub")
    if hi:
        rep.setdefault("markers", []).append("sekcje o wysokiej entropii: %s — prawdopodobnie zaszyfrowany payload" % ", ".join(s["name"] for s in hi))
    if weird:
        rep.setdefault("markers", []).append("dziwne nazwy sekcji: %s — typowy packer" % ", ".join(s["name"] for s in weird))
    if rwx:
        rep.setdefault("markers", []).append("sekcje RWX: %s — shellcode/payload" % ", ".join(s["name"] for s in rwx))

    verdict, sugg = _verdict_pe(rep)
    rep["verdict"] = verdict
    rep["suggestions"] = sugg
    return rep

def _verdict_pe(rep):
    m = " ".join(rep.get("markers", []))
    if rep["nano_core"]:
        return ("PACKED — NanoCore RAT (payload w .rsrc)",
                ["Stub NanoCore: wlasciwy client schowany w zasobach (.rsrc ent~8.0).",
                 "Metoda: de4dot / dnSpy na exe, albo dump .rsrc -> payload; potem wyciagnij host:port z zasobow.",
                 "Nie wolac C2 — tylko wyciagaj konfiguracje."])
    if rep.get("high_entropy_sections") or rep.get("weird_section_names"):
        secs = ", ".join(rep.get("high_entropy_sections") or rep.get("weird_section_names"))
        return ("PACKED — loader ze zaszyfrowana sekcja (%s)" % secs,
                ["Typowy packer/loader (jak Loader.exe s}uiPduo 9.7MB ent=8.0).",
                 "Metoda: de4dot --unpack (jesli .NET) albo dnSpy memory dump w runtime.",
                 "Porownaj imphash mscoree — pojedynczy import CLR to nie odcisk rodziny."])
    if rep["fake_versioninfo"]:
        return ("STUB loader / crack (falszywy VERSIONINFO)",
                ["VERSIONINFO celowo pomieszany — wyglada jak update/crack, nie gotowy implant.",
                 "Metoda: jadx nie; dla .NET de4dot + lista typow (dnlib), szukaj FromBase64/GetProcesses."])
    if rep["clr"]:
        return ("CZYSTY .NET (managed, niepacked w statyce)",
                ["Brak zaszyfrowanych sekcji / dziwnych nazw. Analizuj normalnie (dnSpy, stringi, siec)."])
    return ("PE bez sygnalow packera",
            ["Brak wysokiej entropii / dziwnych sekcji. Analizuj normalnie (strings, imports, siec)."])

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="Detektor pakowania/obfuskacji (APK + .NET PE)")
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true", help="drukuj JSON")
    ap.add_argument("--md", metavar="KARTA.md", help="zapisz karte Obsidian")
    ap.add_argument("--apkid", default="", help="sciezka do apkid (default: /opt/retools/bin/apkid)")
    a = ap.parse_args()

    path = a.file
    if not os.path.exists(path):
        print("brak pliku: " + path); sys.exit(1)

    rep = {"file": path, "size": os.path.getsize(path)}
    with open(path, "rb") as f:
        head = f.read(4)

    if head[:2] == b"MZ":
        analyze_pe(path, rep)
    elif head[:2] == b"PK" or zipfile.is_zipfile(path):
        analyze_apk(path, a.apkid, rep)
    else:
        rep["verdict"] = "UNKNOWN"
        rep["suggestions"] = ["Nie rozpoznano formatu (ani PE, ani ZIP/APK)"]

    if a.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False))
    else:
        print("=== DETEKTOR PACKERA ===")
        print("plik      : %s (%d B)" % (path, rep["size"]))
        print("typ       : %s%s" % (rep["type"].upper(), " (.NET)" if rep.get("clr") else ""))
        print("werdykt   : %s" % rep["verdict"])
        if rep.get("apkid"):
            print("apkid     : %s" % ("; ".join(x for x in rep["apkid"] if x) or "-"))
        if rep.get("sections"):
            print("sekcje    : " + ", ".join("%s(ent=%.2f%s)" % (s["name"], s["entropy"], ",RWX" if s["rwx"] else "") for s in rep["sections"]))
        if rep.get("markers"):
            print("markery   :")
            for mk in rep["markers"]:
                print("  - " + mk)
        print("unpack    :")
        for s in rep["suggestions"]:
            print("  - " + s)

    if a.md:
        with open(a.md, "w") as f:
            f.write("---\ntitle: \"Detektor packera — %s\"\ndate: 2026-08-16\ntags: [packed, detector, auto]\n---\n\n"
                    "# Packer: %s\n\n**Werdykt:** %s\n\n## Markery\n\n"
                    % (os.path.basename(path), os.path.basename(path), rep["verdict"]))
            for mk in rep.get("markers", []):
                f.write("- %s\n" % mk)
            f.write("\n## Sugerowany unpacking\n\n")
            for s in rep["suggestions"]:
                f.write("- %s\n" % s)
        print("karta: " + a.md, file=sys.stderr)

if __name__ == "__main__":
    main()
