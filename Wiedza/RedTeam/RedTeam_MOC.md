---
title: "Red teaming"
date: 2026-08-15
tags: [wiedza, redteam]
---

# Red teaming

Test całościowej odporności organizacji — realistyczne cele, mierzona detekcja i response.

Powiązane: [[Ataki/Ataki_MOC]] · [[Pentest/Pentest_MOC]] · [[Obrona/Obrona_MOC]] · [[Narzedzia/Sliver_C2]]

## Czym różni się od pentestu

| | Pentest | Red team |
|--|---------|----------|
| Zakres | ścisły, znany | szeroki, realistyczny |
| Cel | znaleźć luki | sprawdzić detekcję/response (blue/purple) |
| OPSEC | mniej ważny | kluczowy |
| Wynik | lista luk | "czy obrona zadziałała?" |

## Cykl red team

1. Cele i cele biznesowe (flags).
2. Rekon (OSINT) + infrastruktura C2 (Sliver, domeny, tunele — [[Narzedzia/Cloudflare_Konfiguracja]]).
3. Initial access (phishing, valid creds, exploit).
4. Post-exploit + lateral + persistence (jak w [[Ataki/Ataki_MOC]]).
5. Cel (crown jewels).
6. Raport + purple team (ćwiczenie z obroną).

## OPSEC

- Infrastruktura: redirectory, domeny, CDN/tunele, nie własne IP.
- Payloady: obfuskacja, signing, świadome YARA/Sigma (mało detekcji).
- Timing: poza godzinami SOC.

## Emulacja przeciwnika (adversary emulation)

- Plan = konkretny APT (wg raportu Unit42/Mandiant).
- Narzędzia open: Caldera (MITRE), Atomic Red Team, Red Canary.
- Mapowanie na ATT&CK.

## Purple team

- Współpraca red + blue: wykonaj technikę → sprawdź, czy detekcja działa → popraw regułę.
- Narzędzia: Atomic Red Team (testy jednostkowe detekcji), VECTR (śledzenie), MITRE ATT&CK Navigator.

## Powiązane w labie

- [[Narzedzia/Sliver_C2]] — C2.
- [[Projekty/Infrastruktura_C2/Infrastruktura_C2]] — tunelowanie/domeny.
- [[Analizy/Threat_Intel_MOC]] — detekcja (Suricata/Sigma/YARA).
