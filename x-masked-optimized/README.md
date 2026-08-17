# x-masked.com — wersja zoptymalizowana

Pakiet gotowy do wdrożenia. Wygląd i działanie strony **bez zmian** — zmieniła się tylko
waga, liczba requestów i nagłówki cache.

## Co zostało zrobione

### 1. Obrazki (największy zysk — ~1.2 MB mniej)

| Plik | Było | Jest | Zmiana |
|---|---|---|---|
| `assets/hero.webp` (1920×1080) | 605 728 B | **266 582 B** (WebP q72) | −56% |
| `assets/hero.avif` (nowość) | — | **184 185 B** (AVIF q50) | −70% vs oryginał |
| `assets/hero-mobile.webp` (1080×1920) | 645 168 B | **288 060 B** (WebP q72) | −55% |
| `assets/hero-mobile.avif` (nowość) | — | **189 314 B** (AVIF q50) | −71% vs oryginał |
| `assets/og.jpg` | 243 573 B | **196 064 B** (JPEG q82) | −19% |
| `assets/fonts/*.woff2` (nowość) | — | **96 388 B** (4 pliki variable) | zamiast 7 TTF z Google |

Przeglądarki obsługujące AVIF (Chrome, Edge, Firefox 93+, Safari 16.4+) pobierają **jeden**
plik AVIF zamiast WebP — tło strony schodzi z ~605 KB do ~184 KB. Fallback WebP działa
wszędzie (CSS `image-set` + `@supports`).

### 2. Fonty — self-host zamiast Google Fonts

- **Było:** render-blocking `<link>` do Google Fonts + **7 plików** (DM Sans 400–700
  statyczne + Space Grotesk 500–700 statyczne, TTF dla części UA).
- **Jest:** 4 pliki **variable** woff2 (2 rodziny × latin + latin-ext) na własnej domenie.
  Brak zewnętrznej zależności, brak blokady renderowania, polskie znaki pokryte (latin-ext).
- Preload dwóch krytycznych: `spacegrotesk-latin` (tytuł = LCP) i `dmsans-latin` (body).

### 3. CSS — przycięty i wcięty w HTML

- Usunięte reguły martwe (`.topbar`, `.brand-*`, `.eyebrow`, `.stage-caption`,
  `.results`, `.result-*`, `.inside`, `.hint`, `.footer-note`, `.search-message`,
  `.zangi`/`.threema`/`.signal` — tych elementów nie ma w HTML/JS).
- Minifikacja (cssnano): 13 929 B → **9 350 B**, a całość wklejona do `<style>` w
  `index.html` — **zero dodatkowego requestu na CSS**.
- Czytelna wersja źródłowa: `src/styles.css`.

### 4. JS — minifikacja

- `app.js`: 6 652 B → **4 995 B** (terser, `-c passes=2 -m`). Zachowanie identyczne
  (hasło `start`, triggery portfolio, odmowa na tematy nieetyczne, linki zamaskowanych).
- Czytelna wersja źródłowa: `src/app.js` (to stary plik z produkcji).

### 5. Preload LCP

- `hero.avif` (desktop) i `hero-mobile.avif` (mobile) preloadowane z `fetchpriority="high"`
  i `media` — tło (LCP) startuje od razu, nie czeka na CSS.
- Fonty preloadowane z `crossorigin` (wymagane dla woff2).

### 6. Nagłówki cache (wymaga deployu)

Plik `_headers` (działa w Workers Static Assets i Cloudflare Pages):
- HTML: `max-age=0, must-revalidate` (aktualizacje widoczne natychmiast — jak teraz),
- `/assets/*`, `/favicon.png`, `*.woff2`: `max-age=86400, stale-while-revalidate=604800`
  (1 dzień cache + tydzień SWR — powroty użytkowników bez ponownego pobierania obrazków),
- do tego `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`.

Jeśli Worker serwuje pliki ręcznie, zamiast `_headers` użyj `worker.js` (alternatywa w pakiecie).

## Bilans wagi strony (pierwsze wejście, desktop, Chrome)

| Zasób | Było | Jest |
|---|---|---|
| HTML | 6 733 B | 16 261 B (z inline CSS) |
| CSS | 13 929 B | 0 (inline w HTML) |
| JS | 6 652 B | 4 995 B |
| hero | 605 728 B (WebP) | 184 185 B (AVIF) / 266 582 B (WebP fallback) |
| fonty | ~245 KB woff2 z Google (7 wag) | 96 KB woff2 (2 variable + subsets) |
| fonts CSS + preconnect | 1 651 B + 2 domeny | 0 (self-host) |
| **Razem transfer** | **~865 KB** | **~243 KB** (AVIF) / ~325 KB (WebP) |

