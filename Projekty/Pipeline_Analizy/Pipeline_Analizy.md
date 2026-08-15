---
title: "Pipeline Analizy"
date: 2026-08-14
updated: 2026-08-15
tags: [projekt, pipeline]
status: in_progress
priority: high
category: pipeline
vps: 5.175.189.133
home: /root/android-pipeline
---
# Pipeline Analizy Malware

Automatyczny stack statycznej analizy **APK (Android)** i **PE (Windows)** na C2 #1.

Powiązane: [[Status]] · [[Infrastruktura_C2]] · [[IOC_Backdoor]] · [[Backdoor_Go]] · [[Linki_Zewnętrzne]]

## Lokalizacja

| | |
|--|--|
| VPS | `5.175.189.133` (`vserver959630`, Ubuntu 24.04.4) |
| Home | `/root/android-pipeline/` |
| Samples | `/root/samples/` |
| Wrapper | `/usr/local/bin/android-malware-pipeline` → `bin/pipeline.sh` |
| Cron | `0 2 * * * /root/nightly_pipeline.sh >> /root/samples/logs/cron.log 2>&1` |

Symlinki w `/root/`:

```
/root/pipeline.sh          → /root/android-pipeline/bin/pipeline.sh
/root/batch_analyze.sh     → /root/android-pipeline/bin/batch_analyze.sh
/root/nightly_pipeline.sh  → /root/android-pipeline/bin/nightly_pipeline.sh
```

## Drzewo katalogów

```
/root/android-pipeline/
├── bin/
│   ├── pipeline.sh                 # pełna analiza + JSON/HTML/MD + agregacja
│   ├── batch_analyze.sh            # szybki triage APK i PE
│   ├── nightly_pipeline.sh         # MalwareBazaar → batch → full → daily summary
│   ├── download_malwarebazaar.sh
│   ├── install.sh
│   ├── rat5_clean_run.sh
│   └── rat5_android_clean.sh
├── lib/
│   ├── analyze_static.py           # androguard → JSON/MD (APK)
│   ├── analyze_pe.py               # pefile → JSON/MD/HTML (PE)
│   ├── aggregate_patterns.py       # features.csv + patterns_summary
│   ├── deep_re_pass.py
│   └── yara_generator.py           # auto-YARA + iocs.json
├── web/
│   ├── dashboard.html              # IOC UI
│   ├── serve.py                    # http://127.0.0.1:8766/ + /api/iocs
│   └── iocs.json                   # kopia z reports/
├── config/
│   ├── path.sh                     # PATH + venv
│   ├── pipeline.env                # limity RAM, flagi SKIP_*
│   ├── secrets.env                 # MB_API_KEY (nie commituj)
│   └── crontab.example
├── docs/GUIDE_PL.md
├── tools/
│   ├── apktool/  jadx/  capa/
│   ├── yara-rules/                 # Yara-Rules + custom/pe_triage.yar
│   ├── NusantaraScan/
│   ├── android-mcp/
│   └── android-reverse-engineering-claude-skill/
└── .venv/                          # Python 3.12: androguard, pefile, apkInspector

/root/samples/
├── raw/            # APK (nazwa = SHA256.apk)
├── quarantine/     # ZIP-y z MB (hasło infected) + luźne PE
├── pe/             # wystawione PE po preprocess
├── decompiled/     # apktool
├── sources/        # jadx
├── native/         # wyciągnięte .so
├── reports/<SHA256>/   # JSON + MD + HTML + artefakty
├── features/       # features.csv, patterns_summary.md
├── output/         # wynik lekkiego batcha
├── logs/
├── notes/          # REVERSE_REPORT.md
└── iocs/           # re_static_iocs.json
```

## Komponenty

| Skrypt | Funkcja |
|--------|---------|
| `batch_analyze.sh` | Szybki triage (APK i PE) do `output/` |
| `pipeline.sh` | Pełna analiza z raportami JSON/MD/HTML + CSV wzorców |
| `nightly_pipeline.sh` | Automatyczne nocne uruchomienie (02:00 UTC) |

## Obsługiwane formaty

### APK (Android)

