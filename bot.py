import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_SPACE = "Minhajul-islam/Report_Generation_from_Xrayimages"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🩺 *AI Radiology Report Generator*\n\n"
        "Send me a chest X-ray image and I will generate a detailed radiology report instantly!\n\n"
        "⚠️ For research purposes only. Not for clinical use.",
        parse_mode='Markdown'
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Analyzing your X-ray... please wait.")
    try:
        photo = update.message.photo[-1] if update.message.photo else update.message.document
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive("temp_xray.jpg")

        client = Client(HF_SPACE)
        result = client.predict(
            image="temp_xray.jpg",
            api_name="/generate_report"
        )

        await update.message.reply_text(
            f"🩺 *AI Radiology Report*\n\n{result}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_image))
    print("✅ Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
