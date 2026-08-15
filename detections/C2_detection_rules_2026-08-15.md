# Reguły detekcyjne C2 — 2026-08-15

> **Zakres:** detekcja zaobserwowanej infrastruktury C2 (serwer `.133`, porty 9999/9998, JSON po TCP, brak uwierzytelniania).
> **Status:** experimental.
>
> ⚠️ **Ważne korekty zgodności z faktami (na podstawie analizy kodu):**
> - Faktyczny `agent.py` implementuje **wyłącznie** komendę `screenshot` (agent Linux/X11, `mss`/`xwd`). Ciągi `net_user_add`, `reg_set_value`, `keylog_start` **nie występują** w obserwowanych plikach — pojawiały się wcześniej jedynie jako heurystyki.
> - Port **9998** = kanał CLI (operator). Port **9999** = kanał agentów. Agent łączy się na 9999.
> - Reguły YARA poniżej oparto o **rzeczywiste** ciągi z kodu; sekcja artefaktów odróżnia „obserwowane" od „hipotetycznych" (nieobecnych w kodzie).

---

## 1. Suricata — nieautoryzowane połączenia na port 9998

> Legalny operator łączy się lokalnie (loopback). Alertujemy na każde źródło inne niż pętla zwrotna.

```suricata
# 1.1 Wyjątek: legalny operator z loopback
pass tcp 127.0.0.0/8 any -> $HOME_NET 9998 (msg:"C2 CLI - legal loopback operator"; flow:to_server,established; sid:2026081500; rev:1;)

# 1.2 Alert: połączenie na port 9998 z zewnętrznego źródła
alert tcp $EXTERNAL_NET any -> $HOME_NET 9998 (msg:"Unauthorized C2 CLI connection to port 9998 (external source)"; flow:to_server,established; classtype:attempted-admin; sid:2026081501; rev:1;)

# 1.3 Alert: JSON payload z komendą operatorską na 9998
alert tcp $EXTERNAL_NET any -> $HOME_NET 9998 (msg:"C2 CLI command via JSON on port 9998"; flow:to_server,established; content:"\"cmd\""; nocase; content:"\"send\""; nocase; distance:0; within:128; classtype:attempted-admin; sid:2026081502; rev:1;)
```

**Uwaga:** Suricata nie obsługuje negacji źródła w jednej sygnaturze wprost; standardowo używa się zmiennej `$EXTERNAL_NET` + reguły `pass` dla `127.0.0.0/8` (jak wyżej). Jeśli `$HOME_NET` obejmuje loopback, ustaw poprawnie `$EXTERNAL_NET`, by nie dopasowywać `127.0.0.1`.

---

## 2. Sigma — połączenie wychodzące na 9998 (EventID 5156)

```yaml
title: Outbound Connection to C2 CLI Port 9998 from Python
id: 4a1c7d2e-9b3f-4e6a-8c0d-1f2a3b4c5d01
status: experimental
description: |
  Wykrywa zaakceptowane połączenie wychodzące (WFP, EventID 5156) z procesu
  Python na port 9998 (kanał CLI serwera C2).
author: SOC
date: 2026/08/15
logsource:
  product: windows
  category: network_connection
  service: security
detection:
  selection:
    EventID: 5156
    DestinationPort: 9998
    Application|contains:
      - 'python'
      - 'python3'
      - 'python.exe'
  condition: selection
falsepositives:
  - Legitne skrypty Python używające portu 9998 (rzadkie)
level: high
tags:
  - attack.command_and_control
  - attack.t1571
```

**Uwaga:** pole procesu w zdarzeniu 5156 to `Application` (pełna ścieżka). Jeśli Windows nie loguje nazwy procesu (zależnie od konfiguracji audytu), użyj wariantu bez filtra `Application`, opartego wyłącznie o `DestinationPort: 9998`.

---

## 3. YARA — `server.py` i `agent.py`

> Oparte o **rzeczywiste** ciągi z obserwowanych plików (analiza 2026-08-15).

### 3.1 `C2_Agent_py` (faktyczne ciągi: `screenshot`, `xwd`, `mss`)

```yara
rule C2_Agent_py
{
    meta:
        description = "Detects observed C2 agent.py (Linux/X11 screenshot agent)"
        author = "SOC"
        date = "2026-08-15"
        reference = "internal"

    strings:
        $s_screenshot = "screenshot"        ascii wide
        $s_fn         = "capture_screenshot" ascii wide
        $s_xwd        = "xwd"               ascii
        $s_mss        = "mss"               ascii
        $s_b64        = "data_b64"          ascii
        $s_out        = "/root/rat-c2/out"  ascii
        $s_display    = "DISPLAY"           ascii
        $s_register   = "\"register\""      ascii

    condition:
        filesize < 200KB and
        (uint32(0) != 0x4D5A9000) and
        $s_screenshot and $s_fn and
        (2 of ($s_xwd, $s_mss, $s_b64, $s_out, $s_display, $s_register))
}
```

