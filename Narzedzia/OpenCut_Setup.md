---
tags:
  - opencut
  - video
  - windows
updated: 2026-08-14
---

# OpenCut Setup

Edytor wideo / tool chain **na C2 #3** (Windows Server `5.175.189.57`), nie na Ubuntu pipeline.

Powiązane: [[Laboratorium_Windows]] · [[Infrastruktura_C2]]

## Co było

Na `.57` działały równolegle:

| Proces | Rola | Stan po 14.08 |
|--------|------|----------------|
| `node` — OpenCut | web UI edytora | **zatrzymany** |
| `python` — capcut-mate | helper | **zatrzymany** |
| Scheduled task `OpenCutWeb` | autostart | **Disabled** |
| Scheduled task `CapCutMate` | autostart | **Disabled** |

Cel pauzy: zwolnić RAM pod Ghidra/x64dbg (~646 MB wolne → **~3 GB**). Aplikacje nie zostały usunięte.

Na C2 #1 (`5.175.189.133`) **brak** instalacji OpenCut (`/opt`, `/root` — pusto pod tą nazwą).

## Wznowienie (gdy lab RE nie pracuje)

1. RDP / WinRM na `5.175.189.57`
2. Task Scheduler → `OpenCutWeb` / `CapCutMate` → Enable + Run
3. Albo ręcznie odpalone skróty, które były na pulpicie

Nie odpalać OpenCut równolegle z ciężkim Ghidra na Eval z ~6 GB RAM.

## Relacja do pipeline

OpenCut **nie** jest częścią [[Pipeline_Analizy]]. To osobny workload na hoście Windows.

Auto-montaż na kanał (nie OpenCut): [[Studio_Klip]].
