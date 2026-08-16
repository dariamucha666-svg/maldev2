---
title: "Android RE + analiza dynamiczna — plan"
date: 2026-08-16
updated: 2026-08-16
tags: [lab, tools, android, re, dynamic, frida, mobsf, emulator]
status: plan
---

# Android RE + analiza dynamiczna (roadmap)

Powiązane: [[Narzedzia_RE]] (Windows RE) · [[Zrodla_Mobile_Malware]] (bazy próbek) · [[Mobile_Malware_2024_2025]] (rodziny) · hosty: [[Lab/Hosts]]

Cel: rozszerzyć istniejący pipeline RE (Windows) o **Android**. Faza 1 = statyczna (jak dotychczas), faza 2 = dynamiczna (emulator + Frida), faza 3 = automatyzacja.

## OPSEC / izolacja (najpierw!)

- **Nigdy** nie odpalaj próbki na telefonie codziennego użytku ani na hoscie produkcyjnym.
- Emulator **bez** konta Google, **snapshot** do przywracania, **host-only** sieć.
- Karty NFC: tylko dedykowane / testowe (RatOn / NFSkate).
- Próbki trzymać jako `infected`-zip; nie rozpakowywać bez potrzeby.
- Zob. [[OPSEC/Urzadzenia_i_siec]] i [[OPSEC/Checklist_OPSEC]].

## Faza 1 — statyczna (częściowo już w labie)

| Krok | Narzędzie | Co daje |
|------|-----------|---------|
| Rozpakuj | `apktool` | manifest, zasoby, smali |
| DEX → Java | `jadx` | logika aplikacji |
| Packer / ochrona | `apkid` | wykrycie packera (Zirex / hhcbcu itd.) |
| Uprawnienia / komponenty | `androguard` / MobSF static | exported activity, deeplinki, provider |
| Native `.so` | Ghidra / `rizin` | JNI, hook stack (Dobby / shadowhook / bytehook) |
| Stringi / URL | `strings` / FLOSS | C2, hardcoded |
| Capabilities | `capa` / MobSF | mapowanie zachowań |
| Manifest audit | MobSF / `apkleaks` | nadużycia Accessibility / overlay |

## Faza 2 — dynamiczna

| Warstwa | Narzędzie | Co obserwujemy |
|---------|-----------|----------------|
| Emulator | AVD / Genymotion / Waydroid | izolowane urządzenie (snapshot) |
| Hook runtime | **Frida** + `objection` | wywołania API, SSL-unpinning, dump pamięci |
| Sieć | `mitmproxy` (lab `.133`) + Frida cert-unpinning | C2, exfil |
| PCAP | `tcpdump` / `tshark` | wzorce ruchu |
| System | `logcat`, `strace`, `dumpsys`, `getprop` | aktywność usług, dostęp |
| Zachowania | **MobSF dynamic** | raport behawioralny + wywołania |
| NFC | emulator z NFC + `NFCGate` | RatOn / NFSkate |
| Automatyka UI | `uiautomator` / Appium | obserwacja ATS w sandboxie |

## Faza 3 — automatyzacja (pipeline)

1. Pobranie (MalwareBazaar / Koodous) → hash → karta próbki.
2. Statyczna: apktool + jadx + apkid + MobSF → manifest / uprawnienia / deeplinki / IoC.
3. Dynamiczna: emulator + skrypty Frida + PCAP → raport.
4. IoC → [[Analizy/IOC]] + YARA / Sigma / Suricata (jak dotychczas).
5. Wynik → karta w [[Analizy/Malware]] + wpis [[Analizy/Threat_Intel_MOC]].

## Publiczne raporty jako skrót (zanim odpalimy dynamikę)

Tria.ge / Any.Run / Joe Sandbox / Hybrid Analysis — sprawdzić hash, zanim detonujemy sami. Oszczędza czas i ryzyko.

## Decyzje do podjęcia (następna sesja)

- [ ] Wybór emulatora (AVD vs Waydroid na `.139` vs Genymotion) — pod kątem dysku (40 GB).
- [ ] Która rodzina pierwsza: RatOn (bogate TTP) czy Albiriox (świeży, MaaS)?
- [ ] Czy NFC relay testujemy lokalnie (2× telefon + NFCGate), czy tylko opisujemy z raportów.
- [ ] Frida na `.139` (REMnux-lite) czy osobny host.