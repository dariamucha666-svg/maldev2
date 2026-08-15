---
tags: [pipeline, tags, classification]
updated: 2026-08-15
---

# Tagi ról w pipeline

Po każdym `pipeline.sh` (i ręcznie) skrypt `classify_roles.py` dopisuje do raportu JSON:

```json
"tags": ["pipeline", "apk", "rat", "android"],
"classification": {
  "role": "rat",
  "family": "Android.RAT.Kira",
  "confidence": "wysoka",
  "source": "catalog"
}
```

Źródło prawdy: `/root/android-pipeline/web/catalog.json` (kopia `virus_catalog.json`).  
Heurystyki (gdy hash nie jest w katalogu): Accessibility+overlay → `rat`, SMS cluster → `stealer`, XMRig/stratum → `cryptojacker`, `REQUEST_INSTALL_PACKAGES` → `dropper`, entropia + Dobby/hhcbcu → `packed`.

## Gdzie

| | |
|--|--|
| Skrypt | `/root/android-pipeline/lib/classify_roles.py` |
| Hook | `pipeline.sh` → po `generate_auto_yara` |
| Katalog | `/root/android-pipeline/web/catalog.json` |
| Vault | [[Klasyfikacja_Korpus]] |

## Ręcznie

```bash
source /root/android-pipeline/config/path.sh
python3 /root/android-pipeline/lib/classify_roles.py /root/samples/reports
```

Nowy hash bez wpisu w katalogu dostaje rolę z heurystyki + tag `unlisted`. Dopisz go potem do `catalog.json` i odpal skrypt jeszcze raz.

Tagi YAML w notatkach Obsidian trzymaj spójnie: `rat` `stealer` `backdoor` `dropper` `packed` `phishing` `cryptojacking`.
