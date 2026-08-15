---
title: "Sigma (auto)"
date: 2026-08-15
tags: [sigma, pipeline, detections]
---

# Sigma — auto z pipeline

Wygenerowano `2026-08-15` z `15` IOC. Reguły hashy PE + (opcjonalnie) hosty z stringów. **Bez detonacji.**

## Pliki

| plik | po co |
|------|--------|
| `xmask_network_hosts.yml` | auto |
| `xmask_pe_hashes_file.yml` | auto |
| `xmask_pe_hashes_process.yml` | auto |
| `xmask_role_backdoor_hashes.yml` | auto |
| `xmask_win_account_api_cluster.yml` | auto |

## Role w zbiorze

| role | n |
|------|--:|
| dropper | 7 |
| packed | 2 |
| phishing | 2 |
| stealer | 2 |
| backdoor | 1 |
| rat | 1 |

Konwersja do SIEM: `sigma convert -t splunk xmask_pe_hashes_process.yml` (pakiet `sigma-cli`).

Powiązane: [[Dashboard_IOC]] · [[Pipeline_Analizy]] · [[Klasyfikacja_Korpus]]
