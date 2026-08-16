---
title: "Detekcja AiTM (Evilginx2 / reverse-proxy phishing)"
date: 2026-08-16
tags: [phishing, aitm, detection, sigma, suricata, ct, dns]
status: guide
category: detekcja
---

# Detekcja AiTM (Evilginx2 / reverse-proxy phishing)

AiTM = Adversary-in-the-Middle: ofiara loguje się do prawdziwego serwisu **przez** proxy atakującego,
który kopiuje ciasteczka sesji (w tym post-2FA). Najgroźniejsza forma phishingu — bo **obchodzi MFA**.

Powiązane: [[Narzedzia/Phishlet_Przewodnik]] · [[Evilginx2_Lab]] · [[Narzedzia/Phishing_Detekcja]] · [[Narzedzia/Phishing_Toolkit]]

## Wskaźniki (od najsilniejszego)

| # | Wskaźnik | Gdzie szukać | Trudność |
|---|----------|--------------|----------|
| 1 | **Domena lookalike** (typosquat/punycode/prefiks) | DNS pasywny, fresh registrations | niska |
| 2 | **Cert Transparency**: nowy cert LE dla lookalike tuż przed kampanią | crt.sh / certstream | niska |
| 3 | **Cookie sesji exfil do IP atakującego** (po logowaniu cookie idzie na obcy host) | proxy/web logs | średnia |
| 4 | **Nagłówki reverse-proxy** (Via, X-Forwarded-For/Host) — evilginx część ukrywa | web logs | średnia |
| 5 | **TLS fingerprint** (Go TLS evilginx vs TLS prawdziwego serwisu) | JA3/JA4, zeek | średnia |
| 6 | **Server/baner** (np. BaseHTTP/Python, albo brak znanego bannera) | passive scan | niska |

## 1. Domena lookalike

- Typosquat: g00gle.com, micrsoft.com, 1inkedin.com.
- Prefiks/sufiks: login-microsoft.com, secure-google.com, outlook-verify.net.
- Punycode: np. домен z cyrylicą imitujący ASCII.
- Wykrywanie: DNSTwist / dnstwist, monitoring nowych rejestracji, lista popularnych marek + distance (Levenshtein).

## 2. Certificate Transparency

AiTM potrzebuje ważnego certa dla domeny lookalike (LE), więc cert trafia do logów CT **zanim** kampania ruszy.

- crt.sh: sprawdź certy dla podejrzanej domeny (data wydania vs pierwsze użycie).
- certstream: strumień nowych certów → alert na nazwy bliskie markom.

## 3. Cookie exfil (najmocniejszy dowód)

Sedno AiTM: po udanym logowaniu ciasteczko sesji (np. Microsoft SSID/ESTSAUTH) zostaje wysłane **na IP/domenę atakującego**, nie na IP prawdziwego serwisu.

- W logach proxy: sekwencja GET /login na lookalike → 302 Set-Cookie → kolejny request z tym cookie **do innego origin IP**.
- Heurystyka: cookie z domain .prawdziwa-strona dostarczone z hosta, który nie jest IP tej strony.

## 4. Reverse-proxy nagłówki

evilginx (jak każdy reverse proxy) może zostawiać: Via, X-Forwarded-For, X-Forwarded-Host, X-Forwarded-Proto.
Część evilginx usuwa/nadpisuje — dlatego to wskaźnik pomocniczy, nie jedyny.

## Reguła Sigma (proxy logs)

~~~yaml
title: AiTM phishing - lookalike domain serving login + cookie to external host
id: a1a1a1a1-0000-0000-0000-000000000001
status: experimental
description: Wykrywa reverse-proxy phishing (Evilginx2): logowanie z domeny lookalike i przekazanie ciasteczka sesji na zewnętrzny host.
logsource:
  category: proxy
detection:
  selection_domain:
    http_host|contains:
      - 'login-'
      - 'secure-'
      - 'account-'
      - 'verify-'
  selection_cookie:
    http_cookie|contains: 'session'
  selection_forwarded:
    http_header_X-Forwarded-For|exists: true
  condition: selection_domain and selection_cookie and selection_forwarded
fields:
  - http_host
  - http_cookie
  - src_ip
  - dst_ip
level: high
tags:
  - attack.credential_access
  - attack.t1557
~~~

## Suricata (istniejąca reguła)

Reguła 9000401 w /root/android-pipeline/tools/detection/phishing_tools.rules — heurystyka reverse-proxy (Set-Cookie + X-Forwarded-For). Korelować z CT/DNS (nie samodzielnie).

## MITRE ATT&CK

| TTP | ID |
|-----|-----|
| Adversary-in-the-Middle | T1557 |
| Phishing | T1566 |
| Steal Web Session Cookie | T1539 |
| Credentials from Password Stores (jeśli creds) | T1555 |

## Wskaźniki z mojego dema (Evilginx2_Lab)

- Domena phish **evil.local** (127.0.0.1) proxyuje do origin **mock.local** (127.0.0.2).
- Cookie **session=MOCKSESSION_...** zrewritowane z mock.local na evil.local — to jest dokładnie wskaźnik #3 (cookie z domeny origin dostarczone pod domeną phish).
- W realnym świecie: evil.local = świeżo zarejestrowana lookalike z certem LE z CT; session cookie dostarczone z IP atakującego.

## Następne kroki (do zrobienia)

1. DNSTwist na liście brandów + cron → alert na nowe lookalike.
2. certstream → powiadomienie o certach dla podejrzanych nazw.
3. Zeek/tshark: korelacja Set-Cookie → cookie na zewnętrzny IP (wzbogacić istniejące phishing_tools.zeek).
