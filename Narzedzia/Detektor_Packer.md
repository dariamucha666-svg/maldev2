---
title: "Detektor pakowania / obfuskacji"
date: 2026-08-16
tags: [narzedzia, packed, android, dotnet, analysis]
status: active
---

# Detektor packera — detect_packer.py

Skrypt: `Narzedzia/detect_packer.py` — wykrywa packer/obfuskację dla **APK** i **.NET PE** i sugeruje metodę unpackingu. Nie odpala próbki.

Zbudowany na bazie notatek: [[Android_packed]] · [[Android_native_packed]] (Zirex, hhcbcu/nvcgehin, perski WebView, blob dropper, Albiriox ZipCrypto, ClayRat fake-flag) · [[Win_dotnet_packed]] · [[DotNet_cluster]] (NanoCore, loader ze zaszyfrowaną sekcją).

## Użycie

```bash
python3 Narzedzia/detect_packer.py <plik.apk|plik.exe>
python3 Narzedzia/detect_packer.py <plik> --json        # pełny raport JSON
python3 Narzedzia/detect_packer.py <plik> --md karta.md  # karta Obsidian
python3 Narzedzia/detect_packer.py <plik> --apkid /sciezka/apkid
```

## Co wykrywa

### APK
- **apkid** (jeśli dostępny: `/opt/retools/bin/apkid` lub `--apkid`) — packer/kompilator DEX.
- **ZipCrypto** — wpisy z flagą encrypted (Albiriox: cały APK; ClayRat: tylko manifest = **fake-flag**, nie packer).
- **Wysoka entropia assetów** (>7.5) — payload packera (`nvcgehin`, `dbliqgnjl.dat`, `local_data.db`).
- **Native hooking** — stringi Dobby / shadowhook / bytehook / `com.zirex` / `nativeDecryptPayload` w `.so` → Zirex-style packer.
- **Obfuskacja DEX** — jednoliterowe referencje klas (R8/obfuskator).

### PE / .NET
- Sekcje o entropii >7.5, dziwne nazwy sekcji (`s}uiPduo`), sekcje RWX.
- `NanoCore Client.exe` → NanoCore RAT (payload w `.rsrc`).
- Pomieszany VERSIONINFO (Audacity/Lightroom/XAMPP/Unreal) → fałszywy stub.
- Import `mscoree.dll` / CLR header (pefile; bez pefile — własny minimalny parser sekcji PE w stdlib).

## Sugerowany unpacking (werdykty)

| Werdykt | Metoda |
|---------|--------|
| ZipCrypto (Albiriox) | bkcrack (known-plaintext) albo klucz z droppera (PENNY `com.example.myapplication`) |
| Native loader Zirex | emulator + Frida: hook `nativeDecryptPayload`/`nativeComposeUrl`, frida-dexdump |
| Payload w assets (hhcbcu/blob) | dynamicznie na emulatorze (dropper deszyfruje w runtime) + Frida hook decrypt |
| FAKE-flag manifest (ClayRat) | `zlib.decompress(raw[12:])` odzyskuje AXML — to nie packer |
| Obfuskacja DEX (R8) | jadx/smali — analiza przepływu, nie decrypt |
| NanoCore | de4dot / dnSpy, dump `.rsrc` → payload, wyciągnij host:port z zasobów (nie wołaj C2) |
| Loader z zaszyfrowaną sekcją | de4dot `--unpack` albo dnSpy memory dump w runtime |

## Wynik

Konsola: werdykt + markery + lista kroków unpackingu. `--md` zapisuje kartę Obsidian, `--json` czysty JSON (stdout).

## Powiązane

- [[Analyze_APK_Pipeline]] — pełna analiza APK używa tego samego zestawu heurystyk w karcie.
- Próbki testowe w notatkach: Zirex `b5e8b4ae`, hhcbcu `b2bc6d34`/`d5b94817`, perski WebView `fdbee288`, blob `7834f2ef`, Albiriox `8703ee86`, ClayRat `78878d33`, NanoCore `45b98ab0`/`98df0a98`/`85915561`, Loader `f53ceeb8`.
