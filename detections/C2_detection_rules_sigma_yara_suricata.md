# Reguły detekcyjne C2 — Sigma / YARA / Suricata

> **Data:** 2026-08-15
> **Status:** experimental (dostroić do faktycznych próbek/hashów)
> **Kontekst obserwacji:**
> - Serwer C2: `python3 -u server.py`, nasłuchy `0.0.0.0:9999` (agenci) i `0.0.0.0:9998` (CLI).
> - Agent: `agent.py`, połączenie do serwera na port **9999** (zaobserwowano `5.175.189.57`).
> - Charakterystyczne komendy: `screenshot`, `net_user_add`, `keylog_start`.

---

## 1. Sigma (Windows)

### 1.1 Uruchomienie agenta — EventID 4688

```yaml
title: Execution of C2 Agent (agent.py)
id: 8f3a1c2e-5b7d-4a9e-9c0b-2f6d1e8a4b01
status: experimental
description: Wykrywa uruchomienie skryptu agenta C2 (agent.py) przez interpreter Python.
author: SOC
date: 2026/08/15
logsource:
  product: windows
  category: process_creation
  service: security
detection:
  selection_event:
    EventID: 4688
  selection_cmdline:
    CommandLine|contains:
      - 'agent.py'
      - '-u agent.py'
  selection_interp:
    NewProcessName|endswith:
      - '\python.exe'
      - '\python3.exe'
      - '\pythonw.exe'
  condition: selection_event and (selection_cmdline or selection_interp)
falsepositives:
  - Skrypty Python o nazwie agent.py używane w celach nie-malware
level: high
tags:
  - attack.execution
  - attack.t1059.006
```

### 1.2 Połączenie sieciowe na port 9999 — EventID 5156

```yaml
title: C2 Network Connection to Port 9999 (WFP)
id: 2c9e7b4a-1d6f-4b3a-8e5c-0a9d2f7c8b02
status: experimental
description: Wykrywa zaakceptowane połączenie wychodzące na port 9999 (beacon C2).
author: SOC
date: 2026/08/15
logsource:
  product: windows
  category: network_connection
  service: security
detection:
  selection:
    EventID: 5156
    DestinationPort: 9999
  filter_loopback:
    DestinationAddress|startswith: '127.'
  condition: selection and not filter_loopback
falsepositives:
  - Własne aplikacje używające portu 9999
level: high
tags:
  - attack.command_and_control
  - attack.t1571
```

---

## 2. YARA

### 2.1 `C2_Agent_py`

```yara
rule C2_Agent_py
{
    meta:
        description = "Detects C2 agent.py source (heuristic)"
        author = "SOC"
        date = "2026-08-15"
        reference = "internal"

    strings:
        $s_screenshot = "screenshot"   ascii wide
        $s_useradd    = "net_user_add" ascii wide
        $s_keylog     = "keylog_start" ascii wide
        $s_socket     = "socket"       ascii wide
        $s_connect    = "connect(("    ascii
        $s_sendall    = "sendall"      ascii wide
        $s_recv       = "recv("        ascii wide

    condition:
        filesize < 200KB and
        (uint32(0) != 0x4D5A9000) and
        ( $s_screenshot or $s_keylog or $s_useradd ) and
        ( $s_socket and $s_connect and (1 of ($s_sendall, $s_recv)) )
}
```

### 2.2 `C2_Server_py`

```yara
rule C2_Server_py
{
    meta:
        description = "Detects C2 server.py source (heuristic)"
        author = "SOC"
        date = "2026-08-15"
        reference = "internal"

    strings:
        $s_screenshot = "screenshot"   ascii wide
        $s_useradd    = "net_user_add" ascii wide
        $s_keylog     = "keylog_start" ascii wide
        $s_bind       = "bind(("       ascii
        $s_listen     = "listen("      ascii wide
        $s_accept     = "accept("      ascii wide
        $s_port9      = "9999"         ascii
        $s_port8      = "9998"         ascii

    condition:
        filesize < 200KB and
        (uint32(0) != 0x4D5A9000) and
        $s_bind and $s_listen and $s_accept and
        (1 of ($s_port9, $s_port8)) and
        (1 of ($s_screenshot, $s_useradd, $s_keylog))
}
```

---

## 3. Suricata

> Kierunek: agent (`$HOME_NET`) → serwer C2 (`$EXTERNAL_NET`) na porcie **9999**. Komendy płyną w stronę `to_client`, dane (eksfiltracja) w stronę `to_server`.

```suricata
# 3.1 Nawiązanie sesji C2 na porcie 9999
alert tcp $HOME_NET any -> $EXTERNAL_NET 9999 (msg:"C2 beacon - connection to port 9999"; flow:to_server,established; flowbits:set,rat_c2_9999; classtype:trojan-activity; sid:2026081501; rev:1;)

# 3.2 Kontynuacja sesji (wskaźnik long-lived) - limit 1 alert / 60 s na źródło
alert tcp $HOME_NET any -> $EXTERNAL_NET 9999 (msg:"C2 session ongoing (possible long-lived beacon)"; flow:to_server,established; flowbits:isset,rat_c2_9999; flowbits:set,rat_c2_9999_persist; threshold:type limit, track by_src, count 1, seconds 60; classtype:trojan-activity; sid:2026081502; rev:1;)

# 3.3 JSON payload z polem komendy (serwer -> agent)
alert tcp $EXTERNAL_NET 9999 -> $HOME_NET any (msg:"C2 JSON command payload"; flow:to_client,established; content:"\"cmd\""; nocase; content:"\"screenshot\""; nocase; distance:0; within:128; classtype:trojan-activity; sid:2026081503; rev:1;)

# 3.4 Komendy administracyjne w JSON
alert tcp $EXTERNAL_NET 9999 -> $HOME_NET any (msg:"C2 command - net_user_add"; flow:to_client,established; content:"net_user_add"; nocase; classtype:trojan-activity; sid:2026081504; rev:1;)
alert tcp $EXTERNAL_NET 9999 -> $HOME_NET any (msg:"C2 command - keylog_start"; flow:to_client,established; content:"keylog_start"; nocase; classtype:trojan-activity; sid:2026081505; rev:1;)

# 3.5 Eksfiltracja danych (agent -> serwer)
alert tcp $HOME_NET any -> $EXTERNAL_NET 9999 (msg:"C2 data exfiltration on port 9999"; flow:to_server,established; content:"data:image"; nocase; classtype:trojan-activity; sid:2026081506; rev:1;)
```

**Uwaga o long-lived:** Suricata nie ma natywnego warunku czasu trwania sesji w sygnaturze. Powyżej użyto `flowbits` + `threshold` (limit 1 alert / 60 s) jako przybliżenie. Dokładną detekcję long-lived rekomenduje się realizować korelacją po `flow.age`/`flow.start`/`flow.end` w `eve.json` lub w SIEM.

---

## 4. Uwagi wdrożeniowe

- Reguły są heurystyczne (nazwy plików, porty, stringi) — do produkcji dodać SHA256 próbek.
- Dla 4688/5156 wymagana jest włączona zaawansowana polityka audytu Windows.
- Dla próbek skompilowanych (PyInstaller/PE) dodać do YARA ciągi prologu i warianty `ascii wide`.
- Potwierdzić dokładny format payloadu JSON i dostroić pola `content`.
