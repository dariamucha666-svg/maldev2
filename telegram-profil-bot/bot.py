#!/usr/bin/env python3
"""Bot Telegram analizujący publiczny profil tak, jak robi to Googlebot."""

import logging
import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

GOOGLEBOT_UA = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)

HEADERS = {
    "User-Agent": GOOGLEBOT_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

TIMEOUT = 20
MAX_IMAGE_BYTES = 10 * 1024 * 1024  # limit Telegrama dla zdjęć


def extract_url(raw: str) -> str | None:
    """Wyciąga pierwszy link z wiadomości lub traktuje tekst jako domenę."""
    raw = raw.strip()
    if not raw:
        return None
    match = re.search(r"https?://\S+", raw)
    if match:
        return match.group(0).rstrip(".,;:!?)")
    tokens = raw.split()
    return tokens[0] if tokens else raw


def normalize_url(raw: str) -> str | None:
    """Dodaje schemat, jeśli go brak, i sprawdza poprawność adresu."""
    raw = extract_url(raw)
    if raw is None:
        return None
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    if not parsed.scheme or not parsed.netloc:
        return None
    return raw


def fetch_page(url: str):
    """Pobiera stronę nagłówkami Googlebota."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise RuntimeError(f"Nie udało się pobrać strony: {exc}") from exc
    return response.url, response.status_code, response.text


def extract_profile(html: str, final_url: str) -> dict:
    """Wyciąga tytuł, opis i zdjęcie profilowe z metadanych."""
    soup = BeautifulSoup(html, "html.parser")

    def meta_content(*names: str) -> str | None:
        for name in names:
            for attr in ("property", "name"):
                node = soup.find("meta", attrs={attr: name})
                if node is not None and node.get("content"):
                    content = node["content"].strip()
                    if content:
                        return content
        return None

    title = meta_content("og:title", "twitter:title")
    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    description = meta_content(
        "og:description", "twitter:description", "description"
    )

    image_url = meta_content("og:image", "twitter:image", "twitter:image:src")
    if image_url:
        image_url = urljoin(final_url, image_url)

    return {
        "title": title,
        "description": description,
        "image_url": image_url,
        "domain": urlparse(final_url).netloc,
    }


def download_image(image_url: str) -> bytes | None:
    """Pobiera zdjęcie nagłówkami Googlebota, gdy to faktycznie obraz."""
    try:
        response = requests.get(
            image_url, headers=HEADERS, timeout=TIMEOUT, stream=True
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Nie udało się pobrać zdjęcia: %s", exc)
        return None

    content_type = response.headers.get("Content-Type", "").lower()
    if "image" not in content_type:
        return None

    data = response.content
    if not data or len(data) > MAX_IMAGE_BYTES:
        return None
    return data


def build_caption(profile: dict, status: int) -> str:
    lines = []
    if profile["title"]:
        lines.append(f"📌 {profile['title']}")
    if profile["description"]:
        lines.append("")
        lines.append(f"📝 {profile['description']}")
    lines.append("")
    lines.append(f"🌐 Domena: {profile['domain']}")
    lines.append(f"🔍 Status HTTP: {status}")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Wyślij link do publicznego profilu, a przeanalizuję go jak Googlebot."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Wyślij link do publicznego profilu (np. https://przyklad.pl/profil/nazwa).\n"
        "Odpowiem tytułem, opisem, domeną i statusem HTTP, a zdjęcie profilowe "
        "wyślę jako obrazek z podpisem."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = normalize_url(update.message.text or "")
    if not url:
        await update.message.reply_text("Podaj poprawny link do profilu.")
        return

    await update.message.chat.send_action("typing")

    try:
        final_url, status, html = fetch_page(url)
    except RuntimeError as exc:
        await update.message.reply_text(str(exc))
        return

    profile = extract_profile(html, final_url)
    caption = build_caption(profile, status)

    image_bytes = None
    if profile["image_url"]:
        image_bytes = download_image(profile["image_url"])

    if image_bytes:
        await update.message.reply_photo(photo=image_bytes, caption=caption)
    else:
        await update.message.reply_text(caption)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Ustaw zmienną środowiskową TELEGRAM_BOT_TOKEN.")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
