---
tags:
  - obsidian
  - workflow
  - vault
updated: 2026-08-15
---

# Obsidian Workflow

Powiązane: [[Dashboard]] · [[Dziennik_Lab]] · [[Home]]

## Gdzie jest vault

| Miejsce | Ścieżka |
|---------|---------|
| Kali (ten host) | `/home/kali/obsidian-vault` |
| VPS C2 #1 | `/root/obsidian-vault` |

Na `.133` nie ma binarki `/opt/Obsidian` (został profil AppArmor). Vault to zwykły folder Markdown.

```bash
# Kali
obsidian /home/kali/obsidian-vault
# albo: Obsidian → Open folder as vault
```

## Struktura

```
_Dashboard/     Home.md  Dashboard.md  QuickStart.md
_Templates/     Analiza_Malware  Dziennik_Lab  Projekt  IOC
Projekty/       Infrastruktura_C2/  Pipeline_Analizy/  Analiza_Backdoora_Go/  Wlasny_Stealer/
Analizy/        Malware/  Raporty/  IOC/
Dzienniki/2026/ 2026-08.md          # widok miesiąca
Daily/          YYYY-MM-DD.md       # bot + Calendar (nie ruszać)
Zasoby/         Narzedzia.md  Linki.md  Dokumentacja.md
Obsidian/       Plugins.md
Inbox/  Lab/  Logs/  Narzedzia/  Screenshots/  XMask/
Backlog.md      Kanban.md
```

Wiki-linki `[[Nazwa]]` działają po **nazwie pliku**. `[[Pipeline_Analizy]]` → `Projekty/Pipeline_Analizy/Pipeline_Analizy.md`.

## Jak pisać

1. Nowa sesja → `Daily/YYYY-MM-DD.md` (szablon Dziennik_Lab) + wpis w [[Dziennik_Lab]].
2. Nowa próbka → QuickAdd **Nowa analiza malware** + **Nowy IOC**.
3. Frontmatter: `status`, `priority`, `tags`, `hash`, `category` — to karmi [[Dashboard]].
4. Tagi: `projekt`, `malware`, `ioc`, `pipeline`, `rat`, `stealer`, `backdoor`, `daily`.
5. **Hasła i tokeny poza vaultem.**
6. Bot Telegram: `Inbox/` i `Daily/` zostają. [[Telegram_Obsidian_Bot]]

## Auto-log na `.133`

Na VPS działa samo, bez ręcznego kopiowania:

| Źródło | Gdzie ląduje |
|--------|----------------|
| Interaktywny bash (`script`) | `Logs/terminal_YYYY-MM-DD.log` |
| Koniec `pipeline.sh` | `Analizy/Raporty/analiza_YYYY-MM-DD_HH-MM.md` + `Logs/pipeline_*.log` |
| `journalctl -u sliver` (cron co godz.) | `Logs/sliver_YYYY-MM-DD.log` |

Strażnik w `.bashrc`: tylko sesja interaktywna + TTY, zmienna `UNDER_OBSIDIAN_SCRIPT` — bez pętli. SSH z jedną komendą (`ssh host 'cmd'`) nie wchodzi w `script`.

Szczegóły: [[Obsidian_Auto_Log]]

## Sync Kali ↔ VPS

Po większej edycji:

```bash
rsync -av --exclude '.trash' \
  /home/kali/obsidian-vault/ root@5.175.189.133:/root/obsidian-vault/
```

`alwaysUpdateLinks: true` w `.obsidian/app.json`.
