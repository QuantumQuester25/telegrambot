import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment.")

app = Flask(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Telegram bot application
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚀 Open Gem Hunters", web_app=WebAppInfo(url="https://telegrambot2797.vercel.app"))]]
    )
    await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)

telegram_app.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    loop.create_task(telegram_app.process_update(update))
    return "ok", 200

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

# Setup function for bot + webhook
def setup_bot():
    print("🔄 Initializing Telegram bot + webhook")
    loop.run_until_complete(telegram_app.initialize())
    loop.run_until_complete(telegram_app.bot.set_webhook("https://telegrambot-production-7130.up.railway.app/webhook"))
    print("✅ Bot initialized and webhook set")

# Launch setup in background thread on first Flask request
@app.before_request
def before_request():
    if not getattr(app, 'bot_ready', False):
        threading.Thread(target=setup_bot).start()
        app.bot_ready = True

# Start Flask
if __name__ == "__main__":
    print("🔥 Flask app starting")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
