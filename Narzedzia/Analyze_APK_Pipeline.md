# Pipeline auto-analizy APK

Skrypt: `Narzedzia/analyze_apk.py` — automatyzuje cały łańcuch statycznej analizy APK.

## Użycie

- `python3 Narzedzia/analyze_apk.py --apk <plik.apk> [--out <katalog>]`
- `python3 Narzedzia/analyze_apk.py --hash <sha256>` — pobiera z MalwareBazaar (klucz `~/.mb_api_key`)

## Kroki (automatycznie)

1. Triage: sha256, rozmiar, `file`.
2. `apkid` — wykrycie packera/kompilatora DEX (werdykt trafia do karty jako `Spakowane`).
3. Rozpakowanie + **odzysk manifestu** (fake-encryption trick: podrobiony bit encrypted + zwykły deflate → `zlib.decompress`).
4. Manifest (`androguard axml`) → pakiet, uprawnienia, serwisy, receivery, activity.
5. Dekompilacja (`jadx`) → Java.
6. IoC: IP / URL / domeny (`strings` na DEX).
7. **Skan podejrzanych API** — WebView (`addJavascriptInterface`, `setJavaScriptEnabled` — jak w notatkach dropperów), Accessibility/overlay (bankerzy), SMS (stealery OTP), `DexClassLoader`/`REQUEST_INSTALL_PACKAGES` (droppery), NFC (skimmery `a710209e`), Clipboard (clippery), socket/WebSocket (C2), anty-RE (`ptrace`/Frida/Zirex), kryptografia. Źródło: Java z jadx, fallback: strings na DEX.
8. **Scoring ryzyka uprawnień** — wagi per uprawnienie (`PERM_RISK` w skrypcie) → suma punktów + poziom (niski / średni / wysoki / KRYTYCZNY). Top ryzykowne trafiają do karty.
9. **„Co robi ta apka”** — automatyczny opis zachowania: sygnały API + uprawnienia + werdykt packera składane w czytelne zdania (heurystyki zgodne z [[Role_Tags]]).
10. Generacja **YARA** (UTF-16 package — bo resources.arsc jest Stored) + **karta Obsidian** (.md) z sekcją ryzyka i „co robi ta apka”.

## Wymagania

- `/opt/retools` (apkid + androguard), `/opt/jadx` (jadx), `unzip`/`strings`, klucz MalwareBazaar.

## Wynik

`/tmp/apk_analysis/<sha256-pierwsze12>/` → karta `.md` (ryzyko + podejrzane API + co robi + IoC), reguła `.yar`, `jadx_out/`, `manifest.xml`, `file.txt`.

## Test (ClayRat)

- Wynik: pakiet `io.system.system903`, 41 uprawnień, 4977 plików Java, YARA + karta wygenerowane poprawnie.
- Uwaga: `apkid` rzuca wyjątek na zaszyfrowanym (fake-flag) manifeście — to oczekiwane; pipeline sam odzyskuje manifest dalej.

## Powiązane

- [[Detektor_Packer]] — osobny skrypt `detect_packer.py` do klasyfikacji packera (Zirex / hhcbcu / ZipCrypto / .NET) przed pełną analizą.
