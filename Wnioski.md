---
title: "Wnioski — co już mamy zrobione"
date: 2026-08-16
updated: 2026-08-16
tags: [wnioski, recap, moc, status, lekcje]
status: active
category: podsumowanie
---

# Wnioski — co już mamy zrobione

Synteza sesji 14–16.08: infrastruktura, lab RE, pipeline, malware, detekcja, AD, phishing, web. Powiązane: [[Sesje_MOC]] · [[Recap_2026-08-16]] · [[Recap_2026-08-16_narzedzia_redteam]] · [[Lab/Recap 2026-08-15]] · [[Lab/Recap 2026-08-14]] · [[Daily/2026-08-16]] · pełna inwentaryzacja narzędzi: [[Narzedzia/Inwentaryzacja_Narzedzi]]

---

## 1. Co stoi (infrastruktura)

| Host | Rola | Kluczowe elementy |
|------|------|-------------------|
| `.133` (vserver959630) | Ubuntu 24.04 — pipeline, vault, boty | pipeline APK + PE/ELF, kwarantanna, obsidian-vault, Caddy, fail2ban, cloudflared, sliver-server, boty TG |
| `.139` (vserver580088) | Debian 12 — RE/phishing/detekcja | yara/binwalk/tshark/inetsim/radare2/vol, Evilginx2, SET, GoPhish, Suricata 7 + alerty TG |
| `.57` (vserver781193) | Windows Server 2022 Eval | narzędzia RE (Ghidra, x64dbg, PEStudio, ProcMon…), **promowany na DC**, lab RAT |

Działa: RE statyczny (PE/ELF/APK), pipeline z cronem, detekcja, AD, phishing-lab, C2 (Sliver + własny RAT), web (x-masked.com, MaskGram, maskencrypt), boty TG.

## 2. Najważniejsze osiągnięcia merytoryczne

- **Pipeline PE/ELF** (analyze_pe.py → IoC → YARA → STIX 2.1/CSV/JSON → karta Obsidian → dashboard CLI) przetestowany na realnych próbkach: PE→`rat (0.85)`, ELF→`cryptominer (0.90)`, YARA TP=2/FP=0/FN=0.
- **Pipeline APK** (analyze_apk.py): apkid→odzysk manifestu→androguard→jadx→IoC→YARA; ClayRat: 4977 plików Java, 46 uprawnień, „szyfrowany" manifest = fake (deflate).
- **ClayRat — pełna mapa C2**: trojanizowany klient Grok (xAI); WebSocket `193.111.117.72:8080` (PL/DEDIK, bulletproof) + beacon `packwatheboss.lol` → `91.210.168.138:80` (RU/Timeweb), AES + DEXGuard; dowód w pcap. **To było możliwe dopiero dynamicznie** (emulator + tcpdump + Frida 16.7.19).
- **XWorm V7.4** — C2 odszyfrowane (`tuffman-50943.portmap.host:50943`); **Lumma** — wspólny C2 `64.89.161.173`; **TeleKiller** — reverse shell potwierdzony; **Go backdoor** — garble potwierdzony, hipoteza żywych API otwarta.
- **Windows AD (faza 2) domknięta**: na `.57` działa to, co na Sambie 4.19 miało niuanse — DCSync (11 kont), Kerberoasting, AS-REP, BloodHound, spray.
- **Detekcja**: Suricata+Sigma pokrywają 9/9 technik (replay validator = PASS), korpus walidowany (TP 5→6, FP 5→2).
- **Phishing**: Evilginx2 AiTM domknięty (cookie rewrite mock.local→evil.local, session recording po fixie Host-header), SET zweryfikowany, GoPhish+browser-inject (keylog + form-hijack, exfil poza frameworkiem), przewodnik phishletów + detekcja AiTM (Sigma).
- **Własny RAT**: agent JSON-ND, keylogger WH_KEYBOARD_LL (40 klawiszy przechwycone), screenshot po fixie sesji (tscon), persistence, pełne sprzątanie po testach.

## 3. Lekcje / wnioski przekrojowe

1. **Nie walcz z frameworkiem — zmień platformę.** Samba 4.19 + impacket = 4 martwe techniki (to ograniczenia toolchainu, nie labu). Promocja .57 do Windows DC dała natywny łańcuch w jeden dzień.
2. **Statyka ma ścianę, dynamika ją przebija.** Albiriox (prawdziwy packer ZipCrypto, klucz w dropperze) — statycznie niemożliwy; ClayRat C2 — znaleziony dopiero w emulatorze. Wniosek: packer-detekcja i emulatory to osobne kompetencje do rozwijania.
3. **Środowisko wykonania decyduje o artefaktach.** Sesja 0 (SYSTEM) = brak pulpitu/klawiszy; sesja interaktywna + `tscon` = działający screenshot i keylog. To musi być w runbooku każdego testu agenta.
4. **Wersjonowanie artefaktów zapobiega głupim błędom.** „exe starszy niż źródło" (kończył się exit 0) → `build_agent.sh` z BUILD_ID, freshness-check i manifestem.
5. **Izolacja i sprzątanie to część wyniku, nie dodatek.** Phishing na 127.0.0.1/developer-mode, UFW DENY, firewall DC zawężony do .133/.139, po demo: zatrzymane agenty, usunięte konta/Run, C2 down. Zero realnych celów, zero cracked narzędzi (Cobalt Strike świadomie nie).
6. **Detekcja warta tyle, ile walidacja.** Replay 9 technik przez `detection_validator.py` daje obiektywny PASS/FAIL na technikę; korpus TP/FP zamiast wiary w regułę.
7. **Dokumentacja = proces, nie czynność.** Notatki od razu, sekrety poza vaultem, hook `log_to_obsidian.sh`, auto-sync git co 15 min, chaty zapisywane do Dzienniki/Chaty. Dzięki temu ten przegląd był możliwy w ~10 minut.
8. **Ograniczenia sprzętowe kształtują architekturę.** FlareVM/REMnux nie wejdą na 40 GB VPS → mini-lab rozproszony (Windows RE na .57, CLI na .139). Zagnieżdżony KVM (QEMU/Q35) działa, ale emulator potrafi paść (SIGSEGV).

