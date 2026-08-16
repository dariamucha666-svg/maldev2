---
title: "Dynamiczna analiza własnego RAT-a na .57"
date: 2026-08-16
type: raport
tags: [lab, rat, c2, dynamic-analysis, windows, sysmon, dfir]
status: completed
---

# Dynamiczna analiza własnego RAT-a na .57

> **Charakter:** uruchomienie własnego RAT-a (reverse shell) na laboratorium Windows .57, obserwacja zachowania (sieć, rejestr, procesy, pliki, Sysmon) i sprzątnięcie artefaktów. Środowisko izolowane (VPS lab), bez szkody dla stron trzecich.

## Środowisko

| Rola | Host | System | Nota |
|------|------|--------|------|
| C2 | 5.175.189.133 (vserver959630) | Ubuntu 24.04 | serwer C2 na porcie 9999 |
| Ofiara/agent | 5.175.189.57 (WIN-T5BVVHUNVJI) | Windows Server 2022 Eval | agent uruchomiony jako SYSTEM |

## Co analizowano

Własny agent z projektu [[Wlasny_RAT]]:

- Kod: **C:/Users/Administrator/Desktop/agent.py** na .57 (C2_HOST=5.175.189.133, C2_PORT=9999).
- Protokół: surowy reverse shell — agent łączy się do C2, czeka na komendy, wykonuje je przez subprocess(shell=True) i odsyła stdout/stderr. Obsługuje **cd**, **quit**, resztę traktuje jako komendę powłoki.
- Funkcje z karty projektu (whoami / sysinfo / screenshot / keylog / shell / persistence) są realizowane jako **komendy wykonywane przez shell** (whoami, systeminfo, skrypt PowerShell itd.), a nie wbudowane moduły.

## Ważne ustalenie: agent.exe jest nieaktualny

**C:/Users/Administrator/Desktop/dist/agent.exe** (8 273 172 B, zbudowany 15.08 03:21) **nie działa** — kończy się natychmiast (exit 0, brak wyjścia), bo źródło **agent.py** było modyfikowane później (15.08 04:04). Demonstrację przeprowadzono na źródle przez **C:/Program Files/Python312/python.exe agent.py**. Wniosek: przed użyciem przebudować PyInstallerem (**agent.spec**).

## Przebieg

1. C2 na .133: python3 /root/rat-c2/raw_c2.py (bind 0.0.0.0:9999).
2. Agent na .57 uruchomiony jako zadanie planowane (SYSTEM) — bo proces startowany przez WinRM/Start-Process ginie przy zamknięciu sesji WinRM.
3. Komendy wysyłane z C2 → agent wykonuje → odpowiedź wraca.

## Wyniki komend (skrót)

| Komenda | Wynik |
|---------|-------|
| whoami | nt authority\system (agent działa jako SYSTEM) |
| hostname | WIN-T5BVVHUNVJI |
| ipconfig | 5.175.189.57, brama 5.175.189.1 |
| ver | Windows 10.0.20348.587 |
| systeminfo | Win Server 2022 Standard Evaluation, 6140 MB RAM, QEMU/Q35, AMD64 |
| dir C:/Users/Administrator/Desktop | pełny listing (25 plików) |
| net user | Administrator, cloudbase-init, DefaultAccount, Guest, WDAGUtilityAccount |
| reg add HKLM/.../Run /v Agent | persistence ustawiona (REG_SZ → agent.exe) |
| net user ratdemo DemoPass2026 /add | konto utworzone |
| screenshot (PowerShell) | plik PNG 3179 B, ale CopyFromScreen → "The handle is invalid" (sesja 0 bez pulpitu) |
| keylogger (PowerShell, GetAsyncKeyState) | keylog_57.txt 89 B (nagłówki; brak klawiszy — sesja 0) |

## Artefakty dynamiczne (do detekcji/IR)

