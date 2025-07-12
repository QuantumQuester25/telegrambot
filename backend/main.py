import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Load environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables.")

# Build Telegram application
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Define bot command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🚀 Open Gem Hunters",
            web_app=WebAppInfo(url="https://telegrambot2797.vercel.app")
        )]
    ])
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

telegram_app.add_handler(CommandHandler("start", start))

# Create Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is live!", 200

# Webhook setup route
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://telegrambot-production-a0ac.up.railway.app/webhook/{BOT_TOKEN}"
    asyncio.run(telegram_app.bot.set_webhook(webhook_url))
    return f"Webhook set to: {webhook_url}", 200

# Webhook receiver
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok", 200
