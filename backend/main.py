import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create Telegram application
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command with Mini App button
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

# Register webhook once when app starts
@app.before_first_request
def set_webhook():
    webhook_url = f"https://your-render-url.onrender.com/webhook/{BOT_TOKEN}"
    asyncio.get_event_loop().create_task(
        telegram_app.bot.set_webhook(webhook_url)
    )

# Handle webhook POST request
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok", 200
