---
tags: [index, lab]
updated: 2026-08-15
---

# Malware Lab Vault

**Główny indeks:** [[Dashboard]] · [[QuickStart]] · [[Droga_przez_cyberbezpieczenstwo]]

Statyczna analiza próbek + osobne notatki infrastruktury. Bez detonacji.

## Start tutaj

- [[Droga_przez_cyberbezpieczenstwo]] — recap całej ścieżki (RE → C2 → narzędzia)
- [[Dashboard]] — Dataview + zadania
- [[QuickStart]] — najczęściej używane
- [[Pipeline_Analizy]] — pipeline APK/PE na `.133`
- [[Lab/Recap 2026-08-14]] — recap obu sesji 14.08
- [[Lab/Hosts]] — hosty i ścieżki

## Nawigacja

- [[Status]] — pipeline na `vserver959630`
- [[Daily/2026-08-15]] — dziennik (klasyfikacja)
- [[Klasyfikacja_Korpus]] — co wynika z ról
- [[410a5cba Android RAT kira]] — rekomendowany następny RE
- [[178cb931 Precision Agriculture Go PE]] — backdoor Go
- [[Analizy/IOC/178cb931]]

## Hosty lab

| Rola | Host |
|------|------|
| Analiza / pipeline | `vserver959630` Ubuntu 24.04 (`5.175.189.133`) |
| Windows RE | `WIN-T5BVVHUNVJI` Server 2022 (`5.175.189.57`) — WinRM/RDP |

## Zasady

- Tylko static RE + notatki w tym vaultcie.
- Próbki zostają w `/root/samples/quarantine` i `/root/samples/raw`.
- Nie serwować PE na publicznym HTTP.
- Nie mieszać notatek C2 z raportami analizy.

## Otwarcie vaultu

Ścieżka: `/root/obsidian-vault`

```
obsidian /root/obsidian-vault
```

Jeśli brak binarnego `/opt/Obsidian/obsidian` — vault to zwykły katalog markdown; można go otworzyć z dowolnego klienta Obsidian (Open folder as vault).
