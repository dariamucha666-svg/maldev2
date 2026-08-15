---
title: "Git sync Kali ↔ .133"
date: 2026-08-15
tags: [obsidian, git, workflow]
status: active
---

# Git sync

Bez GitHuba. Źródło prawdy: gołe repo na VPS.

| Gdzie | Ścieżka |
|-------|---------|
| Working (pipeline, bot) | `/root/obsidian-vault` |
| Bare (push/pull) | `/root/obsidian-vault.git` |
| Kali | `/home/kali/obsidian-vault` |
| Remote | `vps133:/root/obsidian-vault.git` |

## Automatyka

| Co | Jak |
|----|-----|
| VPS commit + push | `Narzedzia/git_autocommit.sh` · cron `*/15` · `/etc/cron.d/obsidian-git` |
| Alias | `/root/obsidian-auto-commit.sh` (to samo) |
| Kali pull/push | wtyczka **Obsidian Git** (co 10 min, pull na starcie, push po zapisie) |

Hasła i `Logs/*.log` nie idą do Gita (`.gitignore`).

## GitHub (opcjonalnie, później)

```bash
# na VPS, po utworzeniu pustego repo
git -C /root/obsidian-vault.git remote add github https://github.com/USER/obsidian-vault.git
git -C /root/obsidian-vault.git push github main
```

Nie commituj tokenów.

## Ręcznie z Kali

```bash
git -C /home/kali/obsidian-vault pull --rebase
git -C /home/kali/obsidian-vault push
```
