---
tags:
  - daily
  - journal
  - lab
updated: 2026-08-15
---

# Dziennik Lab

Codzienne wpisy. Szczegóły dnia często też w `Daily/YYYY-MM-DD.md`.

Powiązane: [[Dashboard]] · [[Daily/2026-08-15]] · [[Daily/2026-08-14]] · [[Lab/Recap 2026-08-14]]

---

## 2026-08-15

### Klasyfikacja w vaultcie + tagi pipeline

- [[Klasyfikacja_Korpus]] — tabela „co to oznacza” (RAT 1, backdoor 1, stealer 4+, dropper 5+, packed 3+, cryptojacker 0).
- Karty: [[410a5cba Android RAT kira]], [[4d0f7a96 Android SMS stealer avanegar]], [[a710209e Android NFC skimmer]], [[1b3ceba6 Chrome bank stealer]].
- `classify_roles.py` w `pipeline.sh` po auto-YARA — raporty JSON dostają `tags` + `classification.role`.
- Next RE: de4dot na NanoCore (offline) albo native packed APK.

### Static RE — kira

- `410a5cba` = [ivan-sincek/malware-apk](https://github.com/ivan-sincek/malware-apk) v5.5, lab/PoC, nie kampania.
- Techniki RAT są prawdziwe (a11y + overlay + notifications), C2 nie jest zaszyte.
- [[410a5cba Android RAT kira]]

### Static RE — Chrome MV3 Receita Federal

- `1b3ceba6` = stealer bankowy, nie lab.
- Socket.IO `ws.servpopads.com`; config `servpopads.com`; manifest: `suahoje.com:3000`, `off-game.com:3000`, Cobrowse, update `serpopwin.com`.
- Inputy + cookies + screenshot + fałszywe modale token/QR + ukryty pulpit sesji.
- [[1b3ceba6 Chrome bank stealer]] · [[1b3ceba6]]

### Static RE — klaster .NET

- 3× NanoCore (`NanoCore Client.exe`), 1× Loader 9.8 MB, 1× NursultanCrack, 1× system32+webcam.
- [[DotNet_cluster]] · YARA `nanocore_client.yar`

## 2026-08-14

### Wieczór #4 — YARA `Backdoor_EASports_Go` w pipeline

- Wgrano `/root/android-pipeline/tools/yara-rules/custom/backdoor_easports.yar` na `.133`.
- `pipeline.sh` / `batch_analyze.sh` / nightly biorą cały `custom/*.yar` — bez zmiany skryptów.
- Hit: `Backdoor_EASports_Go` + `Auto_PE_178cb931` na `141935c46a5c4ff1b84b433e84f36e61.exe`.
- Odświeżony `reports/178cb931…/yara.txt`.

### Wieczór #3 — dashboard publiczny :8080

- `/var/www/ioc-dashboard/{index.html,iocs.json}`
- `python3 -m http.server 8080` + UFW 8080/tcp
- http://5.175.189.133:8080 — HTML/JSON 200 z Kali (15 IOC)
- [[Dashboard_IOC]]

### Wieczór #2 — auto-YARA + dashboard (22:15 UTC)

- `yara_generator.py` wpięty w `pipeline.sh` (`generate_auto_yara` po analizie).
- Katalog jako target: `~/pipeline.sh --pe-only /root/samples/quarantine/` — działa (29 plików, PE skipnięty jako już analizowany).
- Wyjście: `/root/samples/reports/auto_rules.yar` + `iocs.json` (15 IOC, 3 reguły).
- `yara … 141935c46a5c4ff1b84b433e84f36e61.exe` → **`Auto_PE_178cb931`**.
- `yara -r … /root/samples/raw/` → 0 hitów (stringi APK z jadx, nie z ZIP).
- Dashboard: `/root/android-pipeline/web/` · `127.0.0.1:8766` · `/api/iocs` 200.
- Sigma: **nie zrobione**.
- Notatka: [[Dashboard_IOC]]

### Sesja wieczór (Kali → `.133`)

- SSH `root@5.175.189.133` — host `vserver959630`, Ubuntu 24.04.4, 78% dysku, 13% RAM.
- Zainwentaryzowany [[Pipeline_Analizy]]: `batch_analyze.sh`, `pipeline.sh`, `nightly_pipeline.sh`, cron `0 2 * * *`.
- Wersje: jadx 1.5.1, apktool 2.11.1, yara 4.5.0, r2 5.5.0, pefile 2024.8.26, capa 9.4.0.
- Stan próbek: 14 APK, 29 JSON, 1 PE w kwarantannie.
- Nightly 02:00 UTC ściągnął 10 APK z MalwareBazaar, 843 unique URL (dużo szumu schematów Android).
- Ręczny `FORCE=1` na PE `141935c46a5c4ff1b84b433e84f36e61.exe` (21:31 UTC) — OK, capa timeout.
- Sliver v1.7.3 daemon aktywny; HTTPS tylko na `127.0.0.1:443` za tunelem `maskchat-c2`. **31337 i 8443 na `*`.**
- Założony pełny indeks vaultu: `_Dashboard/` + `Projekty/` + `Narzedzia/` + `Analizy/` + `Zasoby/`.

### Sesja dzień (recap)

Pełny opis: [[Lab/Recap 2026-08-14]]

- Windows RE na `.57` przygotowany (Ghidra 12.1.2, PEStudio, x64dbg, ProcMon, Wireshark).
- OpenCut / capcut-mate **Disabled** — RAM pod RE.
- Static RE PE Go 1.25.4, cert `easports.gg`, motyw ag/elevator.
- Vault markdown na Kali i na VPS.

### Otwarte

1. Dekompilacja `main.main` + `main.itnlwdcdwymtd`.
2. Overlay hexdump / PKCS#7.
3. capa ≥ 180 s.
4. `go tool nm` / `rabin2 -s` na `.symtab`.
5. PEStudio/x64dbg offline.
6. UFW na 31337 jeśli multiplayer ma być prywatny.
7. Sprawdzić, czy `python3 -m http.server 8765` z `/tmp/pe_in` nie wrócił.

---

## 2026-08-13

- Stage-2 static RE zapisany w `/root/samples/reports/payload_stage2_20260813/REPORT.md`.
- Electron installer config dump — pusty Telegram, URL stage-2, fake „Runtime Components”.
- HEAD domen: żywy tylko `suahoje.com:3000`.
- NSIS `963800f7…` = Electron 64-bit (~259 MB).
- Nightly pipeline 02:02 UTC — daily summary wygenerowany.

---

## 2026-08-12 / 11

- Nightly działa (logi `nightly_20260812.log`).
- Sliver daemon od 12.08 14:45 UTC.
- Tunele Cloudflare: `maskchat-c2` (11.08 00:48), `c2-drugi` (11.08 04:47).
- Pipeline zainstalowany ~08.08 (`install.sh`, wrapper `/usr/local/bin/android-malware-pipeline`).
