---
title: "Walidacja detekcji na korpusie (YARA)"
date: 2026-08-15
updated: 2026-08-15
tags: [detection, yara, validation, false-positive, metrics]
status: analysis
category: detekcja
---

# Walidacja detekcji YARA na korpusie (15.08)

Cel: sprawdzić, czy napisane reguły faktycznie działają na realnych próbkach, czy tylko
„ładnie wyglądają". Wynik: **działają częściowo — są realne FP i FN**.

## Korpus

- 15 próbek z `sample.bin`, 9 z ground-truth CTI (MalwareBazaar).
- 13 plików reguł custom (auto + backdoor + hunt + nanocore + pe_triage + phishing + keyloggers + clipper_stealer + telegram_stealer + xworm).

## Macierz detekcji

| Hash | GT (CTI) | Wykryte reguły | Werdykt |
|------|----------|----------------|---------|
| `00d3f42d` | lummastealer | Lumma_Go_Loader, Lumma_00d3f42d | ✅ TP |
| `178cb931` | — | Backdoor_EASports_Go, **Lumma_Go_Loader (FP)** | ⚠️ FP |
| `197d802c` | — | PE_C2_or_Exfil_Hints | ~ |
| `31d54f8c` | sheetrat | **BRAK** | ❌ FN |
| `45b98ab0` | nanocore | NanoCore_Client_string | ✅ TP |
| `46fb0161` | — | PE_C2_or_Exfil_Hints | ~ |
| `7ae00fe8` | njrat (XWorm) | **BRAK** | ❌ FN |
| `7d8b4974` | — | **Clipper_* (FP)** | ⚠️ FP |
| `85915561` | nanocore | NanoCore_Client_string | ✅ TP |
| `963800f7` | vidar | **Clipper_* (FP)** | ⚠️ FP |
| `98df0a98` | nanocore | NanoCore_Client_string | ✅ TP |
| `bc8d75d9` | nwhstealer | Clipper_*, Lumma_Go_Loader, PE_* | ⚠️ mieszane |
| `cdab250e` | — | BRAK | — |
| `e86fc24e` | lummastealer | Lumma_Go_Loader, **PS_Stealer (FP)** | ✅ TP+FP |
| `f53ceeb8` | — | BRAK | — |

## Metryki

```
próbki:        15
wykryte:       11
niewykryte:     4

ground-truth (CTI): 9
TP (poprawna rodzina): 5   (Lumma×2, NanoCore×3)
FN (niewykryte):       2   (SheetRAT, XWorm/njrat)
FP (błędna rodzina):   ≥5  (Vidar→clipper, NWH→clipper, Go→Lumma, …)
```

## Root causes (dlaczego FP/FN)

### FN — stringi zaszyfrowane
- **XWorm** (`7ae00fe8`): klucz `<Xwormmm>`/`<V74P…>` jest **zaszyfrowany w FieldRva** —
  YARA skanuje surowy binarkę → nie widzi plaintextu. Reguła `XWorm_V74_Key` trafi tylko
  w **odszyfrowaną/dumpniętą** formę (albo wariant bez szyfrowania).

### FN — brak reguły
- **SheetRAT** (`31d54f8c`): brak dedykowanej reguły.

### FP — reguły za szerokie
- **`Lumma_Go_Loader`**: wymaga `runtime.main + VirtualAlloc + GetUserNameExW + …` — to
  **każdy Go malware**, nie tylko Lumma (trafia w Go backdoora `178cb931`).
- **`Clipper_CPP_Xorstr` / `Clipper_Python_Clipboard`**: wymagają `GetClipboardData`/`SetClipboardData`
  — ale **stealerzy też używają clipboard API** (Vidar, NWH). Clipboard ≠ clipper.
- **`AccountTakeover_PowerShell_Stealer`**: `Telemetry + tdata` heurystyka (2-of-5) — za luźna.

## Poprawki (do zrobienia)

1. `Lumma_Go_Loader` → zawęzić (usunąć generyczne `runtime.main`/`VirtualAlloc`, dodać Lumma-specyficzne).
2. `Clipper_*` → wymagać **regex krypto + SetClipboardData** (nie samo clipboard API).
3. `XWorm_V74_Key` → oznaczyć jako „detekcja dumpu/odszyfrowanego", nie surowego PE.
4. Dodać regułę SheetRAT.
5. `AccountTakeover_PowerShell_Stealer` → podnieść próg do 3-4 stringów.

## Wniosek

Walidacja **ujawniła realne problemy** (5 TP / 2 FN / ≥5 FP). Reguły NanoCore i Lumma są OK,
reszta wymaga doprecyzowania. To jest dokładnie wartość, której brakowało — teraz wiemy co
**naprawdę** działa, a co jest za szerokie/za wąskie.
