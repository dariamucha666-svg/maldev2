---
tags:
  - resources
  - links
updated: 2026-08-14
---

# Linki zewnętrzne

Powiązane: [[Pipeline_Analizy]] · [[Sliver_C2]]

## Próbki i threat intel

- [MalwareBazaar](https://bazaar.abuse.ch/) — nightly download (`download_malwarebazaar.sh`, tag `apk`)
- [MalwareBazaar API](https://bazaar.abuse.ch/api/) — klucz w `~/.mb_api_key` / `config/secrets.env` (nie tutaj)
- [VirusTotal](https://www.virustotal.com/) — brak API na boxie; UI wymaga reCAPTCHA

## Narzędzia pipeline

| Projekt | URL | Użycie u nas |
|---------|-----|----------------|
| jadx | https://github.com/skylot/jadx | `tools/jadx` 1.5.1 |
| apktool | https://apktool.org/ | `tools/apktool` 2.11.1 |
| pefile | https://github.com/erocarrera/pefile | venv 2024.8.26 |
| YARA | https://virustotal.github.io/yara/ | 4.5.0 |
| Yara-Rules | https://github.com/Yara-Rules/rules | `tools/yara-rules` |
| radare2 | https://github.com/radareorg/radare2 | 5.5.0 |
| capa (Mandiant) | https://github.com/mandiant/capa | 9.4.0 |
| androguard | https://github.com/androguard/androguard | venv |
| NusantaraScan | https://github.com/Lutfifakee-Project/NusantaraScan | native PE/ELF (**nie** `negativeneutral/…`) |
| Malware-Analyzer | https://github.com/GlgApr/Malware-Analyzer | PE/ELF, nie całe APK |
| Ghidra | https://github.com/NationalSecurityAgency/ghidra | na `.57` 12.1.2 — nie na 6 GB VPS |

## C2 / lab (dokumentacja, nie payloady)

- Sliver: https://github.com/BishopFox/sliver
- cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- Caddy: https://caddyserver.com/docs/caddyfile

## Przewodniki wewnętrzne

- `/root/android-pipeline/docs/GUIDE_PL.md` — skorygowany „Krok 0–4” (bez nieistniejącego `chimera:latest`)
- [[Obsidian_Workflow]]

## Host payloadu (IoC, nie link do klikania)

`http://192.162.199.149/uploads/141935c46a5c4ff1b84b433e84f36e61.exe` — zobacz [[IOC_Backdoor]].