## 4. Otwarte sprawy (next)

- `IG_ACCESS_TOKEN` pusty — bot IG czeka na token.
- RatOn: próbki tylko PolySwarm/VT (premium) — nie do zdobycia z MalwareBazaar.
- Albiriox: potrzebny dropper PENNY (klucz) albo rezygnacja z dynamiki.
- Emulator Androida padł — restart w razie potrzeby; dalej: Frida na kolejnych rodzinach.
- Większy dysk przed powrotem do FlareVM/REMnux.
- DC publiczny z celowo słabymi hasłami lab — utrzymywać firewall zawężony albo wyłączyć.
- Artefakt `opstest01.exe` (Sliver, 19 MB) — zdecydować: zachować w labie czy skasować.
- `main.main` Go backdoora: domknąć dekompilację + overlay 2408 B + lista `main.*` z `.symtab`.

## 5. Werdykt

W 3 dni powstał **kompletny, legalny lab red/blue team end-to-end**: analiza statyczna i dynamiczna malware (Windows/Linux/Android), detekcja z walidacją, AD z natywnym łańcuchem ataku, phishing AiTM, własne narzędzia (pipeline, C2, builder, validator) — wszystko udokumentowane w vaultcie, z sekretami poza repozytorium i z jasno zdefiniowanymi granicami etycznymi. Największy przyrost wartości w najbliższym kroku: **domknięcie otwartych spraw z §4** (token IG, RatOn, Albiriox, dekompilacja backdoora), nie budowanie nowych rzeczy.

---

## Aneks: mapa vaultu (co jest gdzie, 266 notatek)

| Obszar | Zawartość | Wejście |
|--------|-----------|---------|
| **Analizy malware** (42) | 21 kart rodzin + 20 w Analizy/XMask: Go backdoor 178cb931, XWorm, Lumma, ClayRat, Albiriox, RatOn, DroidBot, Frogblight, Zirex, NFC skimmer, SMS stealery, Chrome stealer, .NET cluster, TeleKiller, Laplas, Keylogger | `Analizy/Malware/README` |
| **Wiedza** (31) | baza zagrożeń: Ataki (MITRE), Malware, Pentest (Burp, John, MitM, obfuskacja…), RedTeam, Obrona + feedy auto (MalwareBazaar/CISA KEV/ThreatFox co 6 h) | `Wiedza/README` |
| **Projekty** (17) | Własny RAT (done), Własny Stealer (slot), Pipeline, Infrastruktura C2, Dashboard Bot, Backdoor Go, OCR Android, IG bot, Status projektów, „Pentesty na TG" (edukacja) | `Projekty/Status_Projektow` |
| **Model I-V-E** (23) | metodologia Informacja→Podatności→Eksploatacja + MOC-e faz + analiza dynamiczna demo (nmap, msf_search MS17-010) | `Model_IVE/IVE_MOC` |
| **Detekcje** (10) | reguły na **własne C2** (Sigma/YARA/Suricata, sekwencje + EQL/Splunk/KQL), AiTM, walidacja korpusu | `detections/README` |
| **Narzedzia** (31+ plików) | 30+ własnych skryptów + reguły — pełny spis: [[Narzedzia/Inwentaryzacja_Narzedzi]] | `Narzedzia/Automatyzacja` |
| **OPSEC** (12) | baza obrony osobistej + hardening `.133` (SSH klucze, sysctl, UFW) | `OPSEC/README` |
| **Red Team AD** | lab Samba → Windows DC: łańcuch ataku + detekcja (Suricata/Sigma) | `Lab/RedTeam_AD/Status_Lab` |
| **Phishing** | Evilginx2, GoPhish+inject, SET, phishlety, detekcja AiTM | `Narzedzia/Phishing_Deep_Dive` |
| **Kanał XMaskPoland** | serie HACKPLUG (droga hakera) + opsec.exe (obrona), klipy, `/graj` (3 poziomy/8 ataków/34 metody), studio | `XMask/Serie` |
| **Dzienniki** | Daily 14–16.08, sesje operacyjne, archiwum czatów (DSH/Goose/Grok), Telegram | `Dzienniki/` |
| **Raporty** (9) | dynamiczna analiza RAT .57 (+log), optymalizacja RAT, Sliver engagement, detection coverage, C2 infrastructure, server comparison, artefakty agenta | `raports/` |
| **Zasoby** | droga nauki, linki, szablony, pluginy, dashboard | `Zasoby/Droga_przez_cyberbezpieczenstwo` |
