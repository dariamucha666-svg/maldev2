---
tags: [xmask, video, studio]
date: 2026-08-15
updated: 2026-08-15
---

# Gotowe narzędzia do montażu (GitHub)

Werdykt: nie ma open-source CapCut z promptem i eksportem jak płatna chmura. Najbliższe, co naprawdę skleja klipy + głos + przejścia: **editly**.

| Narzędzie | Link | Co umie | Na naszym VPS |
|-----------|------|---------|----------------|
| **editly** | https://github.com/mifi/editly | klipy + audio + przejścia + Ken Burns + ducking, CLI/JSON, bez watermarku | `npm i` padło na native `gl`. Docker daemon nie stoi. |
| auto-editor | https://github.com/WyattBlue/auto-editor | tylko wycina ciszę | już zainstalowane |
| OpenCut | https://github.com/OpenCut-app/OpenCut | GUI jak CapCut, bez watermarku | headless w roadmapie, nie do `/klip` |
| NCA Toolkit | https://github.com/stephengpope/no-code-architects-toolkit | self-host API: captions, concat | Docker, ciężkie |
| ffmpeg-concat | https://github.com/transitive-bullshit/ffmpeg-concat | sklejka + GL transitions | też potrzebuje GL |
| cutcli / CapCut draft | https://github.com/xuliang2024/cutcli-cookbook | robi **projekt do CapCut**, nie MP4 | wymaga apki CapCut, ryzyko watermarku |

Nie ruszamy „CapCut patcher 2026” — to crack.

Następny krok jak chcemy przestać kleić własne ffmpeg: odpalić Dockera i postawić editly w kontenerze.
