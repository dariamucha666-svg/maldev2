---
title: "Kali NetHunter"
date: 2026-08-16
tags: [wiedza, narzedzia, nethunter, kali, android]
category: narzedzia
---

# Kali NetHunter

**Kali NetHunter** = mobilna platforma pentestowa od zespołu Kali (OffSec) na Androida.
Czyli "Kali na telefonie" — uruchamiasz narzędzia Kali (nmap, Metasploit, Bettercap, aircrack)
bezpośrednio na telefonie.

## Dwa warianty (ważne)

| Wariant | Root | Co potrafi |
|---------|------|-----------|
| **NetHunter (pełny)** | ✅ wymaga | monitor mode WiFi, raw packets (ARP spoof, deauth), HID (emulacja klawiatury/myszki), Metasploit, nmap, Bettercap... |
| **NetHunter Rootless** | ❌ bez roota | ograniczone: podstawowe narzędzia, ale **BEZ raw packets** → **nie zrobi ARP spoof / deauth** |

→ Do Twojego scenariusza (ARP spoof na Samsungu) potrzebny jest **pełny NetHunter (z rootem)**.
  Rootless się nie nada — nie wyśle surowych pakietów.

## Wymagania (pełny NetHunter)

1. **Zrootowany** telefon.
2. **Wspierany model** — Samsung ma wiele wspieranych modeli (oficjalna lista: kali.org → NetHunter).
3. **Odblokowany bootloader** + custom recovery (**TWRP**).

## Instalacja (skrót — robi się na telefonie, nie zdalnie)

1. Odblokuj bootloader (wymaga wyczyszczenia telefonu!).
2. Wgraj **TWRP** (custom recovery).
3. Wgraj obraz **NetHunter** (kernel + rootfs) dla Twojego modelu.
4. Zainstaluj apkę **NetHunter** (+ Magisk module).
5. Uruchom Kali (chroot) → masz pełne narzędzia w terminalu na telefonie.

> ⚠️ Robisz to **fizycznie na telefonie** — ja stąd (VPS) nie wgram Ci systemu na telefon.
> Użyj telefonu "do testów", nie głównego (root = utrata gwarancji + ryzyko).

## Co Ci to da w Twoim scenariuszu

Twój plan: Samsung = ofiara, drugi telefon = NetHunter (atakujący), oba na tym samym WiFi.

- NetHunter (root) na tym samym WiFi co Samsung → **ARP spoof + sniff** (Bettercap), DNS spoof, injekcja HTTP.
- Do **ataków WiFi** (deauth, przechwytywanie handshake) — potrzebny **kompatybilny chipset WiFi** telefonu (nie każdy ma monitor mode).

## Ważne o sieci

- **Samsung na danych komórkowych = NIE do ataku** — dane komórkowe nie są w Twoim LAN-ie,
  atakujący z LAN nie widzi tego ruchu. Samsung musi być **podłączony do tego samego WiFi** co atakujący.

## Alternatywa, którą już masz

Masz **Kali fizycznie (laptop)** — ono już robi ARP spoof/Bettercap bez żadnego NetHuntera.
NetHunter to wygoda mobilności (telefon zamiast laptopa), nie konieczność.

## Powiązane

- [[Lab_MitM_Android_Ofiara]] · [[MitM_NTLM_Relay]] · [[Techniki_i_Narzedzia]]
