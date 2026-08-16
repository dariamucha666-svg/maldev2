---
tags: [lab, tools, remnux, flare]
date: 2026-08-15
updated: 2026-08-15
---

# Narzędzia RE w labie

Nie instalujemy pełnego **FlareVM** ani **REMnux ISO** na tych VPS (dysk ~40 GB, Flare chce 60–80 GB).

Pełna mapa sesji: [[Lab/Recap 2026-08-15]] · hosty: [[Lab/Hosts]] · Android: [[Android_RE_i_Dynamiczna_Analiza]]

## Windows `.57` (`C:\Tools`)

| Narzędzie | Do czego | Stan |
|-----------|----------|------|
| PEStudio | PE: importy, stringi, sekcje | było |
| Detect It Easy | typ / packer | 15.08 |
| FLOSS | stringi zaciemnione | 15.08 |
| capa | zachowania | 15.08 |
| Procmon | FS / rejestr / procesy | było |
| Process Explorer | drzewo procesów | 15.08 |
| Sysmon64 | log zdarzeń | 15.08, Running |
| Wireshark | sieć | było |
| Ghidra 12 | dekompilacja | było |
| x64dbg | debugger | było |
| dnSpy | .NET | 15.08 |
| API Monitor | API | było |
| Python 3.12 + pefile + capstone | skrypty | 15.08 |
| YARA | reguły | brak na Win (404 zip) — użyć `.139` |
| Regshot | diff rejestru | tylko źródła |

## Linux `.139` (REMnux-lite)

`yara` `binwalk` `tshark` `inetsim` `radare2 5.9.8` `vol` (Volatility3) `pefile` `capstone` `foremost` `exiftool` `tcpdump` `gdb`

## Linux `.133`

Już było: radare2, yara, binwalk, tshark, pefile, mitmproxy. Tu siedzi pipeline + vault + bot — nie pakować ciężkiego GUI.

## Pierwszy przebieg (static only)

1. DIE albo PEStudio
2. FLOSS
3. capa
4. Ghidra / r2

Bez detonacji, bez łączenia próbki z internetem. [[Home]]