### 3.2 `C2_Server_py` (faktyczne ciągi: `list`, `send`, `getresult`, `cmd_id`)

```yara
rule C2_Server_py
{
    meta:
        description = "Detects observed C2 server.py (JSON/TCP, dual-port)"
        author = "SOC"
        date = "2026-08-15"
        reference = "internal"

    strings:
        $s_list       = "Aktywne sesje"      ascii wide
        $s_getresult  = "getresult"          ascii wide
        $s_send       = "\"send\""           ascii
        $s_cmd_id     = "cmd_id"             ascii
        $s_cli_conn   = "cli_connections"    ascii
        $s_cmd_resp   = "command_responses"  ascii
        $s_port9      = "9999"               ascii
        $s_port8      = "9998"               ascii

    condition:
        filesize < 300KB and
        (uint32(0) != 0x4D5A9000) and
        $s_getresult and $s_cmd_id and
        (1 of ($s_cli_conn, $s_cmd_resp)) and
        (1 of ($s_port9, $s_port8))
}
```

> **Nie zaobserwowano** w kodzie ciągów: `net_user_add`, `reg_set_value`, `keylog_start`. Nie dodaję ich do reguł jako ciągów „faktycznych" — reguła z nimi dałaby fałszywy obraz możliwości próbki. (Jeśli w innej wersji agenta te komendy się pojawią, należy dopisać osobne `strings`.)

---

## 4. Artefakty po wykonaniu komend

### 4.1 `screenshot` — **faktycznie zaimplementowana** (agent Linux/X11)

| Miejsce | Artefakt |
|---|---|
| **Agent (Linux)** | tworzy katalog `/root/rat-c2/out/`; zapis `screenshot_<epoch_ms>.png` (przez `mss`) lub `.xwd` (fallback `xwd -root -silent -display :10.0`); usunięcie `.xwd`, jeśli PNG się powiódł |
| **Agent — proces** | w fallbacku uruchomienie procesu potomnego `xwd` (widoczne w `ps`, auditd `execve`) |
| **Agent — środowisko** | nadpisanie zmiennej `DISPLAY` (domyślnie `:10.0`) |
| **Sieć** | obraz base64 w polu `data_b64` → wysyłka do serwera na TCP **9999** (duży payload) |
| **Agent — log** | `[agent] wykonano 'screenshot' -> screenshot_<ts>.png` (stdout → `agent*.log`) |
| **Serwer — log** | `Odebrano wynik dla S<ID>#<cmd_id>` (stdout → `server.log`); wynik trzymany **w pamięci** (`command_responses`), nie persistowany na dysk |

### 4.2 `net_user_add`, `reg_set_value`, `keylog` — **nieobecne w obserwowanym kodzie**

> Te komendy **nie są zaimplementowane** w `agent.py` (ani w `server.py`). Wszystkie nieznane komendy trafiają do fallbacku `"unknown command"` i **nie wywołują żadnej zmiany systemowej** (brak artefaktów). Poniższe to wyłącznie **hipotetyczne** artefakty, gdyby takie komendy istniały (np. w innej wersji agenta):

| Komenda | Hipotetyczny artefakt (Windows) | Hipotetyczny artefakt (Linux/serwer) |
|---|---|---|
| `net_user_add` | konto w SAM; Security 4720/4722/4732; proces `net.exe` (4688, Sysmon 1) | `useradd` → wpis w `/etc/passwd`/`/etc/shadow`, log auth (`/var/log/auth.log`) |
| `reg_set_value` | wartość rejestru; Security 4657; Sysmon 12/13 | nie dotyczy (brak rejestru; analog: pliki autostartu) |
| `keylog` | plik z klawiszami; hook DLL (Sysmon 7); Run key (Sysmon 13) | plik keylog; proces z `SetWindowsHookEx` nie dotyczy; analog: `input`/X11 grab |

---

## 5. Podsumowanie

- Reguły Suricata/Sigma/YARA oparto o **zaobserwowany** stan (porty 9998/9999, JSON, brak auth, rzeczywiste ciągi kodu).
- Faktyczna powierzchnia artefaktów ogranicza się do **`screenshot` + eksfiltracja PNG/XWD na 9999**.
- Komendy `net_user_add`/`reg_set_value`/`keylog` w tej próbce **nie istnieją** — sekcja 4.2 ma charakter wyłącznie hipotetyczny.
