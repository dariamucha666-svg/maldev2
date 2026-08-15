---
title: "Sekwencyjne reguły detekcyjne C2"
date: 2026-08-15
type: detekcja
tags: [sigma, correlation, c2, dfir, sequences]
status: experimental
---

# Sekwencyjne reguły detekcyjne — 2026-08-15

> **Cel:** wykrywanie wieloetapowych sekwencji ataku opisanych w `Analiza_artefaktów_agenta_57.md`.
> **Format:** reguły atomowe Sigma (pojedyncze zdarzenia) + reguły korelacyjne Sigma (`correlation`, `type: temporal`, okno 5 minut).
>
> ⚠️ **Korekty techniczne:**
> - **Sysmon Event 3** nie zawiera liczby przesłanych bajtów — „duży transfer" wymaga danych flow (Zeek `conn.log` / Suricata), opisano w Sekwencji C.
> - **Sysmon Event 5/6** to odpowiednio *process terminated* i *driver loaded* — **nie** dotyczą GDI. Przechwycenie ekranu obserwujemy przez Event 1 (proces) + Event 11 (utworzenie `screenshot_*.png`) + Event 3 (połączenie).
> - **USN Journal** nie jest standardowym `logsource` Sigma — dla „utworzenia pliku" używa się Sysmon **Event 11 (FileCreate)**; USN opisano jako źródło dodatkowe.

---

## Sekwencja A — konto + grupa + persistence w `Run`

**Opis ataku:** atakujący tworzy konto (`net user /add`), dodaje je do grupy uprzywilejowanej (np. `Administrators`), a następnie ustawia autostart w kluczu `Run`. Celem jest trwały dostęp uprzywilejowany.

**Zdarzenia źródłowe:**

| Kanał | EventID | Znaczenie |
|---|---|---|
| Security | 4720 | utworzenie konta użytkownika |
| Security | 4732 | dodanie do lokalnej grupy |
| Security | 4657 | modyfikacja wartości rejestru (klucz `Run`) |
| Sysmon | 1 | uruchomienie agenta (proces) |
| Sysmon | 12/13 | utworzenie/ustawienie klucza/wartości rejestru |
| Sysmon | 3 | połączenie sieciowe na 9999 |

### Reguły atomowe (Security)

```yaml
# A1 — utworzenie konta
title: A1 - User Account Created
id: 6a11a0e0-0001-4a01-9a01-000000000001
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4720
  condition: selection
---
# A2 — dodanie do grupy lokalnej
title: A2 - User Added to Local Group
id: 6a11a0e0-0001-4a01-9a01-000000000002
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4732
  condition: selection
---
# A3 — zmiana wartości w kluczu Run
title: A3 - Run Key Registry Value Modified
id: 6a11a0e0-0001-4a01-9a01-000000000003
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4657
    ObjectName|contains: '\CurrentVersion\Run'
  condition: selection
```

### Reguły atomowe (Sysmon)

```yaml
# A4 — uruchomienie agenta (python)
title: A4 - Agent Process Launched
id: 6a11a0e0-0001-4a01-9a01-000000000004
status: experimental
logsource:
  product: windows
  category: process_creation
  service: sysmon
detection:
  selection:
    EventID: 1
    CommandLine|contains:
      - 'agent.py'
      - 'python'
  condition: selection
---
# A5 — zmiana rejestru (Run)
title: A5 - Run Key Registry Change (Sysmon)
id: 6a11a0e0-0001-4a01-9a01-000000000005
status: experimental
logsource:
  product: windows
  category: registry_event
  service: sysmon
detection:
  selection:
    EventID:
      - 12
      - 13
    TargetObject|contains: '\CurrentVersion\Run'
  condition: selection
---
# A6 — połączenie na 9999
title: A6 - Network Connection to Port 9999
id: 6a11a0e0-0001-4a01-9a01-000000000006
status: experimental
logsource:
  product: windows
  category: network_connection
  service: sysmon
detection:
  selection:
    EventID: 3
    DestinationPort: 9999
  condition: selection
```

### Reguły korelacyjne (okno 5 min)

```yaml
# Korelacja A-security: 4720 -> 4732 -> 4657
title: Account + Privilege Escalation + Run Persistence (5m)
id: 6a11a0e0-0002-4a01-9a01-000000000010
status: experimental
correlation:
  type: temporal
  rules:
    - 6a11a0e0-0001-4a01-9a01-000000000001  # A1 4720
    - 6a11a0e0-0001-4a01-9a01-000000000002  # A2 4732
    - 6a11a0e0-0001-4a01-9a01-000000000003  # A3 4657 Run
  timespan: 5m
  group-by:
    - SubjectUserName
    - Computer
  condition: A1 and A2 and A3
---
# Korelacja A-sysmon: Event1 -> Event12/13 -> Event3
title: Agent Launch + Registry Change + C2 Beacon (5m)
id: 6a11a0e0-0002-4a01-9a01-000000000011
status: experimental
correlation:
  type: temporal
  rules:
    - 6a11a0e0-0001-4a01-9a01-000000000004  # A4 Event 1
    - 6a11a0e0-0001-4a01-9a01-000000000005  # A5 Event 12/13
    - 6a11a0e0-0001-4a01-9a01-000000000006  # A6 Event 3
  timespan: 5m
  group-by:
    - Computer
    - User
  condition: A4 and A5 and A6
```

