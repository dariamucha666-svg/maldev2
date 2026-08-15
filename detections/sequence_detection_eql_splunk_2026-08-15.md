---
title: "Sekwencyjne reguły — warianty EQL / Splunk"
date: 2026-08-15
type: detekcja
tags: [eql, splunk, c2, correlation, sequences]
status: experimental
---

# Sekwencyjne reguły detekcyjne — warianty EQL / Splunk

> Uzupełnienie pliku `sequence_detection_rules_2026-08-15.md` (reguły Sigma). Poniżej gotowe zapytania w **EQL (Elastic)** i **SPL (Splunk)**.
>
> **Mapowanie pól:**
> - EQL/Winlogbeat: `winlog.event_id`, `winlog.channel`, `winlog.event_data.*`
> - Splunk (Windows TA / Sysmon TA): `EventCode`, `Channel`, oraz spłaszczone pola `EventData` (`CommandLine`, `Image`, `TargetObject`, `TargetFilename`, `DestinationPort`, `ImageLoaded`, `ObjectName`, `SubjectUserName`, `TargetUserName`, `GroupName`)
>
> **Uwaga o typach:** w Sysmon `DestinationPort` bywa parsowany jako string — porównania zapisano jako `"9999"`. Jeśli w Twoim indeksie jest liczbą, zamień na `== 9999`.

---

## Sekwencja A — konto + grupa + persistence `Run`

### EQL — ścieżka Security (4720 → 4732 → 4657)

```eql
sequence by host.name with maxspan=5m
  [ any where winlog.channel == "Security" and winlog.event_id == 4720 ]
  [ any where winlog.channel == "Security" and winlog.event_id == 4732 ]
  [ any where winlog.channel == "Security" and winlog.event_id == 4657
        and winlog.event_data.ObjectName like "*CurrentVersion*Run*" ]
```

### EQL — ścieżka Sysmon (1 → 12/13 → 3)

```eql
sequence by host.name with maxspan=5m
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 1
        and winlog.event_data.CommandLine like "*python*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id in (12, 13)
        and winlog.event_data.TargetObject like "*CurrentVersion*Run*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 3
        and winlog.event_data.DestinationPort == "9999" ]
```

### Splunk — ścieżka Security

```spl
index=wineventlog sourcetype="WinEventLog:Security"
(EventCode=4720) OR (EventCode=4732) OR (EventCode=4657 AND ObjectName="*CurrentVersion*Run*")
| transaction host maxspan=5m startswith=(EventCode=4720) endswith=(EventCode=4657)
| search EventCode=4732
| table host _time EventCode SubjectUserName TargetUserName GroupName ObjectName
```

### Splunk — ścieżka Sysmon

```spl
index=wineventlog sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational"
(EventCode=1 CommandLine="*python*")
OR (EventCode IN (12,13) TargetObject="*CurrentVersion*Run*")
OR (EventCode=3 DestinationPort=9999)
| transaction host maxspan=5m startswith=(EventCode=1) endswith=(EventCode=3)
| search EventCode IN (12,13)
| table host _time EventCode CommandLine Image TargetObject DestinationPort
```

---

## Sekwencja B — keylogger + eksfiltracja

### EQL

```eql
sequence by host.name with maxspan=5m
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 1
        and winlog.event_data.CommandLine like "*keylog*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 11
        and winlog.event_data.TargetFilename like "*keylog*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 3
        and winlog.event_data.DestinationPort == "9999" ]
```

> **Wariant z hookiem (Event 7)** — zamień krok 2 (Event 11) na:
> ```eql
>   [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
>         and winlog.event_id == 7
>         and winlog.event_data.ImageLoaded like "*keylog*" ]
> ```

### Splunk

```spl
index=wineventlog sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational"
(EventCode=1 CommandLine="*keylog*")
OR (EventCode=11 TargetFilename="*keylog*")
OR (EventCode=7 ImageLoaded="*keylog*")
OR (EventCode=3 DestinationPort=9999)
| transaction host maxspan=5m startswith=(EventCode=1) endswith=(EventCode=3)
| search EventCode IN (11,7)
| table host _time EventCode CommandLine ImageLoaded TargetFilename DestinationPort
```

---

## Sekwencja C — screenshot + eksfiltracja

### EQL

```eql
sequence by host.name with maxspan=5m
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 1
        and winlog.event_data.CommandLine like "*python*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 11
        and winlog.event_data.TargetFilename like "*screenshot*" ]
  [ any where winlog.channel == "Microsoft-Windows-Sysmon/Operational"
        and winlog.event_id == 3
        and winlog.event_data.DestinationPort == "9999" ]
```

### Splunk

```spl
index=wineventlog sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational"
(EventCode=1 CommandLine="*python*")
OR (EventCode=11 TargetFilename="*screenshot*")
OR (EventCode=3 DestinationPort=9999)
| transaction host maxspan=5m startswith=(EventCode=1) endswith=(EventCode=3)
| search EventCode=11
| table host _time EventCode CommandLine TargetFilename DestinationPort
```

### Dodatek — „duży transfer" (flow, Zeek/Suricata w Splunk)

```spl
index=zeek sourcetype="bro_conn"
id.resp_p=9999 resp_bytes>1000000
| table _time id.orig_h id.resp_h id.resp_p orig_bytes resp_bytes
```

---

## Uwagi wdrożeniowe

1. **EQL `sequence`** wymaga indeksów Elastic z mapowaniem ECS/Winlogbeat; `any` to bezpieczna kategoria zdarzenia. Kolejność kroków jest wymuszona (A→B→C) w oknie `maxspan=5m`.
2. **Splunk `transaction`** grupuje po `host`; `startswith`/`endswith` wyznaczają granice transakcji, a `search`/`where` filtruje, czy wystąpił krok pośredni. Dla dużych wolumenów rozważ `eventstats`/`streamstats` zamiast `transaction` (wydajność).
3. **Escaping backslash:** w EQL/Splunk ścieżki rejestru zawierają `\` — w przykładach użyto wzorca `"*CurrentVersion*Run*"`, by uniknąć podwójnego escapowania; dla pełnej precyzji dopisz pełną ścieżkę z escapowaniem (`\\Run\\`).
4. **`DestinationPort`** — dopasuj typ (string vs int) do swojego indeksu.
5. **Event 7** (image load) jest głośny — filtruj po nazwie DLL (`ImageLoaded`), nie po samym EventID.
