---
title: "Phishing toolkit — analiza (SET, Evilginx2, GoPhish, SocialFish, ZPhisher)"
date: 2026-08-15
tags: [phishing, osint, social-engineering, narzedzia, defense]
status: analysis
category: narzedzia
---

# Phishing toolkit — analiza

Zestaw narzędzi phishingowych do **symulacji i detekcji** (nie do ataków na realne cele).
W kontekście laba: rozumieć, jak działają → lepiej je wykrywać.

## Przegląd

| Narzędzie | Język | Typ | Siła | Poziom zagrożenia |
|-----------|-------|-----|------|-------------------|
| **SET** (Social-Engineering Toolkit) | Python | multi-wektor (spear-phish, credential harvester, USB, SMS) | kompletny, ale „stary szkolny" | średni (bez 2FA-bypass) |
| **Evilginx2** | Go | reverse-proxy **AiTM** (przechwytuje sesje/cookie) | **obchodzi 2FA** | **wysoki** |
| **GoPhish** | Go | framework kampanii (e-mail + landing + tracking) | skalowalny, z API | średni–wysoki |
| **SocialFish** | Python | phishing + ngrok, mobile-first | prosty | niski–średni |
| **ZPhisher** | Bash | automatyczny phishing 30+ szablonów | script-kiddie | niski–średni |

---

## SET — Social-Engineering Toolkit (analiza szczegółowa)

Autor: **David Kennedy (TrustedSec)**. Open source, Python. Wiekowe (2009+), ale nadal
w dystrybucjach Kali/Parrot jako `setoolkit`.

### Menu / wektory

```
1) Spear-Phishing Attack Vectors       (mail + payload/attachment)
2) Website Attack Vectors              (credential harvester, tabnabbing, Java Applet…)
3) Infectious Media Generator          (USB: autorun + payload)
4) Create a Payload and Listener       (Metasploit payload)
5) Mass Mailer Attack                  (rozesyłka)
6) Arduino-Based Attack Vector         (Teensy HID)
7) Wireless Access Point Attack Vector (rogue AP)
8) QRCode Generator Attack Vector      (QR → URL)
9) PowerShell Attack Vectors           (PS payload)
10) Third Party Modules
```

### Najczęściej używany: Credential Harvester

1. `setoolkit` → Website Attack Vectors → Credential Harvester → Site Cloner.
2. SET klonuje stronę logowania (np. Gmail), serwuje lokalnie (port 80/443).
3. Ofiara wpisuje login+hasło → POST przechwytywany do pliku (`reports/…harvester…txt`).
4. Opcjonalnie redirect na prawdziwą stronę (żeby nie wzbudzić podejrzeń).

Kluczowy wniosek detekcyjny: SET **nie przechwytuje cookie**, tylko **login+hasło**.
Przy MFA ofiara dostaje kod 2FA, ale SET go nie widzi → **SET nie obchodzi 2FA**.

### Detekcja SET

- Klon strony ma **adres atakującego** (IP/domena), nie oryginalny — sprawdzaj pasek URL.
- POST do atakującego na niestandardowym porcie (nie tylko 443).
- Domyślne artefakty: `setoolkit`, katalog `~/.set/`, logi harvestera.
- W sieci: request do świeżo zarejestrowanej domeny, która 1:1 powiela HTML znanego serwisu.
- YARA: stringi SET w HTML (`setoolkit`, `metasploit`).

---

## Evilginx2 — AiTM (najgroźniejszy z listy)

Autor: **Kuba Gretzky**. Go. **Adversary-in-the-Middle**: nie klon, tylko **reverse proxy**
przez serwer atakującego do prawdziwego serwisu.

- **Phishlets** = pliki YAML opisujące flow logowania i nazwy cookie per serwis.
- Przechwytuje **cookie sesyjne PO zalogowaniu** (w tym sesję po 2FA) → **omija MFA**.
- Używa domen lookalike + Let's Encrypt (certyfikat wygląda „prawdziwie").

### Detekcja Evilginx2

- Domena **lookalike** (typosquat / punycode / prefiks „login-", „secure-").
- Cert Transparency: nowa domena z LE wydanym certyfikatem tuż przed kampanią.
- Cookie dostarczane z IP/domeny **atakującego**, nie oryginalnego serwisu.
- Nagłówki reverse-proxy (`Via`, `X-Forwarded-*`) — choć Evilginx potrafi je ukryć.
- Heurystyka: logowanie do „znanego" serwisu z nieznanej domeny = podejrzenie AiTM.

---

## GoPhish

Go, open source. **Framework kampanii** (nie pojedynczy klon):

- Encje: **Sending Profiles** (SMTP), **Email Templates**, **Landing Pages**, **Groups** (ofiary), **Campaigns**.
- Web UI + **REST API** (automatyzacja).
- Tracking: opened / clicked / submitted (pixel + redirecty).
- Legit użytek: **security awareness** (symulacje w firmie) — i niestety też realne kampanie.

### Detekcja GoPhish

- Domyślny panel admina na porcie **3333** (i `/admin`).
- Tracking pixel / linki z parametrem `rid=` (recipient id).
- Nagłówki SMTP z profilu GoPhish (nazwa user-agenta maila, `X-Mailer`).
- Domena landing page często świeża + cert LE.

---

## SocialFish i ZPhisher (script-kiddie)

- **SocialFish** (Python, UndeadSec): phishing mobile-first (Facebook/Instagram…), integracja **ngrok**. Stary, często zepsuty.
- **ZPhisher** (Bash): automat klonujący **30+ serwisów** (Instagram, Facebook, Google, Netflix…), tunel przez **ngrok / cloudflared / serveo**. Bardzo popularny u początkujących.

### Detekcja

- **Tunel ngrok / cloudflared / serveo** — domena `*.ngrok-free.app` itp. = natychmiastowy sygnał.
- Domyślne szablony stron (identyczne HTML między kampaniami).
- Lokalny serwer na nietypowym porcie + krótki TTL domeny.

---

## Wspólne wskaźniki (detekcja phishing-kitów)

1. **Świeża domena** (rejestracja < 7 dni) + cert LE + klon HTML znanego serwisu.
2. **Tunelowe domeny** (ngrok/cloudflared/serveo/localtunnel).
3. **Lookalike** (typosquat, punycode, prefiksy).
4. **AiTM** — cookie/sesja z IP atakującego po logowaniu.
5. **Tracking** (`rid=`, piksele 1×1, linki redirect).

## Miejsce w labie

- **Nie instalujemy na produkcyjnych hostach** (`.133` = pipeline, `.139` = RE).
- Do **symulacji wewnętrznych** najsensowniejszy jest **GoPhish** (kampanie awareness)
  i **SET Credential Harvester** (pokaz przechwytywania haseł na lokalnym demo).
- **Evilginx2** tylko w izolowanej sieci — to narzędzie AiTM (obchodzi 2FA), najwyższa ostrożność.
- SocialFish/ZPhisher — wyłącznie jako **próbki do detekcji**; uruchamiać tylko na własnych/autoryzowanych środowiskach (mocki), nigdy na realnych celach.

Powiązane: [[Recon_ng_Analiza]] · [[OSINT_Toolkit]] · [[Lab/Hosts]]
