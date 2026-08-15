---
title: "Infrastruktura C2"
date: 2026-08-14
updated: 2026-08-14
tags: [projekt, c2]
status: in_progress
priority: high
category: infra
---
# Infrastruktura C2

Powiązane: [[Sliver_C2]] · [[Cloudflare_Konfiguracja]] · [[Laboratorium_Windows]] · [[Pipeline_Analizy]] · [[Lab/Hosts]]

## Serwery

| VPS | IP | Hostname | System | Rola |
|-----|-----|----------|--------|------|
| C2 #1 | `5.175.189.133` | `vserver959630` | Ubuntu 24.04.4 | Główny C2 + pipeline analizy |
| C2 #2 | `5.175.189.139` | — | Debian 12 | Backup C2 |
| C2 #3 | `5.175.189.57` | `WIN-T5BVVHUNVJI` | Windows Server 2022 Eval | Laboratorium RE + narzędzia |

**C2 #1 (zweryfikowane 2026-08-14 22:00 UTC):** 5.8 GiB RAM, dysk 38 G / 78% (8.7 G wolne), uptime ~3 dni 18 h, kernel `6.8.0-137-generic`.

## Domeny C2

- `https://c2.maskencrypt.eu` → C2 #1 (tunel `maskchat-c2`)
- `https://c2-drugi.maskencrypt.eu` → C2 #2 (tunel `c2-drugi`)

Routing: DNS Cloudflare → tunel → origin na VPS. Publiczny IP serwerów nie musi być w rekordach A usług C2.

## Cloudflare Tunnel

| Pole | Wartość |
|------|---------|
| Tunel główny | `maskchat-c2` |
| UUID | `9608db38-e426-4efb-9145-e93a3c733680` |
| Tunel backup | `c2-drugi` (`b93f944b-72aa-47d4-9289-66a8383f61c2`) |
| Config | `/root/.cloudflared/config.yml` |
| Ingress | `c2.maskencrypt.eu` → `https://127.0.0.1:443` (`noTLSVerify`) |

Szczegóły: [[Cloudflare_Konfiguracja]]

## Sliver C2 (C2 #1)

- Wersja: **v1.7.3** (`3bbaf805`, compiled 2026-02-24)
- Binarne: `/opt/tools/bin/sliver-server`, klient `/opt/tools/bin/sliver-client`
- Unit: `sliver.service` — **active** od 2026-08-12 14:45 UTC
- Home: `/root/.sliver`

### Porty (stan `ss` 14.08)

| Port | Bind | Rola |
|------|------|------|
| `443/tcp` | `127.0.0.1` | HTTPS listener (tylko localhost — wejście przez Cloudflare) |
| `8443/tcp` | `*` | AES staging (TCP, publiczny bind) |
| `31337/tcp` | `*` | Multiplayer / operator |

Klucz AES staging (lab): `D(G+KbPeShVmYq3t`  
IV AES: `8y/B?E(G+KbPeShV`

> **Higiena:** 31337 i 8443 nasłuchują na wszystkich interfejsach. 443 jest schowany za tunelem. Multiplayer nie jest „zamknięty publicznie” w obecnym `ss` — do twardego UFW jeśli ma zostać tylko VPN/localhost.

Komendy operatorskie: [[Sliver_C2]]

## Inne usługi na C2 #1

| Usługa | Stan | Uwagi |
|--------|------|--------|
| `sshd` | `:22` publiczny | jedyny jawny management |
| `caddy` | `:80` + `127.0.0.1:2019` | domyślny static `/usr/share/caddy` |
| `cloudflared` | proces PID 554090 | systemd unit `inactive` — start ręczny / inny unit |
| `adb` | `127.0.0.1:5037` | brak podłączonego urządzenia |
| pipeline | cron `0 2 * * *` | [[Pipeline_Analizy]] |

## Ścieżki

```
/root/android-pipeline/     # pipeline APK+PE
/root/samples/              # raw, quarantine, reports
/root/obsidian-vault/       # kopia vaultu
/root/.sliver/              # stan Sliver
/root/.cloudflared/         # tunele
/opt/tools/bin/             # sliver-server / sliver-client
```
