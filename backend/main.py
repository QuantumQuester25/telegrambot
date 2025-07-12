import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in your .env as your public URL + "/webhook"

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN or WEBHOOK_URL not set in environment.")

app = Flask(__name__)
loop = asyncio.get_event_loop()

telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 /start command received!")
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Open Gem Hunters", web_app=WebAppInfo(url="https://telegrambot2797.vercel.app"))]]
    )
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

telegram_app.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("Webhook received data:", data)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.run_sync(telegram_app.process_update(update))  # Run synchronously
    return "ok", 200



# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

# ✅ Set webhook during startup
async def setup():
    print("🔄 Initializing Telegram bot + webhook")
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ Bot initialized and webhook set")

loop.run_until_complete(setup())

# Gunicorn entry
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
