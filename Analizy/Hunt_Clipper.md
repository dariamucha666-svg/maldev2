---
title: "Hunt + OSINT — Clipper"
date: 2026-08-15
updated: 2026-08-15
tags: [hunt, clipper, clipboard, crypto, pipeline, osint]
status: active
---

# Clipper — hunt w korpusie + OSINT (detekcja)

**Clipper / clipbanker** = malware, które **czyta schowek** i gdy treść wygląda jak adres portfela (BTC `1…`/`3…`/`bc1…`, ETH `0x`+40 hex, TRX `T…`, XMR) **podmienia go na adres atakującego**. Ofiarą jest ten, kto wkleja adres przy wypłacie.

To **nie** jest to samo co stealer (kradzież plików/cookie) ani phishing (fałszywy login). Czasem siedzi w tym samym dropperze.

Powiązane: [[Hunt_Phishing_Stealer]] · [[OSINT_Phishing_Stealer]] · [[Klasyfikacja_Korpus]]

---

## Werdykt labu (15.08, static)

**Brak potwierdzonego clippera** w obecnym zestawie.

Nie ma jednocześnie:
1. API schowka (`SetClipboardData` / `OnPrimaryClipChangedListener`) **oraz**
2. stałych stringów-adresów albo regexów `bc1` / `bitcoin:` / seed 12/24.

To, co wyglądało na clipboard, to szum albo inna rola:

| Hash | Co jest | Werdykt |
|------|---------|---------|
| `7d8b4974…d024` | PE32 Delphi DLL 28 MB, WebView2, importy `Get/Set/EmptyClipboard`, string `ClipboardCmd` | Aplikacja GUI / WebView — schowek do copy URL, **nie** swap BTC. Rola: packed/unlisted. |
| `963800f7…fb4f` | Electron/NSIS dropper, `Open/Set/EmptyClipboard` | Runtime Electron zawsze ma clipboard. Słowo `tron` w JSON = szum tokenów OAuth, nie TRON wallet. Katalog: dropper. |
| `bc8d75d9…8f8f` | tylko `GetClipboard` | Za mało na clipper. |
| APK z `ClipboardManager` (`417406`, `a710209e`, shelltemplate…) | androidx / WebView „kopiuj link” | **FP**. Bez `OnPrimaryClipChangedListener` + tickerów coin. |

Fałszywe „BTC” z regexu `1[a-f0-9]{25}` to **kawałki SHA256** (`141935c46a5c4f…`), nie adresy.

---

## Jak będziemy to łapać dalej

YARA (static, wąskie): `tools/yara-rules/custom/hunt_clipper.yar`

- Win: 2 z {Open,Get,Set}Clipboard **oraz** `bc1` / `bitcoin:` / `wallet`
- Android: `OnPrimaryClipChangedListener` **oraz** `bc1` / `bitcoin:` / USDT / TRX

Nie wystarczy sam `ClipboardManager` (każdy Android UI).

W pipeline: `classify` nie dostaje roli `clipper`, dopóki nie ma adresu + API. Nightly YARA custom już skanuje `custom/*.yar`.

---

## OSINT — klasa (nie IoC z naszego dysku)

Publiczne rodziny / kampanie (czytać, nie odtwarzać):

| Nazwa | Rok | Notatka detekcyjna |
|-------|-----|--------------------|
| Trojan.Clipper / ClipBanker | generic MB | Malwarebytes: podmiana schowka, często z droppera |
| Android/Clipper.C (ESET) | 2019 | pierwszy na Play, przynęta MetaMask |
| CryptoClippy (Unit 42) | 2023 | PT, Google Ads |
| Silent Swap (McAfee) | ext. Chrome | clipper w rozszerzeniu, wiele chainów |
| SnipVex | 2025 | clipbanker w paczkach software (np. drukarki) |
| Microsoft Tor clipper | 2026-06 | WSH + Tor + podmiana + seed 12/24 w schowku |

Detekcja na hoście (Sigma/Sysmon, nie budowa):
- `SetClipboardData` w pętli + nietypowy proces (nie explorer/chrome)
- regex adresu w pamięci procesu bez okna portfela
- nowy mutex + kopia siebie do Startup (klasyczny Win clipper)

---

## Czego nie robię

- Nie piszę clippera ani regexów „do produkcji ataku”.
- Nie testuję podmiany na żywym schowku.
- Nie szukam żywych adresów atakujących w celu użycia.

## Next

1. YARA `hunt_clipper.yar` na surowych PE/APK z kwarantanny (nie tylko raportach).
2. Jeśli pojawi się hit `bc1`+clipboard — nowa karta w `Analizy/Malware/`, rola `clipper`.
