---
tags:
  - cloudflare
  - tunnel
  - dns
updated: 2026-08-14
---

# Cloudflare — konfiguracja

Powiązane: [[Infrastruktura_C2]] · [[Sliver_C2]]

## Tunele

| Nazwa | UUID | Utworzony | Połączenia (14.08) |
|-------|------|-----------|--------------------|
| `maskchat-c2` | `9608db38-e426-4efb-9145-e93a3c733680` | 2026-08-11 00:48 UTC | 2×ams01, 1×ams15, 1×ams21 |
| `c2-drugi` | `b93f944b-72aa-47d4-9289-66a8383f61c2` | 2026-08-11 04:47 UTC | 1×ams08/15/17/18 |

## Routing (C2 #1)

Plik: `/root/.cloudflared/config.yml`

```yaml
tunnel: 9608db38-e426-4efb-9145-e93a3c733680
credentials-file: /root/.cloudflared/9608db38-e426-4efb-9145-e93a3c733680.json

ingress:
  - hostname: c2.maskencrypt.eu
    service: https://127.0.0.1:443
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s
  - service: http_status:404
```

Schemat:

```
DNS (Cloudflare)
  → tunel maskchat-c2
    → cloudflared na VPS (metrics 127.0.0.1:20241)
      → sliver-server HTTPS 127.0.0.1:443
```

Dzięki temu listener 443 **nie** wisi na `0.0.0.0`. Publiczny IP `5.175.189.133` nie musi być w rekordzie A domeny C2.

## Proces vs systemd

- `systemctl is-active cloudflared` → **inactive**
- Proces `cloudflared` **działa** (PID 554090, listen `127.0.0.1:20241`)
- Pliki: `/root/.cloudflared/{config.yml,cert.pem,<uuid>.json}`

Jeśli tunel padnie po reboocie — dopiąć unit albo sprawdzić, czym ten PID jest startowany (nie jest to `cloudflared.service`).

## DNS

| Host | Tunel | Origin |
|------|-------|--------|
| `c2.maskencrypt.eu` | `maskchat-c2` | `https://127.0.0.1:443` (Sliver) |
| `c2-drugi.maskencrypt.eu` | `c2-drugi` | C2 #2 (`5.175.189.139`) |

## Tokeny

Token API Cloudflare leży poza vaultem (nie kopiować do notatek). Certyfikat origin: `/root/.cloudflared/cert.pem`.
