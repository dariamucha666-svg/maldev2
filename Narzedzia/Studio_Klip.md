---
tags: [xmask, video, studio, telegram]
date: 2026-08-15
status: active
---

# Studio — klip → montaż → kanał

OpenCut na `.57` to GUI. Auto-montaż jest na `.133`: **ffmpeg + auto-editor** (GitHub WyattBlue).

## Jak wrzucać

W bocie (tylko Ty):

1. `/klip` → HACKPLUG albo opsec.exe
2. Filmiki z roboty (można kilka)
3. Głos lektora (nagranie / plik audio)
4. *Montuj i wyślij*

Albo: `/klip hackplug podpis pod film`

Bot montuje i puszcza na [XMaskPoland](https://t.me/XMaskPoland).

Limit Telegram: **~19 MB na plik**. Krótkie urywki.

## Co robi montaż

- skleja klipy (pion 1080×1920 albo poziom 1920×1080)
- kładzie lektora, oryginał ścisza
- kartę z nazwą serii
- wycina ciszę (auto-editor)
- normalizuje głos

Pliki robocze: `/root/xmask-studio/jobs/` (po wysłaniu kasowane).
Kod: `/root/obsidian-telegram-bot/studio.py` `render.py`

Cloudflare R2 — jeszcze nie. Najpierw VPS (jest ~15 GB wolnego).
