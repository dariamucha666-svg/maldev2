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
| Remote Kali | `vps133:/root/obsidian-vault.git` (`local`) |
| Remote GitHub | `https://github.com/dariamucha666-svg/maldev2.git` (`origin`) |

## Automatyka

| Co | Jak |
|----|-----|
| VPS commit + push | `Narzedzia/git_autocommit.sh` · cron `*/15` · `/etc/cron.d/obsidian-git` |
| Alias | `/root/obsidian-auto-commit.sh` (to samo) |
| Kali pull/push | wtyczka **Obsidian Git** (co 10 min, pull na starcie, push po zapisie) |

Hasła i `Logs/*.log` nie idą do Gita (`.gitignore`).

## GitHub

`origin` na VPS = `maldev2`. Token **nie** jest w remote URL — leży w `/root/.git-credentials` (chmod 600), poza vaultem.

Auto-push: ten sam cron `*/15` wypycha na `local` i `origin`.

## Ręcznie z Kali

```bash
git -C /home/kali/obsidian-vault pull --rebase
git -C /home/kali/obsidian-vault push
```
