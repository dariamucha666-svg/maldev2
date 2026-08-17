---
title: "Builder agenta z wersjonowaniem"
date: 2026-08-16
tags: [narzedzia, rat, build, lab]
status: active
---

# Builder agenta — build_agent.sh

Skrypt: `Narzedzia/build_agent.sh` — rozwiązuje problem z [[2026-08-16]] (Daily): *„agent.exe nieaktualny — zbudowany 15.08 03:21, źródło zmienione 04:04 → exe kończył się natychmiast”*.

Koniec problemu „exe starszy niż źródło”: pipeline pilnuje kolejności **build → hash → manifest → upload do C2 → timestamp w Obsidianie**.

## Użycie

```bash
build_agent.sh --check                  # tylko kontrola świeżości exe (exit 1 = exe stary)
build_agent.sh                          # pełny pipeline, bez uploadu
build_agent.sh --upload                 # pełny pipeline + scp do C2
build_agent.sh --force                  # przebuduj nawet gdy exe świeży
build_agent.sh --dry-run                # pokaż co by się stało, nic nie wykonuj
```

## Pipeline

1. **Freshness check** — jeśli źródło nowsze niż exe → build; `--check` sam zwraca exit 1 gdy exe stary (do CI/cronu).
2. **Build** — `pyinstaller --onefile --clean --name agent` (distpath/workpath/specpath w `WORK_DIR`, nie w cwd). Przed buildem generowany `_build_info.py` obok źródła: `BUILD_ID`, `VERSION`, `SRC_SHA256` (agent może `import _build_info` i raportować swój build).
3. **Hash** — SHA256 + rozmiar exe.
4. **Manifest** — `manifests/MANIFEST-<build_id>.json` (json z polami src/artifact/toolchain/upload/obsidian) + `MANIFEST-latest.json`. Build ID = UTC `YYYYMMDDTHHMMSSZ`, wersja `YYYYMMDD.<N>` (licznik z `VERSION`).
5. **Upload do C2** — `--upload`: `ssh mkdir -p` + `scp` exe + manifest do `C2_USER@C2_HOST:C2_DIR`. BatchMode (wymaga klucza). Bez flagi — status `skipped` w manifeście.
6. **Timestamp w Obsidianie** — dopisek `## Build agenta vX (UTC)` do `Daily/YYYY-MM-DD.md` (sekcje usuwają hasła/tokeny jak `log_to_obsidian.sh`).

## Konfiguracja (env)

| Zmienna | Default |
|---------|---------|
| `AGENT_SRC` | `/root/rat-c2/agent_win.py` |
| `WORK_DIR` | `/root/rat-c2` |
| `OBSIDIAN_VAULT` | auto: `/root/Obsidian` → `/root/obsidian-vault` |
| `C2_HOST` / `C2_USER` / `C2_DIR` | `5.175.189.133` / `root` / `/root/rat-c2/dist/` |
| `PYINSTALLER` | `pyinstaller` |
| `EXE_NAME` | `agent` |

## Powiązane

- [[Wlasny_RAT]] · [[2026-08-16_optymalizacja_RAT_57]] · [[2026-08-16_dynamiczna_analiza_RAT_57]]
- Manifesty: `/root/rat-c2/manifests/` (wzór jak `MANIFEST-20260815_095202Z-resume.txt` z R2)
