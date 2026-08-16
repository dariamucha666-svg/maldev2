---
title: "Źródła wiedzy o zagrożeniach"
date: 2026-08-15
tags: [wiedza, intel, feeds, sources]
---

# Źródła — skąd brać świeżą wiedzę

Powiązane: [[Zasoby/Linki_Zewnętrzne]] · [[Narzedzia]] · [[Zrodla_Mobile_Malware]] (malware mobilny)

## Feedy / API (da się automatyzować)

| Źródło | Co daje | Jak |
|--------|---------|-----|
| MalwareBazaar (abuse.ch) | Świeże próbki, rodziny, hashe, tagi | API `mb-api.abuse.ch/api/v1/`, nagłówek `Auth-Key` (klucz `~/.mb_api_key`) |
| ThreatFox (abuse.ch) | IoC (IP/domain/url) | API, darmowy klucz |
| URLhaus (abuse.ch) | Złośliwe URL | API |
| CISA KEV | Exploitowane CVE (priorytet patch) | JSON `cisa.gov/known-exploited-vulnerabilities-catalog.json` |
| NVD / CVE | Luki | `services.nvd.nist.gov/rest/json/cves/2.0` |
| AlienVault OTX | Pulse / IoC | `otx.alienvault.com/api/v1/pulses/subscribed` |
| MITRE ATT&CK / D3FEND | TTP + techniki obrony | `github.com/mitre/cti` (STIX/JSON) |
| VX-Underground | Kolekcje malware + papery | `vx-underground.org`, GitHub |
| GreyNoise | IP z internetu (skanery/exploity) | API |

## RSS / blogi vendorów (analizy kampanii)

- Mandiant / Google Cloud Threat Intel (ex-FireEye) — `cloud.google.com/blog/topics/threat-intelligence`
- Unit 42 (Palo Alto) — `unit42.paloaltonetworks.com`
- CrowdStrike Blog — adversary write-ups
- SentinelOne — `sentinelone.com/blog`
- Microsoft Threat Intelligence — `microsoft.com/security/blog`
- SANS Internet Storm Center — dzienne wpisy ISC (`isc.sans.edu`)
- The Hacker News / BleepingComputer / Krebs on Security — news

## Telegram / X (monitoring)

- X: `@vxunderground`, `@malwrhunterteam`, `@TheDFIRReport`, `@BleepinComputer`, `@unit42_intel`, `@GossiTheDog`.
- Telegram: kanały CTI i breach-watch (w labie: [[Narzedzia/Telegram_Security]] — opsec własnego kanału).

## Repozytoria reguł (detekcja)

- Sigma HQ — `github.com/SigmaHQ/sigma`
- Joe Security Sigma — `github.com/joesecurity/sigma-rules`
- Elastic detection rules — `github.com/elastic/detection-rules`
- Splunk security content — `github.com/splunk/security_content`
- YARA rules — `github.com/Yara-Rules/rules`, `github.com/Neo23x0/signature-base` (Florian Roth)
- Atomic Red Team — `github.com/redcanaryco/atomic-red-team` (testy detekcji)

## Jak to przeliczyć na notatki

1. Feed/API → nowe rodziny / CVE / kampanie.
2. Wybierz to, co pasuje do profilu labu (Android/Windows, stealery/RAT/clippery).
3. Dodaj notatkę z [[_Template]] i wpis do [[Aktualizacje]].
