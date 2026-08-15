---
tags: [lab, hosts]
updated: 2026-08-15
---

# Hosty lab

Hasła **nie** trzymamy w vaultcie.

| IP | AceRDP / hostname | OS | Dostęp | Rola |
|----|-------------------|-----|--------|------|
| `5.175.189.133` | `vserver959630` | Ubuntu 24.04.4 | SSH `root`, xrdp (tunel SSH) | pipeline, vault, bot XMask |
| `5.175.189.139` | `vserver580088` | Debian 12 | SSH `root` | REMnux-lite (yara, r2, vol, inetsim) |
| `5.175.189.57` | `WIN-T5BVVHUNVJI` | Windows Server 2022 Eval | WinRM 5985, RDP 3389 | Windows RE (Ghidra / PEStudio / DIE / FLOSS) |
| ? | `vserver781193` | ? | niełączony | trzeci host z panelu AceRDP |

Panel: AceRDP konto `kalasnikov433`, produkt Bronze, NL, status Online.  
Server ID:

- `vserver959630` — `b93ff31c-6694-4977-bb1b-e72b86950815`
- `vserver580088` — `df4b49e4-e885-47f4-b8fd-7572f66a26f5`
- `vserver781193` — `89e43888-450a-436a-8a55-2c75e8c8362c`

Zrzut panelu na pulpicie `.133`: `acerdp-my-servers.png` (bez kolumny IP, bez daty ważności).

## Ścieżki

**.133**

- pipeline: `/root/android-pipeline`
- próbki: `/root/samples/{raw,quarantine,reports,notes}`
- vault: `/root/obsidian-vault`
- bot: `/root/obsidian-telegram-bot`
- unit: `obsidian-telegram-bot.service`
- goose: `/root/.local/bin/goose` (sesja `deepseek-vps`, DeepSeek) — [[Goose_DeepSeek]]

**.139**

- narzędzia: systemowe (`yara`, `binwalk`, `tshark`, `inetsim`, `r2`, `vol`)
- OSINT toolkit: [[Narzedzia/OSINT_Toolkit]] — Recon-ng, amass, subfinder, nuclei, httpx, theHarvester, SpiderFoot, sherlock
- Phishing lab: [[Lab/Phishing_Sim_Lab]] — GoPhish (service `gophish`), SET (`/opt/set`)
- .NET RE: `monodis` (mono-utils)
- SSH: klucz z `.133` (id_ed25519, bez hasła)

**.57**

- narzędzia: `C:\Tools\` (Ghidra, PEStudio, DIE, FLOSS, Procmon, ProcExp, Sysmon, x64dbg, dnSpy, capa)
- próbka: `C:\Tools\samples\backdoor.exe`
- Ghidra project: BackdoorLab

Zobacz [[Lab/Recap 2026-08-15]] · [[Lab/Narzedzia_RE]] · [[Lab/Recap 2026-08-14]] · [[Dashboard]]

## Kanał i studio (15.08)

- kanał: `t.me/XMaskPoland` (id w `.env`, nie tutaj)
- studio: `/root/xmask-studio/jobs/` + `/root/obsidian-telegram-bot/{studio,render,content}.py`
- bot unit: `obsidian-telegram-bot.service`
