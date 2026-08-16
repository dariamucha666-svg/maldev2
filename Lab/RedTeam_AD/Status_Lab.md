---
title: "Status labu Red Team AD"
date: 2026-08-16
tags: [lab, redteam, active-directory, status]
---

# Status labu — wyniki weryfikacji (2026-08-16)

Powiązane: [[README]] · [[Topologia]] · [[Playbook_AD]]

## Co działa (zweryfikowane)

| Technika | Narzędzie | Wynik |
|----------|-----------|-------|
| Skanowanie | nmap | 9/9 portów DC otwarte (53,88,135,139,389,445,464,636,3268) |
| Enum SMB (NTLM) | netexec smb --shares | alice:<ALICE_PASSWORD z env> -> sysvol / netlogon / IPC$ |
| Enum LDAP (simple bind) | ldapsearch | 10 kont wyliczone |
| Password spray | kerbrute passwordspray | bob i carol : <SPRAY_PASSWORD> (2/7) |
| Kerberos TGT | kinit alice | TGT wydane (pre-auth dziala) |
| Enum SPN | impacket-GetUserSPNs | svc_sql, svc_backup (SPN widoczne) |

## Niuanse Samby 4.19 (dzialaja na Windows AD - faza 2)

Flagi i konta sa ustawione poprawnie; to ograniczenia Samba 4.19 + toolchain, nie blad labu.

| Technika | Objaw | Przyczyna |
|----------|-------|-----------|
| Kerberoasting (TGS) | KRB_AP_ERR_INAPP_CKSUM | Samba Heimdal <-> impacket (typy szyfrowania/checksum) |
| AS-REP roasting | KDC_ERR_PREAUTH_REQUIRED | KDC Samby nie honoruje UF_DONT_REQUIRE_PREAUTH (flaga ustawiona: 4260352) |
| DCSync (DRSUAPI) | "byte indices must be integers" | impacket + Python 3.14 (bug typow) |
| BloodHound (NTLM bind) | "session terminated by server" | ldap3 NTLM bind <-> Samba |

Te cztery techniki wymagaja **Windows AD** - to jest cel **fazy 2** (promocja .57 do DC).

## Dostep

- Kali: `docker exec -it kali bash`
- DC: `docker exec -it dc01 bash`
- DVWA: `http://10.10.0.20/` (z Kali)
- Juice Shop: `http://10.10.0.21:3000/` (z Kali)

## Detekcja (purple team) — zweryfikowana

Suricata na bridge'u labnet wykrywa: password spray, SMB enum, LDAP enum (230 alertów w demo).
Reguly Sigma dla logow Windows w `detection/sigma/`. Szczegoly: [[Detekcja]]

## Faza 2 (Windows AD) — WYKONANA ✅

DC: WIN-T5BVVHUNVJI.xmask.lab (5.175.189.57), Windows Server 2022 Eval.
Natywny lancuch dziala (to, co na Sambie 4.19 mialo niuanse):

| Technika | Samba 4.19 | Windows AD |
|----------|-----------|------------|
| DCSync | ⚠️ blad | ✅ pelny zrzut (11 kont) |
| Kerberoasting | ⚠️ checksum | ✅ zcrackowane |
| AS-REP | ⚠️ pre-auth | ✅ zcrackowane |
| BloodHound | ⚠️ NTLM bind | ✅ kolekcja OK |
| Password spray | ✅ | ✅ |

Szczegoly: [[Faza2_Windows_AD]]

1. Promocja Windows Server 2022 (.57) do roli DC (na wlasnym VPS).
2. Dolozenie klienta domeny.
3. Natywny lancuch: Mimikatz, Rubeus, SharpHound/BloodHound, DCSync, Kerberoast, AS-REP.