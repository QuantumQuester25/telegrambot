import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")

app = Flask(__name__)
loop = asyncio.get_event_loop()

# Telegram bot application
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Open Gem Hunters", web_app=WebAppInfo(url="https://telegrambot2797.vercel.app"))]]
    )
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

telegram_app.add_handler(CommandHandler("start", start))

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

# Webhook route (Telegram sends updates here)
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    loop.create_task(telegram_app.process_update(update))
    return "ok", 200

# Set webhook endpoint (call once after deployment)
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    webhook_url = "https://telegrambot-production-7130.up.railway.app/webhook"
    loop.run_until_complete(telegram_app.bot.set_webhook(webhook_url))
    return f"Webhook set to: {webhook_url}", 200

# Initialize bot once at startup
def init_bot():
    print("🔄 Initializing Telegram bot...")
    loop.run_until_complete(telegram_app.initialize())
    print("✅ Telegram bot initialized.")

init_bot()

# Start Flask server
if __name__ == "__main__":
    print("🔥 Flask app starting")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
