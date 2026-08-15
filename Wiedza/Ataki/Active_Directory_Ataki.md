---
title: "Ataki na Active Directory / Windows"
date: 2026-08-15
tags: [wiedza, ataki, active-directory, windows]
category: atak
---

# Ataki na AD / Windows

Większość kampanii po wejściu do sieci celuje w AD (domena → domain admin).

## Kluczowe ataki

| Atak | Jak | Narzędzia | Obrona |
|------|-----|-----------|--------|
| Pass-the-Hash (T1550.002) | reużycie NTLM hash | Mimikatz, Impacket, CME | Credential Guard, LAPS, segmentacja |
| Pass-the-Ticket (T1550.003) | reużycie Kerberos ticket | Rubeus, Mimikatz | monitor 4769, krbtgt rotation |
| Kerberoasting (T1558.003) | TGS dla SPN → crack | Rubeus, Impacket | silne hasła (30+), gMSA |
| AS-REP Roasting (T1558.004) | brak preauth | Rubeus | wyłącz "no preauth" |
| DCSync (T1003.006) | replikacja haseł z DC | Mimikatz, secretsdump | Tier 0 hardening, monitor 4662 |
| Golden Ticket (T1558.001) | forge TGT (krbtgt hash) | Mimikatz | krbtgt reset, monitor |
| Silver Ticket (T1558.002) | forge TGS | Mimikatz | monitor |
| BloodHound paths | mapowanie ścieżek do DA | SharpHound/BloodHound | monitor SAM-R/LDAP, honeytokens, ACL review |
| NTLM relay | relay do SMB/LDAP | ntlmrelayx (Impacket) | SMB signing, LDAPS/EPA, blokada LLMNR/mDNS |
| LLMNR/NBT-NS poisoning | przechwycenie hasha | Responder | wyłącz LLMNR/mDNS, monitor |
| GPO abuse | złe GPO | — | review GPO, monitor |
| Zerologon (CVE-2020-1472) | exploit DC | — | patch (historyczny przykład edge) |

## Tiering (najważniejsza obrona)

- **Tier 0** (DC, PKI, identity) — tylko dedykowane konta admin.
- **Tier 1** (serwery) — admin serwerów.
- **Tier 2** (workstations) — admin stacji.
- Zasada: konto z niższego tieru nie loguje się na wyższy tier (logon restrictions, PAW).

## Detekcja

- 4624 type 3/10 (sieciowe loginy), 4769 (Kerberos service ticket), 4662 (DC replication),
  4720 (user create), 4732 (group add).
- Monitor BloodHound-like: masowe zapytania SAM-R, LDAP enum.
- Honeytokens (fałszywe konta admin — alarm przy użyciu).
