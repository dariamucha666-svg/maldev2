---
title: "Threat Intel — MOC (wszystkie znaleziska)"
date: 2026-08-15
updated: 2026-08-15
tags: [threat-intel, moc, ioc, detection]
status: active
category: moc
---

# Threat Intel — Mapa wszystkich znalezisk

Jedno źródło: rodzina → hash → C2 → IOC → detekcja → nota.

## Próbki z korpusu (RE end-to-end)

| Rodzina | Hash | C2 | Detekcja | Nota |
|---------|------|-----|----------|------|
| **XWorm V7.4** (njRAT-pochodna) | `7ae00fe8…` | `tuffman-50943.portmap.host:50943` (193.161.193.99) | Suricata 9000601-3, Sigma, YARA `XWorm_V74_Key` | [[7ae00fe8 system32 RAT deep dive]] · [[IOC_XWorm_tuffman]] |
| **Lumma Stealer** | `00d3f42d…` | `digitden.cyou` (64.89.161.173) | Suricata 9000701-2, Sigma, YARA `Lumma_00d3f42d_C2_digitden` | [[Clipper_Stealer_Analiza]] |
| **Go Backdoor** (easports.gg, garble) | `178cb931…` | `https://suahoje.com:3000` / `off-game.com` / stage-2 `192.162.199.149` | YARA `Backdoor_Easports`, Sigma xmask | [[IOC_Backdoor]] · [[Backdoor_Go]] · [[Backdoor_Go_Garble_DEobfuscation]] |
| NanoCore / Lumma / NWH / Vidar (korpus) | różne | — | CTI (MalwareBazaar) | [[Klasyfikacja_Korpus]] · [[DotNet_cluster]] |

## Mobile (Android) — 2024–2025 (IoC zebrane, RE przed nami)

| Rodzina | Hash (przykład) | C2 | Status | Nota |
|---------|-----------------|-----|--------|------|
| **Albiriox** (RAT/MaaS, ODF) | `8703ee86…` (apk, MB 2026-07) | `194.32.79.94` | IoC zebrane | [[Albiriox_Android_RAT]] |
| **ClayRat** (RAT, masquerade) | `78878d33…` (apk, MB 2026-03) | `193.111.117.72:8080` (WS) + 3 backup | IoC + dynamic | [[ClayRat_Android_RAT]] |
| **RatOn** (banker, NFC+ATS) | `bf82609c…` (PolySwarm) | — | IoC zebrane | [[RatOn_Android_banker]] |
| **DroidBot** (RAT/MaaS, VNC) | MD5 `0137a72f…` (Cleafy) | — | IoC zebrane | [[DroidBot_Android_RAT]] |
| **Frogblight** (banker, WebView inj) | MD5 `9dac2320…` (Securelist) | REST (Retrofit) | IoC zebrane | [[Frogblight_Android_banker]] |

## Narzędzia przeanalizowane (źródła / dynamicznie)

| Kategoria | Narzędzia | Detekcja |
|-----------|-----------|----------|
| Phishing | SET, Evilginx2, GoPhish, SocialFish, ZPhisher | Suricata 90001xx-90004xx, YARA `phishing_tools.yar` |
| Keyloggery | C++/Python/Advanced, Refog/Spyrix | YARA `keyloggers.yar` |
| Clippery | Laplas, BTC-Clipper, Raccoon, C++ clipper | YARA `clipper_stealer.yar` |
| Stealer kont Telegram | stealer-telegram-acc, TeleKiller, PS | YARA `telegram_stealer.yar` |

## Operacyjny IDS (`.139`)

- **Suricata 7.0.10** (systemd, eth0) + `all_lab.rules` (15 reguł).
- **Telegram alerting**: `suricata-telegram.service` (eve.json → Telegram).
- **Threshold**: reguły Telegram (9000501-3) rate-limit 1/300s (eliminacja self-trigger).

## Reguły detekcji — lokalizacje

```
/android-pipeline/tools/
  detection/all_lab.rules        (Suricata, 15 reguł)
  detection/phishing_tools.rules
  detection/keylogger_exfil.rules
  detection/xworm_tuffman.rules
  detection/lumma_digitden.rules
  sigma-rules/*.yml             (Sigma: xmask, xworm, lumma)
  yara-rules/custom/*.yar       (phishing, keyloggers, clipper_stealer, telegram_stealer, xworm)
```

## Luźne końce

- Refog/Spyrix, Laplas Clipper, Still Sync, Windows Telemetry Update — **brak próbki**.
- Keylogger pyHook (TeleKiller) — pywin32/pyHook EOL, download broken.
- Lumma: 5 próbek w korpusie do porównania C2.