→ waga spada o **~72%** (AVIF), liczba requestów z ~9 do **6** (HTML, JS, hero, 2 fonty,
favicon), znikają 2 zewnętrzne domeny (fonts.googleapis.com, fonts.gstatic.com).
Na mobile tło (hero-mobile) analogicznie: 645 KB → 189 KB AVIF / 288 KB WebP.

## Wdrożenie

```bash
# 1. Wgraj zawartość tego katalogu na maszynę z projektem (np. .133: /root/x-masked)
scp -r . root@5.175.189.133:/root/x-masked/

# 2. Jeśli projekt to Workers Static Assets (bez własnego fetch handlera):
#    - plik _headers zacznie działać automatycznie przy najbliższym deployu
wrangler deploy

# 3. Jeśli Worker serwuje pliki ręcznie:
#    - zastąp handler plikiem worker.js (lub podepnij nagłówki w swoim kodzie)
#    - pamiętaj o binding ASSETS
```

Po deployu warto **wyczyścić cache Cloudflare** (purge all) — stare obrazy były cache'owane
przez edge. Weryfikacja: `curl -sI https://x-masked.com/assets/hero.avif` → ma zwrócić
`200` i `cache-control: public, max-age=86400...`, a `cf-cache-status` (po 2. wejściu) `HIT`.

## Struktura

```
wrangler.toml       konfiguracja Workera (Workers Static Assets + worker)
worker.js           assety + endpoint /api/contact (wysyłka linku na Telegram)
deploy.sh           deploy jedną komendą (wymaga CLOUDFLARE_API_TOKEN)
public/             ← to idzie na Cloudflare
  index.html        finalny HTML (CSS inline, preloady, self-hostowane fonty)
  app.js            zminifikowany (terser) — czat AI + jednorazowe sekrety
  _headers          nagłówki cache (Workers Static Assets / Pages)
  assets/
    hero.avif|webp  tło desktop
    hero-mobile.avif|webp  tło mobile
    og.jpg          obrazek social
    favicon.png
    fonts/          4 × variable woff2
src/                czytelne źródła CSS/JS (nie są serwowane)
```

## Wdrożenie na Cloudflare (bez .133)

```bash
# 1. Ważny token: https://dash.cloudflare.com/profile/api-tokens
#    uprawnienia: Workers Scripts → Edit (konto z workerem x-masked)
export CLOUDFLARE_API_TOKEN=xxxx

# 2. Deploy (z tego katalogu)
./deploy.sh          # albo: wrangler deploy

# 3. Purge cache + weryfikacja
#    curl -sI https://x-masked.com/assets/hero.avif  → cache-control: public, max-age=86400...
```

Custom domains (`x-masked.com`, `www`) zostają przypięte do workera `x-masked`
automatycznie — redeploy tej samej nazwy ich nie rusza.

## Sprzątanie po .133

Po udanym deployu na `.133` można usunąć `rm -rf /root/x-masked` (kod strony)
i ewentualnie zatrzymać cokolwiek, co tam serwowało. Strona żyje w 100% na Cloudflare.

## Funkcje (od 16.08)

