---
title: "Pipeline auto-analizy PE/ELF + narzedzia wspolne"
date: 2026-08-16
tags: [pipeline, pe, elf, yara, ioc, stix, dashboard, malware, analysis]
category: pipeline
status: active
---

# Pipeline PE/ELF + narzedzia wspolne

Rozbudowa pipeline o analize plikow **PE** (Windows) i **ELF** (Linux) oraz trzy
narzedzia spinajace raporty z pipeline (APK i PE/ELF) w IoC, reguly YARA i widok
dashboardu. Format raportu JSON jest zgodny z analyze_apk.py:
file.sha256, analyzed_at, classification.role + sekcje pe|elf,
strings_ioc, suspicious_apis, yara, packer_hints.

Powiązane: [[Analyze_APK_Pipeline]] · [[Dashboard_IOC]] · [[Automatyzacja]] · [[Narzedzia]]

## 1. analyze_pe.py — analiza PE/ELF (statyczna)

Analog analyze_apk.py dla binarek Windows/Linux:

- **PE** (pefile): naglowki, timestamp kompilacji, sekcje + entropia, importy
  DLL/API, eksporty, overlay, TLS callbacks, mapowanie podejrzanych API na
  kategorie (injection / persistence / evasion / crypto / keylog / screenshot /
  network / shell / steal), heurystyki packera (UPX, wysoka entropia, overlay,
  malo importow).
- **ELF** (parser wbudowany, bez zaleznosci): klasa/maszyna/typ, sekcje +
  entropia, symbole UND (importy), DT_NEEDED (biblioteki), BuildID, UPX/Go.
- **Wspolne**: strings → IoC (IP/URL/domeny), klasyfikator roli (regulowy,
  z powodami i confidence), skan istniejacych regul YARA, generacja reguly YARA
  (markery + magic), karta Obsidian, raport JSON, upsert do iocs.json.

### Uzycie

    python3 Narzedzia/analyze_pe.py --file plik.exe [--out /katalog/wynikow]
    python3 Narzedzia/analyze_pe.py --hash <sha256>        # MalwareBazaar (klucz ~/.mb_api_key)
    python3 Narzedzia/analyze_pe.py --file plik --yara-rules Narzedzia/ --no-yara

### Wymagania

- pefile (pip), yara (binarka), strings (binutils), file.
- Czas: analiza PE ~kilka sekund (entropia sekcji), ELF podobnie.

### Klasyfikacja roli (heurystyki)

| Sygnal | Rola |
|--------|------|
| stratum / xmr / monero / randomx / pool | cryptominer |
| keylog + siec/injection | rat |
| screenshot + siec | rat |
| keylog sam | keylogger |
| reverse-shell / cmd.exe + siec | backdoor |
| injection + siec | backdoor |
| injection + persistence | backdoor |
| crypto + steal (clipboard/processy) | stealer |
| wallet / bip39 / seed phrase | clipper |
| siec + download | dropper |

## 2. ioc_to_stix.py — agregator IoC → STIX / CSV / JSON

Czyta katalog raportow (*.json + iocs.json), deduplikuje po SHA256 probki
i po (typ, wartosc) IoC. Wyjscie:

- **STIX 2.1** — bundle: identity + marking-definition TLP + indicators
  (ipv4-addr / domain-name / url / file:hashes) + opcjonalnie observed-data.
- **CSV** — dla SOC: typ, wartosc, hash, rola, rodzina, first_seen.
- **JSON** — dla dashboardu: IoC z first/last_seen, role, rodziny, probki.

### Uzycie

    python3 Narzedzia/ioc_to_stix.py --reports /root/samples/reports --out /tmp/export --observed
    python3 Narzedzia/ioc_to_stix.py --reports /root/samples/reports --format csv --tlp amber
    PIPELINE_REPORTS=/root/samples/reports python3 Narzedzia/ioc_to_stix.py

## 3. yara_gen_test.py — generator + tester regul YARA

Trzy tryby:

- **generate** — regula z probki (markery: URL/IP/domena/API/ciekawe stringi,
  priorytet dla IoC) albo z raportu pipeline (--report).
- **test** — macierz pomylek na korpusie: TP/FP/FN + precision/recall/F1 per
  regula. Korpus: corpus/<family>/* (katalogi benign/unknown = brak
  dopasowania) albo plaski + --labels labels.json (sha256 -> family).
- **scan** — pojedyncza probka vs reguly z wylistowaniem dopasowanych stringow.

### Uzycie

    python3 Narzedzia/yara_gen_test.py generate --sample probka.exe --family Rodzina --c2 "host:port"
    python3 Narzedzia/yara_gen_test.py generate --report raport.json --out generated_rules
    python3 Narzedzia/yara_gen_test.py test --rules generated_rules --corpus /tmp/corpus --out wyniki.md
    python3 Narzedzia/yara_gen_test.py scan --rules Narzedzia --sample probka.exe

Regula z family w meta jest testowana jako detektor TEJ rodziny (TP/FP/FN
liczone przeciw etykietom korpusu). Regula bez family = wlasna rodzina.

## 4. dash-cli.py — CLI dashboardu

Statystyki, os czasu, filtry i raporty bez przegladarki:

    python3 Narzedzia/dash-cli.py --reports /root/samples/reports stats
    python3 Narzedzia/dash-cli.py --reports DIR timeline --days 7
    python3 Narzedzia/dash-cli.py --reports DIR filter --role rat --kind pe --since 2026-08-01
    python3 Narzedzia/dash-cli.py --reports DIR chart --metric roles|kind|family|daily|packer
    python3 Narzedzia/dash-cli.py --reports DIR iocs --type domain --top 20
    python3 Narzedzia/dash-cli.py --reports DIR report <sha256|nazwa> [--html] [--pdf --out plik]

PDF: raport HTML konwertowany przez wkhtmltopdf / weasyprint / chromium
(jesli dostepne), inaczej drukuj z przegladarki.

## Integracja z istniejacym pipeline

- Raporty analyze_pe.py trafiaja do tego samego katalogu co APK
  (/root/samples/reports), wiec build_dashboard_history.py, alert_roles.py
  i dashboard czytaja je bez zmian (schema classification.role + file).
- ioc_to_stix.py mozna dopisac do pipeline.sh (po iocs.json) — eksport
  STIX/CSV dla SOC.
- dash-cli.py report --pdf nadaje sie do raportu z probki w Obsidian
  (karta .md + zalacznik PDF).
