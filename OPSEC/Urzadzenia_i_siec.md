---
title: "Urządzenia i sieć"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, urzadzenia, siec, hardening]
status: active
category: urzadzenia
---

# Urządzenia i sieć

Aktualny, zamknięty system to podstawa. Większość ataków wchodzi przez niezałataną dziurę albo złe ustawienie.

## Urządzenia (telefon, laptop)

- **Aktualizacje automatyczne** włączone (OS, przeglądarka, aplikacje, firmware routera).
- **Pełne szyfrowanie dysku** (BitLocker, FileVault, Android/iOS domyślnie) + blokada ekranu PIN/biometria.
- **Minimalny zestaw aplikacji.** Usuwaj nieużywane; każda to potencjalna dziura.
- **Konta użytkowników:** na co dzień bez admina; admin osobno (UAC / sudo).
- **Backup 3-2-1:** 3 kopie, 2 nośniki, 1 poza domem; testuj odzyskiwanie.
- **Telefon:** Play Protect / weryfikacja aplikacji włączone; nie rootuj bez potrzeby; nie instaluj APK spoza sklepu.

## Sieć

- **Router:** zmień domyślne hasło admina, aktualizuj firmware, wyłącz WPS, włącz WPA3 (albo WPA2).
- **Gościnna sieć** dla urządzeń IoT / gości.
- **Publiczne Wi-Fi:** unikaj do banku/maila; jeśli musisz — zaufany VPN albo własny hotspot.
- **VPN:** chowa IP przed siecią i dostawcą, nie czyni anonimowym ani nie szyfruje całej drogi end-to-end. Do anonimizacji to inna liga (zob. [[Podstawy_OPSEC]]).
- **Bluetooth/NFC:** wyłączaj, gdy nie używasz.

## Hardening (szybka lista)

- Firewall włączony (UFW / Windows Defender Firewall).
- Nie otwieraj portów na świat bez potrzeby (lab: [[Backlog]] i zasady [[Home]]).
- Wyłącz makra w Office z internetu.
- Przeglądarka: blokada reklam/śledzenia (uBlock Origin), DNS z filtrem (NextDNS/Quad9), okno prywatne do rzeczy „na chwilę".
- Sprawdzaj podpięte urządzenia i logi logowania (konta Google/Microsoft).

## Powiązane

- [[Zabezpieczenia_po_prostu]] · [[Komunikacja]] · [[Checklist_OPSEC]]
