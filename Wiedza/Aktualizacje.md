---
title: "Aktualizacje wiedzy"
date: 2026-08-15
updated: 2026-08-15
tags: [wiedza, changelog]
---

# Aktualizacje — dziennik zmian

Najnowsze na górze. Format: data + co dodano + źródło.
Wpisy automatyczne dopisuje `Narzedzia/update_wiedza.sh` (sekcja `### Auto`).

## 2026-08-16

- Analiza baz malware mobilnego (Android/iOS): aktywne vs historyczne → [[Zrodla_Mobile_Malware]].
- Krajobraz aktywnych rodzin 2024–2025 (RatOn, Albiriox, DroidBot, Frogblight, LightSpy) → [[Mobile_Malware_2024_2025]].
- Plan RE + analizy dynamicznej Android (Frida/MobSF/emulator) → [[Android_RE_i_Dynamiczna_Analiza]].
- Źródła: Kaspersky (+56% trojan-banker), Zscaler (+67% Android), Cleafy, ThreatFabric, Barracuda, PolySwarm.
- Karty próbek w [[Analizy/Malware]]: Albiriox, ClayRat, RatOn, DroidBot, Frogblight (hashe SHA256/MD5 + IoC z raportów i MalwareBazaar).
- Static RE (MalwareBazaar, host vserver959630): Albiriox = pełny ZipCrypto packer; ClayRat = `io.system.system903`, Accessibility+overlay+Socket, manifest szyfrowany. Szczegóły w kartach [[Albiriox_Android_RAT]] · [[ClayRat_Android_RAT]].
- jadx na ClayRat (4977 plików Java): trojanizowany klient Grok/xAI + primit'y RAT; C2 szyfrowane → do wydobycia dynamicznie (Frida).
- **Dynamiczna ClayRat**: emulator + tcpdump → C2 WebSocket `193.111.117.72:8080` (PL) + 3 backup (193.111.117.70, 185.100.157.51, 193.221.200.242). Hosting DEDIK/ALINDA. Szczegóły: [[ClayRat_Android_RAT]].

## 2026-08-15

- Utworzono strukturę `Wiedza/` (Ataki, Malware, Pentest, RedTeam, Obrona, Narzędzia, Źródła).
- Zasiano techniki ataku wg MITRE ATT&CK (fazy initial access → impact) z narzędziami i obroną.
- Katalog narzędzi ofensywnych i defensywnych.
- MOC malware (stealery, ransomware, loadery, RAT, clippery, bankery).
- Skrypt `Narzedzia/update_wiedza.sh` (MalwareBazaar + CISA KEV + ThreatFox) + cron `/etc/cron.d/obsidian-wiedza`.

