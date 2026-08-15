---
title: "Indeks pakietu detekcji C2"
date: 2026-08-15
type: index
tags: [index, c2, detections, mapa]
---

# Indeks — pakiet detekcji C2 (2026-08-15)

> Mapa wszystkich artefaktów detekcyjnych i raportów wygenerowanych na podstawie obserwacji infrastruktury C2 (serwer `.133`, porty 9999/9998, JSON po TCP, brak uwierzytelniania).
>
> **Katalog:** `detections/` (reguły) + `raports/` (dokumentacja/analiza).

## 1. Reguły detekcyjne (katalog `detections/`)

| Plik | Zawartość | Silniki |
|------|-----------|---------|
| [[C2_detection_rules_2026-08-15]] | Reguły podstawowe + artefakty (pełna wersja) | Sigma, YARA, Suricata |
| [[C2_detection_rules_sigma_yara_suricata]] | Reguły podstawowe (wersja skondensowana) | Sigma, YARA, Suricata |
| [[sequence_detection_rules_2026-08-15]] | Sekwencje A/B/C (reguły atomowe + korelacja temporalna 5 min) | Sigma |
| [[sequence_detection_eql_splunk_2026-08-15]] | Sekwencje A/B/C — gotowe zapytania | EQL, Splunk |
| [[sequence_detection_kql_2026-08-15]] | Sekwencje A/B/C — gotowe zapytania | KQL (Sentinel/MDE) |
| [[hashes_IOC_2026-08-15]] | Hashe SHA256 próbek + reguły hash-based | YARA, Sigma (plikowe) |

### 1.1 Reguły podstawowe (pojedyncze zdarzenia)

- **Sigma** — `4688` (uruchomienie `agent.py`), `5156` (połączenie na 9999/9998), `5145` (udziały), `4657` (Run key).
- **YARA** — `C2_Agent_py` i `C2_Server_py` (rzeczywiste ciągi: `screenshot`, `xwd`, `mss`, `getresult`, `cmd_id` itd.).
- **Suricata** — beacon na 9999, nieautoryzowany CLI na 9998, JSON payloady, eksfiltracja.

### 1.2 Reguły sekwencyjne (korelacja, okno 5 min)

| Sekwencja | Opis | Dostępne silniki |
|-----------|------|------------------|
| **A** | konto (`4720`) + grupa (`4732`) + persistence `Run` (`4657`/Sysmon 12/13) | Sigma, EQL, Splunk, KQL |
| **B** | keylogger (proces + hook + plik `keylog_*`) + eksfiltracja (9999) | Sigma, EQL, Splunk, KQL |
| **C** | screenshot (proces + plik `screenshot_*`) + eksfiltracja (9999) | Sigma, EQL, Splunk, KQL |

## 2. Raporty i analizy (katalog `raports/`)

| Plik | Zawartość |
|------|-----------|
| [[2026-08-15_C2_infrastructure]] | Dokumentacja architektury (porty, procesy, pliki, protokół JSON) |
| [[server_comparison]] | Porównanie `server.py` (nowy TCP vs stary) + analiza bezpieczeństwa |
| [[Analiza_artefaktów_agenta_57]] | Artefakty forensyczne operacji (`net user`, `Run`, keylogger, screenshot) |

## 3. Mapa zależności

```
Obserwacja infrastruktury (netstat/ps/logi)
        │
        ├─► 2026-08-15_C2_infrastructure.md   (architektura)
        ├─► server_comparison.md              (analiza kodu serwera)
        │
        ▼
Reguły podstawowe ──► C2_detection_rules_*.md  (Sigma/YARA/Suricata)
        │              hashes_IOC_*.md        (SHA256 + reguły hash-based)
        │
        ▼
Analiza artefaktów ──► Analiza_artefaktów_agenta_57.md
        │
        ▼
Reguły sekwencyjne ──► sequence_detection_rules_*.md
                        ├─ Sigma  (korelacja temporalna)
                        ├─ EQL / Splunk
                        └─ KQL (Sentinel/MDE)
```

## 4. Macierz pokrycia

| Obszar detekcji | Sigma | YARA | Suricata | EQL | Splunk | KQL |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|
| Uruchomienie agenta | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Połączenie 9999/9998 | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| Beacon (long-lived) | — | — | ✅ | — | — | — |
| Sekwencja A (konto+Run) | ✅ | — | — | ✅ | ✅ | ✅ |
| Sekwencja B (keylogger) | ✅ | — | — | ✅ | ✅ | ✅ |
| Sekwencja C (screenshot) | ✅ | — | — | ✅ | ✅ | ✅ |
| Payload JSON (sieć) | — | — | ✅ | — | — | — |
| Próbki plików (YARA) | — | ✅ | — | — | — | — |
| Hash próbek (SHA256) | ✅ (plik) | ✅ | — | — | — | — |

## 5. Stan i status

- Wszystkie reguły oznaczone jako **`experimental`** — oparte o nazwy/porty/stringi, nie o hashe próbek.
- Do produkcji: SHA256 próbek już spisane w [[hashes_IOC_2026-08-15]]; do dokończenia — potwierdzić format payloadu JSON i dopasować nazwy pól do docelowego SIEM.
- Sekcje artefaktów dla `net_user_add`/`reg_set_value`/`keylog` w próbce **nie występują** w kodzie (`agent.py` implementuje tylko `screenshot`) — oznaczono je jako hipotetyczne.

---
*Wygenerowano: 2026-08-15. Zakres: obserwacja read-only + detekcja (bez działań operacyjnych na C2).*
