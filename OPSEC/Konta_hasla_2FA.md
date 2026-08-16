---
title: "Konta, hasła i 2FA"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, konta, hasla, 2fa]
status: active
category: konta
---

# Konta, hasła i 2FA

Najczęstszy wektor wejścia: skradzione/wyciekłe hasło + brak 2FA. To naprawia większość włamań na konta.

## Hasła

- **Menedżer haseł** (Bitwarden / 1Password / KeePassXC). Jedno mocne hasło główne (passphrase, 5+ słów).
- **Każde konto = inne hasło.** Reuse = jeden wyciek i kaskada.
- **Nie odpowiadaj na „pytania bezpieczeństwa" prawdą.** Traktuj jak drugie hasło (zapisz w menedżerze).
- **Włącz alerty o wyciekach** (HaveIBeenPwned; menedżer sam sprawdza).

## 2FA / MFA

| Metoda | Siła | Uwagi |
|--------|------|-------|
| SMS | słaba | podatny na SIM swap i przechwycenie; tylko gdy nie ma nic lepszego |
| Aplikacja TOTP (Aegis, 2FAS, Google Authenticator) | dobra | offline, darmowa |
| Klucz sprzętowy (YubiKey) | najlepsza | odporny na phishing, do kluczowych kont |
| Passkey | bardzo dobra | odporny na phishing, wygodny |

- Włącz 2FA **najpierw na mailu** (odzyskiwanie innych kont idzie przez mail).
- **Kody zapasowe** (backup codes) zapisz offline (papier / zaszyfrowany plik), nie w chmurze głównego maila.

## Konta — porządek

- **Osobne maile wg roli:** prywatny, finanse, rejestracje/śmieci, testy/lab. Logowanie social („Zaloguj przez Google") ograniczaj — jedno konto Google trzyma klucze do wielu.
- **Sprawdzaj aktywne sesje** i „wyloguj z innych urządzeń" (Google, Meta, bank, GitHub).
- **Usuwaj martwe konta** — stare konto bez 2FA to tykająca bomba.
- **Nie używaj konta z labu do banku/maila głównego** (patrz [[XMask/opsec.exe/02_Konta|XMask #2 Konta]]).

## Po wycieku / podejrzeniu

1. Zmień hasło (z czystego urządzenia).
2. Włącz / odśwież 2FA.
3. Wyloguj wszystkie sesje.
4. Sprawdź reguły przekierowań w mailu i podpięte aplikacje.
5. Zmień też hasła tam, gdzie używałeś tego samego (dlatego reuse to zło).

## Powiązane

- [[Zabezpieczenia_po_prostu]] · [[Slady_i_prywatnosc]] · [[Checklist_OPSEC]]
