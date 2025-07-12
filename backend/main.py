from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Example command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from webhook!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def index():
    return "Telegram bot is running!"

# Set webhook when deployed (e.g., from another script or manually)
