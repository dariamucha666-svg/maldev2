---
title: "Wiedza — baza o atakach, malware i obronie"
date: 2026-08-15
updated: 2026-08-15
tags: [wiedza, index, moc, intel, malware, pentest, redteam, obrona]
status: active
---

# Wiedza — gromadzenie wiedzy o zagrożeniach

Folder do regularnego gromadzenia wiedzy o: **nowych wirusach, malware, pentestingu,
red teamingu, analizie malware, nowych atakach, narzędziach i obronie.**

> **Zasada:** notatki = wiedza ogólna + konkretne TTP + narzędzia + obrona.
> Konkretne próbki z labu (RE, IoC, detekcja) zostają w [[Analizy]] — tu linkujemy do nich,
> żeby nie dublować.

## Mapa folderu

| Kategoria | Notatka | Co zawiera |
|-----------|---------|------------|
| Techniki ataku | [[Ataki/Ataki_MOC]] | Fazy ataku (MITRE ATT&CK), TTP, narzędzia, obrona |
| Malware / wirusy | [[Malware/Malware_MOC]] | Rodziny: stealery, ransomware, loadery, RAT, clippery |
| Pentesting | [[Pentest/Pentest_MOC]] | Metodologia, web/network/AD, narzędzia, raport |
| Red teaming | [[RedTeam/RedTeam_MOC]] | OPSEC, C2, emulacja przeciwnika, purple team |
| Obrona | [[Obrona/Obrona_MOC]] | Detekcja, hardening, IR, D3FEND, Sigma/YARA |
| Narzędzia | [[Narzedzia]] | Katalog narzędzi ofensywnych i defensywnych |
| Źródła | [[Zrodla]] | Feedy, API, blogi, kanały do śledzenia |
| Dziennik zmian | [[Aktualizacje]] | Co i kiedy dodano (regularne aktualizacje) |
| Feed auto | [[Feed_MalwareBazaar]] · [[Feed_CISA_KEV]] · [[Feed_ThreatFox]] | Auto-generowane snapshoty: próbki / eksploatowane CVE / IoC |

## Jak aktualizujemy (regularnie)

1. **Automat:** `Narzedzia/update_wiedza.sh` — pobiera świeże dane z 3 źródeł:
   MalwareBazaar (próbki), CISA KEV (eksploatowane CVE), ThreatFox (IoC), nadpisuje
   [[Feed_MalwareBazaar]] · [[Feed_CISA_KEV]] · [[Feed_ThreatFox]] i dopisuje wpis do
   [[Aktualizacje]]. Cron: `/etc/cron.d/obsidian-wiedza` (co 6 h). Commit robi `obsidian-git` (co 15 min).
2. **Półautomat:** nowa rodzina / nowy atak / nowe narzędzie → nowa notatka z [[_Template]].
3. **Ręcznie:** po analizie próbki w [[Analizy]] dopisz rodzinę/technikę do odpowiedniego MOC.

## Szablon

- [[_Template]] — szablon wpisu wiedzy (atak / malware / narzędzie / obrona).

## Powiązane

- [[Analizy/Threat_Intel_MOC]] — znaleziska z labu (hash → C2 → detekcja)
- [[OPSEC/README|OPSEC]] — zabezpieczenia po prostu (obrona siebie: konta, ślady, komunikacja, urządzenia)
- [[Zasoby/Droga_przez_cyberbezpieczenstwo]] — ścieżka nauki
- [[Zasoby/Linki_Zewnętrzne]] — pełna lista URL
- [[Home]] — start vaultu