- Detekcja: rozszerzenie `.apk/.xapk/.apks` albo ZIP z `AndroidManifest.xml` / `classes*.dex`
- `apktool` — dekompilacja zasobów / smali
- `jadx` — dekompilacja do Javy/Kotlin
- `androguard` (`analyze_static.py`) — uprawnienia, komponenty, URL-e
- Grep endpointów `http(s)://` i `ws(s)://`
- Native: wypakowanie `lib/*/*.so` + capa / radare2 / NusantaraScan (opcjonalnie)

### PE (Windows)

- Detekcja: `.exe/.dll/.sys/.scr` albo magia `MZ` (`4d5a`) + `file(1)`
- `analyze_pe.py` (pefile) — hashe, sekcje, entropia, importy, stringi, packer score
- `readpe` — nagłówki i IAT
- `ent` — entropia całego pliku
- `radare2` — `iI; iS; ii; iE` (timeout 30 s)
- `capa` — zachowania (timeout **45 s**, na dużych Go często puste)
- `strings` + filtr (http, webhook, telegram, powershell, exodus, …)
- YARA — `custom/` + `packers/` + `antidebug_antivm/` (timeout 60 s)

ZIP-y z MalwareBazaar są rozpakowywane hasłem `infected` (7z).

## Narzędzia (wersje na C2 #1, 14.08)

| Narzędzie | Wersja / ścieżka | Rola |
|-----------|------------------|------|
| apktool | **2.11.1** · `tools/apktool/` | dekompilacja APK |
| jadx | **1.5.1** · `tools/jadx/bin/jadx` | Java/Kotlin |
| pefile | **2024.8.26** · venv | analiza PE |
| YARA | **4.5.0** | reguły detekcji |
| radare2 | **5.5.0** | RE niskopoziomowe |
| capa | **9.4.0** · `tools/capa/capa` | zachowania |
| readpe | `/usr/bin/readpe` | nagłówki PE |
| ent | `/usr/bin/ent` | entropia |
| androguard | venv | static APK |

Aktywacja środowiska:

```bash
source /root/android-pipeline/config/path.sh
# dodaje jadx, apktool, capa do PATH i odpala .venv
```

## Output

Raporty: **`/root/samples/reports/<SHA256>/`**

| Artefakt | Źródło | Zawiera |
|----------|--------|---------|
| `<SHA256>.json` | `analyze_static.py` / `analyze_pe.py` | hashe, nagłówki, importy, stringi, YARA-ready pola |
| `summary.md` / `<SHA256>.md` | ten sam | czytelny raport Markdown |
| HTML (PE) | `analyze_pe.py` | ten sam zestaw w HTML |
| `pe_headers.txt` / `imports.txt` | readpe | COFF/optional + IAT |
| `r2.txt` | radare2 | info, sekcje, importy, eksporty |
| `capa.txt` | capa | MITRE-style behaviors |
| `suspicious_strings.txt` | strings | URL / C2 / LOLBin |
| `yara.txt` | yara | trafienia |
| `sample.bin` / `sample.exe` / `sample.apk` | kopia robocza | nie uruchamiać |
| `features.csv` | `aggregate_patterns.py` | tabela cross-sample |
| `patterns_summary.md` | agregacja | uprawnienia, URL, markery API |
| `daily_summary_YYYYMMDD.md` | nightly | dzienne podsumowanie |

### Layout batcha (`batch_analyze.sh`)

```
~/samples/output/
├── decompiled/      # apktool
├── sources/         # jadx
├── endpoints/       # URL/WS per próbka
├── features/        # hash, permissions, badging
├── reports/         # summary + all_urls_ranked.txt
├── pe_analysis/     # PE triage
└── logs/
```

## Komendy

