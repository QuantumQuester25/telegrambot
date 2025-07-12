import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")

# Flask app
app = Flask(__name__)

# Telegram app
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# Event loop
loop = asyncio.get_event_loop()
bot_initialized = False  # prevent double init

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🚀 Open Gem Hunters", web_app=WebAppInfo(url="https://telegrambot2797.vercel.app"))
    ]])
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

telegram_app.add_handler(CommandHandler("start", start))

@app.before_request
def initialize_bot():
    global bot_initialized
    if not bot_initialized:
        print("🔄 Initializing bot...")
        loop.run_until_complete(telegram_app.initialize())
        loop.run_until_complete(telegram_app.start())  # ✅ Start the bot!
        bot_initialized = True
        print("✅ Bot initialized and started.")

@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://telegrambot-production-39fd.up.railway.app/webhook/{BOT_TOKEN}"
    loop.run_until_complete(telegram_app.bot.set_webhook(webhook_url))
    return f"Webhook set to: {webhook_url}", 200

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        loop.create_task(telegram_app.process_update(update))
        return "ok", 200
    except Exception as e:
        print("❌ Webhook error:", e)
        return "Internal Server Error", 500
