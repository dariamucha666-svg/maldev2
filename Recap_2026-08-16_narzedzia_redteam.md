---
title: "Recap sesji 2026-08-16 — narzedzia red team (I-V-E, Sliver ops, detekcja, packer)"
date: 2026-08-16
updated: 2026-08-16
tags: [recap, session, redteam, sliver, ive, detection, yara, ad]
status: completed
category: podsumowanie
---

# Recap — 16.08 (narzedzia red team: I-V-E, Sliver ops, detekcja, packer)

Sesja rownolegla (07:20–07:40 UTC): realizacja punktow 2–5 z listy narzedzi
(operacje red team, automatyzacja I-V-E, purple-team, malware dev).
Powiązane: [[Sesje_MOC]] · [[IVE_Automatyzacja]] · [[Sliver_Ops]] · [[Detektor_Packer]] · [[Build_Agent]] · [[Recap_2026-08-16]]

## Co zrobiono (chronologicznie)

1. **Automatyzacja I-V-E** (`IVE_Automatyzacja.md`):
   - `target_profile.py` — orchestrator recon→podatnosci→exploity: theHarvester
     (crtsh/hackertarget/otx/rapiddns) → nuclei tech-detect → nmap -sV → sqlmap
     → dossier `Projekty/Recon/<domain>.md` (sekcje I/V/E) + surowe outputy; fallback PATH→docker kali.
   - `cve_correlator.py` — wersje uslug (nmap/nuclei) → CVE → searchsploit + msfconsole;
     karty `cve_<CVE>.md` + `exploit_plan.md`.
   - `password_spray.py` — kerbrute passwordspray z bezpiecznikiem lockout
     (limit prob/konto = threshold − margin) → karta `Lab/RedTeam_AD/Spray_*.md` + alert Telegram.
2. **Sliver ops** (`Sliver_Ops.md`):
   - `sliver_ops.py` — pelny operator CLI: version/sessions/beacons/jobs/profiles/builds,
     profile-save (jak Backdoor_Go_easports), generate/regenerate, stagers,
     tasking (screenshot/keylog/exec/download/upload/ls/ps), kill/rename, log do Obsidian.
     Zakres: wylacznie lab XMask; operacje destrukcyjne wymagaja `--yes`.
   - `sliver_report.py` — raport engagement: timeline + artefakty + co zostalo na hostach
     (OPSEC) + checklist sprzatania + wpis w `Daily/`.
   - `detection_validator.py` — purple-team: replay technik (beacon C2 / ataki AD) przez
     Suricate offline + matcher Sigma → tablica pokrycia technika↔detekcja.
3. **Detektor packera** (`Detektor_Packer.md`): `detect_packer.py` — APK (apkid, ZipCrypto,
   entropia assetow >7.5, native hooking Dobby/shadowhook/Zirex, obfuskacja DEX) i .NET PE
   (NanoCore, loader z zaszyfrowana sekcja) + sugestia metody unpackingu; nie odpala probki.
4. **Builder agenta** (`Build_Agent.md`): `build_agent.sh` — koniec problemu
   „exe starszy niz zrodlo”: freshness check → build (pyinstaller, `_build_info.py` z BUILD_ID)
   → hash → manifest JSON → upload do C2 (opcjonalnie) → timestamp w Obsidian.

## Wyniki / artefakty

- `Logs/sliver_ops/ops.jsonl` — demo: profile-save, generate (dry-run + realny),
  artifact `opstest01.exe`; coverage `coverage_2026-08-16.csv`.
- `raports/2026-08-16_sliver-2026-08-16_engagement.md` — wygenerowany 07:38:25Z przez
  `sliver_report.py`: 15 zdarzen timeline, 6 artefaktow ops.jsonl, beacony/sesje live: 0.
- `raports/2026-08-16_detection_coverage.md` — replay 9 technik: clayrat-beacon/ws/dns,
  kerberoasting, asrep-roast, password-spray, smb-enum, ldap-enum, dcsync — **PASS**
  (Suricata 9000801-9000808 / 1100010-1100015 + Sigma ad-*-001).
- Commit `fd97513` (Sliver ops + engagement + detection validator; fix clayrat 9000802).

## Uwagi

- Rownolegle z ta sesja trwala rozbudowa pipeline PE/ELF — patrz [[Recap_2026-08-16]].
- Reguly/dane: `clayrat.yar` + `clayrat_c2.rules` (Suricata) — analiza ClayRat:
  [[Analizy/Malware/ClayRat_Android_RAT|ClayRat_Android_RAT]].
- Sekrety (hasla, tokeny) poza vaultem, zgodnie z konwencja.
