---
title: "Inwentaryzacja i analiza narzedzi"
date: 2026-08-16
updated: 2026-08-16
tags: [narzedzia, inventory, analiza, tools]
status: active
category: narzedzia
---

# Analiza narzędzi — co już mamy

Przegląd całości: własne skrypty (`Narzedzia/`), narzędzia na hostach, pipeline, boty, web.
Powiązane: [[Automatyzacja]] · [[Pipeline_PE_ELF]] · [[IVE_Automatyzacja]] · [[Sliver_Ops]] · [[Lab/Narzedzia_RE]] · [[Lab/Hosts]] · [[Wiedza/Narzedzia]]

---

## 1. Własne skrypty labu (`Narzedzia/`) — 30+ narzędzi

### 1.1 Analiza malware / pipeline

| Narzędzie | Co robi | Stan |
|-----------|---------|------|
| `analyze_apk.py` | pełny łańcuch APK: triage→apkid→odzysk manifestu→androguard→jadx→IoC→YARA→karta Obsidian | działa (test: ClayRat) |
| `analyze_pe.py` | pipeline PE/ELF: sekcje+entropia, importy, podejrzane API→kategorie, packer-heurystyki, klasyfikator roli, YARA (skan+generacja), `iocs.json` | działa (PE→rat 0.85, ELF→cryptominer 0.90) |
| `detect_packer.py` | detektor packera APK (ZipCrypto, Zirex/Dobby, entropia, fake-flag) + .NET (NanoCore, sekcje) + sugestia unpackingu | działa |
| `yara_gen_test.py` | generacja reguł z próbki/raportu + tester TP/FP/FN, precision/recall/F1 | działa |
| `ioc_to_stix.py` | agregator IoC → STIX 2.1 (TLP), CSV (SOC), JSON (dashboard), dedupe | działa |
| `dash-cli.py` | CLI dashboardu: stats/timeline/filter/chart/iocs/report (MD/HTML/PDF) | działa |
| `build_dashboard_history.py` | history.json dla dashboardu publicznego | działa |
| `export_iocs_hook.sh` | hook do pipeline.sh (STIX/CSV/JSON, niekrytyczny, exit 0) | działa |
| `export_pipeline_to_obsidian.sh` | raporty pipeline → `Analizy/Raporty/` | działa |

### 1.2 Red team / C2 / AD

| Narzędzie | Co robi | Stan |
|-----------|---------|------|
| `sliver_ops.py` | operator CLI Sliver: profiles/generate/stagers/tasking (screenshot/keylog/exec/…) /kill + log do Daily; wire-codec dla Sliver v1.7.1 | działa (opstest01 wygenerowany) |
| `sliver_report.py` | raport engagement: timeline, artefakty, OPSEC (co zostało na hostach), checklist sprzątania | działa |
| `sliver_sessions.py` | snapshot sesji/beaconów/jobów (gRPC, tylko odczyt) | działa |
| `export_sliver_to_obsidian.sh` | sesje Sliver → vault (cron co godzinę) | działa |
| `build_agent.sh` | builder agenta: freshness-check → build → hash → manifest → upload C2 → wpis Daily | działa |
| `password_spray.py` | kerbrute passwordspray z bezpiecznikiem lockout (cap prób/konto, dedupe, alert TG) | działa |
| `target_profile.py` | orchestrator I-V-E: theHarvester→nuclei→nmap→sqlmap→dossier `Projekty/Recon/` | działa |
| `cve_correlator.py` | wersje usług → CVE → searchsploit + msfconsole → karty CVE + exploit_plan | działa |

### 1.3 Detekcja / purple team

| Narzędzie | Co robi | Stan |
|-----------|---------|------|
| `detection_validator.py` | replay technik przez Suricatę offline + matcher Sigma → tablica pokrycia technika↔detekcja | działa (9/9 PASS; złapał bug reguły 9000802) |
| `alert_roles.py` | alerty Telegram, gdy pipeline zaklasyfikuje nowego RAT/stealera (dedupe SHA256) | działa |
| Reguły własne | `clayrat.yar`+`clayrat_c2.rules`, `backdoor_easports.yar/.yml`, `local.rules` (AD), Sigma `ad_*.yml` (5), AiTM Sigma | działa |

