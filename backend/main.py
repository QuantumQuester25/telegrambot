import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in .env")

# Flask app
app = Flask(__name__)
loop = asyncio.get_event_loop()

# Create Telegram Application
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# Ensure initialization only once
initialized = False

# Telegram /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(
        text="🚀 Open Gem Hunters",
        web_app=WebAppInfo(url="https://telegrambot2797.vercel.app")
    )]])
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

# Add command handler
telegram_app.add_handler(CommandHandler("start", start))

# Run initialization before first request
@app.before_request
def init_bot():
    global initialized
    if not initialized:
        loop.create_task(telegram_app.initialize())
        initialized = True

# Root test route
@app.route("/", methods=["GET"])
def root():
    return "Bot is live!", 200

# Health check route
@app.route("/health", methods=["GET"])
def health():
    return "Healthy ✅", 200

# Webhook setup route
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    async def hook():
        await telegram_app.initialize()
        webhook_url = f"https://telegrambot-production-39fd.up.railway.app/webhook/{BOT_TOKEN}"
        await telegram_app.bot.set_webhook(webhook_url)
        return f"Webhook set to: {webhook_url}", 200

    return loop.run_until_complete(hook())

# Webhook endpoint
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    loop.create_task(telegram_app.process_update(update))
    return "ok", 200
