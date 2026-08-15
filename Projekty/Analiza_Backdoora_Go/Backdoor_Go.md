---
title: "Analiza Backdoora Go"
date: 2026-08-14
updated: 2026-08-14
tags: [projekt, malware, backdoor, go]
status: completed
priority: high
sha256: 178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4
category: backdoor
---
# Backdoor Go (easports.gg)

Krótki indeks analizy. Detale: [[Analiza_Backdoora_Go_Detale]] · IoC: [[IOC_Backdoor]] · pełna karta próbki: [[Analizy/Malware/178cb931 Precision Agriculture Go PE]]

## Identyfikacja

| Pole | Wartość |
|------|---------|
| Plik | `141935c46a5c4ff1b84b433e84f36e61.exe` |
| Źródło stage-1 | `http://192.162.199.149/uploads/141935c46a5c4ff1b84b433e84f36e61.exe` |
| Kwarantanna | `/root/samples/quarantine/` |
| Typ | PE32+ GUI x86-64, Go **1.25.4**, garble |
| Rozmiar | 3 344 232 B |
| SHA256 | `178cb931cc846c4ac7bbf2370259e8b9f7d8a45459974115818b5c1e608533c4` |
| Overlay | 2408 B — Authenticode PKCS#7, CN **`easports.gg`** |
| Cert validity | 2026-07-30 → 2027-07-30 (self-signed / fałszywy branding EA) |

Stage-1 to installer Electron (fałszywe „Runtime Components”) — [[Exodus_Modyfikacja]]. Ten PE jest **stage-2**.

## Werdykt roboczy

Mały/średni, zaciemniony **Go 1.25.4 GUI**. Motyw stringów: *Precision Agriculture* + *elevator/cabin*. **0 URL, 0 IP** w plaintext. To **nie** pełny implant Sliver (za mały, brak typowego stosu C2 w pakietach).

Wygląd: overlay / generator logów **albo** custom RAT z C2 złożonym w runtime (`.rdata` / garble). Są stringi admin API (`NetUserAdd`, `LogonUserW`, `CreateProcessW`) — nieudowodnione, czy są wołane.

**Nie detonowany.** Static only na `.133` + headless Ghidra na `.57`.

## Pipeline

Ostatni run: `FORCE=1 pipeline.sh` 21:31 UTC 14.08 — OK, capa timeout 45 s.

Zobacz [[Pipeline_Analizy]].
