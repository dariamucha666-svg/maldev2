---
title: "Sekwencyjne reguły — wariant Sentinel KQL"
date: 2026-08-15
type: detekcja
tags: [kql, sentinel, mde, c2, correlation, sequences]
status: experimental
---

# Sekwencyjne reguły detekcyjne — wariant Sentinel (KQL)

> Uzupełnienie plików `sequence_detection_rules_2026-08-15.md` (Sigma) oraz `sequence_detection_eql_splunk_2026-08-15.md` (EQL/Splunk).
>
> **Mapowanie tabel:**
> - Security (4720/4732/4657) → tabela **`SecurityEvent`**
> - Sysmon 1 (proces) → **`DeviceProcessEvents`**
> - Sysmon 12/13 (rejestr) → **`DeviceRegistryEvents`**
> - Sysmon 3 (sieć) → **`DeviceNetworkEvents`**
> - Sysmon 7 (image load) → **`DeviceImageLoadEvents`**
> - Sysmon 11 (plik) → **`DeviceFileEvents`**
>
> **Wzorzec korelacji:** self-join na `DeviceName`/`Computer` + okno czasowe `between (t .. t + 5m)` wymuszające kolejność (t1 ≤ t2 ≤ t3).

---

## Sekwencja A — konto + grupa + persistence `Run`

### A.1 — ścieżka Security (4720 → 4732 → 4657)

```kql
let window = 5m;
let a1 = SecurityEvent
    | where EventID == 4720
    | project Computer, TargetAccount, t1 = TimeGenerated;
let a2 = SecurityEvent
    | where EventID == 4732
    | project Computer, TargetAccount, t2 = TimeGenerated;
let a3 = SecurityEvent
    | where EventID == 4657
        and ObjectName has "CurrentVersion"
        and ObjectName has "Run"
    | project Computer, ObjectName, t3 = TimeGenerated;
a1
| join kind=inner a2 on Computer
| where t2 between (t1 .. t1 + window)
| join kind=inner a3 on Computer
| where t3 between (t2 .. t2 + window)
| project Computer, Account = TargetAccount, t1, t2, t3, ObjectName
```

### A.2 — ścieżka Sysmon/MDE (proces → rejestr → sieć)

```kql
let window = 5m;
let p = DeviceProcessEvents
    | where ProcessCommandLine contains "python"
    | project DeviceName, t1 = Timestamp, ProcessCommandLine;
let r = DeviceRegistryEvents
    | where RegistryKey has "CurrentVersion" and RegistryKey has "Run"
    | project DeviceName, t2 = Timestamp, RegistryKey;
let n = DeviceNetworkEvents
    | where RemotePort == 9999
    | project DeviceName, t3 = Timestamp, RemoteIP, RemotePort;
p
| join kind=inner r on DeviceName
| where t2 between (t1 .. t1 + window)
| join kind=inner n on DeviceName
| where t3 between (t2 .. t2 + window)
| project DeviceName, t1, t2, t3, ProcessCommandLine, RegistryKey, RemoteIP, RemotePort
```

---

## Sekwencja B — keylogger + eksfiltracja

```kql
let window = 5m;
let p = DeviceProcessEvents
    | where ProcessCommandLine contains "keylog"
    | project DeviceName, t1 = Timestamp, ProcessCommandLine;
let f = DeviceFileEvents
    | where FileName contains "keylog"
    | project DeviceName, t2 = Timestamp, FileName, FolderPath;
let n = DeviceNetworkEvents
    | where RemotePort == 9999
    | project DeviceName, t3 = Timestamp, RemoteIP;
p
| join kind=inner f on DeviceName
| where t2 between (t1 .. t1 + window)
| join kind=inner n on DeviceName
| where t3 between (t2 .. t2 + window)
| project DeviceName, t1, t2, t3, ProcessCommandLine, FileName, FolderPath, RemoteIP
```

> **Wariant z hookiem (Event 7 → `DeviceImageLoadEvents`):** zamień krok `f` na:
> ```kql
> let f = DeviceImageLoadEvents
>     | where FileName contains "keylog"
>     | project DeviceName, t2 = Timestamp, FileName, FolderPath;
> ```

---

## Sekwencja C — screenshot + eksfiltracja

```kql
let window = 5m;
let p = DeviceProcessEvents
    | where ProcessCommandLine contains "python"
    | project DeviceName, t1 = Timestamp, ProcessCommandLine;
let f = DeviceFileEvents
    | where FileName contains "screenshot"
    | project DeviceName, t2 = Timestamp, FileName, FolderPath;
let n = DeviceNetworkEvents
    | where RemotePort == 9999
    | project DeviceName, t3 = Timestamp, RemoteIP;
p
| join kind=inner f on DeviceName
| where t2 between (t1 .. t1 + window)
| join kind=inner n on DeviceName
| where t3 between (t2 .. t2 + window)
| project DeviceName, t1, t2, t3, ProcessCommandLine, FileName, FolderPath, RemoteIP
```

---

## Dodatek — „duży transfer"

`DeviceNetworkEvents` **nie zawiera liczby bajtów**. Dla transferu na porcie 9999 użyj danych flow (np. Zeek w logach niestandardowych / Azure NSG flow):

```kql
CommonSecurityLog   // lub custom table ze zdarzeniami flow
| where DestinationPort == 9999
| where SentBytes > 1000000 or ReceivedBytes > 1000000
| project TimeGenerated, SourceIP, DestinationIP, DestinationPort, SentBytes, ReceivedBytes
```

---

## Uwagi wdrożeniowe

1. **Kolejność wymuszona** przez `t2 between (t1 .. t1 + window)` i `t3 between (t2 .. t2 + window)` — gwarantuje t1 ≤ t2 ≤ t3 w oknie 5 min.
2. **`join kind=inner`** — po pierwszym joinie kolumny `t1`/`t2` współistnieją; drugi join dołącza `t3`. W razie duplikatów kolumn dodaj `| project-rename`/`extend`.
3. **Tabele MDE** (`DeviceProcessEvents` itd.) są dostępne przy integracji z Microsoft Defender for Endpoint. Przy czystym Sysmonie (tabela `Event`) pola `EventData` wymagają parsowania XML (`parse_xml(EventData)` / `extract`) — wtedy mapowanie wykonuje się ręcznie.
4. **`SecurityEvent`** — dla 4657 kolumna `ObjectName` przechowuje ścieżkę klucza; jeśli w Twoim workspace pole nazywa się inaczej, dopasuj (niektóre wdrożenia używają `EventData`/`RenderedDescription`).
5. **Escaping backslash** — w KQL `has`/`contains` na ścieżkach użyto dwóch osobnych warunków (`has "CurrentVersion" and has "Run"`), by uniknąć escapowania `\`.
6. **Wydajność** — self-join bywa kosztowny; zawęź `let` o `where Timestamp > ago(1d)` i rozważ `mv-apply`/`row_window_session` (preview) dla dużych wolumenów.
