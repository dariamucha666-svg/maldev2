---
title: "GoPhish + browser injection — analiza dynamiczna"
date: 2026-08-16
tags: [phishing, gophish, browser-injection, keylogger, js, dynamic-analysis, detection]
status: analysis
category: lab
---

# GoPhish + browser injection — analiza dynamiczna

Dynamiczna analiza: kampania GoPhish, w której **landing page zawiera wstrzyknięty JS** (keylogger + form-hijack), a ofiara (headless Chromium) wpisuje dane i wysyła formularz. Obserwacja, co JS robi w przeglądarce i dokąd exfiltruje.

Powiązane: [[Phishing_Sim_Lab]] · [[SET_Lab]] · [[Narzedzia/Phishing_Detekcja]] · [[detections/AiTM_Detekcja]]

## Setup

- GoPhish na .139 (admin 3333, phish 8080). Landing page "Inject Demo" (id 3) z wstrzykniętym <script>.
- Exfil C2: /opt/gophish/exfil_c2.py (127.0.0.1:9997, loguje beacony).
- Victim: /opt/gophish/victim.py (Playwright headless Chromium) — klika URL, wpisuje j.doe / SecretPass123, submit.

## Wstrzyknięty JS (co analizujemy)

1. **Keylogger** — document.addEventListener("keydown") → bufor klawiszy → co 2 s beacon Image do C2 (/k?d=).
2. **Form-hijack** — document.addEventListener("submit") → odczyt pól getElementById → beacon Image do C2 (/c?d=).

## Wynik (na żywo)

- **Keylogger przechwycił:** /k?d=j.doeSec (fragment klawiszy, exfil co 2 s).
- **Form-hijack przechwycił:** /c?d={"username":"j.doe","password":"SecretPass123"} — pełne creds.
- **GoPhish natywnie:** event "Submitted Data" dla user1, ale **payload None** — bo GoPhish wyciął atrybuty **name** z inputów, więc jego własny capture nie złapał danych. Wstrzyknięty JS ominął to przez getElementById.

## Kluczowy wniosek

GoPhish (framework) + wstrzyknięty JS (browser injection) = **dwie warstwy kradzieży**:
1. GoPhish: tracking kampanii + próba capture form (tu zawiodła przez stripping name).
2. Wstrzyknięty JS: keylog + form-hijack + exfil do własnego C2 (działa niezależnie od GoPhish).

To pokazuje, czemu phish-kity łączą framework (GoPhish) z własnym JS — bo natywny capture ma ograniczenia, a JS daje keylogger i exfil poza frameworkiem.

## Detekcja (wskaźniki)

1. **Wstrzyknięty <script>** w treści landing page — sygnatura: keydown + Image beacon + submit hook.
2. **Exfil do obcego hosta**: beacon Image do /k?d= i /c?d= (query z danymi), nie do domeny kampanii.
3. **Image beacon** (1x1 / new Image().src) — klasyczny kanał exfil (omija CORS).
4. Suricata: reguła na GET z parametrem /k?d= lub /c?d= do zewnętrznego IP.

## Sprzątnięcie

- Exfil C2 zatrzymany. GoPhish campaign + page zostawione jako lab artifact (kampania 3, page 3).

## Pliki (na .139)

- /opt/gophish/landing_inject.html (landing + JS)
- /opt/gophish/exfil_c2.py (C2)
- /opt/gophish/victim.py (Playwright victim)
- /opt/gophish/setup_gophish.py (API setup)