### Przykładowy alert (JSON)

```json
{
  "rule": "Account + Privilege Escalation + Run Persistence (5m)",
  "id": "6a11a0e0-0002-4a01-9a01-000000000010",
  "severity": "critical",
  "host": "WIN-57",
  "window": "5m",
  "events": [
    {"EventID": 4720, "SubjectUserName": "labtest2", "TargetUserName": "labtest2"},
    {"EventID": 4732, "GroupName": "Administrators", "MemberName": "labtest2"},
    {"EventID": 4657, "ObjectName": "\\REGISTRY\\USER\\S-1-5-21-...\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "NewValue": "C:\\Users\\labtest2\\agent.py"}
  ],
  "matched": ["A1", "A2", "A3"]
}
```

---

## Sekwencja B — keylogger + eksfiltracja

**Opis ataku:** keylogger instaluje hook klawiatury (`SetWindowsHookEx`), proces keyloggera działa, a przechwycone dane są eksfiltrowane (plik `keylog_*.txt` + połączenie sieciowe).

**Zdarzenia źródłowe:**

| Kanał | EventID | Znaczenie |
|---|---|---|
| Sysmon | 7 | załadowanie obrazu (hook DLL) |
| Sysmon | 1 | proces keyloggera |
| Sysmon | 3 | połączenie sieciowe (9999) |
| Sysmon | 11 | utworzenie pliku `keylog_*.txt` |

### Reguły atomowe (Sysmon)

```yaml
# B1 — załadowanie hook DLL (Event 7)
title: B1 - Keyboard Hook DLL Loaded
id: 6a11a0e0-0001-4a01-9a01-000000000020
status: experimental
logsource:
  product: windows
  category: image_load
  service: sysmon
detection:
  selection:
    EventID: 7
    ImageLoaded|contains:
      - 'keylog'
      - 'hook'
  condition: selection
---
# B2 — proces keyloggera (Event 1)
title: B2 - Keylogger Process
id: 6a11a0e0-0001-4a01-9a01-000000000021
status: experimental
logsource:
  product: windows
  category: process_creation
  service: sysmon
detection:
  selection:
    EventID: 1
    CommandLine|contains:
      - 'keylog'
      - 'keylogger'
  condition: selection
---
# B3 — połączenie na 9999 (Event 3)
title: B3 - C2 Beacon Port 9999
id: 6a11a0e0-0001-4a01-9a01-000000000022
status: experimental
logsource:
  product: windows
  category: network_connection
  service: sysmon
detection:
  selection:
    EventID: 3
    DestinationPort: 9999
  condition: selection
---
# B4 — utworzenie pliku keylog_*.txt (Event 11)
title: B4 - Keylog File Created
id: 6a11a0e0-0001-4a01-9a01-000000000023
status: experimental
logsource:
  product: windows
  category: file_event
  service: sysmon
detection:
  selection:
    EventID: 11
    TargetFilename|contains: 'keylog'
  condition: selection
```

### Reguła korelacyjna (okno 5 min)

```yaml
title: Keylogger Hook + Process + Exfiltration (5m)
id: 6a11a0e0-0002-4a01-9a01-000000000030
status: experimental
correlation:
  type: temporal
  rules:
    - 6a11a0e0-0001-4a01-9a01-000000000020  # B1 Event 7
    - 6a11a0e0-0001-4a01-9a01-000000000021  # B2 Event 1
    - 6a11a0e0-0001-4a01-9a01-000000000023  # B4 Event 11 (plik keylog)
    - 6a11a0e0-0001-4a01-9a01-000000000022  # B3 Event 3 (9999)
  timespan: 5m
  group-by:
    - Computer
    - User
  condition: B2 and B3 and (B1 or B4)
```

### USN Journal (źródło dodatkowe)

USN Journal nie jest standardowym `logsource` Sigma — wymaga dedykowanej ingestii (np. parser `usn` / narzędzie typu Velociraptor). Logika detekcji analogiczna do `B4`:

```
FileName LIKE '%keylog%' AND Reason IN (FILE_CREATE, DATA_EXTEND, CLOSE)
```

### Przykładowy alert (JSON)

```json
{
  "rule": "Keylogger Hook + Process + Exfiltration (5m)",
  "id": "6a11a0e0-0002-4a01-9a01-000000000030",
  "severity": "high",
  "host": "WIN-57",
  "window": "5m",
  "events": [
    {"EventID": 1, "Image": "C:\\Users\\labtest2\\keylogger.exe"},
    {"EventID": 7, "ImageLoaded": "C:\\Users\\labtest2\\keylog_hook.dll"},
    {"EventID": 11, "TargetFilename": "C:\\Users\\labtest2\\AppData\\Local\\Temp\\keylog_57.txt"},
    {"EventID": 3, "DestinationPort": 9999, "DestinationIp": "5.175.189.133"}
  ],
  "matched": ["B2", "B3", "B4"]
}
```

