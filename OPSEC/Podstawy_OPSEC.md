---
title: "Podstawy OPSEC"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, podstawy, model-zagrozen]
status: active
category: podstawy
---

# Podstawy OPSEC

OPSEC = **Operational Security**. Proces chronienia informacji, które — złożone w całość —
mogą zdradzić Twoje plany, lokalizację, kontakty lub działania.

> OPSEC to nie „zniknąć z internetu". To **wiedzieć, co o Tobie da się zebrać i to ograniczyć**.

## 5 kroków OPSEC

1. **Zidentyfikuj, co chronisz (critical info).** Adres, numery telefonów, konta, relacje, harmonogram, infrastruktura.
2. **Zidentyfikuj zagrożenia.** Kto może chcieć tej informacji i po co (konto, firma, „znajomy", oszust).
3. **Znajdź luki.** Gdzie ta informacja wycieka (social media, zdjęcia, dane w wyciekach, metadane, DNS/WHOIS).
4. **Oceń ryzyko.** Prawdopodobieństwo × skutek. Nie wszystko musisz chronić tak samo.
5. **Zastosuj środki zaradcze i powtarzaj.** Zmień ustawienia, nawyki, narzędzia. Cyklicznie wracaj.

## Model zagrożeń (threat model)

Odpowiedz sobie na 3 pytania:
- **Co chronię?** (konta, pieniądze, prywatność, pracę)
- **Przed kim?** (masowy phishing, oszust, ex, pracodawca, boty skanujące)
- **Co się stanie, jak zawiedzie?** (strata pieniędzy, doxxing, wyciek)

Model decyduje, ile wysiłku wkładasz. Dla większości wystarczy [[Zabezpieczenia_po_prostu]]
(90% roboty, zero paranoi). Anonimowość na poziomie „państwo" to inna liga i inny wysiłek.

## Co najczęściej wycieka (i skąd)

| Co wycieka | Skąd | Jak ograniczyć |
|-----------|------|----------------|
| Hasła | wycieki baz, phishing, reuse | menedżer + unikalne hasła + 2FA |
| Adres / numer | publiczne profile, wycieki, meta zdjęć | minimalizacja, wyłącz geotag |
| Konta powiązane | reuse e-maila, logowanie social | osobne maile, sprawdzaj sesje |
| Metadane | zdjęcia, dokumenty, pliki | wycinaj EXIF, udostępniaj bez meta |
| Infrastruktura | DNS, WHOIS, IP | domeny przez proxy/Cloudflare ([[Narzedzia/Cloudflare_Konfiguracja]]) |

## Powiązane

- [[Zabezpieczenia_po_prostu]] — w pigułce
- [[Slady_i_prywatnosc]] — cyfrowy ślad i OSINT na sobie
- [[Wiedza/RedTeam/RedTeam_MOC|Red teaming]] — OPSEC operatora (infrastruktura, payloady, timing)
