---
tags: [xmask, video, studio, telegram]
date: 2026-08-15
updated: 2026-08-15
status: active
---

# Studio — /klip

OpenCut (GitHub, CapCut-like) to **edytor z myszką**. Nie ma jeszcze headless „prompt → render” jak płatny CapCut w chmurze. Auto-montaż jest lokalny na `.133`: ffmpeg + auto-editor. **Zero znaku wodnego. Zero końcówki CapCut.**

## Flow

1. `/klip` → seria
2. *Ile wrzucasz video?* 0–5
3. *Ile wrzucasz plików audio?* 0–5
4. Prompt: jak ma wyglądać montaż
5. Wrzucasz dokładnie tyle plików
6. Bot montuje i puszcza na kanał

Prompt rozumie m.in.: pion/poziom, szybko/spokojnie, ciemno, zoom, przejścia, napisy, bez ciszy, lektor głośniej.

## Czego nie robimy

Nie odpalamy pirackiego CapCut i nie zdejmujemy cudzych watermarków. Nasz eksport nigdy nie dostaje brandingu CapCut.
