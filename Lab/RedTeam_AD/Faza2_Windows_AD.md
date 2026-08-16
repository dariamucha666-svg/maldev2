---
title: "Faza 2 — Windows AD (plan)"
date: 2026-08-16
tags: [lab, redteam, active-directory, windows, faza2]
---

# Faza 2 — Windows AD (plan)

Cel: przenieść łańcuch z Samby na prawdziwy Windows AD (promocja wlasnego VPS do DC),
gdzie natywnie działają: DCSync, Kerberoasting, AS-REP, Mimikatz, Rubeus, SharpHound.

Powiązane: [[Status_Lab]] · [[Detekcja]] · [[Lab/Hosts]]

## Decyzja o hoście

| Host | Status | Uwaga |
|------|--------|-------|
| .57 | Windows Server 2022 Eval (RE box) | promocja do DC **zakłóci RE** — tylko za zgodą |
| .781193 | wolny, niełączony | **preferowany**, jeśli da się postawić Windows |

Rekomendacja: nowy/izolowany Windows Server na .781193 (lub inny VPS), nie ruszamy .57 bez zgody.

## Kroki — kontroler domeny

1. Windows Server 2022 (Eval), statyczny IP, hostname `DC01`.
2. `Install-ADDSForest -DomainName xmask.lab -DomainNetbiosName XMASK -InstallDns` (PowerShell).
3. Konta jak w Sambie: alice (low-priv), svc_sql/svc_backup (SPN), asrep_user (no-preauth).
4. Klient Windows 10/11 dołączony do domeny (target do lateral movement).

## Natywny łańcuch ataku (działa na Windows AD)

| Technika | Narzędzie | Uwaga |
|----------|-----------|-------|
| DCSync | Mimikatz `lsadump::dcsync` / secretsdump | działa (DRSUAPI Windows) |
| Kerberoasting | Rubeus `kerberoast` / GetUserSPNs | działa (checksum OK) |
| AS-REP | Rubeus `asreproast` / GetNPUsers | działa (no-preauth honorowane) |
| BloodHound | SharpHound + BloodHound CE | mamy obrazy specterops/bloodhound + neo4j |
| Credential dumping | Mimikatz sekurlsa::logonpasswords | — |

## Detekcja (purple) w fazie 2

- Sysmon + Advanced Audit Policy na DC.
- Eventy Windows → reguły Sigma w `detection/sigma/` ([[Detekcja]]).
- Suricata na segmencie Windows (jak w fazie 1).

## Status

- [ ] Wybór VPS na DC (decyzja użytkownika)
- [ ] Promocja DC + klient
- [ ] Natywny łańcuch + detekcja
