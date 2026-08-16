---
title: "Prompt startowy — OPSEC check"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, prompt, start, hardening, szablon]
status: active
category: prompt
---

# Prompt startowy — OPSEC check

Wklej ten prompt do asystenta **za każdym razem, gdy odpalasz maszynę** (albo wracasz do pracy).
Zrobi rutynową kontrolę i utwardzanie OPSEC na `vserver959630` — bez ruszania tego, co działa.

> Jak używać: skopiuj cały blok poniżej i wyślij. Asystent przeczyta
> [[Hardening_vserver959630]] i [[Zabezpieczenia_po_prostu]] jako baseline.

```text
Jesteś asystentem na moim VPS `vserver959630` (Ubuntu 24.04, lab C2 / pipeline / analiza). Pracujesz w vaultcie Obsidian: `/root/obsidian-vault`. Zanim cokolwiek zmienisz, przeczytaj baseline: `OPSEC/Hardening_vserver959630.md` i `OPSEC/Zabezpieczenia_po_prostu.md`.

Wykonaj rutynową kontrolę OPSEC. Kolejność:

1. REKONESANS (tylko odczyt)
   - System: `hostnamectl`, `uname -r`, `uptime`, `apt list --upgradable` (czy są zaległe aktualizacje).
   - Nasłuchy: `ss -tulpn` — wypisz wszystko, co słucha na `0.0.0.0` lub `*`.
   - Firewall: `ufw status verbose`.
   - SSH: `sshd -T | grep -Ei 'permitrootlogin|passwordauthentication|x11forwarding|maxauthtries|kbdinteractiveauthentication'`.
   - fail2ban: `fail2ban-client status sshd` (ile zbanowanych).
   - Logowania: `last -n 10` (udane), `lastb -n 10` (nieudane), `who` / `w` (kto teraz).
   - Użytkownicy z shellem: `grep -E '(/bin/.*sh|/bin/bash)' /etc/passwd`.

2. SPRAWDŹ BASELINE i NAPRAW (jeśli odbiega)
   - SSH (plik `/etc/ssh/sshd_config.d/00-opsec.conf`): `PermitRootLogin prohibit-password`, `PasswordAuthentication no`, `X11Forwarding no`, `MaxAuthTries 3`. Po zmianie: `sshd -t` i `systemctl reload ssh`.
   - Sysctl (plik `/etc/sysctl.d/99-opsec.conf`): redirects / source-route = 0, `tcp_syncookies = 1`. Po zmianie: `sysctl --system`.
   - Dashboard: `systemctl cat ioc-dashboard.service` musi mieć `DASH_BIND=127.0.0.1` (nie `0.0.0.0`). Zweryfikuj `ss -tlnp | grep 8080`.
   - UFW: default `deny (incoming)`. Porty labu NIE mogą być na `Anywhere` — dozwolone tylko: `22` (Anywhere, chroniony fail2ban) i `31337` (tylko IP operatora). `8080/443/8443/4444/9999/8765` mają być zamknięte.
   - `fail2ban` aktywny, `unattended-upgrades` włączone (`systemctl is-active`, `apt-config dump`).

3. IP OPERATORA
   - Wykryj moje obecne IP (z `w` / `last` — adres, z którego jestem zalogowany).
   - Sprawdź, czy reguła `31337` zawiera to IP. Jeśli nie: `ufw allow from <IP> to any port 31337 proto tcp`.

4. WYKRYJ NOWOŚCI (zgłoś, nie naprawiaj sam)
   - Nowe nasłuchy `0.0.0.0`, nowe reguły `Anywhere`, nowe konta z shellem, nowe klucze w `/root/.ssh/authorized_keys`, nowe wpisy crontab.
   - Wypisz je w raporcie i zapytaj, zanim coś zmienisz.

5. RAPORT + ZAPIS
   - Tabela: co OK / co naprawiłeś / co zostało do mojej decyzji.
   - Dopisz wpis z dzisiejszą datą na końcu `OPSEC/Hardening_vserver959630.md`.

Zasady bezpieczeństwa:
- Nie ruszaj tuneli Cloudflare (dash / c2 / dsh → 127.0.0.1) — mają dalej działać.
- Nie zmieniaj `ip_forward` ani `rp_filter` (Docker tego potrzebuje).
- Nie wyłączaj ani nie zamykaj SSH (port 22) — to moje jedyne wejście.
- Wszystko, co mogłoby mnie odciąć (np. zamknięcie 22, zmiana reguł poza 31337/IP) — najpierw zapytaj.
```

## Co sprawdza prompt (skrót)

| Krok | Co robi |
|------|---------|
| 1. Rekonesans | system, nasłuchy, firewall, SSH, fail2ban, logowania, konta |
| 2. Baseline | naprawia SSH/sysctl/dashboard/UFW jeśli odbiega od [[Hardening_vserver959630]] |
| 3. IP operatora | dopisuje Twoje obecne IP do reguły 31337 |
| 4. Nowości | wykrywa nowe porty/reguły/konta/klucze/cron i pyta zanim zmieni |
| 5. Raport | tabela + dopisuje wpis do logu hardeningu |

## Powiązane

- [[Hardening_vserver959630]] — baseline (co już ustawione)
- [[Zabezpieczenia_po_prostu]] — zasady w pigułce
- [[Checklist_OPSEC]] — manualna lista kontrolna
- [[OPSEC/README|OPSEC — mapa]]
