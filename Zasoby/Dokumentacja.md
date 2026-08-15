---
title: "Dokumentacja vaultu"
date: 2026-08-15
tags: [zasoby, obsidian]
---

# Dokumentacja

- [[Obsidian/Plugins]] — lista wtyczek i po co
- [[Obsidian_Workflow]] — konwencje pisania
- [[Obsidian_Auto_Log]] — `Logs/` `Analizy/Raporty/`
- [[Telegram_Obsidian_Bot]] — `Daily/` i `Inbox/` nie ruszać
- [[Dashboard]] — strona startowa

## Frontmatter (minimum)

```yaml
---
title: "…"
date: YYYY-MM-DD
tags: [malware]
status: in_progress   # planned | in_progress | completed
priority: medium      # high | medium | low
hash: ""
category: backdoor
---
```

Dataview czyta te pola na [[Dashboard]].
