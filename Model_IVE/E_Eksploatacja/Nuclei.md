---
title: "Nuclei — skaner podatności oparty na szablonach YAML"
date: 2026-08-16
tags: [ive, e, v, skaner, szablony, narzedzie]
category: narzedzie
status: active
---

# Nuclei

**TL;DR**: szybkie narzędzie do skanowania podatności oparte na **szablonach YAML**.
Autor umieścił je w **E** (jest też świetne w V — tu obustronnie linkuję).

## Co to / do czego

ProjectDiscovery. Go (pojedynczy binary). Szablony YAML opisują detekcję luki/misconfig
(CVE, exposed panels, takeovers, technologies, ssl…). Jest bardzo szybki (asynchronicznie).

| Cecha | Wartość |
|-------|---------|
| Język | Go (single binary) |
| Szablony | 13094 (nuclei-templates v10.4.7) |
| Protokoły | http, tcp, dns, ssl, file, javascript… |
| Tryb | `-u` (1 URL), `-l` (lista), `-t` (szablon/tag), `-tags` |

## Instalacja / aktualizacja (vserver959630)

```bash
nuclei -ut                       # pobierz/aktualizuj szablony → ~/nuclei-templates
nuclei -version                  # v3.11.1
```

## Analiza dynamiczna (2026-08-16)

**Wersja**: nuclei **3.11.1** · **13094 szablonów** (v10.4.7).

**Demo** (`nuclei -u https://example.com -t .../http-missing-security-headers.yaml -silent`)
— braki nagłówków bezpieczeństwa na example.com:

```
[http-missing-security-headers:strict-transport-security] [http] [info] https://example.com
[http-missing-security-headers:content-security-policy] [http] [info] https://example.com
[http-missing-security-headers:permissions-policy] [http] [info] https://example.com
[http-missing-security-headers:x-content-type-options] [http] [info] https://example.com
... (10 braków łącznie)
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`nuclei_help.txt\` — 261 linii,
\`nuclei_templates_count.txt\`, \`nuclei_templates_sample.txt\`,
\`nuclei_demo_example_headers.txt\`, \`nuclei_demo_techdetect.txt\`).

## Użycie

```bash
nuclei -u https://cel.com -tags tech                 # wykrycie technologii
nuclei -u https://cel.com -t cves/ -severity critical  # CVE (critical)
nuclei -l hosts.txt -t http/exposures/               # lista hostów
nuclei -u https://cel.com -t http/takeovers/         # przejęcia subdomen
nuclei -u https://cel.com -t ~/nuclei-templates/ -me results/   # full + matcher output
```

## Szablony — najważniejsze kategorie

```
cves/  exposed-panels/  misconfiguration/  takeovers/  technologies/
exposures/  default-logins/  ssl/  vulnerabilities/
```

## Wynik → gdzie dalej

- Znaleziona luka/CVE → [[Model_IVE/E_Eksploatacja/Metasploit]] / [[Model_IVE/E_Eksploatacja/Sqlmap]].
- W naszym pipeline nuclei skanuje hosty C2 (patrz [[OSINT_Toolkit]]).

## Powiązane

- [[Model_IVE/E_Eksploatacja/E_MOC]] · [[Model_IVE/V_Podatnosci/V_MOC]] · [[OSINT_Toolkit]] · [[Techniki_i_Narzedzia]]
