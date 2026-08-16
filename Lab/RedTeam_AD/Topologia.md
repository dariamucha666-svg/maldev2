---
title: "Topologia labu Red Team AD"
date: 2026-08-16
tags: [lab, redteam, topologia]
---

# Topologia — Red Team AD Lab

```
                        Docker host (.133)
   +--------------------------------------------------+
   |  siec bridge: labnet  10.10.0.0/24               |
   |                                                   |
   |   +----------+       +-----------------------+    |
   |   |  kali    | ----> |  dc01 (Samba AD DC)   |    |
   |   | 10.10.0.10|      |  10.10.0.2            |    |
   |   | (attacker)|      |  XMASK.LAB            |    |
   |   +----------+       |  Kerberos:88 LDAP:389 |    |
   |        |             |  SMB:445  DNS:53      |    |
   |        |             +-----------------------+    |
   |        |                                           |
   |        +-----> dvwa (10.10.0.20)  DVWA             |
   |        +-----> juice-shop (10.10.0.21)             |
   +--------------------------------------------------+

Legenda:
  kali -> dc01 : enum LDAP/SMB, Kerberos (AS-REP, Kerberoast, spray), DCSync
  kali -> dvwa / juice-shop : testy web (SQLi, XSS, ...)
```

## Porty DC (wewnątrz labnet)

| Port | Usługa |
|------|--------|
| 53 | DNS (forwarder 1.1.1.1) |
| 88 | Kerberos |
| 135/139/445 | RPC / NetBIOS / SMB |
| 389/636 | LDAP / LDAPS |
| 464 | kpasswd |
| 3268/3269 | Global Catalog |

## Izolacja

- Lab działa w osobnej sieci bridge, bez publikowania portów na hoście.
- Internet z DC/Kali tylko przez DNS forwarder DC (1.1.1.1) — brak wejścia z zewnątrz.
- Sekrety poza vaultem: `/root/redteam-lab-secrets/` (nie w gicie).
