---
tags:
  - dashboard
  - ioc
  - yara
  - pipeline
updated: 2026-08-15
---

# Dashboard IOC

Powiązane: [[Pipeline_Analizy]] · [[IOC_Backdoor]] · [[Dashboard]]

Centralny widok IoC z raportów pipeline. **Sigma** — jeszcze nie ma (do dodania).

## Pliki

| | |
|--|--|
| UI | `/root/android-pipeline/web/dashboard.html` |
| Serwer | `/root/android-pipeline/web/serve.py` |
| API | `GET /api/iocs` i `GET /iocs.json` |
| Dane | `/root/samples/reports/iocs.json` (kopia w `web/`) |

## Publiczny widok (ścieżka C)

| | |
|--|--|
| Katalog | `/var/www/ioc-dashboard/` |
| Pliki | `index.html` + `iocs.json` (kopia z reports) |
| Serwer | `python3 -m http.server 8080` (bind `0.0.0.0`) |
| URL | **https://dash.maskencrypt.eu/** (Telegram + telefon) |
| Fallback | http://5.175.189.133:8080 |
| UFW | `8080/tcp` ALLOW (`ioc-dashboard`) — **publiczny** |
| PID | `/var/www/ioc-dashboard/server.pid` |
| Log | `/var/www/ioc-dashboard/server.log` |

Sprawdzone z Kali: HTML 200, `iocs.json` 200, 15 próbek / 3 reguły.

Po nowym `pipeline.sh` odśwież dane:

```bash
cp -f /root/samples/reports/iocs.json /var/www/ioc-dashboard/iocs.json
```

Zatrzymanie:

```bash
kill $(cat /var/www/ioc-dashboard/server.pid)
# ufw delete allow 8080/tcp   # jeśli nie ma zostać otwarte
```

Lokalny (niepubliczny) serwer nadal: `127.0.0.1:8766` (`web/serve.py`).

## Co pokazuje karta

- **nazwa wirusa** + rodzina (z `catalog.json`, nie ginie przy nowym `pipeline.sh`)
- **Co to za wirus** / **Jak się bronić**
- hash SHA256
- stringi IoC (zielone)
- YARA, data, nazwa pliku
- filtr po nazwie rodziny / haśle / stringu / `pe` / `apk`

Katalog opisów: `/root/android-pipeline/web/catalog.json` (kopia w `/var/www/ioc-dashboard/catalog.json` i w bocie `virus_catalog.json`). Pipeline nadpisuje `iocs.json`, potem `classify_roles.py` dopisuje `role` + `tags`. [[Role_Tags]]

Bot: `/dashboard`, `/wirus <hash>`, posty: `/xmask` ([[Telegram_Obsidian_Bot]]).

## Stan po runie 22:15 UTC

| | |
|--|--|
| Próbki w `iocs.json` | **15** |
| Reguły YARA | **3** (`Auto_PE_178cb931` + 2× shelltemplate APK) |
| curl `/` | HTTP 200, 5430 B |
| curl `/api/iocs` | HTTP 200 |

PE `178cb931` ma 5 stringów: `LogonUserW`, `NetUserAdd`, `NetUserDel`, `NetShareAdd`, `NetShareDel`.

## Do zrobienia

- Generator **Sigma** (SIEM) — brak
- Tune filtrów APK (URL-e tylko z dekompilacji nie matchują `raw/*.apk`)
