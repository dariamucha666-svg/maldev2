---
title: "Automatyzacja vaultu"
date: 2026-08-15
tags: [obsidian, workflow]
status: active
---

# Automatyzacja

Co już jest spięte, a czego Sliver **nie** umie.

| Co | Jak | Status |
|----|-----|--------|
| Codzienny dziennik | Calendar + Daily Notes → `Daily/YYYY-MM-DD.md`, szablon `_Templates/Dziennik_Lab` | działa |
| Raporty pipeline | `export_pipeline_to_obsidian.sh` na końcu `pipeline.sh` → `Analizy/Raporty/` | działa |
| Zadania | wtyczka Tasks + [[Backlog]] + [[Kanban]] | działa |
| IOC | Dataview na [[Dashboard]] (`#ioc`) | działa |
| Logi terminala Linux | `script` w `.bashrc` na `.133` → `Logs/terminal_*.log` | działa |
| Logi Sliver | cron ogona `sliver.log` + **eksport sesji** | działa |
| Telegram → vault | bot: Inbox + Daily + `Dzienniki/Telegram/YYYY-MM-DD.md` | działa |
| Alerty RAT/stealer | `alert_roles.py` po `classify_roles` i po jobie dashboardu | działa |
| Screenshoty Windows | zadanie „Obsidian Screenshot” co 30 min (gdy sesja interaktywna) | `.57` |
| Git backup + sync | `git_autocommit.sh` co 15 min → bare `obsidian-vault.git`; Kali pull/push przez Obsidian Git | [[Git_Sync]] |
| Podgląd HTML | `export_vault_html.py` + Caddy `127.0.0.1:8081` | tunel SSH, nie :8080 |
| Transcript Windows | `Start-Transcript` w profilu PowerShell na `.57` | ręcznie na `.57` |

## Sliver → Obsidian

W konsoli **nie ma** `sessions --save` (flaga `--save` jest przy `generate`). Zamiast tego:

```bash
/root/obsidian-vault/Narzedzia/export_sliver_to_obsidian.sh
```

Wynik: [[sessions]] (`Projekty/Infrastruktura_C2/sessions.md`). Cron: `/etc/cron.d/obsidian-sliver-sessions` co godzinę.

Żywy widok na dashboardzie: `GET /api/sliver/sessions` (sliver-py, gRPC, tylko odczyt). Zakładka **Sliver** na https://dash.maskencrypt.eu/?tab=c2. Kod: `Narzedzia/sliver_sessions.py`.

Skrypt tylko **listuje** sesje / beacon'y / joby. Nie generuje implantów i nie dump'uje `credentials`.

## Telegram → Obsidian

Bot (nie ręczny `open(..., "a")` z `$(date)` w Pythonie):

- zwykła wiadomość → `Inbox/` + dopisek w `Dzienniki/Telegram/YYYY-MM-DD.md`
- `/dziennik` → `Daily/` + ten sam dziennik Telegram
- `/nowa` → wybrany folder + dziennik Telegram

## Podgląd w przeglądarce

`:8080` to **dashboard IoC** (`/var/www/ioc-dashboard`). Nie ruszamy go.

Vault HTML jest na **localhost:8081** (C2 / sesje nie idą na publiczny IP):

```bash
ssh -L 8081:127.0.0.1:8081 root@5.175.189.133
# potem: http://127.0.0.1:8081/_Dashboard/Dashboard.html
```

Bez Rusta / `obsidian-export` — na boxie nie ma cargo, dysk 78%.

## Screenshoty (.57)

```powershell
# na Windows lab
C:\Tools\Take-Screenshot.ps1
# albo z vaultu po skopiowaniu
```
