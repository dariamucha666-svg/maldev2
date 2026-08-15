---
tags: [lab, hosts]
updated: 2026-08-14
---

# Hosty lab

Hasła **nie** trzymamy w vaultcie.

| IP | Hostname | OS | Dostęp | Rola |
|----|----------|-----|--------|------|
| `5.175.189.133` | `vserver959630` | Ubuntu 24.04.4 | SSH `root` | pipeline, kwarantanna, vault |
| `5.175.189.57` | `WIN-T5BVVHUNVJI` | Windows Server 2022 Eval | WinRM 5985, RDP 3389 | Ghidra / PEStudio / x64dbg |
| `5.175.189.139` | (osobna sesja) | — | SSH | poza recapem PE |

## Ścieżki

**.133**

- pipeline: `/root/android-pipeline`
- próbki: `/root/samples/{raw,quarantine,reports,notes}`
- vault: `/root/obsidian-vault`

**.57**

- narzędzia: `C:\Tools\`
- próbka: `C:\Tools\samples\backdoor.exe`
- Ghidra project: BackdoorLab
- output: `C:\Tools\ghidra_out\`

Zobacz [[Lab/Recap 2026-08-14]] · [[Infrastruktura_C2]] · [[Dashboard]]
