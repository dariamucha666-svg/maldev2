---
title: "OSINT — phishing / stealer w korpusie"
date: 2026-08-15
updated: 2026-08-15
tags: [osint, phishing, stealer, shaparak, nfc, chrome, pipeline]
status: active
---

# OSINT — phishing i stealery (publiczne źródła)

Tylko **wywiad na IOC z labu**. Hashe z [[Hunt_Phishing_Stealer]] + katalog. Bez łączenia do C2 próbek, bez detonacji, bez OSINT na osoby.

Powiązane: [[Hunt_Phishing_Stealer]] · [[1b3ceba6 Chrome bank stealer]] · [[4d0f7a96 Android SMS stealer avanegar]] · [[Klasyfikacja_Korpus]] · [[Dashboard_IOC]]

Źródła: MalwareBazaar API (2026-08-15), Hybrid Analysis (listing), publikacje IBM / Trend Micro / Zimperium / Group-IB / Bitsight / Cyble.

---

## Klastry w naszym zestawie

### A. Iran / Shaparak (płatności + SMS)

| Hash | Lab | MB first_seen | tagi MB | nazwa pliku | vendor |
|------|-----|---------------|---------|-------------|--------|
| `4d0f7a96…48a4` | stealer · Avanegar · `ir.avanegar.core` · „بانکداری ملت” | 2026-08-11 | `apk`, **SHAPARAK** | `app.apk` | RL `Android.Trojan.Generic` · Kaspersky Malware · FileScan MALICIOUS · Triage 6 |
| `fdbee288…e218` | phishing · FaWebView | 2026-08-09 | `apk`, **SHAPARAK** | **Divar.apk** | RL Generic · FileScan MALICIOUS · Triage 6 |

**Shaparak** = irańska sieć płatności kartowych (odpowiednik krajowego switcha). Tag na MB = próbka kręci się wokół ekosystemu IR payments, nie „dowolny APK”.

Avanegar: pakiet `.ir.`, przynęta Bank Mellat, uprawnienia SMS — klasyczny **SMS-OTP stealer** pod bankowość IR. Publiczny kontekst: kampanie IR mobile bankers (Zimperium 2023, deVixor 2026 — overlay JS na banki IR + SMS). To **nie** przypisanie do APT; to ten sam *typ* ofiary/ekosystemu.

Divar = popularny IR marketplace. Fałszywy APK o tej nazwie + tag SHAPARAK = **lure sklepu + płatność**.

MB: [4d0f7a96](https://bazaar.abuse.ch/sample/4d0f7a96a4859f47820ffa8e08b89ff7c7159fa3414a1cfe88db4949d65e48a4/) · Hybrid: [listing](https://hybrid-analysis.com/sample/4d0f7a96a4859f47820ffa8e08b89ff7c7159fa3414a1cfe88db4949d65e48a4)

### B. Para NFC-banker (ten sam wrzut)

| Hash | Lab | MB first_seen | reporter | rozmiar | RL |
|------|-----|---------------|----------|---------|-----|
| `a710209e…4778` | stealer · NewCartao · NFC · „Cartão Protegido” | **2026-08-04 13:30:21** | johnk3r / DE | 2 577 715 | `Android.Trojan.Ravartar` |
| `417406b7…4aaf` | phishing · WebView · dużo URL banków | **2026-08-04 13:30:35** | johnk3r / DE | 2 573 619 | `Android.Backdoor.GhostRAT` |

14 sekund różnicy, ten sam reporter, te same tagi MB (`apk, banker, nfc, signed`), prawie ten sam rozmiar. **Jedna paczka / jeden drop.**

Lab: obie mają te same hosty bankowe w endpointach (Sber, Citi, Caixa, Denizbank…). NewCartao = przynęta „ochrona karty” + NFC. 417406 = WebView z listą banków (phishing overlay / HTML).

Publiczny kontekst 2025–26 (nie twarde ID rodziny, tylko *klasa*):
- Hook v3 — overlay NFC + WebView na kartę (Zimperium)
- GodFather / AntiDot — WebView + NFC
- OverlayPhantom — HTML overlay na 180+ apkach bankowych (Cyble 2026)
- NGate / PhantomCard — tagi NFC na MalwareBazaar

MB: [a710209e](https://bazaar.abuse.ch/sample/a710209edb0b786d20eed3ac5c656546e40da8a07e9f771014434cf656934778/) · [417406b7](https://bazaar.abuse.ch/sample/417406b7e03f1c125d48996a24d0224a013d396d1c5e3e82ff79a34fe5d14aaf/)

### C. Chrome MV3 — Receita Federal (BR)

| Hash | Lab | MB |
|------|-----|-----|
| `1b3ceba6…153e` | stealer · webinject Bradesco / BB / Caixa · C2 w nocie próbki | **brak** na MalwareBazaar |

Nie wrzucone na MB (albo inny hash po rozpakowaniu). Publiczna *klasa* 2025–26: złośliwe rozszerzenia Chrome na banki LATAM — BlackStink (IBM), ParaSiteSnatcher (Trend Micro, BR), Rilide (Trustwave). Nasz werdykt z karty [[1b3ceba6 Chrome bank stealer]] zostaje: webinject, nie lab.

---

## Co z tego wynika do labu (detekcja)

1. **Dwa teatry:** IR (Shaparak / Mellat / Divar / SMS) vs LATAM/EU banker (NFC + WebView + lista banków + Chrome).
2. `417406` i `a710209e` traktować jako **jedną kampanię** przy dalszym RE (te same endpointy).
3. Filtry hunt już łapią `bank-host` + `nfc-card` + `sms` — zostawić, nie spłaszczać do „webview = phishing” (droppery też mają WebView).
4. Chrome `1b3ceba6` nie ma rekordu MB — do OSINT zostaje karta + ewentualnie VT ręcznie (nie submitować jeśli nie trzeba).

## Czego świadomie nie robię

- Nie wchodzę na C2 z notatek (`suahoje.com` itd.).
- Nie robię OSINT na osoby / reporterów poza aliasem MB.
- Nie buduję kitów phishing / stealer.

## Linki do dalszego czytania (klasa, nie IoC)

- IBM BlackStink (Chrome LATAM, 2025)
- Trend Micro ParaSiteSnatcher (Chrome BR)
- Zimperium Hook v3 / Iranian mobile bankers
- Group-IB Wonderland (SMS stealer + dropper)
- Bitsight ToxicPanda (WebView overlay)
