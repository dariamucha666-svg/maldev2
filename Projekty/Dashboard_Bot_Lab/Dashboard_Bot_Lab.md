---
title: "Dashboard + bot + alerty"
date: 2026-08-15
updated: 2026-08-15
tags: [projekt]
status: completed
priority: high
category: lab
---

# Dashboard, bot Telegram, alerty

Notatka zbiorcza z sesji 2026-08-15. Szczegóły narzędzi: [[Dashboard_IOC]] · [[Telegram_Obsidian_Bot]] · [[Automatyzacja]] · [[Sliver_C2]].

## Cel

Jeden widok labu na telefonie + bot, który nie tylko pisze do vaultu, ale też **ściąga / klasyfikuje próbki** i **sam alarmuje** przy nowym RAT/stealerze.

## Co stoi

| Co | Gdzie |
|----|--------|
| Publiczny UI | https://dash.maskencrypt.eu/ |
| Serwis | `ioc-dashboard.service` → `Narzedzia/serve_dashboard.py` (venv `/opt/ioc-dashboard/venv`) |
| Bot | `obsidian-telegram-bot.service` → `/root/obsidian-telegram-bot/bot.py` |
| Alerty | `Narzedzia/alert_roles.py` po `classify_roles` i po jobie dashboardu |
| Stan alertów | `/root/obsidian-telegram-bot/state/alerted.json` (poza gitem) |

## Dashboard (UI)

- Pulpit: liczba próbek, RAT, stealer, żywe sesje Sliver.
- Pasek składu korpusu + oś czasu z kolorami ról (`history.json`).
- Karty w siatce, **Kopiuj** hash, IoC jako chipy, `/` skacze do szukania.
- Ikona XMask: `/var/www/ioc-dashboard/icon.png`.
- Hunt dwufazowy: lab (~2 ms), potem MalwareBazaar.
- `GET /api/boot` — jeden request (iocs + catalog + history + liczniki Sliver), gzip.
- Zakładka Sliver: `GET /api/sliver/sessions` (gRPC sliver-py, tylko odczyt).

## Bot

| Komenda | Działanie |
|---------|-----------|
| `/dashboard` `/status` | Lab + liczby (lokalny `iocs.json` / `/api/boot`) |
| `/wirus` | Karta + przyciski Pobierz / Klasyfikuj |
| `/pobierz <hash>` | `POST /api/job` `add` — jak przycisk na stronie |
| `/klasyfikuj <hash>` | Pokazuje rolę albo odpala pipeline |
| `/alerty` | Ostatnie RAT/stealer z pliku stanu |
| `/xmask` `/laik` `/nowa` … | jak wcześniej |

Token i chat id **poza** vaultem (`.env`, `.owner_id`).

## Alerty RAT / stealer

1. `pipeline.sh` po `classify_roles.py` woła `alert_roles.py`.
2. To samo po udanej analizie z dashboardu (`serve_dashboard.py`).
3. Wysyłka tylko gdy SHA256 **nie** jest w `alerted.json`.
4. 2026-08-15: **seed 7** (5 RAT, 2 stealer) + wiadomość „alerty włączone”. Starych nie spamuje.

Role: `rat`, `stealer` (`ALERT_ROLES` w env, gdy chcesz dodać `backdoor`).

```bash
python3 /root/obsidian-vault/Narzedzia/alert_roles.py --dry-run
python3 /root/obsidian-vault/Narzedzia/alert_roles.py --seed --hello
```

## Werdykt

Działa na `.133`. Nightly / `/klasyfikuj` nowej próbki RAT|stealer ma przyjść na Telegram sam.

## Dalej (nie zrobione)

- Paczka IoC (JSON/CSV z filtra).
- Porównanie dwóch hashy.
- Sigma.
- Kalendarz nightly.

## Powiązane

- [[Dashboard]]
- [[Dashboard_IOC]]
- [[Telegram_Obsidian_Bot]]
- [[Pipeline_Analizy]]
- [[Role_Tags]]
- [[Daily/2026-08-15]]
