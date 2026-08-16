---
title: "Nmap — skan portów i usług"
date: 2026-08-16
tags: [ive, v, podatnosci, skaner, siec]
category: narzedzie
status: active
---

# Nmap

**TL;DR**: skanuje porty i mapuje infrastrukturę — identyfikuje aktywne usługi i ich
wersje (NSE = skrypty detekcji luk). Most między fazą I a V.

## Co to / do czego

Nmap ("Network Mapper") — standard de facto skanowania sieci. Wysyła pakiety, na
podstawie odpowiedzi buduje mapę hostów/portów/usług. Skrypty **NSE** dodają detekcję
luk (np. `http-vuln-*`, `ssl-*`, `smb-vuln-*`).

| Cecha | Wartość |
|-------|---------|
| Licencja | NPSL (open-source) |
| Język | C + Lua (NSE) |
| Tryby | TCP SYN/connect, UDP, version (`-sV`), OS (`-O`), scripts (`-sC`) |

## Analiza dynamiczna (2026-08-16)

**Wersja**: Nmap **7.94SVN**.

**Demo** (`nmap -sV -Pn -p 22,80,443 scanme.nmap.org`) — oficjalny cel testowy Nmapa:

```
Nmap scan report for scanme.nmap.org (45.33.32.156)
PORT    STATE  SERVICE VERSION
22/tcp  open   ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp  open   http    Apache httpd 2.4.7 ((Ubuntu))
443/tcp closed https
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Pełne zrzuty: [[Model_IVE/_analiza_dynamiczna/README]] (\`nmap_version.txt\`,
\`nmap_help.txt\`, \`nmap_scanme.txt\`, \`nmap_localhost.txt\`).

## Użycie

```bash
nmap -sV cel.com                    # wersje usług
nmap -sC -sV -p- cel.com            # wszystkie porty + default scripts
nmap -sV --script vuln cel.com      # skrypty detekcji luk (NSE vuln)
nmap -sV -O cel.com                 # detekcja OS
nmap -sS -p 1-1000 10.0.0.0/24      # szybki skan sieci (SYN)
```

## Wynik → gdzie dalej

- Wersja usługi (np. OpenSSH 6.6.1) → sprawdź CVE → [[Model_IVE/E_Eksploatacja/Metasploit]].
- Web na 80/443 → [[Model_IVE/V_Podatnosci/Burp_Suite]] / [[Model_IVE/V_Podatnosci/OWASP_ZAP]] / [[Model_IVE/E_Eksploatacja/Nuclei]].

## Powiązane

- [[Model_IVE/V_Podatnosci/V_MOC]] · [[Model_IVE/I_Informacja/Shodan]] · [[Techniki_i_Narzedzia]]
