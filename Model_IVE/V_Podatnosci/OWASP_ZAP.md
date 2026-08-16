---
title: "OWASP ZAP — darmowy skaner aplikacji web"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, web]
category: narzedzie
status: documented
---

# OWASP ZAP

**TL;DR**: darmowy, otwartoźródłowy **skaner aplikacji web** (najczęściej używany),
alternatywa dla Burp Suite. Ma GUI, ale też tryb headless/automation (lepszy do skryptów).

## Co to / do czego

Zed Attack Proxy — proxy + skaner DAST. Przechwytuje ruch, spideruje aplikację i
aktywne skanowanie wykrywa luki OWASP Top 10 (SQLi, XSS, SSRF, misconfig…).

| Cecha | Wartość |
|-------|---------|
| Licencja | Apache 2.0 (open-source) |
| Język | Java |
| Interfejs | GUI + API + headless (`zap-baseline`, `zap-full-scan`) |
| Skan | passive (z ruchu) + active (atakuje) |

## Instalacja

```bash
# Docker (najprościej)
docker pull zaproxy/zap-stable
# headless baseline na celu:
docker run --rm -t zaproxy/zap-stable zap-baseline.py -t https://cel.com -r raport.html

# albo paczka/JAR (Java jest na tym hoście — OpenJDK 21)
```

> ⚠️ **Nie odpalane tutaj**: pełny skan ZAP (image ~1.5 GB + ~2 GB RAM na skan)
> przy ~1.5 GiB wolnej pamięci ryzykuje OOM. Dokumentuję + podaję komendy; do
> uruchomienia użyj VM z ≥4 GB RAM albo naszego Kali (patrz [[Wiedza/Pentest/Burp_Suite]]).

## Headless (CI — najprzydatniejsze dla automatyzacji)

```bash
docker run --rm -t zaproxy/zap-stable zap-baseline.py -t http://10.10.0.20 -r baseline.html
docker run --rm -t zaproxy/zap-stable zap-full-scan.py  -t http://10.10.0.20 -r fullscan.html
```

## ZAP vs Burp

| | ZAP | Burp Suite |
|--|-----|------------|
| Cena | darmowy | Community darmowy, Pro płatny |
| Headless/automation | ✅ (baseline/full-scan) | głównie GUI |
| Do skryptów/labu | ✅ lepszy | Pro (płatny scanner) |

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]] · [[Model_IVE/V_Podatnosci/Burp_Suite]] · [[Techniki_i_Narzedzia]]
