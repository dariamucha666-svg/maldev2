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

## Do decyzji — porty wystawione „na świat" (Anywhere)

| Port | Rola | Nasłuch teraz? |
|------|------|----------------|
| 8080 | ioc-dashboard | TAK (0.0.0.0) — wyciek intela |
| 31337 | sliver multiplayer | TAK (0.0.0.0) |
| 22 | SSH | TAK — ale już tylko klucz + fail2ban |
| 443 | https/tunnel | nie (sliver na 127.0.0.1) |
| 8443 | sliver tcp stage AES | nie |
| 4444 | własny RAT C2 | nie |
| 9999 | ? | nie |
| 8765 | ? | nie |

Rekomendacja: dashboard za Cloudflare Access/tunel, 31337 tylko IP operatora, resztę usunąć
albo włączać na żądanie. IP operatora jest dynamiczne — patrz [[Home]].

## Powiązane

- [[OPSEC/README|OPSEC — mapa]] · [[Zabezpieczenia_po_prostu]] · [[Urzadzenia_i_siec]]