```bash
source /root/android-pipeline/config/path.sh

# jedna próbka
bash /root/android-pipeline/bin/pipeline.sh /path/to/sample

# wszystkie APK+PE z raw/ + quarantine/
bash /root/android-pipeline/bin/pipeline.sh

# tylko PE / tylko APK
bash /root/android-pipeline/bin/pipeline.sh --pe-only
bash /root/android-pipeline/bin/pipeline.sh --pe-only /root/samples/quarantine/
bash /root/android-pipeline/bin/pipeline.sh --apk-only

# przebuduj CSV/wzorce z istniejących raportów
bash /root/android-pipeline/bin/pipeline.sh --aggregate-only

# wymuś ponowną analizę
FORCE=1 bash /root/android-pipeline/bin/pipeline.sh /path/to/sample

# szybki triage folderu
bash /root/android-pipeline/bin/batch_analyze.sh /root/samples/raw /root/samples/output
bash /root/android-pipeline/bin/batch_analyze.sh /root/samples/quarantine /root/samples/output

# nocny (ręcznie)
/root/nightly_pipeline.sh
/root/nightly_pipeline.sh --skip-download
/root/nightly_pipeline.sh --download-only
```

Flaga `--force` jest obsługiwana w `pipeline.sh`; `FORCE=1` też (skip-if-exists).

### Zmienne środowiskowe (`config/pipeline.env`)

| Zmienna | Default | Znaczenie |
|---------|---------|-----------|
| `JADX_THREADS` | 2 | wątki jadx (VPS 2 vCPU) |
| `MAX_PARALLEL` | 1 | kolejka sekwencyjna |
| `SKIP_GHIDRA` | 1 | Ghidra na 6 GB RAM wyłączona |
| `SKIP_NATIVE` | 0 (nightly: 1) | ekstrakcja `.so` |
| `SKIP_NUSANTARA` | 0 | NusantaraScan na native |
| `KEEP_DECOMPILED` | 1 (nightly: 0) | kasuj apktool output, oszczędza dysk |
| `SKIP_PE` / `SKIP_APK` | 0 | wyłącz gałąź |
| `MB_TAG` | `apk` | filtr MalwareBazaar |
| `MB_LIMIT` | 10 (nightly) | ile próbek ściągnąć |

## Przepływ nightly (02:00 UTC)

1. Załaduj `path.sh` + `pipeline.env` + `secrets.env` / `~/.mb_api_key`
2. `download_malwarebazaar.sh` (tag=`apk`, limit=10)
3. `batch_analyze.sh raw/ → output/`
4. `pipeline.sh` z `KEEP_DECOMPILED=0 SKIP_NATIVE=1`
5. Zapisz `/root/samples/reports/daily_summary_YYYYMMDD.md`

Logi: `/root/samples/logs/nightly_YYYYMMDD.log`, cron → `/root/samples/logs/cron.log`

## Stan lab (14.08.2026)

| Metryka | Wartość |
|---------|--------:|
| APK w `raw/` | 14 |
| ZIP + PE w `quarantine/` | 29 |
| PE w `pe/` | 0 (katalog pusty — PE leży w quarantine) |
| Raporty JSON | 29 |
| Katalogi raportów | 17 |
| Unique URL (batch) | 843 |
| `REQUEST_INSTALL_PACKAGES` | 8 / 14 (batch) · 35.71% (full) |
| accessibility / SMS / overlay | 7.14% |
| wallet strings | 14.29% |
| native `.so` | 35.71% |

Ostatni ręczny run:

| Pole | Wartość |
|------|---------|
| Czas | 2026-08-14 21:31:32–21:32:19 UTC |
| Cel | `/root/samples/quarantine/141935c46a5c4ff1b84b433e84f36e61.exe` |
| SHA256 | `178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4` |
| Log | `/root/samples/logs/pipeline_20260814T213132Z.log` |
| Wynik | OK, 1 PE, agregacja 14 próbek |
| capa | puste (timeout 45 s) |

Szczegóły próbki: [[Backdoor_Go]] · [[Analiza_Backdoora_Go_Detale]]

## Auto-YARA w pipeline (krok 2)

`pipeline.sh` po analizie (i po `--aggregate-only`) woła `generate_auto_yara`:

```bash
python3 ~/android-pipeline/lib/yara_generator.py "$REPORTS_DIR" \
  "$REPORTS_DIR/auto_rules.yar" --iocs-out "$REPORTS_DIR/iocs.json"
```

Nie zależy od nieistniejącego `summary.json`. Katalog jako argument jest rozwijany (`--pe-only /root/samples/quarantine/`).

