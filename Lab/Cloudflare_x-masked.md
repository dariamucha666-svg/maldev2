---
tags: [lab, cloudflare, web]
updated: 2026-08-16
---

# Cloudflare — x-masked.com

Powiązane: [[Daily/2026-08-15]] · [[Lab/Hosts]] · [[Lab/Cloudflare_zamaskowani]]

## Stan 2026-08-16

| Pole | Wartość |
|------|---------|
| Zone | `x-masked.com` |
| Status | active |
| Zone ID | `a127a7945231e9a997c3ad64352e7789` |
| Nameservery | `raegan.ns.cloudflare.com` / `shane.ns.cloudflare.com` |
| Worker | `x-masked` (Workers Static Assets, assets-only) |
| Account ID | `37632c9870c91b71236843c034a107b1` (konto dariamucha666@gmail.com) |
| Custom domains | `x-masked.com`, `www.x-masked.com` (worker `maskencrypt` ma `app.maskencrypt.eu` — osobno) |
| workers.dev | `https://x-masked.dariamucha666.workers.dev` |

## Kod i deploy (od 16.08 — bez .133)

- Kod: `/root/Obsidian/x-masked-optimized/` (na `.139`) — git lokalny, gotowy do push na GitHub
- Deploy: `cd /root/Obsidian/x-masked-optimized && export CLOUDFLARE_API_TOKEN=… && ./deploy.sh`
  (token: `/root/.lab-keys.sh` / `.grok/config.toml` — UWAGA: wcześniejszy token `cfk_…` był nieważny)
- `.133` już **nie** serwuje strony — `/root/x-masked` na `.133` można usunąć (`rm -rf`)

## Optymalizacja (16.08)

- Obrazy: hero desktop 606→184 KB (AVIF), mobile 645→189 KB (AVIF), fallback WebP q72
- Fonty: Google Fonts (7 wag) → self-host 4 × variable woff2 (~96 KB)
- CSS: 13.9 KB → 9.3 KB minified, wcięty w HTML (0 requestów), wycięte martwe reguły
- JS: terser 6.7 → 5.0 KB (zachowanie identyczne)
- Cache: `_headers` — statyki `max-age=86400, stale-while-revalidate=604800`, HTML `max-age=0`
- Transfer 1. wejście: ~865 KB → ~243 KB (−72%), requesty 9 → 6, zero domen zewnętrznych
- Ostatnia wersja workera: `0ab1f208-a3ee-4a4e-bdd2-4c1740b55e38`

Landing = klon [High Five / Manus](https://highfive-4u7oedif.manus.space/) bez trackera Manus.

## Funkcje (16.08)

Dwa paski wyszukiwania:
- **Górny (czarny) — jednorazowa zaszyfrowana wiadomość**: bez hasła i bez czatu.
  Użytkownik wpisuje kontakt/wiadomość → szyfrowanie w przeglądarce (AES-256-GCM,
  losowy klucz, **klucz nie opuszcza przeglądarki**) → `POST /api/notes` na
  **app.maskencrypt.eu** (D1, burn-once DELETE RETURNING) → na Telegram przez
  **@XMasked_bot** (id 8854215986) na czat `8353275197` leci **link**
  `https://app.maskencrypt.eu/v/<id>#<klucz>`. Po odczytaniu wiadomość znika
  (drugi odczyt = 404 GONE), TTL 24h. Czerwony placeholder pisze się po wejściu.
- **Dolny (biały) — czat AI**: po kliknięciu czat się rozwija, asystent pisze powoli
  i pyta „Linki? Kontakt? Boty na TG? Chcesz może stronę internetową?". Komendy:
  `linki`, `kontakt`, `boty`, `strona`, `pomoc`. `maska` → wskazówka do górnego paska.
- Sekrety workera: `TELEGRAM_BOT_TOKEN` (token @XMasked_bot), `TELEGRAM_CHAT_ID`
  (`8353275197`) — `wrangler secret put`, nie ma ich w repo.
- Uwaga: Bot Fight Mode strefy blokuje `/api/contact` dla nie-przeglądarkowych UA
  (403/1010); przeglądarki przechodzą.
- Ostatnia wersja workera: `09fb14ce-5783-4b44-b2f1-27d5cc864cb2`.
- Worker `maskencrypt` (app.maskencrypt.eu) — redeploy 16.08 (wersja `927f7a2d`):
  wiadomość po odszyfrowaniu **znika też z ekranu** (countdown 6 s, potem „Maska pusta").
  Kod: `/root/Obsidian/maskencrypt/` (index.js + public/, D1 `1c9e8c3b-36c2-447a-9131-feab818fbd01`).
  Serwer kasuje atomowo przy odczycie (DELETE RETURNING) — drugi odczyt = 404 GONE.

