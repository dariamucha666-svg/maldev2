---
title: "Sesje — indeks recapow i logow sesji"
date: 2026-08-16
tags: [moc, sesje, recap, index]
category: podsumowanie
status: active
---

# Sesje — indeks

Mapa notatek z poszczegolnych sesji (czaty z asystentem + sesje operacyjne).

Synteza i wnioski: [[Wnioski]]

## 2026-08-16

| Sesja | Notatka | Zakres |
|-------|---------|--------|
| Operacyjna (00:19–02:03) | [[Dzienniki/2026/2026-08-16_sesja|2026-08-16_sesja]] | RAT .57 (dynamiczna analiza + przebudowa + optymalizacja) + Evilginx2 na .139 |
| Pipeline APK | [[Analyze_APK_Pipeline]] | analyze_apk.py: apkid→androguard→jadx→IoC→YARA→karta Obsidian |
| ClayRat detekcja | [[Analizy/Malware/ClayRat_Android_RAT|ClayRat_Android_RAT]] | YARA clayrat.yar + Suricata clayrat_c2.rules (C2, pkg UTF-16, Grok-markery) |
| Narzedzia red team (07:20–07:40) | [[Recap_2026-08-16_narzedzia_redteam]] | I-V-E (target_profile/cve_correlator/password_spray), Sliver ops + raport + walidacja detekcji, detect_packer, build_agent |
| Rozbudowa pipeline PE/ELF (07:25–08:20) | [[Recap_2026-08-16]] | analyze_pe.py, ioc_to_stix.py, yara_gen_test.py, dash-cli.py, export_iocs_hook.sh |

## 2026-08-15

| Sesja | Notatka | Zakres |
|-------|---------|--------|
| malware/RE pipeline + detekcja | [[Recap_2026-08-15]] | CTI enrichment, OSINT toolkit, phishing (SET/Evilginx2/GoPhish), keyloggery, clippery/Lumma, TeleKiller, XWorm, Go backdoor (garble), Suricata IDS, walidacja YARA |
| popoludnie (Kali) | [[Lab/Recap 2026-08-15]] | dostep do VPS, bot XMask, mini-lab RE |

## 2026-08-14

| Sesja | Notatka | Zakres |
|-------|---------|--------|
| obie sesje dnia | [[Lab/Recap 2026-08-14]] | Kali → .133 (analiza) + .57 (Windows RE) + probka PE |

## Raporty (raports/)

- [[raports/2026-08-16_dynamiczna_analiza_RAT_57|2026-08-16_dynamiczna_analiza_RAT_57]] · [[raports/2026-08-16_optymalizacja_RAT_57|optymalizacja_RAT_57]]
- [[raports/2026-08-16_sliver-2026-08-16_engagement|sliver-2026-08-16_engagement]] · [[raports/2026-08-16_detection_coverage|detection_coverage]]

## Konwencja

- Czaty z asystentem → `Recap_YYYY-MM-DD[_temat].md` (katalog glowny maldev2/).
- Sesje operacyjne (hosty, komendy, artefakty) → `Dzienniki/YYYY/YYYY-MM-DD_sesja.md`.
- Wiele sesji tego samego dnia → sufix tematu, np. `_narzedzia_redteam`.
- Szczegolowe raporty techniczne → `raports/`.
