---
title: "Porównanie server.py (nowy TCP vs stary)"
date: 2026-08-15
type: raport
tags: [c2, analiza-kodu, server, comparison]
status: observation-only
---

# Porównanie `server.py` — wersja nowa vs stara

> **Pliki:**
> - Nowy: `/root/rat-c2/server.py` (TCP, 2 porty)
> - Stary: `/root/server.py` (TCP, 1 port)
>
> **Uwaga wstępna:** w zapytaniu wersja stara opisana była jako „FIFO", ale kod `/root/server.py` **nie używa FIFO/named pipe** — to prosty serwer TCP na porcie `4444` z pętlą opartą o `input()`.

## 1. Architektura

| Aspekt | Nowy (`rat-c2/server.py`) | Stary (`server.py`) |
|---|---|---|
| Porty | **9999** (agenci) + **9998** (CLI operator) | **4444** (pojedynczy) |
| Separacja kanałów | Tak — osobny kanał operatora i agentów | Nie — jeden kanał dla wszystkiego |
| Struktura | Funkcje + stan globalny (słowniki) | Klasa `C2Server` |
| Wątki | Wątek per agent + wątek per klient CLI | Wątek per agent |
| Stan sesji | `clients` (sid→socket), `client_info`, `command_responses`, `cli_connections` | `clients` (lista socketów) |
| Identyfikacja sesji | `S0001`, `S0002`… | brak (tylko adres) |

## 2. Sposób komunikacji

| Aspekt | Nowy | Stary |
|---|---|---|
| Framing | JSON **linia-po-linii** (`\n` jako delimiter) | Brak — surowe bajty |
| Typy wiadomości | `register`, `result`, payload `{cmd_id, command, args}` | Brak typów |
| Kierunek komend | CLI → serwer → agent (JSON) | Operator (konsola serwera) → agent (surowe) |
| Odbiór wyniku | Korelacja `cmd_id`, polecenie `getresult` | `client.recv()` w pętli, wypis na stdout |
| Transport | TCP, plaintext | TCP, plaintext |

**Kluczowa różnica:** wersja nowa ma ustrukturyzowany protokół JSON z korelacją komend/wyników. Wersja stara przesyła surowy tekst bez żadnego protokołu.

## 3. Obsługa komend

| Aspekt | Nowy | Stary |
|---|---|---|
| Parser komend | `process_command()`: `list`, `send`, `getresult`, `help`, `exit` | Brak parsera |
| Walidacja | Minimalna (sprawdzanie liczby argumentów) | Brak |
| Śledzenie wyników | `command_responses[sid][cmd_id]` | Brak |
| Broadcast do CLI | Tak (`broadcast`/`send_to_cli`) | Nie dotyczy |

**Wada wersji starej:** komendy nie pochodzą z sieci — `handle_client()` wywołuje `input()`, które czyta ze **stdin serwera** (konsola lokalna), a nie z gniazda. W efekcie każdy wątek agenta konkuruje o wspólne stdin (race condition), a zdalne sterowanie nie działa tak, jak sugeruje architektura.

## 4. Analiza bezpieczeństwa

### 4.1 Autoryzacja i uwierzytelnianie
- **Obie wersje: BRAK uwierzytelniania.** Każdy, kto osiągnie port, może się podłączyć.
- Nowy: nieautoryzowany klient CLI na `0.0.0.0:9998` może wykonać `list`/`send`/`getresult` — czyli **wyliczyć sesje i wysyłać komendy do agentów**.
- Nowy: nieautoryzowany klient na `9999` może zarejestrować się jako fałszywy agent.

### 4.2 Szyfrowanie
- **Obie wersje: plaintext TCP, bez TLS.** JSON (nowy) i surowy tekst (stary) są czytelne w ruchu sieciowym.

### 4.3 Powierzchnia ataku
- Nowy: **większa** — dwa porty wystawione na `0.0.0.0`, w tym zdalnie sterowalny CLI.
- Stary: mniejsza *de facto*, bo wejście komend jest lokalne (konsola), ale to wynik błędu (`input()`), nie zamierzonej kontroli.

### 4.4 Poprawność / niezawodność
- Nowy: lepsza struktura, ale **brak blokad** wokół współdzielonych słowników (wątki mutują `clients`/`client_info`/`command_responses`) — możliwe race conditions; **ponowne użycie SID** po rozłączeniu (`len(clients)+1`).
- Stary: race na wspólnym stdin, brak framingu, łamliwe parsowanie.

## 5. Wniosek — która wersja jest „bezpieczniejsza"

**Żadna z wersji nie jest bezpieczna** w sensie bezpieczeństwa informacji:

- **Nowa** jest **lepiej zaprojektowana** (protokół JSON, separacja kanałów, korelacja wyników), ale **mniej bezpieczna ekspozycyjnie**: publikuje nieuwierzytelniony, zdalnie sterowalny CLI na `0.0.0.0:9998`, przez który osoba trzecia może wyliczać sesje i sterować agentami. Brak TLS i autoryzacji.
- **Stara** jest **architektonicznie gorsza i w praktyce zepsuta** (komendy z `input()` = stdin lokalne, nie sieć; brak framingu i typów). Jej mniejsza zdalna sterowalność wynika z błędu, nie z zabezpieczenia.

Jeśli „bezpieczniejsza" = „mniejsze ryzyko zdalnego przejęcia kontroli", to stara wersja jest *przypadkowo* mniej narażona (brak sieciowego CLI), ale to nie jest świadome zabezpieczenie. Jeśli „bezpieczniejsza" = „lepsza inżynieria i mniej błędów", wygrywa nowa — pod warunkiem dodania **TLS, uwierzytelniania i blokad wątków**, których obecnie brakuje w obu.

**Rekomendowane minimum bezpieczeństwa (dla wersji nowej):**
1. TLS na obu portach (9998/9999).
2. Uwierzytelnianie klienta CLI (token/klucz) i wzajemne uwierzytelnienie agentów.
3. Wiązanie portu CLI do `127.0.0.1` zamiast `0.0.0.0` (jeśli operator jest lokalny).
4. Blokady (`threading.Lock`) dla współdzielonych słowników.
5. Walidacja i allow-lista nazw komend w `process_command()`.
