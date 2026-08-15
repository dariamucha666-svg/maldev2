---
title: "GRAJ — gra edukacyjna (obrona przez myślenie jak atakujący)"
date: 2026-08-15
updated: 2026-08-15
tags: [gra, telegram, bot, edukacja, cyberbezpieczenstwo, soc]
status: active
category: narzedzia
---

# 🎮 GRAJ — gra edukacyjna w bocie

Gra dla studentów cyberbezpieczeństwa: uczą się **bronić**, myśląc jak atakujący.

Powiązane: [[Telegram_Obsidian_Bot]] · [[Threat_Intel_MOC]] · [[Phishing_Toolkit]]

## Jak grać

W bocie: komenda `/graj` (albo `/gra` / `/play`).

**Przepływ:**
```
GRAJ → poziom (🟢🟡🔴) → atak (historia) → metoda → ⚔️ ATAK → 🛡️ OBRONA → quiz
```

1. Wybierz **poziom trudności**.
2. Wybierz **atak** — bot pokazuje **historię** (scenariusz analityka SOC w Acme Corp).
3. Wybierz **metodę** — bot pokazuje **pełny atak** (kroki).
4. Naciśnij **🛡️ Zobacz obronę** — bot pokazuje **pełną obronę**.
5. Naciśnij **▶️ Quiz** — odpowiadasz na pytania, dostajesz wynik.

## Zawartość (3 poziomy · 8 ataków · 34 metody)

| Poziom | Ataki | Metody |
|--------|-------|--------|
| 🟢 **ŁATWY** | Phishing, Keylogger, Clipper | 14 |
| 🟡 **ŚREDNI** | Stealer (Lumma), Przejęcie Telegrama | 8 |
| 🔴 **TRUDNY** | AiTM (Evilginx), RAT (XWorm), Stealer C2 | 12 |

### Metody phishingu (6)
1. Klon strony (SET Credential Harvester)
2. E-mail z linkiem trackingowym (GoPhish)
3. Spear phishing (celowany)
4. Smishing (SMS phishing)
5. Vishing (phishing telefoniczny)
6. Pretekst (social engineering)

## Techniczne

- Kod: `/root/obsidian-telegram-bot/graj.py` (dane: poziomy, ataki, metody, pytania).
- Handler: `bot.py` → `cmd_graj` + `on_graj_cb` (callback flow `graj:*`).
- Treść oparta na realnych analizach z sesji ([[Threat_Intel_MOC]]).

## Rozbudowa

Aby dodać atak/metodę: dopisz wpis w `graj.py` (struktura: `story`, `methods[]` z `name/attack/defense/questions`).
