---
title: "Ataki — techniki (MITRE ATT&CK)"
date: 2026-08-15
updated: 2026-08-15
tags: [wiedza, ataki, ttps, mitre]
---

# Techniki ataku — mapa TTP

Wg faz MITRE ATT&CK. Dla każdej: co robi, narzędzia, jak wykryć, jak się bronić.
Szczegóły: [[Malware/Malware_MOC]] (rodziny) · [[Narzedzia]] (narzędzia) · [[Obrona/Obrona_MOC]] (obrona).

## 1. Initial Access (początkowy dostęp)

| Technika (ID) | Jak | Narzędzia | Obrona |
|---------------|-----|-----------|--------|
| Phishing (T1566) | mail / załącznik / link | GoPhish, Evilginx2, SET | SPF/DKIM/DMARC, MFA, EDR, szkolenia |
| Spearphishing attachment/link (T1566.001/.002) | celowany złośliwy załącznik/link | jak wyżej | sandbox, MFA, filtrowanie załączników |
| Drive-by Compromise (T1189) | exploit przeglądarki przez stronę | exploit kits | patching, izolacja przeglądarki |
| Valid Accounts (T1078) | skradzione / słabe hasła | credential stuffing, brute | MFA, silne hasła, PAM |
| Exploit Public-Facing App (T1190) | CVE w aplikacji web/VPN | Metasploit, nuclei | patch (CISA KEV), WAF, segmentacja |
| Supply Chain (T1195) | złośliwe zależności / update | — | SBOM, podpisy, przegląd zależności |
| Trusted Relationship (T1199) | przez partnera / MSP | — | zero-trust, segmentacja partnerów |

## 2. Execution (wykonanie kodu)

| Technika | Jak | Narzędzia | Obrona |
|----------|-----|-----------|--------|
| Command & Scripting Interpreter (T1059) | PowerShell, cmd, bash, python | Empire, PS | PowerShell logging, AMSI, blokowanie |
| User Execution (T1204) | makro, LNK, ISO | — | blokada makr, MOTW, ASR |
| WMI (T1047) | wykonanie przez WMI | — | logi WMI, Sysmon |
| Scheduled Task (T1053) | trwałość/wykonanie | schtasks | logi zadań |

## 3. Persistence (trwałość)

| Technika | Jak | Obrona |
|----------|-----|--------|
| Registry Run Keys (T1547.001) | autostart | Sysmon 12/13/14, autoruns |
| Scheduled Task/Job (T1053) | cykliczne | logi zadań |
| Services (T1543) | nowa usługa | EventID 7045, 4697 |
| DLL Search Order Hijacking (T1574.001) | podstawienie DLL | Sysmon ImageLoad |
| BITS Jobs (T1197) | download | logi BITS |
| Web Shell (T1505.003) | skrypt na serwerze | WAF, monitor plików |

## 4. Privilege Escalation (podniesienie uprawnień)

| Technika | Narzędzia | Obrona |
|----------|-----------|--------|
| Exploitation for PrivEsc (T1068) | kernel/CVE | patching |
| Token/Process Injection (T1134) | Mimikatz | EDR, EventID 8 (CreateRemoteThread) |
| UAC Bypass (T1548.002) | fodhelper/eventvwr | UAC full, monitor |
| Credentials in Files/Registry (T1552) | LaZagne | hardening |
| Sudo/Cron abuse (Linux) | — | logi, sudoers |

## 5. Defense Evasion (omijanie obrony)

| Technika | Narzędzia | Obrona |
|----------|-----------|--------|
| Obfuscation (T1027) | packery, garble (Go), Invoke-Obfuscation | unpacking, AMSI |
| Disable/Modify Tools (T1562) | wyłączanie Defender | tamper protection |
| Masquerading (T1036) | nazwa jak legit | reputation, hash |
| Signed Binary Proxy (T1218) | mshta, rundll32, regsvr32 | ASR, logi |
| AMSI Bypass (T1562.001) | patch AMSI | AMSI v2, monitoring |
| Process Injection (T1055) | Mimikatz, Cobalt | EDR |
| Rootkit / Bootkit | — | secure boot, EDR |

## 6. Credential Access (dostęp do poświadczeń)

| Technika | Narzędzia | Obrona |
|----------|-----------|--------|
| OS Credential Dumping (T1003) | Mimikatz (sekurlsa), secretsdump | Credential Guard, LSA protection |
| Kerberoasting (T1558.003) | Rubeus, Impacket | silne hasła, monitor 4769 |
| AS-REP Roasting (T1558.004) | Rubeus | wyłącz "no preauth" |
| Brute Force / Spray (T1110) | CrackMapExec, Kerbrute | lockout, MFA, monitor 4625 |
| Steal Web Session (T1539) | Evilginx2 | phishing-resistant MFA (FIDO2) |
| Keylogging (T1056) | keyloggery | EDR, behavioral |

## 7. Discovery (rozpoznanie wewnątrz)

| Technika | Obrona |
|----------|--------|
| System/Network/Account Discovery (T1082/T1016/T1087) | monitor, honeypot, segmentacja |
| BloodHound collection | monitor LDAP/SAM-R, honeytokens |

## 8. Lateral Movement (ruch boczny)

| Technika | Narzędzia | Obrona |
|----------|-----------|--------|
| Remote Services SMB/WMI/WinRM (T1021) | CrackMapExec, Impacket | segmentacja, monitor 4624 type 3/10 |
| Pass the Hash (T1550.002) | Mimikatz, Impacket | Credential Guard, LAPS |
| Pass the Ticket (T1550.003) | Rubeus, Mimikatz | monitor, krbtgt rotation |

## 9. Collection (zbieranie)

| Technika | Obrona |
|----------|--------|
| Clipboard/Input Capture (T1115/T1056) | monitor |
| Email Collection (T1114) | monitor, DLP |
| Archive Collected Data (T1560) | monitor kompresji |

## 10. Exfiltration (eksfiltracja)

| Technika | Narzędzia | Obrona |
|----------|-----------|--------|
| Exfil over C2 (T1041) | C2 | monitor outbound, proxy/DLP |
| Exfil to Cloud (T1567) | rclone | CASB, monitor |
| DNS exfil (T1048.003) | — | DNS monitoring |

## 11. Impact (skutek)

| Technika | Obrona |
|----------|--------|
| Ransomware (T1486) | backup offline, EDR, MFA |
| Data Destruction (T1485) | backup |
| Defacement (T1491) | backup, monitoring |
| DoS (T1498/T1499) | ochrona DDoS, rate limit |

## Skrót obrony (unieważnia większość)

1. **MFA wszędzie** (FIDO2 > TOTP).
2. **Patching** (CISA KEV najpierw).
3. **Least privilege + LAPS + segmentacja**.
4. **EDR + Sysmon + centralne logi (SIEM)**.
5. **Backup offline (3-2-1)** — ostatnia deska przy ransomware.

Powiązane: [[Obrona/Obrona_MOC]] · [[Malware/Malware_MOC]] · [[Pentest/Pentest_MOC]] · [[RedTeam/RedTeam_MOC]]