- **Sieć:** 5.175.189.57:50206 -> 5.175.189.133:9999 ESTABLISHED (netstat, pid 6668 python.exe).
- **Sysmon EventID 3 (NetworkConnect)** — 4 zdarzenia wyjściowe do 5.175.189.133:9999: proces python.exe/powershell.exe, SourceIp 5.175.189.57, DestinationPort 9999, Initiated=true. To jest sygnał do wykrycia C2 callback.
- **Persistence:** wartość **Agent** w HKLM/Software/Microsoft/Windows/CurrentVersion/Run.
- **Konto:** Security EventID 4720 (utworzenie ratdemo).
- **Pliki:** keylog_57.txt, screenshot_57.png, wdrożone skrypty .ps1 (Sysmon EventID 11 łapie .ps1 per konfig).

## Ograniczenia (istotne dla interpretacji)

- Agent jako SYSTEM w **sesji 0** (zadanie planowane, ServiceAccount) → brak interaktywnego pulpitu, więc screenshot jest czarny/pusty, a keylogger nie łapie klawiszy. Żeby pokazać realny keylog/screenshot, agent musi działać w sesji użytkownika (np. RDP session 1).
- systeminfo / net user pokazują, że host to **QEMU/KVM (Q35)** — to zagnieżdżona maszyna, nie fizyczny serwer.

## Sprzątnięcie (zrobione)

- net user ratdemo /delete → "The command completed successfully." (weryfikacja: "user name could not be found").
- Usunięcie wartości **Agent** z Run (Remove-ItemProperty) → potwierdzone brak.
- Zatrzymanie agenta (Stop-Process) + usunięcie zadania planowanego RATDemo.
- Usunięcie wdrożonych skryptów (.ps1) i agent_out/err.txt.
- Zatrzymanie serwera C2 (port 9999 zwolniony).

## Domknięcie (2026-08-16, drugie przejście)

Po przebudowaniu agenta i odpaleniu w sesji interaktywnej domknięto screenshot + keylog (wcześniej sesja 0 bez pulpitu).

### 1. Przebudowa agent.exe
- PyInstaller: pyinstaller --onefile --clean --name agent agent.py (Python 3.12).
- Nowy: 8 441 645 B, SHA256 6a97d2a006be99ba4ca9d899fd5c274e23081f926a50cb4d893302c913013f60 (stary: 8 273 172 B).
- Backup starego: dist/agent.exe.old.20260816.

### 2. Agent w sesji interaktywnej (session 2)
- Uruchomiony jako zadanie planowane z principal Administrator + LogonType Interactive → proces w session 2 (nie session 0).
- whoami = win-t5bvvhunvji\administrator (nie SYSTEM).
- Sesja 2 była Disconnected (RDP) → CopyFromScreen nadal "handle is invalid". Fix: tscon 2 /dest:console → sesja Active.

### 3. Screenshot — działa
- Po aktywacji sesji: screenshot_57.png = 49 257 B, PNG 1280x800 RGBA (prawdziwy pulpit, nie czarny).

### 4. Keylogger — działa
- Keylogger GetAsyncKeyState z detekcją "pressed since last call" (bit 0) + mapa znaków.
- Wstrzyknięcie klawiszy przez SendKeys (WScript.Shell) w sesji 2.
- keylog_57.txt przechwycił sekwencję "sekretHaslo2026" (S,E,K,R,T,H,A,L,O,0,2,6 + SHIFT) + ENTER. 953 B.
- Uwaga: keylogger pollingowy łapie klawisz raz na interwał (nie rozróżnia powtórzeń w 60 ms); pełną sekwencję da hook WH_KEYBOARD_LL.

### 5. Sprzątnięcie
- Agent zatrzymany, zadania RATInteractive + SendKeysDemo usunięte, skrypty .ps1 usunięte, C2 zatrzymany. Artefakty (screenshot_57.png, keylog_57.txt) zostawione jako dowód.

## Linki

- [[Wlasny_RAT]] · [[Analiza_artefaktów_agenta_57]] · [[Laboratorium_Windows]] · [[Infrastruktura_C2]] · [[Lab/Hosts]]
