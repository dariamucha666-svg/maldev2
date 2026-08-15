---
title: "Status projektów — co działa, co wymaga uwagi"
date: 2026-08-15
updated: 2026-08-15
tags: [status, projekty, bot, pipeline, detekcja]
status: active
category: projekty
---

# Status projektów

Ostatnia aktualizacja: 2026-08-15 (automatycznie + ręcznie).

## ✅ Działa

| Projekt | Stan | Uwagi |
|---------|------|-------|
| Bot Telegram (`/root/obsidian-telegram-bot`) | ✅ active | systemd, Restart=always, error handler dodany |
| Gra `/graj` | ✅ | 3 poziomy · 8 ataków · 34 metody · katalog misji |
| Codzienne podsumowanie (09:00) | ✅ | APScheduler job |
| Pipeline malware/RE (`android-pipeline`) | ✅ | nightly 02:00, CTI + OSINT + nuclei |
| CTI enrichment (`enrich_cti.py`) | ✅ | MalwareBazaar/URLhaus/VT/AbuseIPDB/OTX |
| OSINT toolkit (`.139`) | ✅ | subfinder/amass/nuclei + cache |
| Suricata IDS (`.139`) | ✅ live | 15 reguł + alerty Telegram |
| Detekcja YARA/Suricate/Sigma | ✅ | walidowana: TP 6, FP 2 |
| Pętla optymalizacji (co 2h) | ✅ active | optymalizator → weryfikator |

## ⚠️ Wymaga uwagi

| Projekt | Problem | Co zrobić |
|---------|---------|-----------|
| `tools/detection/*.rules` + `.zeek` | osierocone (niepodpięte do pipeline) | podpiąć do nightly albo usunąć |
| `dashboard.html` (42 KB) | nieużywany | usunąć albo podpiąć |
| `tools/ghidra` / `tools/Malware-Analyzer` | brak (opcjonalne) | `install.sh` albo udokumentować |
| Pliki `.bak*` (6+) | śmieci po optymalizacji | usunąć |
| Refog/Spyrix | brak binarki | czeka na plik do RE |
| Laplas Clipper | brak binarki (IOC tylko) | Any.run/VT z kontem |
| Still Sync / Windows Telemetry Update | brak repo/próbki | znaleźć próbkę |
| Lumma (4 hashe) | brak binarki w korpusie | ściągnąć próbki |
| XWorm YARA | trafia tylko dump (nie surowy PE) | reguła na dump |
| Clipper vs stealer (FP) | nierozróżnialne statycznie | analiza dynamiczna |

## 🔴 Zablokowane (świadomie)

- Refog/Spyrix — rejestracja u vendora (nie zakładamy konta).
- Pełna detonacja stealerów — zasada „nie odpalamy w sieci".
