---
title: "Ransomware i ekstorsja"
date: 2026-08-15
tags: [wiedza, ataki, ransomware]
category: atak
---

# Ransomware i ekstorsja

Szyfrowanie + (dziś zwykle) kradzież danych + groźba publikacji (double/triple extortion).

## Model biznesowy

- **RaaS** (Ransomware-as-a-Service): operator + afiliaci dzielą okup.
- **IAB** (Initial Access Broker): sprzedaje dostęp do firm.
- **Leak sites**: publikacja skradzionych danych jako presja.

## Znane grupy / rodziny

LockBit, BlackCat/ALPHV, Cl0p, Akira, Play, Black Basta, BianLian, Medusa, Royal, Qilin.

## Wektory (jak wchodzą)

- RDP bruteforce (bez MFA).
- Phishing (loader → ransomware).
- Exploit VPN/edge (Ivanti, Fortinet, Citrix, PAN-OS) — patrz CISA KEV.
- Valid creds (z infostealer logs).

## Cykl ataku

1. **Initial access** (jak wyżej).
2. **Rekon wewnętrzny + lateral** (BloodHound, Cobalt).
3. **Eksfiltracja** (rclone, MEGA) — przed szyfrowaniem.
4. **Ransomware:** wyłączenie backupu (`vssadmin delete shadows`), kill EDR, szyfrowanie (AES + RSA).
5. **Nota z okupem + leak site.**

## Obrona

- **Backup: 3-2-1 + offline/immutable** (najważniejsze!).
- MFA na RDP/VPN + segmentacja.
- Patch edge (CISA KEV priorytet).
- EDR + tamper protection + monitor `vssadmin`/`bcdedit`.
- Least privilege + LAPS (blokuje lateral).
- Ćwiczenia IR + playbook ransomware.

## Detekcja (kluczowe sygnały)

- `vssadmin delete shadows`, `wmic shadowcopy delete` (Sysmon/EDR).
- Masywne rename/encrypt (dużo operacji plików).
- Wyłączanie ochrony (`sc stop`, `taskkill`).
- Rclone/MEGA exfil outbound.
- SMB scan + admin shares (C$, ADMIN$).
