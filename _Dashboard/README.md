---
tags:
  - dashboard
  - index
  - cyberlab
updated: 2026-08-15
vault: /home/kali/obsidian-vault
vault_vps: /root/obsidian-vault
---

# 🧠 CyberLab – Centralna Baza Wiedzy

Vault: `/home/kali/obsidian-vault` (Kali) · kopia robocza na VPS: `/root/obsidian-vault`  
Host analizy: `vserver959630` (`5.175.189.133`) — Ubuntu 24.04.4

Starsze notatki sesji: [[Home]] · [[Lab/Recap 2026-08-14]] · [[Status]]

---

## Projekty i Infrastruktura

- [[Infrastruktura_C2]] – Sliver, Cloudflare, VPS-y, domeny
- [[Pipeline_Analizy]] – Automatyczna analiza APK i PE
- [[Laboratorium_Windows]] – Windows Server do analizy dynamicznej
- [[Backdoor_Go]] – Analiza backdoora (easports.gg)

## Narzędzia i Konfiguracje

- [[Cloudflare_Konfiguracja]] – Tunele, DNS, routing
- [[Sliver_C2]] – Komendy, payloady, sesje
- [[OpenCut_Setup]] – Edytor wideo na VPS
- [[Dashboard_IOC]] – Widok IOC + auto-YARA
- [[Dashboard]] – widok Dataview / Tasks
- [[QuickStart]] – skróty
- [[Obsidian_Workflow]] – Jak używamy Obsidian
- [[Obsidian/Plugins]] – wtyczki
- [[Obsidian_Auto_Log]] – auto terminal / pipeline / sliver → `Logs/` `Analizy/Raporty/`
- [[Telegram_Obsidian_Bot]] – bot Telegram → ten vault
- [[XMask/README]] – posty na kanał (RAT / stealer / backdoor / dropper)
- [[Klasyfikacja_Korpus]] – co wynika z klasyfikacji (RAT/stealer/backdoor)
- [[Role_Tags]] – auto-tagi w raportach pipeline
- [[Daily/2026-08-15]] – dziennik 15.08

## Analizy i Wnioski

- [[Exodus_Modyfikacja]] – Próby modyfikacji app.asar
- [[Analiza_Backdoora_Go_Detale]] – Szczegółowy RE backdoora
- [[IOC_Backdoor]] – Hashe, stringi, reguły YARA

## Zasoby i Linki

- [[Linki_Zewnętrzne]] – MalwareBazaar, GitHub, narzędzia
- [[Dziennik_Lab]] – Codzienne notatki z pracy

---

**Auto-YARA + dashboard:** 3 reguły, 15 IOC. Publiczny UI: http://5.175.189.133:8080 · lokalny `127.0.0.1:8766`. [[Dashboard_IOC]]

## Stan lab (2026-08-14 22:00 UTC)

| Host | Rola | Status |
|------|------|--------|
| `5.175.189.133` `vserver959630` | C2 #1 + pipeline + vault | SSH OK, Ubuntu 24.04, dysk 78% |
| `5.175.189.139` | C2 #2 backup | poza recapem PE |
| `5.175.189.57` `WIN-T5BVVHUNVJI` | Lab Windows RE | WinRM + RDP OK |

**Pipeline:** 14 APK w `raw/`, 29 raportów JSON, nightly cron `0 2 * * *`, ostatni ręczny PE run `21:31 UTC` OK.

**Aktywna próbka PE:** [[178cb931 Precision Agriculture Go PE]]  
**Następny cel RE:** [[410a5cba Android RAT kira]] (albo [[1b3ceba6 Chrome bank stealer]])

Werdykt korpusu: RAT 1 · Backdoor 1 · Stealer 4+ · Dropper 5+ · Packed 3+ · Cryptojacker 0. [[Klasyfikacja_Korpus]]

## Zasady vaultu

- Hasła **nie** trzymamy w notatkach (patrz [[Lab/Hosts]]).
- Próbki zostają w `/root/samples/{quarantine,raw}` — nie serwować PE na publicznym HTTP.
- Analiza statyczna i notatki C2 są rozdzielone katalogami (`Analizy/` vs `Projekty/`), ale linkowane z tego dashboardu.
- Taguj: `#pipeline` `#pe` `#apk` `#c2` `#ioc` `#daily`
