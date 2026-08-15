---
title: "Laboratorium Windows"
date: 2026-08-14
updated: 2026-08-14
tags: [projekt, lab]
status: completed
priority: medium
category: lab
---
# Laboratorium Windows

Host do **analizy dynamicznej i głębokiego RE** — nie do produkcji C2.

Powiązane: [[Infrastruktura_C2]] · [[Backdoor_Go]] · [[Analiza_Backdoora_Go_Detale]] · [[OpenCut_Setup]] · [[Lab/Recap 2026-08-14]]

## Host

| | |
|--|--|
| VPS | C2 #3 |
| IP | `5.175.189.57` |
| Hostname | `WIN-T5BVVHUNVJI` |
| OS | Windows Server 2022 Evaluation |
| Dostęp | WinRM `5985`, RDP `3389` (SSH zamknięty) |
| Rola | Ghidra / PEStudio / x64dbg / ProcMon / Wireshark |

Hasła nie zapisujemy w vaultcie — patrz [[Lab/Hosts]].

## Narzędzia (`C:\Tools`)

| Narzędzie | Ścieżka |
|-----------|---------|
| ProcMon | `C:\Tools\Procmon\Procmon64.exe` |
| PEStudio | `C:\Tools\PEStudio\pestudio\pestudio.exe` |
| API Monitor | `C:\Tools\APIMonitor\...\apimonitor-x64.exe` |
| x64dbg | `C:\Tools\x64dbg\release\x64\x64dbg.exe` |
| Ghidra 12.1.2 | `C:\Tools\Ghidra\ghidra_12.1.2_PUBLIC\` |
| JDK 21 | `C:\Tools\jdk\jdk-21.0.12+8\` |
| Wireshark | zainstalowany 14.08 |

Skróty na pulpicie. Projekt Ghidra: **BackdoorLab**.

## Próbka na hoście

- `C:\Tools\samples\backdoor.exe` — kopia `141935c46a5c4ff1b84b433e84f36e61.exe`
- Hash zgodny z [[IOC_Backdoor]] — **nie uruchamiana** w sieci
- Output Ghidra: `C:\Tools\ghidra_out\`

Headless auto-analysis ~44 s, **~1930 funkcji**.

## Higiena z 14.08

Zrobione:

- Zatrzymane `node` (OpenCut) i `python` (capcut-mate) — zwolnione RAM ~646 MB → **~3 GB**
- Zadania `OpenCutWeb` / `CapCutMate` ustawione na **Disabled** (pauza, nie usunięcie)
- Szczegóły edytora: [[OpenCut_Setup]]

Zasady detonacji:

1. Offline / izolowana sieć.
2. Nie odpalać PE z hosta analizy `.133`.
3. ProcMon + Wireshark **przed** pierwszym runem.
4. Snapshot / świadomość, że to Eval — bez produkcji.

## Co jeszcze na `.57`

- PEStudio + x64dbg offline — potwierdzić czy `LogonUserW` / `NetUserAdd` są żywe, czy tylko symbole `x/sys`.
- Overlay 2408 B (Authenticode PKCS#7, CN `easports.gg`).
- Dekompilacja `main.main` + resolvera `main.itnlwdcdwymtd` (skrypt `DecompTwo.java` był w toku).