### Czat AI (dolny biały pasek)
Po kliknięciu czat się rozwija i asystent („Maska") pisze powoli:
pyta o **Linki? Kontakt? Boty na TG? Chcesz może stronę internetową?** i odpowiada
odpowiednimi linkami/kontaktami na komendy: `linki`, `kontakt`, `boty`, `strona`,
`pomoc`, powitania. Fallback podpowiada dostępne komendy. `maska` → wskazówka
o górnym pasku.

### Górny czarny pasek — jednorazowa zaszyfrowana wiadomość (link)
Bez hasła i bez czatu: użytkownik wpisuje kontakt/wiadomość i wysyła. Strona:
- szyfruje tekst **w przeglądarce** (WebCrypto AES-256-GCM, losowy klucz),
- tworzy jednorazowy sekret na **app.maskencrypt.eu** (`POST /api/notes`, tylko
  ciphertext+iv — **klucz nie opuszcza przeglądarki**, jedzie w hashu linku),
- wysyła **link** `https://app.maskencrypt.eu/v/<id>#<klucz>` na Telegram
  (`POST /api/contact` → bot @XMasked_bot).

Właściciel klika link → strona maskencrypt pokazuje „Odszyfruj" → `GET /api/notes/<id>`
**kasuje sekret na serwerze (burn-once, DELETE RETURNING w D1)** → treść pokazuje się
raz. Drugi odczyt = 404 GONE. Sekret wygasa też po 24h (TTL), nawet bez odczytu.

- Sekrety workera: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (`wrangler secret put`)
- Uwaga: Bot Fight Mode strefy blokuje `/api/contact` dla nie-przeglądarkowych UA
  (403/1010); przeglądarki przechodzą.

## Zabezpieczenia (16.08, tura 2)

### Nagłówki bezpieczeństwa (`public/_headers`, dla wszystkich odpowiedzi)

| Nagłówek | Wartość | Po co |
|---|---|---|
| `Content-Security-Policy` | `default-src 'none'`; tylko `script-src 'self'`, `style-src 'self' + sha256` (hash inline CSS), `connect-src 'self' https://app.maskencrypt.eu`, `font-src/img-src 'self'`, `frame-ancestors 'none'`, `base-uri/object-src/form-action` zablokowane | zero XSS z inline scriptów, brak ramek, brak exfil |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | wymuszenie HTTPS (HSTS) |
| `Permissions-Policy` | kamera/mikrofon/geolokalizacja/płatności/USB/`browsing-topics` zablokowane | brak niepotrzebnych uprawnień |
| `Cross-Origin-Opener-Policy` | `same-origin` | izolacja okna (Spectre/clickjacking) |
| `Cross-Origin-Embedder-Policy` | `require-corp` | wymusza CORP na subresources |
| `Cross-Origin-Resource-Policy` | `same-origin` | blokada czytania zasobów z innych źródeł |
| `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` | `nosniff` / `DENY` / `strict-origin-when-cross-origin` | jak wcześniej |

Uwaga: hash w CSP (`sha256-oRNxl...`) dotyczy bloku `<style>` w `index.html`.
Jeśli zmienisz CSS w HTML, przelicz hash (patrz niżej) i zaktualizuj `_headers`,
inaczej przeglądarka odrzuci styl.

```bash
# przeliczenie hasha stylów po edycji index.html:
python3 - <<'EOF'
import re, hashlib, base64
html = open('public/index.html').read()
m = re.search(r'<style>(.*?)</style>', html, re.S)
print('sha256-' + base64.b64encode(hashlib.sha256(m.group(1).encode()).digest()).decode())
EOF
```

### Utwardzony `/api/contact` (`worker.js`)

- **tylko POST** (405), tylko `application/json` (415), limit ciała **4 KB** (413),
- **globalny rate limit w KV** (binding `env.KV`, namespace `x-masked-rate-limit`,
  klucz `rl:<ip>`, TTL 60 s): 5 żądań/min na IP → `429` z `Retry-After` + szybki
  licznik lokalny (per-izolat) jako pierwszy filtr; przy braku KV — fail-open,
- **walidacja Origin** — tylko `https://x-masked.com` i `https://www.x-masked.com` (403),
- walidacja formatu linku (regex) i długości (400),
- szczegóły błędów Telegrama trafiają tylko do logów workera — klient dostaje ogólny błąd (502),
- nagłówki bezpieczeństwa (`nosniff`, CSP `default-src 'none'`, `XFO`, CORP, HSTS,
  `no-store`) na wszystkich odpowiedziach API.

Testy jednostkowe: `node` + mock Telegrama/KV — 20 przypadków (w tym 429 po 5. żądaniu
z tego samego IP). Testy na żywo: ścieżki 405/403/415/400/429 (bez wysyłania na Telegram)
+ finalny happy-path (`{"ok":true}`).

### Reszta

- `robots.txt` — `Disallow: /api/`.
- Globalny limit działa w KV (spójne odczyty, TTL 60 s) — działa między colo.
  Do jeszcze twardszego limitu można dodać regułę Rate Limiting strefy w panelu
  Cloudflare dla `/api/contact` (token deployowy nie ma do tego uprawnień).

## Uwagi na przyszłość

- Przy kolejnych zmianach obrazków: AVIF q50–55 i WebP q72–75 dają najlepszy stosunek
  jakości do wagi (sprawdzone na tych plikach).
- Żeby statyki mogły dostać `immutable` (rok), trzeba hashować nazwy plików
  (`hero.a1b2c3.avif`) przy deployu — wtedy `max-age=31536000, immutable`.
- `og:image` nie wpływa na szybkość strony (pobiera go tylko scraper), więc nie ma sensu
  cisnąć go poniżej ~190 KB.
- `/api/contact` jest publiczne — warto w panelu CF dodać regułę rate-limit dla tej
  ścieżki, żeby ktoś nie zasypał Telegrama spamem.
- Link z kluczem w hashu: jeśli właściciel przekarze link dalej, każdy z linkiem odczyta
  wiadomość (i spali ją). To standardowy model OneTimeSecret.
