---
title: "Pokrycie detekcji — Suricata + Sigma (purple team)"
date: 2026-08-16
type: raport
tags: [lab, purple-team, detekcja, suricata, sigma, coverage]
status: completed
---

# Pokrycie detekcji — technika ↔ reguła

Wygenerowane: `2026-08-16T07:38:51Z` przez `Narzedzia/detection_validator.py` (replay offline, brak ruchu na żywo).

## Metoda

- **Suricata:** syntetyczne pcapy technik puszczane `suricata -r` na regułach `clayrat_c2.rules` (8) + `local.rules` AD lab (11); zbiór SID-ów, które odpaliły → `eve.json`.
- **Sigma:** syntetyczne zdarzenia Windows Security (4768/4769/4662/4771/5145) przez uproszczony matcher (selection/filter + agregacja `count() by` z `timeframe`).
- Pcapy własne: `--pcap <file>` — 0.

## Tablica pokrycia

| Technika | MITRE | Suricata (oczekiwane SID) | Odpaliły | Sigma | Wynik Sigma | Status |
|----------|-------|---------------------------|----------|-------|-------------|--------|
| clayrat-beacon | T1071.001 | 9000801,9000802,9000807 | 9000801,9000802,9000807 | — | — | PASS |
| clayrat-ws | T1071.001 | 9000803 | 9000803 | — | — | PASS |
| clayrat-dns | T1568.002 | 9000808 | 9000808 | — | — | PASS |
| kerberoasting | T1558.003 | 1100011 | 1100011 | ad-kerberoasting-001 | ad-kerberoasting-001 | PASS |
| asrep-roast | T1558.004 | 1100012 | 1100012 | ad-asrep-roasting-001 | ad-asrep-roasting-001 | PASS |
| password-spray | T1110.003 | 1100010 | 1100010 | ad-password-spray-001 | ad-password-spray-001 | PASS |
| smb-enum | T1087/T1018 | 1100013 | 1100013 | ad-smb-ldap-enum-001 | ad-smb-ldap-enum-001 | PASS |
| ldap-enum | T1087/T1018 | 1100014 | 1100014 | — | — | PASS |
| dcsync | T1003.006 | 1100015 | 1100015 | ad-dcsync-001 | ad-dcsync-001 | PASS |

## Szczegóły Suricata

### clayrat-beacon (T1071.001)

- `9000807` MALWARE ClayRat C2 beacon 91.210.168.138:80 — 127.0.0.1 → 91.210.168.138:80 (2025-08-15T23:20:00.002000+0000)
- `9000801` MALWARE ClayRat beacon /huy UA ClayApp/1.0 — 127.0.0.1 → 91.210.168.138:80 (2025-08-15T23:20:00.000000+0000)
- `9000802` MALWARE ClayRat C2 domena packwatheboss.lol — 127.0.0.1 → 91.210.168.138:80 (2025-08-15T23:20:00.000000+0000)

### clayrat-ws (T1071.001)

- `9000803` MALWARE ClayRat C2 WS 193.111.117.72:8080 — 127.0.0.1 → 193.111.117.72:8080 (2025-08-15T23:20:00.002000+0000)

### clayrat-dns (T1568.002)

- `9000808` MALWARE ClayRat C2 DNS packwatheboss.lol — 127.0.0.1 → 1.1.1.1:53 (2025-08-15T23:20:00.000000+0000)

### kerberoasting (T1558.003)

- `1100011` [ATTACK] Kerberoasting (TGS-REQ) — 127.0.0.1 → 10.10.0.2:88 (2025-08-15T23:20:00.002000+0000)
- `1100011` [ATTACK] Kerberoasting (TGS-REQ) — 127.0.0.1 → 10.10.0.2:88 (2025-08-15T23:20:00.000000+0000)

### asrep-roast (T1558.004)

- `1100012` [ATTACK] AS-REP roasting (AS-REQ burst) — 127.0.0.1 → 10.10.0.2:88 (2025-08-15T23:20:04.002000+0000)

### password-spray (T1110.003)

- `1100010` [ATTACK] Kerberos password spray (burst AS-REQ) — 127.0.0.1 → 10.10.0.2:88 (2025-08-15T23:20:06.000000+0000)

### smb-enum (T1087/T1018)

- `1100013` [ATTACK] SMB enum (session burst) — 127.0.0.1 → 10.10.0.2:445 (2025-08-15T23:20:08.002000+0000)

### ldap-enum (T1087/T1018)

- `1100014` [ATTACK] LDAP enum (search burst) — 127.0.0.1 → 10.10.0.2:389 (2025-08-15T23:20:12.002000+0000)

### dcsync (T1003.006)

- `1100015` [ATTACK] DCSync attempt (DRSUAPI) — 127.0.0.1 → 10.10.0.2:445 (2025-08-15T23:20:00.000000+0000)

## Wnioski i luki

- **clayrat-beacon** (T1071.001): ✅ wykryte.
- **clayrat-ws** (T1071.001): ✅ wykryte.
- **clayrat-dns** (T1568.002): ✅ wykryte.
- **kerberoasting** (T1558.003): ✅ wykryte.
- **asrep-roast** (T1558.004): ✅ wykryte.
- **password-spray** (T1110.003): ✅ wykryte.
- **smb-enum** (T1087/T1018): ✅ wykryte.
- **ldap-enum** (T1087/T1018): ✅ wykryte.
- **dcsync** (T1003.006): ✅ wykryte.

## Poprawki reguł (wnioski z walidacji)

- `clayrat_c2.rules` sid 9000802: usunięto `nocase` z `http.host` — Suricata 7.0.10 normalizuje bufor hosta do małych liter; `nocase` łamał dopasowanie (reguła nigdy nie triggerowała). Zweryfikowane replayem (PARTIAL → PASS).

## Źródła reguł

- `Narzedzia/clayrat_c2.rules` (ClayRat C2 — beacon HTTP, WS, DNS, IP)
- `Lab/RedTeam_AD/detection/local.rules` (AD lab — Kerberos/LDAP/SMB/DRSUAPI)
- `Lab/RedTeam_AD/detection/sigma/` (5 reguł Sigma)

Związane: [[Detekcja]] · [[ClayRat_Android_RAT]] · [[Faza2_Windows_AD]]
