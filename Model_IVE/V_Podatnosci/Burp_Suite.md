---
title: "Burp Suite — platforma testów web (faza V)"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, web, gui]
category: narzedzie
status: documented
---

# Burp Suite

**TL;DR**: profesjonalna platforma do testowania aplikacji web — proxy + Repeater +
Intruder + (Pro) Scanner. Szczegóły i workflow w istniejącej nocie:
[[Wiedza/Pentest/Burp_Suite]].

## Rola w modelu I-V-E

W fazie **V** Burp identyfikuje luki web (OWASP Top 10): SQLi, XSS, CSRF, broken auth,
upload, SSRF. W fazie **E** Repeater/Intruder pozwala ręcznie potwierdzić i wykorzystać.

| Cecha | Wartość |
|-------|---------|
| Producent | PortSwigger |
| Wersje | Community (darmowa: Proxy/Repeater/Intruder/Decoder/Comparer) · Pro (płatna: Scanner, BApp, automatyzacja) |
| Interfejs | GUI (Java) |
| Nasz lab | Community 2026.7.2 w Kali — [[Wiedza/Pentest/Burp_Suite]] |

## Szybki workflow

1. Proxy nasłuchuje 127.0.0.1:8080 → przeglądarka przez Burp (cert HTTPS).
2. Proxy → Intercept = podgląd/podmiana żądania.
3. Repeater = ręczne testowanie parametru.
4. Intruder = fuzzing (payloady, brute).
5. (Pro) Scanner = automatyczne luki.

## ⚠️ GUI w labie

Burp to GUI. Na bezgłowym hoście odpalasz przez `ssh -X` lub lokalny desktop —
pełne wyjaśnienie w [[Wiedza/Pentest/Burp_Suite]].

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]] · [[Model_IVE/V_Podatnosci/OWASP_ZAP]] · [[Wiedza/Pentest/Burp_Suite]]
