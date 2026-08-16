---
title: "deepseek-vps-3"
date: 2026-08-16
tags: [chatlog, czat, goose]
source: Goose
session: 20260815_22
cwd: "/root"
messages: 129
tool_calls: 124
status: archived
---

# deepseek-vps-3

> Zapis czatu **Goose** · sesja '20260815_22' · '/root' · wygenerowano 2026-08-16

## Analiza

| Pole | Wartość |
|------|---------|
| Cel | Kontynuacja po zaciętej sesji Goose. NIE wznawiaj starych sesji (deepseek-vps / deepseek-vps-2). To nowy czat. Nie powtarzaj ukończonej roboty. |
| Wiadomości użytkownika | 4 |
| Odpowiedzi asystenta | 1 |
| Akcji narzędziowych | 124 |
| Narzędzia | 'tool'×62, 'result'×62 |
| Pliki | '/etc/cron.d/nightly-pipeline' · '/root/.mb_api_key' · '/root/obsidian-telegram-bot/bot.py' · '/root/obsidian-vault' · '/root/obsidian-vault/Analizy/Threat_Digest/2026-08-15.md' · '/root/obsidian-vault/Daily/2026-08-15.md' · '/root/obsidian-vault/Narzedzia/log_to_obsidian.sh' · '/root/threat_digest.log' · '/root/threat_digest.py' · '/usr/bin/python3' · '2026-08-15.md' · 'Aktualizacje.md' · 'Analizy/Threat_Digest/2026-08-15.md' · 'Analizy/Threat_Digest/YYYY-MM-DD.md' · 'Analizy/Threat_Intel_MOC.md' · 'Daily/2026-08-15.md' · 'Daily/YYYY-MM-DD.md' · 'Feed_CISA_KEV.md' · 'Feed_MalwareBazaar.md' · 'Feed_ThreatFox.md' |
| Hosty | '0x00sec.org' · 'alienvault.com' · 'aliyun.com' · 'feedburner.com' · 'github.com' · 'google.com' · 'googleapis.com' · 'habr.com' · 'krebsonsecurity.com' · 'microsoft.com' · 'packetstormsecurity.com' · 'paloaltonetworks.com' |

## Wniosek (ostatnia odpowiedź asystenta)

Zrobione. Krótki status:

## Threat digest — NVD dodany ✅

**Co zmieniłem w `/root/threat_digest.py`:**
- Nowe źródło **NVD** (`services.nvd.nist.gov/rest/json/cves/2.0/`), ostatnie 2 dni publikacji, do 10 CVE.
- Każde CVE ma metadane: **CVSS (wynik + severity)** + **typ CWE** (mapa `CWE_LABELS` → np. `Path Traversal`, `SQL Injection`, `SSRF`; nieznane kody zostają surowe).
- Ta sama perspektywa `🎯 Hakerzy:` co reszta — interpretacja z opisu + CWE.
- Bonus: poprawka regex `rce` → `\brce\b`, bo fałszywie łapał „resource/source” (np. middleware autoryzacyjny Cedar był błędnie oznaczany jako RCE).

**Efekt w notatce** (`Analizy/Threat_Digest/2026-08-15.md`):
- Sekcja `## Najnowsze CVE (NVD)` z liniami typu:
  `**CVE-2026-16770** · CVSS **9.8 (CRITICAL)** · Argument Injection → 🎯 Hakerzy: RCE…`
- Źródła w stopce i nagłówku zaktualizowane o NVD.

**Commity (vault, clean):**
- `9f27f28` — Threat digest: źródło NVD + regen notatki
- `c72c012` — Log: NVD w threat digest

**Czego NIE ruszałem (zgodnie z ustaleniami):**
- XSS.is / Exploit.in / BreachForums — bez konta, zostają pominięte.
- Bot Telegram / GitHub origin — bez Twojego URL albo `gh`.
- Notatka zalogowana w Daily (`log_to_obsidian.sh`).

Czekam na dalsze instrukcje.

## Pełny zapis

### 👤 Użytkownik — 2026-08-15T17:29:37Z

Kontynuacja po zaciętej sesji Goose. NIE wznawiaj starych sesji (deepseek-vps / deepseek-vps-2). To nowy czat. Nie powtarzaj ukończonej roboty.

# Stan (2026-08-15 ~17:17 UTC)

## Threat digest — GŁÓWNE OTWARTE
Pliki: `/root/threat_digest.py`, notatka `obsidian-vault/Analizy/Threat_Digest/2026-08-15.md`, cron 20:00.

GOTOWE:
- 26 kątów ataku (ATTACK_ANGLES)
- interpret() z linią „🎯 Hakerzy:” przy każdym newsie
- Exploit-DB RSS (publiczne PoC)
- tłumaczenie PL
- commit d4a5861

OTWARTE (zrób to teraz):
1. Dodaj źródło NVD (CVE feed) z metadanymi CVSS/typ i tą samą perspektywą „🎯 Hakerzy:”.
2. Przegeneruj dzisiejszą notatkę i commit do vaultu.
3. NIE loguj się na XSS.is / Exploit.in / BreachForums — brak konta, zostaw pominięte.

## Bot Telegram — kontekst
GOTOWE: folder Wiedza/, `/wiedza`, `/zagrozenia`, git lokalny `/root/obsidian-telegram-bot` (2b9b0ca), bare `/root/obsidian-telegram-bot.git`, cron 15 min.
OTWARTE (NIE rób sam): GitHub origin tylko gdy user poda URL albo będzie `gh`. Nie twórz publicznego repo.

## Analizy — kontekst, nie restartuj
- TeleKiller: payload wyciągnięty, protokół C2 w `Narzedzia/Telegram_Stealer_Analiza.md`
- Lumma/clipper: YARA w pipeline

# Zasady
Po każdej zmianie:
`/root/obsidian-vault/Narzedzia/log_to_obsidian.sh "tytuł" "2–8 zdań, bez sekretów"`
Hasła/tokeny nigdy do vaultu.

Zacznij od NVD w threat digest. Potem krótki status i czekaj na usera.


### 👤 Użytkownik — 2026-08-15T17:29:37Z

<turn-context>
<current-time>2026-08-15 17:29:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
Once given a task, immediately update your todo with all explicit and implicit requirements


# Obsidian hook (każda tura Goose)

Po KAŻDEJ zmianie w labie (instalacja, werdykt, nowy host, nowa sesja, fix, archiwum)
NATYCHMIAST zapisz notatkę — nie na koniec, nie tylko w czacie.

```bash
/root/obsidian-vault/Narzedzia/log_to_obsidian.sh "Krótki tytuł" "2–8 zdań. Bez haseł, tokenów, kluczy."
```

Większa sesja:

```bash
/root/obsidian-vault/Narzedzia/log_to_obsidian.sh --recap "Tytuł sesji" "co zrobiono / wynik / next"
```

