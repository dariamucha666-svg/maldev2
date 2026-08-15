---
title: "Narzędzia — ofensywne i defensywne"
date: 2026-08-15
tags: [wiedza, narzedzia, tools]
---

# Katalog narzędzi

> Katalog główny `Narzedzia/` to **skrypty TEGO labu** (pipeline, bot, logowanie).
> Ta notatka to katalog narzędzi *ofensywnych i defensywnych* do nauki/testów.

## Ofensywne

### Recon / OSINT
| Narzędzie | Do czego |
|-----------|----------|
| amass | pasywne/aktywne mapowanie domen i subdomen |
| subfinder | szybkie zbieranie subdomen |
| theHarvester | emaile, subdomeny, IP z OSINT |
| Shodan / Censys | exposure powierzchni (internet) |
| Nmap | skan portów i usług |
| RustScan | bardzo szybki skan portów |
| masscan | skan całych sieci |

### Web
| Narzędzie | Do czego |
|-----------|----------|
| Burp Suite (Community/Pro) | proxy, fuzzing, testy web |
| OWASP ZAP | darmowa alternatywa Burpa |
| ffuf / gobuster / dirsearch | brute-force ścieżek i wirtualnych hostów |
| sqlmap | SQL injection |
| nuclei | template'owe skany (CVE/misconfig) |
| nikto | skan serwera web |
| wpscan | WordPress |

### Exploit / AD / Windows
| Narzędzie | Do czego |
|-----------|----------|
| Metasploit | framework exploitów |
| CrackMapExec / NetExec | AD: lateral movement, credential spray |
| Impacket | protokoły Windows (secretsdump, psexec, wmiexec, ntlmrelayx) |
| BloodHound + SharpHound | mapowanie relacji AD (attack paths) |
| Mimikatz | dump poświadczeń, pass-the-hash/ticket |
| Responder | LLMNR/NBT-NS/mDNS poisoning |
| Kerbrute | Kerberos brute/spray |
| Rubeus | Kerberos (AS-REP, ticket) |
| evil-winrm | WinRM shell |
| ligolo-ng / chisel | tunelowanie / pivoting |

### C2 / post-exploit
| Narzędzie | Do czego |
|-----------|----------|
| Sliver | C2 (używany w labie — [[Narzedzia/Sliver_C2]]) |
| Cobalt Strike | komercyjny C2 (red team) |
| Havoc / Mythic / Brute Ratel | alternatywy C2 |
| PowerShell Empire | post-exploit |

### Phishing
| Narzędzie | Do czego |
|-----------|----------|
| GoPhish | kampanie phishingowe |
| Evilginx2 | reverse proxy (AiTM, MFA bypass) |
| Modlishka | reverse proxy 2FA |
| SET | social engineering toolkit |

## Defensywne / analiza

### Analiza malware / RE
| Narzędzie | Do czego |
|-----------|----------|
| Ghidra | dekompilator (lab: na `.57`) |
| IDA Pro / Freeware | dekompilator |
| radare2 / rizin | RE framework |
| x64dbg / x32dbg | debugger Windows |
| dnSpy / ILSpy | .NET dekompilacja |
| jadx | APK → Java (lab) |
| apktool | APK unpack/repack (lab) |
| capa (Mandiant) | mapowanie capabilities (lab) |
| FLOSS | deobfuskacja stringów |
| PE-bear / Detect It Easy | headers / packery |
| YARA | reguły detekcji plików (lab) |

### Detekcja / monitoring
| Narzędzie | Do czego |
|-----------|----------|
| Suricata / Snort / Zeek | IDS/NSM (lab: Suricata `.139`) |
| Wazuh / Security Onion | SIEM/EDR open source |
| Velociraptor | DFIR/EDR open source |
| Sysmon + Sigma | detekcja na Windows |
| Sigma | uniwersalne reguły detekcji |
| osquery | endpoint visibility |

### DFIR / forensics
| Narzędzie | Do czego |
|-----------|----------|
| Volatility 3 | analiza RAM |
| Autopsy / Sleuth Kit | analiza dysków |
| KAPE (Eric Zimmerman) | triage + zbieranie artefaktów |
| Eric Zimmerman Tools | Registry/amcache/lnk/prefetch |
| Wireshark / tshark | PCAP |

## Zasada

Najpierw **detekcja/obrona** dla danej techniki, dopiero potem narzędzie ofensywne.
Mapowanie narzędzie → technika w [[Ataki/Ataki_MOC]].