### 1.4 OSINT

| Narzędzie | Gdzie | Do czego |
|-----------|-------|----------|
| Recon-ng 5.1.2, amass 5.1.1, subfinder 2.15, nuclei 3.11.1, httpx 1.10, theHarvester, SpiderFoot 4.0, sherlock 0.16 | `.139` (`/opt/osint`, `/usr/local/bin`) | pivot domen, atrybucja, subdomeny, tech-detect, skan CVE |
| `recon_osint.sh` / `osint_recon.sh` | `.133` pipeline (nightly, krok 3d) | Recon-ng / subfinder+amass+httpx+nuclei, cache 7 dni, alert takeover |

### 1.5 Vault / Obsidian / automatyzacja

| Narzędzie | Co robi |
|-----------|---------|
| `log_to_obsidian.sh` | haczyk Grok/Goose → wpis do Daily (bez sekretów) |
| `chatlog_to_obsidian.py` | automatyczne archiwum czatów (DSH/Goose/Grok) → `Dzienniki/Chaty/` |
| `export_vault_html.py` | stdlib Markdown→HTML, podgląd przez tunel :8081 |
| `git_autocommit.sh` | backup co 15 min do bare repo (bez GitHuba) |
| `update_wiedza.sh` | aktualizacja bazy Wiedza/ (MalwareBazaar + CISA KEV + ThreatFox, cron co 6 h) |
| `serve_dashboard.py` | statyczny dashboard + live hash-hunt (metadata MB) |

### 1.6 Boty / web / media

| Narzędzie | Gdzie | Co robi |
|-----------|-------|---------|
| obsidian-telegram-bot (`bot.py`, `vault.py`, `publish_channel.py`, `studio/render/content.py`) | `.133` | most TG→vault, publikacja kanału 16:00 UTC, wizard `/klip` |
| `profile_analyzer_bot.py` | — | bot analizujący profil TG |
| Instagram bot (`instagram.py`) | — | `/ig` — tylko własne konto Professional (czeka na token) |
| Grok-Video-Lab (`pipeline.py`, `grok_media.py`, `assemble.py`) | — | montaż klipów (ffmpeg + auto-editor) |
| maskencrypt (worker) | Cloudflare | dashboard `dash.maskencrypt.eu` |
| x-masked-optimized (worker) | Cloudflare | landing x-masked.com + `/api/contact`→TG, rate-limit KV |
| MaskGram 2.0 | Cloudflare Workers | messenger: DM, WebSocket, presence, unread |
| instagram_grid | — | generator gridów IG (9-plansza) |
| telegram_session_video | — | wideo edukacyjne o kradzieży sesji (audit.py, 9x16) |

## 2. Narzędzia zewnętrzne (zainstalowane / zweryfikowane)

### Windows `.57` (`C:\Tools`)
Ghidra 12.1.2 + JDK21 · PEStudio · DIE · FLOSS · capa · Procmon · Process Explorer · **Sysmon64 (Running)** · Wireshark · x64dbg · dnSpy · API Monitor · Python 3.12 + pefile + capstone.

### Linux `.139` (REMnux-lite)
yara · binwalk · tshark · inetsim · radare2 5.9.8 · Volatility3 (`vol`) · pefile · capstone · foremost · exiftool · tcpdump · gdb · monodis (.NET) · Evilginx2 3.3.0 CE · SET · GoPhish (service) · Suricata 7 (systemd + alerty TG).

### Linux `.133`
radare2 · yara · binwalk · tshark · pefile · mitmproxy · pipeline APK/PE/ELF · Sliver C2 · boty TG · theHarvester + nuclei (host).

