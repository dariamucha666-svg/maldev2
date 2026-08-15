#!/usr/bin/env bash
# Commit vault changes on the VPS, then sync to the bare remote.
# No GitHub required. Kali / Obsidian Git pull from the same bare repo.
set -u
cd /root/obsidian-vault || exit 1
git config --global --add safe.directory /root/obsidian-vault >/dev/null 2>&1 || true
git config user.name "Obsidian Bot"
git config user.email "bot@localhost"

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S %Z')" >/dev/null
fi

push_one() {
  local remote="$1"
  git remote get-url "$remote" >/dev/null 2>&1 || return 0
  if ! git pull --rebase --autostash "$remote" main >/dev/null 2>&1; then
    git rebase --abort >/dev/null 2>&1 || true
    echo "pull --rebase $remote failed — skip push"
    return 1
  fi
  git push "$remote" main >/dev/null
}

# local bare (Kali SSH) + GitHub origin
push_one local || true
push_one origin || true
echo "ok $(git rev-parse --short HEAD)"
