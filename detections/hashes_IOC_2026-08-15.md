---
title: "IoC — hashe próbek + reguły hash-based"
date: 2026-08-15
type: ioc
tags: [ioc, sha256, yara, sigma, hashes]
status: verified-hash
---

# IoC — hashe próbek i reguły hash-based (2026-08-15)

> **Źródło:** SHA256 policzone z plików na serwerze `.133` (2026-08-15, odczyt).
> **Zakres:** wersje reguł związane z realnymi hashami plików `agent.py`/`server.py` (oraz kopii).
>
> ⚠️ **Ważne:** hashe dotyczą **plików źródłowych Pythona**. Nie trafiają do pola `Hashes` zdarzenia procesu (tam jest hash interpretera `python.exe`) — stosuje się je w **YARA** i **regułach plikowych** (Sysmon Event 15 / FIM / EDR).

## 1. Tabela IOC (SHA256)

| Plik | SHA256 |
|------|--------|
| `/root/rat-c2/agent.py` | `c808ebb19f0de26813e2405444a58bc8ce7c1c84b371b8402e3fef8bade0c548` |
| `/root/rat-c2/server.py` | `417b059455c2e46a685a2fce399e8429f8b59b09a8d63ab05b9423234987d0a6` |
| `/root/server.py` (stary) | `d3521b32ccf32b15dc036abcc1b3832102fa51d4fb79863dcd9de20de350e3f4` |
| `/root/rat-c2/server.py.bak.20260815_054724` | `b4a183b8670e482f995aad8d1e0385900dd0048604b216e2cc8c72d668c89a92` |
| `/root/rat-c2/server.py.save` | `015a0c3d9316dea95593b45f3461b4c0f04f09ae317f0ef7d7e46b20213b797c` |

---

## 2. YARA — reguły hash-based

```yara
import "hash"

rule C2_Agent_py_hash
{
    meta:
        description = "Known C2 agent.py (observed 2026-08-15)"
        sha256 = "c808ebb19f0de26813e2405444a58bc8ce7c1c84b371b8402e3fef8bade0c548"
        author = "SOC"
        date = "2026-08-15"
    condition:
        hash.sha256(0, filesize) == "c808ebb19f0de26813e2405444a58bc8ce7c1c84b371b8402e3fef8bade0c548"
}

rule C2_Server_py_hash
{
    meta:
        description = "Known C2 server.py (observed 2026-08-15)"
        sha256 = "417b059455c2e46a685a2fce399e8429f8b59b09a8d63ab05b9423234987d0a6"
        author = "SOC"
        date = "2026-08-15"
    condition:
        hash.sha256(0, filesize) == "417b059455c2e46a685a2fce399e8429f8b59b09a8d63ab05b9423234987d0a6"
}

rule C2_Server_py_old_hash
{
    meta:
        description = "Known legacy C2 server.py (single-port, observed 2026-08-15)"
        sha256 = "d3521b32ccf32b15dc036abcc1b3832102fa51d4fb79863dcd9de20de350e3f4"
        author = "SOC"
        date = "2026-08-15"
    condition:
        hash.sha256(0, filesize) == "d3521b32ccf32b15dc036abcc1b3832102fa51d4fb79863dcd9de20de350e3f4"
}
```

> Uwaga: `import "hash"` i `hash.sha256(0, filesize)` wymaga YARA ≥ 4.2. Dla starszych wersji użyj zewnętrznego narzędzia (np. `pefile`/`hashdeep`) i porównaj hash w metadanych.

---

## 3. Sigma — reguły plikowe (hash)

> Hash pliku pojawia się w Sysmon **Event 15** (`FileCreateStreamHash`, pole `Hashes`) lub w EDR/FIM. Event 11 (`FileCreate`) hasha **nie zawiera**.

```yaml
title: Known C2 File Detected by Hash (agent.py)
id: 7b22c0f0-0001-4b01-9b01-000000000001
status: stable
description: Wykrywa znany plik agenta C2 (agent.py) po SHA256.
author: SOC
date: 2026/08/15
logsource:
  product: windows
  category: file_event
  service: sysmon
detection:
  selection:
    EventID: 15
    Hashes|contains: 'SHA256=c808ebb19f0de26813e2405444a58bc8ce7c1c84b371b8402e3fef8bade0c548'
  condition: selection
falsepositives:
  - none (hash match is high-confidence)
level: critical
---
title: Known C2 File Detected by Hash (server.py)
id: 7b22c0f0-0001-4b01-9b01-000000000002
status: stable
description: Wykrywa znany plik serwera C2 (server.py) po SHA256.
author: SOC
date: 2026/08/15
logsource:
  product: windows
  category: file_event
  service: sysmon
detection:
  selection:
    EventID: 15
    Hashes|contains: 'SHA256=417b059455c2e46a685a2fce399e8429f8b59b09a8d63ab05b9423234987d0a6'
  condition: selection
falsepositives:
  - none
level: critical
```

> Wariant Linux: dla agenta/serwera działającego na Linuksie (jak tu) hash pliku lepiej egzekwować przez **Auditd** (`-w /root/rat-c2 -p wa -k c2`) lub FIM (np. `auditbeat`/`osquery`), bo Sysmon nie istnieje na Linuksie.

---

## 4. Lista IOC (format plain / CSV)

```csv
type,indicator,description
sha256,c808ebb19f0de26813e2405444a58bc8ce7c1c84b371b8402e3fef8bade0c548,C2 agent.py
sha256,417b059455c2e46a685a2fce399e8429f8b59b09a8d63ab05b9423234987d0a6,C2 server.py (nowy TCP)
sha256,d3521b32ccf32b15dc036abcc1b3832102fa51d4fb79863dcd9de20de350e3f4,C2 server.py (stary)
sha256,b4a183b8670e482f995aad8d1e0385900dd0048604b216e2cc8c72d668c89a92,server.py backup
sha256,015a0c3d9316dea95593b45f3461b4c0f04f09ae317f0ef7d7e46b20213b797c,server.py save
```

---

## 5. Uwagi wdrożeniowe

1. **Hash ≠ proces**: `agent.py`/`server.py` są uruchamiane przez `python3`, więc zdarzenie procesu (Sysmon 1 / 4688) niesie hash `python3`, nie skryptu. Hash pliku wykrywaj w warstwie plikowej (YARA na dysku, Sysmon 15, FIM, `auditbeat`).
2. **Kopie zapasowe** (`server.py.bak*`, `server.py.save`) też mają unikalne hashe — uwzględnij je, by wykryć przywracanie starszych wersji.
3. **YARA `hash` module** wymaga YARA ≥ 4.2; alternatywnie porównuj hash w metadanych przez zewnętrzny skaner.
4. Hash jest **kruchy** — każda zmiana w pliku zmienia hash. Reguły string-based (`[[C2_detection_rules_sigma_yara_suricata]]`) pozostają uzupełnieniem dla wariantów.

---
*Powiązane:* [[C2_detection_rules_2026-08-15]], [[C2_detection_rules_sigma_yara_suricata]], [[README]]
