---
title: "Dostęp do Windows AD DC (.57)"
date: 2026-08-16
tags: [lab, redteam, windows, dostep]
---

# Dostęp do Windows AD DC (.57)

DC: `WIN-T5BVVHUNVJI.xmask.lab` (`5.175.189.57`), domena `XMASK.LAB`.

## WinRM — Kerberos (NTLM wyłączone po promocji)

Po promocji DC WinRM odrzuca NTLM (reklamuje tylko `Negotiate`/Kerberos).
Dostęp przez Kerberos:

1. `/etc/krb5.conf` na .133 wskazuje `XMASK.LAB -> 5.175.189.57` (KDC).
2. `kinit administrator@XMASK.LAB` (hasło w `/root/run57.py`, poza vaultem).
3. Helper: `python3 /root/winrm57.py <script.ps1>` (template: [[winrm57.py.example]]).

## Firewall (zawężony 2026-08-16)

52 reguły wejściowe (AD/LDAP/Kerberos/SMB/RPC/DNS/RDP/WinRM/WMI/Replication)
mają `RemoteAddress = 5.175.189.133 | 5.175.189.139 | 5.175.189.57 | 127.0.0.1`.
Brak reguł `Any`. Zawężenie zrobione skryptem `/tmp/fw_restrict.ps1` przez `winrm57.py`.

## Pułapki (zapisane, żeby nie szukać drugi raz)

- SPN WinRM na DC to `HTTP/WIN-T5BVVHUNVJI.xmask.lab` (nie `WSMAN/...`) → wymagany `kerberos_hostname_override`.
- pywinrm wymaga modułu `pykerberos` (instalacja: `pip install --break-system-packages pykerberos` + `apt install libkrb5-dev python3-dev gcc`).
- Bez override: błąd `Server not found in Kerberos database` (szuka HTTP/5.175.189.57).
- DSRM: `/root/redteam-lab-secrets/windows-dc.env` (poza vaultem).

Powiązane: [[Faza2_Windows_AD]] · [[Status_Lab]] · [[Lab/Hosts]]
