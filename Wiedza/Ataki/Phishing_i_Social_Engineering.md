---
title: "Phishing i social engineering"
date: 2026-08-15
tags: [wiedza, ataki, phishing]
category: atak
---

# Phishing i social engineering

Najczęstszy wektor initial access (T1566). Większość kampanii ransomware/stealerów zaczyna się tu.

## Rodzaje

- **Mass phishing** — masowy, generyczny.
- **Spear phishing** (T1566.001/.002) — celowany (osoba/firma).
- **Whaling** — na zarząd.
- **Vishing / Smishing** — głos / SMS.
- **Business Email Compromise (BEC)** — podszywanie się pod szefa/partnera (cel: przelew).
- **AiTM (Adversary-in-the-Middle)** — Evilginx2/Modlishka: reverse proxy łapie sesję + token 2FA (T1557/T1539).

## Elementy ataku

1. **Pretext** (fabuła: faktura, urlop, reset hasła, pilny przelew).
2. **Spoofing** — domena lookalike, spoofed display name.
3. **Payload** — załącznik (docx z makrem, LNK, ISO, HTML), link (kradzież danych / download).
4. **Landing** — fałszywa strona logowania.

## Narzędzia

| Narzędzie | Do czego |
|-----------|----------|
| GoPhish | kampanie (maile, trackowanie, raport) |
| Evilginx2 / Modlishka | AiTM, phishlet'y, łapanie sesji (MFA bypass) |
| SET | social engineering toolkit |
| ZPhisher / SocialFish | skrypty phishing |
| dnstwist | domeny lookalike (typosquat) |

## Obrona

- **Email:** SPF + DKIM + DMARC (enforce), filtrowanie załączników, sandbox, URL rewrite.
- **Tożsamość:** MFA phishing-resistant (FIDO2/WebAuthn) — TOTP można obejść przez AiTM.
- **Endpoint:** blokada makr (MOTW), ASR, EDR.
- **Ludzie:** szkolenia + symulacje + przycisk "zgłoś phish".
- **Monitor:** nowe domeny lookalike, loginy z nieznanych IP (impossible travel).

## Detekcja

- Logi email gateway (blokady), kliknięcia linków (URL rewrite/proxy).
- Loginy: MFA prompt bombing, logon z nowych lokalizacji (4624 type 3).
- EDR: makro wykonanie, spawn z Office (winword → powershell), LNK/ISO.
