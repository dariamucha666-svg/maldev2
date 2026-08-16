---
title: "Optymalizacja RAT-a — JSON + wbudowane komendy + hook keylogger"
date: 2026-08-16
type: raport
tags: [lab, rat, c2, optimization, keylogger, wh-keyboard-ll]
status: completed
---

# Optymalizacja RAT-a (agent + C2)

Optymalizacja własnego RAT-a z [[Wlasny_RAT]] po dynamicznej analizie [[2026-08-16_dynamiczna_analiza_RAT_57]]. Cel: naprawić znane ograniczenia i zamknąć wbudowane funkcje.

## Co się zmieniło

| Przed | Po |
|-------|-----|
| surowy reverse shell (brak framing) | **JSON newline-delimited** (register/command/result) |
| funkcje przez shell (whoami/systeminfo jako komendy cmd) | **wbudowane komendy** w agencie |
| keylogger pollingowy GetAsyncKeyState (gubił powtórzenia) | **hook WH_KEYBOARD_LL** (łapie każdy klawisz) |
| screenshot tylko przez zewnętrzny .ps1 | **wbudowany** (mss → fallback PowerShell) |
| persistence przez reg.exe w shell | **winreg** (HKCU/HKLM Run key) |
| print bez flush, pojedynczy connect | **flush + reconnect** co 5 s |

## Nowe pliki

- **Agent:** /root/rat-c2/agent_win.py (wdrożony na .57 jako C:/Users/Administrator/Desktop/agent.py)
- **C2:** /root/rat-c2/c2_server.py (port 9999, komendy przez FIFO /tmp/c2in.fifo, zapis binariów do /root/rat-c2/out/)
- Helper transferu dużych plików: /root/deploy57_chunked.py (chunked base64 — stary deploy57.py padał na plikach >4KB przez limit linii WinRM)

## Wbudowane komendy (dispatch "command")

whoami · sysinfo · shell (args.cmd) · screenshot · keylog_start · keylog_stop · persistence (args.path/value/hive) · cd (args.path) · quit

## Test end-to-end (na .57, sesja 2, Administrator)

| Komenda | Wynik |
|---------|-------|
| whoami | user=Administrator hostname=WIN-T5BVVHUNVJI |
| sysinfo | Windows Server 2022 Eval, AMD64, QEMU/Q35, Python 3.12.10 |
| shell (ipconfig) | 5.175.189.57, brama 5.175.189.1 |
| screenshot | PNG 1280x800, 41 553 B (zapisane do /root/rat-c2/out/4_artifact.png) |
| keylog_start + SendKeys + keylog_stop | **40 klawiszy**, pełna sekwencja: SEKRET + SHIFT + HASLO2026 + ENTER + UZYTKOWNIK + SHIFT + ; + ADMIN |
| persistence (HKCU) | Run\Agent = C:/Users/Administrator/Desktop/dist/agent.exe (zweryfikowane reg query) |

## Bugi naprawione w trakcie

1. **WH_KEYBOARD_LL nie startował** — brak restype/argtypes ctypes (64-bit) → hook dostawał złe handle. Fix: jawne sygnatury + hMod=0.
2. **Hook łapał 0 klawiszy** — hook instalowany na wątku głównym, a pętla komunikatów na innym wątku. Fix: instalacja hooka + pętla komunikatów na tym samym wątku.
3. **SendKeys task failował** — sendkeys_57.ps1 był skasowany w cleanup. Fix: redeploy.

## Nowy agent.exe

- Przebudowany PyInstallerem z optymalizowanego źródła.
- Rozmiar: 8 473 799 B, SHA256 e7cb9e260a0fb7c709c02a5663a1b0c3c13e25bfa4bdca153b1853bac5c0efa6.

## Sprzątnięcie

- Persistence (Run "Agent") usunięta, agent + zadania (RATOpt, SendKeysDemo) zatrzymane, sendkeys_57.ps1 usunięty, C2 zatrzymany. Kod agenta + exe zostawione na .57 jako deliverable.

## Linki

- [[Wlasny_RAT]] · [[2026-08-16_dynamiczna_analiza_RAT_57]] · [[Laboratorium_Windows]]
