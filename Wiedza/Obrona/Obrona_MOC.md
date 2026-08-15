---
title: "Obrona — detekcja, hardening, IR"
date: 2026-08-15
tags: [wiedza, obrona, blue team]
---

# Obrona

Powiązane: [[Ataki/Ataki_MOC]] (co wykrywamy) · [[Narzedzia]] (narzędzia) · [[Analizy/Threat_Intel_MOC]] (detekcja w labie)

## Warstwy obrony (defense in depth)

1. **Perimeter:** firewall, WAF, IDS/IPS.
2. **Endpoint:** EDR/AV, Sysmon, hardening.
3. **Tożsamość:** MFA, PAM, least privilege, LAPS.
4. **Sieć:** segmentacja, zero-trust, DNS monitoring.
5. **Dane:** backup, DLP, szyfrowanie.
6. **Ludzie:** szkolenia phishing, świadomość.

## Detekcja — pipeline

Logi (Sysmon, Windows Events, sieć) → SIEM → reguły (Sigma/YARA/Suricata) → alerty → IR.

- **Windows kluczowe Event ID:** 4624/4625 (logon), 4688 (proc create), 7045 (service),
  4104 (PS script block), 4720 (user create), 4769 (Kerberos ticket), 4662 (DC replication).
- **Sysmon:** 1 (proc), 3 (netconn), 7 (image load), 11 (file), 13 (registry).
- **Sigma:** uniwersalne reguły → konwersja na SIEM.
- **YARA:** detekcja plików.
- **Suricata/Zeek:** detekcja sieci.

## MITRE D3FEND (odpowiedź na ATT&CK)

Każda technika ataku ma technikę obrony (np. Credential Access → Credential Hardening/MFA).

## Hardening — checklist szybki

- **Windows:** LAPS, Credential Guard, ASR, blokada makr, tamper protection, AppLocker/WDAC.
- **Linux:** aktualizacje, SSH klucze, fail2ban, SELinux/AppArmor, sudoers minimal.
- **Sieć:** segmentacja VLAN, DMZ, blokada LLMNR/mDNS, DNS filtering.
- **AD:** tiering (Tier 0/1/2), krbtgt rotation, monitor BloodHound paths, honeytokens.

## Incident Response (IR) — cykl

1. Przygotowanie (plany, playbooki).
2. Identyfikacja (detekcja/triage).
3. Ograniczenie (izolacja hosta).
4. Eradykacja (usunięcie, re-image).
5. Recovery (przywrócenie).
6. Lessons learned (retro + poprawa detekcji).

Frameworki: NIST 800-61, SANS PICERL.

## Backup (przeciw ransomware)

**3-2-1:** 3 kopie, 2 media, 1 offsite + offline/immutable.

## Powiązane

- [[Ataki/Ataki_MOC]] — co wykrywamy.
- [[Analizy/Threat_Intel_MOC]] — konkretne reguły w labie (Suricata/Sigma/YARA).
