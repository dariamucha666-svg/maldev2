---
title: "E — Eksploatacja (Exploitation)"
date: 2026-08-16
tags: [ive, e, eksploatacja, exploit]
category: pentest
status: active
---

# E — Eksploatacja (Exploitation)

Faza **E** wykorzystuje luki z fazy V, żeby osiągnąć **cel (C)**: shell, dane,
eskalacja, wpływ. To tu luka zamienia się w realny dostęp.

## Narzędzia

| Narzędzie | Typ | Notatka |
|-----------|-----|---------|
| Metasploit Framework | framework exploitów/post-exploit | [[Model_IVE/E_Eksploatacja/Metasploit]] |
| Sqlmap | automatyczna SQL Injection | [[Model_IVE/E_Eksploatacja/Sqlmap]] |
| Nuclei | template'owy skaner (też V) | [[Model_IVE/E_Eksploatacja/Nuclei]] |

## Charakterystyka

- **Metasploit**: gotowe moduły exploitów (EternalBlue i in.), payloady, meterpreter,
  post-exploit (mimikatz, hashdump), psexec — cały łańcuch E.
- **Sqlmap**: jedna luka (SQLi) → dump bazy, shell, upload pliku.
- **Nuclei**: automatyzacja wykrywania (a przy niektórych szablonach też potwierdzenie
  exploita — np. odczyt plików, RCE-proof w trybie bezpiecznym).

## Flow wewnątrz E

```
luka  ──▶  wybór exploita  ──▶  payload  ──▶  session (meterpreter/shell)  ──▶  C (cel)
```

## Powiązane

- [[Model_IVE/IVE_MOC]] · [[Model_IVE/V_Podatnosci/V_MOC]] · [[Narzedzia/Sliver_C2]] · [[Techniki_i_Narzedzia]]