- Daily: `Daily/YYYY-MM-DD.md`
- Recap: `Lab/Recap YYYY-MM-DD.md`
- Hosty: `Lab/Hosts.md`
- Goose: `Lab/Goose_DeepSeek.md`
Hasła i tokeny NIGDY do vaultu.

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:43Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:43Z

Updated (474 chars)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:46Z

-rw-r--r-- 1 root root 10980 Aug 15 17:16 threat_digest.py
---GIT LOG---
---VAULT GIT---
d4a5861 Threat digest: +26 kątów ataku + Exploit-DB (publiczne PoC)
210fd4a Auto-sync: 2026-08-15 17:13:50 UTC
af6075d Threat digest: podsumowanie 'Jak hakerzy to wykorzystują' + perspektywa ofensywna przy każdym newsie
6a329b0 Auto-sync: 2026-08-15 17:07:17 UTC
0497dc4 Threat digest: polskie tłumaczenia + /zagrozenia w bocie

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:46Z

254 threat_digest.py
---
total 20
drwxr-xr-x 2 root   root    4096 Aug 15 16:55 .
drwxrwxr-x 6 ubuntu ubuntu  4096 Aug 15 16:55 ..
-rw-r--r-- 1 root   root   10931 Aug 15 17:17 2026-08-15.md

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:48Z

#!/usr/bin/env python3
"""Threat digest — zbiera najnowsze ataki i malware z portali (RU/CN/EN) + threat intel.

Zapisuje notatkę w Obsidian: Analizy/Threat_Digest/YYYY-MM-DD.md
Uruchamiane codziennie o 20:00 (cron).
"""
from __future__ import annotations

import datetime
import html
import json
import os
import re
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

VAULT = Path("/root/obsidian-vault")
OUT_DIR = VAULT / "Analizy" / "Threat_Digest"

FEEDS = [
    ("The Hacker News (EN)", "https://feeds.feedburner.com/TheHackersNews"),
    ("Krebs (EN)", "https://krebsonsecurity.com/feed/"),
    ("Xakep.ru (RU)", "https://xakep.ru/feed/"),
    ("Habr infosec (RU)", "https://habr.com/ru/rss/hub/infosecurity/all/?fl=ru"),
    ("Threatpost (EN)", "https://threatpost.com/feed/"),
    ("先知 xz.aliyun (CN)", "https://xz.aliyun.com/feed"),
]

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=20).read()