### Kali (kontener RedTeam_AD / osobny)
Metasploit 6.5.0-dev (msfvenom OK) · Burp Suite Community 2026.7.2 · bettercap 2.41.5 · responder · ntlmrelayx · nmap · sqlmap · kerbrute · impacket (GetUserSPNs, secretsdump) · netexec · ldapsearch · kinit · John the Ripper · BloodHound/SharpHound · Mimikatz · Rubeus · nuclei.

### Detekcja
Suricata 7 (bridge labnet + `.139`) · Sigma (5 reguł AD + AiTM) · YARA custom · Sysmon (Windows).

## 3. Analiza — gdzie jesteśmy mocni, gdzie są luki

### Mocne strony (pełne pokrycie)
- **Statyczna analiza malware** — pełna: PE/ELF/APK, packer-detekcja, IoC, YARA, karty Obsidian.
- **IoC end-to-end** — od próbki do STIX 2.1/CSV/JSON/dashboardu, z dedupe i walidacją reguł (F1).
- **AD lab** — natywny łańcuch Windows DC + spray/Kerberoast/AS-REP/DCSync + BloodHound.
- **Purple team** — obiektywny walidator pokrycia (Suricata+Sigma), który realnie złapał bug reguły.
- **C2 ops** — Sliver CLI + raporty engagement + własny RAT z wersjonowaniem buildów.
- **Phishing** — Evilginx2 (AiTM), GoPhish+browser-inject, SET — wszystko na 127.0.0.1.
- **Dyscyplina procesowa** — automatyzacja vaultu, sekrety poza repo, logowanie do Daily.

### Luki / brakujące ogniwa
| Obszar | Czego brakuje | Dlaczego ważne |
|--------|---------------|----------------|
| **Dynamiczna RE Windows** | brak pełnego FlareVM (dysk 40 GB), x64dbg tylko offline; brak sandboxu (Cuckoo/CAPE/any.run-local) | detonacja na żywo (API call trace, memory dump) |
| **Dynamiczna Android** | emulator niestabilny (SIGSEGV), Frida wymaga pinningu wersji (16.7.19), brak Genymotion/Waydroid | dynamika to jedyna droga dla packerów (Albiriox) |
| **SIEM** | matcher Sigma jest uproszczony (syntetyczne zdarzenia), brak realnego SIEM/Wazuh/ELK | walidacja reguł SIEM na prawdziwych logach |
| **YARA na Windows** | brak (oficjalny zip 404) — tylko CLI na `.139` | skan na żywo na hoście Windows |
| **Regshot** | tylko źródła, brak exe | diff rejestru po detonacji |
| **Fuzzing / binary diffing** | brak (AFL/libFuzzer, diaphora/bindiff) | testy podatności i ewolucja rodzin |
| **Próbki** | RatOn (tylko premium), Albiriox bez droppera PENNY | kompletność analiz |
| **Integracja** | 3-4 skrypty dashboardowe obok siebie (`serve_dashboard.py`, `dash-cli.py`, `web/serve.py`) | konsolidacja, by nie duplikować |

### Doświadczone pułapki (zapisane w notatkach narzędzi)
- `sliver-py` 0.0.19 = protobufy starego Slivera (v1.5) → ręczny wire-codec v1.7.1.
- Suricata 7.0.10 + `nocase` na `http.host` = reguła nigdy nie triggeruje (bufor znormalizowany).
- Samba 4.19 Heimdal łamie Kerberoast/AS-REP/DCSync/BloodHound — rozwiązane przez Windows DC.
- pyinstaller-onefile exe starszy niż źródło — rozwiązane przez `build_agent.sh`.
- Frida 17 nie ładuje Java bridge na Android 9 — działa 16.7.19.

## 4. Wniosek

Mamy **kompletny zestaw własny** (30+ skryptów) + **narzędzia zewnętrzne rozmieszczone sensownie** po hostach (RE na `.57`, OSINT/phishing/detekcja na `.139`, pipeline/C2/boty na `.133`, AD na DC). Brakuje głównie **dynamiki** (sandbox Windows, stabilny emulator Android, realny SIEM) i kilku próbek — to naturalne „następne kroki”, a nie brak kierunku.
