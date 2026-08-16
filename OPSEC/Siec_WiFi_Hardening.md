---
title: "Hardening sieci WiFi"
date: 2026-08-16
updated: 2026-08-16
tags: [opsec, wifi, hardening, siec, router, obrona]
status: active
category: siec
---

# Hardening sieci WiFi

Jak maksymalnie zabezpieczyć domową sieć WiFi przed atakami. Kolejność = priorytet
(najpierw to, co daje najwięcej za najmniej wysiłku).

> Uwaga: to lista do wykonania **na routerze i klientach**. Ja (agent na VPS) nie mam
> fizycznego dostępu do routera domowego — wykonaj to w panelu admina routera
> (zwykle http://192.168.1.1 albo http://192.168.0.1).

## 1. Router — dostęp administracyjny (priorytet #1)

- Zmień **domyślne hasło admina** (silne, unikalne, z menedżera haseł).
- Wyłącz **zdalne zarządzanie (remote/WAN administration)** — admin tylko z LAN.
- Zmień domyślny login jeśli router pozwala.
- Wyłącz **telnet**; SSH zostaw tylko jeśli świadomie go używasz.
- Panel po HTTPS jeśli dostępny; wylogowuj się po skończeniu.

## 2. Szyfrowanie i uwierzytelnianie (priorytet #2)

- **WPA3-Personal** jeśli router i wszystkie klienty wspierają; inaczej **WPA2-AES (CCMP)**.
- Nigdy: WEP, WPA (TKIP), sieć otwarta.
- **Silny PSK** (hasło WiFi): 20+ znaków losowych albo 4–6 słów metodą diceware.
  Nie: imię, data, adres, słownikowe.
- Świadomie zdecyduj o WPA3 "transition mode" (WPA3/WPA2 mieszane) — wygoda vs
  możliwość downgrade do WPA2.

## 3. WPS — wyłącz (priorytet #3)

- **Wyłącz WPS** całkowicie. WPS-PIN łamie się w kilka godzin (atak Pixie Dust /
  brute-force PIN 8 cyfr). Jeśli musisz — zostaw tylko przycisk (PBC).

## 4. Firmware

- Aktualizuj firmware routera na bieżąco (dziury w routerze to najczęstszy wektor wejścia).
- Rozważ **OpenWrt / DD-WRT / FreshTomato** dla dłuższego wsparcia bezpieczeństwa i kontroli.

## 5. Segmentacja sieci

- **Sieć gościnna** (z izolacją klientów) dla gości.
- **Osobna sieć/VLAN dla IoT** (kamery, smart-home, telewizor) — to najsłabsze ogniwo.
- Komputer/NAS/serwer trzymaj na sieci głównej, oddzielonej od IoT.

## 6. Funkcje do wyłączenia

- **UPnP** — malware używa go do otwierania portów.
- **WPS** — patrz wyżej.
- **Zdalne zarządzanie WAN**, **ping WAN (ICMP)**, **DMZ**, **port forwarding** — tylko jeśli naprawdę potrzebne i per-usługa.
- **SSID broadcast** (ukrywanie nazwy) — mała wartość (ukrywa przed laikami, nie przed skanerem), opcjonalnie.

## 7. DNS

- Ustaw na routerze filtrujący DNS: **Quad9 9.9.9.9** (blokada malware), **Cloudflare 1.1.1.2 / 1.0.0.2**, albo **NextDNS**.
- DoH/DoT (szyfrowane DNS) jeśli router wspiera.

## 8. Monitoring i detekcja ataków

- Sprawdzaj **listę podłączonych urządzeń** (nieznany MAC = alarm), blokuj po MAC.
- Przeglądaj **logi routera** (logowania admina, nowe urządzenia).
- Oznaki ataku:
  - **Deauth** — klienci masowo tracą WiFi (atak na handshake). Wykrywanie: Wireshark/monitor mode, detektory deauth.
  - **Evil twin / rogue AP** — podrobiona nazwa sieci. Sprawdzaj BSSID (MAC AP), używaj Fing / WiFi Analyzer.
  - Obce SSID / dziwne sygnały w okolicy.
- Narzędzia: **Fing** (skan sieci), **WiFi Analyzer**, **Wireshark** (monitor mode).

## 9. Klienci (telefon, laptop)

- Aktualizacje automatyczne, firewall włączony.
- Nie łącz się z otwartymi/publicznymi sieciami bez VPN.
- Wyłącz "auto-join" do znanych/otwartych sieci.

## 10. Fizycznie

- Router w miejscu niedostępnym dla obcych — przycisk reset przywraca domyślne (słabe) hasła.
- Zmień domyślny kod resetu/PIN jeśli router ma taką opcję.

## Atak → obrona (ściąga)

| Atak | Obrona |
|------|--------|
| WPS PIN brute (Pixie Dust) | wyłącz WPS |
| Słownik PSK po przechwyceniu handshake | silny PSK; WPA3 (SAE — nie łamie się offline) |
| Evil twin / rogue AP | sprawdzaj BSSID, unikaj otwartych sieci, VPN |
| Deauth → capture handshake | WPA3 z PMF (802.11w), monitoruj deauth |
| KRACK (na kliencie) | aktualizuj klienty |
| UPnP abuse | wyłącz UPnP |
| Exploit firmware routera | aktualizuj firmware / OpenWrt |
| Zdalny admin WAN | wyłącz remote management |

## Powiązane

- [[Urzadzenia_i_siec]] · [[Checklist_OPSEC]] · [[Zabezpieczenia_po_prostu]] · [[Podstawy_OPSEC]]