def clean(text: str) -> str:
    text = re.sub(r"<!\[CDATA\[|\]\]>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def translate(text: str, tl: str = "pl") -> str:
    """Tłumaczenie przez Google Translate (endpoint gtx, bez klucza)."""
    q = urllib.parse.quote(text[:400])
    url = f"https://translate.googleapis.com/
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:51Z

---
title: "Threat digest — 2026-08-15"
date: 2026-08-15
tags: [threat-digest, malware, ataki, aktualnosci]
status: daily
category: threat-intel
---

# Threat digest — 2026-08-15

> Automatycznie zebrane z portali (RU/CN/EN) + MalwareBazaar + ThreatFox.

## 🎯 Jak hakerzy to wykorzystują (skrót)

- obejście logowania → wejście bez hasła, kradzież sesji i danych.
- zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim ktoś załata.
- złośliwe rozszerzenie/proxy → przechwytywanie ruchu, kradzież sesji i haseł.
- luka + PoC → exploit przed łatką, masowe skanowanie Internetu.
- DoS → wyłączenie usługi (szantaż, odwrócenie uwagi od innego ataku).
- ransomware → szyfrowanie plików + wyłudzenie okupu (podwójny szantaż: szyfrowanie + leak).
- SIM swap / złośliwa SIM → przechwycenie 2FA przez SMS, klonowanie karty.
- RAT/stealer → zdalna kontrola, keylogger, kradzież sesji/portfeli.

## Najnowsze ataki i metody

### The Hacker News (EN)
- Atakujący wykorzystują obejście uwierzytelniania SharePoint po wydaniu publicznego PoC
   _(Attackers Exploit SharePoint Authentication Bypass After Public PoC Release)_
   🎯 *Hakerzy:* obejście logowania → wejście bez hasła, kradzież sesji i danych.
- Lazarus wykorzystuje system Windows Zero-Day do uzyskania dostępu do SYSTEMU i wdrożenia backdoora
   _(Lazarus Exploits Windows Zero-Day to Gain SYSTEM Access and Deploy Backdoor)_
   🎯 *Hakerzy:* zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:29:51Z

   🎯 *Hakerzy:* IoT/kamery/TV → botnety, szpiegostwo, sprzedaż dostępu do kamer.
- Skarga sygnalisty na Twitterze: wersja TL;DR
   _(Twitter Whistleblower Complaint: The TL;DR Version)_
   🎯 *Hakerzy:* atak na AI/LLM → kradzież modeli, prompt injection, dekodowanie rozumowania.

### 先知 xz.aliyun (CN)

## Najnowsze exploity / PoC (Exploit-DB)

- [webapps] Apache Gravitino 1.2.1 - SSRF
   🎯 *Hakerzy:* SSRF → serwer sam łączy się z wewnętrznymi usługami (cloud metadata, wewnętrzne API).
- [webapps] Blocksy Companion 2.1.46 - RCE
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
- [remote] PraisonAI praisonaiagents 1.6.77 - Remote Code Execution
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
- [remote] mcp-server-kubernetes 3.8.x - Argument Injection
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
- [dos] LuCI DHCPv6 - Lease Hostname Stored Cross-Site Scripting
   🎯 *Hakerzy:* XSS → kradzież sesji (cookie), phishing w kontekście zaufanej strony.
- [webapps] Planyo_Online_Reservation_System 3.0 - Arbitrary File Read via SSRF
   🎯 *Hakerzy:* SSRF → serwer sam łączy się z wewnętrznymi usługami (cloud metadata, wewnętrzne API).
- [webapps] Ray 2.56.0 - Directory Traversal & Local File Inclusion
   🎯 *Hakerzy:* LFI/traversal → odczyt plików, configów, haseł, kluczy.
- [webapps] OrkesConductor 3.30.2 - Unauthenticated Remote Code Execution
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne pr
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:30:35Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:30:35Z

total 1111
CVE-2026-19757
  keys ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV2', 'ssvcV203']
  desc A vulnerability was found in Dromara lamp-cloud up to 5.10.0. This vulnerability
  weak [{'source': 'cna@vuldb.com', 'type': 'Secondary', 'description': [{'lang': 'en', 'value': 'CWE-22'}]}]
CVE-2026-19758
  keys ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV2']
  desc A vulnerability was determined in dromara lamp-cloud up to 5.10.0. This issue af
  weak [{'source': 'cna@vuldb.com', 'type': 'Primary', 'description': [{'lang': 'en', 'value': 'CWE-22'}]}]
CVE-2026-19761
  keys ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV2', 'ssvcV203']
  desc A vulnerability has been found in DTStack Taier 1.4.0. Affected is the function 
  weak [{'source': 'cna@vuldb.com', 'type': 'Secondary', 'description': [{'lang': 'en', 'value': 'CWE-22'}]}]
CVE-2026-19762
  keys ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV2', 'ssvcV203']
  desc A vulnerability was found in DTStack Taier 1.4.0. Affected by this vulnerability
  weak [{'source': 'cna@vuldb.com', 'type': 'Secondary', 'description': [{'lang': 'en', 'value': 'CWE-22'}]}]
CVE-2026-19763
  keys ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV2']
  desc A vulnerability was determined in DTStack Taier 1.4.0. Affected by this issue is
  weak [{'source': 'cna@vuldb.com', 'type': 'Primary', 'description': [{'lang': 'en', 'value': 'CWE-22'}]}]

### 🛠️ Akcja/narzędzie — 2026-08-15T17:30:39Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:30:39Z

{'cvssData': {'attackComplexity': 'LOW',
              'attackVector': 'NETWORK',
              'availabilityImpact': 'LOW',
              'baseScore': 7.3,
              'baseSeverity': 'HIGH',
              'confidentialityImpact': 'LOW',
              'integrityImpact': 'LOW',
              'privilegesRequired': 'NONE',
              'scope': 'UNCHANGED',
              'userInteraction': 'NONE',
              'vectorString': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L',
              'version': '3.1'},
 'exploitabilityScore': 3.9,
 'impactScore': 3.4,
 'source': 'cna@vuldb.com',
 'type': 'Secondary'}
---v40---
{'cvssData': {'Automatable': 'NOT_DEFINED',
              'Recovery': 'NOT_DEFINED',
              'Safety': 'NOT_DEFINED',
              'attackComplexity': 'LOW',
              'attackRequirements': 'NONE',
              'attackVector': 'NETWORK',
              'availabilityRequirement': 'NOT_DEFINED',
              'baseScore': 5.5,
              'baseSeverity': 'MEDIUM',
              'confidentialityRequirement': 'NOT_DEFINED',
              'exploitMaturity': 'PROOF_OF_CONCEPT',
              'integrityRequirement': 'NOT_DEFINED',
              'modifiedAttackComplexity': 'NOT_DEFINED',
              'modifiedAttackRequirements': 'NOT_DEFINED',
              'modifiedAttackVector': 'NOT_DEFINED',
              'modifiedPrivilegesRequired': 'NOT_DEFINED',
              'modifiedSubAvailabilityImpact': 'NOT_DEFINED',
              'modifiedSubConfidentialityImp
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:15Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:15Z

Edited /root/threat_digest.py (3 lines -> 4 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:25Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:25Z

Edited /root/threat_digest.py (1 lines -> 90 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:28Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:28Z

                out.append(f"{meta}\n   _({desc_en[:140]})_\n   🎯 *Hakerzy:* {angle}")
        return out
    except Exception as e:
        return [f"_(błąd NVD: {e})_"]


def build_note() -> str:
    today = datetime.date.today()
    lines = [
        "---",
        f'title: "Threat digest — {today.isoformat()}"',
        f"date: {today.isoformat()}",
        "tags: [threat-digest, malware, ataki, aktualnosci]",
        "status: daily",
        "category: threat-intel",
        "---",
        "",
        f"# Threat digest — {today.isoformat()}",
        "",
        "> Automatycznie zebrane z portali (RU/CN/EN) + MalwareBazaar + ThreatFox.",
        "",
    ]

    # Zbierz wszystkie tytuły + kąty ataku (do podsumowania)
    angles_seen: list[str] = []
    feed_items: list[tuple[str, list[str]]] = []

    for name, url in FEEDS:
        try:
            titles = parse_feed(fetch(url))
            feed_items.append((name, titles))
            for t in titles:
                for pattern, angle in ATTACK_ANGLES:
                    if re.search(pattern, t.lower()):
                        if angle not in angles_seen:
                            angles_seen.append(angle)
                        break
        except Exception as e:
            feed_items.append((name, [f"_(błąd pobierania: {e})_"]))

    # Podsumowanie: jak hakerzy to wykorzystują
    if angles_seen:
        lines.append("## 🎯 Jak hakerzy to wykorzystują (skrót)")
        lines.append("")
        for angle in ang
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:37Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:37Z

Edited /root/threat_digest.py (43 lines -> 58 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:40Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:40Z

Edited /root/threat_digest.py (3 lines -> 3 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:43Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:43Z

OK compile

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:46Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:31:46Z

**CVE-2026-16770** · CVSS **9.8 (CRITICAL)** · CWE-88
   Wersje PDF::WebKit do 1.2 dla Perla umożliwiają wstrzykiwanie argumentów do wkhtmltopdf za pośrednictwem metatagów w dokumencie źródłowym. W przypadku ciągu HTML lub źródła pliku konstruktor zbiera każdy element w t _(PDF::WebKit versions through 1.2 for Perl allow argument injection into wkhtmltopdf via meta tags in the source document. For an HTML string)_
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
---
**CVE-2026-17431** · CVSS **6.1 (MEDIUM)** · CWE-73
   Wersje PDF::WebKit do 1.2 dla Perla umożliwiają wstrzykiwanie poleceń systemu operacyjnego za pomocą 2-argowej metody open() ścieżki wyjściowej w to_pdf i ścieżek arkusza stylów w _style_tag_for. to_pdf odczytuje wygenerowany plik PDF z powrotem _(PDF::WebKit versions through 1.2 for Perl allow OS command injection via a 2-arg open() of the output path in to_pdf and of stylesheet paths)_
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
---
**CVE-2026-46382** · CVSS **8.7 (HIGH)** · SSRF
   System rezerwacji sal konferencyjnych (MRBS) to oparta na języku PHP aplikacja do rezerwacji sal konferencyjnych. Przed wersją 1.12.2 prywatny/lokalny identyfikator URI dostarczony przez użytkownika można było pobrać bez sprawdzania. Wersja _(The Meeting Room Booking System (MRBS) is a PHP-based application for booking meeting rooms. Prior to version 1.12.2, a user-supplied privat)_
   🎯 *Hakerzy:* SSRF → serwer s
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:01Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:01Z

Edited /root/threat_digest.py (2 lines -> 5 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:03Z

Edited /root/threat_digest.py (1 lines -> 2 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:07Z

zapisano: /root/obsidian-vault/Analizy/Threat_Digest/2026-08-15.md (14991 B)

real	0m13.118s
user	0m0.175s
sys	0m0.040s

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:23Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:23Z

---
title: "Threat digest — 2026-08-15"
date: 2026-08-15
tags: [threat-digest, malware, ataki, aktualnosci]
status: daily
category: threat-intel
---

# Threat digest — 2026-08-15

> Automatycznie zebrane z portali (RU/CN/EN) + NVD (CVE) + MalwareBazaar + ThreatFox.

## 🎯 Jak hakerzy to wykorzystują (skrót)

- obejście logowania → wejście bez hasła, kradzież sesji i danych.
- zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim ktoś załata.
- złośliwe rozszerzenie/proxy → przechwytywanie ruchu, kradzież sesji i haseł.
- luka + PoC → exploit przed łatką, masowe skanowanie Internetu.
- DoS → wyłączenie usługi (szantaż, odwrócenie uwagi od innego ataku).
- ransomware → szyfrowanie plików + wyłudzenie okupu (podwójny szantaż: szyfrowanie + leak).
=== NVD SECTION ===
128:## Najnowsze CVE (NVD)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:25Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:25Z

## Najnowsze CVE (NVD)

- **CVE-2026-16770** · CVSS **9.8 (CRITICAL)** · Argument Injection
   Wersje PDF::WebKit do 1.2 dla Perla umożliwiają wstrzykiwanie argumentów do wkhtmltopdf za pośrednictwem metatagów w dokumencie źródłowym. W przypadku ciągu HTML lub źródła pliku konstruktor zbiera każdy element w t _(PDF::WebKit versions through 1.2 for Perl allow argument injection into wkhtmltopdf via meta tags in the source document. For an HTML string)_
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
- **CVE-2026-17431** · CVSS **6.1 (MEDIUM)** · External File/Path Control
   Wersje PDF::WebKit do 1.2 dla Perla umożliwiają wstrzykiwanie poleceń systemu operacyjnego za pomocą 2-argowej metody open() ścieżki wyjściowej w to_pdf i ścieżek arkusza stylów w _style_tag_for. to_pdf odczytuje wygenerowany plik PDF z powrotem _(PDF::WebKit versions through 1.2 for Perl allow OS command injection via a 2-arg open() of the output path in to_pdf and of stylesheet paths)_
   🎯 *Hakerzy:* RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji.
- **CVE-2026-46382** · CVSS **8.7 (HIGH)** · SSRF
   System rezerwacji sal konferencyjnych (MRBS) to oparta na języku PHP aplikacja do rezerwacji sal konferencyjnych. Przed wersją 1.12.2 prywatny/lokalny identyfikator URI dostarczony przez użytkownika można było pobrać bez sprawdzania. Wersja _(The Meeting Room Booking System (MRBS) is a PHP-based application for booking meeting rooms. Prior to version 1.12.2, a 
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:59Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:32:59Z

match rce pattern: rce

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:03Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:03Z

Edited /root/threat_digest.py (1 lines -> 1 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:06Z

zapisano: /root/obsidian-vault/Analizy/Threat_Digest/2026-08-15.md (15003 B)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:18Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:18Z

145:- **CVE-2026-49473** · CVSS **8.8 (HIGH)** · CWE-436
---exploitdb rce check---
165:- [webapps] Blocksy Companion 2.1.46 - RCE
167:- [remote] PraisonAI praisonaiagents 1.6.77 - Remote Code Execution
169:- [remote] mcp-server-kubernetes 3.8.x - Argument Injection

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:20Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:20Z

- **CVE-2026-49473** · CVSS **8.8 (HIGH)** · CWE-436
   @cedar-policy/authorization-for-expressjs to oprogramowanie pośredniczące Express.js o otwartym kodzie źródłowym, które integruje autoryzację Cedar z aplikacjami Express poprzez mapowanie żądań HTTP na działania Cedar i ocenę _(@cedar-policy/authorization-for-expressjs is an open-source Express.js middleware that integrates Cedar authorization into Express applicati)_
   🎯 *Hakerzy:* obejście logowania → wejście bez hasła, kradzież sesji i danych.

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:24Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:24Z


> Automatycznie zebrane z portali (RU/CN/EN) + NVD (CVE) + MalwareBazaar + ThreatFox.

## 🎯 Jak hakerzy to wykorzystują (skrót)

- obejście logowania → wejście bez hasła, kradzież sesji i danych.
- zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim ktoś załata.
- złośliwe rozszerzenie/proxy → przechwytywanie ruchu, kradzież sesji i haseł.
- luka + PoC → exploit przed łatką, masowe skanowanie Internetu.
- DoS → wyłączenie usługi (szantaż, odwrócenie uwagi od innego ataku).
- ransomware → szyfrowanie plików + wyłudzenie okupu (podwójny szantaż: szyfrowanie + leak).
- SIM swap / złośliwa SIM → przechwycenie 2FA przez SMS, klonowanie karty.
- RAT/stealer → zdalna kontrola, keylogger, kradzież sesji/portfeli.

## Najnowsze ataki i metody

### The Hacker News (EN)
- Atakujący wykorzystują obejście uwierzytelniania SharePoint po wydaniu publicznego PoC
   _(Attackers Exploit SharePoint Authentication Bypass After Public PoC Release)_
   🎯 *Hakerzy:* obejście logowania → wejście bez hasła, kradzież sesji i danych.
- Lazarus wykorzystuje system Windows Zero-Day do uzyskania dostępu do SYSTEMU i wdrożenia backdoora

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:32Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:32Z

 M Analizy/Threat_Digest/2026-08-15.md
--- ls-files threat ---
Analizy/Threat_Digest/2026-08-15.md
Analizy/Threat_Intel_MOC.md
Wiedza/Feed_ThreatFox.md
--- is /root a repo? ---
fatal: not a git repository (or any of the parent directories): .git
--- where is digest tracked? ---
Analizy/Threat_Digest/2026-08-15.md

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:42Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:42Z

9f27f28 Threat digest: źródło NVD (CVE + CVSS/typ) + regen notatki 2026-08-15
15cc780 Auto-sync: 2026-08-15 17:30:01 UTC
d4a5861 Threat digest: +26 kątów ataku + Exploit-DB (publiczne PoC)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:48Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:48Z

daily += /root/obsidian-vault/Daily/2026-08-15.md

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:33:51Z

 M Daily/2026-08-15.md
--- tail daily ---

Stary czat Goose (deepseek-vps) się zaciął. Z Kali odpalono nową sesję deepseek-vps-3 w qterminal (helper goose-vps-133-3). Seed: NVD/CVE w threat digest jako otwarte zadanie; fora z logowaniem pominięte; bot /wiedza + git lokalny bez GitHub origin. Stare okna deepseek-vps i deepseek-vps-2 nie ruszane.


## Threat digest: źródło NVD (CVE + CVSS/typ) (2026-08-15T17:33:48Z)

Dodano do /root/threat_digest.py źródło NVD (API CVE 2.0, ostatnie 2 dni). Każdy CVE dostaje metadane CVSS (wynik + severity), typ CWE (z mapą labeli) i linię „🎯 Hakerzy:”. Poprawiono też regex RCE (\brce\b), żeby nie łapał „resource/source”. Notatka 2026-08-15 przegenerowana i commitowana do vaultu (9f27f28).


### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:07Z

diff --git a/Daily/2026-08-15.md b/Daily/2026-08-15.md
index eaf6973..24287ca 100644
--- a/Daily/2026-08-15.md
+++ b/Daily/2026-08-15.md
@@ -435,3 +435,8 @@ Backend v2 wdrożony: znajomi, DM, lista czatów, WebSocket, presence, typing, u
 
 Stary czat Goose (deepseek-vps) się zaciął. Z Kali odpalono nową sesję deepseek-vps-3 w qterminal (helper goose-vps-133-3). Seed: NVD/CVE w threat digest jako otwarte zadanie; fora z logowaniem pominięte; bot /wiedza + git lokalny bez GitHub origin. Stare okna deepseek-vps i deepseek-vps-2 nie ruszane.
 
+
+## Threat digest: źródło NVD (CVE + CVSS/typ) (2026-08-15T17:33:48Z)
+
+Dodano do /root/threat_digest.py źródło NVD (API CVE 2.0, ostatnie 2 dni). Każdy CVE dostaje metadane CVSS (wynik + severity), typ CWE (z mapą labeli) i linię „🎯 Hakerzy:”. Poprawiono też regex RCE (\brce\b), żeby nie łapał „resource/source”. Notatka 2026-08-15 przegenerowana i commitowana do vaultu (9f27f28).
+

### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:10Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:10Z

--- clean ---
c72c012 Log: NVD w threat digest + regen notatki
9f27f28 Threat digest: źródło NVD (CVE + CVSS/typ) + regen notatki 2026-08-15

### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:16Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:34:16Z

Updated (478 chars)

### 🤖 Asystent — 2026-08-15T17:34:17Z

Zrobione. Krótki status:

## Threat digest — NVD dodany ✅

**Co zmieniłem w `/root/threat_digest.py`:**
- Nowe źródło **NVD** (`services.nvd.nist.gov/rest/json/cves/2.0/`), ostatnie 2 dni publikacji, do 10 CVE.
- Każde CVE ma metadane: **CVSS (wynik + severity)** + **typ CWE** (mapa `CWE_LABELS` → np. `Path Traversal`, `SQL Injection`, `SSRF`; nieznane kody zostają surowe).
- Ta sama perspektywa `🎯 Hakerzy:` co reszta — interpretacja z opisu + CWE.
- Bonus: poprawka regex `rce` → `\brce\b`, bo fałszywie łapał „resource/source” (np. middleware autoryzacyjny Cedar był błędnie oznaczany jako RCE).

**Efekt w notatce** (`Analizy/Threat_Digest/2026-08-15.md`):
- Sekcja `## Najnowsze CVE (NVD)` z liniami typu:
  `**CVE-2026-16770** · CVSS **9.8 (CRITICAL)** · Argument Injection → 🎯 Hakerzy: RCE…`
- Źródła w stopce i nagłówku zaktualizowane o NVD.

**Commity (vault, clean):**
- `9f27f28` — Threat digest: źródło NVD + regen notatki
- `c72c012` — Log: NVD w threat digest

**Czego NIE ruszałem (zgodnie z ustaleniami):**
- XSS.is / Exploit.in / BreachForums — bez konta, zostają pominięte.
- Bot Telegram / GitHub origin — bez Twojego URL albo `gh`.
- Notatka zalogowana w Daily (`log_to_obsidian.sh`).

Czekam na dalsze instrukcje.

### 👤 Użytkownik — 2026-08-15T17:40:09Z

moze byc wiecej tematow, wiecej katow. mozesz analizowac fora hakerskie.  - jesli chodzi o bota na telegramie i zakladke wiedza, pamietajj tez zeby aktualizowac obsidium

### 👤 Użytkownik — 2026-08-15T17:40:09Z

<turn-context>
<current-time>2026-08-15 17:40:00 +00:00</current-time>
<working-directory>/root</working-directory>

Current tasks and notes:
# Threat digest — NVD + regen notatki

- [x] Przeczytać /root/threat_digest.py (obecny stan)
- [x] Dodać źródło NVD (CVE feed) z CVSS/typ + perspektywą „🎯 Hakerzy:”
- [x] Przegenerować notatkę 2026-08-15.md
- [x] Commit do vaultu (9f27f28 + c72c012, clean)
- [x] Log do Obsidian (Daily)
- [x] Krótki status — czekam na usera

# Inne (kontekst, NIE robić bez zgody)
- Bot Telegram: GitHub origin tylko gdy user poda URL / `gh`
- Nie logować na XSS.is / Exploit.in / BreachForums



# Obsidian hook (każda tura Goose)

Po KAŻDEJ zmianie w labie (instalacja, werdykt, nowy host, nowa sesja, fix, archiwum)
NATYCHMIAST zapisz notatkę — nie na koniec, nie tylko w czacie.

```bash
/root/obsidian-vault/Narzedzia/log_to_obsidian.sh "Krótki tytuł" "2–8 zdań. Bez haseł, tokenów, kluczy."
```

Większa sesja:

```bash
/root/obsidian-vault/Narzedzia/log_to_obsidian.sh --recap "Tytuł sesji" "co zrobiono / wynik / next"
```

- Daily: `Daily/YYYY-MM-DD.md`
- Recap: `Lab/Recap YYYY-MM-DD.md`
- Hosty: `Lab/Hosts.md`
- Goose: `Lab/Goose_DeepSeek.md`
Hasła i tokeny NIGDY do vaultu.

</turn-context>

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:02Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:02Z

=== Wiedza/ ===
total 60
drwxr-xr-x  7 root   root   4096 Aug 15 16:55 .
drwxrwxr-x 22 ubuntu ubuntu 4096 Aug 15 16:51 ..
-rw-r--r--  1 root   root   1220 Aug 15 16:56 Aktualizacje.md
drwxr-xr-x  2 root   root   4096 Aug 15 16:52 Ataki
-rw-r--r--  1 root   root   1851 Aug 15 16:55 Feed_CISA_KEV.md
-rw-r--r--  1 root   root   1117 Aug 15 16:55 Feed_MalwareBazaar.md
-rw-r--r--  1 root   root   1298 Aug 15 16:55 Feed_ThreatFox.md
drwxr-xr-x  2 root   root   4096 Aug 15 16:52 Malware
-rw-r--r--  1 root   root   3452 Aug 15 16:51 Narzedzia.md
drwxr-xr-x  2 root   root   4096 Aug 15 16:52 Obrona
drwxr-xr-x  2 root   root   4096 Aug 15 16:52 Pentest
-rw-r--r--  1 root   root   2450 Aug 15 16:56 README.md
drwxr-xr-x  2 root   root   4096 Aug 15 16:52 RedTeam
-rw-r--r--  1 root   root   2482 Aug 15 16:51 Zrodla.md
-rw-r--r--  1 root   root    781 Aug 15 16:51 _Template.md
=== bot tree ===
total 336
drwxrwxr-x  6 ubuntu ubuntu  4096 Aug 15 17:13 .
drwx------ 61 root   root    4096 Aug 15 17:31 ..
-rw-------  1 root   root     497 Aug 15 11:09 .env
-rw-rw-r--  1 ubuntu ubuntu   448 Aug 15 11:07 .env.example
drwxr-xr-x  8 root   root    4096 Aug 15 17:30 .git
-rw-rw-r--  1 ubuntu ubuntu    48 Aug 15 03:25 .gitignore
-rw-------  1 root   root      10 Aug 14 23:11 .owner_id
drwxr-xr-x  5 root   root    4096 Aug 14 23:12 .venv
-rw-rw-r--  1 ubuntu ubuntu  1679 Aug 15 10:41 README.md
drwxr-xr-x  2 root   root    4096 Aug 15 17:06 __pycache__
-rwxr-xr-x  1 root   root    8404 Aug 15 03:25 ale
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:02Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:02Z

=== cron ===
0 20 * * * /usr/bin/python3 /root/threat_digest.py >> /root/threat_digest.log 2>&1
=== threat_digest FEEDS/ANGLES counts ===
31
56:ATTACK_ANGLES = [
89:    for pattern, angle in ATTACK_ANGLES:
288:            for pattern, angle in ATTACK_ANGLES:

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:07Z

=== full crontab ===
# nightly is in /etc/cron.d/nightly-pipeline — do not duplicate here
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
0 20 * * * /usr/bin/python3 /root/threat_digest.py >> /root/threat_digest.log 2>&1
=== Wiedza/README.md ===
---
title: "Wiedza — baza o atakach, malware i obronie"
date: 2026-08-15
updated: 2026-08-15
tags: [wiedza, index, moc, intel, malware, pentest, redteam, obrona]
status: active
---

# Wiedza — gromadzenie wiedzy o zagrożeniach

Folder do regularnego gromadzenia wiedzy o: **nowych wirusach, malware, pentestingu,
red teamingu, analizie malware, nowych atakach, narzędziach i obronie.**

> **Zasada:** notatki = wiedza ogólna + konkretne TTP + narzędzia + obrona.
> Konkretne próbki z labu (RE, IoC, detekcja) zostają w [[Analizy]] — tu linkujemy do nich,
> żeby nie dublować.

## Mapa folderu

| Kategoria | Notatka | Co zawiera |
|-----------|---------|------------|
| Techniki ataku | [[Ataki/Ataki_MOC]] | Fazy ataku (MITRE ATT&CK), TTP, narzędzia, obrona |
| Malware / wirusy | [[Malware/Malware_MOC]] | Rodziny: stealery, ransomware, loadery, RAT, clippery |
| Pentesting | [[Pentest/Pentest_MOC]] | Metodologia, web/network/AD, narzędzia, raport |
| Red teaming | [[RedTeam/RedTeam_MOC]] | OPSEC, C2, emulacja przeciwnika, purple team |
| Obrona | [[Obrona/Obrona_MOC]] | Detekcja, hardening, IR, D3FEND, Sigma/YARA |
| Narzędzia | [[Narzedzia]] | Katalog narzędzi ofensywnych i defensywnych |
| Źródła | [[Zrodla]
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:07Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:07Z

=== Zrodla.md ===
---
title: "Źródła wiedzy o zagrożeniach"
date: 2026-08-15
tags: [wiedza, intel, feeds, sources]
---

# Źródła — skąd brać świeżą wiedzę

Powiązane: [[Zasoby/Linki_Zewnętrzne]] · [[Narzedzia]]

## Feedy / API (da się automatyzować)

| Źródło | Co daje | Jak |
|--------|---------|-----|
| MalwareBazaar (abuse.ch) | Świeże próbki, rodziny, hashe, tagi | API `mb-api.abuse.ch/api/v1/`, nagłówek `Auth-Key` (klucz `~/.mb_api_key`) |
| ThreatFox (abuse.ch) | IoC (IP/domain/url) | API, darmowy klucz |
| URLhaus (abuse.ch) | Złośliwe URL | API |
| CISA KEV | Exploitowane CVE (priorytet patch) | JSON `cisa.gov/known-exploited-vulnerabilities-catalog.json` |
| NVD / CVE | Luki | `services.nvd.nist.gov/rest/json/cves/2.0` |
| AlienVault OTX | Pulse / IoC | `otx.alienvault.com/api/v1/pulses/subscribed` |
| MITRE ATT&CK / D3FEND | TTP + techniki obrony | `github.com/mitre/cti` (STIX/JSON) |
| VX-Underground | Kolekcje malware + papery | `vx-underground.org`, GitHub |
| GreyNoise | IP z internetu (skanery/exploity) | API |

## RSS / blogi vendorów (analizy kampanii)

- Mandiant / Google Cloud Threat Intel (ex-FireEye) — `cloud.google.com/blog/topics/threat-intelligence`
- Unit 42 (Palo Alto) — `unit42.paloaltonetworks.com`
- CrowdStrike Blog — adversary write-ups
- SentinelOne — `sentinelone.com/blog`
- Microsoft Threat Intelligence — `microsoft.com/security/blog`
- SANS Internet Storm Center — dzienne wpisy ISC (`isc.sans.edu`)
- The Hacker News / BleepingComputer / Krebs
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:29Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:41:29Z

BleepingComputer: OK items=15 | New Evooo1Bot Linux botnet turns routers into traffic relay 
SecurityAffairs: OK items=10 | SAP Commerce Cloud CVE-2026-58231 Exploited in the Wild
DarkReading: OK items=50 | Mission-Driven Security: Inside a Global Bank's Defense
FreeBuf: FAIL HTTPError HTTP Error 405: Not Allowed
Seebug: FAIL URLError <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)>
PacketStorm: FAIL URLError <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'rss.packetstormsecurity.com'. (_ssl.c:1000)>
SANS_ISC: OK items=10 | ISC Stormcast For Friday, August 14th, 2026 https://isc.sans
reddit_netsec: OK items=0 | 
reddit_Malware: FAIL HTTPError HTTP Error 429: Too Many Requests
reddit_hacking: FAIL HTTPError HTTP Error 429: Too Many Requests
reddit_cybersecurity: FAIL HTTPError HTTP Error 429: Too Many Requests
Threatpost: OK items=10 | Student Loan Breach Exposes 2.5M Records

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:04Z

hnrss_front: OK items=20 | TreasuryDirect: Prepare for ID.me – Your New Way to Log In
hnrss_sec: FAIL HTTPError HTTP Error 502: Bad Gateway
reddit_old_netsec: OK items=0 | 
reddit_json_netsec: FAIL HTTPError HTTP Error 403: Blocked
--- threatpost dates ---
Wed, 31 Aug 2022 12:57:48 +0000 | Student Loan Breach Exposes 2.5M Records
Tue, 30 Aug 2022 16:00:43 +0000 | Watering Hole Attacks Push ScanBox Keylogger
Mon, 29 Aug 2022 14:56:19 +0000 | Tentacles of ‘0ktapus’ Threat Group Victimize 130 

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:29Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:29Z

0x00sec_rss1: FAIL HTTPError HTTP Error 404: Not Found
0x00sec_rss2: FAIL HTTPError HTTP Error 404: Not Found
0x00sec_root: HTML/other len=26183 | b'<!DOCTYPE html>\n<html lang="en" class="dark-mode">\n\n<head>\n    <meta charset="ut'
seebug_unverified: RSS items=0 | 
packetstorm_feeds: HTML/other len=34752 | b'<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>Packet Storm Security</title>\n<me'

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:47Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:47Z

https://0x00sec.org/latest.rss FAIL HTTPError HTTP Error 404: Not Found
https://0x00sec.org/latest.json FAIL HTTPError HTTP Error 404: Not Found
https://0x00sec.org/categories.rss FAIL HTTPError HTTP Error 404: Not Found

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:52Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:52Z

<link rel="alternate" type="application/rss+xml" title="0x00sec" href="https://0x00sec.org/rss/">
---forum engine hints---

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:42:56Z

items= 15
- Fixing an Impacket bug: How 3-part SPN service tickets can break most 
- Protecting yourself from supply chain attacks, profiling, and slop mac
- Copying Code to Read Only Memory without Using `mprotect`
- Emulating Kimsuky's Initial Access
- Hacking C++ (Part 2)
- Hacking C++ (Part 1)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:43:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:43:06Z

THN: 50 | Attackers Exploit SharePoint Authentication Bypass After Pub
Krebs: 10 | Who’s Tracking You? Use This New Service to Find Out
Xakep: 10 | Четвертый бумажный спецвыпуск «Хакера» уже едет к читателям
Habr: 40 | 8 агентов, 12 волн, 4 дня: как ИИ в одиночку взломал правите
Threatpost: 10 | Student Loan Breach Exposes 2.5M Records
xz.aliyun: 0 | 

### 🛠️ Akcja/narzędzie — 2026-08-15T17:44:20Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:44:20Z

/root/obsidian-telegram-bot/bot.py:683:async def cmd_zagrozenia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
/root/obsidian-telegram-bot/bot.py:710:WIEDZA_FOLDER = "Wiedza"
/root/obsidian-telegram-bot/bot.py:713:def _wiedza_notes(vault: Vault) -> list:
/root/obsidian-telegram-bot/bot.py:721:def _wiedza_label(note) -> str:
/root/obsidian-telegram-bot/bot.py:729:def _wiedza_text(vault: Vault) -> str:
/root/obsidian-telegram-bot/bot.py:730:    notes = _wiedza_notes(vault)
/root/obsidian-telegram-bot/bot.py:732:        return "Brak notatek w `Wiedza/`."
/root/obsidian-telegram-bot/bot.py:737:        "🧠 *Wiedza — baza zagrożeń*",
/root/obsidian-telegram-bot/bot.py:747:            lines.append(f"   • {escape_markdown(_wiedza_label(n), version=1)}")
/root/obsidian-telegram-bot/bot.py:752:def _wiedza_markup(vault: Vault) -> InlineKeyboardMarkup:
/root/obsidian-telegram-bot/bot.py:753:    notes = _wiedza_notes(vault)
/root/obsidian-telegram-bot/bot.py:756:        label = _wiedza_label(n)
/root/obsidian-telegram-bot/bot.py:759:        rows.append([InlineKeyboardButton(label, callback_data=f"wiedza:n:{n.rel}")])
/root/obsidian-telegram-bot/bot.py:760:    rows.append([InlineKeyboardButton("🔄 Odśwież", callback_data="wiedza:r")])
/root/obsidian-telegram-bot/bot.py:764:async def cmd_wiedza(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
/root/obsidian-telegram-bot/bot.py:769:        _wiedza_text(vault),
/root/obsidian-telegram-bot/bot.py:770:        reply_marku
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:44:25Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:44:25Z

async def cmd_zagrozenia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await guard(update):
        return
    vault = get_vault()
    # znajdź najnowszą notatkę threat digest
    digest = [
        n for n in vault.iter_notes()
        if n.folder.replace("\\", "/") == "Analizy/Threat_Digest"
    ]
    if not digest:
        await update.effective_message.reply_text("Brak notatek threat digest.")
        return
    digest.sort(key=lambda n: n.title, reverse=True)
    note = digest[0]
    body = vault.read(note)
    header = f"🌍 *Threat digest*\n`{note.rel}`\n\n"
    chunks = chunk_text(body)
    first = header + chunks[0]
    if len(first) > 4000:
        first = first[:4000]
    await update.effective_message.reply_markdown(first)
    for extra in chunks[1:]:
        await update.effective_message.reply_markdown(extra)


# ---------------- WIEDZA (baza zagrożeń) ----------------

WIEDZA_FOLDER = "Wiedza"



### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:02Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:02Z

    return "".join(seg[0] for seg in data[0] if seg and seg[0])


# Mapowanie tematu → jak hakerzy to wykorzystują (perspektywa ofensywna, do obrony).
ATTACK_ANGLES = [
    (r"zero[- ]day", "zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim ktoś załata."),
    (r"ssrf", "SSRF → serwer sam łączy się z wewnętrznymi usługami (cloud metadata, wewnętrzne API)."),
    (r"\brce\b|remote code|command execution|argument injection", "RCE → zdalne wykonanie kodu, pełne przejęcie serwera/aplikacji."),
    (r"xss|cross[- ]site", "XSS → kradzież sesji (cookie), phishing w kontekście zaufanej strony."),
    (r"lfi|traversal|file inclusion|arbitrary file|directory traversal", "LFI/traversal → odczyt plików, configów, haseł, kluczy."),
    (r"sql|injection|deserializ", "iniekcja (SQL/komend/deserializacja) → kradzież danych lub wykonanie kodu."),
    (r"dos|ddos|denial", "DoS → wyłączenie usługi (szantaż, odwrócenie uwagi od innego ataku)."),
    (r"auth|bypass|login|credential|unauth", "obejście logowania → wejście bez hasła, kradzież sesji i danych."),
    (r"privilege|privesc|escalation|system access", "eskalacja uprawnień → z usera do admina/SYSTEM, pełna kontrola."),
    (r"lazarus|apt|group|0ktapus|nation|state", "grupy APT → celowane, długotrwałe kampanie szpiegowskie (zero-day + backdoor)."),
    (r"extension|vpn|proxy|browser", "złośliwe rozszerzenie/proxy → przechwytywanie ruchu, kradzież sesji i haseł."),
    (r"phish|spear|smishing|vishing|watering h
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:12Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:12Z

Edited /root/threat_digest.py (5 lines -> 6 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:17Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:17Z

Edited /root/threat_digest.py (8 lines -> 11 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:20Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:20Z

Edited /root/threat_digest.py (1 lines -> 1 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:36Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:36Z

Edited /root/threat_digest.py (2 lines -> 30 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:38Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:38Z

127:def parse_feed(data: bytes, limit: int = 6) -> list[str]:

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:41Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:41Z

def parse_feed(data: bytes, limit: int = 6) -> list[str]:
    root = ET.fromstring(data)
    items = root.findall(".//item")[:limit]
    out = []
    for it in items:
        title = clean(it.findtext("title", ""))
        if title:
            title = title[:120]
            angle = interpret(title)
            try:
                pl = translate(title)
                out.append(f"{pl}\n   _({title})_\n   🎯 *Hakerzy:* {angle}")
            except Exception:
                out.append(f"{title}\n   🎯 *Hakerzy:* {angle}")
    return out


def malwarebazaar_recent(key: str, limit: int = 8) -> list[str]:
    """Top sygnatury z ostatnich próbek."""
    try:

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:45Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:45Z

Edited /root/threat_digest.py (10 lines -> 11 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:49Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:49Z

6:Źródła: news RSS (EN/RU) + forum 0x00sec + NVD (CVE) + Exploit-DB + abuse.ch.
344:        for angle in angles_seen[:8]:
348:    lines.append("## Najnowsze ataki i metody")
357:    lines.append("## Najnowsze CVE (NVD)")
364:    lines.append("## Najnowsze exploity / PoC (Exploit-DB)")
370:    key_path = Path("/root/.mb_api_key")
371:    key = key_path.read_text().strip() if key_path.exists() else ""
382:    lines.append("---")
383:    lines.append("Źródła: The Hacker News · Krebs · Xakep.ru · Habr · Threatpost · xz.aliyun · NVD · abuse.ch")

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:51Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:51Z

    note_angles(nvd_items)
    exploit_items = exploitdb_recent()
    note_angles(exploit_items)

    # Podsumowanie: jak hakerzy to wykorzystują
    if angles_seen:
        lines.append("## 🎯 Jak hakerzy to wykorzystują (skrót)")
        lines.append("")
        for angle in angles_seen[:8]:
            lines.append(f"- {angle}")
        lines.append("")

    lines.append("## Najnowsze ataki i metody")
    lines.append("")
    for name, titles in feed_items:
        lines.append(f"### {name}")
        for t in titles:
            lines.append(f"- {t}")
        lines.append("")

    # NVD — świeże CVE z metadanymi CVSS/typ
    lines.append("## Najnowsze CVE (NVD)")
    lines.append("")
    for s in nvd_items:
        lines.append(f"- {s}")
    lines.append("")

    # Exploit-DB (publiczne PoC — najbliższe "forom" bez logowania)
    lines.append("## Najnowsze exploity / PoC (Exploit-DB)")
    lines.append("")
    for s in exploit_items:
        lines.append(f"- {s}")
    lines.append("")

    key_path = Path("/root/.mb_api_key")
    key = key_path.read_text().strip() if key_path.exists() else ""
    if key:
        lines.append("## Najnowsze malware (MalwareBazaar)")
        for s in malwarebazaar_recent(key):
            lines.append(f"- `{s}`")
        lines.append("")
        lines.append("## Najnowsze IOC (ThreatFox, 24h)")
        for s in threatfox_recent(key):
            lines.append(f"- `{s}`")
        lines.append("")

    lines.append("---")
    lines.append("Źródła
…(obcięte)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:56Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:46:56Z

Edited /root/threat_digest.py (1 lines -> 1 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:00Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:00Z

Edited /root/threat_digest.py (5 lines -> 12 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:04Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:04Z

Edited /root/threat_digest.py (3 lines -> 3 lines)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:06Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:06Z

FEEDS: 9
ANGLES: 53
 - The Hacker News (EN)
 - BleepingComputer (EN)
 - Krebs (EN)
 - Security Affairs (EN)
 - Dark Reading (EN)
 - SANS ISC (EN)
 - Xakep.ru (RU)
 - Habr infosec (RU)
 - 0x00sec (forum, EN)

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:10Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:10Z

zapisano: /root/obsidian-vault/Analizy/Threat_Digest/2026-08-15.md (21632 B)

real	0m18.147s
user	0m0.337s
sys	0m0.067s

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:31Z

tool: tool

### 🛠️ Akcja/narzędzie — 2026-08-15T17:47:31Z

---
title: "Threat digest — 2026-08-15"
date: 2026-08-15
tags: [threat-digest, malware, ataki, aktualnosci]
status: daily
category: threat-intel
---

# Threat digest — 2026-08-15

> Automatycznie zebrane z portali (RU/CN/EN) + NVD (CVE) + MalwareBazaar + ThreatFox.

## 🎯 Jak hakerzy to wykorzystują (skrót)

- obejście logowania → wejście bez hasła, kradzież sesji i danych.
- zero-day = broń pierwszego uderzenia: sprzedają na dark webie albo używają zanim ktoś załata.
- złośliwe rozszerzenie/proxy → przechwytywanie ruchu, kradzież sesji i haseł.
- luka + PoC → exploit przed łatką, masowe skanowanie Internetu.
- urządzenia brzegowe → wejście do sieci bez dotykania endpointów, MITM i tunel.
- RAT/stealer → zdalna kontrola, keylogger, kradzież sesji/portfeli.
- DoS → wyłączenie usługi (szantaż, odwrócenie uwagi od innego ataku).
- iniekcja (SQL/komend/deserializacja) → kradzież danych lub wykonanie kodu.
- spyware/zero-click → infekcja bez kliknięcia (wiadomość), pełny monitoring telefonu.
- kernel/ebpf → eskalacja z usera do roota, omijanie ograniczeń kontenera.

## Najnowsze ataki i metody

### The Hacker News (EN)
- Atakujący wykorzystują obejście uwierzytelniania SharePoint po wydaniu publicznego PoC
   _(Attackers Exploit SharePoint Authentication Bypass After Public PoC Release)_
   🎯 *Hakerzy:* obejście logowania → wejście bez hasła, kradzież sesji i danych.
- Lazarus wykorzystuje system Windows Zero-Day do uzyskania dostępu do SYSTEMU i wdrożenia backdoora
   _(Lazarus Ex
…(obcięte)