### Auto
- `2026-08-22 00:00:03 UTC` Feedy: MalwareBazaar (8) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (sh); unknown (sh); DCRat (exe); unknown (exe); unknown (sh); unknown (sh)
- `2026-08-21 18:00:02 UTC` Feedy: MalwareBazaar (8) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (elf); unknown (zip); unknown (exe); unknown (zip); ArkeiStealer (exe); unknown (exe)
- `2026-08-21 12:00:05 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. PureLogsStealer (js); RemusStealer (exe); unknown (exe); unknown (exe); ConnectWise (exe); unknown (exe)
- `2026-08-21 06:00:02 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); Mirai (elf); unknown (exe); unknown (js); unknown (macho); unknown (elf)
- `2026-08-21 00:00:03 UTC` Feedy: MalwareBazaar (5) · CISA KEV (10) · ThreatFox (10) — m.in. Vidar (exe); unknown (exe); unknown (exe); unknown (js); unknown (zip); CVE-2026-72530 TrueConf
- `2026-08-20 18:00:03 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. Mirai (elf); unknown (exe); unknown (exe); unknown (exe); Vidar (exe); Mirai (elf)
- `2026-08-20 12:00:02 UTC` Feedy: MalwareBazaar (6) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (elf); unknown (elf); unknown (exe); unknown (js); unknown (exe); unknown (exe)
- `2026-08-20 06:00:04 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (elf); unknown (sh); unknown (dll); unknown (dll); unknown (dll); Mirai (elf)
- `2026-08-20 00:00:02 UTC` Feedy: MalwareBazaar (3) · CISA KEV (10) · ThreatFox (10) — m.in. WannaCry (exe); unknown (zip); unknown (elf); CVE-2026-64849 MLflow; CVE-2026-33824 Microsoft; CVE-2026-59310 Broadcom
- `2026-08-19 18:00:02 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. RemcosRAT (js); RemcosRAT (exe); unknown (exe); unknown (exe); unknown (exe); unknown (dmg)
- `2026-08-19 12:00:03 UTC` Feedy: MalwareBazaar (7) · CISA KEV (10) · ThreatFox (10) — m.in. Vidar (exe); Socks5Systemz (exe); Mirai (elf); Mirai (elf); unknown (bat); unknown (exe)
- `2026-08-19 06:00:02 UTC` Feedy: MalwareBazaar (6) · CISA KEV (10) · ThreatFox (10) — m.in. Mirai (elf); Mirai (elf); unknown (elf); unknown (elf); unknown (elf); unknown (elf)
- `2026-08-19 00:00:03 UTC` Feedy: MalwareBazaar (5) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); unknown (exe); unknown (elf); unknown (sh); CVE-2026-33824 Microsoft
- `2026-08-18 18:00:03 UTC` Feedy: MalwareBazaar (2) · CISA KEV (10) · ThreatFox (10) — m.in. Phorphiex (exe); AgentTesla (js); CVE-2026-33824 Microsoft; CVE-2026-59310 Broadcom; CVE-2026-55040 Microsoft; CVE-2026-65400 Apple
- `2026-08-18 12:00:03 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); unknown (exe); unknown (exe); unknown (sh); unknown (exe)
- `2026-08-18 06:00:06 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); unknown (zip); Mirai (elf); Mirai (elf); Mirai (elf)
- `2026-08-18 00:00:02 UTC` Feedy: MalwareBazaar (2) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); CVE-2025-62593 Ray-Project; CVE-2026-20349 Cisco; CVE-2026-68820 Microsoft; CVE-2026-72898 Metabase
- `2026-08-17 18:00:03 UTC` Feedy: MalwareBazaar (7) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); Vidar (exe); Vidar (exe); WannaCry (exe); Vidar (exe)
- `2026-08-17 12:00:02 UTC` Feedy: MalwareBazaar (6) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); unknown (exe); unknown (exe); Mirai (elf); unknown (sh)
- `2026-08-17 06:00:03 UTC` Feedy: MalwareBazaar (10) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); Mirai (elf); Mirai (elf); Mirai (elf); Mirai (elf); Mirai (elf)
- `2026-08-16 00:00:03 UTC` Feedy: MalwareBazaar (2) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); CVE-2026-20349 Cisco; CVE-2026-68820 Microsoft; CVE-2026-72898 Metabase; CVE-2026-8037 Progress
- `2026-08-15 18:00:03 UTC` Feedy: MalwareBazaar (9) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); Mirai (elf); unknown (elf); Mirai (elf); Mirai (elf)
- `2026-08-15 16:55:47 UTC` Feedy: MalwareBazaar (9) · CISA KEV (10) · ThreatFox (10) — m.in. unknown (exe); unknown (exe); unknown (sh); unknown (elf); Mirai (elf); unknown (sh)
- `2026-08-15 16:53:00 UTC` MalwareBazaar recent: unknown (exe) `7db44e145483…`; unknown (sh) `45217ea08d83…`; unknown (elf) `a8ce925aaa55…`; Mirai (elf) `bd8715a77f1d…`; unknown (sh) `0ac17b5ec739…`; Vidar (exe) `79399d2ccde8…`; Vidar (exe) `c713bb386cb5…`; unknown (sh) `7df1ad3f2961…`
