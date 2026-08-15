---
title: "Clippery i stealer — analiza (Laplas, Lumma, skrypty Python/C++)"
date: 2026-08-15
updated: 2026-08-15
tags: [clipper, stealer, malware, reverse-engineering, crypto]
status: analysis
category: malware
---

# Clippery i stealer — analiza

Powiązane: [[Keylogger_Analiza]] · [[Hunt_Stealer_Phishing]] · [[Klasyfikacja_Korpus]]

## Przegląd

| Narzędzie | Typ | Język | Cel |
|-----------|-----|-------|-----|
| **Laplas Clipper** | clipper (rodzina malware) | .NET | podmiana adresów krypto (clipboard hijack) |
| **Lumma Stealer** | info stealer (MaaS) | Go (packed) | kradzież: przeglądarki, portfele, tokeny, 2FA |
| **BTC-Clipper** (NightfallGT) | clipper | Python | BTC |
| **Raccoon Clipper** (3022-2) | clipper builder | Python | 9 krypto + PyArmor |
| **Crypto Clipper** (SantiiRepair) | clipper | C++ | 9 krypto + xorstr |

---

## 1. Laplas Clipper (rodzina, .NET)

**Z publicznej wiedzy** (MalwareBazaar: 0 próbek, binarka nie w korpusie).

- Clipboard hijacker .NET — monitoruje schowek, **podmienia adresy krypto** na adres atakującego.
- Wykrywanie adresów: regex (`bc1...`, `0x...`, `T...` itd.) per kryptowaluta.
- Dystrybucja: cracked software, tutoriale „jak zarabiać na crypto", fałszywe minery.
- **Detekcja**: proces monitorujący schowek (Clipboard Viewer / timer), regex krypto, zapis do schowka
  (`SetClipboardData`), częste `OpenClipboard`/`GetClipboardData`.

---

## 2. Lumma Stealer (próbka z korpusu)

### RE artifacts

- **hash**: `00d3f42dc0c6527d375f8b5430915ca27f0da7b9608e446d3e5f6c17082577a5`
- **size/typ**: 2 651 152 B · PE32+ (Go, packed)
- **tags**: `packed`, `unlisted` · sygnatura MalwareBazaar: **`lummastealer`**

### Stringi (statycznie — loader Go + API)

```
VirtualAlloc, LoadLibraryW, GetProcAddress        # dynamiczne ładowanie (packer)
DnsQuery_W, GetAddrInfoW                          # DNS/rozpoznanie C2
CreateProcessW, OpenProcessToken, DuplicateTokenEx # proces/token
CryptGenRandom                                    # krypto
NetUserGetInfo, GetUserNameExW, TranslateNameW     # dane użytkownika
RegCreateKeyExW, RegQueryValueExW, RegDeleteValueW # rejestr
GetComputerNameW, GetTempPathW, GetSystemDirectory # system info
```

**Wniosek:** payload jest **spakowany** (Go loader). C2/config **nie w plaintext** — do odzyskania
trzeba dynamicznie (unpacking). Statycznie widać typowe capabilities stealera (portfele, przeglądarki,
tokeny, rejestr, procesy).

### IOC

- Hash (sha256): `00d3f42d…` (powyżej).
- Rodzina: `LummaStealer` (MaaS, logi → C2 atakującego).

### C2 — ODSZYFROWANE dynamicznie (15.08, sandbox `.57`)

Uruchomiono `lumma.exe` w kontrolowanym sandboxie (DNS logging + 12 s + kill).
Wyczyszczony cache DNS → jedyny niestandardowy wpis:

| | |
|--|--|
| **C2 domena** | **`digitden.cyou`** |
| **C2 IP** | `64.89.161.173` |

- `.cyou` TLD (typowy dla C2). URLhaus: `no_results` (świeże/niezgłoszone).
- Metoda: `DnsCache.log` + `Get-DnsClientCache` po uruchomieniu (bez detonacji exfilu — kill po 12 s).

---

## 3. Autorskie skrypty (Python / C++)

### BTC-Clipper (Python) — `btcClip.py`

- **hash**: `9817d8de9bf7d2740b5b66e30ec1afdd98d7d119074a61cbba05514d4ebdc149`
- **Mechanizm** (z kodu):
  - `ctypes` → `OpenClipboard`/`GetClipboardData`/`GlobalLock` (czytanie schowka).
  - Regex: `^(bc1|[13])[a-zA-HJ-NP-Z0-9]+` (BTC: bech32 + legacy).
  - Podmiana: `echo %s |clip` (wstrzykuje adres atakującego).
  - Persystencja: rejestr Run + replikacja do `%APPDATA%`.
- **IOC**: import `GetClipboardData`/`OpenClipboard`, regex `bc1`, komenda `|clip`.

### Raccoon Clipper (Python, builder) — `main.pyw`

- **hash**: `ba5d2b01be40238dbc977ef03cf0a69a3863035030e304df77a668c922978a66`
- **9 krypto**: BTC, ETH, XMR, LTC, SOL, DOGE, XRP, TRX, BCH (regex per waluta).
- **Builder**: `pyinstaller --onefile` + **PyArmor** (obfuskacja) + ikony.
- **IOC**: multi-regex krypto, PyInstaller/PyArmor, `.pyw` (windowed).

### Crypto Clipper (C++) — `main.cpp` + `xorstr.h`

- **hash (main.cpp)**: `da43ff232de356c89761e8db5a9e53c237db5be28b269b3695a643fdb93c6f46`
- **Mechanizm**:
  - `GetClipboardData`/`SetClipboardData` (schowek).
  - **`xorstr`** — compile-time XOR string obfuscation (ukrywa adresy/nazwy).
  - Persystencja: rejestr (`Register`) + kopia do `%APPDATA%\Clipper\Clipper.exe`.
  - Anti-debug: `show_console()`/`hide_console()`.
- **IOC**: `xorstr`, `OpenClipboard`, rejestr `Clipper`, kopia do `%APPDATA%`.

---

## Wspólne wskaźniki clipperów

1. **Clipboard API**: `OpenClipboard` + `GetClipboardData` + `SetClipboardData` (WinAPI).
2. **Regex krypto**: `bc1`/`1`/`3` (BTC), `0x`+40hex (ETH), `T...` (TRX), `4...` (XMR), `r...` (XRP).
3. **Persystencja**: rejestr Run / kopia do `%APPDATA%`.
4. **Obfuskacja**: `xorstr` (C++), PyArmor (Python), .NET (Laplas).
5. **Podmiana**: szybki loop (100ms–1s) monitorujący schowek.

## Reguły detekcji

YARA → `/root/android-pipeline/tools/yara-rules/custom/clipper_stealer.yar`.

## Next

1. Lumma: unpacking (dynamicznie) → wyciągnąć C2/config.
2. Laplas: znaleźć próbkę (MalwareBazaar/Any.run) → statyczny RE.
