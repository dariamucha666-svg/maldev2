#!/usr/bin/env python3
import os
import re
import logging
import tempfile
from urllib.parse import urlparse
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

# Token NIE idzie do vaultu (repo jest publiczne na GitHub).
# Wstaw go do .env POZA vaultem i eksportuj jako PROFILE_ANALYZER_BOT_TOKEN,
# albo podmień placeholder poniżej. Konwencja vaultu: sekrety poza sejfem.
TOKEN = os.environ.get("PROFILE_ANALYZER_BOT_TOKEN", "TWÓJ_TOKEN_TELEGRAM")
logging.basicConfig(level=logging.INFO)

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def fetch_profile_data(url: str) -> dict:
    """Pobiera dane z publicznego profilu (jako Googlebot)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Tytuł
        title = soup.find("title")
        title_text = title.string.strip() if title and title.string else "Brak tytułu"

        # Opis (Open Graph / meta)
        description = ""
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            description = og_desc["content"]
        else:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                description = meta_desc["content"]
        if not description:
            description = "Brak opisu"

        # Zdjęcie profilowe (Open Graph)
        image_url = ""
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image_url = og_image["content"]

        domain = urlparse(url).netloc

        return {
            "url": url,
            "domain": domain,
            "title": title_text,
            "description": description[:500],
            "image_url": image_url,
            "status_code": response.status_code,
        }
    except Exception as e:
        logging.error(f"Błąd pobierania {url}: {e}")
        return {
            "url": url,
            "domain": "Błąd",
            "title": "Błąd pobierania",
            "description": str(e),
            "image_url": "",
            "status_code": 0,
        }

def generate_report(data: dict) -> str:
    report = []
    report.append(f"🔗 **Analiza profilu**")
    report.append(f"🌐 **Domena:** {data['domain']}")
    report.append(f"📄 **Tytuł:** {data['title']}")
    report.append(f"📝 **Opis:** {data['description']}")
    report.append(f"📊 **Status HTTP:** {data['status_code']}")
    if data['image_url']:
        report.append(f"🖼️ **Zdjęcie:** {data['image_url']}")
    return "\n".join(report)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Wyślij link do publicznego profilu, a przeanalizuję go.\n"
        "Działam jak Googlebot – pobieram tylko publiczne dane."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not is_valid_url(text):
        await update.message.reply_text("❌ To nie wygląda na poprawny link.")
        return

    await update.message.reply_text("⏳ Analizuję profil...")
    data = fetch_profile_data(text)
    report = generate_report(data)

    if data.get("image_url"):
        try:
            img_response = requests.get(data["image_url"], timeout=5)
            if img_response.status_code == 200:
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    tmp.write(img_response.content)
                    tmp_path = tmp.name
                await update.message.reply_photo(
                    photo=InputFile(tmp_path),
                    caption=report,
                    parse_mode="Markdown"
                )
                os.unlink(tmp_path)
                return
        except Exception as e:
            logging.warning(f"Nie udało się pobrać zdjęcia: {e}")

    await update.message.reply_text(report, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Wyślij link do publicznego profilu.\n"
        "Bot zwróci tytuł, opis, zdjęcie i status HTTP."
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
