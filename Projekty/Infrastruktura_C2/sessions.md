---
title: "Sliver sessions"
date: 2026-08-15
updated: 2026-08-15T09:12:01Z
tags: [sliver, c2, sessions, auto]
status: active
category: infra
---

# Sliver — sesje i beacon'y

Wygenerowane: `2026-08-15T09:12:01Z` (auto, nie ręcznie z konsoli).

Sliver **nie ma** `sessions --save`. Eksport: `Narzedzia/export_sliver_to_obsidian.sh`.

## Konsola (`sessions` / `beacons` / `jobs`)

```
Connecting to 127.0.0.1:31337 ...
 ID         Name                   Transport   Remote Address                        Hostname        Username        Process (PID)                                  Integrity   Operating System   Locale   Last Message                                   Health 
========== ====================== =========== ===================================== =============== =============== ============================================== =========== ================== ======== ============================================== ========
 3cb3f905   SEPARATE_CONCLUSION    http(s)     tcp(127.0.0.1:59476)->5.175.189.139   WINLAB          Administrator   C:\Windows\Explorer.EXE (4032)                 -           windows/amd64      en-US    Thu Aug 13 01:19:37 UTC 2026 (55h52m25s ago)   [DEAD] 
 3ffaa554   SIMPLE_BIRTHDAY        http(s)     tcp(127.0.0.1:41738)->5.175.189.139   vserver580088   root            /root/payload_linux (42170)                    -           linux/amd64        C        Wed Aug 12 15:57:10 UTC 2026 (65h14m52s ago)   [DEAD] 
 4396e80d   SEPARATE_CONCLUSION    http(s)     tcp(127.0.0.1:55750)->5.175.189.139   WINLAB          Administrator   C:\Users\Public\p.exe (1212)                   -           windows/amd64      en-US    Wed Aug 12 21:18:33 UTC 2026 (59h53m29s ago)   [DEAD] 
 514150c7   SMOOTH_TARGET          http(s)     tcp(127.0.0.1:41738)->5.175.189.139   vserver580088   root            /root/payload_linux_debug (42713)              -           linux/amd64        C        Wed Aug 12 15:57:09 UTC 2026 (65h14m53s ago)   [DEAD] 
 56374b2a   SEPARATE_CONCLUSION    http(s)     tcp(127.0.0.1:46188)->5.175.189.139   WINLAB          Administrator   C:\Windows\Explorer.EXE (4032)                 -           windows/amd64      en-US    Thu Aug 13 01:19:37 UTC 2026 (55h52m25s ago)   [DEAD] 
 5fd8984b   FIT_MINOR-LEAGUE       http(s)     tcp(127.0.0.1:54718)->5.175.189.139   WINLAB          Administrator   C:\Users\Public\p.exe (1212)                   -           windows/amd64      en-US    Wed Aug 12 15:57:09 UTC 2026 (65h14m53s ago)   [DEAD] 
 752cfecc   SMOOTH_TARGET          http(s)     tcp(127.0.0.1:41738)->5.175.189.139   vserver580088   root            /root/payload_linux_debug (42375)              -           linux/amd64        C        Wed Aug 12 15:57:08 UTC 2026 (65h14m54s ago)   [DEAD] 
 7d9121b9   SIMPLE_BIRTHDAY        http(s)     tcp(127.0.0.1:36376)->5.175.189.139   vserver580088   root            /root/payload_linux (42170)                    -           linux/amd64        C        Thu Aug 13 01:19:38 UTC 2026 (55h52m24s ago)   [DEAD] 
 ac7aee00   SMOOTH_TARGET          http(s)     tcp(127.0.0.1:36376)->5.175.189.139   vserver580088   root            /root/payload_linux_debug (42713)              -           linux/amd64        C        Thu Aug 13 01:13:54 UTC 2026 (55h58m8s ago)    [DEAD] 
 be61ae84   SMOOTH_TARGET          http(s)     tcp(127.0.0.1:36382)->5.175.189.139   vserver580088   root            /root/payload_linux_debug (42375)              -           linux/amd64        C        Thu Aug 13 01:13:17 UTC 2026 (55h58m45s ago)   [DEAD] 
 c0e249f8   MARVELLOUS_AUTOMATON   http(s)     tcp(127.0.0.1:42698)->5.175.189.139   WINLAB          Administrator   C:\Windows\System32\RuntimeBroker.exe (4292)   -           windows/amd64      en-US    Thu Aug 13 01:19:37 UTC 2026 (55h52m25s ago)   [DEAD] 
 e0606627   WILD_HABIT             http(s)     tcp(127.0.0.1:40942)->5.175.189.139   WINLAB          Administrator   C:\Users\Public\fb1.exe (5608)                 -           windows/amd64      en-US    Wed Aug 12 21:18:32 UTC 2026 (59h53m30s ago)   [DEAD] 
 f650c1ad   SEPARATE_CONCLUSION    http(s)     tcp(127.0.0.1:56130)->5.175.189.139   WINLAB          Administrator   C:\Windows\Explorer.EXE (4032)                 -           windows/amd64      en-US    Thu Aug 13 01:19:37 UTC 2026 (55h52m25s ago)   [DEAD] 
 fe76ef79   FIT_MINOR-LEAGUE       http(s)     tcp(127.0.0.1:36434)->5.175.189.139   WINLAB          Administrator   C:\Users\Public\p.exe (1212)                   -           windows/amd64      en-US    Wed Aug 12 21:18:33 UTC 2026 (59h53m29s ago)   [DEAD] 
 ID         Name                      Tasks   Transport   Remote Address                        Hostname   Username        Process (PID)                                              Integrity   Operating System   Locale   Last Check-In                                  Next Check-In                                
========== ========================= ======= =========== ===================================== ========== =============== ========================================================== =========== ================== ======== ============================================== ==============================================
 fc609c70   MATHEMATICAL_MAYONNAISE   0/0     http(s)     tcp(127.0.0.1:47848)->5.175.189.139   WINLAB     Administrator   C:\Windows\system32\UsersPublicbeacon_windows.exe (2196)   -           windows/amd64      en-US    Wed Aug 12 21:17:36 UTC 2026 (59h54m26s ago)   Wed Aug 12 21:18:46 UTC 2026 (59h53m16s ago) 
 ID   Name    Protocol   Port   Domains 
==== ======= ========== ====== =========
 1    https   tcp        443            
 3    TCP     tcp        8443           
```

## Beacon'y (SQLite, bez sekretów)

| name | hostname | os | arch | transport | last_checkin |
|------|----------|----|------|-----------|--------------|
| MATHEMATICAL_MAYONNAISE | WINLAB | windows | amd64 | http(s) | 2026-08-12 21:17:36.063767692+00:00 |

## Hosty (SQLite)

| hostname | os_version | locale | created_at |
|----------|------------|--------|------------|
| WINLAB | windows | en-US | 2026-08-12 15:53:40.478915255+00:00 |
| 3f1516ef2861 | linux | C | 2026-08-11 07:24:33.903160506+00:00 |
| vserver580088 | linux | C | 2026-08-11 05:33:54.623044137+00:00 |

## Listener jobs

| job_id | type | created_at |
|--------|------|------------|
| 3 | stage-listener | 2026-08-12 17:35:14.524171074+00:00 |
| 1 | https | 2026-08-11 07:14:35.384586587+00:00 |

Nie eksportujemy: `credentials`, kluczy implantu, `audit.json`.
