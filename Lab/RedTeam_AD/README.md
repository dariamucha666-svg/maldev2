---
title: "Red Team AD Lab"
date: 2026-08-16
tags: [lab, redteam, active-directory, docker]
category: lab
---

# Red Team AD Lab — XMASK.LAB

Legalny, izolowany lab do ćwiczenia pełnego łańcucha ataków na Active Directory
(na Samba AD — zgodnym z AD DS: Kerberos/LDAP/SMB/DNS) oraz testów aplikacji web.
Wszystko na własnej infrastrukturze, w Dockerze, odizolowane od pipeline.

Powiązane: [[Wiedza/Ataki/Active_Directory_Ataki]] · [[Wiedza/RedTeam/RedTeam_MOC]] · [[Lab/Hosts]]

## Topologia

| Kontener | IP | Rola |
|----------|-----|------|
| dc01 | 10.10.0.2 | Kontroler domeny XMASK.LAB (Samba AD DC) |
| kali | 10.10.0.10 | Atakujący (impacket, netexec, responder, bloodhound, kerbrute, john) |
| dvwa | 10.10.0.20 | Cel web: DVWA |
| juice-shop | 10.10.0.21 | Cel web: OWASP Juice Shop |

Sieć bridge `labnet` = 10.10.0.0/24, izolowana (internet tylko przez DNS forwarder DC).

## Konta domeny (celowo słabe)

| Konto | Rola w łańcuchu |
|-------|-----------------|
| alice | niskoprzywilejowane (znane hasło) — punkt startowy |
| bob / carol | password spray |
| svc_sql (SPN MSSQLSvc/...) | Kerberoasting |
| svc_backup (SPN backup/...) | Kerberoasting |
| asrep_user (no-preauth) | AS-REP roasting |

**Hasła NIE są w vaultcie** — trzyma je `/root/redteam-lab-secrets/env` (poza gitem).
Wordlista do crackowania: `/root/redteam-lab-secrets/lab-passwords.txt` (montowana do Kali jako `/opt/wordlists/lab-passwords.txt`).

## Uruchomienie

```bash
# 1. wygeneruj sekrety (poza vaultem)
bash /root/redteam-lab-secrets/gen.sh

# 2. build + start
cd /root/obsidian-vault/Lab/RedTeam_AD
docker compose --env-file /root/redteam-lab-secrets/env up -d --build

# 3. sprowizjonuj konta domeny (hasła z env)
set -a; . /root/redteam-lab-secrets/env; set +a
docker exec -i -e ALICE_PASSWORD -e BOB_PASSWORD -e CAROL_PASSWORD   -e SVC_SQL_PASSWORD -e SVC_BACKUP_PASSWORD -e ASREP_PASSWORD   dc01 bash -s < /root/obsidian-vault/Lab/RedTeam_AD/dc01/provision-users.sh
```

## Wejście do Kali

```bash
docker exec -it kali bash
```

## Struktura

- `docker-compose.yml` — topologia
- `dc01/` — Dockerfile, entrypoint.sh (provision domeny), provision-users.sh (konta)
- `kali/` — Dockerfile (narzędzia), krb5.conf
- `.env.example` — wzór (bez haseł)

Zobacz: [[Topologia]] · [[Playbook_AD]] · [[Status_Lab]] · [[Detekcja]]
