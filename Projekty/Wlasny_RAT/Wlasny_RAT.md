---
title: "Własny RAT"
date: 2026-08-15
tags: [projekt]
status: completed
priority: medium
category: lab
---

# Własny RAT

Karta projektu z [[Droga_przez_cyberbezpieczenstwo]]. Kod implanta **nie** leży w vaultcie.

## Cel

Labowy agent + serwer C2 w Pythonie (port 4444): `whoami`, `sysinfo`, `screenshot`, keylog, `shell`, persistence (Run key).

## Status

- [x] Zakres opisany w recapie ścieżki
- [x] Notatka projektu
- [ ] Werdykt — kod poza vaultem, tu tylko dokumentacja

## Powiązane

- [[Droga_przez_cyberbezpieczenstwo]]
- [[Wlasny_Stealer]]
- [[Backdoor_Go]]
- [[Infrastruktura_C2]]
- [[Dashboard]]
- [[Backlog]]

## Dynamiczna analiza (2026-08-16)

Uruchomiono i przeanalizowano dynamicznie na .57. Raport: [[2026-08-16_dynamiczna_analiza_RAT_57]] · log: [[2026-08-16_dynamiczna_analiza_RAT_57_log]].

- Kod: **C:/Users/Administrator/Desktop/agent.py** na .57 (C2_HOST=5.175.189.133, C2_PORT=9999 — uwaga: w karcie wyżej jest 4444, realny port to 9999).
- Protokół: surowy reverse shell (nie JSON jak rat-c2/server.py).
- **agent.exe przebudowany** (2026-08-16) — nowy SHA256 6a97d2a0…, 8 441 645 B. Screenshot + keylog domknięte w sesji interaktywnej (session 2).
- Helpery WinRM do .57: /root/run57.py, /root/ps57.py, /root/deploy57.py.
