---
title: "Automatyzacja modelu I-V-E (recon → exploity)"
date: 2026-08-16
tags: [ive, automatyzacja, recon, exploit, pentest, ad]
category: pentest
status: active
---

# Automatyzacja I-V-E

Trzy skrypty spinające flow [[Model_IVE/IVE_MOC]] w jedną linię:
**recon → podatności → exploity**, z wynikami jako karty Obsidian i alertami
Telegram (wzorzec `alert_roles.py`).

| Skrypt | Faza | Co robi | Wynik |
|--------|------|---------|-------|
| `Narzedzia/target_profile.py` | I+V+E | theHarvester → nuclei tech-detect → nmap -sV → sqlmap → korelacja CVE | dossier `Projekty/Recon/<domain>.md` (sekcje I/V/E) + surowe outputy |
| `Narzedzia/cve_correlator.py` | E | wersje (nmap/nuclei) → CVE → searchsploit + msfconsole | karty planu `Projekty/Recon/<domain>/cve_<CVE>.md` + `exploit_plan.md` |
| `Narzedzia/password_spray.py` | E (AD) | kerbrute passwordspray z bezpiecznikiem lockout | karta `Lab/RedTeam_AD/Spray_<domain>_<data>.md` + alert Telegram |

## 1. target_profile.py — dossier celu

```bash
python3 Narzedzia/target_profile.py --domain xmask.lab
python3 Narzedzia/target_profile.py --domain example.com --skip nmap --dry-run
python3 Narzedzia/target_profile.py --domain 127.0.0.1 --urls cele.txt --nuclei-all
```

- **I** — `theHarvester -b crtsh,hackertarget,otx,rapiddns` (pasywnie) + DNS resolve.
- **V** — `nuclei` tech-detect (szablon z 13k pakietu) na celach web; `nmap -Pn -sV
  --script default,http-title,http-headers` na wykrytych IP (jak
  [[Model_IVE/_analiza_dynamiczna/live_demo/i1_nmap_sV.txt|i1_nmap_sV.txt]]);
  `sqlmap --batch --smart --banner` tylko na URL z parametrami.
- **E** — automatycznie woła `cve_correlator.py` na wynikach nmap/nuclei.
- Narzędzia: najpierw `PATH`, potem `docker exec <KALI_CONTAINER>` (np. kali z
  [[Lab/RedTeam_AD/README|RedTeam_AD]]). `--check-tools` pokazuje, co jest gdzie.
- Surowe outputy: `Projekty/Recon/<domain>/raw/`.

## 2. cve_correlator.py — CVE ↔ exploit

```bash
python3 Narzedzia/cve_correlator.py --nmap raw/nmap.txt --nuclei raw/nuclei_tech.jsonl \
    --domain xmask.lab --out Projekty/Recon/xmask.lab --msf
python3 Narzedzia/cve_correlator.py --version "Apache httpd 2.4.49" --domain t --out /tmp/o
python3 Narzedzia/cve_correlator.py --nmap nmap.txt --domain t --out /tmp/o --online --kb moje.json
```

- Wersje z nmap (`-oN`/`-oG`) i nuclei (JSONL: `info.classification.cve-id`).
- Lokalna baza wiedzy (Apache 2.4.49/2.4.50, OpenSSH regreSSHion, MS17-010,
  vsftpd 2.3.4, ProFTPD 1.3.3c, Exim 4.92, SambaCry, nginx resolver, PHP-FPM,
  Ghostcat, Jenkins) — rozszerzalna przez `--kb` (JSON: `[{product, version, cves, note}]`).
- `--online` dociąga metadane/CVSS z `cve.circl.lu`; `--msf` szuka modułów w
  `msfconsole` (wzorzec wyniku: [[Model_IVE/_analiza_dynamiczna/msf_search_ms17010.txt|msf_search_ms17010.txt]]).
- Karta planu: opis, Exploit-DB (searchsploit), moduły Metasploit z gotową komendą,
  kroki, źródła NVD/CIRCL. `exploit_plan.md` = tabela podsumowująca.

## 3. password_spray.py — kerbrute z bezpiecznikiem

```bash
python3 Narzedzia/password_spray.py --domain xmask.lab --dc 10.10.0.2 \
    --users /tmp/users.txt --password 'LabPass2026'
python3 Narzedzia/password_spray.py --domain xmask.lab --dc 10.10.0.2 \
    --users /tmp/users.txt --passwords hasla.txt --delay 60 --dry-run
```

Bezpiecznik (lockout):

| Parametr | Domyslnie | Znaczenie |
|----------|-----------|-----------|
| `--lockout-threshold` | 3 | próg lockoutu DC — weź realny: `net accounts` na DC |
| `--margin` | 1 | próby poniżej progu (zapas bezpieczeństwa) |
| `--max-per-user` | 1 | limit haseł na konto w jednym wywołaniu |
| `--delay` | 60 s | przerwa między partiami haseł |

- **Próby/konto = min(max-per-user, threshold − margin)** — twardy cap; przy
  threshold−margin ≤ 0 skrypt odmawia startu (exit 3).
- Jedno hasło = jedna partia `kerbrute passwordspray -d <domain> --dc <dc> users 'haslo'`
  (wzorzec z [[Lab/RedTeam_AD/Playbook_AD]]), potem `--delay`.
- Dedupe w stanie (`/root/obsidian-spray-state/spray_<domain>.json`): pary
  `user:haslo` już sprawdzone nie wracają; licznik prób na konto.
- Alert Telegram (wzorzec `alert_roles.py`): start, każde trafienie (`VALID LOGIN`),
  koniec z linkiem do karty; `.env` bota w `/root/obsidian-telegram-bot/.env`.
- `--dry-run` pokazuje plan bez dotykania DC.

## Integracja

```
target_profile.py --domain X
        │  I: theHarvester ──► raw/theharvester.json (+.txt)
        │  V: nuclei ─────────► raw/nuclei_tech.jsonl
        │     nmap ───────────► raw/nmap.txt / nmap.gnmap
        │     sqlmap ─────────► raw/sqlmap/
        └─► E: cve_correlator.py --nmap raw/nmap.txt --nuclei raw/nuclei_tech.jsonl
                 └─► Projekty/Recon/X/cve_<CVE>.md + exploit_plan.md
        └─► Projekty/Recon/X.md  (dossier I/V/E, linki do kart)
```

## Uwagi

- **Tylko autoryzowane cele** (lab: [[Lab/RedTeam_AD/README|RedTeam_AD]],
  DVWA/Juice Shop, własne VPS, example.com). Skrypty mają bezpieczne domysły,
  ale to narzędzia ofensywne — zakres zawsze z umowy/zgody.
- narzędzia (nmap/sqlmap/kerbrute/searchsploit/msfconsole) są w kontenerze Kali
  RedTeam_AD; na hoście są tylko theHarvester + nuclei.
- Sekrety (tokeny, hasła) poza vaultem — konwencja jak w `alert_roles.py`.
