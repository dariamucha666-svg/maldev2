---
title: "SET Lab (.139) — Credential Harvester / Site Cloner"
date: 2026-08-16
tags: [phishing, set, credential-harvester, site-cloner, lab, symulacja]
status: active
category: lab
---

# SET Lab na .139 (Social-Engineer Toolkit)

SET = wielowektorowy toolkit (TrustedSec). W labie używany **Credential Harvester + Site Cloner**
— klonuje całą stronę logowania (wget) i serwuje ją, przechwytując login+hasło z POST.
**Do symulacji/awareness — klonować wyłącznie własne/autoryzowane serwisy (mocki), nigdy realne.**

Powiązane: [[Phishing_Sim_Lab]] · [[Narzedzia/Phishing_Detekcja]] · [[Narzedzia/Phishing_Toolkit]] · [[Lab/Hosts]]

## Stan (zweryfikowane 2026-08-16)

| | |
|--|--|
| Ścieżka | /opt/set/setoolkit |
| Config | /etc/setoolkit/set.config |
| Harvester | 0.0.0.0:8081 (proces python3) — serwuje klon + łapie POST |
| Klon (strona) | 127.0.0.1:8090 — "Acme Corp — Employee Portal Sign In" |
| Log creds | /opt/set/src/logs/harvester.log |

## Mechanizm (Credential Harvester)

1. SET klonuje stronę logowania (wget mirror) do web_clone/index.html.
2. Serwuje klon lokalnie (harvester, port 8081).
3. Ofiara wpisuje login+hasło → POST przechwytywany → zapis do harvester.log.
4. Brak trackingu (w przeciwieństwie do GoPhish) — to script-kit, nie framework.

## Weryfikacja na żywo (fresh test)

- POST username=fresh.demo & password=FreshPass2026 → HTTP 000 (SET nie odpowiada poprawnie na POST — to wskaźnik).
- harvester.log dopisany: username=fresh.demo, password=FreshPass2026. ✅

## Detekcja (kluczowe wskaźniki)

1. **Server: BaseHTTP/0.6 Python/3.x** — prosty http.server, nie nginx/apache.
2. **POST z plaintext** username= / password= (brak TLS).
3. **Brak poprawnej odpowiedzi** na POST (curl 000).
4. Artefakty: katalog web_clone/, logi harvester.log, User-Agent wget przy klonowaniu.
5. Suricata: reguły 9000101 (banner) i 9000102 (plaintext POST) w phishing_tools.rules — zweryfikowane.

## Bezpieczeństwo

1. Bind 127.0.0.1 / UFW blokuje 8081, 8090 z zewnątrz (phish-lab-hardening.sh).
2. Klonować wyłącznie własne/autoryzowane serwisy (mocki); nigdy realnych.
3. Czyścić harvester.log po demie (dane logowania ofiary).
4. SET nie obchodzi 2FA (łapie tylko login+hasło, nie cookie) — patrz [[Narzedzia/Phishing_Toolkit]].
