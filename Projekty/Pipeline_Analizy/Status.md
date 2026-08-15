---
title: "Pipeline Status"
date: 2026-08-14
updated: 2026-08-15T09:00
tags: [pipeline, lab, projekt]
status: in_progress
priority: medium
category: pipeline
---
# Pipeline status

Pełny opis (skrypty, formaty, narzędzia, output): **[[Pipeline_Analizy]]**

**Home:** `/root/android-pipeline`  
**Wrapper:** `/usr/local/bin/android-malware-pipeline` → `bin/pipeline.sh`  
**Cron:** `0 2 * * * /root/nightly_pipeline.sh`  
**Samples:** `/root/samples`

## Ostatni run (auto-YARA, `--pe-only` kwarantanna)

| Pole | Wartość |
|------|---------|
| Czas | 2026-08-14 22:15:26 UTC |
| Cel | `--pe-only /root/samples/quarantine/` |
| Log | `/root/samples/logs/pipeline_20260814T221526Z.log` |
| Wynik | 29 plików (1 PE skipnięty, reszta ZIP); auto-YARA 3 reguły / 15 IOC |
| Dashboard | `127.0.0.1:8766` ([[Dashboard_IOC]]) |
| Custom YARA | `Backdoor_EASports_Go` w `tools/yara-rules/custom/backdoor_easports.yar` (23:03 UTC) — każda nowa próbka PE w `pipeline.sh` / nightly |

## Komendy

```bash
# jedna próbka
bash /root/android-pipeline/bin/pipeline.sh /path/to/sample

# tylko PE
bash /root/android-pipeline/bin/pipeline.sh --pe-only

# przebuduj CSV/patterns
bash /root/android-pipeline/bin/pipeline.sh --aggregate-only

# wymuś ponowną analizę
FORCE=1 bash /root/android-pipeline/bin/pipeline.sh /path/to/sample
```

## Stan lab (14.08)

- 14 APK w `raw/`
- 29 raportów JSON
- 1 PE w kwarantannie (ten z [[Analizy/Malware/178cb931 Precision Agriculture Go PE]])
- Dysk: ~8.7 G wolne (78%)
- capa na tym PE nie zdążył w 45s

## Klasyfikacja (15.08)

`classify_roles.py` po auto-YARA. Raporty JSON mają `tags` + `classification.role`.  
Werdykt: [[Klasyfikacja_Korpus]] · hook: [[Role_Tags]]

| role | w raportach JSON |
|------|-----------------:|
| rat | 1 |
| backdoor | 1 |
| stealer | 2 |
| dropper | 5 |
| packed | 5 |
| phishing | 1 |
| cryptojacker | 0 |

(Chrome + .NET siedzą w `catalog.extra`, nie w tych 15 JSON.)

## Powiązane

- [[Pipeline_Analizy]]
- [[Daily/2026-08-14]]
- [[Dziennik_Lab]]
- [[Analizy/Malware/178cb931 Precision Agriculture Go PE]]


## 15.08 wieczór — nightly / export

- `classify_roles.py` **było** w `pipeline.sh` (log 02:12). Nightly teraz woła je **jeszcze raz zawsze**, też gdy brak APK (zostają same PE).
- Usunięty zdublowany cron: zostaje tylko `/etc/cron.d/nightly-pipeline` (user crontab już nie odpala nightly drugi raz).
- `export_pipeline_to_obsidian.sh` pisze krótki `Analizy/Raporty/analiza_*.md` (tabela ról + daily), nie skleja wszystkich historycznych MD.
- Przykład: [[analiza_2026-08-15_08-59]] — 33 próbki: dropper 12, packed 11, rat 5, phishing 2, stealer 2, backdoor 1.

Recap: [[Lab/Recap 2026-08-15]]


## Sigma (15.08)

`lib/sigma_generator.py` po `generate_auto_yara`. 5 reguł z 15 IOC w dashboardzie: PE hashes (process/file), role backdoor, hunting API, hosty sieciowe. Vault: [[detections/generated]] · [[Dashboard_IOC]].
