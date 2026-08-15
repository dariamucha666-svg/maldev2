#!/usr/bin/env bash
# Hourly local commit of the vault. No remote push.
set -u
cd /root/obsidian-vault || exit 1
git config --global --add safe.directory /root/obsidian-vault >/dev/null 2>&1 || true
git config user.name "Obsidian Bot"
git config user.email "bot@localhost"
git add -A
if git diff --cached --quiet; then
  exit 0
fi
git commit -m "auto $(date -u +%Y-%m-%dT%H:%M:%SZ)" >/dev/null
echo "committed $(git rev-parse --short HEAD)"
