---
tags: [grok, video, studio, imagine, ffmpeg]
date: 2026-08-16
updated: 2026-08-16
status: active
---

# Grok Video Lab

Pipeline: **obrazki + opis („przepis") → klipy z Grok Imagine (xAI) → montaż ffmpeg → gotowy film**.

- **Generowanie** robi chmura xAI (nie potrzebujesz lokalnego GPU).
- **Montaż** robi nasz ffmpeg (cięcia, przejścia, audio, skalowanie).
- Zero zależności Pythona — same skrypty na bibliotece standardowej + ffmpeg.

Powiązane: [[Studio_Klip]] · [[Studio_Narzedzia]]

---

## Struktura folderu

| Ścieżka | Rola |
|---|---|
| input/ | tu wrzucasz obrazki |
| output/ | tu lądują gotowe filmy |
| work/ | klipy pośrednie (robocze) |
| audio/ | muzyka / dźwięk pod film |
| przepisy/ | przepisy markdown (sceny) |
| scripts/ | skrypty: grok_media, assemble, pipeline |

---

## Konfiguracja (raz)

1. Wygeneruj klucz API w **console.x.ai → API Keys**.
2. Skopiuj plik konfiguracji i wklej klucz:

        cp .env.example .env

3. Wpisz klucz do pola **XAI_API_KEY** w pliku .env.

Klucz NIE jest zapisywany w gicie (.gitignore ignoruje .env).

**Alternatywa bez klucza** — jeśli masz zalogowany Grok CLI (komenda grok login), skrypty same użyją tokenu z **~/.grok/auth.json**. Uwaga: token z sesji **wygasa** (aktualny wygasł 2026-08-15), więc gdy pojawi się „Brak klucza", zaloguj się ponownie w Grok CLI albo wklej klucz API.

---

## Sposób 1 — tryb prosty (folder obrazków + jeden opis)

Wrzuć obrazki do **input/**, potem:

    python3 scripts/pipeline.py --input-dir input --prompt "powolny zoom, delikatny ruch, realistycznie" --output output/film.mp4

Każdy obrazek staje się krótkim klipem (domyślnie 8 s), a całość jest sklejana z przejściem.

---

## Sposób 2 — tryb przepis (rekomendowany)

Tu opisujesz scenę po scenie, co ma się dziać. To jest miejsce, w którym **uczysz mnie swojego stylu**.

1. Skopiuj **przepisy/demo.md** i podmień pola.
2. Uruchom:

        python3 scripts/pipeline.py --recipe przepisy/moj-klip.md --output output/moj-klip.mp4

Format przepisu (frontmatter + sekcje **## Scena N**):

    ---
    tytul: "Tytuł klipu"
    orientacja: pion        # pion | poziom
    rozdzielczosc: 720p     # 480p | 720p (generowanie)
    canvas: 720             # 720 | 1080 (montaż)
    przejscie: fade         # np. fade, wipeleft, slideleft, circleopen
    audio: audio/muzyka.mp3 # opcjonalne
    ---

    ## Scena 1
    obraz: input/01.png
    prompt: Powolny najazd kamery na twarz, delikatny zoom, ciepłe światło.
    czas: 6

    ## Scena 2
    obraz: input/02.png
    prompt: Płynne przejście, postać odwraca się w stronę kamery, lekki uśmiech.
    czas: 5

Pola sceny: **obraz** (ścieżka do pliku względem przepisu), **prompt** (opis ruchu/akcji), **czas** (1–15 s, domyślnie 8), **audio** (opcjonalnie per scena — w v1 ignorowane w montażu, użyj audio globalnego).

---

## Skrypty — komendy

### grok_media.py (klient xAI)

    python3 scripts/grok_media.py image  --prompt "kot w kosmosie" --out work/
    python3 scripts/grok_media.py edit   --images a.png b.png --prompt "połącz oba" --out work/
    python3 scripts/grok_media.py video  --image a.png --prompt "powolny zoom" --duration 6 --out work/
    python3 scripts/grok_media.py status REQUEST_ID --out work/
    python3 scripts/grok_media.py models

Tryby wideo:

- **tekst → wideo**: sam --prompt
- **obraz → wideo** (obraz = pierwsza klatka): --image plik.png
- **referencje → wideo** (obraz wpływa na treść, nie blokuje 1. klatki): --reference plik.png (max 3)
- **audio referencyjne**: --audio plik.wav (max 3)

Lokalne pliki (obraz/audio) są automatycznie kodowane do base64 data URL — xAI przyjmuje je bez publicznego hostingu.

### assemble.py (montaż)

    python3 scripts/assemble.py --inputs work/a.mp4 work/b.mp4 --output out.mp4 --orientation pion --transition fade --audio audio/muzyka.mp3

---

## Koszty (orientacyjne, mogą się zmienić)

| Co | Cena |
|---|---|
| Obraz | ~0,02 USD/szt |
| Wideo 480p | ~0,05 USD/s |
| Wideo 720p | ~0,07 USD/s |
| Klip 8 s w 720p | ≈ 0,56 USD |

Cena jest w odpowiedzi API jako **usage.cost_in_usd_ticks**.

---

## Ograniczenia (stan na sierpień 2026)

- Pojedynczy klip: **1–15 s** (domyślnie 8 s).
- Rozdzielczość generowania: **480p / 720p**.
- Referencje obrazkowe: max **3** na klip.
- Montaż łączy klipy w dłuższy film (przejścia + audio lokalnie), więc dłuższy materiał = kilka klipów + sklejka.
- Pierwsze wyniki bywają surowe — to normalne. Wspólnie dopracujemy styl przez przepisy.

---

## Szybki start po wgraniu obrazków

    python3 scripts/pipeline.py --input-dir input --prompt "kamera powoli jedzie do przodu, subtelny ruch" --output output/film.mp4 --dry-run   # podgląd planu
    python3 scripts/pipeline.py --input-dir input --prompt "kamera powoli jedzie do przodu, subtelny ruch" --output output/film.mp4            # realnie
