---
title: "Detekcja i purple team"
date: 2026-08-16
tags: [lab, redteam, purpleteam, suricata, sigma]
---

# Detekcja i purple team — Red Team AD Lab

Warstwa detekcji dla labu XMASK.LAB: **Suricata** (sieciowa, na żywo) + **Sigma** (logi Windows, faza 2).

Powiązane: [[Status_Lab]] · [[Playbook_AD]] · [[Wiedza/Obrona/Obrona_MOC]]

## Suricata (IDS na żywo)

Nasluchuje bridge'u labnet (`br-<net_id>`, zwykle `br-13e1412ca9ef`).

```bash
# start (detekcja labnet automatycznie)
bash /root/obsidian-vault/Lab/RedTeam_AD/detection/run-suricata.sh

# alerty
tail -f /var/log/suricata/fast.log
grep '"event_type":"alert"' /var/log/suricata/eve.json | jq -r '.alert.signature' | sort | uniq -c
```

Reguly: `detection/local.rules` (kopiowane do `/etc/suricata/rules/local.rules`).

## Zweryfikowana detekcja (demo 2026-08-16)

| Atak | Reguła (sid) | Wykryty |
|------|--------------|---------|
| Password spray (kerbrute) | 1100010 — burst AS-REQ | ✅ |
| SMB enum (netexec) | 1100013 — session burst | ✅ |
| LDAP enum (ldapsearch) | 1100014 — search burst | ✅ |
| Kerberos/SMB/LDAP/DNS baseline | 1100001-1100005 | ✅ |

Wynik demo: **230 alertów** (spray + SMB + LDAP + baseline).

## Reguły Sigma (logi Windows — faza 2)

W `detection/sigma/`:

| Plik | Technika | ID |
|------|----------|-----|
| ad_password_spray.yml | Password spraying | T1110.003 |
| ad_asrep_roasting.yml | AS-REP roasting | T1558.004 |
| ad_kerberoasting.yml | Kerberoasting | T1558.003 |
| ad_dcsync.yml | DCSync | T1003.006 |
| ad_smb_ldap_enum.yml | SMB/LDAP enum | T1087 / T1018 |

Te reguły dzialaja na logach Windows (Security) — do użycia w fazie 2 (Windows AD).

## Przepływ purple team

1. Wykonaj technikę (np. `kerbrute passwordspray`).
2. Sprawdz detekcję: `grep 'ATTACK' /var/log/suricata/fast.log`.
3. Popraw regułę, jeśli nie wykryto.
4. Mapuj na ATT&CK (tabela wyżej).
