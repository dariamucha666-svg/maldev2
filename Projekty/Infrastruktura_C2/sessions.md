---
title: "Sliver sessions"
date: 2026-08-21
updated: 2026-08-21T12:12:01Z
tags: [sliver, c2, sessions, auto]
status: active
category: infra
---

# Sliver — sesje i beacon'y

Wygenerowane: `2026-08-21T12:12:01Z` (auto, nie ręcznie z konsoli).

Sliver **nie ma** `sessions --save`. Eksport: `Narzedzia/export_sliver_to_obsidian.sh`.

## Konsola (`sessions` / `beacons` / `jobs`)

```
Connecting to 127.0.0.1:31337 ...
[*] No sessions 🙁
 ID         Name                      Tasks   Transport   Remote Address                        Hostname   Username        Process (PID)                                              Integrity   Operating System   Locale   Last Check-In                                   Next Check-In                                 
========== ========================= ======= =========== ===================================== ========== =============== ========================================================== =========== ================== ======== =============================================== ===============================================
 fc609c70   MATHEMATICAL_MAYONNAISE   0/0     http(s)     tcp(127.0.0.1:47848)->5.175.189.139   WINLAB     Administrator   C:\Windows\system32\UsersPublicbeacon_windows.exe (2196)   -           windows/amd64      en-US    Wed Aug 12 21:17:36 UTC 2026 (206h54m25s ago)   Wed Aug 12 21:18:46 UTC 2026 (206h53m15s ago) 
 ID   Name    Protocol   Port   Domains 
==== ======= ========== ====== =========
 1    https   tcp        443            
```

## Beacon'y (SQLite, bez sekretów)

| name | hostname | os | arch | transport | last_checkin |
|------|----------|----|------|-----------|--------------|
| MATHEMATICAL_MAYONNAISE | WINLAB | windows | amd64 | http(s) | 2026-08-12 21:17:36.063767692+00:00 |

## Hosty (SQLite)

| hostname | os_version | locale | created_at |
|----------|------------|--------|------------|
| vserver959630 | linux | C | 2026-08-21 05:07:50.127919579+00:00 |
| WINLAB | windows | en-US | 2026-08-12 15:53:40.478915255+00:00 |
| 3f1516ef2861 | linux | C | 2026-08-11 07:24:33.903160506+00:00 |
| vserver580088 | linux | C | 2026-08-11 05:33:54.623044137+00:00 |

## Listener jobs

| job_id | type | created_at |
|--------|------|------------|
| 3 | stage-listener | 2026-08-12 17:35:14.524171074+00:00 |
| 1 | https | 2026-08-11 07:14:35.384586587+00:00 |

Nie eksportujemy: `credentials`, kluczy implantu, `audit.json`.
