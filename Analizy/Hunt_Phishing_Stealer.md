---
title: "Hunt: phishing + stealer"
date: 2026-08-19
tags: [hunt, phishing, stealer, pipeline]
---

# Hunt — phishing i stealery (static)

Wygenerowano `2026-08-19 02:06 UTC` skryptem `hunt_phishing_stealer.py`. Tylko odczyt raportów / endpointów / katalogu. **Bez detonacji, bez budowy narzędzi.**

Trafienia: **19** próbek · hunt stealer **7** · hunt phishing **17**.

Powiązane: [[Klasyfikacja_Korpus]] · [[Role_Tags]] · [[Dashboard_IOC]] · [[1b3ceba6 Chrome bank stealer]]

## Tabela

| hash | rola | rodzina | hunt | markery |
|------|------|---------|------|---------|
| `cti_enrichme` | ? | — | stealer | nfc-card |
| `0fa3360a6a00` | dropper | Android.Dropper.Porntok | phishing | webview |
| `184ed09b7a83` | dropper | — | phishing | webview |
| `44f9d5c684fb` | dropper | Android.Dropper.ShellTemplate | phishing | webview |
| `a1416a250bf7` | dropper | Android.Dropper.ShellTemplate | phishing | webview |
| `f651876e9185` | dropper | Android.Dropper.CodoPreload | phishing | webview |
| `7d8b4974a693` | packed | — | phishing | webview |
| `2a46a2565d4f` | phishing | — | phishing | webview |
| `417406b7e03f` | phishing | Android.Phishing.WebView | phishing | webview |
| `7b44413023a9` | phishing | — | phishing | webview |
| `fdbee28882e9` | phishing | Android.Phishing.FaWebView | phishing | webview |
| `ff952f33bf27` | phishing | — | phishing | webview |
| `410a5cbaabc1` | rat | Android.Lab.MalwareAPK | phishing | webview,overlay |
| `100d18a17a30` | stealer | — | stealer+phishing | sms,webview |
| `1b3ceba6a829` | stealer | Chrome.Stealer.ReceitaFederal | stealer | catalog |
| `4d0f7a96a485` | stealer | Android.Stealer.Avanegar | stealer+phishing | sms,webview |
| `a710209edb0b` | stealer | Android.Stealer.NewCartao | stealer+phishing | nfc-card,webview |
| `bf70fa02c3a8` | stealer | — | stealer+phishing | sms,webview |
| `e5fa297d6ad6` | stealer | — | phishing | webview |

## Markery w korpusie

| marker | n próbek |
|--------|---------:|
| webview | 17 |
| sms | 3 |
| nfc-card | 2 |
| catalog | 1 |
| overlay | 1 |

## Jak tego używać

- Filtr dashboardu: rola `phishing` / `stealer`.
- Bot: `/wirus <hash>` na wierszu z tabeli.
- Nightly woła ten hunt po `classify_roles.py`.
- To jest **detekcja w labie**, nie przepis na atak.