---

## Sekwencja C — screenshot + eksfiltracja

**Opis ataku:** agent (Python) przechwytuje ekran i wysyła obraz do serwera C2 na port 9999.

**Zdarzenia źródłowe:**

| Kanał | EventID | Znaczenie |
|---|---|---|
| Sysmon | 1 | uruchomienie agenta (python) |
| Sysmon | 11 | utworzenie `screenshot_*.png` |
| Sysmon | 3 | połączenie na 9999 |
| Zeek/Suricata (flow) | — | „duży transfer" (liczba bajtów) |

> **Uwaga:** Sysmon Event 3 nie niesie liczby bajtów. „Duży transfer" realizuj przez korelację z `conn.log` (Zeek: `orig_bytes`/`resp_bytes`) lub flow Suricata. Event 5/6 (terminacja procesu / ładowanie sterownika) nie dotyczą GDI.

### Reguły atomowe (Sysmon)

```yaml
# C1 — proces agenta (python)
title: C1 - Python Agent Process
id: 6a11a0e0-0001-4a01-9a01-000000000040
status: experimental
logsource:
  product: windows
  category: process_creation
  service: sysmon
detection:
  selection:
    EventID: 1
    CommandLine|contains: 'python'
  condition: selection
---
# C2 — utworzenie screenshot_*.png
title: C2 - Screenshot File Created
id: 6a11a0e0-0001-4a01-9a01-000000000041
status: experimental
logsource:
  product: windows
  category: file_event
  service: sysmon
detection:
  selection:
    EventID: 11
    TargetFilename|contains: 'screenshot'
  condition: selection
---
# C3 — połączenie na 9999
title: C3 - C2 Beacon Port 9999
id: 6a11a0e0-0001-4a01-9a01-000000000042
status: experimental
logsource:
  product: windows
  category: network_connection
  service: sysmon
detection:
  selection:
    EventID: 3
    DestinationPort: 9999
  condition: selection
```

### Reguła korelacyjna (okno 5 min)

```yaml
title: Screenshot Capture + C2 Exfiltration (5m)
id: 6a11a0e0-0002-4a01-9a01-000000000050
status: experimental
correlation:
  type: temporal
  rules:
    - 6a11a0e0-0001-4a01-9a01-000000000040  # C1 Event 1
    - 6a11a0e0-0001-4a01-9a01-000000000041  # C2 Event 11
    - 6a11a0e0-0001-4a01-9a01-000000000042  # C3 Event 3
  timespan: 5m
  group-by:
    - Computer
    - User
  condition: C1 and C2 and C3
```

### Dodatek — duży transfer (Zeek `conn.log`)

```json
{
  "ts": "2026-08-15T06:58:00Z",
  "id.orig_h": "5.175.189.57",
  "id.resp_h": "5.175.189.133",
  "id.resp_p": 9999,
  "proto": "tcp",
  "resp_bytes": 1048576
}
```

### Przykładowy alert (JSON)

```json
{
  "rule": "Screenshot Capture + C2 Exfiltration (5m)",
  "id": "6a11a0e0-0002-4a01-9a01-000000000050",
  "severity": "high",
  "host": "WIN-57",
  "window": "5m",
  "events": [
    {"EventID": 1, "Image": "python.exe", "CommandLine": "python agent.py"},
    {"EventID": 11, "TargetFilename": "C:\\Users\\labtest2\\AppData\\Local\\Temp\\screenshot_57.png"},
    {"EventID": 3, "DestinationPort": 9999, "DestinationIp": "5.175.189.133"}
  ],
  "matched": ["C1", "C2", "C3"]
}
```

---

## Ograniczenia i uwagi wdrożeniowe

1. **Korelacja temporalna** wymaga backendu wspierającego `correlation` (np. Elastic, Splunk, Sentinel). Dla silników bez natywnej korelacji reguły tłumaczy się na zapytanie sekwencyjne (EQL `sequence ... by host with maxspan=5m` / Splunk `transaction`).
2. **4657** (zmiana rejestru) pojawia się tylko przy skonfigurowanym SACL audytu obiektów — bez tego Sekwencja A-security nie zadziała; uzupełnieniem jest Sysmon 12/13.
3. **Sysmon Event 7** jest bardzo głośny (każde ładowanie DLL) — filtruj po konkretnej nazwie/sygnaturze hook DLL, nie po samym EventID.
4. **Event 3** bez liczby bajtów — „duży transfer" wyłącznie z danych flow (Zeek/Suricata).
5. Pola `group-by` (`Computer`, `SubjectUserName`, `User`) należy dostosować do nazw pól w docelowym SIEM.
