---
title: "Hardening vserver959630"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, hardening, lab, serwer]
status: active
category: hardening
---

# Hardening vserver959630

Zapis zmian OPSEC wykonanych na VPS `vserver959630` (Ubuntu 24.04, główny lab / pipeline / C2).

## Wykonane (2026-08-16)

### SSH
- `PermitRootLogin prohibit-password` — root tylko kluczem (klucze ED25519 już były w `/root/.ssh/authorized_keys`).
- `PasswordAuthentication no` — hasła wyłączone (trwały brute-force, teraz bez skutku).
- `X11Forwarding no`, `MaxAuthTries 3`, `LoginGraceTime 30`, `ClientAliveInterval 300` / `ClientAliveCountMax 3`.
- Plik: `/etc/ssh/sshd_config.d/00-opsec.conf`.

### Kernel (sysctl)
- Wyłączone ICMP redirects, source routing, ping broadcast; `tcp_syncookies` włączone.
- Plik: `/etc/sysctl.d/99-opsec.conf`.

### Firewall (UFW)
- Usunięte zduplikowane reguły `8443` i `9999` (bez `/tcp`).
- Stan: `Default: deny (incoming)`, logging `on (low)`.

### Już działało
- `fail2ban` (jail `sshd`) — aktywny, ~97 banów.
- `unattended-upgrades` — włączone, 0 zaległych aktualizacji.

## Porty — zamknięte / ograniczone (2026-08-16)

| Port | Rola | Co zrobiono |
|------|------|-------------|
| 8080 | ioc-dashboard | przepięty na 127.0.0.1 (był 0.0.0.0); reguła usunięta. Dostęp tylko przez `dash.maskencrypt.eu` (Cloudflare tunel) |
| 31337 | sliver multiplayer | ograniczony do IP operatora (83.21.x.x); Anywhere usunięte |
| 443 | https/tunnel | reguła usunięta (tunel i tak celuje w 127.0.0.1:443) |
| 8443 | sliver tcp stage AES | reguła usunięta (bez nasłuchu) |
| 4444 | własny RAT C2 | reguła usunięta (bez nasłuchu) |
| 9999 | ? | reguła usunięta (bez nasłuchu) |
| 8765 | ? | reguła usunięta (bez nasłuchu) |
| 22 | SSH | zostaje: tylko klucz + fail2ban |

Tunele Cloudflare (dash / c2 / dsh → 127.0.0.1) dalej działają — nic nie zostało zerwane.

Uwaga: IP operatora jest dynamiczne. Po zmianie IP dopisz je do 31337:
`ufw allow from <IP> to any port 31337 proto tcp`.

## Powiązane

- [[OPSEC/README|OPSEC — mapa]] · [[Zabezpieczenia_po_prostu]] · [[Urzadzenia_i_siec]]
