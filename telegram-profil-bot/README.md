# Bot analizujący profile publiczne

Bot Telegram, który przyjmuje link do profilu publicznego w serwisie
społecznościowym i analizuje stronę tak, jak robi to Googlebot.

## Co robi bot

- Pobiera stronę z nagłówkami Googlebota
- Wyciąga: tytuł, opis / bio, zdjęcie profilowe, domenę i status HTTP
- Wysyła zdjęcie profilowe jako obrazek z podpisem (jeśli jest dostępne)
- Działa wyłącznie na danych publicznych, bez logowania

## Wymagania

- Python 3.10+
- Token bota od @BotFather

## Instalacja

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Konfiguracja

Ustaw token bota w zmiennej środowiskowej:

```bash
export TELEGRAM_BOT_TOKEN="TWOJ_TOKEN"
```

## Uruchomienie

```bash
python bot.py
```

## Użycie

Wyślij botowi link do publicznego profilu, np.:

```
https://przyklad.pl/profil/nazwa
```

Bot odpowie tytułem, opisem, domeną i statusem HTTP, a zdjęcie profilowe
wyśle jako obrazek z podpisem.

