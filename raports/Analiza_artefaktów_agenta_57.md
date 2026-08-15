---
title: "Analiza artefaktów agenta .57"
date: 2026-08-15
type: raport
tags: [forensics, windows, artifacts, c2, dfir]
status: observation-only
---

# Analiza artefaktów agenta `.57`

> **Charakter:** dokumentacja forensyczna — gdzie na dysku/rejestrze/logach systemowych pozostają ślady po operacjach wykonanych na agencie. Służy do **wykrywania i rekonstrukcji** (IR), nie do usuwania śladów.
>
> **Zakres:** `net user /add` (dodanie użytkownika), ustawienie wartości w kluczu `Run` (persistence), keylogger, oraz (dodatkowo) `screenshot`.

---

## 1. Ślady po dodaniu użytkownika (`net user <name> <pass> /add`)

### 1.1 Baza SAM i rejestr
- **`C:\Windows\System32\config\SAM`** — nowy rekord konta (nazwa, RID, pole `F` = czas ostatniego logowania, pole `V` = dane konta). Odczyt wymaga uprawnień SYSTEM lub parsowania offline hivów.
- **`C:\Windows\System32\config\SECURITY`** — wpisy LSA (SID → nazwa).
- Rejestr (widok przez `regedit`/offline): `HKLM\SAM\SAM\Domains\Account\Users\Names\<username>` oraz podklucz RID.
- **`C:\Users\<username>\`** — profil tworzony przy pierwszym logowaniu (jeśli nastąpił): `NTUSER.DAT`, `AppData`, `Desktop`, `Downloads`, itd.

### 1.2 Logi zdarzeń (Security)
| EventID | Znaczenie |
|---|---|
| **4720** | utworzenie konta użytkownika |
| **4722** | włączenie konta |
| **4732** | dodanie do lokalnej grupy (np. `Administrators`) |
| **4728 / 4738** | dodanie do grupy globalnej / zmiana konta |
| **4624** | logowanie (jeśli nastąpiło) |

### 1.3 Procesy i pliki pomocnicze
- `net.exe` → `net1.exe` — **Security 4688** (utworzenie procesu), **Sysmon EventID 1** (CommandLine: `net user ... /add`).
- **Prefetch**: `C:\Windows\Prefetch\NET.EXE-*.pf`, `NET1.EXE-*.pf`.
- **MFT / USN Journal**: wpisy dla nowego katalogu profilu i zmodyfikowanych hivów.

---

## 2. Ślady po ustawieniu wartości w kluczu `Run` (persistence)

### 2.1 Rejestr
- Klucze autostartu:
  - `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
  - `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
  - `...\RunOnce` (jednorazowo)
  - wariant 32-bitowy: `...\Wow6432Node\...\Run`
- Wartość (np. `REG_SZ`/`REG_EXPAND_SZ`) wskazująca na payload.
- **Plik hivu na dysku**: `C:\Users\<user>\NTUSER.DAT` (HKCU) lub `C:\Windows\System32\config\SOFTWARE` (HKLM).
- **LastWriteTime** klucza `Run` = czas modyfikacji.

### 2.2 Logi zdarzeń
| Źródło | EventID | Znaczenie |
|---|---|---|
| Security | **4657** | modyfikacja wartości rejestru — **tylko gdy** skonfigurowano SACL audytu obiektów (domyślnie wyłączone) |
| Sysmon | **13** | RegistryValueSet (ustawienie wartości) |
| Sysmon | **12** | RegistryKey create/delete |
| Sysmon | **1** | uruchomienie `reg.exe`/`regedit.exe` |
| Security | **4688** | uruchomienie `reg.exe` |

### 2.3 Efekt po restarcie/logowaniu
- Po ponownym logowaniu (HKCU) lub starcie (HKLM) payload jest uruchamiany → kolejne **4688 / Sysmon 1** dla payloadu + ewentualne **5156 / Sysmon 3** (połączenie sieciowe).

---

## 3. Ślady keyloggera

| Kategoria | Artefakt |
|---|---|
| **Plik logu** | `keylog_57.txt` (lub ścieżka z konfiguracji) — zwykle `%TEMP%`, `%APPDATA%`, katalog roboczy agenta; wpis w **MFT/USN**, czasy utworzenia/modyfikacji |
| **Proces** | długo żyjący proces keyloggera/agenta — **4688**, **Sysmon 1** |
| **Hooking** | `SetWindowsHookEx(WH_KEYBOARD_LL)` → ładowanie hook DLL do procesów — **Sysmon 7** (Image loaded); alternatywnie pętla `GetAsyncKeyState` (bez hook DLL, tylko proces + obciążenie CPU) |
| **Persistencja** | klucz `Run` (jeśli ustawiony) — **4657** / **Sysmon 13** |
| **Eksfiltracja** | połączenie do C2 na port 9999 — **5156** (WFP), **Sysmon 3** |
| **Prefetch** | `C:\Windows\Prefetch\<keylogger_exe>-*.pf` |
| **Pamięć** | bufor przechwyconych klawiszy w przestrzeni procesu |

---

## 4. Dodatkowo: `screenshot`

| Kategoria | Artefakt |
|---|---|
| **Plik** | `screenshot_57.png` — wpis MFT/USN, czasy |
| **Proces/API** | proces wykonujący przechwycenie (GDI: `BitBlt`/`GetDC`), Sysmon 1 (jeśli nowy proces) |
| **Sieć** | wysyłka obrazu (base64) do C2 na 9999 — 5156 / Sysmon 3 |

---

## 5. Podsumowanie mapowania

| Operacja | Kluczowe ślady dyskowe/rejestru | Kluczowe EventID |
|---|---|---|
| `net user /add` | SAM, profil `C:\Users\...`, prefetch NET*.pf | 4720, 4722, 4732, 4688 |
| `reg add ...Run` | wartość w `Run`, NTUSER.DAT/SOFTWARE | 4657 (jeśli SACL), Sysmon 12/13, 4688 |
| keylogger | plik `keylog_*.txt`, hook DLL, prefetch | 4688, Sysmon 1/7/13, 5156 |
| screenshot | plik `screenshot_*.png` | 4688, Sysmon 1/3, 5156 |

---

## 6. Uwagi do rekonstrukcji (IR)

- Odtworzenie kolejności zdarzeń: skoreluj **4688** (`net.exe`/`reg.exe`) → **4720/4732** (konto) → **4657/Sysmon 13** (Run) → **4624** (logowanie) → uruchomienie payloadu → **5156/Sysmon 3** (połączenie 9999).
- Brak **4657** nie oznacza braku zmiany rejestru — audyt obiektów rejestru jest domyślnie wyłączony; Sysmon 12/13 lub parsowanie hivów (LastWriteTime) jest wtedy niezawodniejsze.
- Pliki `keylog_57.txt` / `screenshot_57.png` same w sobie są artefaktami plikowymi (MFT/USN) — ich treść to dane eksfiltrowane, nie przedmiot tej analizy.
