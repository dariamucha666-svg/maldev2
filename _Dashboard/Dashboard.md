---
title: "Centrum Operacyjne"
date: 2026-08-15
tags: [dashboard, index]
status: active
priority: high
cssclasses: [dashboard]
---

# 🧠 Centrum Operacyjne

Szybki start: [[QuickStart]] · indeks: [[Home]] · ścieżka: [[Droga_przez_cyberbezpieczenstwo]] · zadania: [[Backlog]] · kanban: [[Kanban]] · model I-V-E: [[Model_IVE/IVE_MOC]]

## 📋 Aktywne projekty

```dataview
TABLE status, priority, category
FROM #projekt AND !"Projekty/Zakończone" AND !"\_Templates"
SORT file.mtime DESC
```

## 🦠 Ostatnie analizy malware

```dataview
TABLE date, status, hash, category
FROM #malware AND !"\_Templates"
SORT date DESC
LIMIT 10
```

## 🧷 IOC

```dataview
TABLE date, hash, status
FROM #ioc AND !"\_Templates"
SORT date DESC
LIMIT 10
```

## ✅ Zadania do zrobienia

```tasks
not done
short mode
```

## 📅 Dzienniki

```dataview
LIST
FROM "Daily"
SORT file.name DESC
LIMIT 7
```

## 💬 Telegram (dziś)

```dataview
LIST
FROM "Dzienniki/Telegram"
SORT file.name DESC
LIMIT 5
```

## 📡 Sliver

- [Żywe sesje na dashboardzie](https://dash.maskencrypt.eu/?tab=c2) — `GET /api/sliver/sessions`
- [[sessions]] — auto-eksport sesji / beaconów
- [[Automatyzacja]] — co jest spięte

## 📂 Mapa vaultu

- [[Home]] — spis całej bazy
- [[QuickStart]] — najczęściej używane
- [[Backlog]] — lista zadań
- [[Kanban]] — tablica przepływu
- [[Obsidian/Plugins]] — wtyczki
- [[Obsidian_Workflow]] — jak pisać
- [[Obsidian_Auto_Log]] — logi z `.133`
