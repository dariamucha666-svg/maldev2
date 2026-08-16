---
title: "SpiderFoot — automatyczny OSINT (100+ modułów)"
date: 2026-08-16
tags: [ive, i, osint, recon, narzedzie]
category: narzedzie
status: active
---

# SpiderFoot

**TL;DR**: automatyczny OSINT — jeden skan celu przez **100+ modułów** (DNS, WHOIS,
Shodan, VT, social, dark web…). Ma CLI i Web UI.

## Co to / do czego

Autor: Steve Micallef. Python, MIT. Zbiera wszystko o celu (domena/IP/nick/e-mail)
i scala w relacyjny raport.

| Cecha | Wartość |
|-------|---------|
| Język / licencja | Python · MIT |
| Interfejs | CLI (`sf.py`) + Web UI (localhost:5001) |
| Moduły | 100+ (`sfp_dns`, `sfp_whois`, `sfp_shodan`, `sfp_haveibeenpwned`…) |
| Typy skanów | `-u {all,footprint,investigate,passive}` |
| Klucze API | opcjonalne (Shodan, VT, HIBP…) — bez nich działa trzon pasywny |

## Instalacja (vserver959630)

```bash
git clone --depth 1 https://github.com/smicallef/spiderfoot /opt/ive/spiderfoot
/opt/ive/venv/bin/pip install -r /opt/ive/spiderfoot/requirements.txt
/opt/ive/venv/bin/python /opt/ive/spiderfoot/sf.py -V
```

> ⚠️ Nazwa `spiderfoot` na PyPI to **placeholder 0.0.1** ("No functionality") —
> instaluj **z GitHub**, nie z pip.

## Analiza dynamiczna (2026-08-16)

**Wersja**: SpiderFoot **4.0.0**.

**Demo** (`sf.py -s example.com -m sfp_dns -q`) — moduł DNS:

```
Source             Type            Data
SpiderFoot UI      Internet Name   example.com
SpiderFoot UI      Domain Name     example.com
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`spiderfoot_version.txt\`,
\`spiderfoot_help.txt\`, \`spiderfoot_demo_dns.txt\`).

## Użycie

```bash
# CLI — pasywny skan domeny
python sf.py -s cel.com -u passive -q

# Web UI
python sf.py -l 127.0.0.1:5001
```

## Wynik → gdzie dalej

- Znalezione hosty/IP → [[Model_IVE/V_Podatnosci/Nmap]] · [[Model_IVE/E_Eksploatacja/Nuclei]].
- Porównanie z [[Model_IVE/I_Informacja/Recon-ng]] i [[Model_IVE/I_Informacja/Maltego]].

## Powiązane

- [[Model_IVE/I_Informacja/I_MOC]] · [[OSINT_Toolkit]]
