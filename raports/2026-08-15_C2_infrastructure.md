---
title: "Infrastruktura C2 — dokumentacja techniczna"
date: 2026-08-15
type: raport
tags: [c2, infrastructure, forensics, ioc]
status: observation-only
---

# Infrastruktura C2 — dokumentacja techniczna (2026-08-15)

> **Charakter dokumentu:** opis **zaobserwowanej** infrastruktury (wyłącznie odczyt: `netstat`, `ps`, `screen -ls`, logi). Nie jest to instrukcja uruchamiania ani obsługi — dane pochodzą z obserwacji stanu systemu w dniu 2026-08-15.

## 1. Architektura

```
[ Agent .57 ] ──TCP 9999 (beacon/JSON)──► [ Serwer C2 .133 (VPS) ]
                                              │ 9999 → agenci (wyniki)
                                              │ 9998 → klienci CLI (operator)
                                              ▼
                                          [ CLI (loopback 127.0.0.1:9998) ]
```

| Rola | Host | Adres/port | Proces |
|------|------|-----------|--------|
| Serwer C2 | `.133` (ten VPS) | `0.0.0.0:9999` (agenci), `0.0.0.0:9998` (CLI) | `python3 -u server.py` (PID 637125) |
| Agent zdalny | `.57` | `5.175.189.57:53791` → `5.175.189.133:9999` (ESTABLISHED) | agent (endpoint zdalny) |
| Agent lokalny | `.133` (loopback) | `127.0.0.1` → `:9999` | `/tmp/pil_env/bin/python -u agent.py` (PID 637158) |
| Klient CLI | `.133` (loopback) | `127.0.0.1` → `:9998` | klient CLI (krótkie połączenia) |

- Serwer przyjmuje dwa kanały: **9999** dla agentów (beacon + wyniki) oraz **9998** dla klienta operatorskiego (CLI).
- W logach zaobserwowano sesje agentów `S0002`, `S0003` (rejestracje z `127.0.0.1`) oraz połączenie zdalne z `5.175.189.57`.

## 2. Porty i protokoły

| Port | Protokół | Interfejs | Rola | Właściciel (PID) |
|------|----------|-----------|------|------------------|
| 9999 | TCP | 0.0.0.0 | Agent beacon / wyniki | `python3` 637125 (`server.py`) |
| 9998 | TCP | 0.0.0.0 | CLI operatorskie | `python3` 637125 (`server.py`) |
| 443 | TCP | 127.0.0.1 | *odrębny* `sliver-server` | PID 445365 |
| 8443 | TCP | ::: | *odrębny* `sliver-server` | PID 445365 |
| 31337 | TCP | ::: | *odrębny* `sliver-server` | PID 445365 |

> Protokół C2: **JSON po surowym TCP**. Potwierdzone wpisem w `server.log`: `Zły JSON od S0003: list` — agent/klient wysyła tekst `list` niebędący poprawnym JSON, serwer go odrzuca. Wyniki przesyłane z powrotem jako pary `S<ID>#<numer>` (np. `Odebrano wynik dla S0002#942253`).

## 3. Kluczowe pliki

Katalog roboczy serwera i agenta: **`/root/rat-c2/`**

| Plik | Rozmiar | Rola |
|------|---------|------|
| `server.py` | 8665 B | Serwer C2 (nasłuch 9998/9999) |
| `agent.py` | 4319 B | Agent (beacon, wykonuje komendy: `screenshot` itd.) |
| `run_demo.sh` | 1947 B | Skrypt startowy/demo |
| `server.log` | 1352 B | Log serwera (CLI/agenci) |
| `server_run.log` | 238 B | Log nieudanego startu (`Address already in use`) |
| `agent.log` | 265 B | Log agenta (rejestracja, `screenshot`) |
| `agent_run.log` | 327 B | Log agenta (run #2, dwa `screenshot`) |
| `server.py.bak.20260815_054724` | 5198 B | Kopia zapasowa `server.py` |
| `server.py.save` | 4927 B | Kopia zapasowa `server.py` |
| `out/` | — | Katalog wyjściowy (pliki `screenshot_*.png`) |
| `__pycache__/` | — | Skompilowane moduły Pythona |

> **Uwaga:** pliku `c2cli.py` **nie zaobserwowano** w `/root/rat-c2/`. Komponent CLI widoczny był jedynie jako krótkie połączenia `127.0.0.1 → :9998` (logi `Nowy klient CLI` / `Klient CLI rozłączony`). Nazwa pliku klienta nie została potwierdzona obserwacją.

## 4. Sposób uruchamiania (obserwacja)

Obserwowana hierarchia procesów (z `ps`):

```
637122  SCREEN -dmS c2 bash -c python3 -u server.py > /root/rat-c2/server.log 2>&1
 └─ 637124  bash -c python3 -u server.py > /root/rat-c2/server.log 2>&1
      └─ 637125  python3 -u server.py
```

- Serwer uruchomiony w sesji **GNU screen** o nazwie **`c2`** (detached): `screen -dmS c2 …`.
- Interpretator: `/usr/bin/python3.12`, z flagą `-u` (unbuffered), stdout/stderr przekierowane do `server.log`.
- Agent lokalny uruchomiony z osobnego środowiska: `/tmp/pil_env/bin/python -u agent.py` (PID 637158, PPID 1 — odłączony od terminala).
- `server_run.log` zawiera ślad wcześniejszej próby startu zakończonej `OSError: [Errno 98] Address already in use`.

## 5. Sposób komunikacji

- **Transport:** TCP (raw socket), dwukierunkowy.
- **Format:** JSON (klient→serwer komendy; serwer→agent polecenia; agent→serwer wyniki).
- **Identyfikacja sesji:** agenci otrzymują ID `S<NNNN>`; wyniki korelowane jako `S<ID>#<seq>`.
- **Obserwowane komendy/zdarzenia (z logów):**
  - rejestracja agenta: `[agent] zarejestrowany jako vserver959630 / root`
  - `screenshot` → zapis `screenshot_<epoch_ms>.png` w `out/`
  - `list` → `Zły JSON od S0003: list` (niezgodność formatu)
- **Komendy obecne w artefaktach/łańcuchach** (do detekcji): `screenshot`, `net_user_add`, `keylog_start`, `reg_set_value`.

## 6. Obserwowane IoC (podsumowanie)

| Typ | Wartość |
|-----|---------|
| Port nasłuchu C2 | `9998`, `9999` |
| Proces serwera | `python3 -u server.py` (PID 637125) |
| Proces agenta lokalnego | `/tmp/pil_env/bin/python -u agent.py` (PID 637158) |
| Sesja screen | `c2` (detached, PID 637122) |
| Zdalny agent | `5.175.189.57:53791 → 5.175.189.133:9999` |
| Host agenta lokalnego | `vserver959630` |
| Ścieżka C2 | `/root/rat-c2/` |
| Odnośnik do reguł detekcyjnych | `[[C2_detection_rules_sigma_yara_suricata]]` |
