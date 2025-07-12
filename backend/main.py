import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Load bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Telegram bot application
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Define a command handler (e.g., /start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm alive and running on Render! 🚀")

# Add handler to the application
telegram_app.add_handler(CommandHandler("start", start))

# Create Flask app
app = Flask(__name__)

# Route to receive Telegram webhooks
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok", 200
