---
title: "Przejęcie konta Telegram — analiza (stealer-telegram-acc, TeleKiller, PowerShell)"
date: 2026-08-15
updated: 2026-08-15
tags: [telegram, stealer, account-takeover, malware, reverse-engineering]
status: analysis
category: malware
---

# Przejęcie konta Telegram — analiza narzędzi

Powiązane: [[Keylogger_Analiza]] · [[Clipper_Stealer_Analiza]] · [[Klasyfikacja_Korpus]]

## Przegląd

| Narzędzie | Typ | Mechanizm |
|-----------|-----|-----------|
| **RusGheast/stealer-telegram-acc** | bot phishing (Python) | **social-engineering login flow** (phone + code + 2FA przez bota) |
| **TeleKiller** (ultrasecurity) | tdata stealer (Python) | **kradzież sesji** `tdata` + keylogger + reverse shell |
| **Windows Telemetry Update** (PowerShell) | stealer sesji | złośliwy PS maskujący się jako telemetria |
| **Still Sync** | — | nie znaleziono repo (niszowe / skrót) |

---

## 1. RusGheast/stealer-telegram-acc (Python)

- **hash (run.py)**: `a75c36ebb9a31de9ca528c6efa15a6d1db41eb21cbb6e533ead35aa2f7da9dc0`

### Mechanizm (z kodu)

```python
# aiogram (bot) + telethon (klient Telegram)
bot = Bot(token=TOKEN)                    # bot atakującego
client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
if not await client.is_user_authorized():
    code = await client.send_code_request(phone_number)   # wysyła kod do ofiary
    # → bot pokazuje klawiaturę inline 0-9 → ofiara wpisuje kod
    # → potem password (2FA)
```

**To social-engineering MITM logowania:** ofiara podaje botowi swój numer telefonu, potem kod
logowania (SMS/app) i hasło 2FA — atakujący dostaje **sesję** (plik `sessions/<phone>.session`).

### IOC

- Pliki sesji: `sessions/*.session` (Telethon).
- API: `aiogram` + `telethon` + `TelegramClient.send_code_request`.
- Pretekst: „sharing a ..." (zmusza ofiarę do „udostępnienia konta").

---

## 2. TeleKiller (ultrasecurity, Python)

- **hash (TeleKiller.py)**: `49ba8548371940188ca15fc1d3859280035167c9dc1cd53c826f367a81cd1501`

### Mechanizm (z kodu — payload wstrzykiwany)

```
payload (py2exe na Windows) → socket do atakującego
  ├─ kradzież sesji: archiwizuje %AppData%\Telegram Desktop\tdata\  (make_archive → tdata.tar.bz2)
  ├─ taskkill /F /IM Telegram.exe   (odblokowanie tdata)
  ├─ keylogger: pyHook (HookManager + KeyDown) + clipboard (GetClipboardData)
  ├─ reverse shell: cmd.exe przez socket (cd / wmic / Popen)
  └─ recon: hostname, systeminfo, net localgroup users/Administrators
```

**Klasyczny tdata stealer** — kradnie folder `tdata` (klucze sesji Telegrama), który atakujący
importuje do własnego klienta → **pełne przejęcie konta** (bez hasła/2FA).

### IOC

- Ścieżka: `%AppData%\Telegram Desktop\tdata\` + archiwum `tdata.tar.bz2`.
- `taskkill /F /IM Telegram.exe` (zabija Telegrama przed kradzieżą).
- Obfuskacja: nazwy funkcji = md5-hexy (`a88f05b6...`, `b3c7cbace...`).
- Payload: pyHook + clipboard + socket + `Popen` (RAT).

---

## 3. Windows Telemetry Update (PowerShell)

Brak publicznego repo (kampania). Z publicznej wiedzy:

- Złośliwy PowerShell podszywający się pod „aktualizację telemetrii Windows".
- Kradnie **sesje/cookie/tokeny** (przeglądarki, Telegram, Discord) i exfilruje do C2.
- Dystrybucja: phishing (załącznik `.ps1` / `lnk`) lub loader.
- **Detekcja**: PS z `Invoke-WebRequest`/`Net.WebClient` + ścieżki `Telegram Desktop\tdata`,
  `AppData\Local\Google\Chrome\User Data`, kodowanie base64 (`-enc`).

---

## Wspólne wskaźniki przejęcia konta

1. **Sesja/tdata**: `%AppData%\Telegram Desktop\tdata\` (kradzież sesji).
2. **Kod logowania**: `send_code_request` + inline keyboard 0-9 (phishing login flow).
3. **Keylogger/clipboard**: `pyHook` / `GetClipboardData` (uzupełnia kradzież).
4. **Exfil**: socket / Telegram Bot API / `Invoke-WebRequest`.
5. **Zabijanie procesu**: `taskkill Telegram.exe` (odblokowanie sesji).

## Reguły detekcji

YARA → `/root/android-pipeline/tools/yara-rules/custom/telegram_stealer.yar`.

## Next

1. Dynamiczna analiza payloadu TeleKiller (przechwycić exfil sesji).
2. Znaleźć realną próbkę „Windows Telemetry Update" (Any.run/VT) → statyczny RE.
