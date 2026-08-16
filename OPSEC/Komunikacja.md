---
title: "Komunikacja"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, komunikacja, szyfrowanie]
status: active
category: komunikacja
---

# Komunikacja

Wybierz kanały, które szyfrują end-to-end (E2EE) — treść widzisz Ty i odbiorca, nie pośrednik.

## Komunikatory

| Narzędzie | E2EE | Uwagi |
|-----------|------|-------|
| Signal | tak | złoty standard, minimalne metadane |
| WhatsApp | tak | E2EE, ale wyłącz kopię zapasową w chmurze (łamie E2EE) |
| Telegram | tylko „Secret Chat" | zwykłe czaty i grupy nie są E2EE |
| Matrix/Element | tak (room E2EE) | własny serwer |

- Ważne sprawy: Signal albo Secret Chat.
- **Weryfikuj klucz/bezpieczeństwo** (compare security codes) przy nowym kontakcie, gdy to istotne.

## E-mail

- E-mail **nie jest** E2EE. Traktuj jak pocztówkę.
- Wrażliwe treści: Proton Mail / Tuta (E2EE między użytkownikami tego samego dostawcy) albo szyfruj załączniki (archiwum z hasłem, hasło innym kanałem).
- PGP, jeśli masz konkretną potrzebę — narzędzie scenariuszowe, nie codzienna wygoda.

## Telefon / głos

- Zwykłe połączenia GSM nie są szyfrowane przed operatorem/państwem.
- Signal / WhatsApp voice = E2EE.
- SIM swap: włącz PIN na karcie SIM i u operatora blokadę przeniesienia numeru (jeśli oferuje).

## Zasady

- **Nie wklejaj tokenów/haseł/kluczy** do czatów, kanałów, grup, ticketów (zob. [[XMask/opsec.exe/03_Nie_klikaj|XMask #3]]).
- Nie wysyłaj dokumentów tożsamości jako zwykły mail/SMS.
- Czaty „znikające wiadomości" tam, gdzie się da, i minimalna retencja.
- Konta z komunikatorów też podlegają [[Konta_hasla_2FA]].

## Powiązane

- [[Slady_i_prywatnosc]] · [[Konta_hasla_2FA]] · [[Checklist_OPSEC]]