| Artefakt | Ścieżka |
|----------|---------|
| Reguły | `/root/samples/reports/auto_rules.yar` |
| Kopia custom | `tools/yara-rules/custom/auto_rules.yar` |
| IOC JSON | `/root/samples/reports/iocs.json` + `web/iocs.json` |

Test 22:15 UTC:

```bash
~/pipeline.sh --pe-only /root/samples/quarantine/
cat /root/samples/reports/auto_rules.yar
yara /root/samples/reports/auto_rules.yar /root/samples/quarantine/141935c46a5c4ff1b84b433e84f36e61.exe
# → Auto_PE_178cb931
yara -r /root/samples/reports/auto_rules.yar /root/samples/raw/   # brak trafień
```

`raw/` nic nie złapał: stringi APK (`appassets.shelltemplate.internal`) są z **jadx**, nie leżą plaintext w ZIP. PE-reguła działa, bo API są w binarium.

CLI YARA: ostatni argument to target. `yara rules.yar a.apk b.apk` traktuje `a.apk` jako kolejny plik reguł (błąd parse). Używaj katalogu albo jednego pliku.

Dashboard: [[Dashboard_IOC]]

## Klasyfikacja ról (od 15.08)

Po `generate_auto_yara` pipeline woła `lib/classify_roles.py`. Raport JSON dostaje `tags` (`rat`/`stealer`/`backdoor`/…) i `classification`. Opis: [[Role_Tags]] · wnioski: [[Klasyfikacja_Korpus]].

## Generator auto-YARA (ręcznie)

```bash
python /root/android-pipeline/lib/yara_generator.py \
  /root/samples/reports \
  /root/samples/reports/auto_rules.yar
```

Czyta JSON + `suspicious_strings.txt`, wycina URL/IP/e-mail/API (`NetUserAdd`, `LogonUserW`, …) i zapisuje reguły `Auto_PE_<8>` / `Auto_APK_<8>`. Warunek: magia MZ/ZIP + `2 of ($s*)`.

## YARA — custom (`tools/yara-rules/custom/`)

`pipeline.sh` i `batch_analyze.sh` skanują **wszystkie** `custom/*.yar` (+ packers / antidebug, max 80 plików). Nowa reguła = wrzuć plik do `custom/`.

| Plik | Reguły |
|------|--------|
| `backdoor_easports.yar` | `Backdoor_EASports_Go` — overlay CN `easports.gg` + `NetUserAdd` / `RegSetValueExW` / `CreateProcessW` / `DuplicateTokenEx` / `DnsQuery_W` (ASCII+wide, PE+filesize) |
| `pe_triage.yar` | `PE_UPX_Packer` / `PE_MPRESS_Packer` / `PE_ASPack`, `PE_Suspicious_Injection_APIs`, `PE_Persistence_Strings`, `PE_C2_or_Exfil_Hints` |
| `auto_rules.yar` | generator (`Auto_PE_*` / `Auto_APK_*`) — nadpisywany po każdym runie |

Wdrożone 2026-08-14 23:03 UTC. Hit na `141935c46a5c4ff1b84b433e84f36e61.exe` w `yara.txt` raportu `178cb931…`. Nightly 02:00 UTC bierze ten sam katalog.

Plus indeksy Yara-Rules: packers, antidebug_antivm (max 80 plików na skan).

## Ograniczenia VPS

- ~6 GB RAM / 2 vCPU → `MAX_PARALLEL=1`, `SKIP_GHIDRA=1`
- Dysk 78% — nightly kasuje decompiled (`KEEP_DECOMPILED=0`)
- capa 45 s za krótki na zaciemnione Go (~3 MB)
- Ghidra / x64dbg / PEStudio — na [[Laboratorium_Windows]] (`.57`), nie tutaj
- Publicznego obrazu `chimera:latest` **nie ma** — zastępstwo to ten pipeline (`docs/GUIDE_PL.md`)

## Co odpalać na co dzień

```bash
source ~/android-pipeline/config/path.sh
# szybki przegląd nowych APK
~/android-pipeline/bin/batch_analyze.sh ~/samples/raw ~/samples/output
# albo pełna analiza + wzorce
~/android-pipeline/bin/pipeline.sh
less ~/samples/features/patterns_summary.md
less ~/samples/reports/daily_summary_$(date +%Y%m%d).md
```
